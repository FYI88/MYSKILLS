# Prototype-pollution-safe merging & parsing

## The problem

`_.merge(target, userJson)`, `$.extend(true, {}, userJson)`, and hand-rolled
`mergeDeep` functions copy `__proto__` / `constructor.prototype` keys onto
`Object.prototype`, rewriting behavior app-wide.

## Drop-in safe deep merge

```js
const FORBIDDEN_KEYS = new Set(["__proto__", "constructor", "prototype"]);

function isPlainObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v);
}

function safeMerge(target, ...sources) {
  const out = { ...target };
  for (const src of sources) {
    if (!isPlainObject(src)) continue;
    for (const key of Object.keys(src)) {
      if (FORBIDDEN_KEYS.has(key)) continue;          // never copy these
      if (isPlainObject(src[key]) && isPlainObject(out[key])) {
        out[key] = safeMerge(out[key], src[key]);      // recurse safely
      } else {
        out[key] = src[key];
      }
    }
  }
  return out;
}
```

## Hardened JSON.parse

Two options — validate the schema first (best), or strip dangerous keys
(defense-in-depth):

```js
// Option A: schema-validate BEFORE merging (preferred)
const schema = { type: "object", properties: { name: { type: "string" } },
                 additionalProperties: false };
// (use a validator like zod/ajv — this shape is illustrative)
const parsed = JSON.parse(raw);
const cleaned = schemaValidator.parse(parsed);

// Option B: strip dangerous keys at parse time
const SAFE = JSON.parse(raw, (key, value) =>
  FORBIDDEN_KEYS.has(key) ? undefined : value
);
```

## Where to apply it

- Every place untrusted JSON (URL params, `postMessage`, peer messages,
  server responses) is merged into an object or passed to `_.merge` /
  `Object.assign` / custom `mergeDeep` / `$.extend`.
- Query-string / hash parsers that build objects from user input — test the
  `?__proto__[x]=1` and `#__proto__[x]=1` payloads after fixing.
- If the app uses a library known to be pollution-vulnerable
  (older lodash `_.merge`, jQuery `$.extend` deep), pin a patched version
  and keep the key-stripping guard anyway.

## Verification

After the fix, feed the payloads from `payloads/prototype-pollution.md`
through the sink and confirm `({}).polluted` stays `undefined`.
