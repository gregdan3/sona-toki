# STL
import re
from abc import ABC, abstractmethod
from typing import Set, List, Type
from functools import lru_cache as cache  # cache comes in 3.9

# PDM
import regex
from typing_extensions import override

# LOCAL
from sonatoki.constants import (
    VOWELS,
    NIMI_PU,
    ALPHABET,
    ALL_PUNCT,
    ALLOWABLES,
    CONSONANTS,
    IGNORABLES,
    NIMI_LINKU,
    NIMI_UCSUR,
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


class NimiUCSUR(MemberFilter):
    tokens = set(NIMI_UCSUR)


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

    tokens = set(ALL_PUNCT)


class PunctuationRe(RegexFilter):
    """Faster implementation of `PunctuationRe1`.
    Goes out of date compared to the `regex` library if UNICODE_PUNCT_RANGES is not updated.
    """

    pattern = re.compile(rf"[{ALL_PUNCT_RANGES}]+")


class PunctuationRe1(Regex1Filter):
    """Reference implementation for identifying tokens made entirely of punctuation."""

    pattern = regex.compile(r"[\p{Punctuation}\p{posix_punct}]+")


class OrFilter(Filter):
    """Instantiate with more than one filter to compose them into one filter,
    returning True when any individual filter matches or False otherwise.
    Requires at least two filters.

    OrFilter exists as a compromise between the need to score some filters equally,
    while not adding custom behavior to scorers.
    I could have allowed a position to have a list of filters instead of one filter,
    but this would require cleaning the user's input, and nested handling of lists.
    It also would not have been as powerful- I would need another param for the and/or switch,
    or to not give users the choice.

    Instead, the user is responsible for building an OrFilter out of their desired filters.
    """

    # a scorer with multiple filters in one scoring position,
    filters: List[Type[Filter]]

    def __init__(self, filters: List[Type[Filter]]) -> None:
        if not len(filters) >= 2:
            raise ValueError("Must provide at least one Filter to OrFilter.")
        self.filters = filters

    @override
    @cache(maxsize=None)
    def filter(self, token: str) -> bool:
        for f in self.filters:
            if f.filter(token):
                return True
        return False


class AndFilter(Filter):
    """Instantiate with more than one filter to compose them into one filter,
    returning False when any individual filter fails to match or True otherwise.
    Requires at least two filters."""

    filters: List[Type[Filter]]

    def __init__(self, filters: List[Type[Filter]]) -> None:
        if not len(filters) >= 2:
            raise ValueError("Must provide at least two Filters to AndFilter.")
        self.filters = filters

    @override
    @cache(maxsize=None)
    def filter(self, token: str) -> bool:
        for f in self.filters:
            if not f.filter(token):
                return False
        return True


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
