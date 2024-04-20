# STL
import json
from typing import Dict, List
from pathlib import Path

LINKU = Path(__file__).resolve().parent / Path("linku.json")

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS
ALPHABET_SET = set(ALPHABET)

"""Commonly occurring strings which are some kind of valid Toki Pona or external token"""
ALLOWABLES = {
    "cw",  # Content Warning
    "x",  # ala
    "y",  # anu
    "kxk",  # ken ala ken
    "wxw",  # wile ala wile
}


with open(LINKU) as f:
    r: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_PU: List[str] = [d["word"] for d in r.values() if d["book"] == "pu"]
    NIMI_PU_ALE: List[str] = NIMI_PU + ["namako", "kin", "oko"]
    NIMI_LINKU: List[str] = [
        d["word"] for d in r.values() if d["usage_category"] in ["core", "common"]
    ]
    NIMI_LINKU_ALE: List[str] = [d["word"] for d in r.values()]

NIMI_PU_SET = set(NIMI_PU)
NIMI_PU_ALE_SET = set(NIMI_PU_ALE)
NIMI_LINKU_SET = set(NIMI_LINKU)
NIMI_LINKU_ALE_SET = set(NIMI_LINKU_ALE)
ALLOWABLES_SET = set(ALLOWABLES)

__all__ = [
    "VOWELS",
    #
    "CONSONANTS",
    #
    "ALPHABET",
    "ALPHABET_SET",
    #
    "NIMI_PU",
    "NIMI_PU_SET",
    #
    "NIMI_PU_ALE",
    "NIMI_PU_ALE_SET",
    #
    "NIMI_LINKU",
    "NIMI_LINKU_SET",
    #
    "NIMI_LINKU_ALE",
    "NIMI_LINKU_ALE_SET",
]
