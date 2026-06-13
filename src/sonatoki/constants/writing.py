NOT_IN_PUNCT_CLASS = r"Ⓐ-ⓩ🄰-🅉🅐-🅩🅰-🆉"

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS
"""Commonly occurring strings which are some kind of valid Toki Pona or
external token."""
ALLOWABLES = {
    "anusem",  # clipping of anu seme
    "kxk",  # ken ala ken
    "msa",  # mi sona ala
    "pon",  # pona
    # these may be short enough to be an issue
    # but if they aren't included here, they'll get a zero...
    "tp",  # toki pona
    "sp",  # sina pona, sitelen pona
    "tpt",  # toki pona taso
    "wxw",  # wile ala wile
    "mptp",  # ma pona pi toki pona
}
