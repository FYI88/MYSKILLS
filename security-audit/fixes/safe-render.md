# Safe rendering (XSS sinks)

## Rule of thumb

- **Prefer `textContent`** over `innerHTML` whenever the content is data.
- **If you must render HTML** (rich text, markdown), sanitize with a
  maintained library (`DOMPurify`) at the boundary, configured strict, never
  with raw-HTML passthrough enabled.
- **Context-aware escaping:** escaping for one context is not escaping for
  another. HTML body, attribute, URL, and JS each need their own treatment.

## Vanilla JS — escaping helpers

```js
const HTML_ESCAPES = {
  "&": "&amp;", "<": "&lt;", ">": "&gt;",
  '"': "&quot;", "'": "&#39;", "`": "&#96;",
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"'`]/g, (c) => HTML_ESCAPES[c]);
}

// For attribute values: same set (quotes are the dangerous ones here).
function escapeAttr(value) { return escapeHtml(value); }

// For URLs: never escape into href/src — allowlist schemes + parse:
function safeUrl(raw) {
  try {
    const u = new URL(String(raw), window.location.origin);
    return ["https:", "http:", "mailto:"].includes(u.protocol) ? u.href : "#";
  } catch {
    return "#";
  }
}
```

## Framework sinks

React — never string-concat into `dangerouslySetInnerHTML`; sanitize first:

```jsx
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userHtml) }} />
```

Vue — same idea behind `v-html`; sanitize before binding, or filter it out
of the template entirely and use interpolation (`{{ }}`) which escapes:

```html
<div v-html="sanitizedHtml"></div>
<!-- script -->
this.sanitizedHtml = DOMPurify.sanitize(userHtml);
```

Angular — `bypassSecurityTrustHtml` on unsanitized input is the bug; keep
`DomSanitizer` for *static* trusted templates only and sanitize dynamic
content:

```ts
import DOMPurify from "dompurify";
this.safeHtml = this.sanitizer.bypassSecurityTrustHtml(
  DOMPurify.sanitize(userHtml)
);
```

Svelte — `{@html}` is an innerHTML; sanitize at the boundary:

```svelte
<!-- +page.svelte -->
{@html sanitized}
<!-- script -->
import DOMPurify from "dompurify";
$: sanitized = DOMPurify.sanitize(userHtml);
```

## DOMPurify configuration

```js
DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "br", "ul", "ol", "li"],
  ALLOWED_ATTR: ["href", "title", "target"],
  ALLOW_DATA_ATTR: false,
});
```

Keep the allowlist minimal; `ALLOWED_TAGS` + `ALLOWED_ATTR` beats
blocklist-based config, and `ALLOW_DATA_ATTR: false` kills a common bypass
family.

## Also fixes DOM clobbering

Rendering via `textContent`/escaping means an attacker-injected
`<img id=x name=y>` is inert — there is no HTML to clobber with. Prefer
module-scoped state over `window.<name>` reads so injected elements can't
shadow application globals.
