# STL
from typing import List, Callable

# PDM
import regex as re

# TODO: Entire module should be reworked to match the class scheme of the rest of the module, imo

try:
    # PDM
    import nltk
    from nltk.tokenize import sent_tokenize as __sent_tokenize_nltk
    from nltk.tokenize import word_tokenize as __word_tokenize_nltk
except ImportError as e:
    nltk = e


LANGUAGE = "english"  # for NLTK

SENT_DELIMS_RE = re.compile(r"""(.*?[.?!;:])|(.+?$)""")
SENT_DELIMS_TOK = re.compile(r"""(?<=[.?!:;·…“”"'()\[\]\-]|$)""")
# TODO: are <> or {} that common as *sentence* delims? [] are already a stretch
# TODO: do the typography characters matter?
# NOTE: | / and , are *not* sentence delimiters for my purpose

WORD_DELIMS_RE = re.compile(r"""\s+|(?=[.?!;:'"-])""")
WORD_DELIMS_TOK = re.compile(r"([\p{Punctuation}\p{posix_punct}]+|\s+)")

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
    return [clean for sent in re.split(SENT_DELIMS_TOK, s) if (clean := sent.strip())]


def word_tokenize_tok(s: str) -> List[str]:
    return [clean for word in re.split(WORD_DELIMS_TOK, s) if (clean := word.strip())]
