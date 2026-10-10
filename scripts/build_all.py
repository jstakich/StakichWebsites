"""Rebuilds every generated page and the sitemap. Run: python3 scripts/build_all.py"""
import json
from datetime import date
from html import escape
from pathlib import Path

import build_blog
import build_examples
import build_found
import build_pages
import build_plan_examples
import build_start
from icons import fill_icons
from common import react_mount, EMAIL, FORM_TO, PAY_BADGES, PHONE, PHONE_TEL, SITE, footer, head, scripts, share_mount, topbar
from posts import POSTS

ROOT = Path(__file__).resolve().parent.parent

HOME_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Stakich Websites",
    "url": f"{SITE}/",
    "logo": f"{SITE}/assets/icon-512.png",
    "image": f"{SITE}/assets/og-image.png",
    "description": "Website design, hosting, and care plans for small businesses.",
    "founder": {"@type": "Person", "name": "Jeremy Stakich"},
    "email": EMAIL,
    "address": {"@type": "PostalAddress", "addressLocality": "Charleston", "addressRegion": "TN", "addressCountry": "US"},
    "areaServed": {"@type": "Country", "name": "United States"},
    "priceRange": "$499–$1,499",
    "paymentAccepted": "Credit Card, Debit Card, Apple Pay, Google Pay",
}


def home():
    latest = "\n".join(
        f"""            <article class="blog-item">
              <p class="blog-meta">{build_blog.nice_date(p['date'])}</p>
              <h3><a href="/blog/{p['slug']}.html">{escape(p['title'])}</a></h3>
              <p>{escape(p['excerpt'])}</p>
            </article>"""
        for p in POSTS[:3]
    )
    body = (ROOT / "scripts" / "home_body.html").read_text(encoding="utf-8")
    body = (
        body.replace("{{PAY_BADGES}}", PAY_BADGES)
        .replace("{{LATEST_POSTS}}", latest)
        .replace("{{REACT_HOME}}", react_mount("home", title="Like what you see? Leave a reaction or a comment."))
        .replace("{{SHARE}}", share_mount("Know a business owner who needs a website? Share this"))
        .replace("{{EMAIL}}", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
        .replace("{{FORM_TO}}", FORM_TO)
        .replace("{{PHONE}}", f'<a href="tel:{PHONE_TEL}">{PHONE}</a>')
        .replace("{{PHONE_TEXT}}", PHONE)
        .replace("{{PHONE_TEL}}", PHONE_TEL)
    )
    body = fill_icons(body)
    html = head(
        "Small Business Website Design at a Fair Price | Stakich Websites",
        "Affordable, mobile-friendly websites for small businesses, built and cared for by Jeremy Stakich. From $499 + $49/month, no contract. See examples.",
        "/",
        extra=f'<script type="application/ld+json">{json.dumps(HOME_SCHEMA)}</script>',
    )
    html += topbar() + body + footer() + scripts()
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("wrote index.html")


def sitemap():
    today = date.today().isoformat()
    paths = ["/", "/start", "/examples/", "/blog.html", "/support.html", "/get-found-on-google.html", "/get-found-on-bing.html", "/privacy.html", "/terms.html", "/refund-policy.html"]
    paths += build_plan_examples.public_paths()
    paths += [f"/blog/{p['slug']}.html" for p in POSTS]
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )
    print(f"wrote sitemap.xml ({len(paths)} urls)")


if __name__ == "__main__":
    build_pages.build()
    build_found.build()
    build_start.build()
    build_plan_examples.build()
    build_examples.build()
    build_blog.build()
    home()
    sitemap()
