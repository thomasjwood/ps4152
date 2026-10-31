"""Scrape every national presidential general-election poll table on Wikipedia, 1948-2024, into tidy CSVs.

Sources, per cycle: the 'Nationwide opinion polling for the YYYY United States presidential election' page where
one exists (1968-1980, 2000, 2008-2024); otherwise the 'Polling' table of the 'YYYY United States presidential
election' article (1948-1964, 1984-1992). Wikipedia has no national poll table for 1996 or 2004; those cycles are
only in the monthly series from 'Opinion polling for United States presidential elections' (build_monthly.py).

Outputs (in this folder):
  polls_long.csv      one row per poll question x response (candidates, other, undecided)
  polls_nominees.csv  one row per poll question that includes both eventual major-party nominees
"""
import calendar, datetime as dt, re, sys
import pandas as pd, lxml.html as L
import fetch_util as f

sys.stdout.reconfigure(encoding="utf-8")

NOMINEES = {  # cycle: (Democratic nominee surname, Republican nominee surname)
    1948: ("Truman", "Dewey"), 1952: ("Stevenson", "Eisenhower"), 1956: ("Stevenson", "Eisenhower"),
    1960: ("Kennedy", "Nixon"), 1964: ("Johnson", "Goldwater"), 1968: ("Humphrey", "Nixon"),
    1972: ("McGovern", "Nixon"), 1976: ("Carter", "Ford"), 1980: ("Carter", "Reagan"), 1984: ("Mondale", "Reagan"),
    1988: ("Dukakis", "Bush"), 1992: ("Clinton", "Bush"), 2000: ("Gore", "Bush"), 2008: ("Obama", "McCain"),
    2012: ("Obama", "Romney"), 2016: ("Clinton", "Trump"), 2020: ("Biden", "Trump"), 2024: ("Harris", "Trump"),
}
BIDEN_OUT = dt.date(2024, 7, 21)  # Biden-Trump counts as the 2024 nominee matchup for polls ending before this

MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
MONTHS.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m})
MONTHS["sept"] = 9
MONTH_RE = r"(?:%s)" % "|".join(sorted(MONTHS, key=len, reverse=True))

PARTY_WORDS = [  # (pattern at the end of a header, party code)
    (r"\((?:D|Dem\.?)\)|Democratic|Democrat", "D"), (r"\((?:R|Rep\.?)\)|Republican", "R"),
    (r"\(L\)|Libertarian", "L"), (r"\(G\)|Green", "G"), (r"\((?:I|Ind\.?)\)|Independent", "I"),
    (r"\((?:Ref\.?|Reform)\)|Reform", "Reform"), (r"\(S\)|States' Rights|Dixiecrat", "SR"),
    (r"\(P\)|Progressive", "P"), (r"\((?:AI|A)\)|American Ind\w*\.?", "AI"), (r"No Labels", "No Labels"),
    (r"\(SR\)", "SR"), (r"Forward", "Forward"), (r"\(C\)|Constitution", "C"), (r"Socialist", "Soc"),
    (r"Peace", "Peace"),
]
NOT_VOTE = re.compile(r"distinction|quality|ideology|likelihood|favorab|approval|consider|primar|caucus", re.I)
AGGREGATORS = re.compile(r"\b(RCP|RealClear|FiveThirtyEight|538|270toWin|Decision Desk|Silver Bulletin|"
                         r"Race to the WH|The Hill|Average|aggregate)", re.I)
RESULT = re.compile(r"election result|presidential election$|^final result|^results?$", re.I)


def text(el):
    """Cell text with <br> as a line break, without footnote markers or inline CSS."""
    el = L.fromstring(L.tostring(el))
    for bad in el.xpath('.//style|.//sup[contains(@class,"reference")]|.//*[contains(@style,"display:none")]'):
        bad.drop_tree()
    for br in el.xpath(".//br"):
        br.tail = "\n" + (br.tail or "")
    s = el.text_content().replace("\xa0", " ").replace(" ", " ")
    s = re.sub(r"\[[^\]]*\]", "", s)
    return "\n".join(re.sub(r"\s+", " ", x).strip() for x in s.split("\n") if x.strip())


def refs_map(doc):
    out = {}
    for li in doc.xpath('//li[starts-with(@id,"cite_note")]'):
        a = li.xpath('.//a[contains(@class,"external")]/@href')
        if a:
            out[li.get("id")] = a[0]
    return out


def grid(tab):
    """Expand rowspan/colspan. Returns rows of (cell element, is_th); a spanned cell repeats."""
    rows, carry = [], {}
    for tr in tab.xpath("./tr|./tbody/tr|./thead/tr"):
        row, col, cells = [], 0, tr.xpath("./th|./td")
        while cells or col in carry:
            if col in carry:
                c, n = carry.pop(col)
                row.append(c)
                if n > 1:
                    carry[col] = (c, n - 1)
                col += 1
                continue
            c = cells.pop(0)
            rs = int(re.sub(r"\D", "", c.get("rowspan", "1")) or 1)
            cs = int(re.sub(r"\D", "", c.get("colspan", "1")) or 1)
            for _ in range(cs):
                row.append(c)
                if rs > 1:
                    carry[col] = (c, rs - 1)
                col += 1
        rows.append(row)
    return rows


def pct(s):
    s = s.replace("−", "-")
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", s) or re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*", s)
    return float(m.group(1)) if m else None


def sample(s):
    n = re.search(r"(\d[\d,]*)", s)
    p = re.search(r"\b(LV|RV|A|AV|V)\b", s)
    return (int(n.group(1).replace(",", "")) if n else None), (p.group(1) if p else None)


def split_party(h):
    """'Kamala Harris\\nDemocratic' / 'Harry Truman (D)' -> ('Kamala Harris', 'D')."""
    h = h.replace("\n", " ").strip()
    h = re.sub(r"\((Progressive|Dixiecrat|Reform|Green|Libertarian|Independent|American Independent)\)\s*$",
               r"\1", h)  # '(Progressive)' -> 'Progressive'
    for pat, code in PARTY_WORDS + [(r"Dixiecrat", "SR")]:
        m = re.search(r"\s*(?:%s)\s*$" % pat, h)
        if m and m.start() > 0:
            return h[:m.start()].strip(" .,"), code
    return h.strip(" .,"), None


def parse_dates(s, year_hint):
    """-> (start, end, precision, year_inferred). Handles 'Oct. 28-Nov. 1, 1952', 'May 14–20, 1980',
    'February, 1971', 'Late January, 1976', 'Sep 29–30' (year from hint), 'Dec 31, 2023 – Jan 2, 2024',
    'Sep 30 – Oct 1, Oct 4–6' (split field period: first to last day)."""
    s = re.sub(r"\[[^\]]*\]|\(.*?\)", "", s).replace("–", "-").replace("—", "-").replace("−", "-")
    s = re.sub(r"\b(late|early|mid|beginning of|end of|released|through)[- ]", "", s, flags=re.I)
    years = [int(y) for y in re.findall(r"\b(19[3-9]\d|20[0-2]\d)\b", s)]
    body = re.sub(r"\b(19[3-9]\d|20[0-2]\d)\b", " ", s)
    toks, month = [], None  # every (month, day) in order; a bare day takes the last month seen
    for m in re.finditer(r"\b(%s)\b\.?\s*(\d{1,2})?\b|\b(\d{1,2})\b" % MONTH_RE, body, re.I):
        if m.group(1):
            month = MONTHS[m.group(1).lower()]
            toks.append((month, int(m.group(2)) if m.group(2) else None))
        elif month:
            toks.append((month, int(m.group(3))))
    if not toks:
        return None, None, None, None
    sm, sd = toks[0]
    em, ed = toks[-1]
    ey = years[-1] if years else year_hint
    sy = years[0] if len(years) > 1 else (ey - 1 if sm > em else ey)
    prec = "day" if sd else "month"
    try:
        start = dt.date(sy, sm, sd or 1)
        end = dt.date(ey, em, ed or calendar.monthrange(ey, em)[1]) if (ed or not sd) else dt.date(ey, em, sd)
    except ValueError:
        return None, None, None, None
    if end < start:  # bad cell, e.g. year typo
        end = None
    return start, end, prec, not years


def heading(t):
    h = t.xpath("preceding::*[self::h2 or self::h3 or self::h4][1]")
    return text(h[0]) if h else ""


META = [  # (header pattern, role)
    (r"^poll(ing)?\s*(source|firm|organi[sz]ation)?$|^pollster", "pollster"),
    (r"updated", "skip"), (r"\bdates?\b|^month$|administered|conducted", "date"), (r"sample", "sample"),
    (r"margin\s*of\s*error|^moe$", "moe"), (r"^lead|leading|^margin|lead\s*margin", "skip"),
    (r"undecided|other|abstention|wouldn.t vote|none|neither|don.t know|no opinion", "other"),
]


def classify(h):
    hl = h.lower().replace("\n", " ")
    if hl.strip() == "%":
        return "pct"
    for pat, role in META:
        if re.search(pat, hl):
            return role
    return "cand"


def parse_table(tab, cycle, title, ti, refs):
    g = grid(tab)
    nhead = 0
    while nhead < len(g) and all(c.tag == "th" for c in g[nhead]) and nhead < 3:
        nhead += 1
    if nhead == 0 or nhead >= len(g):
        return []
    ncol = max(len(r) for r in g[:nhead])
    hdr = []
    for j in range(ncol):
        seen, parts = set(), []
        for r in g[:nhead]:
            if j < len(r) and id(r[j]) not in seen:
                seen.add(id(r[j]))
                t = text(r[j])
                if t and t not in parts:
                    parts.append(t)
        hdr.append("\n".join(parts))
    roles = [classify(h) for h in hdr]
    if "pollster" not in roles or "date" not in roles:
        return []
    paired = "pct" in roles
    if not paired and roles.count("cand") < 2:
        return []
    sec = heading(tab)
    if NOT_VOTE.search(sec) or any(h.lower() in ("yes", "no", "support", "good") for h in hdr):
        return []
    hy = re.findall(r"\b(19[3-9]\d|20[0-2]\d)\b", sec)
    year = int(hy[-1]) if hy else cycle
    out = []
    for ri, r in enumerate(g[nhead:]):
        if len(r) < ncol or all(c.tag == "th" for c in r):
            continue
        cells = [text(c) for c in r]
        pi = roles.index("pollster")
        pollster = cells[pi].replace("\n", " ")
        di = roles.index("date")
        dates_raw = cells[di].replace("\n", " ")
        start, end, prec, inferred = parse_dates(dates_raw, year)
        eday = dt.date(cycle, 11, 10)
        if inferred and end and end > eday:  # no year in the cell, newest-first table: it's the year before
            start, end = start.replace(year=start.year - 1), end.replace(year=end.year - 1)
        if end:
            year = end.year
        date_check = ("unparsed" if not start else "end before start" if not end else
                      "after election" if end > eday else
                      "over 4 years before" if end < dt.date(cycle - 4, 11, 10) else "ok")
        n, pop = (None, None)
        if "sample" in roles:
            n, pop = sample(cells[roles.index("sample")])
        moe = cells[roles.index("moe")] if "moe" in roles else None
        ids = [h.lstrip("#") for c in (r[pi], r[di]) for h in c.xpath('.//sup[contains(@class,"reference")]/a/@href')]
        row_type = ("result" if RESULT.search(pollster) else
                    "aggregate" if AGGREGATORS.search(pollster) else "poll")
        resp = []
        for j, role in enumerate(roles):
            if role == "cand" and not paired:
                name, party = split_party(hdr[j])
                resp.append((name, party, cells[j], "candidate"))
            elif role == "pct" and j > 0 and roles[j - 1] == "cand":
                lab = hdr[j - 1].lower()
                party = ("D" if "democrat" in lab else "R" if "republican" in lab else "L" if "libertarian" in lab
                         else "G" if "green" in lab else "I" if "independent" in lab else None)
                nm, p2 = split_party(cells[j - 1])
                resp.append((nm, party or p2, cells[j], "candidate"))
            elif role == "other":
                resp.append((hdr[j].replace("\n", " "), None, cells[j], "other"))
        resp = [(a, b, pct(v), k) for a, b, v, k in resp]
        if sum(v is not None for _, _, v, k in resp if k == "candidate") < 2:
            continue  # annotation rows ('Biden withdraws'), blank rows
        qid = f"{cycle}-{ti:02d}-{ri:04d}"
        for name, party, v, kind in resp:
            if v is None:
                continue
            out.append(dict(cycle=cycle, question_id=qid, row_type=row_type, pollster=pollster,
                            dates_raw=dates_raw, start_date=start, end_date=end, date_precision=prec,
                            year_inferred=inferred, date_check=date_check, sample_size=n, population=pop, moe=moe,
                            response=name, party=party, response_type=kind, pct=v,
                            section=sec, source=f.wiki_url(title), table=ti,
                            ref_url=" ; ".join(dict.fromkeys(refs[i] for i in ids if i in refs))))
    return out


def sources():
    for y in range(1948, 2028, 4):
        if y in (1996, 2004):
            continue
        nat = f"Nationwide opinion polling for the {y} United States presidential election"
        try:
            f.wiki_html(nat)
            yield y, nat
        except KeyError:
            yield y, f"{y} United States presidential election"


def main():
    rows = []
    for cycle, title in sources():
        doc = L.fromstring(f.wiki_html(title))
        refs = refs_map(doc)
        n0 = len(rows)
        for ti, tab in enumerate(doc.xpath('//table[contains(@class,"wikitable")]')):
            rows += parse_table(tab, cycle, title, ti, refs)
        print(cycle, title[:40], len(rows) - n0, "responses")
    d = pd.DataFrame(rows)
    # headers without a party label (e.g. 2008 'Barack Obama'): take the party the same name has elsewhere
    known = d.dropna(subset=["party"]).groupby("response").party.agg(lambda p: p.mode()[0])
    d["party"] = d.party.fillna(d.response.map(known))
    d.to_csv("polls_long.csv", index=False)

    # nominee matchups: questions with both eventual nominees among the candidates
    c = d[d.response_type == "candidate"].copy()
    c["surname"] = c.response.str.replace(r"\s+(Jr|Sr|III|II)\.?$", "", regex=True).str.split().str[-1]
    keep = []
    for qid, q in c.groupby("question_id", sort=False):
        cyc = q.cycle.iloc[0]
        dem, rep = NOMINEES[cyc]
        end = q.end_date.iloc[0] or q.start_date.iloc[0]
        if cyc == 2024 and end is not None and end < BIDEN_OUT:
            dem = "Biden"
        s = dict(zip(q.surname, q.pct))
        if dem in s and rep in s:
            o = d[(d.question_id == qid) & (d.response_type == "other")]
            keep.append(dict(cycle=cyc, question_id=qid, row_type=q.row_type.iloc[0], pollster=q.pollster.iloc[0],
                             dates_raw=q.dates_raw.iloc[0], start_date=q.start_date.iloc[0],
                             end_date=q.end_date.iloc[0], date_precision=q.date_precision.iloc[0],
                             date_check=q.date_check.iloc[0],
                             sample_size=q.sample_size.iloc[0], population=q.population.iloc[0],
                             dem=q.response[q.surname == dem].iloc[0], rep=q.response[q.surname == rep].iloc[0],
                             dem_pct=s[dem], rep_pct=s[rep], n_candidates=len(q),
                             third_party_pct=round(sum(v for k, v in s.items() if k not in (dem, rep)), 2) or None,
                             other_undecided_pct=round(o.pct.sum(), 2) if len(o) else None,
                             source=q.source.iloc[0], ref_url=q.ref_url.iloc[0]))
    nom = pd.DataFrame(keep).drop_duplicates(
        subset=["cycle", "row_type", "pollster", "dates_raw", "dem_pct", "rep_pct", "n_candidates"])
    nom.to_csv("polls_nominees.csv", index=False)
    print("polls_long.csv", d.shape, "questions", d.question_id.nunique())
    print("polls_nominees.csv", nom.shape)
    p = nom[nom.row_type == "poll"].assign(end=lambda x: pd.to_datetime(x.end_date))
    print(p.groupby("cycle").agg(n=("question_id", "size"), first=("end", "min"), last=("end", "max")).to_string())


if __name__ == "__main__":
    main()
