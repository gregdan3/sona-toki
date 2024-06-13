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
    @classmethod
    @abstractmethod
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        """Score a list of tokens using the given `Filter`s, returning a
        `Number` between 0 and 1 inclusive."""
        raise NotImplementedError


class Soften(Scorer):
    """Meta `Scorer` which scales the scores of short messages to reduce the
    impact of shortness on scoring.

    The scores of short messages are scaled by mapping the token count
    to [0.5, 1.0] via the sigmoid function, then raising the score to
    the resultant power.

    For example, a single token scoring 0.64 will score 0.8 instead.
    """

    @staticmethod
    def sigmoid(n: int) -> Number:
        return 1 / (1 + math.exp(-(0.30 * (n - 1))))
        # n-1 makes sigmoid(1) == 0.5
        # 0.30 softens scaling in favor of short input
        # return n / (1+abs(n))   # too weak in 0.7+

    @classmethod
    @override
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        percentage = super().score(tokens, filters)  # type: ignore [abstractmethod]
        len_tokens = len(tokens)
        percentage **= cls.sigmoid(len_tokens)
        return percentage

    def __new__(cls, scorer: Type[Scorer]) -> Type[Scorer]:
        class SoftenedScorer(Soften, scorer): ...

        return SoftenedScorer


class PassFail(Scorer):
    """If a token matches any filter, it scores 1.

    Otherwise, it scores 0.
    """

    @classmethod
    def score_token(cls, token: str, filters: List[Type[Filter]]) -> Number:
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
            total_score += cls.score_token(token, filters)
        return total_score / len_tokens if len_tokens else 0


class Scaling(Scorer):
    """Tokens score 1 for matching the first filter, and a linearly reduced
    amount for matching later filters based on how many filters there are.

    For example, if there are 4 filters, a token scores 1.0, 0.75, 0.50,
    and 0.25 for matching each respectively.

    In other words, filter order matters, weighing earlier listed
    filters higher than later ones. This is desirable to avoid messages
    which would only match weaker filters, as these are less likely to
    be Toki Pona.
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


class SoftPassFail(Soften, PassFail):
    """Same as `PassFail`, but shorter messages are subject to less harsh
    scoring."""


class SoftScaling(Soften, Scaling):
    """Same as `Scaling`, but shorter messages are subject to less harsh
    scoring."""


# class Logarithmic(Scorer): ...


__all__ = ["PassFail", "SoftPassFail", "Scaling", "SoftScaling"]
