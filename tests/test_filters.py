# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from otokipona.Filters import (
    URLs,
    Spoilers,
    Backticks,
    ArrowQuote,
    DoubleQuotes,
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
    assert URLs.process(s).strip() == ""


@given(st.from_regex(Spoilers.pattern.pattern, fullmatch=True))
@example("|| | ||")
@example("|| content\n\n\ncontent ||")
@example("||\n||")
@example("|| \n|\n\n || || ||")
def test_Spoilers(s: str):
    res = Spoilers.process(s).strip()
    assert res == "", res


@given(st.from_regex(Backticks.pattern.pattern, fullmatch=True))
@example("` ` ` `")
def test_Backticks(s: str):
    res = Backticks.process(s).strip()
    assert res == "", res


@given(st.from_regex(ArrowQuote.pattern.pattern, fullmatch=True))
@example("> base")
@example("> newline\n> newline")
def test_ArrowQuote(s: str):
    res = ArrowQuote.process(s).strip()
    assert res == "", res


@given(st.from_regex(DoubleQuotes.pattern.pattern, fullmatch=True))
@example('" "" "')
@example('" "\n" "')
@example('" \n "')
def test_DoubleQuotes(s: str):
    res = DoubleQuotes.process(s).strip()
    assert res == "", res


@given(st.from_regex(SingleQuotes.pattern.pattern, fullmatch=True))
@example("' '' '")
@example("' '\n' '")
@example("' \n '")
def test_SingleQuotes(s: str):
    res = SingleQuotes.process(s).strip()
    assert res == "", res


@given(st.from_regex(DiscordEmotes.pattern.pattern, fullmatch=True))
@example("<a:example:123123>")
@example("<:example:123123>")
def test_DiscordEmotes(s: str):
    res = DiscordEmotes.process(s).strip()
    assert res == "", res
