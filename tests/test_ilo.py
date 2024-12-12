# STL
from typing import List, Tuple

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
    "o lukin, 󱤴󱥬󱥩󱤴󱤧wawa",
    "ni li sona kiwen",
    "nimi namako li toki e ale",
    "mi open mute a",  # mostly eng words
    "mi pali ilo to",
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
    "<:owe:843315277286473778><:owe:843315277286473778><:owe:843315277286473778><:owe:843315277286473778><:owe:843315277286473778>",
    "...",
    " ⟨·⟩, a",
    "·····",
    "o lukin: [[w:QWERTY]]",
    "nasa la mi ken pana e ni: <unrelated_words_that_are_illegal>",
    "❤️",  # heart
    "😊",
    "👨‍👩‍👧‍👧",  # family emoji with zwj
    # every non-emoji in the writables
    "🄀🄁🄂🄃🄄🄅🄆🄇🄈🄉🄊🄋🄌🄍🄎🄏🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩🄪🄫🄬🄭🄮🄯🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅊🅋🅌🅍🅎🅏🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅪🅫🅬🅭🅮🅯🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🆊🆋🆌🆍🆏🆐 🆛🆜🆝🆞🆟🆠🆡🆢🆣🆤🆥🆦🆧🆨🆩🆪🆫🆬🆭🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿",
    "🅰️🅱️🅾️🅱️🅰️",  # blood type emojis
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
    "ilo FaceBook li nasa",
    "mi kepeken ilo MySQL",
    "poki li nasin SQLite",
    "mi musi Space Station 13",
    "jan Tepo en jan Salo en jan Lakuse en pipi Kewapi en soweli Eweke en mi li musi",
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
    "kalamar.",
    "Pingo",
    "pingo",
    "we Luke li alente wa",
]
CORPUS_SPECIFIC_XFAIL: List[str] = []


EXCESSIVE_SYLLABICS = [
    # NOTE: this is sometimes hard to distinguish from EXCESSIVE_ENGLISH
    "manama manama namana namana majani makala",
    "I manipulate a passe pile so a ton emulate, akin to intake",
    "a ton of insolate puke. make no amen, no joke.",
    "I elope so, to an elite untaken tune, some unwise tone",
    "insane asinine lemon awesome atone joke",
    "insane asinine lemon awesome atone",  # i got more clever
    "nope, no, joke",
    "insane",
    "woman",
    "man",
    "opposite",
    "nine emo women see anime alone",
    "i like mini potato",
]

EXCESSIVE_ALPHABETICS = [
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
    "i'm online all the time",
    "How to Cut a Kiwi",
    "ni li make e sense",
    "21st",  # previous false positive; fixed by ProperName change
    "a e i o u",  # voting brings this back to false positive zone...
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
    "musi :P",  # emoticon
    "lete li ike x.x",  # this is an emoticon but passes because 'x' is in Filters.Miscellaneous
    "😃⃢👍",  # sincerely, no idea, but it came up and it should be omitted by emojis but isn't
]

FALSE_POSITIVES = [
    "Knowing a little toki pona",  # name, dict, alphabet, dict, dict- damn, that's hard.
]

IGNORABLE_PAIRS: List[Tuple[str, str]] = [
    ("o lukin e ni: https://example.com/", "o lukin e ni:"),
    ("ni li nasa anu seme <:musiwawa:198591138591>", "ni li nasa anu seme"),
    ("seme la ni li toki pona ala https://example.com/", "seme la ni li toki pona ala"),
    ("```\ndef bad():\n    pass\n``` o lukin e ni", "o lukin e ni"),
    ("mi tawa tomo telo 💦💦", "mi tawa tomo telo"),
    ("o lukin e lipu ni: [[wp:Canvassing]]", "o lukin e lipu ni:"),
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


@pytest.mark.parametrize("pair", IGNORABLE_PAIRS)
def test_pref_ignorable_doesnt_change_score(ilo: Ilo, pair: Tuple[str, str]):
    with_ignorable, without_ignorable = pair
    with_ignorable = ilo.preprocess(with_ignorable)
    without_ignorable = ilo.preprocess(without_ignorable)
    score_with = ilo._is_toki_pona(with_ignorable)["score"]
    score_without = ilo._is_toki_pona(without_ignorable)["score"]
    assert score_with == score_without


@pytest.mark.parametrize("pair", IGNORABLE_PAIRS)
def test_lazy_ignorable_doesnt_change_score(lazy_ilo: Ilo, pair: Tuple[str, str]):
    with_ignorable, without_ignorable = pair
    with_ignorable = lazy_ilo.preprocess(with_ignorable)
    without_ignorable = lazy_ilo.preprocess(without_ignorable)
    score_with = lazy_ilo._is_toki_pona(with_ignorable)["score"]
    score_without = lazy_ilo._is_toki_pona(without_ignorable)["score"]
    assert score_with == score_without


@pytest.mark.parametrize("pair", IGNORABLE_PAIRS)
def test_corpus_ignorable_doesnt_change_score(corpus_ilo: Ilo, pair: Tuple[str, str]):
    with_ignorable, without_ignorable = pair
    with_ignorable = corpus_ilo.preprocess(with_ignorable)
    without_ignorable = corpus_ilo.preprocess(without_ignorable)
    score_with = corpus_ilo._is_toki_pona(with_ignorable)["score"]
    score_without = corpus_ilo._is_toki_pona(without_ignorable)["score"]
    assert score_with == score_without
