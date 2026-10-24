# Encryption-at-rest for sensitive client-side data

WebCrypto AES-GCM with a PBKDF2-derived key. Protects data at rest against
device theft, shared-device users, and other apps/extensions.

## Honest limits — read this before applying

- **XSS defeats this.** The key must live in the page to decrypt, so any
  script running in the origin can decrypt too. Encryption-at-rest is a
  *defense layer*, not a replacement for fixing XSS.
- A passphrase the user types is the only key material a device thief can't
  copy. Deriving from a stored constant protects nothing.
- This does not protect against the *partner* who knows the passphrase —
  which is exactly the threat model of a couples app, so pair it with an
  explicit unlock step, not silent decryption.

## Module: encrypt/decrypt JSON with a passphrase

```js
// storage-crypto.js
const enc = new TextEncoder();
const dec = new TextDecoder();

async function deriveKey(passphrase, salt) {
  const baseKey = await crypto.subtle.importKey(
    "raw", enc.encode(passphrase), "PBKDF2", false, ["deriveKey"]
  );
  return crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: 600_000, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

function bytesToB64(bytes) {
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}

function b64ToBytes(b64) {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

export async function encryptJSON(passphrase, obj) {
  const salt = crypto.getRandomValues(new Uint8Array(16));  // unique per write
  const iv = crypto.getRandomValues(new Uint8Array(12));    // never reused
  const key = await deriveKey(passphrase, salt);
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv }, key, enc.encode(JSON.stringify(obj))
  );
  return {
    v: 1,
    salt: bytesToB64(salt),
    iv: bytesToB64(iv),
    data: bytesToB64(new Uint8Array(ciphertext)),
  };
}

export async function decryptJSON(passphrase, blob) {
  const salt = b64ToBytes(blob.salt);
  const iv = b64ToBytes(blob.iv);
  const key = await deriveKey(passphrase, salt);
  const plaintext = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv }, key, b64ToBytes(blob.data)
  );
  return JSON.parse(dec.decode(plaintext));
}
```

## Usage notes

- **Salt + IV are stored next to the ciphertext** — they are not secrets;
  uniqueness is what matters. A fresh random IV per encryption is
  mandatory (AES-GCM nonce reuse is fatal).
- **600k PBKDF2 iterations** is a current reasonable floor; raise it over
  time and store `v` so old blobs can be migrated.
- **Store the blob with the key** (`v`) so a future format change can be
  detected instead of failing silently.
- **Key in memory:** wipe it when done if the app holds it long-term
  (`crypto.subtle` keys can't be zeroed directly — scope them tightly).
- `btoa`/`atob` on very large blobs: fine for typical app data; for MB-scale
  payloads chunk the base64 conversion.

## When this is and isn't the right fix

- Right: sensitive journal/mood/cycle/message data at rest in a
  shared-device threat model.
- Wrong: a public todo list, or data whose only threat is same-origin XSS
  (fix the XSS; this adds a key-management surface for nothing).
- Architectural note: the strongest fix is *not storing the data
  client-side at all* (server-side with server-managed keys). Say so when
  that's viable.
