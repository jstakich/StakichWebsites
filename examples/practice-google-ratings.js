(function () {
  const card = document.querySelector("[data-practice-google-rating]");
  if (!card) return;

  function loadPlaces(key) {
    if (window.google?.maps?.importLibrary) {
      return window.google.maps.importLibrary("places");
    }
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      const callback = "loadPracticeGooglePlaces";
      const params = new URLSearchParams({ key, callback, loading: "async", v: "weekly" });
      window[callback] = () => {
        delete window[callback];
        window.google.maps.importLibrary("places").then(resolve, reject);
      };
      script.onerror = () => {
        delete window[callback];
        reject(new Error("Google Maps could not load."));
      };
      script.src = "https://maps.googleapis.com/maps/api/js?" + params;
      script.async = true;
      document.head.append(script);
    });
  }

  function phoneDigits(value) {
    return (value || "").replace(/\D/g, "").replace(/^1(?=\d{10}$)/, "");
  }

  function render(place) {
    if (place.googleMapsURI) {
      card.querySelector("[data-google-maps-link]").href = place.googleMapsURI;
    }

    const rating = place.rating;
    const count = place.userRatingCount;
    if (!Number.isFinite(rating) || rating < 1 || rating > 5 ||
        !Number.isInteger(count) || count < 1) return;

    const score = document.createElement("span");
    score.className = "sw-google-stars";
    score.setAttribute("aria-hidden", "true");
    score.textContent = "★★★★★";
    const filled = document.createElement("span");
    filled.textContent = "★★★★★";
    filled.style.width = rating * 20 + "%";
    score.append(filled);

    const summary = card.querySelector("[data-google-rating-summary]");
    const label = count === 1 ? "rating" : "ratings";
    summary.replaceChildren(
      score,
      document.createTextNode(` ${rating.toFixed(1)} out of 5 · ${count.toLocaleString()} ${label}`)
    );
    summary.hidden = false;
  }

  async function showRating() {
    try {
      const response = await fetch("/examples/practice-google-ratings.json");
      if (!response.ok) return;
      const { browserApiKey } = await response.json();
      if (!browserApiKey) return;

      const { Place } = await loadPlaces(browserApiKey);
      const phone = card.dataset.phone;
      const { places } = await Place.searchByText({
        textQuery: phone,
        region: "us",
        maxResultCount: 5,
        fields: ["nationalPhoneNumber", "googleMapsURI", "rating", "userRatingCount"],
      });
      const matches = places.filter(place => (
        phoneDigits(place.nationalPhoneNumber) === phoneDigits(phone)
      ));
      if (matches.length === 1) render(matches[0]);
    } catch {
      // The Maps link remains available if a rating cannot be loaded.
    }
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      if (!entries.some(entry => entry.isIntersecting)) return;
      observer.disconnect();
      showRating();
    });
    observer.observe(card);
  } else {
    showRating();
  }
})();
