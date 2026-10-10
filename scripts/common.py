"""Shared header, footer, and snippets for every generated page."""

SITE = "https://stakichwebsites.com"
EMAIL = "Jeremy@StakichWebsites.com"
FORM_TO = "jeremy@stakichwebsites.com"
PHONE = "(423) 227-7681"
PHONE_TEL = "+14232277681"
CSS_V = "11"
JS_V = "8"

PLANS = {
    "starter": {
        "name": "Starter",
        "setup": 499,
        "monthly": 49,
        "pay_link": "https://buy.stripe.com/aFacN66uR3FOgAf9UefEk00",
    },
    "growth": {
        "name": "Growth",
        "setup": 899,
        "monthly": 79,
        "pay_link": "https://buy.stripe.com/eVq7sMf1n4JSfwbc2mfEk01",
    },
    "pro": {
        "name": "Pro",
        "setup": 1499,
        "monthly": 129,
        "pay_link": "https://buy.stripe.com/eVqcN6dXjgsA1Fl0jEfEk02",
    },
    "test": {
        "name": "Test",
        "setup": 1,
        "monthly": 0,
        "pay_link": "",
        "hidden": True,
    },
}

NAV = [
    ("services", "/#services", "Services"),
    ("examples", "/examples/", "Examples"),
    ("pricing", "/#pricing", "Pricing"),
    ("blog", "/blog.html", "Blog"),
    ("about", "/#about", "About"),
    ("support", "/support.html", "Support"),
]

NAV_ICONS = {
    "services": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5z"/>',
    "examples": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    "pricing": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "blog": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
    "about": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "support": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2.5" y="14" width="4" height="6" rx="1.5"/><rect x="17.5" y="14" width="4" height="6" rx="1.5"/>',
}


def nav_icon(key):
    return f'<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{NAV_ICONS[key]}</svg>'

HTTPS_REDIRECT = '<script>if (location.protocol === "http:" && location.hostname.endsWith("stakichwebsites.com")) location.replace("https:" + location.href.slice(5));</script>'

PAY_BADGES = """<ul class="pay-badges" aria-label="Accepted payment methods">
              <li>Visa</li>
              <li>Mastercard</li>
              <li>American Express</li>
              <li>Discover</li>
              <li>Apple Pay</li>
              <li>Google Pay</li>
            </ul>"""


def head(title, description, path, image="/assets/og-image.png", index=True, extra="", og_type="website"):
    canonical = f'<link rel="canonical" href="{SITE}{path}" />' if index else '<meta name="robots" content="noindex" />'
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    {HTTPS_REDIRECT}
    <title>{title}</title>
    <meta name="description" content="{description}" />
    {canonical}
    <meta name="theme-color" content="#0c1c36" />
    <link rel="icon" href="/assets/icon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:site_name" content="Stakich Websites" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{SITE}{path}" />
    <meta property="og:image" content="{SITE}{image}" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css?v={CSS_V}" />
    {extra}
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
"""


def topbar(active=""):
    links = "\n".join(
        '          <a href="%s"%s>%s<span>%s</span></a>' % (href, ' aria-current="page"' if key == active else "", nav_icon(key), label)
        for key, href, label in NAV
    )
    return f"""    <header class="topbar">
      <div class="container topbar-inner">
        <a class="brand" href="/" aria-label="Stakich Websites home">
          <img src="/assets/icon.svg" alt="" width="40" height="40" />
          <span class="brand-name">Stakich Websites<small>Trusted · Fair price</small></span>
        </a>
        <button class="nav-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" aria-label="Open menu">
          <span class="nav-toggle-bar"></span>
          <span class="nav-toggle-bar"></span>
          <span class="nav-toggle-bar"></span>
        </button>
        <nav id="primary-nav" class="topbar-links" aria-label="Primary">
{links}
          <a class="btn btn-primary" href="/#contact">Get a Free Quote</a>
        </nav>
      </div>
    </header>
    <main id="main">
"""


def footer():
    return f"""    </main>
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div>
            <a class="brand" href="/">
              <img src="/assets/icon.svg" alt="" width="40" height="40" />
              <span class="brand-name">Stakich Websites<small>Trusted · Fair price</small></span>
            </a>
            <p style="margin-top: 16px">Trusted websites for small businesses at a fair price. Owned and operated by Jeremy Stakich in Charleston, Tennessee, serving businesses across the United States.</p>
            <p class="footer-pay-label">We accept all major credit and debit cards. Payments are processed securely by Stripe.</p>
            {PAY_BADGES}
          </div>
          <div>
            <h4>Website</h4>
            <ul>
              <li><a href="/#services">Services</a></li>
              <li><a href="/examples/">Example Websites</a></li>
              <li><a href="/#pricing">Pricing</a></li>
              <li><a href="/blog.html">Blog</a></li>
              <li><a href="/#about">About Jeremy</a></li>
              <li><a href="/#contact">Free Quote</a></li>
            </ul>
          </div>
          <div>
            <h4>Support &amp; Policies</h4>
            <ul>
              <li><a href="/support.html">Customer Support</a></li>
              <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
              <li><a href="/privacy.html">Privacy Policy</a></li>
              <li><a href="/terms.html">Terms of Service</a></li>
              <li><a href="/refund-policy.html">Refund &amp; Cancellation</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <span>© <span data-year>2026</span> Stakich Websites. All rights reserved.</span>
          <span><a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a> · <a href="/refund-policy.html">Refunds</a> · <a href="/support.html">Support</a></span>
        </div>
      </div>
    </footer>
"""


def scripts(extra="", sticky=True):
    cta = '    <a class="btn btn-primary sticky-cta" href="/#contact">Get a Free Quote</a>\n' if sticky else ""
    return f"""{cta}    <script src="/site.js?v={JS_V}" defer></script>
    <script src="/share.js?v={JS_V}" defer></script>
    {extra}
  </body>
</html>
"""


def page_hero(title, intro, eyebrow=""):
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f"""      <section class="page-hero">
        <div class="container">
          {eb}
          <h1>{title}</h1>
          <p>{intro}</p>
        </div>
      </section>
"""


def contact_options():
    items = []
    line = f"Jeremy · {PHONE} · {EMAIL}" if PHONE else f"Jeremy · {EMAIL}"
    if PHONE:
        items.append(f'<a class="reach-btn" href="sms:{PHONE_TEL}">💬 Text me</a>')
        items.append(f'<a class="reach-btn" href="tel:{PHONE_TEL}">📞 Call me</a>')
    items.append(f'<a class="reach-btn" href="mailto:{EMAIL}">✉️ Email me</a>')
    return f'<p class="reach-line">{line}</p><div class="reach">' + "".join(items) + "</div>"


def share_mount(label="Share this page"):
    return f'<div class="share-mount" data-share data-share-label="{label}"></div>'


def cta_band():
    return """      <section class="section">
        <div class="container">
          <div class="cta-band">
            <div>
              <h2>Ready for a website that brings in customers?</h2>
              <p>Get a free quote in one business day. No pressure, no long contract.</p>
            </div>
            <a class="btn btn-navy" href="/#contact">Get My Free Quote</a>
          </div>
        </div>
      </section>
"""
