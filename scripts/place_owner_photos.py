"""Place each shop's own Facebook photos. Matching slot first; leftovers on About.

Skip logos, holiday graphics, ads, blur, and review screenshots.
A file is used once. Re-encode JPEG so hashes stay unique.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FB = Path("/tmp/owner-fb")
BATCH = Path(__file__).with_name("previews_batch.json")
SRC = {
    "outhouse-plumbing": FB / "outhouse-plumbing",
    "eternity-fencing": FB / "eternity-fencing",
    "raschke-sons-electric": FB / "raschke-sons-electric",
    "happy-homes-pressure-washing": FB / "happy-homes-pressure-washing",
    "tennessee-stripes-lawn-care": FB / "tennessee-stripes-lawn-care",
    "southeast-concrete-construction": FB / "southeast-concrete-construction",
    "brandons-tree-service": FB / "brandons-tree-service",
    "all-home-plumbing": FB / "all-home-plumbing",
    "keith-hodge-plumbing": FB / "keith-hodge-plumbing",
    "chattanooga-roofing-contractors": FB / "chattanooga-roofing-contractors",
    "chris-spors-custom-homes": FB / "chris-spors-custom-homes",
    "no-limits-home-improvements": FB / "no-limits-home-improvements",
    "east-tennessee-exterminating": FB / "east-tennessee-exterminating",
}

# slot or extra-caption -> filename in that shop's FB folder
PLANS = {
    "outhouse-plumbing": {
        "hero": "p18.jpg",
        "about": "p48.jpg",
        "svc1": "p19.jpg",
        "svc2": "p41.jpg",
        "svc3": "p32.jpg",
        "svc4": "p3.jpg",
        "svc5": "p47.jpg",
        "svc6": "p4.jpg",
        "work1": ("p45.jpg", "Pipes opened in the wall"),
        "work2": ("p44.jpg", "Water heater service"),
        "work3": ("p67.jpg", "Toilet install"),
        "blog1": "p8.jpg",
        "blog2": "p84.jpg",
        "blog3": "p57.jpg",
        "extras": [
            ("p2.jpg", "Digging in for a new line"),
            ("p6.jpg", "The mini excavator on a water-line job"),
            ("p7.jpg", "A shower pan we set"),
            ("p9.jpg", "New water line in the trench"),
            ("p10.jpg", "Septic tank set"),
            ("p12.jpg", "Shower valve in a new bath"),
            ("p13.jpg", "Whole-house filter canisters"),
            ("p15.jpg", "Trench for a new water line"),
            ("p20.jpg", "New pipe in the ground"),
            ("p22.jpg", "Hose bib running after the repair"),
            ("p23.jpg", "Brass fitting on a new line"),
            ("p27.jpg", "Tub and tile in a bath we plumbed"),
            ("p28.jpg", "Vanity and toilet after the rough-in"),
            ("p30.jpg", "New vanity and toilet"),
            ("p31.jpg", "Kitchen sink after the install"),
            ("p39.jpg", "Water line in an open trench"),
            ("p50.jpg", "Vanity plumbing"),
            ("p52.jpg", "Work truck on a winter call"),
            ("p56.jpg", "Outdoor shower valve"),
            ("p68.jpg", "Well pump in the trench"),
            ("p72.jpg", "Valve box in the ground"),
        ],
    },
    "eternity-fencing": {
        "hero": "p14.jpg",
        "about": "p12.jpg",
        "svc1": "p13.jpg",
        "svc2": "p2.jpg",
        "svc3": "p23.jpg",
        "svc4": "p7.jpg",
        "svc5": "p3.jpg",
        "svc6": "p26.jpg",
        "work1": ("p21.jpg", "New wood privacy fence"),
        "work2": ("p34.jpg", "Vinyl privacy fence"),
        "work3": ("p30.jpg", "Posts set in concrete"),
        "blog1": "p9.jpg",
        "blog2": "p31.jpg",
        "blog3": "p28.jpg",
        "extras": [
            ("p5.jpg", "Chain-link gate for the dog"),
            ("p6.jpg", "Wood privacy fence around the yard"),
            ("p8.jpg", "Picket fence along the lot"),
            ("p10.jpg", "Wood and wire field fence"),
            ("p17.jpg", "Wood and wire along the drive"),
            ("p18.jpg", "Pasture fence"),
            ("p24.jpg", "Aluminum railing at the patio"),
            ("p25.jpg", "Black aluminum fence"),
            ("p27.jpg", "Black aluminum around the pool"),
            ("p32.jpg", "White vinyl with posts capped"),
            ("p33.jpg", "Aluminum fence at the pool"),
            ("p35.jpg", "Pool fence"),
            ("p36.jpg", "Aluminum fence at a pool"),
            ("p37.jpg", "Gate in an aluminum fence"),
            ("p40.jpg", "Wood privacy fence, long run"),
            ("p41.jpg", "Aluminum fence in a big yard"),
        ],
    },
    "raschke-sons-electric": {
        "hero": "p11.jpg",
        "about": "p3.jpg",
        "svc1": "p2.jpg",
        "svc2": "p15.jpg",
        "svc3": "p17.jpg",
        "svc4": "p20.jpg",
        "svc6": "p14.jpg",
        "work1": ("p16.jpg", "Open panel, breakers labeled"),
        "work2": ("p4.jpg", "New outlet install"),
        "work3": ("p18.jpg", "Light fixture swap"),
        "blog1": "p6.jpg",
        "blog2": "p5.jpg",
        "blog3": "p19.jpg",
        "extras": [
            ("p7.jpg", "Porch light we hung"),
            ("p8.jpg", "Exterior light on a metal roof"),
            ("p9.jpg", "Sconce on stone"),
            ("p10.jpg", "House we wired, lit at dusk"),
            ("p21.jpg", "Ceiling fan"),
            ("p22.jpg", "Vanity lights"),
            ("p23.jpg", "Outdoor wall light"),
            ("p25.jpg", "Sconce on a white house"),
            ("p26.jpg", "Chandelier in the dining room"),
            ("p27.jpg", "Pendant lights"),
            ("p28.jpg", "Finished house after the electrical"),
            ("p46.jpg", "The Raschke family"),
        ],
    },
    "happy-homes-pressure-washing": {
        "hero": "p16.jpg",
        "about": "p15.jpg",
        "svc1": "p21.jpg",
        "svc2": "p22.jpg",
        "svc3": "p19.jpg",
        "svc4": "p43.jpg",
        "svc5": "p41.jpg",
        "svc6": "p20.jpg",
        "work1": ("p12.jpg", "House wash on siding"),
        "work2": ("p24.jpg", "Driveway surface clean"),
        "work3": ("p44.jpg", "Deck wash"),
        "blog1": "p6.jpg",
        "blog2": "p4.jpg",
        "blog3": "p5.jpg",
        "extras": [
            ("p2.jpg", "Driveway before and after"),
            ("p8.jpg", "House and drive after a wash"),
            ("p9.jpg", "Barn and lot we washed"),
            ("p10.jpg", "Trailer on a barn job"),
            ("p11.jpg", "Trailer at the shop"),
            ("p17.jpg", "Truck and trailer on site"),
            ("p18.jpg", "Surface cleaner on a drive"),
            ("p23.jpg", "Pool deck after a wash"),
            ("p30.jpg", "Clean concrete walk"),
            ("p32.jpg", "Garage apron after a wash"),
            ("p33.jpg", "Drive after the wash"),
            ("p45.jpg", "Truck on a job"),
            ("p46.jpg", "Trailer behind the truck"),
        ],
    },
    "tennessee-stripes-lawn-care": {
        "hero": "p2.jpg",
        "about": "p25.jpg",
        "svc1": "p3.jpg",
        "svc2": "p44.jpg",
        "svc3": "p39.jpg",
        "svc4": "p46.jpg",
        "svc5": "p40.jpg",
        "svc6": "p20.jpg",
        "work1": ("p8.jpg", "Clean edge along the sidewalk"),
        "work2": ("p38.jpg", "Hedge trimming"),
        "work3": ("p13.jpg", "Fall cleanup before leaves mat down"),
        "blog1": "p4.jpg",
        "blog2": "p33.jpg",
        "blog3": "p47.jpg",
        "extras": [
            ("p5.jpg", "Striped lawn on a slope"),
            ("p6.jpg", "Front yard after a mow"),
            ("p7.jpg", "House lawn, striped"),
            ("p9.jpg", "Corner lot after a mow"),
            ("p10.jpg", "Fresh stripes on a front yard"),
            ("p23.jpg", "Lakeside lawn"),
            ("p24.jpg", "Lake house after a mow"),
            ("p26.jpg", "Hotel lawn we keep"),
            ("p30.jpg", "Beds and trees at a commercial lot"),
            ("p34.jpg", "Brick house after a mow"),
            ("p35.jpg", "Front walk and lawn"),
            ("p36.jpg", "Mulch beds at a brick home"),
            ("p41.jpg", "Open lawn after a cut"),
        ],
    },
    "southeast-concrete-construction": {
        "hero": "p16.jpg",
        "about": "p27.jpg",
        "svc1": "p14.jpg",
        "svc2": "p22.jpg",
        "svc3": "p41.jpg",
        "svc4": "p9.jpg",
        "svc5": "p24.jpg",
        "svc6": "p23.jpg",
        "work1": ("p7.jpg", "New driveway pour"),
        "work2": ("p19.jpg", "Patio slab, broom finish"),
        "work3": ("p3.jpg", "Old slab that needed to come out"),
        "blog1": "p28.jpg",
        "blog2": "p29.jpg",
        "blog3": "p33.jpg",
        "extras": [
            ("p8.jpg", "New pad at a shed"),
            ("p15.jpg", "Basketball pad"),
            ("p17.jpg", "Long driveway pour"),
            ("p20.jpg", "Patio off the house"),
            ("p25.jpg", "New drive at a house"),
            ("p26.jpg", "Shop floor we poured"),
            ("p30.jpg", "Commercial pad"),
            ("p31.jpg", "Drive at the shop"),
            ("p32.jpg", "Fresh slab"),
            ("p34.jpg", "Drive and parking"),
            ("p39.jpg", "Interior slab"),
            ("p40.jpg", "Walk to the porch"),
            ("p44.jpg", "The family"),
            ("p47.jpg", "Finished driveway"),
            ("p48.jpg", "Drive through the trees"),
        ],
    },
    "brandons-tree-service": {
        "hero": "p1.jpg",
        "about": "p27.jpg",
        "svc1": "p23.jpg",
        "svc2": "p8.jpg",
        "svc3": "p7.jpg",
        "svc4": "p17.jpg",
        "svc5": "p4.jpg",
        "svc6": "p6.jpg",
        "work1": ("p24.jpg", "Tree down next to the house"),
        "work2": ("p9.jpg", "Dead limbs off the roof line"),
        "work3": ("p25.jpg", "Cleanup after a take-down"),
        "blog1": "p26.jpg",
        "blog2": "p21.jpg",
        "blog3": "p15.jpg",
        "extras": [
            ("p5.jpg", "Cleanup beside the barn"),
            ("p10.jpg", "Lot after a removal"),
            ("p14.jpg", "Crew and trucks in the woods"),
            ("p16.jpg", "Trucks on a roadside job"),
            ("p18.jpg", "Storm damage at a brick house"),
            ("p19.jpg", "Tree on a house after a storm"),
            ("p20.jpg", "Inside after a tree hit the roof"),
            ("p22.jpg", "Ice on the lines after a storm"),
            ("p28.jpg", "Night job with the bucket truck"),
            ("p29.jpg", "House after a storm"),
            ("p30.jpg", "Night work on a hazard tree"),
            ("p31.jpg", "Crew after a job"),
            ("p38.jpg", "Take-down at a brick house"),
            ("p40.jpg", "Cleanup along the drive"),
        ],
    },
    "all-home-plumbing": {
        "hero": "p6.jpg",
        "about": "p5.jpg",
        "svc1": "p8.jpg",
        "svc2": "p2.jpg",
        "svc3": "p13.jpg",
        "svc4": "p47.jpg",
        "svc5": "p9.jpg",
        "work1": ("p16.jpg", "A leaking pipe under the sink"),
        "work2": ("p43.jpg", "Water heater service"),
        "work3": ("p23.jpg", "Faucet install"),
        "blog2": "p17.jpg",
        "blog3": "p15.jpg",
        "extras": [
            ("p3.jpg", "Plumber at the sink"),
            ("p10.jpg", "Working a drain"),
            ("p40.jpg", "Kitchen faucet running"),
        ],
    },
    "keith-hodge-plumbing": {
        "hero": "p7.jpg",
        "about": "p9.jpg",
        "svc1": "p21.jpg",
        "svc4": "p10.jpg",
        "extras": [
            ("p8.jpg", "Bath we finished"),
        ],
    },
    "chattanooga-roofing-contractors": {
        "hero": "p13.jpg",
        "about": "p21.jpg",
        "svc1": "p16.jpg",
        "svc2": "p15.jpg",
        "svc6": "p20.jpg",
        "work1": ("p14.jpg", "Tear-off and new shingles"),
        "work2": ("p6.jpg", "Walking the roof with the homeowner"),
        "blog1": "p25.jpg",
        "extras": [
            ("p3.jpg", "Deck before a remodel"),
            ("p5.jpg", "Deck we rebuilt"),
            ("p8.jpg", "Living room after a remodel"),
            ("p31.jpg", "The crew inside a finished room"),
            ("p32.jpg", "Kitchen after a remodel"),
            ("p45.jpg", "House after a new roof"),
            ("p48.jpg", "Framing on a remodel"),
        ],
    },
    "chris-spors-custom-homes": {
        "hero": "p15.jpg",
        "about": "p46.jpg",
        "svc1": "p24.jpg",
        "svc2": "p10.jpg",
        "svc3": "p28.jpg",
        "svc4": "p7.jpg",
        "svc5": "p8.jpg",
        "svc6": "p21.jpg",
        "work1": ("p25.jpg", "Drywall, ready for paint"),
        "work2": ("p22.jpg", "Deck on a new house"),
        "work3": ("p4.jpg", "New light and fan"),
        "blog1": "p17.jpg",
        "blog2": "p12.jpg",
        "blog3": "p6.jpg",
        "extras": [
            ("p2.jpg", "Tile shower"),
            ("p3.jpg", "Bath vanity"),
            ("p9.jpg", "Kitchen we built"),
            ("p11.jpg", "Stair rail"),
            ("p14.jpg", "Kitchen and living"),
            ("p16.jpg", "Crane on a house build"),
            ("p18.jpg", "House going up"),
            ("p19.jpg", "House under construction"),
            ("p20.jpg", "Wood ceiling in a new house"),
            ("p26.jpg", "Hall and French doors"),
            ("p30.jpg", "Tile shower, another bath"),
            ("p31.jpg", "Finished house"),
            ("p33.jpg", "Foundation walls"),
            ("p47.jpg", "Job-site sign"),
        ],
    },
    "no-limits-home-improvements": {
        "hero": "p8.jpg",
        "about": "p10.jpg",
        "svc1": "p9.jpg",
        "svc2": "p11.jpg",
        "svc3": "p35.jpg",
        "svc4": "p38.jpg",
        "svc5": "p42.jpg",
        "svc6": "p47.jpg",
        "work1": ("p34.jpg", "Drywall patch, ready for paint"),
        "work2": ("p17.jpg", "Deck repair"),
        "work3": ("p43.jpg", "New windows and trim"),
        "blog1": "p20.jpg",
        "blog2": "p36.jpg",
        "blog3": "p13.jpg",
        "extras": [
            ("p12.jpg", "New deck boards"),
            ("p14.jpg", "Covered deck framing"),
            ("p15.jpg", "Deck stairs"),
            ("p16.jpg", "New stair rail"),
            ("p18.jpg", "Deck stairs from above"),
            ("p19.jpg", "Upper deck"),
            ("p21.jpg", "Wood privacy fence and gate"),
            ("p25.jpg", "Fence we built"),
            ("p28.jpg", "Long run of wood fence"),
            ("p37.jpg", "Drywall patches in a corner"),
            ("p39.jpg", "Fence posts in"),
            ("p40.jpg", "Rail going in"),
            ("p41.jpg", "Deck rail"),
            ("p44.jpg", "New door"),
            ("p48.jpg", "Window in brick"),
        ],
    },
    "east-tennessee-exterminating": {
        "about": "fb1.jpg",
        "extras": [
            ("fb10.jpg", "Our truck on a pre-treat job"),
        ],
    },
}


def save_jpg(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=86)


def main() -> None:
    batch = json.loads(BATCH.read_text())
    by_slug = {p["slug"]: p for p in batch}
    for slug, plan in PLANS.items():
        folder = SRC[slug]
        dest = ROOT / "preview" / slug / "img"
        used = set()
        hashes = set()
        extras = []

        def take(name: str) -> Path:
            p = folder / name
            if not p.exists():
                raise SystemExit(f"missing {p}")
            if name in used:
                raise SystemExit(f"reused {slug}/{name}")
            h = hashlib.md5(p.read_bytes()).hexdigest()
            if h in hashes:
                raise SystemExit(f"duplicate bytes {slug}/{name}")
            used.add(name)
            hashes.add(h)
            return p

        for slot in ("hero", "about") + tuple(f"svc{i}" for i in range(1, 7)) + tuple(f"blog{i}" for i in range(1, 4)):
            if slot not in plan:
                continue
            save_jpg(take(plan[slot]), dest / f"{slot}.jpg")
        if "work1" in plan:
            rec = by_slug[slug]
            photos = []
            for i in range(1, 4):
                key = f"work{i}"
                if key not in plan:
                    photos.append(rec["photos"][i - 1])
                    continue
                fn, cap = plan[key]
                save_jpg(take(fn), dest / f"{key}.jpg")
                photos.append([f"{key}.jpg", cap or rec["photos"][i - 1][1]])
            rec["photos"] = photos
        for fn, cap in plan.get("extras", []):
            n = len(extras) + 1
            out_name = f"owner{n}.jpg"
            save_jpg(take(fn), dest / out_name)
            extras.append([out_name, cap])
        if extras:
            by_slug[slug]["about_photos"] = extras
        print(slug, "used", len(used), "extras", len(extras))
    BATCH.write_text(json.dumps(batch, indent=1) + "\n")
    print("wrote", BATCH)


if __name__ == "__main__":
    main()
