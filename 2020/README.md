# 2020 election-year polls

- `roper scrape/` - Roper iPoll studies pulled 15 Nov 2026 for the Fall 2026 PS 4152 lectures on 2020 (lectures 19 and 20).
  One folder per study (`<Roper ID>_<field start>`), holding the study's `.por` data file and its codebook PDF.
  `manifest.tsv`: Roper ID, field start, study id, file id, md5, file name, sponsor, title. Data-file md5s match Roper's;
  PDFs never do (Roper stamps a citation page at download).

  7 studies: ABC News/Washington Post national polls of June, September and October 2019 and October 6-9, 2020;
  Washington Post/Ipsos surveys of Black Americans, January and June 2020; and the FiveThirtyEight/Ipsos debate panel
  (fielded from September 30, 2020).

  Already in other repos, so not repeated here: the other 2020 ABC/Washington Post, CNN, CBS, Monmouth and Fox polls
  (`ps7160/abc_wapo`, `constraint/cnn`, `ps7160/cbs`, `ps7160/monmouth`, `ps7160/fnc`), the 2020 national and state exit
  polls (`ps7160/exit_polls/edison_2020`), AP VoteCast 2020, and Pew's 2020 American Trends Panel waves (`ps7160/atp`).
