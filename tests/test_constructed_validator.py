# LOCAL
from otokipona.ilo import Ilo
from otokipona.Filters import (
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Punctuations,
)
from otokipona.Scorers import PassFail
from otokipona.Cleaners import ConsecutiveDuplicates
from otokipona.Tokenizers import word_tokenize_tok
from otokipona.Preprocessors import URLs, DiscordEmotes


def test_constructor():
    ilo = Ilo(
        preprocessors=[URLs, DiscordEmotes],
        ignoring_filters=[Numerics, Punctuations],
        scoring_filters=[NimiLinku, Syllabic, Alphabetic, ProperName],
        cleaners=[ConsecutiveDuplicates],
        scorer=PassFail,
        tokenizer=word_tokenize_tok,
    )
    assert not ilo.is_toki_pona("super bruh moment 64")
    assert ilo.is_toki_pona("mi unpa e mama sina")
