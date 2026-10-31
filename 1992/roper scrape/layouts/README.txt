How to read the 1992 CBS News/New York Times polls: "1992 roper dat reader.R" in the lecture 14 folder.
  source("1992 roper dat reader.R"); d <- read_cbsnyt92("cbsnyt1992-oct", label = TRUE)
  cbsnyt92_studies lists every study name; check_cbsnyt92_layout(study) lists data values a layout doesn't code.

WHAT THESE ARE
  Roper has 16 of the 1992 CBS/NYT national polls only as an ASCII .dat plus a scanned questionnaire (no text layer)
  with each item's card/column written in by hand: [1/30] = card 1, column 30. These layouts are those annotations,
  transcribed page by page (Oct 2026), one row per item: var, name, card, col, width, question, codes. Most PDFs also
  end with typed CBS card documentation ("columns X correspond to questions Y", geography codes, and in some a
  single-column frequency printout); that was used to confirm hard-to-read annotations and to add sex (1/22) and the
  card-3 geography (region, cbs_region, state, urbanicity/urbanity, time_zone).
  The 7 other national polls (janrecruit, may2, jul, jul2, aug2, sep2, oct2) come as SPSS portable files; the reader
  reads those directly.

FILE FORMAT (all 16): three 80-column cards per respondent, in order; card number in col 1, respondent ID in cols 2-6
  (agrees across the three cards for every case). Weight: card 3 cols 49-54, xxx.xxx, sums to n (except May, below).
  From August on, "Before 1982" in the years-voted/registered items is a lone "-" punch; the reader reads it as 10.

CHECKS
  - Every coded item: data values vs. the layout's codes (check_cbsnyt92_layout). Left over across all 16 polls:
    23 items with stray codes, 104 cases in all, almost all 1-6 cases of an unprinted open-end code. Largest:
    mar q64 (2/28) code 3, 39 cases, not printed (probably a volunteered "both").
  - Skip patterns: registered-voter blocks are blank for exactly the not-registered cases in every poll; follow-ups
    are blank for exactly the cases their filter excludes.
  - No two layout rows share a column; no duplicate var names.
  - Weighted three-way vote vs. published CBS/NYT toplines (Clinton/Bush/Perot):
      mar   q55        31.5/43.6/15.8   published 31/44/16
      apr   q15        28.2/38.0/23.0   published 28/38/23
      jun   q12        23.7/32.3/30.2   published 24/32/30
      oct3  q9a leaners 41.0/37.2/17.1  published 42/37/17

THINGS TO KNOW
  - The "lean" column after a vote question (jan q6a, feb2 col 38, mar q8a, apr q11a, jun q12a, jul3 q5a, aug q7a,
    aug3 q7a, sep q7a, oct q9a, oct3 q9a, track q9a, ...) is NOT the lean question alone: CBS copied the first
    answer in, so it is the vote with leaners allocated. The layouts label it that way.
  - Income (3/77) is one combined column (4 or 5 categories); the $15k/$30k/$50k follow-ups have no columns.
  - may: 386 cases (IDs 868-1253) have no weight; the weights sum to 867. They are not the Black oversample (mostly
    white; the weighted part already has 211 Black respondents). Unexplained; use the weighted cases.
  - aug3: two surveys in one file. Aug 20 (n=656) has card 1 col 54 filled; Aug 23-24 (n=1186) is blank there. The
    questionnaire is the Aug 20 version; Aug 23-24-only columns are kept as "unknown qNN" with no question text.
  - oct: includes callbacks of 489 debate viewers (q107-q119).
  - debate: card 1 cols 29-57, card 2 cols 66-77, card 3 cols 7-11 and 71-80 hold undocumented data (look like
    demographics) that don't match OCT92A by ID; left out.
  - track (Oct 27 - Nov 2, n=4650): int_day (1/21) is the day of week, 1=Sunday, inferred from when items were added
    or dropped. q2-q9 and q12 were asked of everyone Oct 27-30. likely_wt (3/20-25) is read raw: divide by 1000.
  - oct3: an undocumented 6-digit field at 3/30-35 looks like a second weight; left out.
  - Left out everywhere: first name, phone numbers, interviewer/batch/variance fields.

CLEAN FILES (data/roper scrape/clean/, built by "1992 cbsnyt build.R")
  cbsnyt1992-<poll>.rds   all 23 polls, one tibble each: every item with value labels (haven_labelled) and a variable
                          label "name: question"; study, field_start, field_end and weight (sums to n) up front.
  cbsnyt1992_core.rds     the 23 polls stacked (39,362 rows), the items most of them share as factors with common
                          levels: registered, Bush approval (overall/economy/foreign policy), favorability of Bush,
                          Clinton and Perot, likely to vote, vote (Bush vs. "the Democratic candidate", Bush-Clinton,
                          Bush-Clinton-Perot, and Bush-Clinton-Perot "if Perot were on the ballot" for Jul 16 - Sep),
                          economy rating, 1988 vote, party ID, ideology, sex, age, race, education, income.
                          core_map in the build script says which question each comes from in each poll. NA = not
                          asked (in that poll, or of that respondent: vote items are registered voters only).
  Vote items have leaners allocated wherever a lean follow-up was asked (all but March's 3-way and Feb/Mar Bush-Clinton).
  Income: polls with $50-75K and over $75K are collapsed to "Over $50K".
  Weighted 3-way vote from the core file: mar 43.6/31.5/15.8 (B/C/P), apr 38.0/28.2/23.0, jun (leaners) 34.3/26.0/32.8,
  oct3 (leaners) 37.2/41.0/17.1, track (leaners) 34.7/43.8/16.8.

Roper terms of use: no redistribution of the data. Keep these files out of anything shared with students.
