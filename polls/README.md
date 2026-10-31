# Presidential general-election polls

**Start here:**

| file | what | rows |
|---|---|---|
| `presidential_polls_national_1948-2024.csv` | national polls, every cycle 1948-2024 | 8,105 |
| `presidential_polls_state_2012-2024.csv` | state polls, 2012 (17 states), 2016, 2020, 2024 (all states, plus ME/NE districts) | 10,647 |
| `wikipedia/polls_gallup_monthly.csv` | Gallup trial heats by month, 1936-2024 (dated by month only, so not merged) | 1,129 |

Both combined files have one row per **poll question that includes both eventual major-party nominees**. A poll asking
a two-way and a full-field question, or reporting likely and registered voters separately, has a row for each:
filter on `n_candidates` and `population` to pick one. Built by `build presidential polls combined.R` from the
inputs in `sources/` and `wikipedia/`.

## Columns

`cycle`, `state`/`state_abb` (state file), `pollster`, `start_date`, `end_date`, `sample_size`, `population`
(LV/RV/A/V), `dem`, `rep` (nominee names), `dem_pct`, `rep_pct`, `margin` (dem - rep), `n_candidates`,
`third_party_pct` (named third-party candidates combined), `grade_538` (538's pollster rating, 2020-24),
`source` (the source the numbers come from), `sources` (every source that had the poll), `n_sources`, `source_id`,
`also_ids` (the ids it has in the other sources), `possible_duplicate`, `url`.

## Sources and coverage

| source | file in `sources/` | national | state |
|---|---|---|---|
| 538 | `538_president_polls_historical_2020_2024.csv` (from ps7160) | 2020, 2024 | 2020, 2024 |
| HuffPost Pollster | `huffpost_pollster_2012_races.rds`, `huffpost_pollster_2016_president.rds` (Dropbox) | 2012, 2016 | 2012, 2016 |
| Wikipedia | `wikipedia/polls_nominees.csv` (scraped Oct 2026) | 1948-1992, 2000, 2008-2024 | - |
| RealClearPolitics | `rcp_2004.csv` ... `rcp_2016.csv` (lecture 2) | 2004-2016, two-way only | - |
| pollingreport.com | `pollingreport_2000_gore_bush.csv`, `pollingreport_2008_mccain_obama.csv` | 2000, 2008 | - |

- **1996 has no poll-level data** in any of these, only the Gallup monthly series.
- **2004 is RCP only** (Bush-Kerry, Jan-Nov 2004).
- 1948-1992 are Wikipedia only and thin (8-76 polls a cycle, mostly Gallup and Harris).

## How duplicates are handled

The same poll often appears in two or three sources. Two rows from **different** sources are treated as one poll when
cycle and state match, end dates are within a day, both percentages agree to rounding (538's 44.6 = Wikipedia's 45),
and the pollster names share a word ("ABC/Wash Post" ~ "ABC News/The Washington Post"). The kept row takes its numbers
from the first source in this order: 538, HuffPost Pollster, Wikipedia, RCP, pollingreport. `sources` lists them all.
Rows within one source are never merged with each other (they're separate questions), except exact repeats.

`possible_duplicate = TRUE` (196 national rows, no state rows) marks a row where another source has the same pollster,
end date, population and number of candidates but numbers more than half a point apart: probably the same question
reported differently (e.g. Wikipedia's 2000 page often differs from pollingreport by 1-2 points). They're kept; drop
one side if it matters.

## Rules

- **Nominees** by surname: 1948 Truman/Dewey through 2024 Harris/Trump. For 2024, Biden-Trump counts as the nominee
  matchup for polls ending before July 21, 2024 (Biden's withdrawal), Harris-Trump after.
- Early-cycle polls of the eventual nominees are kept (e.g. 2012 starts in March 2009).
- Wikipedia rows with flagged dates (`date_check != "ok"` in `wikipedia/`) are left out.
- Election results and polling averages (RCP Average, etc.) are left out.

`presidential polls national 00-24.csv` and `presidential poll readme` are the older two-way 2000-2024 file used in
lecture 2; the combined national file supersedes it.
