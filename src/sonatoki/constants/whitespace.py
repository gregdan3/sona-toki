# LOCAL
from sonatoki.utils import find_unicode_chars

UNICODE_WHITESPACE_RANGES = [
    "\\U00000009",  # tab
    "\\U0000000A",  # line feed
    "\\U0000000D",  # carriage return
    "\\U00000020",  # space
    "\\U000000a0",  # no break space
    "\\U00001680",  # ogham space
    "\\U00002000-\\U0000200a",  # various spaces
    # NOTE: three weird cases.
    # ZWS doesn't create visual word boundaries, only text processor boundaries.
    # ZWNJ creates word boundaries and indicates them to text processors
    # ZWJ does not make word boundaries and tends to connect them even
    "\\U0000200b",  # zero width space
    "\\U0000200c",  # zero width non-joiner
    # "\\U0000200d",  # zero width joiner
    "\\U00002028-\\U00002029",  # line, paragraph seps
    "\\U0000202f",  # narrow no break space
    "\\U0000205f",  # math space
    "\\U00003000",  # ideographic space
]
UNICODE_WHITESPACE = find_unicode_chars(UNICODE_WHITESPACE_RANGES)
UNICODE_WHITESPACE_RANGES_STR = "".join(UNICODE_WHITESPACE_RANGES)
