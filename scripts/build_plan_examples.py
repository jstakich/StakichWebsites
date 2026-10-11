"""Builds the full multi-page example websites.

The three plan examples (1 Starter, 2 Growth, 3 Pro) only use features from
their plan. The industry examples have every Pro feature but no plan label.
Run from the project root:  python3 scripts/build_plan_examples.py
"""
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

from client_privacy import privacy_body
from common import HTTPS_REDIRECT, JS_V, PLANS, SITE, react_assets, react_mount, share_mount
from full_examples_data import FULL_SITES
from icons import BING_B, GOOGLE_G, icon
from build_previews import PLAN_EXTRAS
from plan_examples_data import INCLUDED, NOT_INCLUDED, PLAN_SITES

PHONE = "(423) 555-0142"
PHONE_TEL = "+14235550142"
AVATAR_COLORS = ["#1a73e8", "#e8710a", "#188038", "#a142f4", "#d93025"]
ALL_SITES = PLAN_SITES + FULL_SITES


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "examples"
CSS_V = "6"
PLAN_JS_V = "8"
DEMO_CSS_V = "12"
SMS = f"sms:{PHONE_TEL}"
TEL = f"tel:{PHONE_TEL}"


def money(n):
    return "${:,}".format(n)


def nice_date(s):
    d = datetime.strptime(s, "%Y-%m-%d")
    return f"{d:%B} {d.day}, {d.year}"


def url(site, key):
    base = f"/examples/{site['slug']}/"
    return base if key == "index" else f"{base}{key}.html"


def post_url(site, post):
    return f"/examples/{site['slug']}/blog/{post['slug']}.html"


def img(site, kind):
    return f"/examples/img/{site['slug']}/{kind}.jpg"


def has(site, key):
    return any(k == key for k, _ in site["pages"])


def page_name(site, key):
    return dict(site["pages"])[key]


def labeled(site):
    return site.get("labeled", True)


def city(site):
    return site.get("city", "Cleveland, TN")


def plan_tag(site, text=None):
    if not labeled(site):
        return ""
    name = PLANS[site["plan"]]["name"]
    return f'<span class="p-tag p-tag-{site["plan"]}">{icon("badge-check")} {esc(text or name + " plan feature")}</span>'


def next_site(site):
    i = PLAN_SITES.index(site)
    return PLAN_SITES[i + 1] if i + 1 < len(PLAN_SITES) else None


# ---------- page shell ----------

def plan_strip(site):
    if not labeled(site):
        return f"""
    <div class="plan-strip plan-strip-example">
      <div class="wrap">
        <span class="plan-strip-num">{icon('eye')}</span>
        <span class="plan-strip-text"><b>Example website</b> {esc(site['name'])} is not a real business. Stakich Websites built this sample to show what your website could look like.</span>
        <span class="plan-strip-links"><a href="/#pricing">Get one like it</a><a class="plan-strip-next" href="/examples/">See all examples →</a></span>
      </div>
    </div>"""
    plan = PLANS[site["plan"]]
    nxt = next_site(site)
    if nxt:
        more = f'<a class="plan-strip-next" href="{url(nxt, "index")}">Next: {nxt["num"]} {esc(nxt["label"])} →</a>'
    else:
        more = '<a class="plan-strip-next" href="/examples/">See all examples →</a>'
    return f"""
    <div class="plan-strip plan-strip-{site['plan']}">
      <div class="wrap">
        <span class="plan-strip-num">{site['num']}</span>
        <span class="plan-strip-text"><b>{esc(site['label'])}</b> Everything on this site is in the {plan['name']} plan ({money(plan['setup'])} + {money(plan['monthly'])}/mo).</span>
        <span class="plan-strip-links"><a href="{url(site, 'index')}#plan">What's included</a>{more}</span>
      </div>
    </div>"""


def header(site, active):
    links = ""
    for key in site["nav"]:
        cur = ' aria-current="page"' if key == active else ""
        cls = ' class="d-btn d-btn-accent p-nav-cta"' if key == "book" else ""
        links += f'<a href="{url(site, key)}"{cls}{cur}>{esc(page_name(site, key))}</a>'
    mlinks = ""
    for key, name in site["pages"]:
        cur = ' aria-current="page"' if key == active else ""
        mlinks += f'<a href="{url(site, key)}"{cur}>{esc(name)}</a>'
    return f"""
    <header class="d-header p-header">
      <div class="wrap">
        <a class="d-logo" href="{url(site, 'index')}"><i>{icon(site['logo'])}</i>{esc(site['name'])}</a>
        <nav class="d-nav p-nav" aria-label="Main">
          {links}
          <a class="d-btn d-btn-brand p-call" href="{TEL}">{icon('phone')}<span>{PHONE}</span></a>
          <button class="p-menu-btn" type="button" aria-expanded="false" aria-controls="p-mnav">{icon('menu')}<span>Menu</span></button>
        </nav>
      </div>
      <div class="p-mnav" id="p-mnav" hidden>
        <div class="wrap">
          <div class="p-mnav-links">{mlinks}</div>
          <div class="p-mnav-reach"><a class="d-btn d-btn-accent" href="{TEL}">{icon('phone')} Call</a><a class="d-btn d-btn-brand" href="{SMS}">{icon('message-circle')} Text</a></div>
        </div>
      </div>
    </header>"""


def footer(site):
    links = "".join(f'<li><a href="{url(site, k)}">{esc(n)}</a></li>' for k, n in site["pages"])
    addr = f"<br />{esc(site['address'])}" if site.get("address") else ""
    if labeled(site):
        plan = PLANS[site["plan"]]
        about = f"<p>{esc(site['label'])}: a sample website built on the <b>{plan['name']}</b> plan by <a href=\"/\">Stakich Websites</a>.</p>"
        start = f"/start?plan={site['plan']}"
    else:
        about = f'<p>A sample {esc(site["industry"].lower())} website built by <a href="/">Stakich Websites</a>.</p>'
        start = "/start"
    return f"""
    <footer class="d-footer p-footer">
      <div class="wrap">
        <div>
          <b>{esc(site['name'])}</b>{addr}<br />{esc(site['hours'])}
          <p class="p-footer-reach"><a href="{TEL}">{icon('phone')} Call {PHONE}</a><a href="{SMS}">{icon('message-circle')} Text us</a></p>
        </div>
        <ul class="p-footer-links">{links}<li><a href="{url(site, 'privacy')}">Privacy Policy</a></li></ul>
        <div>
          {about}
          <p><a href="{start}">Get a site like this →</a><br /><a href="/examples/">See all examples</a></p>
        </div>
      </div>
    </footer>"""


def sticky(site):
    book = f'<a class="d-btn d-btn-brand" href="{url(site, "book")}">{icon("calendar-days")} Book</a>' if has(site, "book") else ""
    cls = " p-sticky-3" if book else ""
    return f"""
    <div class="d-sticky{cls}"><a class="d-btn d-btn-accent" href="{TEL}">{icon('phone')} Call</a><a class="d-btn d-btn-brand" href="{SMS}">{icon('message-circle')} Text</a>{book}</div>"""


def schema(site):
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": site["name"],
        "telephone": PHONE,
        "url": f"{SITE}{url(site, 'index')}",
        "image": f"{SITE}{img(site, 'hero')}",
        "areaServed": [a if isinstance(a, str) else a[0] for a in site["areas"]],
        "openingHours": site["hours"],
    }
    if site.get("rating"):
        data["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": site["rating"][0], "reviewCount": site["rating"][1]}
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def page(site, active, title, desc, body, path, image=None, noindex=False, extra_head="", share=True):
    style = (
        f"--brand:{site['brand']};--brand-dark:{site['dark']};--accent:{site['accent']};"
        f"--accent-ink:{site['accent_ink']};--bg:{site['bg']};"
    )
    robots = '<meta name="robots" content="noindex" />' if noindex else ""
    share_band = ""
    if share and site["plan"] in ("growth", "pro"):
        label = f"Share {site['name']} with a friend"
        share_band = f'\n      <section class="d-section p-share-band"><div class="wrap">{share_mount(label)}</div></section>'
    og = image or img(site, "hero")
    if active == "index":
        extra_head += schema(site)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    {HTTPS_REDIRECT}
    <title>{esc(title)} (Example Site)</title>
    <meta name="description" content="{esc(desc)}" />
    {robots}
    <link rel="canonical" href="{SITE}{path}" />
    <link rel="icon" href="/assets/icon.svg" type="image/svg+xml" />
    <meta property="og:title" content="{esc(title)} (Example Site)" />
    <meta property="og:description" content="{esc(desc)}" />
    <meta property="og:image" content="{SITE}{og}" />
    <meta property="og:url" content="{SITE}{path}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/examples/demo.css?v={DEMO_CSS_V}" />
    <link rel="stylesheet" href="/examples/plan.css?v={CSS_V}" />
    {extra_head}
  </head>
  <body class="p-site p-site-{site['plan']}" style="{style}">{plan_strip(site)}{header(site, active)}
    <main id="top">{body}{share_band}
    </main>{footer(site)}{sticky(site)}
    <script src="/examples/plan.js?v={PLAN_JS_V}" defer></script>
    <script src="/share.js?v={JS_V}" defer></script>
    {react_assets()}
  </body>
</html>
"""


def write(site, rel, html):
    path = OUT / site["slug"] / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


# ---------- shared sections ----------

def sub_hero(site, title, intro, kind="hero", eyebrow=""):
    eb = f'<p class="p-eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    return f"""
      <section class="d-hero d-hero-photo p-hero-sm" style="--hero:url({img(site, kind)})">
        <div class="wrap">
          {eb}<h1>{esc(title)}</h1>
          <p class="tagline">{esc(intro)}</p>
        </div>
      </section>"""


def reach_buttons(site, primary=None):
    first = primary or (url(site, "contact"), site["cta"])
    return (
        f'<a class="d-btn d-btn-accent" href="{first[0]}">{esc(first[1])}</a>'
        f'<a class="d-btn d-btn-ghost" href="{TEL}">{icon("phone")} Call {PHONE}</a>'
        f'<a class="d-btn d-btn-ghost" href="{SMS}">{icon("message-circle")} Text Us</a>'
    )


def why(site):
    items = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in site["why"])
    return f"""
      <section class="d-section d-section-alt p-why-band">
        <div class="wrap"><div class="d-why">{items}</div></div>
      </section>"""


def service_cards(site, detailed=False):
    cards = ""
    for ico, title, desc, price, points in site["services"]:
        extra = ""
        if detailed:
            lis = "".join(f"<li>{icon('circle-check')}<span>{esc(p)}</span></li>" for p in points)
            if has(site, "book"):
                act = f'<a class="d-btn d-btn-brand" href="{url(site, "book")}?service={quote_plus(booking_name(site, title))}">{esc(site["book"].get("svc_btn", "Book This"))}</a>'
            else:
                act = f'<a class="d-btn d-btn-brand" href="{url(site, "contact")}?service={esc(title)}">Get a Quote</a>'
            extra = f'<ul class="d-checks p-mini-checks">{lis}</ul>{act}'
        cards += f"""
          <article class="d-card p-svc"><div class="d-ico">{icon(ico)}</div><h3>{esc(title)}</h3><p>{esc(desc)}</p><p class="d-price">{esc(price)}</p>{extra}</article>"""
    return f'<div class="d-grid">{cards}\n        </div>'


def booking_name(site, title):
    return site.get("svc_book", {}).get(title, title)


def steps(site):
    cards = "".join(
        f'<article class="d-card d-step"><span class="d-step-num">{i}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for i, (t, d) in enumerate(site["steps"], 1)
    )
    return f"""
      <section class="d-section d-section-alt">
        <div class="wrap">
          <div class="d-head"><h2>How it works</h2><p>Simple, fast, and no pressure.</p></div>
          <div class="p-grid-3">{cards}</div>
        </div>
      </section>"""


def photo_strip(site):
    figs = "".join(
        f'<figure class="d-photo"><img src="{img(site, "g" + str(i))}" alt="{esc(c)}" loading="lazy" width="900" height="675" /><figcaption>{esc(c)}</figcaption></figure>'
        for i, (c, _) in enumerate(site["photos"], 1)
    )
    return f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head"><h2>{esc(page_name(site, 'work'))}</h2><p>{esc(site.get('work_sub', 'Real jobs, real results.'))}</p></div>
          <div class="d-photos">{figs}</div>
          <p class="p-center"><a class="d-btn d-btn-brand" href="{url(site, 'work')}">See more of our work</a></p>
        </div>
      </section>"""


def about_teaser(site):
    name, role = site["owner"]
    return f"""
      <section class="d-section d-section-alt">
        <div class="wrap d-split p-about">
          <div class="d-portrait"><img src="{img(site, 'portrait')}" alt="{esc(name)}, {esc(role)}" loading="lazy" width="600" height="600" /></div>
          <div>
            <p class="d-eyebrow">Meet {esc(name.split()[0])}</p>
            <h2>{esc(site['about_title'])}</h2>
            <p>{esc(site['about'][0])}</p>
            <a class="d-btn d-btn-brand" href="{url(site, 'about')}">Our story</a>
          </div>
        </div>
      </section>"""


def stars(n=5):
    return f'<span class="stars" aria-label="{n} out of 5 stars">' + "★" * n + "</span>"


def review_cards(site, limit=None):
    out = ""
    for i, (q, who, age) in enumerate(site["reviews"][:limit]):
        color = AVATAR_COLORS[(i + len(site["slug"])) % len(AVATAR_COLORS)]
        out += f"""
          <article class="d-review g-review">
            <header><span class="g-avatar" style="background:{color}">{esc(who[0].upper())}</span><div><b>{esc(who)}</b><small>{esc(age)}</small></div>{GOOGLE_G}</header>
            {stars()}
            <p>{esc(q)}</p>
          </article>"""
    return out


def g_summary(site):
    rating, count, _ = site["rating"]
    return f"""
          <div class="g-summary">
            <div class="g-brand">{GOOGLE_G}<span>Google Reviews</span></div>
            <div class="g-score"><b>{rating}</b>{stars()}<small>Based on {count} reviews</small></div>
            <button class="d-btn d-btn-brand" type="button" data-toast="On the real website, this button opens your Google review page, so happy customers can leave a review in one tap.">Review us on Google</button>
          </div>"""


def reviews_teaser(site):
    return f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Google reviews section")}<h2>What customers say</h2></div>
          {g_summary(site)}
          <div class="d-grid">{review_cards(site, 3)}</div>
          <p class="p-center"><a class="d-btn d-btn-brand" href="{url(site, 'reviews')}">Read all reviews</a></p>
        </div>
      </section>"""


def post_cards(site, posts):
    out = ""
    for p in posts:
        out += f"""
          <a class="p-post-card" href="{post_url(site, p)}">
            <img src="{img(site, p['img'])}" alt="" loading="lazy" width="900" height="675" />
            <div><p class="p-date">{nice_date(p['date'])}</p><h3>{esc(p['title'])}</h3><p>{esc(p['excerpt'])}</p><span class="p-more">Read more →</span></div>
          </a>"""
    return f'<div class="p-posts">{out}\n        </div>'


def blog_teaser(site):
    per = "2 new posts every month" if site["plan"] == "pro" else "A new post every month"
    return f"""
      <section class="d-section d-section-alt">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Blog written for you")}<h2>Tips from our blog</h2><p>{per}, ready to share on Facebook and other social media.</p></div>
          {post_cards(site, site['posts'][:3])}
          <p class="p-center"><a class="d-btn d-btn-brand" href="{url(site, 'blog')}">See all posts</a></p>
        </div>
      </section>"""


def primary_cta(site):
    if has(site, "book"):
        return (url(site, "book"), site["book"].get("cta", "Book Online"))
    return (url(site, "contact"), site["cta"])


def cta_band(site):
    primary = primary_cta(site)
    how = site["book"].get("cta_text", "book online") if has(site, "book") else "send a quick quote request"
    return f"""
      <section class="p-cta">
        <div class="wrap p-cta-box">
          <div><h2>Ready when you are.</h2><p>Call, text, or {esc(how)}. We usually reply the same day.</p></div>
          <div class="p-cta-actions">{reach_buttons(site, primary)}</div>
        </div>
      </section>"""


def report_box(site):
    return ""


def plan_box(site):
    key = site["plan"]
    plan = PLANS[key]
    labels = " Smaller plans leave out the parts with black labels." if labeled(site) and key != "starter" else ""
    cards = ""
    for k in ("starter", "growth", "pro"):
        pl = PLANS[k]
        mine = k == key
        flag = '<p class="s-plan-flag">THIS IS THE PLAN YOU\'RE SEEING</p>' if mine else ""
        feats = "".join(f"<li>{icon('circle-check')}<span>{esc(t)}</span></li>" for t in PLAN_EXTRAS[k])
        btn = "d-btn-accent" if mine else "d-btn-ghost-dark"
        cards += f"""
            <div class="s-plan{' s-plan-mine' if mine else ''}">
              {flag}
              <h3>{pl['name']}</h3>
              <p class="s-plan-price"><b>{money(pl['setup'])}</b> setup<br />then <b>{money(pl['monthly'])}/month</b></p>
              <ul>{feats}</ul>
              <a class="d-btn {btn}" href="/start?plan={k}">Pick {pl['name']}</a>
            </div>"""
    return f"""
      <section class="d-section s-end" id="plan">
        <div class="wrap">
          <h2>Like it? It can be yours.</h2>
          <p>This is an example website by Stakich Websites. <b>You're seeing the {plan['name']} plan.</b> To get everything you see here, pick <b>{plan['name']}</b>.{labels} No contract on any plan.</p>
          <div class="s-plans">{cards}
          </div>
          <p>First 10 customers save $100 with code <span class="s-code">FIRST100</span>.</p>
          <div class="p-planbox-actions s-end-actions">
            <a class="d-btn d-btn-accent" href="/start?plan={key}">Get a site like this ({plan['name']} plan)</a>
            <a class="d-btn d-btn-ghost-dark" href="/examples/">See more examples</a>
          </div>
          {react_mount("ex:" + site["slug"], title="What do you think of this example?")}
        </div>
      </section>"""


# ---------- pages ----------

def home(site):
    plan = site["plan"]
    badges = "".join(f"<li>{esc(b)}</li>" for b in site["badges"])
    actions = reach_buttons(site, primary_cta(site))
    if has(site, "estimate"):
        actions = actions.replace(
            f'<a class="d-btn d-btn-ghost" href="{TEL}">',
            f'<a class="d-btn d-btn-ghost" href="{url(site, "estimate")}">{icon("calculator")} {esc(site["est"].get("hero_btn", "Get a Price"))}</a><a class="d-btn d-btn-ghost" href="{TEL}">',
            1,
        )
    body = f"""
      <section class="d-hero d-hero-photo" style="--hero:url({img(site, 'hero')})">
        <div class="wrap">
          <h1>{esc(site['h1'])}</h1>
          <p class="tagline">{esc(site['tagline'])}</p>
          <div class="d-hero-actions">{actions}</div>
          <ul class="d-badges">{badges}</ul>
        </div>
      </section>{why(site)}"""
    if plan == "pro":
        body += pro_tools(site)
    body += f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head"><h2>{esc(site.get('services_title', 'Our services'))}</h2><p>{esc(site.get('services_sub', 'Clear prices and friendly, reliable service.'))}</p></div>
          {service_cards(site)}
          <p class="p-center"><a class="d-btn d-btn-brand" href="{url(site, 'services')}">{esc(site.get('services_link', 'See all services & prices'))}</a></p>
        </div>
      </section>"""
    body += steps(site)
    body += photo_strip(site)
    body += about_teaser(site)
    if has(site, "reviews"):
        body += reviews_teaser(site)
    if has(site, "blog"):
        body += blog_teaser(site)
    if has(site, "areas"):
        body += found_teaser(site)
    body += cta_band(site)
    body += plan_box(site)
    title = f"{site['name']} | {site['industry']} in {city(site)}"
    desc = f"{site['keyword']} by Stakich Websites. {site['tagline']}"
    return page(site, "index", title, desc, body, url(site, "index"))


def pro_tools(site):
    t = site["tools"]
    return f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Pro tools")}<h2>{esc(t['title'])}</h2><p>{esc(t['intro'])}</p></div>
          <div class="p-tools">
            <a class="p-tool-card" href="{url(site, 'estimate')}">
              <span class="p-tool-ico">{icon('calculator')}</span>
              <h3>{esc(t['est_title'])}</h3>
              <p>{esc(t['est_text'])}</p>
              <span class="p-more">{esc(t.get('est_link', 'Get my price'))} →</span>
            </a>
            <a class="p-tool-card" href="{url(site, 'book')}">
              <span class="p-tool-ico">{icon('calendar-days')}</span>
              <h3>{esc(t['book_title'])}</h3>
              <p>{esc(t['book_text'])}</p>
              <span class="p-more">{esc(t.get('book_link', 'Book a time'))} →</span>
            </a>
          </div>
        </div>
      </section>"""


def map_iframe(site):
    q = quote_plus(city(site))
    return f'<iframe title="Map of {esc(city(site))}" src="https://www.google.com/maps?q={q}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'


def found_note(site):
    return f"""
            <div class="p-found-note">
              <p><b>Getting found is part of the Pro plan.</b> When you buy Pro, we set up your free Google and Bing business listings and keep them up to date, so nearby customers see your business on the map, with your hours, photos, and reviews.</p>
              <p class="p-found-links"><a href="/get-found-on-google.html">{GOOGLE_G}<span>How getting found on Google works</span></a><a href="/get-found-on-bing.html">{BING_B}<span>How getting found on Bing works</span></a></p>
            </div>"""


def found_teaser(site):
    text = site.get("found_text", "Just off APD-40, with free parking and a free shuttle within 5 miles.")
    return f"""
      <section class="d-section">
        <div class="wrap d-split p-found">
          <div>
            {plan_tag(site, "Google & Bing listings")}
            <h2>Find us on Google Maps and Bing</h2>
            <p>{esc(site['address'])}. {esc(text)}</p>
            <div class="p-found-badges"><span>{GOOGLE_G} Google Maps</span><span>{BING_B} Bing Maps</span></div>
            <a class="d-btn d-btn-brand" href="{url(site, 'areas')}">{icon('map-pin')} Directions &amp; areas we serve</a>{found_note(site)}
          </div>
          <div class="p-map-mini">{map_iframe(site)}</div>
        </div>
      </section>"""


def services_page(site):
    if has(site, "book"):
        intro = site.get("services_intro", "Clear prices before we start. Tap any service to book it online.")
    else:
        intro = "Clear prices before we start. Tap any service to get a free quote."
    title = page_name(site, "services")
    hero_title = "Services & prices" if title == "Services" else title
    note = site.get("svc_note", ("Not sure what you need?", "Text us a photo", "and we'll tell you."))
    body = sub_hero(site, hero_title, intro, "g1", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap">
          {service_cards(site, detailed=True)}
          <p class="p-note">{esc(note[0])} <a href="{SMS}">{esc(note[1])}</a> {esc(note[2])}</p>
        </div>
      </section>"""
    body += steps(site) + cta_band(site)
    seo = "Services & Prices" if title == "Services" else title
    return page(site, "services", f"{seo} | {site['name']}", f"{site['industry']} services and prices from {site['name']} in {city(site)}.", body, url(site, "services"))


def work_page(site):
    rows = ""
    for i, (cap, text) in enumerate(site["photos"], 1):
        rows += f"""
          <article class="p-row">
            <img src="{img(site, 'g' + str(i))}" alt="{esc(cap)}" loading="lazy" width="900" height="675" />
            <div><h2>{esc(cap)}</h2><p>{esc(text)}</p></div>
          </article>"""
    title = page_name(site, "work")
    body = sub_hero(site, title, site.get("work_intro", "A few recent jobs. New photos are added every month."), "g2", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap p-rows">{rows}
        </div>
      </section>""" + cta_band(site)
    return page(site, "work", f"{title} | {site['name']}", f"Photos of recent work from {site['name']}.", body, url(site, "work"))


def about_page(site):
    name, role = site["owner"]
    paras = "".join(f"<p>{esc(p)}</p>" for p in site["about"])
    checks = "".join(f"<li>{icon('circle-check')}<span>{esc(t)}</span></li>" for t in site["checks"])
    areas = "".join(f"<li>{esc(a if isinstance(a, str) else a[0])}</li>" for a in site["areas"])
    body = sub_hero(site, "About us", site["about_title"], "hero", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap d-split p-about">
          <figure class="d-portrait p-portrait"><img src="{img(site, 'portrait')}" alt="{esc(name)}" width="600" height="600" /><figcaption><b>{esc(name)}</b>{esc(role)}</figcaption></figure>
          <div><h2>Our story</h2>{paras}</div>
        </div>
      </section>
      <section class="d-section d-section-alt">
        <div class="wrap d-split">
          <div><h2>Our promise to you</h2><ul class="d-checks">{checks}</ul></div>
          <div><h2>Areas we serve</h2><ul class="d-areas">{areas}</ul></div>
        </div>
      </section>""" + cta_band(site)
    return page(site, "about", f"About {site['name']}", f"Meet {name}, {role.lower()} at {site['name']} in {city(site)}.", body, url(site, "about"))


def contact_page(site):
    options = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for _, t, _, _, _ in site["services"])
    title = page_name(site, "contact")
    addr = f'<li>{icon("map-pin")} {esc(site["address"])}</li>' if site.get("address") else ""
    form_title = "Send us a message" if has(site, "book") else site["cta"]
    book_note = ""
    if has(site, "book"):
        book_note = f'<p class="p-note">Want to pick a time instead? <a href="{url(site, "book")}">{esc(site["book"].get("contact_link", "Book online"))}</a> or <a href="{url(site, "estimate")}">{esc(site["est"].get("contact_link", "get a price estimate"))}</a>.</p>'
    photo_field = ""
    if site.get("contact_photos", True):
        photo_field = """
              <label for="q-photo">Add photos (optional)</label><input id="q-photo" name="photo" type="file" accept="image/*" multiple data-preview="q-preview" />
              <div class="p-preview" id="q-preview"></div>"""
    body = sub_hero(site, title, "Tell us what you need. We reply fast, usually the same day.", "g3", site["name"])
    body += f"""
      <section class="d-section d-contact p-contact">
        <div class="wrap d-split">
          <div>
            <h2>Call, text, or send the form</h2>
            <p>{esc(site.get("contact_note", "Whatever's easiest for you. A photo of the problem helps us give you a price faster."))}</p>
            <div class="p-reach-big">
              <a class="d-btn d-btn-accent" href="{TEL}">{icon('phone')} Call {PHONE}</a>
              <a class="d-btn d-btn-brand" href="{SMS}">{icon('message-circle')} Text {PHONE}</a>
            </div>
            <ul class="d-info">
              <li>{icon('clock')} {esc(site['hours'])}</li>{addr}
              <li>{icon('map-pin-check')} Serving {esc(', '.join((a if isinstance(a, str) else a[0]) for a in site['areas'][:4]))} and nearby</li>
            </ul>
            {book_note}
          </div>
          <div>
            <form class="d-form p-form" data-kind="quote" data-done="Thanks! Your request is in." novalidate>
              <h3>{esc(form_title)}</h3>
              <label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" data-sum="Name" required />
              <label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" data-sum="Phone" required />
              <label for="q-email">Email (optional)</label><input id="q-email" name="email" type="email" autocomplete="email" data-sum="Email" />
              <label for="q-service">{esc(site.get("form_label", "What do you need?"))}</label><select id="q-service" name="service" data-sum="Service" data-preselect>{options}<option value="Something else">Something else</option></select>
              <label for="q-details">Details</label><textarea id="q-details" name="details" data-sum="Details" placeholder="{esc(site.get("details_ph", "Tell us a little about the job"))}"></textarea>{photo_field}
              <fieldset class="p-radios"><legend>Best way to reach you</legend>
                <label><input type="radio" name="reach" value="Text" data-sum="Reach me by" checked /> Text</label>
                <label><input type="radio" name="reach" value="Call" data-sum="Reach me by" /> Call</label>
                <label><input type="radio" name="reach" value="Email" data-sum="Reach me by" /> Email</label>
              </fieldset>
              <button class="d-btn d-btn-accent" type="submit">{esc(site['cta'] if not has(site, 'book') else 'Send Message')}</button>
              <p class="d-form-msg" aria-live="polite"></p>
            </form>
            <div class="p-confirm" hidden></div>
          </div>
        </div>
      </section>"""
    if has(site, "areas"):
        body += map_block(site)
    return page(site, "contact", f"{title} | {site['name']}", f"Contact {site['name']} in {city(site)}. Call, text, or send a quick request.", body, url(site, "contact"))


def reviews_page(site):
    rating, count, dist = site["rating"]
    bars = "".join(
        f'<div class="p-bar"><span>{5 - i}</span><i><b style="width:{pct}%"></b></i><small>{pct}%</small></div>'
        for i, pct in enumerate(dist)
    )
    body = sub_hero(site, "Customer reviews", f"Rated {rating} out of 5 by {count} customers on Google.", "g3", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Google reviews section")}</div>
          {g_summary(site)}
          <div class="p-bars">{bars}</div>
          <div class="d-grid">{review_cards(site)}</div>
          <p class="d-sample-note">Sample reviews for this example. On your site, your real Google reviews show here.</p>
        </div>
      </section>""" + cta_band(site)
    return page(site, "reviews", f"Reviews | {site['name']}", f"Read {count} Google reviews for {site['name']}, rated {rating} stars.", body, url(site, "reviews"))


def blog_page(site):
    per = "Two new posts every month" if site["plan"] == "pro" else "A new post every month"
    body = sub_hero(site, "Blog", f"{per}: helpful tips from our team.", "g1", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Blog written for you")}<p>Every post has share buttons, so it's easy to post on Facebook and send to friends.</p></div>
          {post_cards(site, site['posts'])}
        </div>
      </section>""" + cta_band(site)
    return page(site, "blog", f"Blog | {site['name']}", f"Tips and advice from {site['name']} in {city(site)}.", body, url(site, "blog"))


def post_body(blocks):
    out = ""
    for kind, val in blocks:
        if kind == "ul":
            out += "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in val) + "</ul>"
        else:
            out += f"<{kind}>{esc(val)}</{kind}>"
    return out


def post_page(site, post):
    others = [p for p in site["posts"] if p is not post][:2]
    name, role = site["owner"]
    data = {
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"],
        "datePublished": post["date"], "author": {"@type": "Person", "name": name},
        "image": f"{SITE}{img(site, post['img'])}", "publisher": {"@type": "Organization", "name": site["name"]},
    }
    ld = f'<script type="application/ld+json">{json.dumps(data)}</script>'
    primary = (url(site, "book"), "Book Online") if has(site, "book") else (url(site, "contact"), site["cta"])
    body = f"""
      <article class="p-article">
        <div class="wrap p-article-wrap">
          <p class="p-crumbs"><a href="{url(site, 'blog')}">← Blog</a></p>
          <h1>{esc(post['title'])}</h1>
          <p class="p-byline">By {esc(name)} · {nice_date(post['date'])}</p>
          <img class="p-article-img" src="{img(site, post['img'])}" alt="" width="900" height="675" />
          <div class="p-article-body">{post_body(post['body'])}</div>
          <div class="p-article-share">{share_mount("Share this post")}{react_mount("post:" + site["slug"] + ":" + post["slug"], title="Was this helpful? Leave a reaction or a comment.")}</div>
          <div class="p-article-cta">
            <h2>Need help?</h2>
            <p>Call or text {esc(site['name'])}. We're happy to answer questions, even if you're not ready to book.</p>
            <div class="p-cta-actions">{reach_buttons(site, primary)}</div>
          </div>
        </div>
      </article>
      <section class="d-section d-section-alt">
        <div class="wrap">
          <div class="d-head"><h2>More from our blog</h2></div>
          {post_cards(site, others)}
        </div>
      </section>"""
    return page(site, "blog", f"{post['title']} | {site['name']}", post["excerpt"], body, post_url(site, post), image=img(site, post["img"]), extra_head=ld, share=False)


def book_page(site):
    b = site["book"]
    options = "".join(f'<option value="{esc(s)}">{esc(s)}</option>' for s in site["booking_services"])
    times = "".join(f'<button type="button" data-time="{esc(t)}">{esc(t)}</button>' for t in site["times"])
    closed = ",".join(str(d) for d in b.get("closed", [0]))
    short = "" if b.get("short_day") is None else str(b.get("short_day", 6))
    detail = ""
    if b.get("detail"):
        label, ph, sumname = b["detail"]
        detail = f'<label for="b-detail">{esc(label)}</label><input id="b-detail" name="detail" placeholder="{esc(ph)}" data-sum="{esc(sumname)}" required />'
    choice = ""
    if b.get("choice"):
        legend, sumname, opts = b["choice"]
        radios = "".join(
            f'<label><input type="radio" name="choice" value="{esc(v)}" data-sum="{esc(sumname)}"{" checked" if i == 0 else ""} /> {esc(lab)}</label>'
            for i, (v, lab) in enumerate(opts)
        )
        choice = f'<fieldset class="p-radios"><legend>{esc(legend)}</legend>{radios}</fieldset>'
    body = sub_hero(site, b.get("title", "Request a time"), b.get("intro", "Pick a service and a time that works for you. We'll text you to confirm. No account needed."), "g3", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap p-tool-wrap">
          <div class="d-head">{plan_tag(site, "Online booking (Pro)")}</div>
          <form class="d-form p-form p-book" data-kind="booking" data-done="{esc(b.get('done', 'Your time is requested!'))}" novalidate>
            <fieldset><legend><span>1</span> {esc(b.get('what', 'What do you need?'))}</legend>
              <select id="b-service" name="service" aria-label="Service" data-sum="{esc(b.get('what_sum', 'Service'))}" data-preselect required><option value="">{esc(b.get('choose', 'Choose a service…'))}</option>{options}</select>
            </fieldset>
            <fieldset><legend><span>2</span> Pick a day that works for you</legend>
              <div class="p-dates" data-days="12" data-closed="{closed}" data-short="{short}" data-short-after="{b.get('short_after', 12)}" role="group" aria-label="Available days"></div>
              <input type="hidden" name="day" data-sum="Day" data-need="a day" required />
            </fieldset>
            <fieldset><legend><span>3</span> Pick a time that works for you</legend>
              <div class="p-times" role="group" aria-label="Available times">{times}</div>
              <p class="p-hint">{esc(b.get('hint', "This is a request. We'll text you to confirm, or suggest the closest open time."))}</p>
              <input type="hidden" name="time" data-sum="Time" data-need="a time" required />
            </fieldset>
            <fieldset><legend><span>4</span> Your info</legend>
              <div class="p-two">
                <div><label for="b-name">Name</label><input id="b-name" name="name" autocomplete="name" data-sum="Name" required /></div>
                <div><label for="b-phone">Mobile phone</label><input id="b-phone" name="phone" type="tel" autocomplete="tel" data-sum="Phone" required /></div>
              </div>
              {detail}
              {choice}
              <label for="b-notes">Anything else? (optional)</label><textarea id="b-notes" name="notes" data-sum="Notes" placeholder="{esc(b.get('notes_ph', 'Questions or details'))}"></textarea>
            </fieldset>
            <button class="d-btn d-btn-accent" type="submit">{icon('calendar-days')} {esc(b.get('submit', 'Request This Time'))}</button>
            <p class="d-form-msg" aria-live="polite"></p>
          </form>
          <div class="p-confirm" hidden></div>
          <p class="p-note">{esc(b.get('est_note', "Not sure what it'll cost?"))} <a href="{url(site, 'estimate')}">{esc(b.get('est_link', 'Get a price estimate first'))}</a>.</p>
        </div>
      </section>"""
    title = page_name(site, "book")
    return page(site, "book", f"{title} | {site['name']}", f"{b['seo']} at {site['name']} in {city(site)}. Pick a day and time, no account needed.", body, url(site, "book"))


def estimate_page(site):
    e = site["est"]
    sizes = "".join(
        f'<label class="p-choice"><input type="radio" name="veh" value="{m}" data-name="{esc(n)}"{" checked" if i == 0 else ""} /><span>{icon(e["size_icon"])}{esc(n)}</span></label>'
        for i, (n, m) in enumerate(e["sizes"])
    )
    items = "".join(
        f'<label class="p-check"><input type="checkbox" value="{k}" data-name="{esc(n)}" data-low="{lo}" data-high="{hi}" data-book="{esc(bk)}" /><span><b>{esc(n)}</b><small>from {money(lo)}</small></span></label>'
        for k, n, lo, hi, bk in site["estimate"]
    )
    body = sub_hero(site, e["title"], e["intro"], "g1", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Quote tool (Pro)")}</div>
          <div class="p-est" data-est data-unit="{esc(e.get('unit', 'service'))}">
            <div>
              <fieldset><legend><span>1</span> {esc(e['size_legend'])}</legend><div class="p-choices">{sizes}</div></fieldset>
              <fieldset><legend><span>2</span> {esc(e.get('pick', 'Pick services'))}</legend><div class="p-checks">{items}</div></fieldset>
            </div>
            <aside class="p-total" aria-live="polite">
              <p class="p-total-label">Your estimate</p>
              <b class="p-total-num" data-est-total>$0</b>
              <p class="p-total-sub" data-est-count>{esc(e.get('empty', 'Pick a service to see your price.'))}</p>
              <ul class="p-total-lines" data-est-lines></ul>
              <a class="d-btn d-btn-accent" data-est-book href="{url(site, 'book')}">{icon('calendar-days')} {esc(e.get('book_btn', 'Book These Services'))}</a>
              <a class="d-btn d-btn-brand" data-est-text href="{SMS}">{icon('message-circle')} Text Me This Estimate</a>
              <p class="p-hint">{esc(e['hint'])}</p>
            </aside>
          </div>
        </div>
      </section>"""
    return page(site, "estimate", f"{e['seo']} | {site['name']}", f"Get an instant {e['seo'].lower()} from {site['name']} in {city(site)}.", body, url(site, "estimate"))


def map_block(site):
    q = quote_plus(city(site))
    return f"""
      <section class="d-section d-section-alt">
        <div class="wrap">
          <div class="d-head">{plan_tag(site, "Google & Bing listings")}<h2>Find us</h2><p>{esc(site['address'])}</p></div>
          <div class="p-map">{map_iframe(site)}</div>
          <div class="p-map-btns">
            <a class="p-map-btn" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">{GOOGLE_G}<span>Open in Google Maps</span></a>
            <a class="p-map-btn" href="https://www.bing.com/maps?q={q}" target="_blank" rel="noopener">{BING_B}<span>Open in Bing Maps</span></a>
            <a class="p-map-btn" href="https://maps.apple.com/?q={q}" target="_blank" rel="noopener">{icon('map-pin')}<span>Open in Apple Maps</span></a>
          </div>
          <p class="d-sample-note">This example shows {esc(city(site))}. Your real address and map pin go here.</p>{found_note(site)}
        </div>
      </section>"""


def areas_page(site):
    cards = "".join(
        f'<article class="d-card p-area"><div class="d-ico">{icon("map-pin-check")}</div><h3>{esc(t)}</h3><p>{esc(m)} {esc(site.get("area_from", "from the shop"))}</p></article>'
        for t, m in site["areas"]
    )
    body = sub_hero(site, "Find us & areas we serve", "Easy to find on Google Maps, Bing, and Apple Maps.", "hero", site["name"])
    body += map_block(site)
    body += f"""
      <section class="d-section">
        <div class="wrap">
          <div class="d-head"><h2>Areas we serve</h2><p>{esc(site.get('areas_intro', 'Drivers come from all over Bradley County and beyond. Free shuttle within 5 miles.'))}</p></div>
          <div class="d-grid p-area-grid">{cards}</div>
          <p class="p-note">Hours: {esc(site['hours'])}</p>
        </div>
      </section>""" + cta_band(site)
    return page(site, "areas", f"Directions & Areas We Serve | {site['name']}", f"Directions to {site['name']} in {city(site)}, and the towns we serve.", body, url(site, "areas"))


def faq_page(site):
    groups = {}
    for cat, q, a in site["faq"]:
        groups.setdefault(cat, []).append((q, a))
    blocks = ""
    for cat, items in groups.items():
        rows = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)
        blocks += f'<div class="p-faq-group"><h2>{esc(cat)}</h2><div class="d-faq">{rows}</div></div>'
    intro = site.get("faq_intro", "Quick answers about booking, prices, and warranties.")
    body = sub_hero(site, "Questions & answers", intro, "g2", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap p-faq">
          <label class="p-search">{icon('search-check')}<input type="search" placeholder="{esc(site.get('faq_ph', "Search questions (try 'warranty')"))}" aria-label="Search questions" data-faq-search /></label>
          {blocks}
          <p class="p-faq-empty" hidden>No matches. <a href="{SMS}">Text us your question</a> instead.</p>
        </div>
      </section>""" + cta_band(site)
    return page(site, "faq", f"FAQ | {site['name']}", f"{intro[:-1]} at {site['name']}.", body, url(site, "faq"))


def privacy_page(site):
    body = sub_hero(site, "Privacy Policy", "How we collect, use, and protect your information.", "hero", site["name"])
    body += f"""
      <section class="d-section">
        <div class="wrap p-article-body" style="max-width:760px">{privacy_body(site["name"], [(PHONE, TEL)], site.get("address") or city(site))}
        </div>
      </section>"""
    return page(site, "privacy", f"Privacy Policy | {site['name']}", f"Privacy policy for {site['name']}.", body, url(site, "privacy"), noindex=True)


BUILDERS = {
    "index": home, "services": services_page, "work": work_page, "about": about_page, "contact": contact_page,
    "reviews": reviews_page, "blog": blog_page, "book": book_page, "estimate": estimate_page, "areas": areas_page, "faq": faq_page,
}


def public_paths():
    paths = []
    for s in ALL_SITES:
        paths += [url(s, k) for k, _ in s["pages"]]
        paths += [post_url(s, p) for p in s.get("posts", [])]
    return paths


def gallery_cards():
    blurbs = {
        "starter": "5 pages, tap to call or text, and a quote form with photo upload. Everything a new business needs.",
        "growth": "Adds a Google reviews page and a blog with a new post each month, and share buttons on every page.",
        "pro": "Adds online booking, an instant price estimate tool, a Find Us map page, and a searchable FAQ.",
    }
    cards = ""
    for s in PLAN_SITES:
        plan = PLANS[s["plan"]]
        cards += f"""
            <div class="example-item">
            <a class="example-card plan-example plan-example-{s['plan']}" href="{url(s, 'index')}">
              <div class="example-thumb" style="background:linear-gradient(180deg,rgba(0,0,0,.05) 30%,{s['dark']}e6),url({img(s, 'hero')}) center/cover">
                <div class="thumb-bar"><i></i><i></i><i></i></div>
                <span class="plan-example-num">{s['num']}</span>
                <strong>{esc(s['name'])}</strong>
                <span>{esc(s['industry'])} · {len(s['pages'])} pages</span>
              </div>
              <div class="example-body">
                <span class="layout-tag">{s['num']} {esc(s['label'])}</span>
                <h3>{plan['name']} plan · {money(plan['setup'])} + {money(plan['monthly'])}/mo</h3>
                <p>{esc(blurbs[s['plan']])}</p>
                <span class="example-link">View {esc(s['label'].lower())} →</span>
              </div>
            </a>{react_mount("ex:" + s["slug"], full=False)}
            </div>"""
    return cards


def full_gallery_cards():
    cards = ""
    for s in FULL_SITES:
        cards += f"""
            <div class="example-item">
            <a class="example-card" href="{url(s, 'index')}">
              <div class="example-thumb" style="background:linear-gradient(180deg,rgba(0,0,0,.05) 30%,{s['dark']}e6),url({img(s, 'hero')}) center/cover">
                <div class="thumb-bar"><i></i><i></i><i></i></div>
                <strong>{esc(s['name'])}</strong>
                <span>{esc(s['industry'])} · {len(s['pages'])} pages</span>
              </div>
              <div class="example-body">
                <span class="layout-tag">{esc(s['industry'])}</span>
                <h3>{esc(s['industry'])} Website</h3>
                <p>{esc(page_name(s, 'book'))}, {esc(page_name(s, 'estimate').lower())} tool, Google reviews, blog, map, FAQ, and tap to call or text.</p>
                <span class="example-link">View example →</span>
              </div>
            </a>{react_mount("ex:" + s["slug"], full=False)}
            </div>"""
    return cards


def build():
    for s in ALL_SITES:
        for key, _ in s["pages"]:
            write(s, "index.html" if key == "index" else f"{key}.html", BUILDERS[key](s))
        for p in s.get("posts", []):
            write(s, f"blog/{p['slug']}.html", post_page(s, p))
        write(s, "privacy.html", privacy_page(s))
        print(f"wrote examples/{s['slug']} ({len(s['pages'])} pages, {len(s.get('posts', []))} posts)")


if __name__ == "__main__":
    build()
