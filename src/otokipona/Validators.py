# STL
from abc import ABC, abstractmethod
from typing import Set

# PDM
import regex as re
from typing_extensions import override

# LOCAL
from otokipona.constants import VOWELS, CONSONANTS


class Validator(ABC):
    @classmethod
    @abstractmethod
    def is_valid(cls, token: str) -> bool:
        raise NotImplementedError


class RegexValidator(Validator):
    pattern: "re.Pattern[str]"

    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return not not re.fullmatch(cls.pattern, token)


class SetValidator(Validator):
    tokens: Set[str]

    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return token in cls.tokens


class Name(Validator):
    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return token == token.capitalize()


class NimiPu(Validator):
    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return False


class NimiLinku(Validator):
    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return False


class Phonotactic(RegexValidator):
    pattern = re.compile(
        rf"^((^[{VOWELS}]|[klmnps][{VOWELS}]|[jt][aeou]|[w][aei])(n(?![mn]))?)+|n$"
    )

    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return False


class Syllabic(Validator):
    pattern = re.compile(
        rf"^([{CONSONANTS}]?[{VOWELS}]n?)([{CONSONANTS}][{VOWELS}]n?)*|n$"
    )

    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return False


class Alphabetic(Validator):
    @classmethod
    @override
    def is_valid(cls, token: str) -> bool:
        return False
