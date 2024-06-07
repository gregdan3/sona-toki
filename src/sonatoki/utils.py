# STL
import re
from typing import List

TO_ESCAPE = ["\\", "^", "[", "]", "-"]


def regex_escape(s: str) -> str:
    """Escape all characters which must be escaped when embedded in a character class."""
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


if __name__ == "__main__":
    """
    Helper script to fetch UNICODE_PUNCT in constants.py
    """

    PUNCT_CATEGORIES = {
        "Pc",
        "Pd",
        "Pe",
        "Pf",
        "Pi",
        "Po",
        "Ps",
        "Sm",
        "Sk",
        "Sc",
        "So",
    }
    # Connector, Dash, Close (end), Final, Initial, Other, Open (sOpen), Math, Modifier (kModifier), Currency, Other

    # NOTE: UnicodeData.txt lists character ranges if there would be many characters.
    # (e.g. CJK Ideograph, First at 4E00 and CJK Ideograph, Last at 9FFF).
    # This does not apply to any currently defined punctuation category.

    EXCEPTION_RANGES = re.compile(r"""[Ⓐ-ⓩ🄰-🅉🅐-🅩🅰-🆉]+""")
    # These groups are in Symbol other (So) but are not part of `\p{Punctuation}`
    # NOTE: There are many characters which look like writing characters but are not. Examples:
    # - kangxi radicals from ⺀ to ⿕ which are for demonstration
    # - circled katakana from  to ㋾ which... shouldn't be in \p{Punctuation} but oh well

    def is_punctuation(data: List[str]):
        return data[2] in PUNCT_CATEGORIES

    def get_character(data: List[str]):
        return chr(int(data[0], 16))

    def is_exception(c: str):
        return not not re.fullmatch(EXCEPTION_RANGES, c)

    # http://www.unicode.org/Public/UNIDATA/UnicodeData.txt
    unicode_punctuation = ""
    with open("UnicodeData.txt", "r") as f:
        for line in f:
            data = line.split(";")
            if not is_punctuation(data):
                continue

            char = get_character(data)
            if is_exception(char):
                continue

            unicode_punctuation += char

    with open("UnicodePunctuation.txt", "w") as f:
        _ = f.write(unicode_punctuation)
