# DOM clobbering payloads

Elements with `id` / `name` attributes become properties of `window` (and,
for forms, of `document.forms`). If library or app code reads
`window.<name>` or checks `if (x)` where `x` is a name an attacker can
inject, the element replaces the expected value.

## Basic clobber

Inject before the script that reads the global:

```html
<img id=x>
<img id=x name=y>            <!-- x.y becomes the element -->
<form id=x name=y></form>    <!-- x.y = form element -->
<a id=x name=y href="https://attacker.example"></a>
```

Then code like `if (window.x) { ... }` or `window.x.y` behaves differently
than the author intended.

## Clobbering a specific API surface

```html
<img name=config>            <!-- if code reads window.config -->
<iframe name=config>         <!-- config.contentWindow = attacker page -->
<form name=location>         <!-- shadows window.location in some engines -->
```

## Realistic gadget: `document.getElementById` confusion

Some libraries check `document.getElementById('x')` and then use the result's
properties. Injecting `<img id=x src=x onerror=...>` can turn the check into
an execution. The exact gadget depends on the library — prove it in the app.

## Triggering it

- XSS that can inject HTML but can't execute JS (e.g. CSP blocks inline
  handlers) is often enough: the clobber itself is the exploit, no script
  needed.
- User-controlled HTML in a comments/messages/rich-text feature is the most
  common entry.

## Fix reference

See `fixes/safe-render.md` (escape instead of injecting) — and note that
clobbering also argues for code that reads explicit globals defensively
(`globalThis.hasOwnProperty("x")` or module-scoped state instead of
`window.x`).
