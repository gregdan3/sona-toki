# PDM
import pytest

# LOCAL
from tests.data.types import Transform
from sonatoki.Tokenizers import (
    SentTokenizer,
    WordTokenizer,
    SentTokenizerRe,
    WordTokenizerRe,
    SentTokenizerRe1,
    WordTokenizerRe1,
)
from tests.data.word_tokenizer_cases import CASES as WORD_CASES
from tests.data.sentence_tokenizer_cases import CASES as SENT_CASES


@pytest.mark.parametrize("case", SENT_CASES)
def test_SentTokenizer(case: Transform, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    fn_tokenized = SentTokenizer.tokenize(case.input)
    assert fn_tokenized == case.output, case.name


@pytest.mark.skip("Deprecated")
@pytest.mark.parametrize("case", SENT_CASES)
def test_SentTokenizerRe(case: Transform, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    re_tokenized = SentTokenizerRe.tokenize(case.input)
    assert re_tokenized == case.output, case.name


@pytest.mark.skip("Deprecated")
@pytest.mark.parametrize("case", SENT_CASES)
def test_SentTokenizerReCompare(case: Transform, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    re_tokenized = SentTokenizerRe.tokenize(case.input)
    re1_tokenized = SentTokenizerRe1.tokenize(case.input)
    assert re_tokenized == re1_tokenized, case.name


@pytest.mark.skip("Deprecated")
@pytest.mark.parametrize("case", SENT_CASES)
def test_SentTokenizerRe1(case: Transform, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    re1_tokenized = SentTokenizerRe1.tokenize(case.input)
    assert re1_tokenized == case.output, case.name


###################
# Word tokenizers #
###################


@pytest.mark.parametrize("case", WORD_CASES)
def test_WordTokenizer(case: Transform, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    fn_tokenized = WordTokenizer.tokenize(case.input)
    assert fn_tokenized == case.output, case.name


@pytest.mark.skip("Deprecated")
@pytest.mark.parametrize("case", WORD_CASES)
def test_WordTokenizerRe(case: Transform, request):
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    re_tokenized = WordTokenizerRe.tokenize(case.input)
    re1_tokenized = WordTokenizerRe1.tokenize(case.input)
    assert re_tokenized == re1_tokenized, case.name


@pytest.mark.skip("Deprecated")
@pytest.mark.parametrize("case", WORD_CASES)
def test_WordTokenizerRe1(case: Transform, request):
    """This implementation will always exhibit the correct behavior, so long as `regex` is up to date
    Thus, it is used as a reference implementation for all other tests"""
    if case.xfail:
        request.node.add_marker(pytest.mark.xfail())

    re1_tokenized = WordTokenizerRe1.tokenize(case.input)
    assert re1_tokenized == case.output, case.name
