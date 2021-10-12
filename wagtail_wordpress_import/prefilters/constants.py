# *****************************
# USED BY filter_fix_styles() *
# *****************************
HTML_TAGS = {
    "address": "block",
    "article": "block",
    "aside": "block",
    "blockquote": "block",
    "canvas": "block",
    "dd": "block",
    "div": "block",
    "dl": "block",
    "dt": "block",
    "fieldset": "block",
    "figcaption": "block",
    "figure": "block",
    "footer": "block",
    "form": "block",
    "h1": "block",
    "h2": "block",
    "h3": "block",
    "h4": "block",
    "h5": "block",
    "h6": "block",
    "header": "block",
    "hr": "block",
    "li": "block",
    "main": "block",
    "nav": "block",
    "noscript": "block",
    "ol": "block",
    "p": "block",
    "pre": "block",
    "section": "block",
    "table": "block",
    "tfoot": "block",
    "ul": "block",
    "video": "block",
    "a": "inline",
    "abbr": "inline",
    "acronym": "inline",
    "b": "inline",
    "bdo": "inline",
    "big": "inline",
    "br": "inline",
    "button": "inline",
    "center": "inline",  # not stricty allowed but here for later styling
    "cite": "inline",
    "code": "inline",
    "dfn": "inline",
    "em": "inline",
    "i": "inline",
    "img": "inline",
    "input": "inline",
    "kbd": "inline",
    "label": "inline",
    "map": "inline",
    "object": "inline",
    "output": "inline",
    "q": "inline",
    "samp": "inline",
    "script": "inline",
    "select": "inline",
    "small": "inline",
    "span": "inline",
    "strong": "inline",
    "sub": "inline",
    "sup": "inline",
    "textarea": "inline",
    "time": "inline",
    "tt": "inline",
    "var": "inline",
}


FILTER_MAPPING = {
    "bold": [
        # transform to <b></b>
        "font-weight:bold;",
    ],
    "italic": [
        # transform to <i></i>
        "font-style:italic;",
    ],
    "bold-italic": [
        # transform to <b><i></i></b>
        "font-style:italic; font-weight:bold;",
        "font-weight:bold; font-style:italic;",
    ],
    "center": [
        # add class align-center
        "text-align:center",
    ],
    "leftfloat": [
        # add class float-left
        "float:left;"
    ],
    "rightfloat": [
        # add class float-right
        "float:right;",
    ],
    "remove": [
        # remove style tag completely
        "font-weight:400;",
        "font-weight:normal;",
    ],
}


# ****************
# USED BY filter_bleach_clean() *
# ****************
ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "aside",
    "b",
    "blockquote",
    "br",
    "button",
    "caption",
    "center",  # not stictly allowed but we convert id later to css on a div
    "code",
    "col",
    "colgroup",
    "del",
    "div",
    "em",
    "footer",
    "form",
    "figure",
    "figcaption",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "iframe",
    "img",
    "input",
    "label",
    "li",
    "ol",
    "option",
    "p",
    "s",
    "script",
    "select",
    "small",
    "span",
    "strike",
    "strong",
    "style",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "time",
    "tr",
    "u",
    "ul",
    "wbr",
]


ALLOWED_ATTRIBUTES = {
    "*": ["class", "style", "id"],
    "a": [
        "aria-label",
        "data-wplink-edit",
        "href",
        "rel",
        "target",
        "title",
        "data-uw-rm-brl",
        "data-saferedirecturl",
        "name",
    ],
    "abbr": ["title"],
    "acronym": ["title"],
    "blockquote": [
        "data-cards",
        "data-lang",
        "data-instgrm-permalink",
        "data-instgrm-version",
        "data-instgrm-captioned",
    ],
    "button": ["data-target", "data-toggle"],
    "col": ["width"],
    "div": [
        "title",
        "data-campaign",
        "data-widget-id",
        "data-offer-id",
        "data-aff-id",
        "data-sub-id",
        "data-color",
        "role",
        "data-mm-rates",
    ],
    "form": ["action", "name", "method", "accept-charset"],
    "h2": ["big", "data-toctitle", "data-tocskip", "data-toskip", "data-toc-title"],
    "h3": ["data-toctitle", "data-tocskip"],
    "i": [
        "aria-hidden",
        "data-toggle",
        "data-placement",
        "title",
        "data-original-title",
    ],
    "iframe": [
        "allowfullscreen",
        "src",
        "width",
        "height",
        "frameborder",
        "scrolling",
        "marginwidth",
        "marginheight",
        "data-mce-fragment",
        "data-name",
        "data-link",
    ],
    "img": [
        "alt",
        "border",
        "data-src",
        "height",
        "sizes",
        "src",
        "srcset",
        "title",
        "width",
    ],
    "input": [
        "name",
        "placeholder",
        "readonly",
        "required",
        "type",
        "min",
        "max",
        "step",
        "value",
        "data-type",
    ],
    "label": ["for"],
    "li": ["aria-level", "value", "data-uw-node-idx"],
    "ol": ["data-mm-title", "start"],
    "option": ["data-desc", "data-option", "value", "selected"],
    "p": ["dir", "lang", "data-tocskip", "data-toctitle", "data-mm-rates"],
    "script": ["async", "charset", "defer", "src", "type"],
    "select": ["name"],
    "span": [
        "aria-invalid",
        "data-reactid",
        "data-preserver-spaces",
        "data-mm-rates",
    ],
    "style": ["*"],
    "table": ["width", "dir", "border", "cellspacing", "cellpadding", "summary"],
    "tbody": ["data-mm-rates"],
    "td": [
        "data-label",
        "width",
        "colspan",
        "data-sheets-value",
        "data-sheets-numberformat",
        "data-sheets-formula",
        "data-sheets-hyperlink",
        "rowspan",
    ],
    "th": ["width", "scope", "colspan", "rowspan"],
    "time": ["datetime"],
    "ul": ["data-mm-title", "data-mm-rates"],
}


ALLOWED_STYLES = [
    "font-size",
    "font-weight",
    "font-style: italic;",
    "font-style",
    "text-align: center",
    "text-align: center;",
]
