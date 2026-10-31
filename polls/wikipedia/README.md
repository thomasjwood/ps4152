# National presidential polls from Wikipedia, 1936-2024

Every national general-election trial heat on Wikipedia, scraped Oct 30, 2026. Rebuild with
`python build_polls.py` and `python build_monthly.py`. Both read the cached pages in `raw/`; delete a file there to
re-download it from Wikipedia.

## Files

| file | one row per | cycles |
|---|---|---|
| `polls_nominees.csv` | poll question that includes both eventual major-party nominees | 1948-1992, 2000, 2008-2024 |
| `polls_long.csv` | poll question x response (every matchup, including hypotheticals, other, undecided) | same |
| `polls_gallup_monthly.csv` | Gallup poll x candidate, dated by month only | 1936-2024, every cycle |

**For most lectures use `polls_nominees.csv`.** Key columns: `cycle`, `pollster`, `start_date`, `end_date`,
`dem`, `rep`, `dem_pct`, `rep_pct`, `n_candidates` (2 = head-to-head; 3+ includes Wallace, Anderson, Perot, Nader,
Johnson, Stein, Kennedy...), `third_party_pct`, `other_undecided_pct`, `sample_size`, `population` (LV/RV/A),
`row_type` (`poll`, `result` = the actual vote, `aggregate` = RCP etc. averages), `date_check`, `source`, `ref_url`
(the poll's citation).

Polls per cycle in `polls_nominees.csv` (`row_type == "poll"`):

| cycle | polls | first end date | last end date |
|---|---|---|---|
| 1948 | 15 | 1947-07 | 1948-10 |
| 1952 | 8 | 1952-06 | 1952-11 |
| 1956 | 19 | 1954-03 | 1956-11 |
| 1960 | 21 | 1957-07 | 1960-11 |
| 1964 | 23 | 1963-11 | 1964-11 |
| 1968 | 23 | 1968-04 | 1968-11 |
| 1972 | 37 | 1971-02 | 1972-11 |
| 1976 | 33 | 1976-01 | 1976-10 |
| 1980 | 76 | 1978-04 | 1980-11 |
| 1984 | 75 | 1982-09 | 1984-11 |
| 1988 | 12 | 1988-05 | 1988-11 |
| 1992 | 57 | 1991-12 | 1992-11 |
| 2000 | 77 | 2000-10 | 2000-11 |
| 2008 | 555 | 2006 | 2008-11 |
| 2012 | 594 | 2009-04 | 2012-11 |
| 2016 | 785 | 2015-05 | 2016-11 |
| 2020 | 804 | 2017-03 | 2020-11 |
| 2024 | 891 | 2021-04 | 2024-11 |

## Sources

- **1968-1980, 2000, 2008-2024:** "Nationwide opinion polling for the YYYY United States presidential election".
- **1948-1964, 1984-1992:** the Polling table of the "YYYY United States presidential election" article (no
  separate polling page exists).
- **1996 and 2004:** Wikipedia has no national poll table; they are only in `polls_gallup_monthly.csv`, from
  "Opinion polling for United States presidential elections".
- 2000's page has only Oct-Nov 2000 polls. For a longer 2000-2024 series see `../presidential polls national 00-24.csv`
  (RCP/pollingreport, two-way only).

## Rules and caveats

- **Nominee matchup** = the question includes both eventual nominees (matched on surname). For 2024, Biden-Trump
  counts until Biden withdrew (polls ending before July 21, 2024), Harris-Trump after.
- A poll that appears in two tables (e.g. a 2008 two-way table and the "Democratic nominee vs. Republican nominee"
  table) is kept once in `polls_nominees.csv`; `polls_long.csv` keeps both.
- **Dates:** `start_date`/`end_date` come from the cell; month-only cells ("February, 1971") get the whole month and
  `date_precision = "month"`. Cells with no year take it from the section heading or the row above
  (`year_inferred`). Field periods with a gap ("Sep 30 - Oct 1, Oct 4-6") run first to last day.
- **`date_check` flags 11 questions** whose Wikipedia dates are wrong or odd, kept as Wikipedia shows them: e.g. 2008
  Gallup "May 9-13, 2012" and Hotline "September 11-13, 2002", a 1992 Gallup "Jul. 24 - Jul. 16", a 1973
  post-election Nixon-McGovern poll. Filter `date_check == "ok"` for plotting.
- `population` and `sample_size` are blank before 1988 (not reported on Wikipedia).
- Event rows (conventions, debates, "Biden withdraws") are dropped.
- `polls_gallup_monthly.csv`: the page frames these as Gallup polls but gives no pollster per row; several polls can
  share a month (`poll_seq` keeps their order). `row_type == "result"` rows are the actual vote.
