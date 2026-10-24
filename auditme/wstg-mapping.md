# OWASP WSTG mapping

Maps every checklist section in SKILL.md to OWASP Web Security Testing Guide
test IDs. Source: the current WSTG (master / v4.3-dev numbering), verified
against the official repository.

**Version note:** the WSTG renumbered several categories after v4.2 — most
notably CORS moved to CLNT-07, and AUTH/IDNT/ATHZ were consolidated. If a
reader quotes v4.2 IDs, the differences are in the affected categories, not
the coverage. This file is the authoritative mapping for this skill.

## Usage rules

During the checklist sweep, mark each mapped test:

- ✅ **executed** — ran it (against code, and live via Phase 4.5 when the
  app runs); record the finding or "clean."
- ⛔ **not applicable** — with grep/tool evidence (e.g. "no backend —
  ATHN/ATHZ/SESS out of scope").
- ⏭️ **not run** — with the reason (mode limitation, no runnable app, no
  live target).

The report's **WSTG Coverage** box collects: tests executed (ID + status),
and in-scope-but-not-run (ID + why). Never claim a WSTG test was "run" from
memory — every mark traces to an action taken in this audit.

---

## §1 — Injection & DOM Security (XSS)

| WSTG ID | Test | Checklist items |
|---|---|---|
| INPV-01 | Reflected XSS | URL params / hash / referrer into sinks |
| INPV-02 | Stored XSS | storage- or server-sourced data into sinks |
| CLNT-01 | DOM-based XSS | client-side sinks (innerHTML, eval-family) |
| CLNT-02 | JavaScript Execution | eval / new Function / string timers / dynamic import |
| CLNT-03 | HTML Injection | innerHTML / insertAdjacentHTML / DOMParser / srcdoc |
| CLNT-04 | Client-side URL Redirect | javascript: hrefs, client-side open redirects |
| CLNT-05 | CSS Injection | style injection, `background: url()` exfil |
| CLNT-13 | Cross Site Script Inclusion | `<script src>` with attacker paths |
| CLNT-15 | Client-side Template Injection | template literals into innerHTML |

No direct WSTG test: framework-specific sinks (`dangerouslySetInnerHTML`,
`v-html`, `[innerHTML]`, `bypassSecurityTrust*`, `{@html}`) and markdown
renderer configuration — covered by the checklist itself (fold them under
CLNT-01/03 when reporting).

## §2 — Prototype Pollution & DOM Clobbering

| WSTG ID | Test | Checklist items |
|---|---|---|
| INPV-22 | Prototype Pollution | merge/assign/extend sinks fed untrusted JSON |
| CLNT-01 | DOM-based XSS | clobbering gadgets that end in a sink |
| CLNT-03 | HTML Injection | clobbering via injected `id`/`name` elements |

No direct WSTG test for DOM clobbering — it is HTML injection by another
name; report it under CLNT-01/03.

## §3 — Client-Side Storage & Encryption-at-Rest

| WSTG ID | Test | Checklist items |
|---|---|---|
| CLNT-12 | Browser Storage | localStorage / IndexedDB / sessionStorage content and exposure |
| ATHN-06 | Browser Cache Weaknesses | cached sensitive pages / API responses |

No direct WSTG test: encryption-at-rest for client data (WebCrypto) and
export-scope checks — skill-specific; report under CLNT-12 with the
encryption findings.

## §4 — Cryptographic Misuse

| WSTG ID | Test | Checklist items |
|---|---|---|
| CRYP-01 | Weak Transport Layer Security | TLS / mixed content transport posture |
| CRYP-02 | Padding Oracle | custom crypto with oracle-like behavior |
| CRYP-03 | Sensitive Info via Unencrypted Channels | plaintext transmission of secrets |
| CRYP-04 | Weak Cryptographic Primitives | md5/sha1, hardcoded keys/IVs, `atob`-as-encryption, `Math.random()` for access gates |

## §5 — Authentication, Sessions, CSRF, Authorization

| WSTG ID | Test | Checklist items |
|---|---|---|
| IDNT-01..05 | Identity lifecycle (roles, registration, provisioning, enumeration, username policy) | account-related checks when auth exists |
| ATHN-01..11 | Authentication (transport, defaults, lockout, bypass, remember-password, cache, weak methods, security questions, reset, alternative channel, MFA) | §5 password/token handling |
| ATHZ-01..05 (+05.1/05.2) | Authorization (directory traversal, schema bypass, privilege escalation, IDOR, OAuth) | IDOR / client-side role checks |
| SESS-01..11 | Session management (schema, cookie attributes, fixation, exposed variables, CSRF, logout, timeout, puzzling, hijacking, JWT, concurrent sessions) | §5 token/session + CSRF items |
| APIT-01..04 (+99) | API (recon, BOLA, excessive data exposure, BFLA, GraphQL) | when a backend API is in scope |

All of §5 is ⛔ N/A for a pure client-side app — grep for the backend
surface first and say so.

## §6 — postMessage & Cross-Origin Communication

| WSTG ID | Test | Checklist items |
|---|---|---|
| CLNT-11 | Web Messaging | origin checks, payload validation, BroadcastChannel |

No direct WSTG test for the `event.source`-vs-`event.origin` nuance —
fold into CLNT-11.

## §7 — Network & Transport

| WSTG ID | Test | Checklist items |
|---|---|---|
| CRYP-01 | Weak TLS | mixed content / transport |
| CRYP-03 | Sensitive Info via Unencrypted Channels | ws:// vs wss://, http:// fetches |
| CLNT-07 | Cross Origin Resource Sharing | CORS config, credentialed wildcard |
| CLNT-10 | WebSockets | origin validation, tokens in URL, message handling |
| INPV-19 | Server-Side Request Forgery | server-side fetch of user-controlled URLs |

No direct WSTG test: Referrer leakage / Referrer-Policy — fold into
CONF-14 (headers) when reporting.

## §8 — P2P, WebRTC, Multi-User Abuse

| WSTG ID | Test | Checklist items |
|---|---|---|
| CLNT-10 | WebSockets | closest WSTG analog for realtime channels |

No direct WSTG test: WebRTC IP leakage, TURN credential exposure, data
channel validation — skill-specific. State this explicitly in the report;
do not stretch a WSTG ID over them.

## §9 — Service Workers, PWA & Caching

| WSTG ID | Test | Checklist items |
|---|---|---|
| ATHN-06 | Browser Cache Weaknesses | sensitive pages/API responses cached |
| CLNT-12 | Browser Storage | CacheStorage content |
| CONF-12 | Content Security Policy | SW scope + policy interaction |

No direct WSTG test: SW update hijacking / cache poisoning / `skipWaiting`
abuse — skill-specific.

## §10 — WebViews, Electron, Tauri, Hybrid Shells

WSTG targets browser web apps; the shell-specific surface
(`nodeIntegration`, `contextIsolation`, IPC validation,
`addJavascriptInterface`, Tauri capabilities, custom schemes) has **no WSTG
coverage**. Closest analogs: CLNT-02 (JS execution) and CLNT-13 (script
inclusion). Report this section as "beyond WSTG scope — skill-specific
checks," not as mapped tests.

## §11 — Supply Chain & Build Pipeline

| WSTG ID | Test | Checklist items |
|---|---|---|
| CONF-03 | File Extensions Handling for Sensitive Information | leaked config/backup artifacts |
| CONF-04 | Old, Backup and Unreferenced Files | `.env`, `.git`, stale artifacts deployed |
| CONF-10 | Subdomain Takeover | dangling DNS for CDNs/hosting |

No direct WSTG test: SRI, dependency CVE data (use `tools/osv-check.py`),
inlined build-time secrets (`import.meta.env`/`process.env`) — skill-specific.

## §12 — Secrets & Credential Hygiene

| WSTG ID | Test | Checklist items |
|---|---|---|
| ATHN-01 | Credentials over Encrypted Channel | credential transport |
| ATHN-02 | Default Credentials | hardcoded credentials (client-shipped is public) |
| CONF-04 | Old, Backup and Unreferenced Files | `.env` / test fixtures with real secrets |

## §13 — Security Headers & CSP (full audit)

| WSTG ID | Test | Checklist items |
|---|---|---|
| CONF-07 | HTTP Strict Transport Security | HSTS presence/values |
| CONF-12 | Content Security Policy | CSP strictness + bypass testing |
| CONF-14 | Other HTTP Security Header Misconfigurations | nosniff, Referrer-Policy, Permissions-Policy, COOP/COEP |
| CLNT-07 | Cross Origin Resource Sharing | CORS (cross-ref §7) |
| CLNT-09 | Clickjacking | frame-ancestors / X-Frame-Options |

## §14 — Information Leakage & Privacy

| WSTG ID | Test | Checklist items |
|---|---|---|
| INFO-03 | Webserver Metafiles | robots/sitemap/well-known leakage |
| INFO-05 | Web Page Content for Information Leakage | console logs, comments, internal paths |
| ERRH-01 | Improper Error Handling | verbose errors to end users |
| ERRH-02 | Stack Traces | stack traces surfaced in UI |
| CLNT-14 | Reverse Tabnabbing | `window.open` / links without `noopener` |
| ATHN-06 | Browser Cache Weaknesses | cached auth pages |

No direct WSTG test: source maps in prod, telemetry/tracking disclosure,
`sendBeacon` consent, `window.name`/`history` state leaks — fold into
INFO-05 where possible, otherwise skill-specific.

## §15 — Input Validation, Uploads & Resource Exhaustion

| WSTG ID | Test | Checklist items |
|---|---|---|
| INPV-05 (+05.6, 05.7) | SQL / NoSQL / ORM Injection | backend data layer |
| INPV-06..13 | LDAP / XML / SSI / XPath / IMAP / Code / Command / Format String | server-side injection |
| INPV-15 | HTTP Response Splitting | header injection |
| INPV-16 | HTTP Request Smuggling | proxy/backend desync |
| INPV-17 | Host Header Injection | host header trust |
| INPV-18 | Server-side Template Injection | SSTI |
| INPV-20 | Mass Assignment | unchecked fields in updates |
| INPV-21 | CSV Injection | exported spreadsheets |
| INPV-23 | Insecure Deserialization | untrusted serialized input |
| ATHZ-01 | Directory Traversal File Include | path traversal in filenames |
| BUSL-08 | Upload of Unexpected File Types | type allowlisting on uploads |
| BUSL-09 | Upload of Malicious Files | SVG/HTML/polyglot stored XSS |
| BUSL-05 | Number of Times a Function Can Be Used Limits | rate limiting on invite codes / actions |
| BUSL-07 | Defenses Against Application Misuse | peer abuse, spam, resource exhaustion |

No direct WSTG test: ReDoS, unbounded loops over remote data, blob URL
lifecycle — fold under BUSL-07 / INPV items as best fit, or skill-specific.

---

## WSTG areas outside this skill's default scope — add in deep mode

The 15 sections above cover WSTG's client-side, auth, session, crypto,
error-handling, and header surface. These WSTG areas are **not** walked by
default; deep mode (or any audit with a backend / business logic in scope)
must add them:

| WSTG area | Tests | Add when |
|---|---|---|
| Information Gathering | INFO-01..10 (recon, fingerprinting, attack-surface mapping) | a live target is reachable (Phase 4.5) |
| Identity Management | IDNT-01..05 (registration, provisioning, enumeration, username policy) | auth exists |
| Business Logic | BUSL-01..10 (data validation, request forging, integrity, timing, function limits, workflow circumvention, misuse defenses, uploads, payment) | server-side business logic exists |
| API Testing | APIT-01..04 + 99 (recon, BOLA, excessive data exposure, BFLA, GraphQL) | a backend API is in scope |

When these run, their results join the same report with the same severity
rules — and the WSTG Coverage box lists them as executed, not as an
afterthought.
