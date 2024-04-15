# STL
import json
from typing import List
from pathlib import Path

LINKU = Path(__file__).resolve().parent / Path("linku.json")

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS
ALPHABET_SET = set(ALPHABET)


with open(LINKU) as f:
    r = json.loads(f.read())
    NIMI_PU: List[str] = [d["word"] for d in r.values() if d["book"] == "pu"]
    NIMI_LINKU: List[str] = [
        d["word"] for d in r.values() if d["usage_category"] in ["core", "common"]
    ]

NIMI_PU_SET = set(NIMI_PU)
NIMI_LINKU_SET = set(NIMI_LINKU)

__all__ = [
    "VOWELS",
    "CONSONANTS",
    "ALPHABET",
    "ALPHABET_SET",
    "NIMI_PU",
    "NIMI_PU_SET",
    "NIMI_LINKU",
    "NIMI_LINKU_SET",
]
