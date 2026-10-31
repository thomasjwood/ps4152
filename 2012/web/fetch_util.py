"""Shared helpers: fetch a Wikipedia page's rendered HTML via the MediaWiki API and cache it in raw/."""
import json, os, requests
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = {"User-Agent": "OSU-PS4152-course-data/1.0 (wood.1080@osu.edu)"}
os.makedirs(RAW, exist_ok=True)

def wiki_html(title, refresh=False):
    fn = os.path.join(RAW, "wiki_" + title.replace("/", "_") + ".html")
    if refresh or not os.path.exists(fn):
        r = requests.get("https://en.wikipedia.org/w/api.php",
                         params={"action": "parse", "page": title, "prop": "text",
                                 "format": "json", "redirects": 1, "formatversion": 2},
                         headers=UA, timeout=60)
        r.raise_for_status()
        html = r.json()["parse"]["text"]
        open(fn, "w", encoding="utf-8").write(html)
    return open(fn, encoding="utf-8").read()

def wiki_url(title):
    return "https://en.wikipedia.org/wiki/" + title

def get(url, fn, refresh=False, binary=False):
    path = os.path.join(RAW, fn)
    if refresh or not os.path.exists(path):
        r = requests.get(url, headers=UA, timeout=120)
        r.raise_for_status()
        open(path, "wb").write(r.content)
    return path
