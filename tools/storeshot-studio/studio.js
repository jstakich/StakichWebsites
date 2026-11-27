"use strict";

// Older cached pages still reference this URL. Send them to the matching editor markup.
const editorPage = new URL("index.html", document.baseURI);
editorPage.searchParams.set("release", "editor6");
editorPage.searchParams.set("fresh", Date.now());
editorPage.hash = window.location.hash || "#editor";
if (new URL(window.location.href).searchParams.get("release") !== "editor6") {
  window.location.replace(editorPage.href);
} else {
  const status = document.getElementById("editor-loading");
  if (status) status.textContent = "An older copy of the editor is cached. Open StoreShot Studio in a new browser tab.";
}
