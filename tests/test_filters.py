# STL
import string

# PDM
import regex as re
import hypothesis.strategies as st
from hypothesis import HealthCheck, given, assume, example, settings

# LOCAL
from sonatoki.Filters import (
    NimiPu,
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Phonotactic,
    Punctuations,
)
from sonatoki.Cleaners import ConsecutiveDuplicates
from sonatoki.constants import NIMI_PU, NIMI_LINKU

# FILESYSTEM
from .test_utils import ALPHABETIC_RE, PROPER_NAME_RE


@given(st.sampled_from(NIMI_PU))
@example("lukin")
@example("selo")
@example("li")
def test_NimiPu(s: str):
    res = NimiPu.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU))
@example("pona")
@example("tonsi")
@example("kipisi")
@example("n")
def test_NimiLinku(s: str):
    res = NimiLinku.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU))
def test_nimi_linku_properties(s: str):
    assert ConsecutiveDuplicates.clean(s) == s, repr(s)
    assert Alphabetic.filter(s), repr(s)
    assert Syllabic.filter(s), repr(s)
    assert Phonotactic.filter(s), repr(s)
    # Passing phonotactic implies all of the above


@given(st.from_regex(Phonotactic.pattern.pattern, fullmatch=True))
@example("kijetesantakalu")
@example("n")
def test_Phonotactic(s: str):
    res = Phonotactic.filter(s)
    assert res, repr(s)


@given(st.from_regex(Syllabic.pattern.pattern, fullmatch=True))
@example("wuwojitiwunwonjintinmanna")
def test_Syllabic(s: str):
    res = Syllabic.filter(s)
    assert res, repr(s)


@given(st.from_regex(ALPHABETIC_RE, fullmatch=True))
@example("muems")
@example("mpptp")
@example("tptpt")
def test_Alphabetic(s: str):
    res = Alphabetic.filter(s)
    assert res, repr(s)


@given(st.from_regex(PROPER_NAME_RE, fullmatch=True))
def test_ProperName(s: str):
    res = ProperName.filter(s)
    assert res, repr(s)


# I use `regex`'s Unicode property feature, which Hypothesis doesn't understand
# So I have to provide a different regex tha doesn't technically match
@given(st.from_regex(r"[^\w\s]+", fullmatch=True))
@example("⟨·⟩")
@example("…")
@example("「　」")
@example(string.punctuation)
@settings(suppress_health_check=[HealthCheck.filter_too_much])  # FIXME
def test_Punctuations(s: str):
    _ = assume(re.fullmatch(Punctuations.pattern.pattern, s))
    res = Punctuations.filter(s)
    assert res, repr(s)


@given(st.from_regex(r"\d+", fullmatch=True))
@example("124125")
@example("99990000")
def test_Numeric(s: str):
    res = Numerics.filter(s)
    assert res, repr(s)
