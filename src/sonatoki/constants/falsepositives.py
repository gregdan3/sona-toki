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
    "aja",
    "ajaja",
    "ajajaja",
    "ajajajaja",
    "ajajajajaja",
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
    "awa",
    "awake",
    "awaken",
    "awawa",
    "awawawa",
    "awawawawa",
    "awawawawawa",
    "awesome",
    "eje",
    "ejeje",
    "ejejeje",
    "ejejejeje",
    "ejejejejeje",
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
    "ja",  # "yes" in some langs
    "jaja",
    "jajaja",
    "jajajaja",
    "jajajajaja",
    "japan",
    "japanese",
    "japon",
    "je",
    "jeje",
    "jejeje",
    "jejejeje",
    "jejejejeje",
    "joke",
    "june",
    "kale",
    "kana",  # things in other langs that might get imported
    "kanji",
    "kilo",
    "lake",
    "lame",
    "late",
    "latin",
    "latina",
    "latine",
    "latino",
    "le",
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
    "mesa",  # unknown other language, not just eng
    "meta",
    "mile",
    "min",  # esperanto possessive
    "mine",
    "mini",
    "minute",
    "miso",
    "misuse",
    "mojosa",  # esperanto "cool"
    "mojose",  # esperanto 'youthful style'
    "momento",
    "momenton",
    "mon",
    "mono",
    "muse",
    "name",
    "nani",  # romanization of japanese "what"
    "ne",  # no in some languages
    "nepali",
    "nine",
    "ninja",
    "no",
    "non",
    "none",
    "nono",
    "nonono",
    "nononono",
    "nonononono",
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
    "papa",  # spanish and english father
    "pe",
    "pelo",  # spanish for hair
    "pen",  # borderline
    "pin",
    "pole",
    "polite",
    "pope",
    "potato",
    "puta",  # spanish 'bitch'
    "salami",
    "salute",
    "saluton",
    "same",
    "se",  # see
    "semen",
    "semi",
    "sen",  # seen
    "sense",
    "si",  # spanish yes
    "silo",
    "sine",
    "site",
    "so",
    "sole",
    "solo",
    "somali",
    "some",
    "sometime",
    "son",  # primarily "son" and "soon", a bit of sona typo/clipping...
    "sun",
    "ta",
    "take",
    "taken",
    "tape",
    "ten",
    "tense",
    "ti",
    "time",
    "tin",
    "titan",
    "to",
    "toke",
    "ton",
    "tone",
    "tote",
    "u",
    "un",
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
    "wo",
    "woke",
    "woman",
    "women",
    "won",
    # "aka" # in sandbox
    # tuki tiki
    "i",
    "iku",
    "ilu",
    "ka",  # tuki tiki mostly, but not entirely
    "kati",
    "ki",
    "kiku",
    "lapi",
    "lika",
    "liti",
    "muku",
    "muti",
    "paka",
    "puka",
    "pula",
    "taka",
    "tama",
    "tiki",
    "tiko",
    "tiku",
    "tila",
    "tili",
    "tilu",
    "time",
    "timi",
    "tipi",
    "tipo",
    "titi",
    "tuki",
    "tula",
    "tulu",
    "tuti",
    "uli",
    "upi",
}

FALSE_POS_ALPHABETIC: Set[str] = {
    "al",  # all
    "also",
    "animal",
    "animals",
    "as",
    "autism",
    "emotes",
    "estas",
    "is",
    "isnt",
    "it",
    "its",
    "j",
    "jam",
    "jes",
    "jokes",
    "just",
    "kaj",
    "link",
    "litle",
    "lmao",
    "lol",
    "m",
    "makes",
    "males",
    "mas",
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
    "ok",
    "os",  # some command prefix...
    "post",
    "simple",
    "sometimes",
    "spam",
    "t",
    "tens",
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
    "ja",  # basically 'yes' in german
    "je",  # 1st person pronoun, french
    "ka",  # tuki tiki 'being'
    "kana",  # japanese script
    "ki",  # mostly noise and tuki tiki
    "lu",  # preposition in tuki tiki
    "me",  # 1st person singular, english
    "ne",  # no in several languages
    "nu",  # "new" in english, "now" in dutch
    "omen",  # ominous
    "pa",  # variety of non-tp languages
    "papa",  # spanish father
    "se",  # spanish particle, english "see"
    "sole",  # singular, of shoe
    "ta",  # french
    "take",  # acquire, perhaps forcefully or without permission
    "ten",  # 10
    "to",  # to, too
    "u",  # no u
    "we",  # 1st person plural, english
    "wi",  # wii and discussions of syllables
    # "ke" # NOTE: this is here commented so i don't investigate again. it needs to stay.
    # "lo",  # common typo of 'li' and 'lon' but not really a problem
    # unexplored candidates for removal
    # "ewe",  # sheep
}
