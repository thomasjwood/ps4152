# Candidates in American general elections, 2006-2024

`candidates_2006-2024.rds`: every general-election candidate for House, Senate, governor and president, 2006-2024
(odd years are specials and off-year governors' races). One row per candidate per race, 15,639 rows. Read with
`readr::read_rds()`; variable labels are kept from the Stata original.

Source: Cha, Jeremiah; Kuriwaki, Shiro; Snyder, James M. Jr., "Candidates in American General Elections",
Harvard Dataverse, doi:10.7910/DVN/DGDRDT, version 4.1, file `candidates_2006-2024` ("Main dataset, V4").
CC0 1.0. Downloaded Nov 2026 as the original `.dta` (md5 3d90f2105c79b9542a2ae6932ca8aa24) and saved as rds.

## Columns

| column | what |
|---|---|
| `year` | year of the election |
| `state` | two-letter state abbreviation |
| `office` | H = House, S = Senate, G = governor, P = president |
| `dist` | congressional district number (House only) |
| `type` | G = general, S = special |
| `nextup` | next year the seat is up |
| `party`, `party_formal` | party, short (D, R, Lbt, Grn, I, Other ...) and as listed on the ballot |
| `name_snyder` | candidate name, "LAST, FIRST" |
| `inc` | 1 = incumbent |
| `candidatevotes`, `totalvotes` | the candidate's votes and all votes cast in the race |
| `won` | 1 = won the general election |
| `runoff` | 1 = runoff election (where applicable) |
