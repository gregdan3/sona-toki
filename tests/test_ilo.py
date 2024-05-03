# LOCAL
from sonatoki.ilo import Ilo
from sonatoki.Filters import (
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Punctuations,
)
from sonatoki.Scorers import Scaling, SoftScaling
from sonatoki.Cleaners import ConsecutiveDuplicates
from sonatoki.Tokenizers import word_tokenize_tok
from sonatoki.Preprocessors import (
    URLs,
    DiscordEmotes,
    DiscordSpecial,
    DiscordChannels,
    DiscordMentions,
)


def test_constructor():
    ilo = Ilo(
        preprocessors=[
            URLs,
            DiscordEmotes,
            DiscordMentions,
            DiscordChannels,
            DiscordSpecial,
        ],
        ignoring_filters=[Numerics, Punctuations],
        scoring_filters=[NimiLinku, Syllabic, ProperName, Alphabetic],
        cleaners=[ConsecutiveDuplicates],
        scorer=SoftScaling,
        tokenizer=word_tokenize_tok,
        passing_score=0.8,
    )
    # ilo._logging_threshold = 0.8
    assert ilo.is_toki_pona("mi unpa e mama sina")
    # toki pona
    assert ilo.is_toki_pona("mama sina li lon seme? mi wile toki tawa ona")
    assert ilo.is_toki_pona("sina sike pakala")
    # names
    assert ilo.is_toki_pona("musi Homestuck li ike tawa mi")
    # typoes
    assert ilo.is_toki_pona("mi mtue o kama sona")
    assert ilo.is_toki_pona("mi mute o kma son")
    # phonotactically valid
    assert ilo.is_toki_pona("ni li tenpo penpo")
    # alphabetically valid
    assert ilo.is_toki_pona("ni li tptpt")
    # a single
    assert ilo.is_toki_pona("sipisi")

    # soft scaling with syllablic filter at 2/4 will pass up to 5 syllablic words
    assert ilo.is_toki_pona("walawa malama walama malama mupi")
    # but fail 6 or more
    assert not ilo.is_toki_pona("manama manama namana namana majani makala")

    # TODO: should soft scaling save an alphabetically valid single word?
    assert not ilo.is_toki_pona("tok")
    assert not ilo.is_toki_pona("mtue")

    # just english
    assert not ilo.is_toki_pona("bong")
    assert not ilo.is_toki_pona("super bruh moment 64")
    # all names
    assert not ilo.is_toki_pona("I Want To Evade The Filter")
    # all alphabetic
    assert not ilo.is_toki_pona(
        "aaa i non-saw usa's most multiple element-set. it's as asinine as in `e`-less speak"
    )
