# STL
import string

# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from sonatoki.Filters import (
    NimiPu,
    Numeric,
    OrFilter,
    Syllabic,
    Alphabetic,
    NimiKuLili,
    NimiKuSuli,
    ProperName,
    Phonotactic,
    Punctuation,
    AlphabeticRe,
    LongSyllabic,
    NimiLinkuCore,
    PunctuationRe,
    LongAlphabetic,
    NimiPuSynonyms,
    OrMemberFilter,
    PunctuationRe1,
    LongPhonotactic,
    NimiLinkuCommon,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
)
from sonatoki.Cleaners import Lowercase, ConsecutiveDuplicates
from sonatoki.constants import (
    NIMI_PU,
    NIMI_KU_LILI,
    NIMI_KU_SULI,
    NIMI_LINKU_CORE,
    NIMI_PU_SYNONYMS,
    NIMI_LINKU_COMMON,
    NIMI_LINKU_OBSCURE,
    NIMI_LINKU_SANDBOX,
    NIMI_LINKU_UNCOMMON,
)

# FILESYSTEM
from .test_utils import PROPER_NAME_RE


@given(st.sampled_from(NIMI_PU))
@example("lukin")
@example("selo")
@example("li")
def test_NimiPu(s: str):
    res = NimiPu.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU_CORE))
@example("pona")
def test_NimiLinkuCore(s: str):
    res = NimiLinkuCore.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU_COMMON))
@example("n")
@example("tonsi")
@example("kipisi")
def test_NimiLinkuCommon(s: str):
    res = NimiLinkuCommon.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU_UNCOMMON))
def test_NimiLinkuUncommon(s: str):
    res = NimiLinkuUncommon.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU_OBSCURE))
def test_NimiLinkuObscure(s: str):
    res = NimiLinkuObscure.filter(s)
    assert res, repr(s)


@given(st.sampled_from(NIMI_LINKU_SANDBOX))
@example("kalamARR")
@example("Pingo")
def test_NimiLinkuSandbox(s: str):
    s = Lowercase.clean(s)
    s = ConsecutiveDuplicates.clean(s)
    # above two are necessary due to kalamARR and Pingo
    res = NimiLinkuSandbox.filter(s)
    assert res, repr(s)


@given(st.from_regex(Phonotactic.pattern.pattern, fullmatch=True))
@example("kijetesantakalu")
@example("n")
def test_Phonotactic(s: str):
    res = Phonotactic.filter(s)
    assert res, repr(s)


@given(st.from_regex(Phonotactic.pattern.pattern, fullmatch=True))
def test_LongPhonotactic(s: str):
    len_ok = len(s) >= LongPhonotactic.length
    res = LongPhonotactic.filter(s)
    assert res == len_ok, repr(s)  # will match given fullmatch


@given(st.from_regex(Syllabic.pattern.pattern, fullmatch=True))
@example("wuwojitiwunwonjintinmanna")
def test_Syllabic(s: str):
    res = Syllabic.filter(s)
    assert res, repr(s)


@given(st.from_regex(Syllabic.pattern.pattern, fullmatch=True))
def test_LongSyllabic(s: str):
    len_ok = len(s) >= LongSyllabic.length
    res = LongSyllabic.filter(s)
    assert res == len_ok


@given(st.from_regex(AlphabeticRe.pattern.pattern, fullmatch=True))
@example("muems")
@example("mpptp")
@example("tptpt")
def test_Alphabetic(s: str):
    res_fn = Alphabetic.filter(s)
    res_re = AlphabeticRe.filter(s)
    assert res_fn == res_re, repr(s)


@given(st.from_regex(AlphabeticRe.pattern.pattern, fullmatch=True))
def test_LongAlphabetic(s: str):
    len_ok = len(s) >= LongAlphabetic.length
    res = LongAlphabetic.filter(s)
    assert res == len_ok


@given(st.from_regex(AlphabeticRe.pattern.pattern, fullmatch=True))
def test_AlphabeticRe(s: str):
    res_re = AlphabeticRe.filter(s)
    assert res_re, repr(s)


@given(st.from_regex(PROPER_NAME_RE, fullmatch=True))
def test_ProperName(s: str):
    res = ProperName.filter(s)
    assert res, repr(s)


@given(st.from_regex(PunctuationRe.pattern.pattern, fullmatch=True))
@example("[]")
@example(r"\\")
@example(r"\"")
@example("⟨·⟩")
@example("…")
@example("「」")
@example(string.punctuation)
def test_PunctuationRe1(s: str):
    res = PunctuationRe1.filter(s)
    assert res, repr(s)


@given(st.from_regex(PunctuationRe.pattern.pattern, fullmatch=True))
def test_PunctuationRe(s: str):
    res_re = PunctuationRe.filter(s)
    res_re1 = PunctuationRe1.filter(s)
    assert res_re == res_re1, repr(s)


@given(st.from_regex(PunctuationRe.pattern.pattern, fullmatch=True))
@example("\U000f1990")  # UCSUR char
def test_Punctuation(s: str):
    res_fn = Punctuation.filter(s)
    res_re1 = PunctuationRe1.filter(s)
    assert res_fn == res_re1, repr(s)


@given(st.from_regex(r"\d+", fullmatch=True))
@example("124125")
@example("99990000")
def test_Numeric(s: str):
    res = Numeric.filter(s)
    assert res, repr(s)


@given(
    st.from_regex(PunctuationRe.pattern.pattern, fullmatch=True)
    | st.from_regex(r"\d+", fullmatch=True),
)
def test_OrFilter(s: str):
    filter = OrFilter(Punctuation, Numeric)
    res = filter.filter(s)
    res_punctuation = Punctuation.filter(s)
    res_numeric = Numeric.filter(s)
    assert res and (res_punctuation or res_numeric)


# NOTE: No subset filter test because A | B is not the same as A combined with B.
# e.g. "apple" passes Alphabetic, "..." passes Punctuation, "apple..." passes neither
# but would incorrectly pass a combined filter.
@given(st.sampled_from(NIMI_PU + NIMI_LINKU_OBSCURE))
def test_OrMemberFilter(s: str):
    filter = OrMemberFilter(NimiPu, NimiLinkuObscure)
    res = filter.filter(s)
    res_pu = NimiPu.filter(s)
    res_obscure = NimiLinkuObscure.filter(s)
    assert res and (res_pu or res_obscure)


@given(
    st.sampled_from(
        NIMI_KU_SULI
        + NIMI_KU_LILI
        + NIMI_LINKU_UNCOMMON
        + NIMI_LINKU_OBSCURE
        + NIMI_LINKU_SANDBOX,
    )
)
def test_OrMemberFilter_IsipinEpiku(s: str):
    filter = OrMemberFilter(
        NimiKuSuli, NimiKuLili, NimiLinkuUncommon, NimiLinkuObscure, NimiLinkuSandbox
    )

    s = Lowercase.clean(s)
    s = ConsecutiveDuplicates.clean(s)

    res = filter.filter(s)
    res_ku_suli = NimiKuSuli.filter(s)
    res_ku_lili = NimiKuLili.filter(s)
    res_uncommon = NimiLinkuUncommon.filter(s)
    res_obscure = NimiLinkuObscure.filter(s)
    res_sandbox = NimiLinkuSandbox.filter(s)
    assert res and (
        res_ku_suli or res_ku_lili or res_uncommon or res_obscure or res_sandbox
    )


@given(st.sampled_from(NIMI_PU + NIMI_PU_SYNONYMS))
def test_pu_filters_non_overlap(s: str):
    res_pu = NimiPu.filter(s)
    res_synonyms = NimiPuSynonyms.filter(s)
    assert (res_pu + res_synonyms) == 1


@given(st.sampled_from(NIMI_KU_SULI + NIMI_KU_LILI))
def test_ku_filters_non_overlap(s: str):
    res_ku_suli = NimiKuSuli.filter(s)
    res_ku_lili = NimiKuLili.filter(s)
    assert (res_ku_suli + res_ku_lili) == 1


@given(
    st.sampled_from(
        NIMI_LINKU_CORE
        + NIMI_LINKU_COMMON
        + NIMI_LINKU_UNCOMMON
        + NIMI_LINKU_OBSCURE
        + NIMI_LINKU_SANDBOX
    )
)
def test_linku_filters_non_overlap(s: str):
    s = Lowercase.clean(s)
    s = ConsecutiveDuplicates.clean(s)

    res_core = NimiLinkuCore.filter(s)
    res_common = NimiLinkuCommon.filter(s)
    res_uncommon = NimiLinkuUncommon.filter(s)
    res_obscure = NimiLinkuObscure.filter(s)
    res_sandbox = NimiLinkuSandbox.filter(s)

    assert (res_core + res_common + res_uncommon + res_obscure + res_sandbox) == 1


@given(st.sampled_from(NIMI_LINKU_CORE + NIMI_LINKU_COMMON + NIMI_LINKU_UNCOMMON))
def test_nimi_linku_properties(s: str):
    assert ConsecutiveDuplicates.clean(s) == s, repr(s)
    assert Alphabetic.filter(s), repr(s)
    assert Syllabic.filter(s), repr(s)
    assert Phonotactic.filter(s), repr(s)
    # Passing phonotactic implies all of the above
