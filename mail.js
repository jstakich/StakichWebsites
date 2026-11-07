(function () {
  var forms = document.querySelectorAll("form[data-mail]");
  if (!forms.length) return;

  forms.forEach(function (form) {
    var url = form.getAttribute("data-mail-api");
    if (!url) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (form.reportValidity && !form.reportValidity()) return;
      var button = form.querySelector('button[type="submit"]');
      if (!button || button.disabled) return;
      button.disabled = true;
      var old = button.textContent;
      button.textContent = "Sending...";
      var note = form.querySelector("[data-mail-error]");
      if (!note) {
        note = document.createElement("p");
        note.className = "field-error";
        note.setAttribute("data-mail-error", "");
        note.setAttribute("role", "alert");
        button.insertAdjacentElement("afterend", note);
      }
      note.textContent = "";
      var fields = {};
      var honey = "";
      new FormData(form).forEach(function (value, key) {
        if (typeof value !== "string" || !value.trim()) return;
        if (key === "_honey") honey = value.trim();
        if (key.charAt(0) === "_") return;
        fields[key] = value.trim();
      });
      var subjectEl = form.querySelector('[name="_subject"]');
      var nextEl = form.querySelector('[name="_next"]');
      var payload = {
        type: "order",
        subject: subjectEl ? subjectEl.value : "Website form",
        replyTo: fields.email || "",
        honey: honey,
        customerCopy: false,
        fields: fields
      };
      function postOnce() {
        var ctrl = new AbortController();
        var timer = setTimeout(function () { ctrl.abort(); }, 20000);
        return fetch(url, {
          method: "POST",
          body: JSON.stringify(payload),
          signal: ctrl.signal
        }).then(function (response) {
          clearTimeout(timer);
          return response.json();
        }).then(function (result) {
          if (!result || result.ok !== true) throw new Error("send failed");
        }).catch(function (err) {
          clearTimeout(timer);
          throw err;
        });
      }
      function trySend(left) {
        return postOnce().catch(function () {
          if (left <= 1) throw new Error("send failed");
          return new Promise(function (resolve) { setTimeout(resolve, 4000); }).then(function () {
            return trySend(left - 1);
          });
        });
      }
      trySend(3).then(function () {
        if (nextEl && nextEl.value) window.location.href = nextEl.value;
        else button.textContent = "Sent";
      }).catch(function () {
        button.disabled = false;
        button.textContent = old;
        note.textContent = "That didn't send. Text or call (423) 227-7681 and I'll take it from here.";
      });
    });
  });
})();
