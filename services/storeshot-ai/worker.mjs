const outputSchema = {
  type: "object",
  additionalProperties: false,
  required: ["captions"],
  properties: {
    captions: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["id", "text"],
        properties: {id: {type: "string"}, text: {type: "string"}},
      },
    },
  },
};
const instructions = {
  translate: "Write natural app-store screenshot captions in the exact target locale. Translate the benefit and marketing intent in context while preserving facts, proper names, format and product claims. Never invent facts, ratings, users, awards or testimonials. Respect each maxChars limit. Return one caption for each input ID, in order.",
  draft: "Write concise app-store screenshot captions using only claims supported by the supplied app description. Start with the primary user benefit, then cover distinct features and practical reasons to use the app. Never invent social proof, statistics or testimonials. Respect each maxChars limit. Return one caption for each input ID, in order.",
};
function normalizedLocale(value) {
  if (typeof value !== "string" || value.length > 24) return null;
  try { return Intl.getCanonicalLocales(value)[0]; } catch { return null; }
}
function requiredText(value, max) {
  return typeof value === "string" && value.trim() !== "" && Array.from(value).length <= max;
}
async function readRequest(request) {
  const reader = request.body?.getReader();
  if (!reader) throw new Error("Request body required.");
  const chunks = [];
  let length = 0;
  try {
    for (;;) {
      const {done, value} = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > 16_384) {
        await reader.cancel();
        throw new Error("Request exceeds 16 KB.");
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }
  return JSON.parse(await new Blob(chunks).text());
}
function normalize(body) {
  if (!body || !Object.hasOwn(instructions, body.action)) return null;
  const action = body.action;
  const sourceLocale = normalizedLocale(body.sourceLocale);
  const targetLocale = normalizedLocale(body.targetLocale);
  if (!sourceLocale || !targetLocale || (action === "translate" && sourceLocale === targetLocale)) return null;
  const raw = body.captions;
  if (!Array.isArray(raw) || !raw.length || raw.length > 30) return null;
  const ids = new Set();
  const captions = [];
  for (const entry of raw) {
    if (!entry || typeof entry.id !== "string" || !/^[a-z0-9_-]{1,52}$/i.test(entry.id) || ids.has(entry.id)
      || !Number.isInteger(entry.slide) || entry.slide < 1 || entry.slide > 10
      || !["headline", "subtitle", "badge"].includes(entry.field)) return null;
    if (action === "translate" && !requiredText(entry.text, 180)) return null;
    ids.add(entry.id);
    captions.push({
      id: entry.id, field: entry.field, slide: entry.slide,
      maxChars: entry.field === "headline" ? 72 : entry.field === "badge" ? 40 : 125,
      ...(action === "translate" ? {text: entry.text} : {}),
    });
  }
  const context = {};
  for (const [key, max] of [["appName", 80], ["category", 80], ["tone", 80], ["description", 320]]) {
    const value = body.context?.[key];
    if (value != null && (typeof value !== "string" || Array.from(value).length > max)) return null;
    if (value?.trim()) context[key] = value.trim();
  }
  if (action === "draft" && !context.description) return null;
  return {action, sourceLocale, targetLocale, context, captions};
}
async function generate(env, input, signal, fetcher) {
  const response = await fetcher("https://api.openai.com/v1/responses", {
    method: "POST",
    signal,
    headers: {Authorization: `Bearer ${env.OPENAI_API_KEY}`, "Content-Type": "application/json"},
    body: JSON.stringify({
      model: env.OPENAI_MODEL || "gpt-4o-mini",
      store: false,
      max_output_tokens: 2400,
      instructions: instructions[input.action],
      input: JSON.stringify(input),
      text: {format: {type: "json_schema", name: "store_captions", strict: true, schema: outputSchema}},
    }),
  });
  if (!response.ok) throw new Error("Translation service response failed.");
  const responseBody = await response.json();
  if (responseBody.status !== "completed") throw new Error("Translation service returned incomplete output.");
  const content = responseBody.output?.flatMap(item => item.content || []).find(item => item.type === "output_text");
  const result = JSON.parse(content?.text || "null");
  if (!Array.isArray(result?.captions) || result.captions.length !== input.captions.length || result.captions.some((row, index) => {
    const source = input.captions[index];
    return row?.id !== source.id || !requiredText(row.text, source.maxChars);
  })) throw new Error("Translation service returned invalid captions.");
  return result;
}
export async function handleRequest(request, env, fetcher = fetch) {
  const origin = request.headers.get("Origin");
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map(value => value.trim());
  const cors = origin && allowed.includes(origin) ? {
    "Access-Control-Allow-Origin": origin, "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type", Vary: "Origin",
  } : {};
  const reply = (body, status = 200) => Response.json(body, {status, headers: {...cors, "Cache-Control": "no-store"}});
  if (!cors["Access-Control-Allow-Origin"]) return reply({error: "Origin unavailable."}, 403);
  if (request.method === "OPTIONS") return new Response(null, {status: 204, headers: cors});
  if (new URL(request.url).pathname !== "/captions" || request.method !== "POST") return reply({error: "Use POST /captions."}, 404);
  if (!env.OPENAI_API_KEY || !env.CAPTION_LIMIT) return reply({error: "AI caption service is not configured."}, 503);
  const identity = request.headers.get("CF-Connecting-IP") || "unknown";
  const {success} = await env.CAPTION_LIMIT.limit({key: identity});
  if (!success) return reply({error: "Too many translation requests. Try again in a minute."}, 429);
  let input;
  try { input = normalize(await readRequest(request)); } catch { return reply({error: "Invalid caption request."}, 400); }
  if (!input) return reply({error: "Invalid caption fields or language."}, 400);
  try {
    const signal = AbortSignal.any([request.signal, AbortSignal.timeout(24_000)]);
    return reply(await generate(env, input, signal, fetcher));
  } catch {
    return reply({error: "The caption service couldn’t return a complete result. Please retry."}, 502);
  }
}
export default {fetch: (request, env) => handleRequest(request, env)};
