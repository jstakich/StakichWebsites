"""Builds the example websites and the examples gallery.

Run from the project root:  python3 scripts/build_examples.py
"""
from pathlib import Path

from common import SITE, cta_band, footer, head, page_hero, scripts, share_mount, topbar

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "examples"

SITES = [
    {
        "slug": "lawn-care",
        "industry": "Lawn Care & Landscaping",
        "keyword": "Lawn Care Website Example",
        "layout": "Call Now",
        "name": "Green Leaf Lawn Care",
        "emoji": "🌿",
        "brand": "#2f6b3a", "dark": "#1b4223", "accent": "#ffd166", "accent_ink": "#1d2b1f", "bg": "#f6f8f3",
        "h1": "A greener, cleaner yard without lifting a finger.",
        "tagline": "Weekly mowing, edging, leaf cleanup, and landscaping for homes and businesses in Cleveland and Bradley County.",
        "cta": "Get a Free Estimate",
        "badges": ["Licensed & insured", "Free estimates", "Same-week service"],
        "services": [
            ("🌱", "Weekly Mowing", "Mow, edge, trim, and blow every visit so your yard always looks sharp.", "From $35/visit"),
            ("🍂", "Leaf Cleanup", "Fall and spring cleanups, hauled away so you don't have to bag a thing.", "From $95"),
            ("✂️", "Hedge Trimming", "Neat, healthy shrubs and hedges shaped the way you like them.", "From $60"),
            ("🌸", "Mulch & Beds", "Fresh mulch, weeding, and flower bed care for real curb appeal.", "From $120"),
            ("💧", "Aeration & Seeding", "Thicker, greener grass with core aeration and overseeding.", "From $150"),
            ("🏢", "Commercial Lawns", "Reliable grounds care for offices, churches, and rentals.", "Custom quote"),
        ],
        "why": [("12+", "years in business"), ("900+", "yards cared for"), ("4.9★", "average rating"), ("48 hr", "estimate turnaround")],
        "gallery": [("🏡", "Front yard refresh"), ("🌳", "Shrub shaping"), ("🍁", "Fall cleanup"), ("🌼", "New flower beds")],
        "areas": ["Cleveland", "Charleston", "Ooltewah", "Calhoun", "McDonald", "Georgetown"],
        "reviews": [
            ("They show up the same day every week and the yard looks perfect.", "Dana R., Cleveland"),
            ("Fair price, friendly crew, and they texted before every visit.", "Mike T., Ooltewah"),
            ("Our church grounds have never looked better. Highly recommend.", "Pastor Lee, Calhoun"),
        ],
        "faq": [
            ("Do you offer free estimates?", "Yes. We'll look at your yard and give you a written price, usually within 48 hours."),
            ("Do I have to sign a contract?", "No. Weekly service is month-to-month, and you can pause anytime."),
            ("What if it rains on my service day?", "We'll text you and come the next dry day."),
        ],
        "hours": "Mon–Sat 7am–6pm",
    },
    {
        "slug": "pressure-washing",
        "industry": "Pressure Washing",
        "keyword": "Pressure Washing Website Example",
        "layout": "Call Now",
        "name": "Blue Ridge Pressure Washing",
        "emoji": "💦",
        "brand": "#1565c0", "dark": "#0b3a75", "accent": "#4fd1ff", "accent_ink": "#062a44", "bg": "#f3f7fc",
        "h1": "Make your home look brand new again.",
        "tagline": "House washing, driveways, decks, and roofs, cleaned safely with soft-wash and hot-water equipment.",
        "cta": "Get a Free Quote",
        "badges": ["Fully insured", "Soft-wash safe", "100% satisfaction promise"],
        "services": [
            ("🏠", "House Washing", "Gentle soft-wash removes mold, mildew, and grime from siding.", "From $249"),
            ("🚗", "Driveways & Sidewalks", "Hot-water surface cleaning that lifts oil stains and dirt.", "From $129"),
            ("🪵", "Deck & Fence", "Bring wood back to life, ready for stain or sealing.", "From $179"),
            ("🏚️", "Roof Soft Wash", "Remove black streaks safely without damaging shingles.", "From $399"),
            ("🧱", "Patios & Pavers", "Clean and re-sand pavers for a like-new patio.", "From $149"),
            ("🏬", "Commercial", "Storefronts, dumpster pads, and parking areas.", "Custom quote"),
        ],
        "why": [("2,000+", "homes washed"), ("5★", "Google rating"), ("$2M", "insured"), ("24 hr", "quote reply")],
        "gallery": [("✨", "Siding before & after"), ("🚙", "Driveway cleaning"), ("🌲", "Deck restore"), ("🏡", "Roof soft wash")],
        "areas": ["Chattanooga", "Cleveland", "Hixson", "Signal Mountain", "Ringgold", "East Ridge"],
        "reviews": [
            ("Our driveway looks like it was just poured. Amazing difference.", "Kelly S., Hixson"),
            ("On time, professional, and careful around our plants.", "James W., Chattanooga"),
            ("The roof streaks are completely gone. Worth every penny.", "Angela P., Ringgold"),
        ],
        "faq": [
            ("Is pressure washing safe for my siding?", "Yes. We use low-pressure soft-washing on siding and roofs, so nothing gets damaged."),
            ("Do I need to be home?", "No. We just need access to an outside water spigot."),
            ("How long does it last?", "Most homes stay clean for 1–2 years depending on shade and weather."),
        ],
        "hours": "Mon–Sat 8am–7pm",
    },
    {
        "slug": "hvac-plumbing",
        "industry": "HVAC & Plumbing",
        "keyword": "HVAC & Plumbing Website Example",
        "layout": "Call Now",
        "name": "Summit Heating, Air & Plumbing",
        "emoji": "🔧",
        "brand": "#c62828", "dark": "#7f1416", "accent": "#ffc857", "accent_ink": "#3a1a00", "bg": "#fbf6f5",
        "h1": "Fast, honest heating, cooling, and plumbing repair.",
        "tagline": "24/7 emergency service. Upfront prices before we start, and no surprise fees.",
        "cta": "Call for Service",
        "badges": ["24/7 emergencies", "Upfront pricing", "Licensed technicians"],
        "services": [
            ("❄️", "AC Repair", "Same-day AC repair for all major brands. Cool again fast.", "$79 service call"),
            ("🔥", "Furnace & Heat Pumps", "Repair, tune-ups, and new system installs.", "$79 service call"),
            ("🚿", "Plumbing Repair", "Leaks, clogs, running toilets, and broken pipes fixed right.", "From $99"),
            ("🛁", "Water Heaters", "Tank and tankless water heater repair and replacement.", "From $1,295 installed"),
            ("🧰", "Maintenance Plans", "Two tune-ups a year plus priority service and discounts.", "$15/month"),
            ("🏗️", "New Construction", "Full HVAC and plumbing for new homes and remodels.", "Custom quote"),
        ],
        "why": [("24/7", "emergency service"), ("60 min", "average arrival"), ("1 yr", "labor warranty"), ("A+", "BBB rating")],
        "gallery": [("🌡️", "New AC install"), ("🛠️", "Furnace tune-up"), ("🚰", "Pipe repair"), ("♨️", "Tankless heater")],
        "areas": ["Cleveland", "Athens", "Chattanooga", "Dayton", "Etowah", "Benton"],
        "reviews": [
            ("AC died at 9pm in July and they had it running by 10:30. Lifesavers.", "Robert H., Athens"),
            ("Told me the price before starting. No upsell, no games.", "Sherry M., Cleveland"),
            ("Replaced our water heater the same day. Clean, quick work.", "Tom B., Dayton"),
        ],
        "faq": [
            ("Do you charge extra for nights and weekends?", "Our emergency rate is shown upfront before any work begins."),
            ("Do you offer financing?", "Yes. New systems can be financed with approved credit."),
            ("Which brands do you service?", "All major brands, including Trane, Carrier, Lennox, Goodman, and Rheem."),
        ],
        "hours": "Open 24/7 for emergencies",
    },
    {
        "slug": "roofing",
        "industry": "Roofing & Contractors",
        "keyword": "Roofing Contractor Website Example",
        "layout": "Call Now",
        "name": "Ironwood Roofing & Construction",
        "emoji": "🏠",
        "brand": "#37474f", "dark": "#1c2529", "accent": "#ff8f00", "accent_ink": "#2a1600", "bg": "#f5f6f7",
        "h1": "Roofs built to protect your family for decades.",
        "tagline": "Roof replacement, storm damage repair, and insurance claim help from a local, family-owned contractor.",
        "cta": "Get a Free Inspection",
        "badges": ["Free roof inspections", "Insurance claim help", "Lifetime warranty options"],
        "services": [
            ("🏠", "Roof Replacement", "Architectural shingles and metal roofs installed by our own crews.", "Free estimate"),
            ("⛈️", "Storm Damage", "Hail and wind damage repair, and we work directly with your insurance.", "Free inspection"),
            ("🔨", "Roof Repair", "Leaks, missing shingles, and flashing fixed fast.", "From $295"),
            ("🌧️", "Gutters", "Seamless gutters and gutter guards in 20+ colors.", "From $8/ft"),
            ("🪟", "Siding & Windows", "Vinyl siding, trim, and energy-efficient windows.", "Free estimate"),
            ("🏗️", "Remodels", "Additions, decks, and remodeling projects.", "Custom quote"),
        ],
        "why": [("25 yrs", "in business"), ("3,500+", "roofs installed"), ("Lifetime", "warranty options"), ("GAF", "certified")],
        "gallery": [("🏡", "Full replacement"), ("🌩️", "Storm repair"), ("🔩", "Metal roof"), ("🪜", "Gutter install")],
        "areas": ["Cleveland", "Chattanooga", "Athens", "Dalton, GA", "Ooltewah", "Collegedale"],
        "reviews": [
            ("They handled everything with our insurance. New roof in two days.", "Brenda K., Collegedale"),
            ("Crew cleaned up every nail. Looks fantastic.", "Steve G., Cleveland"),
            ("Honest inspection. They told us we only needed a repair, not a new roof.", "Linda F., Athens"),
        ],
        "faq": [
            ("Will insurance pay for my roof?", "If you have storm damage, often yes. We inspect for free and help with your claim."),
            ("How long does a roof replacement take?", "Most homes are done in 1–2 days."),
            ("Do you offer financing?", "Yes, with low monthly payment options."),
        ],
        "hours": "Mon–Fri 7am–6pm · Sat by appointment",
    },
    {
        "slug": "house-cleaning",
        "industry": "House Cleaning",
        "keyword": "House Cleaning Website Example",
        "layout": "Book Now",
        "name": "Sparkle & Shine Cleaning Co.",
        "emoji": "🧽",
        "brand": "#00897b", "dark": "#005a50", "accent": "#ffb4c2", "accent_ink": "#4a0f1c", "bg": "#f3faf8",
        "h1": "Come home to a spotless house.",
        "tagline": "Trusted, background-checked cleaners for weekly, biweekly, and move-out cleaning. Book online in 60 seconds.",
        "cta": "Book a Cleaning",
        "badges": ["Background-checked team", "Supplies included", "Happiness guarantee"],
        "services": [
            ("🏡", "Standard Clean", "Kitchens, baths, dusting, floors, and more, every visit.", "From $120"),
            ("✨", "Deep Clean", "Top-to-bottom detail cleaning, perfect for a first visit.", "From $220"),
            ("📦", "Move-In / Move-Out", "Get your deposit back with a full empty-home clean.", "From $280"),
            ("🏢", "Office Cleaning", "After-hours cleaning for small offices.", "Custom quote"),
            ("🪟", "Windows & Blinds", "Inside windows, sills, and blinds add-on.", "+$45"),
            ("🧺", "Laundry & Linens", "Wash, fold, and fresh bed linens add-on.", "+$30"),
        ],
        "menu": [
            ("Regular Cleaning", [("1–2 bedrooms", "Weekly or biweekly", "$120"), ("3 bedrooms", "Weekly or biweekly", "$150"), ("4+ bedrooms", "Weekly or biweekly", "$185")]),
            ("One-Time Cleaning", [("Deep clean", "Recommended first visit", "$220+"), ("Move-out clean", "Empty home", "$280+"), ("Post-party clean", "Next-day service", "$160+")]),
        ],
        "why": [("1,200+", "happy homes"), ("4.9★", "average rating"), ("100%", "insured team"), ("24 hr", "re-clean promise")],
        "gallery": [("🍽️", "Sparkling kitchen"), ("🛁", "Fresh bathroom"), ("🛏️", "Tidy bedroom"), ("🪴", "Clean living room")],
        "areas": ["Cleveland", "Chattanooga", "Ooltewah", "Collegedale", "Athens"],
        "reviews": [
            ("Same cleaner every time and she's wonderful. My house smells amazing.", "Rachel D., Ooltewah"),
            ("Booking online took one minute. So easy.", "Chris L., Cleveland"),
            ("Got our full deposit back thanks to their move-out clean.", "Jasmine T., Chattanooga"),
        ],
        "faq": [
            ("Do I need to provide supplies?", "No. We bring everything, including eco-friendly products on request."),
            ("Will I get the same cleaner?", "Yes, we assign a regular cleaner for recurring visits."),
            ("What if I'm not happy?", "Tell us within 24 hours and we'll come back and re-clean for free."),
        ],
        "hours": "Mon–Fri 8am–5pm",
    },
    {
        "slug": "barber-salon",
        "industry": "Barbers & Salons",
        "keyword": "Barber Shop Website Example",
        "layout": "Book Now",
        "name": "Main Street Barber Co.",
        "emoji": "💈",
        "brand": "#1a1a1a", "dark": "#000000", "accent": "#d4a24c", "accent_ink": "#1a1206", "bg": "#f7f5f1",
        "h1": "Sharp cuts. Hot towels. Good conversation.",
        "tagline": "Classic and modern cuts, fades, and beard trims. Walk in or book your chair online.",
        "cta": "Book Your Chair",
        "badges": ["Walk-ins welcome", "Online booking", "Free parking"],
        "services": [
            ("✂️", "Classic Cut", "Scissor or clipper cut with a hot-towel neck shave.", "$25"),
            ("💈", "Skin Fade", "Clean, detailed fade styled exactly how you like it.", "$30"),
            ("🧔", "Beard Trim", "Shape, line-up, and hot towel finish.", "$15"),
            ("🪒", "Hot Towel Shave", "Traditional straight-razor shave.", "$35"),
            ("👦", "Kids Cut", "Ages 12 and under.", "$18"),
            ("⭐", "The Works", "Cut, beard, and hot towel shave.", "$55"),
        ],
        "menu": [
            ("Haircuts", [("Classic cut", "Includes neck shave", "$25"), ("Skin fade", "Detailed blend", "$30"), ("Kids cut", "12 and under", "$18")]),
            ("Beard & Shave", [("Beard trim", "Shape and line-up", "$15"), ("Hot towel shave", "Straight razor", "$35"), ("The Works", "Cut + beard + shave", "$55")]),
        ],
        "why": [("15 yrs", "on Main Street"), ("4", "master barbers"), ("4.8★", "Google rating"), ("7 days", "a week")],
        "gallery": [("💇", "Skin fade"), ("🧔", "Beard shape-up"), ("🪒", "Hot towel shave"), ("😎", "Classic pompadour")],
        "areas": ["Downtown Cleveland", "Charleston", "Calhoun", "Athens"],
        "reviews": [
            ("Best fade in town, hands down. Booking online is a game changer.", "Marcus J."),
            ("Took my son for his first cut. They were so patient with him.", "Amanda B."),
            ("Hot towel shave was the most relaxing 30 minutes of my week.", "Derek W."),
        ],
        "faq": [
            ("Do you take walk-ins?", "Yes. Booking online guarantees your time, but walk-ins are always welcome."),
            ("Do you accept cards?", "Yes. All major cards, Apple Pay, and cash."),
            ("How early should I arrive?", "Five minutes before your appointment is perfect."),
        ],
        "hours": "Mon–Sat 9am–7pm · Sun 11am–4pm",
    },
    {
        "slug": "restaurant",
        "industry": "Restaurants & Food Trucks",
        "keyword": "Restaurant Website Example",
        "layout": "Menu & Visit",
        "name": "Smoky Ridge BBQ",
        "emoji": "🍖",
        "brand": "#8d2b0b", "dark": "#4e1604", "accent": "#ffb703", "accent_ink": "#2b1600", "bg": "#fbf6ef",
        "h1": "Slow-smoked Tennessee barbecue, made fresh daily.",
        "tagline": "Hickory-smoked brisket, pulled pork, ribs, and homemade sides. Dine in, carry out, or book us to cater.",
        "cta": "See the Menu",
        "badges": ["Dine in & carry out", "Catering available", "Family owned"],
        "services": [
            ("🍽️", "Dine In", "Grab a seat in our family-friendly dining room.", "Open daily"),
            ("🛍️", "Carry Out", "Call ahead and your order will be hot and ready.", "Call to order"),
            ("🎉", "Catering", "Weddings, parties, and office lunches from 20 to 500 guests.", "From $14/person"),
            ("🚚", "Food Truck", "Find our truck at events around town every weekend.", "See schedule"),
            ("🎁", "Gift Cards", "The perfect gift for barbecue lovers.", "Any amount"),
            ("🥧", "Family Packs", "Feed 4–6 people with meat, sides, and rolls.", "From $49"),
        ],
        "menu": [
            ("Smoked Meats", [("Pulled pork plate", "With 2 sides and cornbread", "$13.99"), ("Brisket plate", "Sliced or chopped, 2 sides", "$16.99"), ("Half rack ribs", "Dry rub or sauced, 2 sides", "$18.99")]),
            ("Sides & Sweets", [("Mac & cheese", "Baked, three cheeses", "$3.99"), ("Smoked baked beans", "With burnt ends", "$3.99"), ("Banana pudding", "Homemade daily", "$4.49")]),
        ],
        "why": [("14 hrs", "smoked low & slow"), ("Hickory", "wood only"), ("Daily", "homemade sides"), ("500", "guest catering")],
        "gallery": [("🥩", "Sliced brisket"), ("🍖", "Smoked ribs"), ("🧀", "Mac & cheese"), ("🍌", "Banana pudding")],
        "areas": ["Cleveland", "Charleston", "Calhoun", "Chattanooga catering"],
        "reviews": [
            ("Best brisket I've had outside of Texas. The banana pudding is unreal.", "Greg M."),
            ("They catered our wedding for 200 and everyone raved.", "Hannah & Luke"),
            ("Friendly staff, huge portions, fair prices. We come every Friday.", "The Watson family"),
        ],
        "faq": [
            ("Do you take call-ahead orders?", "Yes! Call us and your food will be ready for pickup."),
            ("How far ahead should I book catering?", "Two weeks is best, but call us. We can often do less."),
            ("Do you have gluten-free options?", "Our meats and most sides are gluten-free. Just ask."),
        ],
        "hours": "Tue–Sat 11am–8pm · Sun 11am–3pm",
    },
    {
        "slug": "law-firm",
        "industry": "Law, Accounting & Insurance",
        "keyword": "Law Firm Website Example",
        "layout": "Trust & Expertise",
        "name": "Harper & Lowe, Attorneys at Law",
        "emoji": "⚖️",
        "brand": "#1f3a5f", "dark": "#0f2038", "accent": "#c9a227", "accent_ink": "#1d1700", "bg": "#f6f7f9",
        "h1": "Experienced legal help when it matters most.",
        "tagline": "Personal injury, family law, and estate planning. Free consultations, and we answer every call.",
        "cta": "Free Consultation",
        "badges": ["Free consultations", "30+ years combined", "No fee unless we win*"],
        "services": [
            ("🚗", "Personal Injury", "Car accidents, slip and falls, and workplace injuries. No fee unless we win.", "Free consultation"),
            ("👨‍👩‍👧", "Family Law", "Divorce, custody, and child support handled with care and discretion.", "Free consultation"),
            ("📜", "Wills & Estates", "Wills, trusts, and powers of attorney to protect your family.", "Flat-fee options"),
            ("🏠", "Real Estate", "Closings, deeds, and property disputes.", "Flat-fee options"),
            ("💼", "Small Business", "Forming LLCs, contracts, and business disputes.", "Free consultation"),
            ("🧾", "Probate", "Guiding families through the probate process.", "Free consultation"),
        ],
        "why": [("30+", "years combined"), ("1,000+", "clients helped"), ("Free", "consultations"), ("Same day", "call back")],
        "bio": ("Meet the attorneys", "Sarah Harper and David Lowe have served East Tennessee families for over 30 years combined. They believe legal help should be honest, understandable, and personal. You'll always speak with an attorney, not a call center."),
        "areas": ["Bradley County", "Hamilton County", "McMinn County", "Polk County", "Meigs County"],
        "reviews": [
            ("They explained everything in plain English and fought hard for me.", "Former injury client"),
            ("Made a hard divorce as smooth as it could be. Truly caring.", "Family law client"),
            ("Our wills were done quickly and the flat fee was very fair.", "Estate planning client"),
        ],
        "faq": [
            ("How much does a consultation cost?", "Your first consultation is free and confidential."),
            ("What does 'no fee unless we win' mean?", "For injury cases, you pay attorney fees only if we recover money for you."),
            ("Can we meet by phone or video?", "Yes. We meet in person, by phone, or by video, whichever is easier for you."),
        ],
        "hours": "Mon–Fri 8:30am–5pm · Evenings by appointment",
    },
]

PHONE = "(423) 555-0142"
PHONE_TEL = "+14235550142"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def services_html(site):
    cards = "".join(
        f"""
          <article class="d-card"><div class="d-ico">{ico}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><p class="d-price">{esc(p)}</p></article>"""
        for ico, t, d, p in site["services"]
    )
    title = {"Menu & Visit": "What we offer", "Trust & Expertise": "Practice areas"}.get(site["layout"], "Our services")
    return f"""
    <section class="d-section" id="services">
      <div class="wrap">
        <div class="d-head"><h2>{title}</h2><p>Clear prices and friendly, reliable service.</p></div>
        <div class="d-grid">{cards}
        </div>
      </div>
    </section>"""


def why_html(site):
    items = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in site["why"])
    return f"""
    <section class="d-section d-section-alt">
      <div class="wrap"><div class="d-why">{items}</div></div>
    </section>"""


def gallery_html(site):
    if "gallery" not in site:
        return ""
    tiles = "".join(f'<div class="d-tile">{e}<small>{esc(t)}</small></div>' for e, t in site["gallery"])
    return f"""
    <section class="d-section" id="work">
      <div class="wrap">
        <div class="d-head"><h2>Recent work</h2><p>Real photos of your work go here, which is one of the best ways to win new customers.</p></div>
        <div class="d-gallery">{tiles}</div>
      </div>
    </section>"""


def menu_html(site):
    if "menu" not in site:
        return ""
    cols = ""
    for heading, rows in site["menu"]:
        r = "".join(
            f'<div class="d-menu-row"><div>{esc(n)}<span>{esc(d)}</span></div><b>{esc(p)}</b></div>' for n, d, p in rows
        )
        cols += f"<div><h3>{esc(heading)}</h3>{r}</div>"
    title = "Menu" if site["layout"] == "Menu & Visit" else "Prices"
    booking = ""
    if site["layout"] == "Book Now":
        booking = """
        <div class="d-head" style="margin-top:48px"><h2>Pick a time</h2><p>Choose an opening and we'll confirm by text.</p></div>
        <div class="d-slots"><button type="button">Tue 9:00</button><button type="button">Tue 11:30</button><button type="button">Wed 1:00</button><button type="button">Thu 10:00</button><button type="button">Fri 3:30</button><button type="button">Sat 9:30</button></div>
        <p style="text-align:center"><a class="d-btn d-btn-brand" href="#contact">Book This Time</a></p>"""
    return f"""
    <section class="d-section d-section-alt" id="menu">
      <div class="wrap">
        <div class="d-head"><h2>{title}</h2><p>Simple, honest pricing. No surprises.</p></div>
        <div class="d-menu">{cols}</div>{booking}
      </div>
    </section>"""


def bio_html(site):
    if "bio" not in site:
        return ""
    t, d = site["bio"]
    return f"""
    <section class="d-section d-section-alt" id="about">
      <div class="wrap d-split">
        <div class="d-portrait">👩‍⚖️</div>
        <div><h2>{esc(t)}</h2><p>{esc(d)}</p><a class="d-btn d-btn-brand" href="#contact">Schedule a Free Consultation</a></div>
      </div>
    </section>"""


def reviews_html(site):
    cards = "".join(
        f'<div class="d-review"><div class="stars">★★★★★</div><p>"{esc(q)}"</p><b>— {esc(w)}</b></div>' for q, w in site["reviews"]
    )
    areas = "".join(f"<li>{esc(a)}</li>" for a in site["areas"])
    return f"""
    <section class="d-section" id="reviews">
      <div class="wrap">
        <div class="d-head"><h2>What customers say</h2></div>
        <div class="d-grid">{cards}</div>
        <p class="d-sample-note">Sample reviews for this example. Your real Google reviews can show here automatically.</p>
        <div class="d-head" style="margin-top:56px"><h2>Areas we serve</h2></div>
        <ul class="d-areas">{areas}</ul>
      </div>
    </section>"""


def faq_html(site):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in site["faq"])
    return f"""
    <section class="d-section d-section-alt" id="faq">
      <div class="wrap">
        <div class="d-head"><h2>Questions</h2></div>
        <div class="d-faq">{items}</div>
      </div>
    </section>"""


def contact_html(site):
    select = "".join(f"<option>{esc(t)}</option>" for _, t, _, _ in site["services"])
    return f"""
    <section class="d-section d-contact" id="contact">
      <div class="wrap d-split">
        <div>
          <h2>{esc(site["cta"])}</h2>
          <p>Tell us what you need and we'll get back to you fast, usually the same day.</p>
          <ul class="d-info">
            <li>📞 <a href="tel:{PHONE_TEL}" style="color:#fff">{PHONE}</a></li>
            <li>🕒 {esc(site["hours"])}</li>
            <li>📍 Serving {esc(", ".join(site["areas"][:3]))} and nearby</li>
          </ul>
        </div>
        <form class="d-form">
          <label for="n">Name</label><input id="n" required />
          <label for="p">Phone</label><input id="p" type="tel" required />
          <label for="s">Service</label><select id="s">{select}</select>
          <label for="m">Details</label><textarea id="m"></textarea>
          <button class="d-btn d-btn-accent" type="submit">{esc(site["cta"])}</button>
          <p class="d-form-msg" aria-live="polite"></p>
        </form>
      </div>
    </section>"""


def demo_page(site):
    style = (
        f"--brand:{site['brand']};--brand-dark:{site['dark']};--accent:{site['accent']};"
        f"--accent-ink:{site['accent_ink']};--bg:{site['bg']};"
    )
    title = f"{site['keyword']}: {site['name']} | Stakich Websites"
    desc = f"See a real example of a {site['industry'].lower()} website built by Stakich Websites: mobile-friendly, fast, and designed to bring in calls."
    path = f"/examples/{site['slug']}/"
    order = [services_html, why_html, menu_html, bio_html, gallery_html, reviews_html, faq_html, contact_html]
    body = "".join(fn(site) for fn in order)
    nav_link = {"Menu & Visit": ("#menu", "Menu"), "Book Now": ("#menu", "Prices")}.get(site["layout"], ("#work", "Our Work"))
    if site["layout"] == "Trust & Expertise":
        nav_link = ("#about", "Attorneys")
    badges = "".join(f"<li>{esc(b)}</li>" for b in site["badges"])
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{SITE}{path}" />
    <link rel="icon" href="/assets/icon.svg" type="image/svg+xml" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:image" content="{SITE}/assets/og-image.png" />
    <meta property="og:url" content="{SITE}{path}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/examples/demo.css?v=1" />
  </head>
  <body style="{style}">
    <div class="demo-banner">Example {esc(site["industry"].lower())} website by Stakich Websites.<a href="/#contact">Get one like this →</a></div>
    <header class="d-header">
      <div class="wrap">
        <a class="d-logo" href="#top"><i>{site["emoji"]}</i>{esc(site["name"])}</a>
        <nav class="d-nav">
          <a href="#services">Services</a>
          <a href="{nav_link[0]}">{nav_link[1]}</a>
          <a href="#reviews">Reviews</a>
          <a class="d-btn d-btn-brand" href="tel:{PHONE_TEL}">📞 {PHONE}</a>
        </nav>
      </div>
    </header>
    <main id="top">
      <section class="d-hero" data-emoji="{site["emoji"]}">
        <div class="wrap">
          <h1>{esc(site["h1"])}</h1>
          <p class="tagline">{esc(site["tagline"])}</p>
          <div class="d-hero-actions">
            <a class="d-btn d-btn-accent" href="#contact">{esc(site["cta"])}</a>
            <a class="d-btn d-btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a>
          </div>
          <ul class="d-badges">{badges}</ul>
        </div>
      </section>{body}
    </main>
    <footer class="d-footer">
      <div class="wrap">
        <div><b>{esc(site["name"])}</b><br />{PHONE} · {esc(site["hours"])}</div>
        <div>Example website designed by <a href="/">Stakich Websites</a>. <a href="/examples/">See more examples</a></div>
      </div>
    </footer>
    <a class="d-btn d-btn-accent d-sticky" href="tel:{PHONE_TEL}">📞 Call Now</a>
    <script src="/examples/demo.js?v=1" defer></script>
  </body>
</html>
"""


def gallery_page():
    cards = ""
    for s in SITES:
        cards += f"""
            <a class="example-card" href="/examples/{s['slug']}/">
              <div class="example-thumb" style="background:linear-gradient(140deg,{s['dark']},{s['brand']})">
                <div class="thumb-bar"><i></i><i></i><i></i></div>
                <span class="thumb-emoji">{s['emoji']}</span>
                <strong>{esc(s['name'])}</strong>
                <span>{esc(s['tagline'][:70])}…</span>
              </div>
              <div class="example-body">
                <span class="layout-tag">{esc(s['layout'])} layout</span>
                <h3>{esc(s['industry'])} Website</h3>
                <p>{esc(LAYOUT_BLURB[s['layout']])}</p>
                <span class="example-link">View example →</span>
              </div>
            </a>"""
    html = head(
        "Example Websites for Small Businesses | Stakich Websites",
        "See example websites for lawn care, pressure washing, HVAC, roofing, cleaning, barbers, restaurants, and law firms, all built by Stakich Websites.",
        "/examples/",
    )
    html += topbar("examples")
    html += page_hero(
        "Example websites for small businesses",
        "Click any example to see the full website, exactly how your customers would see it on a phone or computer. Each one is built around how that type of customer buys.",
        "Examples",
    )
    html += f"""      <section class="section">
        <div class="container">
          <div class="example-grid">{cards}
          </div>
          {share_mount("Share these examples")}
        </div>
      </section>
"""
    html += cta_band()
    html += footer()
    html += scripts()
    (OUT / "index.html").write_text(html, encoding="utf-8")


LAYOUT_BLURB = {
    "Call Now": "Big tap-to-call buttons, a free quote form, service areas, and before-and-after photos, built to make the phone ring.",
    "Book Now": "A clear price list and an easy booking section, so customers can pick a time without calling.",
    "Menu & Visit": "Menu with prices, hours, location, and catering, everything hungry customers look for first.",
    "Trust & Expertise": "Credentials, attorney bios, practice areas, and a free consultation form that builds trust before the first call.",
}


def build():
    for s in SITES:
        d = OUT / s["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(demo_page(s), encoding="utf-8")
        print("wrote examples/" + s["slug"])
    gallery_page()
    print("wrote examples/index.html")


if __name__ == "__main__":
    build()
