# StoreShot caption service

The GitHub Pages editor runs on-device translation by default. This Worker enables context-aware ASO translation and the Magic Draft copy generator. It sends caption text, target locale, and the optional app context to OpenAI. Uploaded image files stay in the browser.

## Enable hosted caption generation

1. Open this directory in a terminal with Wrangler 4.36 or later and an eligible Cloudflare account. Verify the rate-limit namespace ID is available in that account.
2. Set `OPENAI_API_KEY` as a Worker secret with `npx wrangler secret put OPENAI_API_KEY`. Never add the key to Git or to the editor HTML.
3. Deploy with `npx wrangler deploy`. `ALLOWED_ORIGINS` must include the deployed editor origin. `OPENAI_MODEL` must support Responses API Structured Outputs.
4. Set the `storeshot-ai-endpoint` meta tag in the editor HTML to the deployed HTTPS URL ending in `/captions`, then publish the editor. Set provider spending limits before exposing paid generation publicly. The Worker limits requests per client IP per Cloudflare location.

## API contract

POST JSON to `/captions`. The payload includes `action` (`translate` or `draft`), `sourceLocale`, `targetLocale`, optional `context` fields (`appName`, `category`, `tone`, `description`), and up to 30 `captions` with `id`, `slide` (1–10), `field` (`headline`, `subtitle`, or `badge`), and `text` for translation. Draft requests require a description. Responses return `captions` with the same IDs in the same order and the generated text. Images, storage state, and device settings are excluded.
