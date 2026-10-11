"""Privacy policy text for the websites built for customers (previews and examples). Mirrors the Stakich Websites policy."""
from html import escape

UPDATED = "October 11, 2026"


def privacy_body(name, contact, location):
    """contact: list of (label, href) like [("(423) 555-0142", "tel:+14235550142")]."""
    n = escape(name)
    reach = " · ".join(f'<a href="{escape(h)}">{escape(t)}</a>' for t, h in contact)
    first = f'<a href="{escape(contact[0][1])}">{escape(contact[0][0])}</a>'
    return f"""
            <h2>Information we collect</h2>
            <p>When you call, text, email, fill out a form, request a quote or appointment, or become a customer of {n}, we collect the information you give us, such as your name, phone number, email address, address, and details about what you need.</p>
            <h2>How we use it</h2>
            <ul>
              <li>To reply to your questions and send quotes</li>
              <li>To schedule and confirm appointments</li>
              <li>To provide our services and follow up on your job</li>
            </ul>
            <h2>What we never do</h2>
            <p>We do not sell, rent, or trade your personal information. We share it only with services needed to run this website and our business (such as our form provider and our hosting provider), or when required by law.</p>
            <h2>No tracking</h2>
            <p>This website does not use analytics or tracking tools. If you leave a form half-finished, your answers may be saved only on your own device so you don't lose them.</p>
            <h2>Your choices</h2>
            <p>You can ask us to see, correct, or delete the information we have about you at any time. Just contact us at {first}.</p>
            <h2>Contact</h2>
            <p>{n} · {escape(location)} · {reach}</p>
            <p><em>Last updated: {UPDATED}</em></p>"""
