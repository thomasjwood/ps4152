"""Helper used to verify timeline_1992.md: fetch Wikipedia articles (cached in raw/)
and print sentences containing given keywords, so each dated claim can be checked."""
import re, sys, lxml.html as L
import fetch_util as f

def text(title):
    d = L.fromstring(f.wiki_html(title))
    for bad in d.xpath('//sup|//style|//table'):
        bad.drop_tree()
    return re.sub(r"\s+", " ", d.text_content())

def grep(title, *keys, width=220):
    t = text(title)
    for k in keys:
        hits = [m.start() for m in re.finditer(k, t)]
        for h in hits[:3]:
            print(f"[{title}] {k}: ...{t[max(0, h - width):h + width]}...")
        if not hits:
            print(f"[{title}] {k}: NOT FOUND")

if __name__ == "__main__":
    grep(sys.argv[1], *sys.argv[2:])
