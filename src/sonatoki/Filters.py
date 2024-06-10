# STL
import re
from abc import ABC, abstractmethod
from typing import Set, List, Type
from functools import lru_cache as cache  # cache comes in 3.9

# PDM
import regex
from typing_extensions import override

# LOCAL
from sonatoki.utils import prep_dictionary
from sonatoki.constants import (
    VOWELS,
    NIMI_PU,
    ALPHABET,
    ALL_PUNCT,
    ALLOWABLES,
    CONSONANTS,
    IGNORABLES,
    NIMI_UCSUR,
    NIMI_KU_LILI,
    NIMI_KU_SULI,
    NIMI_LINKU_CORE,
    ALL_PUNCT_RANGES,
    NIMI_PU_SYNONYMS,
    NIMI_LINKU_COMMON,
    NIMI_LINKU_OBSCURE,
    NIMI_LINKU_SANDBOX,
    UCSUR_PUNCT_RANGES,
    NIMI_LINKU_UNCOMMON,
)

regex.DEFAULT_VERSION = regex.VERSION1


class Filter(ABC):
    @classmethod
    @abstractmethod
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        raise NotImplementedError


class MinLen(Filter):
    """
    Meta filter meant to be inherited by another filter to add a length requirement.
    Multiple-inherit with `MinLen` as the first argument so `super()` resolves correctly.
    You may also construct any other filter with a minimum length filter like so:

    ```
    MinLen(Alphabetic, 3)
    ```
    """

    length = 0

    @classmethod
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        if len(token) < cls.length:
            return False
        return super().filter(token)

    def __new__(cls, filter: Type[Filter], length_: int) -> Type[Filter]:
        class MinLenFilter(MinLen, Filter):
            length = length_

        return MinLenFilter


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
    tokens = prep_dictionary(ALLOWABLES)


class EnglishIgnorables(MemberFilter):
    """NOTE: Not recommended for use.
    It is better to use a Long* filter such as LongSyllabic than to use this filter.
    This filter hides words from scoring rather than scoring them poorly,
    which is more of a benefit than a loss for a word you would like to omit."""

    tokens = prep_dictionary(IGNORABLES)


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


class LongProperName(MinLen, ProperName):
    length = 2  # reject "names" of length 1


class NimiPu(MemberFilter):
    tokens = prep_dictionary(NIMI_PU)


class NimiPuSynonyms(MemberFilter):
    tokens = prep_dictionary(NIMI_PU_SYNONYMS)


class NimiKuSuli(MemberFilter):
    tokens = prep_dictionary(NIMI_KU_SULI)


class NimiKuLili(MemberFilter):
    tokens = prep_dictionary(NIMI_KU_LILI)


class NimiLinkuCore(MemberFilter):
    tokens = prep_dictionary(NIMI_LINKU_CORE)


class NimiLinkuCommon(MemberFilter):
    tokens = prep_dictionary(NIMI_LINKU_COMMON)


class NimiLinkuUncommon(MemberFilter):
    tokens = prep_dictionary(NIMI_LINKU_UNCOMMON)


class NimiLinkuObscure(MemberFilter):
    tokens = prep_dictionary(NIMI_LINKU_OBSCURE)


class NimiLinkuSandbox(MemberFilter):
    tokens = prep_dictionary(NIMI_LINKU_SANDBOX)


class NimiUCSUR(MemberFilter):
    tokens = prep_dictionary(NIMI_UCSUR)


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


class LongPhonotactic(MinLen, Phonotactic):
    length = 3


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


class LongSyllabic(MinLen, Syllabic):
    length = 3


class Alphabetic(SubsetFilter):
    tokens = set(ALPHABET)


class AlphabeticRe(RegexFilter):
    pattern = re.compile(rf"[{ALPHABET}]+", flags=re.IGNORECASE)


class LongAlphabetic(MinLen, Alphabetic):
    length = 3


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

    pattern = regex.compile(
        rf"[\p{{Punctuation}}\p{{posix_punct}}{UCSUR_PUNCT_RANGES}]+"
    )


class OrFilter:
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

    @staticmethod
    def __generic_filter(*filters_: Type[Filter]) -> Type[Filter]:

        class CombinedFilter(Filter):
            filters: List[Type[Filter]] = list(filters_)  # TODO: tuple better?

            @classmethod
            @override
            @cache(maxsize=None)
            def filter(cls, token: str) -> bool:
                for f in cls.filters:
                    if f.filter(token):
                        return True
                return False

        return CombinedFilter

    def __new__(cls, *filters: Type[Filter]) -> Type[Filter]:
        if not len(filters) >= 2:
            raise ValueError("Provide at least two Filters to OrFilter.")

        member_filters = [f for f in filters if issubclass(f, MemberFilter)]
        if len(member_filters) >= 2:
            raise Warning("Use OrMemberFilter for combining two or more MemberFilters.")

        filter = cls.__generic_filter(*filters)

        return filter


class OrMemberFilter:
    @staticmethod
    def __member_filter(*filters: Type[MemberFilter]) -> Type[MemberFilter]:
        all_token_sets: List[Set[str]] = [f.tokens for f in filters]
        all_tokens: Set[str] = set().union(*all_token_sets)

        class CombinedFilter(MemberFilter):
            tokens = all_tokens

        return CombinedFilter

    def __new__(cls, *filters_: Type[MemberFilter]) -> Type[MemberFilter]:
        if not len(filters_) >= 2:
            raise ValueError("Provide two or more MemberFilters to OrMemberFilter.")
        filter = cls.__member_filter(*filters_)
        return filter


class AndFilter(Filter):
    """Instantiate with more than one filter to compose them into one filter,
    returning False when any individual filter fails to match or True otherwise.
    Requires at least two filters."""

    def __new__(cls, *filters_: Type[Filter]) -> Type[Filter]:
        if not len(filters_) >= 2:
            raise ValueError("Must provide at least two Filters to AndFilter.")

        class AnonymousAndFilter(Filter):
            filters: List[Type[Filter]] = list(filters_)  # TODO: tuple better?

            @classmethod
            @override
            @cache(maxsize=None)
            def filter(cls, token: str) -> bool:
                for f in cls.filters:
                    if not f.filter(token):
                        return False
                return True

        return AnonymousAndFilter


__all__ = [
    "Alphabetic",
    "AndFilter",
    "EnglishIgnorables",
    "LongAlphabetic",
    "LongPhonotactic",
    "LongProperName",
    "LongSyllabic",
    "MinLen",
    "NimiLinkuCore",
    "NimiLinkuSandbox",
    "NimiPu",
    "NimiPuSynonyms",
    "NimiUCSUR",
    "Numeric",
    "OrFilter",
    "Phonotactic",
    "ProperName",
    "Punctuation",
    "Syllabic",
]
