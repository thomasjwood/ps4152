# Combine every presidential general-election poll database we have into two files, one row per poll question
# that includes both eventual major-party nominees:
#   presidential_polls_national_1948-2024.csv
#   presidential_polls_state_2012-2024.csv
# Run from the polls/ folder. Inputs are in sources/ and wikipedia/ (see README.md for where each came from).
# Duplicates across sources (the same poll in Wikipedia, RCP and Pollster, say) are collapsed to one row.

library(tidyverse)

nominees <- tribble(
  ~cycle, ~dem, ~rep,
  1948, "Truman", "Dewey", 1952, "Stevenson", "Eisenhower", 1956, "Stevenson", "Eisenhower",
  1960, "Kennedy", "Nixon", 1964, "Johnson", "Goldwater", 1968, "Humphrey", "Nixon", 1972, "McGovern", "Nixon",
  1976, "Carter", "Ford", 1980, "Carter", "Reagan", 1984, "Mondale", "Reagan", 1988, "Dukakis", "Bush",
  1992, "Clinton", "Bush", 1996, "Clinton", "Dole", 2000, "Gore", "Bush", 2004, "Kerry", "Bush",
  2008, "Obama", "McCain", 2012, "Obama", "Romney", 2016, "Clinton", "Trump", 2020, "Biden", "Trump",
  2024, "Harris", "Trump"
)
biden_out <- as.Date("2024-07-21")   # Biden-Trump is the 2024 nominee matchup for polls ending before this

states <- tibble(state = c(state.name, "District of Columbia"), state_abb = c(state.abb, "DC"))

pop_code <- \(x) {
  x <- str_to_lower(coalesce(x, ""))
  case_when(str_detect(x, "^lv|likely") ~ "LV", str_detect(x, "^rv|registered") ~ "RV",
            str_detect(x, "^a$|adult") ~ "A", str_detect(x, "^v$|^voters") ~ "V", TRUE ~ NA_character_)
}

# ---- Wikipedia (national, 1948-2024 less 1996/2004) ----
wiki <- read_csv("wikipedia/polls_nominees.csv", show_col_types = FALSE) |>
  filter(row_type == "poll", date_check == "ok") |>
  transmute(source = "Wikipedia", source_id = question_id, cycle, state = NA_character_, pollster,
            start_date, end_date, sample_size, population = pop_code(population), dem, rep, dem_pct, rep_pct,
            n_candidates, third_party_pct, url = coalesce(ref_url, source))

# ---- RCP (national, 2004-2016; two-way) ----
# Dates have no year ("M/D - M/D") and files run newest-first, so the year rolls back from the election year at
# each 1 -> 12 jump in start month (see lecture 2's 'buiilding a 2000-2024 presidential election polls.R').
rcp <- map_dfr(c(2004, 2008, 2012, 2016), \(cyc) {
  d <- read_csv(str_glue("sources/rcp_{cyc}.csv"), show_col_types = FALSE, locale = locale(encoding = "UTF-8"))
  nm <- names(d)
  dcol <- nm[str_detect(nm, "D\\)?\\.?$")][1]
  rcol <- nm[str_detect(nm, "R\\)?\\.?$")][1]
  d |>
    filter(!str_detect(pollster, "^(RCP Average|Final Results)$"),
           str_detect(date, "^\\s*\\d+/\\d+\\s*-\\s*\\d+/\\d+\\s*$")) |>
    mutate(sm = as.integer(str_extract(date, "^\\s*(\\d+)", 1)), sd = as.integer(str_extract(date, "^\\s*\\d+/(\\d+)", 1)),
           em = as.integer(str_extract(date, "-\\s*(\\d+)/", 1)), ed = as.integer(str_extract(date, "/(\\d+)\\s*$", 1)),
           year = cyc - cumsum(!is.na(lag(sm)) & sm - lag(sm) >= 11),
           end_date = make_date(if_else(em < sm, year + 1, year), em, ed),
           start_date = make_date(year, sm, sd),
           n = as.numeric(str_extract(sample, "\\d+")), pop = str_extract(sample, "[A-Z]+$")) |>
    transmute(source = "RCP", source_id = str_c("rcp", cyc, "-", row_number()), cycle = cyc, state = NA_character_,
              pollster = str_trim(pollster), start_date, end_date, sample_size = n, population = pop_code(pop),
              dem = nominees$dem[nominees$cycle == cyc], rep = nominees$rep[nominees$cycle == cyc],
              dem_pct = suppressWarnings(as.numeric(.data[[dcol]])), rep_pct = suppressWarnings(as.numeric(.data[[rcol]])),
              n_candidates = 2, third_party_pct = NA_real_, url = "https://www.realclearpolling.com")
}) |>
  filter(!is.na(dem_pct), !is.na(rep_pct))

# ---- pollingreport.com 2000 (national) ----
pr2000 <- read_csv("sources/pollingreport_2000_gore_bush.csv", show_col_types = FALSE) |>
  filter(!is.na(gore_pct), !is.na(bush_pct)) |>
  transmute(source = "pollingreport", source_id = str_c("pr2000-", row_number()), cycle = 2000, state = NA_character_,
            pollster = pollster_normalized, start_date = as.Date(field_start), end_date = as.Date(field_end),
            sample_size, population = pop_code(sample_type), dem = "Al Gore", rep = "George W. Bush",
            dem_pct = gore_pct, rep_pct = bush_pct, n_candidates = n_way,
            third_party_pct = na_if(rowSums(pick(buchanan_pct, nader_pct, browne_pct, phillips_pct, hagelin_pct), na.rm = TRUE), 0),
            url = "https://www.pollingreport.com")

# ---- pollingreport-style 2008 table (national) ----
# Dates: "11/3/2008", "11/2-3/08", "1/11-14/07", "10/31-11/2/08"
pr2008 <- read_csv("sources/pollingreport_2008_mccain_obama.csv", show_col_types = FALSE,
                   col_types = cols(.default = "c")) |>
  mutate(m = str_match(Dates, "^(\\d+)/(\\d+)(?:/(\\d+))?(?:-(?:(\\d+)/)?(\\d+)(?:/(\\d+))?)?$"),
         sm = as.integer(m[, 2]), sd = as.integer(m[, 3]),
         em = coalesce(as.integer(m[, 5]), sm), ed = coalesce(as.integer(m[, 6]), sd),
         yr = as.integer(coalesce(m[, 7], m[, 4])), yr = if_else(yr < 100, yr + 2000L, yr),
         end_date = make_date(yr, em, ed), start_date = make_date(if_else(sm > em, yr - 1L, yr), sm, sd),
         across(c(McCain, Obama, Barr, Nader), \(v) suppressWarnings(as.numeric(v)))) |>
  filter(!is.na(McCain), !is.na(Obama), !is.na(end_date)) |>
  transmute(source = "pollingreport", source_id = str_c("pr2008-", row_number()), cycle = 2008, state = NA_character_,
            pollster = Pollster, start_date, end_date, sample_size = as.numeric(str_extract(`N/Pop`, "\\d+")),
            population = pop_code(str_extract(`N/Pop`, "[A-Z]+$")), dem = "Barack Obama", rep = "John McCain",
            dem_pct = Obama, rep_pct = McCain, n_candidates = 2 + !is.na(Barr) + !is.na(Nader),
            third_party_pct = na_if(rowSums(cbind(Barr, Nader), na.rm = TRUE), 0), url = "https://www.pollingreport.com")

# ---- HuffPost Pollster 2012 (national + 17 states) ----
not_cand <- "other|undecided|refused|wouldn|not vot|none|no one|someone|don.?t know|neither|lean"
pollster12 <- readRDS("sources/huffpost_pollster_2012_races.rds") |>
  as_tibble() |>
  mutate(across(where(is.factor), as.character)) |>
  filter(str_detect(question, "President: Romney vs. Obama|General Election: Romney vs. Obama")) |>
  # a poll's two-way and multi-candidate versions share an id: the k-th 'Obama' row starts version k
  group_by(id, question, state, subpopulation, choice) |>
  mutate(version = row_number()) |>
  group_by(id, question, state, subpopulation, version) |>
  summarise(pollster = first(pollster), start_date = as.Date(first(start_date)), end_date = as.Date(first(end_date)),
            sample_size = first(observations), dem_pct = sum(value[choice == "Obama"]), rep_pct = sum(value[choice == "Romney"]),
            n_candidates = sum(!str_detect(str_to_lower(choice), not_cand)),
            third_party_pct = na_if(sum(value[!choice %in% c("Obama", "Romney") & !str_detect(str_to_lower(choice), not_cand)]), 0),
            url = first(source), .groups = "drop") |>
  filter(dem_pct > 0, rep_pct > 0) |>
  transmute(source = "HuffPost Pollster", source_id = str_c("hp", id, "-", version), cycle = 2012,
            state = if_else(state == "US", NA_character_, state), pollster, start_date, end_date, sample_size,
            population = pop_code(subpopulation), dem = "Barack Obama", rep = "Mitt Romney", dem_pct, rep_pct,
            n_candidates, third_party_pct, url)

# ---- HuffPost Pollster 2016 (national + 50 states and DC) ----
pollster16 <- readRDS("sources/huffpost_pollster_2016_president.rds") |>
  as_tibble() |>
  filter(!is.na(Clinton), !is.na(Trump)) |>
  transmute(source = "HuffPost Pollster", source_id = str_c("hp16-", poll_slug, "-", row_number()), cycle = 2016,
            state = if_else(as.character(slug) == "US", NA_character_, as.character(slug)), pollster = survey_house,
            start_date, end_date, sample_size = observations, population = pop_code(sample_subpopulation),
            dem = "Hillary Clinton", rep = "Donald Trump", dem_pct = Clinton, rep_pct = Trump,
            n_candidates = 2 + (coalesce(Johnson, 0) > 0) + (coalesce(McMullin, 0) > 0),
            third_party_pct = na_if(coalesce(Johnson, 0) + coalesce(McMullin, 0), 0),
            url = "https://elections.huffingtonpost.com/pollster")

# ---- 538 (national + state, 2020-2024) ----
f538 <- read_csv("sources/538_president_polls_historical_2020_2024.csv", show_col_types = FALSE) |>
  filter(stage == "general") |>
  mutate(start_date = mdy(start_date), end_date = mdy(end_date),
         surname = str_remove(candidate_name, ",? (Jr|Sr|III|II)\\.?$") |> word(-1),
         dem_nom = case_when(cycle == 2020 ~ "Biden", end_date < biden_out ~ "Biden", TRUE ~ "Harris"))
fte <- f538 |>
  group_by(question_id) |>
  filter(any(surname == dem_nom & party == "DEM"), any(surname == "Trump" & party == "REP")) |>
  summarise(poll_id = first(poll_id), cycle = first(cycle), state = first(state),
            pollster = first(coalesce(display_name, pollster)), start_date = first(start_date), end_date = first(end_date),
            sample_size = first(sample_size), population = pop_code(first(population)),
            dem = first(candidate_name[surname == dem_nom & party == "DEM"]), rep = first(candidate_name[surname == "Trump"]),
            dem_pct = first(pct[surname == dem_nom & party == "DEM"]), rep_pct = first(pct[surname == "Trump"]),
            n_candidates = n(), third_party_pct = na_if(sum(pct[!(surname %in% c(first(dem_nom), "Trump"))]), 0),
            grade_538 = first(numeric_grade), url = first(url), .groups = "drop") |>
  transmute(source = "538", source_id = str_c("538q", question_id), cycle, state, pollster, start_date, end_date,
            sample_size, population, dem, rep, dem_pct, rep_pct, n_candidates, third_party_pct, grade_538, url)

# ---- stack, standardize states, collapse duplicates ----
precedence <- c("538", "HuffPost Pollster", "Wikipedia", "RCP", "pollingreport")
stop_words <- c("poll", "polls", "news", "the", "university", "college", "research", "group", "inc", "and", "of",
                "survey", "center", "institute", "associates", "strategies", "opinion", "reports", "daily", "tracking")
tokens <- \(p) str_to_lower(p) |> str_replace_all("[^a-z0-9 ]", " ") |> str_split("\\s+") |>
  map(\(t) setdiff(t[nchar(t) > 1], stop_words))

all <- bind_rows(fte, pollster12, pollster16, wiki, rcp, pr2000, pr2008) |>
  mutate(state = case_when(is.na(state) ~ NA_character_,
                           nchar(state) == 2 ~ states$state[match(state, states$state_abb)],
                           TRUE ~ state),
         rank = match(source, precedence),
         dem = str_squish(dem), rep = str_squish(rep)) |>
  filter(!is.na(end_date), !is.na(dem_pct), !is.na(rep_pct)) |>
  # exact repeats inside one source (Pollster lists some polls twice)
  distinct(source, cycle, state, pollster, start_date, end_date, population, dem_pct, rep_pct, n_candidates,
           .keep_all = TRUE) |>
  arrange(cycle, state, rank, end_date) |>
  mutate(row = row_number(), tok = tokens(pollster))

# a row duplicates an earlier (higher-precedence) row from another source when cycle and state match, end dates are
# within a day, both percentages agree to rounding (538's 44.6 = Wikipedia's 45), and the pollster names share a word.
# Rows within one source are never collapsed: those are separate questions (LV and RV, two-way and full field).
key <- all |> mutate(geo = coalesce(state, "US")) |>
  select(row, cycle, geo, dem_pct, rep_pct, end_date, tok, source)
pairs <- key |>
  mutate(lo = end_date - 1, hi = end_date + 1) |>
  inner_join(key |> rename(row2 = row, dem2 = dem_pct, rep2 = rep_pct, end2 = end_date, tok2 = tok, source2 = source),
             by = join_by(cycle, geo, lo <= end2, hi >= end2), relationship = "many-to-many") |>
  filter(row2 < row, source != source2, abs(dem_pct - dem2) <= 0.5, abs(rep_pct - rep2) <= 0.5) |>
  filter(map2_lgl(tok, tok2, \(a, b) length(intersect(a, b)) > 0)) |>
  arrange(row, row2) |>
  distinct(row, .keep_all = TRUE)        # each duplicate joins its highest-precedence match
keep_of <- set_names(all$row, all$row)
for (i in seq_len(nrow(pairs))) {               # point each duplicate at its earliest (highest-precedence) match
  r <- pairs$row[i]; k <- pairs$row2[i]
  while (keep_of[[as.character(k)]] != k) k <- keep_of[[as.character(k)]]
  if (keep_of[[as.character(r)]] == r) keep_of[[as.character(r)]] <- k
}
all <- all |>
  mutate(keeper = unname(keep_of[as.character(row)]))
srcs <- all |>
  group_by(keeper) |>
  summarise(sources = str_c(unique(source[order(rank)]), collapse = "; "), n_sources = n_distinct(source),
            also_ids = str_c(source_id[row != keeper], collapse = "; "), .groups = "drop")

combined <- all |>
  filter(row == keeper) |>
  left_join(srcs, by = "keeper") |>
  mutate(also_ids = na_if(also_ids, ""),
         margin = dem_pct - rep_pct,
         # another source has the same pollster, end date, population and number of candidates but numbers more than
         # half a point apart: probably the same question reported differently. Flagged, not dropped.
         dk = str_c(cycle, coalesce(state, "US"), end_date, coalesce(population, "?"), n_candidates)) |>
  group_by(dk) |>
  mutate(possible_duplicate = map_lgl(row_number(), \(i) any(map_lgl(seq_len(n())[-i], \(j)
    !str_detect(sources[j], fixed(source[i])) && length(intersect(tok[[i]], tok[[j]])) > 0)))) |>
  ungroup() |>
  left_join(states |> rename(state_name = state), by = c("state" = "state_name")) |>
  transmute(cycle, state, state_abb, pollster, start_date, end_date, sample_size, population, dem, rep, dem_pct,
            rep_pct, margin, n_candidates, third_party_pct, grade_538, source, sources, n_sources, source_id,
            also_ids, possible_duplicate, url) |>
  arrange(cycle, state, end_date, pollster)

national <- combined |> filter(is.na(state)) |> select(-state, -state_abb)
state <- combined |> filter(!is.na(state))

write_csv(national, str_glue("presidential_polls_national_{min(national$cycle)}-{max(national$cycle)}.csv"), na = "")
write_csv(state, str_glue("presidential_polls_state_{min(state$cycle)}-{max(state$cycle)}.csv"), na = "")

# ---- report ----
cat("input rows by source:\n"); print(count(all, source))
cat("\nnational:", nrow(national), "polls\n")
print(national |> group_by(cycle) |> summarise(polls = n(), first = min(end_date), last = max(end_date),
                                               multi_source = sum(n_sources > 1), flagged = sum(possible_duplicate)), n = 30)
cat("\nstate:", nrow(state), "polls\n")
print(state |> group_by(cycle) |> summarise(polls = n(), states = n_distinct(state), first = min(end_date),
                                            last = max(end_date), multi_source = sum(n_sources > 1)))
