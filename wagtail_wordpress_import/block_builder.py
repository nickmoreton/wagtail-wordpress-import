import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.module_loading import import_string
from wagtail.images.models import Image as ImportedImage

from wagtail_wordpress_import.block_builder_defaults import (
    conf_fallback_block,
    conf_html_tags_to_blocks,
)


def conf_promote_child_tags():
    return getattr(
        settings,
        "WAGTAIL_WORDPRESS_IMPORTER_PROMOTE_CHILD_TAGS",
        {
            "TAGS_TO_PROMOTE": ["iframe", "form", "blockquote"],
            "PARENTS_TO_REMOVE": ["p", "div", "span"],
        },
    )


# this is not what i'd expect to see but some images return text/html CDN maybe?
VALID_IMAGE_CONTENT_TYPES = [
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
    "text/html",
]

IMAGE_SRC_DOMAIN = "https://www.budgetsaresexy.com"  # note no trailing /


class BlockBuilder:
    def __init__(self, value, node, logger):
        self.soup = BeautifulSoup(value, "lxml")
        self.blocks = []  # for each page this holds the sequence of StreamBlocks
        self.logged_items = {"processed": 0, "imported": 0, "skipped": 0, "items": []}
        self.node = node
        self.logger = logger

    def promote_child_tags(self):
        """
        Some HTML tags that can be at the top level, e.g. the parent is the
        body when using BS4 are getting placed inside or existed inside other HTML tags.
        We pull out these HTML tags and move them to the top level.
        returns: None
            but modifies the page soup
        """
        config_promote_child_tags = conf_promote_child_tags()
        promotee_tags = config_promote_child_tags["TAGS_TO_PROMOTE"]
        removee_tags = config_promote_child_tags["PARENTS_TO_REMOVE"]

        for promotee in promotee_tags:
            promotees = self.soup.findAll(promotee)
            for promotee in promotees:
                if promotee.parent.name in removee_tags:
                    promotee.parent.replace_with(promotee)

    def get_builder_function(self, element):
        """
        params
            element: an HTML tag
        returns:
            a function to parse the block from configuration
        """
        function = [
            import_string(builder[1]["FUNCTION"])
            for builder in conf_html_tags_to_blocks()
            if element.name == builder[0]
        ]
        if function:
            return function[0]

    def build(self):
        """
        params:
            None
        returns:
            a list of block dicts

        The value to be processed her should have only top level HTML tags.
        The HTML is parsed to a sequence of StreamField blocks.
        If a HTML tag does have child blocks we should parse then inside the
        build_block_* method
        """
        soup = self.soup.find("body").findChildren(recursive=False)
        cached_fallback_value = (
            ""  # keep appending fall back content here, by default is Rich Text block
        )
        cached_fallback_function = import_string(
            conf_fallback_block()
        )  # Rich Text block
        counter = 0
        for element in soup:  # each single top level tag
            counter += 1
            # the builder function for the element tag from config
            builder_function = self.get_builder_function(element)

            if builder_function:  # build a block
                if cached_fallback_value:
                    cached_fallback_value = cached_fallback_function(
                        cached_fallback_value,
                        self.blocks,
                    )  # before building a block write fall back cache to a block
                self.blocks.append(builder_function(element))  # write the new block
            else:
                if element.text.strip():  # exclude a tag that is empty
                    cached_fallback_value += str(element)

            if cached_fallback_value and counter == len(
                soup
            ):  # the last tag so just build whats left in the fall back cache
                cached_fallback_value = cached_fallback_function(
                    cached_fallback_value, self.blocks
                )

        return self.blocks

    def image_linker(self, tag):
        soup = BeautifulSoup(tag, "html.parser", exclude_encodings=True)
        images = soup.find_all("img")

        for image in images:
            image_saved = self.get_image(image)
            if image_saved:
                alignment = self.get_alignment_class(image)
                img_alt = image.attrs["alt"] if "alt" in image.attrs else None
                tag = '<embed embedtype="image" id="{}" alt="{}" format="{}" />'.format(
                    image_saved.id, img_alt, alignment
                )

        return tag

    def get_alignment_class(self, image):
        alignment = "fullwidth"

        if "class" in image.attrs:
            if "align-left" in image.attrs["class"]:
                alignment = "left"
            elif "align-right" in image.attrs["class"]:
                alignment = "right"

        return alignment

    def get_image(self, image):

        if image.get("src"):
            name = image.get("src").split("/")[-1]  # need the last part
            temp = NamedTemporaryFile(delete=True)
            image_src = check_image_src(image.get("src")).strip("/")
        else:
            self.logged_items["items"].append(
                {
                    "id": self.node.get("wp:post_id"),
                    "title": self.node.get("title"),
                    "link": self.node.get("link"),
                    "reason": "no src provided",
                }
            )
            self.logger.images.append(
                {
                    "id": self.node.get("wp:post_id"),
                    "title": self.node.get("title"),
                    "link": self.node.get("link"),
                    "reason": "no src provided",
                }
            )
            return

        try:
            image_exists = ImportedImage.objects.get(title=name)
            return image_exists

        except ImportedImage.DoesNotExist:

            try:
                response = requests.get(image_src, timeout=10)
                status_code = response.status_code
                content_type = response.headers.get("Content-Type")

                if (
                    content_type
                    and content_type.lower() not in VALID_IMAGE_CONTENT_TYPES
                ):
                    self.logged_items["items"].append(
                        {
                            "id": self.node.get("wp:post_id"),
                            "title": self.node.get("title"),
                            "link": self.node.get("link"),
                            "reason": "invalid image types match or no content type",
                        }
                    )
                    self.logger.images.append(
                        {
                            "id": self.node.get("wp:post_id"),
                            "title": self.node.get("title"),
                            "link": self.node.get("link"),
                            "reason": "invalid image types match or no content type",
                        }
                    )
                    return

                if status_code == 200:
                    temp.name = name
                    temp.write(response.content)
                    temp.flush()
                    new_image = ImportedImage(file=File(file=temp), title=name)
                    new_image.save()
                    return new_image

            except requests.exceptions.ConnectionError:
                self.logged_items["items"].append(
                    {
                        "id": self.node.get("wp:post_id"),
                        "title": self.node.get("title"),
                        "link": self.node.get("link"),
                        "reason": "connection error",
                    }
                )
                self.logger.images.append(
                    {
                        "id": self.node.get("wp:post_id"),
                        "title": self.node.get("title"),
                        "link": self.node.get("link"),
                        "reason": "connection error",
                    }
                )


def check_image_src(src):
    # some images have relative src values
    if not src.startswith("http"):
        print(
            "WARNING: relative file {}. Image may be broken, trying with domain name prepended. ".format(
                src
            )
        )
        return IMAGE_SRC_DOMAIN + "/" + src
    return src
