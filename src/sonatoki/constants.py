# STL
import json
from typing import Dict, List
from pathlib import Path

LINKU = Path(__file__).resolve().parent / Path("linku.json")
SANDBOX = Path(__file__).resolve().parent / Path("sandbox.json")

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS
ALPHABET_SET = set(ALPHABET)

LANGUAGE = "english"  # for NLTK

# `\p{posix_punct}` character class
POSIX_PUNCT = r"""-!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""
PRUNED_POSIX_PUNCT = r"""$+<=>^`|~"""  # only those that are not in UNICODE_PUNCT

# `\p{Punctuation}` character class
UNICODE_PUNCT = r"""!"#%&'()*,-./:;?@\[\\\]_{}¡§«¶·»¿;·՚՛՜՝՞՟։֊־׀׃׆׳״؉؊،؍؛؝؞؟٪٫٬٭۔܀܁܂܃܄܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾࡞।॥॰৽੶૰౷಄෴๏๚๛༄༅༆༇༈༉༊་༌།༎༏༐༑༒༔༺༻༼༽྅࿐࿑࿒࿓࿔࿙࿚၊။၌၍၎၏჻፠፡።፣፤፥፦፧፨᐀᙮᚛᚜᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠆᠇᠈᠉᠊᥄᥅᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᭽᭾᯼᯽᯾᯿᰻᰼᰽᰾᰿᱾᱿᳀᳁᳂᳃᳄᳅᳆᳇᳓‐‑‒–—―‖‗‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›※‼‽‾‿⁀⁁⁂⁃⁅⁆⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⁽⁾₍₎⌈⌉⌊⌋〈〉❨❩❪❫❬❭❮❯❰❱❲❳❴❵⟅⟆⟦⟧⟨⟩⟪⟫⟬⟭⟮⟯⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⧘⧙⧚⧛⧼⧽⳹⳺⳻⳼⳾⳿⵰⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸓⸔⸕⸖⸗⸘⸙⸚⸛⸜⸝⸞⸟⸠⸡⸢⸣⸤⸥⸦⸧⸨⸩⸪⸫⸬⸭⸮⸰⸱⸲⸳⸴⸵⸶⸷⸸⸹⸺⸻⸼⸽⸾⸿⹀⹁⹂⹃⹄⹅⹆⹇⹈⹉⹊⹋⹌⹍⹎⹏⹒⹓⹔⹕⹖⹗⹘⹙⹚⹛⹜⹝、。〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〽゠・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶꡷꣎꣏꣸꣹꣺꣼꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꫰꫱꯫﴾﴿︐︑︒︓︔︕︖︗︘︙︰︱︲︳︴︵︶︷︸︹︺︻︼︽︾︿﹀﹁﹂﹃﹄﹅﹆﹇﹈﹉﹊﹋﹌﹍﹎﹏﹐﹑﹒﹔﹕﹖﹗﹘﹙﹚﹛﹜﹝﹞﹟﹠﹡﹣﹨﹪﹫！＂＃％＆＇（）＊，－．／：；？＠［＼］＿｛｝｟｠｡｢｣､･𐄀𐄁𐄂𐎟𐏐𐕯𐡗𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕𐩖𐩗𐩘𐩿𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐬹𐬺𐬻𐬼𐬽𐬾𐬿𐮙𐮚𐮛𐮜𐺭𐽕𐽖𐽗𐽘𐽙𐾆𐾇𐾈𐾉𑁇𑁈𑁉𑁊𑁋𑁌𑁍𑂻𑂼𑂾𑂿𑃀𑃁𑅀𑅁𑅂𑅃𑅴𑅵𑇅𑇆𑇇𑇈𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑚𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑚹𑜼𑜽𑜾𑠻𑥄𑥅𑥆𑧢𑨿𑩀𑩁𑩂𑩃𑩄𑩅𑩆𑪚𑪛𑪜𑪞𑪟𑪠𑪡𑪢𑬀𑬁𑬂𑬃𑬄𑬅𑬆𑬇𑬈𑬉𑱁𑱂𑱃𑱄𑱅𑱰𑱱𑻷𑻸𑽃𑽄𑽅𑽆𑽇𑽈𑽉𑽊𑽋𑽌𑽍𑽎𑽏𑿿𒑰𒑱𒑲𒑳𒑴𒿱𒿲𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖭄𖺗𖺘𖺙𖺚𖿢𛲟𝪇𝪈𝪉𝪊𝪋𞥞𞥟"""
# NOTE: This list diverges slightly from the raw list, since []\ must be escaped
# The [] need to be escaped to avoid prematurely closing the regex character class
# The \ needs to be escaped to be considered as a raw \

# https://www.compart.com/en/unicode/category
# https://unicode.org/Public/UNIDATA/UnicodeData.txt


"""Commonly occurring strings which are some kind of valid Toki Pona or external token"""
ALLOWABLES = {
    "cw",  # Content Warning
    "x",  # ala
    "y",  # anu
    "kxk",  # ken ala ken
    "wxw",  # wile ala wile
}


with open(LINKU) as f:
    r: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_PU: List[str] = [d["word"] for d in r.values() if d["book"] == "pu"]
    NIMI_PU_ALE: List[str] = NIMI_PU + ["namako", "kin", "oko"]
    NIMI_LINKU: List[str] = [
        d["word"] for d in r.values() if d["usage_category"] in ["core", "common"]
    ]
    NIMI_LINKU_ALE: List[str] = [d["word"] for d in r.values()]

with open(SANDBOX) as f:
    r: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_LINKU_SANDBOX: List[str] = [d["word"] for d in r.values()]


NIMI_PU_SET = set(NIMI_PU)
NIMI_PU_ALE_SET = set(NIMI_PU_ALE)
NIMI_LINKU_SET = set(NIMI_LINKU)
NIMI_LINKU_ALE_SET = set(NIMI_LINKU_ALE)
NIMI_LINKU_SANDBOX_SET = set(NIMI_LINKU_SANDBOX)
ALLOWABLES_SET = set(ALLOWABLES)

__all__ = [
    "VOWELS",
    #
    "CONSONANTS",
    #
    "ALPHABET",
    "ALPHABET_SET",
    #
    "NIMI_PU",
    "NIMI_PU_SET",
    #
    "NIMI_PU_ALE",
    "NIMI_PU_ALE_SET",
    #
    "NIMI_LINKU",
    "NIMI_LINKU_SET",
    #
    "NIMI_LINKU_ALE",
    "NIMI_LINKU_ALE_SET",
    #
    "NIMI_LINKU_SANDBOX",
    "NIMI_LINKU_SANDBOX_SET",
]
