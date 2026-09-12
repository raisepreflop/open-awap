# Offline verification

No network, no account, no vendor. Everything below runs against the JSON-LD credential
([`certificate.jsonld`](certificate.jsonld)) and, optionally, a sealed version of the manuscript.

## 1. Is the credential untampered?

```js
import { createHash } from "node:crypto";
const sha256 = (s) => "sha256:" + createHash("sha256").update(s).digest("hex");

const credential = JSON.parse(await fs.readFile("certificate.jsonld", "utf8"));
const { "awap:integrity": stored, ...body } = credential;
console.log(sha256(JSON.stringify(body)) === stored);   // true = untampered
```

## 2. Is this credential about *this* file?

Hash the **bytes** of the file, not its extracted text, and look for the result in
`awap:versions`:

```bash
shasum -a 256 la-casa-v1.docx      # → compare with awap:versions[].sha256
```

A match binds the credential to that exact file. No match means the credential is about a
different state of the work — which is a fact about the file, not necessarily a forgery: a work
has as many sealed versions as it has sealings.

## 3. What does it actually claim?

Read these five fields together, in this order, and refuse to read any of them alone:

| Field | Question it answers |
|---|---|
| `awap:coverage` | From what point in the life of the work does a record exist? |
| `awap:track` | `transformation` means **the origin was never observed** |
| `awap:score` | Authorship in what *was* observed — `value` exact, `band` for its precision |
| `awap:score.excluded` | Which components had no data and were left out |
| `awap:quadrant` | The pair, read as a position |

`coverage` and `score.value` MUST NOT be summed or averaged (SPEC §6.1). A credential that
carries a combined figure is not AWAP 2.0 conformant, whatever it is called.

## 4. Is it verifiable by a third party yet?

```js
if (credential["awap:provisional"]) {
  // Not anchored in any public registry: nobody can check it from outside.
  // The local record signature only detects hand edits that did not recompute it.
}
```

## 5. What it does not tell you

- Nothing about the origin of text predating `awap:entryTs`.
- Nothing derived from a detector: there is none in the protocol.
- `awap:baseline.declarationOptions` is the **author's declaration**, recorded and unverified
  (`declarationVerified` is always `false`).
- `provenanceScan` documents declarations found inside the file. Finding no marks never means the
  text is human.
