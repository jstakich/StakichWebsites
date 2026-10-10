/*
 * Stripe payment links.
 * Paste each plan's Stripe Payment Link between the quotes.
 * While a link is empty, that plan's button goes to the contact form instead.
 */
var STRIPE_LINKS = {
  starter: "",
  growth: "",
  pro: "",
};

(function () {
  var topbar = document.querySelector(".topbar");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");

  if (topbar && toggle && nav) {
    var setOpen = function (open) {
      topbar.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };

    toggle.addEventListener("click", function () {
      setOpen(!topbar.classList.contains("is-open"));
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        setOpen(false);
      }
    });

    window.matchMedia("(min-width: 901px)").addEventListener("change", function (event) {
      if (event.matches) {
        setOpen(false);
      }
    });
  }

  var planSelect = document.getElementById("plan");

  document.querySelectorAll("[data-plan]").forEach(function (button) {
    var plan = button.getAttribute("data-plan");
    var link = STRIPE_LINKS[plan];

    if (link) {
      button.href = link;
      button.setAttribute("rel", "noopener");
      return;
    }

    button.href = "/#contact";
    button.addEventListener("click", function () {
      if (planSelect) {
        planSelect.value = plan;
      }
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
