# STL
from typing import List, Type

# PDM
import pytest
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from sonatoki.Filters import (
    Filter,
    NimiPu,
    Numeric,
    Syllabic,
    Alphabetic,
    ProperName,
    Phonotactic,
    NimiLinkuCore,
    PunctuationRe,
    NimiLinkuCommon,
)
from sonatoki.Scorers import Scorer, Scaling, PassFail, SoftScaling, SoftPassFail

# FILESYSTEM
from .test_utils import token_strategy

FILTERS = [
    NimiPu,
    Numeric,
    Syllabic,
    NimiLinkuCore,
    NimiLinkuCommon,
    Alphabetic,
    ProperName,
    Phonotactic,
    PunctuationRe,
]

SCORERS = [
    PassFail,
    SoftPassFail,
    Scaling,
    SoftScaling,
]


@pytest.mark.parametrize("scorer", SCORERS)  # test each scorer
@given(
    st.lists(st.sampled_from(FILTERS), min_size=1, unique=True),
    st.lists(token_strategy, min_size=0, max_size=10),
)
@example(st.sampled_from(FILTERS), [])
def test_score_bounds(scorer: Scorer, filters: List[Type[Filter]], text: List[str]):
    score = scorer.score(text, filters)
    assert 0 <= score <= 1, (score, filters, text)
