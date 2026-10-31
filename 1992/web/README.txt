1992 ELECTION LECTURE: NON-ROPER WEB DATA          built Oct 27, 2026
==========================================================================
Every CSV has a `source` column (URL). Every file is rebuilt by the build_*.py
script named below. Run them from this folder with
C:\Users\thoma\AppData\Local\Python\bin\python.exe.
Downloads are cached in raw/; pass refresh=True in fetch_util.py to re-fetch.
fetch_util.py holds the shared download helpers: Wikipedia is fetched through
the MediaWiki API (action=parse).
Run order: build_fec_1992_state.py comes before build_state_pres_1976_1996.py.
Everything else is independent.

polls_1992.csv  (57 rows)                                build_polls_1992.py
  National general-election trial heats, Dec 1991 - Nov 1 1992.
  Columns: pollster, dates (as printed), start, end, Clinton, Bush, Perot,
  other, undecided, lead, race, date (= end), sample, note, ref_url, source.
  - race is "Clinton-Bush-Perot" when the poll has a Perot number, otherwise
    "Clinton-Bush". Each poll appears once, in whichever race Wikipedia
    printed: two-way polls before late March and while Perot was out
    (Jul 17 - Sep 30), three-way otherwise.
  - The page named in the brief, "Nationwide opinion polling for the 1992
    United States presidential election", DOES NOT EXIST on Wikipedia (checked
    via the API). The only national polling table is in the "Polling" section
    of the main article "1992 United States presidential election". This file
    is that table, parsed programmatically.
  - The table has no sample sizes, so `sample` is empty. The Election Results
    row and the event divider rows are dropped.
  - ref_url = the external link in each row's footnote, where there is one.
  - One date error, kept as is: Gallup "Jul. 24 - Jul. 16" has end < start, so
    end is NA. Gallup's approval poll ran Jul 24-26.
  - Dec 26-30 Harris row is 1991. Year is inferred from the reverse-chronological
    order of the table.

polls_1992_primaries.csv  (66 rows, long: poll x candidate)     build_polls_1992.py
  Democratic nomination polls from "1992 Democratic Party presidential
  primaries". There are 6 national polls (Gallup Sep 1991 - Feb 1992, NYT/CBS)
  and 3 New Hampshire polls (Feb 12-15, 1992, with sample sizes).
  - date is approximate: the 15th of the month when only a month is given,
    as in lecture 13's polls_1980_dem_nomination.csv.
  - This is all Wikipedia has, and it is thin.
  - The Republican primaries article has NO polling table, so there are no
    Bush-Buchanan nomination polls here.
  - Suspicious: Wikipedia shows Brown at exactly 21% in all four Gallup
    national polls. That looks like a copy error on the page; treat Brown's
    Gallup series as unreliable.

primary_results_1992.csv  (700 rows, long: contest x candidate)
                                                 build_primary_results_1992.py
  Primary and caucus results for both parties, from the results tables of
  "1992 Democratic Party presidential primaries" and "1992 Republican Party
  presidential primaries".
  - The brief put polls and results in one file. Results are split out here
    because the shapes differ.
  - Candidates:
      D: Clinton, Brown, Tsongas, Harkin, Kerrey, Others, Uncommitted
      R: Bush, Buchanan, Others
  - Columns: date, state, contest_type, candidate, delegates, votes, pct,
    measure, total, pct_check, flag, raw (the original cell text).
  - measure = "votes" for popular votes. Caucus rows count county, state or
    district delegates instead (CDs, SDs, DDs).
  - pct_check recomputes each share from the parsed counts. flag = TRUE where
    it differs from Wikipedia's printed pct by more than 1.5 points (24 rows).
    Most flags are real Wikipedia errors:
      - D Washington DC: the Brown and Tsongas vote counts are copied from
        the North Carolina row.
      - D NC: Clinton is printed as 54.10% but his count implies 64.1%.
      - D Oklahoma and Wisconsin: the "Others" counts duplicate other cells.
      - R Illinois: Bush's 556,280 is copied from the Texas row; the printed
        76.4% is probably right.
      - R NJ: printed pcts don't match the counts.
    Some R flags only reflect the incomplete "Others" column.
  - Delegate sums:
      D (the table mixes contest stages): Clinton 2,004 vs. Wikipedia's
      table total of 1,997; Brown 606 vs. 588. Use the table totals for
      delegate counts.
      R: Bush 1,544 matches; Buchanan 359 vs. 367.
  - Votes summed over Democratic primaries: Clinton 10.54M. Wikipedia's
    infobox gives Brown 4,071,232 and Tsongas 3,656,010; the sums here run a
    little higher (Brown 4.12M, Tsongas 3.71M).

bush_approval.csv  (113 rows)                         build_bush_approval.py
  Gallup job approval for G.H.W. Bush, Jan 1989 - Jan 1993.
  Columns: start, end, approve, disapprove, unsure, source.
  - From the American Presidency Project (UCSB) presidential job approval
    page. Its "George Bush Approval Ratings 1989-1993" chart reads a public
    Google Sheet (gid 1868734071), downloaded as CSV. Roper was not used.
  - Peak 89/8 on Feb 28 - Mar 3, 1991. Low 29/60 on Jul 31 - Aug 2, 1992.
  - Every row sums to 100 (within 1).

state_pres_1976_1996.csv  (1,067 rows)        build_state_pres_1976_1996.py
  State presidential returns 1976, 80, 84, 88, 92, 96 (50 states + DC).
  Columns: state, st, year, party, candidate, votes, total, total_mit, pct,
    ev, note, source.
  - party: D, R, I (Anderson 1980, Perot 1992/1996), O (everyone else summed).
  - total excludes blank/over/under/void rows. total_mit is MIT's raw total.
  - Votes: MIT Election Data + Science Lab, "U.S. President 1976-2024",
    Harvard Dataverse doi:10.7910/DVN/42MVDX (file id 13887042, v10.1).
    Fusion ballot lines (NY etc.) are summed per candidate.
  - EV: parsed from each year's Wikipedia state results table, including the
    Maine/Nebraska district rows. Totals are 538 except 1976 (Reagan 1
    faithless elector, WA) and 1988 (Bentsen 1, WV) = 537. Those faithless
    electors are not attributed to a kept candidate.
  - Two corrections, both marked in `note`:
    1992: all rows use the FEC's official state counts (fec_1992_state.csv).
      MIT's 1992 South Carolina is wrong: Clinton 525,514 (FEC 479,514),
      Perot 119,257 (FEC 138,872). MIT also differs by a few to a few hundred
      votes in DE, FL (-1,100), NE, RI, WA. For 1992, Other = FEC total minus
      the big three.
    1996: MIT has no "PEROT, ROSS" row in AL, MS, NJ, SD, TN; his votes sit in
      an unnamed INDEPENDENT row. Perot's votes there are taken from
      Wikipedia's 1996 state table, and Other is the residual.
  - Remaining MIT vs. Wikipedia differences (not corrected; see
    raw/check_state_mit_vs_wikipedia.csv): 74 state-candidate cells, mostly
    small. Largest:
      1988 LA Dukakis: MIT 717,460 vs. Wiki 734,281
      1984 WA Mondale: 798,352 vs. 807,352
      1976 VT Carter: 77,798 vs. 81,044
      1976 VT Ford: 100,387 vs. 102,085
    Not checked against the FEC 1976-88 reports.
  - County data was not rebuilt: see lecture 13/data/pres_vote_by_county_1868_2024.rds.

fec_1992_state.csv  (153 rows = 51 x Clinton/Bush/Perot)  build_fec_1992_state.py
  FEC "Federal Elections 92", 1992 Electoral and Popular Vote Summary (report
  p. 10), text-extracted from the scanned PDF.
  - The parsed columns add up exactly to the report's printed totals
    (Bush 39,104,545; Clinton 44,909,889; Perot 19,742,267; total
    104,426,659; EV 370-168).

results_1992.csv  (39 rows)                           build_results_1992.py
  National results for 1988, 1992, 1996: candidate, party, votes, pct, ev,
  total_votes, votes_mit (cross-check), source.
  - 1992: FEC popular-vote summary, all 25 lines incl. write-ins and NV
    "None of these".
  - 1988 and 1996: Wikipedia results tables.
  - Turnout is in turnout_1980_2000.csv  (6 rows):
      VEP turnout from the US Elections Project national sheet:
      1980 54.2, 1984 55.2, 1988 52.8, 1992 58.1, 1996 51.7, 2000 54.2.
      The sheet has rates only, no VEP counts.
      The FEC 1992 report gives VAP 189,044,000 and 55.24% VAP turnout.

fred_1988_1994.csv  (1,200 rows, long: date, value, series, description, source)
                                                     build_fred_1988_1994.py
  Monthly, Jan 1985 - Dec 1996. The file name is the one requested; the
  window is wider.
  Series:
    UNRATE, CPIAUCSL, CPI_YOY (computed 12-month % change), A229RX0 (real
    disposable income per capita), A229RX0_YOY (computed), A191RL1Q225SBEA
    (quarterly real GDP growth, SAAR, 48 rows), UMCSENT, FEDFUNDS, USREC.
  - Official NBER dates: peak July 1990, trough March 1991. FRED's USREC = 1
    for Aug 1990 - Mar 1991 (FRED's convention: the peak month is excluded).
  - Unemployment peaked at 7.8% in Jun 1992 and was 7.3% in Oct 1992.
  - CPI inflation peaked at 6.4% yoy in Oct 1990.

ads_1992.csv  (24 rows)                                    build_ads_1992.py
  Every 1992 ad in the Museum of the Moving Image's Living Room Candidate
  archive: 10 Bush, 10 Clinton, 4 Perot.
  Columns: title, candidate, party, sponsor, maker, air_date (Bush ads only;
  the site lists no dates for the others), transcript_start, video_file
  (site mp4 name), url.
  - The site has no description field. transcript_start (the first ~240
    characters of the transcript) stands in for one.

timeline_1992.md
  A dated campaign timeline from the 1990 budget deal and the Gulf War to the
  inauguration, with URLs inline. Each date/number was checked against at
  least one source. "[W]" marks items backed only by Wikipedia. Conflicts are
  marked NOTE. Main ones:
    - Tsongas withdrawal: Mar 19 (contemporary press) vs. "Mar 17" (Wikipedia).
    - Weinberger indictment: Jun 16 (Walsh report) vs. Jun 17 (Wikipedia).
    - VP debate: Wikipedia says "Thursday, Oct 13". Oct 13, 1992 was a Tuesday.
    - LA riot deaths: Wikipedia gives both 55 and 63.
    - Wikipedia's 1992 national totals differ slightly from the FEC's
      (Bush 39,104,550 vs. 39,104,545; Perot 19,743,821 vs. 19,742,267).
  timeline_check.py is the helper used to grep the cached Wikipedia text.

NOT OBTAINED
  - A dedicated Wikipedia national polling page for 1992 (does not exist), and
    sample sizes for the national polls.
  - Republican nomination polling (no Wikipedia table).
  - VEP counts. Only turnout rates are on the Elections Project sheet.
  - Living Room Candidate air dates for Clinton and Perot ads.
