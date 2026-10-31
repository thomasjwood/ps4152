"""Build results_1992.csv (national presidential results 1988, 1992, 1996) and
turnout_1980_2000.csv (VEP turnout, US Elections Project).

1992: FEC 'Federal Elections 92' popular-vote summary (all ballot-listed candidates)
      and electoral-vote summary.
1988, 1996: Wikipedia '<year> United States presidential election' results table.
Every year also carries `votes_mit`, the sum of the MIT state file (1976-2024
president, Harvard Dataverse) for the same candidate, as a cross-check."""
import io, re
import pandas as pd, pypdf
import fetch_util as f

rows = []
# ---------------- 1992 from FEC ----------------
FEC = "https://www.fec.gov/resources/cms-content/documents/federalelections92.pdf"
r = pypdf.PdfReader(f.get(FEC, "fec_federalelections92.pdf"))
txt = r.pages[13].extract_text()
lines = [l.strip() for l in txt.splitlines() if l.strip()]
i0 = [i for i, l in enumerate(lines) if l.startswith("Candidate (Party")][0] + 1
cands, nums = [], []
for l in lines[i0:]:
    m = re.match(r"^(.*\))\s*([\d,]+)?$", l)
    if l == "Total":
        break
    if m:
        cands.append(m.group(1)); nums.append(m.group(2))
    else:
        cands.append(l); nums.append(None)          # 'None of These Candidates (Nevada)' etc.
k = lines.index("Total")
loose = [int(x.replace(",", "")) for x in lines[k + 1:] if re.fullmatch(r"[\d,]+", x)]
total92 = loose.pop(len([n for n in nums if n is None]))   # numbers listed after the names, then the total
it = iter(loose)
vals = [int(n.replace(",", "")) if n else next(it) for n in nums]
assert sum(vals) == total92, (sum(vals), total92)
EV92 = {"Bill Clinton": 370, "George Bush": 168}
for c, v in zip(cands, vals):
    m = re.match(r"^(.*?)\s*\((.*)\)$", c)
    name, party = (m.group(1), m.group(2)) if m else (c, "")
    # OCR in the scanned report reads W as Y in a few names
    name = name.replace("Yrite-In", "Write-In").replace("Mac Yarren", "Mac Warren")
    party = {"Socialist Yorkers": "Socialist Workers", "Yorkers League": "Workers League",
             "Yorkers Yorld": "Workers World"}.get(party, party)
    rows.append(dict(year=1992, candidate=name, party=party, votes=v, pct=100 * v / total92,
                     ev=EV92.get(name, 0), total_votes=total92, source=FEC + " (report pp. 9-10)"))
print("FEC 1992 total", total92, "candidates", len(cands))

# ---------------- 1988, 1996 from Wikipedia ----------------
for y in (1988, 1996):
    T = f"{y}_United_States_presidential_election"
    ts = pd.read_html(io.StringIO(f.wiki_html(T)))
    t = [t for t in ts if "Presidential candidate" in " ".join(map(str, t.columns.to_flat_index()))][0]
    t.columns = ["candidate", "party", "home", "votes", "pct", "ev"] + list(t.columns[6:])
    tot = int(t.loc[t.candidate == "Total", "votes"].iloc[0])
    for _, x in t.iterrows():
        if x.candidate in ("Total", "Needed to win"):
            continue
        v = re.sub(r"\D", "", str(x.votes))
        rows.append(dict(year=y, candidate=re.sub(r"\s*\(incumbent\)|\[.*?\]", "", x.candidate),
                         party=re.sub(r"\[.*?\]", "", x.party), votes=int(v) if v else None,
                         pct=100 * int(v) / tot if v else None,
                         ev=int(x.ev) if str(x.ev).isdigit() else None, total_votes=tot,
                         source=f.wiki_url(T) + "#Results"))
d = pd.DataFrame(rows)
# ---------------- MIT cross-check ----------------
mit = pd.read_csv(f.RAW + "/mit_1976-2024-president.csv")
mit = mit[mit.year.isin([1988, 1992, 1996])]
last = lambda s: s.split(",")[0].strip().upper() if isinstance(s, str) else ""
mitsum = mit.groupby(["year", mit.candidate.map(last)]).candidatevotes.sum()
d["votes_mit"] = [mitsum.get((y, c.replace(" (incumbent)", "").split()[-1].upper()), None)
                  if c not in ("Other", "Total") else None for y, c in zip(d.year, d.candidate)]
d.loc[d.candidate.str.contains("None of|Write-In|Other"), "votes_mit"] = None
d.to_csv("results_1992.csv", index=False)
print(d[["year", "candidate", "party", "votes", "pct", "ev", "votes_mit"]].to_string())

# ---------------- turnout ----------------
SHEET = "https://docs.google.com/spreadsheets/d/1bH38j6_e8yA9xq8OMlyLOL6h_iTS7ABQMKNxzFgKBDo/export?format=csv"
t = pd.read_csv(f.get(SHEET, "electproject_national_turnout.csv"))
t = t.iloc[:, :2]; t.columns = ["year", "vep_turnout"]
t = t[t.year.between(1980, 2000)].copy()
t["source"] = "https://www.electproject.org/national-1789-present (sheet " + SHEET.replace("/export?format=csv", "") + ")"
t.to_csv("turnout_1980_2000.csv", index=False)
print(t)
