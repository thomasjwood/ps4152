"""Parse the FEC's 'Federal Elections 92' report (1992 Electoral and Popular Vote
Summary, report p. 10 / PDF p. 15) into fec_1992_state.csv, and the national
popular-vote summary (PDF p. 14). Text is extracted with pypdf from the scanned
report, so numbers are reassembled from OCR fragments and checked against the
report's own column totals."""
import re
import pandas as pd, pypdf
import fetch_util as f

URL = "https://www.fec.gov/resources/cms-content/documents/federalelections92.pdf"
p = f.get(URL, "fec_federalelections92.pdf")
r = pypdf.PdfReader(p)
page = r.pages[14].extract_text()
rows = []
for line in page.splitlines():
    m = re.match(r"^([A-Za-z]{2})\s+(\d{1,2})\s+(.*)$", line.strip())
    if not m:
        continue
    st, ev, rest = m.group(1).upper(), int(m.group(2)), m.group(3)
    # OCR: thousands separators come out as , ' ; or a space; '.' is stray noise.
    # Whitespace continues a number when the previous token ends, or the next
    # token starts, with a separator (, ' ;); otherwise it separates numbers.
    toks = [t.strip(".") for t in rest.split() if t.strip(".")]
    nums_s = []
    for t in toks:
        if nums_s and (nums_s[-1][-1] in ",';" or t[0] in ",';"):
            nums_s[-1] += t
        else:
            nums_s.append(t)
    s = " ".join(re.sub(r"[^\d]", "", t) for t in nums_s)
    nums = [int(t) for t in s.split()]
    if len(nums) != 4:
        print("could not parse:", line); continue
    rows.append(dict(st=st, ev=ev, Bush=nums[0], Clinton=nums[1], Perot=nums[2], total=nums[3]))
d = pd.DataFrame(rows)
tot = re.search(r"Total:\s*168\s+370\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", page)
T = [int(x.replace(",", "")) for x in tot.groups()]
print("states parsed:", len(d), " EV:", d.ev.sum())
print("column sums vs report totals:", d[["Bush", "Clinton", "Perot", "total"]].sum().tolist(), T)
d["ev_winner"] = (d.Clinton > d.Bush).map({True: "Clinton", False: "Bush"})
d = d.melt(id_vars=["st", "ev", "ev_winner", "total"], value_vars=["Clinton", "Bush", "Perot"],
           var_name="candidate", value_name="votes")
d["ev"] = d.ev.where(d.candidate == d.ev_winner, 0)
d["pct"] = 100 * d.votes / d.total
d["source"] = URL + " (p. 10 of report)"
d.drop(columns="ev_winner").to_csv("fec_1992_state.csv", index=False)
print(d.shape)
