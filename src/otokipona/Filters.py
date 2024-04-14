# STL
from abc import ABC, abstractmethod
from typing import Callable

# PDM
import regex as re
from typing_extensions import override

# LOCAL
from otokipona.utils import InputType

Processor = Callable[[str], str]


class Filter(ABC):
    input: InputType

    @classmethod  # order matters
    @abstractmethod
    def process(cls, msg: str) -> str:
        raise NotImplementedError


class RegexFilter(Filter):
    pattern: "re.Pattern[str]"
    replace: str = " "

    @classmethod
    @override
    def process(cls, msg: str) -> str:
        return re.sub(cls.pattern, cls.replace, msg)


"""
The following classes are Ignorables.

Ignorables are tokens which do not count toward the accepted number of tokens
or the total number of tokens.
This is generally because they are considered external to Toki Pona.

It is likely that every user will want to use these. 
Not having them will cause many false negatives, such as when a URL is divided
into its parts and checked as a token.
"""


class URLs(RegexFilter):
    """Remove http(s) protocol URLs"""

    input = InputType.Message
    pattern = re.compile(r"https?:\/\/\S+")


class DiscordEmotes(RegexFilter):
    """Remove text-formatted Discord emotes `<flags:name:id>`"""

    input = InputType.Message
    pattern = re.compile(r"<a?:[a-zA-Z0-9_]{2,}:[0-9]{2,}>")


"""
The following classes are Containers.

Containers are a special case of Ignorables, where an entire segment of an input
may be removed and not counted toward the accepted or total number of tokens.

Some users may prefer to use these so that they may quote third parties who 
would likely be using a language other than Toki Pona.
"""


class SingleQuotes(RegexFilter):
    input = InputType.Message
    pattern = re.compile(r"'[^']+'")


class DoubleQuotes(RegexFilter):
    input = InputType.Message
    pattern = re.compile(r'"[^"]+"')


class Backticks(RegexFilter):
    """Remove paired backticks and their contents `like this`"""

    input = InputType.Message
    pattern = re.compile(r"`[^`]+`")


class Spoilers(RegexFilter):
    """Remove paired double bars and their contents `||like this||`"""

    input = InputType.Message
    pattern = re.compile(r"\|\|(?:(?!\|\|).)+\|\|", flags=re.S)  # . matches newline


class ArrowQuote(RegexFilter):
    """Remove lines beginning with `> `"""

    input = InputType.Message
    pattern = re.compile(r"^>\ .+$", re.MULTILINE)


class NonAlphabetic(Filter):
    input = InputType.Token

    @classmethod
    @override
    def process(cls, msg: str) -> str:
        return msg if msg.isalpha() else ""


__all__ = [
    "URLs",
    "DiscordEmotes",
    "SingleQuotes",
    "DoubleQuotes",
    "Backticks",
    "Spoilers",
    "ArrowQuote",
    "NonAlphabetic",
    # "Name",
]
