# STL

# PDM
import hypothesis.strategies as st
from hypothesis import assume, given, example, reproduce_failure

# LOCAL
from sonatoki.Cleaners import ConsecutiveDuplicates

# FILESYSTEM
from .test_utils import overlapping_pairs


@given(st.from_regex(ConsecutiveDuplicates.pattern.pattern))
@example("tooooki a")
@example("muuuuuu")
@example("nnn")
@example("")
@example(
    "manna"
)  # syllabically valid, but not phonotactically valid; errantly matches phonotactic filter after this cleaner
def test_ConsecutiveDuplicates(s: str):
    _ = assume("\n" not in s)
    res = ConsecutiveDuplicates.clean(s)
    for a, b in overlapping_pairs(res):
        assert a != b, (s, res)
