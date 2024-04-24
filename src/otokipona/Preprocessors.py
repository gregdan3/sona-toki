"""
"Preprocessors" are classes which strip content from a given string prior to tokenization.
There are currently two distinct types of Preprocessor:

- Remove a token from a string which would be difficult to identify after tokenization. 
  - URLs
  - DiscordEmotes
- Remove a section of a string which is contained in or marked by certain character(s). Also called "Containers"
  - SingleQuotes
  - DoubleQuotes
  - Backticks
  - Spoilers
  - ArrowQuote

Order does not generally matter, but if there were two overlapping containers such as in the string "|| spoiler ` monospace || `", order would matter.
As such, each Preprocessor exposes a .precedence attribute which is optionally usable for ordering them. Lower precedence means it should be applied first.
"""

# STL
from abc import ABC, abstractmethod

# PDM
import regex as re
from typing_extensions import override

re.DEFAULT_VERSION = re.VERSION1


class Preprocessor(ABC):
    precedence: int = 0

    @classmethod  # order matters
    @abstractmethod
    def process(cls, msg: str) -> str:
        raise NotImplementedError


class RegexPreprocessor(Preprocessor):
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


class URLs(RegexPreprocessor):
    """Remove http(s) protocol URLs"""

    pattern = re.compile(r"https?:\/\/\S+")


class DiscordEmotes(RegexPreprocessor):
    """Remove text-formatted Discord emotes `<flags:name:id>`"""

    pattern = re.compile(r"<a?:[a-zA-Z0-9_]{2,}:[0-9]{2,}>")


class DiscordMentions(RegexPreprocessor):
    pattern = re.compile(r"<@[\!\&]?[0-9]{2,}>")


class DiscordChannels(RegexPreprocessor):
    pattern = re.compile(r"<#[0-9]{2,}>")


class DiscordSpecial(RegexPreprocessor):
    pattern = re.compile(r"<id:[a-zA-Z0-9_]{4,}>")


"""
The following classes are Containers.

Containers are a special case of Ignorables, where an entire segment of an input
may be removed and not counted toward the accepted or total number of tokens.

Some users may prefer to use these so that they may quote third parties who 
would likely be using a language other than Toki Pona.
"""


class SingleQuotes(RegexPreprocessor):
    pattern = re.compile(r"'[^']+'", flags=re.S)  # . matches newline


class DoubleQuotes(RegexPreprocessor):
    pattern = re.compile(r'"[^"]+"', flags=re.S)


class Backticks(RegexPreprocessor):
    """Remove paired backticks and their contents `like this`"""

    precedence = -10
    pattern = re.compile(r"`[^`]+`", flags=re.S)


class Spoilers(RegexPreprocessor):
    """Remove paired double bars and their contents `||like this||`"""

    pattern = re.compile(r"\|\|(?:(?!\|\|).)+\|\|", flags=re.S)


class ArrowQuote(RegexPreprocessor):
    """Remove lines beginning with `> `"""

    pattern = re.compile(r"^>\ .+$", re.MULTILINE)


__all__ = [
    "DiscordEmotes",
    "SingleQuotes",
    "DoubleQuotes",
    "ArrowQuote",
    "Backticks",
    "Spoilers",
    "URLs",
]
