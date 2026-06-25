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
    Numeric,
    NimiUCSUR,
    Alphabetic,
    NimiKuLili,
    NimiKuSuli,
    ProperName,
    Phonotactic,
    Punctuation,
    AllStopwords,
    Miscellaneous,
    NimiLinkuCore,
    NimiLinkuCommon,
    FalsePosSyllabic,
    NimiLinkuByUsage,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
    FalsePosAlphabetic,
)
from sonatoki.Scorers import (
    Scorer,
    Soften,
    PassFail,
    Weighted,
    SoftScaling,
    SoftPassFail,
)
from sonatoki.Cleaners import RECOMMENDED_CLEANERS, Cleaner, ConsecutiveDuplicates
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
    empty_passes: NotRequired[bool]
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
}

ExperimentalConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": RECOMMENDED_CLEANERS,
    "ignoring_filters": RECOMMENDED_IGNORING_FILTERS,
    "scoring_filters": [
        Len(Or(NimiLinkuCore, NimiLinkuCommon, NimiLinkuUncommon, NimiUCSUR), max=19),
        Len(Or(NimiLinkuObscure(sub=DICT_PHONOMATCHES)), min=2, max=24),
        Len(Or(NimiLinkuSandbox(sub=DICT_PHONOMATCHES), Miscellaneous), min=2, max=24),
        Len(And(Phonotactic, Not(FalsePosSyllabic)), min=3, max=24),
        Len(ProperName, min=2, max=24),
        Len(AllStopwords, max=24),
        Len(
            And(Alphabetic, Not(Or(FalsePosSyllabic, FalsePosAlphabetic))),
            min=3,
            max=24,
        ),
    ],
    "scorer": Soften(
        Weighted(
            lambda i, n: (
                1,
                0.9,
                0.8,
                0.75,
                0.5,
                -0.15,  # small penalty, but can't be certain
                0.25,
            )[i]
        )
    ),
    "passing_score": 0.8,
}


"""Mimics the previous implementation of ilo pi toki pona taso."""
LazyConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [Alphabetic, NimiUCSUR, PuName, Miscellaneous],
    "scorer": PassFail,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizerRe,  # mimics old tokenizer
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
        Len(
            And(
                Phonotactic,
                Not(
                    Or(
                        FalsePosSyllabic,
                        NimiLinkuCore,
                        NimiLinkuCommon,
                    )
                ),
            ),
            min=3,
        ),
        Len(ProperName, min=2),
        Len(And(Alphabetic, Not(FalsePosAlphabetic)), min=3),
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}


__all__ = [
    "BaseConfig",
    "CorpusConfig",
    "IloConfig",
    "LazyConfig",
    "PrefConfig",
]
