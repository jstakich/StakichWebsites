"""Builds blog posts, blog.html, blogs.json, and ready-to-paste social captions."""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

from common import SITE, cta_band, footer, head, page_hero, react_mount, scripts, share_mount, topbar
from posts import POSTS

ROOT = Path(__file__).resolve().parent.parent


def nice_date(iso):
    return date.fromisoformat(iso).strftime("%B %-d, %Y")


def plain(html):
    return re.sub(r"<[^>]+>", "", html).replace("&amp;", "&")


def article_html(post):
    url = f"{SITE}/blog/{post['slug']}.html"
    faq_html = "\n".join(
        f"              <details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in post["faq"]
    )
    related = [p for p in POSTS if p["slug"] != post["slug"]][:3]
    related_html = "\n".join(
        f'                <li><a href="/blog/{p["slug"]}.html">{escape(p["title"])}</a></li>' for p in related
    )
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post["title"],
            "description": post["description"],
            "datePublished": post["date"],
            "dateModified": post["date"],
            "author": {"@type": "Person", "name": "Jeremy Stakich"},
            "publisher": {"@type": "Organization", "name": "Stakich Websites", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon-512.png"}},
            "image": f"{SITE}/assets/og-image.png",
            "mainEntityOfPage": url,
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in post["faq"]
            ],
        },
    ]
    extra = f'<script type="application/ld+json">{json.dumps(schema)}</script>'
    tags = "".join(f'<span class="blog-tag">{escape(t)}</span>' for t in post["tags"])

    html = head(escape(post["seo_title"]), escape(post["description"]), f"/blog/{post['slug']}.html", extra=extra, og_type="article")
    html += topbar("blog")
    html += f"""      <section class="page-hero">
        <div class="container">
          <p class="eyebrow"><a href="/blog.html">Blog</a></p>
          <h1>{escape(post['title'])}</h1>
          <p class="byline">By Jeremy Stakich · {nice_date(post['date'])} · {tags}</p>
        </div>
      </section>
      <section class="section">
        <div class="container article">
          <div class="article-body">
            <p class="quick-answer"><strong>Quick answer:</strong> {post['quick']}</p>
            {share_mount("Share this article")}
{post['body']}
            <h2>Frequently asked questions</h2>
            <div class="faq">
{faq_html}
            </div>
            <div class="article-cta">
              <h3>Want a website that brings in customers?</h3>
              <p>Plans start at $199 to build and $49 per month. No contract, and you always own your domain.</p>
              <a class="btn btn-primary" href="/#contact">Free Quote</a>
              <a class="btn btn-green" href="/#pricing">Get Started</a>
              <a class="btn btn-outline" href="/examples/">See Example Websites</a>
            </div>
            {share_mount("Found this helpful? Share it")}
            {react_mount("blog:" + post["slug"], title="Was this helpful? Leave a reaction or a comment.")}
            <div class="related">
              <h3>Keep reading</h3>
              <ul>
{related_html}
              </ul>
            </div>
          </div>
        </div>
      </section>
"""
    html += footer() + scripts()
    return html


def social_captions(post):
    url = f"{SITE}/blog/{post['slug']}.html"
    quick = plain(post["quick"])
    tags = " ".join("#" + re.sub(r"[^A-Za-z]", "", t) for t in post["tags"]) + " #SmallBusiness #WebDesign"
    return f"""SOCIAL POSTS FOR: {post['title']}
Link: {url}

=== FACEBOOK ===
{post['title']}

{quick}

Read the full guide: {url}

=== INSTAGRAM (put the link in your bio) ===
{post['title']} 👇

{quick}

Full guide at stakichwebsites.com (link in bio).
{tags}

=== X / TWITTER ===
{post['title']}
{url}
{tags}

=== LINKEDIN ===
Small business owners ask me this all the time: {post['title'].split(':')[0].split('(')[0].strip()}?

{quick}

I wrote a plain-English guide here: {url}

=== GOOGLE BUSINESS PROFILE (choose "Learn more" button, paste link) ===
{quick}
Read more: {url}
"""


def blog_index():
    items = "\n".join(
        f"""            <article class="blog-item" data-search="{escape((p['title'] + ' ' + p['excerpt'] + ' ' + ' '.join(p['tags'])).lower())}">
              <p class="blog-meta">{nice_date(p['date'])} · {''.join(f'<span class="blog-tag">{escape(t)}</span>' for t in p['tags'])}</p>
              <h3><a href="/blog/{p['slug']}.html">{escape(p['title'])}</a></h3>
              <p>{escape(p['excerpt'])}</p>
              {react_mount("blog:" + p["slug"], full=False)}
            </article>"""
        for p in POSTS
    )
    html = head("Small Business Website Blog: Costs, Google & Tips | Stakich Websites", "Plain-English guides for small business owners: website costs, getting on Google Maps, and what makes a website bring in customers.", "/blog.html")
    html += topbar("blog")
    html += page_hero("Small Business Website Blog", "Plain-English guides on website costs, Google, and getting more customers online.", "Blog")
    html += f"""      <section class="section">
        <div class="container">
          <div class="blog-search">
            <label class="sr-only" for="blog-q">Search articles</label>
            <input id="blog-q" type="search" placeholder="Search articles…" autocomplete="off" />
          </div>
          <div class="blog-list" id="blog-list">
{items}
          </div>
          <p id="blog-empty" hidden>No articles match that search.</p>
          {share_mount("Share the blog")}
        </div>
      </section>
"""
    html += cta_band() + footer()
    html += scripts("""<script>
      (function () {
        var q = document.getElementById("blog-q");
        var items = document.querySelectorAll("#blog-list .blog-item");
        var empty = document.getElementById("blog-empty");
        q.addEventListener("input", function () {
          var v = q.value.trim().toLowerCase(), shown = 0;
          items.forEach(function (el) {
            var hit = !v || el.getAttribute("data-search").indexOf(v) !== -1;
            el.hidden = !hit;
            if (hit) shown++;
          });
          empty.hidden = shown !== 0;
        });
      })();
    </script>""")
    return html


def build():
    (ROOT / "blog").mkdir(exist_ok=True)
    (ROOT / "social").mkdir(exist_ok=True)
    for post in POSTS:
        (ROOT / "blog" / f"{post['slug']}.html").write_text(article_html(post), encoding="utf-8")
        (ROOT / "social" / f"{post['slug']}.txt").write_text(social_captions(post), encoding="utf-8")
        print("wrote blog/" + post["slug"] + ".html")
    (ROOT / "blog.html").write_text(blog_index(), encoding="utf-8")
    data = [
        {k: p[k] for k in ("slug", "title", "description", "date", "tags", "excerpt")} | {"url": f"/blog/{p['slug']}.html"}
        for p in POSTS
    ]
    (ROOT / "blogs.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("wrote blog.html, blogs.json, social/*.txt")


if __name__ == "__main__":
    build()
