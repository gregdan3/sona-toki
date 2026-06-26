# PDM
import pytest

# LOCAL
from sonatoki.Configs import (
    LazyConfig,
    PrefConfig,
    CorpusConfig,
    IsipinEpikuConfig,
    ExperimentalConfig,
)
from tests.data.types import Performance

CONFIGS = [
    Performance(PrefConfig, name="preferred", score=0.9),
    Performance(CorpusConfig, name="corpus", score=0.9),
    Performance(LazyConfig, name="lazy", score=0.5),
    Performance(ExperimentalConfig, name="experimental", score=0.8),
    Performance(IsipinEpikuConfig, name="isipin epiku", score=0.2),
]

PARAMETERIZED = [pytest.param(c, id=c.name) for c in CONFIGS]
