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
    def to_tokens(cls, s: str) -> List[str]:
        tokens: List[str] = []

        slen = len(s)
        i = 0
        while i < slen:

            last_match = i
            while i < slen and s[i] in cls.delimiters:
                # no special case
                i += 1
            if i > last_match:
                tokens.append(s[last_match:i])

            last_match = i
            while i < slen and s[i] not in cls.delimiters:
                if NimiUCSUR.filter(s[i]):
                    if i > last_match:
                        tokens.append(s[last_match:i])
                    tokens.append(s[i])
                    last_match = i + 1

                i += 1
            if i > last_match:
                tokens.append(s[last_match:i])

        return tokens

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        if not s:
            return []

        tokens: List[str] = []
        candidates: List[str] = s.split()

        for candidate in candidates:
            results = cls.to_tokens(candidate)
            tokens.extend(results)

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
