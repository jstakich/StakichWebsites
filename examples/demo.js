(function () {
  document.querySelectorAll(".d-slots button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.parentNode.querySelectorAll("button").forEach(function (b) {
        b.classList.remove("is-picked");
      });
      btn.classList.add("is-picked");
    });
  });

  document.querySelectorAll(".d-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var msg = form.querySelector(".d-form-msg");
      if (msg) {
        msg.textContent = "This is an example website, so the form doesn't send. Yours would!";
      }
    });
  });

  function toast(text) {
    var el = document.querySelector(".d-toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "d-toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = text;
    el.classList.add("is-on");
    clearTimeout(el._t);
    el._t = setTimeout(function () {
      el.classList.remove("is-on");
    }, 4200);
  }

  // Fake business contact links show a note instead of calling, texting, or emailing.
  // Links to Jeremy and empty-recipient share links still work.
  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest('a[href^="tel:"], a[href^="sms:"], a[href^="mailto:"]');
    if (!link) return;
    var href = link.getAttribute("href");
    var kind = href.split(":")[0];
    var to = href.slice(kind.length + 1).split("?")[0];
    if (!to) return;
    if (kind === "mailto" ? /stakichwebsites\.com$/i.test(to) : to.replace(/\D/g, "").slice(-10) === "4232277681") return;
    event.preventDefault();
    var action = kind === "tel" ? "call" : kind === "sms" ? "text" : "email";
    toast("This is an example website, so the " + (kind === "mailto" ? "email isn't" : "number isn't") + " real. On your site, this button would " + action + " you.");
  }, true);
})();
