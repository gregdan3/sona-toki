# STL
from abc import ABC, abstractmethod
from typing import Set
from functools import lru_cache as cache  # cache comes in 3.9

# PDM
import regex as re
from typing_extensions import override

# LOCAL
from sonatoki.constants import (
    VOWELS,
    CONSONANTS,
    NIMI_PU_SET,
    ALPHABET_SET,
    ALLOWABLES_SET,
    NIMI_LINKU_SET,
    NIMI_PU_ALE_SET,
    NIMI_LINKU_ALE_SET,
)

re.DEFAULT_VERSION = re.VERSION1


class Filter(ABC):
    @classmethod
    @abstractmethod
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        raise NotImplementedError


class RegexFilter(Filter):
    pattern: "re.Pattern[str]"

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return not not re.fullmatch(cls.pattern, token)


class SetFilter(Filter):
    tokens: Set[str]

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return token.lower() in cls.tokens


class Miscellaneous(SetFilter):
    tokens = ALLOWABLES_SET


class ProperName(Filter):
    """Determines if a given token is a valid name (also called a loan word).
    When Toki Pona is written with the Latin alphabet, names are generally
    capitalized at their start. This filter identifies those tokens.

    Note that this alone cannot determine if a token is a valid name, because
    a standalone name is considered invalid in Toki Pona- names generally have head nouns.
    This tool only examines one token at a time, so cannot detect names any better than identifying their capital letter.
    """

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return token == token.capitalize()


class NimiPu(SetFilter):
    tokens = NIMI_PU_SET


class NimiPuAle(SetFilter):
    tokens = NIMI_PU_ALE_SET


class NimiLinku(SetFilter):
    tokens = NIMI_LINKU_SET


class NimiLinkuAle(SetFilter):
    tokens = NIMI_LINKU_ALE_SET


class Phonotactic(RegexFilter):
    """Determines if a given token is phonotactically valid Toki Pona (or `n`).
    Excludes both consecutive nasals and the illegal syllables:
    - "nm", "nn"
    - "wu", "wo", "ji", "ti"

    Note that if this validator is used after `Cleaners.ConsecutiveDuplicates`,
    "nn" cannot be found."""

    pattern = re.compile(
        rf"^((^[{VOWELS}]|[klmnps][{VOWELS}]|[jt][aeou]|[w][aei])(n(?![mn]))?)+$|^n$",
        # Can't split initial vowel group off like in Syllabics because of
        # consecutive nasal detection; it is costly to duplicate
        flags=re.IGNORECASE,
    )


class Syllabic(RegexFilter):
    """Determines if a given token is syllabically valid Toki Pona (or `n`).
    Words must have correctly ordered vowels and consonants, but the phonotactic
    exceptions are not considered."""

    # rf"^((^[{VOWELS}]|[{CONSONANTS}][{VOWELS}])n?)+$|^n$"
    # Alterative I was exploring takes ~15% more steps
    pattern = re.compile(
        rf"^(?:^[{VOWELS}]n?)?(?:[{CONSONANTS}][{VOWELS}]n?)*$|^n$",
        flags=re.IGNORECASE,
    )


class Alphabetic(Filter):
    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        # Faster than regex version
        return set(token.lower()).issubset(ALPHABET_SET)


class Numerics(Filter):
    """Determine if a given token is entirely numeric.
    Covers all numeric symbols in Unicode.

    This will fail to find numeric tokens such as "1.111" or "-42",
    but if used with the aggressive tokenizer designed for `tok`, these will be
    split into `["1", ".", "111"]` and `["-", "42"]` respectively. As such, the
    numeric tokens will be split from their punctuation."""

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, msg: str) -> bool:
        return msg.isnumeric()


class Punctuations(RegexFilter):
    pattern = re.compile(r"[\p{Punctuation}\p{posix_punct}]+")


__all__ = [
    "NimiPu",
    "NimiLinku",
    "NimiLinkuAle",
    "Phonotactic",
    "Syllabic",
    "Alphabetic",
    "ProperName",
    "Punctuations",
    "Numerics",
]
