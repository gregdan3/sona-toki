# STL
import re
from abc import ABC, abstractmethod
from typing import List

# PDM
import regex
from typing_extensions import override

# LOCAL
from sonatoki.constants import UNICODE_PUNCT, PRUNED_POSIX_PUNCT

try:
    # PDM
    import nltk
    from nltk.tokenize import sent_tokenize as __sent_tokenize_nltk
    from nltk.tokenize import word_tokenize as __word_tokenize_nltk
except ImportError as e:
    nltk = e


regex.DEFAULT_VERSION = regex.VERSION1


class Tokenizer(ABC):
    @classmethod
    @abstractmethod
    def tokenize(cls, s: str) -> List[str]: ...


class NoOpTokenizer(Tokenizer):
    """This is a special case that you do not want or need."""

    @classmethod
    @override
    def tokenize(cls, s: str) -> List[str]:
        return [s]


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


class WordTokenizerTok(RegexTokenizer):
    pattern = re.compile(rf"""([{PRUNED_POSIX_PUNCT}{UNICODE_PUNCT}]+|\s+)""")


class SentTokenizerTok(RegexTokenizer):
    pattern = re.compile(r"""(?<=[.?!:;·…“”"'()\[\]\-])|$""", flags=re.MULTILINE)
    # TODO: are <> or {} that common as *sentence* delims? [] are already a stretch
    # TODO: do the typography characters matter?
    # NOTE: | / and , are *not* sentence delimiters for my purpose


class WordTokenizerRe(RegexTokenizer):
    pattern = re.compile(r"""(?<=[.?!;:'"-])""")


class SentTokenizerRe(RegexTokenizer):
    pattern = re.compile(r"""(.*?[.?!;:])|(.+?$)""")


if not isinstance(nltk, ImportError):

    class WordTokenizerNLTK(Tokenizer):
        @classmethod
        @override
        def tokenize(cls, s: str) -> List[str]:
            return __word_tokenize_nltk(text=s, language=LANGUAGE)

    class SentTokenizerNLTK(Tokenizer):
        @classmethod
        @override
        def tokenize(cls, s: str) -> List[str]:
            return __sent_tokenize_nltk(text=s, language=LANGUAGE)
