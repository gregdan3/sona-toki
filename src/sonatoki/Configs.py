# STL
from copy import deepcopy
from typing import List, Type, TypedDict

# PDM
from typing_extensions import NotRequired

# LOCAL
from sonatoki.Filters import (
    Or,
    And,
    Not,
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
    NimiLinkuCommon,
    FalsePosSyllabic,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
)
from sonatoki.Scorers import Number, Scorer, PassFail, SoftScaling, SoftPassFail
from sonatoki.Cleaners import Cleaner, ConsecutiveDuplicates
from sonatoki.Tokenizers import Tokenizer
from sonatoki.Preprocessors import (
    URLs,
    Emoji,
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
    "preprocessors": [Emoji, Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        Or(NimiLinkuCore, NimiLinkuCommon, NimiUCSUR, Miscellaneous),
        And(LongSyllabic, Not(FalsePosSyllabic)),
        # NOTE: These are allowed to pass name and alphabetic below, because they *could* be wrong
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}

CorpusConfig: IloConfig = {
    "preprocessors": [Emoji, Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        Or(
            NimiLinkuCore,
            NimiLinkuCommon,
            NimiLinkuUncommon,
            NimiLinkuObscure,
            NimiLinkuSandbox,
            NimiUCSUR,
            Miscellaneous,
        ),
        And(LongSyllabic, Not(FalsePosSyllabic)),
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}
"""Mimics the previous implementation of ilo pi toki pona taso."""
LazyConfig: IloConfig = {
    "preprocessors": [Emoji, Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [Alphabetic, NimiUCSUR, ProperName, Miscellaneous],
    "scorer": SoftPassFail,
    "passing_score": 0.8,
}
"""This is extremely silly."""
IsipinEpikuConfig: IloConfig = {
    "preprocessors": [Emoji, Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        Or(
            NimiKuSuli,
            NimiKuLili,
            NimiLinkuUncommon,
            NimiLinkuObscure,
            NimiLinkuSandbox,
        ),
        And(LongSyllabic, Not(FalsePosSyllabic)),
        LongProperName,
        LongAlphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}


DiscordConfig: IloConfig = {
    "preprocessors": [Emoji, Backticks, URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        Or(NimiLinkuCore, NimiLinkuCommon, NimiUCSUR, Miscellaneous),
        And(LongSyllabic, Not(FalsePosSyllabic)),
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
