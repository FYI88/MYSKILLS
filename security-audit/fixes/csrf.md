# CSRF protection for state-changing requests

Scope: only applies when there is a server (or a serverless function) — a
pure client-side app has no CSRF surface (grep the manifest/fetch targets to
confirm, and say so in the report).

## Layer 1 — cookies (cheap, often sufficient)

```http
Set-Cookie: session=...; HttpOnly; Secure; SameSite=Lax; Path=/
```

- **`SameSite=Lax`** blocks cross-site POST/form submission while keeping
  top-level GET navigation working. `Strict` if the app can tolerate it.
- **`HttpOnly`** keeps the token out of JS (defends the session against
  XSS — but see the honest note below).
- **`Secure`** prevents plaintext cookie transit.
- `SameSite=None` (needed for cross-site embeds) **disables** this layer —
  then the CSRF token layer below is mandatory.

## Layer 2 — CSRF token (custom header pattern)

Server issues a token; the client echoes it in a header on every mutating
request. Attacker pages can't read the token (same-origin policy) and can't
set custom headers cross-origin without a preflight the server rejects.

Client:

```js
// Fetch wrapper — attach the token to every state-changing request.
async function api(path, { method = "GET", body, headers = {} } = {}) {
  const res = await fetch(path, {
    method,
    body: body ? JSON.stringify(body) : undefined,
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken,   // read once from the server
      ...headers,
    },
    credentials: "same-origin",
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}
```

Server (illustrative):

```js
// Issue: on login/session creation, put the token in a cookie AND in a
// response body field (double-submit pattern) or server-side store.
// Verify: reject any mutating request whose X-CSRF-Token doesn't match.
app.post("/api/*", (req, res, next) => {
  if (req.method !== "GET" && req.get("X-CSRF-Token") !== req.csrfToken()) {
    return res.status(403).json({ error: "csrf" });
  }
  next();
});
```

## WebSockets — CSWSH

A WebSocket opened from an attacker page rides the user's cookies. The
server **must validate the `Origin` header** against an allowlist; add
`SameSite=Lax` on the session cookie as a second layer. Tokens in the
socket URL are leak-prone — use a header/subprotocol or origin + SameSite.

## Honest notes for the report

- `HttpOnly` cookies reduce — but do not eliminate — the XSS-session-theft
  chain: an XSS can still *perform* state-changing actions on the user's
  behalf. Say so; the real fix for session theft remains fixing XSS.
- Don't claim CSRF is "N/A" just because the UI is client-rendered — check
  the actual mutating endpoints.

## Verification

- From an attacker page, attempt a cross-origin form POST and a cross-origin
  fetch with `credentials: "include"` — both must fail (no cookie sent, no
  preflight allowed).
- Re-run the app's own flows to confirm tokens still work after a session
  refresh (tokens must survive page reloads).
