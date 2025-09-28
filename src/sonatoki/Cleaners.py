# STL
import re
from abc import ABC, abstractmethod
from sys import intern

# PDM
from typing_extensions import override


class Cleaner(ABC):
    @classmethod
    @abstractmethod
    def clean(cls, token: str) -> str:
        """Transform a token to remove some undesirable part."""
        raise NotImplementedError


class RegexCleaner(Cleaner):
    pattern: "re.Pattern[str]"
    replace: str

    @classmethod
    @override
    def clean(cls, token: str) -> str:
        return intern(re.sub(cls.pattern, cls.replace, token))


class ConsecutiveDuplicates(Cleaner):
    """Remove consecutive duplicates from an input string, ignoring case.

    The first match of any 2+ will become `\\1`, preserving initial case.
    For example, `FfFoo` will reduce to `Foo`, and `bBAR` will reduce to `bAR`.

    This is desirable for Toki Pona written with the Latin alphabet because strings
    may be altered for emphasis or effect, such as in "sonaaaa" or "AAAAAA".

    This may be undesirable for moraic scripts like Hiragana, where `わわ` would be
    incorrectly reduced to `わ`. This does preserve phonotactic validity, though.
    """

    @classmethod
    @override
    def clean(cls, token: str) -> str:
        if not token:
            return token

        output = token[0]
        last_output = output.lower()  # ignore case in comparison
        for i in range(1, len(token)):
            cur_char = intern(token[i])
            lower_cur_char = intern(cur_char.lower())
            if lower_cur_char == last_output:
                continue
            output += cur_char  # preserve case of string
            last_output = lower_cur_char
        output = intern(output)
        return output


class ConsecutiveDuplicatesRe(RegexCleaner):
    """Reference implementation for `ConsecutiveDuplicates`."""

    pattern: "re.Pattern[str]" = re.compile(r"(.)\1+", flags=re.IGNORECASE)
    replace: str = r"\1"


class Lowercase(Cleaner):
    @classmethod
    @override
    def clean(cls, token: str) -> str:
        return intern(token.lower())


__all__ = [
    "ConsecutiveDuplicates",
    "Lowercase",
]
