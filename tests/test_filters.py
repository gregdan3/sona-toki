# STL
import string

# PDM
import regex as re
import hypothesis.strategies as st
from hypothesis import HealthCheck, given, assume, example, settings

# LOCAL
from otokipona.Filters import (
    URLs,
    Numerics,
    Spoilers,
    Backticks,
    ArrowQuote,
    DoubleQuotes,
    Punctuations,
    SingleQuotes,
    DiscordEmotes,
)


@given(st.from_regex(URLs.pattern.pattern, fullmatch=True))
@example("https://google.com")
@example("https://mun.la")
@example("https://discord.gg/")
@example("http://example.com")
@example("http://localhost:80")
def test_URLs(s: str):
    assert URLs.filter(s).strip() == ""


@given(st.from_regex(r"\d+", fullmatch=True))
@example("124125")
@example("99990000")
def test_Numeric(s: str):
    res = Numerics.filter(s)
    for c in res:
        assert not c.isdigit()
    # assert res == "", (repr(s), repr(res))


@given(st.from_regex(Spoilers.pattern.pattern, fullmatch=True))
@example("|| | ||")
@example("|| content\n\n\ncontent ||")
@example("||\n||")
@example("|| \n|\n\n || || ||")
def test_Spoilers(s: str):
    res = Spoilers.filter(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(Backticks.pattern.pattern, fullmatch=True))
@example("` ` ` `")
def test_Backticks(s: str):
    res = Backticks.filter(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(ArrowQuote.pattern.pattern, fullmatch=True))
@example("> base")
@example("> newline\n> newline")
def test_ArrowQuote(s: str):
    res = ArrowQuote.filter(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DoubleQuotes.pattern.pattern, fullmatch=True))
@example('" "" "')
@example('" "\n" "')
@example('" \n "')
def test_DoubleQuotes(s: str):
    res = DoubleQuotes.filter(s).strip()
    assert res == "", (repr(s), repr(res))


# I use `regex`'s Unicode property feature, which Hypothesis doesn't understand
# So I have to provide a different regex tha doesn't technically match
@given(st.from_regex(rf"[^\w\s]+", fullmatch=True))
@example("⟨·⟩")
@example("…")
@example("「　」")
@example(string.punctuation)
@settings(suppress_health_check=[HealthCheck.filter_too_much])  # FIXME
def test_Punctuations(s: str):
    _ = assume(re.fullmatch(Punctuations.pattern.pattern, s))
    res = Punctuations.filter(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(SingleQuotes.pattern.pattern, fullmatch=True))
@example("' '' '")
@example("' '\n' '")
@example("' \n '")
def test_SingleQuotes(s: str):
    res = SingleQuotes.filter(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordEmotes.pattern.pattern, fullmatch=True))
@example("<a:example:123123>")
@example("<:example:123123>")
def test_DiscordEmotes(s: str):
    res = DiscordEmotes.filter(s).strip()
    assert res == "", (repr(s), repr(res))
