# sona toki

<div align="center">

![Test workflow for this library](https://github.com/gregdan3/sona-toki/workflows/Tests/badge.svg)
[![Version number for this library](https://img.shields.io/pypi/v/sonatoki?logo=python&logoColor=%23cccccc)](https://pypi.org/project/sonatoki)

</div>

## What is **sona toki**?

This library, "Language Knowledge," helps you identify whether a message is in Toki Pona. It does so by determining whether a large enough number of words in a statement are "in Toki Pona". No grammar checking, yet.

I wrote this library with a variety of scraps and lessons learned from a prior project, [ilo pi toki pona taso, "toki-pona-only tool"](https://github.com/gregdan3/ilo-pi-toki-pona-taso). That tool now uses this library to great success!

If you've ever worked on a similar project, you know the question "is this message in [language]" is not a consistent one- the environment, topic, preferences of the speaker, and much more, can all alter whether a given message is "in" any specific language. This complexity applies to Toki Pona too.

So, this project "solves" that complex problem by offering an opinionated tokenizer and a configurable parser, allowing you to tune its output to your preferences and goals. [Even silly ones.](https://sona.pona.la/wiki/isipin_epiku)

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
from sonatoki.Filters import NimiLinkuCore, NimiLinkuCommon, Phonotactic, ProperName, Or
from sonatoki.Scorers import SoftPassFail

def main():
    config = deepcopy(BaseConfig)
    config["scoring_filters"].extend([Or(NimiLinkuCore, NimiLinkuCommon), Phonotactic, ProperName])
    config["scorer"] = SoftPassFail

    ilo = Ilo(**config)
    ilo.is_toki_pona("mu mu!")  # True
    ilo.is_toki_pona("mi namako e moku mi")  # True
    ilo.is_toki_pona("ma wulin")  # False

if __name__ == "__main__":
    main()
```

`Ilo` is highly configurable by necessity, so I recommend looking through the premade configs in `Configs` as well as the individual `Preprocessors`, `Filters`, and `Scorers`. In `Cleaners`, all you need is `ConsecutiveDuplicates`. In `Tokenizers`, the preferred tokenizers `WordTokenizer` and `SentTokenizer` are already the default in `Ilo`.

## Development

1. Install [pdm](https://github.com/pdm-project/pdm)
1. `pdm install --dev`
1. Open any file you like!

## FAQ

### Why isn't this README/library written in Toki Pona?

The intent is to show our methodology to the Unicode Consortium, particularly to the Script Encoding Working Group (previously the Script Ad Hoc Group). As far as we're aware, zero members of the committee know Toki Pona, which unfortunately means we fall back on English.

I originally intended to translate this file and library into Toki Pona once Unicode had reviewed our proposal, but this library has picked up some interest outside of the Toki Pona community, so this library and README will remain accessible to them.

### What's the deal with the tokenizers?

The Toki Pona tokenizer `sonatoki.Tokenizers.WordTokenizer` attempts to tokenize statements such that every token either represents a word candidate ("toki", "mumumu") or a complete non-candidate ("..!", "123").
This design is highly undesirable for NLTK's English tokenizer because English words can have "punctuation" characters in them such as `'` or `-`.
Toki Pona doesn't have any mid-word symbols when rendered in the Latin alphabet or in [Private Use Area Unicode characters](https://www.kreativekorp.com/ucsur/), so a more aggressive tokenizer is highly desirable.

The goal of splitting into word candidates and non-candidates is important, because any [encoding of Toki Pona's logographic script](https://www.kreativekorp.com/ucsur/charts/sitelen.html) will require each character be split into its own token, where the default behavior would be to leave consecutive non-punctuation together.

### Aren't there a lot of false positives?

For any individual filter, yes. Here are some examples:

- `ProperName` will errantly match text in languages without a capital/lowercase distinction
- `Alphabetic` matches words so long as they are only made of letters in Toki Pona's alphabet, which is 14 letters of the Latin alphabet.
- `Syllabic` and `Phonetic`, despite imposing more structure than `Alphabetic`, will match a surprising amount of English words. For example, every word in "an awesome joke!" matches.
- `NimiPu` and `NimiLinkuCore` will match `a`, `mute`, `open` regardless of the surrounding language.

This is point of `Ilo` and the `Scorers`: None of these filters would _individually_ be able to correctly identify a Toki Pona statement, but all of them working together with some tuning are able to achieve a surprisingly high accuracy.

### Don't some of the cleaners/filters conflict?

Yes, though not terribly much.

- `ConsecutiveDuplicates` may errantly change a word's validity. For example, "manna" is phonotactically invalid in Toki Pona, but would become "mana" which is valid.
- `ConsecutiveDuplicates` will not work correctly with syllabaries, though this should not change the validity of the analyzed word unless you attempt to dictionary match these words.
- If you build your own `MemberFilter` with words that have capital letters or consecutive duplicates, they will never match unless you use `prep_dictionary`.

You'll notice these are mostly casued by applying latin alphabet filters to non-latin text. Working on it!
