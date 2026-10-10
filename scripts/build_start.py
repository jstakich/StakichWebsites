"""Builds the Start Your Website step-by-step form (start.html) and the standalone payment page (pay.html)."""
import json
from pathlib import Path

from common import EMAIL, FORM_TO, PAY_BADGES, PHONE, PHONE_TEL, PLANS, SITE, contact_options, footer, head, page_hero, scripts, topbar

ROOT = Path(__file__).resolve().parent.parent
JS = '<script src="/start.js?v=5" defer></script>'
REQ = '<span class="tag tag-req">Required</span>'
OPT = '<span class="tag tag-opt">Optional</span>'


def plans_json():
    data = {k: {"name": p["name"], "setup": p["setup"], "monthly": p["monthly"], "link": p["pay_link"]} for k, p in PLANS.items()}
    return f"<script>window.SW_PLANS = {json.dumps(data)};</script>"


def field(fid, name, label, kind="text", required=True, placeholder="", attrs=""):
    tag = REQ if required else OPT
    req = " required" if required else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    if kind == "textarea":
        control = f'<textarea id="{fid}" name="{name}"{ph}{req}{attrs}></textarea>'
    else:
        control = f'<input id="{fid}" name="{name}" type="{kind}"{ph}{req}{attrs} />'
    return f"""              <div class="field">
                <label for="{fid}">{label} {tag}</label>
                {control}
                <p class="field-error" aria-live="polite"></p>
              </div>"""


def group(label, name, options, kind="checkbox", required=True):
    tag = REQ if required else OPT
    req_attr = ' required' if kind == "radio" and required else ""
    group_attr = " data-required-group" if kind == "checkbox" and required else ""
    boxes = "\n".join(
        f'                  <label class="choice"><input type="{kind}" name="{name}" value="{o}"{req_attr} /> <span>{o}</span></label>'
        for o in options
    )
    return f"""              <div class="field" role="group" aria-label="{label}">
                <span class="label">{label} {tag}</span>
                <div class="choices"{group_attr}>
{boxes}
                </div>
                <p class="field-error" aria-live="polite"></p>
              </div>"""


def plan_choices():
    out = []
    for key, p in PLANS.items():
        hidden = " hidden" if p.get("hidden") else ""
        price = f"${p['setup']:,} setup, then ${p['monthly']}/month" if p["monthly"] else f"${p['setup']:,} one time (testing only)"
        out.append(f"""                  <label class="choice-card"{hidden}>
                    <input type="radio" name="plan" value="{p['name']}" data-plan-key="{key}" required />
                    <span><b>{p['name']}</b><small>{price}</small></span>
                  </label>""")
    return "\n".join(out)


def nav(step, last=False):
    back = '<button class="btn btn-ghost" type="button" data-back>Back</button>' if step > 1 else "<span></span>"
    nxt = (
        '<button class="btn btn-primary" type="submit">Save &amp; Continue to Payment</button>'
        if last
        else '<button class="btn btn-primary" type="button" data-next>Next</button>'
    )
    return f'              <div class="step-nav">{back}{nxt}</div>'


STUCK = (
    f'              <p class="stuck">Stuck or have a question? <a href="sms:{PHONE_TEL}">💬 Text Jeremy</a> · <a href="tel:{PHONE_TEL}">📞 Call</a> · <a href="mailto:{EMAIL}">✉️ Email</a></p>'
    if PHONE
    else f'              <p class="stuck">Stuck or have a question? <a href="mailto:{EMAIL}">✉️ Email Jeremy</a></p>'
)


def pay_panel(standalone):
    others = " · ".join(f'<a href="/pay?plan={k}">{p["name"]}</a>' for k, p in PLANS.items() if not p.get("hidden"))
    hidden = "" if standalone else " hidden"
    return f"""          <section class="pay-step" id="pay-step"{hidden}>
            <div class="pay-box">
              <p class="eyebrow">Last step</p>
              <h2 id="pay-title" tabindex="-1">Thanks! I have your answers.</h2>
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
                <li>Send your logo and photos by text or email whenever they're ready.</li>
                <li>I build your website. Most are ready for you to review in about 7 days.</li>
                <li>You ask for changes until you're happy, then it goes live.</li>
              </ol>
              <p>Change your mind before I start designing? You get a full refund. See the <a href="/refund-policy">refund policy</a>.</p>
              <h2>Want to talk first?</h2>
              <p>That's fine. Your answers are saved. Reach me any way below, and I'll send your payment link whenever you're ready.</p>
              {contact_options()}
            </div>
          </section>"""


def start_page():
    body = f"""      <section class="section">
        <div class="container start-wrap">
          <div class="start-progress" id="start-progress">
            <p><span id="step-count">4 short steps</span> · <span id="step-name">About 5 minutes</span></p>
            <div class="progress-track"><div class="progress-fill" id="step-bar"></div></div>
          </div>

          <form class="form start-form" id="start-form" action="https://formsubmit.co/{FORM_TO}" method="POST" enctype="multipart/form-data" novalidate>
            <input type="hidden" name="_subject" value="New website order — Stakich Websites" />
            <input type="hidden" name="_next" value="{SITE}/pay" />
            <input type="hidden" name="_template" value="table" />
            <input type="hidden" name="_captcha" value="false" />
            <input type="text" name="_honey" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" />

            <fieldset class="form-step" data-step-name="Your plan" tabindex="-1">
              <legend>Pick your plan</legend>
              <div class="field" role="group" aria-label="Plan">
{plan_choices()}
                <p class="field-error" aria-live="polite"></p>
              </div>
              <p class="field-help">Not sure? Pick the closest one. You can switch before you pay.</p>
{nav(1)}
{STUCK}
            </fieldset>

            <fieldset class="form-step" data-step-name="How to reach you" tabindex="-1">
              <legend>How can I reach you?</legend>
{field("s-name", "name", "Your name", attrs=' autocomplete="name" enterkeyhint="next"')}
{field("s-business", "business", "Business name", required=False, placeholder="Leave blank if you don't have one yet", attrs=' autocomplete="organization" enterkeyhint="next"')}
{field("s-phone", "phone", "Cell phone", kind="tel", placeholder="423-555-0123", attrs=' autocomplete="tel" inputmode="tel" enterkeyhint="next"')}
{field("s-email", "email", "Email", kind="email", placeholder="you@example.com", attrs=' autocomplete="email" inputmode="email" autocapitalize="off" spellcheck="false" enterkeyhint="next"')}
{group("Best way to reach you (pick any)", "contact_by", ["Text", "Phone call", "Email"])}
{nav(2)}
{STUCK}
            </fieldset>

            <fieldset class="form-step" data-step-name="Your business" tabindex="-1">
              <legend>Tell me about your business</legend>
{field("s-type", "business_type", "Type of business", placeholder="Lawn care, salon, roofing…", attrs=' enterkeyhint="next"')}
{field("s-area", "service_area", "Town or area you serve", placeholder="Cleveland, TN and nearby", attrs=' enterkeyhint="next"')}
{field("s-services", "services", "Main services or products", kind="textarea", placeholder="Example: mowing, mulch, leaf cleanup, pressure washing")}
{nav(3)}
{STUCK}
            </fieldset>

            <fieldset class="form-step" data-step-name="Your website" tabindex="-1">
              <legend>What should your website do?</legend>
{group("What should visitors do?", "visitor_actions", ["Call me", "Text me", "Request a quote", "Book an appointment", "See my menu or prices", "Visit my location"], required=False)}
{group("Do you have a logo?", "has_logo", ["Yes", "No", "Not sure"], kind="radio")}
{group("Do you have photos of your work, team, or place?", "has_photos", ["Yes", "A few", "No"], kind="radio")}
              <div class="field">
                <label for="s-files">Upload your logo or a few photos {OPT}</label>
                <input id="s-files" name="attachment" type="file" accept="image/*,.pdf" multiple />
                <p class="field-help">Up to 10 MB total. Bigger files? Text or email them to me later.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
{field("s-current", "current_website", "Current website, if you have one", required=False, placeholder="Leave blank if none", attrs=' inputmode="url" autocapitalize="off" spellcheck="false"')}
{field("s-other", "other_notes", "Anything else?", kind="textarea", required=False, placeholder="Hours, colors you like, websites you like, best times to reach you…")}
              <div class="field">
                <label class="choice agree"><input type="checkbox" name="agreed_to_terms" value="Yes" required /> <span>I agree to the <a href="/terms" target="_blank">Terms</a> and <a href="/refund-policy" target="_blank">Refund Policy</a>. {REQ}</span></label>
                <p class="field-error" aria-live="polite"></p>
              </div>
{nav(4, last=True)}
              <p class="form-fine">Next you'll see your total and pay securely. Your answers are only shared with me. See the <a href="/privacy">privacy policy</a>.</p>
{STUCK}
            </fieldset>
            <p class="save-status" id="save-status" aria-live="polite"></p>
          </form>
{pay_panel(standalone=False)}
        </div>
      </section>
"""
    html = head(
        "Start Your Website | Stakich Websites",
        "Start your small business website: answer 4 short steps about your business, then pay securely. Questions anytime by text, call, or email.",
        "/start",
    )
    html += topbar("pricing")
    html += page_hero("Start Your Website", "4 short steps, about 5 minutes. Then pay securely. Questions anytime by text, call, or email.", "Get started")
    html += body + footer() + scripts(plans_json() + "\n    " + JS, sticky=False)
    (ROOT / "start.html").write_text(html, encoding="utf-8")
    print("wrote start.html")


def pay_page():
    body = f"""      <section class="section">
        <div class="container start-wrap">
{pay_panel(standalone=True)}
        </div>
      </section>
"""
    html = head("Pay for Your Website | Stakich Websites", "Pay securely for your Stakich Websites plan.", "/pay", index=False)
    html += topbar("pricing")
    html += page_hero("Pay for Your Website", "One secure payment and I get to work.", "Last step")
    html += body + footer() + scripts(plans_json() + "\n    " + JS, sticky=False)
    (ROOT / "pay.html").write_text(html, encoding="utf-8")
    print("wrote pay.html")


def build():
    start_page()
    pay_page()


if __name__ == "__main__":
    build()
