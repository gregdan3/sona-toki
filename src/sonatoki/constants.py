# STL
import json
from typing import Dict, List
from pathlib import Path

# LOCAL
from sonatoki.utils import find_unicode_ranges

# `\p{Punctuation}` character class
UNICODE_PUNCT = r"""!"#%&'()*+,-./:;<=>?@[\]^_`{|}~¡¦§¨©«¬®¯°±´¶·¸»¿×÷˂˃˄˅˒˓˔˕˖˗˘˙˚˛˜˝˞˟˥˦˧˨˩˪˫˭˯˰˱˲˳˴˵˶˷˸˹˺˻˼˽˾˿͵;΄΅·϶҂՚՛՜՝՞՟։֊֍֎־׀׃׆׳״؆؇؈؉؊،؍؎؏؛؝؞؟٪٫٬٭۔۞۩۽۾܀܁܂܃܄܅܆܇܈܉܊܋܌܍߶߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾࡞࢈।॥॰৺৽੶૰୰௳௴௵௶௷௸௺౷౿಄൏൹෴๏๚๛༁༂༃༄༅༆༇༈༉༊་༌།༎༏༐༑༒༓༔༕༖༗༚༛༜༝༞༟༴༶༸༺༻༼༽྅྾྿࿀࿁࿂࿃࿄࿅࿇࿈࿉࿊࿋࿌࿎࿏࿐࿑࿒࿓࿔࿕࿖࿗࿘࿙࿚၊။၌၍၎၏႞႟჻፠፡።፣፤፥፦፧፨᎐᎑᎒᎓᎔᎕᎖᎗᎘᎙᐀᙭᙮᚛᚜᛫᛬᛭᜵᜶។៕៖៘៙៚᠀᠁᠂᠃᠄᠅᠆᠇᠈᠉᠊᥀᥄᥅᧞᧟᧠᧡᧢᧣᧤᧥᧦᧧᧨᧩᧪᧫᧬᧭᧮᧯᧰᧱᧲᧳᧴᧵᧶᧷᧸᧹᧺᧻᧼᧽᧾᧿᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᭡᭢᭣᭤᭥᭦᭧᭨᭩᭪᭴᭵᭶᭷᭸᭹᭺᭻᭼᭽᭾᯼᯽᯾᯿᰻᰼᰽᰾᰿᱾᱿᳀᳁᳂᳃᳄᳅᳆᳇᳓᾽᾿῀῁῍῎῏῝῞῟῭΅`´῾‐‑‒–—―‖‗‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›※‼‽‾‿⁀⁁⁂⁃⁄⁅⁆⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁒⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⁺⁻⁼⁽⁾₊₋₌₍₎℀℁℃℄℅℆℈℉℔№℗℘℞℟℠℡™℣℥℧℩℮℺℻⅀⅁⅂⅃⅄⅊⅋⅌⅍⅏↊↋←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢⇣⇤⇥⇦⇧⇨⇩⇪⇫⇬⇭⇮⇯⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿⌀⌁⌂⌃⌄⌅⌆⌇⌈⌉⌊⌋⌌⌍⌎⌏⌐⌑⌒⌓⌔⌕⌖⌗⌘⌙⌚⌛⌜⌝⌞⌟⌠⌡⌢⌣⌤⌥⌦⌧⌨〈〉⌫⌬⌭⌮⌯⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⌽⌾⌿⍀⍁⍂⍃⍄⍅⍆⍇⍈⍉⍊⍋⍌⍍⍎⍏⍐⍑⍒⍓⍔⍕⍖⍗⍘⍙⍚⍛⍜⍝⍞⍟⍠⍡⍢⍣⍤⍥⍦⍧⍨⍩⍪⍫⍬⍭⍮⍯⍰⍱⍲⍳⍴⍵⍶⍷⍸⍹⍺⍻⍼⍽⍾⍿⎀⎁⎂⎃⎄⎅⎆⎇⎈⎉⎊⎋⎌⎍⎎⎏⎐⎑⎒⎓⎔⎕⎖⎗⎘⎙⎚⎛⎜⎝⎞⎟⎠⎡⎢⎣⎤⎥⎦⎧⎨⎩⎪⎫⎬⎭⎮⎯⎰⎱⎲⎳⎴⎵⎶⎷⎸⎹⎺⎻⎼⎽⎾⎿⏀⏁⏂⏃⏄⏅⏆⏇⏈⏉⏊⏋⏌⏍⏎⏏⏐⏑⏒⏓⏔⏕⏖⏗⏘⏙⏚⏛⏜⏝⏞⏟⏠⏡⏢⏣⏤⏥⏦⏧⏨⏩⏪⏫⏬⏭⏮⏯⏰⏱⏲⏳⏴⏵⏶⏷⏸⏹⏺⏻⏼⏽⏾⏿␀␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟␠␡␢␣␤␥␦⑀⑁⑂⑃⑄⑅⑆⑇⑈⑉⑊⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◉◊○◌◍◎●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☰☱☲☳☴☵☶☷☸☹☺☻☼☽☾☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿⚀⚁⚂⚃⚄⚅⚆⚇⚈⚉⚊⚋⚌⚍⚎⚏⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛⚜⚝⚞⚟⚠⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯⚰⚱⚲⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿⛀⛁⛂⛃⛄⛅⛆⛇⛈⛉⛊⛋⛌⛍⛎⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡⛢⛣⛤⛥⛦⛧⛨⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿✀✁✂✃✄✅✆✇✈✉✊✋✌✍✎✏✐✑✒✓✔✕✖✗✘✙✚✛✜✝✞✟✠✡✢✣✤✥✦✧✨✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋❌❍❎❏❐❑❒❓❔❕❖❗❘❙❚❛❜❝❞❟❠❡❢❣❤❥❦❧❨❩❪❫❬❭❮❯❰❱❲❳❴❵➔➕➖➗➘➙➚➛➜➝➞➟➠➡➢➣➤➥➦➧➨➩➪➫➬➭➮➯➰➱➲➳➴➵➶➷➸➹➺➻➼➽➾➿⟀⟁⟂⟃⟄⟅⟆⟇⟈⟉⟊⟋⟌⟍⟎⟏⟐⟑⟒⟓⟔⟕⟖⟗⟘⟙⟚⟛⟜⟝⟞⟟⟠⟡⟢⟣⟤⟥⟦⟧⟨⟩⟪⟫⟬⟭⟮⟯⟰⟱⟲⟳⟴⟵⟶⟷⟸⟹⟺⟻⟼⟽⟾⟿⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿⤀⤁⤂⤃⤄⤅⤆⤇⤈⤉⤊⤋⤌⤍⤎⤏⤐⤑⤒⤓⤔⤕⤖⤗⤘⤙⤚⤛⤜⤝⤞⤟⤠⤡⤢⤣⤤⤥⤦⤧⤨⤩⤪⤫⤬⤭⤮⤯⤰⤱⤲⤳⤴⤵⤶⤷⤸⤹⤺⤻⤼⤽⤾⤿⥀⥁⥂⥃⥄⥅⥆⥇⥈⥉⥊⥋⥌⥍⥎⥏⥐⥑⥒⥓⥔⥕⥖⥗⥘⥙⥚⥛⥜⥝⥞⥟⥠⥡⥢⥣⥤⥥⥦⥧⥨⥩⥪⥫⥬⥭⥮⥯⥰⥱⥲⥳⥴⥵⥶⥷⥸⥹⥺⥻⥼⥽⥾⥿⦀⦁⦂⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⦙⦚⦛⦜⦝⦞⦟⦠⦡⦢⦣⦤⦥⦦⦧⦨⦩⦪⦫⦬⦭⦮⦯⦰⦱⦲⦳⦴⦵⦶⦷⦸⦹⦺⦻⦼⦽⦾⦿⧀⧁⧂⧃⧄⧅⧆⧇⧈⧉⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟⧠⧡⧢⧣⧤⧥⧦⧧⧨⧩⧪⧫⧬⧭⧮⧯⧰⧱⧲⧳⧴⧵⧶⧷⧸⧹⧺⧻⧼⧽⧾⧿⨀⨁⨂⨃⨄⨅⨆⨇⨈⨉⨊⨋⨌⨍⨎⨏⨐⨑⨒⨓⨔⨕⨖⨗⨘⨙⨚⨛⨜⨝⨞⨟⨠⨡⨢⨣⨤⨥⨦⨧⨨⨩⨪⨫⨬⨭⨮⨯⨰⨱⨲⨳⨴⨵⨶⨷⨸⨹⨺⨻⨼⨽⨾⨿⩀⩁⩂⩃⩄⩅⩆⩇⩈⩉⩊⩋⩌⩍⩎⩏⩐⩑⩒⩓⩔⩕⩖⩗⩘⩙⩚⩛⩜⩝⩞⩟⩠⩡⩢⩣⩤⩥⩦⩧⩨⩩⩪⩫⩬⩭⩮⩯⩰⩱⩲⩳⩴⩵⩶⩷⩸⩹⩺⩻⩼⩽⩾⩿⪀⪁⪂⪃⪄⪅⪆⪇⪈⪉⪊⪋⪌⪍⪎⪏⪐⪑⪒⪓⪔⪕⪖⪗⪘⪙⪚⪛⪜⪝⪞⪟⪠⪡⪢⪣⪤⪥⪦⪧⪨⪩⪪⪫⪬⪭⪮⪯⪰⪱⪲⪳⪴⪵⪶⪷⪸⪹⪺⪻⪼⪽⪾⪿⫀⫁⫂⫃⫄⫅⫆⫇⫈⫉⫊⫋⫌⫍⫎⫏⫐⫑⫒⫓⫔⫕⫖⫗⫘⫙⫚⫛⫝̸⫝⫞⫟⫠⫡⫢⫣⫤⫥⫦⫧⫨⫩⫪⫫⫬⫭⫮⫯⫰⫱⫲⫳⫴⫵⫶⫷⫸⫹⫺⫻⫼⫽⫾⫿⬀⬁⬂⬃⬄⬅⬆⬇⬈⬉⬊⬋⬌⬍⬎⬏⬐⬑⬒⬓⬔⬕⬖⬗⬘⬙⬚⬛⬜⬝⬞⬟⬠⬡⬢⬣⬤⬥⬦⬧⬨⬩⬪⬫⬬⬭⬮⬯⬰⬱⬲⬳⬴⬵⬶⬷⬸⬹⬺⬻⬼⬽⬾⬿⭀⭁⭂⭃⭄⭅⭆⭇⭈⭉⭊⭋⭌⭍⭎⭏⭐⭑⭒⭓⭔⭕⭖⭗⭘⭙⭚⭛⭜⭝⭞⭟⭠⭡⭢⭣⭤⭥⭦⭧⭨⭩⭪⭫⭬⭭⭮⭯⭰⭱⭲⭳⭶⭷⭸⭹⭺⭻⭼⭽⭾⭿⮀⮁⮂⮃⮄⮅⮆⮇⮈⮉⮊⮋⮌⮍⮎⮏⮐⮑⮒⮓⮔⮕⮗⮘⮙⮚⮛⮜⮝⮞⮟⮠⮡⮢⮣⮤⮥⮦⮧⮨⮩⮪⮫⮬⮭⮮⮯⮰⮱⮲⮳⮴⮵⮶⮷⮸⮹⮺⮻⮼⮽⮾⮿⯀⯁⯂⯃⯄⯅⯆⯇⯈⯉⯊⯋⯌⯍⯎⯏⯐⯑⯒⯓⯔⯕⯖⯗⯘⯙⯚⯛⯜⯝⯞⯟⯠⯡⯢⯣⯤⯥⯦⯧⯨⯩⯪⯫⯬⯭⯮⯯⯰⯱⯲⯳⯴⯵⯶⯷⯸⯹⯺⯻⯼⯽⯾⯿⳥⳦⳧⳨⳩⳪⳹⳺⳻⳼⳾⳿⵰⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸓⸔⸕⸖⸗⸘⸙⸚⸛⸜⸝⸞⸟⸠⸡⸢⸣⸤⸥⸦⸧⸨⸩⸪⸫⸬⸭⸮⸰⸱⸲⸳⸴⸵⸶⸷⸸⸹⸺⸻⸼⸽⸾⸿⹀⹁⹂⹃⹄⹅⹆⹇⹈⹉⹊⹋⹌⹍⹎⹏⹐⹑⹒⹓⹔⹕⹖⹗⹘⹙⹚⹛⹜⹝⺀⺁⺂⺃⺄⺅⺆⺇⺈⺉⺊⺋⺌⺍⺎⺏⺐⺑⺒⺓⺔⺕⺖⺗⺘⺙⺛⺜⺝⺞⺟⺠⺡⺢⺣⺤⺥⺦⺧⺨⺩⺪⺫⺬⺭⺮⺯⺰⺱⺲⺳⺴⺵⺶⺷⺸⺹⺺⺻⺼⺽⺾⺿⻀⻁⻂⻃⻄⻅⻆⻇⻈⻉⻊⻋⻌⻍⻎⻏⻐⻑⻒⻓⻔⻕⻖⻗⻘⻙⻚⻛⻜⻝⻞⻟⻠⻡⻢⻣⻤⻥⻦⻧⻨⻩⻪⻫⻬⻭⻮⻯⻰⻱⻲⻳⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻⿼⿽⿾⿿、。〃〄〈〉《》「」『』【】〒〓〔〕〖〗〘〙〚〛〜〝〞〟〠〰〶〷〽〾〿゛゜゠・㆐㆑㆖㆗㆘㆙㆚㆛㆜㆝㆞㆟㇀㇁㇂㇃㇄㇅㇆㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇑㇒㇓㇔㇕㇖㇗㇘㇙㇚㇛㇜㇝㇞㇟㇠㇡㇢㇣㇯㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛㈜㈝㈞㈪㈫㈬㈭㈮㈯㈰㈱㈲㈳㈴㈵㈶㈷㈸㈹㈺㈻㈼㈽㈾㈿㉀㉁㉂㉃㉄㉅㉆㉇㉐㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㉼㉽㉾㉿㊊㊋㊌㊍㊎㊏㊐㊑㊒㊓㊔㊕㊖㊗㊘㊙㊚㊛㊜㊝㊞㊟㊠㊡㊢㊣㊤㊥㊦㊧㊨㊩㊪㊫㊬㊭㊮㊯㊰㋀㋁㋂㋃㋄㋅㋆㋇㋈㋉㋊㋋㋌㋍㋎㋏㋐㋑㋒㋓㋔㋕㋖㋗㋘㋙㋚㋛㋜㋝㋞㋟㋠㋡㋢㋣㋤㋥㋦㋧㋨㋩㋪㋫㋬㋭㋮㋯㋰㋱㋲㋳㋴㋵㋶㋷㋸㋹㋺㋻㋼㋽㋾㋿㌀㌁㌂㌃㌄㌅㌆㌇㌈㌉㌊㌋㌌㌍㌎㌏㌐㌑㌒㌓㌔㌕㌖㌗㌘㌙㌚㌛㌜㌝㌞㌟㌠㌡㌢㌣㌤㌥㌦㌧㌨㌩㌪㌫㌬㌭㌮㌯㌰㌱㌲㌳㌴㌵㌶㌷㌸㌹㌺㌻㌼㌽㌾㌿㍀㍁㍂㍃㍄㍅㍆㍇㍈㍉㍊㍋㍌㍍㍎㍏㍐㍑㍒㍓㍔㍕㍖㍗㍘㍙㍚㍛㍜㍝㍞㍟㍠㍡㍢㍣㍤㍥㍦㍧㍨㍩㍪㍫㍬㍭㍮㍯㍰㍱㍲㍳㍴㍵㍶㍷㍸㍹㍺㍻㍼㍽㍾㍿㎀㎁㎂㎃㎄㎅㎆㎇㎈㎉㎊㎋㎌㎍㎎㎏㎐㎑㎒㎓㎔㎕㎖㎗㎘㎙㎚㎛㎜㎝㎞㎟㎠㎡㎢㎣㎤㎥㎦㎧㎨㎩㎪㎫㎬㎭㎮㎯㎰㎱㎲㎳㎴㎵㎶㎷㎸㎹㎺㎻㎼㎽㎾㎿㏀㏁㏂㏃㏄㏅㏆㏇㏈㏉㏊㏋㏌㏍㏎㏏㏐㏑㏒㏓㏔㏕㏖㏗㏘㏙㏚㏛㏜㏝㏞㏟㏠㏡㏢㏣㏤㏥㏦㏧㏨㏩㏪㏫㏬㏭㏮㏯㏰㏱㏲㏳㏴㏵㏶㏷㏸㏹㏺㏻㏼㏽㏾㏿䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿꒐꒑꒒꒓꒔꒕꒖꒗꒘꒙꒚꒛꒜꒝꒞꒟꒠꒡꒢꒣꒤꒥꒦꒧꒨꒩꒪꒫꒬꒭꒮꒯꒰꒱꒲꒳꒴꒵꒶꒷꒸꒹꒺꒻꒼꒽꒾꒿꓀꓁꓂꓃꓄꓅꓆꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꜀꜁꜂꜃꜄꜅꜆꜇꜈꜉꜊꜋꜌꜍꜎꜏꜐꜑꜒꜓꜔꜕꜖꜠꜡꞉꞊꠨꠩꠪꠫꠶꠷꠹꡴꡵꡶꡷꣎꣏꣸꣹꣺꣼꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꩷꩸꩹꫞꫟꫰꫱꭛꭪꭫꯫﬩﮲﮳﮴﮵﮶﮷﮸﮹﮺﮻﮼﮽﮾﮿﯀﯁﯂﴾﴿﵀﵁﵂﵃﵄﵅﵆﵇﵈﵉﵊﵋﵌﵍﵎﵏﷏﷽﷾﷿︐︑︒︓︔︕︖︗︘︙︰︱︲︳︴︵︶︷︸︹︺︻︼︽︾︿﹀﹁﹂﹃﹄﹅﹆﹇﹈﹉﹊﹋﹌﹍﹎﹏﹐﹑﹒﹔﹕﹖﹗﹘﹙﹚﹛﹜﹝﹞﹟﹠﹡﹢﹣﹤﹥﹦﹨﹪﹫！＂＃％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～｟｠｡｢｣､･￢￣￤￨￩￪￫￬￭￮￼�𐄀𐄁𐄂𐄷𐄸𐄹𐄺𐄻𐄼𐄽𐄾𐄿𐅹𐅺𐅻𐅼𐅽𐅾𐅿𐆀𐆁𐆂𐆃𐆄𐆅𐆆𐆇𐆈𐆉𐆌𐆍𐆎𐆐𐆑𐆒𐆓𐆔𐆕𐆖𐆗𐆘𐆙𐆚𐆛𐆜𐆠𐇐𐇑𐇒𐇓𐇔𐇕𐇖𐇗𐇘𐇙𐇚𐇛𐇜𐇝𐇞𐇟𐇠𐇡𐇢𐇣𐇤𐇥𐇦𐇧𐇨𐇩𐇪𐇫𐇬𐇭𐇮𐇯𐇰𐇱𐇲𐇳𐇴𐇵𐇶𐇷𐇸𐇹𐇺𐇻𐇼𐎟𐏐𐕯𐡗𐡷𐡸𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕𐩖𐩗𐩘𐩿𐫈𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐬹𐬺𐬻𐬼𐬽𐬾𐬿𐮙𐮚𐮛𐮜𐺭𐽕𐽖𐽗𐽘𐽙𐾆𐾇𐾈𐾉𑁇𑁈𑁉𑁊𑁋𑁌𑁍𑂻𑂼𑂾𑂿𑃀𑃁𑅀𑅁𑅂𑅃𑅴𑅵𑇅𑇆𑇇𑇈𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑚𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑚹𑜼𑜽𑜾𑜿𑠻𑥄𑥅𑥆𑧢𑨿𑩀𑩁𑩂𑩃𑩄𑩅𑩆𑪚𑪛𑪜𑪞𑪟𑪠𑪡𑪢𑬀𑬁𑬂𑬃𑬄𑬅𑬆𑬇𑬈𑬉𑱁𑱂𑱃𑱄𑱅𑱰𑱱𑻷𑻸𑽃𑽄𑽅𑽆𑽇𑽈𑽉𑽊𑽋𑽌𑽍𑽎𑽏𑿕𑿖𑿗𑿘𑿙𑿚𑿛𑿜𑿡𑿢𑿣𑿤𑿥𑿦𑿧𑿨𑿩𑿪𑿫𑿬𑿭𑿮𑿯𑿰𑿱𑿿𒑰𒑱𒑲𒑳𒑴𒿱𒿲𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖬼𖬽𖬾𖬿𖭄𖭅𖺗𖺘𖺙𖺚𖿢𛲜𛲟𜽐𜽑𜽒𜽓𜽔𜽕𜽖𜽗𜽘𜽙𜽚𜽛𜽜𜽝𜽞𜽟𜽠𜽡𜽢𜽣𜽤𜽥𜽦𜽧𜽨𜽩𜽪𜽫𜽬𜽭𜽮𜽯𜽰𜽱𜽲𜽳𜽴𜽵𜽶𜽷𜽸𜽹𜽺𜽻𜽼𜽽𜽾𜽿𜾀𜾁𜾂𜾃𜾄𜾅𜾆𜾇𜾈𜾉𜾊𜾋𜾌𜾍𜾎𜾏𜾐𜾑𜾒𜾓𜾔𜾕𜾖𜾗𜾘𜾙𜾚𜾛𜾜𜾝𜾞𜾟𜾠𜾡𜾢𜾣𜾤𜾥𜾦𜾧𜾨𜾩𜾪𜾫𜾬𜾭𜾮𜾯𜾰𜾱𜾲𜾳𜾴𜾵𜾶𜾷𜾸𜾹𜾺𜾻𜾼𜾽𜾾𜾿𜿀𜿁𜿂𜿃𝀀𝀁𝀂𝀃𝀄𝀅𝀆𝀇𝀈𝀉𝀊𝀋𝀌𝀍𝀎𝀏𝀐𝀑𝀒𝀓𝀔𝀕𝀖𝀗𝀘𝀙𝀚𝀛𝀜𝀝𝀞𝀟𝀠𝀡𝀢𝀣𝀤𝀥𝀦𝀧𝀨𝀩𝀪𝀫𝀬𝀭𝀮𝀯𝀰𝀱𝀲𝀳𝀴𝀵𝀶𝀷𝀸𝀹𝀺𝀻𝀼𝀽𝀾𝀿𝁀𝁁𝁂𝁃𝁄𝁅𝁆𝁇𝁈𝁉𝁊𝁋𝁌𝁍𝁎𝁏𝁐𝁑𝁒𝁓𝁔𝁕𝁖𝁗𝁘𝁙𝁚𝁛𝁜𝁝𝁞𝁟𝁠𝁡𝁢𝁣𝁤𝁥𝁦𝁧𝁨𝁩𝁪𝁫𝁬𝁭𝁮𝁯𝁰𝁱𝁲𝁳𝁴𝁵𝁶𝁷𝁸𝁹𝁺𝁻𝁼𝁽𝁾𝁿𝂀𝂁𝂂𝂃𝂄𝂅𝂆𝂇𝂈𝂉𝂊𝂋𝂌𝂍𝂎𝂏𝂐𝂑𝂒𝂓𝂔𝂕𝂖𝂗𝂘𝂙𝂚𝂛𝂜𝂝𝂞𝂟𝂠𝂡𝂢𝂣𝂤𝂥𝂦𝂧𝂨𝂩𝂪𝂫𝂬𝂭𝂮𝂯𝂰𝂱𝂲𝂳𝂴𝂵𝂶𝂷𝂸𝂹𝂺𝂻𝂼𝂽𝂾𝂿𝃀𝃁𝃂𝃃𝃄𝃅𝃆𝃇𝃈𝃉𝃊𝃋𝃌𝃍𝃎𝃏𝃐𝃑𝃒𝃓𝃔𝃕𝃖𝃗𝃘𝃙𝃚𝃛𝃜𝃝𝃞𝃟𝃠𝃡𝃢𝃣𝃤𝃥𝃦𝃧𝃨𝃩𝃪𝃫𝃬𝃭𝃮𝃯𝃰𝃱𝃲𝃳𝃴𝃵𝄀𝄁𝄂𝄃𝄄𝄅𝄆𝄇𝄈𝄉𝄊𝄋𝄌𝄍𝄎𝄏𝄐𝄑𝄒𝄓𝄔𝄕𝄖𝄗𝄘𝄙𝄚𝄛𝄜𝄝𝄞𝄟𝄠𝄡𝄢𝄣𝄤𝄥𝄦𝄩𝄪𝄫𝄬𝄭𝄮𝄯𝄰𝄱𝄲𝄳𝄴𝄵𝄶𝄷𝄸𝄹𝄺𝄻𝄼𝄽𝄾𝄿𝅀𝅁𝅂𝅃𝅄𝅅𝅆𝅇𝅈𝅉𝅊𝅋𝅌𝅍𝅎𝅏𝅐𝅑𝅒𝅓𝅔𝅕𝅖𝅗𝅘𝅙𝅚𝅛𝅜𝅝𝅗𝅥𝅘𝅥𝅘𝅥𝅮𝅘𝅥𝅯𝅘𝅥𝅰𝅘𝅥𝅱𝅘𝅥𝅲𝅪𝅫𝅬𝆃𝆄𝆌𝆍𝆎𝆏𝆐𝆑𝆒𝆓𝆔𝆕𝆖𝆗𝆘𝆙𝆚𝆛𝆜𝆝𝆞𝆟𝆠𝆡𝆢𝆣𝆤𝆥𝆦𝆧𝆨𝆩𝆮𝆯𝆰𝆱𝆲𝆳𝆴𝆵𝆶𝆷𝆸𝆹𝆺𝆹𝅥𝆺𝅥𝆹𝅥𝅮𝆺𝅥𝅮𝆹𝅥𝅯𝆺𝅥𝅯𝇁𝇂𝇃𝇄𝇅𝇆𝇇𝇈𝇉𝇊𝇋𝇌𝇍𝇎𝇏𝇐𝇑𝇒𝇓𝇔𝇕𝇖𝇗𝇘𝇙𝇚𝇛𝇜𝇝𝇞𝇟𝇠𝇡𝇢𝇣𝇤𝇥𝇦𝇧𝇨𝇩𝇪𝈀𝈁𝈂𝈃𝈄𝈅𝈆𝈇𝈈𝈉𝈊𝈋𝈌𝈍𝈎𝈏𝈐𝈑𝈒𝈓𝈔𝈕𝈖𝈗𝈘𝈙𝈚𝈛𝈜𝈝𝈞𝈟𝈠𝈡𝈢𝈣𝈤𝈥𝈦𝈧𝈨𝈩𝈪𝈫𝈬𝈭𝈮𝈯𝈰𝈱𝈲𝈳𝈴𝈵𝈶𝈷𝈸𝈹𝈺𝈻𝈼𝈽𝈾𝈿𝉀𝉁𝉅𝌀𝌁𝌂𝌃𝌄𝌅𝌆𝌇𝌈𝌉𝌊𝌋𝌌𝌍𝌎𝌏𝌐𝌑𝌒𝌓𝌔𝌕𝌖𝌗𝌘𝌙𝌚𝌛𝌜𝌝𝌞𝌟𝌠𝌡𝌢𝌣𝌤𝌥𝌦𝌧𝌨𝌩𝌪𝌫𝌬𝌭𝌮𝌯𝌰𝌱𝌲𝌳𝌴𝌵𝌶𝌷𝌸𝌹𝌺𝌻𝌼𝌽𝌾𝌿𝍀𝍁𝍂𝍃𝍄𝍅𝍆𝍇𝍈𝍉𝍊𝍋𝍌𝍍𝍎𝍏𝍐𝍑𝍒𝍓𝍔𝍕𝍖𝛁𝛛𝛻𝜕𝜵𝝏𝝯𝞉𝞩𝟃𝠀𝠁𝠂𝠃𝠄𝠅𝠆𝠇𝠈𝠉𝠊𝠋𝠌𝠍𝠎𝠏𝠐𝠑𝠒𝠓𝠔𝠕𝠖𝠗𝠘𝠙𝠚𝠛𝠜𝠝𝠞𝠟𝠠𝠡𝠢𝠣𝠤𝠥𝠦𝠧𝠨𝠩𝠪𝠫𝠬𝠭𝠮𝠯𝠰𝠱𝠲𝠳𝠴𝠵𝠶𝠷𝠸𝠹𝠺𝠻𝠼𝠽𝠾𝠿𝡀𝡁𝡂𝡃𝡄𝡅𝡆𝡇𝡈𝡉𝡊𝡋𝡌𝡍𝡎𝡏𝡐𝡑𝡒𝡓𝡔𝡕𝡖𝡗𝡘𝡙𝡚𝡛𝡜𝡝𝡞𝡟𝡠𝡡𝡢𝡣𝡤𝡥𝡦𝡧𝡨𝡩𝡪𝡫𝡬𝡭𝡮𝡯𝡰𝡱𝡲𝡳𝡴𝡵𝡶𝡷𝡸𝡹𝡺𝡻𝡼𝡽𝡾𝡿𝢀𝢁𝢂𝢃𝢄𝢅𝢆𝢇𝢈𝢉𝢊𝢋𝢌𝢍𝢎𝢏𝢐𝢑𝢒𝢓𝢔𝢕𝢖𝢗𝢘𝢙𝢚𝢛𝢜𝢝𝢞𝢟𝢠𝢡𝢢𝢣𝢤𝢥𝢦𝢧𝢨𝢩𝢪𝢫𝢬𝢭𝢮𝢯𝢰𝢱𝢲𝢳𝢴𝢵𝢶𝢷𝢸𝢹𝢺𝢻𝢼𝢽𝢾𝢿𝣀𝣁𝣂𝣃𝣄𝣅𝣆𝣇𝣈𝣉𝣊𝣋𝣌𝣍𝣎𝣏𝣐𝣑𝣒𝣓𝣔𝣕𝣖𝣗𝣘𝣙𝣚𝣛𝣜𝣝𝣞𝣟𝣠𝣡𝣢𝣣𝣤𝣥𝣦𝣧𝣨𝣩𝣪𝣫𝣬𝣭𝣮𝣯𝣰𝣱𝣲𝣳𝣴𝣵𝣶𝣷𝣸𝣹𝣺𝣻𝣼𝣽𝣾𝣿𝤀𝤁𝤂𝤃𝤄𝤅𝤆𝤇𝤈𝤉𝤊𝤋𝤌𝤍𝤎𝤏𝤐𝤑𝤒𝤓𝤔𝤕𝤖𝤗𝤘𝤙𝤚𝤛𝤜𝤝𝤞𝤟𝤠𝤡𝤢𝤣𝤤𝤥𝤦𝤧𝤨𝤩𝤪𝤫𝤬𝤭𝤮𝤯𝤰𝤱𝤲𝤳𝤴𝤵𝤶𝤷𝤸𝤹𝤺𝤻𝤼𝤽𝤾𝤿𝥀𝥁𝥂𝥃𝥄𝥅𝥆𝥇𝥈𝥉𝥊𝥋𝥌𝥍𝥎𝥏𝥐𝥑𝥒𝥓𝥔𝥕𝥖𝥗𝥘𝥙𝥚𝥛𝥜𝥝𝥞𝥟𝥠𝥡𝥢𝥣𝥤𝥥𝥦𝥧𝥨𝥩𝥪𝥫𝥬𝥭𝥮𝥯𝥰𝥱𝥲𝥳𝥴𝥵𝥶𝥷𝥸𝥹𝥺𝥻𝥼𝥽𝥾𝥿𝦀𝦁𝦂𝦃𝦄𝦅𝦆𝦇𝦈𝦉𝦊𝦋𝦌𝦍𝦎𝦏𝦐𝦑𝦒𝦓𝦔𝦕𝦖𝦗𝦘𝦙𝦚𝦛𝦜𝦝𝦞𝦟𝦠𝦡𝦢𝦣𝦤𝦥𝦦𝦧𝦨𝦩𝦪𝦫𝦬𝦭𝦮𝦯𝦰𝦱𝦲𝦳𝦴𝦵𝦶𝦷𝦸𝦹𝦺𝦻𝦼𝦽𝦾𝦿𝧀𝧁𝧂𝧃𝧄𝧅𝧆𝧇𝧈𝧉𝧊𝧋𝧌𝧍𝧎𝧏𝧐𝧑𝧒𝧓𝧔𝧕𝧖𝧗𝧘𝧙𝧚𝧛𝧜𝧝𝧞𝧟𝧠𝧡𝧢𝧣𝧤𝧥𝧦𝧧𝧨𝧩𝧪𝧫𝧬𝧭𝧮𝧯𝧰𝧱𝧲𝧳𝧴𝧵𝧶𝧷𝧸𝧹𝧺𝧻𝧼𝧽𝧾𝧿𝨷𝨸𝨹𝨺𝩭𝩮𝩯𝩰𝩱𝩲𝩳𝩴𝩶𝩷𝩸𝩹𝩺𝩻𝩼𝩽𝩾𝩿𝪀𝪁𝪂𝪃𝪅𝪆𝪇𝪈𝪉𝪊𝪋𞅏𞥞𞥟𞲬𞴮𞻰𞻱🀀🀁🀂🀃🀄🀅🀆🀇🀈🀉🀊🀋🀌🀍🀎🀏🀐🀑🀒🀓🀔🀕🀖🀗🀘🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣🀤🀥🀦🀧🀨🀩🀪🀫🀰🀱🀲🀳🀴🀵🀶🀷🀸🀹🀺🀻🀼🀽🀾🀿🁀🁁🁂🁃🁄🁅🁆🁇🁈🁉🁊🁋🁌🁍🁎🁏🁐🁑🁒🁓🁔🁕🁖🁗🁘🁙🁚🁛🁜🁝🁞🁟🁠🁡🁢🁣🁤🁥🁦🁧🁨🁩🁪🁫🁬🁭🁮🁯🁰🁱🁲🁳🁴🁵🁶🁷🁸🁹🁺🁻🁼🁽🁾🁿🂀🂁🂂🂃🂄🂅🂆🂇🂈🂉🂊🂋🂌🂍🂎🂏🂐🂑🂒🂓🂠🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂬🂭🂮🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂼🂽🂾🂿🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃌🃍🃎🃏🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃜🃝🃞🃟🃠🃡🃢🃣🃤🃥🃦🃧🃨🃩🃪🃫🃬🃭🃮🃯🃰🃱🃲🃳🃴🃵🄍🄎🄏🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩🄪🄫🄬🄭🄮🄯🅊🅋🅌🅍🅎🅏🅪🅫🅬🅭🅮🅯🆊🆋🆌🆍🆎🆏🆐🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🆛🆜🆝🆞🆟🆠🆡🆢🆣🆤🆥🆦🆧🆨🆩🆪🆫🆬🆭🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🈀🈁🈂🈐🈑🈒🈓🈔🈕🈖🈗🈘🈙🈚🈛🈜🈝🈞🈟🈠🈡🈢🈣🈤🈥🈦🈧🈨🈩🈪🈫🈬🈭🈮🈯🈰🈱🈲🈳🈴🈵🈶🈷🈸🈹🈺🈻🉀🉁🉂🉃🉄🉅🉆🉇🉈🉐🉑🉠🉡🉢🉣🉤🉥🌀🌁🌂🌃🌄🌅🌆🌇🌈🌉🌊🌋🌌🌍🌎🌏🌐🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜🌝🌞🌟🌠🌡🌢🌣🌤🌥🌦🌧🌨🌩🌪🌫🌬🌭🌮🌯🌰🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🍽🍾🍿🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎔🎕🎖🎗🎘🎙🎚🎛🎜🎝🎞🎟🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄🏅🏆🏇🏈🏉🏊🏋🏌🏍🏎🏏🏐🏑🏒🏓🏔🏕🏖🏗🏘🏙🏚🏛🏜🏝🏞🏟🏠🏡🏢🏣🏤🏥🏦🏧🏨🏩🏪🏫🏬🏭🏮🏯🏰🏱🏲🏳🏴🏵🏶🏷🏸🏹🏺🏻🏼🏽🏾🏿🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾🐿👀👁👂👃👄👅👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄💅💆💇💈💉💊💋💌💍💎💏💐💑💒💓💔💕💖💗💘💙💚💛💜💝💞💟💠💡💢💣💤💥💦💧💨💩💪💫💬💭💮💯💰💱💲💳💴💵💶💷💸💹💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈📉📊📋📌📍📎📏📐📑📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧📨📩📪📫📬📭📮📯📰📱📲📳📴📵📶📷📸📹📺📻📼📽📾📿🔀🔁🔂🔃🔄🔅🔆🔇🔈🔉🔊🔋🔌🔍🔎🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔙🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮🔯🔰🔱🔲🔳🔴🔵🔶🔷🔸🔹🔺🔻🔼🔽🔾🔿🕀🕁🕂🕃🕄🕅🕆🕇🕈🕉🕊🕋🕌🕍🕎🕏🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧🕨🕩🕪🕫🕬🕭🕮🕯🕰🕱🕲🕳🕴🕵🕶🕷🕸🕹🕺🕻🕼🕽🕾🕿🖀🖁🖂🖃🖄🖅🖆🖇🖈🖉🖊🖋🖌🖍🖎🖏🖐🖑🖒🖓🖔🖕🖖🖗🖘🖙🖚🖛🖜🖝🖞🖟🖠🖡🖢🖣🖤🖥🖦🖧🖨🖩🖪🖫🖬🖭🖮🖯🖰🖱🖲🖳🖴🖵🖶🖷🖸🖹🖺🖻🖼🖽🖾🖿🗀🗁🗂🗃🗄🗅🗆🗇🗈🗉🗊🗋🗌🗍🗎🗏🗐🗑🗒🗓🗔🗕🗖🗗🗘🗙🗚🗛🗜🗝🗞🗟🗠🗡🗢🗣🗤🗥🗦🗧🗨🗩🗪🗫🗬🗭🗮🗯🗰🗱🗲🗳🗴🗵🗶🗷🗸🗹🗺🗻🗼🗽🗾🗿😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧😨😩😪😫😬😭😮😯😰😱😲😳😴😵😶😷😸😹😺😻😼😽😾😿🙀🙁🙂🙃🙄🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏🙐🙑🙒🙓🙔🙕🙖🙗🙘🙙🙚🙛🙜🙝🙞🙟🙠🙡🙢🙣🙤🙥🙦🙧🙨🙩🙪🙫🙬🙭🙮🙯🙰🙱🙲🙳🙴🙵🙶🙷🙸🙹🙺🙻🙼🙽🙾🙿🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤🚥🚦🚧🚨🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚵🚶🚷🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛅🛆🛇🛈🛉🛊🛋🛌🛍🛎🛏🛐🛑🛒🛓🛔🛕🛖🛗🛜🛝🛞🛟🛠🛡🛢🛣🛤🛥🛦🛧🛨🛩🛪🛫🛬🛰🛱🛲🛳🛴🛵🛶🛷🛸🛹🛺🛻🛼🜀🜁🜂🜃🜄🜅🜆🜇🜈🜉🜊🜋🜌🜍🜎🜏🜐🜑🜒🜓🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭🜮🜯🜰🜱🜲🜳🜴🜵🜶🜷🜸🜹🜺🜻🜼🜽🜾🜿🝀🝁🝂🝃🝄🝅🝆🝇🝈🝉🝊🝋🝌🝍🝎🝏🝐🝑🝒🝓🝔🝕🝖🝗🝘🝙🝚🝛🝜🝝🝞🝟🝠🝡🝢🝣🝤🝥🝦🝧🝨🝩🝪🝫🝬🝭🝮🝯🝰🝱🝲🝳🝴🝵🝶🝻🝼🝽🝾🝿🞀🞁🞂🞃🞄🞅🞆🞇🞈🞉🞊🞋🞌🞍🞎🞏🞐🞑🞒🞓🞔🞕🞖🞗🞘🞙🞚🞛🞜🞝🞞🞟🞠🞡🞢🞣🞤🞥🞦🞧🞨🞩🞪🞫🞬🞭🞮🞯🞰🞱🞲🞳🞴🞵🞶🞷🞸🞹🞺🞻🞼🞽🞾🞿🟀🟁🟂🟃🟄🟅🟆🟇🟈🟉🟊🟋🟌🟍🟎🟏🟐🟑🟒🟓🟔🟕🟖🟗🟘🟙🟠🟡🟢🟣🟤🟥🟦🟧🟨🟩🟪🟫🟰🠀🠁🠂🠃🠄🠅🠆🠇🠈🠉🠊🠋🠐🠑🠒🠓🠔🠕🠖🠗🠘🠙🠚🠛🠜🠝🠞🠟🠠🠡🠢🠣🠤🠥🠦🠧🠨🠩🠪🠫🠬🠭🠮🠯🠰🠱🠲🠳🠴🠵🠶🠷🠸🠹🠺🠻🠼🠽🠾🠿🡀🡁🡂🡃🡄🡅🡆🡇🡐🡑🡒🡓🡔🡕🡖🡗🡘🡙🡠🡡🡢🡣🡤🡥🡦🡧🡨🡩🡪🡫🡬🡭🡮🡯🡰🡱🡲🡳🡴🡵🡶🡷🡸🡹🡺🡻🡼🡽🡾🡿🢀🢁🢂🢃🢄🢅🢆🢇🢐🢑🢒🢓🢔🢕🢖🢗🢘🢙🢚🢛🢜🢝🢞🢟🢠🢡🢢🢣🢤🢥🢦🢧🢨🢩🢪🢫🢬🢭🢰🢱🤀🤁🤂🤃🤄🤅🤆🤇🤈🤉🤊🤋🤌🤍🤎🤏🤐🤑🤒🤓🤔🤕🤖🤗🤘🤙🤚🤛🤜🤝🤞🤟🤠🤡🤢🤣🤤🤥🤦🤧🤨🤩🤪🤫🤬🤭🤮🤯🤰🤱🤲🤳🤴🤵🤶🤷🤸🤹🤺🤻🤼🤽🤾🤿🥀🥁🥂🥃🥄🥅🥆🥇🥈🥉🥊🥋🥌🥍🥎🥏🥐🥑🥒🥓🥔🥕🥖🥗🥘🥙🥚🥛🥜🥝🥞🥟🥠🥡🥢🥣🥤🥥🥦🥧🥨🥩🥪🥫🥬🥭🥮🥯🥰🥱🥲🥳🥴🥵🥶🥷🥸🥹🥺🥻🥼🥽🥾🥿🦀🦁🦂🦃🦄🦅🦆🦇🦈🦉🦊🦋🦌🦍🦎🦏🦐🦑🦒🦓🦔🦕🦖🦗🦘🦙🦚🦛🦜🦝🦞🦟🦠🦡🦢🦣🦤🦥🦦🦧🦨🦩🦪🦫🦬🦭🦮🦯🦰🦱🦲🦳🦴🦵🦶🦷🦸🦹🦺🦻🦼🦽🦾🦿🧀🧁🧂🧃🧄🧅🧆🧇🧈🧉🧊🧋🧌🧍🧎🧏🧐🧑🧒🧓🧔🧕🧖🧗🧘🧙🧚🧛🧜🧝🧞🧟🧠🧡🧢🧣🧤🧥🧦🧧🧨🧩🧪🧫🧬🧭🧮🧯🧰🧱🧲🧳🧴🧵🧶🧷🧸🧹🧺🧻🧼🧽🧾🧿🨀🨁🨂🨃🨄🨅🨆🨇🨈🨉🨊🨋🨌🨍🨎🨏🨐🨑🨒🨓🨔🨕🨖🨗🨘🨙🨚🨛🨜🨝🨞🨟🨠🨡🨢🨣🨤🨥🨦🨧🨨🨩🨪🨫🨬🨭🨮🨯🨰🨱🨲🨳🨴🨵🨶🨷🨸🨹🨺🨻🨼🨽🨾🨿🩀🩁🩂🩃🩄🩅🩆🩇🩈🩉🩊🩋🩌🩍🩎🩏🩐🩑🩒🩓🩠🩡🩢🩣🩤🩥🩦🩧🩨🩩🩪🩫🩬🩭🩰🩱🩲🩳🩴🩵🩶🩷🩸🩹🩺🩻🩼🪀🪁🪂🪃🪄🪅🪆🪇🪈🪐🪑🪒🪓🪔🪕🪖🪗🪘🪙🪚🪛🪜🪝🪞🪟🪠🪡🪢🪣🪤🪥🪦🪧🪨🪩🪪🪫🪬🪭🪮🪯🪰🪱🪲🪳🪴🪵🪶🪷🪸🪹🪺🪻🪼🪽🪿🫀🫁🫂🫃🫄🫅🫎🫏🫐🫑🫒🫓🫔🫕🫖🫗🫘🫙🫚🫛🫠🫡🫢🫣🫤🫥🫦🫧🫨🫰🫱🫲🫳🫴🫵🫶🫷🫸🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻🬼🬽🬾🬿🭀🭁🭂🭃🭄🭅🭆🭇🭈🭉🭊🭋🭌🭍🭎🭏🭐🭑🭒🭓🭔🭕🭖🭗🭘🭙🭚🭛🭜🭝🭞🭟🭠🭡🭢🭣🭤🭥🭦🭧🭨🭩🭪🭫🭬🭭🭮🭯🭰🭱🭲🭳🭴🭵🭶🭷🭸🭹🭺🭻🭼🭽🭾🭿🮀🮁🮂🮃🮄🮅🮆🮇🮈🮉🮊🮋🮌🮍🮎🮏🮐🮑🮒🮔🮕🮖🮗🮘🮙🮚🮛🮜🮝🮞🮟🮠🮡🮢🮣🮤🮥🮦🮧🮨🮩🮪🮫🮬🮭🮮🮯🮰🮱🮲🮳🮴🮵🮶🮷🮸🮹🮺🮻🮼🮽🮾🮿🯀🯁🯂🯃🯄🯅🯆🯇🯈🯉🯊"""
# https://www.compart.com/en/unicode/category
# https://unicode.org/Public/UNIDATA/UnicodeData.txt

# `\p{posix_punct}` character class
POSIX_PUNCT = r"""-!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""
ALL_PUNCT_RANGES = "".join(find_unicode_ranges(POSIX_PUNCT + UNICODE_PUNCT))
SENTENCE_PUNCT = """.?!:;'"()[-]“”·…"""


LINKU = Path(__file__).resolve().parent / Path("linku.json")
SANDBOX = Path(__file__).resolve().parent / Path("sandbox.json")

VOWELS = "aeiou"
CONSONANTS = "jklmnpstw"
ALPHABET = VOWELS + CONSONANTS

LANGUAGE = "english"  # for NLTK

"""Commonly occurring strings which are some kind of valid Toki Pona or external token"""
ALLOWABLES = {
    "cw",  # Content Warning
    "x",  # ala
    "y",  # anu
    "kxk",  # ken ala ken
    "wxw",  # wile ala wile
}

with open(LINKU) as f:
    linku: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_PU: List[str] = [d["word"] for d in linku.values() if d["book"] == "pu"]
    NIMI_PU_ALE: List[str] = NIMI_PU + ["namako", "kin", "oko"]
    NIMI_LINKU: List[str] = [
        d["word"] for d in linku.values() if d["usage_category"] in ["core", "common"]
    ]
    NIMI_LINKU_ALE: List[str] = [d["word"] for d in linku.values()]

with open(SANDBOX) as f:
    sandbox: Dict[str, Dict[str, str]] = json.loads(f.read())
    NIMI_LINKU_SANDBOX: List[str] = [d["word"] for d in sandbox.values()]

del linku
del sandbox

__all__ = [
    "ALPHABET",
    "CONSONANTS",
    "NIMI_LINKU",
    "NIMI_LINKU_ALE",
    "NIMI_LINKU_SANDBOX",
    "NIMI_PU",
    "NIMI_PU_ALE",
    "VOWELS",
    "UNICODE_PUNCT",
    "ALLOWABLES",
    "POSIX_PUNCT",
]
