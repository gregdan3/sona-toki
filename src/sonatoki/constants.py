# STL
import json
from typing import Set, Dict, List
from pathlib import Path

# LOCAL
from sonatoki.utils import find_unicode_chars, find_unicode_ranges

# `\p{Punctuation}` character class
# https://www.compart.com/en/unicode/category
# https://unicode.org/Public/UNIDATA/UnicodeData.txt
# NOTE: WAY too large to store as a string of each char
UNICODE_PUNCT_RANGES = [
    "\\U00000021-\\U0000002f",
    "\\U0000003a-\\U00000040",
    "\\U0000005b-\\U00000060",
    "\\U0000007b-\\U0000007e",
    "\\U000000a1-\\U000000a9",
    "\\U000000ab-\\U000000ac",
    "\\U000000ae-\\U000000b1",
    "\\U000000b4",
    "\\U000000b6-\\U000000b8",
    "\\U000000bb",
    "\\U000000bf",
    "\\U000000d7",
    "\\U000000f7",
    "\\U000002c2-\\U000002c5",
    "\\U000002d2-\\U000002df",
    "\\U000002e5-\\U000002eb",
    "\\U000002ed",
    "\\U000002ef-\\U000002ff",
    "\\U00000375",
    "\\U0000037e",
    "\\U00000384-\\U00000385",
    "\\U00000387",
    "\\U000003f6",
    "\\U00000482",
    "\\U0000055a-\\U0000055f",
    "\\U00000589-\\U0000058a",
    "\\U0000058d-\\U0000058f",
    "\\U000005be",
    "\\U000005c0",
    "\\U000005c3",
    "\\U000005c6",
    "\\U000005f3-\\U000005f4",
    "\\U00000606-\\U0000060f",
    "\\U0000061b",
    "\\U0000061d-\\U0000061f",
    "\\U0000066a-\\U0000066d",
    "\\U000006d4",
    "\\U000006de",
    "\\U000006e9",
    "\\U000006fd-\\U000006fe",
    "\\U00000700-\\U0000070d",
    "\\U000007f6-\\U000007f9",
    "\\U000007fe-\\U000007ff",
    "\\U00000830-\\U0000083e",
    "\\U0000085e",
    "\\U00000888",
    "\\U00000964-\\U00000965",
    "\\U00000970",
    "\\U000009f2-\\U000009f3",
    "\\U000009fa-\\U000009fb",
    "\\U000009fd",
    "\\U00000a76",
    "\\U00000af0-\\U00000af1",
    "\\U00000b70",
    "\\U00000bf3-\\U00000bfa",
    "\\U00000c77",
    "\\U00000c7f",
    "\\U00000c84",
    "\\U00000d4f",
    "\\U00000d79",
    "\\U00000df4",
    "\\U00000e3f",
    "\\U00000e4f",
    "\\U00000e5a-\\U00000e5b",
    "\\U00000f01-\\U00000f17",
    "\\U00000f1a-\\U00000f1f",
    "\\U00000f34",
    "\\U00000f36",
    "\\U00000f38",
    "\\U00000f3a-\\U00000f3d",
    "\\U00000f85",
    "\\U00000fbe-\\U00000fc5",
    "\\U00000fc7-\\U00000fcc",
    "\\U00000fce-\\U00000fda",
    "\\U0000104a-\\U0000104f",
    "\\U0000109e-\\U0000109f",
    "\\U000010fb",
    "\\U00001360-\\U00001368",
    "\\U00001390-\\U00001399",
    "\\U00001400",
    "\\U0000166d-\\U0000166e",
    "\\U0000169b-\\U0000169c",
    "\\U000016eb-\\U000016ed",
    "\\U00001735-\\U00001736",
    "\\U000017d4-\\U000017d6",
    "\\U000017d8-\\U000017db",
    "\\U00001800-\\U0000180a",
    "\\U00001940",
    "\\U00001944-\\U00001945",
    "\\U000019de-\\U000019ff",
    "\\U00001a1e-\\U00001a1f",
    "\\U00001aa0-\\U00001aa6",
    "\\U00001aa8-\\U00001aad",
    "\\U00001b5a-\\U00001b6a",
    "\\U00001b74-\\U00001b7e",
    "\\U00001bfc-\\U00001bff",
    "\\U00001c3b-\\U00001c3f",
    "\\U00001c7e-\\U00001c7f",
    "\\U00001cc0-\\U00001cc7",
    "\\U00001cd3",
    "\\U00001fbd",
    "\\U00001fbf-\\U00001fc1",
    "\\U00001fcd-\\U00001fcf",
    "\\U00001fdd-\\U00001fdf",
    "\\U00001fed-\\U00001fef",
    "\\U00001ffd-\\U00001ffe",
    "\\U00002010-\\U00002027",
    "\\U00002030-\\U0000205e",
    "\\U0000207a-\\U0000207e",
    "\\U0000208a-\\U0000208e",
    "\\U000020a0-\\U000020c0",
    "\\U00002100-\\U00002101",
    "\\U00002103-\\U00002106",
    "\\U00002108-\\U00002109",
    "\\U00002114",
    "\\U00002116-\\U00002118",
    "\\U0000211e-\\U00002123",
    "\\U00002125",
    "\\U00002127",
    "\\U00002129",
    "\\U0000212e",
    "\\U0000213a-\\U0000213b",
    "\\U00002140-\\U00002144",
    "\\U0000214a-\\U0000214d",
    "\\U0000214f",
    "\\U0000218a-\\U0000218b",
    "\\U00002190-\\U00002426",
    "\\U00002440-\\U0000244a",
    "\\U0000249c-\\U000024b5",
    "\\U00002500-\\U00002775",
    "\\U00002794-\\U00002b73",
    "\\U00002b76-\\U00002b95",
    "\\U00002b97-\\U00002bff",
    "\\U00002ce5-\\U00002cea",
    "\\U00002cf9-\\U00002cfc",
    "\\U00002cfe-\\U00002cff",
    "\\U00002d70",
    "\\U00002e00-\\U00002e2e",
    "\\U00002e30-\\U00002e5d",
    "\\U00002e80-\\U00002e99",
    "\\U00002e9b-\\U00002ef3",
    "\\U00002f00-\\U00002fd5",
    "\\U00002ff0-\\U00002fff",
    "\\U00003001-\\U00003004",
    "\\U00003008-\\U00003020",
    "\\U00003030",
    "\\U00003036-\\U00003037",
    "\\U0000303d-\\U0000303f",
    "\\U0000309b-\\U0000309c",
    "\\U000030a0",
    "\\U000030fb",
    "\\U00003190-\\U00003191",
    "\\U00003196-\\U0000319f",
    "\\U000031c0-\\U000031e3",
    "\\U000031ef",
    "\\U00003200-\\U0000321e",
    "\\U0000322a-\\U00003247",
    "\\U00003250",
    "\\U00003260-\\U0000327f",
    "\\U0000328a-\\U000032b0",
    "\\U000032c0-\\U000033ff",
    "\\U00004dc0-\\U00004dff",
    "\\U0000a490-\\U0000a4c6",
    "\\U0000a4fe-\\U0000a4ff",
    "\\U0000a60d-\\U0000a60f",
    "\\U0000a673",
    "\\U0000a67e",
    "\\U0000a6f2-\\U0000a6f7",
    "\\U0000a700-\\U0000a716",
    "\\U0000a720-\\U0000a721",
    "\\U0000a789-\\U0000a78a",
    "\\U0000a828-\\U0000a82b",
    "\\U0000a836-\\U0000a839",
    "\\U0000a874-\\U0000a877",
    "\\U0000a8ce-\\U0000a8cf",
    "\\U0000a8f8-\\U0000a8fa",
    "\\U0000a8fc",
    "\\U0000a92e-\\U0000a92f",
    "\\U0000a95f",
    "\\U0000a9c1-\\U0000a9cd",
    "\\U0000a9de-\\U0000a9df",
    "\\U0000aa5c-\\U0000aa5f",
    "\\U0000aa77-\\U0000aa79",
    "\\U0000aade-\\U0000aadf",
    "\\U0000aaf0-\\U0000aaf1",
    "\\U0000ab5b",
    "\\U0000ab6a-\\U0000ab6b",
    "\\U0000abeb",
    "\\U0000fb29",
    "\\U0000fbb2-\\U0000fbc2",
    "\\U0000fd3e-\\U0000fd4f",
    "\\U0000fdcf",
    "\\U0000fdfc-\\U0000fdff",
    "\\U0000fe10-\\U0000fe19",
    "\\U0000fe30-\\U0000fe52",
    "\\U0000fe54-\\U0000fe66",
    "\\U0000fe68-\\U0000fe6b",
    "\\U0000ff01-\\U0000ff0f",
    "\\U0000ff1a-\\U0000ff20",
    "\\U0000ff3b-\\U0000ff40",
    "\\U0000ff5b-\\U0000ff65",
    "\\U0000ffe0-\\U0000ffe6",
    "\\U0000ffe8-\\U0000ffee",
    "\\U0000fffc-\\U0000fffd",
    "\\U00010100-\\U00010102",
    "\\U00010137-\\U0001013f",
    "\\U00010179-\\U00010189",
    "\\U0001018c-\\U0001018e",
    "\\U00010190-\\U0001019c",
    "\\U000101a0",
    "\\U000101d0-\\U000101fc",
    "\\U0001039f",
    "\\U000103d0",
    "\\U0001056f",
    "\\U00010857",
    "\\U00010877-\\U00010878",
    "\\U0001091f",
    "\\U0001093f",
    "\\U00010a50-\\U00010a58",
    "\\U00010a7f",
    "\\U00010ac8",
    "\\U00010af0-\\U00010af6",
    "\\U00010b39-\\U00010b3f",
    "\\U00010b99-\\U00010b9c",
    "\\U00010ead",
    "\\U00010f55-\\U00010f59",
    "\\U00010f86-\\U00010f89",
    "\\U00011047-\\U0001104d",
    "\\U000110bb-\\U000110bc",
    "\\U000110be-\\U000110c1",
    "\\U00011140-\\U00011143",
    "\\U00011174-\\U00011175",
    "\\U000111c5-\\U000111c8",
    "\\U000111cd",
    "\\U000111db",
    "\\U000111dd-\\U000111df",
    "\\U00011238-\\U0001123d",
    "\\U000112a9",
    "\\U0001144b-\\U0001144f",
    "\\U0001145a-\\U0001145b",
    "\\U0001145d",
    "\\U000114c6",
    "\\U000115c1-\\U000115d7",
    "\\U00011641-\\U00011643",
    "\\U00011660-\\U0001166c",
    "\\U000116b9",
    "\\U0001173c-\\U0001173f",
    "\\U0001183b",
    "\\U00011944-\\U00011946",
    "\\U000119e2",
    "\\U00011a3f-\\U00011a46",
    "\\U00011a9a-\\U00011a9c",
    "\\U00011a9e-\\U00011aa2",
    "\\U00011b00-\\U00011b09",
    "\\U00011c41-\\U00011c45",
    "\\U00011c70-\\U00011c71",
    "\\U00011ef7-\\U00011ef8",
    "\\U00011f43-\\U00011f4f",
    "\\U00011fd5-\\U00011ff1",
    "\\U00011fff",
    "\\U00012470-\\U00012474",
    "\\U00012ff1-\\U00012ff2",
    "\\U00016a6e-\\U00016a6f",
    "\\U00016af5",
    "\\U00016b37-\\U00016b3f",
    "\\U00016b44-\\U00016b45",
    "\\U00016e97-\\U00016e9a",
    "\\U00016fe2",
    "\\U0001bc9c",
    "\\U0001bc9f",
    "\\U0001cf50-\\U0001cfc3",
    "\\U0001d000-\\U0001d0f5",
    "\\U0001d100-\\U0001d126",
    "\\U0001d129-\\U0001d164",
    "\\U0001d16a-\\U0001d16c",
    "\\U0001d183-\\U0001d184",
    "\\U0001d18c-\\U0001d1a9",
    "\\U0001d1ae-\\U0001d1ea",
    "\\U0001d200-\\U0001d241",
    "\\U0001d245",
    "\\U0001d300-\\U0001d356",
    "\\U0001d6c1",
    "\\U0001d6db",
    "\\U0001d6fb",
    "\\U0001d715",
    "\\U0001d735",
    "\\U0001d74f",
    "\\U0001d76f",
    "\\U0001d789",
    "\\U0001d7a9",
    "\\U0001d7c3",
    "\\U0001d800-\\U0001d9ff",
    "\\U0001da37-\\U0001da3a",
    "\\U0001da6d-\\U0001da74",
    "\\U0001da76-\\U0001da83",
    "\\U0001da85-\\U0001da8b",
    "\\U0001e14f",
    "\\U0001e2ff",
    "\\U0001e95e-\\U0001e95f",
    "\\U0001ecac",
    "\\U0001ecb0",
    "\\U0001ed2e",
    "\\U0001eef0-\\U0001eef1",
    "\\U0001f000-\\U0001f02b",
    "\\U0001f030-\\U0001f093",
    "\\U0001f0a0-\\U0001f0ae",
    "\\U0001f0b1-\\U0001f0bf",
    "\\U0001f0c1-\\U0001f0cf",
    "\\U0001f0d1-\\U0001f0f5",
    "\\U0001f10d-\\U0001f12f",
    "\\U0001f14a-\\U0001f14f",
    "\\U0001f16a-\\U0001f16f",
    "\\U0001f18a-\\U0001f1ad",
    "\\U0001f1e6-\\U0001f202",
    "\\U0001f210-\\U0001f23b",
    "\\U0001f240-\\U0001f248",
    "\\U0001f250-\\U0001f251",
    "\\U0001f260-\\U0001f265",
    "\\U0001f300-\\U0001f6d7",
    "\\U0001f6dc-\\U0001f6ec",
    "\\U0001f6f0-\\U0001f6fc",
    "\\U0001f700-\\U0001f776",
    "\\U0001f77b-\\U0001f7d9",
    "\\U0001f7e0-\\U0001f7eb",
    "\\U0001f7f0",
    "\\U0001f800-\\U0001f80b",
    "\\U0001f810-\\U0001f847",
    "\\U0001f850-\\U0001f859",
    "\\U0001f860-\\U0001f887",
    "\\U0001f890-\\U0001f8ad",
    "\\U0001f8b0-\\U0001f8b1",
    "\\U0001f900-\\U0001fa53",
    "\\U0001fa60-\\U0001fa6d",
    "\\U0001fa70-\\U0001fa7c",
    "\\U0001fa80-\\U0001fa88",
    "\\U0001fa90-\\U0001fabd",
    "\\U0001fabf-\\U0001fac5",
    "\\U0001face-\\U0001fadb",
    "\\U0001fae0-\\U0001fae8",
    "\\U0001faf0-\\U0001faf8",
    "\\U0001fb00-\\U0001fb92",
    "\\U0001fb94-\\U0001fbca",
    "\\U000f1990-\\U000f199d",  # UCSUR punctuation
]

UCSUR_PUNCT_RANGES = UNICODE_PUNCT_RANGES[-1]  # NOTE: THIS CAN CHANGE

UNICODE_PUNCT = find_unicode_chars(UNICODE_PUNCT_RANGES)
# this is a large string.

# `\p{posix_punct}` character class
POSIX_PUNCT = r"""-!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""
POSIX_PUNCT_RANGES = find_unicode_ranges(POSIX_PUNCT)

ALL_PUNCT = "".join(sorted(list(set(POSIX_PUNCT + UNICODE_PUNCT))))
ALL_PUNCT_RANGES = "".join(find_unicode_ranges(ALL_PUNCT))
# combined bc the result could be simpler

SENTENCE_PUNCT = """.?!:;'"()[-]“”·…"""


LINKU = Path(__file__).resolve().parent / Path("linku.json")
SANDBOX = Path(__file__).resolve().parent / Path("sandbox.json")

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS

LANGUAGE = "english"  # for NLTK
"""Commonly occurring strings which are some kind of valid Toki Pona or
external token."""
ALLOWABLES = {
    "x",  # ala
    "y",  # anu
    "kxk",  # ken ala ken
    "wxw",  # wile ala wile
    "msa",
}

PHONOMATCHES = {
    "non",
    "nope",
    "some",
    "like",
    "use",
    "imo",
    "time",
    "man",
    "also",
}

ALPHABETIC_MATCHES: Set[str] = set()

IGNORABLES = PHONOMATCHES | ALPHABETIC_MATCHES

UCSUR_RANGES = [
    "\\U000F1900-\\U000F1977",  # pu
    "\\U000F1978-\\U000F1988",  # ku suli
    "\\U000F19A0-\\U000F19A3",  # ku lili
]
NIMI_UCSUR = find_unicode_chars(UCSUR_RANGES)


# NIMI_PU_UCSUR_RANGES = ["\\U000F1900-\\U000F1977"]
# NIMI_PU_ALE_UCSUR_RANGES = NIMI_PU_UCSUR_RANGES + ["\\U000F1978-\\U000F197A"]


def category_helper(data: Dict[str, Dict[str, str]], key: str, value: str) -> Set[str]:
    return {d["word"] for d in data.values() if d[key] == value}


with open(LINKU) as f:
    linku: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_PU = category_helper(linku, "book", "pu")
    NIMI_PU_SYNONYMS = {"namako", "kin", "oko"}

    NIMI_KU_SULI = category_helper(linku, "book", "ku suli")
    NIMI_KU_LILI = category_helper(linku, "book", "ku lili")

    NIMI_LINKU_CORE = category_helper(linku, "usage_category", "core")
    NIMI_LINKU_COMMON = category_helper(linku, "usage_category", "common")
    NIMI_LINKU_UNCOMMON = category_helper(linku, "usage_category", "uncommon")
    NIMI_LINKU_OBSCURE = category_helper(linku, "usage_category", "obscure")

with open(SANDBOX) as f:
    sandbox: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_LINKU_SANDBOX = {d["word"] for d in sandbox.values()}

del linku
del sandbox

__all__ = [
    "ALLOWABLES",
    "ALL_PUNCT",
    "ALL_PUNCT_RANGES",
    "ALPHABET",
    "CONSONANTS",
    "NIMI_KU_LILI",
    "NIMI_KU_SULI",
    "NIMI_LINKU_COMMON",
    "NIMI_LINKU_CORE",
    "NIMI_LINKU_OBSCURE",
    "NIMI_LINKU_SANDBOX",
    "NIMI_LINKU_UNCOMMON",
    "NIMI_PU",
    "NIMI_PU_SYNONYMS",
    "POSIX_PUNCT",
    "POSIX_PUNCT_RANGES",
    "UNICODE_PUNCT",
    "UNICODE_PUNCT_RANGES",
    "VOWELS",
]
