"""Build state_pres_1976_1996.csv: state presidential returns 1976-1996.

Votes: MIT Election Data + Science Lab, 'U.S. President 1976-2024'
(Harvard Dataverse doi:10.7910/DVN/42MVDX, file 1976-2024-president.csv).
Rows for one candidate on several ballot lines (e.g. New York fusion lines) are summed.
`total` = all candidate votes in the state EXCLUDING blank/void/over/under-vote rows
(MIT's `totalvotes` includes those in a few states); `total_mit` keeps MIT's figure.
Kept candidates: the Democratic and Republican nominees, Anderson (1980) and Perot
(1992, 1996); everyone else is summed into party 'O' (Other).

Electoral votes: parsed from the state results tables of Wikipedia's
'<year> United States presidential election' articles (MIT has no EV column).
The same tables are used to cross-check MIT's vote counts (see build log / README)."""
import io, re
import pandas as pd
import fetch_util as f

MIT_URL = "https://dataverse.harvard.edu/api/access/datafile/13887042"
MIT_DOI = "https://doi.org/10.7910/DVN/42MVDX"
f.get(MIT_URL, "mit_1976-2024-president.csv")
d = pd.read_csv(f.RAW + "/mit_1976-2024-president.csv")
d = d[d.year.between(1976, 1996)].copy()
NONVOTE = {"BLANK VOTE", "BLANK VOTE/SCATTERING", "BLANK VOTE/VOID VOTE/SCATTERING", "BLANK VOTES",
           "OVER VOTE", "OVERVOTES", "UNDERVOTES", "VOID VOTE"}
d["nonvote"] = d.candidate.isin(NONVOTE)

NOMINEES = {  # year: {MIT candidate: (party code, display name)}
    1976: {"CARTER, JIMMY": ("D", "Carter"), "FORD, GERALD": ("R", "Ford")},
    1980: {"CARTER, JIMMY": ("D", "Carter"), "REAGAN, RONALD": ("R", "Reagan"), "ANDERSON, JOHN B.": ("I", "Anderson")},
    1984: {"MONDALE, WALTER": ("D", "Mondale"), "REAGAN, RONALD": ("R", "Reagan")},
    1988: {"DUKAKIS, MICHAEL": ("D", "Dukakis"), "BUSH, GEORGE H.W.": ("R", "Bush")},
    1992: {"CLINTON, BILL": ("D", "Clinton"), "BUSH, GEORGE H.W.": ("R", "Bush"), "PEROT, ROSS": ("I", "Perot")},
    1996: {"CLINTON, BILL": ("D", "Clinton"), "DOLE, ROBERT": ("R", "Dole"), "PEROT, ROSS": ("I", "Perot")},
}
def lab(r):
    return NOMINEES[r.year].get(r.candidate, ("O", "Other"))
d[["party", "candidate_short"]] = pd.DataFrame([lab(r) for r in d.itertuples()], index=d.index)
tot = d[~d.nonvote].groupby(["year", "state"]).candidatevotes.sum().rename("total")
tot_mit = d.groupby(["year", "state"]).totalvotes.first().rename("total_mit")
s = (d[~d.nonvote].groupby(["year", "state", "state_po", "party", "candidate_short"]).candidatevotes.sum()
     .rename("votes").reset_index()
     .merge(tot.reset_index(), on=["year", "state"]).merge(tot_mit.reset_index(), on=["year", "state"]))
s["pct"] = 100 * s.votes / s.total
s["state"] = s.state.str.title().str.replace("Of Columbia", "of Columbia")

# ---- electoral votes and cross-check from Wikipedia ----
def flat(c):
    return [str(x).replace("\xad", "") for x in c]
ev_rows, wk_rows = [], []
for y in NOMINEES:
    T = f"{y}_United_States_presidential_election"
    ts = pd.read_html(io.StringIO(f.wiki_html(T)))
    t = [t for t in ts if isinstance(t.columns, pd.MultiIndex) and t.shape[0] > 50
         and any("State" in str(c) for c in t.columns)][0]
    cols = [flat(c) for c in t.columns]
    st_col = [i for i, c in enumerate(cols) if c[-1] == "State"][0]
    for short in set(v[1] for v in NOMINEES[y].values()):
        for i, c in enumerate(cols):
            head = " ".join(c[:-1])
            if short in head and not head.startswith("Unnamed"):
                kind = c[-1]
                for _, r in t.iterrows():
                    stn = re.sub(r"\[.*?\]|†|\*", "", str(r.iloc[st_col])).strip()
                    stn = {"D.C.": "District of Columbia", "Washington, D.C.": "District of Columbia"}.get(stn, stn)
                    val = re.sub(r"[^\d.]", "", str(r.iloc[i]))
                    if kind in ("E", "electoral votes"):
                        ev_rows.append(dict(year=y, state=stn, candidate_short=short, ev=int(val) if val else 0))
                    elif kind in ("#", "Vote"):
                        wk_rows.append(dict(year=y, state=stn, candidate_short=short, votes_wiki=float(val) if val else None))
ev = pd.DataFrame(ev_rows).drop_duplicates(["year", "state", "candidate_short"])
# Maine / Nebraska congressional-district rows (e.g. 'Maine-1') -> add to the state's EV
ev["state"] = ev.state.str.replace(r"^(Maine|Nebraska)\W*(?:CD)?\s*-?\s*\d.*$", r"\1", regex=True)
ev = ev.groupby(["year", "state", "candidate_short"], as_index=False).ev.sum()
wk = pd.DataFrame(wk_rows).drop_duplicates(["year", "state", "candidate_short"])
s = s.merge(ev, on=["year", "state", "candidate_short"], how="left")
print("wiki state names not in MIT:", sorted(set(ev.state) - set(s.state)))
s.loc[(s.party != "O") & s.ev.isna(), "ev"] = 0   # candidates with no EV column (Anderson, Perot)
s.loc[s.party == "O", "ev"] = None
s["source"] = MIT_DOI + " (votes); https://en.wikipedia.org/wiki/" + s.year.astype(str) + "_United_States_presidential_election (ev)"
# ---- 1996: MIT has no 'PEROT, ROSS' row in AL, MS, NJ, SD, TN; his votes sit in an
# unnamed INDEPENDENT row (candidate NA) that may also include other independents.
# Add Perot rows from Wikipedia's 1996 state table; Other = total - Clinton - Dole - Perot.
s["note"] = ""
w96 = wk[(wk.year == 1996) & (wk.candidate_short == "Perot")].set_index("state").votes_wiki
for st in sorted(set(s[s.year == 1996].state) - set(s[(s.year == 1996) & (s.candidate_short == "Perot")].state)):
    base = s[(s.year == 1996) & (s.state == st)].iloc[0].copy()
    base["party"], base["candidate_short"], base["votes"], base["ev"] = "I", "Perot", int(w96[st]), 0
    base["note"] = "Perot votes from Wikipedia (MIT row has no candidate name)"
    s = pd.concat([s, base.to_frame().T], ignore_index=True)
    m = (s.year == 1996) & (s.state == st)
    s.loc[m & (s.party == "O"), "votes"] = s.loc[m, "total"].iloc[0] - s.loc[m & (s.party != "O"), "votes"].sum()
    s.loc[m & (s.party == "O"), "note"] = "Other = total - Clinton - Dole - Perot(Wikipedia)"
s["pct"] = 100 * s.votes.astype(float) / s.total.astype(float)
# ---- 1992: replace with the FEC's official 'Federal Elections 92' state counts ----
# MIT's 1992 South Carolina row is wrong (Clinton 525,514 vs FEC 479,514; Perot
# 119,257 vs 138,872) and a few other states differ slightly; use FEC for all 1992
# states. Other = FEC state total - (Clinton + Bush + Perot). Run build_fec_1992_state.py first.
fec = pd.read_csv("fec_1992_state.csv")
for r in fec.itertuples():
    m = (s.year == 1992) & (s.state_po == r.st)
    mm = m & (s.candidate_short == r.candidate)
    if int(s.loc[mm, "votes"].iloc[0]) != r.votes:
        s.loc[mm, "note"] = f"FEC count; MIT had {int(s.loc[mm, 'votes'].iloc[0]):,}"
    s.loc[mm, "votes"] = r.votes
    s.loc[m, "total"] = r.total
for st in fec.st.unique():
    m = (s.year == 1992) & (s.state_po == st)
    big3 = s.loc[m & (s.party != "O"), "votes"].sum()
    s.loc[m & (s.party == "O"), "votes"] = s.loc[m, "total"].iloc[0] - big3
s["pct"] = 100 * s.votes / s.total
s["source"] = s.source.where(s.year != 1992,
    "https://www.fec.gov/resources/cms-content/documents/federalelections92.pdf (votes); "
    "https://en.wikipedia.org/wiki/1992_United_States_presidential_election (ev)")
s = s.rename(columns={"state_po": "st", "candidate_short": "candidate"})
s = s.sort_values(["year", "state", "party"])
s = s[["state", "st", "year", "party", "candidate", "votes", "total", "total_mit", "pct", "ev", "note", "source"]]
s.to_csv("state_pres_1976_1996.csv", index=False)
print(s.shape)
print(s.groupby(["year", "candidate"]).agg(votes=("votes", "sum"), ev=("ev", "sum")).to_string())
# ev total check (faithless electors 1976 WA, 1988 WV go to people not kept here)
print(s.groupby("year").ev.sum())
# cross-check MIT vs Wikipedia state counts
x = s.merge(wk.rename(columns={"candidate_short": "candidate"}), on=["year", "state", "candidate"], how="inner")
print("(1992 rows are FEC counts at this point)")
x["diff"] = x.votes - x.votes_wiki
print("state-candidate cells compared:", len(x), " differing:", (x["diff"].abs() > 0).sum())
print(x[x["diff"].abs() > 1000][["year", "state", "candidate", "votes", "votes_wiki", "diff"]].to_string())
x[x["diff"] != 0][["year", "state", "candidate", "votes", "votes_wiki", "diff"]].to_csv("raw/check_state_mit_vs_wikipedia.csv", index=False)
