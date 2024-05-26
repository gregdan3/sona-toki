# STL
import re
from abc import ABC, abstractmethod
from typing import Set
from functools import lru_cache as cache  # cache comes in 3.9

# PDM
import regex
from typing_extensions import override

# LOCAL
from sonatoki.constants import (
    VOWELS,
    NIMI_PU,
    ALPHABET,
    ALLOWABLES,
    CONSONANTS,
    IGNORABLES,
    NIMI_LINKU,
    POSIX_PUNCT,
    UNICODE_PUNCT,
    NIMI_LINKU_LILI,
    ALL_PUNCT_RANGES,
    NIMI_PU_SYNONYMS,
    NIMI_LINKU_SANDBOX,
)

regex.DEFAULT_VERSION = regex.VERSION1


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


class Regex1Filter(Filter):
    pattern: "regex.Pattern[str]"

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return not not regex.fullmatch(cls.pattern, token)


class MemberFilter(Filter):
    tokens: Set[str]

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return token.lower() in cls.tokens


class SubsetFilter(Filter):
    tokens: Set[str]

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return set(token.lower()).issubset(cls.tokens)


class Miscellaneous(MemberFilter):
    tokens = set(ALLOWABLES)


class EnglishIgnorables(MemberFilter):
    tokens = set(IGNORABLES)


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
        # TODO:  If the token is in a script which doesn't have a case distinction,
        # this will errantly match.


class NimiPu(MemberFilter):
    tokens = set(NIMI_PU)


class NimiPuAle(MemberFilter):
    tokens = set(NIMI_PU + NIMI_PU_SYNONYMS)


class NimiLinku(MemberFilter):
    tokens = set(NIMI_LINKU)


class NimiLinkuAle(MemberFilter):
    tokens = set(NIMI_LINKU + NIMI_LINKU_LILI)


class NimiLinkuSandbox(MemberFilter):
    tokens = set(NIMI_LINKU + NIMI_LINKU_LILI + NIMI_LINKU_SANDBOX)


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


class Alphabetic(SubsetFilter):
    tokens = set(ALPHABET)


class AlphabeticRe(RegexFilter):
    pattern = re.compile(rf"[{ALPHABET}]+", flags=re.IGNORECASE)


class Numeric(Filter):
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


class Punctuation(SubsetFilter):
    """Identify whether a token is entirely punctuation. Fastest implementation."""

    tokens = set(POSIX_PUNCT + UNICODE_PUNCT)


class PunctuationRe(RegexFilter):
    """Faster implementation of `PunctuationRe1`.
    Goes out of date compared to the `regex` library if UNICODE_PUNCT is not updated."""

    pattern = re.compile(rf"[{ALL_PUNCT_RANGES}]+")


class PunctuationRe1(Regex1Filter):
    """Reference implementation for identifying tokens made entirely of punctuation."""

    pattern = regex.compile(r"[\p{Punctuation}\p{posix_punct}]+")


__all__ = [
    "Alphabetic",
    "EnglishIgnorables",
    "NimiLinku",
    "NimiLinkuAle",
    "NimiLinkuSandbox",
    "NimiPu",
    "NimiPuAle",
    "Numeric",
    "Phonotactic",
    "ProperName",
    "Punctuation",
    "Syllabic",
]
