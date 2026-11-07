/**
 * Stakich Websites: likes, reactions, and comments.
 *
 * Paste this whole file into Extensions > Apps Script on a Google Sheet,
 * then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
 * The "Reactions" and "Comments" tabs are created automatically.
 * To hide a comment, tick its box in the "Hide" column.
 * Visitors can edit or delete their own comments from the same browser.
 * Order-form and quote emails also come through this script (type "order").
 * Photo uploads after payment use type "photos". Each business gets a folder
 * in Google Drive named "Stakich orders", and the email has a link to each file.
 * Mail goes out from the Google account that deployed it. Redeploy after editing
 * (Deploy > Manage deployments > Edit > New version) or the live URL keeps the old code.
 * Adding Drive means Google will ask you to allow Drive access when you deploy.
 */
const REACTIONS = ['like', 'love', 'care', 'haha', 'wow'];
const MAX_NAME = 40;
const MAX_TEXT = 600;
const MAX_COMMENTS_PER_HOUR = 30;
const SITE_NAME = 'stakichwebsites.com';

function doGet(e) {
  const keys = String((e && e.parameter && e.parameter.keys) || '')
    .split(',')
    .map(cleanKey)
    .filter(Boolean)
    .slice(0, 40);
  return json(readData(keys));
}

const ORDER_TO = 'jeremy@stakichwebsites.com';
const CUSTOMER_NOTE = "Thanks, I have your answers! If you haven't paid yet, you can finish here: https://stakichwebsites.com/pay. After you pay, send your logo and photos here: https://stakichwebsites.com/photos. I start building right away, using your answers, photos, and your Facebook and Google pages. I'll send you a link to see your website, usually within 1 to 2 weeks. Questions? Just reply to this email or text (423) 227-7681.\n\nJeremy, Stakich Websites";
const ORDER_LABELS = {
  plan: 'Plan',
  name: 'Name',
  business: 'Business',
  phone: 'Phone',
  email: 'Email',
  contact_by: 'Best way to reach them',
  business_type: 'Type of work',
  service_area: 'Service area',
  business_address: 'Address',
  services: 'Services',
  business_hours: 'Hours',
  facebook_page: 'Facebook',
  google_profile: 'Google',
  domain: 'Domain',
  domain_wanted: 'Domain name',
  has_logo: 'Has a logo',
  has_photos: 'Has photos',
  preview_link: 'Preview',
  current_site: 'Current website',
  message: 'Message',
  notes: 'Notes',
  agreed_to_terms: 'Agreed to terms',
  order_ref: 'Order ref',
  section_finished: 'Section finished',
  note: 'Note',
};

function emailOk(value) {
  value = String(value || '').trim();
  return value.length < 120 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function sendOrder(data) {
  if (data.honey) return { ok: true };
  const subject = String(data.subject || 'Website form').replace(/[\r\n]/g, ' ').slice(0, 180);
  const fields = data.fields && typeof data.fields === 'object' ? data.fields : {};
  const lines = [];
  Object.keys(fields).slice(0, 40).forEach(function (key) {
    if (!/^[a-z0-9_]{1,40}$/.test(key)) return;
    const value = String(fields[key] || '').replace(/[\r\n]+/g, ' ').trim().slice(0, 2000);
    if (!value) return;
    lines.push((ORDER_LABELS[key] || key) + ': ' + value);
  });
  if (!lines.length) return { ok: false, error: 'Empty.' };

  const cache = CacheService.getScriptCache();
  const hour = Number(cache.get('order-hour') || 0);
  if (hour >= 40) return { ok: false, error: 'Busy.' };

  const reply = emailOk(data.replyTo) ? String(data.replyTo).trim() : '';
  const body = lines.join('\n');
  const stamp = Utilities.base64EncodeWebSafe(
    Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, subject + '\n' + body)
  ).slice(0, 24);
  if (cache.get('ord:' + stamp)) return { ok: true };

  const attachments = [];
  let total = 0;
  (Array.isArray(data.files) ? data.files : []).slice(0, 4).forEach(function (file) {
    try {
      const name = String(file.name || 'file').replace(/[^\w.\- ]/g, '').slice(0, 80) || 'file';
      const bytes = Utilities.base64Decode(String(file.data || ''));
      if (!bytes.length || bytes.length > 1200000 || total + bytes.length > 4000000) return;
      total += bytes.length;
      attachments.push(Utilities.newBlob(bytes, String(file.type || 'application/octet-stream').slice(0, 80), name));
    } catch (err) {}
  });

  const mail = { to: ORDER_TO, subject: subject, body: body };
  if (reply) mail.replyTo = reply;
  if (attachments.length) mail.attachments = attachments;
  MailApp.sendEmail(mail);
  if (data.customerCopy === true && reply) {
    try {
      MailApp.sendEmail({
        to: reply,
        subject: 'I have your answers, Stakich Websites',
        body: CUSTOMER_NOTE,
        replyTo: ORDER_TO,
      });
    } catch (err) {}
  }
  cache.put('ord:' + stamp, '1', 180);
  cache.put('order-hour', String(hour + 1), 3600);
  try {
    sheet('Orders', ['Time', 'Subject', 'From', 'Details']).appendRow([new Date(), subject, reply, body.slice(0, 5000)]);
  } catch (err) {}
  return { ok: true };
}

function safeBusiness(value) {
  const name = String(value || '').replace(/[\\/:*?"<>|]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 80);
  return name || 'New customer';
}

function ordersRoot() {
  const found = DriveApp.getFoldersByName('Stakich orders');
  return found.hasNext() ? found.next() : DriveApp.createFolder('Stakich orders');
}

function businessFolder(business) {
  const parent = ordersRoot();
  const found = parent.getFoldersByName(business);
  return found.hasNext() ? found.next() : parent.createFolder(business);
}

function fileExt(file) {
  const match = String(file.name || '').match(/\.([a-z0-9]{1,8})$/i);
  if (match) return '.' + match[1].toLowerCase();
  const type = String(file.type || '').toLowerCase();
  if (type.indexOf('png') >= 0) return '.png';
  if (type.indexOf('webp') >= 0) return '.webp';
  if (type.indexOf('gif') >= 0) return '.gif';
  if (type.indexOf('pdf') >= 0) return '.pdf';
  if (type.indexOf('svg') >= 0) return '.svg';
  if (type.indexOf('heic') >= 0) return '.heic';
  if (type.indexOf('jpeg') >= 0 || type.indexOf('jpg') >= 0) return '.jpg';
  return '';
}

function nameTaken(folder, title) {
  const files = folder.getFiles();
  while (files.hasNext()) {
    const name = files.next().getName();
    if (name === title || name.indexOf(title + '.') === 0) return true;
  }
  return false;
}

function countTitled(folder, prefix) {
  let count = 0;
  const files = folder.getFiles();
  while (files.hasNext()) {
    if (files.next().getName().indexOf(prefix) === 0) count++;
  }
  return count;
}

function fileTitle(folder, business, kind) {
  if (kind === 'logo') {
    let title = business + ' logo';
    let n = 2;
    while (nameTaken(folder, title)) {
      title = business + ' logo ' + n;
      n++;
    }
    return title;
  }
  if (kind === 'price') {
    let title = business + ' price list';
    let n = 2;
    while (nameTaken(folder, title)) {
      title = business + ' price list ' + n;
      n++;
    }
    return title;
  }
  return business + ' photo ' + (countTitled(folder, business + ' photo') + 1);
}

function savePhotos(data) {
  if (data.honey) return { ok: true };
  const business = safeBusiness(data.business);
  const cache = CacheService.getScriptCache();
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const folder = businessFolder(business);
    if (data.done === true) {
      const lines = ['Business: ' + business];
      if (data.plan) lines.push('Plan: ' + String(data.plan).slice(0, 40));
      if (emailOk(data.email)) lines.push('Email: ' + String(data.email).trim());
      if (data.ref) lines.push('Order ref: ' + String(data.ref).replace(/[\r\n]/g, '').slice(0, 80));
      lines.push('Folder: ' + folder.getUrl());
      const files = folder.getFiles();
      let count = 0;
      while (files.hasNext()) {
        const file = files.next();
        lines.push(file.getName() + ': ' + file.getUrl());
        count++;
      }
      if (!count) return { ok: true };
      const body = lines.join('\n');
      const subject = ('Photos after payment: ' + business).slice(0, 180);
      const stamp = Utilities.base64EncodeWebSafe(
        Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, subject + '\n' + body)
      ).slice(0, 24);
      if (!cache.get('pic:' + stamp)) {
        MailApp.sendEmail({ to: ORDER_TO, subject: subject, body: body, replyTo: emailOk(data.email) ? String(data.email).trim() : ORDER_TO });
        cache.put('pic:' + stamp, '1', 180);
        try {
          sheet('Orders', ['Time', 'Subject', 'From', 'Details']).appendRow([new Date(), subject, String(data.email || ''), body.slice(0, 5000)]);
        } catch (err) {}
      }
      return { ok: true, folder: folder.getUrl() };
    }

    const kind = data.kind === 'logo' || data.kind === 'price' ? data.kind : 'photo';
    const file = data.file || {};
    const bytes = Utilities.base64Decode(String(file.data || ''));
    if (!bytes.length || bytes.length > 25000000) return { ok: false, error: 'Too big.' };
    const title = fileTitle(folder, business, kind) + fileExt(file);
    const saved = folder.createFile(Utilities.newBlob(bytes, String(file.type || 'application/octet-stream').slice(0, 80), title));
    return { ok: true, name: saved.getName(), url: saved.getUrl() };
  } finally {
    lock.releaseLock();
  }
}

function doPost(e) {
  let data;
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return json({ ok: false, error: 'Bad request.' });
  }
  if (data && data.type === 'order') {
    try {
      return json(sendOrder(data));
    } catch (err) {
      return json({ ok: false, error: 'Mail failed.' });
    }
  }
  if (data && data.type === 'photos') {
    try {
      return json(savePhotos(data));
    } catch (err) {
      return json({ ok: false, error: 'Save failed.' });
    }
  }
  const key = cleanKey(data.key);
  if (!key) return json({ ok: false, error: 'Bad request.' });

  let mine = null;
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    if (data.type === 'react') {
      react(key, data.add, data.remove);
    } else if (data.type === 'comment') {
      const result = addComment(key, data);
      if (!result.ok) return json(result);
      mine = result.mine || null;
    } else if (data.type === 'edit' || data.type === 'delete') {
      const result = changeComment(key, data);
      if (!result.ok) return json(result);
    } else {
      return json({ ok: false, error: 'Bad request.' });
    }
  } finally {
    lock.releaseLock();
  }
  const out = readData([key]);
  out.ok = true;
  if (mine) out.mine = mine;
  return json(out);
}

function cleanKey(k) {
  k = String(k || '').trim().toLowerCase();
  return /^[a-z0-9:-]{1,60}$/.test(k) ? k : '';
}

function sheet(name, header) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(header);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, header.length).setFontWeight('bold');
  }
  return sh;
}

function reactionSheet() {
  return sheet('Reactions', ['Page'].concat(REACTIONS));
}

const COMMENT_HEADER = ['Time', 'Page', 'Name', 'Comment', 'Hide', 'ID', 'Key', 'Edited'];

function commentSheet() {
  const sh = sheet('Comments', COMMENT_HEADER);
  if (sh.getLastColumn() < COMMENT_HEADER.length) {
    sh.getRange(1, 1, 1, COMMENT_HEADER.length).setValues([COMMENT_HEADER]).setFontWeight('bold');
  }
  return sh;
}

function hashToken(token) {
  return Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(token)));
}

function checkText(text) {
  if (text.length < 2) return 'Please write a comment.';
  if (/https?:\/\/|www\.|\.(com|net|org|ru|xyz)\b/i.test(text)) return "Links aren't allowed in comments.";
  return '';
}

function changeComment(key, data) {
  const id = String(data.id || '');
  const token = String(data.token || '');
  if (!id || !token) return { ok: false, error: 'Bad request.' };
  const sh = commentSheet();
  const rows = sh.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][5] !== id || rows[i][1] !== key) continue;
    if (rows[i][6] !== hashToken(token)) return { ok: false, error: "You can only change your own comments." };
    if (data.type === 'delete') {
      sh.deleteRow(i + 1);
      return { ok: true };
    }
    const text = safe(data.text).slice(0, MAX_TEXT);
    const problem = checkText(text);
    if (problem) return { ok: false, error: problem };
    sh.getRange(i + 1, 4).setValue(text);
    sh.getRange(i + 1, 8).setValue(new Date());
    return { ok: true };
  }
  return { ok: false, error: 'That comment was already removed.' };
}

function react(key, add, remove) {
  const sh = reactionSheet();
  const rows = sh.getDataRange().getValues();
  let row = -1;
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === key) {
      row = i + 1;
      break;
    }
  }
  if (row === -1) {
    sh.appendRow([key].concat(REACTIONS.map(function () { return 0; })));
    row = sh.getLastRow();
  }
  [[add, 1], [remove, -1]].forEach(function (pair) {
    const col = REACTIONS.indexOf(pair[0]);
    if (col === -1) return;
    const cell = sh.getRange(row, col + 2);
    cell.setValue(Math.max(0, (Number(cell.getValue()) || 0) + pair[1]));
  });
}

function safe(s) {
  s = String(s || '').replace(/\s+/g, ' ').trim();
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function addComment(key, data) {
  if (data.website) return { ok: true };
  const name = safe(data.name).slice(0, MAX_NAME);
  const text = safe(data.text).slice(0, MAX_TEXT);
  if (name.length < 1) return { ok: false, error: 'Please add your name.' };
  const problem = checkText(text) || checkText(text + ' ' + name);
  if (problem) return { ok: false, error: problem };

  const cache = CacheService.getScriptCache();
  const dupKey = 'c:' + Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, key + text));
  if (cache.get(dupKey)) return { ok: false, error: 'Looks like you already posted that.' };
  const hourCount = Number(cache.get('hour') || 0);
  if (hourCount >= MAX_COMMENTS_PER_HOUR) return { ok: false, error: 'Lots of comments right now. Please try again later.' };

  const sh = commentSheet();
  const id = Utilities.getUuid();
  const token = Utilities.getUuid();
  sh.appendRow([new Date(), key, name, text, false, id, hashToken(token), '']);
  sh.getRange(sh.getLastRow(), 5).insertCheckboxes();
  cache.put(dupKey, '1', 600);
  cache.put('hour', String(hourCount + 1), 3600);

  try {
    MailApp.sendEmail(
      Session.getEffectiveUser().getEmail(),
      'New comment on ' + SITE_NAME,
      name + ' commented on "' + key + '":\n\n' + text +
        '\n\nTo hide it, open your Google Sheet and tick the box in the Hide column.\n' +
        SpreadsheetApp.getActiveSpreadsheet().getUrl()
    );
  } catch (err) {}
  return { ok: true, mine: { id: id, token: token } };
}

function readData(keys) {
  const counts = {};
  const comments = {};
  if (!keys.length) return { counts: counts, comments: comments };
  const want = {};
  keys.forEach(function (k) {
    want[k] = true;
    counts[k] = {};
    REACTIONS.forEach(function (r) { counts[k][r] = 0; });
    comments[k] = [];
  });

  const rows = reactionSheet().getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (!want[rows[i][0]]) continue;
    REACTIONS.forEach(function (r, j) {
      counts[rows[i][0]][r] = Number(rows[i][j + 1]) || 0;
    });
  }

  const crow = commentSheet().getDataRange().getValues();
  for (let i = crow.length - 1; i >= 1; i--) {
    const k = crow[i][1];
    if (!want[k] || crow[i][4] === true || comments[k].length >= 50) continue;
    comments[k].push({
      id: String(crow[i][5] || ''),
      edited: !!crow[i][7],
      time: crow[i][0] instanceof Date ? crow[i][0].toISOString() : String(crow[i][0]),
      name: String(crow[i][2]).replace(/^'/, ''),
      text: String(crow[i][3]).replace(/^'/, ''),
    });
  }
  return { counts: counts, comments: comments };
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
