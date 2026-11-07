(function () {
  var form = document.getElementById("photos-form");
  if (!form) return;
  var mailUrl = form.getAttribute("data-mail-api");
  var status = document.getElementById("photos-status");
  var forLine = document.getElementById("photos-for");
  var businessField = document.getElementById("photos-business-field");
  var businessInput = document.getElementById("photos-business");
  var MAX_FILE = 25 * 1024 * 1024;

  function readBuyer() {
    try {
      var live = JSON.parse(sessionStorage.getItem("sw_start") || "{}");
      if (live && (live.business || live.name || live.email)) return live;
    } catch (e) {}
    try {
      return JSON.parse(localStorage.getItem("sw_buyer") || "{}");
    } catch (e) {
      return {};
    }
  }

  var buyer = readBuyer();
  var knownBusiness = (buyer.business || buyer.name || "").trim();
  if (knownBusiness) {
    forLine.textContent = "These are for " + knownBusiness + ". Skip anything you don't have on this phone.";
  } else if (businessField) {
    businessField.hidden = false;
    if (businessInput) businessInput.required = true;
  }

  function businessName() {
    if (knownBusiness) return knownBusiness;
    return businessInput ? businessInput.value.trim() : "";
  }

  function setStatus(text) {
    if (status) status.textContent = text || "";
  }

  function fileToData(file) {
    return new Promise(function (resolve, reject) {
      var reader = new FileReader();
      reader.onload = function () {
        var raw = String(reader.result || "");
        var comma = raw.indexOf(",");
        resolve(comma >= 0 ? raw.slice(comma + 1) : "");
      };
      reader.onerror = function () { reject(new Error("read")); };
      reader.readAsDataURL(file);
    });
  }

  function post(payload) {
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, 60000);
    return fetch(mailUrl, {
      method: "POST",
      body: JSON.stringify(payload),
      signal: ctrl.signal
    }).then(function (response) {
      clearTimeout(timer);
      return response.json();
    }).then(function (result) {
      if (!result || result.ok !== true) throw new Error((result && result.error) || "send failed");
      return result;
    }).catch(function (err) {
      clearTimeout(timer);
      throw err;
    });
  }

  function pickedFiles() {
    var list = [];
    [
      ["logo", "logo"],
      ["photos", "photo"],
      ["price_list", "price"]
    ].forEach(function (pair) {
      var input = form.querySelector('[name="' + pair[0] + '"]');
      if (!input || !input.files) return;
      Array.prototype.forEach.call(input.files, function (file) {
        list.push({ kind: pair[1], file: file });
      });
    });
    return list;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var business = businessName();
    if (!business) {
      setStatus("Add the business name so the files can be named.");
      if (businessInput) businessInput.focus();
      return;
    }
    var files = pickedFiles();
    if (!files.length) {
      setStatus("Add a logo, a photo, or a price list. Or text them to (423) 227-7681.");
      return;
    }
    var tooBig = files.filter(function (item) { return item.file.size > MAX_FILE; });
    if (tooBig.length) {
      setStatus("One file is over 25 MB. Send that one by text, and keep the others here.");
      return;
    }
    var button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    var honey = (form.querySelector('[name="_honey"]') || {}).value || "";
    var saved = [];
    var failed = [];

    function sendAt(index) {
    if (index >= files.length) {
      if (!saved.length) {
        button.disabled = false;
        setStatus("That didn't send. Text the photos to (423) 227-7681.");
        return;
      }
      return post({
          type: "photos",
          done: true,
          honey: honey,
          business: business,
          plan: buyer.plan || "",
          email: buyer.email || "",
          ref: buyer.ref || ""
        }).then(function () {
          form.hidden = true;
          var done = document.createElement("div");
          done.className = "pay-box";
          done.innerHTML = "<h2>Got them.</h2><p>I'll use these on your website." +
            (failed.length ? " A few did not send. Text those to (423) 227-7681." : "") +
            "</p>";
          form.parentNode.insertBefore(done, form);
        }).catch(function () {
          button.disabled = false;
          setStatus(saved.length
            ? "The files are saved. The email notice did not send. Text me if you don't hear back."
            : "That didn't send. Text the photos to (423) 227-7681.");
        });
      }
      var item = files[index];
      setStatus("Sending " + (index + 1) + " of " + files.length + "…");
      return fileToData(item.file).then(function (data) {
        return post({
          type: "photos",
          honey: honey,
          business: business,
          plan: buyer.plan || "",
          email: buyer.email || "",
          ref: buyer.ref || "",
          kind: item.kind,
          file: {
            name: item.file.name || "photo",
            type: item.file.type || "application/octet-stream",
            data: data
          }
        });
      }).then(function () {
        saved.push(item.file.name);
        return sendAt(index + 1);
      }).catch(function () {
        failed.push(item.file.name);
        return sendAt(index + 1);
      });
    }

    sendAt(0);
  });
})();
