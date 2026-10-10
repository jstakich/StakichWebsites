"""Tell Bing/IndexNow about new or updated pages. Usage: python3 scripts/indexnow.py [--all | /blog/x.html ...]"""
import json
import sys
import urllib.request
from pathlib import Path
import re

SITE = "https://stakichwebsites.com"
KEY = "e084dacdfecf5945fd187049614c07b7"
ROOT = Path(__file__).resolve().parent.parent

args = sys.argv[1:]
if not args or args == ["--all"]:
    urls = re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text())
else:
    urls = [SITE + "/" + a.lstrip("/") for a in args]

body = json.dumps({"host": "stakichwebsites.com", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req) as r:
    print(r.status, f"submitted {len(urls)} urls")
