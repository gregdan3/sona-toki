# LOCAL
from sonatoki.ilo import Ilo
from sonatoki.Configs import LazyConfig, PrefConfig, CorpusConfig

pref_ilo = Ilo(**PrefConfig)
lazy_ilo = Ilo(**LazyConfig)
corp_ilo = Ilo(**CorpusConfig)
