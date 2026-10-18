"""Build 30 Pro preview sites from the lead sheet (Oct 18, 2026).

Uses real contact info only. No invented reviews. Sample photos from examples/img.
Wordmark logos when we do not have theirs. Sample prices are labeled in the builder.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import struct
import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "examples" / "img"
OUT_JSON = Path(__file__).with_name("previews_batch.json")
LEADS = Path.home() / "Developer/StakichLeads/data/lead_sheet.tsv"
LEADS_JSON = Path.home() / "Developer/StakichLeads/data"

NAMES = [
    "East Tennessee Exterminating",
    "The Xterminator",
    "All Home Plumbing Co.",
    "Royal Flush Plumbing",
    "Axis Roofing",
    "Above All Plumbing",
    "Reese Plumbing",
    "Keith Colloms Plumbing Services",
    "Outhouse Plumbing",
    "Raschke & Sons Electric",
    "Eternity Fencing",
    "Happy Homes Pressure Washing",
    "Lawn Daddy Landscapes",
    "Piggy Power Washing",
    "Ricks Painting and Pressure Washing",
    "Southeast Concrete Construction",
    "Tennessee Stripes Lawn Care",
    "Feezell Total Maintenance",
    "First Class Fence",
    "Patriotic Pressure Washing",
    "Brandon's Tree Service",
    "GreenFoot Pest Solutions",
    "Wildlife Control Chattanooga",
    "Chattanooga Roofing Contractors",
    "Chris Spors Custom Homes, LLC",
    "Don's Fence Co",
    "Keith Hodge Plumbing LLC",
    "No Limits Home Improvements LLC",
    "Randolph Painting",
    "Goodwin Fences and Decks",
]


def slug_of(msg):
    m = re.search(r"preview/([a-z0-9-]+)", msg or "")
    return m.group(1) if m else ""


def maps_lookup():
    found = {}
    for fn in LEADS_JSON.glob("leads_2026-10-*.json"):
        for b in json.loads(fn.read_text()):
            found.setdefault(b["name"].lower(), b)
    for fn in LEADS_JSON.glob("maps_*.json"):
        if "knoxville" in fn.name:
            continue
        for b in json.loads(fn.read_text()):
            found.setdefault(b["name"].lower(), b)
    return found


def google_links(maps_url):
    if not maps_url:
        return "", ""
    m = re.search(r"1s0x([0-9a-f]+):0x([0-9a-f]+)", maps_url, re.I)
    pid = ""
    p = re.search(r"19s(ChIJ[A-Za-z0-9_-]+)", maps_url)
    if p:
        pid = p.group(1)
    cid = ""
    if m:
        cid = str(int(m.group(2), 16))
        if not pid:
            h1, h2 = int(m.group(1), 16), int(m.group(2), 16)
            raw = bytes([0x0A, 0x12, 0x09]) + struct.pack("<Q", h1) + bytes([0x11]) + struct.pack("<Q", h2)
            pid = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    g = f"https://www.google.com/maps?cid={cid}" if cid else ""
    r = f"https://search.google.com/local/writereview?placeid={pid}" if pid else ""
    return g, r


def first_name(owner):
    o = (owner or "").strip()
    if not o:
        return ""
    return o.split()[0]


def wordmark(name, brand, dest):
    w, h = 900, 400
    img = Image.new("RGB", (w, h), brand)
    draw = ImageDraw.Draw(img)
    text = name.replace(" LLC", "").replace(" Co.", " Co").replace("  ", " ").strip()
    font = None
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        if Path(path).exists():
            font = ImageFont.truetype(path, 54)
            break
    if font is None:
        font = ImageFont.load_default()
    # wrap
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        box = draw.textbbox((0, 0), trial, font=font)
        if box[2] > w - 80 and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    total_h = 0
    sizes = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        sizes.append(box)
        total_h += box[3] - box[1] + 12
    y = (h - total_h) // 2
    for line, box in zip(lines, sizes):
        tw = box[2] - box[0]
        draw.text(((w - tw) // 2, y), line, fill="#ffffff", font=font)
        y += box[3] - box[1] + 12
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "PNG")


def copy_photos(dirs, dest):
    dest.mkdir(parents=True, exist_ok=True)
    files = []
    for d in dirs:
        folder = IMG / d
        if not folder.exists():
            continue
        for p in sorted(folder.glob("*.jpg")):
            files.append(p)
    names = []
    for i, src in enumerate(files):
        name = f"p{i+1}.jpg"
        shutil.copy2(src, dest / name)
        names.append(name)
    # ensure at least 12 by cycling
    if not names:
        raise SystemExit(f"no photos in {dirs}")
    i = 0
    while len(names) < 12:
        src = files[i % len(files)]
        name = f"p{len(names)+1}.jpg"
        shutil.copy2(src, dest / name)
        names.append(name)
        i += 1
    return names


def trade_of(typ, name):
    s = f"{typ} {name}".lower()
    if "pest" in s or "exterminat" in s or "wildlife" in s:
        return "pest"
    if "plumb" in s:
        return "plumbing"
    if "roof" in s:
        return "roofing"
    if "electric" in s:
        return "electric"
    if "fence" in s:
        return "fence"
    if "pressure" in s or "soft wash" in s:
        return "wash"
    if "tree" in s:
        return "tree"
    if "lawn" in s or "landscape" in s:
        return "lawn"
    if "concrete" in s:
        return "concrete"
    if "paint" in s:
        return "paint"
    if "home" in s or "handyman" in s or "construct" in s:
        return "handyman"
    return "handyman"


TRADES = {
    "pest": {
        "brand": "#1d4a2a", "dark": "#122e1a", "accent": "#d4b35a", "accent_ink": "#122e1a", "bg": "#f6f8f4",
        "dirs": ["growth-pest-control", "lawn-care"],
        "topic": "pest control",
        "h1": "Pest control in {city}.",
        "tagline": "Local pest control for homes and businesses. Call or request a visit. We treat what you are seeing and help keep it from coming back.",
        "badges": ["Free inspections", "Homes and businesses", "Local and licensed", "Rated on Google"],
        "sub": "Ants, roaches, rodents, termites, and more.",
        "services": [
            ("General Pest Control", "Regular service for ants, roaches, spiders, and other household pests."),
            ("Termite Control", "Inspections and treatment to protect wood from termites."),
            ("Rodent Control", "Mice and rats. We find how they get in and close it up."),
            ("Mosquito Control", "Yard treatments in warm months so you can use your porch again."),
            ("Bed Bug Treatment", "A careful plan for bed bugs, not a one-spray guess."),
            ("Commercial Pest Control", "Restaurants, shops, and offices that need a steady schedule."),
        ],
        "about_title": "Local pest control you can call.",
        "work_sub": "Sample photos for this preview. Send yours and we will swap them in.",
        "estimate": [
            ("General pest visit", 99, 175),
            ("Quarterly service", 250, 450),
            ("Termite inspection", 0, 150),
            ("Rodent visit", 150, 350),
            ("Mosquito yard treatment", 80, 160),
        ],
        "booking": ["General pest control", "Termites", "Rodents", "Mosquitoes", "Bed bugs", "Commercial", "Something else"],
        "posts": [
            ("signs-you-need-pest-control", "Signs You Need Pest Control",
             "Seeing bugs once is one thing. Seeing them every week is another."),
            ("how-to-keep-ants-out-of-the-kitchen", "How to Keep Ants Out of the Kitchen",
             "A few small habits make ant treatments work better."),
            ("what-to-expect-on-a-pest-visit", "What to Expect on a Pest Control Visit",
             "Here is how a typical visit works, from the first look to the treatment."),
        ],
        "faq": [
            ("Do you treat homes and businesses?", "Yes. We handle both."),
            ("Are estimates or inspections free?", "Yes. Call and we will set a time to look."),
            ("Do I have to be home?", "For most interior work, yes. For some yard treatments, we can work if we can get in the yard."),
            ("What if they come back?", "Call us. A good plan includes follow-up, not one spray and goodbye."),
        ],
    },
    "plumbing": {
        "brand": "#1b365d", "dark": "#11233d", "accent": "#e0b25a", "accent_ink": "#11233d", "bg": "#f5f7fb",
        "dirs": ["hvac-plumbing", "starter-handyman"],
        "topic": "plumbing",
        "h1": "Plumbing repair and service in {city}.",
        "tagline": "Leaks, clogs, water heaters, and sewer work. Call or request a visit. We show up, find the problem, and tell you what it will take.",
        "badges": ["Free estimates", "Residential plumbing", "Water heaters", "Local plumber"],
        "sub": "Repairs, water heaters, drains, and new work.",
        "services": [
            ("Leak Repair", "Find the leak and fix it, including pipes in walls and under slabs when we can."),
            ("Drain Cleaning", "Clogged sinks, tubs, and main lines."),
            ("Water Heaters", "Repair or replace tank and tankless water heaters."),
            ("Sewer Lines", "Sewer clogs, camera checks, and line repair."),
            ("Faucets and Toilets", "Running toilets, dripping faucets, and fixture swaps."),
            ("New Plumbing", "Rough-in and finish plumbing for remodels and new work."),
        ],
        "about_title": "A local plumber you can call.",
        "work_sub": "Sample photos for this preview. Send job photos and we will put them on the site.",
        "estimate": [
            ("Service call", 95, 175),
            ("Drain cleaning", 150, 350),
            ("Water heater install", 1200, 2800),
            ("Toilet install", 180, 400),
            ("Sewer camera", 200, 400),
        ],
        "booking": ["Leak", "Clogged drain", "Water heater", "Sewer line", "Toilet or faucet", "Remodel plumbing", "Something else"],
        "posts": [
            ("what-to-do-when-a-pipe-leaks", "What to Do When a Pipe Leaks",
             "Shut the water off first. Then call. Here is how to find the valve."),
            ("signs-your-water-heater-is-failing", "Signs Your Water Heater Is on Its Way Out",
             "Rust, popping sounds, and no hot water are the usual warnings."),
            ("when-a-clog-is-more-than-a-clog", "When a Clog Is More Than a Clog",
             "If it keeps coming back, the problem may be in the main line."),
        ],
        "faq": [
            ("Do you do emergency leaks?", "Call. If we can get there, we will."),
            ("Are estimates free?", "Yes, for most jobs once we see the problem."),
            ("Do you replace water heaters?", "Yes. Tank and many tankless units."),
            ("What areas do you cover?", "We work in {city} and nearby towns."),
        ],
    },
    "roofing": {
        "brand": "#4a2e1b", "dark": "#2c1a10", "accent": "#d7b56a", "accent_ink": "#2c1a10", "bg": "#faf7f2",
        "dirs": ["roofing", "starter-handyman"],
        "topic": "roofing",
        "h1": "Roofing and repairs in {city}.",
        "tagline": "New roofs, leak repairs, and storm damage. Local crew. Free estimates. We tell you if a repair will do, or if it is time to replace.",
        "badges": ["Free estimates", "Roof repairs", "New roofs", "Local roofer"],
        "sub": "Shingles, leaks, storm damage, and gutters.",
        "services": [
            ("New Roofs", "Full tear-off and new shingles, done in a few days on most homes."),
            ("Leak Repair", "Find where water is getting in and fix that spot."),
            ("Storm Damage", "Hail and wind. We look it over and show you what we find."),
            ("Pipe Boots and Flashing", "Small parts that cause a lot of leaks if they fail."),
            ("Gutters", "New gutters and repairs so water leaves the house."),
            ("Inspections", "A walk of the roof before you buy, sell, or file a claim."),
        ],
        "about_title": "Roofing from a local crew.",
        "work_sub": "Sample photos for this preview. Send photos of your roofs and we will add them.",
        "estimate": [
            ("Leak repair", 250, 800),
            ("Pipe boot", 150, 350),
            ("Roof inspection", 0, 150),
            ("Gutter section", 200, 600),
            ("Full roof replacement", 8000, 16000),
        ],
        "booking": ["Leak repair", "New roof", "Storm damage", "Inspection", "Gutters", "Something else"],
        "posts": [
            ("after-a-hail-storm", "After a Hail Storm on Your Roof",
             "Do not climb up there. Look from the ground, take photos, and get it checked."),
            ("repair-or-replace-your-roof", "Repair or Replace? A Straight Answer",
             "Age, leaks, and missing shingles tell you more than a sales pitch."),
            ("why-pipe-boots-leak", "Why So Many Roofs Leak at the Pipe Boot",
             "Rubber boots dry out in the Tennessee sun. It is a cheap fix if you catch it."),
        ],
        "faq": [
            ("Is the estimate free?", "Yes."),
            ("How long does a new roof take?", "Most homes are a few days once we are on the schedule."),
            ("Do you work with insurance?", "We can document storm damage. You decide about the claim."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "electric": {
        "brand": "#1a2744", "dark": "#10182c", "accent": "#f0c14b", "accent_ink": "#10182c", "bg": "#f6f7fb",
        "dirs": ["starter-handyman", "hvac-plumbing"],
        "topic": "electrical work",
        "h1": "Electrical repair and installs in {city}.",
        "tagline": "Panels, outlets, lighting, and troubleshooting. Safe work from a local electrician. Call or request a visit.",
        "badges": ["Licensed electrician", "Free estimates", "Panels and lighting", "Local service"],
        "sub": "Repairs, new circuits, panels, and lighting.",
        "services": [
            ("Electrical Repair", "Breakers that trip, outlets that die, lights that flicker."),
            ("Panel Upgrades", "Older panels that cannot keep up with today's load."),
            ("Lighting", "Indoor and outdoor lighting, fans, and swaps."),
            ("New Circuits", "Power where you need it, including shops and additions."),
            ("EV Chargers", "A dedicated circuit for a home charger when the panel can take it."),
            ("Safety Checks", "A look at wiring before you buy, sell, or remodel."),
        ],
        "about_title": "A local electrician.",
        "work_sub": "Sample photos for this preview. Send job photos and we will use them.",
        "estimate": [
            ("Service call", 95, 175),
            ("Outlet or switch", 120, 250),
            ("Ceiling fan", 180, 350),
            ("New circuit", 350, 900),
            ("Panel upgrade", 1800, 4500),
        ],
        "booking": ["Repair", "Panel", "Lighting", "New circuit", "EV charger", "Safety check", "Something else"],
        "posts": [
            ("why-your-breaker-keeps-tripping", "Why Your Breaker Keeps Tripping",
             "It is usually a load problem or a bad breaker, not bad luck."),
            ("when-to-upgrade-an-electrical-panel", "When to Upgrade an Electrical Panel",
             "If you are adding a/c, a shop, or a charger, the panel may be the bottleneck."),
            ("flickering-lights-are-a-warning", "Flickering Lights Are a Warning",
             "Do not ignore them. Loose connections get hot."),
        ],
        "faq": [
            ("Are you licensed?", "Yes. Electrical work in Tennessee needs a license."),
            ("Are estimates free?", "Yes for most jobs after we see the work."),
            ("Do you do small jobs?", "Yes. One outlet still counts."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "fence": {
        "brand": "#2d4a1e", "dark": "#1a2e12", "accent": "#c9a24a", "accent_ink": "#1a2e12", "bg": "#f6f8f2",
        "dirs": ["lawn-care", "starter-handyman"],
        "topic": "fencing",
        "h1": "Fences and gates in {city}.",
        "tagline": "Wood, vinyl, chain link, and gates. Built for how you actually use the yard. Free estimates.",
        "badges": ["Free estimates", "Wood and vinyl", "Gates", "Local fence crew"],
        "sub": "Privacy fence, chain link, repairs, and gates.",
        "services": [
            ("Privacy Fence", "Wood privacy fence for the backyard."),
            ("Vinyl Fence", "Low-maintenance vinyl when you do not want to stain every year."),
            ("Chain Link", "Yards, dogs, and simple boundaries."),
            ("Gates", "Walk gates and drive gates that actually swing and latch."),
            ("Fence Repair", "Posts that lean, panels that blew out, hardware that failed."),
            ("HOA Help", "We can match what your neighborhood allows."),
        ],
        "about_title": "Fence work from a local crew.",
        "work_sub": "Sample photos for this preview. Send photos of your jobs and we will add them.",
        "estimate": [
            ("Fence repair", 150, 500),
            ("Walk gate", 250, 600),
            ("Privacy fence (per section)", 400, 900),
            ("Chain link (per section)", 250, 550),
        ],
        "booking": ["New privacy fence", "Vinyl", "Chain link", "Gate", "Repair", "Something else"],
        "posts": [
            ("wood-vs-vinyl-fence", "Wood vs Vinyl Fence",
             "Wood costs less up front. Vinyl costs less to keep. Here is a simple way to choose."),
            ("how-deep-fence-posts-should-go", "How Deep Fence Posts Should Go",
             "Shallow posts lean. We set them deep enough for Tennessee clay and wind."),
            ("when-to-repair-a-fence-instead", "When to Repair a Fence Instead of Replacing It",
             "A few bad posts is a repair. A whole run that is rotten is a replacement."),
        ],
        "faq": [
            ("Do you give free estimates?", "Yes. We look at the line and measure."),
            ("Do you pull permits?", "If the city or HOA needs one, we will talk through it."),
            ("How long does a fence take?", "Most yards are a few days once materials are in."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "wash": {
        "brand": "#0e4a6e", "dark": "#0a3149", "accent": "#7ec8e3", "accent_ink": "#0a3149", "bg": "#f3f8fb",
        "dirs": ["pressure-washing", "lawn-care"],
        "topic": "pressure washing",
        "h1": "Pressure washing and soft washing in {city}.",
        "tagline": "Houses, driveways, roofs, and sidewalks. Dirt and mildew come off. The surface stays. Free estimates.",
        "badges": ["Free estimates", "House wash", "Driveways", "Soft wash for siding"],
        "sub": "Houses, concrete, roofs, and patios.",
        "services": [
            ("House Wash", "Soft wash for siding so paint and vinyl are not blasted."),
            ("Driveways and Sidewalks", "Concrete that looks new again."),
            ("Roof Soft Wash", "Mildew on shingles, treated the right way."),
            ("Patios and Decks", "Buildup from leaves, pollen, and shade."),
            ("Fences", "Wood and vinyl fences that have turned gray or green."),
            ("Gutters and Soffit", "Streaks under the roof line."),
        ],
        "about_title": "A local wash crew.",
        "work_sub": "Sample photos for this preview. Before-and-afters of your jobs will look better. Send them.",
        "estimate": [
            ("Driveway", 150, 400),
            ("House wash", 250, 550),
            ("Roof soft wash", 300, 700),
            ("Patio or deck", 125, 350),
        ],
        "booking": ["House wash", "Driveway", "Roof", "Patio or deck", "Fence", "Something else"],
        "posts": [
            ("soft-wash-vs-pressure-wash", "Soft Wash vs Pressure Wash",
             "Siding wants a soft wash. Concrete can take pressure. Mixing those up does damage."),
            ("how-often-to-wash-a-house", "How Often to Wash a House in East Tennessee",
             "Pollen, mildew, and shade. Most homes look better once a year."),
            ("why-driveways-turn-black", "Why Driveways Turn Black",
             "It is usually mildew and oil, not stained concrete. It comes off."),
        ],
        "faq": [
            ("Will pressure washing hurt my siding?", "We use a soft wash on houses. High pressure is for concrete."),
            ("Are estimates free?", "Yes."),
            ("Do I need to be home?", "Not always, as long as we can get to the water spigot."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "lawn": {
        "brand": "#2a5a24", "dark": "#173616", "accent": "#e2c15a", "accent_ink": "#173616", "bg": "#f5f8f2",
        "dirs": ["lawn-care", "pressure-washing"],
        "topic": "lawn care",
        "h1": "Lawn care and landscaping in {city}.",
        "tagline": "Mowing, beds, cleanups, and yard work you can count on. Local crew. Request a quote.",
        "badges": ["Local lawn crew", "Mowing and beds", "Cleanups", "Free quotes"],
        "sub": "Mowing, mulch, beds, and seasonal cleanups.",
        "services": [
            ("Mowing", "A regular schedule so the yard stays even."),
            ("Edging and Blowing", "Walks and drives left clean."),
            ("Mulch and Beds", "Beds pulled, mulched, and looking tended."),
            ("Leaf Cleanup", "Fall and spring cleanups."),
            ("Shrub Trimming", "Hedges and shrubs kept in shape."),
            ("Yard Cleanup", "Overgrown lots brought back under control."),
        ],
        "about_title": "Lawn work from a local crew.",
        "work_sub": "Sample photos for this preview. Send photos of your yards and we will put them up.",
        "estimate": [
            ("One-time mow", 45, 90),
            ("Weekly mowing", 35, 75),
            ("Mulch beds", 250, 800),
            ("Leaf cleanup", 150, 450),
        ],
        "booking": ["Mowing", "Mulch and beds", "Cleanup", "Shrub trimming", "One-time visit", "Something else"],
        "posts": [
            ("how-often-to-mow-in-tennessee", "How Often to Mow in Tennessee",
             "In peak summer, weekly is normal. In a dry spell, you can stretch it."),
            ("mulch-that-actually-helps", "Mulch That Actually Helps",
             "Too little does nothing. Too much smothers roots. Here is a simple depth."),
            ("fall-cleanup-before-leaves-mat", "Fall Cleanup Before Leaves Mat Down",
             "A thick mat of wet leaves kills grass. Get them up before winter."),
        ],
        "faq": [
            ("Do you mow weekly?", "Yes, on a schedule we set with you."),
            ("Are quotes free?", "Yes."),
            ("Do you bring the clippings?", "We bag or mulch, whichever you want."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "tree": {
        "brand": "#23401c", "dark": "#152610", "accent": "#d0b25a", "accent_ink": "#152610", "bg": "#f5f7f1",
        "dirs": ["lawn-care", "starter-handyman"],
        "topic": "tree work",
        "h1": "Tree service in {city}.",
        "tagline": "Tree removal, trimming, and stump grinding. Safe work around houses and power lines. Free estimates.",
        "badges": ["Free estimates", "Tree removal", "Trimming", "Stump grinding"],
        "sub": "Removals, trimming, storm cleanup, and stumps.",
        "services": [
            ("Tree Removal", "Take the tree down in pieces when it sits next to a house."),
            ("Trimming", "Dead wood and limbs that hang over the roof or drive."),
            ("Stump Grinding", "The stump gone so you can mow or plant."),
            ("Storm Cleanup", "Trees down after wind. We cut and haul."),
            ("Lot Clearing", "Trees and brush cleared for a build or a view."),
            ("Hazard Trees", "Leaning or rotting trees that should not wait."),
        ],
        "about_title": "Tree work from a local crew.",
        "work_sub": "Sample photos for this preview. Send photos of your jobs and we will add them.",
        "estimate": [
            ("Small tree trim", 200, 500),
            ("Tree removal", 500, 2500),
            ("Stump grinding", 150, 400),
            ("Storm cleanup", 300, 1500),
        ],
        "booking": ["Tree removal", "Trimming", "Stump grinding", "Storm cleanup", "Lot clearing", "Something else"],
        "posts": [
            ("when-a-tree-should-come-down", "When a Tree Should Come Down",
             "Lean, rot, and big dead limbs are the usual signs. Do not wait for a storm."),
            ("why-stump-grinding-matters", "Why Stump Grinding Matters",
             "A stump is a tripping hazard and a sprout factory. Grinding is the clean finish."),
            ("trimming-vs-topping", "Trimming vs Topping",
             "Topping hurts the tree. Trimming dead and crossing wood is the right job."),
        ],
        "faq": [
            ("Do you give free estimates?", "Yes. We look at the tree and the drop zone."),
            ("Do you haul the wood?", "Yes, unless you want it left for firewood."),
            ("Can you work around power lines?", "If lines are involved, we plan that before we cut."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "concrete": {
        "brand": "#3a3a3a", "dark": "#1e1e1e", "accent": "#d2b36a", "accent_ink": "#1e1e1e", "bg": "#f6f6f4",
        "dirs": ["starter-handyman", "pressure-washing"],
        "topic": "concrete work",
        "h1": "Concrete driveways, slabs, and patios in {city}.",
        "tagline": "New pours, repairs, and replacements. The finish is only as good as the base under it. Free quotes.",
        "badges": ["Free quotes", "Driveways", "Slabs", "Local concrete crew"],
        "sub": "Driveways, patios, slabs, and tear-out.",
        "services": [
            ("Driveways", "New concrete drives with a solid base."),
            ("Patios and Slabs", "Patios, shop slabs, and pads."),
            ("Tear-out and Replace", "Old cracked concrete out, new pour in."),
            ("Sidewalks", "Walks that drain and do not trip people."),
            ("Footers", "Footers and small foundation work."),
            ("Broom and Finish", "A finish that matches the rest of the house."),
        ],
        "about_title": "Concrete from a local crew.",
        "work_sub": "Sample photos for this preview. Send photos of pours and we will add them.",
        "estimate": [
            ("Small slab", 1200, 2800),
            ("Patio", 2500, 6000),
            ("Driveway", 4500, 12000),
            ("Tear-out (section)", 400, 1200),
        ],
        "booking": ["Driveway", "Patio or slab", "Tear-out", "Sidewalk", "Footer", "Something else"],
        "posts": [
            ("why-new-concrete-cracks", "Why New Concrete Cracks",
             "Usually the base, not the mix. We pack it before we pour."),
            ("how-long-before-you-drive-on-it", "How Long Before You Drive on New Concrete",
             "Give it time. Cars too soon leave marks you cannot undo."),
            ("repair-or-replace-a-driveway", "Repair or Replace a Driveway",
             "A few sunken spots can be cut out. A whole drive that is shot should come out."),
        ],
        "faq": [
            ("Do you give free quotes?", "Yes. We measure and look at access."),
            ("How long does a driveway take?", "Prep, pour, and cure. We will give you a clear timeline."),
            ("Do you tear out old concrete?", "Yes."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "paint": {
        "brand": "#4a2a4a", "dark": "#2c182c", "accent": "#e0c56a", "accent_ink": "#2c182c", "bg": "#faf7f4",
        "dirs": ["starter-handyman", "pressure-washing"],
        "topic": "painting",
        "h1": "Interior and exterior painting in {city}.",
        "tagline": "Houses, rooms, and trim. Prep is most of the job. Free estimates.",
        "badges": ["Free estimates", "Interior", "Exterior", "Local painter"],
        "sub": "Rooms, exteriors, decks, and trim.",
        "services": [
            ("Interior Painting", "Rooms, ceilings, and trim."),
            ("Exterior Painting", "Siding and trim that can take Tennessee weather."),
            ("Prep and Repair", "Scraping, caulk, and small wood repair before paint."),
            ("Decks and Porches", "Paint or stain that sticks."),
            ("Cabinets", "Cabinet painting when a full kitchen redo is too much."),
            ("Pressure Wash First", "Exteriors get washed before paint."),
        ],
        "about_title": "Painting from a local crew.",
        "work_sub": "Sample photos for this preview. Send before-and-afters and we will use them.",
        "estimate": [
            ("One room", 300, 700),
            ("Interior (whole house)", 2500, 7000),
            ("Exterior", 2800, 8000),
            ("Deck stain", 400, 1200),
        ],
        "booking": ["Interior", "Exterior", "Deck or porch", "Cabinets", "Repair and paint", "Something else"],
        "posts": [
            ("paint-fails-without-prep", "Paint Fails Without Prep",
             "Skip the scrape and caulk and it peels. Prep is the job."),
            ("best-time-to-paint-outside", "Best Time to Paint Outside in Tennessee",
             "Not in a heat wave and not right before rain. Mild and dry is the window."),
            ("one-room-or-the-whole-house", "One Room or the Whole House",
             "Start with the room you live in. We can plan the rest."),
        ],
        "faq": [
            ("Do you move furniture?", "We move what we can and cover the rest."),
            ("Are estimates free?", "Yes."),
            ("Do you paint exteriors?", "Yes, including wash and prep."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
    "handyman": {
        "brand": "#3b2a1a", "dark": "#241910", "accent": "#e0b35a", "accent_ink": "#241910", "bg": "#faf7f2",
        "dirs": ["starter-handyman", "pressure-washing"],
        "topic": "home repairs",
        "h1": "Home repair and remodeling in {city}.",
        "tagline": "Repairs, small remodels, and punch lists. One call instead of five. Free estimates.",
        "badges": ["Free estimates", "Licensed and insured", "Repairs and remodels", "Local"],
        "sub": "Repairs, carpentry, and small remodels.",
        "services": [
            ("Home Repairs", "The list on the fridge. We work through it."),
            ("Carpentry", "Doors, trim, stairs, and wood that has given up."),
            ("Drywall", "Holes, cracks, and texture."),
            ("Painting", "Rooms and touch-up after repairs."),
            ("Small Remodels", "Bathrooms, kitchens, and rooms that need more than a patch."),
            ("Exterior", "Decks, fences, and the outside punch list."),
        ],
        "about_title": "A local crew for the house.",
        "work_sub": "Sample photos for this preview. Send photos of your jobs and we will add them.",
        "estimate": [
            ("Small repair", 100, 300),
            ("Drywall patch", 150, 450),
            ("Door or trim", 200, 600),
            ("Bathroom refresh", 2500, 8000),
        ],
        "booking": ["Repair list", "Carpentry", "Drywall", "Paint", "Remodel", "Something else"],
        "posts": [
            ("a-repair-list-that-gets-done", "A Repair List That Gets Done",
             "Write it down. We come through the house and knock it out in order."),
            ("when-a-patch-is-not-enough", "When a Patch Is Not Enough",
             "If the wood behind it is rotten, we fix that first."),
            ("what-to-expect-on-a-small-remodel", "What to Expect on a Small Remodel",
             "A clear plan, a start date, and a house you can still live in."),
        ],
        "faq": [
            ("Do you do small jobs?", "Yes."),
            ("Are estimates free?", "Yes."),
            ("Are you licensed and insured?", "Yes."),
            ("What areas do you cover?", "{city} and nearby towns."),
        ],
    },
}


def post_bodies(trade, biz, phone, city):
    t = TRADES[trade]
    extras = {
        "pest": [
            [("p", f"Bugs in {city} do not wait. If you keep seeing the same ones, it is time for a real visit, not another store spray."),
             ("h2", "What to watch for"),
             ("ul", ["Trails of ants on the counter", "Droppings in the pantry or garage", "Wasps at the eaves", "Scratching in the walls at night"]),
             ("h2", "What we do"),
             ("p", f"We look at where they are coming from, treat that, and talk about what will keep them out. Call {biz} at {phone}.")],
            [("p", "Ants follow food and water. Wipe the crumbs and you make the treatment last."),
             ("h2", "Simple habits"),
             ("ul", ["Wipe counters at night", "Take the trash out", "Fix the dripping faucet", "Store pet food in a sealed bin"]),
             ("h2", "Then call"),
             ("p", f"If they are still coming, it is a nest, not a few scouts. Call {phone}.")],
            [("p", "A visit is not a mystery. We look, we treat, we tell you the plan."),
             ("h2", "On site"),
             ("p", "We walk the house or building and look at the spots you mentioned, plus the usual hiding places."),
             ("h2", "After"),
             ("p", f"You will know what we did and when to call us back. {phone}.")],
        ],
        "plumbing": [
            [("p", "If water is on the floor, shut it off at the valve or the meter. Then call."),
             ("h2", "Find the valve"),
             ("p", "Under the sink, behind the toilet, or at the main where the water enters the house."),
             ("h2", "Then call us"),
             ("p", f"{biz} at {phone}. We will tell you if we can come now.")],
            [("p", "Water heaters fail slowly, then all at once."),
             ("h2", "Signs"),
             ("ul", ["Rusty water", "Popping or banging", "Water on the floor around the tank", "Not enough hot water"]),
             ("h2", "Repair or replace"),
             ("p", f"If it is 10 to 12 years old, replacement is usually the honest answer. Call {phone}.")],
            [("p", "A clog that comes back every week is often in the main line, not the sink trap."),
             ("h2", "When to snake vs camera"),
             ("p", "If we have been here twice for the same clog, we look with a camera."),
             ("h2", "Call"),
             ("p", f"{phone}. Tell us which fixtures are slow.")],
        ],
        "roofing": [
            [("p", "After hail, stay off the roof. Look from the ground for missing shingles and dents in vents."),
             ("h2", "Take photos"),
             ("p", "Date them. Inside stains count too."),
             ("h2", "Get it checked"),
             ("p", f"Call {biz} at {phone} for a look before you call insurance.")],
            [("p", "A leak does not always mean a new roof."),
             ("h2", "Repair is enough when"),
             ("ul", ["The roof is fairly young", "The leak is in one spot", "Shingles around it still look sound"]),
             ("h2", "Replace when"),
             ("p", f"It is old, it leaks in many places, or shingles are curling across the roof. Call {phone} and we will say which.")],
            [("p", "Pipe boots are the rubber collars around roof vents. Sun cooks them."),
             ("h2", "A cheap leak"),
             ("p", "Replacing a boot is a small job. Waiting until the decking rots is not."),
             ("h2", "Have us look"),
             ("p", f"{phone}.")],
        ],
        "electric": [
            [("p", "A breaker that trips over and over is telling you the circuit is overloaded or the breaker is tired."),
             ("h2", "Do not keep resetting it"),
             ("p", "That is how wires heat up."),
             ("h2", "Call"),
             ("p", f"{biz} at {phone}. We will find the load or the fault.")],
            [("p", "Old panels were not built for today's kitchens, a/c, and chargers."),
             ("h2", "Signs you need more"),
             ("ul", ["You have to unplug one thing to run another", "The panel is warm", "You still have fuses"]),
             ("h2", "A look first"),
             ("p", f"Call {phone}. We will tell you if an upgrade is next.")],
            [("p", "Flicker can be a loose bulb. It can also be a loose wire."),
             ("h2", "If it is more than one light"),
             ("p", "Treat it as a wiring problem until we prove it is not."),
             ("h2", "Call"),
             ("p", f"{phone}.")],
        ],
        "fence": [
            [("p", "Wood looks classic and costs less to start. Vinyl skips the stain every few years."),
             ("h2", "Pick for the yard"),
             ("p", "Dogs, privacy, and HOA rules all matter more than a catalog photo."),
             ("h2", "We will walk it"),
             ("p", f"Call {biz} at {phone} for a measure.")],
            [("p", "Posts that sit in a shallow hole lean after the first wet winter."),
             ("h2", "How we set them"),
             ("p", "Deep enough for frost and clay, packed so they stay."),
             ("h2", "Ask us"),
             ("p", f"{phone}.")],
            [("p", "If a few posts failed in a storm, repair. If the whole run is rotten at the ground, replace."),
             ("h2", "We will say which"),
             ("p", f"Call {phone} and we will look before you buy a whole new fence you may not need.")],
        ],
        "wash": [
            [("p", "Pressure is for concrete. Soft wash is for siding and roofs. Using the wrong one leaves marks."),
             ("h2", "What we use where"),
             ("ul", ["House and vinyl: soft wash", "Driveway and sidewalk: pressure", "Roof: a low-pressure mix"]),
             ("h2", "Book a wash"),
             ("p", f"{biz} at {phone}.")],
            [("p", "East Tennessee pollen and mildew stack up. Most houses look better with a wash once a year."),
             ("h2", "Spring is a good time"),
             ("p", "After the oak pollen drops, not during it."),
             ("h2", "Call"),
             ("p", f"{phone}.")],
            [("p", "Black streaks on concrete are often mildew, not a stain in the slab."),
             ("h2", "It comes off"),
             ("p", "Oil spots take more work. We will tell you what will and will not lift."),
             ("h2", "Get a quote"),
             ("p", f"{phone}.")],
        ],
        "lawn": [
            [("p", "In a wet Tennessee summer, weekly mowing keeps the yard even. In a drought, skip a week rather than scalp it."),
             ("h2", "Height matters"),
             ("p", "Taller grass shades the soil and needs less water."),
             ("h2", "Set a schedule"),
             ("p", f"Call {biz} at {phone}.")],
            [("p", "Two to three inches of mulch is enough. A volcano around the trunk is too much."),
             ("h2", "Beds first"),
             ("p", "Pull weeds, edge, then mulch. Mulch on weeds is a waste."),
             ("h2", "We can do the beds"),
             ("p", f"{phone}.")],
            [("p", "Wet leaves mat down and kill the grass under them."),
             ("h2", "Do not wait until January"),
             ("p", "A couple of passes in fall beats one miserable day in the cold."),
             ("h2", "Book a cleanup"),
             ("p", f"{phone}.")],
        ],
        "tree": [
            [("p", "A tree that leans toward the house, or has a big dead top, is not a wait-and-see job."),
             ("h2", "Look for"),
             ("ul", ["A new lean after rain", "Fungus at the base", "Large dead limbs over the roof"]),
             ("h2", "Get a look"),
             ("p", f"Call {biz} at {phone}.")],
            [("p", "Leaving a stump means sprouts, a mower hazard, and a hole later."),
             ("h2", "Grind it"),
             ("p", "We grind below grade so you can cover it with soil or sod."),
             ("h2", "Add it to the removal"),
             ("p", f"{phone}.")],
            [("p", "Topping a tree does not make it safer. It makes weak sprouts."),
             ("h2", "Trim instead"),
             ("p", "Take dead wood and limbs that rub or hang over the house."),
             ("h2", "Ask us"),
             ("p", f"{phone}.")],
        ],
        "concrete": [
            [("p", "Cracks that show up in the first year are often a base that was not packed."),
             ("h2", "What we do first"),
             ("p", "Grade, gravel, pack, then pour."),
             ("h2", "Talk to us"),
             ("p", f"{biz} at {phone}.")],
            [("p", "New concrete needs days, not hours, before a car sits on it."),
             ("h2", "We will tell you the date"),
             ("p", "Weather changes cure time. We do not guess."),
             ("h2", "Pour day"),
             ("p", f"Call {phone} to get on the schedule.")],
            [("p", "Saw-cut a bad section if the rest is sound. Replace the whole drive if it is mapped with cracks."),
             ("h2", "We will measure both"),
             ("p", f"{phone}.")],
        ],
        "paint": [
            [("p", "Paint on dirty, chalky, or wet wood peels. Wash, scrape, caulk, then paint."),
             ("h2", "That is the job"),
             ("p", "The color is the last hour, not the whole day."),
             ("h2", "Get an estimate"),
             ("p", f"{biz} at {phone}.")],
            [("p", "Paint outside in mild, dry weather. Hot siding flashes the paint. Rain washes it."),
             ("h2", "We watch the week"),
             ("p", "If the forecast turns, we wait."),
             ("h2", "Book"),
             ("p", f"{phone}.")],
            [("p", "One room still counts. You do not have to paint the whole house to start."),
             ("h2", "Pick the room you live in"),
             ("p", f"Call {phone} and we will quote that room first.")],
        ],
        "handyman": [
            [("p", "A written list gets done. A pile of 'when you have time' jobs does not."),
             ("h2", "We work the list"),
             ("p", "Doors, leaks, holes in the wall, the deck board that flexes."),
             ("h2", "Start"),
             ("p", f"Call {biz} at {phone}.")],
            [("p", "A pretty patch over rotten wood comes back. We open it up if we have to."),
             ("h2", "Honest first"),
             ("p", "If it is bigger than a patch, we say so before we start."),
             ("h2", "Call"),
             ("p", f"{phone}.")],
            [("p", "Small remodels still need a plan: what stays, what goes, and how you live in the house while we work."),
             ("h2", "Walk through"),
             ("p", f"Call {phone} and we will walk the room.")],
        ],
    }
    return extras[trade]


def about_paras(trade, biz, owner, city, phone, area):
    who = f"I'm {first_name(owner)}" if first_name(owner) else "We're"
    if first_name(owner):
        p1 = f"{first_name(owner)} runs {biz} in {city}. {who} the person you talk to, not a call center."
    else:
        p1 = f"{biz} is a local crew in {city}. You call us, we come look, and we tell you what it will take."
    p2 = {
        "pest": f"We handle homes and businesses. If you keep seeing the same pests, call {phone} and we will set a visit.",
        "plumbing": f"Leaks, clogs, water heaters, and sewer work. Call {phone} and tell us what is going on.",
        "roofing": f"New roofs, leak repairs, and storm checks. Call {phone} for a free look.",
        "electric": f"Repairs, panels, lighting, and new circuits. Call {phone}.",
        "fence": f"New fence, a gate that works, or a repair after a storm. Call {phone} for a measure.",
        "wash": f"Houses, drives, and roofs. Call {phone} for a free estimate.",
        "lawn": f"Mowing, beds, and cleanups. Call {phone} to set a schedule.",
        "tree": f"Removals, trimming, and stumps. Call {phone} for a free estimate.",
        "concrete": f"Driveways, slabs, and tear-out. Call {phone} for a quote.",
        "paint": f"Rooms and exteriors. Prep first, then paint. Call {phone}.",
        "handyman": f"The repair list and small remodels. Call {phone} for a free estimate.",
    }[trade]
    p3 = f"We work in {area}."
    return [p1, p2, p3]


def build_one(row, maps):
    name = row["Business"]
    slug = slug_of(row["complete message to send"])
    if name == "Goodwin Fences and Decks":
        slug = "goodwin-fences-and-decks"
    trade = trade_of(row["Type"], name)
    t = TRADES[trade]
    city = row["Town"] or "East Tennessee"
    city_short = city.split(",")[0]
    phone = row["Phone"]
    owner = row["Owner"]
    addr = row["Mailing Address"] or city
    email = row["Email"]
    fb = row["Facebook"]
    rec = maps.get(name.lower()) or {}
    if not rec:
        for k, v in maps.items():
            if name.lower()[:16] in k:
                rec = v
                break
    g, grev = google_links(rec.get("maps_url", ""))
    rating = (row["Google Rating"] or "").strip()
    nrev = row["Reviews"].strip()
    rating_t = None
    if rating:
        rating_t = [rating, int(nrev) if nrev.isdigit() else None]

    dest = ROOT / "preview" / slug / "img"
    photos = copy_photos(t["dirs"], dest)
    wordmark(name, t["brand"], dest / "logo.png")

    hero, about = photos[0], photos[1]
    svc_imgs = photos[2:8]
    work = photos[8:11]
    post_imgs = photos[9:12] if len(photos) >= 12 else photos[3:6]

    services = []
    for i, (title, blurb) in enumerate(t["services"]):
        services.append([svc_imgs[i % len(svc_imgs)], title, blurb])

    posts = []
    bodies = post_bodies(trade, name, phone, city_short)
    dates = ["2026-10-08", "2026-09-24", "2026-09-10"]
    for i, ((pslug, title, excerpt), body) in enumerate(zip(t["posts"], bodies)):
        posts.append({
            "slug": pslug,
            "date": dates[i],
            "img": f"/preview/{slug}/img/{post_imgs[i % len(post_imgs)]}",
            "title": title,
            "excerpt": excerpt,
            "body": body,
        })

    faq = [(q, a.format(city=city_short)) for q, a in t["faq"]]
    faq.append(("How do I get started?", f"Call or text {phone}, or use the request form on this site."))

    who = first_name(owner)
    greet = who if who else "the shop"
    p = {
        "slug": slug,
        "name": name,
        "owner": who,
        "plan": "pro",
        "brand": t["brand"], "dark": t["dark"], "accent": t["accent"], "accent_ink": t["accent_ink"], "bg": t["bg"],
        "logo": "logo.png",
        "hero": f"/preview/{slug}/img/{hero}",
        "h1": t["h1"].format(city=city_short),
        "tagline": t["tagline"],
        "badges": t["badges"],
        "city": city,
        "services_sub": t["sub"],
        "phone": phone,
        "email": email,
        "address": addr,
        "area": f"{city_short} and nearby towns",
        "facebook": fb,
        "google": g,
        "google_review": grev,
        "services": services,
        "about_photo": about,
        "about_alt": f"{name} in {city_short}",
        "about_title": t["about_title"],
        "about": about_paras(trade, name, owner, city_short, phone, f"{city_short} and nearby towns"),
        "work_sub": t["work_sub"],
        "photos": [[work[i % len(work)], cap] for i, cap in enumerate(
            ["On the job", "A recent project", "Work in progress"]
        )],
        "size_label": "Job size",
        "sizes": [["Small", "1"], ["Medium", "1.7"], ["Large", "2.6"]],
        "estimate": t["estimate"],
        "est_sub": "Pick the job size and what you need. See a rough price range in seconds.",
        "est_note": "Sample prices for this preview. Real quotes come after we see the job.",
        "est_btn": "Get a free estimate",
        "book_title": "Request a visit",
        "book_btn": "Request my visit",
        "book_sub": "Tell us what is going on and pick a day. We will call or text to set a time.",
        "contact_title": "Call or request a visit",
        "cta_line": f"Call {phone} or send a request. We will get back to you.",
        "post_help": f"Call {phone} for a free estimate.",
        "book_ph": "What needs to be done, and where is the property?",
        "faq_try": "estimate",
        "booking_services": t["booking"],
        "times": ["8:00 AM", "10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM"],
        "posts": posts,
        "faq": faq,
    }
    if rating_t:
        p["rating"] = rating_t
    return p


def main():
    with LEADS.open() as f:
        rows = {r["Business"]: r for r in csv.DictReader(f, delimiter="\t")}
    maps = maps_lookup()
    batch = []
    for name in NAMES:
        if name not in rows:
            raise SystemExit(f"missing {name}")
        p = build_one(rows[name], maps)
        batch.append(p)
        print("prepared", p["slug"])
    OUT_JSON.write_text(json.dumps(batch, indent=1))
    Path(__file__).with_name("previews_batch.py").write_text(
        "import json\nfrom pathlib import Path\nBATCH = json.loads(Path(__file__).with_name('previews_batch.json').read_text())\n"
    )
    print("wrote", len(batch), "previews")


if __name__ == "__main__":
    main()
