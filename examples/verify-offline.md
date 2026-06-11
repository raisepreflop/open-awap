# Verifying an AWAP credential offline

No network, no account, no vendor. You need the `certificate.jsonld` file and,
optionally, the final manuscript.

## 1. Integrity of the credential (Node.js)

```js
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const credential = JSON.parse(readFileSync("certificate.jsonld", "utf8"));
const { "awap:integrity": stored, ...body } = credential;
const recomputed = "sha256:" +
  createHash("sha256").update(JSON.stringify(body)).digest("hex");

console.log(recomputed === stored ? "UNTAMPERED ✓" : "TAMPERED ✗");
```

The same in Python:

```python
import hashlib, json

cred = json.load(open("certificate.jsonld"))
stored = cred.pop("awap:integrity")
recomputed = "sha256:" + hashlib.sha256(
    json.dumps(cred, separators=(",", ":"), ensure_ascii=False).encode()
).hexdigest()
print("UNTAMPERED" if recomputed == stored else "TAMPERED")
```

> Note: integrity is computed over the canonical serialization produced by the
> signer. Implementations MUST document their canonicalization (key order,
> separators) so independent verifiers can reproduce it.

## 2. Binding to the manuscript (optional)

If you hold the final manuscript file, recompute its hash and compare with
`awap:manuscriptHash`:

```bash
shasum -a 256 manuscript.docx
```

## 3. Public cross-check (optional, online)

Open `awap:verifyUrl` (or scan the QR on the certificate document) and compare
title, author, HAS and hashes with the credential in hand.
