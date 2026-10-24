# Hardening Electron / Tauri / WebView bridges

## Electron — the secure baseline

Main process window config:

```js
const win = new BrowserWindow({
  webPreferences: {
    contextIsolation: true,   // renderer can't reach Node
    nodeIntegration: false,   // no require() in the renderer
    sandbox: true,            // renderer runs sandboxed
    preload: path.join(__dirname, "preload.js"),
  },
});
```

Preload — expose only the channels the renderer needs:

```js
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("app", {
  saveNote: (payload) => ipcRenderer.invoke("notes:save", payload),
  // Never: ipcRenderer.send / ipcRenderer.invoke with an arbitrary channel.
});
```

Main — validate sender AND arguments on every channel:

```js
ipcMain.handle("notes:save", (event, payload) => {
  // 1. Sender: which frame is calling?
  const url = new URL(event.senderFrame?.url ?? "");
  if (url.origin !== "https://app.example.com") return { error: "bad sender" };

  // 2. Arguments: never trust the renderer's claims.
  if (typeof payload?.title !== "string" || payload.title.length > 200) {
    return { error: "invalid payload" };
  }
  if (typeof payload?.body !== "string" || payload.body.length > 50_000) {
    return { error: "invalid payload" };
  }

  // 3. Act with validated data only.
  return saveNote({ title: payload.title, body: payload.body });
});
```

Treat every renderer as potentially compromised: XSS in the renderer must
not become RCE in the main process.

## shell.openExternal / openPath — allowlist everything

```js
const SAFE_SCHEMES = new Set(["https:", "http:", "mailto:"]);

function safeOpenExternal(raw) {
  try {
    const u = new URL(String(raw));
    if (!SAFE_SCHEMES.has(u.protocol)) return;
    if (u.protocol === "http:" || u.protocol === "https:") {
      // host allowlist too, if the app only opens known sites
    }
    shell.openExternal(u.href);
  } catch {
    /* invalid URL — drop it */
  }
}
```

`file:` is never in the allowlist for user-controlled input — that's the RCE.

## Tauri

- **Capabilities:** list only the commands the frontend may invoke; don't
  grant `core:default` + everything.
- **`dangerousRemoteDomainIpcAccess`** must stay false — remote content
  (http(s) pages loaded in the webview) must not reach IPC at all. If a
  remote page genuinely needs a command, expose a minimal wrapper with
  validation, not the raw `invoke` surface.
- **Shell plugin:** never pass user input to `Command`/`open` without
  allowlisting arguments and the binary path.
- **CSP:** set `app.security.csp` in `tauri.conf.json` (see csp.md).

## Android / iOS WebView

```java
// Android — never for remote content:
webView.getSettings().setJavaScriptEnabled(true);      // only for trusted local content
webView.getSettings().setAllowFileAccess(false);
webView.getSettings().setAllowContentAccess(false);
// Do NOT addJavascriptInterface() on a WebView that loads remote pages.
```

The classic CVE-2012-6636-class bug is a JS bridge exposed to remote pages
— every message the page can reach is an RCE. If a bridge is unavoidable:
allowlist the injected object's methods, validate every argument in the
native layer, and load only HTTPS content you control.

## Verification

- In the audit report, map each hardening item to the Electron/Tauri/WebView
  grep group hits so the user can see exactly which flags were checked.
- Test the IPC surface: from a compromised-renderer mindset, attempt to
  invoke channels that weren't exposed (must be rejected by the main
  process, not by UI hiding).
