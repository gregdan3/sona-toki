# PDM
import pytest

# LOCAL
from sonatoki.ilo import Ilo
from sonatoki.Configs import LazyConfig, PrefConfig


@pytest.fixture
def ilo():
    ilo = Ilo(**PrefConfig)
    # ilo.logging_threshold = 0.8
    return ilo


@pytest.fixture()
def lazy_ilo():
    ilo = Ilo(**LazyConfig)
    # ilo.logging_threshold = 0.8
    return ilo


ALL_VALID = [
    "mi unpa e mama sina",
    "mama sina li lon seme? mi wile toki tawa ona",
    "sina sike pakala",
    "    sina    seme     e     mi     ?",
    "AAAAAAAAAAA",
    "muuuu MUUU muUuUuU",
    "wawa mute. " * 10,
]

IGNORABLES = [
    "",
    " ",
    "2+2=5",
    "kiwen moli 42",
    "https://mun.la/sona",
    "https://example.com/",
    "mi wile e ni: <https://example.com> li pona",
    "lipu https://example.com li kama pona",
    "...",
    " ⟨·⟩, a",
    "·····",
]

SYLLABIC_MATCHES = [
    "ni li tenpo penpo",
    "sipisi",
    "walawa malama walama malama mupi",
    "mi sona ala e nimi sunopatikuna",
    "kalama wuwojiti li pana e sona",
    "jan Awaja en jan Alasali en jan Akesinu li pona",  # syllables match before names here
]

ALPHABETIC_MATCHES = [
    "mi mtue o kama sona",
    "mi mute o kma son",
    "ni li tptpt",
    "mi wile pana lon sptp",
    "tmo tawa mi li pona mute la mi kepeken ona lon tenpo mute",
    "mi pakla lon nimi pi mute lili, taso ale li pona tan ni: mi toki mute",
]

NAME_MATCHES = [
    "musi Homestuck li ike tawa mi",
    "ilo Google li sona ala e nimi Emoticon la mi wile utala e ona",
    "toki Kanse li lon",
    "toki Lojban li nasa e lawa mi",
]

SOME_INVALID = ["kulupu xerox li ike", "mi tawa ma ohio"]


EXCESSIVE_SYLLABICS = [
    "manama manama namana namana majani makala",
]

EXCESSIVE_ALPHABETICS = [
    "21st",  # candidate for xfails?
    "tok",
    "mut",
    "mtue",
    "I wait, I sulk, as a tool I make stoops to ineptness.",
    "aaa i non-saw usa's most multiple element-set. it's as asinine as in `e`-less speak",
    "mi pakla ln tepo mtue ls mi kn ala tok poan aun seem",
    "so, to atone like papa—an awesome anon (no-name) sin man—i ate an asinine lemon-limelike tomato jalapeno isotope. 'nonsense!' amen. note to Oman: take mine katana to imitate a ninja in pantomime. atomise one nuke? 'insane misuse!' same. likewise, Susan, awaken a pepino melon in a linen pipeline. (penile) emanate semen. joke: manipulate a tame toneme to elope online tonite",
]

EXCESSIVE_NAMES = [
    "I Want To Evade The Filter",
    "If You Do This The Bot Can't See You",
    "This Is A Statement In Perfect Toki Pona, I Guarantee",
]

NON_MATCHES = [
    "bong",
    "super bruh moment 64",
    "homestuck",
    "homestuck Homestuck",
]

XFAILS = [
    "lete li ike x.x",  # emoticon should not be a problem
]


@pytest.mark.parametrize(
    "text",
    ALL_VALID
    + SYLLABIC_MATCHES
    + ALPHABETIC_MATCHES
    + NAME_MATCHES
    + SOME_INVALID
    + IGNORABLES,
)
def test_known_good(ilo: Ilo, lazy_ilo: Ilo, text: str):
    assert ilo.is_toki_pona(text), text


@pytest.mark.parametrize(
    "text", EXCESSIVE_SYLLABICS + EXCESSIVE_ALPHABETICS + EXCESSIVE_NAMES + NON_MATCHES
)
def test_known_bad(ilo: Ilo, text: str):
    assert not ilo.is_toki_pona(text), text


@pytest.mark.parametrize(
    "text",
    ALL_VALID
    + SYLLABIC_MATCHES
    + ALPHABETIC_MATCHES
    + NAME_MATCHES
    + SOME_INVALID
    + IGNORABLES,
)
def test_known_good_lazy(lazy_ilo: Ilo, text: str):
    assert lazy_ilo.is_toki_pona(text), text
    # assumption: lazy ilo should pass anything the more strict ilo does


@pytest.mark.parametrize("text", NON_MATCHES)
def test_known_bad_lazy(lazy_ilo: Ilo, text: str):
    assert not lazy_ilo.is_toki_pona(text), text


@pytest.mark.parametrize(
    "text", EXCESSIVE_SYLLABICS + EXCESSIVE_ALPHABETICS + EXCESSIVE_NAMES
)
def test_weakness_of_lazy(lazy_ilo: Ilo, text: str):
    # NOTE: This is demonstrative, not preferential
    assert lazy_ilo.is_toki_pona(text), text


@pytest.mark.xfail
@pytest.mark.parametrize("text", XFAILS)
def test_known_xfails(ilo: Ilo, text: str):
    assert ilo.is_toki_pona(text)
