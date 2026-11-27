"use strict";
const $ = id => document.getElementById(id);
const sizes = {
  iphone: ["iPhone 6.9 inch", 1320, 2868],
  iphone69alt: ["iPhone 6.9 / 6.7 inch", 1290, 2796],
  iphone63: ["iPhone 6.3 inch", 1206, 2622],
  iphone65: ["iPhone 6.5 inch", 1242, 2688],
  iphone65alt: ["iPhone 6.5 inch alternative", 1284, 2778],
  ipad: ["iPad 13 inch", 2064, 2752],
  android: ["Google Play phone", 1080, 1920],
  android1440: ["Google Play phone HD", 1440, 2560],
  feature: ["Google Play feature graphic", 1024, 500],
};
const themes = {
  violet: ["Violet", "#302461", "#a66cf4", "#ffffff"],
  coast: ["Coast", "#123c52", "#43aea8", "#ffffff"],
  bloom: ["Bloom", "#ffcfac", "#ed8295", "#321e3b"],
  ink: ["Ink", "#101b38", "#4265b6", "#ffffff"],
  sage: ["Sage", "#e0ead6", "#7ab0a3", "#172e33"],
  plain: ["Solid", "#263a60", "#263a60", "#ffffff"],
};
const fontStack = {sans: "Arial", serif: "Georgia", mono: "monospace"};
const scriptFonts = {
  ja: "Noto Sans JP", ko: "Noto Sans KR", "zh-Hans": "Noto Sans SC", "zh-Hant": "Noto Sans TC",
  ar: "Noto Sans Arabic", fa: "Noto Sans Arabic", ur: "Noto Sans Arabic", he: "Noto Sans Hebrew",
  bn: "Noto Sans Bengali", hi: "Noto Sans Devanagari", ta: "Noto Sans Tamil", th: "Noto Sans Thai",
};
const frameColors = {dark: "#151c2c", light: "#c4b8a5", ipad: "#212632", pixel: "#242b2c", clay: "#ded7cc", none: "#151c2c"};
const templates = {
  hero: ["Panoramic split hero", {theme: "violet", frame: "dark", deviceTilt: -12}, true],
  duo: ["Tilted duo", {theme: "ink", frame: "light", deviceTilt: 12, devicePerspective: 18, deviceScale: 90}, false],
  minimal: ["Minimal typography", {theme: "plain", frame: "none", font: "serif", deviceScale: 80}, false],
  pop: ["Feature close-up", {theme: "coast", fit: "cover", deviceScale: 105}, false],
  neon: ["Dark mode neon", {theme: "ink", accent: "#914df7", mesh: true}, false],
  rating: ["Social proof", {theme: "bloom", frame: "clay", font: "serif"}, false],
  soft: ["Soft clay", {theme: "sage", frame: "clay", deviceShadow: 38}, false],
  editorial: ["Editorial grid", {theme: "bloom", font: "serif", align: "start", deviceX: 6}, false],
  contrast: ["High contrast", {theme: "plain", background: "#101224", ink: "#ffffff", frame: "light", align: "left"}, false],
  focus: ["Product focus", {theme: "coast", frame: "pixel", deviceTilt: -5, deviceScale: 110}, false],
  tablet: ["Tablet showcase", {theme: "sage", frame: "ipad", deviceScale: 92}, false],
  type: ["Bold headline", {theme: "violet", scale: 125, deviceScale: 77, align: "center"}, false],
};
function captionFont(code, font) {
  const family = scriptFonts[code] || scriptFonts[new Intl.Locale(code).language];
  return [family && `"${family}"`, fontStack[font], "system-ui", "sans-serif"].filter(Boolean).join(", ");
}
async function loadCaptionFonts(screen, code) {
  const family = scriptFonts[code] || scriptFonts[new Intl.Locale(code).language];
  if (!family || !document.fonts) return;
  const caption = getLocale(screen, code);
  await Promise.all(captionFields.map((field, index) => {
    const text = caption[field].trim();
    return text ? document.fonts.load(`${index ? 400 : 700} 16px "${family}"`, text).catch(() => {}) : null;
  }));
}
const baseStyle = {theme: "violet", background: themes.violet[1], ink: themes.violet[3], font: "sans", align: "start", scale: 100, frame: "dark", fit: "contain"};
const newID = () => crypto.randomUUID?.() ||
  Array.from(crypto.getRandomValues(new Uint8Array(16)), byte => byte.toString(16).padStart(2, "0")).join("");
const makeScreen = (name, headline, subtitle, capture = null) => ({
  id: newID(), name, style: {...baseStyle},
  locales: {"en-US": {headline, subtitle, capture, previous: null}},
});
const makeDemo = () => ({
  screens: ["Today", "Your routine", "Progress"].map(name => makeScreen(name, "", "")),
  locales: ["en-US"], exports: {}, demo: true, sampleCaptionsCleared: true,
});
const captionFields = ["headline", "subtitle"];
const localizedFields = [...captionFields, "badge"];
function clearLegacySampleCaptions(project) {
  if (!project.demo || project.sampleCaptionsCleared) return;
  const defaults = {
    headline: new Set(["Make time for a reset", "Build a routine you’ll keep", "See how far you’ve come"]),
    subtitle: new Set(["Small moments for a calmer day", "Find a rhythm that works for you", "Every small step counts"]),
  };
  for (const screen of project.screens) {
    for (const caption of Object.values(screen.locales)) {
      for (const field of captionFields) {
        if (defaults[field].has(caption[field]) || defaults[field].has(caption.translatedFrom?.[field])) {
          caption[field] = "";
          if (caption.translatedFrom) delete caption.translatedFrom[field];
        }
      }
    }
  }
  project.sampleCaptionsCleared = true;
}
let project = makeDemo();
let selected = 0, locale = "en-US", size = "iphone", comparing = false;
let requestedLocale = "en-US";
let savedTimer, renderVersion = 0, galleryVersion = 0;
let database;
const backupKey = "storeshot-studio-caption-backup";
const captionEndpoint = document.querySelector('meta[name="storeshot-ai-endpoint"]').content.trim();
const contextFields = {"app-name": "appName", "app-category": "category", "app-tone": "tone", "app-description": "description"};
const captureFields = ["capture", "previous"];
let busy = false;
const images = new WeakMap();

function openStorage() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("storeshot-studio", 1);
    request.onupgradeneeded = () => request.result.createObjectStore("workspace");
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
    request.onblocked = () => reject(new Error("Local storage is blocked."));
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
function storageNotice(message) {
  $("storage-status").textContent = message;
  $("storage-status").hidden = !message;
}
function readBackup() {
  try {
    const backup = JSON.parse(localStorage.getItem(backupKey));
    return backup && isSavedProject(backup) ? backup : null;
  } catch {
    return null;
  }
}
function writeBackup() {
  try {
    localStorage.setItem(backupKey, JSON.stringify(project, (key, value) =>
      key === "blob" || key === "bytes" ? undefined : value));
    return true;
  } catch {
    return false;
  }
}
function persist(saveImmediately = false) {
  project.view = {screen: getCurrent().id, locale, requestedLocale, size, zoom: Number($("gallery-zoom").value)};
  project.savedAt = Math.max(Date.now(), (project.savedAt || 0) + 1);
  const backedUp = writeBackup();
  if (!database) {
    storageNotice(backedUp ? "Captions and settings are saved in this browser. Uploaded images can only be used in this session."
      : "This browser is blocking local saves. Export your work before closing or refreshing.");
    return;
  }
  storageNotice(saveImmediately ? "Saving uploaded screenshots…" : backedUp ? "Captions and settings saved." : "Saving project…");
  clearTimeout(savedTimer);
  savedTimer = setTimeout(saveProject, 250);
  if (saveImmediately) return saveProject();
}
async function saveProject() {
  if (savedTimer === undefined) return;
  clearTimeout(savedTimer);
  savedTimer = undefined;
  try {
    const transaction = database.transaction("workspace", "readwrite");
    transaction.objectStore("workspace").put(project, "project");
    await new Promise((resolve, reject) => {
      transaction.oncomplete = resolve;
      transaction.onabort = () => reject(transaction.error);
      transaction.commit?.();
    });
    storageNotice(hasMissingCaptures(project)
      ? "Captions and settings saved. Some uploaded images need to be added again."
      : "Saved in this browser.");
  } catch {
    storageNotice("The full project couldn’t be saved. Export your screenshots before closing.");
  }
}
window.addEventListener("pagehide", saveProject);

function getCurrent() {
  return project.screens[selected];
}
function getLocale(screen, code = locale) {
  return screen.locales[code];
}
function hasCaptureData(capture) {
  return Boolean(capture?.bytes?.byteLength || capture?.blob?.size);
}
function actualCapture(screen, code = locale) {
  const capture = getLocale(screen, code).capture;
  const sourceCapture = getLocale(screen, "en-US").capture;
  return hasCaptureData(capture) ? capture : hasCaptureData(sourceCapture) ? sourceCapture : null;
}
function captureLocaleForPreview(screen) {
  return hasCaptureData(screen.locales[requestedLocale]?.capture) ? requestedLocale : locale;
}
function loadImage(url) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error("This image could not be opened."));
    image.src = url;
  });
}
async function decodeCapture(capture) {
  const bytes = capture.bytes ?? await capture.blob.arrayBuffer();
  const blob = new Blob([bytes], {type: capture.type || capture.blob?.type});
  const url = URL.createObjectURL(blob);
  try {
    return await loadImage(url);
  } catch {
    const dataUrl = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(reader.error);
      reader.readAsDataURL(blob);
    });
    return loadImage(dataUrl);
  } finally {
    URL.revokeObjectURL(url);
  }
}
function imageFor(capture) {
  if (!capture) return Promise.resolve(null);
  if (!images.has(capture)) {
    images.set(capture, decodeCapture(capture).catch(error => {
      images.delete(capture);
      throw error;
    }));
  }
  return images.get(capture);
}

function roundPath(ctx, x, y, w, h, radius) {
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(x, y, w, h, radius);
  else ctx.rect(x, y, w, h);
}
function fillRound(ctx, x, y, w, h, radius, color) {
  roundPath(ctx, x, y, w, h, radius);
  ctx.fillStyle = color;
  ctx.fill();
}
function fitImage(ctx, image, x, y, w, h, mode) {
  const scale = Math[mode === "cover" ? "max" : "min"](w / image.width, h / image.height);
  const iw = image.width * scale, ih = image.height * scale;
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(image, x + (w - iw) / 2, y + (h - ih) / 2, iw, ih);
  return scale;
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
  fillRound(ctx, 20, 48, 49, 8, 4, "#5f4da2");
  fillRound(ctx, 20, 72, [159, 137, 104][variant % 3], 18, 6, "#c9bde6");
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
  fillRound(ctx, 34, 216, 105, 10, 5, "#ffffffb5");
  fillRound(ctx, 34, 239, 75, 7, 3, "#ffffff6b");
  fillRound(ctx, 20, 312, 72, 11, 5, "#c9bde6");
  for (const [i, color] of ["#e9ddfc", "#def1e8", "#ffe7dc"].entries()) {
    const top = 337 + i * 63;
    fillRound(ctx, 17, top, 266, 52, 10, "white");
    fillRound(ctx, 28, top + 9, 34, 34, 8, color);
    fillRound(ctx, 75, top + 17, 85 - i * 9, 7, 3, "#c9bde6");
    fillRound(ctx, 75, top + 30, 54, 5, 2, "#e5ddf3");
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
function isRightToLeft(code) {
  return new Intl.Locale(code).getTextInfo?.().direction === "rtl" || /^(ar|fa|he|ur|ps|sd)(-|$)/.test(code);
}
function draw(canvas, screen, code, target, image, factor = 1, spread = null) {
  const [, outW, outH] = sizes[target];
  canvas.width = Math.round(outW * factor);
  canvas.height = Math.round(outH * factor);
  const ctx = canvas.getContext("2d", {alpha: false});
  ctx.scale(canvas.width / outW, canvas.height / outH);
  const style = screen.style, strings = getLocale(screen, code);
  const width = outW, height = outH;
  const paint = spread?.lead.style || style;
  const offset = spread?.half * width || 0;
  const span = spread ? width * 2 : width;
  const accent = paint.accent || (paint.theme === "plain" ? paint.background : themes[paint.theme][2]);
  const gradient = ctx.createLinearGradient(-offset, height, span - offset, 0);
  gradient.addColorStop(0, paint.background);
  gradient.addColorStop(1, accent);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);
  if (paint.mesh) {
    const mesh = ctx.createRadialGradient(span * .7 - offset, height * .24, 0, span * .7 - offset, height * .24, span * .56);
    mesh.addColorStop(0, accent);
    mesh.addColorStop(1, "#ffffff00");
    ctx.fillStyle = mesh;
    ctx.fillRect(0, 0, width, height);
  }
  if (paint.theme !== "plain") {
    ctx.strokeStyle = "#ffffff29";
    ctx.lineWidth = width * .003;
    for (let ring = 0; ring < 5; ring++) {
      ctx.beginPath();
      ctx.ellipse(span * .8 - offset, height * .78, width * (.34 + ring * .11), height * .2, -.55, 0, Math.PI * 2);
      ctx.stroke();
    }
  }
  const feature = target === "feature";
  const pad = width * .085;
  const maxWidth = feature ? width * .48 : width - pad * 2;
  const textTop = height * (feature ? .2 : .063);
  const maxTextSize = Math.min(width * .087, height * (feature ? .13 : .072)) * style.scale / 100;
  const capHeight = height * (feature ? .64 : spread ? .24 : .265);
  const rtl = isRightToLeft(code);
  const stack = captionFont(code, style.font);
  const subtitleStack = captionFont(code, style.subtitleFont || style.font);
  ctx.save();
  ctx.direction = rtl ? "rtl" : "ltr";
  function measure(fontSize) {
    const subSize = fontSize * .43;
    ctx.font = `700 ${fontSize}px ${stack}`;
    const headline = strings.headline.trim() ? linesFor(ctx, strings.headline, maxWidth, code) : [];
    ctx.font = `400 ${subSize}px ${subtitleStack}`;
    const subtitle = strings.subtitle.trim() ? linesFor(ctx, strings.subtitle, maxWidth, code) : [];
    const textHeight = headline.length * fontSize * 1.15 + subtitle.length * subSize * 1.35
      + (headline.length && subtitle.length ? subSize * .55 : 0);
    return {textSize: fontSize, subSize, headline, subtitle, textHeight};
  }
  let fitted = measure(maxTextSize);
  if (fitted.textHeight > capHeight) {
    let bottom = 0, top = maxTextSize;
    for (let attempt = 0; attempt < 14; attempt++) {
      const candidate = measure((bottom + top) / 2);
      if (candidate.textHeight <= capHeight) {
        bottom = candidate.textSize;
        fitted = candidate;
      } else {
        top = candidate.textSize;
      }
    }
  }
  const {textSize, subSize, headline, subtitle, textHeight} = fitted;
  ctx.beginPath();
  ctx.rect(0, textTop - textSize * .2, width, capHeight + textSize * .2);
  ctx.clip();
  ctx.fillStyle = style.ink;
  ctx.textBaseline = "top";
  ctx.textAlign = style.align === "start" ? (rtl ? "right" : "left") : style.align === "left" ? "left" : "center";
  const textX = ctx.textAlign === "left" ? pad : ctx.textAlign === "right" ? pad + maxWidth : pad + maxWidth / 2;
  let y = textTop;
  ctx.font = `700 ${textSize}px ${stack}`;
  for (const line of headline) {
    ctx.fillText(line, textX, y, maxWidth);
    y += textSize * 1.15;
  }
  if (headline.length && subtitle.length) y += subSize * .55;
  const subtitleTop = y;
  ctx.font = `400 ${subSize}px ${subtitleStack}`;
  for (const line of subtitle) {
    ctx.fillText(line, textX, y, maxWidth);
    y += subSize * 1.35;
  }
  ctx.restore();
  const deviceStyle = spread?.lead.style || style;
  const deviceImage = spread ? spread.image : image;
  const areaTop = feature ? height * .08 : spread ? height * .36 : Math.max(height * .237, textTop + textHeight + height * .034);
  const aspect = target === "ipad" || deviceStyle.frame === "ipad" ? .74 : .48;
  const available = height - areaTop - height * (strings.badge && !spread ? .115 : .062);
  const deviceScale = (deviceStyle.deviceScale ?? 100) / 100;
  const deviceAngle = (deviceStyle.deviceTilt ?? (spread ? -12 : 0)) * Math.PI / 180;
  const dh = Math.min(available, width * .81 / aspect) * deviceScale;
  const dw = dh * aspect;
  const centerX = (feature ? width * .78 : spread ? width - offset : width / 2) + width * (deviceStyle.deviceX || 0) / 100;
  const centerY = areaTop + available / 2 + (deviceStyle.deviceY || 0) * height / 100;
  const bezel = deviceStyle.frame === "none" ? 0 : dw * .025;
  const rad = dw * (deviceStyle.frame === "ipad" ? .052 : .075);
  ctx.save();
  ctx.beginPath();
  const deviceStart = feature ? width * .57 : 0;
  ctx.rect(deviceStart, areaTop, width - deviceStart, height - areaTop);
  ctx.clip();
  ctx.translate(centerX, centerY);
  ctx.rotate(deviceAngle);
  const perspective = (deviceStyle.devicePerspective || 0) / 100;
  ctx.transform(1 - Math.abs(perspective) * .34, 0, perspective * .62, 1, 0, 0);
  const dx = -dw / 2, dy = -dh / 2;
  const shadow = (deviceStyle.deviceShadow ?? 70) / 70;
  ctx.save();
  ctx.shadowColor = "#080e2e76";
  ctx.shadowBlur = width * .036 * shadow;
  ctx.shadowOffsetY = width * .02 * shadow;
  fillRound(ctx, dx, dy, dw, dh, rad, frameColors[deviceStyle.frame] || frameColors.dark);
  ctx.restore();
  roundPath(ctx, dx + bezel, dy + bezel, dw - bezel * 2, dh - bezel * 2, Math.max(0, rad - bezel));
  ctx.clip();
  ctx.fillStyle = "#151c2c";
  ctx.fillRect(dx, dy, dw, dh);
  const captureScale = deviceImage
    ? fitImage(ctx, deviceImage, dx + bezel, dy + bezel, dw - bezel * 2, dh - bezel * 2, deviceStyle.fit)
    : 1;
  if (!deviceImage) drawDemo(ctx, dx + bezel, dy + bezel, dw - bezel * 2, dh - bezel * 2, 0);
  if (deviceStyle.frame === "dark" || deviceStyle.frame === "light") {
    fillRound(ctx, -dw * .11, dy + bezel + dw * .023, dw * .22, dw * .058, dw * .029, "#111620");
  } else if (deviceStyle.frame === "pixel") {
    fillRound(ctx, -dw * .019, dy + bezel + dw * .032, dw * .038, dw * .038, dw * .019, "#111620");
  }
  if (deviceStyle.cleanStatus) {
    const bar = dw * .105;
    ctx.fillStyle = "#151c2c";
    ctx.fillRect(dx + bezel, dy + bezel, dw - bezel * 2, bar);
    ctx.fillStyle = "#fff";
    ctx.font = `700 ${bar * .48}px sans-serif`;
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText("9:41", dx + dw * .13, dy + bezel + bar * .55);
    ctx.fillText("● ▰", dx + dw * .75, dy + bezel + bar * .55);
  }
  ctx.restore();
  if (strings.badge && !spread) {
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = `700 ${width * .035}px sans-serif`;
    ctx.fillStyle = style.ink;
    ctx.fillText(strings.badge, width / 2, height * .96, maxWidth);
  }
  const messages = [];
  if (textSize < maxTextSize * .91) messages.push("Text was reduced to fit. Check it at the final size.");
  if (deviceImage && deviceStyle.fit === "cover" && Math.abs(deviceImage.width / deviceImage.height - (dw - bezel * 2) / (dh - bezel * 2)) > .045) messages.push("Fill frame crops this capture. Choose Show full image to keep its edges.");
  if (captureScale > 1.05) messages.push("This capture is being enlarged at the selected export size. A higher-resolution original will look sharper.");
  if (image && !strings.capture && code !== "en-US") messages.push("This language is using the English app capture.");
  return {
    warning: messages.join(" "),
    subtitleTop: subtitleTop / height,
    subtitleHeight: Math.max(0, Math.min(y, textTop + capHeight) - subtitleTop) / height,
  };
}

const languageChoices = [
  "ar", "bn", "bg", "ca", "zh-Hans", "zh-Hant", "cs", "da", "nl", "en-AU", "en-CA", "en-GB",
  "et", "fi", "fr-CA", "fr-FR", "de-DE", "el", "he", "hi", "hr", "hu", "id", "it",
  "ja", "ko", "lv", "lt", "ms", "nb", "fa", "pl", "pt-BR", "pt-PT", "ro", "ru",
  "sk", "sl", "es-ES", "es-MX", "es-US", "sv", "ta", "th", "tr", "uk", "ur", "vi",
];
const languageNames = new Intl.DisplayNames(["en"], {type: "language", languageDisplay: "standard"});
const languageLabel = code => languageNames.of(code) || code;

const localModels = {
  ar: ["ar", "034a684356c19021a187cda4d7f823298b913921"],
  de: ["de", "1ca130c44c4c5441ef16d48aae521a424ab644f7"],
  es: ["es", "4b002a4c7edd54a7ced58877258b87f7efd3f892"],
  fr: ["fr", "28726206f80896b90035bd99cccd5cc1e151f916"],
  hi: ["hi", "7aad72006a1588a9c3485ed6203aed99eebbc872"],
  it: ["it", "075406e3c8c2c30634d4a1bd8f00c21d9e162011"],
  nl: ["nl", "c3a0541231a7329b4492809fc2bd7ab7d2ceb0bc"],
  ru: ["ru", "e050376e960175e8ddc5cff85025dc8436cddd68"],
  uk: ["uk", "e6ca587292984b343fd829b6430ed55858496525"],
  "zh-Hans": ["zh", "046f55aec303cdee3e0318604406d4df20f1e8ea"],
};
function localModel(code) {
  const {language} = new Intl.Locale(code);
  const opus = localModels[code === "zh-Hant" ? "zh-Hans" : code] || localModels[language];
  if (opus) return {model: "Xenova/opus-mt-en-" + opus[0], revision: opus[1]};
  // M2M100 covers the remaining non-English options in the caption language picker.
  if (language !== "en" && languageChoices.includes(code)) {
    return {
      model: "Xenova/m2m100_418M",
      revision: "9c374f0b7aca709787cea97b047bfbbd1559d177",
      targetLanguage: language === "nb" ? "no" : language,
    };
  }
}
const unsupportedNativeLanguages = new Set();
function nativeTarget(code) {
  const {language, script} = new Intl.Locale(code);
  return script ? `${language}-${script}` : language;
}
function canTranslateLocale(code) {
  return new Intl.Locale(code).language !== "en"
    && Boolean(captionEndpoint || (globalThis.Translator && !unsupportedNativeLanguages.has(nativeTarget(code)))
      || (globalThis.Worker && globalThis.WebAssembly && localModel(code)));
}
async function checkTranslationSupport(code) {
  if (captionEndpoint || !canTranslateLocale(code) || (globalThis.Worker && globalThis.WebAssembly && localModel(code))
    || !globalThis.Translator?.availability) return;
  const targetLanguage = nativeTarget(code);
  try {
    if (await globalThis.Translator.availability({sourceLanguage: "en", targetLanguage}) === "unavailable") {
      unsupportedNativeLanguages.add(targetLanguage);
      if (requestedLocale === code) renderLanguageSettings();
    }
  } catch {
    // Keep the translation option available when the browser cannot report support.
  }
}


function makeOption(label, value) {
  return new Option(label, value);
}
function selectScreen(index) {
  cancelTranslation();
  selected = index;
  comparing = false;
  render();
  persist();
}
function spreadFor(screens, index, code, target) {
  if (!project.panoramic || target === "feature" || (index ^ 1) >= screens.length || index < 0) return null;
  const lead = screens[index - index % 2];
  return {lead, half: index % 2, capture: actualCapture(lead, code)};
}
let galleryKeys = "";
function renderGallery() {
  const gallery = $("gallery");
  const keys = project.screens.map(screen => screen.id).join("|");
  if (galleryKeys !== keys) {
    galleryKeys = keys;
    gallery.replaceChildren(...project.screens.map((screen, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "gallery-slide";
      button.setAttribute("aria-label", `Edit slide ${index + 1}: ${screen.name}`);
      const canvas = document.createElement("canvas");
      canvas.setAttribute("aria-hidden", "true");
      const name = document.createElement("span");
      name.textContent = screen.name;
      button.append(canvas, name);
      button.onclick = () => selectScreen(index);
      button.ondragover = event => {
        if (!event.dataTransfer.types.includes("Files")) return;
        event.preventDefault();
        button.classList.add("is-dropping");
      };
      button.ondragleave = () => button.classList.remove("is-dropping");
      button.ondrop = event => {
        const files = [...event.dataTransfer.files];
        if (files.length !== 1) return;
        event.preventDefault();
        event.stopPropagation();
        button.classList.remove("is-dropping");
        if (busy) return;
        selectScreen(index);
        importFiles(files, true);
      };
      return button;
    }));
  }
  const code = locale, target = size;
  const [, width, height] = sizes[target];
  const zoom = Number($("gallery-zoom").value) / 100;
  const token = ++galleryVersion;
  gallery.classList.toggle("is-panoramic", Boolean(project.panoramic && target !== "feature"));
  for (const [index, button] of [...gallery.children].entries()) {
    const screen = project.screens[index];
    button.setAttribute("aria-pressed", String(index === selected));
    button.style.width = `${Math.round(210 * width / height * zoom)}px`;
    const imageCode = captureLocaleForPreview(screen);
    const spread = spreadFor(project.screens, index, imageCode, target);
    const capture = spread ? spread.capture : actualCapture(screen, imageCode);
    const textLocale = code !== "en-US" && !hasSavedCaptions(screen, code) && hasCaptionText(getLocale(screen, "en-US"))
      ? "en-US" : code;
    button.lastElementChild.textContent = textLocale === code ? screen.name : `${screen.name} · English`;
    button.dir = isRightToLeft(textLocale) ? "rtl" : "ltr";
    Promise.all([imageFor(capture).catch(() => null), loadCaptionFonts(screen, textLocale)]).then(([image]) => {
      if (token !== galleryVersion) return;
      if (spread) spread.image = image;
      const ratio = Math.max(1, window.devicePixelRatio || 1);
      draw(button.firstElementChild, screen, textLocale, target, image, Math.min(1, 210 * zoom * ratio / height), spread);
    }).catch(error => { if (token === galleryVersion) notice(error.message); });
  }
}
function renderList() {
  $("screen-list").replaceChildren(...project.screens.map((screen, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.setAttribute("aria-pressed", String(index === selected));
    const capture = actualCapture(screen, captureLocaleForPreview(screen));
    const mini = document.createElement("span");
    mini.className = "thumb";
    mini.setAttribute("aria-hidden", "true");
    if (capture) {
      imageFor(capture).then(image => {
        if (!mini.isConnected) return;
        const thumbnail = document.createElement("canvas");
        thumbnail.width = 80;
        thumbnail.height = 112;
        fitImage(thumbnail.getContext("2d"), image, 0, 0, 80, 112, "cover");
        const preview = document.createElement("img");
        preview.alt = "";
        preview.src = thumbnail.toDataURL();
        mini.replaceWith(preview);
      }).catch(() => {});
    }
    const name = document.createElement("span");
    name.className = "screen-name";
    name.textContent = screen.name;
    button.append(mini, name);
    button.onclick = () => selectScreen(index);
    return button;
  }));
}
async function renderCanvas() {
  const token = ++renderVersion;
  const screen = getCurrent(), code = locale, target = size;
  const imageCode = captureLocaleForPreview(screen);
  const spread = spreadFor(project.screens, selected, imageCode, target);
  const current = spread ? spread.capture : actualCapture(screen, imageCode);
  const savedPrevious = getLocale(screen, imageCode).previous;
  const previous = hasCaptureData(savedPrevious) ? savedPrevious : null;
  $("canvas-caption").classList.toggle("is-sample", !current);
  $("compare").disabled = !previous || Boolean(spread);
  $("compare").setAttribute("aria-pressed", String(Boolean(comparing && previous)));
  $("previous").hidden = !(comparing && previous);
  $("after-label").hidden = $("previous").hidden;
  try {
    const [image, old] = await Promise.all([
      imageFor(current).catch(() => null),
      comparing && !spread ? imageFor(previous).catch(() => null) : null,
      loadCaptionFonts(screen, code),
    ]);
    if (token !== renderVersion) return;
    const previewScale = Math.min(1, .32 * Math.max(1, window.devicePixelRatio || 1));
    if (spread) spread.image = image;
    const {warning, subtitleTop, subtitleHeight} = draw($("art"), screen, code, target, image, previewScale, spread);
    $("canvas-caption").classList.toggle("is-sample", !image);
    const subtitleButton = $("canvas-subtitle");
    subtitleButton.hidden = !subtitleHeight;
    subtitleButton.style.top = subtitleTop * 100 + "%";
    subtitleButton.style.height = subtitleHeight * 100 + "%";
    if (old) draw($("before"), screen, code, target, old, previewScale);
    if (comparing && !old) {
      $("previous").hidden = true;
      $("after-label").hidden = true;
    }
    const missing = !image && (getLocale(screen, code).capture || getLocale(screen, "en-US").capture);
    $("warning").textContent = missing
      ? "The saved image couldn’t be opened. Use Replace capture to reattach the original. Your captions are intact."
      : warning;
    $("warning").hidden = !$("warning").textContent;
    const [, width, height] = sizes[target];
    $("dimensions").textContent = `${width} × ${height} px`;
  } catch (error) {
    if (token === renderVersion) notice(error.message);
  }
}
const controls = {
  font: "font", align: "align", "type-scale": "scale", background: "background", ink: "ink", frame: "frame", fit: "fit",
  "device-scale": "deviceScale", "device-x": "deviceX", "device-y": "deviceY", "device-tilt": "deviceTilt",
  "device-shadow": "deviceShadow", "device-perspective": "devicePerspective", "clean-status": "cleanStatus",
};
const deviceDefaults = {deviceScale: 100, deviceX: 0, deviceY: 0, deviceTilt: 0, devicePerspective: 0, deviceShadow: 70, cleanStatus: false};
function renderLanguageSettings() {
  const choices = [...new Set([...project.locales, ...languageChoices])]
    .filter(code => code !== "en-US")
    .sort((a, b) => languageLabel(a).localeCompare(languageLabel(b), "en"));
  $("locale").replaceChildren(makeOption(languageLabel("en-US"), "en-US"), ...choices.map(code => {
    const manual = new Intl.Locale(code).language !== "en" && !canTranslateLocale(code);
    return makeOption(languageLabel(code) + (manual ? " (manual)" : ""), code);
  }));
  $("locale").value = requestedLocale;
  const canTranslate = canTranslateLocale(requestedLocale);
  const english = nativeTarget(requestedLocale) === "en";
  $("translate").disabled = english;
  $("translate").textContent = english || canTranslate ? "Translate" : "Edit manually";
  const waiting = requestedLocale !== locale;
  $("translation-note").hidden = english || (!waiting && canTranslate);
  $("translation-note").textContent = canTranslate
    ? `Preview is showing ${languageLabel(locale)}. Click Translate for ${languageLabel(requestedLocale)}.`
    : `Automatic translation to ${languageLabel(requestedLocale)} is unavailable in this browser. Choose Edit manually to enter your own captions.`;
}
function syncCaptionInputs(field, value) {
  for (const id of [field, "quick-" + field]) {
    const input = $(id);
    if (input.value !== value) input.value = value;
    input.dir = isRightToLeft(locale) ? "rtl" : "auto";
  }
}
function renderSettings() {
  const screen = getCurrent(), strings = getLocale(screen);
  $("project-state").textContent = project.demo ? "Sample project" : `${project.screens.length} screens · ${project.locales.length} languages`;
  renderLanguageSettings();
  $("size").value = size;
  $("panorama-mode").checked = Boolean(project.panoramic);
  for (const field of captionFields) syncCaptionInputs(field, strings[field]);
  $("badge-copy").value = strings.badge || "";
  $("badge-copy").dir = isRightToLeft(locale) ? "rtl" : "auto";
  for (const [id, key] of Object.entries(controls)) {
    const control = $(id);
    const value = screen.style[key] ?? deviceDefaults[key];
    if (control.type === "checkbox") control.checked = Boolean(value);
    else control.value = value;
  }
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
  const screen = getCurrent();
  if (locale !== requestedLocale && hasSavedCaptions(screen, requestedLocale)) {
    locale = requestedLocale;
    comparing = false;
  }
  if (locale !== "en-US" && !hasCaptionText(getLocale(screen)) && hasCaptionText(getLocale(screen, "en-US"))) {
    locale = "en-US";
  }
  const caption = getLocale(screen);
  if (caption.translatedFrom) {
    const source = getLocale(screen, "en-US");
    for (const field of captionFields) {
      if (!caption[field].trim() && !Object.hasOwn(caption.translatedFrom, field)) caption[field] = source[field];
    }
  }
  renderSettings();
  renderList();
  renderGallery();
  return renderCanvas();
}
function changeDesign() {
  persist();
  renderGallery();
  renderCanvas();
}
function addCaptionLanguage(code) {
  if (project.locales.includes(code)) return;
  project.locales.push(code);
  for (const screen of project.screens) {
    screen.locales[code] = {headline: "", subtitle: "", capture: null, previous: null};
  }
}
function screenName(name) {
  return name.replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ").trim() || "Screenshot";
}
async function captureFrom(file) {
  if (file.size > 25 * 1024 * 1024) throw new Error("Screenshots must be 25 MB or smaller.");
  if (!["image/png", "image/jpeg", "image/webp"].includes(file.type)
    && !(file.type === "" && /\.(png|jpe?g|webp)$/i.test(file.name))) throw new Error("Choose a PNG, JPEG, or WebP image.");
  const extension = file.name.split(".").pop().toLowerCase();
  const type = file.type || (extension.startsWith("jp") ? "image/jpeg" : "image/" + extension);
  const capture = {id: newID(), bytes: await file.arrayBuffer(), type};
  const image = await imageFor(capture);
  if (image.width * image.height > 32_000_000) throw new Error("This image exceeds 32 megapixels. Resize it before importing.");
  return capture;
}
async function importFiles(files, replace) {
  if (!files.length || busy) return;
  const target = getCurrent(), code = replace ? requestedLocale : locale;
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
          addCaptionLanguage(code);
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
      await persist(true);
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
function asImage(canvas, type, quality) {
  return new Promise((resolve, reject) => canvas.toBlob(
    blob => blob?.type === type ? resolve(blob) : reject(new Error("The image could not be encoded.")), type, quality,
  ));
}
async function renderImage(screen, code, target, spread, format = "png") {
  const imageScreen = spread?.lead || screen;
  const capture = spread ? spread.capture : actualCapture(screen, code);
  if (!capture && (getLocale(imageScreen, code).capture || getLocale(imageScreen, "en-US").capture)) {
    throw new Error("The screenshot is missing. Use Replace capture before exporting.");
  }
  const canvas = document.createElement("canvas");
  const [image] = await Promise.all([imageFor(capture), loadCaptionFonts(screen, code)]);
  if (spread) spread.image = image;
  draw(canvas, screen, code, target, image, 1, spread);
  try {
    if (format === "jpg") return await asImage(canvas, "image/jpeg", .96);
    const blob = await asImage(canvas, "image/png");
    const type = new Uint8Array(await blob.slice(24, 26).arrayBuffer());
    if (type[0] === 8 && type[1] === 2) return blob;
    return await encodeRGB(canvas);
  } finally {
    canvas.width = 1;
    canvas.height = 1;
  }
}
function filename(name) {
  return name.normalize("NFKD").replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "").slice(0, 56).toLowerCase() || "screenshot";
}
function entryFor(screen, code, target, index, format = "png") {
  const [, w, h] = sizes[target];
  const signature = [index, screen.name, screen.style, getLocale(screen, code).headline,
    getLocale(screen, code).subtitle, getLocale(screen, code).badge || "", actualCapture(screen, code)?.id || "sample-placeholder"];
  if (screen.style.align === "left" && isRightToLeft(code)) signature.push("left-alignment");
  if (actualCapture(screen, code)) signature.push("high-quality-resampling");
  const spread = spreadFor(project.screens, index, code, target);
  signature.push("text-fitting-v2");
  if (spread) signature.push(spread.half, spread.lead.style, spread.capture?.id);
  return {
    key: `${screen.id}:${code}:${target}:${format}`,
    signature: JSON.stringify(signature),
    name: `exports/${code}/${target}-${w}x${h}/${String(index + 1).padStart(2, "0")}_${filename(screen.name)}.${format}`,
    screen, code, target, spread, format,
  };
}
const crcTable = Uint32Array.from({length: 256}, (_, byte) => {
  let value = byte;
  for (let bit = 0; bit < 8; bit++) value = value & 1 ? 0xedb88320 ^ (value >>> 1) : value >>> 1;
  return value;
});
function crc32(bytes) {
  let crc = 0xffffffff;
  for (const value of bytes) crc = (crc >>> 8) ^ crcTable[(crc ^ value) & 255];
  return (crc ^ 0xffffffff) >>> 0;
}
function pngChunk(type, payload) {
  const bytes = new Uint8Array(payload.length + 12);
  const view = new DataView(bytes.buffer);
  view.setUint32(0, payload.length);
  bytes.set(new TextEncoder().encode(type), 4);
  bytes.set(payload, 8);
  view.setUint32(payload.length + 8, crc32(bytes.subarray(4, payload.length + 8)));
  return bytes;
}
async function encodeRGB(canvas) {
  if (!globalThis.CompressionStream) throw new Error("This browser couldn’t encode an opaque RGB PNG. Try exporting in a current browser.");
  const {width, height} = canvas;
  const pixels = canvas.getContext("2d").getImageData(0, 0, width, height).data;
  const rows = new Uint8Array((width * 3 + 1) * height);
  let input = 0, output = 0;
  for (let y = 0; y < height; y++) {
    rows[output++] = 1;
    for (let x = 0; x < width; x++) {
      for (let channel = 0; channel < 3; channel++) {
        rows[output++] = pixels[input + channel] - (x ? pixels[input + channel - 4] : 0);
      }
      input += 4;
    }
  }
  const stream = new Blob([rows]).stream().pipeThrough(new CompressionStream("deflate"));
  const compressed = new Uint8Array(await new Response(stream).arrayBuffer());
  const header = new Uint8Array(13);
  const view = new DataView(header.buffer);
  view.setUint32(0, width);
  view.setUint32(4, height);
  header[8] = 8;
  header[9] = 2;
  return new Blob([new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]),
    pngChunk("IHDR", header), pngChunk("IDAT", compressed), pngChunk("IEND", new Uint8Array())], {type: "image/png"});
}
function zip(files) {
  const local = [], directory = [];
  const encoder = new TextEncoder();
  let offset = 0, directorySize = 0;
  for (const {name, blob, crc} of files) {
    const path = encoder.encode(name);
    if (offset + blob.size + path.length + 30 > 0xffffffff) throw new Error("This ZIP exceeds 4 GB. Export fewer sizes or languages at a time.");
    const header = new DataView(new ArrayBuffer(30));
    header.setUint32(0, 0x04034b50, true);
    header.setUint16(4, 20, true);
    header.setUint16(6, 0x800, true);
    header.setUint16(12, 33, true);
    header.setUint32(14, crc, true);
    header.setUint32(18, blob.size, true);
    header.setUint32(22, blob.size, true);
    header.setUint16(26, path.length, true);
    local.push(header.buffer, path, blob);
    const central = new DataView(new ArrayBuffer(46));
    central.setUint32(0, 0x02014b50, true);
    central.setUint16(4, 20, true);
    new Uint8Array(central.buffer, 6, 26).set(new Uint8Array(header.buffer, 4, 26));
    central.setUint32(42, offset, true);
    directory.push(central.buffer, path);
    directorySize += 46 + path.length;
    offset += 30 + path.length + blob.size;
  }
  if (offset + directorySize + 22 > 0xffffffff) throw new Error("This ZIP exceeds 4 GB. Export fewer sizes or languages at a time.");
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
  $("export-note").textContent = project.demo ? "This set includes sample app screens." : "Exports are grouped by language and device. Feature graphics use the first selected slide.";
  $("export-dialog").showModal();
}
async function exportBatch(event) {
  event.preventDefault();
  if (busy) return;
  const checked = id => [...$(id).querySelectorAll("input:checked")].map(input => input.value);
  const format = $("export-format").value;
  const targets = checked("export-sizes"), codes = checked("export-locales");
  const selectedScreens = new Set(checked("export-screens"));
  if (!targets.length || !codes.length || !selectedScreens.size) {
    $("export-note").textContent = "Choose at least one output size, language, and screen.";
    return;
  }
  if (targets.some(target => target.startsWith("android")) && selectedScreens.size > 8) {
    $("export-note").textContent = "Google Play accepts up to 8 phone screenshots. Uncheck a screen or export the Apple set separately.";
    return;
  }
  const first = project.screens.find(screen => selectedScreens.has(screen.id));
  const entries = codes.flatMap(code => targets.flatMap(target =>
    project.screens.flatMap((screen, index) => selectedScreens.has(screen.id) && (target !== "feature" || screen === first)
      ? [entryFor(screen, code, target, index, format)] : []),
  ));
  const chosen = $("changed").checked ? entries.filter(e => project.exports[e.key] !== e.signature) : entries;
  if (!chosen.length) {
    $("export-note").textContent = "Nothing has changed in this selection since your last export.";
    return;
  }
  const missing = chosen.find(({screen, code}) => code !== "en-US"
    && hasCaptionText(getLocale(screen, "en-US")) && !hasSavedCaptions(screen, code));
  if (missing) {
    $("export-note").textContent = `Translate ${missing.screen.name} into ${languageLabel(missing.code)} before exporting this set.`;
    return;
  }
  busy = true;
  $("export-submit").disabled = true;
  try {
    const files = [];
    let total = 0;
    for (const [index, entry] of chosen.entries()) {
      $("export-note").textContent = `Rendering ${index + 1} of ${chosen.length}…`;
      const image = await renderImage(entry.screen, entry.code, entry.target, entry.spread, entry.format);
      total += image.size;
      if (total > 0xffffffff) throw new Error("This ZIP exceeds 4 GB. Export fewer sizes or languages at a time.");
      files.push({name: entry.name, blob: image, crc: crc32(new Uint8Array(await image.arrayBuffer()))});
    }
    downloadBlob(zip(files), "storeshot-studio.zip");
    for (const entry of chosen) project.exports[entry.key] = entry.signature;
    persist();
    $("export-dialog").close();
    notice(`Downloaded ${files.length} ${format === "jpg" ? "JPEG" : "PNG"} files in a ZIP.`);
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
    downloadBlob(await renderImage(screen, code, target, entry.spread), entry.name.replaceAll("/", "-"));
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
    delete getCurrent().style.accent;
    renderSettings();
    changeDesign();
  };
  $("themes").append(button);
}
for (const [id, key] of Object.entries(controls)) {
  const control = $(id);
  const changeEvent = control.tagName === "SELECT" ? "change" : "input";
  control.addEventListener(changeEvent, event => {
    const value = control.type === "range" ? Number(control.value)
      : control.type === "checkbox" ? control.checked : control.value;
    getCurrent().style[key] = value;
    if (id === "type-scale") $("type-value").value = value + "%";
    changeDesign();
  });
}
function updateCaption(field, value) {
  cancelTranslation();
  const screen = getCurrent();
  const caption = getLocale(screen);
  caption[field] = value;
  if (locale !== "en-US") {
    caption.translatedFrom = false;
    (screen.translationDraft ??= {})[field] = value;
  } else if (screen.translationDraft) {
    delete screen.translationDraft[field];
  }
  syncCaptionInputs(field, value);
  changeDesign();
}
for (const field of captionFields) {
  $(field).oninput = event => updateCaption(field, event.target.value);
}
$("badge-copy").oninput = event => {
  cancelTranslation();
  getLocale(getCurrent()).badge = event.target.value;
  changeDesign();
};
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
  const files = [...event.dataTransfer.files];
  importFiles(files, files.length === 1 && Boolean(event.target.closest(".editable-preview")));
});
$("size").onchange = event => { size = event.target.value; changeDesign(); };
$("gallery-zoom").oninput = event => {
  $("gallery-zoom-value").value = event.target.value + "%";
  renderGallery();
  persist();
};
$("gallery").ondragover = event => { if (event.dataTransfer.types.includes("Files")) event.preventDefault(); };
$("gallery").ondrop = event => {
  const files = [...event.dataTransfer.files];
  if (!files.length) return;
  event.preventDefault();
  importFiles(files, false);
};
$("panorama-mode").onchange = event => {
  project.panoramic = event.target.checked;
  comparing = false;
  changeDesign();
};
$("locale").onchange = event => {
  const code = event.target.value;
  if ((busy && !translationController) || (!languageChoices.includes(code) && !project.locales.includes(code))) {
    event.target.value = requestedLocale;
    return;
  }
  cancelTranslation();
  requestedLocale = code;
  if (nativeTarget(code) === "en") {
    const source = getLocale(getCurrent(), "en-US");
    addCaptionLanguage(code);
    if (code !== "en-US" && !hasSavedCaptions(getCurrent(), code)) {
      const captions = getLocale(getCurrent(), code);
      for (const field of captionFields) captions[field] = source[field];
    }
    locale = code;
  }
  comparing = false;
  render();
  persist();
  checkTranslationSupport(code);
};
$("compare").onclick = () => { comparing = !comparing; renderCanvas(); };
const quickEditor = $("quick-editor");
const captionButtons = {headline: $("canvas-caption"), subtitle: $("canvas-subtitle")};
let activeCaptionButton;
function closeQuickEditor() {
  quickEditor.hidden = true;
  activeCaptionButton?.setAttribute("aria-expanded", "false");
}
for (const field of captionFields) {
  const editor = $("quick-" + field);
  const button = captionButtons[field];
  button.onclick = () => {
    closeQuickEditor();
    activeCaptionButton = button;
    button.setAttribute("aria-expanded", "true");
    quickEditor.hidden = false;
    editor.focus({preventScroll: true});
    editor.select();
  };
  editor.oninput = event => updateCaption(field, event.target.value);
}
document.addEventListener("focusin", event => {
  if (!quickEditor.hidden && !event.target.closest("#quick-editor, #headline, #subtitle")) closeQuickEditor();
});
$("quick-done").onclick = () => { activeCaptionButton?.focus(); closeQuickEditor(); };
quickEditor.onkeydown = event => {
  if (event.key === "Escape") $("quick-done").click();
};
$("earlier").onclick = () => move(-1);
$("later").onclick = () => move(1);
$("template").replaceChildren(...Object.entries(templates).map(([id, [label]]) => makeOption(label, id)));
$("apply-template").onclick = () => {
  const [label, style, panoramic] = templates[$("template").value];
  const [, background, , ink] = themes[style.theme];
  for (const screen of project.screens) {
    screen.style = {...baseStyle, background, ink, ...style};
  }
  project.panoramic = panoramic;
  comparing = false;
  render();
  persist();
  notice(`${label} applied to all slides.`);
};
$("apply-brand").onclick = () => {
  for (const screen of project.screens) {
    Object.assign(screen.style, {
      background: $("brand-primary").value, accent: $("brand-secondary").value,
      font: $("brand-font").value, subtitleFont: "sans", mesh: $("brand-mesh").checked,
    });
  }
  render();
  persist();
  notice("Brand kit applied to all slides.");
};
$("apply").onclick = () => {
  const style = {...getCurrent().style};
  for (const screen of project.screens) screen.style = {...style};
  persist();
  notice("Style applied to all screens. Captions and captures kept.");
};
$("duplicate").onclick = () => {
  cancelTranslation();
  const clone = structuredClone(getCurrent());
  clone.id = newID();
  clone.name += " copy";
  project.screens.splice(++selected, 0, clone);
  comparing = false;
  persist();
  render();
};
$("remove").onclick = () => {
  cancelTranslation();
  project.screens.splice(selected, 1);
  selected = Math.min(selected, project.screens.length - 1);
  comparing = false;
  persist();
  render();
};
function hasCaptionText(caption) {
  return Boolean(caption && localizedFields.some(field => caption[field]?.trim()));
}
function hasSavedCaptions(screen, code) {
  const caption = getLocale(screen, code);
  if (!hasCaptionText(caption) || caption.translatedFrom === null) return false;
  if (caption.translatedFrom !== undefined) return true;
  const source = getLocale(screen, "en-US");
  return localizedFields.some(field => caption[field]?.trim() && caption[field] !== source[field]);
}
function translationSourceLocale() {
  return nativeTarget(locale) === "en" ? locale : "en-US";
}
function captionContext() {
  return Object.fromEntries(Object.entries(contextFields).map(([id, key]) => [key, $(id).value.trim()]));
}
async function requestCaptionBatch(action, sourceLocale, targetLocale, entries, signal) {
  const captions = entries.map(({screen, field, source}, index) => ({
    id: String(index), slide: project.screens.indexOf(screen) + 1, field, text: source,
  }));
  const payload = JSON.stringify({action, sourceLocale, targetLocale, captions, context: captionContext()});
  const send = () => fetch(captionEndpoint, {
    method: "POST", headers: {"Content-Type": "application/json"}, body: payload, signal,
  });
  let response = await send();
  if (response.status >= 500 && !signal.aborted) {
    await response.body?.cancel();
    response = await send();
  }
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new Error(data?.error || "The caption service is unavailable. Try again.");
  if (!Array.isArray(data?.captions) || data.captions.length !== entries.length ||
      data.captions.some((caption, index) => caption?.id !== String(index) || typeof caption.text !== "string" || !caption.text.trim())) {
    throw new Error("The service returned an incomplete caption set. Try again.");
  }
  return data.captions.map(caption => caption.text.trim());
}
for (const id of Object.keys(contextFields)) {
  $(id).oninput = () => { project.captionContext = captionContext(); persist(); };
}
$("magic-draft").onclick = async () => {
  if (!captionEndpoint || busy) return;
  if (!$("app-description").value.trim()) {
    $("app-description").focus();
    notice("Describe the app before generating copy.");
    return;
  }
  const entries = project.screens.flatMap(screen => captionFields.filter(field =>
    !getLocale(screen, "en-US")[field].trim()).map(field => ({screen, field})));
  if (!entries.length) return notice("Every English caption already has text.");
  busy = true;
  $("magic-draft").disabled = true;
  notice("Generating draft copy…");
  try {
    const results = await requestCaptionBatch("draft", "en-US", "en-US", entries, AbortSignal.timeout(55_000));
    for (const [index, {screen, field}] of entries.entries()) {
      if (!project.screens.includes(screen)) continue;
      const caption = getLocale(screen, "en-US");
      if (!caption[field].trim()) caption[field] = results[index];
    }
    render();
    persist();
    notice("Draft copy added to empty English captions.");
  } catch (error) {
    notice(error.message || "Copy generation didn’t finish. Try again.");
  } finally {
    busy = false;
    $("magic-draft").disabled = false;
  }
};
function openTranslation() {
  const screen = getCurrent();
  const source = {...getLocale(screen, translationSourceLocale()), ...screen.translationDraft};
  for (const field of captionFields) $("source-" + field).value = source[field];
  $("translate-summary").textContent = `Translate English captions into ${languageLabel(requestedLocale)} on this device. The first translation may download a language pack.`;
  $("translate-manually").hidden = true;
  $("translation-panel").hidden = false;
  $("translate-options").hidden = false;
}
function editTranslationManually() {
  const source = getLocale(getCurrent());
  addCaptionLanguage(requestedLocale);
  if (!hasSavedCaptions(getCurrent(), requestedLocale)) {
    const captions = getLocale(getCurrent(), requestedLocale);
    for (const field of captionFields) captions[field] = source[field];
    captions.translatedFrom = false;
  }
  locale = requestedLocale;
  comparing = false;
  persist();
  $("translation-panel").hidden = true;
  render();
  $("headline").focus();
}
$("translate-manually").onclick = editTranslationManually;
$("translate").onclick = () => {
  if (busy) return;
  if (!canTranslateLocale(requestedLocale)) return editTranslationManually();
  openTranslation();
  translateCaptions();
};

function translateLocally(code, modelInfo, texts, signal, progress) {
  return new Promise((resolve, reject) => {
    if (signal.aborted) return reject(signal.reason);
    const worker = new Worker("translation-worker.js?v=6", {type: "module"});
    let timeout;
    function finish(callback, value) {
      clearTimeout(timeout);
      worker.terminate();
      signal.removeEventListener("abort", cancel);
      callback(value);
    }
    function cancel() {
      finish(reject, signal.reason);
    }
    function waitForWorker() {
      clearTimeout(timeout);
      timeout = setTimeout(() => finish(reject, new Error("Translation timed out. Try again.")), 120000);
    }
    signal.addEventListener("abort", cancel, {once: true});
    worker.onerror = () => finish(reject, new Error("The translation engine couldn’t load. Check your connection and try again."));
    worker.onmessage = ({data}) => {
      waitForWorker();
      if (data.results) finish(resolve, data.results);
      else if (data.error) finish(reject, new Error("The language pack couldn’t load or run on this device."));
      else if (Number.isFinite(data.progress)) progress(`Downloading language pack · ${data.progress}%`);
      else if (Number.isInteger(data.completed)) progress(`Translating caption ${data.completed + 1} of ${data.total}…`);
    };
    waitForWorker();
    worker.postMessage({...modelInfo, texts, traditional: code === "zh-Hant"});
  });
}

function isCaptionTranslation(source, translated) {
  if (typeof translated !== "string" || !translated.trim()) return false;
  const sourceLength = Array.from(source.trim()).length;
  const translatedLength = Array.from(translated.trim()).length;
  return translatedLength <= Math.max(24, sourceLength * 3 + 6);
}

function isUnchangedCaption(source, translated) {
  const words = text => text.normalize("NFC").toLowerCase().match(/[\p{L}\p{N}]+/gu)?.join(" ");
  return /[a-z]/i.test(source) && words(source) === words(translated);
}

async function translateWithModel(code, texts, signal, progress) {
  let nativeResults;
  if (globalThis.Translator && !unsupportedNativeLanguages.has(nativeTarget(code))) {
    let translator;
    try {
      translator = await globalThis.Translator.create({
        sourceLanguage: "en", targetLanguage: nativeTarget(code), signal,
        monitor(monitor) {
          monitor.addEventListener("downloadprogress", event =>
            progress(`Downloading language pack · ${Math.round(event.loaded * 100)}%`));
        },
      });
      const results = [];
      for (const [index, text] of texts.entries()) {
        progress(`Translating caption ${index + 1} of ${texts.length}…`);
        const result = await translator.translate(text, {signal});
        if (!isCaptionTranslation(text, result)) {
          throw new Error("The translation was empty or too long for the source caption.");
        }
        results.push(result.trim());
      }
      if (!results.some((result, index) => isUnchangedCaption(texts[index], result))) return results;
      nativeResults = results;
    } catch (error) {
      if (!localModel(code) || signal.aborted) throw error;
    } finally {
      translator?.destroy?.();
    }
  }
  const model = localModel(code);
  if (!model || !globalThis.Worker || !globalThis.WebAssembly) {
    if (nativeResults) return nativeResults;
    throw new Error("Automatic translation is unavailable for this language in your browser.");
  }
  progress(model.targetLanguage
    ? "Preparing a shared multilingual pack. The first download is about 630 MB."
    : "Preparing the language pack. The first download may take a minute.");
  if (!nativeResults) return translateLocally(code, model, texts, signal, progress);
  const retry = texts.filter((text, index) => isUnchangedCaption(text, nativeResults[index]));
  try {
    const results = await translateLocally(code, model, retry, signal, progress);
    const bySource = new Map(retry.map((text, index) => [text, results[index]]));
    return texts.map((text, index) => {
      const result = bySource.get(text);
      return isCaptionTranslation(text, result) ? result : nativeResults[index];
    });
  } catch (error) {
    if (signal.aborted) throw error;
    return nativeResults;
  }
}

// Short interface captions often lack enough context for the local model.
const shortCaptions = {
  tr: {hello: "merhaba", hi: "selam", test: "test", merhaba: "merhaba", "start here": "buradan başlayın", "thank you": "teşekkür ederim"},
  ur: {hello: "سلام", hi: "سلام", test: "ٹیسٹ", "start here": "یہاں سے شروع کریں", "thank you": "شکریہ"},
  vi: {hello: "xin chào", hi: "chào bạn", test: "thử nghiệm", "start here": "bắt đầu tại đây", "thank you": "cảm ơn"},
};
async function translateTexts(code, texts, signal, progress) {
  const phrases = shortCaptions[code];
  if (!phrases) return translateWithModel(code, texts, signal, progress);
  const exact = new Map();
  for (const text of texts) {
    const match = /^(.+?)([.!?]*)$/u.exec(text.trim());
    if (!match) continue;
    const [, word, punctuation] = match;
    const key = word.toLowerCase().replace(/\s+/g, " ");
    if (!Object.hasOwn(phrases, key)) continue;
    const result = phrases[key];
    const caption = /^[A-Z]/.test(word) ? result[0].toLocaleUpperCase(code) + result.slice(1) : result;
    exact.set(text, caption + punctuation);
  }
  const remaining = texts.filter(text => !exact.has(text));
  if (remaining.length) {
    const results = await translateWithModel(code, remaining, signal, progress);
    remaining.forEach((text, index) => exact.set(text, results[index]));
  }
  return texts.map(text => exact.get(text));
}

let translationController;
async function translateCaptions() {
  if (busy || !canTranslateLocale(requestedLocale)) return;
  const target = requestedLocale;
  const current = getCurrent();
  const sourceLocale = translationSourceLocale();
  const edited = Object.fromEntries(captionFields.map(field => [field, $("source-" + field).value]));
  const screens = $("translate-all").checked ? [...project.screens] : [current];
  const entries = screens.flatMap(screen => localizedFields.map(field => ({
    screen, field,
    source: (screen === current && field !== "badge" ? edited : getLocale(screen, sourceLocale))[field] || "",
  })));
  const active = entries.filter(entry => entry.source.trim());
  const texts = [...new Set(active.map(entry => entry.source))];
  const summary = $("translate-summary");
  const submit = $("translate-submit");
  if (!texts.length) {
    summary.textContent = "Enter an English headline or supporting text here, then click Translate.";
    return;
  }
  translationController = new AbortController();
  const {signal} = translationController;
  busy = true;
  $("translate-options").hidden = true;
  submit.disabled = true;
  $("translate-manually").hidden = true;
  $("translate-all").disabled = true;
  for (const field of captionFields) $("source-" + field).disabled = true;
  try {
    const progress = message => { summary.textContent = message; };
    let results;
    if (captionEndpoint) {
      progress("Translating with your app context…");
      results = await requestCaptionBatch("translate", sourceLocale, target, active,
        AbortSignal.any([signal, AbortSignal.timeout(55_000)]));
    } else {
      const local = await translateTexts(target, texts, signal, progress);
      const byText = new Map(texts.map((text, index) => [text, local[index]]));
      results = active.map(entry => byText.get(entry.source));
    }
    if (signal.aborted) throw signal.reason;
    if (results.length !== active.length || active.some(({source}, index) =>
      captionEndpoint ? !results[index]?.trim() : !isCaptionTranslation(source, results[index]))) {
      throw new Error("The translation service returned incomplete or unusually long text. Try again.");
    }
    let unchanged = 0;
    addCaptionLanguage(target);
    for (const [index, {screen, field, source}] of active.entries()) {
      const caption = getLocale(screen, target);
      const result = results[index];
      if (isUnchangedCaption(source, result)) {
        unchanged++;
        if (!caption[field]?.trim() || (caption.translatedFrom && caption.translatedFrom[field] !== source)) {
          caption[field] = source;
          delete caption.translatedFrom?.[field];
        }
        caption.translatedFrom ??= {};
        continue;
      }
      caption[field] = result;
      if (!caption.translatedFrom) caption.translatedFrom = {};
      caption.translatedFrom[field] = source;
    }
    const original = getLocale(current, sourceLocale);
    const draft = Object.fromEntries(captionFields.filter(field => edited[field] !== original[field]).map(field => [field, edited[field]]));
    if (Object.keys(draft).length) current.translationDraft = draft;
    else delete current.translationDraft;
    locale = target;
    comparing = false;
    persist();
    $("translation-panel").hidden = true;
    render();
    if (unchanged) {
      notice(unchanged === active.length ? `The wording stayed the same in ${languageLabel(target)}. You can edit the captions directly.`
        : "Some captions stayed the same. Review both captions before exporting.");
    } else {
      notice("Captions translated. Review them before exporting.");
    }
  } catch (error) {
    if (signal.aborted) $("translation-panel").hidden = true;
    else {
      summary.textContent = error.message || "Translation didn’t finish. Try again.";
      $("translate-manually").hidden = false;
      checkTranslationSupport(target);
    }
  } finally {
    translationController = null;
    $("translate-options").hidden = false;
    submit.disabled = false;
    $("translate-all").disabled = false;
    for (const field of captionFields) $("source-" + field).disabled = false;
    busy = false;
  }
}
$("translate-form").onsubmit = event => {
  event.preventDefault();
  translateCaptions();
};
function cancelTranslation() {
  if (translationController) translationController.abort();
  $("translation-panel").hidden = true;
}
$("cancel-translate").onclick = cancelTranslation;
$("download").onclick = exportCurrent;
$("batch").onclick = openExport;
$("export-form").onsubmit = exportBatch;
for (const close of document.querySelectorAll("[data-close]")) {
  close.onclick = () => { if (!busy) $(close.dataset.close).close(); };
}
$("export-dialog").addEventListener("cancel", event => { if (busy) event.preventDefault(); });
async function loadSavedWorkspace() {
  let timeout;
  let opened;
  let expired = false;
  try {
    return await Promise.race([
      (async () => {
        opened = await openStorage();
        if (expired) {
          opened.close();
          return;
        }
        return {db: opened, stored: await readProject(opened)};
      })(),
      new Promise((_, reject) => {
        timeout = setTimeout(() => {
          expired = true;
          opened?.close();
          reject(new Error("Local project loading timed out."));
        }, 2500);
      }),
    ]);
  } finally {
    clearTimeout(timeout);
  }
}
function isSavedProject(stored) {
  return Array.isArray(stored.screens) && stored.screens.length > 0
    && Array.isArray(stored.locales) && stored.locales.includes("en-US")
    && stored.screens.every(screen => screen?.style && stored.locales.every(code => {
      const caption = screen.locales?.[code];
      return caption && captionFields.every(field => typeof caption[field] === "string");
    }));
}
function restoreBackup(backup, stored) {
  const savedCaptures = new Map();
  for (const screen of stored?.screens || []) {
    for (const caption of Object.values(screen.locales)) {
      for (const field of captureFields) {
        const capture = caption[field];
        if (hasCaptureData(capture)) savedCaptures.set(capture.id, capture);
      }
    }
  }
  for (const screen of backup.screens) {
    for (const caption of Object.values(screen.locales)) {
      for (const field of captureFields) {
        const capture = caption[field];
        if (!capture) continue;
        const saved = savedCaptures.get(capture.id);
        if (saved) caption[field] = saved;
      }
    }
  }
}
function hasMissingCaptures(workspace) {
  return workspace.screens.some(screen => Object.values(screen.locales).some(caption =>
    captureFields.some(field => caption[field] && !hasCaptureData(caption[field]))));
}
async function initialize() {
  let stored;
  try {
    const {db, stored: savedProject} = await loadSavedWorkspace();
    if (savedProject && !isSavedProject(savedProject)) {
      db.close();
      throw new Error("The saved workspace could not be restored.");
    }
    stored = savedProject;
    database = db;
  } catch {
    // Caption recovery can still use the browser's lightweight backup.
  }
  const backup = readBackup();
  const useBackup = backup && (!stored || (backup.savedAt || 0) > (stored.savedAt || 0));
  if (useBackup) {
    restoreBackup(backup, stored);
    stored = backup;
  }
  if (stored) {
    project = stored;
    clearLegacySampleCaptions(project);
    const view = project.view;
    selected = Math.max(0, project.screens.findIndex(screen => screen.id === view?.screen));
    if (project.locales.includes(view?.locale)) locale = view.locale;
    requestedLocale = view?.requestedLocale || locale;
    if (canTranslateLocale(locale) && !hasSavedCaptions(getCurrent(), locale)) locale = "en-US";
    if (Object.hasOwn(sizes, view?.size)) size = view.size;
    if (view?.zoom >= 65 && view.zoom <= 160) {
      $("gallery-zoom").value = view.zoom;
      $("gallery-zoom-value").value = view.zoom + "%";
    }
  }
  $("copy-context").hidden = !captionEndpoint;
  for (const [id, key] of Object.entries(contextFields)) $(id).value = project.captionContext?.[key] || "";
  render();
  if (stored) {
    if (database && !useBackup) writeBackup();
    storageNotice(hasMissingCaptures(project)
      ? "Recovered captions and settings. Some uploaded images couldn’t be restored."
      : "Saved in this browser.");
  } else if (!database) {
    storageNotice("Local project storage couldn’t open. The editor will try to save captions as you type.");
  }
  checkTranslationSupport(requestedLocale);
  $("workbench").hidden = false;
  $("editor-loading").hidden = true;
  $("upload").disabled = false;
}
initialize().catch(error => {
  console.error("StoreShot editor failed to start", error);
  $("editor-loading").textContent = "The editor couldn’t start. Reload this page in a regular browser tab to try again.";
});
