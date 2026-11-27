"use strict";
const $ = id => document.getElementById(id);
const sizes = {
  iphone: ["iPhone 6.9 inch", 1320, 2868],
  iphone65: ["iPhone 6.5 inch", 1242, 2688],
  ipad: ["iPad 13 inch", 2064, 2752],
  android: ["Google Play phone", 1080, 1920],
};
const themes = {
  violet: ["Violet", "#302461", "#a66cf4", "#ffffff"],
  coast: ["Coast", "#123c52", "#43aea8", "#ffffff"],
  bloom: ["Bloom", "#ffcfac", "#ed8295", "#321e3b"],
  ink: ["Ink", "#101b38", "#4265b6", "#ffffff"],
  sage: ["Sage", "#e0ead6", "#7ab0a3", "#172e33"],
  plain: ["Solid", "#263a60", "#263a60", "#ffffff"],
};
const fontStack = {sans: "Arial, sans-serif", serif: "Georgia, serif", mono: "monospace"};
const baseStyle = {theme: "violet", background: themes.violet[1], ink: themes.violet[3], font: "sans", align: "center", scale: 100, frame: "dark", fit: "contain"};
const newID = () => crypto.randomUUID();
const makeScreen = (name, headline, subtitle, capture = null) => ({
  id: newID(), name, style: {...baseStyle},
  locales: {"en-US": {headline, subtitle, capture, previous: null}},
});
const makeDemo = () => ({
  screens: [
    makeScreen("Today", "Make time for a reset", "Small moments for a calmer day"),
    makeScreen("Your routine", "Build a routine you’ll keep", "Find a rhythm that works for you"),
    makeScreen("Progress", "See how far you’ve come", "Every small step counts"),
  ],
  locales: ["en-US"], exports: {}, demo: true,
});
let project = makeDemo();
let selected = 0, locale = "en-US", size = "iphone", comparing = false;
let savedTimer, renderVersion = 0, lastThumbnail = [];
let database;
let busy = false;
const images = new WeakMap();

function openStorage() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("storeshot-studio", 1);
    request.onupgradeneeded = () => request.result.createObjectStore("workspace");
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
function readProject(db) {
  return new Promise((resolve, reject) => {
    const request = db.transaction("workspace").objectStore("workspace").get("project");
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
function notice(message) {
  $("status").textContent = message;
}
function persist() {
  if (!database) return;
  clearTimeout(savedTimer);
  savedTimer = setTimeout(() => {
    const transaction = database.transaction("workspace", "readwrite");
    transaction.objectStore("workspace").put(project, "project");
    transaction.onerror = () => notice("This browser couldn’t save the project. Export your screenshots before closing.");
  }, 250);
}

function getCurrent() {
  return project.screens[selected];
}
function getLocale(screen, code = locale) {
  return screen.locales[code];
}
function actualCapture(screen, code = locale) {
  return getLocale(screen, code).capture || getLocale(screen, "en-US").capture;
}
function imageFor(capture) {
  if (!capture) return Promise.resolve(null);
  if (!images.has(capture.blob)) {
    images.set(capture.blob, new Promise((resolve, reject) => {
      const url = URL.createObjectURL(capture.blob);
      const image = new Image();
      image.onload = () => { URL.revokeObjectURL(url); resolve(image); };
      image.onerror = () => { URL.revokeObjectURL(url); reject(new Error("This image could not be opened.")); };
      image.src = url;
    }));
  }
  return images.get(capture.blob);
}

function roundPath(ctx, x, y, w, h, radius) {
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, radius);
}
function fillRound(ctx, x, y, w, h, radius, color) {
  roundPath(ctx, x, y, w, h, radius);
  ctx.fillStyle = color;
  ctx.fill();
}
function fitImage(ctx, image, x, y, w, h, mode) {
  const scale = Math[mode === "cover" ? "max" : "min"](w / image.width, h / image.height);
  const iw = image.width * scale, ih = image.height * scale;
  ctx.drawImage(image, x + (w - iw) / 2, y + (h - ih) / 2, iw, ih);
}
function drawDemo(ctx, x, y, w, h, variant) {
  const u = w / 300;
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(u, u);
  const height = h / u;
  ctx.fillStyle = "#f5f1ff";
  ctx.fillRect(0, 0, 300, height);
  ctx.fillStyle = "#262445";
  ctx.textAlign = "left";
  ctx.font = "700 12px Arial";
  ctx.fillText("9:41", 20, 23);
  ctx.fillText("● ● ▰", 242, 23);
  ctx.fillStyle = "#5f4da2";
  ctx.font = "700 13px Arial";
  ctx.fillText("STILL", 20, 56);
  ctx.fillStyle = "#272343";
  ctx.font = "700 25px Arial";
  ctx.fillText(["Take a breath", "Your routine", "Small steps"][variant % 3], 20, 91);
  const card = ctx.createLinearGradient(20, 120, 280, 310);
  card.addColorStop(0, "#4f3c9d");
  card.addColorStop(1, "#8f71d4");
  fillRound(ctx, 17, 112, 266, 177, 19, card);
  ctx.strokeStyle = "#ffffff75";
  for (const radius of [28, 40, 53]) {
    ctx.beginPath();
    ctx.arc(229, 175, radius, 0, Math.PI * 2);
    ctx.stroke();
  }
  ctx.fillStyle = "white";
  ctx.font = "700 19px Arial";
  ctx.fillText(["A quiet reset", "Evening wind-down", "Your weekly check-in"][variant % 3], 34, 222);
  ctx.font = "13px Arial";
  ctx.fillText("5 minute session", 34, 246);
  ctx.fillStyle = "#272343";
  ctx.font = "700 17px Arial";
  ctx.fillText("Explore", 20, 320);
  for (const [i, label] of ["Clear your mind", "Rest and recharge", "Start fresh"].entries()) {
    const top = 337 + i * 63;
    fillRound(ctx, 17, top, 266, 52, 10, "white");
    fillRound(ctx, 28, top + 9, 34, 34, 8, ["#e9ddfc", "#def1e8", "#ffe7dc"][i]);
    ctx.fillStyle = "#302a50";
    ctx.font = "700 13px Arial";
    ctx.fillText(label, 75, top + 31);
  }
  ctx.restore();
}
function linesFor(ctx, text, width, language) {
  const lines = [];
  const words = typeof Intl.Segmenter === "function"
    ? new Intl.Segmenter(language, {granularity: "word"})
    : null;
  function splitLongWord(word) {
    const glyphs = typeof Intl.Segmenter === "function"
      ? [...new Intl.Segmenter(language).segment(word)].map(part => part.segment)
      : Array.from(word);
    let line = "";
    for (const glyph of glyphs) {
      if (line && ctx.measureText(line + glyph).width > width) {
        lines.push(line);
        line = "";
      }
      line += glyph;
    }
    return line;
  }
  for (const paragraph of text.split("\n")) {
    let line = "";
    const segments = words ? [...words.segment(paragraph)].map(part => part.segment) : paragraph.split(/(\s+)/u);
    for (const segment of segments) {
      if (!line && !segment.trim()) continue;
      if (ctx.measureText((line + segment).trimEnd()).width <= width) {
        line += segment;
        continue;
      }
      if (line.trim()) lines.push(line.trim());
      line = ctx.measureText(segment).width > width ? splitLongWord(segment) : segment.trimStart();
    }
    lines.push(line.trimEnd());
  }
  return lines;
}
function draw(canvas, screen, code, target, image, factor = 1) {
  const [, outW, outH] = sizes[target];
  canvas.width = Math.round(outW * factor);
  canvas.height = Math.round(outH * factor);
  const ctx = canvas.getContext("2d", {alpha: false});
  ctx.scale(canvas.width / outW, canvas.height / outH);
  const style = screen.style, strings = getLocale(screen, code);
  const width = outW, height = outH;
  const gradient = ctx.createLinearGradient(0, height, width, 0);
  gradient.addColorStop(0, style.background);
  gradient.addColorStop(1, style.theme === "plain" ? style.background : themes[style.theme][2]);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);
  if (style.theme !== "plain") {
    ctx.strokeStyle = "#ffffff29";
    ctx.lineWidth = width * .003;
    for (let ring = 0; ring < 5; ring++) {
      ctx.beginPath();
      ctx.ellipse(width * .8, height * .78, width * (.34 + ring * .11), height * .2, -.55, 0, Math.PI * 2);
      ctx.stroke();
    }
  }
  const pad = width * .085;
  const maxWidth = width - pad * 2;
  const textTop = height * .063;
  let textSize = Math.min(width * .087, height * .045) * style.scale / 100;
  const capHeight = height * .257;
  let headline, subtitle, subSize, textHeight;
  const stack = fontStack[style.font];
  for (let attempt = 0; attempt < 18; attempt++) {
    subSize = textSize * .42;
    ctx.font = `700 ${textSize}px ${stack}`;
    headline = strings.headline.trim() ? linesFor(ctx, strings.headline, maxWidth, code) : [];
    ctx.font = `400 ${subSize}px ${stack}`;
    subtitle = strings.subtitle.trim() ? linesFor(ctx, strings.subtitle, maxWidth, code) : [];
    textHeight = headline.length * textSize * 1.12 + subtitle.length * subSize * 1.3
      + (headline.length && subtitle.length ? subSize * .55 : 0);
    if (textHeight <= capHeight || attempt === 17) break;
    textSize *= .94;
  }
  ctx.save();
  ctx.beginPath();
  ctx.rect(0, textTop - textSize * .2, width, capHeight + textSize * .2);
  ctx.clip();
  ctx.fillStyle = style.ink;
  ctx.textBaseline = "top";
  const rtl = new Intl.Locale(code).getTextInfo?.().direction === "rtl" || /^(ar|fa|he|ur|ps|sd)(-|$)/.test(code);
  ctx.direction = rtl ? "rtl" : "ltr";
  ctx.textAlign = style.align === "left" ? (rtl ? "right" : "left") : "center";
  const textX = style.align === "left" ? (rtl ? width - pad : pad) : width / 2;
  let y = textTop;
  ctx.font = `700 ${textSize}px ${stack}`;
  for (const line of headline) {
    ctx.fillText(line, textX, y);
    y += textSize * 1.12;
  }
  if (headline.length && subtitle.length) y += subSize * .55;
  ctx.font = `400 ${subSize}px ${stack}`;
  for (const line of subtitle) {
    ctx.fillText(line, textX, y);
    y += subSize * 1.3;
  }
  ctx.restore();
  const areaTop = Math.max(height * .237, textTop + textHeight + height * .034);
  const aspect = target === "ipad" ? .74 : .48;
  const dh = Math.min(height - areaTop - height * .062, width * .81 / aspect);
  const dw = dh * aspect;
  const dx = (width - dw) / 2, dy = areaTop;
  const bezel = style.frame === "none" ? 0 : dw * .025;
  const rad = dw * .075;
  ctx.save();
  ctx.shadowColor = "#080e2e76";
  ctx.shadowBlur = width * .036;
  ctx.shadowOffsetY = width * .02;
  fillRound(ctx, dx, dy, dw, dh, rad, style.frame === "light" ? "#ebeff6" : "#151c2c");
  ctx.restore();
  ctx.save();
  roundPath(ctx, dx + bezel, dy + bezel, dw - bezel * 2, dh - bezel * 2, Math.max(0, rad - bezel));
  ctx.clip();
  ctx.fillStyle = "#151c2c";
  ctx.fillRect(dx, dy, dw, dh);
  if (image) fitImage(ctx, image, dx + bezel, dy + bezel, dw - bezel * 2, dh - bezel * 2, style.fit);
  else drawDemo(ctx, dx + bezel, dy + bezel, dw - bezel * 2, dh - bezel * 2, Math.max(0, project.screens.findIndex(s => s.id === screen.id)));
  ctx.restore();
  const messages = [];
  if (textHeight > capHeight) messages.push("Some text doesn’t fit. Shorten it or reduce the text size.");
  else if (textSize < Math.min(width * .087, height * .045) * style.scale / 110) messages.push("Text was reduced to fit. Check it at the final size.");
  if (image && style.fit === "cover" && Math.abs(image.width / image.height - (dw - bezel * 2) / (dh - bezel * 2)) > .045) messages.push("Fill frame crops this capture. Choose Show full image to keep its edges.");
  if (image && !strings.capture && code !== "en-US") messages.push("This language is using the English app capture.");
  return messages.join(" ");
}

const languageChoices = [
  "ar", "bn", "bg", "ca", "zh-Hans", "zh-Hant", "cs", "da", "nl", "en-AU", "en-CA", "en-GB",
  "et", "fi", "fr-CA", "fr-FR", "de", "el", "he", "hi", "hr", "hu", "id", "it",
  "ja", "ko", "lv", "lt", "ms", "nb", "fa", "pl", "pt-BR", "pt-PT", "ro", "ru",
  "sk", "sl", "es-ES", "es-MX", "es-US", "sv", "ta", "th", "tr", "uk", "ur", "vi",
];
const languageNames = new Intl.DisplayNames(["en"], {type: "language", languageDisplay: "standard"});
const languageLabel = code => languageNames.of(code) || code;

function makeOption(label, value) {
  return new Option(label, value);
}
function renderList() {
  lastThumbnail.forEach(url => URL.revokeObjectURL(url));
  lastThumbnail = [];
  $("screen-list").replaceChildren(...project.screens.map((screen, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.setAttribute("aria-pressed", String(index === selected));
    const capture = actualCapture(screen);
    const mini = document.createElement(capture ? "img" : "span");
    if (capture) {
      const url = URL.createObjectURL(capture.blob);
      lastThumbnail.push(url);
      mini.src = url;
      mini.alt = "";
    } else {
      mini.className = "thumb";
      mini.setAttribute("aria-hidden", "true");
    }
    const name = document.createElement("span");
    name.className = "screen-name";
    name.textContent = screen.name;
    button.append(mini, name);
    button.onclick = () => {
      selected = index;
      comparing = false;
      render();
    };
    return button;
  }));
}
async function renderCanvas() {
  const token = ++renderVersion;
  const screen = getCurrent(), code = locale, target = size;
  const current = actualCapture(screen, code), previous = getLocale(screen, code).previous;
  $("compare").disabled = !previous;
  $("compare").setAttribute("aria-pressed", String(Boolean(comparing && previous)));
  $("previous").hidden = !(comparing && previous);
  $("after-label").hidden = $("previous").hidden;
  try {
    const image = await imageFor(current);
    const old = comparing && previous ? await imageFor(previous) : null;
    if (token !== renderVersion) return;
    const warning = draw($("art"), screen, code, target, image, .32);
    if (old) draw($("before"), screen, code, target, old, .32);
    $("warning").textContent = warning;
    $("warning").hidden = !warning;
    const [, width, height] = sizes[target];
    $("dimensions").textContent = `${width} × ${height} px`;
  } catch (error) {
    if (token === renderVersion) notice(error.message);
  }
}
const controls = {font: "font", align: "align", "type-scale": "scale", background: "background", ink: "ink", frame: "frame", fit: "fit"};
function renderSettings() {
  const screen = getCurrent(), strings = getLocale(screen);
  $("project-state").textContent = project.demo ? "Sample project" : `${project.screens.length} screens · ${project.locales.length} languages`;
  $("locale").replaceChildren(...project.locales.map(code => makeOption(languageLabel(code), code)));
  $("locale").value = locale;
  $("translate").hidden = locale === "en-US" || !globalThis.Translator;
  $("translation-note").hidden = locale === "en-US" || Boolean(globalThis.Translator);
  $("translation-note").textContent = "Automatic translation needs a supported desktop browser. You can edit captions here.";
  $("size").value = size;
  $("headline").value = strings.headline;
  $("subtitle").value = strings.subtitle;
  for (const [id, key] of Object.entries(controls)) $(id).value = screen.style[key];
  $("type-value").value = screen.style.scale + "%";
  $("earlier").disabled = selected === 0;
  $("later").disabled = selected === project.screens.length - 1;
  $("remove").disabled = project.screens.length === 1;
  $("duplicate").disabled = project.screens.length >= 10;
  for (const button of $("themes").children) {
    button.setAttribute("aria-pressed", String(button.dataset.theme === screen.style.theme));
  }
}
function render() {
  renderSettings();
  renderList();
  renderCanvas();
}
function changeDesign() {
  persist();
  renderCanvas();
}
function freshLocale(screen) {
  return {headline: getLocale(screen).headline, subtitle: getLocale(screen).subtitle, capture: null, previous: null};
}
function screenName(name) {
  return name.replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ").trim() || "Screenshot";
}
async function captureFrom(file) {
  if (file.size > 25 * 1024 * 1024) throw new Error("Screenshots must be 25 MB or smaller.");
  if (!["image/png", "image/jpeg", "image/webp"].includes(file.type)
    && !(file.type === "" && /\.(png|jpe?g|webp)$/i.test(file.name))) throw new Error("Choose a PNG, JPEG, or WebP image.");
  const capture = {id: newID(), blob: file};
  const image = await imageFor(capture);
  if (image.width * image.height > 32_000_000) throw new Error("This image exceeds 32 megapixels. Resize it before importing.");
  return capture;
}
async function importFiles(files, replace) {
  if (!files.length || busy) return;
  const target = getCurrent(), code = locale;
  const keepDemo = project.demo;
  const capacity = keepDemo ? 10 : 10 - project.screens.length;
  const limit = replace ? 1 : capacity;
  if (!limit) return notice("This project can hold 10 screens. Remove one to add another.");
  busy = true;
  let imported = 0;
  const problems = new Set();
  try {
    for (const file of files.slice(0, limit)) {
      try {
        const capture = await captureFrom(file);
        if (replace) {
          const version = getLocale(target, code);
          const old = actualCapture(target, code);
          version.previous = old;
          version.capture = capture;
          comparing = Boolean(old);
        } else {
          if (keepDemo && !imported) {
            project.screens = [];
            project.demo = false;
          }
          const screen = makeScreen(screenName(file.name), "", "", capture);
          for (const language of project.locales.slice(1)) {
            screen.locales[language] = {headline: "", subtitle: "", capture: null, previous: null};
          }
          project.screens.push(screen);
          if (!imported) selected = project.screens.length - 1;
          comparing = false;
        }
        imported++;
      } catch (error) {
        problems.add(error.message);
      }
    }
    if (files.length > limit) problems.add("Only the first 10 screens fit in this project.");
    if (imported) {
      persist();
      render();
      $("editor").scrollIntoView({block: "start", behavior: "smooth"});
    }
    notice([replace && imported ? "Capture replaced. Design kept." : imported ? `${imported} screenshot${imported === 1 ? "" : "s"} added.` : "", ...problems].filter(Boolean).join(" "));
  } finally {
    busy = false;
  }
}
function move(offset) {
  const index = selected + offset;
  if (index < 0 || index >= project.screens.length) return;
  [project.screens[selected], project.screens[index]] = [project.screens[index], project.screens[selected]];
  selected = index;
  persist();
  render();
}
function downloadBlob(blob, name) {
  const publisher = document.createElement("a");
  publisher.href = URL.createObjectURL(blob);
  publisher.download = name;
  document.body.append(publisher);
  publisher.click();
  publisher.remove();
  setTimeout(() => URL.revokeObjectURL(publisher.href), 60000);
}
function asPNG(canvas) {
  return new Promise((resolve, reject) => canvas.toBlob(
    blob => blob ? resolve(blob) : reject(new Error("The image could not be encoded.")), "image/png",
  ));
}
async function renderPNG(screen, code, target) {
  const canvas = document.createElement("canvas");
  draw(canvas, screen, code, target, await imageFor(actualCapture(screen, code)));
  const blob = await asPNG(canvas);
  canvas.width = 1;
  canvas.height = 1;
  return blob;
}
function filename(name) {
  return name.normalize("NFKD").replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "").slice(0, 56).toLowerCase() || "screenshot";
}
function entryFor(screen, code, target, index) {
  const [, w, h] = sizes[target];
  return {
    key: `${screen.id}:${code}:${target}`,
    signature: JSON.stringify([index, screen.name, screen.style, getLocale(screen, code).headline,
      getLocale(screen, code).subtitle, actualCapture(screen, code)?.id || "sample"]),
    name: `${code}/${target}-${w}x${h}/${String(index + 1).padStart(2, "0")}-${filename(screen.name)}.png`,
    screen, code, target,
  };
}
const crcTable = Uint32Array.from({length: 256}, (_, byte) => {
  let value = byte;
  for (let bit = 0; bit < 8; bit++) value = value & 1 ? 0xedb88320 ^ (value >>> 1) : value >>> 1;
  return value;
});
function zip(files) {
  const local = [], directory = [];
  const encoder = new TextEncoder();
  let offset = 0, directorySize = 0;
  for (const {name, bytes} of files) {
    const path = encoder.encode(name);
    let crc = 0xffffffff;
    for (const value of bytes) crc = (crc >>> 8) ^ crcTable[(crc ^ value) & 255];
    crc ^= 0xffffffff;
    const header = new DataView(new ArrayBuffer(30));
    header.setUint32(0, 0x04034b50, true);
    header.setUint16(4, 20, true);
    header.setUint16(6, 0x800, true);
    header.setUint16(12, 33, true);
    header.setUint32(14, crc, true);
    header.setUint32(18, bytes.length, true);
    header.setUint32(22, bytes.length, true);
    header.setUint16(26, path.length, true);
    local.push(header.buffer, path, bytes);
    const central = new DataView(new ArrayBuffer(46));
    central.setUint32(0, 0x02014b50, true);
    central.setUint16(4, 20, true);
    new Uint8Array(central.buffer, 6, 26).set(new Uint8Array(header.buffer, 4, 26));
    central.setUint32(42, offset, true);
    directory.push(central.buffer, path);
    directorySize += 46 + path.length;
    offset += 30 + path.length + bytes.length;
  }
  const end = new DataView(new ArrayBuffer(22));
  end.setUint32(0, 0x06054b50, true);
  end.setUint16(8, files.length, true);
  end.setUint16(10, files.length, true);
  end.setUint32(12, directorySize, true);
  end.setUint32(16, offset, true);
  return new Blob([...local, ...directory, end.buffer], {type: "application/zip"});
}
function checkChoice(text, value, checked) {
  const label = document.createElement("label");
  label.className = "checkbox";
  const input = document.createElement("input");
  input.type = "checkbox";
  input.value = value;
  input.checked = checked;
  label.append(input, text);
  return label;
}
function openExport() {
  if (busy) return;
  $("export-sizes").replaceChildren(...Object.entries(sizes).map(([key, [label, w, h]]) => checkChoice(`${label} · ${w} × ${h}`, key, key === size)));
  $("export-locales").replaceChildren(...project.locales.map(code => checkChoice(languageLabel(code), code, code === locale)));
  $("export-screens").replaceChildren(...project.screens.map(screen => checkChoice(screen.name, screen.id, true)));
  $("export-note").textContent = project.demo ? "This set includes sample app screens." : "Folders are grouped by language and device.";
  $("export-dialog").showModal();
}
async function exportBatch(event) {
  event.preventDefault();
  if (busy) return;
  const checked = id => [...$(id).querySelectorAll("input:checked")].map(input => input.value);
  const targets = checked("export-sizes"), codes = checked("export-locales");
  const selectedScreens = new Set(checked("export-screens"));
  if (!targets.length || !codes.length || !selectedScreens.size) {
    $("export-note").textContent = "Choose at least one output size, language, and screen.";
    return;
  }
  if (targets.includes("android") && selectedScreens.size > 8) {
    $("export-note").textContent = "Google Play accepts up to 8 phone screenshots. Uncheck a screen or export the Apple set separately.";
    return;
  }
  const entries = codes.flatMap(code => targets.flatMap(target =>
    project.screens.flatMap((screen, index) => selectedScreens.has(screen.id) ? [entryFor(screen, code, target, index)] : []),
  ));
  const chosen = $("changed").checked ? entries.filter(e => project.exports[e.key] !== e.signature) : entries;
  if (!chosen.length) {
    $("export-note").textContent = "Nothing has changed in this selection since your last export.";
    return;
  }
  if (chosen.length > 60) {
    $("export-note").textContent = "Choose fewer languages or sizes to export up to 60 images at a time.";
    return;
  }
  busy = true;
  $("export-submit").disabled = true;
  try {
    const files = [];
    for (const [index, entry] of chosen.entries()) {
      $("export-note").textContent = `Rendering ${index + 1} of ${chosen.length}…`;
      const png = await renderPNG(entry.screen, entry.code, entry.target);
      files.push({name: entry.name, bytes: new Uint8Array(await png.arrayBuffer())});
    }
    downloadBlob(zip(files), "storeshot-studio.zip");
    for (const entry of chosen) project.exports[entry.key] = entry.signature;
    persist();
    $("export-dialog").close();
    notice(`Downloaded ${files.length} PNG files in a ZIP.`);
  } catch (error) {
    $("export-note").textContent = error.message;
  } finally {
    $("export-submit").disabled = false;
    busy = false;
  }
}
async function exportCurrent() {
  if (busy) return;
  busy = true;
  const screen = structuredClone(getCurrent()), code = locale, target = size;
  const entry = entryFor(screen, code, target, selected);
  try {
    downloadBlob(await renderPNG(screen, code, target), entry.name.replaceAll("/", "-"));
    project.exports[entry.key] = entry.signature;
    persist();
    notice("PNG downloaded.");
  } catch (error) {
    notice(error.message);
  } finally {
    busy = false;
  }
}

$("size").replaceChildren(...Object.entries(sizes).map(([key, [name]]) => makeOption(name, key)));
for (const [id, [label, start, end, ink]] of Object.entries(themes)) {
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.theme = id;
  const swatch = document.createElement("i");
  swatch.style.background = `linear-gradient(145deg, ${start}, ${end})`;
  button.append(swatch, label);
  button.onclick = () => {
    Object.assign(getCurrent().style, {theme: id, background: start, ink});
    renderSettings();
    changeDesign();
  };
  $("themes").append(button);
}
for (const [id, key] of Object.entries(controls)) {
  $(id).oninput = event => {
    const value = id === "type-scale" ? Number(event.target.value) : event.target.value;
    getCurrent().style[key] = value;
    if (id === "type-scale") $("type-value").value = value + "%";
    changeDesign();
  };
}
for (const id of ["headline", "subtitle"]) {
  $(id).oninput = event => {
    getLocale(getCurrent())[id] = event.target.value;
    changeDesign();
  };
}
for (const id of ["upload", "add"]) $(id).onclick = () => $("files").click();
$("replace").onclick = () => $("replacement").click();
for (const [id, replace] of [["files", false], ["replacement", true]]) {
  $(id).onchange = event => {
    const input = event.target;
    const files = [...input.files];
    input.value = "";
    importFiles(files, replace);
  };
}
const stage = document.querySelector(".stage");
stage.addEventListener("dragover", event => {
  if (!event.dataTransfer.types.includes("Files")) return;
  event.preventDefault();
  stage.classList.add("is-dropping");
});
stage.addEventListener("dragleave", event => {
  if (!stage.contains(event.relatedTarget)) stage.classList.remove("is-dropping");
});
stage.addEventListener("drop", event => {
  if (!event.dataTransfer.files.length) return;
  event.preventDefault();
  stage.classList.remove("is-dropping");
  importFiles([...event.dataTransfer.files], false);
});
$("size").onchange = event => { size = event.target.value; renderCanvas(); };
$("locale").onchange = event => { locale = event.target.value; comparing = false; render(); };
$("compare").onclick = () => { comparing = !comparing; renderCanvas(); };
const quickCaption = $("quick-caption");
$("canvas-caption").onclick = () => {
  quickCaption.value = $("headline").value;
  quickCaption.hidden = false;
  quickCaption.focus({preventScroll: true});
  quickCaption.select();
};
quickCaption.oninput = () => {
  $("headline").value = quickCaption.value;
  getLocale(getCurrent()).headline = quickCaption.value;
  changeDesign();
};
quickCaption.onblur = () => { quickCaption.hidden = true; };
quickCaption.onkeydown = event => {
  if (event.key === "Escape") $("canvas-caption").focus();
};
$("earlier").onclick = () => move(-1);
$("later").onclick = () => move(1);
$("apply").onclick = () => {
  const style = {...getCurrent().style};
  for (const screen of project.screens) screen.style = {...style};
  persist();
  notice("Style applied to all screens. Captions and captures kept.");
};
$("duplicate").onclick = () => {
  const clone = structuredClone(getCurrent());
  clone.id = newID();
  clone.name += " copy";
  project.screens.splice(++selected, 0, clone);
  comparing = false;
  persist();
  render();
};
$("remove").onclick = () => {
  project.screens.splice(selected, 1);
  selected = Math.min(selected, project.screens.length - 1);
  comparing = false;
  persist();
  render();
};
$("add-locale").onclick = () => {
  if (project.locales.length >= 12) {
    notice("A project can have up to 12 languages.");
    return;
  }
  const choices = languageChoices.filter(code => !project.locales.includes(code))
    .sort((a, b) => languageLabel(a).localeCompare(languageLabel(b), "en"));
  const placeholder = makeOption("Choose a language", "");
  placeholder.disabled = true;
  $("locale-choice").replaceChildren(placeholder, ...choices.map(code => makeOption(languageLabel(code), code)));
  $("locale-choice").value = "";
  $("locale-dialog").showModal();
};
$("locale-form").onsubmit = event => {
  event.preventDefault();
  const code = $("locale-choice").value;
  if (!languageChoices.includes(code) || project.locales.includes(code) || project.locales.length >= 12) return;
  project.locales.push(code);
  for (const screen of project.screens) screen.locales[code] = freshLocale(screen);
  locale = code;
  comparing = false;
  $("locale-dialog").close();
  persist();
  render();
};
$("translate").onclick = () => {
  const code = new Intl.Locale(locale);
  $("translate-summary").textContent = `Translate the English captions into ${languageLabel(locale)}. Only caption text is translated on this device.`;
  $("translate-all").checked = false;
  if (code.language === "en") {
    $("translation-note").hidden = false;
    $("translation-note").textContent = "This version already uses English. You can edit its wording directly.";
    return;
  }
  $("translate-dialog").showModal();
};
$("translate-form").onsubmit = async event => {
  event.preventDefault();
  if (busy || !globalThis.Translator) return;
  const target = locale;
  const screens = $("translate-all").checked ? [...project.screens] : [getCurrent()];
  const summary = $("translate-summary");
  const submit = $("translate-submit");
  let translator;
  busy = true;
  submit.disabled = true;
  try {
    const options = {sourceLanguage: "en", targetLanguage: new Intl.Locale(target).language};
    translator = await globalThis.Translator.create({
      ...options,
      monitor(monitor) {
        monitor.addEventListener("downloadprogress", progress => {
          summary.textContent = `Preparing translation · ${Math.round(progress.loaded * 100)}%`;
        });
      },
    });
    const updates = [];
    for (const [index, screen] of screens.entries()) {
      summary.textContent = `Translating screen ${index + 1} of ${screens.length}…`;
      const source = getLocale(screen, "en-US");
      const captions = {};
      for (const field of ["headline", "subtitle"]) {
        captions[field] = source[field].trim() ? await translator.translate(source[field]) : "";
      }
      updates.push([screen, captions]);
    }
    for (const [screen, captions] of updates) Object.assign(getLocale(screen, target), captions);
    persist();
    $("translate-dialog").close();
    render();
    notice("Captions translated. Review them before exporting.");
  } catch {
    summary.textContent = "Automatic translation is unavailable for this language or browser. You can enter the captions yourself.";
  } finally {
    translator?.destroy();
    submit.disabled = false;
    busy = false;
  }
};
$("translate-dialog").addEventListener("cancel", event => { if (busy) event.preventDefault(); });
$("download").onclick = exportCurrent;
$("batch").onclick = openExport;
$("export-form").onsubmit = exportBatch;
for (const close of document.querySelectorAll("[data-close]")) {
  close.onclick = () => { if (!busy) $(close.dataset.close).close(); };
}
$("export-dialog").addEventListener("cancel", event => { if (busy) event.preventDefault(); });
render();
openStorage().then(async db => {
  const stored = await readProject(db);
  if (stored && project.demo && renderVersion === 1) {
    project = stored;
    render();
  }
  database = db;
  persist();
}).catch(() => notice("Local project saving is unavailable in this browser. You can still edit and export."));
