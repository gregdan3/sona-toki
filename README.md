# sona toki

<div align="center">

![Test workflow for this library](https://github.com/gregdan3/sona-toki/workflows/Tests/badge.svg)
[![Version number for this library](https://img.shields.io/pypi/v/sonatoki?logo=python&logoColor=%23cccccc)](https://pypi.org/project/sonatoki)

</div>

## What is **sona toki**?

This library, "Language Knowledge," helps you identify whether a message is in Toki Pona. It does so by determining whether a large enough number of words in a statement are "in Toki Pona". No grammar checking, yet.

I wrote this library with a variety of scraps and lessons learned from a prior project, [ilo pi toki pona taso, "toki-pona-only tool"](https://github.com/gregdan3/ilo-pi-toki-pona-taso). That tool now uses this library to great success!

If you've ever worked on a similar project, you know the question "is this message in [language]" is not a consistent one- the environment, time, preferences of the speaker, and much more, can all alter whether a given message is "in" any specific language. This complexity applies to Toki Pona too.

So, this project "solves" that complex problem by offering an opinionated tokenizer and a configurable parser, allowing you to tune its output to your preferences and goals. [Even silly ones.](https://sona.pona.la/wiki/isipin_epiku).

## Quick Start

Install with your preferred Python package manager. Example:

```sh
pdm init  # if your pyproject.toml doesn't exist yet
pdm add sonatoki
```

Then get started with a script along these lines:

```py
from sonatoki.ilo import Ilo
from sonatoki.Configs import PrefConfig

def main():
    ilo = Ilo(**PrefConfig)
    ilo.is_toki_pona("imagine how is touch the sky")  # False
    ilo.is_toki_pona("o pilin insa e ni: sina pilin e sewi")  # True
    ilo.is_toki_pona("I Think I Can Evade Detection")  # False

if __name__ == "__main__":
    main()
```

Or if you'd prefer to configure on your own:

```py
from copy import deepcopy
from sonatoki.ilo import Ilo
from sonatoki.Configs import BaseConfig
from sonatoki.Filters import NimiLinkuCore, Phonotactic, ProperName
from sonatoki.Scorers import SoftPassFail

def main():
    config = deepcopy(BaseConfig)
    config["scoring_filters"].extend([NimiLinkuCore, Phonotactic, ProperName])
    config["scorer"] = SoftPassFail

    ilo = Ilo(**config)
    ilo.is_toki_pona("mu mu!")  # True
    ilo.is_toki_pona("mi namako e moku mi")  # True
    ilo.is_toki_pona("ma wulin")  # False

if __name__ == "__main__":
    main()
```

`Ilo` is highly configurable by necessity, so I recommend looking through the premade configs in `Configs` as well as the individual `Preprocessors`, `Filters`, and `Scorers`. The `Cleaners` module only contains one cleaner, which I recommend always using. Similarly, the `Tokenizers` module contains several other word tokenizers, but their performance will be worse than the dedicated Toki Pona tokenizer `WordTokenizerTok`.

## Development

1. Install [pdm](https://github.com/pdm-project/pdm)
1. `pdm install --dev`
1. Open any file you like!

## FAQ

### Why isn't this README/library written in Toki Pona?

The intent is to show our methodology to the Unicode Consortium, particularly to the Script Encoding Working Group (previously the Script Ad Hoc Group). As far as we're aware, zero members of the committee know Toki Pona, which unfortunately means we fall back on English.

After our proposal has been examined and a result given by the committee, I will translate this file and library into Toki Pona, with a note left behind for those who do not understand it.

### What's the deal with the tokenizers?

The Toki Pona tokenizer `sonatoki.Tokenizers.WordTokenizer` has the goal of tokenizing statements such that every token either represents a word candidate ("toki", "mumumu") or a complete non-candidate ("..!", "123").
This design is highly undesirable for NLTK's English tokenizer because English words can have "punctuation" characters in them.
But Toki Pona doesn't have any mid-word symbols when rendered in the Latin alphabet or in [Private Use Area Unicode characters](https://www.kreativekorp.com/ucsur/), so a more aggressive tokenizer is highly desirable.

The goal of splitting into word candidates and non-candidates is important, because any [encoding of Toki Pona's logographic script](https://www.kreativekorp.com/ucsur/charts/sitelen.html) will require each character be split into its own token, where the default behavior would be to leave consecutive non-punctuation together.

### Aren't there a lot of false positives?

Yes, depending on the filter you choose and how you apply it.
It's up to you to use this tool responsibly on input you've done your best to clean, such as by using stronger filters before weaker ones.
For now though, here's a list of relevant false positives:

- `ProperName` will errantly match text in languages without a capital/lowercase distinction, artificially increasing scores.
- `Alphabetic` will match a _lot_ of undesirable text- it essentially allows 14 letters of the English alphabet. For example, "I'm well" would match as _three_ words: "i", "m", "well".
- `NimiPu` and other sets containing `a`, `mute`, `open`, and others will unavoidably match those words in English text too.

### Don't some of the cleaners/filters conflict?

Yes, though not terribly much.

- `ConsecutiveDuplicates` may errantly change a word's validity. For example, "manna" is phonotactically invalid in Toki Pona, but would become "mana" which is valid.
- `ConsecutiveDuplicates` will not work correctly with syllabaries, though this should not change the validity of the analyzed word unless you attempt to dictionary match these words.
- If you build your own `MemberFilter` with words that have capital letters or consecutive duplicates, they will never match unless you use `prep_dictionary`.

You'll notice these are mostly casued by applying latin alphabet filters to non-latin text. Working on it!
