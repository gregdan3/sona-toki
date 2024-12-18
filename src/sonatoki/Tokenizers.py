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
from sonatoki.constants import (
    ALL_PUNCT,
    INTRA_WORD_PUNCT,
    ALL_SENTENCE_PUNCT,
    UNICODE_WHITESPACE,
    ALL_PUNCT_RANGES_STR,
    UCSUR_CARTOUCHE_LEFT,
    UCSUR_CARTOUCHE_RIGHT,
    UCSUR_MINUS_CARTOUCHE,
)

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
    intra_word_punct = set(INTRA_WORD_PUNCT)

    @classmethod
    def is_delimiter(cls, c: str) -> bool:
        return c in cls.delimiters or not c

    @classmethod
    def add_token(cls, s: str, tokens: List[str], last_match: int, i: int):
        if i > last_match:
            tokens.append(s[last_match:i])

    @classmethod
    def to_tokens(cls, s: str) -> List[str]:
        tokens: List[str] = []

        slen = len(s)
        i = 0
        did_skip = False  # ensure exists
        while i < slen:

            # contiguous punctuation chars
            last_match = i
            while i < slen and cls.is_delimiter(s[i]):
                # no special case
                i += 1
            cls.add_token(s, tokens, last_match, i)

            # contiguous writing chars (much harder)
            last_match = i
            while i < slen and not cls.is_delimiter(s[i]):
                did_skip = False
                # we skip and see another writing char, or init

                if NimiUCSUR.filter(s[i]):
                    cls.add_token(s, tokens, last_match, i)
                    tokens.append(s[i])
                    i += 1
                    last_match = i
                    continue

                next_char = s[i + 1] if i + 1 < slen else ""
                if next_char in cls.intra_word_punct:
                    did_skip = True
                    i += 2
                    continue

                i += 1

            if did_skip:
                # we skipped, but there wasn't another writing character
                cls.add_token(s, tokens, last_match, i - 1)
                last_match = i - 1
                # there may be punctuation though
                # TODO: this is duplicated
                while i < slen and cls.is_delimiter(s[i]):
                    i += 1

            cls.add_token(s, tokens, last_match, i)

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
    delimiters: Set[str] = set(ALL_SENTENCE_PUNCT + "\n")  # regex does \n with a flag
    intra_word_punct: Set[str] = set(INTRA_WORD_PUNCT)
    all_punct: Set[str] = set(ALL_PUNCT + UNICODE_WHITESPACE)

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        if not s:
            return []

        tokens: List[str] = []

        slen = len(s)
        last_match = 0
        i = 0
        while i < slen:
            # if a cartouche appears, we do not want to split on its punctuation
            if s[i] == UCSUR_CARTOUCHE_LEFT:
                right_i = s.find(UCSUR_CARTOUCHE_RIGHT, i)
                contained: set[str] = set()
                if right_i > 0:
                    contained = set(s[i + 1 : right_i])
                # but it must contain only non-cartouche UCSUR chars
                if contained and contained.issubset(UCSUR_MINUS_CARTOUCHE):
                    i = right_i + 1
                    continue
            if s[i] not in cls.delimiters:
                i += 1
                continue
            if s[i] in cls.intra_word_punct:
                prev = s[i - 1] if i > 0 else ""
                next = s[i + 1] if i + 1 < slen else ""
                if (
                    prev
                    and next
                    and prev not in cls.all_punct
                    and next not in cls.all_punct
                ):
                    i += 2
                    continue

            match = s[last_match : i + 1].strip()
            last_match = i + 1  # newlines can strip but idc
            if not match:
                i += 1
                continue
            tokens.append(match)
            i += 1

        match = s[last_match:].strip()
        if match:
            tokens.append(match)

        return tokens


@deprecated(
    "SentTokenizerRe is a previous reference implementation. Its behavior has diverged from SentTokenizer and it may not be restored."
)
class SentTokenizerRe(RegexTokenizer):
    pattern = re.compile(
        rf"""(?<=[{regex_escape(ALL_SENTENCE_PUNCT)}])|$""", flags=re.MULTILINE
    )
    # TODO: are <> or {} that common as *sentence* delims? [] are already a stretch
    # TODO: do the typography characters matter?
    # NOTE: | / and , are *not* sentence delimiters for my purpose


@deprecated(
    "SentTokenizerRe1 is a previous reference implementation. Its behavior has diverged from SentTokenizer and it may not be restored."
)
class SentTokenizerRe1(Regex1Tokenizer):
    pattern = regex.compile(
        rf"""(?<=[{regex_escape(ALL_SENTENCE_PUNCT)}]|$)""", flags=regex.MULTILINE
    )


__all__ = [
    "WordTokenizer",
    "SentTokenizer",
]
