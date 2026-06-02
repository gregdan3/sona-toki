# LOCAL
from sonatoki.utils import find_unicode_chars

UCSUR_RANGES = [
    "\\U000F1900-\\U000F1977",  # pu
    "\\U000F1978-\\U000F1988",  # ku suli
    "\\U000F1989-\\U000F198B",  # ni directions
    "\\U000F198C",  # secular sewi
    "\\U000F19A0-\\U000F19A3",  # ku lili
    "\\U000F19A4-\\U000F19BA",  # everything else
]

UCSUR_SENTENCE_PUNCT = """󱦜󱦝"""

UCSUR_PUNCT_RANGES = ["\\U000f1990-\\U000f199d"]
UCSUR_PUNCT_RANGES_STR = "".join(UCSUR_PUNCT_RANGES)
"""Private Use Area glyphs are given the apt but unhelpful 'Private Use'
class."""

UCSUR_CARTOUCHE_LEFT = "󱦐"
UCSUR_CARTOUCHE_RIGHT = "󱦑"

NIMI_UCSUR = find_unicode_chars(UCSUR_RANGES)
ALL_UCSUR = NIMI_UCSUR + find_unicode_chars(UCSUR_PUNCT_RANGES)
UCSUR_MINUS_CARTOUCHE = set(ALL_UCSUR).difference(
    {UCSUR_CARTOUCHE_LEFT, UCSUR_CARTOUCHE_RIGHT}
)
# NIMI_PU_UCSUR_RANGES = ["\\U000F1900-\\U000F1977"]
# NIMI_PU_ALE_UCSUR_RANGES = NIMI_PU_UCSUR_RANGES + ["\\U000F1978-\\U000F197A"]
