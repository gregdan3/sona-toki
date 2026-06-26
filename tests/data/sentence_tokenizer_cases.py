# LOCAL
from tests.data.types import Transform

CASES = [
    Transform("mu. mu.", ["mu.", "mu."], False, name="basic1"),
    Transform("mu! mu!", ["mu!", "mu!"], False, name="basic2"),
    Transform("mu? mu?", ["mu?", "mu?"], False, name="basic3"),
    Transform("mi mu. mi wawa.", ["mi mu.", "mi wawa."], False, name="basic4"),
    Transform("", [], False, name="empty"),
    Transform("  \n  ", [], False, name="whitespace"),
    Transform(
        "sina lon seme?\nmi wile lon poka...\n",
        ["sina lon seme?", "mi wile lon poka.", ".", "."],
        False,
        name="newline basic",
    ),
    Transform(
        "sina lon seme\nmi wile lon poka",
        ["sina lon seme", "mi wile lon poka"],
        False,
        name="newline alone",
    ),
    Transform(
        "mi sona ala e ni- sina seme a",
        ["mi sona ala e ni-", "sina seme a"],
        False,
        name="dash",
    ),
    Transform(
        "mi mu tawa sina, mi wawa e sina.",
        ["mi mu tawa sina, mi wawa e sina."],
        False,
        name="comma",
    ),
    Transform(
        "toki li tan kulupu Kuko li ni: 'o ike ala!'",
        ["toki li tan kulupu Kuko li ni:", "'o ike ala!", "'"],
        False,
        name="singlequotes",
    ),
    Transform(
        'ona li toki e ni: "mama sina"',
        ["ona li toki e ni:", '"mama sina"'],
        False,
        name="doublequotes",
    ),
    Transform(
        'this is a bit dumb, right? they said "where is the pacific ocean?"',
        ["this is a bit dumb, right?", 'they said "where is the pacific ocean?', '"'],
        False,
        name="doublequotes 2",
    ),
    Transform(
        'they said "wow, its made"',
        ['they said "wow, its made"'],
        False,
        name="doublequotes 3",
    ),
    Transform(
        "||...||",
        ["||.", ".", ".", "||"],
        False,
        name="mixed periods spoilers",
    ),
    Transform("h..", ["h.", "."], False, name="trailing periods"),
    Transform("h.!", ["h.", "!"], False, name="trailing periods 2"),
    Transform(
        "e.g. monsuta",
        ["e.g.", "monsuta"],
        False,
        name="intraword punctuation 1",
    ),
    Transform(
        "isn't that game-breaking? i think so",
        ["isn't that game-breaking?", "i think so"],
        False,
        name="intraword punctuation 2",
    ),
    Transform(
        "e.g.\n- monsuta\n- monsi\n- ma",
        ["e.g.", "-", "monsuta", "-", "monsi", "-", "ma"],
        False,
        name="intraword punctuation 3",
    ),
    Transform(
        "look at this variable: leaf_node_right",
        ["look at this variable:", "leaf_node_right"],
        False,
        name="intraword punctuation 4",
    ),
    Transform(
        "toki! sitelen pini ni li tu ala e toki. ni kin. taso ni li pini e toki anu seme: pini la ni li toki sin.\n",
        [
            "toki!",
            "sitelen pini ni li tu ala e toki.",
            "ni kin.",
            "taso ni li pini e toki anu seme:",
            "pini la ni li toki sin.",
        ],
        False,
        name="multiline with fake intraword",
    ),
    Transform("!.h", ["!", ".", "h"], False, name="fake intraword punct 1"),
    Transform(
        "life-altering\u2003pseudo-science.\u2003and\u2003non-sense",
        ["life-altering\u2003pseudo-science.", "and\u2003non-sense"],
        False,
        name="full width space",
    ),
    Transform(
        "ona li ken lukin e sitelen [_ike_nanpa_lete_ike]. ni li pona kin.",
        [
            "ona li ken lukin e sitelen [",
            "_ike_nanpa_lete_ike]",
            ".",
            "ni li pona kin.",
        ],
        False,
        name="discovered case 1",
    ),
    Transform(
        "👨\u200d👩\u200d👧\u200d👧",
        ["👨\u200d👩\u200d👧\u200d👧"],
        False,
        name="zwj in emoji",
    ),
    Transform(
        "\U000f1944\U000f196c\U000f1969\U000f1934\U000f199c\U000f1944\U000f196c\U000f1969\U000f1934",
        [
            "\U000f1944\U000f196c\U000f1969\U000f1934\U000f199c",
            "\U000f1944\U000f196c\U000f1969\U000f1934",
        ],
        False,
        name="UCSUR 1",
    ),
    Transform(
        "\U000f1934\U000f193a\U000f1990\U000f1918\U000f199c\U000f1915\U000f199c\U000f193e\U000f1991\U000f1990\U000f193c\U000f199d\U000f1991",
        [
            "\U000f1934\U000f193a\U000f1990\U000f1918\U000f199c",
            "\U000f1915\U000f199c",
            "\U000f193e\U000f1991\U000f1990\U000f193c\U000f199d",
            "\U000f1991",
        ],
        True,
        name="UCSUR 2 (original)",
    ),
    Transform(
        "\U000f1934\U000f193a\U000f1990\U000f1918\U000f199c\U000f1915\U000f199c\U000f193e\U000f1991\U000f1990\U000f193c\U000f199d\U000f1991",
        [
            "\U000f1934\U000f193a\U000f1990\U000f1918\U000f199c\U000f1915\U000f199c\U000f193e\U000f1991\U000f1990\U000f193c\U000f199d\U000f1991"
        ],
        False,
        name="UCSUR 2 (preferred)",
    ),
    Transform(
        "\U000f1934\U000f1990\U000f1991\U000f1990\U000f1991",
        ["\U000f1934\U000f1990\U000f1991\U000f1990\U000f1991"],
        False,
        name="UCSUR 3",
    ),
    Transform(
        "\U000f1934\U000f1990\U000f1990",
        ["\U000f1934\U000f1990\U000f1990"],
        False,
        name="UCSUR 4",
    ),
    Transform(
        "\U000f1991\U000f1934\U000f1990\U000f1990",
        ["\U000f1991\U000f1934\U000f1990\U000f1990"],
        False,
        name="UCSUR 5",
    ),
    Transform(
        "\U000f1990nvidia shield. and other nvidia products.\U000f1991",
        ["\U000f1990nvidia shield.", "and other nvidia products.", "\U000f1991"],
        False,
        name="UCSUR 6",
    ),
    Transform(
        "\U000f1934\U000f193a\U000f1990\U000f1918\U000f199c\U000f1990\U000f1915\U000f1990\U000f199c\U000f193e\U000f1991\U000f1990\U000f193c\U000f199d\U000f1991",
        [
            "\U000f1934\U000f193a\U000f1990\U000f1918\U000f199c",
            "\U000f1990\U000f1915\U000f1990\U000f199c\U000f193e\U000f1991\U000f1990\U000f193c\U000f199d\U000f1991",
        ],
        False,
        name="UCSUR 7",
    ),
    Transform(
        "\U000f1934\U000f193a\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f199d\U000f1991",
        [
            "\U000f1934\U000f193a\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f1990\U000f199d\U000f1991"
        ],
        False,
        name="UCSUR 8",
    ),
    Transform(
        "\U000f193f\U000f1941\U000f1927\U000f1954\u200d\U000f1963",
        ["\U000f193f\U000f1941\U000f1927\U000f1954\u200d\U000f1963"],
        False,
        name="UCSUR 9",
    ),
    Transform(
        "\U000f1934\u200b\U000f194c\u200b\U000f1909\u200b\U000f1961\u200b\U000f194d\u200b\U000f196c\u200b\U000f1954\u200b\U000f1969\u200b\U000f1931\u200b\U000f1934",
        [
            "\U000f1934\u200b\U000f194c\u200b\U000f1909\u200b\U000f1961\u200b\U000f194d\u200b\U000f196c\u200b\U000f1954\u200b\U000f1969\u200b\U000f1931\u200b\U000f1934"
        ],
        False,
        name="UCSUR 10",
    ),
    Transform(
        "\U000f196c\u200d\U000f1954\u200b\U000f196c\U000f1995\U000f1954",
        ["\U000f196c\u200d\U000f1954\u200b\U000f196c\U000f1995\U000f1954"],
        False,
        name="UCSUR 11",
    ),
]
