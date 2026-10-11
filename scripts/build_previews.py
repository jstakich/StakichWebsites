"""Builds private preview websites into /preview/<slug>/. Not linked anywhere, not in the sitemap, and noindex.

Every preview shows every feature that fits the business (default: Pro plan), and says clearly which plan it shows.
"""
from datetime import datetime
from html import escape
from pathlib import Path

from common import EMAIL, JS_V, PHONE, PHONE_TEL, PLANS, share_mount
from icons import BING_B, GOOGLE_G, icon
from client_privacy import privacy_body
from previews_data import PREVIEWS

ROOT = Path(__file__).resolve().parent.parent
STYLES = ROOT / "styles.css"
CUR = ' aria-current="page"'
AVATAR_COLORS = ["#1a73e8", "#e8710a", "#188038", "#a142f4", "#d93025"]
FB_PATH = "M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"
FB = f'<svg class="fb-logo" viewBox="0 0 24 24" aria-hidden="true"><path fill="#1877F2" d="{FB_PATH}"/></svg>'

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#1d1d1f;background:var(--bg);line-height:1.6}
img{max-width:100%;display:block}a{color:inherit}.ico{width:1.1em;height:1.1em;vertical-align:-.18em;flex:none}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
.pv-bar{position:sticky;top:0;z-index:50;background:#111;color:#fff;font-size:14px;padding:8px 0}
.pv-bar .wrap{display:flex;gap:10px 16px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.pv-bar b{color:#ffd166}.pv-bar a.btn{padding:7px 14px;font-size:14px;flex:none}
.pv-bar .wrap>span{flex:1 1 320px}
.hdr .brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;font-weight:800;font-size:19px;line-height:1.15;max-width:300px}
@media(max-width:600px){.hdr .brand{font-size:15px;gap:8px}.hdr .brand img{height:40px}}
.hdr{background:var(--brand);color:#fff}.hdr .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 20px}
.hdr img{height:56px;width:auto;border-radius:6px}.hdr nav{display:flex;gap:18px;font-weight:600;font-size:15px}.hdr nav a{text-decoration:none;opacity:.9}.hdr nav a[aria-current]{opacity:1;border-bottom:2px solid var(--accent)}.hdr nav{flex-wrap:wrap;justify-content:flex-end;gap:6px 16px}
.hdr .wrap{position:relative}.mnav{display:none}.mnav summary{list-style:none;cursor:pointer;display:flex;gap:6px;align-items:center;font-weight:700;padding:10px 12px;border:2px solid rgba(255,255,255,.6);border-radius:999px}
.mnav summary::-webkit-details-marker{display:none}.mnav div{position:absolute;right:20px;top:100%;z-index:40;background:var(--brand);border-radius:0 0 14px 14px;padding:8px 18px 14px;display:grid;min-width:220px;box-shadow:0 8px 20px rgba(0,0,0,.25)}
.mnav div a{padding:10px 0;font-weight:700;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.15)}
.mnav div a.btn{margin-top:12px;justify-content:center;border-bottom:0;padding:12px 16px}
@media(max-width:760px){.hdr nav{display:none}.mnav{display:block}.hdr .hdr-call{display:none}.hdr .brand{max-width:none;flex:1;min-width:0}.pv-bar{position:static}.hdr{position:sticky;top:0;z-index:45}}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;font-weight:700;text-decoration:none;border:2px solid transparent;cursor:pointer}
.btn-acc{background:var(--accent);color:var(--accent-ink)}.btn-ghost{border-color:rgba(255,255,255,.7);color:#fff}.btn-brand{background:var(--brand);color:#fff}
.hero{position:relative;color:#fff;background:var(--dark) center/cover no-repeat}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.78),rgba(0,0,0,.35))}
.hero .wrap{position:relative;padding:72px 20px 64px}.hero h1{font-size:clamp(30px,5vw,50px);line-height:1.12;margin:0 0 14px;max-width:760px}
.hero p{font-size:19px;max-width:640px;margin:0 0 22px}.btns{display:flex;flex-wrap:wrap;gap:10px}
.stars{color:#fbbc04;letter-spacing:2px}.hero .rate{margin-top:18px;font-weight:600}
.badges{background:var(--dark);color:#fff}.badges .wrap{display:flex;flex-wrap:wrap;gap:8px 26px;justify-content:center;padding:14px 20px;font-weight:600;font-size:15px}
.badges span{display:inline-flex;gap:7px;align-items:center}.badges .ico{color:var(--accent)}
section{padding:60px 0}section h2{font-size:clamp(26px,3.6vw,36px);margin:0 0 8px;line-height:1.2}.sub{margin:0 0 28px;color:#555;font-size:18px}
.alt{background:#fff}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.08)}.alt .card{background:var(--bg)}
.card img{aspect-ratio:46/30;object-fit:cover;width:100%}.card div{padding:14px 16px 18px}.card h3{margin:0 0 4px;font-size:18px}.card p{margin:0;color:#555;font-size:15px}
.about{display:grid;gap:30px;grid-template-columns:240px 1fr;align-items:start}.about img{border-radius:14px;width:100%}
@media(max-width:700px){.about{grid-template-columns:1fr}.about img{max-width:220px}}
.photos{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}.photos figure{margin:0}.photos img{border-radius:12px;aspect-ratio:4/3;object-fit:cover;width:100%}
.photos figcaption{font-size:14px;color:#555;margin-top:4px}
.rev{background:#fff;border-radius:14px;padding:20px;box-shadow:0 2px 10px rgba(0,0,0,.08)}.rev p{margin:6px 0 10px}.rev b{font-size:15px}
.faq details{background:#fff;border-radius:12px;padding:0 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,.06)}.faq summary{font-weight:700;cursor:pointer;padding:16px 0}.faq details p{margin:0 0 16px}
.contact{background:var(--brand);color:#fff}.contact .sub{color:rgba(255,255,255,.85)}.contact ul{list-style:none;padding:0;margin:0 0 24px}.contact li{display:flex;gap:10px;align-items:center;margin:8px 0;font-size:17px}
.contact .ico{color:var(--accent)}.contact .btn .ico,.contact .map-btn .ico{color:inherit}iframe{width:100%;height:280px;border:0;border-radius:14px;margin-top:20px}
.pv-end{background:#111;color:#fff;text-align:center}.pv-end p{max-width:640px;margin:0 auto 14px;font-size:17px}.pv-end .code{color:#ffd166;font-weight:700}
.pv-plan{background:#fff8d6;border-bottom:3px solid #ffd166;color:#2b2100}.pv-plan .wrap{padding:16px 20px;font-size:17px}.pv-plan b{font-size:19px}
.chip{display:inline-block;background:#111;color:#ffd166;font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:4px 10px;border-radius:999px;margin-bottom:10px}
.tool{background:#fff;border-radius:16px;padding:22px;box-shadow:0 2px 12px rgba(0,0,0,.08);max-width:760px}
.tool fieldset{border:0;padding:0;margin:0 0 16px}.tool legend{font-weight:800;margin-bottom:8px}
.opt{display:flex;gap:10px;align-items:center;padding:10px 12px;border:1px solid #ddd;border-radius:10px;margin:6px 0;cursor:pointer;background:#fff}
.opt input{width:20px;height:20px;accent-color:var(--brand)}.opt small{margin-left:auto;color:#666}
.est-out{font-size:26px;font-weight:800;margin:10px 0 4px;color:var(--brand)}.hint{font-size:14px;color:#666}
.tool label.f{display:block;font-weight:700;margin:12px 0 4px}.tool input[type=text],.tool input[type=tel],.tool input[type=date],.tool select,.tool textarea{width:100%;padding:12px;border:1px solid #ccc;border-radius:10px;font:inherit}
.done{background:#e8f6ec;border:1px solid #9fd3ad;border-radius:12px;padding:14px;margin-top:14px;font-weight:600}
.post{background:#fff;border-radius:14px;padding:18px;box-shadow:0 2px 10px rgba(0,0,0,.08)}.alt .post{background:var(--bg)}.post h3{margin:0 0 6px;font-size:18px}.post p{margin:0;color:#555;font-size:15px}
.pv-end ul{list-style:none;padding:0;margin:0 auto 18px;max-width:560px;text-align:left}.pv-end li{display:flex;gap:8px;margin:6px 0}.pv-end li .ico{color:#ffd166;margin-top:3px}
.g-logo,.bing-logo,.fb-logo{width:1.25em;height:1.25em;flex:none;vertical-align:-.25em}
.fb-btn{background:#1877F2;color:#fff}.fb-btn .fb-logo path{fill:#fff}
.g-summary{display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center;background:#fff;border-radius:16px;padding:18px 22px;box-shadow:0 2px 10px rgba(0,0,0,.08);margin-bottom:22px}
.alt .g-summary{background:var(--bg)}.g-brand{display:flex;gap:8px;align-items:center;font-weight:700}.g-score{display:flex;gap:10px;align-items:center}.g-score b{font-size:32px}.g-score small{color:#666}
.rev header{display:flex;gap:10px;align-items:center}.rev header div{flex:1}.rev header small{display:block;color:#777;font-size:13px}
.g-avatar{width:38px;height:38px;border-radius:50%;color:#fff;display:grid;place-items:center;font-weight:700}
.map-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}.map-btn{display:inline-flex;gap:8px;align-items:center;background:#fff;color:#1d1d1f;border-radius:999px;padding:10px 16px;font-weight:700;text-decoration:none}
.faq-search{display:flex;gap:8px;align-items:center;background:#fff;border:1px solid #ccc;border-radius:999px;padding:10px 16px;margin-bottom:16px;max-width:520px}.faq-search input{border:0;outline:0;font:inherit;flex:1;background:transparent}
.posts{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}.post-card{display:block;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.08);text-decoration:none}
.alt .post-card{background:var(--bg)}.post-card img{aspect-ratio:4/3;object-fit:cover;width:100%}.post-card div{padding:14px 16px 18px}.post-card h3{margin:2px 0 6px;font-size:18px}.post-card p{margin:0;color:#555;font-size:15px}
.date{font-size:13px;color:#777}.more{display:inline-block;margin-top:8px;font-weight:700;color:var(--brand)}
.article{max-width:760px;margin:0 auto;padding:40px 20px}.article h1{font-size:clamp(28px,4.5vw,42px);line-height:1.15;margin:8px 0}.article img{border-radius:14px;margin:18px 0;width:100%}
.article h2{font-size:24px;margin:26px 0 6px}.article p,.article li{font-size:18px}.crumbs a{font-weight:700;color:var(--brand)}
.stats{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}.stat{background:#fff;border-radius:14px;padding:16px;box-shadow:0 2px 10px rgba(0,0,0,.08)}.stat b{display:block;font-size:30px;color:var(--brand)}
.bar{display:grid;grid-template-columns:150px 1fr 44px;gap:10px;align-items:center;margin:8px 0}.bar i{background:#eee;border-radius:999px;height:12px;overflow:hidden}.bar i b{display:block;height:100%;background:var(--accent)}
.plans{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:24px 0;text-align:left}
.plan{background:#1d1d1f;border:2px solid #333;border-radius:16px;padding:20px;display:flex;flex-direction:column}.plan h3{margin:0 0 4px;font-size:24px}
.plan-price{margin:0 0 12px!important;font-size:16px!important}.plan-price b{font-size:22px;color:#fff}.plan ul{list-style:none;padding:0;margin:0 0 16px;flex:1}.plan li{display:flex;gap:8px;margin:6px 0;font-size:15px}.plan li .ico{color:#ffd166;margin-top:3px}
.plan-mine{border:3px solid #ffd166;background:#2a2410;box-shadow:0 0 0 4px rgba(255,209,102,.25)}.plan-flag{background:#ffd166;color:#111;font-weight:900;font-size:13px;letter-spacing:.05em;border-radius:999px;padding:5px 12px;margin:0 0 10px!important;align-self:flex-start}
@media(max-width:760px){.plans .plan .plan-flag,.plan .plan-flag{font-size:12px;letter-spacing:.02em;white-space:nowrap}}
.share-band{padding:30px 0;background:#fff;border-top:1px solid #eee}
.phero{position:relative;color:#fff;background:var(--dark) center/cover no-repeat}.phero:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.8),rgba(0,0,0,.45))}
.phero .wrap{position:relative;padding:46px 20px 40px}.phero h1{font-size:clamp(28px,4.6vw,44px);margin:0 0 8px;line-height:1.15}.phero p{margin:0;font-size:18px;max-width:640px}
.center{text-align:center;margin-top:24px}.mini-cta{background:var(--dark);color:#fff;text-align:center}.mini-cta p{margin:0 0 14px;font-size:18px}
.foot-links{margin:0 0 10px;line-height:2}.foot-links a{color:#fff}
footer{background:var(--dark);color:rgba(255,255,255,.75);text-align:center;font-size:14px;padding:22px 0}
"""

PLAN_EXTRAS = {
    "starter": ["Up to 5 pages, mobile-friendly", "Tap to call or text, plus a quote form", "Monthly hosting, HTTPS, security, and backups", "Built to show up in Google search", "2 small updates each month (new photos or text changes)"],
    "growth": ["Everything in Starter", "Up to 8 pages", "1 blog post written for you each month", "Blogs ready to share on social media", "Google reviews section", "Share buttons on every page"],
    "pro": ["Everything in Growth", "Up to 12 pages", "Online booking, menu, or quote tools", "2 blog posts each month", "Priority same-day updates when possible", "Get found on Google & Bing: your Google and Bing listings set up and kept current"],
}

SCRIPT = """<script>
(function(){
  var mn=document.querySelector(".mnav");
  if(mn){document.addEventListener("click",function(ev){if(mn.open&&(!mn.contains(ev.target)||ev.target.closest(".mnav div a")))mn.open=false;});
    document.addEventListener("keydown",function(ev){if(ev.key==="Escape")mn.open=false;});}
  var est=document.getElementById("est");
  if(est){var out=document.getElementById("est-out");
    est.addEventListener("change",function(){
      var m=parseFloat((est.querySelector("input[name=size]:checked")||{value:1}).value),lo=0,hi=0,n=0;
      est.querySelectorAll("input[name=item]:checked").forEach(function(c){lo+=+c.dataset.lo;hi+=+c.dataset.hi;n++;});
      var f=function(x){return "$"+(Math.round(x*m/10)*10).toLocaleString("en-US");};
      out.textContent=n?("About "+f(lo)+" to "+f(hi)):"Pick an item to see a price range.";
    });}
  var bk=document.getElementById("bk");
  if(bk)bk.addEventListener("submit",function(ev){ev.preventDefault();var d=document.getElementById("bk-done");d.hidden=false;d.scrollIntoView({block:"center",behavior:"smooth"});});
  var q=document.getElementById("faq-q");
  if(q)q.addEventListener("input",function(){var t=q.value.toLowerCase(),any=false;
    document.querySelectorAll("#faq details").forEach(function(d){var hit=d.textContent.toLowerCase().indexOf(t)>-1;d.hidden=!hit;if(hit)any=true;});
    document.getElementById("faq-none").hidden=any;});
})();
</script>"""


def e(s):
    return escape(str(s))


def tel(phone):
    return "+1" + "".join(c for c in phone if c.isdigit())


def nice_date(s):
    d = datetime.strptime(s, "%Y-%m-%d")
    return f"{d:%B} {d.day}, {d.year}"


def chip(text):
    return f'<span class="chip">{e(text)}</span>'


def share_css():
    css = STYLES.read_text(encoding="utf-8")
    a = css.index("/* ---------- Share buttons")
    b = css.index("/* ----------", a + 10)
    return css[a:b]


class Ctx:
    def __init__(self, p):
        self.p = p
        self.base = f"/preview/{p['slug']}/"
        self.img = self.base + "img/"
        self.plan_key = p.get("plan", "pro")
        self.plan = PLANS[self.plan_key]
        self.keep = f"/start?plan={self.plan_key}&amp;preview={p['slug']}"
        self.tel = tel(p["phone"])
        self.first = p["owner"].split()[0] if p.get("owner") else ""
        self.ask = f" Ask for {self.first}." if self.first else ""
        self.who = self.first or "We"
        self.whose = f"{self.first}'s" if self.first else "your"
        self.has_reviews = bool(p.get("reviews") or p.get("rating"))

    def post_url(self, post):
        return f"{self.base}blog/{post['slug']}.html"

    def url(self, key):
        return self.base if key == "index" else f"{self.base}{key}.html"

    def pages(self):
        p = self.p
        out = [("index", "Home"), ("services", "Services"), ("work", "Our Work"), ("about", "About")]
        if self.has_reviews:
            out.append(("reviews", "Reviews"))
        if p.get("posts"):
            out.append(("blog", "Blog"))
        if p.get("estimate"):
            out.append(("estimate", "Price Estimate"))
        if p.get("booking_services"):
            out.append(("book", "Book"))
        out += [("faq", "FAQ"), ("contact", "Contact")]
        return out


def shell(c, title, body, extra_head="", share=True, active=""):
    p, plan = c.p, c.plan
    plan_line = f"{plan['name'].upper()} plan: ${plan['setup']:,} setup, then ${plan['monthly']}/month"
    css_vars = f':root{{--white:#fff;--navy:#1d1d1f;--sky-line:#dde3ea;--radius:14px;--font-head:inherit;--font-body:inherit;--brand:{p["brand"]};--dark:{p["dark"]};--accent:{p["accent"]};--accent-ink:{p["accent_ink"]};--bg:{p["bg"]}}}'
    links = "".join(
        f'<a href="{c.url(k)}"{CUR if k == active else ""}>{e(n)}</a>' for k, n in c.pages() if k != "index"
    )
    foot_links = " · ".join(f'<a href="{c.url(k)}">{e(n)}</a>' for k, n in c.pages())
    social = ""
    if p.get("facebook"):
        social += f'<a class="map-btn" href="{e(p["facebook"])}" target="_blank" rel="noopener">{FB} Visit us on Facebook</a>'
    if p.get("google"):
        social += f'<a class="map-btn" href="{e(p["google"])}" target="_blank" rel="noopener">{GOOGLE_G} Find us on Google</a>'
    share_band = ""
    if share and c.plan_key in ("growth", "pro"):
        label = f"Share {p['name']} with a friend"
        share_band = f'\n    <section class="share-band"><div class="wrap">{share_mount(label)}</div></section>'
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex, nofollow" />
    <title>{e(title)}</title>
    <meta name="description" content="{e(p['tagline'])}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="{e(p['name'])}" />
    <meta property="og:title" content="{e(title)}" />
    <meta property="og:description" content="{e(p['tagline'])}" />
    <meta property="og:image" content="https://stakichwebsites.com{p['hero']}" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="/assets/favicon-32.png" />
    <style>{css_vars}{CSS}{share_css()}</style>{extra_head}
  </head>
  <body>
    <div class="pv-bar"><div class="wrap">
      <span><b>FREE PREVIEW</b> for {e(p['name'])} · You're looking at the <b>{e(plan_line)}</b> · <a href="{c.base}#plans" style="color:#ffd166">See all plans and prices</a></span>
      <a class="btn btn-acc" href="{c.keep}">Keep this website</a>
    </div></div>
    <header class="hdr"><div class="wrap">
      <a class="brand" href="{c.base}"><img src="{c.img}{p['logo']}" alt="" width="124" height="56" /><span>{e(p['name'])}</span></a>
      <nav>{links}</nav>
      <a class="btn btn-acc hdr-call" href="tel:{c.tel}">{icon("phone")} Call</a>
      <details class="mnav"><summary>{icon("menu")} Menu</summary><div>{links}<a class="btn btn-acc" href="tel:{c.tel}">{icon("phone")} Call {e(p['phone'])}</a></div></details>
    </div></header>
    <main id="top">{body}
    </main>{share_band}
    <footer><div class="wrap">
      <div class="map-btns" style="justify-content:center;margin:0 0 12px">{social}</div>
      <p class="foot-links">{foot_links}</p>
      © {e(p['name'])} · {e(p['address'])} · <a href="tel:{c.tel}">{e(p['phone'])}</a><br /><a href="{c.base}privacy.html">Privacy Policy</a> · Free preview by <a href="/">Stakich Websites</a> · Not live yet
    </div></footer>
    {SCRIPT}
    <script src="/share.js?v={JS_V}" defer></script>
  </body>
</html>
"""


def review_cards(c, limit=None):
    out = ""
    for i, r in enumerate(c.p.get("reviews", [])[:limit]):
        text, who = r[0], r[1]
        color = AVATAR_COLORS[i % len(AVATAR_COLORS)]
        out += f"""
          <article class="rev">
            <header><span class="g-avatar" style="background:{color}">{e(who[0].upper())}</span><div><b>{e(who)}</b><small>Google review</small></div>{GOOGLE_G}</header>
            <span class="stars">★★★★★</span>
            <p>“{e(text)}”</p>
          </article>"""
    return out


def reviews_section(c, limit=None):
    p = c.p
    if not c.has_reviews:
        return ""
    rating, count = p["rating"]
    rv = p.get("google_review")
    g = p.get("google")
    review_btn = f'<a class="btn btn-acc" href="{e(rv)}" target="_blank" rel="noopener">{icon("square-pen")} Review us on Google</a>' if rv else ""
    read_btn = f'<a class="btn btn-brand" href="{e(g)}" target="_blank" rel="noopener">{icon("star")} Read all reviews on Google</a>' if g else ""
    more = f'<p class="center"><a class="btn btn-brand" href="{c.url("reviews")}">See all reviews</a></p>' if limit and len(p.get("reviews", [])) > limit else ""
    cards = f'<div class="grid">{review_cards(c, limit)}\n        </div>' if p.get("reviews") else ""
    return f"""
      <section id="reviews" class="alt"><div class="wrap">
        {chip("Growth and Pro plan feature")}
        <h2>What customers say</h2>
        <div class="g-summary">
          <div class="g-brand">{GOOGLE_G}<span>Google Reviews</span></div>
          <div class="g-score"><b>{rating}</b><span class="stars">★★★★★</span><small>Based on {count} reviews</small></div>
          <div class="btns">{review_btn}{read_btn}</div>
        </div>
        {cards}
        {more}
      </div></section>"""


def estimate_section(c):
    p = c.p
    if not p.get("estimate"):
        return ""
    sizes = "".join(
        f'<label class="opt"><input type="radio" name="size" value="{m}"{" checked" if i == 0 else ""} /> {e(n)}</label>'
        for i, (n, m) in enumerate(p["sizes"])
    )
    items = "".join(
        f'<label class="opt"><input type="checkbox" name="item" data-lo="{lo}" data-hi="{hi}" /> {e(n)}<small>${lo:,}–${hi:,}</small></label>'
        for n, lo, hi in p["estimate"]
    )
    return f"""
      <section id="estimate" class="alt"><div class="wrap">
        {chip("Pro plan feature")}
        <h2>Instant price estimate</h2>
        <p class="sub">{e(p.get("est_sub", "Pick your home size and what you need. See a price range in seconds, day or night."))}</p>
        <form class="tool" id="est" onsubmit="return false">
          <fieldset><legend>{e(p.get("size_label", "Your home size"))}</legend>{sizes}</fieldset>
          <fieldset><legend>What do you need?</legend>{items}</fieldset>
          <p class="est-out" id="est-out">Pick an item to see a price range.</p>
          <p class="hint">{e(p.get("est_note", "Sample prices for this preview. Real prices are set by the owner before the website goes live."))}</p>
          <a class="btn btn-brand" href="{c.url("book")}">{icon("calendar-days")} {e(p.get("est_btn", "Request a free estimate"))}</a>
        </form>
      </div></section>"""


def booking_section(c):
    p = c.p
    if not p.get("booking_services"):
        return ""
    opts = "".join(f"<option>{e(x)}</option>" for x in p["booking_services"])
    times = "".join(f"<option>{e(t)}</option>" for t in p.get("times", ["Morning", "Afternoon", "Evening"]))
    return f"""
      <section id="book"><div class="wrap">
        {chip("Pro plan feature")}
        <h2>{e(p.get("book_title", "Request a free estimate online"))}</h2>
        <p class="sub">Pick what you need and a day that works. {e(c.who)} will call or text to confirm. No account needed.</p>
        <form class="tool" id="bk">
          <label class="f" for="bk-s">What do you need?</label><select id="bk-s">{opts}</select>
          <label class="f" for="bk-d">Day</label><input id="bk-d" type="date" />
          <label class="f" for="bk-t">Time</label><select id="bk-t">{times}</select>
          <label class="f" for="bk-n">Your name</label><input id="bk-n" type="text" autocomplete="name" />
          <label class="f" for="bk-p">Cell phone</label><input id="bk-p" type="tel" autocomplete="tel" />
          <label class="f" for="bk-a">Address and details</label><textarea id="bk-a" rows="3" placeholder="{e(p.get('book_ph', 'Street and town, and a few details'))}"></textarea>
          <p style="margin-top:16px"><button class="btn btn-brand" type="submit">{icon("calendar-days")} {e(p.get("book_btn", "Request my estimate"))}</button></p>
          <p class="done" id="bk-done" hidden>This is a preview, so nothing was sent. On the live website, this request goes straight to {e(c.whose)} email, so it pops up on the phone right away.</p>
        </form>
      </div></section>"""


def post_cards(c, posts):
    return "".join(
        f'<a class="post-card" href="{c.post_url(x)}"><img src="{e(x["img"])}" alt="" loading="lazy" /><div><span class="date">{nice_date(x["date"])}</span><h3>{e(x["title"])}</h3><p>{e(x["excerpt"])}</p><span class="more">Read more →</span></div></a>'
        for x in posts
    )


def blog_section(c, limit=None):
    if not c.p.get("posts"):
        return ""
    per = "2 new posts every month" if c.plan_key == "pro" else "A new post every month"
    more = f'<p class="center"><a class="btn btn-brand" href="{c.url("blog")}">See all posts</a></p>' if limit else ""
    return f"""
      <section id="blog"><div class="wrap">
        {chip("Growth and Pro plan feature")}
        <h2>Tips from our blog</h2>
        <p class="sub">{per}, written for you and ready to share on Facebook.</p>
        <div class="posts">{post_cards(c, c.p["posts"][:limit])}</div>
        {more}
      </div></section>"""


def faq_section(c):
    p = c.p
    rows = "\n".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    return f"""
      <section id="faq" class="faq alt"><div class="wrap">
        <h2>Common questions</h2>
        <p class="sub">Quick answers before you call.</p>
        <label class="faq-search">{icon("search-check")}<input id="faq-q" type="search" placeholder="Search questions (try '{e(p.get("faq_try", "warranty"))}')" aria-label="Search questions" /></label>
{rows}
        <p id="faq-none" hidden>No matches. <a href="sms:{c.tel}">Text us your question</a> instead.</p>
      </div></section>"""


def contact_section(c):
    p = c.p
    q = p["address"].replace(" ", "+")
    fb = f'<li>{FB} <a href="{e(p["facebook"])}" target="_blank" rel="noopener">Find us on Facebook</a></li>' if p.get("facebook") else ""
    g = f'<li>{GOOGLE_G} <a href="{e(p["google"])}" target="_blank" rel="noopener">See us on Google</a></li>' if p.get("google") else ""
    rv = f'<li>{icon("square-pen")} <a href="{e(p["google_review"])}" target="_blank" rel="noopener">Review us on Google</a></li>' if p.get("google_review") else ""
    hours = f'<li>{icon("clock")} {e(p["hours"])}</li>' if p.get("hours") else ""
    return f"""
      <section id="contact" class="contact"><div class="wrap">
        <h2>{e(p.get("contact_title", "Get your free estimate"))}</h2>
        <p class="sub">Call, text, or email.{e(c.ask)}</p>
        <ul>
          <li>{icon("phone")} <a href="tel:{c.tel}">{e(p['phone'])}</a></li>
          <li>{icon("mail")} <a href="mailto:{e(p['email'])}">{e(p['email'])}</a></li>
          <li>{icon("map-pin")} {e(p['address'])}</li>
          <li>{icon("map")} Serving {e(p['area'])}</li>
          {hours}{g}{rv}{fb}
        </ul>
        <div class="btns"><a class="btn btn-acc" href="tel:{c.tel}">{icon("phone")} Call now</a><a class="btn btn-ghost" href="sms:{c.tel}">{icon("message-circle")} Text us</a></div>
        <h3 style="margin-top:30px">Find us</h3>
        {chip("Pro plan: Google and Bing listings")}
        <iframe title="Map to {e(p['name'])}" loading="lazy" src="https://maps.google.com/maps?q={e(q)}&amp;output=embed"></iframe>
        <div class="map-btns">
          <a class="map-btn" href="https://www.google.com/maps/search/?api=1&amp;query={e(q)}" target="_blank" rel="noopener">{GOOGLE_G} Google Maps</a>
          <a class="map-btn" href="https://www.bing.com/maps?q={e(q)}" target="_blank" rel="noopener">{BING_B} Bing Maps</a>
          <a class="map-btn" href="https://maps.apple.com/?q={e(q)}" target="_blank" rel="noopener">{icon("map-pin")} Apple Maps</a>
        </div>
      </div></section>"""


def plan_cards(c):
    cards = ""
    for key in ("starter", "growth", "pro"):
        pl = PLANS[key]
        mine = key == c.plan_key
        flag = '<p class="plan-flag">THIS IS THE PLAN YOU\'RE SEEING</p>' if mine else ""
        feats = "".join(f"<li>{icon('circle-check')} {e(x)}</li>" for x in PLAN_EXTRAS[key])
        btn_cls = "btn-acc" if mine else "btn-ghost"
        cards += f"""
          <div class="plan{' plan-mine' if mine else ''}">
            {flag}
            <h3>{e(pl['name'])}</h3>
            <p class="plan-price"><b>${pl['setup']:,}</b> setup<br />then <b>${pl['monthly']}/month</b></p>
            <ul>{feats}</ul>
            <a class="btn {btn_cls}" href="/start?plan={key}&amp;preview={c.p['slug']}">Pick {e(pl['name'])}</a>
          </div>"""
    return f'<div class="plans">{cards}\n        </div>'


def end_section(c):
    p, plan = c.p, c.plan
    return f"""
      <section class="pv-end" id="plans"><div class="wrap">
        <h2>Like it? It can be yours.</h2>
        <p>Jeremy at Stakich Websites built this free preview for {e(p['name'])}. <b>You're seeing the {e(plan['name'])} plan.</b> To keep everything you see here, pick <b>{e(plan['name'])}</b>. Smaller plans leave out the parts with black labels. No contract on any plan.</p>
        {plan_cards(c)}
        <p>First 10 customers save $100 with code <span class="code">FIRST100</span>.</p>
        <div class="btns" style="justify-content:center">
          <a class="btn btn-acc" href="{c.keep}">Keep this website ({e(plan['name'])} plan)</a>
          <a class="btn btn-ghost" href="sms:{PHONE_TEL}">{icon("message-circle")} Text Jeremy {e(PHONE)}</a>
          <a class="btn btn-ghost" href="mailto:{EMAIL}?subject={e(p['name'])}%20website">{icon("mail")} Email Jeremy</a>
        </div>
      </div></section>"""


def page_hero(c, title, sub):
    return f"""
      <div class="phero" style="background-image:url('{c.p['hero']}')"><div class="wrap">
        <h1>{e(title)}</h1>
        <p>{e(sub)}</p>
      </div></div>"""


def services_section(c, limit=None):
    p = c.p
    cards = "\n".join(
        f'<article class="card"><img src="{c.img}{f}" alt="{e(t)}" loading="lazy" width="460" height="300" /><div><h3>{e(t)}</h3><p>{e(d)}</p></div></article>'
        for f, t, d in p["services"][:limit]
    )
    more = f'<p class="center"><a class="btn btn-brand" href="{c.url("services")}">See all {len(p["services"])} services</a></p>' if limit else ""
    return f"""
      <section id="services"><div class="wrap">
        <h2>Our services</h2>
        <p class="sub">{e(p.get('services_sub', 'Friendly, reliable service from a local, family-owned business.'))}</p>
        <div class="grid">
{cards}
        </div>
        {more}
      </div></section>"""


def about_section(c, teaser=False):
    p = c.p
    paras = p["about"][:1] if teaser else p["about"]
    about = "".join(f"<p>{e(x)}</p>" for x in paras)
    owner = f"<p><b>{e(p['owner'])}</b>, Owner</p>" if p.get("owner") else ""
    more = f'<p><a class="btn btn-brand" href="{c.url("about")}">Our story</a></p>' if teaser else owner
    return f"""
      <section id="about" class="alt"><div class="wrap about">
        <img src="{c.img}{p['about_photo']}" alt="{e(p.get('about_alt') or p.get('owner') or p['name'])}" />
        <div><h2>{e(p['about_title'])}</h2>{about}{more}</div>
      </div></section>"""


def work_section(c):
    photos = "\n".join(f'<figure><img src="{c.img}{f}" alt="{e(cap)}" loading="lazy" /><figcaption>{e(cap)}</figcaption></figure>' for f, cap in c.p["photos"])
    return f"""
      <section id="work"><div class="wrap">
        <h2>Our work</h2>
        <p class="sub">{e(c.p.get("work_sub", "Photos from recent jobs. New photos are added as jobs are finished."))}</p>
        <div class="photos">
{photos}
        </div>
      </div></section>"""


def mini_cta(c):
    plan = c.plan
    book = f'<a class="btn btn-ghost" href="{c.url("book")}">{icon("calendar-days")} Book online</a>' if c.p.get("booking_services") else ""
    return f"""
      <section class="mini-cta"><div class="wrap">
        <p>{e(c.p.get("cta_line", "Ready for a free estimate? Call, text, or book online."))}{e(c.ask)}</p>
        <div class="btns" style="justify-content:center">
          <a class="btn btn-acc" href="tel:{c.tel}">{icon("phone")} Call {e(c.p['phone'])}</a>
          <a class="btn btn-ghost" href="sms:{c.tel}">{icon("message-circle")} Text us</a>
          {book}
        </div>
      </div></section>
      <div class="pv-plan"><div class="wrap">
        <b>This preview shows the {e(plan['name'].upper())} plan.</b> <a href="{c.base}#plans">See all plans and prices</a> or <a href="{c.keep}">keep this website</a>.
      </div></div>"""


def home(c):
    p, plan = c.p, c.plan
    badges = "".join(f'<span>{icon("circle-check")} {e(b)}</span>' for b in p["badges"])
    rate = ""
    if p.get("rating"):
        r, n = p["rating"]
        txt = f"{r} on Google ({n} reviews)"
        rate = f'<p class="rate">{GOOGLE_G} <span class="stars">★★★★★</span> ' + (f'<a href="{e(p["google"])}" target="_blank" rel="noopener">{txt}</a>' if p.get("google") else txt) + "</p>"
    est_btn = f'<a class="btn btn-ghost" href="{c.url("estimate")}">{icon("calculator")} Get a price</a>' if p.get("estimate") else ""
    book_btn = f'<a class="btn btn-ghost" href="{c.url("book")}">{icon("calendar-days")} Book online</a>' if p.get("booking_services") else ""
    body = f"""
      <div class="hero" style="background-image:url('{p['hero']}')"><div class="wrap">
        <h1>{e(p['h1'])}</h1>
        <p>{e(p['tagline'])}</p>
        <div class="btns">
          <a class="btn btn-acc" href="tel:{c.tel}">{icon("phone")} Call {e(p['phone'])}</a>
          {est_btn}{book_btn}
          <a class="btn btn-ghost" href="sms:{c.tel}">{icon("message-circle")} Text us</a>
        </div>
        {rate}
      </div></div>
      <div class="badges"><div class="wrap">{badges}</div></div>
      <div class="pv-plan"><div class="wrap">
        <b>This preview shows the {e(plan['name'].upper())} plan.</b> To keep everything you see here, pick <b>{e(plan['name'])}</b> when you order. Parts marked with a black label are only in certain plans.
      </div></div>
{services_section(c, limit=6)}
{about_section(c, teaser=True)}
{reviews_section(c, limit=3)}
{blog_section(c, limit=3)}
{end_section(c)}"""
    return shell(c, f"{p['name']} | Free Website Preview", body, active="index")


def sub_page(c, key, title, sub, section):
    return shell(c, f"{title} | {c.p['name']}", page_hero(c, title, sub) + section + mini_cta(c), active=key)


def sub_pages(c):
    p = c.p
    first = c.first
    out = {
        "services": ("Services", p.get("services_sub", "Everything we offer, all in one place."), services_section(c)),
        "work": ("Our Work", f"Real jobs from around {p.get('city', 'our area')}.", work_section(c)),
        "about": ("About Us", p["about_title"], about_section(c)),
        "faq": ("Questions & Answers", "Quick answers before you call.", faq_section(c)),
        "contact": ("Contact", f"Call, text, or email.{c.ask}", contact_section(c)),
    }
    if c.has_reviews:
        out["reviews"] = ("Customer Reviews", f"Rated {p['rating'][0]} out of 5 on Google.", reviews_section(c))
    if p.get("posts"):
        out["blog"] = ("Blog", "Helpful tips from our team.", blog_section(c))
    if p.get("estimate"):
        out["estimate"] = ("Price Estimate", "See a price range in seconds, day or night.", estimate_section(c))
    if p.get("booking_services"):
        out["book"] = ("Book Online", p.get("book_sub", f"Request a free estimate. {c.who} will call or text to confirm."), booking_section(c))
    return out


def post_page(c, post):
    p = c.p
    blocks = ""
    for kind, val in post["body"]:
        if kind == "ul":
            blocks += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in val) + "</ul>"
        else:
            blocks += f"<{kind}>{e(val)}</{kind}>"
    others = [x for x in p["posts"] if x is not post]
    body = f"""
      <article class="article">
        <p class="crumbs"><a href="{c.url("blog")}">← Blog</a></p>
        {chip("Growth and Pro plan feature: blog written for you")}
        <h1>{e(post['title'])}</h1>
        <p class="date">By {e(p.get('owner') or p['name'])} · {nice_date(post['date'])}</p>
        <img src="{e(post['img'])}" alt="" />
        {blocks}
        <div style="margin-top:28px">{share_mount("Share this post")}</div>
        <div class="tool" style="margin-top:28px">
          <h2 style="margin-top:0">Need help?</h2>
          <p>Call or text {e(p['name'])}. {e(p.get("post_help", "Estimates are free."))}</p>
          <div class="btns"><a class="btn btn-acc" href="tel:{c.tel}">{icon("phone")} Call {e(p['phone'])}</a><a class="btn btn-brand" href="sms:{c.tel}">{icon("message-circle")} Text us</a></div>
        </div>
      </article>
      <section class="alt"><div class="wrap">
        <h2>More from our blog</h2>
        <div class="posts">{post_cards(c, others)}</div>
      </div></section>"""
    return shell(c, f"{post['title']} | {p['name']}", body, share=False)


def privacy_page(c):
    p = c.p
    contact = [(p["phone"], f"tel:{c.tel}")]
    if p.get("email"):
        contact.insert(0, (p["email"], f"mailto:{p['email']}"))
    body = f"""
      <article class="article">
        <p class="crumbs"><a href="{c.base}">← Home</a></p>
        <h1>Privacy Policy</h1>{privacy_body(p["name"], contact, p["address"])}
      </article>"""
    return shell(c, f"Privacy Policy | {p['name']}", body)


def write(rel, html):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def build():
    for p in PREVIEWS:
        c = Ctx(p)
        write(f"preview/{p['slug']}/index.html", home(c))
        for post in p.get("posts", []):
            write(f"preview/{p['slug']}/blog/{post['slug']}.html", post_page(c, post))
        for key, (title, sub, section) in sub_pages(c).items():
            write(f"preview/{p['slug']}/{key}.html", sub_page(c, key, title, sub, section))
        write(f"preview/{p['slug']}/privacy.html", privacy_page(c))
        print(f"wrote preview/{p['slug']} ({len(p.get('posts', []))} posts)")


if __name__ == "__main__":
    build()
