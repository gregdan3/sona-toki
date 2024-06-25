# STL
from copy import deepcopy
from typing import List, Type, TypedDict

# PDM
from typing_extensions import NotRequired

# LOCAL
from sonatoki.Filters import (
    Filter,
    Numeric,
    Syllabic,
    NimiUCSUR,
    Alphabetic,
    NimiKuLili,
    NimiKuSuli,
    ProperName,
    Punctuation,
    LongSyllabic,
    Miscellaneous,
    NimiLinkuCore,
    LongAlphabetic,
    LongProperName,
    OrMemberFilter,
    NimiLinkuCommon,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
)
from sonatoki.Scorers import Number, Scorer, PassFail, SoftScaling, SoftPassFail
from sonatoki.Cleaners import Cleaner, ConsecutiveDuplicates
from sonatoki.Tokenizers import Tokenizer
from sonatoki.Preprocessors import (
    URLs,
    Backticks,
    Reference,
    Preprocessor,
    AngleBracketObject,
)


class IloConfig(TypedDict):
    preprocessors: List[Type[Preprocessor]]
    cleaners: List[Type[Cleaner]]
    ignoring_filters: List[Type[Filter]]
    scoring_filters: List[Type[Filter]]
    scorer: Type[Scorer]
    passing_score: Number
    word_tokenizer: NotRequired[Type[Tokenizer]]
    sent_tokenizer: NotRequired[Type[Tokenizer]]


# TODO: branching configs? config builder?

BaseConfig: IloConfig = {
    "preprocessors": [URLs],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [],
    "scorer": PassFail,
    "passing_score": 0.8,
}


PrefConfig: IloConfig = {
    "preprocessors": [Backticks, URLs, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        OrMemberFilter(NimiLinkuCore, NimiLinkuCommon, NimiUCSUR, Miscellaneous),
        LongSyllabic,
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}

CorpusConfig: IloConfig = {
    "preprocessors": [Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        OrMemberFilter(
            NimiLinkuCore,
            NimiLinkuCommon,
            NimiLinkuUncommon,
            NimiLinkuObscure,
            NimiLinkuSandbox,
            NimiUCSUR,
            Miscellaneous,
        ),
        LongSyllabic,
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}
"""Mimics the previous implementation of ilo pi toki pona taso."""
LazyConfig: IloConfig = {
    "preprocessors": [Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [Alphabetic, NimiUCSUR, ProperName, Miscellaneous],
    "scorer": SoftPassFail,
    "passing_score": 0.8,
}
"""This is extremely silly."""
IsipinEpikuConfig: IloConfig = {
    "preprocessors": [Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        OrMemberFilter(
            NimiKuSuli,
            NimiKuLili,
            NimiLinkuUncommon,
            NimiLinkuObscure,
            NimiLinkuSandbox,
        ),
        LongSyllabic,
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}


DiscordConfig: IloConfig = {
    "preprocessors": [Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        OrMemberFilter(NimiLinkuCore, NimiLinkuCommon, NimiUCSUR, Miscellaneous),
        LongSyllabic,
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}

TelegramConfig: IloConfig = deepcopy(PrefConfig)
ForumConfig: IloConfig = deepcopy(PrefConfig)


__all__ = [
    "BaseConfig",
    "CorpusConfig",
    "DiscordConfig",
    "ForumConfig",
    "IloConfig",
    "LazyConfig",
    "PrefConfig",
    "TelegramConfig",
]
