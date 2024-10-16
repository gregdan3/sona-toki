# STL
import string

# PDM
import hypothesis.strategies as st
from hypothesis import given, example

# LOCAL
from sonatoki.Filters import (
    Or,
    And,
    Len,
    Not,
    NimiPu,
    PuName,
    Numeric,
    Syllabic,
    Alphabetic,
    NimiKuLili,
    NimiKuSuli,
    Phonotactic,
    Punctuation,
    AlphabeticRe,
    LongSyllabic,
    MemberFilter,
    NimiLinkuCore,
    PunctuationRe,
    LongAlphabetic,
    PunctuationRe1,
    LongPhonotactic,
    NimiLinkuCommon,
    FalsePosSyllabic,
    NimiLinkuObscure,
    NimiLinkuSandbox,
    NimiLinkuUncommon,
)
from sonatoki.Cleaners import Lowercase, ConsecutiveDuplicates
from sonatoki.constants import FALSE_POS_SYLLABIC, words_by_tag

# FILESYSTEM
from .test_utils import PROPER_NAME_RE


@given(st.sampled_from(list(words_by_tag("book", "pu"))))
@example("lukin")
@example("selo")
@example("li")
def test_NimiPu(s: str):
    res = NimiPu.filter(s)
    assert res, repr(s)


@given(st.sampled_from(list(words_by_tag("usage_category", "core"))))
@example("pona")
def test_NimiLinkuCore(s: str):
    res = NimiLinkuCore.filter(s)
    assert res, repr(s)


@given(st.sampled_from(list(words_by_tag("usage_category", "common"))))
@example("n")
@example("tonsi")
@example("kipisi")
def test_NimiLinkuCommon(s: str):
    res = NimiLinkuCommon.filter(s)
    assert res, repr(s)


@given(st.sampled_from(list(words_by_tag("usage_category", "uncommon"))))
def test_NimiLinkuUncommon(s: str):
    res = NimiLinkuUncommon.filter(s)
    assert res, repr(s)


@given(st.sampled_from(list(words_by_tag("usage_category", "obscure"))))
@example("pake")
@example("san")
def test_NimiLinkuObscure(s: str):
    res = NimiLinkuObscure.filter(s)
    assert res, repr(s)


@given(st.sampled_from(list(words_by_tag("usage_category", "sandbox"))))
@example("kalamARR")
@example("Pingo")
def test_NimiLinkuSandbox(s: str):
    s = Lowercase.clean(s)
    s = ConsecutiveDuplicates.clean(s)
    # above two are necessary due to kalamARR and Pingo
    res = NimiLinkuSandbox.filter(s)
    assert res, repr(s)


@given(st.from_regex(Phonotactic.pattern, fullmatch=True))
@example("kijetesantakalu")
@example("n")
def test_Phonotactic(s: str):
    res = Phonotactic.filter(s)
    assert res, repr(s)


@given(st.from_regex(Phonotactic.pattern, fullmatch=True))
def test_LongPhonotactic(s: str):
    len_ok = len(s) >= LongPhonotactic.minlen
    res = LongPhonotactic.filter(s)
    assert res == len_ok, repr(s)  # will match given fullmatch


@given(st.from_regex(Syllabic.pattern, fullmatch=True))
@example("wuwojitiwunwonjintinmanna")
def test_Syllabic(s: str):
    res = Syllabic.filter(s)
    assert res, repr(s)


@given(st.from_regex(Syllabic.pattern, fullmatch=True))
def test_LongSyllabic(s: str):
    len_ok = len(s) >= LongSyllabic.minlen
    res = LongSyllabic.filter(s)
    assert res == len_ok


@given(st.from_regex(AlphabeticRe.pattern, fullmatch=True))
@example("muems")
@example("mpptp")
@example("tptpt")
def test_Alphabetic(s: str):
    res_fn = Alphabetic.filter(s)
    res_re = AlphabeticRe.filter(s)
    assert res_fn == res_re, repr(s)


@given(st.from_regex(AlphabeticRe.pattern, fullmatch=True))
def test_LongAlphabetic(s: str):
    len_ok = len(s) >= LongAlphabetic.minlen
    res = LongAlphabetic.filter(s)
    assert res == len_ok


@given(st.from_regex(AlphabeticRe.pattern, fullmatch=True))
def test_AlphabeticRe(s: str):
    res_re = AlphabeticRe.filter(s)
    assert res_re, repr(s)


@given(st.from_regex(PROPER_NAME_RE, fullmatch=True))
def test_ProperName(s: str):
    res = PuName.filter(s)
    assert res, repr(s)


@given(st.from_regex(PunctuationRe.pattern, fullmatch=True))
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


@given(st.from_regex(PunctuationRe.pattern, fullmatch=True))
def test_PunctuationRe(s: str):
    res_re = PunctuationRe.filter(s)
    res_re1 = PunctuationRe1.filter(s)
    assert res_re == res_re1, repr(s)


@given(st.from_regex(PunctuationRe.pattern, fullmatch=True))
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


@given(st.from_regex(r"\d+", fullmatch=True))
def test_Len_minimum(s: str):
    minlen = 4
    filter = Len(Numeric, min=minlen)

    res = filter.filter(s)
    exp = len(s) >= minlen
    assert res == exp


@given(st.from_regex(r"\d+", fullmatch=True))
def test_Len_maximum(s: str):
    maxlen = 6
    filter = Len(Numeric, max=maxlen)

    res = filter.filter(s)
    exp = len(s) <= maxlen
    assert res == exp


@given(st.from_regex(r"\d+", fullmatch=True))
def test_Len_min_and_max(s: str):
    minlen = 3
    maxlen = 7
    filter = Len(Numeric, min=minlen, max=maxlen)

    res = filter.filter(s)
    exp = minlen <= len(s) <= maxlen
    assert res == exp


@given(
    st.from_regex(PunctuationRe.pattern, fullmatch=True)
    | st.from_regex(r"\d+", fullmatch=True),
)
def test_OrFilter(s: str):
    filter = Or(Punctuation, Numeric)
    res = filter.filter(s)
    res_punctuation = Punctuation.filter(s)
    res_numeric = Numeric.filter(s)
    assert res and (res_punctuation or res_numeric)


# NOTE: No subset filter test because A | B is not the same as A combined with B.
# e.g. "apple" passes Alphabetic, "..." passes Punctuation, "apple..." passes neither
# but would incorrectly pass a combined filter.
@given(
    st.sampled_from(
        list(words_by_tag("book", "pu") | words_by_tag("usage_category", "obscure"))
    )
)
def test_MemberFilters_OrFilter(s: str):
    filter = Or(NimiPu, NimiLinkuObscure)
    assert issubclass(filter, MemberFilter)

    res = filter.filter(s)
    res_pu = NimiPu.filter(s)
    res_obscure = NimiLinkuObscure.filter(s)
    assert res and (res_pu or res_obscure)


@given(
    st.sampled_from(
        list(
            words_by_tag("book", "ku suli")
            | words_by_tag("book", "ku lili")
            | words_by_tag("usage_category", "uncommon")
            | words_by_tag("usage_category", "obscure")
            | words_by_tag("usage_category", "sandbox")
        ),
    )
)
def test_OrFilter_IsipinEpiku(s: str):
    filter = Or(
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


@given(st.sampled_from(list(words_by_tag("book", "pu"))))
def test_AndFilter(s: str):
    s = s.capitalize()
    f = And(PuName, NimiPu)
    assert f.filter(s)


@given(st.sampled_from(list(words_by_tag("book", "pu"))))
def test_NotFilter(s: str):
    f = Not(NimiPu)
    assert not f.filter(s)


@given(
    st.sampled_from(list(FALSE_POS_SYLLABIC))
    | st.from_regex(Syllabic.pattern, fullmatch=True)
    | st.from_regex(AlphabeticRe.pattern, fullmatch=True)
)
def test_AndNotFilter(s: str):
    AndNotFilter = And(Syllabic, Not(FalsePosSyllabic))

    res_syl = Syllabic.filter(s)
    res_fp = FalsePosSyllabic.filter(s)
    res_composed = AndNotFilter.filter(s)

    if not res_syl:
        # if it isn't syllabic in the first place, it shouldn't match anything
        assert not res_fp and not res_syl and not res_composed

    if res_fp:
        # syl matched- but if fp matches, then the composed filter should not match
        assert not res_composed


@given(
    st.sampled_from(list(words_by_tag("book", "pu") | words_by_tag("book", "ku suli")))
)
def test_AddTokensToMemberFilter(s: str):
    PuEnKuSuliFilter = NimiPu(add=NimiKuSuli.tokens)
    assert PuEnKuSuliFilter.filter(s)


@given(
    st.sampled_from(
        list(
            words_by_tag("usage_category", "sandbox") | words_by_tag("book", "ku lili")
        )
    )
)
def test_AddTokensToMemberFilterNegative(s: str):
    PuEnKuSuliFilter = NimiPu(add=NimiKuSuli.tokens)
    assert not PuEnKuSuliFilter.filter(s)


@given(
    st.sampled_from(
        list(
            words_by_tag("book", "pu")
            | words_by_tag("book", "ku suli")
            | words_by_tag("book", "ku lili")
            | words_by_tag("usage_category", "uncommon")
            | words_by_tag("usage_category", "obscure")
            | words_by_tag("usage_category", "sandbox")
        ),
    )
    | st.from_regex(Syllabic.pattern, fullmatch=True)
)
def test_SubTokensFromMemberFilter(s: str):
    NimiAlaFilter = NimiLinkuCore(sub=NimiPu.tokens)
    # core is a strict subset of pu
    # if kin becomes core, needs to be corrected

    assert not NimiAlaFilter.filter(s)
