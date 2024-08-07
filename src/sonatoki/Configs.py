# STL
from copy import deepcopy
from typing import Set, List, Type, TypedDict, cast

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
    Phonotactic,
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

# TODO: create a mechanism to omit tokens from a filter with more granularity
__corpus_tokens_dict: Set[str] = cast(
    Set[str],
    CorpusConfig["scoring_filters"][
        0
    ].tokens,  # pyright: ignore[reportAttributeAccessIssue]
)
__corpus_tokens_dict -= {
    # Sandbox words are removed from the CorpusConfig if they appear more frequently in English than Toki Pona by a factor of at least 3.
    # In this case, all of these appear more often in English by a factor of at least 10.
    "aka",  # also known as
    "an",  # article
    "api",  # API
    "i",  # 1st person
    "kana",  # japanese script
    "me",  # 1st person
    "ne",  # "no" in several languages
    "nu",  # "new", now in dutch
    "se",  # spanish particle, "see"
    "take",  # acquire, perhaps forcefully or without permission
    "ten",  # 10
    "to",  # to, too
    "u",  # no u
    "we",  # 1st person plural
    "wi",  # wii and discussions of syllables
    "sole",  # singular, of shoe
    # unexplored candidates for removal
    # "omen",  # ominous
    # "papa",  # father
    # "lo",  # "lo" and "loo"
    # "ewe",  # sheep
    # "pa",  # father- eh?
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
