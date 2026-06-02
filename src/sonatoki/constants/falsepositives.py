# STL
from typing import Set
from pathlib import Path

SYLLABICS = Path(__file__).resolve().parent / Path("syllabic.txt")
ALPHABETICS = Path(__file__).resolve().parent / Path("alphabetic.txt")

# with open(SYLLABICS, "r", encoding="utf-8") as f:
#     FALSE_POS_SYLLABIC = {line.strip() for line in f}
#
# with open(ALPHABETICS, "r", encoding="utf-8") as f:
#     FALSE_POS_ALPHABETIC = {line.strip() for line in f}


# NOTE: This is being tracked manually rather than fetched from syllabics.txt until I am convinced that solution is appropriate
FALSE_POS_SYLLABIC = {
    "alike",
    "alone",
    "amen",
    "amo",  # love in spanish, ammo in english
    "amuse",
    "an",
    "animate",
    "anime",
    "antelope",
    "antena",
    "anti",
    "apetite",
    "asasin",
    "asasinate",
    "asinine",
    "asume",
    "ate",
    "atone",
    "awake",
    "awaken",
    "awesome",
    "eliminate",
    "elite",
    "elo",
    "emanate",
    "emo",
    "emoji",
    "emote",
    "i",
    "iluminate",
    "ime",  # "in my experience"
    "imense",
    "imitate",
    "imo",  # "in my opinion"
    "in",
    "inanimate",
    "injoke",
    "insane",
    "insolate",
    "insulate",
    "intense",
    "into",
    "ipa",
    "isolate",
    "jaja",
    "jajaja",
    "jajajaja",
    "jajajajaja",
    "japan",
    "japanese",
    "japon",
    "ja",  # "yes" in some langs
    "joke",
    "june",
    "kale",
    "ka",  # tuki tiki mostly
    "kilo",
    "lame",
    "late",
    "latina",
    "latine",
    "latino",
    "lemon",
    "leson",
    "like",
    "likewise",
    "line",
    "lone",
    "lose",
    "luna",
    "make",
    "male",
    "man",
    "manipulate",
    "mate",
    "me",
    "melon",
    "meme",
    "men",
    "menu",
    "meta",
    "mile",
    "min",  # borderline
    "mine",
    "mini",
    "minute",
    "miso",
    "misuse",
    "mon",
    "mono",
    "muse",
    "name",
    "nani",  # romanization of japanese "what"
    "ne",  # "no" in some languages
    "nepali",
    "nine",
    "ninja",
    "no",
    "non",
    "none",
    "nono",
    "nonsense",
    "nope",
    "nose",
    "note",
    "omen",
    "on",
    "one",
    "online",
    "onto",
    "oposite",
    "owo",  # emoticon
    "pale",
    "pelo",  # spanish for hair
    "pen",  # borderline
    "pin",
    "pole",
    "polite",
    "pope",
    "potato",
    "puta",  # spanish 'bitch'
    "salami",
    "saluton",
    "same",
    "semen",
    "semi",
    "sense",
    "sen",  # seen
    "se",  # see
    "silo",
    "sine",
    "so",
    "solo",
    "somali",
    "some",
    "sometime",
    "son",  # sona typo, but also "son" and "soon"
    "sun",
    "take",
    "taken",
    "tape",
    "ten",
    "tense",
    "time",
    "to",
    "ton",
    "tone",
    "tote",
    "une",
    "unite",
    "unlike",
    "unmute",
    "uno",
    "usa",
    "use",
    "usona",
    "usono",
    "uwu",  # emoticon
    "wana",
    "we",  # word in sandbox
    "win",
    "wine",
    "wise",
    "woke",
    "woman",
    "women",
    "won",
    # tuki tiki
    "iku",
    "ilu",
    "kati",
    "kiku",
    "lapi",
    "paka",
    "pula",
    "taka",
    "tiki",
    "tiku",
    "tila",
    "tilu",
    "timi",
    "muti",
    "titi",
    "tuki",
    "tula",
    "upi",
    # "aka" # in sandbox
    # "papa",  # now in sandbox
}

FALSE_POS_ALPHABETIC: Set[str] = {
    "also",
    "animal",
    "animals",
    "as",
    "emotes",
    "is",
    "isnt",
    "it",
    "its",
    "jam",
    "jokes",
    "just",
    "kaj",
    "link",
    "litle",
    "lmao",
    "lol",
    "makes",
    "males",
    "mates",
    "mean",
    "means",
    "meant",
    "memes",
    "moment",
    "names",
    "new",
    "nopes",
    "not",
    "noun",
    "os",  # some command prefix...
    "post",
    "simple",
    "sometimes",
    "spam",
    "t",
    "unles",
    "uses",
    "wait",
    "waow",
    "wel",
    "wow",
}


DICT_PHONOMATCHES = {
    # Sandbox words are removed from the CorpusConfig if they appear more frequently in languages other than Toki Pona by a factor of at least 3.
    # In this case, all of these appear more often in other languages by a factor of at least 10.
    "aka",  # also known as
    "an",  # article
    "api",  # API
    "i",  # 1st person
    "je",  # 1st person pronoun, french
    "ja",  # basically 'yes' in german
    "ka",  # tuki tiki 'being'
    # "ke" # NOTE: this is here commented so i don't investigate again. it needs to stay.
    "kana",  # japanese script
    "ki",  # mostly noise
    "lu",  # preposition in tuki tiki
    "me",  # 1st person singular, english
    "ne",  # "no" in several languages
    "nu",  # "new" in english, "now" in dutch
    "omen",  # ominous
    "pa",  # variety of non-tp languages
    "se",  # spanish particle, english "see"
    "sole",  # singular, of shoe
    "take",  # acquire, perhaps forcefully or without permission
    "ten",  # 10
    "to",  # to, too
    "u",  # no u
    "we",  # 1st person plural, english
    "wi",  # wii and discussions of syllables
    # unexplored candidates for removal
    # "papa",  # father
    # "lo",  # "lo" and "loo"
    # "ewe",  # sheep
}
