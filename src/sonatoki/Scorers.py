# STL
import math
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Union

# PDM
from typing_extensions import override

# LOCAL
from sonatoki.Filters import Filter

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
        if not tokens:
            return 1

        total_score = 0
        len_tokens = len(tokens)
        for token in tokens:
            total_score += cls.__score(token, filters)
        return total_score / len_tokens if len_tokens else 0


class Scaling(Scorer):
    """
    The sooner a token matches a filter, the higher its score.
    In other words, filter order matters, weighing earlier listed filters higher than later ones.
    This is desirable to avoid messages which would only match weaker filters, as these are less likely to be Toki Pona.
    """

    @classmethod
    def score_token(cls, token: str, filters: List[Type[Filter]], scale: int):
        for i, f in enumerate(filters):
            if f.filter(token):
                return scale - i
        return 0

    @classmethod
    @override
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        if not tokens:
            return 1

        total_score = 0
        len_filters = len(filters)
        max_score = len(tokens) * len_filters
        for token in tokens:
            total_score += cls.score_token(token, filters, len_filters)
        return total_score / max_score if max_score else 0


class SoftScaling(Scaling):
    """Shorter messages are subject to less harsh scoring
    by mapping the token count to [0.5, 1.0] via the sigmoid function,
    then raising the score to the resultant power.
    For example, a single token scoring 0.64 will now score 0.8.
    """

    @staticmethod
    def sigmoid(n: int) -> Number:
        return 1 / (1 + math.exp(-(0.30 * (n - 1))))
        # n-1 makes sigmoid(1) == 0.5
        # 0.30 softens scaling against input
        # return n / (1+abs(n))   # too weak in 0.7+

    @classmethod
    @override
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        if not tokens:
            return 1

        total_score = 0
        len_filters = len(filters)
        len_tokens = len(tokens)

        max_score = len_tokens * len_filters
        for token in tokens:
            total_score += cls.score_token(token, filters, len_filters)

        percentage = total_score / max_score if max_score else 0
        percentage **= cls.sigmoid(len_tokens)
        return percentage


class Logarithmic(Scorer): ...


__all__ = ["PassFail", "Scaling", "SoftScaling"]
