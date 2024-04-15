# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from otokipona.Cleaners import ConsecutiveDuplicates
from otokipona.constants import NIMI_PU, ALPHABET, NIMI_LINKU
from otokipona.Validators import (
    Name,
    NimiPu,
    Syllabic,
    NimiLinku,
    Alphabetic,
    Phonotactic,
)


@given(st.sampled_from(NIMI_PU))
@example("lukin")
@example("selo")
@example("li")
def test_NimiPu(s: str):
    res = NimiPu.is_valid(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU))
@example("pona")
@example("tonsi")
@example("kipisi")
@example("n")
def test_NimiLinku(s: str):
    res = NimiLinku.is_valid(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU))
def test_nimi_linku_properties(s: str):
    assert ConsecutiveDuplicates.clean(s) == s, repr(s)
    assert Alphabetic.is_valid(s), repr(s)
    assert Syllabic.is_valid(s), repr(s)
    assert Phonotactic.is_valid(s), repr(s)
    # Passing phonotactic implies all of the above


@given(st.from_regex(Phonotactic.pattern.pattern, fullmatch=True))
@example("kijetesantakalu")
@example("n")
def test_Phonotactic(s: str):
    res = Phonotactic.is_valid(s)
    assert res, repr(s)


@given(st.from_regex(Syllabic.pattern.pattern, fullmatch=True))
@example("wuwojitiwunwonjintinmanna")
def test_Syllabic(s: str):
    res = Syllabic.is_valid(s)
    assert res, repr(s)


@given(st.from_regex(rf"[{ALPHABET}{ALPHABET.upper()}]+", fullmatch=True))
@example("muems")
@example("mpptp")
def test_Alphabetic(s: str):
    res = Alphabetic.is_valid(s)
    assert res, repr(s)


@given(st.from_regex(r"[A-Z][a-z]*", fullmatch=True))
def test_Name(s: str):
    res = Name.is_valid(s)
    assert res, repr(s)
