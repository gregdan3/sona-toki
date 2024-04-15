# STL
from abc import ABC, abstractmethod
from typing import Set
from functools import lru_cache as cache  # cache comes in 3.9

# PDM
import regex as re
from typing_extensions import override

# LOCAL
from otokipona.constants import (
    VOWELS,
    CONSONANTS,
    NIMI_PU_SET,
    ALPHABET_SET,
    NIMI_LINKU_SET,
)


class Validator(ABC):
    @classmethod
    @abstractmethod
    @cache(maxsize=None)
    def is_valid(cls, token: str) -> bool:
        raise NotImplementedError


class RegexValidator(Validator):
    pattern: "re.Pattern[str]"

    @classmethod
    @override
    @cache(maxsize=None)
    def is_valid(cls, token: str) -> bool:
        return not not re.fullmatch(cls.pattern, token)


class SetValidator(Validator):
    tokens: Set[str]

    @classmethod
    @override
    @cache(maxsize=None)
    def is_valid(cls, token: str) -> bool:
        return token in cls.tokens


class Name(Validator):
    """Determines if a given token is a valid name (also called a loan word)
    When Toki Pona is written with the Latin alphabet, names are generally
    capitalized at their start.
    Thus, we assume this holds for any input token.

    Note that this alone cannot determine if a token is a valid name, because
    a standalone name is considered invalid in Toki Pona- names generally have head nouns.
    """

    @classmethod
    @override
    @cache(maxsize=None)
    def is_valid(cls, token: str) -> bool:
        return token == token.capitalize()


class NimiPu(SetValidator):
    tokens = NIMI_PU_SET


class NimiLinku(SetValidator):
    tokens = NIMI_LINKU_SET


class Phonotactic(RegexValidator):
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


class Syllabic(RegexValidator):
    """Determines if a given token is syllabically valid Toki Pona (or `n`).
    Words must have correctly ordered vowels and consonants, but the phonotactic
    exceptions are not considered."""

    # rf"^((^[{VOWELS}]|[{CONSONANTS}][{VOWELS}])n?)+$|^n$"
    # Alterative I was exploring takes ~15% more steps
    pattern = re.compile(
        rf"^(?:^[{VOWELS}]n?)?(?:[{CONSONANTS}][{VOWELS}]n?)*$|^n$",
        flags=re.IGNORECASE,
    )


class Alphabetic(Validator):
    @classmethod
    @override
    @cache(maxsize=None)
    def is_valid(cls, token: str) -> bool:
        # Faster than regex version
        return set(token.lower()).issubset(ALPHABET_SET)
