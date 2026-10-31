# 2012 election polls (ps 4152, lectures 15-16)

- ` scrape/` - 13 national polls from Rper iPll, Oct 2011 - Nov 2012, one folder per study (`<Rper ID>_<field start>`):
  Rper's SPSS portable file plus its codebook and topline PDFs. `manifest.tsv` gives each file's Rper study/file ID and MD5.
- `exit polls/` - Edison/NEP national exit polls, 2012 and 2008 (`usmi2012-natelec.por`, `usmi2008-natelec.por`).
- `web/` - national polling from Wikipedia: `polls_2012.csv` (Obama vs. every Republican, 2009-2012) and
  `polls_2012_gop_primary.csv` (Republican nomination), rebuilt by `build_polls_2012.py`.

ANES time series and cumulative files: https://github.com/thomasjwood/constraint/tree/main/anes_ts
