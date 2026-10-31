"""Build bush_approval.csv: Gallup job approval for George H. W. Bush, 1989-1993.
Source: The American Presidency Project (UCSB), 'Presidential Job Approval' page,
whose 'George Bush Approval Ratings 1989-1993' chart reads from a public Google
Sheet (key 1iEl565M1mICTubTtoxXMdxzaHzAcPTnb3kpRndsrfyY, gid 1868734071).
UCSB attributes the series to Gallup (via the Roper Center)."""
import pandas as pd
import fetch_util as f

SHEET = ("https://docs.google.com/spreadsheets/d/1iEl565M1mICTubTtoxXMdxzaHzAcPTnb3kpRndsrfyY/"
         "export?format=csv&gid=1868734071")
PAGE = "https://www.presidency.ucsb.edu/statistics/data/presidential-job-approval"
path = f.get(SHEET, "ucsb_bush41_approval.csv")
d = pd.read_csv(path)
d.columns = ["start", "end", "approve", "disapprove", "unsure"]
for c in ["start", "end"]:
    d[c] = pd.to_datetime(d[c], format="%m/%d/%Y").dt.date
d["source"] = PAGE + " (data sheet: " + SHEET.replace("export?format=csv&", "edit#") + ")"
d = d.sort_values("end", ascending=False)
bad = d[(d.approve + d.disapprove + d.unsure).sub(100).abs() > 1]
if len(bad):
    print("rows not summing to 100:\n", bad)
d.to_csv("bush_approval.csv", index=False)
print(d.shape, d.end.min(), d.end.max())
print("max", d.loc[d.approve.idxmax()].to_dict())
print("min", d.loc[d.approve.idxmin()].to_dict())
