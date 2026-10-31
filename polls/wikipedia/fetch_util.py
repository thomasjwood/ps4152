"""Fetch a Wikipedia page's rendered HTML via the MediaWiki API, caching it in raw/."""
import os, requests
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = {"User-Agent": "OSU-PS4152-course-data/1.0 (wood.1080@osu.edu)"}
os.makedirs(RAW, exist_ok=True)

def wiki_html(title, refresh=False):
    fn = os.path.join(RAW, title.replace("/", "_").replace(" ", "_") + ".html")
    if refresh or not os.path.exists(fn):
        r = requests.get("https://en.wikipedia.org/w/api.php",
                         params={"action": "parse", "page": title, "prop": "text",
                                 "format": "json", "redirects": 1, "formatversion": 2},
                         headers=UA, timeout=120)
        r.raise_for_status()
        j = r.json()
        if "error" in j:
            raise KeyError(title)
        open(fn, "w", encoding="utf-8").write(j["parse"]["text"])
    return open(fn, encoding="utf-8").read()

def wiki_url(title):
    return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
