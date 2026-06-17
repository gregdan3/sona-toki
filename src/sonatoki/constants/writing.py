NOT_IN_PUNCT_CLASS = r"Ⓐ-ⓩ🄰-🅉🅐-🅩🅰-🆉"

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS
"""Commonly occurring strings which are some kind of valid Toki Pona or
external token."""
ALLOWABLES = {
    "anusem",  # clipping of anu seme
    "ansem",  # clipping of anu seme
    "anse",  # clipping of anu seme
    "kxk",  # ken ala ken
    "kx",  # ken ala
    "msa",  # mi sona ala
    "pon",  # pona
    # these may be short enough to be an issue
    # but if they aren't included here, they'll get a zero...
    "tp",  # toki pona
    "sp",  # sina pona, sitelen pona
    "tpt",  # toki pona taso
    "wxw",  # wile ala wile
    "wx",  # wile ala
    "mptp",  # ma pona pi toki pona
    "stln",  # sitelen
    "stpn",  # sitelen pona
    "tptpt",  # tenpo pi toki pona taso
}
JUNKABLES = {
    # Strings which don't obviously belong to any specific language,
    # or which are frequently involved in non-language sequences.
    # Single letters ordered by frequency in ilo Muni as of 2025-10-20.
    # "e",
    # "a",
    # "o",
    # "n",
    # "i"
    "x",  # ala, emoticons
    "p",  # mi, emoticons
    # "s",
    # "j",
    # "u",
    "y",  # seme, rare emoticons
    # "b",
    # "c",
    # "m",
    # "w",
    "d",  # emoticons
    # "r",
    # "l",
    "k",  # ken
    # "h"
    # "t",
    # "v",
    # "f",
    # "z",
    # "g",
    # "q",
}
