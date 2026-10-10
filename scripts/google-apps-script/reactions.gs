/**
 * Stakich Websites: likes, reactions, and comments.
 *
 * Paste this whole file into Extensions > Apps Script on a Google Sheet,
 * then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
 * The "Reactions" and "Comments" tabs are created automatically.
 * To hide a comment, tick its box in the "Hide" column.
 * Visitors can edit or delete their own comments from the same browser.
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

function doPost(e) {
  let data;
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return json({ ok: false, error: 'Bad request.' });
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
