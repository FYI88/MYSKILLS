# Content Security Policy

## Strict baseline policy

```
default-src 'self';
script-src 'self';
style-src 'self';
img-src 'self' data:;
font-src 'self';
connect-src 'self';
object-src 'none';
base-uri 'none';
form-action 'self';
frame-ancestors 'none';
upgrade-insecure-requests
```

Rules that make it strict:

- **No `unsafe-inline` / `unsafe-eval`** in `script-src`. Inline scripts get
  nonces or hashes instead (below); dynamic code gets refactored.
- **`object-src 'none'`** — blocks the `<object>`/`<embed>` bypass family.
- **`base-uri 'none'`** — blocks the `<base>` hijack of relative URLs.
- **`frame-ancestors 'none'`** — clickjacking. Set `'self'` if embedding in
  your own app is a feature.
- Add hosts only as needed, one at a time: CDNs go in `script-src` with SRI
  (see sri.md) — and an allowlisted host with an open JSONP endpoint is a
  bypass, so vet what you allowlist.

## Nonces for legitimate inline scripts

```html
<script nonce="<server-generated-per-request>">
  /* inline app bootstrap */
</script>
```

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-<server-generated-per-request>'; ...
```

Nonces must be **fresh per response** and served from the server, never
hardcoded — a static nonce in a static file is the same as `unsafe-inline`.

## Serving it: headers, not meta

Meta tags can't set `frame-ancestors`, `sandbox`, or `report-uri`, so serve
via header when you control hosting:

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
```

- **nginx:** add_header in the server block (use `always` to include error pages)
- **Netlify:** `_headers` file or `netlify.toml` `[[headers]]`
- **Vercel:** `vercel.json` `headers` array
- **GitHub Pages:** can't set headers — use the meta tag and accept the
  `frame-ancestors` limitation

## Electron (recommended, via webRequest)

```js
const { session } = require("electron");
const CSP = "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'";
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      "Content-Security-Policy": [CSP],
    },
  });
});
```

## Tauri (tauri.conf.json)

```json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    }
  }
}
```

## Verification after applying

- Load the app and read the console — a correct policy produces zero
  violations (the browser reports each one; that's the fastest signal).
- Re-run the CSP-bypass payloads from `payloads/csp-bypass.md`: object,
  base, data:, JSONP-on-allowlisted-host, inline handlers.
- In the audit report, a CSP that holds against all of those upgrades the
  paired XSS finding's residual risk.
