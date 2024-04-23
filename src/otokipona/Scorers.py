# STL
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Union

# PDM
from typing_extensions import override

# LOCAL
from otokipona.Filters import Filter

Number = Union[int, float]
Weights = Dict[str, Number]


class Scorer(ABC):
    weights: Weights

    # @classmethod
    # def __score(cls, token: str, filters: List[Type[Filter]]) -> Tuple[int, Number]:
    #     for filter in filters:
    #         if not filter.filter(token):
    #             continue
    #         # NOTE: We assume the filters are ordered by their score
    #         # Thus the first match is also the highest scoring
    #         return filter.counts, cls.weights[filter.__name__]
    #         # TODO: override weight if count is 0?
    #     return 1, 0

    @classmethod
    @abstractmethod
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        raise NotImplementedError


class PassFail(Scorer):
    """The token passes any filter or fails all of them, scoring 1 or 0 respectively."""

    @classmethod
    def __score(cls, token: str, filters: List[Type[Filter]]) -> Number:
        for f in filters:
            if f.filter(token):
                return 1
        return 0

    @classmethod
    @override
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        total_score = 0
        len_tokens = len(tokens)
        for token in tokens:
            total_score += cls.__score(token, filters)
        return total_score / len_tokens if len_tokens else 0


class Scaling(Scorer):
    """
    The sooner a token matches a filter, the higher its scaling factor.
    In other words, filter order matters, weighing earlier listed filters higher than later ones.
    """

    @classmethod
    def __score(cls, token: str, filters: List[Type[Filter]], scale: int):
        for i, f in enumerate(filters):
            if f.filter(token):
                return scale - i
        return 0

    @classmethod
    @override
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        total_score = 0
        len_tokens = len(tokens)
        max_scale = len_tokens - 1
        max_score = max_scale * len_tokens
        for token in tokens:
            total_score += cls.__score(token, filters, max_scale)
        return total_score / max_score if max_score else 0


class Logarithmic(Scorer): ...


__all__ = ["PassFail"]
