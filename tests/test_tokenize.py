# STL
from typing import List, TypedDict

# PDM
import yaml
import pytest

# LOCAL
from sonatoki.Tokenizers import (
    SentTokenizer,
    WordTokenizer,
    SentTokenizerRe,
    WordTokenizerRe,
    SentTokenizerRe1,
    WordTokenizerRe1,
)


class TokenizerTest(TypedDict):
    name: str
    input: str
    output: List[str]
    should_be_equal: bool
    xfail: bool


def load_params_from_yaml(json_path: str) -> List[TokenizerTest]:
    with open(json_path) as f:
        return yaml.safe_load(f)


def load_tokenizer_tests(json_path: str) -> List[TokenizerTest]:
    tests = load_params_from_yaml(json_path)
    formatted_tests: List[TokenizerTest] = []
    for test in tests:
        formatted_tests.append(
            TokenizerTest(
                xfail=test.get("xfail", False),
                name=test.get("name", ""),
                input=test["input"],
                output=test.get("output", []),
                should_be_equal=test.get("should_be_equal", True),
            )
        )

    return formatted_tests


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_sentences_tok.yml")
)
def test_SentTokenizer(test: TokenizerTest):
    if test["xfail"]:
        pytest.xfail()

    fn_tokenized = SentTokenizer.tokenize(test["input"])
    re1_tokenized = SentTokenizerRe1.tokenize(test["input"])
    assert fn_tokenized == re1_tokenized, test["name"]


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_sentences_tok.yml")
)
def test_SentTokenizerRe(test: TokenizerTest):
    if test["xfail"]:
        pytest.xfail()

    re_tokenized = SentTokenizerRe.tokenize(test["input"])
    re1_tokenized = SentTokenizerRe1.tokenize(test["input"])
    assert re_tokenized == re1_tokenized, test["name"]


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_sentences_tok.yml")
)
def test_SentTokenizerRe1(test: TokenizerTest):
    if test["xfail"]:
        pytest.xfail()

    re1_tokenized = SentTokenizerRe1.tokenize(test["input"])
    assert re1_tokenized == test["output"], test["name"]


###################
# Word tokenizers #
###################


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_words_tok.yml")
)
def test_WordTokenizer(test: TokenizerTest):
    if test["xfail"]:
        pytest.xfail()

    fn_tokenized = WordTokenizer.tokenize(test["input"])
    # re1_tokenized = WordTokenizerRe1.tokenize(test["input"])
    # assert fn_tokenized == re1_tokenized, test["name"]
    assert fn_tokenized == test["output"], test["name"]


# @pytest.mark.parametrize(
#     "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_words_tok.yml")
# )
# def test_WordTokenizerRe(test: TokenizerTest):
#     if test["xfail"]:
#         pytest.xfail()
#
#     re_tokenized = WordTokenizerRe.tokenize(test["input"])
#     re1_tokenized = WordTokenizerRe1.tokenize(test["input"])
#     assert re_tokenized == re1_tokenized, test["name"]
#
#
# @pytest.mark.parametrize(
#     "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_words_tok.yml")
# )
# def test_WordTokenizerRe1(test: TokenizerTest):
#     """This implementation will always exhibit the correct behavior, so long as `regex` is up to date
#     Thus, it is used as a reference implementation for all other tests"""
#     if test["xfail"]:
#         pytest.xfail()
#
#     re1_tokenized = WordTokenizerRe1.tokenize(test["input"])
#     assert re1_tokenized == test["output"], test["name"]
