(function () {
  var STROKE = ' fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
  var ICONS = {
    facebook:
      '<path fill="currentColor" d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/>',
    x: '<path fill="currentColor" d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/>',
    linkedin:
      '<path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>',
    text:
      '<path fill="currentColor" d="M12 2.5C6.2 2.5 1.5 6.4 1.5 11.2c0 2.7 1.5 5.1 3.8 6.7-.2 1.5-.9 2.9-2 3.9 2.1.1 4.1-.6 5.6-1.8 1 .3 2 .4 3.1.4 5.8 0 10.5-3.9 10.5-8.7S17.8 2.5 12 2.5z"/>',
    email: '<rect x="2" y="4" width="20" height="16" rx="2"' + STROKE + '/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"' + STROKE + "/>",
    share: '<path d="M12 2v13M16 6l-4-4-4 4M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"' + STROKE + "/>",
    qr:
      '<rect x="3" y="3" width="5" height="5" rx="1"' + STROKE + '/><rect x="16" y="3" width="5" height="5" rx="1"' + STROKE + '/><rect x="3" y="16" width="5" height="5" rx="1"' + STROKE + '/><path d="M21 16h-3a2 2 0 0 0-2 2v3M21 21v.01M12 7v3a2 2 0 0 1-2 2H7M3 12h.01M12 3h.01M12 16v.01M16 12h1M21 12v.01M12 21v-1"' + STROKE + "/>",
    copy:
      '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"' + STROKE + '/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"' + STROKE + "/>",
  };

  function icon(name) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + ICONS[name] + "</svg>";
  }

  function pageUrl() {
    var canonical = document.querySelector('link[rel="canonical"]');
    return (canonical && canonical.href) || window.location.href.split("#")[0].split("?")[0];
  }

  function pageTitle() {
    var h1 = document.querySelector("h1");
    return (h1 && h1.textContent.trim()) || document.title;
  }

  function copyText(text, done) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(function () {
        legacyCopy(text, done);
      });
    } else {
      legacyCopy(text, done);
    }
  }

  function legacyCopy(text, done) {
    var input = document.createElement("textarea");
    input.value = text;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.left = "-9999px";
    document.body.appendChild(input);
    input.select();
    try {
      document.execCommand("copy");
      done();
    } catch (e) {
      /* ignore */
    }
    document.body.removeChild(input);
  }

  var QR_IMG = "/assets/qr/stakichwebsites-qr.png";
  var QR_VIDEO = "/assets/qr/stakichwebsites-qr-tiktok.mp4";
  var qrBox = null;
  var qrFiles = null;

  function loadQrFiles() {
    if (qrFiles || typeof File !== "function" || !window.fetch) return;
    qrFiles = {};
    [["video", QR_VIDEO, "stakichwebsites-qr-tiktok.mp4", "video/mp4"], ["image", QR_IMG, "stakichwebsites-qr.png", "image/png"]].forEach(function (f) {
      fetch(f[1])
        .then(function (r) {
          return r.blob();
        })
        .then(function (b) {
          qrFiles[f[0]] = new File([b], f[2], { type: f[3] });
        })
        .catch(function () {});
    });
  }

  function shareFile(kind, fallback) {
    var file = qrFiles && qrFiles[kind];
    if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
      navigator.share({ files: [file], title: "Stakich Websites", text: "Scan to visit stakichwebsites.com" }).catch(function () {});
    } else {
      fallback.click();
    }
  }

  function openQr() {
    if (!qrBox) {
      var css = document.createElement("style");
      css.textContent =
        ".qr-modal{position:fixed;inset:0;z-index:1000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(8,18,36,.72)}" +
        ".qr-modal[hidden]{display:none}" +
        ".qr-card{position:relative;width:min(400px,100%);max-height:calc(100vh - 32px);overflow:auto;background:#fff;color:#0c1c36;border-radius:20px;padding:22px;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.35);font:inherit}" +
        ".qr-card img{display:block;width:100%;max-width:300px;height:auto;margin:0 auto 12px;border-radius:14px}" +
        ".qr-card h2{margin:0 0 4px;font-size:1.25rem}.qr-card p{margin:0 0 14px;font-size:.95rem;color:#3b4a63}" +
        ".qr-actions{display:grid;gap:8px}" +
        ".qr-actions a,.qr-actions button{display:flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:10px 14px;border-radius:12px;border:0;font:inherit;font-weight:700;text-decoration:none;cursor:pointer}" +
        ".qr-main{background:#f29a3b;color:#2a1600}.qr-alt{background:#eef3fa;color:#13294b}" +
        ".qr-tip{margin:12px 0 0!important;font-size:.85rem!important}" +
        ".qr-close{position:absolute;top:8px;right:8px;width:40px;height:40px;border:0;border-radius:50%;background:#eef3fa;color:#13294b;font-size:1.4rem;line-height:1;cursor:pointer}";
      document.head.appendChild(css);
      qrBox = document.createElement("div");
      qrBox.className = "qr-modal";
      qrBox.hidden = true;
      qrBox.setAttribute("role", "dialog");
      qrBox.setAttribute("aria-modal", "true");
      qrBox.setAttribute("aria-label", "QR code for stakichwebsites.com");
      qrBox.innerHTML =
        '<div class="qr-card">' +
        '<button type="button" class="qr-close" aria-label="Close">&times;</button>' +
        "<h2>Scan to visit my website</h2>" +
        "<p>Point a phone camera at the code. It opens stakichwebsites.com, no typing needed.</p>" +
        '<img src="' + QR_IMG + '" alt="QR code that opens stakichwebsites.com" width="1080" height="1350" />' +
        '<div class="qr-actions">' +
        '<button type="button" class="qr-main" data-qr-share="video">Share QR video (TikTok, Reels)</button>' +
        '<button type="button" class="qr-alt" data-qr-share="image">Share QR picture</button>' +
        '<a class="qr-alt" href="' + QR_VIDEO + '" download="stakichwebsites-qr-tiktok.mp4" data-qr-save="video">Save video</a>' +
        '<a class="qr-alt" href="' + QR_IMG + '" download="stakichwebsites-qr.png" data-qr-save="image">Save picture</a>' +
        "</div>" +
        '<p class="qr-tip">To post on TikTok: save the video, open TikTok, tap <b>+</b>, then <b>Upload</b> and pick it.</p>' +
        "</div>";
      document.body.appendChild(qrBox);
      qrBox.addEventListener("click", function (e) {
        if (e.target === qrBox || e.target.closest(".qr-close")) closeQr();
        var btn = e.target.closest("[data-qr-share]");
        if (btn) {
          var kind = btn.getAttribute("data-qr-share");
          shareFile(kind, qrBox.querySelector('[data-qr-save="' + kind + '"]'));
        }
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && !qrBox.hidden) closeQr();
      });
    }
    loadQrFiles();
    qrBox.hidden = false;
    qrBox.querySelector(".qr-close").focus();
  }

  function closeQr() {
    qrBox.hidden = true;
  }

  function build(mount) {
    var url = mount.getAttribute("data-share-url") || pageUrl();
    var title = mount.getAttribute("data-share-title") || pageTitle();
    var label = mount.getAttribute("data-share-label") || "Share this page";
    var u = encodeURIComponent(url);
    var t = encodeURIComponent(title);

    var links = [
      ["facebook", "Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + u],
      ["x", "Post on X", "https://twitter.com/intent/tweet?url=" + u + "&text=" + t],
      ["linkedin", "LinkedIn", "https://www.linkedin.com/sharing/share-offsite/?url=" + u],
      ["text", "Text", "sms:?&body=" + t + "%20" + u],
      ["email", "Email", "mailto:?subject=" + t + "&body=" + t + "%0A%0A" + u],
    ];

    var html = '<p class="share-label">' + label + '</p><div class="share-actions">';
    links.forEach(function (l) {
      var external = l[0] === "text" || l[0] === "email" ? "" : ' target="_blank" rel="noopener noreferrer"';
      html +=
        '<a class="share-btn share-' + l[0] + '" href="' + l[2] + '"' + external + ">" + icon(l[0]) + "<span>" + l[1] + "</span></a>";
    });
    html +=
      '<button type="button" class="share-btn share-native" hidden>' + icon("share") + "<span>Share</span></button>" +
      '<button type="button" class="share-btn share-copy">' + icon("copy") + "<span>Copy link</span></button>" +
      '<button type="button" class="share-btn share-qr">' + icon("qr") + "<span>QR code</span></button>" +
      '</div><p class="share-status" aria-live="polite"></p>';
    mount.innerHTML = html;

    var status = mount.querySelector(".share-status");
    mount.querySelector(".share-copy").addEventListener("click", function () {
      copyText(url, function () {
        status.textContent = "Link copied!";
        setTimeout(function () {
          status.textContent = "";
        }, 2200);
      });
    });

    mount.querySelector(".share-qr").addEventListener("click", openQr);

    var native = mount.querySelector(".share-native");
    if (typeof navigator.share === "function") {
      native.hidden = false;
      native.addEventListener("click", function () {
        navigator.share({ title: title, text: title, url: url }).catch(function () {});
      });
    }
  }

  document.querySelectorAll("[data-share]").forEach(build);
})();
