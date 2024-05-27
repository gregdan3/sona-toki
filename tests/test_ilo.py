# PDM
import pytest

# LOCAL
from sonatoki.ilo import Ilo
from sonatoki.Configs import LazyConfig, PrefConfig, CorpusConfig


@pytest.fixture
def ilo() -> Ilo:
    ilo = Ilo(**PrefConfig)
    return ilo


@pytest.fixture()
def lazy_ilo() -> Ilo:
    ilo = Ilo(**LazyConfig)
    return ilo


@pytest.fixture()
def corpus_ilo() -> Ilo:
    ilo = Ilo(**CorpusConfig)
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
    "o lukin: [[w:QWERTY]]",
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

SOME_INVALID = [
    "kulupu xerox li ike",
    "mi tawa ma ohio",
    "sina toki e nimi what pi toki Inli",
    "wawa la o lukin e ni: your mom",
]

CORPUS_SPECIFIC = [
    "ki le konsi si te isipin epiku le pasila to",
    'jasima omekapo, ki nimisin "jasima enko nimisin". ki enko alu linluwi Jutu alu epiku ki epiku baba is you. ki likujo "SINtelen pona", ki epiku alu "sitelen pona". ki kepen wawajete isipin, kin ki yupekosi alu lipamanka alu wawajete, kin ki enko isipin lipamanka linluwi alu wawajete',
]


EXCESSIVE_SYLLABICS = [
    # NOTE: these are actually harder to spot bc of the EnglishIgnorables filter
    # it simply stops counting all the short english phonomatches
    # so you can use any number of them...
    "manama manama namana namana majani makala",
    "I manipulate a passe pile so a ton emulate, akin to intake",
    "a ton of insolate puke. make no amen, no joke.",
    "I elope so, to an elite untaken tune, some unwise tone",
]

EXCESSIVE_ALPHABETICS = [
    "21st",  # candidate for xfails?
    "wen i tok usin onli notes in toki pona i look silli. ",
    "I wait, I sulk, as a tool I make stoops to ineptness.",
    "aaa i non-saw usa's most multiple element-set. it's as asinine as in `e`-less speak",
    "so, to atone like papa—an awesome anon (no-name) sin man—i ate an asinine lemon-limelike tomato jalapeno isotope. 'nonsense!' amen. note to Oman: take mine katana to imitate a ninja in pantomime. atomise one nuke? 'insane misuse!' same. likewise, Susan, awaken a pepino melon in a linen pipeline. (penile) emanate semen. joke: manipulate a tame toneme to elope online tonite",
]

EXCESSIVE_TYPOES = [
    "mi pakla ln tepo mtue ls mi kn ala tok poan aun seem",
    "sina poan",
]

EXCESSIVE_NAMES = [
    "I Want To Evade The Filter",
    "If You Do This The Bot Can't See You",
    "This Is A Statement In Perfect Toki Pona, I Guarantee",
    "How to Cut a Kiwi",  # previous false positive; fixed by english ignorables
]

EXCESSIVE_ENGLISH = [
    "me when i tawa sike",  # previous false positive; fixed by english ignorables
]

NON_MATCHES = [
    "bong",
    "super bruh moment 64",
    "homestuck",
    "homestuck Homestuck",
]

KNOWN_GOOD = (
    ALL_VALID
    + SYLLABIC_MATCHES
    + ALPHABETIC_MATCHES
    + NAME_MATCHES
    + SOME_INVALID
    + IGNORABLES
)

KNOWN_BAD = (
    EXCESSIVE_SYLLABICS
    + EXCESSIVE_ALPHABETICS
    + EXCESSIVE_NAMES
    + EXCESSIVE_TYPOES
    + NON_MATCHES
)

FALSE_NEGATIVES = [
    # emoticon should not be a problem
    "lete li ike x.x",
    # a token that is one edit off a known word should be allowed
    "tok",
    "mut",
    "poan",
    "mtue",
]

FALSE_POSITIVES = [
    "Maybe I’m too nasa",
]


@pytest.mark.parametrize("text", KNOWN_GOOD)
def test_known_good(ilo: Ilo, text: str):
    assert ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_GOOD + CORPUS_SPECIFIC)
def test_known_good_for_corpus(corpus_ilo: Ilo, text: str):
    assert corpus_ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_BAD + CORPUS_SPECIFIC)
def test_known_bad(ilo: Ilo, text: str):
    assert not ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_BAD)
def test_known_bad_for_corpus(corpus_ilo: Ilo, text: str):
    assert not corpus_ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_GOOD)
def test_known_good_lazy(lazy_ilo: Ilo, text: str):
    assert lazy_ilo.is_toki_pona(text), text
    # assumption: lazy ilo should pass anything the more strict ilo does


@pytest.mark.parametrize("text", NON_MATCHES)
def test_known_bad_lazy(lazy_ilo: Ilo, text: str):
    assert not lazy_ilo.is_toki_pona(text), text


# yes this set manip is silly
@pytest.mark.parametrize("text", list(set(KNOWN_BAD) - set(NON_MATCHES)))
def test_weakness_of_lazy(lazy_ilo: Ilo, text: str):
    # NOTE: This is demonstrative, not preferential
    assert lazy_ilo.is_toki_pona(text), text


@pytest.mark.xfail
@pytest.mark.parametrize("text", FALSE_POSITIVES)
def test_false_positives(ilo: Ilo, text: str):
    assert not ilo.is_toki_pona(text)


@pytest.mark.xfail
@pytest.mark.parametrize("text", FALSE_NEGATIVES)
def test_false_negatives(ilo: Ilo, text: str):
    assert ilo.is_toki_pona(text)
