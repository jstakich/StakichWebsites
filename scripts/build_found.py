"""Builds the Pro-plan "Get Found on Google" and "Get Found on Bing" pages."""
from build_pages import page
from common import EMAIL, FORM_TO, PLANS, SITE, contact_options
from icons import BING_B, GOOGLE_G, icon

PRO = PLANS["pro"]
PRO_PRICE = f"${PRO['setup']:,} setup, then ${PRO['monthly']}/month"


def steps(items):
    return '<ol class="gs-steps">' + "".join(f"<li>{t}</li>" for t in items) + "</ol>"


def checklist(items):
    return '<ul class="gs-included">' + "".join(f"<li>{icon('circle-check')}<span>{t}</span></li>" for t in items) + "</ul>"


def pro_notice(service):
    return f"""          <div class="pro-only">
            <span class="pro-only-tag">{icon("sparkles")} Pro plan only</span>
            <h2>{service} is included in the Pro plan</h2>
            <p>The Pro plan is {PRO_PRICE}. I manage and update your Google and Bing listings. From the start, add me as Manager. If you don't have a Google or Bing listing yet, that part is yours.</p>
            <p class="pro-only-note">On Starter or Growth? Your website is still built to be found in search, with page titles, a sitemap, and fast loading. Listing management and upkeep is only in Pro. You can upgrade anytime.</p>
            <div class="pro-only-actions">
              <a class="btn btn-primary" href="/start?plan=pro">Get the Pro Plan</a>
              <a class="btn btn-ghost" href="/#pricing">Compare Plans</a>
            </div>
          </div>"""


def jump(logo):
    return f"""          <nav class="gs-jump" aria-label="Jump to a section">
            <a href="#why">{logo}<span><b>Why</b>It brings calls</span></a>
            <a href="#included">{icon("sparkles")}<span><b>Pro plan</b>What I do</span></a>
            <a href="#your-steps">{icon("square-pen")}<span><b>Your part</b>About 10 minutes</span></a>
            <a href="#finished">{icon("circle-check")}<span><b>Last step</b>Tell me you're done</span></a>
          </nav>"""


def done_form(slug, subject, checks):
    boxes = "".join(f'<label><input type="checkbox" name="{n}" value="Yes" /> {t}</label>' for n, t in checks)
    return f"""            <form class="form gs-form" action="https://formsubmit.co/{FORM_TO}" method="POST">
              <input type="hidden" name="_subject" value="{subject}" />
              <input type="hidden" name="_next" value="{SITE}/{slug}.html#done" />
              <input type="hidden" name="_template" value="table" />
              <input type="hidden" name="_captcha" value="false" />
              <input type="text" name="_honey" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" />
              <div class="form-row">
                <div class="field"><label for="gs-name">Your name</label><input id="gs-name" name="name" type="text" autocomplete="name" required /></div>
                <div class="field"><label for="gs-business">Business name</label><input id="gs-business" name="business" type="text" autocomplete="organization" required /></div>
              </div>
              <fieldset class="gs-checks">
                <legend>What did you finish?</legend>
                {boxes}
              </fieldset>
              <div class="field"><label for="gs-notes">Stuck on anything? (optional)</label><textarea id="gs-notes" name="notes" rows="3" placeholder="Tell me which step and what you see."></textarea></div>
              <button class="btn btn-primary btn-block" type="submit">I'm Done, Let Jeremy Know</button>
            </form>
            <p class="gs-help">Stuck? Text me a screenshot and I'll point you to the next tap.</p>
{contact_options()}"""


GOOGLE_STEPS = steps([
    'Go to <a href="https://www.google.com/business/" target="_blank" rel="noopener">google.com/business</a> and tap <strong>Manage now</strong>.',
    "Sign in with your Google account (your Gmail). No account? Tap <strong>Create account</strong>. It takes 2 minutes.",
    "Type your business name. If it shows up, pick it. If not, choose <strong>Add your business to Google</strong>.",
    'Choose the category that fits best, like "Lawn care service" or "Barber shop."',
    "If customers come to you, add your address. If you go to customers, add the towns you serve instead.",
    "Add your business phone number. Skip the website and extra questions. I'll fill those in.",
    "Verify. Google will ask you to confirm by text, phone call, email, or a short video of your business. Follow what it asks. A video can take a few days to be approved.",
])

GOOGLE_ACCESS_STEPS = steps([
    "While signed in, search Google for your business name. Your Business Profile appears at the top.",
    "Tap the <strong>three dots</strong> (⋮), then <strong>Business Profile settings</strong>.",
    "Tap <strong>People and access</strong>, then <strong>Add</strong>.",
    f"Enter <strong>{EMAIL}</strong>, choose <strong>Manager</strong>, and tap <strong>Invite</strong>.",
])

BLOCK_1 = checklist([
                "<strong>Listing finished:</strong> the right categories, your services and prices, hours, service area, and a description written to match what customers search for.",
                "<strong>Photos:</strong> your logo, a cover photo, and photos of your work.",
                "<strong>Connected to your website:</strong> your website, phone, and quote or booking link all go to the right place.",
                "<strong>More reviews:</strong> a \"Review us on Google\" button on your website and a review link you can text to happy customers.",
                "<strong>A monthly Google post</strong>, like a special offer or seasonal reminder, so your listing stays active.",
                "<strong>Always up to date:</strong> new hours, holiday hours, photos, and services. Just text me the change.",
            ])

BLOCK_2 = done_form("get-found-on-google", "Get Found on Google: customer finished steps", [
    ("google_listing", "Step 1: My business is on Google"),
    ("google_verified", "Google verified it (not still waiting)"),
    ("google_manager", "Step 2: I added Jeremy as a manager"),
])

BLOCK_3 = checklist([
                "<strong>Listing checked and finished:</strong> I make sure your name, phone, address, hours, and categories match Google exactly. Matching info helps you rank higher.",
                "<strong>Photos and services</strong> added, the same as your Google listing.",
                "<strong>Your website added to Bing:</strong> I set up Bing Webmaster Tools so your web pages show up in Bing search, not just your map listing.",
                "<strong>New pages sent to Bing automatically,</strong> so new services and blog posts show up fast.",
                "<strong>Kept in sync:</strong> when your hours or services change, I update Bing too.",
            ])

BLOCK_4 = done_form("get-found-on-bing", "Get Found on Bing: customer finished steps", [
    ("bing_import", "I imported my business to Bing"),
    ("bing_user", "I added Jeremy as a user"),
])


GOOGLE = f"""{pro_notice("Getting found on Google")}
{jump(GOOGLE_G)}
          <div id="done" class="gs-done">{icon("circle-check")} Thanks! I got your message and I'll take it from here.</div>
          <div class="prose gs">
            <h2 id="why">{GOOGLE_G} Why your Google listing matters</h2>
            <p>When someone nearby searches for what you do, like "lawn care near me," Google shows a map with a few local businesses <strong>above</strong> the regular websites. Each one is a <strong>Google Business Profile</strong>: your name, stars and reviews, hours, photos, and a big <strong>Call</strong> button.</p>
            <p>For most local businesses, this listing brings in more calls than the website itself. Google's listing is free, but managing it the right way and keeping it fresh takes time every month. That's what the Pro plan covers.</p>

            <h2 id="included">{icon("sparkles")} What I do for you in the Pro plan</h2>
            {BLOCK_1}

            <h2 id="your-steps">{icon("square-pen")} Your part: about 10 minutes</h2>
            <p>From the start, add <strong>{EMAIL}</strong> as <strong>Manager</strong>. If you don't have a Google listing yet, that part is yours. Google only lets the business owner add one. You never share your password, and you stay the owner.</p>
            <h3>Step 1: If you don't have a Google listing yet</h3>
            {GOOGLE_STEPS}
            <h3>Step 2: Add me as a manager</h3>
            <p>Type <strong>{EMAIL}</strong>, choose Manager, and tap Invite. This lets me do everything above from my own account. You can remove me anytime with one tap.</p>
            {GOOGLE_ACCESS_STEPS}

            <h2>What happens next</h2>
            <p>As soon as you tap the button below, I accept your invite and update your hours, photos, and info, usually within 2–3 business days. A brand-new listing can take a few weeks to start showing up high in Google Maps. Reviews and monthly posts help it climb.</p>
            <p>Want to show up on Bing too? It only takes 3 more minutes: <a href="/get-found-on-bing.html">Get Found on Bing</a>.</p>

            <h2 id="finished">{icon("circle-check")} Tell me you're done</h2>
            <p>Check off what you finished and tap the button. I'll get an email and take it from there.</p>
{BLOCK_2}
          </div>"""

BING_STEPS = steps([
    'Finish <a href="/get-found-on-google.html#your-steps">Get Found on Google</a> first. Bing copies your Google listing, so you won\'t type anything twice.',
    'Go to <a href="https://www.bingplaces.com/" target="_blank" rel="noopener">bingplaces.com</a> and sign in with the <strong>same Google account</strong>.',
    "Choose <strong>Import from Google Business Profile</strong> and allow access.",
    "Select your business and tap <strong>Import</strong>. Bing copies everything over, and your listing usually goes live within a few days.",
    f"Open <strong>Manage users</strong>, add <strong>{EMAIL}</strong>, and save. This lets me keep Bing up to date for you.",
])

BING = f"""{pro_notice("Getting found on Bing")}
{jump(BING_B)}
          <div id="done" class="gs-done">{icon("circle-check")} Thanks! I got your message and I'll take it from here.</div>
          <div class="prose gs">
            <h2 id="why">{BING_B} Why Bing matters</h2>
            <p>Bing is the search engine built into <strong>Windows computers</strong> and the <strong>Microsoft Edge</strong> browser. Bing's results also power searches on <strong>Yahoo</strong> and <strong>DuckDuckGo</strong>. Many people, especially on work computers, search with Bing without even knowing it.</p>
            <p>A <strong>Bing Places</strong> listing puts your business on Bing Maps with your hours, phone number, photos, and website, so those customers find you instead of a competitor. Fewer businesses bother with Bing, which makes it easier to stand out.</p>

            <h2 id="included">{icon("sparkles")} What I do for you in the Pro plan</h2>
            {BLOCK_3}

            <h2 id="your-steps">{icon("square-pen")} Your part: about 3 minutes</h2>
            <p>From the start, add <strong>{EMAIL}</strong> as a <strong>user</strong> (that's Bing's name for Manager). If you don't have a Bing listing yet, that part is yours. You never share your password with me.</p>
            {BING_STEPS}

            <h2>What happens next</h2>
            <p>As soon as you tap the button below, I update your Bing listing and add your website to Bing, usually within 2–3 business days.</p>

            <h2 id="finished">{icon("circle-check")} Tell me you're done</h2>
            <p>Check off what you finished and tap the button. I'll get an email and take it from there.</p>
{BLOCK_4}
          </div>"""

REDIRECT = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="robots" content="noindex" />
    <meta http-equiv="refresh" content="0; url=/get-found-on-google.html" />
    <link rel="canonical" href="{site}/get-found-on-google.html" />
    <title>Get Found on Google | Stakich Websites</title>
  </head>
  <body><p>This page moved to <a href="/get-found-on-google.html">Get Found on Google</a>.</p></body>
</html>
"""


def build():
    page(
        "get-found-on-google.html",
        "Get Found on Google",
        "Show up on Google Maps and Google Search when nearby customers look for what you do. Google Business Profile management and upkeep, included in the Stakich Websites Pro plan.",
        "Show up on Google Maps and Google Search when nearby customers look for what you do.",
        GOOGLE,
        active="found",
        eyebrow="Pro plan",
    )
    page(
        "get-found-on-bing.html",
        "Get Found on Bing",
        "Show up on Bing, Yahoo, and DuckDuckGo. Bing Places listing management and Bing search setup, included in the Stakich Websites Pro plan.",
        "Show up on Bing, Yahoo, and DuckDuckGo when customers search on Windows computers and Microsoft Edge.",
        BING,
        active="found",
        eyebrow="Pro plan",
    )
    from pathlib import Path

    (Path(__file__).resolve().parent.parent / "get-on-google.html").write_text(REDIRECT.format(site=SITE), encoding="utf-8")
    print("wrote get-found-on-google.html, get-found-on-bing.html, get-on-google.html (redirect)")


if __name__ == "__main__":
    build()
