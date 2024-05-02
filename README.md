# sona toki

## What is **sona toki**?

This library, "Language Knowledge," helps you identify whether a message is in Toki Pona. No grammar checking, yet, which means this more checks whether a given message has enough Toki Pona words.

I wrote it with a variety of scraps and lessons learned from a prior project, [ilo pi toki pona taso, "toki-pona-only tool"](https://github.com/gregdan3/ilo-pi-toki-pona-taso). That tool will be rewritten to use this library shortly.

If you've ever worked on a similar project, you know the question "is this message in [language]" is not a consistent one- the environment, time, preferences of the speaker, and much more, can all alter whether a given message is "in toki pona," and this applies to essentially any language.

This project "solves" that complex problem by offering a highly configurable and incredibly lazy parser

## Quick Start

Install with your preferred Python package manager. Example:

```sh
pdm init  # if your pyproject.toml doesn't exist yet
pdm add sonatoki
```

Then get started with a script along these lines:

```py
from sonatoki.Filters import (
    Numerics,
    Syllabic,
    NimiLinku,
    Alphabetic,
    ProperName,
    Punctuations,
)
from sonatoki.Scorers import Scaling
from sonatoki.Cleaners import ConsecutiveDuplicates
from sonatoki.Tokenizers import word_tokenize_tok
from sonatoki.Preprocessors import URLs, DiscordEmotes

def main():
    ilo = Ilo(
        preprocessors=[URLs, DiscordEmotes],
        ignoring_filters=[Numerics, Punctuations],
        scoring_filters=[NimiLinku, Syllabic, ProperName, Alphabetic],
        cleaners=[ConsecutiveDuplicates],
        scorer=Scaling,
        tokenizer=word_tokenize_tok,
    )
    ilo.is_toki_pona("imagine how is touch the sky")  # False
    ilo.is_toki_pona("o pilin insa e ni: sina pilin e sewi")  # True

if __name__ == "__main__":
    main()
```

`Ilo` is highly configurable by design, so I recommend exploring the `Preprocessors`, `Filters`, and `Scorers` modules. The `Cleaners` module only contains one cleaner, which I highly recommend. The `Tokenizers` module contains several other word tokenizers, but their performance will be worse than the

## Development

1. Install [pdm](https://github.com/pdm-project/pdm)
1. `pdm sync --dev`
1. Open any file you like!

## FAQ

### Why isn't this README/library written in Toki Pona?

The intent is to show our methodology to the Unicode Consortium, particularly to the Script Encoding Working Group (previously the Script Ad Hoc Group). As far as we're aware, zero members of the committee know Toki Pona, which unfortunately means we fall back on English.

After our proposal has been examined and a result given by the committee, I will translate this file and library into Toki Pona, with a note left behind for those who do not understand it.

### Why aren't any of the specific
