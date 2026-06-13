# STL
from typing import List, Type, TypedDict

# PDM
from typing_extensions import NotRequired

# LOCAL
from sonatoki.types import Number
from sonatoki.Filters import (
    RECOMMENDED_IGNORING_FILTERS,
    Or,
    And,
    Len,
    Not,
    Filter,
    PuName,
    NimiUCSUR,
    Alphabetic,
    NimiKuLili,
    NimiKuSuli,
    ProperName,
    Phonotactic,
    Miscellaneous,
    FalsePosSyllabic,
    NimiLinkuByUsage,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
    FalsePosAlphabetic,
)
from sonatoki.Scorers import Scorer, PassFail, SoftScaling, SoftPassFail
from sonatoki.Cleaners import RECOMMENDED_CLEANERS, Cleaner
from sonatoki.constants import DICT_PHONOMATCHES
from sonatoki.Tokenizers import Tokenizer, WordTokenizerRe
from sonatoki.Preprocessors import RECOMMENDED_PREPROCESSORS, URLs, Preprocessor


class IloConfig(TypedDict):
    preprocessors: List[Type[Preprocessor]]
    cleaners: List[Type[Cleaner]]
    ignoring_filters: List[Type[Filter]]
    scoring_filters: List[Type[Filter]]
    scorer: Type[Scorer]
    passing_score: Number
    empty_passes: bool
    word_tokenizer: NotRequired[Type[Tokenizer]]
    sent_tokenizer: NotRequired[Type[Tokenizer]]


# TODO: branching configs? config builder?

BaseConfig: IloConfig = {
    "preprocessors": [URLs],
    "cleaners": RECOMMENDED_CLEANERS,
    "ignoring_filters": RECOMMENDED_IGNORING_FILTERS,
    "scoring_filters": [],
    "scorer": PassFail,
    "passing_score": 0.8,
    "empty_passes": True,
}


PrefConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": RECOMMENDED_CLEANERS,
    "ignoring_filters": RECOMMENDED_IGNORING_FILTERS,
    "scoring_filters": [
        Len(Or(NimiLinkuByUsage(30), NimiUCSUR), max=15),
        Len(And(Phonotactic, Not(FalsePosSyllabic)), min=3, max=24),
        # NOTE: These are allowed to pass name and alphabetic below, because they *could* be wrong
        Len(ProperName, min=2, max=24),
        Len(
            And(Alphabetic, Not(Or(FalsePosSyllabic, FalsePosAlphabetic))),
            min=3,
            max=24,
        ),
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
    "empty_passes": True,
}

"""Intended for use in collecting data with ilo Muni."""
CorpusConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": RECOMMENDED_CLEANERS,
    "ignoring_filters": RECOMMENDED_IGNORING_FILTERS,
    "scoring_filters": [
        Len(
            Or(
                # awkward but efficient syntax
                NimiLinkuByUsage(0)(sub=DICT_PHONOMATCHES),
                NimiUCSUR,
                Miscellaneous,
            ),
            max=19,
        ),
        Len(And(Phonotactic, Not(FalsePosSyllabic)), min=3, max=24),
        Len(ProperName, min=2, max=24),
        Len(
            And(Alphabetic, Not(Or(FalsePosSyllabic, FalsePosAlphabetic))),
            min=3,
            max=24,
        ),
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
    "empty_passes": True,  # my client doesn't fail empty sentences; it just omits them
}
"""Mimics the previous implementation of ilo pi toki pona taso."""
LazyConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": RECOMMENDED_CLEANERS,
    "ignoring_filters": RECOMMENDED_IGNORING_FILTERS,
    "scoring_filters": [Alphabetic, NimiUCSUR, PuName, Miscellaneous],
    "scorer": SoftPassFail,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizerRe,  # mimics old tokenizer
    "empty_passes": True,
}
"""This is extremely silly."""
IsipinEpikuConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": RECOMMENDED_CLEANERS,
    "ignoring_filters": RECOMMENDED_IGNORING_FILTERS,
    "scoring_filters": [
        Or(
            NimiKuSuli,
            NimiKuLili,
            NimiLinkuUncommon,
            NimiLinkuObscure,
            NimiLinkuSandbox,
        ),
        Len(And(Phonotactic, Not(FalsePosSyllabic)), min=3),
        Len(ProperName, min=2),
        Len(And(Alphabetic, Not(FalsePosAlphabetic)), min=3),
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
    "empty_passes": True,
}


__all__ = [
    "BaseConfig",
    "CorpusConfig",
    "IloConfig",
    "LazyConfig",
    "PrefConfig",
]
