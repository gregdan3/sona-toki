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
    ilo.debug = True
    assert not ilo.is_toki_pona("super bruh moment 64")
    assert ilo.is_toki_pona("mi unpa e mama sina")
    assert ilo.is_toki_pona("mama sina li mu tan mi")
    assert ilo.is_toki_pona("toki. sike li pona ala. o anpa.")
    assert ilo.is_toki_pona("musi Homestuck li ike tawa mi")
    assert ilo.is_toki_pona("mi mtue o kama sona")
    assert ilo.is_toki_pona("ni li tenpo penpo")
    assert ilo.is_toki_pona("ni li tptpt")

    assert not ilo.is_toki_pona("I'm Trying To Evade The Filter")
    assert not ilo.is_toki_pona(
        """aaa i non-saw usa's most multiple element-set
it's as asinine as in `e`-less speak"""
    )
