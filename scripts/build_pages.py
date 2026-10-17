"""Builds policy pages, support, thank-you, and 404 from the shared header/footer."""
from pathlib import Path

from icons import icon
from common import EMAIL, PAY_BADGES, PHONE, SITE, contact_options, share_mount, footer, head, page_hero, scripts, topbar

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "October 10, 2026"
TERMS_UPDATED = "October 17, 2026"
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
              <li><strong>Starter:</strong> $199 setup, then $49 per month. Up to 5 pages, mobile-friendly; tap to call or text, plus a quote form; monthly hosting, HTTPS, security, and backups; built to show up in Google search; and 2 small updates each month (new photos or text changes).</li>
              <li><strong>Growth:</strong> $299 setup, then $79 per month. Everything in Starter; up to 8 pages; 1 blog post written for you each month; blogs ready to share on social media; a Google reviews section; and share buttons on every page.</li>
              <li><strong>Pro:</strong> $499 setup, then $129 per month. Everything in Growth; up to 12 pages; online booking, menu, or quote tools; 2 blog posts each month; priority same-day updates when possible; and your Google and Bing listings set up and kept current.</li>
            </ul>
            <p>Blog posts and your privacy policy page don't count toward your page limit.</p>
            <p>Work outside your plan (for example, extra pages or custom features) will be quoted in writing before it starts.</p>
            <h2>3. Payment</h2>
            <p>We accept all major credit and debit cards, including Visa, Mastercard, American Express, and Discover, as well as Apple Pay and Google Pay. Payments are processed securely by Stripe; we never see or store your full card number. The setup fee and your first month are paid together before design work begins. After that, the monthly plan is billed automatically every month on the same date to your card on file until canceled. Prices are in US dollars.</p>
            <h2>4. Your responsibilities</h2>
            <p>You agree to provide accurate business information, and you confirm that you have the right to use any logos, photos, and text you send us. You are responsible for the claims your business makes on its website.</p>
            <h2>5. Ownership</h2>
            <p>Your logos, photos, and written content belong to you. If you need a domain name, we register and renew it for you as part of your plan. If you cancel and your account is paid up, we will transfer the domain to you on request. If you already own a domain, it stays yours. The website design and code belong to Stakich Websites and may be used for your business while your plan is active. If you cancel, your website goes offline at the end of your billing month.</p>
            <h2>6. Cancellation</h2>
            <p>There is no contract. You may cancel your monthly plan at any time by email. Cancellation takes effect at the end of your current billing month, and your website stays online until then. Refunds are covered by our <a href="/refund-policy.html">Refund &amp; Cancellation Policy</a>.</p>
            <h2>7. Website availability</h2>
            <p>We work to keep your website online and secure, but we cannot guarantee uninterrupted service, since hosting depends on third-party providers. We do not guarantee specific Google rankings, traffic, or sales, because search engines control their own results.</p>
            <h2>8. Limitation of liability</h2>
            <p>To the extent allowed by law, our total liability for any claim related to our services is limited to the amount you paid us in the three months before the claim.</p>
            <h2>9. Changes to these terms</h2>
            <p>We may update these terms from time to time. Changes will be posted on this page with a new date. Price changes for existing customers will be announced by email at least 30 days in advance.</p>
            <h2>10. Governing law</h2>
            <p>These terms are governed by the laws of the State of Tennessee, USA.</p>
            <p><em>Last updated: {TERMS_UPDATED}</em></p>""")

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
            <h2>No tracking</h2>
            <p>This website does not use analytics or tracking tools, and we don't track visitors on the websites we build for our customers. While you fill out the order form, your answers are saved only on your own device so you don't lose them. Stripe may use cookies on its secure payment pages to process your payment.</p>
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
              <li>No contract. Cancel anytime by emailing {MAIL}.</li>
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

SUPPORT = f"""          <div class="prose">
            <p><b>Already a customer?</b> The <a href="/customer-guide.html">Customer Guide</a> answers the most common questions: your domain, changes, Google, quote requests, billing, and more.</p>
          </div>
          <div class="support-reach">
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
              <p>Stripe emails a receipt every month. Change your card in that email (I never see your card). Can't find it, or have a question about a charge? Email {MAIL} and I'll send you Stripe's page.</p>
            </article>
          </div>
          <div class="prose">
            <h2>How to request a change</h2>
            <ol>
              <li>Email {MAIL} with the subject "Website change" and your business name.</li>
              <li>Describe what you'd like changed and on which page.</li>
              <li>Attach any new photos, logos, or documents.</li>
            </ol>
            <p>Most small changes are done within 1–2 business days. Pro plan customers get priority same-day updates when possible.</p>
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
            <p>There's no contract. To cancel, email {MAIL}. Your site stays online through the end of your billing month. See the <a href="/refund-policy.html">Refund &amp; Cancellation Policy</a> for details.</p>
            <h2>Policies</h2>
            <ul>
              <li><a href="/privacy.html">Privacy Policy</a></li>
              <li><a href="/terms.html">Terms of Service</a></li>
              <li><a href="/refund-policy.html">Refund &amp; Cancellation Policy</a></li>
            </ul>
            {share_mount("Know a business owner who needs help with their website? Share this")}
            <p><small>Payment logos from the open-source <a href="https://github.com/datatrans/payment-logos" target="_blank" rel="noopener">payment-logos</a> project by Datatrans, licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>.</small></p>
          </div>"""



DOMAIN_STEPS = f"""            <p>This lets me point your domain to your new website. It takes about 2 minutes, and you never share your password. Your email keeps working, and the domain stays yours.</p>
            <p><b>GoDaddy:</b></p>
            <ol>
              <li>Sign in to GoDaddy and tap your name at the top right, then <b>Account Settings</b>, then <b>Delegate Access</b>.</li>
              <li>Tap <b>Invite to Access</b>, type <b>Jeremy Stakich</b> and <b>{EMAIL}</b>.</li>
              <li>Choose <b>Products &amp; Domains</b>, then tap <b>Invite</b>.</li>
            </ol>
            <p><b>Squarespace:</b> Sign in, open <b>Domains</b>, tap your domain, then <b>Permissions</b>. Invite <b>{EMAIL}</b> and allow it to manage the domain.</p>
            <p><b>Wix:</b> Sign in, open your site's <b>Settings</b>, then <b>Roles &amp; Permissions</b>. Tap <b>Invite People</b>, type <b>{EMAIL}</b>, and choose <b>Admin (Co-Owner)</b>.</p>
            <p><b>Any other company:</b> Sign in and look for <b>Delegate Access</b>, <b>Share Access</b>, or <b>Permissions</b>, and invite <b>{EMAIL}</b>.</p>
            <p><b>Not sure where you bought it?</b> Search your email for your domain name and the word "renewal." The company that sends the renewal emails is the one.</p>
            <p>Please don't cancel or move your domain. Once your new website is live, you can cancel your old website plan, but keep paying the yearly domain renewal.</p>"""

THANKS = prose(f"""
            <h2>Thank you! I've got it.</h2>
            <p>Thanks for choosing Stakich Websites. If you sent a message, I'll reply within one business day. If you just paid, I'm starting on your website. Here's what happens next.</p>
            <h2>Just paid? What happens next</h2>
            <ol>
              <li>Stripe emails you a receipt.</li>
              <li>I build your website using your answers, your photos, and your Facebook and Google pages. You don't need to send anything else unless you want to.</li>
              <li>I text or email you a link to see your website, usually within 1–2 weeks.</li>
              <li>You ask for changes until you're happy, then it goes live.</li>
            </ol>
            <h2>Need a new domain? Nothing to do.</h2>
            <p>If you picked a new web address on the form, I buy it and set it up for you. It's included in your plan.</p>
            <h2>Already own your domain? Give me access</h2>
{DOMAIN_STEPS}
            <h2>Pro plan: connect your Google and Bing listings</h2>
            <p>You create the listing. Google only lets the business owner do that. Then you add me as Manager so I can keep your hours, photos, and info up to date. You never share your password.</p>
            <p><b>Already have a Google listing?</b></p>
            <ol>
              <li>Sign in to the Google account you use for your business, then search Google for your business name.</li>
              <li>On your business profile, tap the <b>⋮</b> menu (three dots), then <b>Business Profile settings</b>, then <b>People and access</b>.</li>
              <li>Tap <b>Add</b>, type <b>{EMAIL}</b>, choose <b>Manager</b>, and tap <b>Invite</b>.</li>
            </ol>
            <p><b>No Google listing yet?</b> You create it, then add me as Manager. The steps are on <a href="/get-found-on-google.html">Get Found on Google</a>.</p>
            <p><b>Bing:</b> You import your Google listing to Bing, then add me as a user. I manage it after that. The steps are on <a href="/get-found-on-bing.html">Get Found on Bing</a>.</p>
            <h2>Questions?</h2>
            <p>Most answers are in the <a href="/customer-guide.html">Customer Guide</a>. You can also call, text, or email me anytime.</p>
{contact_options()}
            {share_mount("Know another business owner who needs a website? Share this page")}
            <p><a class="btn btn-primary" href="/">Back to the home page</a></p>""")

def faq(*items):
    rows = "\n".join(f"""              <details>
                <summary>{q}</summary>
                {a}
              </details>""" for q, a in items)
    return f'            <div class="faq">\n{rows}\n            </div>'


_G0 = faq(
    ("What happens after I pay?", "<p>Stripe emails you a receipt. I build your website from your order form answers, your photos, and your Facebook and Google pages. In about 1–2 weeks I text or email you a link to see it. You ask for any changes, and once you're happy, it goes live.</p>"),
    ("Do I need to send you anything else?", "<p>No. Your order form has what I need. If you think of more photos or details later, text or email them anytime.</p>"),
    ("How long until my website is live?", "<p>Usually 1–2 weeks after you order. Changes you ask for during the review are part of that.</p>"),
    ("Can I see my website before it goes live?", "<p>Yes. I send you a private link first. Nothing goes live until you say it looks good.</p>"),
    ("I have an old website. What do I do with it?", "<p>Keep it running until your new website is live. After that, you can cancel your old website plan (like GoDaddy Websites + Marketing, Wix, or Squarespace). Keep paying for your domain, though. That's your web address.</p>"),
    ("Can you use the words and photos from my old website?", "<p>Yes. I move over anything worth keeping, so nothing important gets lost.</p>"),
    ("I don't have a logo or many photos. Is that OK?", "<p>Yes. Send what you have, even photos from your phone. I can also use photos from your Facebook page.</p>"),)
_G1 = faq(
    ("I picked a new domain on the form. What do I do?", "<p>Nothing. I buy it, set it up, and renew it every year. It's included in your plan.</p>"),
    ("I already own my domain. What do I do?", DOMAIN_STEPS),
    ("Will my business email stop working?", "<p>No. If you get email at your domain (like you@yourbusiness.com), I leave the email settings alone, so it keeps working the whole time.</p>"),
    ("Can I get an email address like you@yourbusiness.com?", "<p>Email isn't part of the website plans, and I don't set it up. The cheap way to get you@yourbusiness.com in Gmail is <a href=\"https://workspace.google.com\" target=\"_blank\" rel=\"noopener\">Google Workspace Business Starter</a>. It's about $7 a month per person if you pay for a year, or about $8 a month if you pay month to month. You buy it from Google and pay Google. It works in the Gmail app like a normal Gmail account, with your business address on it.</p><p>Microsoft 365 Business Basic is about the same price if you'd rather use Outlook. Google's prices can change, so check their site before you buy.</p>"),
    ("What happens to my domain if I cancel?", "<p>If you already owned it, it stays yours, just like before. If I bought it for you and your account is paid up, I'll transfer it to you when you ask. You can take it anywhere.</p>"),)
_G2 = faq(
    ("How do I ask for a change?", f"<p>Text {PHONE} or email {MAIL}. Tell me what to change and on which page, and attach any new photos. That's it.</p>"),
    ("What's a small update?", "<p>Things like new hours, prices, phone number, photos, a new service, or changing some text. Starter and Growth include 2 small updates each month. Pro gets priority same-day updates when possible.</p>"),
    ("How fast are changes made?", "<p>Most small changes are done in 1–2 business days. If your website is ever down or broken, I fix it the same day.</p>"),
    ("Can I edit the website myself?", "<p>You don't need to. There's no login to learn or forget. Just text or email what you want changed and I'll do it.</p>"),
    ("Can I add more pages?", "<p>Starter includes up to 5 pages, Growth up to 8, and Pro up to 12. Blog posts and your privacy policy page don't count toward that. Need more? Ask about moving up a plan.</p>"),
    ("Can I switch plans?", "<p>Yes. Text or email me which plan you want. I'll tell you exactly what changes before anything is charged.</p>"),
    ("Who writes my blog posts?", "<p>I do, on Growth (1 post a month) and Pro (2 posts a month). Each post is ready to share on Facebook or other social media. Got a topic or a question customers ask a lot? Send it and I'll write about it.</p>"),
    ("Do you post on my Facebook for me?", "<p>No. I write the blog posts on Growth and Pro. You share them yourself with the buttons on your website. It only takes a few seconds.</p>"),)
_G3 = faq(
    ("Will my website show up on Google?", "<p>Yes. Every plan is built to show up in Google search, with the right titles, descriptions, and local info. Google usually takes a few weeks to show a new website, so don't worry if it's not there on day one. No one can honestly promise the #1 spot, but a fast, clear website helps a lot.</p>"),
    ("What does the Pro plan do with Google and Bing?", "<p>You create the Google listing (Google only lets the owner do that), then add <b>" + EMAIL + "</b> as a Manager. I keep the hours, photos, and info current. Same idea on Bing: you import Google, then add me. I do not create the listing. The steps are on your <a href=\"/thank-you.html\">thank-you page</a>, <a href=\"/get-found-on-google.html\">Get Found on Google</a>, and <a href=\"/get-found-on-bing.html\">Get Found on Bing</a>.</p>"),
    ("How do I get more Google reviews?", "<p>Ask happy customers right after a good job, and text them your review link. Never pay or give discounts for reviews, because that's against Google's rules. On Growth and Pro, your website shows your Google reviews.</p>"),
    ("Can I see how many people visit my website?", "<p>I don't put tracking on your website, to protect your customers' privacy. The best signs are more calls, texts, and quote requests. Ask new customers \"How did you find us?\" If you have a Google Business Profile, Google also shows you how many people found you there.</p>"),)
_G4 = faq(
    ("Where do quote requests and messages go?", "<p>Straight to your email, so they pop up on your phone right away. Calls and texts from your website go to your phone number.</p>"),
    ("I got an email asking me to confirm my form. Is that real?", "<p>Yes. The first time your quote form is used, you may get one email from FormSubmit asking you to confirm. Tap the button once, so every request reaches you.</p>"),
    ("I'm not getting quote request emails.", f"<p>Check your spam or junk folder and mark the email as \"not spam.\" Still nothing? Text me at {PHONE} and I'll test it right away.</p>"),
    ("My phone number, hours, or address changed.", "<p>Text or email me the new info. It counts as a small update, and I'll also update your Google listing if you're on Pro.</p>"),)
_G5 = faq(
    ("When am I charged?", "<p>You pay the setup fee and your first month together. After that, your monthly plan is charged automatically on the same date each month.</p>"),
    ("How do I pay, and is it safe?", "<p>All major cards, Apple Pay, and Google Pay, processed securely by Stripe. I never see or store your full card number.</p>"),
    ("How do I update my card or get a receipt?", f"<p>Stripe emails a receipt every month. To change your card, open that email and use Stripe's update-card link. I never see your card number, so don't email it to me. If you can't find the receipt, email {MAIL} and I'll send you Stripe's page. Same if you have a question about a charge.</p>"),
    ("Is there a contract?", "<p>No. You can cancel anytime.</p>"),
    ("How do I cancel?", f"<p>Email {MAIL}. Your website stays online until the end of your billing month, and you won't be charged again after that.</p>"),
    ("Can I get a refund?", "<p>Full refund if you cancel before design work starts. Half of the setup fee back if you cancel after work starts but before your website goes live. No refund after it's live, since the work is done. Details: <a href=\"/refund-policy.html\">Refund &amp; Cancellation Policy</a>.</p>"),
    ("Does my monthly price stay the same?", "<p>Yes. You keep paying the monthly price of the plan you picked. It doesn't jump after the first year.</p>"),)
_G6 = faq(
    ("What's mine?", "<p>Your logo, photos, and words are always yours. If you already owned your domain, it stays yours. If I bought it for you, I'll transfer it to you if you ever leave.</p>"),
    ("What happens to my website if I cancel?", "<p>It goes offline at the end of your billing month. The website design and code belong to Stakich Websites. Full details are in the <a href=\"/terms.html\">Terms of Service</a>.</p>"),
    ("Is my website safe and backed up?", "<p>Yes. Every plan includes HTTPS (the padlock), security, monitoring, and backups, so any change can be undone.</p>"),
    ("Do you sell my information or track my visitors?", "<p>No. I never sell your information, and I don't track visitors on your website. See the <a href=\"/privacy.html\">Privacy Policy</a>.</p>"),)

GUIDE = prose(f"""
            <p>Everything you need to know as a Stakich Websites customer, in one place. Can't find your answer? Call or text {PHONE} or email {MAIL}.</p>
            <p><b>Jump to:</b> <a href="#start">Getting started</a> · <a href="#domain">Your domain</a> · <a href="#changes">Changes and updates</a> · <a href="#google">Google and getting found</a> · <a href="#forms">Calls, texts, and quote requests</a> · <a href="#billing">Billing and canceling</a> · <a href="#own">What you own</a></p>

            <h2 id="start">Getting started</h2>
{_G0}

            <h2 id="domain">Your domain (web address)</h2>
{_G1}

            <h2 id="changes">Changes and updates</h2>
{_G2}

            <h2 id="google">Google and getting found</h2>
{_G3}

            <h2 id="forms">Calls, texts, and quote requests</h2>
{_G4}

            <h2 id="billing">Billing and canceling</h2>
{_G5}

            <h2 id="own">What you own</h2>
{_G6}

            <h2>Still have a question?</h2>
            <p>Call, text, or email me. I usually reply the same day.</p>
{contact_options()}
            {share_mount("Know a business owner who needs a website? Share this")}""")

NOT_FOUND = prose("""
            <h2 id="nf-title">This page doesn't exist.</h2>
            <p id="nf-text">The link may be old or mistyped.</p>
            <p><a class="btn btn-primary" href="/">Go to the home page</a></p>
            <script>
            (function () {
              var path = location.pathname;
              var m = path.match(/^\\/preview\\/([^\\/]+)/i);
              if (!m) return;
              // Fix the common copy-paste mistakes: capital letters, a stray period or bracket at the end, doubled slashes.
              var slug = decodeURIComponent(m[1]).toLowerCase().replace(/[^a-z0-9-]+/g, "");
              var fixed = "/preview/" + slug + "/";
              if (slug && fixed !== path) {
                location.replace(fixed);
                return;
              }
              document.getElementById("nf-title").textContent = "That preview link isn't quite right.";
              document.getElementById("nf-text").innerHTML = "Part of the link may have been cut off when it was copied. Call or text Jeremy at <a href=\\"tel:+14232277681\\">(423) 227-7681</a>, or email <a href=\\"mailto:jeremy@stakichwebsites.com\\">jeremy@stakichwebsites.com</a>, and I'll send you the right link.";
            })();
            </script>""")


def build():
    page("terms.html", "Terms of Service", "Terms of service for Stakich Websites website design, hosting, and care plans.", "The simple terms for working with Stakich Websites.", TERMS)
    page("privacy.html", "Privacy Policy", "Privacy policy for Stakich Websites: what information we collect, how it's used, how Stripe protects payments, and how to request deletion.", "How your information is collected, used, and protected.", PRIVACY)
    page("refund-policy.html", "Refund & Cancellation Policy", "Refund and cancellation policy for Stakich Websites setup fees and monthly plans.", "Fair, clear rules for refunds and canceling.", REFUND)
    page("support.html", "Customer Support", "Get help with your Stakich Websites website: request changes, billing help, and contact support at Jeremy@StakichWebsites.com.", "Website changes, billing, and questions. Real help from a real person.", SUPPORT, active="support", eyebrow="Support")
    page("customer-guide.html", "Customer Guide", "Answers for Stakich Websites customers: what happens after you pay, your domain, changes and updates, Google, quote requests, billing, and canceling.", "Everything you need to know, in one place.", GUIDE, active="guide", eyebrow="Customers")
    page("thank-you.html", "Thank You", "Thanks for choosing Stakich Websites.", "You're all set. Here's what happens next.", THANKS, index=False)
    page("404.html", "Page Not Found", "Page not found.", "Sorry, we couldn't find that page.", NOT_FOUND, index=False)


if __name__ == "__main__":
    build()
