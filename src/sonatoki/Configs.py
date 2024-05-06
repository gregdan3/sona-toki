# STL
from copy import deepcopy
from typing import List, Type, TypedDict

# PDM
from typing_extensions import NotRequired

# LOCAL
from sonatoki.Filters import (
    Filter,
    NimiPu,
    Numeric,
    Syllabic,
    NimiLinku,
    NimiPuAle,
    Alphabetic,
    ProperName,
    Phonotactic,
    Punctuation,
    NimiLinkuAle,
)
from sonatoki.Scorers import Number, Scorer, PassFail, SoftScaling, SoftPassFail
from sonatoki.Cleaners import Cleaner, ConsecutiveDuplicates
from sonatoki.Tokenizers import Tokenizer, WordTokenizerTok
from sonatoki.Preprocessors import (
    URLs,
    Preprocessor,
    DiscordEmotes,
    DiscordSpecial,
    DiscordChannels,
    DiscordMentions,
)


class IloConfig(TypedDict):
    preprocessors: List[Type[Preprocessor]]
    word_tokenizer: Type[Tokenizer]
    cleaners: List[Type[Cleaner]]
    ignoring_filters: List[Type[Filter]]
    scoring_filters: List[Type[Filter]]
    scorer: Type[Scorer]
    passing_score: Number


BaseConfig: IloConfig = {
    "preprocessors": [URLs],
    "cleaners": [ConsecutiveDuplicates],
    "ignoring_filters": [Numeric, Punctuation],
    "scoring_filters": [],
    "scorer": PassFail,
    "passing_score": 0.8,
    "word_tokenizer": WordTokenizerTok,
}


PrefConfig: IloConfig = deepcopy(BaseConfig)
PrefConfig["scoring_filters"].extend([NimiLinku, Syllabic, ProperName, Alphabetic])
PrefConfig["scorer"] = SoftScaling


LazyConfig: IloConfig = deepcopy(BaseConfig)
LazyConfig["scoring_filters"].extend([Alphabetic, ProperName])
LazyConfig["scorer"] = SoftPassFail

DiscordConfig: IloConfig = deepcopy(PrefConfig)
DiscordConfig["preprocessors"].extend(
    [DiscordEmotes, DiscordMentions, DiscordChannels, DiscordSpecial]
)
TelegramConfig: IloConfig = deepcopy(PrefConfig)
ForumConfig: IloConfig = deepcopy(PrefConfig)

__all__ = [
    "IloConfig",
    "BaseConfig",
    "PrefConfig",
    "LazyConfig",
    "DiscordConfig",
    "TelegramConfig",
    "ForumConfig",
]
