# Open AWAP — Specification v1.0

**Augmented Writing Audit Protocol (AWAP)** · Rais Busom · June 2026
Spec license: CC BY 4.0 · Status: stable

This document specifies (1) the event model for recording an AI-assisted writing
process, (2) the Human Authorship Score (HAS 2.0), (3) the certificate artifacts,
and (4) the verification procedures. Conformance keywords (MUST, SHOULD, MAY) are
to be interpreted as in RFC 2119.

---

## 1. Concepts

- **Project** — one written work (book, manuscript, screenplay) under audit.
- **Session** — a contiguous writing period. Events belong to exactly one session.
- **Event** — an append-only record of a single act in the writing process.
- **Dossier** (expediente) — the complete ordered event log of a project plus its
  session metadata. The dossier is the *process evidence*.
- **Certificate** — the signed summary artifact derived from the dossier at
  completion time.

An implementation MUST persist events append-only and MUST NOT allow editing or
deleting past events through the normal writing workflow.

## 2. Event model

Every event carries at minimum:

```
ts            ISO-8601 timestamp (UTC)
session_id    opaque identifier of the active session
event_type    one of the types below
```

### 2.1 Event types

| `event_type` | Meaning | Required fields |
|---|---|---|
| `document_created` | The human authored a foundational document | `document_type`, `tokens_revised_by_human` (≈ word count × 1.33) |
| `text_generated` | An AI generated text | `document_type` (usually `draft`), `ai_model`, `tokens_generated` |
| `text_revised` | The human revised/rewrote AI-generated text | `tokens_revised_by_human` |
| `conversation_turn` | A human instruction to the AI during a session | `directive_weight` (see §3.2) |

### 2.2 Document types and authorship levels

`document_type` classifies the *intellectual layer* a document belongs to:

| Level | `document_type` | Points |
|---|---|---|
| 1 | `premise` | 100 |
| 2 | `synopsis` | 85 |
| 3 | `bible` (project/world bible) | 75 |
| 4 | `outline` | 60 |
| 5 | `style_instructions` | 40 |
| 6 | (human revision of AI text) | 25 |
| 7 | `draft` (AI-generated text) | 5 |

The point scale encodes the protocol's core thesis: **authorship is conceiving the
work, not typing the words.** A human-written premise weighs 20× an AI-generated
draft token-for-token.

Token estimation: implementations SHOULD use ≈ 1 token per 0.75 words for languages
like English and Spanish when exact counts are unavailable.

## 3. Human Authorship Score (HAS 2.0)

The HAS is a two-component score in [0, 100]: a **documentary core** modulated by a
bounded **conversational axis**.

### 3.1 Documentary HAS

```
HAS_doc = Σ (points_level × presence_level × revision_ratio_level) / max_possible × 100
```

- `presence` ∈ {0, 1}: whether the project contains a human-authored document at
  that level.
- `revision_ratio` ∈ [0, 1]: for AI-generated layers, the share of AI tokens the
  human subsequently revised (from `text_revised` events over `text_generated`
  totals). For purely human levels it is 1.
- `max_possible` is the sum of points for all levels.

### 3.2 Conversational modifier (±10%)

```
HAS_final = HAS_doc × clamp(0.9 + 0.2·C, 0.90, 1.10)
```

where **C** measures how *directive* the human was versus how autonomous the AI was:

```
C = Σ directive_weight(human turns)
    ─────────────────────────────────────────────────────────
    Σ directive_weight(human turns) + count(text_generated)
```

| Human turn | `directive_weight` |
|---|---|
| Empty or trivial ("ok", "continue", "thanks") | 0.1 |
| Very short (< 12 characters) | 0.2 |
| Substantive (decision, correction, direction) | 1.0 |

The conversational axis MUST NOT move the score more than ±10%. The documentary
core always dominates.

### 3.3 Interpretation bands (informative)

80–100 dominant human authorship · 50–79 genuine co-authorship ·
20–49 AI-dominant · 0–19 mostly AI.

## 4. Certificate artifacts

On completion (`sign` operation), an implementation MUST produce:

| Artifact | Description |
|---|---|
| Certificate document (e.g. PDF) | Human-readable: title, author, HAS with level breakdown, AI models used, hashes, and a QR code pointing to the public verification URL |
| JSON-LD credential | Machine-readable credential (see §4.1) with SHA-256 integrity, verifiable offline |
| License/summary record | Full signing data (JSON) retained with the dossier |

### 4.1 JSON-LD credential

The credential uses schema.org plus an `awap:` vocabulary. Required properties:

```jsonc
{
  "@context": ["https://schema.org", {"awap": "https://awap.dev/vocab#"}],
  "@type": "CreativeWork",
  "name": "<title>",
  "author": {"@type": "Person", "name": "<author>"},
  "dateCreated": "<ISO-8601>",
  "awap:hasScore": 87,                      // HAS_final, integer 0-100
  "awap:scoreBreakdown": { /* per-level contributions */ },
  "awap:aiModels": ["<model identifiers used>"],
  "awap:manuscriptHash": "sha256:<hex>",    // hash of the final manuscript
  "awap:logHash": "sha256:<hex>",           // hash of the canonical event log
  "awap:certHash": "<16 hex chars>",        // see §4.2
  "awap:verifyUrl": "<public verification URL>",
  "awap:integrity": "sha256:<hex>"          // see §5.2
}
```

### 4.2 cert_hash

`cert_hash` is 16 hexadecimal characters derived from
`SHA-256(manuscript_hash ‖ log_hash ‖ signing_timestamp)` (first 16 hex chars).
It is the public identifier of the certificate.

### 4.3 Signing gate (normative)

An implementation MUST refuse to sign unless an audit verdict over the final
manuscript exists and is **timestamped later than the most recent manuscript
change**. If content changes after the verdict, the gate MUST be re-run.
Rationale: the value of the certificate *is* the rigor of its process.

## 5. Verification

### 5.1 Public verification (online)

The QR / `awap:verifyUrl` resolves to a public page showing title, author, HAS,
models used, and hashes — with **no login**. Verifiers compare the certificate in
hand against the published record.

### 5.2 Offline verification (no network, no vendor)

The JSON-LD credential is self-verifying:

```js
// 1. Remove awap:integrity; 2. canonical JSON.stringify of the rest; 3. SHA-256.
const { "awap:integrity": stored, ...body } = credential;
const recomputed = "sha256:" + sha256(JSON.stringify(body));
console.log(recomputed === stored); // true = untampered
```

Additionally, anyone holding the final manuscript MAY recompute
`awap:manuscriptHash` to bind the credential to the exact text.

## 6. Privacy

Only certificate metadata is published for verification. The raw event log
(the dossier) remains with the author and is disclosed at the author's discretion
(e.g., to a registrar or platform on request). Implementations MUST NOT publish
manuscript content or raw events as part of verification.

## 7. Conformance

An implementation is **AWAP-conformant** if it: (a) records the four event types
append-only with the required fields; (b) computes HAS 2.0 exactly as §3;
(c) produces the three artifacts of §4 including the JSON-LD credential with
integrity; (d) enforces the signing gate of §4.3; and (e) supports both
verification procedures of §5.

---

© 2026 Rais Busom · CC BY 4.0. Cite as: *Busom, R. — Open AWAP: Augmented Writing
Audit Protocol, v1.0 (2026).*
