"""Finds CC0 stock photo candidates on Openverse and builds numbered contact sheets for picking."""
import json
import sys
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("/tmp/photo_candidates")
BAD = ("png", "clipart", "illustration", "drawing", "sketch", "vintage", "(1", "(c.", "painting", "engraving", "poster", "sticker", "vector", "icon", "pattern", "lithograph", "print", "card")

QUERIES = {
    "lawn-care": ["lawn mower", "mowing lawn", "gardener", "landscaper", "riding mower", "tractor", "lawn", "hedge trimming", "leaf blower"],
    "pressure-washing": ["pressure washer", "power washing", "washing driveway", "cleaning deck", "house exterior", "worker cleaning"],
    "hvac-plumbing": ["plumber", "technician", "air conditioner", "repairman", "handyman tools", "water heater", "pipes"],
    "roofing": ["roof", "roofer", "roofing", "construction worker", "shingles", "contractor"],
    "house-cleaning": ["cleaning", "maid", "mop", "kitchen clean", "cleaning lady", "vacuum"],
    "barber-salon": ["barber", "haircut", "hair salon", "barbershop"],
    "restaurant": ["barbecue", "bbq ribs", "smoked meat", "restaurant", "brisket", "burger"],
    "law-firm": ["lawyer", "attorney", "business meeting", "office handshake", "businesswoman", "law books"],
    "nursing-home": ["nurse elderly", "caregiver", "senior woman", "elderly care", "nursing home", "senior couple"],
    "home": ["small business owner", "shop owner", "laptop business", "contractor truck", "work truck"],
}


def search(q, source):
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "source": source, "license": "cc0", "page_size": 20, "aspect_ratio": "wide"}
    )
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "StakichWebsites/1.0"}), timeout=30) as r:
        return json.load(r).get("results", [])


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
        return Image.open(BytesIO(r.read())).convert("RGB")


def main(keys):
    OUT.mkdir(exist_ok=True)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
    for key in keys:
        seen, picks = set(), []
        for q in QUERIES[key]:
            for source in ("stocksnap", "rawpixel"):
                try:
                    results = search(q, source)
                except Exception as e:
                    print("search fail", q, source, e)
                    continue
                for r in results:
                    t = (r.get("title") or "").lower()
                    if r["id"] in seen or any(b in t for b in BAD):
                        continue
                    if source == "rawpixel" and not t.startswith("free"):
                        continue
                    seen.add(r["id"])
                    picks.append(r)
        picks = picks[:48]
        meta, thumbs = [], []
        for i, r in enumerate(picks):
            try:
                im = fetch(r["thumbnail"] if r.get("thumbnail") else r["url"])
            except Exception:
                try:
                    im = fetch(r["url"])
                except Exception:
                    continue
            im.thumbnail((360, 240))
            thumbs.append(im)
            meta.append({"n": len(thumbs), "id": r["id"], "title": r["title"], "url": r["url"], "source": r["source"], "landing": r["foreign_landing_url"], "w": r.get("width"), "h": r.get("height")})
        cols = 6
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 370, rows * 250), "white")
        d = ImageDraw.Draw(sheet)
        for i, im in enumerate(thumbs):
            x, y = (i % cols) * 370 + 5, (i // cols) * 250 + 5
            sheet.paste(im, (x, y))
            d.rectangle([x, y, x + 52, y + 36], fill="black")
            d.text((x + 6, y + 2), str(i + 1), fill="yellow", font=font)
        sheet.save(OUT / f"{key}.jpg", quality=80)
        (OUT / f"{key}.json").write_text(json.dumps(meta, indent=1))
        print(key, len(thumbs))


if __name__ == "__main__":
    main(sys.argv[1:] or list(QUERIES))
