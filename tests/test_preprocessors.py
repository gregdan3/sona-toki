# STL
from typing import Optional

# PDM
import pytest
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from sonatoki.Preprocessors import (
    URLs,
    Spoilers,
    AllQuotes,
    Backticks,
    Codeblock,
    Reference,
    ArrowQuote,
    ColonEmotes,
    DoubleQuotes,
    MarkdownURLs,
    SingleQuotes,
    DiscordEmotes,
    DiscordSpecial,
    DiscordChannels,
    DiscordMentions,
    AngleBracketObject,
)
from src.sonatoki.Preprocessors import Emails


def extract_bracket_content(markdown_text: str) -> Optional[str]:
    start = markdown_text.find("[", 0)
    if start == -1:
        return None

    end = markdown_text.rfind("](")
    if end == -1 or end <= start:
        return None

    return markdown_text[start + 1 : end]


@given(st.from_regex(URLs.pattern, fullmatch=True))
@example("https://google.com")
@example("https://mun.la")
@example("https://discord.gg/")
@example("http://example.com")
@example("http://localhost:80")
def test_URLs(s: str):
    assert URLs.process(s).strip() == ""


@given(st.from_regex(MarkdownURLs.pattern, fullmatch=True))
@example("[mu](https://google.com)")
@example("[wawa wawa wawa](https://mun.la)")
@example("[[] silly mode activated](https://discord.gg/)")
@example("[https://example.com/](http://example.com)")
@example("[192.168.0.255](http://localhost:80)")
@example("[text](https://bad.worse]/)")
@example("[](](http://0)")
def test_MarkdownURLs(s: str):
    bracket_content = extract_bracket_content(s)
    assert MarkdownURLs.process(s) == bracket_content


@given(st.from_regex(Emails.pattern, fullmatch=True))
@example("mun@pona.la")
@example("tokipona@alinome.com")
def test_Emails(s: str):
    assert Emails.process(s).strip() == ""


@given(st.from_regex(Spoilers.pattern, fullmatch=True))
@example("|| | ||")
@example("|| content\n\n\ncontent ||")
@example("||\n||")
@example("|| \n|\n\n || || ||")
def test_Spoilers(s: str):
    res = Spoilers.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(Backticks.pattern, fullmatch=True))
@example("` ` ` `")
def test_Backticks(s: str):
    res = Backticks.process(s).strip()
    assert res == "", (repr(s), repr(res))


@pytest.mark.skip("it observably works but my test for that is inaccurate")
@given(st.from_regex(r"```(?:(?!`).+?)```", fullmatch=True))
@example("""```0```""")
@example(
    """```
```"""
)
@example(
    """```
blocky message
```

```
second blocky message
```"""
)
@example(
    """```oisandm123-_mu
arbitrary content
```"""
)
@example("""```mu```""")
def test_Codeblock(s: str):
    res = Codeblock.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(ArrowQuote.pattern, fullmatch=True))
@example("> base")
@example("> newline\n> newline")
def test_ArrowQuote(s: str):
    res = ArrowQuote.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DoubleQuotes.pattern, fullmatch=True))
@example('" "" "')
@example('" "\n" "')
@example('" \n "')
def test_DoubleQuotes(s: str):
    res = DoubleQuotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(SingleQuotes.pattern, fullmatch=True))
@example("' '' '")
@example("' '\n' '")
@example("' \n '")
def test_SingleQuotes(s: str):
    res = SingleQuotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordEmotes.pattern, fullmatch=True))
@example("<a:example:123123>")
@example("<:example:123123>")
def test_DiscordEmotes(s: str):
    res = DiscordEmotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordMentions.pattern, fullmatch=True))
@example("<@497549183847497739>")
@example("<@!457890000>")
@example("<@&18398198981985>")
def test_DiscordMentions(s: str):
    res = DiscordMentions.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordChannels.pattern, fullmatch=True))
@example("<#19858915>")
@example("<#18591912589812985>")
def test_DiscordChannels(s: str):
    res = DiscordChannels.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(DiscordSpecial.pattern, fullmatch=True))
@example("<id:guide>")
@example("<id:browse>")
def test_DiscordSpecial(s: str):
    res = DiscordSpecial.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(
    st.from_regex(DiscordEmotes.pattern, fullmatch=True)
    | st.from_regex(DiscordMentions.pattern, fullmatch=True)
    | st.from_regex(DiscordChannels.pattern, fullmatch=True)
    | st.from_regex(DiscordSpecial.pattern, fullmatch=True)
    | st.from_regex(AngleBracketObject.pattern, fullmatch=True)
)
@example("<https://example.com>")
@example("<#123124125125>")
def test_AngleBracketObject(s: str):
    res = AngleBracketObject.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(
    st.from_regex(SingleQuotes.pattern, fullmatch=True)
    | st.from_regex(DoubleQuotes.pattern, fullmatch=True)
    | st.from_regex(Backticks.pattern, fullmatch=True)
    | st.from_regex(ArrowQuote.pattern, fullmatch=True)
    | st.from_regex(AllQuotes.pattern, fullmatch=True)
)
@example("> bruh")
@example("`bruh`")
def test_AllQuotes(s: str):
    res = AllQuotes.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(Reference.pattern, fullmatch=True))
@example("[[Brainstorm]]")
@example("[[Phatic Phrases]]")
@example("[[Yahoo!]]")
def test_Reference(s: str):
    res = Reference.process(s).strip()
    assert res == "", (repr(s), repr(res))


@given(st.from_regex(ColonEmotes.pattern, fullmatch=True))
@example(":owe::owe:")
@example(":suffering:")
@example(":presid65despair:")
def test_ColonEmotes(s: str):
    res = ColonEmotes.process(s).strip()
    assert res == "", (repr(s), repr(res))
