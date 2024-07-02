# STL
import re
from abc import ABC, abstractmethod
from typing import Set, List

# PDM
import regex
from typing_extensions import override, deprecated

# LOCAL
from sonatoki.utils import regex_escape
from sonatoki.Filters import NimiUCSUR  # seriously this sucks
from sonatoki.constants import ALL_PUNCT, SENTENCE_PUNCT, ALL_PUNCT_RANGES_STR

regex.DEFAULT_VERSION = regex.VERSION1


class Tokenizer(ABC):
    @classmethod
    @abstractmethod
    def tokenize(cls, s: str) -> List[str]: ...


class SetTokenizer(Tokenizer):
    delimiters: Set[str]


class RegexTokenizer(Tokenizer):
    pattern: "re.Pattern[str]"

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        return [clean for word in re.split(cls.pattern, s) if (clean := word.strip())]


class Regex1Tokenizer(Tokenizer):
    pattern: "regex.Pattern[str]"

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        return [
            clean for word in regex.split(cls.pattern, s) if (clean := word.strip())
        ]


class WordTokenizer(SetTokenizer):
    delimiters = set(ALL_PUNCT)

    @classmethod
    def __helper(cls, s: str, tokens: List[str], last_match: int, i: int):
        match = s[last_match:i].split()
        [tokens.append(t) for t in match if t]

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        if not s:
            return []

        tokens: List[str] = []

        i = 0  # ensure i is bound
        last_match = 0
        last_membership = s[0] in cls.delimiters
        for i, char in enumerate(s):
            mem = char in cls.delimiters
            ucsur = NimiUCSUR.filter(char)
            changed = (mem != last_membership) or ucsur
            # this keeps contiguous words together, but splits UCSUR
            if not changed:
                continue

            if ucsur:
                if i > last_match:
                    # Add the token before UCSUR character
                    cls.__helper(s, tokens, last_match, i)
                # Add UCSUR character itself as a token
                tokens.append(char)
                last_match = i + 1
                last_membership = mem
                continue

            cls.__helper(s, tokens, last_match, i)
            last_match = i
            last_membership = mem

        cls.__helper(s, tokens, last_match, i + 1)
        return tokens


@deprecated(
    "WordTokenizerRe is a previous reference implementation. Its behavior has diverged from WordTokenizer and it may not be restored."
)
class WordTokenizerRe(RegexTokenizer):
    pattern = re.compile(rf"""([{ALL_PUNCT_RANGES_STR}]+|\s+)""")


@deprecated(
    "WordTokenizerRe1 is a previous reference implementation. Its behavior has diverged from WordTokenizer and it may not be restored."
)
class WordTokenizerRe1(Regex1Tokenizer):
    """Reference implementation for WordTokenizer."""

    pattern = regex.compile(r"""([\p{posix_punct}\p{Punctuation}]+|\s+)""")


class SentTokenizer(SetTokenizer):
    delimiters = set(SENTENCE_PUNCT + "\n")  # regex does \n with a flag

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        if not s:
            return []

        tokens: List[str] = []
        last_match = 0
        for i, char in enumerate(s):
            if char not in cls.delimiters:
                continue

            match = s[last_match : i + 1].strip()
            last_match = i + 1  # newlines can strip but idc
            if not match:
                continue
            tokens.append(match)

        match = s[last_match:].strip()
        if match:
            tokens.append(match)

        return tokens


class SentTokenizerRe(RegexTokenizer):
    pattern = re.compile(
        rf"""(?<=[{regex_escape(SENTENCE_PUNCT)}])|$""", flags=re.MULTILINE
    )
    # TODO: are <> or {} that common as *sentence* delims? [] are already a stretch
    # TODO: do the typography characters matter?
    # NOTE: | / and , are *not* sentence delimiters for my purpose


class SentTokenizerRe1(Regex1Tokenizer):
    pattern = regex.compile(
        rf"""(?<=[{regex_escape(SENTENCE_PUNCT)}]|$)""", flags=regex.MULTILINE
    )


__all__ = [
    "WordTokenizer",
    "SentTokenizer",
]
