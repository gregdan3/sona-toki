# STL
import logging
from typing import List, Type, Tuple

# LOCAL
from sonatoki.Filters import Filter
from sonatoki.Scorers import Number, Scorer
from sonatoki.Cleaners import Cleaner
from sonatoki.Tokenizers import Tokenizer
from sonatoki.Preprocessors import Preprocessor

LOG = logging.getLogger(__name__)


class Ilo:
    __preprocessors: List[Type[Preprocessor]]
    __word_tokenizer: Type[Tokenizer]
    __cleaners: List[Type[Cleaner]]
    __ignoring_filters: List[Type[Filter]]
    __scoring_filters: List[Type[Filter]]
    __scorer: Type[Scorer]
    __passing_score: Number
    logging_threshold: Number = -1

    def __init__(
        self,
        preprocessors: List[Type[Preprocessor]],
        cleaners: List[Type[Cleaner]],
        ignoring_filters: List[Type[Filter]],
        scoring_filters: List[Type[Filter]],
        scorer: Type[Scorer],
        passing_score: Number,
        word_tokenizer: Type[Tokenizer],
    ):
        super().__init__()
        # avoid keeping a ref to user's list just in case
        self.__preprocessors = [*preprocessors]
        self.__word_tokenizer = word_tokenizer
        self.__cleaners = [*cleaners]
        self.__ignoring_filters = [*ignoring_filters]
        self.__scoring_filters = [*scoring_filters]
        self.__scorer = scorer
        self.__passing_score = passing_score

    def preprocess(self, msg: str) -> str:
        for p in self.__preprocessors:
            msg = p.process(msg)
        return msg

    def word_tokenize(self, msg: str) -> List[str]:
        """It is *highly* recommended that you run `ilo.preprocess` first."""
        return self.__word_tokenizer.tokenize(msg)

    def clean_token(self, token: str) -> str:
        for c in self.__cleaners:
            token = c.clean(token)
        return token

    def clean_tokens(self, tokens: List[str]) -> List[str]:
        # NOTE: tested, making a new list with a for loop *is* faster than:
        # list comp, generator comp, in-place replacement
        cleaned_tokens: List[str] = list()
        for token in tokens:
            cleaned_token = self.clean_token(token)
            if not cleaned_token:
                # TODO: warn user?
                continue
            cleaned_tokens.append(cleaned_token)
        return cleaned_tokens

    def _filter_token(self, token: str) -> bool:
        for f in self.__ignoring_filters:
            if f.filter(token):
                return True
        return False

    def filter_tokens(self, tokens: List[str]) -> List[str]:
        filtered_tokens: List[str] = []
        for token in tokens:
            if self._filter_token(token):
                continue
            # the ignoring filter is true if the token matches
            # the user wants to ignore these so keep non-matching tokens
            filtered_tokens.append(token)
        return filtered_tokens

    def score_tokens(self, tokens: List[str]) -> float:
        return self.__scorer.score(tokens, self.__scoring_filters)

    def _is_toki_pona(
        self, message: str
    ) -> Tuple[str, List[str], List[str], List[str], Number, bool]:
        """Returns all components of the processing algorithm:
        - Preprocessed message (str)
        - Tokenized message (list[str])
        - Filtered message (list[str])
        - Cleaned message (list[str])
        - Score (float)
        - Result (bool)"""
        preprocessed = self.preprocess(message)
        tokenized = self.word_tokenize(preprocessed)
        filtered = self.filter_tokens(tokenized)
        cleaned = self.clean_tokens(filtered)
        score = self.score_tokens(cleaned)
        result = score >= self.__passing_score

        if score <= self.logging_threshold:
            LOG.debug("msg: %.2f  %s", score, repr(message))
            LOG.debug("preproc:   %s", repr(preprocessed))
            LOG.debug("tokenized: %s", tokenized)
            LOG.debug("filtered:  %s", filtered)
            LOG.debug("cleaned:   %s", cleaned)
        # TODO: Move to each function? Loses ability to control when logging occurs by threshold

        return preprocessed, tokenized, filtered, cleaned, score, result

    def is_toki_pona(self, message: str) -> bool:
        """Determines whether a single statement is or is not Toki Pona."""
        *_, result = self._is_toki_pona(message)
        return result
