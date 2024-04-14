# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from otokipona.Validators import (
    Name,
    NimiPu,
    Syllabic,
    NimiLinku,
    Alphabetic,
    Phonotactic,
)


@given(st.from_regex(Phonotactic.pattern.pattern, fullmatch=True))
@example("n")
def test_Phonotactic(s: str):
    res = Phonotactic.is_valid(s)
    assert res


@given(st.from_regex(Syllabic.pattern.pattern, fullmatch=True))
@example("n")
def test_Syllabic(s: str):
    res = Syllabic.is_valid(s)
    assert res
