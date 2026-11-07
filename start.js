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

    var q = new URLSearchParams();
    if (saved.email) q.set("prefilled_email", saved.email);
    if (saved.ref) q.set("client_reference_id", saved.ref);
    payBtn.style.display = "";
    payBtn.textContent = "Pay " + money(today) + " Securely";
    payBtn.href = plan.link + (q.toString() ? "?" + q.toString() : "");
    payBtn.removeAttribute("aria-disabled");
  }

  function refId(text) {
    var raw = (text || "order").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
    if (!raw) raw = "order";
    return (raw + "-" + Date.now().toString(36)).slice(0, 200);
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
  var mailUrl = form.getAttribute("data-mail-api");
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
      var box = steps[current].querySelector("input:not([type='hidden']):not([type='radio']):not([type='checkbox']):not([type='file']), textarea");
      if (box) box.focus({ preventScroll: true });
      else steps[current].focus({ preventScroll: true });
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

    if (el.type === "tel") {
      var digits = phoneDigits(value);
      if (digits.length === 10) {
        var pretty = digits.slice(0, 3) + "-" + digits.slice(3, 6) + "-" + digits.slice(6);
        if (el.value !== pretty) el.value = pretty;
        value = pretty;
      }
    }
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
      if (!el.name || SKIP[el.name] || el.type === "file") return;
      if (el.type === "hidden" && el.name !== "business_hours") return;
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
    if (!value) {
      if (!businessBase()) return "Type a name you like, like yourbusiness.com.";
      if (domainIdeas && !domainIdeas.hidden && domainIdeas.querySelector("button")) return "Tap one of the free names below, or type a name you like.";
      return "Tap one of the free names below, or type a name you like.";
    }
    var d = cleanDomain(value);
    if (!d) return "Please type a name like yourbusiness.com.";
    if (domainStatus[d] === "taken") return "That name is taken. Tap one of the free names below.";
    return "";
  }

  function rdapUrl(d) {
    if (/\.com$/.test(d)) return "https://rdap.verisign.com/com/v1/domain/" + encodeURIComponent(d);
    if (/\.net$/.test(d)) return "https://rdap.verisign.com/net/v1/domain/" + encodeURIComponent(d);
    return "https://rdap.org/domain/" + encodeURIComponent(d);
  }

  function lookupDomain(d) {
    if (domainCache[d]) return domainCache[d];
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 2500);
    var direct = rdapUrl(d).indexOf("verisign.com") >= 0;
    var pending = fetch(rdapUrl(d), { signal: ctrl.signal })
      .then(function (r) {
        // A direct Verisign 404 means the name is free. rdap.org also returns 404 for endings it can't check, so those count only after a registry redirect.
        var result = r.status === 404 && (direct || r.redirected) ? "free" : r.ok ? "taken" : "unknown";
        if (result === "unknown") delete domainCache[d];
        else domainStatus[d] = result;
        return result;
      })
      .catch(function () {
        delete domainCache[d];
        return "unknown";
      })
      .then(function (result) {
        clearTimeout(timer);
        return result;
      });
    domainCache[d] = pending;
    return pending;
  }

  function slugWords(value) {
    return value.toLowerCase().replace(/&/g, " and ").replace(/['\u2019]/g, "").split(/[^a-z0-9]+/).filter(Boolean);
  }

  function areaParts() {
    var raw = val("service_area");
    var bits = raw.split(",");
    var cityWords;
    var state = "";
    if (bits.length > 1) {
      cityWords = slugWords(bits[0]);
      var found = (bits[1] || "").match(/([a-z]{2})/i);
      state = found ? found[1].toLowerCase() : "";
    } else {
      cityWords = slugWords(raw);
      var last = cityWords[cityWords.length - 1] || "";
      if (last.length === 2) {
        state = last;
        cityWords = cityWords.slice(0, -1);
      }
    }
    return {
      city: cityWords.join(""),
      state: state,
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
      ? [base, base + a.state, a.type && base.indexOf(a.type) < 0 ? a.type + a.city : "", base + "co"]
      : [base, base + a.city, a.city + base, base + a.state, a.type && base.indexOf(a.type) < 0 ? base + a.type : "", base + "co"];
    var more = [base + "services", base.length <= 16 ? "the" + base : "", "call" + base, "my" + base, base + "online", base + "hq", base + a.state];
    var seen = {};
    function clean(names) {
      var list = [];
      names.forEach(function (n) {
        if (!n || n.length < 3 || n.length > 26 || seen[n] || !/^[a-z0-9]+$/.test(n)) return;
        seen[n] = 1;
        list.push(n + ".com");
      });
      return list;
    }
    var firstList = clean(first);
    if (base.length >= 3 && base.length <= 26) firstList.push(base + ".net");
    return [firstList, clean(more)];
  }

  var ideaGen = 0;
  var ideasWait = Promise.resolve();
  var domainWait = Promise.resolve();

  function hideDomainIdeas() {
    ideaGen++;
    ideasFor = "";
    if (domainIdeas) domainIdeas.hidden = true;
  }

  function markPicked() {
    if (!domainIdeas || !domainInput) return;
    var currentName = cleanDomain(domainInput.value);
    domainIdeas.querySelectorAll("[data-domain-idea]").forEach(function (b) {
      var on = b.getAttribute("data-domain-idea") === currentName;
      b.classList.toggle("is-picked", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function paintIdeas(free, done, note, box) {
    free = free.slice(0, 3);
    var have = Array.prototype.map.call(box.querySelectorAll("[data-domain-idea]"), function (b) {
      return b.getAttribute("data-domain-idea");
    }).join(",");
    if (have !== free.join(",")) {
      box.innerHTML = "";
      free.forEach(function (d) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "domain-idea";
        b.textContent = d;
        b.setAttribute("data-domain-idea", d);
        box.appendChild(b);
      });
    }
    markPicked();
    if (free.length >= 3) note.textContent = "These 3 names are free. Tap one.";
    else if (!done) note.textContent = "Finding 3 free names…";
    else if (!free.length) note.textContent = "Type a name you like in the box and I'll check it.";
    else note.textContent = "Tap a free name, or type your own.";
  }

  function watchFree(list, onUpdate) {
    var state = list.map(function () { return "wait"; });
    return Promise.all(list.map(function (d, i) {
      return lookupDomain(d).then(function (result) {
        state[i] = result;
        var free = [];
        for (var n = 0; n < state.length; n++) {
          if (state[n] === "wait") break;
          if (state[n] === "free") free.push(list[n]);
          if (free.length >= 3) break;
        }
        onUpdate(free, state.indexOf("wait") === -1);
      });
    }));
  }

  function showDomainIdeas(base) {
    if (!domainIdeas) return;
    var lists = domainCandidates(base);
    if (!lists[0].length) return hideDomainIdeas();
    var key = lists[0].join(",") + "|" + lists[1].join(",");
    var box = domainIdeas.querySelector(".domain-idea-list");
    if (key === ideasFor && !domainIdeas.hidden && box.querySelector("button")) return;
    ideasFor = key;
    var gen = ++ideaGen;
    var note = domainIdeas.querySelector("p");
    box.innerHTML = "";
    note.textContent = "Finding 3 free names…";
    domainIdeas.hidden = false;
    var firstShown = [];
    ideasWait = watchFree(lists[0], function (free, done) {
      if (gen !== ideaGen) return;
      firstShown = free.slice(0, 3);
      paintIdeas(firstShown, done && !lists[1].length, note, box);
    }).then(function () {
      if (gen !== ideaGen || firstShown.length >= 3 || !lists[1].length) return;
      return watchFree(lists[1], function (extra, done) {
        if (gen !== ideaGen) return;
        paintIdeas(firstShown.concat(extra), done, note, box);
      });
    }).catch(function () {});
  }

  function warmDomains() {
    var lists = domainCandidates(businessBase());
    lists[0].forEach(lookupDomain);
  }

  function checkDomain() {
    if (!domainInput || !domainCheck) return;
    clearTimeout(domainTimer);
    domainAsked = "";
    var picked = form.querySelector('input[name="domain"]:checked');
    var raw = domainInput.value.trim();
    var d = cleanDomain(raw);
    if (picked && picked.value === "Yes, I have one") {
      setDomainCheck("", "");
      hideDomainIdeas();
      domainWait = Promise.resolve();
      return;
    }
    if (!d) {
      setDomainCheck(picked && !raw ? "" : "", "");
      if (picked && !raw && businessBase()) showDomainIdeas(businessBase());
      else if (picked && !raw) setDomainCheck("Type a name you like, like yourbusiness.com.", "");
      else hideDomainIdeas();
      domainWait = Promise.resolve();
      return;
    }
    if (domainStatus[d] === "free") {
      setDomainCheck(d + " looks available!", "free");
      markPicked();
      domainWait = Promise.resolve();
      return;
    }
    if (domainStatus[d] === "taken") {
      setDomainCheck(d + " is taken.", "taken");
      showDomainIdeas(d.split(".")[0]);
      domainWait = Promise.resolve();
      return;
    }
    domainWait = new Promise(function (resolve) {
      domainTimer = setTimeout(function () {
        domainAsked = d;
        setDomainCheck("Checking " + d + "…", "");
        lookupDomain(d).then(function (result) {
          if (domainAsked !== d) return resolve();
          var err = errorBox(domainInput);
          if (err && err.textContent) checkField(domainInput);
          if (result === "free") {
            setDomainCheck(d + " looks available!", "free");
            hideDomainIdeas();
          } else if (result === "taken") {
            setDomainCheck(d + " is taken.", "taken");
            showDomainIdeas(d.split(".")[0]);
          } else {
            setDomainCheck("I couldn't check that name just now. You can still use it.", "");
            hideDomainIdeas();
          }
          resolve();
        });
      }, 250);
    });
  }

  function whenDomainReady(fn) {
    Promise.race([
      Promise.all([domainWait, ideasWait]).catch(function () {}),
      new Promise(function (resolve) { setTimeout(resolve, 2500); })
    ]).then(fn);
  }

  function pickedPlan() {
    var radio = form.querySelector('input[name="plan"]:checked');
    return radio ? { key: radio.getAttribute("data-plan-key"), name: radio.value } : { key: "", name: "" };
  }

  function val(name) {
    var el = form.querySelector('[name="' + name + '"]');
    return el ? el.value.trim() : "";
  }

  function orderData(includeFiles) {
    var data = new FormData(form);
    data.delete("_next");
    ["logo", "photos", "price_list"].forEach(function (name) {
      var input = form.querySelector('[name="' + name + '"]');
      if (!includeFiles || !input || !input.files || !input.files.length) data.delete(name);
    });
    var email = val("email");
    if (email) data.set("_replyto", email);
    return data;
  }

  var OUTBOX = "stakich-order-outbox";

  function readOutbox() {
    try {
      var items = JSON.parse(localStorage.getItem(OUTBOX) || "[]");
      if (!Array.isArray(items)) return [];
      var kept = items.filter(function (item) {
        return item && item.payload && Date.now() - (item.created || item.at || 0) < 2 * 24 * 60 * 60 * 1000;
      });
      if (kept.length !== items.length) writeOutbox(kept);
      return kept;
    } catch (e) {
      return [];
    }
  }

  function writeOutbox(items) {
    try {
      localStorage.setItem(OUTBOX, JSON.stringify(items.slice(-6)));
    } catch (e) {}
  }

  function remember(payload) {
    var copy = {
      type: "order",
      subject: payload.subject,
      replyTo: payload.replyTo || "",
      honey: payload.honey || "",
      customerCopy: !!payload.customerCopy,
      fields: payload.fields || {},
      files: []
    };
    var items = readOutbox();
    items.push({
      id: String(Date.now()) + Math.random().toString(16).slice(2),
      created: Date.now(),
      at: Date.now(),
      payload: copy
    });
    writeOutbox(items);
  }

  function postPayload(payload) {
    if (!mailUrl) return Promise.reject(new Error("send failed"));
    var body = JSON.stringify(payload);
    var hasFiles = payload.files && payload.files.length;
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, hasFiles ? 30000 : 20000);
    var opts = { method: "POST", body: body, signal: ctrl.signal };
    if (!hasFiles && body.length < 60000) opts.keepalive = true;
    return fetch(mailUrl, opts).then(function (response) {
      clearTimeout(timer);
      return response.json();
    }).then(function (result) {
      if (!result || result.ok !== true) throw new Error("send failed");
    }).catch(function (err) {
      clearTimeout(timer);
      throw err;
    });
  }

  var flushing = false;
  function flushOutbox() {
    if (flushing) return;
    var due = readOutbox().filter(function (item) { return Date.now() - item.at >= 15000; });
    if (!due.length) return;
    flushing = true;
    var item = due[0];
    postPayload(item.payload).then(function () {
      writeOutbox(readOutbox().filter(function (row) { return row.id !== item.id; }));
      flushing = false;
      flushOutbox();
    }).catch(function () {
      var rows = readOutbox();
      rows.forEach(function (row) {
        if (row.id === item.id) row.at = Date.now();
      });
      writeOutbox(rows);
      flushing = false;
    });
  }

  function shrinkFile(file) {
    if (!/^image\//.test(file.type) || file.type === "image/svg+xml" || file.size <= 900000) {
      return Promise.resolve(file);
    }
    return new Promise(function (resolve) {
      var img = new Image();
      var url = URL.createObjectURL(file);
      img.onload = function () {
        URL.revokeObjectURL(url);
        var edge = Math.max(img.width, img.height) || 1;
        var scale = Math.min(1, 1600 / edge);
        var canvas = document.createElement("canvas");
        canvas.width = Math.max(1, Math.round(img.width * scale));
        canvas.height = Math.max(1, Math.round(img.height * scale));
        canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height);
        function atQuality(quality) {
          canvas.toBlob(function (blob) {
            if (!blob) { resolve(file); return; }
            if (blob.size > 900000 && quality > 0.4) { atQuality(Math.round((quality - 0.15) * 100) / 100); return; }
            var base = String(file.name || "photo").replace(/\.[^.]+$/, "") || "photo";
            resolve(new File([blob], base + ".jpg", { type: "image/jpeg" }));
          }, "image/jpeg", quality);
        }
        atQuality(0.72);
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        resolve(file);
      };
      img.src = url;
    });
  }

  function readFiles(includeFiles) {
    if (!includeFiles) return Promise.resolve([]);
    var picked = [];
    ["logo", "photos", "price_list"].forEach(function (name) {
      var input = form.querySelector('[name="' + name + '"]');
      if (!input || !input.files) return;
      Array.prototype.forEach.call(input.files, function (file) { picked.push(file); });
    });
    return Promise.all(picked.slice(0, 4).map(shrinkFile)).then(function (shrunk) {
      var used = 0;
      return Promise.all(shrunk.map(function (file) {
        if (!file || file.size > 1200000 || used + file.size > 4000000) return null;
        used += file.size;
        return new Promise(function (resolve) {
          var reader = new FileReader();
          reader.onload = function () {
            var raw = String(reader.result || "");
            var comma = raw.indexOf(",");
            resolve({
              name: file.name,
              type: file.type || "application/octet-stream",
              data: comma >= 0 ? raw.slice(comma + 1) : ""
            });
          };
          reader.onerror = function () { resolve(null); };
          reader.readAsDataURL(file);
        });
      })).then(function (list) {
        return list.filter(function (file) { return file && file.data; });
      });
    });
  }

  function payloadFrom(data, files, customerCopy) {
    var fields = {};
    data.forEach(function (value, key) {
      if (typeof value !== "string" || !value.trim() || key.charAt(0) === "_") return;
      fields[key] = value.trim();
    });
    return {
      type: "order",
      subject: data.get("_subject") || "Order form",
      replyTo: data.get("_replyto") || "",
      honey: data.get("_honey") || "",
      customerCopy: !!customerCopy,
      fields: fields,
      files: files || []
    };
  }

  function postMail(data, includeFiles, customerCopy) {
    return readFiles(includeFiles).then(function (files) {
      if (includeFiles && !files.length) {
        data.set("note", "They finished the photo section. No files were attached. Ask them for their logo and photos. They have not paid yet.");
      }
      var payload = payloadFrom(data, files, customerCopy);
      return postPayload(payload).catch(function () {
        if (!files.length) throw new Error("send failed");
        data.set("note", "They finished the photo section. The files did not attach. Ask them for their logo and photos. They have not paid yet.");
        return postPayload(payloadFrom(data, [], customerCopy));
      });
    });
  }

  function sendSection(stepIndex, readyToPay) {
    var step = steps[stepIndex];
    var section = step.getAttribute("data-step-name") || ("Step " + (stepIndex + 1));
    var who = val("business") || val("name") || pickedPlan().name || "New lead";
    var includeFiles = step.getAttribute("data-send-files") === "yes" && !readyToPay;
    var subject = readyToPay
      ? "Order form, complete: " + who + " (every answer, no photos)"
      : "Order form, step " + (stepIndex + 1) + " of " + steps.length + " (" + section + "): " + who;
    if (val("preview_link")) subject += " — FROM PREVIEW";
    var note = readyToPay
      ? "They finished the form. This email has every answer and no photo files. If the photo email has nothing attached, ask them for their logo and photos. The payment page is next. They have not paid yet."
      : (includeFiles
        ? "They finished the photo section. Photos are attached here. They have not paid yet."
        : "They finished this section. They have not paid yet.");
    function once(withFiles) {
      var data = orderData(withFiles);
      data.set("_subject", subject);
      data.set("section_finished", section);
      data.set("note", note);
      return postMail(data, withFiles, !!readyToPay);
    }
    return once(includeFiles).catch(function () {
      var data = orderData(false);
      data.set("_subject", subject);
      data.set("section_finished", section);
      data.set("note", note);
      remember(payloadFrom(data, [], !!readyToPay));
    });
  }

  function saveNow() {
    try {
      localStorage.setItem(DRAFT, JSON.stringify({ t: Date.now(), step: current, data: collect() }));
    } catch (e) {}
  }

  function finish(plan) {
    finished = true;
    clearTimeout(saveTimer);
    var saved = readSession();
    var session = {
      plan: plan.key,
      name: val("name") || saved.name || "",
      email: val("email") || saved.email || "",
      business: val("business") || saved.business || "",
      ref: saved.ref || refId(val("business") || val("name")),
      ready: 1
    };
    try {
      sessionStorage.setItem(SESSION, JSON.stringify(session));
    } catch (e) {}
    form.hidden = true;
    document.getElementById("start-progress").hidden = true;
    var pay = document.getElementById("pay-step");
    pay.hidden = false;
    fillPay(plan.key, session);
    pay.scrollIntoView({ behavior: "smooth", block: "start" });
    document.getElementById("pay-title").focus({ preventScroll: true });
  }

  var moving = false;
  form.addEventListener("click", function (event) {
    var idea = event.target.closest("[data-domain-idea]");
    if (idea) {
      domainInput.value = idea.getAttribute("data-domain-idea");
      domainStatus[domainInput.value] = "free";
      setDomainCheck(domainInput.value + " looks available!", "free");
      markPicked();
      checkField(domainInput);
      saveDraft();
    } else if (event.target.closest("[data-next]")) {
      if (moving) return;
      moving = true;
      whenDomainReady(function () {
        moving = false;
        if (!validStep(steps[current])) return;
        sendSection(current, false);
        if (current === 2) warmDomains();
        show(current + 1, true);
        if (domainInput && steps[current].contains(domainInput)) checkDomain();
        saveDraft();
      });
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

  var warmTimer;
  form.addEventListener("input", function (event) {
    if (event.target === domainInput) checkDomain();
    if (event.target.name === "business" || event.target.name === "business_type" || event.target.name === "service_area") {
      clearTimeout(warmTimer);
      warmTimer = setTimeout(warmDomains, 400);
    }
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
    whenDomainReady(function () {
      if (!validStep(steps[current])) return;
      var plan = pickedPlan();
      var button = form.querySelector('button[type="submit"]');
      if (button.disabled) return;
      button.disabled = true;
      var saved = readSession();
      var session = {
        plan: plan.key,
        name: val("name"),
        email: val("email"),
        business: val("business"),
        ref: saved.ref || refId(val("business") || val("name")),
        ready: 0
      };
      var refBox = form.querySelector('[name="order_ref"]');
      if (refBox) refBox.value = session.ref;
      try {
        sessionStorage.setItem(SESSION, JSON.stringify(session));
      } catch (e) {}
      var stepIndex = current;
      saveNow();
      finish(plan);
      sendSection(stepIndex, true).catch(function () {
        setTimeout(function () { sendSection(stepIndex, false); }, 5000);
      });
    });
  });

  function setupHours() {
    var root = document.getElementById("hours-field");
    if (!root) return;
    var hidden = document.getElementById("s-hours");
    var summary = document.getElementById("hours-summary");
    var DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    var appointment = false;
    var dash = "\u2013";

    function dayBtn(name) {
      return root.querySelector('[data-day="' + name + '"]');
    }
    function row(name) {
      return root.querySelector('[data-day-row="' + name + '"]');
    }
    function timeSel(name, which) {
      return root.querySelector("[data-" + which + '="' + name + '"]');
    }
    function dayOn(name) {
      var b = dayBtn(name);
      return !!(b && b.classList.contains("is-on"));
    }
    function setDay(name, on) {
      var b = dayBtn(name);
      var r = row(name);
      if (!b) return;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (r) r.classList.toggle("is-on", on);
    }
    function setTime(name, which, value) {
      var sel = timeSel(name, which);
      if (!sel) return;
      if ([].some.call(sel.options, function (o) { return o.text === value || o.value === value; })) sel.value = value;
    }
    function timeValue(name, which) {
      var sel = timeSel(name, which);
      return sel ? sel.value : "";
    }
    function dayNames(dayPart) {
      var names = [];
      if (dayPart === "Every day") return DAYS.slice();
      dayPart.split(", ").forEach(function (chunk) {
        if (chunk.indexOf(dash) >= 0) {
          var ab = chunk.split(dash);
          var a = DAYS.indexOf(ab[0]);
          var b = DAYS.indexOf(ab[1]);
          if (a >= 0 && b >= a) for (var n = a; n <= b; n++) names.push(DAYS[n]);
        } else if (DAYS.indexOf(chunk) >= 0) names.push(chunk);
      });
      return names;
    }
    function sentence() {
      if (appointment) return "By appointment";
      var groups = [];
      DAYS.forEach(function (d, i) {
        if (!dayOn(d)) return;
        var open = timeValue(d, "open");
        var close = timeValue(d, "close");
        var last = groups[groups.length - 1];
        if (last && last.open === open && last.close === close) {
          last.days.push(d);
          last.end = i;
          last.consecutive = last.consecutive && i === last.prev + 1;
          last.prev = i;
        } else {
          groups.push({ days: [d], start: i, end: i, prev: i, consecutive: true, open: open, close: close });
        }
      });
      if (!groups.length) return "";
      return groups.map(function (g) {
        var label = g.days.length === 7 ? "Every day" : (g.consecutive && g.days.length > 1 ? DAYS[g.start] + dash + DAYS[g.end] : g.days.join(", "));
        return label + ", " + g.open + dash + g.close;
      }).join("; ");
    }
    function paint(fromUser) {
      var text = sentence();
      hidden.value = text;
      summary.textContent = text ? "Hours: " + text : "No hours yet. Turn on the days you are open.";
      root.querySelectorAll("[data-preset-value]").forEach(function (b) {
        b.classList.toggle("is-on", b.getAttribute("data-preset-value") === text);
      });
      if (fromUser) saveDraft();
    }
    function readSaved(value) {
      if (value === "By appointment") {
        appointment = true;
        DAYS.forEach(function (d) { setDay(d, false); });
        paint(false);
        return;
      }
      appointment = false;
      DAYS.forEach(function (d) { setDay(d, false); });
      value.split("; ").forEach(function (part) {
        var bits = part.split(", ");
        var times = bits[bits.length - 1] || "";
        if (times.indexOf(dash) < 0) return;
        var pair = times.split(dash);
        dayNames(bits.slice(0, -1).join(", ")).forEach(function (d) {
          setDay(d, true);
          setTime(d, "open", pair[0]);
          setTime(d, "close", pair[1]);
        });
      });
      paint(false);
    }
    root.addEventListener("click", function (event) {
      var preset = event.target.closest("[data-preset-value]");
      var day = event.target.closest("[data-day]");
      if (preset) {
        readSaved(preset.getAttribute("data-preset-value"));
        saveDraft();
      } else if (day) {
        appointment = false;
        setDay(day.getAttribute("data-day"), !day.classList.contains("is-on"));
        paint(true);
      }
    });
    root.addEventListener("change", function (event) {
      var open = event.target.getAttribute("data-open");
      var close = event.target.getAttribute("data-close");
      var name = open || close;
      if (!name) return;
      appointment = false;
      setDay(name, true);
      paint(true);
    });
    if (hidden.value) readSaved(hidden.value);
    else paint(false);
  }

  var startAt = restoreDraft();
  if (params.get("plan")) selectPlan(params.get("plan"));
  var preview = (params.get("preview") || "").replace(/[^a-z0-9-]/g, "");
  if (preview) {
    var usePreview = form.querySelector('input[name="use_preview"]');
    if (usePreview) usePreview.checked = true;
    var previewLink = form.querySelector('[name="preview_link"]');
    if (previewLink) previewLink.value = location.origin + "/preview/" + preview;
    var more = document.getElementById("more-details");
    if (more) more.open = true;
  }
  showPlanExtras();
  showDomainExtras();
  showUploadExtras();
  checkDomain();
  setupHours();
  if (startAt > 0 && !pickedPlan().key) startAt = 0;
  var editBtn = document.getElementById("edit-answers");
  if (editBtn) {
    editBtn.addEventListener("click", function () {
      finished = false;
      form.hidden = false;
      document.getElementById("start-progress").hidden = false;
      document.getElementById("pay-step").hidden = true;
      show(steps.length - 1, true);
    });
  }
  if (readSession().ready && pickedPlan().key) finish(pickedPlan());
  else show(startAt, false);
  setInterval(flushOutbox, 15000);
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") flushOutbox();
  });
})();
