# STL
import re
from abc import ABC, abstractmethod
from typing import Set, List, Type
from functools import lru_cache as cache  # cache comes in 3.9

# PDM
import regex
from typing_extensions import override, deprecated

# LOCAL
from sonatoki.utils import prep_dictionary
from sonatoki.constants import (
    VOWELS,
    NIMI_PU,
    ALPHABET,
    ALL_PUNCT,
    ALLOWABLES,
    CONSONANTS,
    NIMI_UCSUR,
    NIMI_KU_LILI,
    NIMI_KU_SULI,
    NIMI_LINKU_CORE,
    NIMI_PU_SYNONYMS,
    NIMI_LINKU_COMMON,
    FALSE_POS_SYLLABIC,
    NIMI_LINKU_OBSCURE,
    NIMI_LINKU_SANDBOX,
    NOT_IN_PUNCT_CLASS,
    NIMI_LINKU_UNCOMMON,
    ALL_PUNCT_RANGES_STR,
    FALSE_POS_ALPHABETIC,
    UCSUR_PUNCT_RANGES_STR,
    EMOJI_VARIATION_SELECTOR_RANGES_STR,
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


class FalsePosSyllabic(MemberFilter):
    """A MemberFilter of words which would match Syllabic (and often Phonetic),
    but are words in other languages."""

    tokens = prep_dictionary(FALSE_POS_SYLLABIC)


class FalsePosAlphabetic(MemberFilter):
    """A MemberFilter of words which would match Alphabetic, but are words in
    other languages."""

    tokens = prep_dictionary(FALSE_POS_ALPHABETIC)


class ProperName(Filter):
    """Determines if a given token is a valid name (also called a loan word).
    When Toki Pona is written with the Latin alphabet, names are generally
    capitalized at their start. This filter identifies those tokens.

    Note that this alone cannot determine if a token is a valid name,
    because a standalone name is considered invalid in Toki Pona- names
    generally have head nouns. This tool only examines one token at a
    time, so cannot detect names any better than identifying their
    capital letter.
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
    "nn" cannot be found.
    """

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

    Words must have correctly ordered vowels and consonants, but the
    phonotactic exceptions are not considered.
    """

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
    """Determine if a given token is entirely numeric. Covers all numeric
    symbols in Unicode.

    This will fail to find numeric tokens such as "1.111" or "-42",
    but if used with the aggressive tokenizer designed for `tok`, these will be
    split into `["1", ".", "111"]` and `["-", "42"]` respectively. As such, the
    numeric tokens will be split from their punctuation.
    """

    @classmethod
    @override
    @cache(maxsize=None)
    def filter(cls, msg: str) -> bool:
        return msg.isnumeric()


class Punctuation(SubsetFilter):
    """Identify whether a token is entirely punctuation.

    Fastest implementation.
    """

    tokens = set(ALL_PUNCT)


class PunctuationRe(RegexFilter):
    """Faster implementation of `PunctuationRe1`.

    Goes out of date compared to the `regex` library if UNICODE_PUNCT_RANGES is not updated.
    """

    pattern = re.compile(rf"[{ALL_PUNCT_RANGES_STR}]+")


class PunctuationRe1(Regex1Filter):
    """Reference implementation for identifying tokens made entirely of
    punctuation."""

    pattern = regex.compile(
        rf"[\p{{Punctuation}}\p{{posix_punct}}{NOT_IN_PUNCT_CLASS}{UCSUR_PUNCT_RANGES_STR}{EMOJI_VARIATION_SELECTOR_RANGES_STR}]+"
    )


class Or:
    """Instantiate with more than one filter to compose them into one filter,
    returning True when any individual filter matches or False otherwise.
    Requires at least two filters. If two or more MemberFilters are provided,
    they will be combined by creating a single set with the members of every
    individual filter.

    Or exists as a compromise between the need to score some filters
    equally, while not adding custom behavior to scorers. I could have
    allowed a position to have a list of filters instead of one filter,
    but this would require cleaning the user's input, and nested
    handling of lists. It also would not have been as powerful- I would
    need another param for the and/or switch, or to not give users the
    choice.

    Instead, the user is responsible for building an OrFilter out of
    their desired filters.
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

    @staticmethod
    def __member_filter(*filters: Type[MemberFilter]) -> Type[MemberFilter]:
        all_token_sets: List[Set[str]] = [f.tokens for f in filters]
        all_tokens: Set[str] = set().union(*all_token_sets)

        class CombinedFilter(MemberFilter):
            tokens = all_tokens

        return CombinedFilter

    def __new__(cls, *filters: Type[Filter]) -> Type[Filter]:
        if not len(filters) >= 2:
            raise ValueError("Provide at least two Filters to OrFilter.")

        member_filters = [f for f in filters if issubclass(f, MemberFilter)]
        other_filters = [f for f in filters if not issubclass(f, MemberFilter)]
        if len(member_filters) >= 2:
            # we can save some effort by making a single filter out of these
            member_filter = cls.__member_filter(*member_filters)
            other_filters.append(member_filter)
        else:
            other_filters.extend(member_filters)

        if len(other_filters) == 1:  # we only had member filters
            # TODO: this sucks?
            return other_filters[0]

        filter = cls.__generic_filter(*other_filters)
        return filter


class And:
    """Instantiate with more than one filter to compose them into one filter,
    returning False when any individual filter fails to match or True
    otherwise.

    Requires at least two filters.
    """

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


class Not(Filter):
    """
    Meta filter which may be inherited by or constructed with a filter to invert its output.
    ---
    ```
    from sonatoki.Filters import Alphabetic, Not

    my_filter = Not(Alphabetic)
    class MyFilter(Not, Alphabetic):
        ...
    ```
    """

    @classmethod
    @cache(maxsize=None)
    def filter(cls, token: str) -> bool:
        return not super().filter(token)

    def __new__(cls, filter: Type[Filter]) -> Type[Filter]:
        class NotFilter(Not, filter): ...

        return NotFilter


__all__ = [
    "Alphabetic",
    "And",
    "FalsePosSyllabic",
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
    "Not",
    "Numeric",
    "Or",
    "Phonotactic",
    "ProperName",
    "Punctuation",
    "Syllabic",
]
