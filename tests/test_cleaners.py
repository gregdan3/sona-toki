# STL

# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from otokipona.Cleaners import ConsecutiveDuplicates

# FILESYSTEM
from .test_utils import overlapping_pairs


@given(st.from_regex(ConsecutiveDuplicates.pattern.pattern))
@example("tooooki a")
@example("muuuuuu")
@example("nnn")
@example("")
def test_ConsecutiveDuplicates(s: str):
    res = ConsecutiveDuplicates.clean(s)
    for a, b in overlapping_pairs(res):
        assert a != b, (s, res)
