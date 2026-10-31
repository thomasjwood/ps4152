# 1992 election polls (ps 4152, lecture 14)

- `roper scrape/` - 1991-93 polls from Roper iPoll, one folder per study (`<Roper ID>_<field start>`), including the
  VRS 1992 national exit poll (`31098701_1992-11-03/vrs1992natelec.por`). The 16 CBS/NYT polls that exist only as
  ASCII `.dat` files are read with `1992 roper dat reader.R`, using the layouts in `layouts/` (see its README).
- `roper toplines/` - iPoll topline pulls (JSON).
- `web/` - Wikipedia polling (`polls_1992.csv`, `polls_1992_primaries.csv`), results, approval and FRED series, each
  with the `build_*.py` script that makes it.

ANES time series and cumulative files: https://github.com/thomasjwood/constraint/tree/main/anes_ts
