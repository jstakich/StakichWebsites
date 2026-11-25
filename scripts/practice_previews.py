"""Content for Pro practice proposals published under /preview/."""
import re
from urllib.parse import quote_plus

from build_plan_examples import build_site


def article(topic, title, intro, paragraphs):
    return {
        "slug": topic,
        "date": "2026-11-25",
        "title": title,
        "excerpt": intro,
        "img": f"b-{topic}",
        "body": [("p", intro), *[(kind, text) for heading, copy in paragraphs
                                  for kind, text in (("h2", heading), ("p", copy))]],
    }


def preview(*, slug, name, owner, industry, city, address, phone, hours, colors,
            initials, headline, tagline, intro, biography, services, visit, faq, posts, photos,
            original, home_gallery, blog_photos, closed=(0, 6), short_day=None, hero_file="hero.jpg"):
    law = industry == "Law Firm"
    appointment = "Consultation" if law else "Appointment"
    request = "Request a consultation" if law else "Request an appointment"
    subject = "matter" if law else "visit"
    action = f"Request a {'consultation' if law else 'visit'}"
    services_label = "Practice Areas" if law else "Services"
    brand, dark, accent, bg = colors
    asset = f"/preview/{slug}/img/"
    image_keys = ("hero", "home-portrait", "portrait", "g1", "g2", "g3",
                  *(post["img"] for post in posts),
                  *(f"home-g{i}" for i in range(1, len(home_gallery) + 1)),
                  *(f"thumb-{post['img']}" for post in posts))
    photos = [*photos, *(photo for _, photo in home_gallery), *blog_photos]
    assert len(image_keys) == len(photos) == len(set(photos))
    google_maps = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{name}, {address}")
    return {
        "preview": True, "plan": "pro", "labeled": False, "slug": slug,
        "name": name, "industry": industry, "city": city, "address": address,
        "phone": phone, "phone_tel": "+1" + re.sub(r"\D", "", phone),
        "brand": brand, "dark": dark, "accent": accent, "accent_ink": "#151b20", "bg": bg,
        "logo_file": asset + "mark.svg", "initials": initials, "original": original,
        "hours": hours, "h1": headline, "tagline": tagline, "cta": "Contact the office",
        "badges": [services[0][1], services[1][1], city],
        "pages": [
            ("index", "Home"), ("services", services_label), ("about", "About"),
            ("work", "Plan Your Visit"), ("book", f"Request {appointment}"),
            ("reviews", "Reviews"), ("blog", "Blog"), ("areas", "Find Us"),
            ("faq", "FAQ"), ("contact", "Contact"),
        ],
        "nav": ["services", "about", "blog", "book"],
        "practice_photo_layout": True, "hero_size": (1440, 1080),
        "wide_hero": law,
        "image_map": {kind: asset + (hero_file if kind == "hero" else kind + ".jpg") for kind in image_keys},
        "photo_credits": [(kind.replace("-", " ").capitalize(), source)
                          for kind, (_, source) in zip(image_keys, photos)],
        "photo_assets": dict(zip(image_keys, (photo for photo, _ in photos))),
        "services_title": "How we can help" if law else "Care and services",
        "services_sub": intro, "services_intro": intro,
        "services_link": "Explore practice areas" if law else "Explore services",
        "services": [(icon, title, copy, "", points) for icon, title, copy, points in services],
        "svc_note": ("Questions about a service?", "Contact the office", "to discuss next steps."),
        "why": [(services[0][1], "Practice focus"), (services[1][1], "Services available"),
                (city, "Office location")],
        "owner": owner, "about_title": f"About {owner[0]}", "about": biography,
        "checks": ["Bring your questions", "Discuss your options", "Confirm next steps with the office"],
        "photos": visit,
        "home_gallery_captions": [caption for caption, _ in home_gallery],
        "home_gallery_title": {
            "Dentist": "A look at family dental care",
            "Chiropractor": "A look at chiropractic care",
            "Law Firm": "Preparing to meet with an attorney",
        }[industry],
        "work_sub": "Illustrative photos of what a visit can involve.",
        "work_intro": "What to know before you visit. The photos on this page are illustrative.",
        "steps": [
            ("Choose a reason for your visit", f"Start with the service that best fits your {subject}."),
            ("Request a time", "Choose a preferred day and time in the preview form."),
            ("Confirm with the office", "Call the office directly to make an actual appointment."),
        ],
        "areas": [(city, "Office location")], "area_from": "",
        "areas_intro": "Use the address below to plan your route. Call the office with questions before you travel.",
        "found_text": "Use the directions page for Google, Bing, or Apple Maps.",
        "google_maps": google_maps,
        "tools": {
            "title": f"Plan your {appointment.lower()}",
            "intro": "Choose a service and try the online request form.",
            "book_title": request,
            "book_text": "Pick a preferred day and time and review the request before you finish.",
            "book_link": action,
        },
        "booking_services": [service[1] for service in services] + ["Something else"],
        "times": ["9:00 AM", "10:30 AM", "11:00 AM", "3:30 PM", "4:00 PM"],
        "book": {
            "title": request,
            "seo": request,
            "intro": "Try the request form with sample information.",
            "hint": "These times illustrate the booking experience. Call the office for actual availability.",
            "notes_ph": "Use sample information only.",
            "closed": closed, "short_day": short_day,
            "cta": action, "cta_text": f"try the {appointment.lower()} request form",
            "svc_btn": action, "contact_link": action.lower(),
        },
        "faq_intro": "Common questions about services, appointments, and visiting the office.",
        "faq_ph": "Search questions",
        "faq": faq,
        "contact_note": "Use the listed phone number to reach the office outside this preview.",
        "contact_photos": False,
        "details_ph": "Use sample details only. Please leave out private information.",
        "form_label": "What would you like to ask about?",
        "posts": posts,
    }


def stock(photo_id, slug):
    return str(photo_id), f"https://www.pexels.com/photo/{slug}-{photo_id}/"


DENTAL_CHAIR = stock(5355858, "dental-facility")
DENTAL_EXAM = stock(5622238, "dentist-with-patient-in-office")
DENTAL_TOOLS = stock(31786502, "dental-tools-and-model-teeth-in-a-clinic")
DENTAL_GUIDANCE = ("examples/dentist/routine-visit-guidance.jpg", "https://www.pexels.com/photo/cheerful-young-female-dentist-discussing-tooth-structure-with-client-3845757/")
DENTAL_OFFICE = ("examples/dentist/dental-office.jpg", "https://www.pexels.com/photo/dental-chair-and-equipment-in-a-clinic-6812480/")
DENTAL_MODEL = ("examples/dentist/dental-model-consultation.jpg", "https://www.pexels.com/photo/dentist-showing-a-dental-model-to-a-patient-12746003/")
DENTAL_TRAY = ("examples/dentist/dental-instruments.jpg", "https://www.pexels.com/photo/close-up-of-dental-tools-5622028/")
DENTAL_VISIT = ("examples/dentist/welcoming-visit.jpg", "https://www.pexels.com/photo/smiling-young-ethnic-female-patient-in-dental-chair-in-modern-clinic-3881145/")
DENTAL_TEACHING = ("examples/dentist/dental-education.jpg", "https://www.pexels.com/photo/dentist-holding-dental-model-in-clinic-32852532/")
PAPERWORK = ("examples/dentist/appointment-paperwork.jpg", "https://www.pexels.com/photo/doctor-handing-a-document-8413294/")
SCALES = stock(5669602, "judgement-scale-and-gavel-in-judge-office")
LEGAL_FILES = stock(5673483, "group-of-diverse-colleagues-near-table-with-gavel")
DESK = stock(5668772, "crop-asian-judge-working-on-laptop-in-office")
RECORDS = stock(6829535, "a-person-writing-on-a-notebook")
DESK_DETAIL = stock(5668802, "wooden-gavel-on-wooden-surface")
SIGNING = stock(6077447, "judge-signing-on-the-papers")
NOTEPAD = stock(6779632, "a-person-writing-on-a-notepad")
WOOD_SCALES = stock(5669619, "judges-desk-with-gavel-and-scales")
LAW_BOOKS = stock(5668882, "justice-scales-and-gavel-on-wooden-surface")
NOTES = stock(7658354, "a-person-writing-on-a-notebook")
DENTAL_CONSULT = ("examples/dentist/hero.jpg", "https://www.pexels.com/photo/cheerful-young-female-dentist-talking-with-patient-in-modern-clinic-3884101/")
DENTAL_CARE = ("examples/dentist/care.jpg", "https://www.pexels.com/photo/man-sitting-on-dental-chair-3845810/")
DENTAL_FIRST = ("examples/dentist/first-visit-conversation.jpg", "https://www.pexels.com/photo/dentist-holding-a-dental-model-6627328/")
DENTAL_TEAM = stock(3952124, "medical-staff-with-tablet-and-lying-patient-in-dental-clinic")
DENTAL_EXPLAIN = stock(4971507, "a-dentist-talking-to-a-patient-while-holding-a-tooth-model")
DENTAL_CHECKUP = stock(6627561, "photograph-of-a-person-getting-a-dental-check-up")
LEGAL_DESK = stock(5668791, "male-lawyer-working-on-laptop-in-office")
LEGAL_REVIEW = stock(5673479, "mature-asian-legislator-working-with-laptop-at-table-with-gavel")
TABLET_NOTES = stock(5708212, "a-person-writing-on-notebook")
WRITTEN_NOTES = stock(4841706, "close-up-shot-of-a-person-writing-on-a-notebook-on-a-wooden-desk")
CASE_NOTES = stock(5951369, "a-person-writing-in-the-notebook")
OFFICE_NOTES = stock(34862446, "hands-writing-in-notebook-on-modern-office-desk")



LIFELONG = preview(
    slug="lifelong-dental-care", name="Lifelong Dental Care", owner=("Dr. Stacy Roszkowski", "Dentist"),
    industry="Dentist", city="Inver Grove Heights, MN",
    address="2125 Upper 55th St E, Suite 210, Inver Grove Heights, MN 55077",
    phone="(651) 457-4888", hours="Mon and Thu 8 am–5 pm · Tue 7 am–6 pm · Wed 7:30 am–noon",
    colors=("#246162", "#123c3c", "#e8c675", "#f4f8f7"), initials="LD",
    headline="Dental care for every stage of life.",
    tagline="Family dentistry, preventive visits, and restorative care in Inver Grove Heights.",
    intro="From checkups and cleanings to crowns and implants, see what the practice offers and find the right reason for your visit.",
    biography=[
        "Dr. Stacy Roszkowski provides family and cosmetic dentistry at Lifelong Dental Care. She earned her dental degree at the University of Minnesota and completed a residency at Hennepin County Medical Center.",
        "The practice also offers restorative care, including dental implants, and lists on-site oral surgery with Dr. Mark Roszkowski.",
    ],
    services=[
        ("heart-handshake", "Family dentistry", "Dental care for children, adults, and seniors.", ["Comprehensive exams", "Discuss dental care for your family"]),
        ("shield-check", "Preventive care", "Routine exams and professional cleanings.", ["Preventive visits", "Ask about follow-up care"]),
        ("sparkles", "Cosmetic dentistry", "Discuss ways to address the appearance of your smile.", ["Whitening options", "Tooth-colored materials"]),
        ("circle-check", "Crowns and bridges", "Ask about restoring a damaged tooth or replacing missing teeth.", ["Crowns", "Bridges"]),
        ("circle-check", "Dental implants", "Discuss implant options and the steps involved in an evaluation.", ["Implant consultation", "Restorative planning"]),
        ("stethoscope", "Oral surgery and extractions", "Ask the office about extractions and other oral surgery services.", ["Wisdom teeth", "Discuss the procedure and follow-up"]),
    ],
    visit=[
        ("Before your first visit", "Ask the office whether to complete the new-patient forms ahead of time."),
        ("Insurance questions", "The office says it works with most insurance plans. Call to check your specific coverage."),
        ("Finding the office", "The practice is in Suite 210 at 2125 Upper 55th Street East."),
    ],
    faq=[
        ("Appointments", "Are you accepting new patients?", "The practice lists new-patient appointments. Call to ask about availability."),
        ("Insurance", "Can I check my insurance first?", "Yes. Contact the office with your plan information to verify coverage."),
        ("Services", "Does the practice offer oral surgery?", "The practice lists oral surgery, extractions, and implants."),
        ("Location", "Where is the office?", "The office is in Suite 210 at 2125 Upper 55th Street East in Inver Grove Heights."),
    ],
    posts=[
        article("first-family-dental-visit", "Preparing for a family dental visit", "A little preparation can make a visit easier for the whole family.",
                [("What to bring", "Ask the office about new-patient forms and whether prior records would be useful. Bring your insurance information if you plan to use it."), ("What to ask", "Write down questions about cleanings, preventive care, and what the office recommends discussing at the first appointment.")]),
        article("talking-about-dental-implants", "Questions for an implant consultation", "A consultation is an opportunity to learn the steps involved and ask what alternatives are available.",
                [("Ask about the evaluation", "Find out what information the dentist needs to assess your options and what the appointment will cover."), ("Ask for a plan in writing", "Before deciding, ask who will handle each step, what visits might be needed, and how the office estimates costs.")]),
        article("check-dental-insurance", "What to ask about dental insurance", "A quick call about coverage can help you plan ahead.",
                [("Confirm your plan", "Have your plan name ready when you call. Ask how the office handles claims and what information it needs from you."), ("Discuss expected costs", "Ask for an estimate of your share of the cost before scheduling additional work.")]),
    ],
    photos=[DENTAL_CONSULT, DENTAL_TEACHING, DENTAL_OFFICE, DENTAL_VISIT, DENTAL_TOOLS, DENTAL_EXAM,
            DENTAL_GUIDANCE, DENTAL_MODEL, PAPERWORK],
    home_gallery=[
        ("A dental team preparing for a visit", DENTAL_TEAM),
        ("A visit to the dental chair", DENTAL_CARE),
        ("Going over a dental model", DENTAL_FIRST),
    ],
    blog_photos=[DENTAL_CHECKUP, DENTAL_EXPLAIN, DENTAL_TRAY],
    original="https://www.lifelongdds.com/", hero_file="dental-consultation.jpg", closed=(0, 5, 6), short_day=3,
)

COURT_STREET = preview(
    slug="court-street-legal", name="Court Street Legal", owner=("Rod M. Jones", "Attorney at Law"),
    industry="Law Firm", city="Salem, OR", address="387 Court Street NE, Salem, OR 97301",
    phone="(503) 365-2855", hours="Call the office for appointment availability.",
    colors=("#284e60", "#162c3c", "#e2be77", "#f6f8fa"), initials="CS",
    headline="Legal representation for serious injury and wrongful death.",
    tagline="Rod M. Jones represents clients in injury, wrongful death, and insurance matters in Oregon.",
    intro="Court Street Legal focuses on serious injuries and wrongful death claims, including matters involving vehicle accidents and insurance.",
    biography=[
        "Rod M. Jones leads Court Street Legal in Salem. He has represented individuals and businesses in Oregon state and federal courts.",
        "The firm focuses on serious injuries and wrongful death. Its website also lists insurance and business claims, along with the option to discuss an off-site consultation.",
    ],
    services=[
        ("heart-handshake", "Serious injuries", "Discuss injuries and losses connected with an accident.", ["Review the circumstances", "Identify questions for a consultation"]),
        ("users", "Wrongful death", "Speak with an attorney about a death connected with a possible claim.", ["Discuss the next conversation", "Ask what information may be useful"]),
        ("car", "Vehicle accidents", "Talk through the circumstances of a car crash and any injury claims.", ["Accident information", "Insurance correspondence"]),
        ("file-text", "Insurance claims", "Ask about a dispute involving coverage or an insurer’s response.", ["Policies", "Letters or claim decisions"]),
        ("briefcase", "Business claims", "Ask the firm whether it can help with a business dispute.", ["Review the nature of the dispute", "Discuss the scope of the matter"]),
    ],
    visit=[
        ("Arrange a consultation", "Call before visiting the Salem office."),
        ("Ask about meeting options", "The firm lists hospital, rehabilitation facility, and home visits. Ask whether one can be arranged."),
        ("Prepare for your visit", "Make a brief timeline and ask what records to bring. Keep confidential details out of the preview form."),
    ],
    faq=[
        ("Practice areas", "What does the firm focus on?", "Court Street Legal focuses on serious injury and wrongful death claims."),
        ("Appointments", "Can I ask about meeting outside the office?", "Yes. The firm says it can discuss visits elsewhere in Oregon."),
        ("Location", "Where is the office in Salem?", "The office is at 387 Court Street NE."),
        ("Preparing", "Should I send sensitive details in this form?", "Use sample information here. Call the office for instructions on sharing documents securely."),
    ],
    posts=[
        article("prepare-for-an-injury-consultation", "Preparing for an injury consultation", "Bring an overview of what happened and a list of questions you want answered.",
                [("Make a short timeline", "Write down the date, location, people involved, and important conversations. Keep supporting papers organized by date."), ("Ask what to bring", "Call the firm to ask which records would be useful and how they should be shared securely.")]),
        article("organize-insurance-correspondence", "Organizing insurance correspondence", "Keeping records together makes it easier to explain where things stand.",
                [("Keep letters and notices together", "Make a folder for policy pages, claim letters, and important contact details."), ("Write down questions", "Note any language you do not understand and bring those questions to a consultation. An attorney can discuss what the documents mean in your specific situation.")]),
        article("questions-for-a-legal-consultation", "Questions to ask at a legal consultation", "Decide what you want to learn before the meeting.",
                [("Ask how the firm works", "Find out who you would speak with, how updates are handled, and how the firm explains fees."), ("Ask about the next step", "Before you leave, ask what information is still needed and how to follow up.")]),
    ],
    photos=[SCALES, LEGAL_FILES, WOOD_SCALES, DESK_DETAIL, LAW_BOOKS, NOTES, SIGNING, RECORDS, NOTEPAD],
    home_gallery=[
        ("Preparing for a legal consultation", LEGAL_DESK),
        ("Taking notes about the matter", WRITTEN_NOTES),
        ("Keeping records organized", OFFICE_NOTES),
    ],
    blog_photos=[LEGAL_REVIEW, TABLET_NOTES, CASE_NOTES],
    original="https://courtstreetlegal.com/",
)

ANDERSON = preview(
    slug="dr-bradley-r-anderson-dds", name="Dr. Bradley R. Anderson, DDS",
    owner=("Dr. Bradley R. Anderson", "Dentist"), industry="Dentist", city="Glen Allen, VA",
    address="11420 W Broad St, Glen Allen, VA 23060",
    phone="(804) 360-3500", hours="Mon–Thu 8 am–5 pm · Fri 8 am–noon",
    colors=("#28546b", "#163647", "#f0c77f", "#f3f8fb"), initials="BA",
    headline="Family and cosmetic dentistry in Short Pump.",
    tagline="From regular cleanings to restorative care, find the right visit for you and your family.",
    intro="The Glen Allen office provides preventive, restorative, and cosmetic dental services and accepts new patients.",
    biography=[
        "Dr. Bradley R. Anderson earned his dental degree from Virginia Commonwealth University in 1989 and has practiced in the Richmond area since then.",
        "His team provides family and cosmetic dentistry in Short Pump. The practice offers digital X-rays and is located near West Broad Street and Pump Road.",
    ],
    services=[
        ("shield-check", "Family dental care", "Routine exams and cleanings for your family.", ["Dental checkups", "Professional cleanings"]),
        ("sparkles", "Cosmetic dentistry", "Discuss cosmetic options, including teeth whitening.", ["Whitening", "Ask which options suit your goals"]),
        ("circle-check", "Crowns and bridges", "Discuss ways to restore damaged teeth and address gaps.", ["Crowns", "Bridges"]),
        ("circle-check", "Tooth fillings", "Ask about treatment and materials for restoring a tooth.", ["Tooth assessment", "Filling options"]),
        ("heart-handshake", "Dentures and implants", "Review replacement options with the dental team.", ["Dentures and partials", "Dental implants"]),
        ("stethoscope", "Root canal care", "Contact the office about an evaluation and next steps.", ["Evaluation", "Treatment questions"]),
    ],
    visit=[
        ("New patient appointments", "Call to ask about an appointment and any information the office needs before your visit."),
        ("Getting to Short Pump", "The office is in the shopping center near West Broad Street and Pump Road."),
        ("Discuss treatment options", "Tell the dental team what prompted your visit and bring the questions you want to ask."),
    ],
    faq=[
        ("Appointments", "Are you accepting new patients?", "Yes. Call the Glen Allen office to arrange a first visit."),
        ("Services", "Do you offer teeth whitening?", "Yes. Contact the office to ask about teeth whitening and cosmetic dentistry."),
        ("Hours", "Is the office open Friday?", "The office lists Friday hours from 8 am to noon."),
        ("Directions", "Where is the office?", "The office is at 11420 W Broad St in Glen Allen, in the Short Pump area."),
    ],
    posts=[
        article("first-visit-short-pump", "Planning your first Short Pump dental visit", "A first visit is a chance to bring up concerns and learn how the office works.",
                [("Before you call", "Decide which times work for you. Ask about forms, insurance details, and whether the office needs recent records."), ("When you arrive", "Let the dental team know what prompted your visit. Ask how they will explain any recommended care.")]),
        article("crowns-bridges-conversation", "Questions about crowns and bridges", "A consultation can help you understand the difference between the options being discussed.",
                [("Ask what the restoration is for", "Have the dental team show you which tooth or area they are discussing and explain the goal of the treatment."), ("Plan for follow-up", "Ask about the number of visits, how your bite will be checked, and what will happen afterward.")]),
        article("ask-about-teeth-whitening", "What to ask before teeth whitening", "A conversation with the dentist can help you decide which questions matter for your smile.",
                [("Talk about your goals", "Explain the change you are hoping to see and ask what is realistic with your current restorations and dental history."), ("Compare your options", "Ask about timing, costs, and follow-up. Give yourself time to consider the answers before choosing.")]),
    ],
    photos=[DENTAL_EXAM, DENTAL_MODEL, DENTAL_TRAY, DENTAL_CHAIR, DENTAL_OFFICE, PAPERWORK,
            DENTAL_VISIT, DENTAL_TOOLS, DENTAL_GUIDANCE],
    home_gallery=[
        ("What happens during a checkup", DENTAL_CHECKUP),
        ("A dental care conversation", DENTAL_CONSULT),
        ("A closer look at dental care", DENTAL_FIRST),
    ],
    blog_photos=[DENTAL_TEAM, DENTAL_EXPLAIN, DENTAL_TEACHING],
    original="https://www.dentistinshortpump.com/", short_day=5,
)

PEREZ = preview(
    slug="law-office-of-roger-perez", name="Law Office of Roger Perez",
    owner=("Roger Perez", "Attorney at Law"), industry="Law Firm", city="San Antonio, TX",
    address="427 S. Saint Mary’s St, San Antonio, TX 78205",
    phone="(210) 224-2240", hours="Call the office for appointment availability.",
    colors=("#36546b", "#172e46", "#e7ba76", "#f6f7fb"), initials="RP",
    headline="Talk through your legal options in San Antonio.",
    tagline="Divorce, family law, car accidents, and criminal defense. Hablamos español.",
    intro="Find your practice area and prepare for a conversation with the office about next steps.",
    biography=[
        "Roger Perez practices in San Antonio. His office lists divorce, family law, car accidents, and criminal defense among its practice areas.",
        "The office is on South Saint Mary’s Street in downtown San Antonio and offers assistance in Spanish.",
    ],
    services=[
        ("file-text", "Divorce", "Discuss divorce concerns, the documents involved, and questions to bring.", ["Divorce consultation", "Questions about the process"]),
        ("users", "Family law", "Talk about a family matter and ask the office which records would be useful.", ["Family law consultation", "Discuss next steps"]),
        ("car", "Car accidents", "Speak with the office about a vehicle crash and related concerns.", ["Accident information", "Insurance correspondence"]),
        ("shield-check", "Criminal defense", "Contact the office about a criminal matter or court notice.", ["Consultation about the matter", "Ask what documents to share"]),
    ],
    visit=[
        ("Call about your matter", "Tell the office the general type of legal matter and ask how to arrange a consultation."),
        ("Ask for help in Spanish", "The office offers Spanish-language assistance. Ask for it when you call."),
        ("Plan your downtown visit", "Confirm the appointment location and ask about parking before traveling downtown."),
    ],
    faq=[
        ("Services", "What kinds of matters does the office handle?", "The office lists divorce, family law, car accidents, and criminal defense."),
        ("Language", "¿Hablan español?", "Sí. Llame a la oficina para pedir atención en español."),
        ("Appointments", "How do I arrange a consultation?", "Call the San Antonio office to ask about appointments."),
        ("Privacy", "Can I put case details in the preview?", "Please use sample information here. Ask the office how to share documents securely."),
    ],
    posts=[
        article("prepare-for-a-family-law-meeting", "Preparing for a family law consultation", "A list of priorities can help you use the time effectively.",
                [("List the questions you want answered", "Note your most pressing concerns and what you are hoping to understand after the meeting."), ("Ask what to bring", "Check with the office about relevant papers and how to share them privately.")]),
        article("organize-car-accident-records", "Organizing records after a car accident", "Keeping records in one place helps you describe what happened.",
                [("Save your correspondence", "Collect reports, correspondence, and contact information. Keep originals and note where each item came from."), ("Prepare to talk with the office", "Write down questions about the documents you have and ask whether any others would be useful for an initial discussion.")]),
        article("before-a-defense-consultation", "What to bring to a defense consultation", "Start with the paperwork you received and the questions you want to ask.",
                [("Keep copies in one folder", "Gather any notice or court papers you received. Note any dates printed on the documents so you can discuss them directly with counsel."), ("Discuss how to communicate", "Ask how to exchange documents securely and where to direct follow-up questions.")]),
    ],
    photos=[DESK, NOTEPAD, DESK_DETAIL, LEGAL_FILES, SCALES, WOOD_SCALES, NOTES, LAW_BOOKS, SIGNING],
    home_gallery=[
        ("Reviewing a legal matter", LEGAL_REVIEW),
        ("Preparing questions", CASE_NOTES),
        ("Getting paperwork together", OFFICE_NOTES),
    ],
    blog_photos=[TABLET_NOTES, RECORDS, WRITTEN_NOTES],
    original="https://www.rogerperez.com/",
)

OYAKAWA = preview(
    slug="susan-oyakawa", name="Dr. Susan L. Oyakawa, DC",
    owner=("Dr. Susan Oyakawa", "Chiropractor"), industry="Chiropractor", city="San Francisco, CA",
    address="1364 Valencia St, San Francisco, CA 94110", phone="(415) 648-3327",
    hours="Weekday appointments. Check the practice scheduler for current times.",
    colors=("#366a59", "#163b31", "#edca86", "#f4f8f4"), initials="SO",
    headline="Chiropractic care on Valencia Street.",
    tagline="Explore care for movement and joint concerns, from the head, neck, and shoulders to the hips, knees, and feet.",
    intro="Dr. Susan Oyakawa’s practice lists care for a range of movement and joint concerns, including recovery after a motor vehicle injury.",
    biography=[
        "Dr. Susan Oyakawa sees patients at her office on Valencia Street in San Francisco’s Mission District.",
        "Her practice describes a focus on factors that contribute to physical discomfort. The office offers scheduling for both new and returning patients.",
    ],
    services=[
        ("activity", "Head, jaw, and neck", "Discuss concerns involving the head, jaw, or neck.", ["Head and neck concerns", "Jaw movement questions"]),
        ("heart-handshake", "Shoulders, elbows, and wrists", "Ask about shoulder, elbow, or wrist concerns that affect day-to-day movement.", ["Shoulder care", "Elbow and wrist concerns"]),
        ("circle-check", "Hips and pelvis", "Discuss hip and pelvic concerns and their effect on movement.", ["Hip concerns", "Pelvic movement"]),
        ("circle-check", "Knees, ankles, and feet", "Ask whether the practice can help with concerns affecting your lower limbs.", ["Knee concerns", "Ankle and foot concerns"]),
        ("stethoscope", "Sciatica and arthritis concerns", "Bring questions about symptoms, movement, and available options.", ["Sciatica concerns", "Arthritis questions"]),
        ("car", "Motor vehicle injury recovery", "Ask about scheduling a visit to discuss accident-related concerns.", ["Discuss a first visit", "Ask about records to bring"]),
    ],
    visit=[
        ("First-time visits", "Ask the office what to bring and how much time to allow."),
        ("Returning patients", "The practice offers online scheduling for both new and established patients on its official site."),
        ("Mission District location", "The office is on Valencia Street. Open directions to check your route before leaving."),
    ],
    faq=[
        ("Appointments", "Can new patients schedule online?", "The practice offers online scheduling for new and returning patients on its official site."),
        ("Services", "Does the practice see patients after a vehicle injury?", "Motor vehicle injury recovery is listed among the practice’s services."),
        ("Hours", "Where can I check current appointment times?", "Use the official scheduler or call the office."),
        ("Directions", "Where is the office?", "The office is at 1364 Valencia Street, San Francisco."),
    ],
    posts=[
        article("first-chiropractic-visit", "Preparing for a chiropractic visit", "Think about the concerns you want to discuss and how they affect your routine.",
                [("Write down your questions", "Note when the concern started, what makes it noticeable, and what you want to be able to do more comfortably."), ("Confirm visit details", "Ask the office what to bring and what it expects to cover at the first appointment.")]),
        article("keeping-track-of-movement-concerns", "Keeping track of movement concerns", "Everyday observations can help you explain what you are experiencing.",
                [("Notice the context", "Write down what you were doing when the concern came up and how it affected the rest of your day."), ("Bring your notes", "Use your notes as a starting point for questions about the assessment and options.")]),
        article("questions-after-vehicle-injury", "Questions for a visit after a vehicle injury", "Call the office to learn what information it needs before your visit.",
                [("Ask about paperwork", "Find out whether the office wants relevant records and how you should share them."), ("Plan the first conversation", "Make a short list of your concerns and ask how the practice handles follow-up appointments.")]),
    ],
    photos=[
        ("examples/chiropractor/hands-on-care.jpg", "https://www.pexels.com/photo/woman-lying-on-massage-table-having-chiropractic-therapy-5794021/"),
        stock(3992806, "woman-having-a-check-up"),
        ("examples/chiropractor/consultation-notes.jpg", "https://www.pexels.com/photo/a-person-taking-notes-while-talking-to-the-patient-8413183/"),
        ("examples/chiropractor/reception-conversation.jpg", "https://www.pexels.com/photo/woman-in-black-long-sleeves-explaining-the-services-on-a-customer-6812437/"),
        ("examples/chiropractor/guided-band-exercise.jpg", "https://www.pexels.com/photo/crop-anonymous-woman-stretching-elastic-band-near-professional-chiropractor-4506166/"),
        ("examples/chiropractor/guided-mat-exercise.jpg", "https://www.pexels.com/photo/physiotherapist-exercising-with-a-patient-20860617/"),
        PAPERWORK,
        NOTES,
        ("examples/chiropractor/back-assessment.jpg", "https://www.pexels.com/photo/physiotherapist-looking-at-patient-back-20860586/"),
    ],
    home_gallery=[
        ("A shoulder and upper-back assessment", stock(4506110, "crop-anonymous-chiropractor-examining-spine-of-fit-lady-in-hospital")),
        ("Discussing questions before care", ("examples/chiropractor/patient-questions.jpg", "https://www.pexels.com/photo/a-doctor-talking-to-a-patient-while-holding-a-tablet-4266936/")),
        ("Guidance during a seated exercise", stock(20860594, "physiotherapist-instructing-patient")),
    ],
    blog_photos=[
        ("examples/chiropractor/patient-care-discussion.jpg", "https://www.pexels.com/photo/male-doctor-talking-to-a-patient-6129444/"),
        ("examples/chiropractor/assisted-leg-stretch.jpg", "https://www.pexels.com/photo/physiotherapist-working-with-patient-20860579/"),
        WRITTEN_NOTES,
    ],
    original="https://www.drsusanoyakawa.com/", short_day=5,
)

OYAKAWA["official_booking"] = "https://www.drsusanoyakawa.com/schedule"
OYAKAWA["image_map"].update({
    "home-portrait": "/preview/susan-oyakawa/img/office-consultation.jpg",
    "home-g1": "/preview/susan-oyakawa/img/shoulder-assessment.jpg",
    "home-g3": "/preview/susan-oyakawa/img/seated-exercise.jpg",
})

SITES = (LIFELONG, COURT_STREET, ANDERSON, PEREZ, OYAKAWA)


def build():
    for site in SITES:
        build_site(site)


if __name__ == "__main__":
    build()
