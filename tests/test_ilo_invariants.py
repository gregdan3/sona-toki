# PDM
import pytest

# LOCAL
from sonatoki.ilo import Ilo
from tests.data.types import Equal, Performance
from tests.data.ilo_config_cases import PARAMETERIZED
from tests.data.ilo_invariant_cases import CASES


@pytest.fixture(params=PARAMETERIZED)
def perf(request: pytest.FixtureRequest) -> Ilo:
    return request.param


@pytest.mark.parametrize("case", CASES)
def test_score_invariant(perf: Performance, case: Equal, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())
    ilo = Ilo(**perf.config)

    score_with = ilo.make_scorecard(case.s1)["score"]
    score_without = ilo.make_scorecard(case.s2)["score"]
    assert score_with == score_without
