"""Gallup presidential trial heats, 1936-2024, from Wikipedia's 'Opinion polling for United States presidential
elections': one table per cycle, one row per poll, dated only by month (Month | candidate % ...). The page frames
these as Gallup's polls but gives no pollster per row. It is the only Wikipedia national series for 1996 and 2004.

Output: polls_gallup_monthly.csv, one row per poll x candidate, plus each cycle's 'Actual result' rows
(row_type = 'result'); the page's 'Difference between actual result and final poll' rows are dropped.
"""
import re, sys
import pandas as pd, lxml.html as L
import fetch_util as f
from build_polls import text, grid, pct, split_party, heading, MONTHS

sys.stdout.reconfigure(encoding="utf-8")
TITLE = "Opinion polling for United States presidential elections"


def main():
    doc = L.fromstring(f.wiki_html(TITLE))
    out = []
    for tab in doc.xpath('//table[contains(@class,"wikitable")]'):
        cycle = int(re.search(r"\d{4}", heading(tab)).group())
        g = grid(tab)
        hdr = [text(c) for c in g[0]]
        if not hdr or hdr[0].lower() != "month":
            continue
        seq = 0
        for r in g[1:]:
            cells = [text(c).replace("\n", " ") for c in r]
            if len(cells) < len(hdr) or re.match(r"difference", cells[0], re.I):
                continue
            vals = [pct(v) for v in cells[1:len(hdr)]]
            if sum(v is not None for v in vals) < 2:
                continue  # months with no poll
            result = bool(re.search(r"result", cells[0], re.I))
            ms = [MONTHS[m.lower()] for m in re.findall(r"[A-Za-z]+", cells[0]) if m.lower() in MONTHS]
            seq += 1
            for h, v in zip(hdr[1:], vals):
                name, party = split_party(re.sub(r"\s*%\s*$", "", h))
                if v is not None:
                    out.append(dict(cycle=cycle, poll_seq=None if result else seq,
                                    row_type="result" if result else "poll", month_label=cells[0],
                                    month=ms[-1] if ms else None, candidate=name, party=party, pct=v,
                                    source=f.wiki_url(TITLE)))
    d = pd.DataFrame(out)
    d.to_csv("polls_gallup_monthly.csv", index=False)
    print("polls_gallup_monthly.csv", d.shape)
    p = d[d.row_type == "poll"]
    print(p.groupby("cycle").poll_seq.nunique().to_frame("polls").T.to_string())
    print(sorted(d.candidate.unique()))


if __name__ == "__main__":
    main()
