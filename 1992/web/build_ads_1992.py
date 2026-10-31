"""Build ads_1992.csv: the 1992 commercials in the Museum of the Moving Image's
Living Room Candidate archive (https://www.livingroomcandidate.org/commercials/1992).
For each ad page: title, candidate, sponsor, maker, original air date, and the
opening of the transcript (as a short description; the site has no separate
description field), plus the page and video URLs."""
import re, html, time
import pandas as pd
import fetch_util as f

BASE = "https://www.livingroomcandidate.org"
lst = open(f.get(BASE + "/commercials/1992", "lrc_1992.html"), encoding="utf-8", errors="replace").read()
slugs = list(dict.fromkeys(re.findall(r'href="/commercials/1992/([^"#]+)#(\d+)"', lst)))
videos = dict((i, v) for v, i in re.findall(r'href="#/video/([^"]+\.mp4)" data-id="(\d+)"', lst))
rows = []
for slug, did in slugs:
    p = f.get(f"{BASE}/commercials/1992/{slug}", f"lrc_1992_{slug}.html")
    s = open(p, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    t = re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", t))
    m = re.search(r'\n"([^\n]+?)," (\w+), 1992\n(.*?)\nclose\nCredits', t, flags=re.S)
    title, cand, transcript = (m.group(1), m.group(2), m.group(3).strip()) if m else (None, None, "")
    cr = re.search(r"Credits\n(.*?)From Museum", t, flags=re.S)
    credits = [x.strip() for x in cr.group(1).split("\n") if x.strip()] if cr else []
    sponsor = credits[1].rstrip(",") if len(credits) > 1 else None
    maker = next((c.replace("Maker: ", "") for c in credits if c.startswith("Maker:")), None)
    air = next((c.replace("Original air date: ", "") for c in credits if c.startswith("Original air date:")), None)
    desc = re.sub(r"\s+", " ", transcript)
    desc = desc[:240].rsplit(" ", 1)[0] + "..." if len(desc) > 240 else desc
    v = videos.get(did)
    rows.append(dict(title=title, candidate=cand,
                     party={"d": "D", "r": "R", "i": "I"}.get(v.split("-")[1], None) if v else None,
                     sponsor=sponsor, maker=maker, air_date=air, transcript_start=desc,
                     video_file=v, url=f"{BASE}/commercials/1992/{slug}", source=f"{BASE}/commercials/1992"))
    time.sleep(0.3)
d = pd.DataFrame(rows).sort_values(["candidate", "title"])
d.to_csv("ads_1992.csv", index=False)
print(d[["title", "candidate", "party", "air_date", "maker"]].to_string())
