# STL
from typing import List, Type

# PDM
import pytest
import hypothesis.strategies as st
from hypothesis import given

# LOCAL
from sonatoki.Filters import (
    Filter,
    NimiPu,
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Phonotactic,
    Punctuations,
)
from sonatoki.Scorers import Scorer, Scaling, PassFail, SoftScaling

# FILESYSTEM
from .test_utils import token_strategy

FILTERS = [
    NimiPu,
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Phonotactic,
    Punctuations,
]

SCORERS = [
    PassFail,
    Scaling,
    SoftScaling,
]


@pytest.mark.parametrize("scorer", SCORERS)  # test each scorer
@given(
    st.lists(st.sampled_from(FILTERS), min_size=1, unique=True),
    st.lists(token_strategy, min_size=0, max_size=10),
)
def test_score_bounds(scorer: Scorer, filters: List[Type[Filter]], text: List[str]):
    score = scorer.score(text, filters)
    assert 0 <= score <= 1, (score, filters, text)
