# PDM
import pytest
import hypothesis.strategies as st
from hypothesis import given

# LOCAL
from sonatoki.Tokenizers import (
    Tokenizer,
    SentTokenizer,
    WordTokenizer,
    SentTokenizerRe,
    WordTokenizerRe,
    SentTokenizerRe1,
    WordTokenizerRe1,
)

SENT_TOKENIZERS = [
    SentTokenizer,
    SentTokenizerRe,
    SentTokenizerRe1,
]
WORD_TOKENIZERS = [
    WordTokenizer,
    WordTokenizerRe,
    WordTokenizerRe1,
]


@pytest.mark.parametrize("tokenizer", SENT_TOKENIZERS)
@given(st.from_regex(r".*"))
def test_sentence_tokenize_idempotence(tokenizer: Tokenizer, s: str):
    tokenized = tokenizer.tokenize(s)
    restored = "\n".join(tokenized)
    retokenized = tokenizer.tokenize(restored)
    assert tokenized == retokenized, (s, tokenized, retokenized)


@pytest.mark.parametrize("tokenizer", WORD_TOKENIZERS)
@given(st.from_regex(r".*"))
def test_semi_idempotence_word(tokenizer: Tokenizer, s: str):
    tokenized = tokenizer.tokenize(s)
    restored = " ".join(tokenized)
    retokenized = tokenizer.tokenize(restored)
    assert tokenized == retokenized, (s, tokenized, retokenized)


# @pytest.mark.parametrize("tokenizer", SENT_TOKENIZERS)
# @given(st.from_regex(r".*"))
# def test_sentence_reconstructable(tokenizer: Tokenizer, s: str):
#     tokenized = tokenizer.tokenize(s)
#     restored = "\n".join(tokenized)
#     assert tokenized == retokenized, (s, tokenized, retokenized)
#
#
# @pytest.mark.parametrize("tokenizer", WORD_TOKENIZERS)
# @given(st.from_regex(r".*"))
# def test_word_reconstructable(tokenizer: Tokenizer, s: str):
#     tokenized = tokenizer.tokenize(s)
#     restored = " ".join(tokenized)
#     retokenized = tokenizer.tokenize(restored)
#     assert tokenized == retokenized, (s, tokenized, retokenized)
