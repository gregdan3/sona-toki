# STL
import re
from abc import ABC, abstractmethod

# PDM
from typing_extensions import override


class Cleaner(ABC):
    @classmethod
    @abstractmethod
    def clean(cls, token: str) -> str:
        raise NotImplementedError


class RegexCleaner(Cleaner):
    pattern: "re.Pattern[str]"
    replace: str

    @classmethod
    @override
    def clean(cls, token: str) -> str:
        return re.sub(cls.pattern, cls.replace, token)


class ConsecutiveDuplicates(RegexCleaner):
    """Remove consecutive duplicates from an input string, ignoring case.

    The first match of any 2+ will become `\\1`, preserving initial case.
    For example, `FfFoo` will reduce to `Foo`, and `bBAR` will reduce to `bAR`.

    This is desirable for Toki Pona written with the Latin alphabet because strings
    may be altered for emphasis or effect, such as in "sonaaaa" or "AAAAAA".

    This may be undesirable for moraic scripts like Hiragana, where `わわ` would be
    incorrectly reduced to `わ`. This does preserve phonotactic validity, though."""

    pattern = re.compile(r"(.)\1+", flags=re.IGNORECASE)
    replace = r"\1"


__all__ = ["ConsecutiveDuplicates"]
