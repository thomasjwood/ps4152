"""Build fred_1988_1994.csv: FRED series for 1985-1996 (long format, like
lecture 13's fred_1947_2026.csv: date, value, series), plus derived series.
Downloads https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID> for each ID.
(File name kept as requested; the window is 1985-01 to 1996-12.)"""
import io, time
import pandas as pd, requests
import fetch_util as f

IDS = {"UNRATE": "Unemployment rate, %, monthly SA",
       "CPIAUCSL": "CPI-U all items, index 1982-84=100, monthly SA",
       "A229RX0": "Real disposable personal income per capita, chained 2017 $, monthly SAAR",
       "A191RL1Q225SBEA": "Real GDP growth, % change from preceding quarter, SAAR (quarterly)",
       "UMCSENT": "U. Michigan consumer sentiment, index 1966Q1=100 (monthly; pre-1978 quarterly)",
       "FEDFUNDS": "Effective federal funds rate, %, monthly",
       "USREC": "NBER recession indicator (1 = recession month)"}
out = []
for i in IDS:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={i}"
    for attempt in range(4):
        try:
            p = f.get(url, f"fred_{i}.csv", refresh=True)
            break
        except Exception as e:
            print(i, "retry", e); time.sleep(5)
    d = pd.read_csv(p)
    d.columns = ["date", "value"]
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values("date")
    if i == "CPIAUCSL":
        y = d.copy()
        y["value"] = (100 * (y.value / y.value.shift(12) - 1)).round(2)
        y["series"] = "CPI_YOY"; y["description"] = "CPI-U inflation, % change from 12 months earlier (computed)"
        y["source"] = url
        out.append(y)
    if i == "A229RX0":
        y = d.copy()
        y["value"] = (100 * (y.value / y.value.shift(12) - 1)).round(2)
        y["series"] = "A229RX0_YOY"; y["description"] = "Real disposable income per capita, % change from 12 months earlier (computed)"
        y["source"] = url
        out.append(y)
    d["series"] = i; d["description"] = IDS[i]; d["source"] = url
    out.append(d)
df = pd.concat(out)
df = df[(df.date >= "1985-01-01") & (df.date <= "1996-12-31")]
df["date"] = df.date.dt.date
df[["date", "value", "series", "description", "source"]].to_csv("fred_1988_1994.csv", index=False)
print(df.groupby("series").agg(n=("value", "size"), first=("date", "min"), last=("date", "max")))
rec = df[(df.series == "USREC") & (df.value == 1)]
print("USREC==1 months:", rec.date.min(), rec.date.max(), len(rec))
for s in ["UNRATE", "CPI_YOY", "FEDFUNDS", "UMCSENT"]:
    x = df[(df.series == s) & (df.date.astype(str).between("1989-01-01", "1993-01-31"))]
    print(s, "max", x.loc[x.value.idxmax(), ["date", "value"]].tolist(), "min", x.loc[x.value.idxmin(), ["date", "value"]].tolist())
x = df[(df.series == "UNRATE") & (df.date.astype(str).str[:7].isin(["1992-06", "1992-10", "1992-11", "1989-01", "1990-06"]))]
print(x[["date", "value"]])
