# Threat-model presets

Pre-answered versions of the Phase 0 three-question interview for the
common cases. Offer these during the interview; the user picks one (or
answers the three questions directly).

**Usage rules:**

1. **A preset pre-answers, it doesn't skip.** Still confirm the two most
   consequential answers with the user: *shared device?* and *backend in
   scope?* — those two override everything else in the tuning.
2. **Presets can be overridden and combined.** The user picks a preset,
   then changes any answer (e.g. "couples-app, but it also has a server").
   The changed answers win; state what changed in the report.
3. **No preset fits → ask the three questions directly.**
4. State the preset (and any overrides) in the report's Interview line.

---

## couples-app — couples / personal-data app

**Offer when:** shared journals, mood/cycle trackers, private chat, couples
game modes — intimate data shared between two users, often on the same
device.

**Interview pre-answers:**
1. **Crown jewel:** intimate personal data — journal entries, mood/cycle
   logs, private messages.
2. **Adversaries:** the ex-partner, shared-device users, a device thief,
   browser extensions, a compromised CDN/dependency.
3. **Shared device:** **YES** — the defining trait of this preset.

**Severity tuning:**
- §3 storage items and shared-device leakage default to **CRITICAL** —
  plaintext localStorage of cycle/mood data readable via devtools on a
  shared laptop is a critical finding in this model.
- Encryption-at-rest (`fixes/storage-encryption.md`) is a recommended fix,
  not a nice-to-have — with its honest limits stated: the partner who
  knows the passphrase, and any same-origin XSS, both defeat it.
- Explicit unlock steps (passphrase before viewing private fields) are
  security requirements, not UX niceties.
- Export/backup (§3): "my export" must never silently include the
  partner's private entries.
- The ex-partner is an adversary with the device, the password, and
  emotional motivation — multi-account separation is security, not
  courtesy.

---

## saas-with-backend — web SaaS (accounts + server API)

**Offer when:** a typical web app with user accounts, a server-side API,
and anything customer-affecting (subscriptions, payments, shared data
between tenants).

**Interview pre-answers:**
1. **Crown jewel:** user accounts, credentials and session tokens,
   customer data (PII / payments if present), API keys.
2. **Adversaries:** anyone on the public internet, credential-stuffers,
   other tenants (IDOR/BOLA between accounts), compromised third-party
   dependencies.
3. **Shared device:** **NO** (each user on their own device) — but the
   multi-tenant boundary replaces it as the top concern.

**Severity tuning:**
- §5 (auth/sessions/CSRF/IDOR) is the hot section; server-side role and
  object checks are the real security (client-side checks are UI).
- Backend in scope → the WSTG extension tests are **mandatory in deep
  mode**: APIT (BOLA/BFLA/excessive data exposure), BUSL (business logic),
  IDNT (identity lifecycle), INPV injection family. See
  `wstg-mapping.md`.
- Tokens in localStorage + any XSS = account-takeover chain — escalate
  storage-of-token findings; prefer `httpOnly` cookies; require a strict
  CSP.
- CSRF and CORS/headers (§7, §13) matter here more than in any other
  preset; wildcard-ACAO with credentials is CRITICAL.
- Client-side storage (§3) is lower-stakes than the couples preset
  (server holds the data) — but session/refresh tokens at rest and cached
  auth responses still get checked.

---

## p2p-game — multiplayer / P2P game

**Offer when:** WebRTC or WebSocket realtime multiplayer, invite/room
codes, in-game chat, shared state between players.

**Interview pre-answers:**
1. **Crown jewel:** session/identity control, invite and room codes,
   in-game state, chat.
2. **Adversaries:** **malicious peers** (the defining adversary), session
   hijackers, script-kiddies, cheaters, and anyone who can guess a code.
3. **Shared device:** usually no; confirm.

**Severity tuning:**
- §8 (P2P) and §15 (input/resource exhaustion) treat **every peer message
  as hostile input**: type-check, length-bound, schema-check before DOM,
  storage, or state.
- `Math.random()` for room/invite codes is **CRITICAL** here — codes gate
  access and are brute-forceable at 53 bits of predictability. Use
  `crypto.getRandomValues()` and enforce rate limits on code attempts
  (`wstg-mapping.md` → BUSL-05).
- Hardcoded TURN credentials are CRITICAL (any player can read the source)
  — issue server-side, short-lived, per-session.
- Data-channel payloads: 10MB strings, malformed JSON, deep nesting = DoS
  against other players; a malicious peer can crash the lobby.
- Signaling channel must be authenticated — a stranger injecting offers
  into someone else's session is a session hijack.
- IP leakage matters if the game should hide the user's real IP from
  peers (`iceTransportPolicy: 'relay'`).

---

## electron-desktop — Electron / Tauri / WebView shell

**Offer when:** a desktop (or mobile-webview) app whose renderer runs web
content — Electron, Tauri, Capacitor, Android/iOS WebView.

**Interview pre-answers:**
1. **Crown jewel:** whatever the app processes locally, plus the machine
   itself — the renderer's reach is the attacker's reach.
2. **Adversaries:** remote attackers via web content loaded in the app,
   malicious websites (if the app opens links/webviews), supply-chain
   compromise of the auto-update channel, local attackers with device
   access.
3. **Shared device:** confirm; the shell surface matters regardless.

**Severity tuning:**
- §10 is the hot section: `nodeIntegration`, `contextIsolation`, `sandbox`
  flags; IPC validation in main (treat every renderer as compromised);
  `shell.openExternal`/`openPath` allowlists (RCE via `file://`);
  `addJavascriptInterface` on remote content.
- **Any XSS in the renderer is a potential RCE** — a renderer XSS finding
  chains to full machine compromise if the shell isn't hardened; report
  the chain at CRITICAL.
- Auto-update integrity is supply chain: unsigned/unverified update
  channels are a standing remote-code-execution vector (`fixes/sri.md`
  mindset applies to the updater too).
- CSP for the shell (`fixes/csp.md` — Electron `webRequest`, Tauri
  `app.security.csp`) is defense-in-depth for exactly the renderer→shell
  chain.
- `webview` tags / remote content + `allowRunningInsecureContent` +
  broad custom protocol handlers each merit their own finding.

---

## Combining with modes

- **quick** mode: preset + two confirmation questions only.
- **standard** mode: preset answers, then the full loop.
- **deep** mode: presets with a backend (saas, p2p-game with a server, or
  any override that adds one) pull in the WSTG extension tests
  (BUSL / APIT / IDNT / INFO) — see `wstg-mapping.md`.
