# Paper handoff — continue in next session

**Manuscript:** `paper/qpd_reactor_cevns_spectra.tex` (PRD full article, RevTeX 4-2, two-column).
**Branch:** `claude/qpd-cevns-muon-spectrum-aaa8da`. **Last commit:** `2fcf6f2` (draft full PRD manuscript). Working tree is clean.

## Current state
- **First full draft complete and compiles cleanly** (0 undefined citations, 0 undefined refs, 0 multiply-defined labels, 0 errors; 13 pp).
- Sections are separate files under `paper/sections/` and `\input` into the master: intro, model, cevns, backgrounds, response, results, discussion, conclusions, appendix-cevns, appendix-response. Abstract + figures + acknowledgments are in the master.
- **Bibliography** `paper/references.bib`: 21 entries, verified against arXiv/INSPIRE/DOI/NIST (no hallucinations). `guan2015` is preprint-only (arXiv:1509.06176, intentionally no journal coords); `labchico2022` author list trimmed to verified names + "and others".
- **Figures** in `paper/figures/`: `reconstructed_energy_spectra.pdf` (main, Fig.~spectra), `energy_response.pdf` (Fig.~response), `cevns_dRdT_deposited.pdf` (Fig.~cevns). Regenerate from the repo via the phase-6/5/3 scripts if the underlying data changes.

## NOT done yet (next steps, in order)
1. **Confirm author list + affiliation.** The title page has a `[PLACEHOLDER]` affiliation ("Lanqing Yuan, Washington University in St. Louis") — only the human can set the real author list (co-authors? the QPD group?). Edit `\author`/`\affiliation` in the master (or `authors` in `PAPER-CONFIG.json`).
2. **Run the staged referee / peer review:** `/gpd:peer-review paper/qpd_reactor_cevns_spectra.tex` (six-pass adversarial review: overclaim, math/physics soundness, significance, etc.). This produces the review-contract artifacts (BIBLIOGRAPHY-AUDIT.json, reproducibility-manifest.json, REFEREE-REPORT). Address findings.
3. Optional: expand any section; tighten toward a specific PRD length; add a systematics table.

## BUILD RECIPE (from `paper/`)
```
pdflatex -interaction=nonstopmode qpd_reactor_cevns_spectra.tex
bibtex   qpd_reactor_cevns_spectra
pdflatex -interaction=nonstopmode qpd_reactor_cevns_spectra.tex
pdflatex -interaction=nonstopmode qpd_reactor_cevns_spectra.tex
```
(or `latexmk -pdf qpd_reactor_cevns_spectra.tex`). Build artifacts (`*.aux/log/out/bbl/...`) are gitignored.

## ⚠ GOTCHAS — read before touching the paper
- **Do NOT re-run `gpd paper-build`.** The master was hand-refactored after the initial build: (a) split into `\input{sections/*}` files, (b) `\documentclass` changed `prl`→`prd` (full article), (c) abstract + figure captions fixed to real LaTeX. Re-running `gpd paper-build` regenerates the master from `PAPER-CONFIG.json` and would REVERT all three. Edit the master/section files directly instead. (`PAPER-CONFIG.json`'s section `content` fields still hold the ORIGINAL plain-text seeds — they are stale; the section `.tex` files are authoritative.)
- **`paper/ARTIFACT-MANIFEST.json` sha256 is stale** (master was hand-edited after build). The peer-review preflight may flag it — regenerate/reconcile the manifest against the final master at that point (without overwriting the master), or update it to the current sha.
- **Label convention:** the CEvNS flux fold is `eq:cevnsfold` (in cevns.tex + appendix-cevns.tex); the response matrix fold is `eq:fold` (in results.tex). Keep them distinct.

## Project facts the paper depends on (already in the repo/memory)
- **Non-paralyzable censoring** is the adopted project-wide convention (CONVENTIONS §F resolved 2026-07-21). Paralyzable is a computed sensitivity only.
- **Display rule: nothing below 10 eV** on any figure (memory `plot-energy-floor-10ev`; enforced in `src/qpd_potential/fold.py` xlim). Keep this for any new/regenerated figure.
- The **four honest caveats** must stay stated (abstract/discussion/conclusions): (1) no saturated-regime response anchor → muon pile-up is an instrumental artifact, not a line; (2) site-dependent ±factor-2 γ flux; (3) sub-1.8 MeV reactor-flux placeholder (~6–10% band below 95 eV); (4) f_prompt/r crossover band. Framing is **stage-1 feasibility**, never sensitivity/discovery.
- Phase SUMMARY/VERIFICATION **frontmatter was normalized** (commits b439508/2e7eca7/8538a0a) so `gpd validate review-preflight write-paper --strict` passes.
- Running `pytest tests/` re-stamps a `git_sha` line into `data/flux/*.csv` (cosmetic) — revert with `git checkout -- data/flux/*.csv` to keep the tree clean.

## How to resume
Open a fresh session in this worktree and either read this file, or run `/gpd:resume-work`, then `/gpd:peer-review paper/qpd_reactor_cevns_spectra.tex`.
