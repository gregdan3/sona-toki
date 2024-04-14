# STL
import re
from abc import ABC, abstractmethod
from functools import partial

# PDM
from typing_extensions import override

CONSECUTIVE_DUPLICATES_RE = r"(.)\1+"
CONSECUTIVE_DUPLICATES_RE = re.compile(CONSECUTIVE_DUPLICATES_RE)
WORD_CLEANERS = [
    # NOTE: ORDER MATTERS
    lambda s: s.lower(),  # lowercase
    partial(re.sub, CONSECUTIVE_DUPLICATES_RE, r"\1"),  # rm consecutive duplicates
]


class Cleaner(ABC):
    @classmethod
    @abstractmethod
    def clean(cls, token: str) -> str:
        pass


class RegexCleaner(Cleaner):
    pattern: "re.Pattern[str]"
    replace: str

    @classmethod
    @override
    def clean(cls, token: str) -> str:
        return re.sub(cls.pattern, cls.replace, token)


class ConsecutiveDuplicates(RegexCleaner):
    pattern = re.compile(r"(.)\1+")
    replace = r"\1"


def clean_token(s: str, skip_dedupe=False) -> str:
    """Transform a token to better adhere to regex matching

    According to TOKEN_CLEANERS:
    - Make string lowercase
    - Remove consecutive duplicates from string
    - Remove strings matching any in COMMON_ALLOWABLES
    """
    for cleaner in WORD_CLEANERS:
        s = cleaner(s)
        if skip_dedupe:
            # WARNING: if TOKEN_CLEANERS has >2 items or order changes, FIXME
            return s
    return s
