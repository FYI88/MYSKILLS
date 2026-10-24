# Payload Library

Tested, copy-paste attack strings for building PoCs. **Authorized audits only.**

Rules for using these:

1. **Match the context.** The same string behaves differently in an HTML
   body, an attribute, a URL, a script block, or a CSS value. Each file notes
   which context its payloads target. Escaping that works for one context is
   not escaping for another.
2. **Verify against the actual sink before reporting.** A payload that
   "should" fire is a suspicion; one you ran in the app (or traced end to
   end with certainty) is a finding. If you can't verify, label the finding
   `UNVERIFIED — needs <check>`.
3. **Never ship a payload into a production system.** These exist to prove
   reachability in a controlled pre-release audit.
4. **Shortest payload wins.** The minimal string that fires is the one that
   belongs in the PoC — it proves the sink is reachable without noise.

Index:

| File | What it proves |
|------|----------------|
| [xss.md](xss.md) | Injection into HTML / attribute / URL / JS / CSS contexts |
| [prototype-pollution.md](prototype-pollution.md) | `__proto__` / `constructor.prototype` poisoning of merges and parsers |
| [dom-clobbering.md](dom-clobbering.md) | Element `id`/`name` shadowing globals and library reads |
| [csp-bypass.md](csp-bypass.md) | Gadgets that defeat a permissive or misconfigured CSP |
| [postmessage.md](postmessage.md) | Cross-origin message injection when origin checks are missing |
| [websocket.md](websocket.md) | WebSocket origin/transport/token issues and peer-input abuse |

If the app's stack needs something not here (framework-specific sink, custom
protocol), build the payload against the actual sink and document it in the
finding — this library is a starting point, not a ceiling.
