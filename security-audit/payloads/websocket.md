# WebSocket payloads

Targets: transport (ws:// vs wss://), token placement, origin validation,
and message handling.

## Transport & credential checks (grep-driven, not payloads)

- `ws://` instead of `wss://` → traffic readable in transit. CRITICAL if
  anything sensitive flows over the socket.
- Token in the URL (`new WebSocket("wss://host/?token=...")`) → leaks via
  server logs, proxies, and the Referer header of anything the page loads
  after. Fix: token in a header or subprotocol.
- Server must validate the `Origin` header — a socket open from an attacker
  page means CSWSH (cross-site WebSocket hijacking) with the user's session.

## Message handling payloads

If messages are rendered or stored without validation, the same injection
families apply over the wire:

```
</script><img src=x onerror=alert(1)>
{"type":"message","text":"<svg onload=alert(1)>"}
{"__proto__":{"polluted":1}}
```

A 100MB string, malformed JSON, and deep JSON nesting test the app's bounds:

```js
socket.send("x".repeat(100 * 1024 * 1024));      // memory / quota DoS
socket.send("not json");                          // crash on parse?
socket.send(JSON.stringify({a:{a:{a:{a:{...}}}}})); // stack overflow?
```

## Reporting rule

Distinguish transport findings (WARNING unless sensitive data flows, then
CRITICAL) from message-handling findings (peer-controlled data reaching DOM /
storage = CRITICAL, exactly like any other injection).

## Fix reference

See `fixes/csrf.md` (CSWSH/origin mitigation shares the SameSite + origin
story) and `fixes/safe-render.md` (validating peer messages before render).
