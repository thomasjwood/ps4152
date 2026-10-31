"""Build polls_1992.csv (national general-election trial heats) and
polls_1992_primaries.csv (Democratic nomination polling) from Wikipedia.

Wikipedia has no separate "Nationwide opinion polling for the 1992 ..." page
(checked via the MediaWiki API, Oct 2026); the national polls live in the
"Polling" table of the main '1992 United States presidential election' article.
The Republican primaries article has no polling table.
"""
import io, re, datetime as dt
import pandas as pd, lxml.html as L
import fetch_util as f

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

def refs_map(doc):
    """cite_note id -> first external URL in that reference."""
    out = {}
    for li in doc.xpath('//li[starts-with(@id,"cite_note")]'):
        a = li.xpath('.//a[contains(@class,"external")]/@href')
        if a:
            out[li.get("id")] = a[0]
    return out

def row_refs(tr, refs):
    ids = [h.lstrip("#") for h in tr.xpath('.//sup[contains(@class,"reference")]/a/@href')]
    return " ; ".join(dict.fromkeys(refs[i] for i in ids if i in refs))

def clean(s):
    return re.sub(r"\[[^\]]*\]", "", str(s)).strip()

def pct(s):
    s = clean(s)
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", s)
    return float(m.group(1)) if m else None

def md(s):
    """'Oct. 31' -> (10, 31)"""
    m = re.match(r"([A-Za-z]+)\.?\s*(\d+)", s.strip())
    return MONTHS[m.group(1)[:3].lower()], int(m.group(2))

def table_after_heading(doc, heading_id):
    h = doc.xpath(f'//*[@id="{heading_id}"]')[0]
    return h.xpath('following::table[contains(@class,"wikitable")][1]')[0]

# ---------------- general election ----------------
TITLE = "1992_United_States_presidential_election"
html = f.wiki_html(TITLE)
doc = L.fromstring(html)
refs = refs_map(doc)
tab = [t for t in doc.xpath("//table") if not t.xpath(".//table")
       if "Poll source" in t.text_content() and "Perot" in t.text_content()][0]
rows, year, prev_month = [], 1992, 12
for tr in tab.xpath('.//tr')[1:]:
    tds = [clean(td.text_content()) for td in tr.xpath('./td|./th')]
    if len(tds) < 7 or tds[0].startswith("Election"):
        continue
    pollster, dates = tds[0], tds[1].replace("–", "-").replace("—", "-")
    parts = [p.strip() for p in dates.split("-") if p.strip()]
    sm, sd = md(parts[0])
    if len(parts) > 1:
        try:
            em, ed = md(parts[1])
        except Exception:
            em, ed = sm, int(re.match(r"\d+", parts[1]).group())
    else:
        em, ed = sm, sd
    # table is in reverse chronological order; a jump up in month means previous year
    if em > prev_month + 1:
        year -= 1
    prev_month = em
    syear = year - 1 if sm > em else year
    start, end = dt.date(syear, sm, sd), dt.date(year, em, ed)
    note = ""
    if end < start:
        note = f"Wikipedia gives field dates '{tds[1]}' (end before start); end set to NA. Gallup's approval poll in bush_approval.csv ran Jul 24-26, 1992, so the end is probably Jul 26"
        end = None
    clinton, bush, perot = pct(tds[2]), pct(tds[3]), pct(tds[4])
    rows.append(dict(
        pollster=pollster, dates=tds[1], start=start, end=end,
        Clinton=clinton, Bush=bush, Perot=perot, other=pct(tds[5]), undecided=pct(tds[6]),
        lead=tds[7], race="Clinton-Bush-Perot" if perot is not None else "Clinton-Bush",
        date=end or start, sample=None, note=note,
        ref_url=row_refs(tr, refs), source=f.wiki_url(TITLE) + "#Polling"))
gen = pd.DataFrame(rows)
gen.to_csv("polls_1992.csv", index=False)
print("polls_1992.csv", gen.shape)
print(gen[["pollster", "dates", "start", "end", "Clinton", "Bush", "Perot", "race"]].to_string())

# ---------------- Democratic nomination polls ----------------
TITLE = "1992_Democratic_Party_presidential_primaries"
html = f.wiki_html(TITLE)
doc = L.fromstring(html)
refs = refs_map(doc)
out = []
for t in doc.xpath('//table'):
    txt = t.text_content()
    if "Poll source" not in txt:
        continue
    df = pd.read_html(io.StringIO(L.tostring(t, encoding="unicode")))[0]
    trs = [tr for tr in t.xpath('.//tr') if tr.xpath('./td')]
    scope = "New Hampshire primary" if "Sample size" in df.columns else "National"
    for (_, r), tr in zip(df.iterrows(), trs):
        cands = [c for c in df.columns if c not in ("Poll source", "Publication", "Sample size", "MoE")]
        for c in cands:
            v = clean(r[c])
            out.append(dict(
                party="Democratic", scope=scope, pollster=clean(r["Poll source"]),
                published=clean(r["Publication"]),
                sample=clean(r.get("Sample size", "")) or None,
                candidate=c, pct=pct(v), raw=v,
                ref_url=row_refs(tr, refs), source=f.wiki_url(TITLE) + "#Polling"))
nom = pd.DataFrame(out)
# approximate date, as in lecture 13's polls_1980_dem_nomination.csv (mid-month for month-only dates)
def approx(p, scope):
    p = p.replace("–", "-")
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2}),\s*(\d{4})", p)
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{4})", p)
    if m:
        return dt.date(int(m.group(2)), MONTHS[m.group(1)[:3].lower()], 15)
    m = re.match(r"([A-Za-z]+)\.?\s+\d+\s*-\s*(\d+)", p)  # NH polls 'Feb. 12-14' (1992)
    if m:
        return dt.date(1992, MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
    return None
nom["date"] = [approx(p, s) for p, s in zip(nom.published, nom.scope)]
nom.to_csv("polls_1992_primaries.csv", index=False)
print("polls_1992_primaries.csv", nom.shape)
print(nom.pivot_table(index=["scope", "pollster", "published"], columns="candidate", values="pct").to_string())
