#!/usr/bin/env python3
"""Save Google reviews into google-reviews.json. Same setup as Stress Free Flow.

Google only returns the latest 5 reviews. The page reads the saved file.
It does not call Google on every visit.

Usage:
  GOOGLE_MAPS_API_KEY=your_key python3 scripts/fetch-google-reviews.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "google-reviews.json"
PLACE_ID = "ChIJ9TbnsvnvNGMRlP27w38acG4"
REVIEW_URL = "https://g.page/r/CZT9u8N_GnBuEBM/review"
MAPS_URL = "https://www.google.com/maps?cid=7957889677610712468"


def main() -> int:
    key = (os.environ.get("GOOGLE_MAPS_API_KEY") or os.environ.get("GOOGLE_PLACES_API_KEY") or "").strip()
    if not key:
        print("Set GOOGLE_MAPS_API_KEY (or GOOGLE_PLACES_API_KEY) and re-run.", file=sys.stderr)
        return 1

    params = urllib.parse.urlencode(
        {
            "place_id": PLACE_ID,
            "fields": "name,rating,user_ratings_total,reviews,url",
            "key": key,
        }
    )
    url = "https://maps.googleapis.com/maps/api/place/details/json?" + params
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    status = payload.get("status")
    if status != "OK":
        print(f"Places API error: {status} {payload.get('error_message', '')}", file=sys.stderr)
        return 1

    result = payload.get("result") or {}
    reviews = []
    for item in result.get("reviews") or []:
        reviews.append(
            {
                "author": item.get("author_name") or "Google reviewer",
                "rating": int(item.get("rating") or 0),
                "text": (item.get("text") or "").strip(),
                "relativeTime": item.get("relative_time_description") or "",
            }
        )

    data = {
        "placeId": PLACE_ID,
        "name": result.get("name") or "Stakich Websites",
        "rating": result.get("rating"),
        "userRatingsTotal": int(result.get("user_ratings_total") or 0),
        "updatedAt": date.today().isoformat(),
        "reviewUrl": REVIEW_URL,
        "mapsUrl": result.get("url") or MAPS_URL,
        "reviews": reviews,
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    written = sum(1 for review in reviews if review["text"])
    print(
        f"Wrote {OUT.name}: rating={data['rating']} total={data['userRatingsTotal']} "
        f"reviews={len(reviews)} with_words={written}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
