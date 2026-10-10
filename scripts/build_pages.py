"""Builds the simple content pages (policies, thank-you, 404) from the shared header/footer.

Run from the project root:  python3 scripts/build_pages.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "October 9, 2026"
EMAIL = "jeremystakich2@gmail.com"

HEAD = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} | Stakich Websites</title>
    <meta name="description" content="{description}" />
    {canonical}
    <meta name="theme-color" content="#0c1c36" />
    {robots}
    <link rel="icon" href="/assets/icon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css?v=1" />
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="topbar">
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
          <a href="/#services">Services</a>
          <a href="/#industries">Who I Help</a>
          <a href="/#pricing">Pricing</a>
          <a href="/#about">About</a>
          <a href="/#faq">FAQ</a>
          <a class="btn btn-primary" href="/#contact">Get a Free Quote</a>
        </nav>
      </div>
    </header>
    <main id="main">
"""

FOOT = """    </main>
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div>
            <a class="brand" href="/">
              <img src="/assets/icon.svg" alt="" width="40" height="40" />
              <span class="brand-name">Stakich Websites<small>Trusted · Fair price</small></span>
            </a>
            <p style="margin-top: 16px">Trusted websites for small businesses at a fair price. Owned and operated by Jeremy Stakich in Charleston, Tennessee.</p>
          </div>
          <div>
            <h4>Website</h4>
            <ul>
              <li><a href="/#services">Services</a></li>
              <li><a href="/#pricing">Pricing</a></li>
              <li><a href="/#about">About</a></li>
              <li><a href="/#contact">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4>Policies</h4>
            <ul>
              <li><a href="/terms.html">Terms of Service</a></li>
              <li><a href="/privacy.html">Privacy Policy</a></li>
              <li><a href="/refund-policy.html">Refund &amp; Cancellation</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <span>© <span data-year>2026</span> Stakich Websites. All rights reserved.</span>
          <a href="mailto:{email}">{email}</a>
        </div>
      </div>
    </footer>
    <script src="/site.js?v=1" defer></script>
  </body>
</html>
""".replace("{email}", EMAIL)


def page(filename, title, description, intro, body, index=True):
    canonical = f'<link rel="canonical" href="https://stakichwebsites.com/{filename}" />' if index else ""
    robots = "" if index else '<meta name="robots" content="noindex" />'
    html = HEAD.format(title=title, description=description, canonical=canonical, robots=robots)
    html += f"""      <section class="page-hero">
        <div class="container">
          <h1>{title}</h1>
          <p>{intro}</p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="prose">
{body}
          </div>
        </div>
      </section>
"""
    html += FOOT
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


TERMS = f"""
            <h2>1. Who we are</h2>
            <p>Stakich Websites ("we," "us") is owned and operated by Jeremy Stakich, a sole proprietor based in Charleston, Tennessee, USA. We design, build, host, and maintain websites for small businesses. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

            <h2>2. Services and plans</h2>
            <p>We offer three plans, each with a one-time setup fee and a monthly care plan:</p>
            <ul>
              <li><strong>Starter:</strong> $499 setup, then $49 per month. Up to 5 pages, hosting, HTTPS, Google search setup, and small monthly updates.</li>
              <li><strong>Growth:</strong> $899 setup, then $79 per month. Everything in Starter, up to 8 pages, one blog post per month, social media captions, and a reviews section.</li>
              <li><strong>Pro:</strong> $1,499 setup, then $129 per month. Everything in Growth, up to 12 pages, booking/menu/quote tools, two blog posts per month, and Google Business Profile posts.</li>
            </ul>
            <p>Work outside your plan (for example, extra pages or custom features) will be quoted in writing before it starts.</p>

            <h2>3. Payment</h2>
            <p>Payments are processed securely by Stripe. The setup fee is due before design work begins. The monthly plan begins when your website goes live and is billed automatically every month to the card on file until canceled. Prices are in US dollars.</p>

            <h2>4. Your responsibilities</h2>
            <p>You agree to provide accurate business information, and you confirm that you have the right to use any logos, photos, and text you send us. You are responsible for the claims your business makes on its website.</p>

            <h2>5. Ownership</h2>
            <p>Your domain name is registered in your name and belongs to you. Your logos, photos, and written content belong to you. Once all setup fees are paid, you own the design of your website. If you cancel, we will provide a copy of your website files on request.</p>

            <h2>6. Cancellation</h2>
            <p>There is no long-term contract. You may cancel your monthly plan at any time by email. Cancellation takes effect at the end of your current billing month, and your website stays online until then. Refunds are covered by our <a href="/refund-policy.html">Refund &amp; Cancellation Policy</a>.</p>

            <h2>7. Website availability</h2>
            <p>We work to keep your website online and secure, but we cannot guarantee uninterrupted service, since hosting depends on third-party providers. We do not guarantee specific Google rankings, traffic, or sales, because search engines control their own results.</p>

            <h2>8. Limitation of liability</h2>
            <p>To the extent allowed by law, our total liability for any claim related to our services is limited to the amount you paid us in the three months before the claim.</p>

            <h2>9. Changes to these terms</h2>
            <p>We may update these terms from time to time. Changes will be posted on this page with a new date. Price changes for existing customers will be announced by email at least 30 days in advance.</p>

            <h2>10. Governing law</h2>
            <p>These terms are governed by the laws of the State of Tennessee, USA.</p>

            <p><em>Last updated: {UPDATED}</em></p>
"""

PRIVACY = f"""
            <h2>Information we collect</h2>
            <p>When you fill out our contact form or become a customer, we collect the information you give us, such as your name, business name, email address, phone number, and details about your business.</p>
            <p>Payments are processed by Stripe. We never see or store your full card number. Stripe's handling of payment data is described in the <a href="https://stripe.com/privacy" target="_blank" rel="noopener">Stripe Privacy Policy</a>.</p>

            <h2>How we use it</h2>
            <ul>
              <li>To reply to your questions and send quotes</li>
              <li>To build, host, and update your website</li>
              <li>To send receipts, billing notices, and service updates</li>
            </ul>

            <h2>What we never do</h2>
            <p>We do not sell, rent, or trade your personal information. We share it only with services needed to run our business (such as Stripe for payments and our form and hosting providers), or when required by law.</p>

            <h2>Cookies and analytics</h2>
            <p>This website may use basic analytics to understand how many people visit and which pages are useful. This information is not used to identify you personally.</p>

            <h2>Your choices</h2>
            <p>You can ask us to see, correct, or delete the information we have about you at any time by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

            <h2>Contact</h2>
            <p>Stakich Websites, Charleston, Tennessee, USA · <a href="mailto:{EMAIL}">{EMAIL}</a></p>

            <p><em>Last updated: {UPDATED}</em></p>
"""

REFUND = f"""
            <h2>Setup fee</h2>
            <ul>
              <li><strong>Full refund</strong> if you cancel before design work begins.</li>
              <li><strong>50% refund</strong> if you cancel after work has started but before your website goes live.</li>
              <li><strong>No refund</strong> after your website has gone live, since the work has been completed and delivered.</li>
            </ul>

            <h2>Monthly plan</h2>
            <ul>
              <li>No long-term contract. Cancel anytime by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</li>
              <li>Cancellation takes effect at the end of your current billing month. You will not be charged again after that.</li>
              <li>Monthly payments already made are not refunded for partial months.</li>
            </ul>

            <h2>Our satisfaction promise</h2>
            <p>You review your website before it goes live, and we make changes until you are happy with it. If something isn't right, tell us and we will work to fix it.</p>

            <h2>How refunds are paid</h2>
            <p>Approved refunds are returned to the original card through Stripe, usually within 5–10 business days.</p>

            <h2>Questions</h2>
            <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll reply within one business day.</p>

            <p><em>Last updated: {UPDATED}</em></p>
"""

THANKS = """
            <h2>Your message was sent.</h2>
            <p>Thanks for reaching out to Stakich Websites. I'll reply within one business day with a plan and a price for your website.</p>
            <p><a class="btn btn-primary" href="/">Back to the home page</a></p>
"""

NOT_FOUND = """
            <h2>This page doesn't exist.</h2>
            <p>The link may be old or mistyped.</p>
            <p><a class="btn btn-primary" href="/">Go to the home page</a></p>
"""

if __name__ == "__main__":
    page("terms.html", "Terms of Service", "Terms of service for Stakich Websites website design, hosting, and care plans.", "The simple terms for working with Stakich Websites.", TERMS)
    page("privacy.html", "Privacy Policy", "How Stakich Websites collects, uses, and protects your information.", "How your information is collected, used, and protected.", PRIVACY)
    page("refund-policy.html", "Refund & Cancellation Policy", "Refund and cancellation policy for Stakich Websites setup fees and monthly plans.", "Fair, clear rules for refunds and canceling.", REFUND)
    page("thank-you.html", "Thank You", "Thanks for contacting Stakich Websites.", "Your quote request is on its way.", THANKS, index=False)
    page("404.html", "Page Not Found", "Page not found.", "Sorry, we couldn't find that page.", NOT_FOUND, index=False)
