#!/bin/env python3
# STL
import os
import json
import argparse
from typing import Any, Set, Dict, List

# PDM
import emoji
import requests

# LOCAL
from sonatoki.utils import find_unicode_ranges
from sonatoki.Filters import (
    Or,
    LongSyllabic,
    NimiLinkuCore,
    LongAlphabetic,
    NimiLinkuCommon,
    NimiLinkuObscure,
    NimiLinkuUncommon,
)
from sonatoki.Cleaners import ConsecutiveDuplicates
from sonatoki.constants import (
    UCSUR_PUNCT_RANGES,
    UNICODE_PUNCT_RANGES,
    EMOJI_VARIATION_SELECTOR_RANGES,
)

HERE = os.path.dirname(os.path.realpath(__file__))

UNICODE_DATA = "https://unicode.org/Public/UNIDATA/UnicodeData.txt"

LINKU_WORDS = "https://api.linku.la/v1/words?lang=en"
LINKU_SANDBOX = "https://api.linku.la/v1/sandbox?lang=en"

WORDS_10K = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt"
WORDS_25K = "https://raw.githubusercontent.com/dolph/dictionary/master/popular.txt"
WORDS_479K = (
    "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
)

HEADERS = {  # pretend to be Chrome 121, just in case
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3"
}


def download(url: str) -> str:
    if not url.startswith("https://"):
        raise ValueError(url)

    resp = requests.get(url, timeout=5, headers=HEADERS)
    return resp.text


def download_json(url: str) -> Dict[str, Any]:
    resp = download(url)
    return json.loads(resp)


def regen_linku_data():
    data = download_json(LINKU_WORDS)
    with open(os.path.join(HERE, "linku.json"), "w") as f:
        _ = f.write(json.dumps(data))

    data = download_json(LINKU_SANDBOX)
    with open(os.path.join(HERE, "sandbox.json"), "w") as f:
        _ = f.write(json.dumps(data))


def regen_false_negatives():
    # TODO: regen from my frequency data where the score is below 0.8?
    KnownWords = Or(
        NimiLinkuCore,
        NimiLinkuCommon,
        NimiLinkuUncommon,
        NimiLinkuObscure,
    )

    syllabic_matches: Set[str] = set()
    alphabetic_matches: Set[str] = set()
    data = download(WORDS_25K)
    for word in data.splitlines():
        if not word:
            continue
        word = ConsecutiveDuplicates.clean(word)

        if KnownWords.filter(word):
            # ignore dictionary
            continue
        if LongSyllabic.filter(word):
            syllabic_matches.add(word)
            continue
        if LongAlphabetic.filter(word):
            alphabetic_matches.add(word)
            continue

    # TODO: include short matches or no?
    with open(os.path.join(HERE, "syllabic.txt"), "w") as f:
        syllabic_final = sorted([word + "\n" for word in syllabic_matches])
        f.writelines(syllabic_final)

    with open(os.path.join(HERE, "alphabetic.txt"), "w") as f:
        alphabetic_final = sorted([word + "\n" for word in alphabetic_matches])
        f.writelines(alphabetic_final)


def regen_unicode_data():
    PUNCT_CATEGORIES = {
        # Punctuation
        "Pc",  # Connector
        "Pd",  # Dash
        "Pe",  # Close (end)
        "Pf",  # Final
        "Pi",  # Initial
        "Po",  # Other
        "Ps",  # Open (sOpen)
        # Symbol
        "Sm",  # Math
        "Sk",  # Modifier (kModifier)
        "Sc",  # Currency
        "So",  # Other
    }
    r"""These characters are in Symbol other (So) but are not in
    `\p{Punctuation}` However, I began excluding them again, because it turns
    out that some sequences of latin alphabet emoji."""

    # NOTE: There are many characters which look like writing characters but are in the punctuation character class. Examples:
    # - kangxi radicals from ⺀ to ⿕ which are for demonstration, not writing
    # - parenthesized hangul letters and syllables from ㈀ to ㈜
    # - circled katakana from ㋐ to ㋾
    # the latter two shouldn't be in `\p{Punctuation}` if the latin alphabet isn't... oof

    def is_punctuation(data: List[str]):
        return data[2] in PUNCT_CATEGORIES

    def get_character(data: List[str]):
        return chr(int(data[0], 16))

    unicode_data = download(UNICODE_DATA)
    unicode_punctuation = ""
    for line in unicode_data.split("\n"):
        if not line:  # damn you, trailing newline
            continue
        # NOTE: UnicodeData.txt lists a range if there are many consecutive similar characters
        # (e.g. CJK Ideograph, First at 4E00 and CJK Ideograph, Last at 9FFF).
        # This does not apply to any currently defined punctuation category.

        unicode_data = line.split(";")
        if not is_punctuation(unicode_data):
            continue

        char = get_character(unicode_data)

        unicode_punctuation += char

    unicode_punctuation = emoji.replace_emoji(unicode_punctuation)

    unicode_ranges = find_unicode_ranges(unicode_punctuation)
    unicode_ranges.extend(UCSUR_PUNCT_RANGES)
    # unicode_ranges.extend(EMOJI_VARIATION_SELECTOR_RANGES)  # made unnecessary by emoji library
    unicode_ranges = sorted(unicode_ranges)
    # sorted in case my manual additions are out of order

    if unicode_ranges != UNICODE_PUNCT_RANGES:
        output = json.dumps(unicode_ranges, indent=4, ensure_ascii=True)
        print(output)


def main(argv: argparse.Namespace):
    regen_unicode_data()
    regen_linku_data()
    regen_false_negatives()


if __name__ == "__main__":
    """Helper script to fetch UNICODE_PUNCT in constants.py."""
    parser = argparse.ArgumentParser()

    # TODO: choice between regen unicode data, regen linku, regen english phonomatches
    argv = parser.parse_args()
    main(argv)
