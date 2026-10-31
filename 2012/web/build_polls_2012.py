"""Build polls_2012.csv (national general-election trial heats, Obama vs. every Republican polled) and
polls_2012_gop_primary.csv (national Republican nomination polling) from Wikipedia.

General: 'Nationwide opinion polling for the 2012 United States presidential election'. The first wikitable is
post-convention Obama-Romney (phase "general"); the 1,000-row "Before Convention Nominations / Two-way race"
table has Obama against Romney, Gingrich, Santorum, Perry, Palin ... (phase "pre-convention"), with pollster and
dates spread across rows by rowspan. The 3/4/5-way tables are tiny and skipped.
"""
import re, datetime as dt
import pandas as pd, lxml.html as L
import fetch_util as f

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

def refs_map(doc):
    out = {}
    for li in doc.xpath('//li[starts-with(@id,"cite_note")]'):
        a = li.xpath('.//a[contains(@class,"external")]/@href')
        if a:
            out[li.get("id")] = a[0]
    return out

def clean(s):
    return re.sub(r"\[[^\]]*\]", "", str(s)).replace("\xa0", " ").strip()

def pct(s):
    m = re.search(r"(\d+(?:\.\d+)?)\s*%?", clean(s))
    return float(m.group(1)) if m and "%" in clean(s) else None

def grid(tab, refs):
    """Expand rowspan/colspan into a list of rows of (text, ref urls) cells."""
    out, carry = [], {}
    for tr in tab.xpath('.//tr'):
        row, col = [], 0
        cells = tr.xpath('./th|./td')
        while cells or col in carry:
            if col in carry:
                cell, n = carry[col]
                row.append(cell)
                carry[col] = (cell, n - 1) if n > 1 else None
                if carry[col] is None:
                    del carry[col]
                col += 1
                continue
            c = cells.pop(0)
            ids = [h.lstrip("#") for h in c.xpath('.//sup[contains(@class,"reference")]/a/@href')]
            cell = (clean(c.text_content()), [refs[i] for i in ids if i in refs])
            rs, cs = int(c.get("rowspan", 1) or 1), int(c.get("colspan", 1) or 1)
            for k in range(cs):
                row.append(cell)
                if rs > 1:
                    carry[col] = (cell, rs - 1)
                col += 1
        out.append(row)
    return out

def dates(s):
    """'October 22 – November 4, 2012' / 'June 25 – July 5, 2012' / 'Jan. 12–15, 2012' -> (start, end)."""
    s = s.replace("–", "-").replace("—", "-")
    years = [int(y) for y in re.findall(r"\b(20\d\d)\b", s)]
    s2 = re.sub(r",?\s*\b20\d\d\b", "", s)
    parts = [p.strip() for p in s2.split("-") if p.strip()]
    def md(p, default_m=None):
        m = re.match(r"([A-Za-z]+)\.?\s*(\d+)", p)
        if m:
            return MONTHS[m.group(1)[:3].lower()], int(m.group(2))
        return default_m, int(re.match(r"\d+", p).group())
    try:
        sm, sd = md(parts[0])
        em, ed = md(parts[-1], sm)
        ey = years[-1]
        sy = years[0] if len(years) > 1 else (ey - 1 if sm > em else ey)
        return dt.date(sy, sm, sd), dt.date(ey, em, ed)
    except Exception:
        return None, None

def sample(s):
    m = re.search(r"([\d,]+)\s*(LV|RV|A)\b", s)
    return (int(m.group(1).replace(",", "")), m.group(2)) if m else (None, None)

# ---------------- general election ----------------
TITLE = "Nationwide_opinion_polling_for_the_2012_United_States_presidential_election"
doc = L.fromstring(f.wiki_html(TITLE))
refs = refs_map(doc)
tabs = doc.xpath('//table[contains(@class,"wikitable")]')
rows = []

# post-convention: Poll source | Date | Obama | Romney | Lead | Sample | MoE
for r in grid(tabs[0], refs)[1:]:
    if len(r) < 7 or r[0][0].startswith("RCP"):
        continue
    st, en = dates(r[1][0])
    n, pop = sample(r[5][0])
    rows.append(dict(pollster=r[0][0], dates=r[1][0], start=st, end=en, dem="Barack Obama", dem_pct=pct(r[2][0]),
                     rep="Mitt Romney", rep_pct=pct(r[3][0]), lead=r[4][0], n=n, pop=pop, moe=r[6][0],
                     phase="general", ref_url=" ; ".join(dict.fromkeys(r[0][1] + r[1][1]))))

# pre-convention two-way: Poll source | Date | Dem | % | Rep | % | Lead | Sample | MoE
pre = [t for t in tabs if len(t.xpath('.//tr')) > 500][0]
for r in grid(pre, refs)[1:]:
    if len(r) < 9:
        continue
    st, en = dates(r[1][0])
    n, pop = sample(r[7][0])
    rows.append(dict(pollster=r[0][0], dates=r[1][0], start=st, end=en, dem=r[2][0], dem_pct=pct(r[3][0]),
                     rep=r[4][0], rep_pct=pct(r[5][0]), lead=r[6][0], n=n, pop=pop, moe=r[8][0],
                     phase="pre-convention", ref_url=" ; ".join(dict.fromkeys(r[0][1] + r[1][1]))))

gen = pd.DataFrame(rows)
gen["date"] = gen.end.fillna(gen.start)
gen["source"] = f.wiki_url(TITLE)
gen.to_csv("polls_2012.csv", index=False)
print("polls_2012.csv", gen.shape, "unparsed dates:", gen.date.isna().sum())
print(gen.groupby(["phase", "rep"]).size().sort_values(ascending=False).head(15).to_string())

# ---------------- Republican nomination ----------------
TITLE = "Nationwide_opinion_polling_for_the_2012_Republican_Party_presidential_primaries"
doc = L.fromstring(f.wiki_html(TITLE))
refs = refs_map(doc)
out = []
for t in doc.xpath('//table[contains(@class,"wikitable")]'):
    g = grid(t, refs)
    head = [c[0] for c in g[0]]
    if not head or head[0] != "Poll source" or "Mitt Romney" not in " ".join(head).replace("\n", " "):
        continue
    head = [re.sub(r"([a-z])([A-Z])", r"\1 \2", re.sub(r"\s+", " ", h)) for h in head]  # 'JonHuntsman'
    cands = [h for h in head[3:]]
    for r in g[1:]:
        if len(r) != len(head):
            continue
        st, en = dates(r[2][0])
        n, pop = sample(r[1][0])
        for c, cell in zip(cands, r[3:]):
            out.append(dict(pollster=r[0][0], dates=r[2][0], start=st, end=en, n=n, pop=pop,
                            candidate=c, pct=pct(cell[0]), raw=cell[0],
                            ref_url=" ; ".join(dict.fromkeys(r[0][1] + r[2][1]))))
nom = pd.DataFrame(out)
nom["date"] = nom.end.fillna(nom.start)
nom["source"] = f.wiki_url(TITLE)
nom.to_csv("polls_2012_gop_primary.csv", index=False)
print("polls_2012_gop_primary.csv", nom.shape, "unparsed dates:", nom.date.isna().sum(),
      nom.date.min(), nom.date.max())
print(nom[nom.candidate != "Others"].groupby("candidate").pct.agg(["count", "max"]).sort_values("count").to_string())
