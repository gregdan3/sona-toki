# STL
from copy import deepcopy
from typing import List, Type, Union, TypedDict

# LOCAL
from sonatoki.Filters import (
    Filter,
    NimiPu,
    Numeric,
    OrFilter,
    Syllabic,
    NimiLinku,
    NimiPuAle,
    NimiUCSUR,
    Alphabetic,
    ProperName,
    Phonotactic,
    Punctuation,
    NimiLinkuAle,
    NimiLinkuSandbox,
    EnglishIgnorables,
)
from sonatoki.Scorers import Number, Scorer, PassFail, SoftScaling, SoftPassFail
from sonatoki.Cleaners import Cleaner, ConsecutiveDuplicates
from sonatoki.Tokenizers import Tokenizer, WordTokenizer
from sonatoki.Preprocessors import (
    URLs,
    Reference,
    Preprocessor,
    DiscordEmotes,
    DiscordSpecial,
    DiscordChannels,
    DiscordMentions,
    AngleBracketObject,
)


class IloConfig(TypedDict):
    preprocessors: List[Type[Preprocessor]]
    word_tokenizer: Type[Tokenizer]
    cleaners: List[Type[Cleaner]]
    ignoring_filters: List[Type[Filter]]
    scoring_filters: List[Type[Filter]]
    scorer: Type[Scorer]
    passing_score: Number


# TODO: branching configs?

BaseConfig: IloConfig = {
    "preprocessors": [URLs],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [],
    "scorer": PassFail,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizer,
}


PrefConfig: IloConfig = {
    "preprocessors": [URLs, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation, EnglishIgnorables],
    "scoring_filters": [
        OrFilter(NimiLinku, NimiUCSUR),
        Syllabic,
        ProperName,
        Alphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizer,
}

CorpusConfig: IloConfig = {
    "preprocessors": [URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation, EnglishIgnorables],
    "scoring_filters": [
        OrFilter(NimiLinkuSandbox, NimiUCSUR),
        Syllabic,
        ProperName,
        Alphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizer,
}


LazyConfig: IloConfig = {
    "preprocessors": [URLs],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [Alphabetic, NimiUCSUR, ProperName],
    "scorer": SoftPassFail,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizer,
}

DiscordConfig: IloConfig = {
    "preprocessors": [URLs, AngleBracketObject, Reference],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation, EnglishIgnorables],
    "scoring_filters": [
        OrFilter(NimiLinku, NimiUCSUR),
        Syllabic,
        ProperName,
        Alphabetic,
    ],
    "scorer": SoftScaling,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizer,
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
