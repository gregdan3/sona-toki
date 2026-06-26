# LOCAL
from tests.data.types import Equal

CASES = [
    Equal("", ""),
    Equal(" ", ""),
    Equal("2+2=5", ""),
    Equal("https://mun.la/sona", ""),
    Equal("https://example.com/", ""),
    Equal(
        "<:owe:843315277286473778><:owe:843315277286473778><:owe:843315277286473778><:owe:843315277286473778><:owe:843315277286473778>",
        "",
    ),
    Equal("...", ""),
    Equal("·····", ""),
    Equal("❤️", ""),  # heart
    Equal("😊", ""),
    Equal("👨‍👩‍👧‍👧", ""),  # family emoji with zwj
    # every non-emoji in the writables
    Equal(
        "🄀🄁🄂🄃🄄🄅🄆🄇🄈🄉🄊🄋🄌🄍🄎🄏🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩🄪🄫🄬🄭🄮🄯🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🅊🅋🅌🅍🅎🅏🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅪🅫🅬🅭🅮🅯🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🆊🆋🆌🆍🆏🆐 🆛🆜🆝🆞🆟🆠🆡🆢🆣🆤🆥🆦🆧🆨🆩🆪🆫🆬🆭🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿",
        "",
    ),
    Equal("🅰️🅱️🅾️🅱️🅰️", ""),  # blood type emojis
    Equal("kiwen moli 42", "kiwen moli"),
    Equal("mi wile e ni: <https://example.com> li pona", "mi wile e ni: li pona"),
    Equal("lipu https://example.com li kama pona", "lipu li kama pona"),
    Equal(" ⟨·⟩, a", "a"),
    Equal("o lukin: [[w:QWERTY]]", "o lukin:"),
    Equal(
        "nasa la mi ken pana e ni: <unrelated_words_that_are_illegal>",
        "nasa la mi ken pana e ni:",
    ),
    Equal("o tawa [lipu ni](https://example.com) a", "o tawa lipu ni a"),
    Equal("mi pana e lipu ni: [[Borborygmos]]", "mi pana e lipu ni:"),
    Equal("o lukin: [[Borborygmos]]", "o lukin:"),
    Equal("pona :o", "pona o"),
    Equal("a. sona. pona.  ._.", "a sona pona"),
    Equal("monsuta a O_O", "monsuta a"),
    Equal("mi pilin ike v.v", "mi pilin ike", True),  # due to Lazy
    Equal("sina wile lukin anu seme  uwu", "sina wile lukin anu seme"),
    Equal("super bruh moment 64", "super bruh moment"),
    Equal("o lukin e ni: https://example.com/", "o lukin e ni:"),
    Equal("ni li nasa anu seme <:musiwawa:198591138591>", "ni li nasa anu seme"),
    Equal(
        "seme la ni li toki pona ala https://example.com/",
        "seme la ni li toki pona ala",
    ),
    Equal("```\ndef bad():\n    pass\n``` o lukin e ni", "o lukin e ni"),
    Equal("mi tawa tomo telo 💦💦", "mi tawa tomo telo"),
    Equal("o lukin e lipu ni: [[wp:Canvassing]]", "o lukin e lipu ni:"),
    Equal("I see :)", "I see"),
    Equal("te amo <3", "te amo"),
    Equal("Laura, te amo <3", "Laura te amo"),
    Equal("kalamARRRR", "kalamar"),
    Equal("mi musi Space Station 13", "mi musi Space Station"),
    Equal("    sina    seme     e     mi     ?", "sina seme e mi?"),
    Equal("muuuu MUUU muUuUuU", "mu mu mu"),
    Equal("󱥄󱥬󱥩󱤴", "o toki tawa mi", True),  # due to isipin epiku
    Equal("󱥬‍󱥔​󱥬󱦕󱥔", "toki pona toki pona", True),  # same
    Equal("󱥬‍󱥔​󱥬󱦕󱥔", "󱥬‍󱥔󱥬󱥔"),
    Equal("nope, no, joke", "nope no joke"),
]
