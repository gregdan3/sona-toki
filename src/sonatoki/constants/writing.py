NOT_IN_PUNCT_CLASS = r"Ⓐ-ⓩ🄰-🅉🅐-🅩🅰-🆉"

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS
"""Commonly occurring strings which are some kind of valid Toki Pona or
external token."""
ALLOWABLES = {
    # "x",  # ala
    # "y",  # anu
    "kxk",  # ken ala ken
    "wxw",  # wile ala wile
    "msa",
    "anusem",
    "pon",  # pona
}
