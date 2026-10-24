# Subresource Integrity for third-party resources

## The fix shape

```html
<script src="https://cdn.jsdelivr.net/npm/dompurify@3.4.13/dist/purify.min.js"
        integrity="sha384-ZuC+DIACqSIZTsp+7YF57cR5Y+6qXa7YFbEKdA/EHA/R0T+41dtorqucYl71Zp+t"
        crossorigin="anonymous"></script>
```

(Version 3.4.13 is the current patched release — pin a version that
`tools/osv-check.py` reports as clean, and regenerate the hash when you
bump.)

- **Pin the version** in the URL — floating `@latest` URLs can't have a
  stable hash.
- **`crossorigin="anonymous"` is required** for SRI to apply to
  cross-origin scripts (and for `Access-Control-Allow-Origin` responses).
- **Regenerate the hash on every dependency bump** — and update the
  integrity attribute in the same change that bumps the version, or the
  script silently stops loading.

## Generate the real hash

Use the tool:

```bash
python tools/sri.py https://cdn.jsdelivr.net/npm/dompurify@3.4.13/dist/purify.min.js --tag
```

Manual equivalent (if the tool can't run):

```bash
curl -sL <url> | openssl dgst -sha384 -binary | openssl base64 -A
```

Put the output (e.g. `sha384-9Zg...`) into the `integrity` attribute.

## What this closes

A compromised or swapped CDN file becomes a load failure instead of
arbitrary code execution in the page — the classic supply-chain attack with
zero warning signs. Note in the finding: **SRI alone doesn't fix a CDN that
changes its pinned file; it makes the change loud instead of silent.**

## When SRI can't apply

- Same-origin scripts don't need it (SRI still fine if you want it).
- Some third-party embeds (Google Maps, Stripe Elements) don't offer stable
  SRI — then scope them (sandboxed iframe) and say so in the finding.

## Also check

- `<link rel="stylesheet">` gets the same treatment (`integrity` +
  `crossorigin="anonymous"`).
- `importScripts()` in a service worker pulls remote scripts with no SRI
  mechanism — prefer self-hosted copies there and say so.
