"""Machine-check params.py against the LOCKED CONVENTIONS.md Numerical Factor Registry.

Every convention-bearing constant must equal its registry value (CONVENTIONS.md
"Numerical Factor Registry" + Sections C/D/E/F). Trapping ratios must satisfy the
LOWER-bound margin Delta_abs/Delta_tr >= 2 (no upper bound imposed). Flagged
values must carry a non-HIGH confidence tag.
"""

import math

from qpd_potential import params as p


def test_cevns_registry_constants():
    # Section C: weak-interaction constants.
    assert p.SIN2_THETA_W.value == 0.2387
    assert p.ONE_MINUS_4SIN2THETAW.value == 0.0452
    # 1 - 4 sin^2 theta_W must be self-consistent with sin^2 theta_W.
    assert math.isclose(
        p.ONE_MINUS_4SIN2THETAW.value, 1 - 4 * p.SIN2_THETA_W.value, abs_tol=1e-9
    )
    # Section A.2: (hbar c)^2 conversion.
    assert p.HBARC2.value == 3.894e-28
    # Section C: prefactor is 4*pi, NOT 8*pi.
    assert math.isclose(p.CEVNS_PREFACTOR_DENOM.value, 4 * math.pi, rel_tol=1e-12)
    assert not math.isclose(p.CEVNS_PREFACTOR_DENOM.value, 8 * math.pi, rel_tol=1e-6)
    assert p.G_F.value == 1.1663787e-5


def test_detector_registry_constants():
    # Section D: detector normalization.
    assert p.GE_ATOMS_PER_KG.value == 8.29e24
    assert p.GE_DENSITY.value == 5.323
    assert p.GE_MOLAR_MASS.value == 72.63
    assert p.REACTOR_POWER.value == 3.0
    assert p.REACTOR_POWER.units == "GW_th"  # thermal, not electric


def test_efficiency_and_censoring_registry_constants():
    # Section E: efficiency baseline.
    assert p.EPSILON.value == 0.5
    # Section F: resolving time 40 us (NOT the 20 us sampling interval).
    assert p.TAU_D.value == 40e-6
    assert p.SAMPLING.value == 20e-6
    assert p.TAU_D.value != p.SAMPLING.value  # do not conflate the two
    # CONTEXT decision D: default censoring variant.
    assert p.DEFAULT_CENSORING == "non_paralyzable"
    assert p.DEFAULT_CENSORING in p.CENSORING_VARIANTS


def test_trapping_ratios_lower_bound_only():
    # Delta_abs/Delta_tr is a LOWER-bound trapping margin (>= ~2). The Al->Hf
    # 4.75 ratio is a valid LARGER margin, NOT a ceiling violation.
    r_ta_al = p.trapping_ratio("Ta->Al")
    r_al_hf = p.trapping_ratio("Al->Hf")
    assert math.isclose(r_ta_al, 3.58, abs_tol=0.02)
    assert math.isclose(r_al_hf, 4.75, abs_tol=0.02)
    assert r_ta_al >= 2.0
    assert r_al_hf >= 2.0  # lower bound only; no upper bound asserted


def test_flagged_values_are_not_high_confidence():
    # The three genuinely uncertain inputs must be tagged non-HIGH.
    assert p.DELTA_ABS_TA.confidence != "HIGH"
    assert p.F_PROMPT.confidence != "HIGH"
    assert p.R_SPOT.confidence != "HIGH"
    # ... and each must carry an explanatory note flag.
    assert p.DELTA_ABS_TA.note
    assert p.F_PROMPT.note
    assert p.R_SPOT.note


def test_table_ii_per_design_values():
    # Spot-check the verbatim Table II transcription (Ramanathan 2026, p. 14).
    d1 = p.DESIGN_TA_AL
    assert d1.delta_tr.value == 190e-6
    assert d1.v_tr.value == 100.0
    assert d1.K.value == 3e3
    assert d1.tau_qp.value == 1e-3
    assert d1.n_0.value == 0.3
    assert d1.T_opr.value == 0.1

    d2 = p.DESIGN_AL_HF
    assert d2.delta_tr.value == 40e-6
    assert d2.v_tr.value == 1000.0
    assert d2.K.value == 2e4
    assert d2.tau_qp.value == 400e-6  # caption/lit value, not the 1 ms table cell
    assert d2.n_0.value == 0.03
    assert d2.T_opr.value == 0.025


def test_no_quenching_symbols_in_params_source():
    # A fieldless phonon calorimeter has NO ionization-suppression scale split.
    import pathlib

    src = pathlib.Path(p.__file__).read_text().lower()
    for forbidden in ("kevee", "kevnr", "lindhard", "quench"):
        assert forbidden not in src, f"forbidden token {forbidden!r} present in params.py"
