# STL

# PDM
import hypothesis.strategies as st
from hypothesis import given, assume, example

# LOCAL
from sonatoki.Cleaners import ConsecutiveDuplicates, ConsecutiveDuplicatesRe

# FILESYSTEM
from .test_utils import overlapping_pairs


@given(st.from_regex(ConsecutiveDuplicatesRe.pattern.pattern))
@example("tooooki a")
@example("muuuuuu")
@example("nnn")
@example("")
@example("manna")  # syllabically but not phonotactically valid
def test_ConsecutiveDuplicatesRe(s: str):
    _ = assume("\n" not in s)
    res = ConsecutiveDuplicatesRe.clean(s)
    for a, b in overlapping_pairs(res):
        assert a.lower() != b.lower(), (s, res)


@given(st.from_regex(ConsecutiveDuplicatesRe.pattern.pattern))
@example("Aaa")
@example("aAa")
@example("aaA")
@example("BbbbrrrRRRUUuuuhHhHhH")
def test_ConsecutiveDuplicates(s: str):
    _ = assume("\n" not in s)
    res_re = ConsecutiveDuplicatesRe.clean(s)
    res_fn = ConsecutiveDuplicates.clean(s)
    assert res_re == res_fn, repr(s)
