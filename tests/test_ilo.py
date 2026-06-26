# STL
from typing import Dict, List, Tuple
from collections import defaultdict

# PDM
import pytest

# LOCAL
from sonatoki.ilo import Ilo
from sonatoki.types import Number
from tests.data.types import Transform, Performance
from tests.data.ilo_config_cases import PARAMETERIZED
from tests.data.ilo_sentence_cases import ALL_SENTENCES

REPORTS: Dict[str, List[Tuple[Transform, bool]]] = defaultdict(list)


@pytest.fixture(params=PARAMETERIZED)
def case(request: pytest.FixtureRequest) -> Ilo:
    return request.param


def credit(case: Performance, score: Number, passed: bool) -> Number:
    passing = case.config["passing_score"]
    lower = passing - case.variance
    upper = passing + case.variance

    if lower <= score <= upper:
        return 2 / 3 if passed else 1 / 3

    return 1 if passed else 0


def test_ilo(case: Performance):
    ilo = Ilo(**case.config)
    report = REPORTS[case.name]
    expected = case.score

    passing_score = case.config["passing_score"]
    total_weight = 0.0
    passed_weight = 0.0

    for sentence in ALL_SENTENCES:
        scorecard = ilo.make_scorecard(sentence.input)
        score = scorecard["score"]
        result = score >= passing_score
        passed = result == sentence.output

        multiplier = credit(case, score, passed)
        if sentence.xfail and not passed:
            continue

        report.append((sentence, passed))

        total_weight += sentence.weight
        passed_weight += sentence.weight * multiplier

    score = passed_weight / total_weight
    assert score >= expected
