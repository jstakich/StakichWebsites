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

    window.matchMedia("(min-width: 1361px)").addEventListener("change", function (event) {
      if (event.matches) {
        setOpen(false);
      }
    });
  }

  document.querySelectorAll(".nav-drop").forEach(function (drop) {
    var btn = drop.querySelector(".nav-drop-btn");
    var setDrop = function (open) {
      drop.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    };
    btn.addEventListener("click", function (event) {
      event.stopPropagation();
      setDrop(!drop.classList.contains("is-open"));
    });
    document.addEventListener("click", function (event) {
      if (!drop.contains(event.target)) {
        setDrop(false);
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        setDrop(false);
      }
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
