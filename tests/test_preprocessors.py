# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from sonatoki.Preprocessors import (
    URLs,
    Spoilers,
    AllQuotes,
    Backticks,
    Reference,
    ArrowQuote,
    DoubleQuotes,
    SingleQuotes,
    DiscordEmotes,
    DiscordSpecial,
    DiscordChannels,
    DiscordMentions,
    AngleBracketObject,
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
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(Backticks.pattern.pattern, fullmatch=True))
@example("` ` ` `")
def test_Backticks(s: str):
    res = Backticks.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(ArrowQuote.pattern.pattern, fullmatch=True))
@example("> base")
@example("> newline\n> newline")
def test_ArrowQuote(s: str):
    res = ArrowQuote.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DoubleQuotes.pattern.pattern, fullmatch=True))
@example('" "" "')
@example('" "\n" "')
@example('" \n "')
def test_DoubleQuotes(s: str):
    res = DoubleQuotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(SingleQuotes.pattern.pattern, fullmatch=True))
@example("' '' '")
@example("' '\n' '")
@example("' \n '")
def test_SingleQuotes(s: str):
    res = SingleQuotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordEmotes.pattern.pattern, fullmatch=True))
@example("<a:example:123123>")
@example("<:example:123123>")
def test_DiscordEmotes(s: str):
    res = DiscordEmotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordMentions.pattern.pattern, fullmatch=True))
@example("<@497549183847497739>")
@example("<@!457890000>")
@example("<@&18398198981985>")
def test_DiscordMentions(s: str):
    res = DiscordMentions.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordChannels.pattern.pattern, fullmatch=True))
@example("<#19858915>")
@example("<#18591912589812985>")
def test_DiscordChannels(s: str):
    res = DiscordChannels.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordSpecial.pattern.pattern, fullmatch=True))
@example("<id:guide>")
@example("<id:browse>")
def test_DiscordSpecial(s: str):
    res = DiscordSpecial.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(
    st.from_regex(DiscordEmotes.pattern.pattern, fullmatch=True)
    | st.from_regex(DiscordMentions.pattern.pattern, fullmatch=True)
    | st.from_regex(DiscordChannels.pattern.pattern, fullmatch=True)
    | st.from_regex(DiscordSpecial.pattern.pattern, fullmatch=True)
    | st.from_regex(AngleBracketObject.pattern.pattern, fullmatch=True)
)
@example("<https://example.com>")
@example("<#123124125125>")
def test_AngleBracketObject(s: str):
    res = AngleBracketObject.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(
    st.from_regex(SingleQuotes.pattern.pattern, fullmatch=True)
    | st.from_regex(DoubleQuotes.pattern.pattern, fullmatch=True)
    | st.from_regex(Backticks.pattern.pattern, fullmatch=True)
    | st.from_regex(ArrowQuote.pattern.pattern, fullmatch=True)
    | st.from_regex(AllQuotes.pattern.pattern, fullmatch=True)
)
@example("> bruh")
@example("`bruh`")
def test_AllQuotes(s: str):
    res = AllQuotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(Reference.pattern.pattern, fullmatch=True))
@example("[[Brainstorm]]")
@example("[[Phatic Phrases]]")
@example("[[Yahoo!]]")
def test_Reference(s: str):
    res = Reference.process(s).strip()
    assert res == "", (repr(s), repr(res))
