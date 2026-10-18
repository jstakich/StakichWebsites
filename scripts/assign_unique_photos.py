"""Give every site its own photos. Never reuse a photo twice, anywhere.

Run: python3 scripts/assign_unique_photos.py
Check: python3 scripts/assign_unique_photos.py --check

Uses Unsplash lite keywords (already unzipped at /tmp/unsplash-lite) plus
any leftover files in examples/img/subjects that are not already on a site.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "examples" / "img"
PREVIEW = ROOT / "preview"
BATCH = Path(__file__).with_name("previews_batch.json")
UNSPLASH = Path("/tmp/unsplash-lite")
CACHE = Path("/tmp/unphotos")
SKIP_NAMES = {"logo.png", "logo.jpg", "logo.jpeg", "logo.webp", "logo.svg"}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_oct18_previews import NAMES, LEADS, slug_of, trade_of  # noqa: E402

SLOTS = (
    ["hero.jpg", "about.jpg"]
    + [f"svc{i}.jpg" for i in range(1, 7)]
    + [f"work{i}.jpg" for i in range(1, 4)]
    + [f"blog{i}.jpg" for i in range(1, 4)]
)

# Preferred Unsplash keywords per (trade, filename). First list that still
# has an unused photo wins. Keep these tight so a vinyl-fence post never
# gets an interior-paint shot.
POOLS = {
    "plumbing": {
        "hero.jpg": [["plumbing", "bathroom"], ["sink"], ["pipe"], ["shower"], ["kitchen"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["pipe"], ["plumbing"], ["sink"], ["wrench"], ["basement"]],
        "svc2.jpg": [["drain"], ["sink"], ["plumbing"], ["laundry"], ["tile"]],
        "svc3.jpg": [["plumbing"], ["bathroom"], ["pipe"], ["basement"], ["laundry"]],
        "svc4.jpg": [["pipe"], ["drain"], ["plumbing"], ["basement"], ["wrench"]],
        "svc5.jpg": [["toilet"], ["bathroom"], ["bathtub"], ["shower"], ["tile"]],
        "svc6.jpg": [["plumbing"], ["pipe"], ["bathroom"], ["kitchen"], ["tile"]],
        "work1.jpg": [["sink"], ["pipe"], ["plumbing"], ["kitchen"], ["wrench"]],
        "work2.jpg": [["plumbing"], ["bathroom"], ["basement"], ["laundry"]],
        "work3.jpg": [["toilet"], ["bathroom"], ["bathtub"], ["shower"]],
        "blog1.jpg": [["pipe"], ["leak"], ["plumbing"], ["wrench"], ["basement"]],
        "blog2.jpg": [["bathroom"], ["plumbing"], ["laundry"], ["tile"]],
        "blog3.jpg": [["drain"], ["sink"], ["laundry"], ["tile"]],
    },
    "pest": {
        "hero.jpg": [["insect"], ["ant"], ["spider"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["ant"], ["insect"]],
        "svc2.jpg": [["termite"], ["insect"]],
        "svc3.jpg": [["rodent"], ["mouse"], ["rat"]],
        "svc4.jpg": [["mosquito"], ["insect"]],
        "svc5.jpg": [["bug"], ["insect"]],
        "svc6.jpg": [["ant"], ["insect"]],
        "work1.jpg": [["ant"], ["insect"]],
        "work2.jpg": [["rodent"], ["mouse"]],
        "work3.jpg": [["mosquito"], ["insect"]],
        "blog1.jpg": [["insect"], ["ant"]],
        "blog2.jpg": [["ant"], ["insect"]],
        "blog3.jpg": [["insect"]],
    },
    "roofing": {
        "hero.jpg": [["roof"], ["gutter"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["roof"], ["gutter"]],
        "svc2.jpg": [["roof"]],
        "svc3.jpg": [["hail"], ["roof"]],
        "svc4.jpg": [["gutter"], ["roof"]],
        "svc5.jpg": [["roof"]],
        "svc6.jpg": [["roof"], ["hail"]],
        "work1.jpg": [["roof"]],
        "work2.jpg": [["roof"], ["gutter"]],
        "work3.jpg": [["hail"], ["roof"]],
        "blog1.jpg": [["hail"], ["roof"]],
        "blog2.jpg": [["roof"]],
        "blog3.jpg": [["gutter"], ["roof"]],
    },
    "electric": {
        "hero.jpg": [["wire"], ["construction"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["wire"], ["construction"]],
        "svc2.jpg": [["wire"]],
        "svc3.jpg": [["construction"], ["wire"]],
        "svc4.jpg": [["wire"]],
        "svc5.jpg": [["construction"]],
        "svc6.jpg": [["wire"], ["construction"]],
        "work1.jpg": [["wire"]],
        "work2.jpg": [["construction"]],
        "work3.jpg": [["wire"]],
        "blog1.jpg": [["wire"]],
        "blog2.jpg": [["construction"]],
        "blog3.jpg": [["wire"]],
    },
    "fence": {
        "hero.jpg": [["fence"], ["gate"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["fence"]],
        "svc2.jpg": [["fence"], ["gate"]],
        "svc3.jpg": [["fence"]],
        "svc4.jpg": [["gate"], ["fence"]],
        "svc5.jpg": [["fence"]],
        "svc6.jpg": [["fence"]],
        "work1.jpg": [["fence"]],
        "work2.jpg": [["fence"]],
        "work3.jpg": [["gate"], ["fence"]],
        "blog1.jpg": [["fence"]],
        "blog2.jpg": [["fence"]],
        "blog3.jpg": [["fence"], ["gate"]],
    },
    "wash": {
        "hero.jpg": [["siding"], ["deck"], ["driveway"], ["brick"], ["house"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["siding"], ["deck"], ["brick"], ["house"]],
        "svc2.jpg": [["driveway"], ["concrete"], ["brick"]],
        "svc3.jpg": [["siding"], ["brick"], ["house"]],
        "svc4.jpg": [["deck"], ["wood"]],
        "svc5.jpg": [["fence"], ["siding"], ["brick"]],
        "svc6.jpg": [["siding"], ["deck"], ["house"]],
        "work1.jpg": [["siding"], ["brick"], ["house"]],
        "work2.jpg": [["driveway"], ["concrete"], ["brick"]],
        "work3.jpg": [["deck"], ["wood"]],
        "blog1.jpg": [["siding"], ["house"], ["brick"]],
        "blog2.jpg": [["siding"], ["deck"], ["house"]],
        "blog3.jpg": [["driveway"], ["concrete"], ["brick"]],
    },
    "lawn": {
        "hero.jpg": [["lawn"], ["grass"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["lawn"], ["grass"]],
        "svc2.jpg": [["hedge"], ["garden"]],
        "svc3.jpg": [["garden"], ["hedge"]],
        "svc4.jpg": [["lawn"]],
        "svc5.jpg": [["hedge"], ["garden"]],
        "svc6.jpg": [["lawn"], ["grass"]],
        "work1.jpg": [["lawn"]],
        "work2.jpg": [["hedge"], ["garden"]],
        "work3.jpg": [["lawn"], ["garden"]],
        "blog1.jpg": [["lawn"]],
        "blog2.jpg": [["garden"]],
        "blog3.jpg": [["lawn"], ["grass"]],
    },
    "tree": {
        "hero.jpg": [["tree"], ["stump"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["tree"], ["logging"]],
        "svc2.jpg": [["tree"]],
        "svc3.jpg": [["stump"], ["tree"]],
        "svc4.jpg": [["tree"]],
        "svc5.jpg": [["logging"], ["tree"]],
        "svc6.jpg": [["tree"]],
        "work1.jpg": [["tree"]],
        "work2.jpg": [["tree"]],
        "work3.jpg": [["stump"], ["tree"]],
        "blog1.jpg": [["tree"]],
        "blog2.jpg": [["stump"], ["tree"]],
        "blog3.jpg": [["tree"]],
    },
    "concrete": {
        "hero.jpg": [["concrete"], ["driveway"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["concrete"], ["driveway"]],
        "svc2.jpg": [["concrete"]],
        "svc3.jpg": [["concrete"]],
        "svc4.jpg": [["driveway"], ["concrete"]],
        "svc5.jpg": [["concrete"]],
        "svc6.jpg": [["concrete"]],
        "work1.jpg": [["concrete"], ["driveway"]],
        "work2.jpg": [["concrete"]],
        "work3.jpg": [["driveway"], ["concrete"]],
        "blog1.jpg": [["concrete"]],
        "blog2.jpg": [["concrete"]],
        "blog3.jpg": [["concrete"]],
    },
    "paint": {
        "hero.jpg": [["paint"], ["brush"], ["siding"], ["wall"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["paint"], ["brush"], ["wall"]],
        "svc2.jpg": [["siding"], ["paint"], ["brick"], ["house"]],
        "svc3.jpg": [["brush"], ["paint"], ["wall"]],
        "svc4.jpg": [["deck"], ["paint"], ["wood"]],
        "svc5.jpg": [["paint"], ["brush"], ["wall"]],
        "svc6.jpg": [["siding"], ["paint"], ["brick"]],
        "work1.jpg": [["paint"], ["brush"], ["wall"]],
        "work2.jpg": [["siding"], ["paint"], ["house"]],
        "work3.jpg": [["brush"], ["paint"], ["wall"]],
        "blog1.jpg": [["brush"], ["paint"], ["wall"]],
        "blog2.jpg": [["siding"], ["paint"], ["house"], ["brick"]],
        "blog3.jpg": [["paint"], ["wall"], ["brush"]],
    },
    "handyman": {
        "hero.jpg": [["hammer"], ["construction"], ["tools"]],
        "about.jpg": [["worker"], ["construction"], ["man"]],
        "svc1.jpg": [["construction"], ["hammer"]],
        "svc2.jpg": [["deck"], ["hammer"]],
        "svc3.jpg": [["construction"]],
        "svc4.jpg": [["paint"], ["brush"]],
        "svc5.jpg": [["hammer"], ["construction"]],
        "svc6.jpg": [["deck"], ["construction"]],
        "work1.jpg": [["construction"]],
        "work2.jpg": [["deck"]],
        "work3.jpg": [["wire"], ["construction"]],
        "blog1.jpg": [["hammer"], ["construction"]],
        "blog2.jpg": [["construction"]],
        "blog3.jpg": [["deck"], ["hammer"]],
    },
    "cleaning": {
        "s1.jpg": [["kitchen"], ["bathroom"], ["laundry"]],
        "s2.jpg": [["bathroom"], ["laundry"], ["interior"]],
        "s3.jpg": [["kitchen"], ["laundry"]],
        "s4.jpg": [["bathroom"], ["kitchen"], ["interior"]],
        "s5.jpg": [["kitchen"], ["bathroom"], ["laundry"], ["interior"]],
    },
    "barber": {
        "s1.jpg": [["hair"], ["portrait"]],
        "s2.jpg": [["hair"], ["portrait"]],
    },
}

BAN = {
    "butterfly", "flower", "flowers", "art", "canvas", "gallery", "museum",
    "abstract", "statue", "sculpture", "fashion", "model", "wedding",
    "cat", "dog", "puppy", "kitten", "food", "dessert", "beach sunset",
}


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def is_photo(p: Path) -> bool:
    return (
        p.is_file()
        and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        and p.name.lower() not in SKIP_NAMES
        and p.stat().st_size > 2000
    )


def iter_site_photos():
    for d in IMG.iterdir():
        if not d.is_dir() or d.name in ("subjects", "owner-logos", "assigned", "unique"):
            continue
        for p in d.iterdir():
            if is_photo(p):
                yield f"examples/{d.name}", p
    for d in PREVIEW.iterdir():
        if not d.is_dir():
            continue
        img = d / "img"
        if not img.is_dir():
            continue
        for p in img.iterdir():
            if is_photo(p):
                yield f"preview/{d.name}", p


def check():
    by_hash = defaultdict(list)
    intra = defaultdict(lambda: defaultdict(list))
    for site, p in iter_site_photos():
        h = md5(p)
        by_hash[h].append(f"{site}/{p.name}")
        intra[site][h].append(p.name)
    bad_intra = []
    for site, hs in intra.items():
        for h, names in hs.items():
            if len(names) > 1:
                bad_intra.append((site, names))
    bad_cross = []
    for h, files in by_hash.items():
        sites = {f.rsplit("/", 1)[0] for f in files}
        if len(sites) > 1:
            bad_cross.append(files)
    print(f"intra-site repeats: {len(bad_intra)}")
    for site, names in bad_intra[:30]:
        print(" ", site, names)
    print(f"cross-site repeats: {len(bad_cross)}")
    for files in bad_cross[:30]:
        print(" ", files)
    empty = empty_slot_files()
    print(f"empty slots: {len(empty)}")
    for p in empty[:20]:
        print(" ", p)
    if bad_intra or bad_cross or empty:
        return 1
    print("all photos unique")
    return 0


def load_keywords():
    kw_photos = defaultdict(set)
    photo_kws = defaultdict(set)
    path = UNSPLASH / "keywords.tsv000"
    if not path.exists():
        raise SystemExit("missing /tmp/unsplash-lite/keywords.tsv000")
    with path.open() as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            pid, kw = parts[0], parts[1].lower().strip()
            photo_kws[pid].add(kw)
            kw_photos[kw].add(pid)
    urls = {}
    with (UNSPLASH / "photos.tsv000").open() as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            urls[parts[0]] = parts[2]
    banned = set()
    for b in BAN:
        banned |= kw_photos.get(b, set())
    return kw_photos, photo_kws, urls, banned


def download(pid: str, url: str, dest: Path) -> Path | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 4000:
        return dest
    full = url + "?w=1400&q=80&fit=crop"
    req = urllib.request.Request(full, headers={"User-Agent": "StakichWebsites/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
    except Exception as e:
        print("dl fail", pid, e)
        return None
    if len(data) < 4000:
        return None
    dest.write_bytes(data)
    try:
        im = Image.open(dest)
        im.verify()
    except Exception:
        dest.unlink(missing_ok=True)
        return None
    return dest


def batch_slugs():
    rows = []
    with LEADS.open() as f:
        import csv
        for row in csv.DictReader(f, delimiter="\t"):
            if row["Business"] in NAMES:
                rows.append(row)
    out = []
    for row in rows:
        name = row["Business"]
        slug = slug_of(row["complete message to send"])
        if name == "Goodwin Fences and Decks":
            slug = "goodwin-fences-and-decks"
        out.append((slug, trade_of(row["Type"], name)))
    return out


def pick(kw_photos, photo_kws, banned, used_ids, groups):
    for kws in groups:
        for kw in kws:
            for pid in sorted(kw_photos.get(kw, ())):
                if pid in used_ids or pid in banned:
                    continue
                if photo_kws[pid] & BAN:
                    continue
                return pid
    return None


def jpeg_save(src: Path, dest: Path):
    im = Image.open(src).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=86, optimize=True)


def dup_targets():
    """Keep one copy of each unique photo; replace every extra copy."""
    by_hash = defaultdict(list)
    for site, p in iter_site_photos():
        by_hash[md5(p)].append((site, p))
    used_hashes = set()
    targets = []
    for h, files in by_hash.items():
        files_sorted = sorted(
            files,
            key=lambda x: (0 if x[0].startswith("examples/") else 1, x[1].as_posix()),
        )
        used_hashes.add(h)
        if len(files_sorted) == 1:
            continue
        for _site, p in files_sorted[1:]:
            targets.append(p)
    return targets, used_hashes


def trade_for_path(p: Path, slug_trade: dict) -> str:
    slug = p.parent.parent.name if p.parent.name == "img" else p.parent.name
    if slug in slug_trade:
        return slug_trade[slug]
    if slug == "mommadees-cleaning":
        return "cleaning"
    if slug == "snip-n-time":
        return "barber"
    raise SystemExit(f"no trade for {p}")


def empty_slot_files():
    out = []
    slug_trade = dict(batch_slugs())
    for slug, _trade in slug_trade.items():
        d = PREVIEW / slug / "img"
        for name in SLOTS:
            p = d / name
            if not p.exists() or p.stat().st_size < 2000:
                out.append(p)
    extras = [
        PREVIEW / "mommadees-cleaning" / "img" / "s5.jpg",
        PREVIEW / "mommadees-cleaning" / "img" / "s2.jpg",
        PREVIEW / "snip-n-time" / "img" / "s1.jpg",
        PREVIEW / "snip-n-time" / "img" / "s2.jpg",
    ]
    for p in extras:
        if not p.exists() or p.stat().st_size < 2000:
            out.append(p)
    return out


def assign():
    kw_photos, photo_kws, urls, banned = load_keywords()
    CACHE.mkdir(parents=True, exist_ok=True)
    used_ids = {p.stem for p in CACHE.glob("*.jpg")}
    targets, used_hashes = dup_targets()
    targets = list(dict.fromkeys(list(targets) + empty_slot_files()))
    slug_trade = dict(batch_slugs())
    print(f"files to fill: {len(targets)}")

    ok = 0
    missing = []
    fail = []
    for dest in targets:
        trade = trade_for_path(dest, slug_trade)
        groups = POOLS.get(trade, {}).get(dest.name) or [["house"], ["interior"], ["construction"], ["workshop"]]
        placed = False
        for _try in range(40):
            pid = pick(kw_photos, photo_kws, banned, used_ids, groups)
            if not pid:
                break
            used_ids.add(pid)
            path = download(pid, urls[pid], CACHE / f"{pid}.jpg")
            if not path:
                fail.append((dest, pid))
                continue
            tmp = dest.with_suffix(".tmp.jpg")
            jpeg_save(path, tmp)
            h = md5(tmp)
            if h in used_hashes:
                tmp.unlink(missing_ok=True)
                continue
            tmp.replace(dest)
            used_hashes.add(h)
            ok += 1
            placed = True
            break
        if not placed:
            missing.append((trade, dest.name, dest))
            print("  NEED", trade, dest.name)

    print(f"wrote {ok}, still missing {len(missing)}")
    leftover = Path("/tmp/unique_photo_missing.json")
    leftover.write_text(json.dumps({
        "missing": [[t, s, str(d)] for t, s, d in missing],
        "fail": [[str(d), p] for d, p in fail],
    }, indent=2))
    return missing, fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        sys.exit(check())
    missing, fail = assign()
    rc = check()
    if missing or fail:
        sys.exit(2)
    sys.exit(rc)


if __name__ == "__main__":
    main()
