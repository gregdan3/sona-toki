# STL
from typing import List, Type, Tuple

# LOCAL
from sonatoki.Filters import Filter
from sonatoki.Scorers import Number, Scorer
from sonatoki.Cleaners import Cleaner
from sonatoki.Tokenizers import Tokenizer, SentTokenizer, WordTokenizer
from sonatoki.Preprocessors import Preprocessor

# tokenized, filtered, cleaned, score, result
Scorecard = Tuple[List[str], List[str], List[str], Number, bool]
# TODO: scorecard kinda sucks as a name


class Ilo:
    __preprocessors: List[Type[Preprocessor]]
    __sent_tokenizer: Type[Tokenizer]
    __word_tokenizer: Type[Tokenizer]
    __cleaners: List[Type[Cleaner]]
    __ignoring_filters: List[Type[Filter]]
    __scoring_filters: List[Type[Filter]]
    __scorer: Type[Scorer]
    __passing_score: Number

    def __init__(
        self,
        preprocessors: List[Type[Preprocessor]],
        cleaners: List[Type[Cleaner]],
        ignoring_filters: List[Type[Filter]],
        scoring_filters: List[Type[Filter]],
        scorer: Type[Scorer],
        passing_score: Number,
        word_tokenizer: Type[Tokenizer] = WordTokenizer,
        sent_tokenizer: Type[Tokenizer] = SentTokenizer,
    ):
        super().__init__()
        # avoid keeping a ref to user's list just in case
        self.__preprocessors = [*preprocessors]
        self.__sent_tokenizer = sent_tokenizer
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

    def sent_tokenize(self, msg: str) -> List[str]:
        return self.__sent_tokenizer.tokenize(msg)

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

    def _is_toki_pona(self, message: str) -> Scorecard:
        """Process a message into its tokens, then filters, cleans, and scores
        them. Returns all parts. Message must already be preprocessed, normally
        done in `self.is_toki_pona(message)`.

        Returns all components of the processing algorithm except preprocessing:
        - Tokenized message (list[str])
        - Filtered message (list[str])
        - Cleaned message (list[str])
        - Score (float)
        - Result (bool)
        """
        tokenized = self.word_tokenize(message)
        filtered = self.filter_tokens(tokenized)
        cleaned = self.clean_tokens(filtered)
        score = self.score_tokens(cleaned)
        result = score >= self.__passing_score

        return tokenized, filtered, cleaned, score, result

    def is_toki_pona(self, message: str) -> bool:
        """Determines whether a single statement is or is not Toki Pona."""
        message = self.preprocess(message)
        *_, result = self._is_toki_pona(message)
        return result

    def _are_toki_pona(self, message: str) -> List[Scorecard]:
        """Split a message into sentences, then return a list each sentence's
        results via `self._is_toki_pona()`.

        Message must already be preprocessed, normally done in
        `self.are_toki_pona(message)`.
        """
        results: List[Scorecard] = list()
        for sentence in self.sent_tokenize(message):
            result = self._is_toki_pona(sentence)
            results.append(result)
        return results

    def are_toki_pona(self, message: str) -> List[bool]:
        """Splits a statement into sentences, then determines if each is or is not Toki Pona.
        NOTE: You will need to decide how to score the result. Examples:

        ```
        def all_must_pass(message: str) -> bool:
            return all(ILO.are_toki_pona(message))

        def portion_must_pass(message: str, score: Number = 0.8) -> bool:
            results = ILO.are_toki_pona(message)
            sent_count = len(results)
            passing = results.count(True)
            return (passing / sent_count) >= score
        ```
        """
        message = self.preprocess(message)
        results = self._are_toki_pona(message)
        return [res[-1] for res in results]
