"""Builds the Start Your Website step-by-step form (start.html) and the standalone payment page (pay.html)."""
import json
from pathlib import Path

from icons import icon
from common import EMAIL, FORM_TO, PAY_BADGES, PHONE, PHONE_TEL, PLANS, SITE, contact_options, footer, head, page_hero, scripts, topbar

ROOT = Path(__file__).resolve().parent.parent
JS = '<script src="/start.js?v=13" defer></script>'
REQ = '<span class="tag tag-req">Required</span>'
OPT = '<span class="tag tag-opt">Optional</span>'


def plans_json():
    data = {k: {"name": p["name"], "setup": p["setup"], "monthly": p["monthly"], "link": p["pay_link"]} for k, p in PLANS.items()}
    return f"<script>window.SW_PLANS = {json.dumps(data)};</script>"


def field(fid, name, label, kind="text", required=True, placeholder="", attrs="", help=""):
    tag = REQ if required else OPT
    req = " required" if required else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    if help:
        attrs += f' aria-describedby="{fid}-help"'
    if kind == "textarea":
        control = f'<textarea id="{fid}" name="{name}"{ph}{req}{attrs}></textarea>'
    else:
        control = f'<input id="{fid}" name="{name}" type="{kind}"{ph}{req}{attrs} />'
    help_line = f'\n                <p class="field-help" id="{fid}-help">{help}</p>' if help else ""
    return f"""              <div class="field">
                <label for="{fid}">{label} {tag}</label>
                {control}{help_line}
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


LOOKS = "\n".join(
    f'                  <label class="choice"><input type="radio" name="design_look" value="{v}" /> <span>{v}</span></label>'
    for v in [
        "Bold and strong: gray and orange (like the roofing sample)",
        "Fresh and clean: teal and pink (like the house cleaning sample)",
        "Warm and friendly: red and gold (like the restaurant sample)",
        "Classy and trusted: navy and gold (like the law firm sample)",
        "You pick for me",
    ]
)


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
    f'              <p class="stuck">Stuck or have a question? <a href="sms:{PHONE_TEL}">{icon("message-circle")} Text Jeremy</a> · <a href="tel:{PHONE_TEL}">{icon("phone")} Call</a> · <a href="mailto:{EMAIL}">{icon("mail")} Email</a></p>'
    if PHONE
    else f'              <p class="stuck">Stuck or have a question? <a href="mailto:{EMAIL}">{icon("mail")} Email Jeremy</a></p>'
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
                <li>I pull your photos, hours, and reviews from your Facebook and Google pages. Have more? Text or email them anytime.</li>
                <li>I build your website. Most are ready in 1–2 weeks.</li>
                <li>You ask for changes until you're happy, then it goes live.</li>
              </ol>
              <p>On Pro, I manage and update your Google and Bing listings. From the start, add me as Manager. If you don't have a Google or Bing listing yet, you'll need to set that up. I'll send those steps on the thank-you page after you pay.</p>
              <p>Change your mind before I start designing? You get a full refund. See the <a href="/refund-policy" target="_blank">refund policy</a>.</p>
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
            <input type="hidden" name="_subject" value="ORDER FORM filled out (not paid yet, check Stripe) — Stakich Websites" />
            <input type="hidden" name="_next" value="{SITE}/pay" />
            <input type="hidden" name="_template" value="table" />
            <input type="hidden" name="_captcha" value="false" />
            <input type="hidden" name="_autoresponse" value="Thanks, I have your answers! If you haven't paid yet, you can finish here: {SITE}/pay. After you pay, I start building right away, using your answers, photos, and your Facebook and Google pages. I'll send you a link to see your website, usually within 1–2 weeks. Questions? Just reply to this email or text {PHONE}. — Jeremy, Stakich Websites" />
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
              <div class="field">
                <label for="s-address">Business address {REQ}</label>
                <input id="s-address" name="business_address" type="text" placeholder="123 Main St, Cleveland, TN 37311" autocomplete="street-address" enterkeyhint="next" required />
                <p class="field-help">Used to show your business on a map on your website. If you work from home or go to your customers, just put your town and state.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
{field("s-services", "services", "Main services or products", kind="textarea", placeholder="Example: mowing, mulch, leaf cleanup, pressure washing")}
{field("s-hours", "business_hours", "Business hours", required=False, placeholder="Mon–Fri 8–5, Sat 9–1, closed Sunday", attrs=' enterkeyhint="next"')}
              <div class="field">
                <label for="s-facebook">Facebook page name {OPT}</label>
                <input id="s-facebook" name="facebook_page" type="text" placeholder="The name of your business page on Facebook" autocapitalize="words" enterkeyhint="next" />
                <p class="field-help">No need to look it up. I'll find it and grab your photos and info, so you don't have to send them.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="s-google">Your business name on Google {OPT}</label>
                <input id="s-google" name="google_profile" type="text" placeholder="The name people search to find you" autocapitalize="words" enterkeyhint="next" />
                <p class="field-help">No need to look it up. I'll find your Google listing and use your reviews, hours, and photos from it.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
{nav(3)}
{STUCK}
            </fieldset>

            <fieldset class="form-step" data-step-name="Your website" tabindex="-1">
              <legend>What should your website do?</legend>
{group("Did I send you a free preview website?", "use_preview", ["Yes, use my preview as the starting point", "Yes, but I'd like something different", "No"], kind="radio", required=False)}
              <div class="field">
                <label for="s-preview">Preview link {OPT}</label>
                <input id="s-preview" name="preview_link" type="text" placeholder="stakichwebsites.com/preview/your-business" inputmode="url" autocapitalize="off" spellcheck="false" enterkeyhint="next" />
                <p class="field-help">Please note: some features in your preview may only come with certain plans. A Google reviews section and monthly blog posts come with Growth and Pro. Online booking, menus, and quote tools come with Pro. I'll build your website to match the plan you pick. Want a feature from a bigger plan? Go back to step 1 and switch plans, or just ask me.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
{group("What should visitors do?", "visitor_actions", ["Call me", "Text me", "Request a quote", "Book an appointment", "See my menu or prices", "Visit my location"], required=False)}
{group("Do you have a logo?", "has_logo", ["Yes", "No", "Not sure"], kind="radio")}
              <div data-logo-upload hidden>
              <div class="field">
                <label for="s-logo">Upload your logo {OPT}</label>
                <input id="s-logo" name="logo" type="file" accept="image/*,.svg,.pdf" disabled />
                <p class="field-help">One file. This is the picture next to your business name. Don't have it on this phone? Skip and text it later.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
              </div>
{group("Do you have photos of your work, team, or place?", "has_photos", ["Yes", "A few", "No"], kind="radio")}
              <div data-photo-upload hidden>
              <div class="field">
                <label for="s-photos">Upload a few photos {OPT}</label>
                <input id="s-photos" name="photos" type="file" accept="image/*" multiple disabled />
                <p class="field-help">Work, team, or your place. Up to 10 MB total with your logo. Bigger files? Text or email them later.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
              </div>
              <div class="field">
                <label for="s-prices">Upload your price list {OPT}</label>
                <input id="s-prices" name="price_list" type="file" accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.csv,.txt" multiple />
                <p class="field-help">A photo, PDF, or spreadsheet of your services and prices. This is how I set up your price list, menu, or the Pro plan's instant quote tool. Don't have one written down? Skip it and text me later.</p>
                <p class="field-error" aria-live="polite"></p>
              </div>
              <div class="field" role="group" aria-label="Which sample website look do you like best?">
                <span class="label">Which sample website look do you like best? {OPT}</span>
                <div class="choices">
{LOOKS}
                </div>
                <p class="field-error" aria-live="polite"></p>
              </div>
{field("s-colors", "favorite_colors", "Colors you like", required=False, placeholder="Example: navy and gold, or match my logo", attrs=' enterkeyhint="next"')}
{group("Do you have a web address (like yourbusiness.com)?", "domain", ["Yes, I have one", "No, help me pick one"], kind="radio")}
{field("s-domain", "domain_wanted", "Your web address, or one you'd like", placeholder="yourbusiness.com", attrs=' inputmode="url" autocapitalize="off" spellcheck="false"', help="This is what people type to find your website, like google.com or walmart.com.")}
              <p class="domain-check" id="domain-check" aria-live="polite"></p>
              <div class="domain-ideas" id="domain-ideas" aria-live="polite" hidden><p></p><div class="domain-idea-list"></div></div>
              <div class="domain-extra" data-domain-extra hidden>
{group("Where did you buy it? No need to look it up.", "domain_company", ["GoDaddy", "Squarespace", "Wix", "Other", "Not sure"], kind="radio", required=False)}
{group("Do you get email at this address (like you@yourbusiness.com)?", "domain_email", ["Yes", "No", "Not sure"], kind="radio", required=False)}
              </div>
{field("s-current", "current_website", "Current website, if you have one", required=False, placeholder="Leave blank if none", attrs=' inputmode="url" autocapitalize="off" spellcheck="false"')}
{field("s-other", "other_notes", "Anything else?", kind="textarea", required=False, placeholder="Websites you like, things you want to say, best times to reach you…")}
              <div class="plan-extra" data-plans="growth pro" hidden>
{field("s-faqs", "customer_questions", "Questions customers ask you a lot (Growth and Pro)", kind="textarea", required=False, placeholder="Example: How much does a new roof cost? Do you work with insurance? How long does it take?")}
                <p class="field-help">I turn these into your monthly blog posts.</p>
              </div>
              <div class="plan-extra" data-plans="pro" hidden>
{field("s-book-svc", "booking_services", "Which services can people book online? (Pro)", kind="textarea", required=False, placeholder="Example: free estimate, roof repair, gutter cleaning")}
{field("s-book-times", "booking_times", "Days and times you take appointments (Pro)", required=False, placeholder="Example: Mon–Fri 8–4, Sat mornings")}
{group("Where should booking requests go? (Pro)", "booking_to", ["Text me", "Email me", "Both"], kind="radio", required=False)}
{field("s-est", "estimate_prices", "Starting prices for your instant price estimate (Pro)", kind="textarea", required=False, placeholder="Example: roof repair $300–$750, new gutters $1,200–$2,200. Or upload your price list above.")}
                <p class="field-help">Ballpark ranges are fine. You can change them anytime. On Pro, I manage and update your Google and Bing listings. From the start, add me as Manager. If you don't have a Google or Bing listing yet, you'll need to set that up. Those steps come after you pay, on the thank-you page.</p>
              </div>
              <div class="field">
                <label class="choice agree"><input type="checkbox" name="agreed_to_terms" value="Yes" required /> <span>I agree to the <a href="/terms" target="_blank">Terms</a> and <a href="/refund-policy" target="_blank">Refund Policy</a>. {REQ}</span></label>
                <p class="field-error" aria-live="polite"></p>
              </div>
{nav(4, last=True)}
              <p class="form-fine">Next you'll see your total and pay securely. Your answers are only shared with me. See the <a href="/privacy" target="_blank">privacy policy</a>.</p>
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
