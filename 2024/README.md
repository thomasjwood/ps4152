# 2024 election polls

- `roper toplines/` - Roper iPoll question toplines, US national, pulled 13 Nov 2026 (one JSON per search;
  same fields as `1992/roper toplines/`, plus `sid`/`qid` for the iPoll study and question ids and Roper's `notes`).
  Searches (keyword, field dates):
  - `mip.json` - "most important problem", 2021-01-20 to 2024-11-05
  - `too_old.json` - "too old", 2023-01-01 to 2024-11-05
  - `sharpness.json` - "mental sharpness", 2023-01-01 to 2024-11-05
  - `trust_immig.json`, `trust_econ.json`, `trust_infl.json` - "trust immigration / economy / inflation", 2023-01-01 to 2024-11-05
  - `betterjob_immig.json`, `betterjob_econ.json`, `betterjob_infl.json` - "better job immigration / economy / inflation", 2023-01-01 to 2024-11-05
  - `approve_immig.json`, `approve_infl.json` - "approve Biden handling immigration / inflation", 2021-01-20 to 2024-11-05

  Keyword searches are broad: each file includes some off-topic items (e.g. "too old" catches health questions).
  Filter on `text` before use.
