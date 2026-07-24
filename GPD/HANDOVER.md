# Handover — QPD reactor-CEvNS project

**Written:** 2026-07-23 · **Milestone v2.0 COMPLETE** (all 9 phases, 8–16) · **Suite: 861 passed, 0 failed**
**Branch state:** everything merged to `main`; `origin/main == local main` at `b7472af`.

---

## 0. Read this first

**`notebooks/paper_calculations.ipynb` is the user's.** They hand-edited the single-design figure
cell on 2026-07-23 (commit `b7472af` "Fro DARPA PM") and said *"this is how I want it."* That commit
was prepared for a DARPA PM.

- Do **not** re-execute-and-commit it just to refresh outputs.
- Do **not** sync its parameters or styling to `scripts/make_combined_spectrum.py`.
- If a physics change genuinely requires touching it, say what and why and let the user apply it.

**Known, deliberate divergence** — do not "fix" unilaterally:

| | `SUPP` (muon / γ / neutron) |
|---|---|
| `scripts/make_combined_spectrum.py` | 500 / 100 / 100 |
| `notebooks/paper_calculations.ipynb` | **1000 / 500 / 200** ← user's |

They produce different figures and different S/B. The notebook is the presentation artifact.

---

## 1. Where the project stands

Milestone v2.0 asked: what are the reactor-CEvNS signal and the in-band particle-background budget
for a 4″×4″×2 mm (~110 g) Ge wafer read out by QPDs?

**Phase 8's geometry gate (VALD-09) returned NO FIT** — a face-parallel 10.16 cm wafer needs a
covering circle of 14.3684 cm against a published 10.0 cm COV cap crystal (clearance −4.3684 cm).
The v2.0 premise (sit inside NUCLEUS's shielding/veto at the Chooz VNS) is **void**. Per user
decision the project reverted to the v1.0 paper's **unshielded surface** treatment, with the paper's
**3 GW_th at 25 m** scenario as the primary normalization (∫Φ = 7.5e12, frozen
`data/flux/reactor_flux_v1.0.csv`).

**Headline, unsuppressed** (10–100 eV reconstructed RoI, veto credit exactly 1.0):

| design | S/B (estimates) | S/B (incl. bounds — a *lower* bound) |
|---|---|---|
| Ta→Al | 1.33e−2 | 7.29e−3 |
| Al→Hf | 1.32e−2 | 7.27e−3 |

**With assumed NUCLEUS-equivalent suppression** (script's 500/100/100): S/B = 1.33 / 0.73. That
est. value ≳ 1 is a genuine consistency check — NUCLEUS's own paper claims *"S/B ≳ 1 in the
10–100 eV RoI"* for CaWO₄, and their combined shield+veto factors applied to our Ge signal
reproduce it.

The suppression is an **assumed** scenario, not earned credit: the factors are CaWO₄ event-rate
reductions and most need the COV/MV veto the wafer does not geometrically fit. The user accepted
this explicitly on the premise that a real experiment will build shielding of similar performance.

---

## 2. Open items, roughly by importance

1. **The paper is NOT updated.** `paper/` has zero commits from this milestone; its PDF predates
   everything. Its abstract commits to "the three dominant channels — CEvNS, muons, environmental
   gammas," but the measured RoI budget is **~99% neutrons + capture**, channels the paper does not
   contain. Updating it is a real rewrite, not a regeneration. **Do not run `gpd paper-build`** —
   the master `.tex` was hand-refactored (see memory).
2. **Landau–Vavilov validity floor = 4111.8 eV indicts 209 of the 584 bins the v1.0 manuscript
   already published** (35.8%). Nothing was tuned to avoid this. It is about the paper, not the
   milestone.
3. **Reactor-correlated neutrons are not modelled at all.** Deferred since Phase 7, never added. A
   bare-core estimate puts reactor neutron flux at 25 m near the *neutrino* flux (~3e12 cm⁻²s⁻¹);
   only the reactor's own bioshield (site-specific, not in this project) brings it down. Our neutron
   background is therefore a floor, and this is the single most consequential omission.
4. **VALD-12 is window-conditional and its backtracking trigger is live.** ROADMAP/REQUIREMENTS say
   the CONUS+ window is 0.4–1 keV_ee; `GPD/literature/SUMMARY.md` says 160 eV_ee. The ratio spans
   4.5 decades between them. 0.4–1 keV_ee was pre-registered and **failed by 3.28 decades**.
5. **S/B has external validation of its numerator only.** The 407.7 dru CaWO₄ closure has no
   reproducible artifact (GPD prose only), and with VALD-11 deleted there is no background-side
   target-swap validation at all.
6. Stale REQUIREMENTS text still describing the void VNS premise: CALC-11/18/19/20/23/25, VALD-12,
   plus a cited CONVENTIONS §D VNS lock that was never applied.
7. **SC4 of Phase 16 describes a quantity that cannot exist** ("the LEE amplitude at which
   S/B_particle = 1"); replacements shipped under their own names. Wording still needs disposition.

---

## 3. Things that will bite you if you don't know them

- **Confirmation pressure is a live failure mode here, and checking has paid every single time.**
  Five roadmap success criteria were superseded *by measurement*. Phase 11's moment check fired;
  Phase 12 refuted SC2 (44% off, not "a few percent"); Phase 13 found SC4's mechanism cancels
  analytically; Phase 15 found the obvious "too small to resolve" argument would have been false;
  Phase 14 caught its own 4.86× bug by cross-check. **Plan a genuine disconfirming check in every
  phase, and prefer ones that are not algebraic identities of what they purport to corroborate** —
  Phase 11 found three such identities in the roadmap and Phase 12 a fourth.
- **Cross-axis errors are the recurring bug class.** Deposit energy ≠ reconstructed energy; the
  slope is ~0.497, measured, not assumed. Phase 13 caught itself doing this; Phase 14 wrote a
  forbidden proxy against it; I reintroduced it once in the figure (hand-picked ×0.5) and had to
  fix it. Always map through the response matrix's own median.
- **Use `/opt/anaconda3/bin/python3`** (numpy 1.26.4, scipy 1.17.1, pytest 7.4.0, NCrystal 4.4.6).
  scipy is **absent** from the gpd venv.
- **Evidence discipline:** every quoted number must be reproducible from a locally frozen artifact
  via a recorded command. WebFetch produced two *verified* factual errors during Phase 8 and is not
  a quote source.
- Running the suite rewrites `data/flux/*.csv` provenance headers — pre-existing churn, revert
  before committing.
- Interpolators **raise** outside their domains by design; new tracked `.csv`/`.npz` need a
  disposition row in `artifacts/v2.0/legacy_grid_disposition.csv` or the closure guard fails.
- `shared_energy_grid` default is still `v1.0`; the 744-bin extended axis is opt-in
  (`version="v2.0-ext"`). Its docstring wrongly calls v2.0-ext the default — check
  `DEFAULT_GRID_VERSION`.

---

## 4. Physics worth carrying forward

- **The ~2.7 eV step in the neutron reconstructed spectrum is real**: it is the kinematic edge of the
  ⁷³Ge elastic resonance (669 b at E_n = 102.59 eV). Max recoil T = 0.0536 × 102.59 = 5.50 eV,
  → ×0.497 ≈ 2.7 eV reconstructed. Above it the resonance is kinematically forbidden, so the rate
  steps down. **But Phase 13 measured that this imprint washes out on the reconstructed axis**
  (statistic 3.4 vs its own threshold of 5) — do not quote it as a usable discriminant in E_rec.
- **⁷¹Ge electron capture is a neutron background**, one decay removed: ⁷⁰Ge(n,γ)⁷¹Ge → EC. Its
  saturation activity *equals* the ⁷⁰Ge(n,γ) rate (1054.15/kg/day, exactly). All three
  neutron-driven channels share one incident fluence, so they share one suppression factor.
- **Ge is the *better* neutron target per kg than CaWO₄** by ~1.45× (Phase 13, superseding SC4) —
  the kinematic factor cancels analytically; the Ge/W ratio is entirely atoms/kg.
- The 100 meV bin is the least reliable number in the milestone (48.98% kernel leakage below the
  grid floor, skewness 0.590). Report leakage; never renormalize.

---

## 5. Suggested next actions

1. Decide the CONUS+ analysis window (item 4) — it sets VALD-12's verdict.
2. Decide the paper strategy (item 1): full revision, minimal correction, or a standalone gap memo.
   The neutron omission is too large to leave standing in a paper about a band neutrons dominate.
3. If S/B realism matters, add a phase for **reactor-correlated neutrons** (item 3) and/or compute
   the passive-shield attenuation ourselves by re-folding an attenuated incident flux through Ge,
   rather than inheriting CaWO₄ event-rate factors.
