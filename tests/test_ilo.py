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
    "󱥄󱥬󱥩󱤴",  # "o toki tawa mi" in UCSUR
    "󱤴󱤧󱤑󱥍󱦗󱤖󱥡󱦘󱤬󱥭‍󱥡󱥚",
    "󱤑󱦐󱥗󱦜󱦈󱦜󱥉󱦜󱦑󱥄󱤤󱤂󱤉󱥆󱤀",
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
    "nasa la mi ken pana e ni: <unrelated_words_that_are_illegal>",
    "❤️",  # heart
    "😊",
    "👨‍👩‍👧‍👧",  # family emoji with zwj
    # every non-emoji in
    "🄀🄁🄂🄃🄄🄅🄆🄇🄈🄉🄊🄋🄌🄍🄎🄏🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩🄪🄫🄬🄭🄮🄯🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅊🅋🅌🅍🅎🅏🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅪🅫🅬🅭🅮🅯🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🆊🆋🆌🆍🆏🆐 🆛🆜🆝🆞🆟🆠🆡🆢🆣🆤🆥🆦🆧🆨🆩🆪🆫🆬🆭🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿",
    "🅰️🅱️🅾️🅱️🅰️",  # blood type emojis
    # "😃⃢👍",  # sincerely, no idea, but it came up
]

SYLLABIC_MATCHES = [
    "ni li tenpo penpo",
    "sipisi",
    "walawa malama walama malama mupi",
    "mi sona ala e nimi sunopatikuna",
    "kalama wuwojiti li pana e sona",
    "jan Awaja en jan Alasali en jan Akesinu li pona",  # syllables match before names here
    "jan Ke Tami",
    "kulupu Kuko",
]

ALPHABETIC_MATCHES = [
    "mi mtue o kama sona",
    "mi mute o kma son",  # this one is odd because `son` is an unintended phonetic match
    "mi mute o kama kne snoa a",
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
    "ilo Firefox",
    "mi musi Space Station 13",
]

SOME_INVALID = [
    "󱤎󱥁󱤡󱥀󱤬󱥚󱥁󱤧󱤬󱦜󱤬󱥆󱤡󱥞󱤘󱤆󱤉󱥬󱥠󱥞󱦜󱤬󱥓「Input mode」󱤿󱥮󱤧󱤬󱦜󱤘󱤡󱥫󱥁󱤡󱥞󱤙󱤿「Direct」󱦜󱤿󱥁󱤧󱥈",
    "kulupu xerox li ike",
    "mi tawa ma ohio",
    "sina toki e nimi what pi toki Inli",
    "wawa la o lukin e ni: your mom",
]

CORPUS_SPECIFIC = [
    # "ki le konsi si te isipin epiku le pasila to",
    "ki konsi te isipin epiku pasila to",  # the sandbox has not documented si or le
    'jasima omekapo, ki nimisin "jasima enko nimisin". ki enko alu linluwi Jutu alu epiku ki epiku baba is you. ki likujo "SINtelen pona", ki epiku alu "sitelen pona". ki kepen wawajete isipin, kin ki yupekosi alu lipamanka alu wawajete, kin ki enko isipin lipamanka linluwi alu wawajete',
    "kalamARRRR",
    "Pingo",
    "we Luke",
]
CORPUS_SPECIFIC_XFAIL = [
    "How to Cut a Kiwi",
    "a e i o u",
]


EXCESSIVE_SYLLABICS = [
    # NOTE: these are actually harder to spot bc of the EnglishIgnorables filter
    # it simply stops counting all the short english phonomatches
    # so you can use any number of them...
    "manama manama namana namana majani makala",
    "I manipulate a passe pile so a ton emulate, akin to intake",
    "a ton of insolate puke. make no amen, no joke.",
    "I elope so, to an elite untaken tune, some unwise tone",
    "insane asinine lemon awesome atone joke",
    "insane asinine lemon awesome atone",  # i got more clever
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
]

EXCESSIVE_ENGLISH = [
    "me when i tawa sike",  # previous false positive; fixed by english ignorables
    "Maybe I’m too nasa",  # previous false positive; fixed by LongSyllabic and LongAlphabetic
    "I see :)",
    "I wanna see",  # same down to here
]

NON_MATCHES = [
    "bong",
    "super bruh moment 64",
    "homestuck",
    "homestuck Homestuck",
    "what if i went to the store ",
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
    + EXCESSIVE_ENGLISH
    + NON_MATCHES
)

FALSE_NEGATIVES = [
    # emoticon should not be a problem
    # a token that is one edit off a known word should be allowed
    "mi pnoa",
    "tok",
    "mut",
    "poan",
    "mtue",
    "mi nasa B^)",  # emoticon
]

FALSE_POSITIVES = [
    "lete li ike x.x",  # this is an emoticon but passes because 'x' is in Filters.Miscellaneous
]


@pytest.mark.parametrize("text", KNOWN_GOOD)
def test_known_good_pref(ilo: Ilo, text: str):
    assert ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_BAD + CORPUS_SPECIFIC)
def test_known_bad_pref(ilo: Ilo, text: str):
    assert not ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_GOOD + CORPUS_SPECIFIC)
def test_known_good_corpus(corpus_ilo: Ilo, text: str):
    assert corpus_ilo.is_toki_pona(text), text


@pytest.mark.parametrize("text", KNOWN_BAD)
def test_known_bad_corpus(corpus_ilo: Ilo, text: str):
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
def test_false_positives_pref(ilo: Ilo, text: str):
    assert not ilo.is_toki_pona(text)


@pytest.mark.xfail
@pytest.mark.parametrize("text", FALSE_NEGATIVES)
def test_false_negatives_pref(ilo: Ilo, text: str):
    assert ilo.is_toki_pona(text)


@pytest.mark.xfail
@pytest.mark.parametrize("text", CORPUS_SPECIFIC_XFAIL)
def test_false_positives_corpus(corpus_ilo: Ilo, text: str):
    assert not corpus_ilo.is_toki_pona(text)
