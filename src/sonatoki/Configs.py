# STL
from typing import List, Type, TypedDict

# PDM
from typing_extensions import NotRequired

# LOCAL
from sonatoki.types import Number
from sonatoki.Filters import (
    Or,
    And,
    Len,
    Not,
    Filter,
    PuName,
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
    LongAlphabetic,
    LongProperName,
    FalsePosSyllabic,
    NimiLinkuByUsage,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
    FalsePosAlphabetic,
)
from sonatoki.Scorers import Scorer, Soften, Voting, PassFail, SoftScaling, SoftPassFail
from sonatoki.Cleaners import Cleaner, ConsecutiveDuplicates
from sonatoki.Tokenizers import Tokenizer, WordTokenizerRe
from sonatoki.Preprocessors import (
    RECOMMENDED_PREPROCESSORS,
    URLs,
    Emoji,
    Codeblock,
    Reference,
    Preprocessor,
    AngleBracketObject,
)

__DICT_PHONOMATCHES = {
    # Sandbox words are removed from the CorpusConfig if they appear more frequently in English than Toki Pona by a factor of at least 3.
    # In this case, all of these appear more often in English by a factor of at least 10.
    "aka",  # also known as
    "an",  # article
    "api",  # API
    "i",  # 1st person
    "je",  # 1st person pronoun, french
    "kana",  # japanese script
    "me",  # 1st person singular, english
    "ne",  # "no" in several languages
    "nu",  # "new" in english, "now" in dutch
    "omen",  # ominous
    "se",  # spanish particle, english "see"
    "sole",  # singular, of shoe
    "take",  # acquire, perhaps forcefully or without permission
    "ten",  # 10
    "to",  # to, too
    "u",  # no u
    "we",  # 1st person plural, english
    "wi",  # wii and discussions of syllables
    # unexplored candidates for removal
    # "papa",  # father
    # "lo",  # "lo" and "loo"
    # "ewe",  # sheep
    # "pa",  # father- eh?
}


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
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        Len(Or(NimiLinkuByUsage(30), NimiUCSUR), max=15),
        Len(And(Syllabic, Not(FalsePosSyllabic)), min=3, max=24),
        # NOTE: These are allowed to pass name and alphabetic below, because they *could* be wrong
        Len(ProperName, min=2, max=24),
        Len(And(Alphabetic, Not(FalsePosAlphabetic)), min=3, max=24),
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}

CorpusConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [
        Len(
            Or(
                # awkward but efficient syntax
                NimiLinkuByUsage(0)(sub=__DICT_PHONOMATCHES),
                NimiUCSUR,
                Miscellaneous,
            ),
            max=19,
        ),
        Len(And(Syllabic, Not(FalsePosSyllabic)), min=3, max=24),
        Len(ProperName, min=2, max=24),
        Len(And(Alphabetic, Not(FalsePosAlphabetic)), min=3, max=24),
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
}
"""Mimics the previous implementation of ilo pi toki pona taso."""
LazyConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [Alphabetic, NimiUCSUR, PuName, Miscellaneous],
    "scorer": SoftPassFail,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizerRe,  # mimics old tokenizer
}
"""This is extremely silly."""
IsipinEpikuConfig: IloConfig = {
    "preprocessors": RECOMMENDED_PREPROCESSORS,
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
        And(LongAlphabetic, Not(FalsePosAlphabetic)),
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
