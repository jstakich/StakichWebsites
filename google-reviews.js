(function () {
  const roots = document.querySelectorAll("[data-google-reviews]");
  if (!roots.length) {
    return;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function stars(rating) {
    const count = Math.max(0, Math.min(5, Math.round(Number(rating) || 0)));
    return "★★★★★".slice(0, count) + "☆☆☆☆☆".slice(0, 5 - count);
  }

  function summaryText(data) {
    const total = Number(data.userRatingsTotal || 0);
    const average = Number(data.rating || 0);
    const averageLabel = average >= 4.95 ? "5.0" : average ? average.toFixed(1) : "";
    if (!total) {
      return "No Google ratings yet.";
    }
    const word = total === 1 ? "rating" : "ratings";
    return averageLabel + " on Google, from " + total + " " + word + ".";
  }

  function card(review) {
    const author = escapeHtml(review.author || "Google reviewer");
    const text = (review.text || "").trim();
    const body = text
      ? "<p>" + escapeHtml(text) + "</p>"
      : "<p>No written comment on Google.</p>";
    return (
      '<article class="card" style="max-width: 640px;">' +
      '<p style="margin: 0 0 8px; color: #e2a100; letter-spacing: 2px; font-size: 1.15rem;" aria-label="' +
      (review.rating || 0) +
      ' out of 5 stars">' +
      stars(review.rating) +
      "</p>" +
      "<h3 style=\"margin: 0 0 6px;\">" +
      author +
      "</h3>" +
      body +
      "</article>"
    );
  }

  function note(data) {
    const maps = data.mapsUrl || "https://www.google.com/maps?cid=7957889677610712468";
    const write = data.reviewUrl || "https://g.page/r/CZT9u8N_GnBuEBM/review";
    const reviewsLink = location.pathname.endsWith("/reviews.html")
      ? ""
      : '<a href="/reviews.html">Reviews</a> · ';
    return (
      reviewsLink +
      '<a href="' +
      escapeHtml(maps) +
      '" target="_blank" rel="noopener">Read it on Google</a> · <a href="' +
      escapeHtml(write) +
      '" target="_blank" rel="noopener">Write a review</a>'
    );
  }

  function render(data) {
    const reviews = Array.isArray(data.reviews) ? data.reviews : [];
    roots.forEach(function (root) {
      const summary = root.querySelector("[data-google-reviews-summary]");
      const list = root.querySelector("[data-google-reviews-list]");
      const footnote = root.querySelector("[data-google-reviews-note]");
      if (summary) summary.textContent = summaryText(data);
      if (list) {
        list.innerHTML = reviews.length
          ? reviews.map(card).join("")
          : "<p>No written reviews yet.</p>";
      }
      if (footnote) footnote.innerHTML = note(data);
    });
  }

  fetch("/google-reviews.json", { cache: "no-cache" })
    .then(function (response) {
      if (!response.ok) throw new Error("missing");
      return response.json();
    })
    .then(render)
    .catch(function () {
      roots.forEach(function (root) {
        const summary = root.querySelector("[data-google-reviews-summary]");
        if (summary && !summary.textContent) {
          summary.textContent = "Google reviews could not load.";
        }
      });
    });
})();
