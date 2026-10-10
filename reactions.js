(function () {
  var mounts = document.querySelectorAll("[data-rx]");
  if (!mounts.length) return;
  var API = mounts[0].getAttribute("data-rx-api");
  if (!API) return;

  var TYPES = [
    { id: "like", emoji: "👍", label: "Like", color: "#1877f2" },
    { id: "love", emoji: "❤️", label: "Love", color: "#f33e58" },
    { id: "care", emoji: "🥰", label: "Care", color: "#f7b125" },
    { id: "haha", emoji: "😆", label: "Haha", color: "#f7b125" },
    { id: "wow", emoji: "😮", label: "Wow", color: "#f7b125" },
  ];
  var byId = {};
  TYPES.forEach(function (t) {
    byId[t.id] = t;
  });

  var state = {};

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function mine(key) {
    try {
      return localStorage.getItem("rx:" + key) || "";
    } catch (e) {
      return "";
    }
  }

  function setMine(key, val) {
    try {
      if (val) localStorage.setItem("rx:" + key, val);
      else localStorage.removeItem("rx:" + key);
    } catch (e) {}
  }

  function ago(iso) {
    var s = Math.max(1, (Date.now() - new Date(iso).getTime()) / 1000);
    if (s < 60) return "Just now";
    var units = [
      [31536000, "y"],
      [604800, "w"],
      [86400, "d"],
      [3600, "h"],
      [60, "m"],
    ];
    for (var i = 0; i < units.length; i++) {
      if (s >= units[i][0]) return Math.floor(s / units[i][0]) + units[i][1];
    }
    return "Just now";
  }

  function post(payload) {
    return fetch(API, { method: "POST", body: JSON.stringify(payload) }).then(function (r) {
      return r.json();
    });
  }

  function merge(data) {
    Object.keys(data.counts || {}).forEach(function (k) {
      state[k] = state[k] || { counts: {}, comments: [] };
      state[k].counts = data.counts[k];
      if (data.comments && data.comments[k]) state[k].comments = data.comments[k];
      var my = mine(k);
      if (my && !(data.counts[k][my] > 0)) setMine(k, "");
    });
  }

  function total(key) {
    var c = (state[key] && state[key].counts) || {};
    return TYPES.reduce(function (n, t) {
      return n + (c[t.id] || 0);
    }, 0);
  }

  function renderAll() {
    mounts.forEach(render);
  }

  function render(m) {
    var key = m.getAttribute("data-rx");
    var s = state[key] || { counts: {}, comments: [] };
    var my = mine(key);

    var icons = m.querySelector(".rx-icons");
    icons.innerHTML = "";
    TYPES.filter(function (t) {
      return (s.counts[t.id] || 0) > 0;
    })
      .sort(function (a, b) {
        return (s.counts[b.id] || 0) - (s.counts[a.id] || 0);
      })
      .slice(0, 3)
      .forEach(function (t) {
        var i = el("span", "rx-ico", t.emoji);
        i.title = t.label + ": " + s.counts[t.id];
        icons.appendChild(i);
      });
    var n = total(key);
    var count = m.querySelector(".rx-count");
    if (!n) count.textContent = m.classList.contains("rx-full") ? "Be the first to react" : "";
    else if (my) count.textContent = n === 1 ? "You" : "You and " + (n - 1) + (n - 1 === 1 ? " other" : " others");
    else count.textContent = String(n);

    var likeBtn = m.querySelector(".rx-like");
    var t = byId[my];
    likeBtn.querySelector(".rx-like-ico").textContent = t ? t.emoji : "👍";
    likeBtn.querySelector(".rx-like-text").textContent = t ? t.label : "Like";
    likeBtn.style.color = t ? t.color : "";
    likeBtn.setAttribute("aria-pressed", t ? "true" : "false");

    var cc = m.querySelector(".rx-ccount");
    if (cc) {
      var k = s.comments.length;
      cc.textContent = k ? k + (k === 1 ? " comment" : " comments") : "";
      var list = m.querySelector(".rx-list");
      list.innerHTML = "";
      s.comments.forEach(function (c) {
        var item = el("div", "rx-item");
        item.appendChild(el("span", "rx-avatar", (c.name || "?").charAt(0).toUpperCase()));
        var body = el("div", "rx-bubble");
        body.appendChild(el("b", null, c.name));
        body.appendChild(el("p", null, c.text));
        var wrap = el("div");
        wrap.appendChild(body);
        wrap.appendChild(el("small", "rx-time", ago(c.time)));
        item.appendChild(wrap);
        list.appendChild(item);
      });
    }
  }

  function choose(key, id) {
    var old = mine(key);
    var next = old === id ? "" : id;
    state[key] = state[key] || { counts: {}, comments: [] };
    var c = state[key].counts;
    if (old) c[old] = Math.max(0, (c[old] || 0) - 1);
    if (next) c[next] = (c[next] || 0) + 1;
    setMine(key, next);
    renderAll();
    post({ type: "react", key: key, add: next, remove: old })
      .then(function (d) {
        merge(d);
        renderAll();
      })
      .catch(function () {});
  }

  function build(m) {
    var key = m.getAttribute("data-rx");
    var full = m.classList.contains("rx-full");

    var summary = el("div", "rx-summary");
    var left = el("span", "rx-left");
    left.appendChild(el("span", "rx-icons"));
    left.appendChild(el("span", "rx-count"));
    summary.appendChild(left);
    if (full) {
      var cc = el("button", "rx-ccount");
      cc.type = "button";
      summary.appendChild(cc);
    }

    var actions = el("div", "rx-actions");
    var likeWrap = el("div", "rx-like-wrap");
    var like = el("button", "rx-btn rx-like");
    like.type = "button";
    like.appendChild(el("span", "rx-like-ico", "👍"));
    like.appendChild(el("span", "rx-like-text", "Like"));
    var picker = el("div", "rx-picker");
    picker.setAttribute("role", "group");
    picker.setAttribute("aria-label", "Reactions");
    TYPES.forEach(function (t) {
      var b = el("button", "rx-pick", t.emoji);
      b.type = "button";
      b.title = t.label;
      b.setAttribute("aria-label", t.label);
      b.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        likeWrap.classList.remove("is-open");
        choose(key, t.id);
      });
      picker.appendChild(b);
    });
    likeWrap.appendChild(picker);
    likeWrap.appendChild(like);
    actions.appendChild(likeWrap);

    var hoverTimer;
    var pressTimer;
    var longPressed = false;
    likeWrap.addEventListener("mouseenter", function () {
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () {
        likeWrap.classList.add("is-open");
      }, 450);
    });
    likeWrap.addEventListener("mouseleave", function () {
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () {
        likeWrap.classList.remove("is-open");
      }, 300);
    });
    like.addEventListener(
      "touchstart",
      function () {
        longPressed = false;
        pressTimer = setTimeout(function () {
          longPressed = true;
          likeWrap.classList.add("is-open");
        }, 450);
      },
      { passive: true }
    );
    like.addEventListener("touchend", function (e) {
      clearTimeout(pressTimer);
      if (longPressed) e.preventDefault();
    });
    like.addEventListener("touchmove", function () {
      clearTimeout(pressTimer);
    });
    like.addEventListener("contextmenu", function (e) {
      e.preventDefault();
    });
    like.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (longPressed) {
        longPressed = false;
        return;
      }
      clearTimeout(hoverTimer);
      likeWrap.classList.remove("is-open");
      choose(key, mine(key) ? mine(key) : "like");
    });
    document.addEventListener("click", function (e) {
      if (!likeWrap.contains(e.target)) likeWrap.classList.remove("is-open");
    });

    var box;
    if (full) {
      var cbtn = el("button", "rx-btn rx-cbtn");
      cbtn.type = "button";
      cbtn.appendChild(el("span", null, "💬"));
      cbtn.appendChild(el("span", null, "Comment"));
      actions.appendChild(cbtn);

      var sbtn = el("button", "rx-btn rx-sbtn");
      sbtn.type = "button";
      sbtn.appendChild(el("span", null, "↗"));
      sbtn.appendChild(el("span", "rx-stext", "Share"));
      sbtn.addEventListener("click", function () {
        var data = { title: document.title, url: location.href.split("#")[0] };
        if (navigator.share) {
          navigator.share(data).catch(function () {});
        } else if (navigator.clipboard) {
          navigator.clipboard.writeText(data.url).then(function () {
            sbtn.querySelector(".rx-stext").textContent = "Link copied";
            setTimeout(function () {
              sbtn.querySelector(".rx-stext").textContent = "Share";
            }, 2000);
          });
        }
      });
      actions.appendChild(sbtn);

      box = el("div", "rx-box");
      var form = el("form", "rx-form");
      form.noValidate = true;
      form.innerHTML =
        '<input class="rx-name" name="name" maxlength="40" placeholder="Your name" autocomplete="name" aria-label="Your name" />' +
        '<div class="rx-write"><textarea name="text" maxlength="600" rows="2" placeholder="Write a comment…" aria-label="Write a comment"></textarea>' +
        '<button type="submit" class="rx-send" aria-label="Post comment">➤</button></div>' +
        '<input class="rx-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" />' +
        '<p class="rx-msg" aria-live="polite"></p>';
      box.appendChild(form);
      box.appendChild(el("div", "rx-list"));
      var nameIn = form.querySelector(".rx-name");
      var textIn = form.querySelector("textarea");
      var hpIn = form.querySelector(".rx-hp");

      try {
        localStorage.removeItem("rx:name");
      } catch (e) {}

      function openBox() {
        textIn.focus();
      }
      cbtn.addEventListener("click", openBox);
      cc.addEventListener("click", openBox);

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var msg = form.querySelector(".rx-msg");
        var name = nameIn.value.trim();
        var text = textIn.value.trim();
        if (!name) {
          msg.textContent = "Please add your name.";
          nameIn.focus();
          return;
        }
        if (text.length < 2) {
          msg.textContent = "Please write a comment.";
          textIn.focus();
          return;
        }
        msg.textContent = "Posting…";
        form.classList.add("is-busy");
        post({ type: "comment", key: key, name: name, text: text, website: hpIn.value })
          .then(function (d) {
            form.classList.remove("is-busy");
            if (!d.ok) {
              msg.textContent = d.error || "Something went wrong. Please try again.";
              return;
            }
            msg.textContent = "Thanks! Your comment is posted.";
            textIn.value = "";
            merge(d);
            renderAll();
          })
          .catch(function () {
            form.classList.remove("is-busy");
            msg.textContent = "Couldn't post right now. Please try again.";
          });
      });
    }

    m.appendChild(summary);
    m.appendChild(actions);
    if (box) m.appendChild(box);
  }

  mounts.forEach(build);
  var keys = Array.prototype.map
    .call(mounts, function (m) {
      return m.getAttribute("data-rx");
    })
    .filter(function (k, i, a) {
      return a.indexOf(k) === i;
    });
  renderAll();
  mounts.forEach(function (m) {
    m.classList.add("is-ready");
  });
  fetch(API + "?keys=" + encodeURIComponent(keys.join(",")))
    .then(function (r) {
      return r.json();
    })
    .then(function (d) {
      merge(d);
      renderAll();
    })
    .catch(function () {});
})();
