"""Build primary_results_1992.csv: 1992 Democratic and Republican primary/caucus
results by contest, parsed from the results tables on Wikipedia's
'1992 Democratic Party presidential primaries' and
'1992 Republican Party presidential primaries' articles.

Long format: one row per contest x candidate. `measure` says what `votes` counts:
'votes' (popular vote), or for caucuses 'CDs'/'SDs'/'DDs' (county/state/district
delegates). `pct_check` recomputes the share from the parsed counts so that
Wikipedia typos can be spotted (`flag`)."""
import io, re
import pandas as pd
import fetch_util as f

TYPES = r"(Primary Primary|Primary|Caucuses|Caucus|County Conventions|District Conventions|State Convention|primary|caucus)"

def clean(s):
    s = "" if pd.isna(s) else str(s)
    return re.sub(r"\[[^\]]*\]", "", s).replace("\xa0", " ").strip()

def num(s):
    return float(s.replace(",", "")) if s else None

def parse_cell(raw, party):
    s = clean(raw)
    out = dict(delegates=None, votes=None, pct=None, measure=None, raw=s)
    if s in ("", "-", "–", "—", "?", "nan"):
        return out
    m = re.search(r"(\d+)\s*Del\.", s)
    if m:
        out["delegates"] = int(m.group(1)); s = (s[:m.start()] + s[m.end():]).strip()
    if party == "R" and re.fullmatch(r"\d{1,3}", s):   # delegates only (e.g. NY: '103')
        out["delegates"] = int(s); return out
    if party == "R":
        m = re.match(r"^(\d{1,3})\s+(?=\d)", s)       # leading delegate count (followed by a vote count)
        if m and not re.match(r"^\d{1,3},", s):
            out["delegates"] = int(m.group(1)); s = s[m.end():].strip()
    # all "count [unit] (pct)" groups
    groups = re.findall(r"([\d,]+)?\s*(CDs|SDs|DDs|SD)?\s*\((\d+(?:\.\d+)?)%?\)", s)
    if groups:
        # prefer the raw popular-vote group (no unit) if present
        g = [x for x in groups if not x[1]] or groups
        cnt, unit, p = g[-1]
        out.update(votes=num(cnt), pct=float(p), measure=unit or "votes")
    else:
        m = re.match(r"^([\d,]+)$", s)
        if m:
            out.update(votes=num(m.group(1)), measure="votes")
    return out

rows = []
# ---------------- Democrats ----------------
T = "1992_Democratic_Party_presidential_primaries"
ts = pd.read_html(io.StringIO(f.wiki_html(T)))
d = [t for t in ts if isinstance(t.columns, pd.MultiIndex) and "Bill Clinton" in " ".join(map(str, t.columns.to_flat_index()))][0]
cands = ["Bill Clinton", "Jerry Brown", "Paul Tsongas", "Tom Harkin", "Bob Kerrey", "Others", "Uncommitted"]
d.columns = ["date", "contest", "pledged"] + cands
for _, r in d.iterrows():
    contest = clean(r["contest"])
    if contest.startswith("Total"):
        continue
    m = re.match(rf"^(.*?)\s*{TYPES}\s*(.*)$", contest)
    state, ctype, total = (m.group(1), m.group(2), m.group(3)) if m else (contest, "", "")
    tm = re.match(r"([\d,]+)\s*(CDs|SDs|DDs)?", total)
    date = re.sub(r"\s*\(.*$", "", clean(r["date"]))
    for c in cands:
        p = parse_cell(r[c], "D")
        rows.append(dict(party="Democratic", date=date + ", 1992", state=state,
                         contest_type=ctype.replace("Primary Primary", "Primary").lower(),
                         total_reported=num(tm.group(1)) if tm else None,
                         total_measure=(tm.group(2) or "votes") if tm else None,
                         pledged_delegates=clean(r["pledged"]),
                         candidate=c, **p, source=f.wiki_url(T) + "#Results"))

# ---------------- Republicans ----------------
T = "1992_Republican_Party_presidential_primaries"
ts = pd.read_html(io.StringIO(f.wiki_html(T)))
g = [t for t in ts if isinstance(t.columns, pd.MultiIndex) and "Pat Buchanan" in " ".join(map(str, t.columns.to_flat_index()))][0]
g = g.iloc[:, :6]
g.columns = ["date", "pledged", "contest", "George H. W. Bush", "Pat Buchanan", "Others"]
for _, r in g.iterrows():
    contest = clean(r["contest"])
    if contest in ("Contest", "") or contest.startswith("Total") or clean(r["date"]).startswith("Total"):
        continue
    m = re.match(rf"^(.*?)\s*{TYPES}\s*(.*)$", contest)
    state, ctype = (m.group(1), m.group(2)) if m else (contest.replace("[?]", "").strip(), "")
    date = re.sub(r"\s*\(.*$", "", clean(r["date"]))
    for c in ["George H. W. Bush", "Pat Buchanan", "Others"]:
        p = parse_cell(r[c], "R")
        rows.append(dict(party="Republican", date=date + ", 1992", state=state,
                         contest_type=ctype.lower(), total_reported=None, total_measure=None,
                         pledged_delegates=clean(r["pledged"]),
                         candidate=c, **p, source=f.wiki_url(T) + "#Results"))

df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"], format="%B %d, %Y").dt.date
df.loc[df.candidate == "Bill Clinton", "candidate"] = "Bill Clinton"
# recompute shares from parsed counts (same measure within contest)
key = ["party", "date", "state", "contest_type"]
vv = df[df.measure.notna()].groupby(key + ["measure"])["votes"].transform("sum")
df.loc[df.measure.notna(), "sum_counts"] = vv
df["total"] = df.total_reported.where(df.total_reported.notna() & (df.total_measure == df.measure), df.sum_counts)
df["pct_check"] = (100 * df.votes / df.total).round(2)
df["flag"] = ((df.pct - df.pct_check).abs() > 1.5) & df.pct.notna() & df.pct_check.notna()
df = df.drop(columns=["sum_counts"])
df.to_csv("primary_results_1992.csv", index=False)
print(df.shape)
print(df[df.flag][["party", "date", "state", "candidate", "votes", "pct", "pct_check", "raw"]].to_string())
# national popular-vote totals for primaries (votes measure, primaries only)
pv = df[(df.measure == "votes") & df.contest_type.str.contains("primary")].groupby(["party", "candidate"]).votes.sum()
print(pv)
