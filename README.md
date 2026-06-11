# Open AWAP

**The open specification of the Augmented Writing Audit Protocol (AWAP) — process-evidence of human authorship in AI-assisted writing.**

Author: **Rais Busom** · v1.0 (June 2026) · Spec license: CC BY 4.0 · Examples: MIT

---

## The problem

AI-assisted works sit in a legal and reputational gray zone. The U.S. Copyright Office
(*Copyright and Artificial Intelligence, Part 2*, Jan 2025) ruled that only the
**documented human contribution** of an AI-assisted work is copyrightable. Amazon KDP
requires AI-content disclosure. Authors have been publicly accused of publishing
"AI slop" — with no standard way to defend their process.

Existing certifications verify the **result** (post-hoc text scans, sworn declarations)
or the **identity** of the author. None of them record the **process**.

## What AWAP does

AWAP defines a minimal, tool-agnostic protocol for logging the writing process as it
happens — what the human wrote, what the AI generated, what the human revised, and when —
and for deriving from that log:

1. a **Human Authorship Score (HAS, 0–100)** that weighs *intellectual authorship*
   (who conceived the work) over typing volume, and
2. a **verifiable certificate**: a signed document with a QR code pointing to a public
   verification URL, plus a JSON-LD credential with SHA-256 integrity that can be
   verified **offline**, with no account and no vendor.

The audit trail is *process evidence* — the same class of documentation the U.S.
Copyright Office asks for when registering AI-assisted works. AWAP makes that dossier
build itself, session by session.

## What this repository contains

| File | Contents |
|------|----------|
| [`SPEC.md`](SPEC.md) | The protocol: event model, document levels, HAS formula, certificate format, verification procedures |
| [`examples/certificate.jsonld`](examples/certificate.jsonld) | A complete sample JSON-LD credential |
| [`examples/verify-offline.md`](examples/verify-offline.md) | Step-by-step offline verification (10 lines of code) |

## What this repository does NOT contain

AWAP is **an open spec with independent implementations**. Reference implementations
(the logging engine, the certificate signer, the editorial tooling built on top) are
commercial products and are not part of this repository. Anyone may implement the
protocol from this spec — that is the point of publishing it.

First registered precedent: the author registered his own AI-assisted book,
*Hacking Hemingway*, with the U.S. Copyright Office.

## Design principles

- **Process over result.** A scan of finished text can be fooled in either direction;
  a session-by-session trail bound to the final text cannot be retrofitted.
- **Evidence, not guarantee.** An AWAP dossier is documentation an author can present —
  to a platform, a publisher, or a registrar. It is not a legal warranty.
- **Verifiable by anyone.** Public QR verification requires no account; offline JSON-LD
  verification requires no network.
- **Tool-agnostic.** The protocol does not assume any particular AI model, writing app,
  or vendor.

## Status

v1.0 — stable. The event model and HAS 2.0 formula are in production use.
Feedback and implementation reports: open an issue.

---

© 2026 Rais Busom. Specification text licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code examples under MIT.
