"""Builds private preview websites into /preview/<slug>/. Not linked anywhere, not in the sitemap, and noindex."""
from html import escape
from pathlib import Path

from common import EMAIL, PHONE, PHONE_TEL, PLANS
from icons import icon
from previews_data import PREVIEWS

ROOT = Path(__file__).resolve().parent.parent

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#1d1d1f;background:var(--bg);line-height:1.6}
img{max-width:100%;display:block}a{color:inherit}.ico{width:1.1em;height:1.1em;vertical-align:-.18em;flex:none}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
.pv-bar{position:sticky;top:0;z-index:50;background:#111;color:#fff;font-size:14px;padding:8px 0}
.pv-bar .wrap{display:flex;gap:10px 16px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.pv-bar b{color:#ffd166}.pv-bar a.btn{padding:7px 14px;font-size:14px}
.hdr{background:var(--brand);color:#fff}.hdr .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 20px}
.hdr img{height:56px;width:auto;border-radius:6px}.hdr nav{display:flex;gap:18px;font-weight:600;font-size:15px}.hdr nav a{text-decoration:none;opacity:.9}
@media(max-width:760px){.hdr nav{display:none}}
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
.faq details{background:#fff;border-radius:12px;padding:14px 18px;margin-bottom:10px;box-shadow:0 1px 6px rgba(0,0,0,.06)}.faq summary{font-weight:700;cursor:pointer}
.contact{background:var(--brand);color:#fff}.contact .sub{color:rgba(255,255,255,.85)}.contact ul{list-style:none;padding:0;margin:0 0 24px}.contact li{display:flex;gap:10px;align-items:center;margin:8px 0;font-size:17px}
.contact .ico{color:var(--accent)}iframe{width:100%;height:280px;border:0;border-radius:14px;margin-top:20px}
.pv-end{background:#111;color:#fff;text-align:center}.pv-end p{max-width:640px;margin:0 auto 14px;font-size:17px}.pv-end .code{color:#ffd166;font-weight:700}
footer{background:var(--dark);color:rgba(255,255,255,.75);text-align:center;font-size:14px;padding:22px 0}
"""


def e(s):
    return escape(str(s))


def tel(phone):
    return "+1" + "".join(c for c in phone if c.isdigit())


def build_one(p):
    img = f"/preview/{p['slug']}/img/"
    plan = PLANS[p.get("plan", "starter")]
    keep = f"/start?plan={p.get('plan', 'starter')}&amp;preview={p['slug']}"
    phone_tel = tel(p["phone"])
    rating, count = p["rating"]
    services = "\n".join(
        f'<article class="card"><img src="{img}{f}" alt="{e(t)}" loading="lazy" width="460" height="300" /><div><h3>{e(t)}</h3><p>{e(d)}</p></div></article>'
        for f, t, d in p["services"]
    )
    photos = "\n".join(f'<figure><img src="{img}{f}" alt="{e(c)}" loading="lazy" /><figcaption>{e(c)}</figcaption></figure>' for f, c in p["photos"])
    reviews = "\n".join(f'<article class="rev"><span class="stars">★★★★★</span><p>“{e(t)}”</p><b>{e(n)}</b></article>' for t, n in p["reviews"])
    faq = "\n".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    about = "".join(f"<p>{e(x)}</p>" for x in p["about"])
    badges = "".join(f'<span>{icon("circle-check")} {e(b)}</span>' for b in p["badges"])
    fb = f'<li>{icon("users")} <a href="{e(p["facebook"])}" target="_blank" rel="noopener">Find us on Facebook</a></li>' if p.get("facebook") else ""
    maps_q = p["address"].replace(" ", "+")
    css_vars = f':root{{--brand:{p["brand"]};--dark:{p["dark"]};--accent:{p["accent"]};--accent-ink:{p["accent_ink"]};--bg:{p["bg"]}}}'
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex, nofollow" />
    <title>{e(p['name'])} | Free Website Preview</title>
    <link rel="icon" href="/assets/favicon-32.png" />
    <style>{css_vars}{CSS}</style>
  </head>
  <body>
    <div class="pv-bar"><div class="wrap">
      <span><b>Free preview</b> made for {e(p['name'])} by Stakich Websites. Not live yet.</span>
      <a class="btn btn-acc" href="{keep}">Keep this website</a>
    </div></div>
    <header class="hdr"><div class="wrap">
      <a href="#top"><img src="{img}{p['logo']}" alt="{e(p['name'])} logo" width="124" height="56" /></a>
      <nav><a href="#services">Services</a><a href="#about">About</a><a href="#reviews">Reviews</a><a href="#faq">FAQ</a><a href="#contact">Contact</a></nav>
      <a class="btn btn-acc" href="tel:{phone_tel}">{icon("phone")} Call</a>
    </div></header>
    <main id="top">
      <div class="hero" style="background-image:url('{p['hero']}')"><div class="wrap">
        <h1>{e(p['h1'])}</h1>
        <p>{e(p['tagline'])}</p>
        <div class="btns">
          <a class="btn btn-acc" href="tel:{phone_tel}">{icon("phone")} Call {e(p['phone'])}</a>
          <a class="btn btn-ghost" href="sms:{phone_tel}">{icon("message-circle")} Text us</a>
          <a class="btn btn-ghost" href="mailto:{e(p['email'])}?subject=Free%20estimate">{icon("mail")} Free estimate</a>
        </div>
        <p class="rate"><span class="stars">★★★★★</span> {rating} on Google ({count} reviews)</p>
      </div></div>
      <div class="badges"><div class="wrap">{badges}</div></div>

      <section id="services"><div class="wrap">
        <h2>Our services</h2>
        <p class="sub">Roofing and home improvement, from the inside out and from the ground up.</p>
        <div class="grid">
{services}
        </div>
      </div></section>

      <section id="about" class="alt"><div class="wrap about">
        <img src="{img}{p['about_photo']}" alt="{e(p['owner'])}" />
        <div><h2>{e(p['about_title'])}</h2>{about}<p><b>{e(p['owner'])}</b>, Owner</p></div>
      </div></section>

      <section id="work"><div class="wrap">
        <h2>Our work</h2>
        <p class="sub">A few photos from recent jobs.</p>
        <div class="photos">
{photos}
        </div>
      </div></section>

      <section id="reviews" class="alt"><div class="wrap">
        <h2>What customers say</h2>
        <p class="sub"><span class="stars">★★★★★</span> {rating} on Google from {count} reviews</p>
        <div class="grid">
{reviews}
        </div>
      </div></section>

      <section id="faq" class="faq"><div class="wrap">
        <h2>Common questions</h2>
        <p class="sub">Quick answers before you call.</p>
{faq}
      </div></section>

      <section id="contact" class="contact"><div class="wrap">
        <h2>Get your free estimate</h2>
        <p class="sub">Call, text, or email. Ask for {e(p['owner'].split()[0])}.</p>
        <ul>
          <li>{icon("phone")} <a href="tel:{phone_tel}">{e(p['phone'])}</a></li>
          <li>{icon("mail")} <a href="mailto:{e(p['email'])}">{e(p['email'])}</a></li>
          <li>{icon("map-pin")} {e(p['address'])}</li>
          <li>{icon("map")} Serving {e(p['area'])}</li>
          {fb}
        </ul>
        <div class="btns"><a class="btn btn-acc" href="tel:{phone_tel}">{icon("phone")} Call now</a><a class="btn btn-ghost" href="sms:{phone_tel}">{icon("message-circle")} Text us</a></div>
        <iframe title="Map to {e(p['name'])}" loading="lazy" src="https://maps.google.com/maps?q={e(maps_q)}&output=embed"></iframe>
      </div></section>

      <section class="pv-end"><div class="wrap">
        <h2>Like it? It can be yours.</h2>
        <p>Jeremy at Stakich Websites built this free preview for {e(p['name'])}. Keep it for ${plan['setup']} to set up and ${plan['monthly']} a month for hosting, updates, and help showing up on Google. No contract.</p>
        <p>First 10 customers save $100 with code <span class="code">FIRST100</span>.</p>
        <div class="btns" style="justify-content:center">
          <a class="btn btn-acc" href="{keep}">Keep this website</a>
          <a class="btn btn-ghost" href="sms:{PHONE_TEL}">{icon("message-circle")} Text Jeremy {e(PHONE)}</a>
          <a class="btn btn-ghost" href="mailto:{EMAIL}?subject={e(p['name'])}%20website">{icon("mail")} Email Jeremy</a>
        </div>
      </div></section>
    </main>
    <footer><div class="wrap">© {e(p['name'])} · Free preview by <a href="/">Stakich Websites</a> · Not live yet</div></footer>
  </body>
</html>
"""
    out = ROOT / "preview" / p["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote preview/{p['slug']}")


def build():
    for p in PREVIEWS:
        build_one(p)


if __name__ == "__main__":
    build()
