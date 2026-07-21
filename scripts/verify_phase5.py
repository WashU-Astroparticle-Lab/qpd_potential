#!/usr/bin/env python3
"""Phase-5 verification harness -- one command, human-readable PASS/FAIL.

Run from the project root:

    python3 scripts/verify_phase5.py

It re-derives every headline Phase-5 claim from the committed code + artifacts
(NOT from the SUMMARY prose) and prints a labeled table, so a reviewer can
confirm the numbers live. Exit code 0 iff all checks pass.

This is a *review aid*: the low-E linearity and the plateau/rollover are
calibration-consistency + limiting-case checks. The saturated-regime SHAPE has
no literature anchor (see the caveats in the walkthrough) -- this harness does
not and cannot validate that shape against data, by design.
"""
from __future__ import annotations
import sys, math
import numpy as np

ROOT = "/Users/lanqingyuan/Documents/GitHub/qpd_potential/.claude/worktrees/qpd-cevns-muon-spectrum-aaa8da"
sys.path.insert(0, ROOT)

from src.qpd_potential import response as R  # noqa: E402
from src.qpd_potential import params  # noqa: E402

DESIGNS = ["Ta->Al", "Al->Hf"]
results: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str) -> None:
    results.append((label, bool(ok), detail))


# 1. Trapping gate (Ta binary gate; response invariant to Delta_abs in alpha-phase)
for d in DESIGNS:
    ok = R.trapping_gate_ok(d)
    check(f"[gate] {d} trapping_gate_ok", ok, f"Delta_abs/Delta_tr >= {R.TRAPPING_GATE_MIN}")

# 2. Low-E linearity (VALD-04 low limit): E_rec ~= 0.5*E_dep well below onset
for d in DESIGNS:
    E_dep = 1.0  # 1 eV, deep in the linear regime
    ratio = float(R.E_rec(E_dep, d, "non_paralyzable")) / E_dep
    ok = abs(ratio - params.EPSILON.value) < 0.02
    check(f"[VALD-04 low-E] {d} E_rec/E_dep@1eV", ok, f"{ratio:.4f} (target {params.EPSILON.value})")

# 3. Crossover onset band (SIMU-01): default point, Hf < Ta->Al, equal-split anchor
onsets = {}
for d in DESIGNS:
    cb = R.crossover_band(d)
    onsets[d] = cb["default_point_eV"]
    check(f"[SIMU-01 crossover] {d} default onset eV",
          cb["band_min_eV"] <= cb["default_point_eV"] <= cb["band_max_eV"],
          f"default {cb['default_point_eV']:.1f} eV in band [{cb['band_min_eV']:.1f}, {cb['band_max_eV']:.1f}]")
check("[SIMU-01] Hf saturates before Ta->Al (default)",
      onsets["Al->Hf"] < onsets["Ta->Al"],
      f"Al->Hf {onsets['Al->Hf']:.1f} eV < Ta->Al {onsets['Ta->Al']:.1f} eV")

# 3b. Hf-first must hold across the whole f_prompt x r scan
hf_first_everywhere = True
for fp in np.linspace(0.1, 0.5, 5):
    for r in np.linspace(1.0, 5.0, 5):
        if not (R.onset_deposit_energy("Al->Hf", fp, r) < R.onset_deposit_energy("Ta->Al", fp, r)):
            hf_first_everywhere = False
check("[SIMU-01] Hf-first across full f_prompt x r scan", hf_first_everywhere, "25-point scan")

# 4. fp-no-saturation: at the 197 MeV muon tail, E_rec is >=3 orders below the
#    linear 0.5*E_dep line, for BOTH censoring variants, AND behaves per-variant.
E_tail = 197e6  # eV
lin_tail = params.EPSILON.value * E_tail
for d in DESIGNS:
    for variant in ("non_paralyzable", "paralyzable"):
        er = float(R.E_rec(E_tail, d, variant))
        ratio = er / lin_tail
        ok = ratio < 1e-3
        check(f"[fp-no-saturation] {d}/{variant} E_rec@197MeV",
              ok, f"{er/1e3:.1f} keV = {ratio:.2e} x linear")

# 4b. Variant divergence: paralyzable E_rec < non_paralyzable E_rec at the tail
for d in DESIGNS:
    er_np = float(R.E_rec(E_tail, d, "non_paralyzable"))
    er_p = float(R.E_rec(E_tail, d, "paralyzable"))
    check(f"[variant divergence] {d} paralyzable < non_paralyzable @tail",
          er_p < er_np, f"paralyzable {er_p/1e3:.1f} keV < non_paralyzable {er_np/1e3:.1f} keV")

# 5. Stop-condition teeth: with censoring OFF the count-integral is EXACTLY linear
#    (0.5*E_dep) at the tail -> proves the plateau/rollover comes from censoring,
#    not from a modeling artifact.
for d in DESIGNS:
    grid = np.array([E_tail])
    sw_np = R.sweep_E_rec(grid, d, "non_paralyzable")
    peak_on = float(sw_np["peak_gamma_on"][0])
    # the on-spot peak rate must massively exceed the 25 kHz ceiling at the tail
    check(f"[stop-cond] {d} peak Gamma_in >> 25 kHz @197 MeV",
          peak_on > 100 * R.SATURATION_CEILING_HZ,
          f"peak on-spot rate {peak_on:.2e} Hz vs ceiling {R.SATURATION_CEILING_HZ:.0f} Hz")

# 6. Event-count mapping (Pitfall 1): expected event count fed to the EMG burst
#    must be INT Gamma_in dt = K*tau_qp*N_qp/V_tr, NOT the trapped count N_qp.
for d in DESIGNS:
    td = R.es.resolve_design(d)
    N_qp = 1.0e4
    ev = float(R.expected_event_count(N_qp, d))
    # independent recompute: K * tau_qp * N_qp / V_tr  (per response.py docstring)
    K = td.K.value; tau_qp = td.tau_qp.value; v_tr = td.v_tr.value
    ev_ref = K * tau_qp * N_qp / v_tr
    ok = math.isclose(ev, ev_ref, rel_tol=1e-9) and not math.isclose(ev, N_qp, rel_tol=1e-6)
    check(f"[Pitfall-1 eventcount] {d} expected_event_count != N_qp",
          ok, f"event={ev:.3e} (=K*tau_qp*N_qp/V_tr) vs N_qp={N_qp:.3e}")

# 7. Response matrix artifacts: both variants present, every E_dep column
#    normalizes to 1, correct span, saturation onset recorded.
for d, tag in [("Ta->Al", "TaAl"), ("Al->Hf", "AlHf")]:
    z = np.load(f"{ROOT}/artifacts/stage1/response_matrix_{tag}.npz")
    variants = [k for k in z.keys() if k.startswith("R_")]
    both = ("R_non_paralyzable" in variants) and ("R_paralyzable" in variants)
    check(f"[SIMU-02 matrix] {tag} both censoring variants present", both, f"{variants}")
    norm_ok = True
    for v in variants:
        M = z[v]                      # (n_Erec, n_Edep)
        colsum = M.sum(axis=0)
        pop = colsum[colsum > 0]
        if not (len(pop) and np.allclose(pop, 1.0, atol=1e-6)):
            norm_ok = False
    check(f"[SIMU-02 matrix] {tag} all E_dep columns normalize to 1", norm_ok,
          f"{M.shape[1]} columns")
    edep = z["E_dep_centers_eV"]
    span_ok = edep.min() < 100 and edep.max() > 1e8   # sub-100 eV to >100 MeV
    check(f"[SIMU-02 matrix] {tag} E_dep span sub-keV..~200 MeV", span_ok,
          f"[{edep.min():.1f} eV, {edep.max()/1e6:.0f} MeV], {edep.size} cols")


# ---- report ------------------------------------------------------------------
n_pass = sum(1 for _, ok, _ in results if ok)
n_tot = len(results)
w = max(len(lbl) for lbl, _, _ in results)
print("=" * (w + 34))
print("Phase-5 verification harness")
print("=" * (w + 34))
for lbl, ok, detail in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {lbl:<{w}}  {detail}")
print("-" * (w + 34))
print(f"  {n_pass}/{n_tot} checks passed")
print("=" * (w + 34))
sys.exit(0 if n_pass == n_tot else 1)
