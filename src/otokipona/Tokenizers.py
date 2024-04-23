# STL
from typing import List, Callable

# PDM
import regex as re

try:
    # PDM
    import nltk
    from nltk.tokenize import sent_tokenize as __sent_tokenize_nltk
    from nltk.tokenize import word_tokenize as __word_tokenize_nltk
except ImportError as e:
    nltk = e


LANGUAGE = "english"  # for NLTK

SENT_DELIMS_RE = r"""(.*?[.?!;:])|(.+?$)"""
SENT_DELIMS_RE = re.compile(SENT_DELIMS_RE)

SENT_DELIMS_TOK = r"""(.*?[.?!;:-])|(.+?$)"""
SENT_DELIMS_TOK = re.compile(SENT_DELIMS_TOK)


WORD_DELIMS_RE = r"""\s+|(?=[.?!;:'"-])"""
WORD_DELIMS_RE = re.compile(WORD_DELIMS_RE)

WORD_DELIMS_TOK = r"([\p{Punctuation}\p{posix_punct}]+|\s+)"
WORD_DELIMS_TOK = re.compile(WORD_DELIMS_TOK)

Tokenizer = Callable[[str], List[str]]


if not isinstance(nltk, ImportError):

    def sent_tokenize_nltk(s: str) -> List[str]:
        return __sent_tokenize_nltk(text=s, language=LANGUAGE)

    def word_tokenize_nltk(s: str) -> List[str]:
        return __word_tokenize_nltk(text=s, language=LANGUAGE)


def sent_tokenize_re(s: str) -> List[str]:
    return [
        clean
        for sent in re.findall(SENT_DELIMS_RE, s)
        if (clean := sent[0].strip() or sent[1].strip())
    ]


def word_tokenize_re(s: str) -> List[str]:
    return [clean for word in re.split(WORD_DELIMS_RE, s) if (clean := word.strip())]


def sent_tokenize_tok(s: str) -> List[str]:
    return [
        clean
        for sent in re.findall(SENT_DELIMS_TOK, s)
        if (clean := sent[0].strip() or sent[1].strip())
    ]


def word_tokenize_tok(s: str) -> List[str]:
    return [clean for word in re.split(WORD_DELIMS_TOK, s) if (clean := word.strip())]
