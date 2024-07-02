# STL
import itertools
from typing import Set, List, TypeVar, Iterable

# LOCAL
from sonatoki.Cleaners import Lowercase, ConsecutiveDuplicates

TO_ESCAPE = ["\\", "^", "[", "]", "-"]

T = TypeVar("T")


def prep_dictionary(words: Iterable[str]) -> Set[str]:
    out: Set[str] = set()
    cleaners = [Lowercase, ConsecutiveDuplicates]
    for word in words:
        for c in cleaners:
            word = c.clean(word)
        out.add(word)
    return out


def regex_escape(s: str) -> str:
    """Escape all characters which must be escaped when embedded in a character
    class."""
    for c in TO_ESCAPE:
        s = s.replace(c, rf"\{c}")  # one backslash
    return s


def to_range(start: int, prev: int) -> str:
    if start == prev:
        return rf"\U{start:08x}"
    return rf"\U{start:08x}-\U{prev:08x}"


def find_unicode_ranges(chars: str) -> List[str]:
    if not chars:
        return []

    s_chars = sorted(set(chars))

    ranges: List[str] = []
    start = ord(s_chars[0])
    prev = start

    for i in range(1, len(s_chars)):
        cur = ord(s_chars[i])
        if cur == prev + 1:  # range is still contiguous
            prev = cur
            continue

        ranges.append(to_range(start, prev))
        start = prev = cur

    last = ord(s_chars[-1])
    ranges.append(to_range(start, last))

    return ranges


def find_unicode_chars(ranges: List[str]) -> str:
    result: List[str] = []
    for item in ranges:
        if "-" in item:
            start, end = item.split("-")
            start = int(start.lstrip("\\U"), 16)
            end = int(end.lstrip("\\U"), 16)
            result.extend(chr(code_point) for code_point in range(start, end + 1))
        else:
            result.append(chr(int(item.lstrip("\\U"), 16)))
    return "".join(result)


def overlapping_pairs(iterable: Iterable[T]) -> Iterable[T]:
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    return overlapping_ntuples(iterable, n=2)


def overlapping_ntuples(iterable: Iterable[T], n: int) -> Iterable[T]:
    teed = itertools.tee(iterable, n)
    for i in range(1, n):
        for j in range(i):
            _ = next(teed[i], None)
            # offset start by position

    # ends when any iter is empty; all groups will be same size
    return zip(*teed)
