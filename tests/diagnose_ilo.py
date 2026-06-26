# PDM
import pytest

# LOCAL
from sonatoki.ilo import Ilo
from tests.data.types import Transform, Performance
from tests.data.ilo_config_cases import PARAMETERIZED
from tests.data.ilo_sentence_cases import ALL_SENTENCES


@pytest.fixture(params=PARAMETERIZED)
def case(request: pytest.FixtureRequest) -> Ilo:
    return request.param


@pytest.mark.parametrize("sentence", ALL_SENTENCES)
def test_ilo(case: Performance, sentence: Transform):
    ilo = Ilo(**case.config)
    result = ilo.is_toki_pona(sentence.input)
    label = (sentence.name, sentence.input) if sentence.name else sentence.input
    assert result == sentence.output, (case.name, label)
