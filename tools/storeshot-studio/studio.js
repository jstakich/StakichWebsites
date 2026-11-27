"use strict";

// Older cached pages still reference this URL. Send them to the matching editor markup.
const editorPage = new URL("index.html", document.baseURI);
editorPage.searchParams.set("release", "editor5");
editorPage.hash = window.location.hash || "#editor";
if (window.location.href !== editorPage.href) {
  window.location.replace(editorPage.href);
} else {
  const status = document.getElementById("editor-loading");
  if (status) status.textContent = "An older copy of the editor is cached. Open StoreShot Studio in a new browser tab.";
}
