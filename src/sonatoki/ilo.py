# STL
from typing import List, Type

# LOCAL
from sonatoki.types import Number, Scorecard
from sonatoki.Filters import Filter
from sonatoki.Scorers import Scorer, SentNoOp, SentenceScorer
from sonatoki.Cleaners import Cleaner
from sonatoki.Tokenizers import Tokenizer, SentTokenizer, WordTokenizer
from sonatoki.Preprocessors import Preprocessor


class Ilo:
    __preprocessors: List[Type[Preprocessor]]
    __sent_tokenizer: Type[Tokenizer]
    __word_tokenizer: Type[Tokenizer]
    __cleaners: List[Type[Cleaner]]
    __ignoring_filters: List[Type[Filter]]
    __scoring_filters: List[Type[Filter]]
    __scorer: Type[Scorer]
    __sentence_scorer: Type[SentenceScorer]
    __passing_score: Number
    __empty_passes: bool

    def __init__(
        self,
        preprocessors: List[Type[Preprocessor]],
        cleaners: List[Type[Cleaner]],
        ignoring_filters: List[Type[Filter]],
        scoring_filters: List[Type[Filter]],
        scorer: Type[Scorer],
        passing_score: Number,
        empty_passes: bool = True,
        sentence_scorer: Type[SentenceScorer] = SentNoOp,
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
        self.__sentence_scorer = sentence_scorer
        self.__passing_score = passing_score
        self.__empty_passes = empty_passes

    def preprocess(self, msg: str) -> str:
        for p in self.__preprocessors:
            msg = p.process(msg)
        return msg

    def word_tokenize(self, msg: str) -> List[str]:
        """It is *highly* recommended that you run `ilo.preprocess` first."""
        return self.__word_tokenizer.tokenize(msg)

    def sent_tokenize(self, msg: str) -> List[str]:
        """It is *highly* recommended that you run `ilo.preprocess` first."""
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

    def score_sentences(self, scorecards: List[Scorecard]) -> List[Scorecard]:
        return self.__sentence_scorer.score(scorecards)

    def _is_toki_pona(self, message: str) -> Scorecard:
        """Process a message into its tokens, then filters, cleans, and scores
        them. Message must already be preprocessed, normally done in
        `self.is_toki_pona(message)`.

        Returns a `Scorecard` with all changes to the input text and a score.
        """
        tokenized = self.word_tokenize(message)
        filtered = self.filter_tokens(tokenized)
        cleaned = self.clean_tokens(filtered)
        score = self.score_tokens(cleaned)
        if not self.__empty_passes and not cleaned:
            # NOTE: filtered will already be empty
            # but clean_tokens can *technically* omit tokens too
            score = 0

        scorecard: Scorecard = {
            "text": message,
            "tokenized": tokenized,
            "filtered": filtered,
            "cleaned": cleaned,
            "score": score,
        }

        return scorecard

    def make_scorecard(self, message: str) -> Scorecard:
        """Preprocess a message, then create and return a `Scorecard` for that
        message."""
        message = self.preprocess(message)
        return self._is_toki_pona(message)

    def is_toki_pona(self, message: str) -> bool:
        """Determines whether a text is or is not Toki Pona."""
        scorecard = self.make_scorecard(message)
        return scorecard["score"] >= self.__passing_score

    def _are_toki_pona(self, message: str) -> List[Scorecard]:
        """Split a message into sentences, then return a list with each
        sentence's scorecard from `self._is_toki_pona()`.

        Message must already be preprocessed, normally done in
        `self.are_toki_pona(message)`.
        """
        scorecards: List[Scorecard] = list()
        for sentence in self.sent_tokenize(message):
            result = self._is_toki_pona(sentence)
            scorecards.append(result)
        scorecards = self.score_sentences(scorecards)
        return scorecards

    def make_scorecards(self, message: str) -> List[Scorecard]:
        """Preprocess a message, then create and return a `Scorecard` for each
        sentence in that message."""
        message = self.preprocess(message)
        return self._are_toki_pona(message)

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
        scorecards = self._are_toki_pona(message)
        return [card["score"] >= self.__passing_score for card in scorecards]
