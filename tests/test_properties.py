# PDM
import hypothesis.strategies as st
from hypothesis import given, assume

# LOCAL
from sonatoki.Filters import (
    NimiPu,
    Syllabic,
    Alphabetic,
    NimiKuLili,
    NimiKuSuli,
    Phonotactic,
    NimiLinkuCore,
    NimiPuSynonyms,
    NimiLinkuCommon,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
)
from sonatoki.Cleaners import Lowercase, ConsecutiveDuplicates
from sonatoki.constants import (
    NIMI_PU_SYNONYMS,
    FALSE_POS_SYLLABIC,
    FALSE_POS_ALPHABETIC,
    words_by_tag,
    words_by_usage,
)


@given(st.sampled_from(list(words_by_tag("book", "pu") | NIMI_PU_SYNONYMS)))
def test_pu_filters_non_overlap(s: str):
    res_pu = NimiPu.filter(s)
    res_synonyms = NimiPuSynonyms.filter(s)
    assert (res_pu + res_synonyms) == 1


@given(
    st.sampled_from(
        list(words_by_tag("book", "ku suli") | words_by_tag("book", "ku lili"))
    )
)
def test_ku_filters_non_overlap(s: str):
    s = Lowercase.clean(s)
    s = ConsecutiveDuplicates.clean(s)
    res_ku_suli = NimiKuSuli.filter(s)
    res_ku_lili = NimiKuLili.filter(s)
    assert (res_ku_suli + res_ku_lili) == 1


@given(st.sampled_from(list(words_by_usage(0))))
def test_linku_filters_non_overlap(s: str):
    _ = assume(s != "su")

    s = Lowercase.clean(s)
    s = ConsecutiveDuplicates.clean(s)

    res_core = NimiLinkuCore.filter(s)
    res_common = NimiLinkuCommon.filter(s)
    res_uncommon = NimiLinkuUncommon.filter(s)
    res_obscure = NimiLinkuObscure.filter(s)
    res_sandbox = NimiLinkuSandbox.filter(s)

    assert (res_core + res_common + res_uncommon + res_obscure + res_sandbox) == 1


@given(st.sampled_from(list(words_by_usage(30))))
def test_nimi_linku_properties(s: str):
    assert ConsecutiveDuplicates.clean(s) == s, repr(s)
    assert Alphabetic.filter(s), repr(s)
    assert Syllabic.filter(s), repr(s)
    assert Phonotactic.filter(s), repr(s)
    # Passing phonotactic implies all of the above


@given(st.sampled_from(list(FALSE_POS_ALPHABETIC)))
def test_false_pos_properties(s: str):
    res_syllabic = Syllabic.filter(s)
    res_alphabetic = Alphabetic.filter(s)
    assert res_alphabetic and not res_syllabic
