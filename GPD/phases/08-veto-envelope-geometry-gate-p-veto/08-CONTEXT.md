# Phase 8 Context — Veto-Envelope Geometry Gate (P-VETO)

**Status:** No `/gpd:discuss-phase` session was run for this phase.
**Recorded:** 2026-07-22, during autonomous roadmap execution.

## Provenance of this file

This file is **not** a transcript of a discussion with the user. It exists to record,
honestly and auditably, what the binding intent for Phase 8 actually is, given that the
user issued a standing session directive to run the roadmap to completion without
per-phase discussion unless a genuine blocker arises.

No new user decisions were collected while writing this file. Everything below is
transcribed from artifacts that already existed before this session's execution began.

## Decisions (LOCKED — carried from prior artifacts, not newly elicited)

1. **The five ROADMAP Phase 8 success criteria are binding verbatim.** See
   `GPD/ROADMAP.md`, section "### Phase 8: Veto-Envelope Geometry Gate (P-VETO)".
   They are the definition of done for this phase.

2. **Forbidden proxies are binding, including one explicit prior user decision.**
   From the same ROADMAP section: `fp-veto-credit-transfer` (inheriting gram-scale
   rejection factors for a 110 g monolithic wafer); **inventing a resized veto or
   continuing with a reduced veto credit if the gate fails — recorded in the ROADMAP as
   an explicit user decision dated 2026-07-22**; and proceeding past a failed gate on a
   premise already known false.

3. **Requirement VALD-09** is the requirement this phase advances. See
   `GPD/REQUIREMENTS.md`.

4. **Stop-condition behavior is fixed by SC5.** If the wafer does not fit, the phase
   reports the milestone premise as void and returns control to the user for re-scope.
   It does not assume a reduced veto credit and does not invent a resized veto.

## Agent's Discretion

- Method for reading the veto envelope dimensions, subject to the evidence-route
  amendment documented in `08-03-PLAN.md` (the ROADMAP's named source, NUCLEUS
  EPJC 86,29 Fig. 1e/f, was verified during research to carry no scale bar and no
  dimension callout).
- Module decomposition, test design, and artifact layout.
- Which comparison basis carries the verdict, provided the choice is justified by
  stated precision intervals and sign-robustness rather than asserted.

## Deferred / Out of Scope

- Any Phase 9–16 work. This phase is a gate only.
- Crediting the ~10,300 QPD sensors as a spatial-coincidence handle (recorded during
  research as a future direction with an explicit prohibition on crediting it in v2.0).
- Editing `GPD/REQUIREMENTS.md` VALD-09 or the ROADMAP anchor line to fix the
  unlabelled "~9 cm²" footprint figure. Plan 08-05 flags it; no plan edits those files.

## Open items carried into execution

- The Goupy 2024 thesis (HAL tel-05298505) is not machine-retrievable in this
  environment. It is planned as optional, non-blocking enrichment requiring a manual
  browser download by the user. It is the only route that could plausibly overturn the
  expected verdict.
- Research-doc §F1 was found false during planning round 2 and retracted in place. The
  planner recorded that it was wrong **in the direction that favoured the project's
  expected conclusion**, and flagged other F1-dependent content in that document as
  suspect until re-checked.
