---
name: security-audit
description: |-
  Performs an exhaustive, adversarial, multi-pass security audit of web apps — HTML/JS/CSS, IndexedDB/localStorage, WebRTC/P2P/STUN/TURN, PWA/Service Worker, WebView/Electron/Tauri, CSP & security headers, auth/session/CSRF, prototype pollution, supply chain, and build pipeline. ALWAYS use this skill when the user asks for a "security check," "audit," "pentest," "vulnerability scan," "is this safe to ship," "hack this," "crack it," "red team," or invokes "/security-audit" — and proactively suggest it whenever the user is about to ship, deploy, publish, or share a link to an app that handles user input, personal data, or peer-to-peer connections, even if they did not ask for a security review by name. This skill is relentless: it hunts rather than checks, runs a deterministic tooling harness (grep blitz, SRI hashing, OSV CVE lookup), maps the checklist to OWASP WSTG test IDs, builds proof-of-concept exploits for CRITICAL findings and verifies them in a live browser when the app can run, chains low-severity bugs into high-impact attacks, re-audits its own fixes, and never declares an app clean without a second adversarial pass from a different attacker persona.
---

# Security Audit — Relentless Edition

## Philosophy

A security audit that stops after one pass through a checklist is not a
security audit — it's a lint run. This skill is built to be **relentless**:

- **Assume guilt.** The codebase is guilty until every claim below is verified
  against the actual code — never against what the code is *supposed* to do.
  A variable named `sanitizedInput` is not evidence of sanitization. Read the
  function.
- **Evidence or nothing.** Every finding cites `file:line`. Every "N/A" cites
  the tool output or grep that proved it. Unverified claims are labeled
  `UNVERIFIED` and given the exact check needed to resolve them.
- **Hunt, don't check.** The checklist is a starting map, not a destination.
  For each category, actively try to **break** the app, not just look for the
  pattern.
- **Prove the criticals.** A CRITICAL finding without at least a sketch of a
  working exploit (input → sink → payload) is a suspicion, not a finding.
  Build the PoC or downgrade it and say why.
- **Chain the bugs.** Three WARNINGs that compose into one CRITICAL are one
  CRITICAL. Report the chain at the severity of its worst end state, not its
  worst component.
- **Never resolve your own findings silently.** No CRITICAL or WARNING is
  closed without showing the user the exact fix and re-auditing it.
- **Second opinion is mandatory.** After the first pass, re-run the whole
  audit from a different attacker persona (see Phase 9). First passes have
  blind spots; the persona sweep exists to find them.

Two hard rules:

1. **No item is skipped because it "doesn't apply."** If there's no WebRTC,
   say so explicitly: `N/A — confirmed via grep (0 hits)`. A missing section
   reads as "not checked," not "not applicable."
2. **No CRITICAL or WARNING finding is closed by the audit's own author
   without showing the user the exact diff.** Propose the fix; let the user
   (or a follow-up turn) confirm it landed correctly before calling anything
   resolved.

---

## Skill layout — what ships with this skill

This skill is a directory, not a single file. Use the parts in place of
doing everything by hand:

```
skills/security-audit/
├── SKILL.md                # this orchestrator — the process
├── wstg-mapping.md         # Phase 4: checklist → OWASP WSTG test IDs
├── threat-model-presets.md # Phase 0: pre-answered threat models
├── findings.schema.json    # Phase 10: machine-readable findings output
├── issue-template.md       # Phase 10: ready-to-file agent-brief issues
├── tools/
│   ├── greps.json          # the full pattern arsenal (single source of truth)
│   ├── run-greps.py        # Phase 2: runs every group, writes hits.json
│   ├── sri.py              # Phase 7: real SRI hashes for CDN fixes
│   ├── osv-check.py        # Phase 1/11: real CVE data via the OSV API
│   ├── validate-findings.py # Phase 10: checks findings.json
│   └── sync-install.sh     # post-edit: propagate to ~/.claude/skills
├── payloads/               # Phase 5: tested attack strings for PoCs
│   ├── xss.md · prototype-pollution.md · dom-clobbering.md
│   ├── csp-bypass.md · postmessage.md · websocket.md
└── fixes/                  # Phase 7: drop-in secure patterns
    ├── safe-render.md · safe-merge.md · storage-encryption.md
    ├── csp.md · sri.md · postmessage.md · csrf.md · secure-ipc.md
```

**Fallback rule:** if a tool can't run (no Python/ripgrep/network), do the
step manually and note it in the report under "Tooling gaps." If the app
can't be built or run, the dynamic phase (4.5) is skipped *explicitly* and
noted there too — never pretend to have observed runtime behavior you
didn't. Never skip a step just because its tool is missing.

**Keeping the installed copy in sync:** if you installed this skill to
`~/.claude/skills` (so `/security-audit` works from any project), run
`bash tools/sync-install.sh` from this workspace copy after editing — add
`--downloads` to also refresh the flat copies in `~/Downloads`, or
`--check` to see whether the installed copy is already current.

---

## The Relentless Loop (execute in order, every time)

| # | Phase | Output |
|---|-------|--------|
| 0 | **Threat model** — assets, adversaries, trust boundaries, data flows | severity yardstick |
| 1 | **Inventory** — every file, config, dependency, entry point | scan scope |
| 2 | **Grep blitz** — `tools/run-greps.py` → `hits.json` | hit list w/ file:line |
| 3 | **Full read** — every hot line and every file with data flow to a sink | coverage map |
| 4 | **Checklist sweep** — walk all 15 sections, breaking each one | findings |
| 4.5 | **Dynamic (live browser)** — run the app, watch console/network, verify PoCs in-page | runtime evidence + verified PoCs |
| 5 | **PoCs** — build exploit sketches for every CRITICAL (`payloads/`) | proof |
| 6 | **Chaining** — compose findings into attack paths | chain severities |
| 7 | **Fixes** — exact drop-in replacements (`fixes/`) | patches |
| 8 | **Re-audit** — re-run the tool, re-read, confirm no regression | verified fixes |
| 9 | **Persona sweep** — repeat from a different attacker's mindset | second opinion |
| 10 | **Report** — full template at the bottom | deliverable |

Do not declare the audit complete until phases 0–9 (plus the dynamic
phase) have all run. If any phase was skipped, the report says so
explicitly under "Coverage gaps."

---

## Modes — quick / standard / deep

Route by the request, not by effort preference:

| Mode | Use when | What runs |
|------|----------|-----------|
| **quick** | "quick check," "skim it," "is this obviously broken," casual or low-sensitivity asks | 0 (3-question interview only) → 1 → 2 → 4 (only sections with grep hits) → PoC + fix for any CRITICAL found. Everything skipped is listed as coverage gaps. |
| **standard** | the default — any full "security audit" request | the complete loop, phases 0–10 |
| **deep** | "pentest," "red team," "crack it," "exploit it," or apps handling highly sensitive data | standard + Phase 4.5 mandatory, osv-check on every dependency, exploit development + chaining for the top CRITICAL, all five persona sweeps, and the WSTG extension tests (BUSL / APIT / IDNT / INFO from wstg-mapping.md) when a backend or business logic is in scope |

Rules:

1. **quick is scope control, not effort reduction.** A CRITICAL found in
   quick mode still gets a PoC and a fix. The report says "quick mode — run
   standard for full coverage."
2. **deep adds depth, not looseness.** Same honesty rules, more work.
3. **Unclear intent → standard.** When in doubt, run the full loop.

---

## Phase 0 — Threat Model (interview first, then map)

Severity is meaningless without a threat model. Before reading any code, ask
**the user three questions** (quick mode: these three, no more):

1. **Crown jewel — what's worth stealing or breaking here?** Options: health
   / intimate personal data, credentials or tokens, payments, P2P identity,
   chat/messages, nothing sensitive. If they won't say, assume the most
   sensitive plausible answer and state the assumption in the report.
2. **Adversaries — who can attack?** Options: anyone on the public internet,
   malicious peers inside the app, shared-device users, a device thief with
   the laptop/phone, browser extensions, a compromised CDN/dependency.
3. **Shared device — do multiple people use this app on one browser
   profile?** Yes/no. The single biggest severity multiplier for client-side
   apps.

**Or pick a preset** — `threat-model-presets.md` pre-answers these three
questions for the common cases (couples-app, SaaS-with-backend, P2P game,
Electron desktop). A preset doesn't skip the interview: still confirm the
two most consequential answers with the user (*shared device?* and
*backend in scope?*), and let them override anything. State the preset
(and any overrides) in the report's Interview line.

How the answers tune severity (state the tuning in the report):

- Sensitive data + shared device → §3 storage items and shared-device
  leakage default to CRITICAL; encryption-at-rest becomes a recommended
  fix, not a nice-to-have.
- Credentials/tokens as crown jewel → §5 (auth) and §12 (secrets) get the
  deep treatment; tokens in localStorage escalate to CRITICAL.
- No backend → auth/CSRF/IDOR/SSRF items are N/A with grep proof; the CORS
  and HSTS checks shrink to what the client can enforce.
- Malicious peers in scope → §8 (P2P) and §15 (input/resource exhaustion)
  treat every peer message as hostile input.
- Device thief in scope → every at-rest item (storage, caches, cookies,
  source maps, console logs) is judged at device-in-hand severity.

Then complete the four steps below against the interview answers.

1. **Assets (crown jewels).** Enumerate what's actually worth stealing or
   breaking: specific data fields (health data, chats, cycle logs, messages,
   credentials), tokens, keys, privileged capabilities (admin actions, P2P
   identity, invite codes). Name them concretely — "user data" is not an asset
   list.
2. **Adversaries.** List who can attack and what they can touch:
   - casual visitor / script-kiddie (can only see what ships)
   - malicious remote peer (WebRTC / P2P / multiplayer)
   - shared-device user or device thief (filesystem + devtools + extensions)
   - compromised third party (CDN, dependency, analytics script)
   - the backend itself (if it exists, is it trusted or semi-trusted?)
   - the user's own browser profile (other tabs/extensions same-origin?)
3. **Trust boundaries.** Identify every place untrusted data crosses into
   trusted code: URL params → app state, `postMessage` → handlers, peer →
   `onmessage`, storage → renderer, server → DOM, CDN script → page. Mark each
   boundary in the code as you go.
4. **Data flows.** For each asset: where is it created, stored, rendered,
   transmitted, exported? Trace it end to end. Any hop that is plaintext,
   unvalidated, or reachable by an adversary is a finding.

A mood-tracker's journal stored in plaintext localStorage is CRITICAL in a
shared-laptop threat model and WARNING in a single-user private-browser
model — the threat model decides. State yours in the report.

---

## Phase 1 — Inventory

1. List every `.html`, `.js`, `.mjs`, `.ts`, `.jsx`, `.tsx`, `.css`, `sw.js`,
   worker files, `manifest.json`, `package.json` / lockfile, `*.config.*`,
   `.env*`, Dockerfile/CI files, and server config (nginx/Apache/Netlify/
   Vercel headers, if present).
2. Identify the **stack** — framework (React/Vue/Angular/Svelte/vanilla),
   bundler (Vite/Webpack/esbuild/Rollup), runtime (browser/Electron/Tauri/
   Capacitor/WebView), backend (if any). The stack decides which sink patterns
   matter in Phase 2.
3. Identify **entry points**: the HTML file(s), main entry JS, service
   workers, workers, iframes, popups, `webview` tags. Every entry point is a
   potential attacker surface.
4. Record **which files are shipped to the client** vs. server-only vs.
   build-only. Anything shipped to the client is public by definition.
5. If dependencies exist, run `tools/osv-check.py --manifest <app>/package.json
   --lockfile <app>/package-lock.json` and record real CVE findings. If the
   tool can't run (no network/parse failure), fall back to web search on the
   pinned versions and mark the claims accordingly.

---

## Phase 2 — Grep Blitz (tool-driven)

Run the deterministic harness:

```bash
python tools/run-greps.py --root <app-dir> --output <app-dir>/hits.json
```

- It reads every pattern group from `tools/greps.json`, runs them all, and
  writes `hits.json` (group, pattern, file, line, snippet) plus a per-group
  hit/no-hit summary.
- **The per-group summary is the evidence for "N/A" claims** in the report —
  quote it: `WebRTC: N/A — grep group 'webrtc-p2p': 0 hits`.
- On any hit, open the file and read the surrounding context; a bare match
  list is not an audit. Correlate hits with the threat model's trust
  boundaries — a hit on a hot path is a finding; a hit in dead code is INFO.
- If the tool can't run, work through `tools/greps.json` by hand with a
  line-numbered search and note the manual fallback in the report.
- If the scan truncates on its time budget (default 300s, `--time-budget`
  to change), the skipped patterns are recorded in hits.json's summary —
  list them under Tooling gaps; truncated coverage is partial coverage.
- Run a single group when re-checking one category:
  `python tools/run-greps.py --root <app-dir> --group xss-dom-sinks`.

---

## Phase 3 — Full Read with Coverage Tracking

1. Read every file the grep blitz flagged **plus** every file that carries a
   data flow to a sink, even if it didn't match a pattern (the sink's source
   is often clean-looking).
2. Maintain a **coverage map**: file → checklist sections applied to it. Any
   file never read is a coverage gap; list it in the report.
3. A line that can carry attacker-controlled data to a sink is **hot**. Trace
   it end to end: source → transformations → sink. Note transformations that
   claim to sanitize and verify them against the actual sink semantics
   (encoding for the context the data lands in: HTML, attribute, URL, JS,
   CSS — escaping for one is not escaping for all; see `fixes/safe-render.md`).
4. **Dead code still gets flagged** (INFO at minimum) — it's often the first
   thing a future attacker re-enables.
5. Variable names, comments, and READMEs are not evidence. A function named
   `sanitize()` that does `return str.replace(/</g, '')` but is used inside a
   `style` attribute is a bug, not a fix.

---

## Phase 4 — The 15-Section Inspection Checklist

For each section: check the items, **try to break the thing**, and classify
against the Phase 0 threat model. Every finding gets file:line. PoC payloads
come from `payloads/`; fix patterns come from `fixes/`; the WSTG tests each
section maps to live in `wstg-mapping.md` — mark each one ✅ executed /
⛔ N/A (with evidence) / ⏭️ not run (with reason) for the report's WSTG
Coverage box.

### 1. Injection & DOM Security (XSS)

- [ ] Any use of `innerHTML`, `outerHTML`, `insertAdjacentHTML`,
      `document.write`, `DOMParser` (with `text/html`), `createContextualFragment`,
      or `srcdoc` with data that originates from user input, storage, URL
      params, a remote peer, or a server response. CRITICAL unless the string
      is provably static developer-authored text.
- [ ] Any use of `eval()`, `new Function()`, string-arg `setTimeout` /
      `setInterval`, dynamic `import()` / `importScripts()` with a variable
      path, or `Function` constructor — CRITICAL regardless of input source.
- [ ] **Template literals in the DOM** — `` element.innerHTML = `<div>${userValue}</div>` ``
      is the same bug in disguise. Check explicitly; grep misses line-wrapped
      strings.
- [ ] Framework sinks: React `dangerouslySetInnerHTML`, Vue `v-html`,
      Angular `[innerHTML]` / `bypassSecurityTrust*` / `$sce.trustAs*`,
      Svelte `{@html ...}` — each is an innerHTML in a trench coat.
- [ ] User-controlled values used as **attributes**: `href`, `src`, `action`,
      `style`, `on*` handlers built dynamically. Check for `javascript:` URIs
      and CSS injection via `style` (exfiltration via `background: url()`).
- [ ] URL params, `location.hash`, `document.referrer`, `postMessage`
      payloads treated as trusted without validation.
- [ ] Markdown / rich-text renderers: escaping on by default? Raw-HTML
      passthrough off? If the renderer is a dependency, check its known XSS
      CVEs.
- [ ] **Break it:** match the exact sink context and fire the shortest
      payload (`payloads/xss.md`). Fixes: `fixes/safe-render.md`.

### 2. Prototype Pollution & DOM Clobbering

- [ ] **Prototype pollution:** any recursive merge/assign/extend
      (`Object.assign`, `_.merge`, `$.extend`, custom `mergeDeep`) fed with
      untrusted JSON (from URL params, postMessage, peers, server). CRITICAL
      if reachable. Test with `payloads/prototype-pollution.md`; fix with
      `fixes/safe-merge.md`.
- [ ] **DOM clobbering:** HTML elements with `id`/`name` become globals
      (`window.foo`) and can shadow built-ins. Any code that reads
      `window.<name>` or checks `if (x)` on an injectable name is
      exploitable. Test with `payloads/dom-clobbering.md`.

### 3. Client-Side Storage & Encryption-at-Rest

- [ ] **Sensitive data at rest:** private records (health data, journals,
      mood/cycle logs, messages) in plaintext `localStorage` / IndexedDB.
      Readable by any script in the origin, any browser extension, and anyone
      with devtools or filesystem access. CRITICAL in shared-device or
      extension-rich threat models.
- [ ] **Global exposure:** sensitive data attached to `window`,
      `globalThis`, or non-namespaced globals.
- [ ] **No encryption-at-rest** for the most sensitive fields. Fix:
      `fixes/storage-encryption.md` (AES-GCM + PBKDF2) — including its honest
      limits (XSS still defeats it; a known passphrase defeats it).
- [ ] **Export/share/backup:** does an export silently bundle more than the
      user intended (partner's private entries in "my export")? Check the
      exact field list.
- [ ] **Quota/eviction:** does the app handle `QuotaExceededError` and
      storage clearing without silent data loss or a broken empty-state?
- [ ] **Shared-device leakage:** in multi-user apps, can one user read the
      other's private fields without an explicit unlock? Elevated to CRITICAL
      for couples/personal-data apps by default (see last section).

### 4. Cryptographic Misuse

- [ ] **Weak RNG for security-relevant values:** `Math.random()` for tokens,
      IDs, invite codes, share links, nonces, or anything that gates access —
      CRITICAL. `Math.random()` is predictable and 53-bit — brute-forceable
      for access gates. Use `crypto.getRandomValues()` / `crypto.randomUUID()`.
- [ ] **Custom crypto:** hand-rolled ciphers, XOR "encryption", ROT13-style
      obfuscation presented as security, AES with a hardcoded key/IV, ECB
      mode, reused nonces/IVs, `md5`/`sha1` for anything security-relevant.
- [ ] **`atob`/`base64`/`Buffer.from` used as "encryption"** — encoding is
      not encryption. CRITICAL if it protects anything sensitive.
- [ ] **Weak key derivation:** fixed passwords, PBKDF2 with <100k iterations,
      no salt, salt reuse. **Non-constant-time** secret comparison (`==` on
      hashes).

### 5. Authentication, Sessions, CSRF, Authorization

(Only if the app has auth/backend — otherwise N/A with grep proof.)

- [ ] **Password handling:** HTTPS only, never logged, never in URLs, never
      stored client-side in plaintext, never compared client-side. Backend
      uses a real KDF (bcrypt/argon2/scrypt).
- [ ] **Token/session storage:** auth tokens in `localStorage` are
      XSS-stealable by definition — note the risk; prefer `httpOnly` cookies
      for server-side sessions; if localStorage tokens are required, CSP must
      be strict (the token is only as safe as your XSS posture).
- [ ] **Token handling:** expiry enforced both sides, rotation on privilege
      change, revocation on logout, no token in URLs or `postMessage` to
      unknown origins.
- [ ] **CSRF:** state-changing requests protected by CSRF token or SameSite
      cookie + custom-header pattern? Fix: `fixes/csrf.md`.
- [ ] **Authorization (IDOR):** for every mutating operation, is the actor
      checked for the right to act on the target object, or does the client
      just send an id? Client-side "you can't see this" checks are UI, not
      security — if the server trusts the client's claim, that's CRITICAL.
- [ ] **Session fixation / logout:** logout invalidates server-side? Login
      doesn't reuse a pre-login session id? **Client-side role checks:** any
      capability gated only in JS with the server unguarded is a finding.

### 6. postMessage & Cross-Origin Communication

- [ ] Every `message` listener **must** check `event.origin` against an
      allowlist before touching `event.data`. Missing origin check =
      CRITICAL. Wildcard `*` in the target origin of `postMessage` = data
      leak to whoever is listening.
- [ ] `event.data` is attacker-controlled: validate schema, types, and
      length before it touches DOM, storage, or app state.
- [ ] `MessageChannel`/`BroadcastChannel` use — who else can join, and is
      the payload validated?
- [ ] **Break it:** post the payloads in `payloads/postmessage.md` from an
      attacker origin. Fix: `fixes/postmessage.md`.

### 7. Network & Transport

- [ ] **Mixed content:** HTTP resources loaded from an HTTPS page.
- [ ] **URL-building with user input:** `fetch(userControlledUrl)` or
      template-built URLs. Client-side: open-redirect / credential-leak;
      with any server proxy component: SSRF. CRITICAL if a server fetches on
      the client's behalf.
- [ ] **WebSockets:** `wss://` only, server validates `Origin`, no tokens in
      the URL query. Messages validated like any untrusted input
      (`payloads/websocket.md`; CSWSH fix in `fixes/csrf.md`).
- [ ] **CORS (if backend):** wildcard `Access-Control-Allow-Origin` with
      credentials, or `ACAO: null` — CRITICAL.
- [ ] **Referrer leakage:** sensitive tokens/IDs in the URL + no
      `Referrer-Policy` → secrets leak via the Referer header.
- [ ] **Open redirects:** `location.href = userInput` or `?next=` /
      `?redirect=` — fix with an allowlist.
- [ ] **DNS rebinding** consideration if there's a server or local service:
      does the client validate hostnames on local/privileged endpoints?

### 8. P2P, WebRTC, Multi-User Abuse

- [ ] **IP leakage:** SDP candidates exposing LAN/internal IPs without user
      awareness. `iceTransportPolicy: 'relay'` when the app must hide the
      user's real IP from the peer.
- [ ] **TURN credentials hardcoded** in client JS — CRITICAL, visible to
      anyone viewing source. Must be issued server-side, short-lived,
      per-session.
- [ ] **Data-channel input treated as trusted:** `RTCDataChannel.onmessage`
      data is a remote peer's arbitrary input — type-check, length-bound,
      schema-check before touching DOM, storage, or state.
- [ ] **Signaling channel:** authenticated? Can a stranger inject offers
      into someone else's session?
- [ ] **Connection-state handling:** stale UI implying a secure connection
      after disconnect/renegotiation.
- [ ] **Multi-user abuse:** in any app where users interact, a malicious
      peer is an adversary in the threat model: can they inject HTML, spam,
      hijack identity, or crash others (see §15)?
- [ ] **Break it:** connect two peers and send injection, oversized, and
      malformed payloads from the *other* peer's side.

### 9. Service Workers, PWA & Caching

- [ ] **Service worker fetch handler** blindly caches/proxies third-party or
      unauthenticated responses; cache keys manipulable to serve stale or
      malicious content.
- [ ] **Update hijacking:** can the SW serve a malicious cached version
      indefinitely? Check `skipWaiting`/`clients.claim` and
      cache-versioning; confirm `updateViaCache` doesn't defeat updates.
- [ ] **manifest.json scope creep:** `start_url`/`scope` granting broader
      access than intended.
- [ ] **Sensitive pages cached:** authenticated pages/API responses cached
      without `Cache-Control: no-store` — readable from disk by anyone with
      device access.
- [ ] **SW as an attack surface:** a compromised or misrouted SW is a
      man-in-the-middle for the whole origin. Message handling in the SW
      validates origin and payload?

### 10. WebViews, Electron, Tauri, Hybrid Shells

- [ ] **Electron:** `nodeIntegration: true`, `contextIsolation: false`,
      `sandbox: false`, `enableRemoteModule`, `nodeIntegrationInWorker`,
      `webview` tags with untrusted content, `shell.openExternal` /
      `shell.openPath` fed with user input (RCE via `file://`), broad custom
      protocol handlers. Any one of these with renderer-controlled input is
      CRITICAL. Fix: `fixes/secure-ipc.md`.
- [ ] **Preload scripts** expose overly broad IPC, or main trusts renderer
      messages without validating sender/arguments. Treat every renderer as
      compromised.
- [ ] **Tauri:** shell/`Command`/`open` with user input,
      `dangerousRemoteDomainIpcAccess`, broad capability files, arbitrary
      `invoke`, missing `app.security.csp`.
- [ ] **Android/iOS WebView:** `setJavaScriptEnabled` on untrusted content,
      `addJavascriptInterface` exposed to remote pages (JS-bridge RCE),
      `allowFileAccess`, `loadUrl` with user input, missing
      `originWhitelist` on Capacitor plugins.
- [ ] **Deep links / custom schemes** routing user-controlled input into app
      actions.

### 11. Supply Chain & Build Pipeline

- [ ] **CDN scripts without SRI:** any third-party `<script src=` / `<link>`
      without `integrity` + `crossorigin="anonymous"` — CRITICAL. Fix:
      compute the real hash with `tools/sri.py`, see `fixes/sri.md`.
- [ ] **Dependencies with known CVEs:** use `tools/osv-check.py` output
      (Phase 1); never claim a version is vulnerable from memory.
- [ ] **Outdated/abandoned deps** — no maintenance in years = future CVEs.
- [ ] **Third-party script scope:** analytics, fonts, embeds running with
      full page privileges. Each is a standing XSS bridge; can any be scoped
      down (sandboxed iframe, loaded only when needed)?
- [ ] **Build pipeline:** dev flags in prod builds (`NODE_ENV !==
      'production'` branches, `VITE_*`/`process.env` secrets inlined into
      shipped JS — public by definition), source maps shipped to prod, `.env`
      committed, `.git` folder deployed.
- [ ] **Lockfile discipline:** deps pinned (lockfile committed) or floating
      ranges that silently shift the supply chain?

### 12. Secrets & Credential Hygiene

- [ ] Hardcoded API keys/tokens/passwords anywhere in client-shipped code —
      public by definition. CRITICAL. Includes keys in
      `import.meta.env`/`process.env` inlined at build time.
- [ ] `.env` files, configs, or test fixtures with real secrets bundled or
      committed (check `.gitignore`, deployed artifacts, `*.map` files).
- [ ] Secrets in URLs, logs, error messages, or localStorage.
- [ ] Predictable ID/token generation — `Math.random()` gating any access —
      CRITICAL; `crypto.getRandomValues()` / `crypto.randomUUID()` instead.
- [ ] **Grep for real key formats** (`sk-…`, `AKIA…`, `ghp_…`, `xoxb-…`,
      `AIza…`, `-----BEGIN … PRIVATE KEY-----`) — not just the word "key".

### 13. Security Headers & CSP (full audit)

Even with no server, check the meta tag / hosting config / Electron
`webRequest` / Tauri CSP. Absent server? State it and check what the client
can enforce.

- [ ] **CSP present and strict:** `default-src 'self'`; no
      `unsafe-inline`/`unsafe-eval` in `script-src`; explicit
      `object-src 'none'`, `base-uri 'none'`, `form-action 'self'`;
      `frame-ancestors` set; `upgrade-insecure-requests` present. Missing CSP
      = WARNING minimum, CRITICAL if any XSS finding exists (CSP is the
      safety net for exactly that failure mode). Fix: `fixes/csp.md`.
- [ ] **CSP bypasses:** `'unsafe-inline'`/`'unsafe-eval'`, wildcard hosts,
      `https:`/`http:`/`data:` in script-src, JSONP on allowlisted hosts,
      missing `object-src`/`base-uri`. Test with `payloads/csp-bypass.md`.
- [ ] **Nonce/hash usage** — inline scripts covered by nonces/hashes, or
      relying on `unsafe-inline`?
- [ ] **Other headers:** `X-Frame-Options`/`frame-ancestors` (clickjacking),
      `X-Content-Type-Options: nosniff`, `Referrer-Policy`,
      `Strict-Transport-Security`, `Permissions-Policy`, COOP/COEP
      (note tradeoffs before demanding COEP).
- [ ] **Clickjacking:** can the app be iframed by third parties? If it
      handles anything sensitive, block it.
- [ ] **iframe sandbox:** untrusted embeds have `sandbox` set — and
      `allow-same-origin`+`allow-scripts` together is an escape hatch.

### 14. Information Leakage & Privacy

- [ ] `console.log`/`debug` printing tokens, personal records, or full app
      state in production.
- [ ] Verbose error messages / stack traces / internal paths surfaced to the
      end user.
- [ ] Source maps in prod (proprietary logic; often re-include dev secrets).
- [ ] **Privacy leakage:** fingerprinting, tracking pixels, undisclosed
      telemetry, `navigator.sendBeacon` with unconsented payloads, excessive
      permission requests (camera/mic/geolocation at load instead of
      on-demand).
- [ ] Tab-nabbing: `window.open` / target links without
      `rel="noopener noreferrer"` — the new page can rewrite
      `window.opener.location`.
- [ ] `window.name` carrying data across origins; `history` state leaking
      sensitive data into the address bar.

### 15. Input Validation, Uploads & Resource Exhaustion

- [ ] **File uploads** (if any): SVG/HTML uploads are stored XSS (served
      same-origin), path traversal in filenames, polyglot files, no size
      limits, no type allowlisting. Serve uploads from a separate origin or
      with `Content-Disposition: attachment` + `nosniff`.
- [ ] **Validation depth:** lengths, types, schemas enforced before data
      reaches sinks? A 10MB string from a peer into `innerHTML` or
      `localStorage.setItem` is a DoS even when it can't XSS.
- [ ] **ReDoS:** user/peer-controlled input run through regexes on the hot
      path — catastrophic backtracking = client DoS.
- [ ] **Unbounded loops over remote data**, recursive rendering of
      attacker-controlled nested structures (deep JSON → stack overflow),
      `URL.createObjectURL` blobs never revoked (memory leak).
- [ ] **Zip/tar bombs** if any archive handling exists.
- [ ] **Break it:** feed the app its own max inputs — maximum-length
      strings, deeply nested JSON, malformed types (`NaN`, `Infinity`,
      negative indices, `__proto__` keys) — and watch for crashes, hangs, or
      weird state.

---

## Phase 4.5 — Dynamic (Live Browser)

Static analysis finds candidates; the live browser proves them. If the app
can be built and run, and this environment provides a live/preview browser,
run the app and use it for two passes:

**4.5a — Observe.** Watch the console and network from app load onward.
Record every signal with the exact browser message text and, where
identifiable, the file:line of the code that produced the request
(correlate with the Phase 2 hit list):

- **Console violations (the headline catches):**
  - **CSP violations** — "Refused to … violates the following Content
    Security Policy directive: …" — each message names the directive that's
    too loose (or proves the policy is enforced). Then still attack the
    policy with `payloads/csp-bypass.md`.
  - **Failed SRI** — "Failed to find a valid digest in the 'integrity'
    attribute" — the pinned hash is wrong or the CDN changed the file (a
    supply-chain tripwire working as intended; WARNING until you confirm
    which).
  - **Mixed content** — "Mixed Content: … was loaded over HTTPS, but
    requested an insecure resource" — capture the exact URLs.
  - **Data leaks in console** — tokens, personal records, or stack traces
    with internal paths printed at runtime.
  - **Runtime failures** — QuotaExceededError, service-worker
    registration/update errors, unhandled rejections exposing app
    internals.
- **Network signals:**
  - **Security headers on real responses** — is CSP/XFO/nosniff/
    Referrer-Policy actually served, with the values the config claims?
    (A config that never ships is a WARNING on its own.)
  - **CORS errors** and credentialed requests to wildcard-ACAO endpoints.
  - **WebSocket handshakes** — ws:// vs wss://, tokens in the URL, origin
    rejections from the server.
  - **Third-party requests** — analytics/tracking/telemetry that grep
    missed (checklist §14); `Cache-Control` on authenticated responses
    (§9).
- A category with zero runtime activity is additional N/A evidence — note
  it next to the grep hit counts ("no WebSocket handshakes observed").

Record everything in the report's Dynamic section. A signal that maps to a
checklist item upgrades it from "should check" to "observed."

**4.5b — Verify.** For every CRITICAL finding from the static pass,
reproduce the PoC in the running app:

1. Navigate to the state where the sink is reachable (the URL, input,
   message, or peer payload that reaches the hot line).
2. Inject the context-matched payload from `payloads/` through the real
   input path — not by editing the page.
3. Confirm impact with a **benign marker**: a window flag
   (`window.__xss_verified = true`), a DOM mutation, or a console marker.
   Never exfiltrate to real attacker infrastructure; this is a pre-release
   audit of an authorized target.
4. Snapshot the result (DOM check + console). Confirmed execution = the
   finding is **verified live**. Not confirmed = keep the static finding,
   label it **static-only**, and say why (sink not reachable from the UI,
   CSP blocked it, input never reaches the sink).
5. Re-run the CSP-bypass payloads against the live policy while you're in
   the page.

**Degradation:** if the app can't be built/run or no live browser is
available, skip this phase *explicitly* — report it under "Tooling gaps"
and mark every CRITICAL PoC "static-only (app not runnable)". Static
reasoning with honest labels is fine; pretending to have observed runtime
behavior is not.

---

## Phase 5 — Proof of Concept (for every CRITICAL)

For each CRITICAL finding, show the shortest path from attacker input to
impact. Use the context-matched payloads from `payloads/`, and verify them
against the actual sink — in the live browser via Phase 4.5b when the app
is runnable, by end-to-end static tracing otherwise. Every PoC carries a
verification status (see the Fix Generation Format):

```
PoC: <the shortest repro>
1. Attacker controls: <input / message / peer payload / URL>
2. Reaches: <file:line, the sink>
3. Payload: <the minimal payload, e.g. `"><img src=x onerror=steal()>`>
4. Impact: <what actually happens — cookie theft, store wipe, peer RCE, ...>
```

If you cannot construct a working PoC, say so: downgrade to WARNING with the
reason ("PoC blocked — sink is reachable only from trusted paths", etc.), or
label `UNVERIFIED — needs <specific check>`.

## Phase 6 — Chaining

After individual findings, look for **composition**:

- Missing CSP + one `innerHTML` sink = full RCE surface, not "XSS plus a
  policy gap."
- Weak `Math.random()` invite code + no rate limit = account hijack.
- `postMessage` without origin check + sensitive action handler = remote
  action trigger.
- Any XSS + auth token in localStorage = session theft.
- `nodeIntegration: true` + any XSS = full machine compromise (Electron).

Report each chain at the severity of its end state, and list the component
findings beneath it. Chains are where "low" findings stop being low.

## Phase 7 — Fixes

For every finding, output the exact Fix Generation Format below. Use the
drop-in patterns in `fixes/` as the starting shape, adapted to the app's
actual vulnerable code. Where the real fix is architectural ("move this to
the server"), say so and give the smallest concrete step that reduces risk
today. CDN fixes get a real hash from `tools/sri.py`, not a placeholder.

## Phase 8 — Re-audit the fixes

1. **Load the previous run's findings.json (if this is a follow-up run).**
   Every `open` / `fix-proposed` finding is a debt item to verify in this
   pass; every `resolved` one is a regression to re-confirm. Update
   `status` as findings are verified — this is what makes the audit
   re-auditable instead of a snapshot. Validate the file with
   `python tools/validate-findings.py findings.json`.
2. Apply each fix to the code (or walk it if you lack execution access).
3. Re-run the relevant grep group:
   `python tools/run-greps.py --root <app-dir> --group <id>` — and diff the
   hits against the first run's `hits.json`; every fixed finding's hit must
   be gone, and no new hits may appear.
4. Re-read the changed code: does the fix reintroduce the issue elsewhere?
   Does it break functionality (a pre-release audit must not trade a vuln
   for a broken feature)?
5. Re-check chains: did fixing one link break the chain or shift it?
6. Re-run the dynamic observe pass (Phase 4.5a): fixed headers, policies,
   and hashes must produce zero violations in the live browser.
7. Only then mark the finding resolved — with the user's confirmation if
   they applied the fix themselves.

## Phase 9 — Persona sweep (mandatory second opinion)

Re-run the audit from at least three attacker mindsets, chosen from the
Phase 0 threat model. Each persona re-reads the code looking for *their*
path to the crown jewels:

- **The thief** — has the device: filesystem, devtools, extensions. What's
  readable at rest? localStorage, IndexedDB, caches, cookies, source maps.
- **The XSS hunter** — assumes one bug exists and asks: what's the blast
  radius? Where can a single script tag reach: tokens, P2P identity, admin
  actions, other users' data?
- **The malicious peer** — for any multi-user/P2P app: what can I send the
  other user that hurts them?
- **The supply-chain saboteur** — what third-party code runs with full
  privileges, and what would a compromised version of it steal?
- **The session hijacker** — where do tokens live, how are they stored, and
  what can read them?

Record what each persona found that pass one missed. If a persona found
nothing new, say so — a genuine empty sweep is data too.

---

## Severity Classification

Judge severity against the **Phase 0 threat model** — the same pattern is
CRITICAL in one app and WARNING in another. General rules:

- 🔴 **CRITICAL** — proven or near-proven remote impact on a sensitive
  asset: exploitable XSS reaching sensitive data, hardcoded credentials in
  shipped code, plaintext sensitive personal data in a shared-device context,
  `Math.random()` gating access, missing SRI on a privileged CDN script,
  `nodeIntegration` + any XSS, prototype pollution reachable from untrusted
  input, missing postMessage origin check on a sensitive handler.
- 🟡 **WARNING** — real risk, defense-in-depth, or exploitable only with
  unrealistic preconditions: missing CSP, unhandled disconnect state, no
  encryption-at-rest for moderately sensitive fields, verbose errors, missing
  headers, no rate limiting on invite codes (when the code is otherwise
  strong).
- 🟢 **INFO** — best-practice polish: source maps in prod with nothing
  sensitive, minor logging cleanup, dep bumps with no known CVE, missing
  `rel="noopener"` on a link to a fully trusted domain.

Rules:

1. **Never downgrade to make the report look better.** Unsure between two
   severities? Default to the higher and let the user argue it down with
   context you didn't have.
2. **Chains report at their end-state severity.**
3. **Unproven criticals are labeled UNVERIFIED** with the exact check needed,
   not silently downgraded.

---

## Fix Generation Format

Every finding uses this exact shape (copy-pasteable):

```
### 🔴 CRITICAL — <short title>
**File:** path/to/file.js:LINE
**Issue:** <one or two plain-language sentences>

**Vulnerable:**
​```js
<exact current code>
​```

**Fixed:**
​```js
<drop-in secure replacement — from fixes/, adapted to the real code>
​```

**Why this works:** <one sentence — the attack this closes>

**PoC:** <shortest repro — input → sink → impact>

**Verified:** <live browser — PoC executed in-page | static-only — <why>>
```

---

## Final Report Template

Produce the human report below **and** emit `findings.json` in the skill
working directory (schema: `findings.schema.json`; validate with
`python tools/validate-findings.py findings.json`). Then generate
ready-to-file issue bodies from `issue-template.md` for every CRITICAL and
WARNING finding — they plug straight into the ask-matt triage flow.

```
# Security Audit — <app name>

## Threat Model
Mode: <quick | standard | deep>
Interview: <Q1/Q2/Q3 answers — or preset used + overrides — and the
severity tuning they drove>
Assets: <concrete list>
Adversaries: <concrete list>
Trust boundaries: <where untrusted data crosses into trusted code>
Data flows: <asset → store → render → transmit → export, one line each>

## Scope & Coverage
Files scanned: <list; any unread file listed under Coverage gaps>
Stack: <framework, bundler, runtime, backend>
Tooling: <run-greps engine + hits.json path, osv-check result, tooling gaps>
Findings data: findings.json (schema findings.schema.json, validated with
tools/validate-findings.py)
Grep groups checked: <hit/no-hit each — from the tool summary or manual run>
Coverage gaps: <files never fully read, phases skipped, tools that couldn't
run, app not runnable (dynamic phase skipped)>

## Summary
🔴 Critical: N   🟡 Warning: N   🟢 Info: N
(Chains: N — each reported at end-state severity)

## Dynamic (live browser)
Observed: <CSP violations, SRI failures, mixed content, header values on
real responses, WebSocket handshakes, third-party requests — exact browser
messages + file:line where identifiable>
PoCs verified live: <finding IDs that executed in-page>
PoCs static-only: <finding IDs + why — app not runnable / sink not
reachable from UI / blocked by CSP>

## WSTG Coverage
Tests executed: <WSTG ID + status per mapped test — ✅ executed / ⛔ N/A
with evidence / ⏭️ not run with reason>
In-scope but not run: <IDs + why — no backend, app not runnable, mode
limitation>
Extension tests (deep mode): <BUSL / APIT / IDNT / INFO tests run, if any>

## Findings
<one block per finding, Critical → Warning → Info, Fix Generation Format>

## Chains
<each chain: components → end-state severity → fix priority>

## Sections confirmed N/A
<explicit, with grep-group evidence — e.g. "WebRTC: N/A — group
'webrtc-p2p': 0 hits">

## Second Opinion (persona sweep)
<what each persona found (or genuinely found nothing), and what pass one
missed>

## Ship Verdict
<"NOT SHIP-READY — N critical findings above (and N chains)" OR
 "Ship-ready — 0 critical findings; N warnings recommended before/soon
 after launch" — never a vague "looks pretty good">

## Filed issues
<N issue bodies generated from issue-template.md — one per CRITICAL and
WARNING finding, chains as one issue at end-severity; statuses tracked in
findings.json>
```

---

## When the audit target is a couples / personal-data app specifically

If the app stores intimate personal data shared between two users on
potentially the same device (mood/cycle trackers, shared journals, private
game modes, chat, health data), elevate by default:

- §3's plaintext-at-rest and shared-device leakage items are **CRITICAL** —
  a plaintext localStorage blob of cycle or mood data readable by anyone who
  opens devtools on a shared laptop is a CRITICAL finding in this context,
  even though the same pattern might be WARNING for a public todo list.
- Add **"the ex-partner"** to the adversary list: someone with the device,
  the password, and emotional motivation. Multi-account separation and
  explicit unlock steps become security requirements, not UX niceties.
- Export/backup features (§3) get extra scrutiny — "my export" must never
  silently include the partner's private entries.
- Note honestly when client-side crypto is theater: a passphrase-derived key
  stored in the same origin is protection against device theft, not against
  XSS or the partner who knows the passphrase (`fixes/storage-encryption.md`
  says the same).

---

## Honesty & Verification Rules

1. **Cite file:line for every finding.** No line number, no finding.
2. **Cite tool/grep output for every N/A.** "No WebRTC" must be backed by
   the grep group's zero hits, not vibes.
3. **Never fabricate findings** — if you can't verify a suspicion, label it
   `UNVERIFIED — needs <check>` instead of padding the report. This includes
   dependency CVEs: use `tools/osv-check.py` or a cited search, never memory.
4. **Say when you didn't finish.** Skipped a phase, an unread file, or a
   tool that couldn't run? It goes in "Coverage gaps" / "Tooling gaps," not
   the void.
5. **Plain language.** No "security theater" padding, no vague "hardening
   recommended." Every finding names the concrete attack it prevents.
6. **The verdict is binary and explicit.** Zero criticals = "Ship-ready —
   0 critical findings; N warnings…". Any critical = "NOT SHIP-READY — N
   critical findings." Never "looks pretty good."
