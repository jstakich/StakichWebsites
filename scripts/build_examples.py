"""Builds the examples gallery page.

The example websites themselves are built by build_plan_examples.py.
Run from the project root:  python3 scripts/build_examples.py
"""
from pathlib import Path

from build_plan_examples import FULL_SITES, full_gallery_cards, gallery_cards
from common import cta_band, footer, head, page_hero, react_mount, scripts, share_mount, topbar

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "examples"


def gallery_page():
    html = head(
        "Example Websites for Small Businesses | Stakich Websites",
        "Browse full Pro website examples for dentists, chiropractors, and attorneys, plus more small-business websites and plan examples.",
        "/examples/",
    )
    html += topbar("examples")
    html += page_hero(
        "Example websites for small businesses",
        "Explore complete, mobile-friendly examples for a dentist, a chiropractor, and an attorney. Each practice site includes services, appointment requests, helpful information, and more.",
        "Examples",
    )
    html += f"""      <section class="section section-sky">
        <div class="container">
          <div class="section-head">
            <p class="eyebrow" style="color: var(--amber-dark)">Professional practice examples</p>
            <h2>Dentist, chiropractor, and attorney websites</h2>
            <p>Explore the first three Pro examples. Each one has service details, appointment requests, reviews marked for demonstration, blog posts, and clear contact options.</p>
          </div>
          <div class="example-grid">{full_gallery_cards(FULL_SITES[:3])}
          </div>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="section-head">
            <p class="eyebrow" style="color: var(--amber-dark)">Start here</p>
            <h2>One full example for each plan</h2>
            <p>Click around. The forms, booking, and price tools all work, just like they would on your site.</p>
          </div>
          <div class="example-grid plan-example-grid">{gallery_cards()}
          </div>
        </div>
      </section>
      <section class="section section-sky">
        <div class="container">
          <div class="section-head">
            <h2>More examples by type of business</h2>
            <p>Each one is a full website with online booking or quote tools, reviews, a blog, and more.</p>
          </div>
          <div class="example-grid">{full_gallery_cards(FULL_SITES[3:])}
          </div>
          {share_mount("Share these examples")}
          {react_mount("examples", title="Which example is your favorite? Leave a reaction or a comment.")}
        </div>
      </section>
"""
    html += cta_band()
    html += footer()
    html += scripts()
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    (OUT / "index.html").write_text(html, encoding="utf-8")


def build():
    gallery_page()
    print("wrote examples/index.html")


if __name__ == "__main__":
    build()
