"""Builds policy pages, support, thank-you, and 404 from the shared header/footer."""
from pathlib import Path

from icons import BING_B, GOOGLE_G, icon
from common import EMAIL, FORM_TO, PAY_BADGES, SITE, contact_options, share_mount, footer, head, page_hero, scripts, topbar

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "October 10, 2026"
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'


def page(filename, title, description, intro, body, active="", index=True, eyebrow=""):
    html = head(f"{title} | Stakich Websites", description, "/" + filename, index=index)
    html += topbar(active)
    html += page_hero(title, intro, eyebrow)
    html += f"""      <section class="section">
        <div class="container">
{body}
        </div>
      </section>
"""
    html += footer() + scripts()
    (ROOT / filename).write_text(html, encoding="utf-8")
    print("wrote", filename)


def prose(inner):
    return f'          <div class="prose">\n{inner}\n          </div>'


TERMS = prose(f"""
            <h2>1. Who we are</h2>
            <p>Stakich Websites ("we," "us") is owned and operated by Jeremy Stakich, a sole proprietor based in Charleston, Tennessee, USA. We design, build, host, and maintain websites for small businesses. Contact: {MAIL}.</p>
            <h2>2. Services and plans</h2>
            <p>We offer three plans, each with a one-time setup fee and a monthly care plan:</p>
            <ul>
              <li><strong>Starter:</strong> $499 setup, then $49 per month. Up to 5 pages, hosting, HTTPS, Google search setup, and small monthly updates.</li>
              <li><strong>Growth:</strong> $899 setup, then $79 per month. Everything in Starter, up to 8 pages, one blog post per month, social media captions, and a reviews section.</li>
              <li><strong>Pro:</strong> $1,499 setup, then $129 per month. Everything in Growth, up to 12 pages, booking/menu/quote tools, two blog posts per month, and a monthly website visitor report.</li>
            </ul>
            <p>Work outside your plan (for example, extra pages or custom features) will be quoted in writing before it starts.</p>
            <h2>3. Payment</h2>
            <p>We accept all major credit and debit cards, including Visa, Mastercard, American Express, and Discover, as well as Apple Pay and Google Pay. Payments are processed securely by Stripe; we never see or store your full card number. The setup fee and your first month are paid together before design work begins. After that, the monthly plan is billed automatically every month on the same date to your card on file until canceled. Prices are in US dollars.</p>
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
            <p><em>Last updated: {UPDATED}</em></p>""")

PRIVACY = prose(f"""
            <h2>Information we collect</h2>
            <p>When you fill out our contact form, email us, or become a customer, we collect the information you give us, such as your name, business name, email address, phone number, and details about your business.</p>
            <p>Payments are processed by Stripe. We never see or store your full card number. Stripe's handling of payment data is described in the <a href="https://stripe.com/privacy" target="_blank" rel="noopener">Stripe Privacy Policy</a>.</p>
            <h2>How we use it</h2>
            <ul>
              <li>To reply to your questions and send quotes</li>
              <li>To build, host, and update your website</li>
              <li>To send receipts, billing notices, and service updates</li>
            </ul>
            <h2>What we never do</h2>
            <p>We do not sell, rent, or trade your personal information. We share it only with services needed to run our business (such as Stripe for payments, our form provider, and our hosting provider), or when required by law.</p>
            <h2>Cookies and analytics</h2>
            <p>This website may use basic analytics to understand how many people visit and which pages are useful. This information is not used to identify you personally.</p>
            <h2>Your choices</h2>
            <p>You can ask us to see, correct, or delete the information we have about you at any time by emailing {MAIL}.</p>
            <h2>Contact</h2>
            <p>Stakich Websites · Charleston, Tennessee, USA · {MAIL}</p>
            <p><em>Last updated: {UPDATED}</em></p>""")

REFUND = prose(f"""
            <h2>Setup fee</h2>
            <ul>
              <li><strong>Full refund</strong> of your setup fee and first month if you cancel before design work begins.</li>
              <li><strong>50% refund</strong> if you cancel after work has started but before your website goes live.</li>
              <li><strong>No refund</strong> after your website has gone live, since the work has been completed and delivered.</li>
            </ul>
            <h2>Monthly plan</h2>
            <ul>
              <li>No long-term contract. Cancel anytime by emailing {MAIL}.</li>
              <li>Cancellation takes effect at the end of your current billing month. You will not be charged again after that.</li>
              <li>Monthly payments already made are not refunded for partial months.</li>
            </ul>
            <h2>Our satisfaction promise</h2>
            <p>You review your website before it goes live, and we make changes until you are happy with it. If something isn't right, tell us and we will work to fix it.</p>
            <h2>How refunds are paid</h2>
            <p>Approved refunds are returned to the original card through Stripe, usually within 5–10 business days.</p>
            <h2>Questions</h2>
            <p>Email {MAIL} and we'll reply within one business day.</p>
            <p><em>Last updated: {UPDATED}</em></p>""")

ICON_MAIL = icon("mail")
ICON_EDIT = icon("square-pen")
ICON_CARD = icon("credit-card")

SUPPORT = f"""          <div class="support-reach">
            <h2>Call, text, or email me</h2>
{contact_options()}
          </div>
          <div class="support-grid">
            <article class="card">
              <div class="icon-badge">{ICON_MAIL}</div>
              <h3>Email support</h3>
              <p>Email {MAIL} anytime. I reply within one business day, usually much sooner.</p>
            </article>
            <article class="card">
              <div class="icon-badge">{ICON_EDIT}</div>
              <h3>Request a website change</h3>
              <p>Need new hours, prices, photos, or a new service? Email what you'd like changed (attach photos if you have them). Small updates are included in every plan.</p>
            </article>
            <article class="card">
              <div class="icon-badge">{ICON_CARD}</div>
              <h3>Billing help</h3>
              <p>Update your card, get a receipt, or ask about a charge by emailing {MAIL}. Payments are handled securely by Stripe.</p>
            </article>
          </div>
          <div class="prose">
            <h2>How to request a change</h2>
            <ol>
              <li>Email {MAIL} with the subject "Website change" and your business name.</li>
              <li>Describe what you'd like changed and on which page.</li>
              <li>Attach any new photos, logos, or documents.</li>
            </ol>
            <p>Most small changes are done within 1–2 business days. Pro plan customers get priority same-day updates.</p>
            <h2>Response times</h2>
            <ul>
              <li><strong>Website down or broken:</strong> same day</li>
              <li><strong>Small updates:</strong> 1–2 business days</li>
              <li><strong>Questions and quotes:</strong> within 1 business day</li>
            </ul>
            <h2>Payments we accept</h2>
            <p>We accept all major credit and debit cards, plus Apple Pay and Google Pay. Every payment is processed securely through Stripe, so your card details are never stored on our website.</p>
            {PAY_BADGES}
            <h2>Canceling or pausing</h2>
            <p>There's no long contract. To cancel, email {MAIL}. Your site stays online through the end of your billing month. See the <a href="/refund-policy.html">Refund &amp; Cancellation Policy</a> for details.</p>
            <h2>Policies</h2>
            <ul>
              <li><a href="/privacy.html">Privacy Policy</a></li>
              <li><a href="/terms.html">Terms of Service</a></li>
              <li><a href="/refund-policy.html">Refund &amp; Cancellation Policy</a></li>
            </ul>
            {share_mount("Know a business owner who needs help with their website? Share this")}
            <p><small>Payment logos from the open-source <a href="https://github.com/datatrans/payment-logos" target="_blank" rel="noopener">payment-logos</a> project by Datatrans, licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>.</small></p>
          </div>"""


def steps(items):
    return "<ol class=\"gs-steps\">" + "".join(f"<li>{t}</li>" for t in items) + "</ol>"


STEPS_1 = steps([
    '''Go to <a href="https://www.google.com/business/" target="_blank" rel="noopener">google.com/business</a> and tap <strong>Manage now</strong>.''',
    "Sign in with your Google account (your Gmail). No account? Tap <strong>Create account</strong>. It takes 2 minutes.",
    "Type your business name. If it shows up, pick it. If not, choose <strong>Add your business to Google</strong>.",
    '''Choose the category that fits best, like "Lawn care service" or "Barber shop."''',
    "If customers come to you, add your address. If you go to customers, add the towns you serve instead.",
    "Add your business phone number and your website address. No website yet? Skip it. I'll add it later.",
    "Verify. Google will ask you to confirm by text, phone call, email, or a short video of your business. Follow what it asks. A video can take a few days to be approved.",
    "Skip the rest of the extra questions. I'll fill them in for you.",
])
STEPS_2 = steps([
    "While signed in, search Google for your business name. Your Business Profile appears at the top.",
    "Tap the <strong>three dots</strong> (⋮), then <strong>Business Profile settings</strong>.",
    "Tap <strong>People and access</strong>, then <strong>Add</strong>.",
    f"Enter <strong>{EMAIL}</strong>, choose <strong>Manager</strong>, and tap <strong>Invite</strong>.",
])
STEPS_3 = steps([
    '''Go to <a href="https://www.bingplaces.com/" target="_blank" rel="noopener">bingplaces.com</a> and sign in with the <strong>same Google account</strong> from Step 1.''',
    "Choose <strong>Import from Google Business Profile</strong> and allow access.",
    "Select your business and tap <strong>Import</strong>. That's it. Bing copies everything over, and your listing usually goes live within a few days.",
    f"Optional: open <strong>Manage users</strong>, add <strong>{EMAIL}</strong>, and I can update Bing for you too.",
])

GET_ON_GOOGLE = f"""          <nav class="gs-jump" aria-label="Jump to a step">
            <a href="#google">{GOOGLE_G}<span><b>Step 1</b>Get on Google</span></a>
            <a href="#google-access">{GOOGLE_G}<span><b>Step 2</b>Add me on Google</span></a>
            <a href="#bing">{BING_B}<span><b>Step 3</b>Get on Bing</span></a>
            <a href="#finished">{icon("circle-check")}<span><b>Step 4</b>Tell me you're done</span></a>
          </nav>
          <div id="done" class="gs-done">{icon("circle-check")} Thanks! I got your message and I'll take it from here.</div>
          <div class="prose gs">
            <p class="gs-lead">This takes about <strong>15 minutes</strong>. Google and Bing require the business owner to do these steps, so I can't do them for you. Once they're done, I handle everything else: your hours, photos, services, and website link.</p>

            <h2 id="google">{GOOGLE_G} Step 1: Get your business on Google</h2>
            <p>This puts your business on Google Search and Google Maps.</p>
            {STEPS_1}

            <h2 id="google-access">{GOOGLE_G} Step 2: Add me as a manager on Google</h2>
            <p>This lets me update your listing for you. You stay the owner and can remove me anytime.</p>
            {STEPS_2}

            <h2 id="bing">{BING_B} Step 3: Get your business on Bing</h2>
            <p>Bing powers search on Windows computers, Microsoft Edge, and other search engines. You can copy your Google listing in a few clicks.</p>
            {STEPS_3}

            <h2 id="finished">{icon("circle-check")} Step 4: Tell me you're done</h2>
            <p>Check off what you finished and tap the button. I'll get an email and take it from there.</p>
            <form class="form gs-form" action="https://formsubmit.co/{FORM_TO}" method="POST">
              <input type="hidden" name="_subject" value="Get on Google &amp; Bing: customer finished steps" />
              <input type="hidden" name="_next" value="{SITE}/get-on-google.html#done" />
              <input type="hidden" name="_template" value="table" />
              <input type="hidden" name="_captcha" value="false" />
              <input type="text" name="_honey" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" />
              <div class="form-row">
                <div class="field"><label for="gs-name">Your name</label><input id="gs-name" name="name" type="text" autocomplete="name" required /></div>
                <div class="field"><label for="gs-business">Business name</label><input id="gs-business" name="business" type="text" autocomplete="organization" required /></div>
              </div>
              <fieldset class="gs-checks">
                <legend>What did you finish?</legend>
                <label><input type="checkbox" name="google_listing" value="Yes" /> Step 1: My business is on Google</label>
                <label><input type="checkbox" name="google_verified" value="Yes" /> Google verified it (not still waiting)</label>
                <label><input type="checkbox" name="google_manager" value="Yes" /> Step 2: I added Jeremy as a manager</label>
                <label><input type="checkbox" name="bing_import" value="Yes" /> Step 3: I imported my business to Bing</label>
                <label><input type="checkbox" name="bing_user" value="Yes" /> I added Jeremy on Bing</label>
              </fieldset>
              <div class="field"><label for="gs-notes">Stuck on anything? (optional)</label><textarea id="gs-notes" name="notes" rows="3" placeholder="Tell me which step and what you see."></textarea></div>
              <button class="btn btn-primary btn-block" type="submit">I'm Done, Let Jeremy Know</button>
            </form>
            <p class="gs-help">Stuck? Text a screenshot to me and I'll point you to the next tap.</p>
{contact_options()}
          </div>"""


THANKS = prose(f"""
            <h2>Your message was sent.</h2>
            <p>Thanks for reaching out to Stakich Websites. I'll reply within one business day with a plan and a price for your website. Questions in the meantime? Call, text, or email me.</p>
{contact_options()}
            {share_mount("Know another business owner who needs a website? Share this page")}
            <p><a class="btn btn-primary" href="/">Back to the home page</a></p>""")

NOT_FOUND = prose("""
            <h2>This page doesn't exist.</h2>
            <p>The link may be old or mistyped.</p>
            <p><a class="btn btn-primary" href="/">Go to the home page</a></p>""")


def build():
    page("terms.html", "Terms of Service", "Terms of service for Stakich Websites website design, hosting, and care plans.", "The simple terms for working with Stakich Websites.", TERMS)
    page("privacy.html", "Privacy Policy", "Privacy policy for Stakich Websites: what information we collect, how it's used, how Stripe protects payments, and how to request deletion.", "How your information is collected, used, and protected.", PRIVACY)
    page("refund-policy.html", "Refund & Cancellation Policy", "Refund and cancellation policy for Stakich Websites setup fees and monthly plans.", "Fair, clear rules for refunds and canceling.", REFUND)
    page("support.html", "Customer Support", "Get help with your Stakich Websites website: request changes, billing help, and contact support at Jeremy@StakichWebsites.com.", "Website changes, billing, and questions. Real help from a real person.", SUPPORT, active="support", eyebrow="Support")
    page("get-on-google.html", "Get on Google & Bing", "Simple steps to put your business on Google Maps, Google Search, and Bing, and give Stakich Websites access to manage it.", "Put your business on Google Maps, Google Search, and Bing in about 15 minutes.", GET_ON_GOOGLE, index=False, eyebrow="For customers")
    page("thank-you.html", "Thank You", "Thanks for contacting Stakich Websites.", "Your quote request is on its way.", THANKS, index=False)
    page("404.html", "Page Not Found", "Page not found.", "Sorry, we couldn't find that page.", NOT_FOUND, index=False)


if __name__ == "__main__":
    build()
