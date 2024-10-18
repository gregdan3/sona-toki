# STL
import math
from abc import ABC, abstractmethod
from typing import List, Type

# PDM
from typing_extensions import override

# LOCAL
from sonatoki.types import Number, Scorecard
from sonatoki.Filters import Pass, Filter


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


class Voting(Scaling):
    """Derives from `Scaling` in assigning scores from 0 to 1 based on the
    first matching filter out of the list of filters. However, after all scores
    are derived, each token scoring less than the threshold is assigned the
    average score of its nearest 3 neighbors. The default threshold is 0.

    If there are 3 or fewer tokens, this scorer is identical to the
    Scaling scorer.

    If the Voting scorer is created with a Filter, tokens must also
    match that filter to be considered for voting. For example, the
    following Voting filter would only check words with a score of 0.3
    or less that still match the Syllabic filter: `Voting(Syllabic, 0.3)`
    """

    prereq: Type[Filter] = Pass
    threshold: int = 0

    def __new__(cls, filter: Type[Filter], threshold_: int = 0) -> Type[Scorer]:
        class AnonVoting(Voting):
            prereq = filter
            threshold = threshold_

        return AnonVoting

    @classmethod
    @override
    def score(cls, tokens: List[str], filters: List[Type[Filter]]) -> Number:
        if not tokens:
            return 1

        if len(tokens) < 4:
            return super().score(tokens, filters)

        len_filters = len(filters)
        max_score = len(tokens) * len_filters

        # score_token only emits ints
        # but the averaging emits floats
        # it doesn't really matter as long as no score exceeds len_filters
        scores: List[Number] = []
        for token in tokens:
            score = cls.score_token(token, filters, len_filters)
            scores.append(score)

        # only consider scores from before voting
        copied_scores = scores[:]
        for i, (token, score) in enumerate(zip(tokens, copied_scores)):
            if score > cls.threshold:
                continue
            if not cls.prereq.filter(token):
                continue

            # TODO: this is kinda dumb.
            # we want to get exactly 3 neighbors, favoring 2 before and 1 after
            # the way i'm doing this is both bad and slow as hell
            start = max(i - 2, 0)
            end = min(i + 1, len(scores) - 1)
            neighbors = copied_scores[start:i] + copied_scores[i + 1 : end + 1]
            scores[i] = sum(neighbors) / len(neighbors)

        total_score = sum(scores)

        return total_score / max_score if max_score else 0


class SoftPassFail(Soften, PassFail):
    """Same as `PassFail`, but shorter messages are subject to less harsh
    scoring."""


class SoftScaling(Soften, Scaling):
    """Same as `Scaling`, but shorter messages are subject to less harsh
    scoring."""


class SoftVoting(Soften, Voting):
    """Same as `Voting`, but shorter messages are subject to less harsh
    scoring."""


class SentenceScorer(ABC):
    @classmethod
    @abstractmethod
    def score(cls, scorecards: List[Scorecard]) -> List[Scorecard]:
        """Re-score a list of sentences (scorecards, sentences with all their
        metadata) and return them."""
        raise NotImplementedError


class SentNoOp(SentenceScorer):
    @classmethod
    @override
    def score(cls, scorecards: List[Scorecard]) -> List[Scorecard]:
        return scorecards


class SentAvg(SentenceScorer):
    @classmethod
    @override
    def score(cls, scorecards: List[Scorecard]) -> List[Scorecard]:
        if not scorecards:
            return scorecards

        total = sum(card["score"] for card in scorecards)
        avg = total / len(scorecards)
        for card in scorecards:
            card["score"] = avg
        return scorecards


class SentWeightedAvg(SentenceScorer):
    @classmethod
    @override
    def score(cls, scorecards: List[Scorecard]) -> List[Scorecard]:
        if not scorecards:
            return scorecards

        weighted_total = 0
        total_len = 0
        for card in scorecards:
            cardlen = len(card["cleaned"])
            cardscore = card["score"]

            weighted_total += cardlen * cardscore
            total_len += cardlen

        weighted_avg = weighted_total / total_len
        for card in scorecards:
            card["score"] = weighted_avg
        return scorecards


__all__ = [
    "PassFail",
    "Scaling",
    "SoftPassFail",
    "SoftScaling",
    "Soften",
    "SentAvg",
    "SentWeightedAvg",
]
