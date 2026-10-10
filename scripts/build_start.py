"""Builds the Start Your Website questionnaire (start.html) and the payment step (pay.html)."""
import json
from pathlib import Path

from common import FORM_TO, PAY_BADGES, PLANS, SITE, contact_options, footer, head, page_hero, scripts, topbar

ROOT = Path(__file__).resolve().parent.parent


def plan_choices():
    out = []
    for key, p in PLANS.items():
        out.append(f"""              <label class="choice-card">
                <input type="radio" name="plan" value="{p['name']}" data-plan-key="{key}" required />
                <span><b>{p['name']}</b> ${p['setup']:,} setup, then ${p['monthly']}/mo</span>
              </label>""")
    return "\n".join(out)


def checks(name, options, required=False):
    req = " data-required-group" if required else ""
    boxes = "\n".join(
        f'                <label class="choice"><input type="checkbox" name="{name}" value="{o}" /> {o}</label>'
        for o in options
    )
    return f'              <div class="choices"{req}>\n{boxes}\n              </div>'


def radios(name, options):
    boxes = "\n".join(
        f'                <label class="choice"><input type="radio" name="{name}" value="{o}" required /> {o}</label>'
        for o in options
    )
    return f'              <div class="choices">\n{boxes}\n              </div>'


STEPS = """          <ol class="start-steps">
            <li><b>1</b><span><strong>Tell me about your business</strong>About 5 minutes. No tech words.</span></li>
            <li><b>2</b><span><strong>Pay securely</strong>Card, Apple Pay, or Google Pay through Stripe.</span></li>
            <li><b>3</b><span><strong>I build it, you approve it</strong>We keep in touch by text, call, or email.</span></li>
          </ol>"""


def start_page():
    body = f"""      <section class="section">
        <div class="container start-wrap">
{STEPS}
          <div class="start-help">
            <p><strong>Questions before you start?</strong> Reach me any way you like. I reply within one business day.</p>
            {contact_options()}
          </div>
          <form class="form start-form" id="start-form" action="https://formsubmit.co/{FORM_TO}" method="POST">
            <input type="hidden" name="_subject" value="New website order — Stakich Websites" />
            <input type="hidden" name="_next" value="{SITE}/pay" />
            <input type="hidden" name="_template" value="table" />
            <input type="hidden" name="_captcha" value="false" />
            <input type="text" name="_honey" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" />

            <fieldset>
              <legend>1. Pick your plan</legend>
{plan_choices()}
              <p class="field-help">Not sure? Pick the closest one. You can change it before you pay.</p>
            </fieldset>

            <fieldset>
              <legend>2. About you</legend>
              <div class="form-row">
                <div class="field">
                  <label for="s-name">Your name</label>
                  <input id="s-name" name="name" type="text" autocomplete="name" required />
                </div>
                <div class="field">
                  <label for="s-business">Business name</label>
                  <input id="s-business" name="business" type="text" autocomplete="organization" required />
                </div>
              </div>
              <div class="form-row">
                <div class="field">
                  <label for="s-email">Email</label>
                  <input id="s-email" name="email" type="email" autocomplete="email" required />
                </div>
                <div class="field">
                  <label for="s-phone">Cell phone</label>
                  <input id="s-phone" name="phone" type="tel" autocomplete="tel" required />
                </div>
              </div>
              <div class="field">
                <span class="label">Best way to reach you (pick any)</span>
{checks("contact_by", ["Text", "Phone call", "Email"], required=True)}
              </div>
              <div class="field">
                <label for="s-times">Best days and times to reach you</label>
                <input id="s-times" name="best_times" type="text" placeholder="Example: weekdays after 5 pm" />
              </div>
            </fieldset>

            <fieldset>
              <legend>3. About your business</legend>
              <div class="form-row">
                <div class="field">
                  <label for="s-type">Type of business</label>
                  <input id="s-type" name="business_type" type="text" placeholder="Lawn care, salon, roofing…" required />
                </div>
                <div class="field">
                  <label for="s-area">Town or area you serve</label>
                  <input id="s-area" name="service_area" type="text" placeholder="Cleveland, TN and nearby" required />
                </div>
              </div>
              <div class="field">
                <label for="s-services">Main services or products you offer</label>
                <textarea id="s-services" name="services" placeholder="Example: mowing, mulch, leaf cleanup, pressure washing" required></textarea>
              </div>
              <div class="field">
                <label for="s-hours">Business hours (if any)</label>
                <input id="s-hours" name="hours" type="text" placeholder="Mon–Fri 8–5, Sat by appointment" />
              </div>
            </fieldset>

            <fieldset>
              <legend>4. Your website</legend>
              <div class="field">
                <span class="label">What should visitors do on your website? (pick any)</span>
{checks("visitor_actions", ["Call me", "Text me", "Request a quote", "Book an appointment", "See my menu or prices", "Visit my location"])}
              </div>
              <div class="form-row">
                <div class="field">
                  <label for="s-current">Current website (if any)</label>
                  <input id="s-current" name="current_website" type="text" placeholder="Leave blank if none" />
                </div>
                <div class="field">
                  <label for="s-domain">Website name you want</label>
                  <input id="s-domain" name="domain_wanted" type="text" placeholder="Example: smithlawncare.com or not sure" />
                </div>
              </div>
              <div class="field">
                <span class="label">Do you have a logo?</span>
{radios("has_logo", ["Yes", "No", "Not sure"])}
              </div>
              <div class="field">
                <span class="label">Do you have photos of your work, team, or place?</span>
{radios("has_photos", ["Yes", "A few", "No"])}
              </div>
              <div class="field">
                <label for="s-style">Colors, style, or websites you like (optional)</label>
                <textarea id="s-style" name="style_notes" placeholder="Example: blue and green, simple and clean. I like the look of…"></textarea>
              </div>
              <div class="field">
                <label for="s-other">Anything else I should know? (optional)</label>
                <textarea id="s-other" name="other_notes"></textarea>
              </div>
              <p class="field-help">You'll send your logo and photos later by text or email. No need to have them ready now.</p>
            </fieldset>

            <label class="choice agree"><input type="checkbox" name="agreed_to_terms" value="Yes" required /> I agree to the <a href="/terms" target="_blank">Terms of Service</a> and <a href="/refund-policy" target="_blank">Refund Policy</a>.</label>
            <button class="btn btn-primary btn-block" type="submit">Save My Answers &amp; Continue to Payment</button>
            <p class="form-fine">Next you'll see your total and pay securely. Your answers are only shared with me. See the <a href="/privacy">privacy policy</a>.</p>
          </form>
        </div>
      </section>
"""
    html = head(
        "Start Your Website | Stakich Websites",
        "Start your small business website: answer a few quick questions about your business, then pay securely. Questions anytime by text, call, or email.",
        "/start",
    )
    html += topbar("pricing")
    html += page_hero("Start Your Website", "Answer a few quick questions about your business, then pay securely. Questions anytime by text, call, or email.", "Get started")
    html += body + footer() + scripts(f'<script src="/start.js?v=1" defer></script>')
    (ROOT / "start.html").write_text(html, encoding="utf-8")
    print("wrote start.html")


def pay_page():
    data = {k: {"name": p["name"], "setup": p["setup"], "monthly": p["monthly"], "link": p["pay_link"]} for k, p in PLANS.items()}
    others = " · ".join(f'<a href="/pay?plan={k}">{p["name"]}</a>' for k, p in PLANS.items())
    body = f"""      <section class="section">
        <div class="container start-wrap">
          <div class="pay-box">
            <p class="eyebrow">Last step</p>
            <h2 id="pay-title">Thanks! I have your answers.</h2>
            <p class="pay-plan" id="pay-plan">Choose your plan below.</p>
            <p class="pay-total" id="pay-total"></p>
            <a class="btn btn-primary btn-block pay-btn" id="pay-btn" href="/#pricing" rel="noopener">Pay Securely</a>
            <p class="form-fine">🔒 Processed by Stripe. Your card details never touch this website.</p>
            {PAY_BADGES}
            <p class="pay-switch">Want a different plan? {others}</p>
          </div>

          <div class="prose">
            <h2>What happens after you pay</h2>
            <ol>
              <li>I contact you within one business day, the way you asked: text, call, or email.</li>
              <li>You send your logo and photos by text or email whenever they're ready.</li>
              <li>I build your website. Most are ready to review in about 7 days.</li>
              <li>You ask for changes until you're happy, then it goes live.</li>
            </ol>
            <p>Change your mind before I start designing? You get a full refund. See the <a href="/refund-policy">refund policy</a>.</p>
            <h2>Want to talk first?</h2>
            <p>That's fine. Your answers are already saved. Reach me any way below, and I'll send your payment link whenever you're ready.</p>
            {contact_options()}
          </div>
        </div>
      </section>
"""
    html = head("Pay for Your Website | Stakich Websites", "Pay securely for your Stakich Websites plan.", "/pay", index=False)
    html += topbar("pricing")
    html += page_hero("Pay for Your Website", "One secure payment and I get to work.", "Step 2 of 2")
    html += body + footer()
    html += scripts(f'<script>window.SW_PLANS = {json.dumps(data)};</script>\n    <script src="/start.js?v=1" defer></script>')
    (ROOT / "pay.html").write_text(html, encoding="utf-8")
    print("wrote pay.html")


def build():
    start_page()
    pay_page()


if __name__ == "__main__":
    build()
