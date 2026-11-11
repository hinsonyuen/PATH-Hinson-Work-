"""Print arms-related keyword hits in one Gazette file, with page (file line), offset, nearest port heading and context.
Usage: python3 find_hits.py Customs_Gazette_1894_Q2_No102.txt [context_after=200]
Lines starting H are port/section headings found on the page; K are keyword hits (nearby hits are merged)."""
import re, html, sys
f = sys.argv[1]; after = int(sys.argv[2]) if len(sys.argv) > 2 else 200
L = open('/mnt/project-files/' + f, encoding='utf-8', errors='replace').read().split('\n')
kw = re.compile(r"rifle|musket|carbine|re?volv|pisto?l|pis-|cannon|ordnance|cartr|ammun|munition|percus|gun ?powder|dynam|explos|detonat|torpedo|sword|bayonet|dagger|military|sal.{0,2}p.?e?tre|\bnitre|nitrate|chlorate|s.?u.?lph|brim.?.?tone|\bguns?\b|\barms\b|fire-? ?arms|bullet|pistol barrel|\bfuse", re.I)
skip = re.compile(r"gunpowder\W+(total|green|dust|tea)|(hyson|imperial|twankay)\W+gun ?powder|sulphate|sulphuric", re.I)
hdr = re.compile(r"(?:\d{1,2} ?[.\-—]+ ?)?\b(?:NEWCHWANG|TIENTSIN|CHEFOO|CHUNGKING|ICHANG|SHASI|YOCHOW|HANKOW|KIUKIANG|WUHU|NANKING|CHINKIANG|SHANGHAI|SOOCHOW|HANGCHOW|NINGPO|WENCHOW|SANTUAO|FOOCHOW|TAMSUI|TAKOW|TAINAN|AMOY|SWATOW|CANTON|KOWLOON|LAPPA|KONGMOON|SAMSHUI|WUCHOW|KIUNGCHOW|PAKHOI|LUNGCHOW|MENGTSZ|SZEMAO|TENGYUEH|KIAOCHOW|ANTUNG|DAIREN|HARBIN|CHANGSHA|NANNING)\b|(?:III?|IV|V|VI)\. ?-? ?(?:IMPORTS|EXPORTS|RE-EXPORTS)|FINES AND CONFISCATIONS")
for n, s in enumerate(L, 1):
    s = html.unescape(s); spans = []
    for m in kw.finditer(s):
        if skip.search(s[max(0, m.start()-30):m.end()+25]): continue
        a, b = max(0, m.start()-70), min(len(s), m.start()+after)
        if spans and a <= spans[-1][1]: spans[-1][1] = b
        else: spans.append([a, b])
    if not spans: continue
    hs = [(m.start(), m.group()) for m in hdr.finditer(s)]
    print(f"== line {n}: headings {[(p, h) for p, h in hs][:8]}")
    for a, b in spans: print(f"  K@{a}: {s[a:b]}")
