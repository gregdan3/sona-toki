# STL
import itertools

# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from otokipona.Cleaners import ConsecutiveDuplicates


def overlapping_pairs(iterable: str):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    _ = next(b, None)
    return zip(a, b)


@given(st.from_regex(ConsecutiveDuplicates.pattern.pattern))
@example("tooooki a")
@example("muuuuuu")
@example("nnn")
@example("")
def test_consecutive_duplicates(s: str):
    res = ConsecutiveDuplicates.clean(s)
    for a, b in overlapping_pairs(res):
        assert a != b, (s, res)
