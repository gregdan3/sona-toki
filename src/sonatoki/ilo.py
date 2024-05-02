# STL
from typing import List, Type

# LOCAL
from sonatoki.Filters import Filter
from sonatoki.Scorers import Number, Scorer
from sonatoki.Cleaners import Cleaner
from sonatoki.Tokenizers import Tokenizer
from sonatoki.Preprocessors import Preprocessor


class Ilo:
    __preprocessors: List[Type[Preprocessor]]
    __cleaners: List[Type[Cleaner]]
    __ignoring_filters: List[Type[Filter]]
    __scoring_filters: List[Type[Filter]]
    __scorer: Type[Scorer]
    __tokenize: Tokenizer
    __passing_score: Number
    debug: bool = False

    def __init__(
        self,
        preprocessors: List[Type[Preprocessor]],
        cleaners: List[Type[Cleaner]],
        ignoring_filters: List[Type[Filter]],
        scoring_filters: List[Type[Filter]],
        scorer: Type[Scorer],
        tokenizer: Tokenizer,  # NOTE: no wrapper needed?
        passing_score: Number,
    ):
        super().__init__()
        # avoid keeping a ref to user's list just in case
        self.__preprocessors = [*preprocessors]
        self.__cleaners = [*cleaners]
        self.__ignoring_filters = [*ignoring_filters]
        self.__scoring_filters = [*scoring_filters]
        self.__scorer = scorer
        self.__tokenize = tokenizer
        self.__passing_score = passing_score

    def __preprocess(self, msg: str) -> str:
        for p in self.__preprocessors:
            msg = p.process(msg)
        return msg

    def __clean_token(self, token: str) -> str:
        for c in self.__cleaners:
            token = c.clean(token)
        return token

    def __clean_tokens(self, tokens: List[str]) -> List[str]:
        # NOTE: tested, making a new list with a for loop *is* faster than
        # - list comps
        # - generator comps
        # - in-place replacement/removal
        # - in place replacement with result of generator comp
        cleaned_tokens: List[str] = list()
        for token in tokens:
            cleaned_token = self.__clean_token(token)
            if not cleaned_token:
                # TODO: warn user?
                continue
            cleaned_tokens.append(cleaned_token)
        return cleaned_tokens

    def __filter_token(self, token: str) -> bool:
        for f in self.__ignoring_filters:
            if f.filter(token):
                return True
        return False

    def __filter_tokens(self, tokens: List[str]) -> List[str]:
        filtered_tokens: List[str] = []
        for token in tokens:
            if self.__filter_token(token):
                continue
            # the ignoring filter is true if the token matches
            # the user wants to ignore these so keep non-matching tokens
            filtered_tokens.append(token)
        return filtered_tokens

    def __score_tokens(self, tokens: List[str]) -> float:
        return self.__scorer.score(tokens, self.__scoring_filters)

    def is_toki_pona(self, message: str) -> bool:
        preprocessed = self.__preprocess(message)
        tokenized = self.__tokenize(preprocessed)
        filtered = self.__filter_tokens(tokenized)
        cleaned = self.__clean_tokens(filtered)
        score = self.__score_tokens(cleaned)

        if self.debug:
            print("msg: %.2f  %s" % (score, repr(message)))
            print("Preproc:   %s" % repr(preprocessed))
            print("Tokenized: %s" % tokenized)
            print("Filtered:  %s" % filtered)
            print("Cleaned:   %s" % cleaned)
            print()

        return score >= self.__passing_score
