(function () {
  var params = new URLSearchParams(location.search);

  function toast(text) {
    var el = document.querySelector(".p-toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "p-toast";
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

  document.querySelectorAll("[data-toast]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      toast(btn.getAttribute("data-toast"));
    });
  });

  // Mobile menu
  var menuBtn = document.querySelector(".p-menu-btn");
  var menu = document.getElementById("p-mnav");
  if (menuBtn && menu) {
    var openHtml = menuBtn.innerHTML;
    var closeHtml = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18" /><line x1="18" y1="6" x2="6" y2="18" /></svg><span>Close</span>';
    menuBtn.addEventListener("click", function () {
      var opening = menu.hasAttribute("hidden");
      if (opening) menu.removeAttribute("hidden");
      else menu.setAttribute("hidden", "");
      menuBtn.setAttribute("aria-expanded", opening ? "true" : "false");
      menuBtn.setAttribute("aria-label", opening ? "Close menu" : "Open menu");
      menuBtn.innerHTML = opening ? closeHtml : openHtml;
    });
  }

  // Preselect a service from ?service=
  var wanted = params.get("service");
  if (wanted) {
    document.querySelectorAll("select[data-preselect]").forEach(function (sel) {
      for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === wanted) sel.selectedIndex = i;
      }
    });
  }
  var notes = params.get("notes");
  if (notes) {
    var box = document.querySelector('textarea[name="notes"]');
    if (box) box.value = notes;
  }

  // Photo previews
  document.querySelectorAll("input[type=file][data-preview]").forEach(function (input) {
    var out = document.getElementById(input.getAttribute("data-preview"));
    input.addEventListener("change", function () {
      out.innerHTML = "";
      Array.prototype.slice.call(input.files, 0, 6).forEach(function (file) {
        if (!/^image\//.test(file.type)) return;
        var im = document.createElement("img");
        im.src = URL.createObjectURL(file);
        im.alt = file.name;
        out.appendChild(im);
      });
    });
  });

  // Booking: days and times
  var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  document.querySelectorAll(".p-book").forEach(function (form) {
    var dates = form.querySelector(".p-dates");
    var times = form.querySelector(".p-times");
    var dayInput = form.querySelector('input[name="day"]');
    var timeInput = form.querySelector('input[name="time"]');
    var count = parseInt(dates.getAttribute("data-days"), 10) || 12;
    var closed = (dates.getAttribute("data-closed") || "0").split(",").filter(Boolean);
    var shortDay = dates.getAttribute("data-short") || "";
    var shortAfter = parseInt(dates.getAttribute("data-short-after"), 10) || 12;
    var d = new Date();
    d.setHours(12, 0, 0, 0);
    var made = 0;
    while (made < count) {
      d.setDate(d.getDate() + 1);
      if (closed.indexOf(String(d.getDay())) !== -1) continue;
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("data-day", d.getDay());
      b.setAttribute("data-label", DAYS[d.getDay()] + ", " + MONTHS[d.getMonth()] + " " + d.getDate());
      b.innerHTML = "<small>" + DAYS[d.getDay()] + "</small><b>" + d.getDate() + "</b><small>" + MONTHS[d.getMonth()] + "</small>";
      dates.appendChild(b);
      made++;
    }

    function pick(group, btn) {
      group.querySelectorAll("button").forEach(function (x) {
        x.classList.remove("is-picked");
        x.setAttribute("aria-pressed", "false");
      });
      if (btn) {
        btn.classList.add("is-picked");
        btn.setAttribute("aria-pressed", "true");
      }
    }

    function refreshTimes(dayBtn) {
      var short = shortDay !== "" && dayBtn.getAttribute("data-day") === shortDay;
      times.querySelectorAll("button").forEach(function (t, i) {
        var m = /(\d+):\d+\s*(AM|PM)/.exec(t.getAttribute("data-time"));
        var hour = m ? (parseInt(m[1], 10) % 12) + (m[2] === "PM" ? 12 : 0) : 0;
        var taken = short && hour >= shortAfter;
        t.disabled = taken;
        if (taken && t.classList.contains("is-picked")) {
          pick(times, null);
          timeInput.value = "";
        }
      });
    }

    dates.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      pick(dates, btn);
      dayInput.value = btn.getAttribute("data-label");
      dates.closest("fieldset").classList.remove("is-bad");
      refreshTimes(btn);
    });
    times.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn || btn.disabled) return;
      pick(times, btn);
      timeInput.value = btn.getAttribute("data-time");
      times.closest("fieldset").classList.remove("is-bad");
    });
  });

  // Forms: check, then show a confirmation
  function labelFor(form, field) {
    if (field.getAttribute("data-need")) return field.getAttribute("data-need");
    var lab = field.id && form.querySelector('label[for="' + field.id + '"]');
    return (lab ? lab.textContent : field.getAttribute("aria-label") || field.name).toLowerCase();
  }

  document.querySelectorAll("form.p-form").forEach(function (form) {
    var msg = form.querySelector(".d-form-msg");
    var confirmBox = form.nextElementSibling;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var missing = [];
      var first = null;
      form.querySelectorAll("[required]").forEach(function (f) {
        var bad = !f.value.trim();
        if (!bad && f.type === "tel") bad = f.value.replace(/\D/g, "").length < 10;
        f.classList.toggle("is-bad", bad);
        if (f.type === "hidden") f.closest("fieldset").classList.toggle("is-bad", bad);
        if (bad) {
          missing.push(labelFor(form, f));
          if (!first && f.type !== "hidden") first = f;
        }
      });
      var email = form.querySelector('input[type="email"]');
      if (email && email.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)) {
        missing.push("a valid email");
        email.classList.add("is-bad");
        first = first || email;
      }
      if (missing.length) {
        msg.textContent = "Please add " + missing.join(", ") + ".";
        msg.classList.add("is-error");
        if (first) first.focus();
        return;
      }
      msg.textContent = "";
      msg.classList.remove("is-error");

      var list = document.createElement("ul");
      var seen = {};
      form.querySelectorAll("[data-sum]").forEach(function (f) {
        if ((f.type === "radio" || f.type === "checkbox") && !f.checked) return;
        var label = f.getAttribute("data-sum");
        if (seen[label] || !f.value.trim()) return;
        seen[label] = true;
        var li = document.createElement("li");
        var b = document.createElement("b");
        b.textContent = label + ": ";
        li.appendChild(b);
        li.appendChild(document.createTextNode(f.value.trim()));
        list.appendChild(li);
      });
      var photos = form.querySelector("input[type=file]");
      if (photos && photos.files.length) {
        var li2 = document.createElement("li");
        li2.innerHTML = "<b>Photos: </b>" + photos.files.length + " attached";
        list.appendChild(li2);
      }

      var booking = form.getAttribute("data-kind") === "booking";
      confirmBox.innerHTML =
        '<div class="p-confirm-ico">✓</div><h3></h3><p class="p-confirm-lead"></p>' +
        '<p class="p-confirm-demo">This is an example website, so nothing was actually sent. On your real site, this goes straight to your phone and email.</p>' +
        '<button type="button" class="d-btn d-btn-brand">Send another</button>';
      confirmBox.querySelector("h3").textContent = form.getAttribute("data-done");
      confirmBox.querySelector(".p-confirm-lead").textContent = booking
        ? "We'll text you shortly to confirm your appointment."
        : "We'll get back to you soon, usually the same day.";
      confirmBox.insertBefore(list, confirmBox.querySelector(".p-confirm-demo"));
      confirmBox.querySelector("button").addEventListener("click", function () {
        form.reset();
        form.querySelectorAll(".is-picked").forEach(function (x) {
          x.classList.remove("is-picked");
        });
        form.querySelectorAll('input[type="hidden"]').forEach(function (x) {
          x.value = "";
        });
        var pv = form.querySelector(".p-preview");
        if (pv) pv.innerHTML = "";
        confirmBox.hidden = true;
        form.hidden = false;
        form.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      form.hidden = true;
      confirmBox.hidden = false;
      confirmBox.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    form.addEventListener("input", function (e) {
      e.target.classList.remove("is-bad");
    });
  });

  // Price estimate
  document.querySelectorAll("[data-est]").forEach(function (est) {
    var total = est.querySelector("[data-est-total]");
    var countEl = est.querySelector("[data-est-count]");
    var lines = est.querySelector("[data-est-lines]");
    var bookLink = est.querySelector("[data-est-book]");
    var textLink = est.querySelector("[data-est-text]");
    var bookBase = bookLink.getAttribute("href");
    var smsBase = textLink.getAttribute("href");

    var unit = est.getAttribute("data-unit") || "service";
    var emptyText = countEl.textContent;

    function round5(n) {
      return Math.round(n / 5) * 5;
    }
    function money(n) {
      return "$" + n.toLocaleString("en-US");
    }

    function update() {
      var veh = est.querySelector('input[name="veh"]:checked');
      var mult = parseFloat(veh.value);
      var lo = 0;
      var hi = 0;
      var picked = [];
      lines.innerHTML = "";
      est.querySelectorAll('input[type="checkbox"]:checked').forEach(function (c) {
        var l = round5(parseFloat(c.getAttribute("data-low")) * mult);
        var h = round5(parseFloat(c.getAttribute("data-high")) * mult);
        lo += l;
        hi += h;
        picked.push(c);
        var li = document.createElement("li");
        var name = document.createElement("span");
        name.textContent = c.getAttribute("data-name");
        var price = document.createElement("b");
        price.textContent = money(l) + "–" + money(h);
        li.appendChild(name);
        li.appendChild(price);
        lines.appendChild(li);
      });
      if (!picked.length) {
        total.textContent = "$0";
        countEl.textContent = emptyText;
        bookLink.setAttribute("href", bookBase);
        textLink.setAttribute("href", smsBase);
        est.classList.remove("has-items");
        return;
      }
      est.classList.add("has-items");
      total.textContent = money(lo) + "–" + money(hi);
      countEl.textContent = picked.length + " " + unit + (picked.length === 1 ? "" : "s") + " · " + veh.getAttribute("data-name");
      var names = picked.map(function (c) {
        return c.getAttribute("data-name");
      });
      var summary = "Estimate (" + veh.getAttribute("data-name") + "): " + names.join(", ") + " = " + money(lo) + "–" + money(hi);
      bookLink.setAttribute(
        "href",
        bookBase + "?service=" + encodeURIComponent(picked[0].getAttribute("data-book")) + "&notes=" + encodeURIComponent(summary)
      );
      textLink.setAttribute("href", smsBase + "?&body=" + encodeURIComponent("Hi! I'd like to book. " + summary));
    }

    est.addEventListener("change", update);
    update();
  });

  // FAQ search
  var search = document.querySelector("[data-faq-search]");
  if (search) {
    var empty = document.querySelector(".p-faq-empty");
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var any = false;
      document.querySelectorAll(".p-faq-group").forEach(function (g) {
        var groupHit = false;
        g.querySelectorAll("details").forEach(function (d) {
          var hit = !q || d.textContent.toLowerCase().indexOf(q) !== -1;
          d.hidden = !hit;
          if (hit && q) d.open = true;
          if (!q) d.open = false;
          groupHit = groupHit || hit;
        });
        g.hidden = !groupHit;
        any = any || groupHit;
      });
      empty.hidden = any;
    });
  }
})();
