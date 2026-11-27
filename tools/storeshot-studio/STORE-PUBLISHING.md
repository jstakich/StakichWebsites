# StoreShot publishing integration

The static editor ships with direct uploads disabled. Set the Publish to Stores dialog's `data-endpoint` to a same-origin backend path when the backend and account system are available. Store private keys and service-account credentials in the server's encrypted credential store. Present credential management on the server's settings page. Keep credentials out of editor storage, exported archives, and responses.

## Browser contract

- `GET /capabilities` looks up the authenticated user's current plan and app connections. Return `{"plan":"pro","listings":[{"id":"opaque-id","label":"My app · App Store","sizes":["iphone","iphone63","ipad"]}]}`. The other eligible plan is `agency`. Return an empty list for accounts without store connections.
- `GET /settings` opens the authenticated app and credential settings. For Apple, collect the Issuer ID, Key ID, private `.p8` key, and app ID. For Google, collect the service-account JSON and Android package name.
- `POST /uploads` takes multipart fields `listingId`, `archive` (ZIP), and `assets` (a JSON array of archive paths, locales, presets, widths, heights, and formats). Return success once the job has been durably accepted or the upload has completed.

Recheck the plan and listing ownership on every upload and settings request. Apply CSRF protection, request size limits, archive validation and image decoding, and verify actual screenshot dimensions against the destination's supported formats. Issue Apple API tokens and Google OAuth credentials on the backend. Use stable job IDs and record per-asset failures so retries can resume without duplicating screenshots.

For Apple, resolve the app-version localization, create or resolve the screenshot set, reserve each upload, transfer its bytes and commit the asset. For Google, use an edit transaction and handle screenshot replacement explicitly. Treat the final commit as a separate action that requires confirmation, because it can send changes for publishing. Select `ERROR_IF_IN_REVIEW` to avoid canceling an existing review. Limit edits to the chosen screenshot assets. This contract does not implement those backend operations.

- [Apple screenshot sets](https://developer.apple.com/documentation/appstoreconnectapi/app-screenshot-sets)
- [Google Play image uploads](https://developers.google.com/android-publisher/api-ref/rest/v3/edits.images/upload)
