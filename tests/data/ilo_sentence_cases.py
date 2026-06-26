# LOCAL
from tests.data.types import Transform

ALL_VALID = [
    Transform("mi unpa e mama sina", True),
    Transform("mama sina li lon seme? mi wile toki tawa ona", True),
    Transform("sina sike pakala", True),
    Transform("    sina    seme     e     mi     ?", True),
    Transform("AAAAAAAAAAA", True),
    Transform("muuuu MUUU muUuUuU", True),
    Transform(
        "wawa mute. wawa mute. wawa mute. wawa mute. wawa mute. wawa mute. wawa mute. wawa mute. wawa mute. wawa mute. ",
        True,
    ),
    Transform("󱥄󱥬󱥩󱤴", True),  # "o toki tawa mi" in UCSUR
    Transform("󱤴󱤧󱤑󱥍󱦗󱤖󱥡󱦘󱤬󱥭‍󱥡󱥚", True),
    Transform("󱤑󱦐󱥗󱦜󱦈󱦜󱥉󱦜󱦑󱥄󱤤󱤂󱤉󱥆󱤀", True),
    Transform("o lukin, 󱤴󱥬󱥩󱤴󱤧wawa", True),
    Transform("ni li sona kiwen", True),
    Transform("nimi namako li toki e ale", True),
    Transform("mi open mute a", True),  # mostly eng words
    Transform("mi pali ilo to", True),
    Transform("󱤴​󱥌​󱤉​󱥡​󱥍​󱥬​󱥔​󱥩​󱤱​󱤴", True),
    Transform("󱤴󱥷󱦕󱤴", True),
    Transform("󱥬‍󱥔​󱥬󱦕󱥔", True, weight=2.0),
    Transform("󱤴​󱤊​󱥞​󱤧​󱤻‍󱥔. 󱥁​󱤧​󱥙​󱥩​󱥞?", True),
    Transform("󱤴󱤊󱥞󱤧󱤻‍󱥔. 󱥁󱤧󱥙󱥩󱥞", True),
]

SYLLABIC_MATCHES = [
    Transform("ni li tenpo penpo", True),
    Transform("sipisi", True),
    Transform("walawa malama walama malama mupi", True, weight=0.5),
    Transform("mi sona ala e nimi sunopatikuna", True, weight=0.8),
    Transform("mi sona e nimi sutopatikuna", True, weight=0.8),
    Transform("kalama wuwojiti li pana e sona", True, weight=0.5),
    Transform(
        "jan Awaja en jan Alasali en jan Akesinu li pona", True
    ),  # syllables match before names here
    Transform("jan Ke Tami", True, weight=2.0),
    Transform("kulupu Kuko", True),
]

ALPHABETIC_MATCHES = [
    Transform("mi mtue o kama sona", True, weight=0.5),
    Transform("mi mute o kma son", True, weight=0.5),
    Transform("mi mute o kama kne snoa a", True, weight=0.5),
    Transform("ni li tptpt", True, weight=0.5),
    Transform("mi wile pana lon sptp", True, weight=0.5),
    Transform(
        "tmo tawa mi li pona mute la mi kepeken ona lon tenpo mute", True, weight=0.5
    ),
    Transform(
        "mi pakla lon nimi pi mute lili, taso ale li pona tan ni: mi toki mute",
        True,
        weight=0.5,
    ),
]

NAME_MATCHES = [
    Transform("musi Homestuck li ike tawa mi", True, weight=2.0),
    Transform("ilo Google li sona ala e nimi Emoticon la mi wile utala e ona", True),
    Transform("toki Kanse li lon", True),
    Transform("toki Lojban li nasa e lawa mi", True),
    Transform("ilo Firefox", True),
    Transform("ilo FaceBook li nasa", True, weight=2.0),
    Transform("mi kepeken ilo MySQL", True, weight=2.0),
    Transform("o weka e ilo ChatGPT", True, weight=2.0),
    Transform("poki li nasin SQLite", True),
    Transform("mi musi Space Station 13", True, weight=3),
    Transform(
        "jan Tepo en jan Salo en jan Lakuse en pipi Kewapi en soweli Eweke en mi li musi",
        True,
        weight=1.5,
    ),
]

SOME_INVALID = [
    Transform(
        "󱤎󱥁󱤡󱥀󱤬󱥚󱥁󱤧󱤬󱦜󱤬󱥆󱤡󱥞󱤘󱤆󱤉󱥬󱥠󱥞󱦜󱤬󱥓「Input mode」󱤿󱥮󱤧󱤬󱦜󱤘󱤡󱥫󱥁󱤡󱥞󱤙󱤿「Direct」󱦜󱤿󱥁󱤧󱥈", True
    ),
    Transform("kulupu xerox li ike", True),
    Transform("mi tawa ma ohio", True),
    Transform("sina toki e nimi what pi toki Inli", True),
    Transform("wawa la o lukin e ni: your mom", True),
]

CORPUS_SPECIFIC = [
    Transform("ki le konsi si te isipin epiku le pasila to", True, weight=0.25),
    Transform(
        "ki konsi te isipin epiku pasila to", True, weight=0.25
    ),  # the sandbox has not documented si or le
    Transform(
        'jasima omekapo, ki nimisin "jasima enko nimisin". ki enko alu linluwi Jutu alu epiku ki epiku baba is you. ki likujo "SINtelen pona", ki epiku alu "sitelen pona". ki kepen wawajete isipin, kin ki yupekosi alu lipamanka alu wawajete, kin ki enko isipin lipamanka linluwi alu wawajete',
        True,
        weight=0.25,
    ),
    Transform("kalamARRRR", True, weight=0.25),
    Transform("kalamar.", True, weight=0.25),
    Transform("Pingo", True, weight=0.25),
    Transform("pingo", True, weight=0.25),
    Transform("we Luke li alente wa", True, weight=0.5),
]

EXCESSIVE_SYLLABICS = [
    # NOTE: this is sometimes hard to distinguish from EXCESSIVE_ENGLISH
    Transform("manama manama namana namana majani makala", False),
    Transform("I manipulate a passe pile so a ton emulate, akin to intake", False),
    Transform("a ton of insolate puke. make no amen, no joke.", False),
    Transform("I elope so, to an elite untaken tune, some unwise tone", False),
    Transform("insane asinine lemon awesome atone joke", False),
    Transform("insane asinine lemon awesome atone", False),  # i got more clever
    Transform("nope, no, joke", False),
    Transform("insane", False),
    Transform("woman", False),
    Transform("man", False),
    Transform("opposite", False),
    Transform("nine emo women see anime alone", False),
    Transform("i like mini potato", False),
    Transform("sanwi pi amu e tili", False),
    Transform("te amo <3", False),
    Transform("Laura, te amo <3", False),
    Transform("jajaja", False),
    Transform("ja ja ja ja", False),
    Transform("ja ja", False),
    Transform("ja", False),
    Transform("mi le kujo nenka ta pi ta", False),
    Transform("o lo sun titan peko", False),
    Transform("usa usa", False),
    Transform("j'en note.", False),
    Transform("j'en mise", False),
]

EXCESSIVE_ALPHABETICS = [
    Transform("wen i tok usin onli notes in toki pona i look silli. ", False),
    Transform("I wait, I sulk, as a tool I make stoops to ineptness.", False),
    Transform(
        "aaa i non-saw usa's most multiple element-set. it's as asinine as in `e`-less speak",
        False,
    ),
    Transform(
        "so, to atone like papa—an awesome anon (no-name) sin man—i ate an asinine lemon-limelike tomato jalapeno isotope. 'nonsense!' amen. note to Oman: take mine katana to imitate a ninja in pantomime. atomise one nuke? 'insane misuse!' same. likewise, Susan, awaken a pepino melon in a linen pipeline. (penile) emanate semen. joke: manipulate a tame toneme to elope online tonite",
        False,
    ),
    Transform("jes mi estas.", False),
    Transform("jes ja, unu momento", False),
    Transform("kiku tiki tuki tiki", False),
]

EXCESSIVE_TYPOES = [
    Transform("mi pakla ln tepo mtue ls mi kn ala tok poan aun seem", False),
    Transform("sina poan", False),
    Transform("ona lu pnoa", False),
]

EXCESSIVE_NAMES = [
    Transform("I Want To Evade The Filter", False),
    Transform("If You Do This The Bot Can't See You", False),
    Transform("This Is A Statement In Perfect Toki Pona, I Guarantee", False),
]

EXCESSIVE_ENGLISH = [
    Transform(
        "me when i tawa sike", False
    ),  # previous false positive; fixed by english ignorables
    Transform(
        "Maybe I’m too nasa", False
    ),  # previous false positive; fixed by LongSyllabic and LongAlphabetic
    Transform("I see :)", False),
    Transform("I wanna see", False),  # same down to here
    Transform("i'm online all the time", False),
    Transform("How to Cut a Kiwi", False),
    Transform("ni li make e sense", False),
    Transform("21st", False),  # previous false positive; fixed by ProperName change
    Transform("a e i o u", False),
    Transform("ni li make e sense tawa mi", False),
    Transform("ni li make e sense", False),
    Transform("does 'mi wile pana e sona' make sense?", False),
]

NON_MATCHES = [
    Transform("bong", False),
    Transform("super bruh moment 64", False),
    Transform("homestuck", False),
    Transform("homestuck Homestuck", False),
    Transform("what if i went to the store ", False),
]

KNOWN_GOOD = (
    ALL_VALID + SYLLABIC_MATCHES + ALPHABETIC_MATCHES + NAME_MATCHES + SOME_INVALID
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
    Transform("mi pnoa", True, True),
    Transform("tok", True, True),
    Transform("mut", True, True),
    Transform("poan", True, True),
    Transform("mtue", True, True),
    Transform("mi nasa B^)", True, True),  # emoticon
    Transform("musi :P", True, True),  # emoticon
    Transform("ala :x", True, True),
    Transform(
        "😃⃢👍", True, True
    ),  # sincerely, no idea, but it came up and it should be omitted by emojis but isn't
    Transform("lete li ike x.x", True, True),  # works for corpus but not for lazy..
]

FALSE_POSITIVES = [
    Transform("Knowing a little toki pona", False, True),
]


ALL_SENTENCES = (
    KNOWN_GOOD
    + KNOWN_BAD
    + CORPUS_SPECIFIC
    + NON_MATCHES
    + FALSE_POSITIVES
    + FALSE_NEGATIVES
)
