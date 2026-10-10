(function () {
  var ICONS = {
    facebook:
      '<path fill="currentColor" d="M14 8h2.5V4.8c-.4-.1-1.5-.2-2.8-.2-2.8 0-4.7 1.7-4.7 4.8V12H7v3.5h2V22h3.5v-6.5H15l.5-3.5h-3V10c0-1 .3-1.9 1.5-1.9z"/>',
    x: '<path fill="currentColor" d="M17.8 3h3.1l-6.8 7.8L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.3-8.3L2 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/>',
    linkedin:
      '<path fill="currentColor" d="M5 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM3.3 9h3.4v11.5H3.3zM9 9h3.3v1.6c.5-.9 1.7-1.9 3.5-1.9 3.6 0 4.3 2.4 4.3 5.4v6.4h-3.4v-5.7c0-1.4 0-3.1-1.9-3.1s-2.2 1.5-2.2 3v5.8H9z"/>',
    text:
      '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M4 5h16v11H9l-5 4z"/>',
    email:
      '<rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 7l9 6 9-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    share:
      '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M12 3v11M8 7l4-4 4 4M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/>',
    copy:
      '<rect x="9" y="9" width="11" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M5 15V5a2 2 0 0 1 2-2h9"/>',
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

  function build(mount) {
    var url = mount.getAttribute("data-share-url") || pageUrl();
    var title = mount.getAttribute("data-share-title") || pageTitle();
    var label = mount.getAttribute("data-share-label") || "Share this page";
    var u = encodeURIComponent(url);
    var t = encodeURIComponent(title);

    var links = [
      ["facebook", "Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + u],
      ["x", "X", "https://twitter.com/intent/tweet?url=" + u + "&text=" + t],
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
