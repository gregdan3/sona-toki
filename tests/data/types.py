# STL
from typing import List, Union
from dataclasses import dataclass

# LOCAL
from sonatoki.types import Number
from sonatoki.Configs import IloConfig


@dataclass
class Transform:
    """A test case. An arbitrary operation is performed on `input` which is
    expected to result in `output`."""

    input: str
    output: Union[bool, str, List[str]]
    xfail: bool = False
    weight: Number = 1.0
    name: str = ""


@dataclass
class Equal:
    """A test case. An operation is performed on both `s1` and `s2` which is
    expected to have the same outcome for both."""

    s1: str
    s2: str
    xfail: bool = False
    weight: Number = 1.0
    name: str = ""


@dataclass
class Performance:
    """Test cases specifically for sonatoki.ilo.Ilo.
    Score describes the minimum performance of the config against all test cases.

    Variance describes the allowable range of an individual test score. If a
    test would fail, but the score is within `variance` of passing for that
    config, the test passes with a penalty."""

    config: IloConfig
    score: Number = 0.8
    variance: Number = 0.05
    name: str = ""
