# Safe postMessage handling

## Safe receive (handler)

```js
const ALLOWED_ORIGINS = new Set([
  "https://app.example.com",
  "https://embed.example.com",
]);

const ALLOWED_TYPES = new Set(["SET_STATE", "PLAY", "PAUSE"]);
const MAX_PAYLOAD = 4096;

window.addEventListener("message", (event) => {
  // 1. Origin allowlist — the non-negotiable check.
  if (!ALLOWED_ORIGINS.has(event.origin)) return;

  // 2. Shape check: message must be an object.
  const msg = event.data;
  if (typeof msg !== "object" || msg === null || Array.isArray(msg)) return;

  // 3. Type allowlist + length bounds before ANY state change.
  if (!ALLOWED_TYPES.has(msg.type)) return;
  if (typeof msg.payload !== "string" || msg.payload.length > MAX_PAYLOAD) return;

  // 4. Only now touch app state / DOM / storage.
  handleMessage(msg);
});
```

Also validate `event.source` when the handler holds a reference to a
specific frame/window — origin alone is right for most cases, but for
high-privilege actions verify the source is the window you opened.

## Safe send

Never target `"*"` — the message is readable by any listener on that window:

```js
// Wrong:
iframe.contentWindow.postMessage(data, "*");
// Right:
iframe.contentWindow.postMessage(data, "https://embed.example.com");
```

## In service workers

The same rules apply to `message` events in `navigator.serviceWorker` /
`clients` flows: validate `event.origin` and `event.data` before doing
anything with caches or responses.

## Verification

- From an attacker origin, post the payloads in `payloads/postmessage.md`
  and confirm nothing happens (origin check holds).
- From the allowlisted origin, confirm legit messages still work (fix didn't
  break the feature).
- Send oversized / malformed messages and confirm they're dropped, not
  crash or stored.
