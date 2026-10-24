# Fix Library

Drop-in secure patterns for the audit's most common findings. Every finding
in the report must show exact vulnerable code and an exact replacement — this
library is where the replacements come from.

Rules for using these:

1. **Adapt, don't paste blindly.** Each pattern is a starting shape for the
   app's actual code. The report's "Fixed" block must be the app's real
   vulnerable code replaced, not a generic snippet.
2. **Preserve behavior.** A pre-release audit must not trade a vulnerability
   for a broken feature. If the fix changes behavior (e.g. encryption makes
   an export unreadable elsewhere), say so in the finding.
3. **Re-audit after applying.** Re-run the relevant grep group and re-read
   the changed lines (Phase 8). Never mark resolved without that pass.
4. **Escaping must match the sink context.** See safe-render.md — HTML
   escaping is not attribute escaping is not URL escaping is not JS escaping.

Index:

| File | Fixes |
|------|-------|
| [safe-render.md](safe-render.md) | innerHTML / v-html / dangerouslySetInnerHTML sinks → safe rendering |
| [safe-merge.md](safe-merge.md) | Prototype pollution → pollution-safe merge + hardened JSON.parse |
| [storage-encryption.md](storage-encryption.md) | Plaintext sensitive storage → AES-GCM + PBKDF2 at rest |
| [csp.md](csp.md) | Missing/weak CSP → strict policy, headers vs meta, Electron/Tauri |
| [sri.md](sri.md) | CDN scripts without SRI → integrity attributes (use tools/sri.py) |
| [postmessage.md](postmessage.md) | Missing origin checks → safe handler + safe send |
| [csrf.md](csrf.md) | State-changing requests without CSRF protection |
| [secure-ipc.md](secure-ipc.md) | Electron/Tauri/WebView bridge hardening |

Where the real fix is architectural (move this to the server), the finding
must say so and give the smallest concrete step that reduces risk today.
