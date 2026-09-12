# Open AWAP 2.0

**The open specification of the Augmented Writing Audit Protocol (AWAP) — process-evidence of
human authorship in AI-assisted writing.**

Author: **Rais Busom** · v2.0 (September 2026) · Spec license: CC BY 4.0 · Examples: MIT

> v2.0 replaces v1.0 and is not backwards compatible. If you implemented v1.0, read
> [What changed, and why](#what-changed-in-v20-and-why) first. The old text is kept at
> [`legacy/SPEC-v1.0.md`](legacy/SPEC-v1.0.md) so that certificates already issued under it
> remain readable.

---

## The problem

AI-assisted works sit in a legal and reputational gray zone. The U.S. Copyright Office
(*Copyright and Artificial Intelligence, Part 2*, January 2025) held that prompts alone do not
make an output copyrightable and that selecting among AI outputs is not enough either — what
counts is the human expression perceptible in the result, the creative selection and arrangement,
and creative modification. Amazon KDP requires AI-content disclosure. Authors have been publicly
accused of publishing "AI slop" with no standard way to answer.

Existing certifications verify the **result** (post-hoc text scans, sworn declarations) or the
**identity** of the author. Neither records the **process** — and no detector can recover a
process that was never observed.

## What AWAP does

AWAP defines a minimal, tool-agnostic protocol for logging a writing process as it happens and
for reporting, from that log alone, **two numbers that are never combined**:

- **Coverage (X axis)** — from which point in the life of the work a record exists. It is fixed
  once, when the work enters the registry, and never changes.
- **Authorship in what was observed (Y axis)** — the **HAS** (Human Authorship Score), computed
  over the recorded window only, with the same formula in both tracks.

A work that enters with a finished manuscript can still earn a high Y: the protocol documents the
rewriting. What it can never earn is a claim about its origin, because nobody watched it being
written. That distinction is the whole protocol.

## The two tracks

The track is **derived** from the entry point, not chosen by the author:

| Entry point | Coverage | Track |
|---|---|---|
| `premise` — not one word of the work exists yet | 100 | Origin |
| `bible` — premise or synopsis already written outside the record | 85 | Origin |
| `outline` — structure exists outside the record; no prose | 75 | Origin |
| `partial_draft` — prose exists, incomplete | 50 | Transformation |
| `manuscript` — a complete manuscript exists | 20 | Transformation |
| `file` — only the finished file; no process will follow | 0 | Transformation |

A work on the Transformation track MUST seal its starting file (V0) by hash, MUST run a
provenance scan on it, and MUST carry a signed **origin declaration** from the author, which the
protocol records and **never verifies**. AI used during rewriting counts exactly as it does on the
Origin track: without that rule, the Transformation track would be a laundering mechanism.

## The four quadrants

Conventional boundary at 50 on both axes. A work at 51 and a work at 49 are not different kinds
of thing; show the point and its band, never the line as if it separated natural categories.

| | Y high | Y low |
|---|---|---|
| **X high** | **Q1 · Verified authorship** — the only position that admits the full claim | **Q4 · Documented generation** — a recorded process that shows little human authorship |
| **X low** | **Q2 · Accredited transformation** — documented human work on an unobserved base | **Q3 · Unaccredited** — sealed and scanned only; no score |

Q4 is not the failure quadrant: it is what makes the instrument serious, and it has its own
market — anyone who must declare accurately to a platform or a publisher needs exactly this
proof.

## How the score is computed

Everything is derived from events; nothing from a scan of the text. Seven components, published
weights, versioned (`has_version`). Weights are product policy, not mathematics: publish them,
version them, and never change them inside a project without recomputing and saying so.

| Component | Signal | Weight (2.1) |
|---|---|---|
| Pure human text | words never generated, over final words | **5** |
| Non-literal decisions | human decisions on plot, character, POV, chronology, ending | **4** |
| Subsequent intervention | how much of what was kept the human reworked, graded by how much changed | **3** |
| Documentary precedence | documents authored before the first generation | **2** |
| Selection and rejection | proposals discarded over proposals decided | **2** |
| Direction | volume of human instruction over volume generated | **1** |
| Temporal continuity | dispersion of sessions across distinct days | **1** |

The weighting follows what a registrar actually recognises: human expression and creative
modification weigh most; choosing among outputs and writing prompts weigh least, because on their
own they do not establish authorship.

**Rules that matter more than the weights:**

- A component with no data is **excluded and renormalised** — never imputed. The certificate says
  which components took part and which did not.
- With no generation events in the window there is **no score at all** (Q3). A work nobody watched
  being written cannot score 100 for "no AI text conserved".
- The result is reported as an **exact value and a band of 10**. The exact number is what people
  ask for; the band is what says how much precision the number really has.

## The certificate

Every issuance carries the same eight sections in the same order. **The origin section does not
disappear on the Transformation track: it stays visibly empty.** The gap communicates better than
any explanation.

1. Identification of the work and the author
2. **Origin** — Origin track: the documentary chain. Transformation track: `[NOT RECORDED]`, the
   entry date, and the author's declaration
3. **Recorded process** — window, sessions, events, version chain
4. **Position** — coverage · score (exact value and band) · quadrant · `has_version`
5. **Transformation** — Transformation track only
6. **Declared and recorded AI use**
7. **What this certificate does not accredit** — mandatory, fixed text
8. **Hash chain and signature**

Section 7 is not a disclaimer bolted on by a lawyer; it is the reason the rest can be believed:

> This certificate does not accredit the origin of any text predating the date of entry into the
> registry. It contains no AI-text detector and does not rely on one. It does not claim the work
> is "human", "AI-free", or any single percentage of humanity. Coverage and the score are
> different measures over different windows: they are not summed, and they are not compared
> across quadrants. AWAP does not prevent fraud: it makes the certificate state only true things.

Never, on any track or in any derived marketing material: "human work", "written by a human",
"AI-free" without the explicit window; any claim about origin on the Transformation track, even
hedged; a single percentage of humanity; or a comparison of scores across quadrants.

## What this repository contains

| File | Contents |
|------|----------|
| [`SPEC.md`](SPEC.md) | The protocol: entry points, tracks, event model, score, quadrants, certificate, verification, conformance |
| [`examples/certificate.jsonld`](examples/certificate.jsonld) | A complete sample JSON-LD credential |
| [`examples/verify-offline.md`](examples/verify-offline.md) | Step-by-step offline verification |
| [`legacy/SPEC-v1.0.md`](legacy/SPEC-v1.0.md) | v1.0, superseded, kept for certificates issued under it |

## What this repository does NOT contain

AWAP is **an open spec with independent implementations**. Reference implementations (the logging
engine, the certificate generator, the editorial tooling built on top) are commercial products and
are not part of this repository. Anyone may implement the protocol from this spec — that is the
point of publishing it.

## What changed in v2.0, and why

v1.0 scored a work by which foundational documents existed and how much of the AI's text the human
had revised, and produced **one number** between 0 and 100.

Three problems, in order of severity:

1. **It rewarded claims it could not observe.** A `premise` document scored 100 points whether the
   record had watched it being written or the author had dropped it in afterwards. v2.0 fixes the
   observation window as a separate axis and never lets it be traded against the score.
2. **A single number invites exactly one question: "is it high?"** Once a single figure exists, it
   is the only one anyone reads, and it becomes the single surface to attack in a dispute. v2.0
   reports two numbers and forbids combining them, in any form, including a weighted average "for
   internal use only".
3. **It had no place for the most common case:** an author with a finished manuscript who wants to
   document the rewriting. v1.0 could only score it low; v2.0 gives it the Transformation track,
   with the origin left visibly unrecorded.

Migration: v1.0 certificates stay valid as v1.0 documents. A v1.0 `hasScore` is **not** comparable
to a v2.0 score and must not be presented as one.

## Design principles

- **Process over result.** A scan of finished text can be fooled in either direction; a
  session-by-session trail bound to the final text cannot be retrofitted.
- **AWAP certifies what it observed, never what it infers.** Origin is not recoverable after the
  fact, and the protocol says so instead of guessing.
- **Evidence, not guarantee.** An AWAP dossier is documentation an author can present — to a
  platform, a publisher, or a registrar. It is not a legal warranty.
- **A low score must be reachable.** If it were not, this would be a provenance laundry.
- **Private by default.** The position belongs to the author: the registry keeps the whole record
  and the author decides what to publish.
- **Tool-agnostic.** The protocol assumes no particular AI model, writing app, or vendor.

## Status

v2.0 — stable. The model, the two tracks, the score and the certificate document are implemented
in the reference implementation and ship with its next release. Three parts are specified and
**not yet implemented anywhere**: transformation depth (§4.6), the JSON-LD credential (§8.4) and
the public anchoring of the certificate hash (§8.3) — which is why certificates issued today are
marked provisional, as §8.3 requires. Feedback and implementation reports: open an issue.

---

© 2026 Rais Busom. Specification text licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code examples under MIT.
