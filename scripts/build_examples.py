"""Builds the example websites and the examples gallery.

Run from the project root:  python3 scripts/build_examples.py
"""
from pathlib import Path

from example_extras import EXTRAS
from icons import icon
from common import HTTPS_REDIRECT, JS_V, SITE, cta_band, footer, head, page_hero, scripts, share_mount, topbar

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
    {
        "slug": "nursing-home",
        "industry": "Nursing Home & Senior Care",
        "keyword": "Nursing Home Website Example",
        "layout": "Tour & Admissions",
        "name": "Rosewood Hills Health & Rehabilitation",
        "emoji": "🌷",
        "brand": "#2f5d62", "dark": "#1d3c40", "accent": "#e8a87c", "accent_ink": "#3a1f0d", "bg": "#f7f5f2",
        "h1": "Compassionate nursing care that feels like home.",
        "tagline": "Skilled nursing, short-term rehab, and long-term care for your loved one. Schedule a tour or talk with admissions today.",
        "cta": "Schedule a Tour",
        "badges": ["24/7 licensed nurses", "Medicare & Medicaid accepted", "Tours 7 days a week"],
        "services": [
            ("🩺", "Skilled Nursing", "Around-the-clock care from licensed nurses and certified nursing assistants.", "Medicare & Medicaid accepted"),
            ("🦵", "Short-Term Rehab", "Physical, occupational, and speech therapy to help residents get back home after a hospital stay.", "Therapy 6 days a week"),
            ("🏡", "Long-Term Care", "A safe, caring home with help with daily living, meals, and medications.", "Private & semi-private rooms"),
            ("🧠", "Memory Care", "A secure, calm setting with staff trained in Alzheimer's and dementia care.", "Secure neighborhood"),
            ("🛏️", "Respite Care", "Short stays that give family caregivers a well-earned break.", "Stays from 3 days"),
            ("🕊️", "Hospice Support", "Comfort-focused care in partnership with local hospice providers.", "Family support included"),
        ],
        "why": [("24/7", "licensed nursing"), ("6 days", "of therapy a week"), ("7 days", "tours available"), ("1 call", "to start admissions")],
        "admissions": [
            ("Call or request a tour", "Talk with our admissions team. We answer questions and explain your options."),
            ("Visit and meet the team", "Tour rooms, dining, and therapy, and meet the nurses who will care for your loved one."),
            ("Insurance check", "We verify Medicare, Medicaid, VA, or private insurance benefits for you, at no cost."),
            ("Move-in day", "We coordinate with the hospital or doctor and help make move-in calm and simple."),
        ],
        "payers": ["Medicare", "Medicaid", "VA benefits", "Private insurance", "Long-term care insurance", "Private pay"],
        "daily": ["Chef-prepared meals & snacks", "Daily activities & music", "Faith services", "Beauty & barber shop", "Garden courtyard", "Family video calls"],
        "bio": ("Meet our care team", "Our nurses, therapists, and aides are led by a Director of Nursing with more than 20 years of experience. Many of our team members have been here for over a decade, so residents see familiar, caring faces every day.", "👩‍⚕️", "Talk With Admissions"),
        "gallery_title": "Take a look inside",
        "gallery_note": "Real photos of your rooms, dining, and grounds go here. Families want to see where their loved one will live.",
        "gallery": [("🛏️", "Private rooms"), ("🍽️", "Dining room"), ("🌳", "Garden courtyard"), ("🏋️", "Therapy gym"), ("🎨", "Activity room"), ("💇", "Beauty salon")],
        "reviews_title": "What families say",
        "areas": ["Cleveland", "Chattanooga", "Athens", "Ooltewah", "Charleston", "Calhoun"],
        "reviews": [
            ("The nurses treated my mother like their own family. We always felt welcome.", "Resident's daughter"),
            ("Dad came for rehab after his hip surgery and went home stronger than before.", "Rehab patient's son"),
            ("They answered every question and helped us with Medicaid. A huge relief.", "Family member"),
        ],
        "faq": [
            ("Do you accept Medicare and Medicaid?", "Yes. We accept Medicare, Medicaid, VA benefits, most private insurance, and private pay. We'll verify coverage for you."),
            ("What are visiting hours?", "Families are welcome every day. We ask visitors to sign in at the front desk."),
            ("What should we bring on move-in day?", "Comfortable clothing, toiletries, a few favorite photos or keepsakes, and a list of medications. We'll send you a full checklist."),
            ("How quickly can my loved one be admitted?", "Often within 24–48 hours of a hospital discharge, depending on bed availability."),
            ("Are you hiring?", "Yes. We're always looking for caring nurses, CNAs, and support staff. Apply online in a few minutes."),
        ],
        "hours": "Admissions 7 days, 8am–7pm · Nursing care 24/7",
        "form_label": "Type of care",
        "form_title": "Schedule a tour or ask a question",
    },
]

PHONE = "(423) 555-0142"
PHONE_TEL = "+14235550142"


SERVICE_ICONS = {
    "Weekly Mowing": "tractor", "Leaf Cleanup": "leaf", "Hedge Trimming": "shrub", "Mulch & Beds": "flower-2",
    "Aeration & Seeding": "sprout", "Commercial Lawns": "building",
    "House Washing": "house", "Driveways & Sidewalks": "car", "Deck & Fence": "fence", "Roof Soft Wash": "spray-can",
    "Patios & Pavers": "brick-wall", "Commercial": "store",
    "AC Repair": "snowflake", "Furnace & Heat Pumps": "flame", "Plumbing Repair": "wrench", "Water Heaters": "shower-head",
    "Maintenance Plans": "calendar-check", "New Construction": "construction",
    "Roof Replacement": "house", "Storm Damage": "cloud-lightning", "Roof Repair": "hammer", "Gutters": "cloud-rain",
    "Siding & Windows": "app-window", "Remodels": "ruler",
    "Standard Clean": "house", "Deep Clean": "sparkles", "Move-In / Move-Out": "package", "Office Cleaning": "building",
    "Windows & Blinds": "blinds", "Laundry & Linens": "shirt",
    "Classic Cut": "scissors", "Skin Fade": "scissors-line-dashed", "Beard Trim": "brush", "Hot Towel Shave": "droplets",
    "Kids Cut": "baby", "The Works": "sparkles",
    "Dine In": "utensils-crossed", "Carry Out": "shopping-bag", "Catering": "chef-hat", "Food Truck": "truck",
    "Gift Cards": "gift", "Family Packs": "users",
    "Personal Injury": "car", "Family Law": "users", "Wills & Estates": "scroll-text", "Real Estate": "house",
    "Small Business": "briefcase", "Probate": "file-text",
    "Skilled Nursing": "stethoscope", "Short-Term Rehab": "activity", "Long-Term Care": "house-heart",
    "Memory Care": "brain", "Respite Care": "bed", "Hospice Support": "heart-handshake",
}

LOGO_ICONS = {
    "lawn-care": "leaf", "pressure-washing": "droplets", "hvac-plumbing": "wrench", "roofing": "house",
    "house-cleaning": "sparkles", "barber-salon": "scissors", "restaurant": "flame", "law-firm": "scale",
    "nursing-home": "house-heart",
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def services_html(site):
    cards = "".join(
        f"""
          <article class="d-card"><div class="d-ico">{icon(SERVICE_ICONS[t])}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><p class="d-price">{esc(p)}</p></article>"""
        for ico, t, d, p in site["services"]
    )
    title = {"Menu & Visit": "What we offer", "Trust & Expertise": "Practice areas", "Tour & Admissions": "Care we provide"}.get(site["layout"], "Our services")
    sub = "Every level of care, under one roof." if site["layout"] == "Tour & Admissions" else "Clear prices and friendly, reliable service."
    return f"""
    <section class="d-section" id="services">
      <div class="wrap">
        <div class="d-head"><h2>{title}</h2><p>{sub}</p></div>
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


PHOTO_CAPTIONS = {
    "lawn-care": ["Crisp edging on every visit", "Hedge and shrub trimming", "Fall leaf cleanup"],
    "pressure-washing": ["House washing", "Deck restoration", "Patios that look brand new"],
    "hvac-plumbing": ["Leak and drain repair", "Water heater installs", "Friendly, on-time service"],
    "roofing": ["A finished roof replacement", "Free roof inspections", "Clean, fast tear-offs"],
    "house-cleaning": ["Living rooms, vacuumed and dusted", "Sparkling bathrooms", "A friendly, trusted team"],
    "barber-salon": ["Hot towel straight razor shaves", "Our shop", "Beard trims and shaping"],
    "restaurant": ["Smoked low and slow on site", "Come hungry, stay a while", "Pulled pork sandwich and sides"],
    "law-firm": ["Personal attention for every client", "Our office", "Wills and estate planning"],
    "nursing-home": ["Therapy gym and rehab", "Comfortable private rooms", "Garden courtyard"],
}


def img(site, kind):
    return f"/examples/img/{site['slug']}/{kind}.jpg"


def gallery_html(site):
    if site["slug"] in PHOTO_CAPTIONS:
        figs = "".join(
            f'<figure class="d-photo"><img src="{img(site, f"g{i}")}" alt="{esc(c)}" loading="lazy" width="900" height="675" /><figcaption>{esc(c)}</figcaption></figure>'
            for i, c in enumerate(PHOTO_CAPTIONS[site["slug"]], 1)
        )
        return f"""
    <section class="d-section" id="work">
      <div class="wrap">
        <div class="d-head"><h2>{esc(site.get("gallery_title", "Recent work"))}</h2><p>{esc(site.get("gallery_note", "Photos of your real jobs go here, one of the best ways to win new customers."))}</p></div>
        <div class="d-photos">{figs}</div>
      </div>
    </section>"""
    if "gallery" not in site:
        return ""
    tiles = "".join(f'<div class="d-tile">{e}<small>{esc(t)}</small></div>' for e, t in site["gallery"])
    return f"""
    <section class="d-section" id="work">
      <div class="wrap">
        <div class="d-head"><h2>{esc(site.get("gallery_title", "Recent work"))}</h2><p>{esc(site.get("gallery_note", "Real photos of your work go here, which is one of the best ways to win new customers."))}</p></div>
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
    t, d, portrait, button = (*site["bio"], "👩‍⚖️", "Schedule a Free Consultation")[:4]
    return f"""
    <section class="d-section d-section-alt" id="about">
      <div class="wrap d-split">
        <div class="d-portrait">{f'<img src="{img(site, "portrait")}" alt="{esc(t)}" loading="lazy" width="600" height="600" />' if (OUT / "img" / site["slug"] / "portrait.jpg").exists() else portrait}</div>
        <div><h2>{esc(t)}</h2><p>{esc(d)}</p><a class="d-btn d-btn-brand" href="#contact">{esc(button)}</a></div>
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
        <div class="d-head"><h2>{esc(site.get("reviews_title", "What customers say"))}</h2></div>
        <div class="d-grid">{cards}</div>
        <p class="d-sample-note">Sample reviews for this example. Your real Google reviews can show here automatically.</p>
        <div class="d-head" style="margin-top:56px"><h2>Areas we serve</h2></div>
        <ul class="d-areas">{areas}</ul>
      </div>
    </section>"""


def admissions_html(site):
    if "admissions" not in site:
        return ""
    steps = "".join(
        f'<article class="d-card"><div class="d-ico">{i}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for i, (t, d) in enumerate(site["admissions"], 1)
    )
    payers = "".join(f"<li>{esc(p)}</li>" for p in site["payers"])
    daily = "".join(f"<li>{esc(p)}</li>" for p in site["daily"])
    return f"""
    <section class="d-section" id="admissions">
      <div class="wrap">
        <div class="d-head"><h2>Admissions made simple</h2><p>Four easy steps. We guide your family through every one.</p></div>
        <div class="d-grid d-steps">{steps}</div>
        <div class="d-split" style="margin-top:56px;align-items:start">
          <div><h3>Insurance &amp; payment we accept</h3><ul class="d-areas">{payers}</ul></div>
          <div><h3>Daily life here</h3><ul class="d-areas">{daily}</ul></div>
        </div>
        <div class="d-careers">
          <div><h3>Join our caring team</h3><p>Now hiring RNs, LPNs, CNAs, and dietary staff. Competitive pay and great benefits.</p></div>
          <a class="d-btn d-btn-brand" href="#contact">Apply Online</a>
        </div>
      </div>
    </section>"""


def offer_html(site):
    offer = EXTRAS.get(site["slug"], {}).get("offer")
    if not offer:
        return ""
    head, text = offer
    return f"""
    <section class="d-offer">
      <div class="wrap">
        <div class="d-offer-box">
          <div class="d-offer-ico">{icon("gift")}</div>
          <div><p class="d-offer-tag">Special offer</p><h2>{esc(head)}</h2><p>{esc(text)}</p></div>
          <div class="d-offer-actions"><a class="d-btn d-btn-accent" href="tel:{PHONE_TEL}">{icon("phone")} Call</a><a class="d-btn d-btn-ghost" href="sms:{PHONE_TEL}">{icon("message-circle")} Text</a></div>
        </div>
      </div>
    </section>"""


def about_html(site):
    about = EXTRAS.get(site["slug"], {}).get("about")
    if not about:
        return ""
    title, paras, points = about
    text = "".join(f"<p>{esc(t)}</p>" for t in paras)
    checks = "".join(f"<li>{icon('circle-check')}<span>{esc(t)}</span></li>" for t in points)
    return f"""
    <section class="d-section" id="story">
      <div class="wrap d-split d-about">
        <div><p class="d-eyebrow">About us</p><h2>{esc(title)}</h2>{text}<a class="d-btn d-btn-brand" href="#contact">{esc(site["cta"])}</a></div>
        <ul class="d-checks">{checks}</ul>
      </div>
    </section>"""


def steps_html(site):
    steps = EXTRAS.get(site["slug"], {}).get("steps")
    if not steps:
        return ""
    cards = "".join(
        f'<article class="d-card d-step"><span class="d-step-num">{i}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for i, (t, d) in enumerate(steps, 1)
    )
    return f"""
    <section class="d-section d-section-alt" id="how">
      <div class="wrap">
        <div class="d-head"><h2>How it works</h2><p>Simple, fast, and no pressure.</p></div>
        <div class="d-grid d-grid-3">{cards}</div>
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
          <h2>{esc(site.get("form_title", site["cta"]))}</h2>
          <p>Tell us what you need and we'll get back to you fast, usually the same day.</p>
          <ul class="d-info">
            <li>{icon("phone")} {PHONE}</li>
            <li class="d-reach"><a class="d-btn d-btn-accent" href="tel:{PHONE_TEL}">{icon("phone")} Call Us</a><a class="d-btn d-btn-ghost" href="sms:{PHONE_TEL}">{icon("message-circle")} Text Us</a></li>
            <li>{icon("clock")} {esc(site["hours"])}</li>
            <li>{icon("map-pin")} Serving {esc(", ".join(site["areas"][:3]))} and nearby</li>
          </ul>
        </div>
        <form class="d-form">
          <label for="n">Name</label><input id="n" required />
          <label for="p">Phone</label><input id="p" type="tel" required />
          <label for="s">{esc(site.get("form_label", "Service"))}</label><select id="s">{select}</select>
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
    title = f"{site['keyword']} | Stakich Websites"
    desc = f"See a real example of a {site['industry'].lower()} website built by Stakich Websites: mobile-friendly, fast, and designed to bring in calls."
    path = f"/examples/{site['slug']}/"
    order = [services_html, why_html, offer_html, about_html, steps_html, admissions_html, menu_html, bio_html, gallery_html, reviews_html, faq_html, contact_html]
    body = "".join(fn(site) for fn in order)
    nav_link = {"Menu & Visit": ("#menu", "Menu"), "Book Now": ("#menu", "Prices"), "Tour & Admissions": ("#admissions", "Admissions")}.get(site["layout"], ("#work", "Our Work"))
    if site["layout"] == "Trust & Expertise":
        nav_link = ("#about", "Attorneys")
    badges = "".join(f"<li>{esc(b)}</li>" for b in site["badges"])
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    {HTTPS_REDIRECT}
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="canonical" href="{SITE}{path}" />
    <link rel="icon" href="/assets/icon.svg" type="image/svg+xml" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:image" content="{SITE}{img(site, 'hero')}" />
    <link rel="preload" as="image" href="{img(site, 'hero')}" />
    <meta property="og:url" content="{SITE}{path}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/examples/demo.css?v=9" />
  </head>
  <body style="{style}">
    <div class="demo-banner">Example {esc(site["industry"].lower())} website by Stakich Websites.<a href="/#contact">Get one like this →</a></div>
    <header class="d-header">
      <div class="wrap">
        <a class="d-logo" href="#top"><i>{icon(LOGO_ICONS[site["slug"]])}</i>{esc(site["name"])}</a>
        <nav class="d-nav">
          <a href="#services">Services</a>
          <a href="{nav_link[0]}">{nav_link[1]}</a>
          <a href="#reviews">Reviews</a>
          <a class="d-btn d-btn-brand" href="tel:{PHONE_TEL}">{icon("phone")} {PHONE}</a>
        </nav>
      </div>
    </header>
    <main id="top">
      <section class="d-hero d-hero-photo" style="--hero:url({img(site, 'hero')})">
        <div class="wrap">
          <h1>{esc(site["h1"])}</h1>
          <p class="tagline">{esc(site["tagline"])}</p>
          <div class="d-hero-actions">
            <a class="d-btn d-btn-accent" href="#contact">{esc(site["cta"])}</a>
            <a class="d-btn d-btn-ghost" href="tel:{PHONE_TEL}">{icon("phone")} Call {PHONE}</a>
            <a class="d-btn d-btn-ghost" href="sms:{PHONE_TEL}">{icon("message-circle")} Text Us</a>
          </div>
          <ul class="d-badges">{badges}</ul>
        </div>
      </section>{body}
      <section class="d-share">
        <div class="wrap">
          {share_mount("Like this example? Share it with a business owner who needs a website", title="Example " + esc(site["industry"].lower()) + " website by Stakich Websites")}
        </div>
      </section>
    </main>
    <footer class="d-footer">
      <div class="wrap">
        <div><b>{esc(site["name"])}</b><br />{PHONE} · {esc(site["hours"])}</div>
        <div>Example website designed by <a href="/">Stakich Websites</a>. <a href="/examples/">See more examples</a></div>
      </div>
    </footer>
    <div class="d-sticky"><a class="d-btn d-btn-accent" href="tel:{PHONE_TEL}">{icon("phone")} Call Now</a><a class="d-btn d-btn-brand" href="sms:{PHONE_TEL}">{icon("message-circle")} Text Us</a></div>
    <script src="/examples/demo.js?v=1" defer></script>
    <script src="/share.js?v={JS_V}" defer></script>
  </body>
</html>
"""


def gallery_page():
    cards = ""
    for s in SITES[-1:] + SITES[:-1]:
        cards += f"""
            <a class="example-card" href="/examples/{s['slug']}/">
              <div class="example-thumb" style="background:linear-gradient(180deg,rgba(0,0,0,.05) 30%,{s['dark']}e6),url(/examples/img/{s['slug']}/hero.jpg) center/cover">
                <div class="thumb-bar"><i></i><i></i><i></i></div>
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
        "See example websites for nursing homes, lawn care, pressure washing, HVAC, roofing, cleaning, barbers, restaurants, and law firms by Stakich Websites.",
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
    "Tour & Admissions": "Levels of care, insurance accepted, a simple admissions guide, photo tour, and a schedule-a-tour form that reassures worried families. Also recruits staff.",
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
