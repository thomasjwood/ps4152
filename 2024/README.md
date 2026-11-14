# 2024 election-year polls

- `roper scrape/` - every US study fielded in calendar 2024 that Roper iPoll holds with a data file, pulled 13 Nov 2026.
  One folder per study (`<Roper ID>_<field start>`), holding one data file (SPSS `.sav` where offered, else `.por`/`.dta`/`.csv`)
  plus the study's PDFs (codebook, questionnaire, topline). `manifest.tsv`: Roper ID, field start, study id, file id,
  md5, file name, sponsor, title. Data-file md5s match Roper's; PDFs never do (Roper stamps a citation page at download).

  40 studies: ABC News/Ipsos (Feb, Mar SOTU, May), CNN (June), Pew ATP waves 140/145/155, Washington Post-Schar Deciders
  (May), Reuters/Ipsos (Jan large sample, Feb foreign affairs), USA Today/Ipsos Florida, Axios/Ipsos, Chicago Council,
  Knight/Ipsos, KFF (5), SSRS (2), PPIC, Fannie Mae National Housing Survey (12 months), and AP-NORC (Jan, Feb, Jul;
  API/AP-NORC election insights; USAFacts/AP-NORC; Pearson/AP-NORC). The six AP-NORC studies are restricted on iPoll, so
  their `.sav` files were downloaded by hand (no PDFs); md5s match Roper's.

  Not here: the 23 AARP surveys (restricted, and not about the election). Roper had no 2024 exit poll microdata as of
  this pull.
