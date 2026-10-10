(function () {
  var params = new URLSearchParams(location.search);
  var SESSION = "sw_start";
  var DRAFT = "sw_draft";
  var DRAFT_MAX_AGE = 14 * 24 * 60 * 60 * 1000;
  var MAX_UPLOAD = 10 * 1024 * 1024;
  var plans = window.SW_PLANS || {};

  function readSession() {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION) || "{}");
    } catch (e) {
      return {};
    }
  }

  function money(n) {
    return "$" + n.toLocaleString();
  }

  function fillPay(key, saved) {
    var payBtn = document.getElementById("pay-btn");
    if (!payBtn) return;
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
      ? money(today) + " today (" + money(plan.setup) + " setup + first month), then " + money(plan.monthly) + "/month. Cancel anytime."
      : money(today) + " one time.";

    if (!plan.link) {
      payBtn.textContent = "Payment link not set up yet";
      payBtn.removeAttribute("href");
      payBtn.setAttribute("aria-disabled", "true");
      return;
    }

    payBtn.style.display = "";
    payBtn.textContent = "Pay " + money(today) + " Securely";
    payBtn.href = plan.link + (saved.email ? "?prefilled_email=" + encodeURIComponent(saved.email) : "");
  }

  var form = document.getElementById("start-form");

  if (!form) {
    var saved = readSession();
    fillPay(params.get("plan") || saved.plan, saved);
    return;
  }

  var steps = Array.prototype.slice.call(form.querySelectorAll(".form-step"));
  var stepCount = document.getElementById("step-count");
  var stepName = document.getElementById("step-name");
  var stepBar = document.getElementById("step-bar");
  var status = document.getElementById("save-status");
  var ajaxUrl = form.getAttribute("action").replace("formsubmit.co/", "formsubmit.co/ajax/");
  var SKIP = { _honey: 1, _subject: 1, _next: 1, _template: 1, _captcha: 1, agreed_to_terms: 1 };
  var current = 0;

  form.classList.add("is-stepped");

  function show(index, focus) {
    current = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach(function (step, n) {
      step.hidden = n !== current;
    });
    stepCount.textContent = "Step " + (current + 1) + " of " + steps.length;
    stepName.textContent = steps[current].getAttribute("data-step-name");
    stepBar.style.width = ((current + 1) / steps.length) * 100 + "%";
    if (focus) {
      document.getElementById("start-progress").scrollIntoView({ behavior: "smooth", block: "start" });
      steps[current].focus({ preventScroll: true });
    }
  }

  function errorBox(el) {
    var box = el.closest(".field");
    return box ? box.querySelector(".field-error") : null;
  }

  function setError(el, msg) {
    var box = errorBox(el);
    if (box) box.textContent = msg;
    if (el.type !== "radio" && el.type !== "checkbox") {
      el.setAttribute("aria-invalid", msg ? "true" : "false");
    }
    return !msg;
  }

  function phoneDigits(value) {
    var digits = value.replace(/\D/g, "");
    return digits.length === 11 && digits.charAt(0) === "1" ? digits.slice(1) : digits;
  }

  function checkField(el) {
    var value = (el.value || "").trim();

    if (el.type === "file") {
      var total = 0;
      form.querySelectorAll('input[type="file"]').forEach(function (input) {
        Array.prototype.forEach.call(input.files || [], function (f) {
          total += f.size;
        });
      });
      return setError(el, total > MAX_UPLOAD ? "Your uploads add up to more than 10 MB. Pick fewer, or text them to me later." : "");
    }
    if (el.type === "radio") {
      var picked = form.querySelector('input[name="' + el.name + '"]:checked');
      return setError(el, el.required && !picked ? "Please pick one." : "");
    }
    if (el.type === "checkbox") {
      return setError(el, el.required && !el.checked ? "Please check this box to continue." : "");
    }
    if (el.required && !value) {
      return setError(el, "This one is required.");
    }
    if (value && el.type === "tel" && phoneDigits(value).length !== 10) {
      return setError(el, "Please enter a 10-digit phone number, like 423-555-0123.");
    }
    if (value && el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return setError(el, "Please enter an email like name@example.com.");
    }
    return setError(el, "");
  }

  function checkGroup(group) {
    var ok = !!group.querySelector("input:checked");
    var box = errorBox(group);
    if (box) box.textContent = ok ? "" : "Please pick at least one.";
    return ok;
  }

  function validStep(step) {
    var ok = true;
    var first = null;
    var seenRadio = {};

    step.querySelectorAll("input, textarea").forEach(function (el) {
      if (el.type === "hidden" || el.classList.contains("hp-field")) return;
      if (el.type === "radio") {
        if (seenRadio[el.name]) return;
        seenRadio[el.name] = true;
      }
      if (el.type === "checkbox" && el.closest("[data-required-group]")) return;
      if (!checkField(el)) {
        ok = false;
        first = first || el;
      }
    });

    step.querySelectorAll("[data-required-group]").forEach(function (group) {
      if (!checkGroup(group)) {
        ok = false;
        first = first || group.querySelector("input");
      }
    });

    if (first) {
      first.focus();
      first.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    return ok;
  }

  function collect() {
    var data = {};
    form.querySelectorAll("input, textarea").forEach(function (el) {
      if (!el.name || SKIP[el.name] || el.type === "file" || el.type === "hidden") return;
      if (el.type === "checkbox" || el.type === "radio") {
        if (el.checked) (data[el.name] = data[el.name] || []).push(el.value);
      } else if (el.value) {
        data[el.name] = el.value;
      }
    });
    return data;
  }

  var saveTimer;
  var finished = false;
  function saveDraft() {
    clearTimeout(saveTimer);
    if (finished) return;
    saveTimer = setTimeout(function () {
      try {
        localStorage.setItem(DRAFT, JSON.stringify({ t: Date.now(), step: current, data: collect() }));
        status.textContent = "✓ Your answers are saved on this device.";
      } catch (e) {}
    }, 600);
  }

  function restoreDraft() {
    try {
      var draft = JSON.parse(localStorage.getItem(DRAFT) || "null");
      if (!draft) return 0;
      if (Date.now() - draft.t > DRAFT_MAX_AGE) {
        localStorage.removeItem(DRAFT);
        return 0;
      }
      Object.keys(draft.data).forEach(function (name) {
        var value = draft.data[name];
        form.querySelectorAll('[name="' + name + '"]').forEach(function (el) {
          if (el.type === "checkbox" || el.type === "radio") {
            el.checked = value.indexOf(el.value) !== -1;
            if (el.checked && el.closest(".choice-card")) el.closest(".choice-card").hidden = false;
          } else {
            el.value = value;
          }
        });
      });
      status.textContent = "Welcome back! Your answers were saved.";
      return draft.step || 0;
    } catch (e) {
      return 0;
    }
  }

  function selectPlan(key) {
    var radio = form.querySelector('[data-plan-key="' + key + '"]');
    if (!radio) return;
    radio.closest(".choice-card").hidden = false;
    radio.checked = true;
  }

  function pickedPlan() {
    var radio = form.querySelector('input[name="plan"]:checked');
    return radio ? { key: radio.getAttribute("data-plan-key"), name: radio.value } : { key: "", name: "" };
  }

  function val(name) {
    var el = form.querySelector('[name="' + name + '"]');
    return el ? el.value.trim() : "";
  }

  function sendStartedLead() {
    var plan = pickedPlan();
    var flag = "sw_started_" + val("email");
    try {
      if (sessionStorage.getItem(flag)) return;
      sessionStorage.setItem(flag, "1");
    } catch (e) {}

    var data = new FormData();
    data.append("_subject", "Started a website order (not finished yet): " + (val("business") || val("name")));
    data.append("_template", "table");
    data.append("plan", plan.name);
    ["name", "business", "phone", "email"].forEach(function (name) {
      data.append(name, val(name));
    });
    data.append("contact_by", (collect().contact_by || []).join(", "));
    data.append("note", "They finished step 2 of 4. If you don't get a full order soon, reach out.");
    fetch(ajaxUrl, { method: "POST", body: data, headers: { Accept: "application/json" } }).catch(function () {});
  }

  function finish(plan) {
    finished = true;
    clearTimeout(saveTimer);
    try {
      localStorage.removeItem(DRAFT);
    } catch (e) {}
    form.hidden = true;
    document.getElementById("start-progress").hidden = true;
    var pay = document.getElementById("pay-step");
    pay.hidden = false;
    fillPay(plan.key, readSession());
    pay.scrollIntoView({ behavior: "smooth", block: "start" });
    document.getElementById("pay-title").focus({ preventScroll: true });
  }

  form.addEventListener("click", function (event) {
    if (event.target.closest("[data-next]")) {
      if (!validStep(steps[current])) return;
      if (current === 1) sendStartedLead();
      show(current + 1, true);
      saveDraft();
    } else if (event.target.closest("[data-back]")) {
      show(current - 1, true);
    }
  });

  form.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" || event.target.tagName === "TEXTAREA" || event.target.tagName === "BUTTON") return;
    if (current < steps.length - 1) {
      event.preventDefault();
      steps[current].querySelector("[data-next]").click();
    }
  });

  form.addEventListener("input", saveDraft);
  form.addEventListener("change", function (event) {
    var el = event.target;
    if (el.closest("[data-required-group]")) checkGroup(el.closest("[data-required-group]"));
    else if (el.type === "radio" || el.type === "checkbox" || el.type === "file") checkField(el);
    saveDraft();
  });
  form.addEventListener("focusout", function (event) {
    var el = event.target;
    if ((el.tagName === "INPUT" || el.tagName === "TEXTAREA") && el.type !== "radio" && el.type !== "checkbox" && el.type !== "file") {
      if (el.value || el.getAttribute("aria-invalid") === "true") checkField(el);
    }
  });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden" && !finished) {
      clearTimeout(saveTimer);
      try {
        localStorage.setItem(DRAFT, JSON.stringify({ t: Date.now(), step: current, data: collect() }));
      } catch (e) {}
    }
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!validStep(steps[current])) return;

    var plan = pickedPlan();
    var button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    button.textContent = "Saving your answers…";

    form.querySelector('[name="_subject"]').value = "New website order (" + plan.name + "): " + (val("business") || val("name"));
    form.querySelector('[name="_next"]').value = location.origin + "/pay?plan=" + encodeURIComponent(plan.key);
    try {
      sessionStorage.setItem(SESSION, JSON.stringify({ plan: plan.key, name: val("name"), email: val("email") }));
    } catch (e) {}

    fetch(ajaxUrl, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (response) {
        if (!response.ok) throw new Error("send failed");
        return response.json();
      })
      .then(function (result) {
        if (String(result.success) !== "true") throw new Error("send failed");
        finish(plan);
      })
      .catch(function () {
        HTMLFormElement.prototype.submit.call(form);
      });
  });

  var startAt = restoreDraft();
  if (params.get("plan")) selectPlan(params.get("plan"));
  if (startAt > 0 && !pickedPlan().key) startAt = 0;
  show(startAt, false);
})();
