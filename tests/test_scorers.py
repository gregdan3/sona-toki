# STL
from typing import List

# LOCAL
from otokipona.Filters import (
    NimiPu,
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Phonotactic,
    Punctuations,
)
from otokipona.Scorers import PassFail


def test_PassFail():
    s = PassFail.score(["mi", "unpa", "e", "mama", "sina"], [NimiPu, ProperName])
    print(s)
    s = PassFail.score(["Ona Li Nasa Mute"], [NimiPu, ProperName])
    print(s)
