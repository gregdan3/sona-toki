# STL
from typing import Dict, List, Tuple, Union, Literal, TypedDict

Number = Union[int, float]
# tokenized, filtered, cleaned, score, result
Scorecard = Tuple[List[str], List[str], List[str], Number, bool]
# TODO: scorecard kinda sucks as a name

LinkuUsageDate = Union[
    Literal["2020-04"],
    Literal["2021-10"],
    Literal["2022-08"],
    Literal["2023-09"],
    # Literal["2024-09"],
]

LinkuUsageCategory = Union[
    Literal["core"],
    Literal["common"],
    Literal["uncommon"],
    Literal["obscure"],
    Literal["sandbox"],
]

LinkuBooks = Union[
    Literal["pu"],
    Literal["ku suli"],
    Literal["ku lili"],
    Literal["none"],
]


class LinkuWord(TypedDict):
    id: str
    author_verbatim: str
    author_verbatim_source: str
    book: str
    coined_era: str
    coined_year: str
    creator: List[str]
    ku_data: Dict[str, int]
    see_also: List[str]
    resources: Dict[str, str]
    representations: Dict[str, Union[str, List[str]]]
    source_language: str
    usage_category: LinkuUsageCategory
    word: str
    deprecated: bool
    etymology: List[Dict[str, str]]
    audio: List[Dict[str, str]]
    pu_verbatim: Dict[str, str]
    usage: Dict[LinkuUsageDate, int]
    translations: Dict[str, Dict[str, str]]
