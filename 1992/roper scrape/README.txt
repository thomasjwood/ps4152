ROPER CENTER iPOLL SCRAPE, 1992 ELECTION CYCLE (pulled 2026-10-27)

Scope: every U.S. study in Roper iPoll with interview dates 1991-06-01 to 1993-01-31 that has downloadable files:
633 studies (617 with files; 16 list no files), 2,070 of 2,075 files, 621 MB.
Includes national polls (CBS/NYT, ABC/WaPo, Gallup/CNN/USA Today, Gallup/Newsweek, NBC/WSJ, LA Times, Times Mirror,
Yankelovich/Time/CNN, Washington Post, AP, USA Today, U.S. News, Roper Reports), the VRS national and state exit polls
and primary exit polls, the LA Times exit poll, and state polls (Minnesota, Iowa, Connecticut, Rhode Island, California,
Atlanta Journal-Constitution southern polls, etc.).

Layout: one folder per study, "<Roper archive id>_<first interview date>", holding every file Roper lists for it
(codebook PDF/DOC, ASCII .dat, SPSS .por/.sav, Stata .dta, csv, readme).

roper_1992_index.json: one record per study: archiveId, dir, title, surveyBy, conductedBy, coverage, subdivisions
(state for state polls), interview start/end, abstract, Roper study id, and each file's name/type/format/size/md5.
"tier" is only the download order (0 exit polls, 1 political national polls, 2 other political, 3 media/pollster
non-political, 4 everything else).

Key studies:
  31098701_1992-11-03  VRS national election day exit poll (vrs1992natelec.por / .dat, codebook)
  31098702-31098751    VRS state exit polls, Nov 3 1992 (one folder per state)
  310987xx-310988xx    VRS state primary exit polls, Feb-Jun 1992
  31092997_1992-11-03  LA Times national exit poll
  31088151-31088163    Gallup/CNN/USA Today fall tracking polls (31088163 = phase 2-3 cumulative file)
  31091395-31091397    CBS/NYT October polls and pre-election tracking
  31086760-31086772    ABC/WaPo election polls

Checks: every data file (.dat/.por/.sav/.dta/.csv) and readme matches Roper's md5 checksum. Codebook PDFs don't match
because Roper stamps a citation/terms page onto PDFs at download, so they're larger than the listed size; the content is
the same codebook.
Not downloadable (Roper returns HTTP 500 every time): 5 LA Times ballot PDFs:
  31092973 uslat1992-273_FLballot.pdf, 31092984 uslat1992-286_CAballot.pdf,
  31092997 uslat1992-303_calballot.pdf / _nyballot.pdf / _natballot.pdf

Roper terms of use: no redistribution of the data. Keep these files out of anything shared with students.
