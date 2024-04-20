# STL
from typing import List, Type, Tuple

# LOCAL
from otokipona.Filters import Filter
from otokipona.Scorers import Scorer
from otokipona.Cleaners import Cleaner
from otokipona.Tokenizers import Tokenizer
from otokipona.Preprocessors import Preprocessor


class Ilo:
    __preprocessors: List[Type[Preprocessor]]
    __cleaners: List[Type[Cleaner]]
    __ignoring_filters: List[Type[Filter]]
    __scoring_filters: List[Type[Filter]]
    __scorer: Type[Scorer]
    __tokenize: Tokenizer

    def __init__(
        self,
        preprocessors: List[Type[Preprocessor]],
        cleaners: List[Type[Cleaner]],
        ignoring_filters: List[Type[Filter]],
        scoring_filters: List[Type[Filter]],
        scorer: Type[Scorer],
        tokenizer: Tokenizer,  # NOTE: no wrapper needed?
    ):
        super().__init__()
        # avoid keeping a ref to user's list just in case
        self.__preprocessors = [*preprocessors]
        self.__cleaners = [*cleaners]
        self.__ignoring_filters = [*ignoring_filters]
        self.__scoring_filters = [*scoring_filters]
        self.__scorer = scorer
        self.__tokenize = tokenizer

    def __preprocess(self, msg: str) -> str:
        for p in self.__preprocessors:
            msg = p.process(msg)
        return msg

    # def __tokenize(self, msg: str) -> List[str]:
    #     return self.__tokenizer(msg)

    def __clean_tokens(self, tokens: List[str]) -> List[str]:
        cleaned_tokens: List[str] = list()
        for token in tokens:
            cleaned_token = token
            for c in self.__cleaners:
                cleaned_token = c.clean(cleaned_token)
            if cleaned_token == "":
                raise ValueError("Cleaned token %s and it became empty!" % token)
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
        # TODO: assert 0 <= score <= 1
        return self.__scorer.score(tokens, self.__scoring_filters)

    def is_toki_pona(self, message: str) -> bool:
        message = self.__preprocess(message)
        tokens = self.__tokenize(message)
        # TODO: find falsifying case or prove assumption:
        # order of filter and clean doesn't matter.
        # doing filter first is more efficient if this is true
        tokens = self.__filter_tokens(tokens)
        tokens = self.__clean_tokens(tokens)
        score = self.__score_tokens(tokens)
        return score > 0.8
        # return False
