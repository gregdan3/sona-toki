# STL
import itertools

# PDM
import hypothesis.strategies as st

# LOCAL
from sonatoki.Filters import Syllabic, Phonotactic, AlphabeticRe
from sonatoki.constants import NIMI_LINKU, NIMI_LINKU_LILI

PROPER_NAME_RE = r"[A-Z][a-z]*"

token_strategy = (
    st.sampled_from(NIMI_LINKU + NIMI_LINKU_LILI)
    | st.from_regex(Phonotactic.pattern.pattern, fullmatch=True)
    | st.from_regex(Syllabic.pattern.pattern, fullmatch=True)
    | st.from_regex(PROPER_NAME_RE, fullmatch=True)
    | st.from_regex(AlphabeticRe.pattern.pattern, fullmatch=True)
)


token_list_strategy = st.lists(
    token_strategy,
    min_size=0,
    max_size=10,
    unique=True,
)


def overlapping_pairs(iterable: str):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    _ = next(b, None)
    return zip(a, b)
