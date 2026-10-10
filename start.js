(function () {
  var params = new URLSearchParams(location.search);
  var STORE = "sw_start";

  var form = document.getElementById("start-form");
  if (form) {
    var wanted = params.get("plan");
    if (wanted) {
      var radio = form.querySelector('[data-plan-key="' + wanted + '"]');
      if (radio) {
        radio.closest("label").hidden = false;
        radio.checked = true;
      }
    }

    form.addEventListener("submit", function (event) {
      var groups = form.querySelectorAll("[data-required-group]");
      for (var i = 0; i < groups.length; i++) {
        if (!groups[i].querySelector("input:checked")) {
          event.preventDefault();
          groups[i].classList.add("is-missing");
          groups[i].scrollIntoView({ behavior: "smooth", block: "center" });
          return;
        }
        groups[i].classList.remove("is-missing");
      }

      var picked = form.querySelector('input[name="plan"]:checked');
      var key = picked ? picked.getAttribute("data-plan-key") : "";
      var name = form.querySelector('[name="name"]').value.trim();
      var business = form.querySelector('[name="business"]').value.trim();
      var email = form.querySelector('[name="email"]').value.trim();

      try {
        sessionStorage.setItem(STORE, JSON.stringify({ plan: key, name: name, email: email }));
      } catch (e) {}

      form.querySelector('[name="_next"]').value = location.origin + "/pay?plan=" + encodeURIComponent(key);
      form.querySelector('[name="_subject"]').value =
        "New website order (" + (picked ? picked.value : "plan?") + "): " + (business || name);
    });
  }

  var plans = window.SW_PLANS;
  var payBtn = document.getElementById("pay-btn");
  if (plans && payBtn) {
    var saved = {};
    try {
      saved = JSON.parse(sessionStorage.getItem(STORE) || "{}");
    } catch (e) {}

    var key = params.get("plan") || saved.plan;
    var plan = plans[key];
    var title = document.getElementById("pay-title");

    if (saved.name) {
      title.textContent = "Thanks, " + saved.name.split(" ")[0] + "! I have your answers.";
    } else {
      title.innerHTML = 'Pay for your website. <a href="/start">Haven\u2019t answered the questions yet? Start here.</a>';
    }

    if (!plan) {
      payBtn.style.display = "none";
      return;
    }

    var today = plan.setup + plan.monthly;
    document.getElementById("pay-plan").textContent = plan.name + " plan";
    document.getElementById("pay-total").textContent = plan.monthly
      ? "$" + today.toLocaleString() + " today ($" + plan.setup.toLocaleString() + " setup + first month), then $" +
        plan.monthly + "/month. Cancel anytime."
      : "$" + today.toLocaleString() + " one time.";

    if (!plan.link) {
      payBtn.textContent = "Payment link not set up yet";
      payBtn.removeAttribute("href");
      payBtn.setAttribute("aria-disabled", "true");
      return;
    }

    payBtn.textContent = "Pay $" + today.toLocaleString() + " Securely";
    payBtn.href = plan.link + (saved.email ? "?prefilled_email=" + encodeURIComponent(saved.email) : "");
  }
})();
