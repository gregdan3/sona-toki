# STL
import json
from typing import Set, Dict, Optional
from pathlib import Path

# LOCAL
from sonatoki.types import LinkuWord, LinkuUsageDate

LINKU = Path(__file__).resolve().parent / Path("linku.json")
SANDBOX = Path(__file__).resolve().parent / Path("sandbox.json")

LATEST_DATE = "2025-09"
# hardcoding this seems bad, but it means the parser is stable w.r.t. Linku!


def linku_data() -> Dict[str, LinkuWord]:
    # NOTE: this does open+read+parse two files each time you construct a filter
    # but i expect users to construct filters only at the start of runtime
    # there is no reason to waste your RAM by leaving the linku data in it
    with open(LINKU, "r", encoding="utf-8") as f:
        linku: Dict[str, LinkuWord] = json.loads(f.read())
    with open(SANDBOX, "r", encoding="utf-8") as f:
        sandbox: Dict[str, LinkuWord] = json.loads(f.read())

    return {**linku, **sandbox}


def words_by_tag(tag: str, value: str) -> Set[str]:
    data = linku_data()
    return {d["word"] for d in data.values() if d[tag] == value}


def words_by_usage(
    usage: int,
    date: Optional[LinkuUsageDate] = None,
) -> Set[str]:
    if not date:
        date = LATEST_DATE
    data = linku_data()

    result: Set[str] = set()
    for word in data.values():
        if usage == 0:
            result.add(word["word"])
            continue

        usages = word["usage"]
        if date in usages and usages[date] >= usage:
            result.add(word["word"])

    return result


NIMI_PU_SYNONYMS = {"namako", "kin", "oko"}
