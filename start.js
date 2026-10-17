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
        if (input.disabled) return;
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
    if (el === domainInput) {
      return setError(el, domainError(value));
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

  function showPlanExtras() {
    var key = pickedPlan().key;
    form.querySelectorAll("[data-plans]").forEach(function (box) {
      box.hidden = (" " + box.getAttribute("data-plans") + " ").indexOf(" " + key + " ") < 0;
    });
  }

  function showDomainExtras() {
    var picked = form.querySelector('input[name="domain"]:checked');
    var has = !!picked && picked.value === "Yes, I have one";
    form.querySelectorAll("[data-domain-extra]").forEach(function (box) {
      box.hidden = !has;
    });
  }

  function toggleUpload(sel, on) {
    form.querySelectorAll(sel).forEach(function (box) {
      box.hidden = !on;
      var input = box.querySelector('input[type="file"]');
      if (!input) return;
      input.disabled = !on;
      if (!on) setError(input, "");
    });
  }

  function showUploadExtras() {
    var logo = form.querySelector('input[name="has_logo"]:checked');
    var photos = form.querySelector('input[name="has_photos"]:checked');
    toggleUpload("[data-logo-upload]", !!(logo && logo.value === "Yes"));
    toggleUpload("[data-photo-upload]", !!(photos && photos.value !== "No"));
  }

  var domainInput = form.querySelector('[name="domain_wanted"]');
  var domainCheck = document.getElementById("domain-check");
  var domainTimer;
  var domainAsked = "";

  function cleanDomain(value) {
    var d = value.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/^www\./, "").split(/[\/?#]/)[0].replace(/\s+/g, "");
    if (d && d.indexOf(".") < 0) d += ".com";
    return /^[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(d) ? d : "";
  }

  function setDomainCheck(text, kind) {
    domainCheck.textContent = text;
    domainCheck.className = "domain-check" + (kind ? " is-" + kind : "");
  }

  var domainIdeas = document.getElementById("domain-ideas");
  var domainCache = {};
  var domainStatus = {};
  var ideasFor = "";
  var LEGAL_WORDS = { llc: 1, inc: 1, corp: 1, ltd: 1, company: 1 };

  function hasDomainAlready() {
    var picked = form.querySelector('input[name="domain"]:checked');
    return !!picked && picked.value === "Yes, I have one";
  }

  function domainError(value) {
    if (hasDomainAlready()) {
      if (!value) return "Please type your web address.";
      return cleanDomain(value) ? "" : "Please type it like yourbusiness.com.";
    }
    if (!value) return "Tap one of the free names below, or type a name you like.";
    var d = cleanDomain(value);
    if (!d) return "Please type a name like yourbusiness.com.";
    if (domainStatus[d] === "taken") return "That name is taken. Tap one of the free names below.";
    return "";
  }

  function lookupDomain(d) {
    if (!domainCache[d]) {
      domainCache[d] = fetch("https://rdap.org/domain/" + encodeURIComponent(d))
        .then(function (r) {
          // rdap.org answers 404 itself for endings it can't look up; only a registry's 404 means free.
          var result = r.status === 404 && r.redirected ? "free" : r.ok ? "taken" : "unknown";
          domainStatus[d] = result;
          return result;
        })
        .catch(function () {
          delete domainCache[d];
          return "unknown";
        });
    }
    return domainCache[d];
  }

  function slugWords(value) {
    return value.toLowerCase().replace(/&/g, " and ").replace(/['\u2019]/g, "").split(/[^a-z0-9]+/).filter(Boolean);
  }

  function areaParts() {
    var area = val("service_area").split(",");
    var state = (area[1] || "").match(/^\s*([a-z]{2})\b/i);
    return {
      city: slugWords(area[0] || "").join(""),
      state: state ? state[1].toLowerCase() : "",
      type: slugWords(val("business_type").split(/[,/]/)[0] || "").join(""),
    };
  }

  function businessBase() {
    var words = slugWords(val("business")).filter(function (w) {
      return !LEGAL_WORDS[w];
    });
    if (words[0] === "the" && words.length > 1) words.shift();
    if (words.length) return words.join("");
    var a = areaParts();
    return a.city && a.type ? a.city + a.type : "";
  }

  function domainCandidates(base) {
    if (!base) return [[], []];
    var a = areaParts();
    var hasCity = !!a.city && base.indexOf(a.city) >= 0;
    var first = hasCity
      ? [base, base + a.state, a.type + a.city, "the" + base, base + "pros", base + "co"]
      : [base, base + a.state, base + a.city, a.city + base, base.indexOf(a.type) < 0 ? base + a.type : "", base + a.city + a.state, "the" + base, base + "co"];
    var more = [base + "services", base + "llc", base + a.state + "llc", "call" + base, "my" + base, base + "online", base + "hq", base + "team", base + "now"];
    var seen = {};
    function clean(names) {
      var list = [];
      names.forEach(function (n) {
        if (n.length < 3 || n.length > 40 || seen[n] || !/^[a-z0-9]+$/.test(n)) return;
        seen[n] = 1;
        list.push(n + ".com");
      });
      return list;
    }
    var firstList = clean(first);
    firstList.push(base + ".net");
    return [firstList, clean(more)];
  }

  function freeOnes(list) {
    return Promise.all(list.map(lookupDomain)).then(function (results) {
      return list.filter(function (d, i) {
        return results[i] === "free";
      });
    });
  }

  function hideDomainIdeas() {
    ideasFor = "";
    if (domainIdeas) domainIdeas.hidden = true;
  }

  function showDomainIdeas(base) {
    if (!domainIdeas) return;
    var lists = domainCandidates(base);
    if (!lists[0].length) return hideDomainIdeas();
    var key = lists[0].join(",");
    if (key === ideasFor) return;
    ideasFor = key;
    var note = domainIdeas.querySelector("p");
    var box = domainIdeas.querySelector(".domain-idea-list");
    box.innerHTML = "";
    note.textContent = "Finding free names for you…";
    domainIdeas.hidden = false;
    freeOnes(lists[0]).then(function (free) {
      if (free.length >= 3 || !lists[1].length) return free;
      return freeOnes(lists[1]).then(function (extra) {
        return free.concat(extra);
      });
    }).then(function (free) {
      if (ideasFor !== key) return;
      free = free.slice(0, 3);
      if (!free.length) {
        note.textContent = "Type a name you like in the box above and I'll check it.";
        return;
      }
      note.textContent = "These names are free. Tap one to use it:";
      free.forEach(function (d) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "domain-idea";
        b.textContent = d;
        b.setAttribute("data-domain-idea", d);
        box.appendChild(b);
      });
    });
  }

  function checkDomain() {
    if (!domainInput || !domainCheck) return;
    clearTimeout(domainTimer);
    domainAsked = "";
    var picked = form.querySelector('input[name="domain"]:checked');
    var d = cleanDomain(domainInput.value);
    if (picked && picked.value === "Yes, I have one") {
      setDomainCheck("", "");
      hideDomainIdeas();
      return;
    }
    if (!d) {
      setDomainCheck("", "");
      if (picked && !domainInput.value.trim()) showDomainIdeas(businessBase());
      else hideDomainIdeas();
      return;
    }
    domainTimer = setTimeout(function () {
      domainAsked = d;
      setDomainCheck("Checking " + d + "…", "");
      lookupDomain(d).then(function (result) {
        if (domainAsked !== d) return;
        var err = errorBox(domainInput);
        if (err && err.textContent) checkField(domainInput);
        if (result === "free") {
          setDomainCheck(d + " looks available!", "free");
          hideDomainIdeas();
        } else if (result === "taken") {
          setDomainCheck(d + " is taken.", "taken");
          showDomainIdeas(d.split(".")[0]);
        } else {
          setDomainCheck("", "");
          hideDomainIdeas();
        }
      });
    }, 700);
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
    var idea = event.target.closest("[data-domain-idea]");
    if (idea) {
      domainInput.value = idea.getAttribute("data-domain-idea");
      hideDomainIdeas();
      checkField(domainInput);
      checkDomain();
      saveDraft();
    } else if (event.target.closest("[data-next]")) {
      if (!validStep(steps[current])) return;
      if (current === 1) sendStartedLead();
      show(current + 1, true);
      if (domainInput && steps[current].contains(domainInput)) checkDomain();
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

  form.addEventListener("input", function (event) {
    if (event.target === domainInput) checkDomain();
    saveDraft();
  });
  form.addEventListener("change", function (event) {
    var el = event.target;
    if (el.closest("[data-required-group]")) checkGroup(el.closest("[data-required-group]"));
    else if (el.type === "radio" || el.type === "checkbox" || el.type === "file") checkField(el);
    if (el.name === "plan") showPlanExtras();
    if (el.name === "has_logo" || el.name === "has_photos") showUploadExtras();
    if (el.name === "domain") {
      showDomainExtras();
      checkDomain();
    }
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

    form.querySelector('[name="_subject"]').value = "New website order (" + plan.name + "): " + (val("business") || val("name")) + (val("preview_link") ? " — FROM PREVIEW" : "");
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
  var preview = (params.get("preview") || "").replace(/[^a-z0-9-]/g, "");
  if (preview) {
    var usePreview = form.querySelector('input[name="use_preview"]');
    if (usePreview) usePreview.checked = true;
    var previewLink = form.querySelector('[name="preview_link"]');
    if (previewLink) previewLink.value = location.origin + "/preview/" + preview + "/";
  }
  showPlanExtras();
  showDomainExtras();
  showUploadExtras();
  checkDomain();
  if (startAt > 0 && !pickedPlan().key) startAt = 0;
  show(startAt, false);
})();
