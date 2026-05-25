# STL
from typing import Dict, List, Union, Literal, TypedDict

Number = Union[int, float]


# TODO: scorecard kinda sucks as a name
class Scorecard(TypedDict):
    text: str
    tokenized: List[str]
    filtered: List[str]
    cleaned: List[str]
    score: Number


LinkuUsageDate = Union[
    Literal["2020-04"],
    Literal["2021-10"],
    Literal["2022-08"],
    Literal["2023-09"],
    Literal["2024-09"],
    Literal["2025-09"],
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
    author_source: str
    book: str
    coined_era: str
    creation_date: str
    author: List[str]
    ku_data: Dict[str, int]
    see_also: List[str]
    resources: Dict[str, str]
    representations: Dict[str, Union[str, List[str]]]
    source_language: str
    usage_category: LinkuUsageCategory
    word: str
    deprecated: bool
    audio: List[Dict[str, str]]
    pu_verbatim: Dict[str, str]
    usage: Dict[LinkuUsageDate, int]
    glyph_ids: List[str]
    primary_glyph_id: str
    image: str
    svg: str
    translations: Dict[str, str]
