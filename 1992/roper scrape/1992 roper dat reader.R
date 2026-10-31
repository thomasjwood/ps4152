# Read the 1992 CBS News/New York Times polls from the Roper scrape by study name; see
# data/roper scrape/layouts/README.txt for what is verified and how.
#
#   d <- read_cbsnyt92("cbsnyt1992-oct")                 # one column per layout row, named by its var (q1, q13a, ...)
#   d <- read_cbsnyt92("cbsnyt1992-oct", label = TRUE)   # value labels attached (haven_labelled)
#   cbsnyt92_layout("cbsnyt1992-oct")                    # the layout: var, name, card, col, width, question, codes
#   check_cbsnyt92_layout("cbsnyt1992-oct")              # codes in the data that the layout doesn't list
#
# Most of these polls are on Roper only as a .dat plus a scanned questionnaire whose card/column positions are written
# in by hand ([1/30] = card 1, column 30). Every .dat has three 80-column cards per respondent, in order, with the card
# number in column 1 and the respondent ID in columns 2-6 (checked: IDs agree across the three cards for every case).
# The cards are joined into one 240-column record, so card 2 column 5 is logical column 85. Weight: card 3, columns
# 49-54, xxx.xxx (sums to n; May leaves 386 cases unweighted). The studies Roper ships as SPSS portable files are
# read from those instead.

library(tidyverse)
library(haven)

roper_dir <- "data/roper scrape"

cbsnyt92_studies <- tribble(
  ~study,                  ~dir,                   ~file,
  "cbsnyt1992-jan",        "31091387_1992-01-06",  "JAN92A.dat",
  "cbsnyt1992-janrecruit", "31090762_1992-01-14",  "c92jan92b.por",     # CBS only
  "cbsnyt1992-sotu",       "31091388_1992-01-22",  "Jan92c.dat",
  "cbsnyt1992-feb",        "31091383_1992-02-19",  "FEB92A.dat",
  "cbsnyt1992-feb2",       "31091384_1992-02-26",  "FEB92B.dat",
  "cbsnyt1992-mar",        "31091392_1992-03-26",  "MAR92A.dat",
  "cbsnyt1992-apr",        "31091379_1992-04-20",  "APR92A.dat",
  "cbsnyt1992-may",        "31091393_1992-05-06",  "MAY92A.dat",
  "cbsnyt1992-may2",       "31091394_1992-05-27",  "31091394.por",
  "cbsnyt1992-jun",        "31091391_1992-06-17",  "JUN92A.dat",
  "cbsnyt1992-jul",        "31091389_1992-07-08",  "31091389.por",
  "cbsnyt1992-jul2",       "31090763_1992-07-14",  "c92july92b.por",    # CBS only
  "cbsnyt1992-jul3",       "31091390_1992-07-16",  "JULY92C.dat",
  "cbsnyt1992-aug",        "31091380_1992-08-11",  "AUG92A.dat",
  "cbsnyt1992-aug2",       "31090760_1992-08-18",  "c92aug92b.por",     # CBS only
  "cbsnyt1992-aug3",       "31091381_1992-08-20",  "AUG92C.dat",
  "cbsnyt1992-sep",        "31091399_1992-09-09",  "SEPT92A.dat",
  "cbsnyt1992-sep2",       "31090765_1992-09-22",  "c92sept92b.por",    # CBS only
  "cbsnyt1992-oct",        "31091395_1992-10-02",  "OCT92A.dat",        # plus callbacks of debate viewers
  "cbsnyt1992-debate",     "31091382_1992-10-12",  "DEB92B.dat",
  "cbsnyt1992-oct2",       "31090764_1992-10-16",  "c92oct92b.por",     # CBS only
  "cbsnyt1992-oct3",       "31091396_1992-10-21",  "OCT92C.dat",
  "cbsnyt1992-track",      "31091397_1992-10-27",  "OCT92D.dat"         # pre-election tracking, Oct 27 - Nov 1
)

cbsnyt92_layout <- function(study) {
  f <- file.path(roper_dir, "layouts", str_c(study, ".csv"))
  if (!file.exists(f)) stop(study, ": no layout (see data/roper scrape/layouts/README.txt)")
  read_csv(f, col_types = "cciiicc") |>
    mutate(loc = (card - 1) * 80 + col)
}

cbsnyt92_records <- function(study) {
  s <- cbsnyt92_studies[cbsnyt92_studies$study == study, ]
  x <- read_lines(file.path(roper_dir, s$dir, s$file)) |> str_remove("\r$")
  m <- matrix(str_pad(x, 80, "right"), ncol = 3, byrow = TRUE)
  stopifnot(all(str_sub(m[, 1], 1, 1) == "1"), all(str_sub(m[, 3], 1, 1) == "3"))
  str_c(m[, 1], m[, 2], m[, 3])
}

read_cbsnyt92 <- function(study, label = FALSE) {
  s <- cbsnyt92_studies[cbsnyt92_studies$study == study, ]
  if (str_detect(s$file, "\\.por$")) {
    d <- read_por(file.path(roper_dir, s$dir, s$file)) |> rename_with(str_to_lower)
    return(if (label) d else zap_labels(d))
  }
  lay <- cbsnyt92_layout(study)
  rec <- cbsnyt92_records(study)
  d <- map2(lay$loc, lay$width, \(l, w) {
    v <- str_trim(str_sub(rec, l, l + w - 1))
    # From August on, "Before 1982" in the years-voted/registered items (card 2) is a lone 11-row punch, which comes
    # through as "-"; read it as 10 so it isn't lost as a blank
    if (w == 1) v <- if_else(v == "-", "10", v)
    suppressWarnings(as.numeric(v))
  }) |>
    set_names(lay$var) |>
    as_tibble() |>
    mutate(id = as.numeric(str_sub(rec, 2, 6)),
           weight = as.numeric(str_sub(rec, 160 + 49, 160 + 54)) / 1000,
           .before = 1)
  if (label) {
    for (i in seq_len(nrow(lay))) {
      if (is.na(lay$codes[i])) next
      kv <- str_split_1(lay$codes[i], "; ")
      code <- suppressWarnings(as.numeric(str_extract(kv, "^-?[0-9]+")))
      ok <- !is.na(code) & !duplicated(code)
      d[[lay$var[i]]] <- labelled(d[[lay$var[i]]], labels = set_names(code[ok], str_remove(kv[ok], "^-?[0-9]+=")),
                                  label = lay$name[i])
    }
  }
  d
}

# For each coded item: values in the data the layout doesn't list (blank = not asked, shown as NA), and how many
# cases have them. A good layout leaves only blanks and the odd stray punch.
check_cbsnyt92_layout <- function(study) {
  lay <- cbsnyt92_layout(study) |> filter(!is.na(codes))
  d <- read_cbsnyt92(study)
  map(seq_len(nrow(lay)), \(i) {
    listed <- str_split_1(lay$codes[i], "; ") |> str_extract("^-?[0-9]+") |> as.numeric()
    x <- d[[lay$var[i]]]
    tibble(var = lay$var[i], card = lay$card[i], col = lay$col[i], n_blank = sum(is.na(x)),
           unlisted = list(sort(table(x[!is.na(x) & !x %in% listed]), decreasing = TRUE)))
  }) |>
    list_rbind() |>
    mutate(n_unlisted = map_int(unlisted, sum),
           unlisted = map_chr(unlisted, \(t) str_c(names(t), ":", t, collapse = " ")))
}
