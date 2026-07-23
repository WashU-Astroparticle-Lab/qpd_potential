# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-13 Plan 13-02 acceptance tests.

ROADMAP SC4 (kinematic compression, adjudicated by measurement) and SC5 second
half (the >20 MeV omission bounded at the surface), plus the CALC-24 disposition.

EVERY tolerance is a module constant declared HERE, before any check runs.
"""
from __future__ import annotations

import os
import re

import numpy as np

from qpd_potential import neutron_recoil as nr

# --------------------------------------------------------------------------- #
# TOLERANCES -- declared before the checks run                                  #
# --------------------------------------------------------------------------- #
F_CANCELLATION_TOL = 1.0e-5      # the plan's pass condition on the f spread
PLAN_13_01_CONVERGENCE_TOL = 5.0e-3   # the quadrature tolerance it must beat
ATOMS_PER_KG_CROSSCHECK_TOL = 1.0e-3  # N_A x 1000/M vs the frozen-table N_Ge/rho
KINEMATIC_PART_TOL = 5.0e-3      # residual f dependence from the FINITE ceiling
LETHARGY_FLATNESS_RECORDED = 1.390    # 09-02 Section 5
LETHARGY_FLATNESS_TOL = 5.0e-3
ROADMAP_F_W = 0.0215             # the roadmap's own quoted kinematic factors,
ROADMAP_F_CA = 0.0952            # reproduced from 4A/(1+A)^2 with A the dominant
ROADMAP_F_O = 0.2215             # natural isotope's mass number
ROADMAP_F_TOL = 5.0e-5
RECORDED_ABOVE_197MEV_FRACTION = 0.21   # 09-02 Section 6.2
RECORDED_FRACTION_TOL = 0.02

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "13-ge-neutron-fold-from-the-sea-level-flux-p-tgt",
    "13-02-COMPRESSION-AND-OMISSIONS.md")

_T_PROBE = np.array([0.1, 1.0, 10.0, 31.6, 100.0, 1000.0])
_ROI_MASK = (_T_PROBE >= nr.ROI_LO_eV) & (_T_PROBE <= nr.ROI_HI_eV)


# --------------------------------------------------------------------------- #
# test-f-cancellation                                                           #
# --------------------------------------------------------------------------- #
def test_f_cancellation_across_four_kinematic_factors():
    """Analytically exact; numerically it must beat the 13-01 quadrature tolerance."""
    r = nr.f_cancellation_residual()
    assert set(r["f_values"]) == {0.0215, 0.0536, 0.0952, 0.2215}
    assert r["max_spread"] <= F_CANCELLATION_TOL, r["max_spread"]
    assert r["max_spread"] < PLAN_13_01_CONVERGENCE_TOL
    assert r["max_dev_from_closed_form"] <= F_CANCELLATION_TOL


def test_roadmap_kinematic_factors_are_reproduced_from_mass_numbers():
    """The ratio is the INPUT to SC4, so it must at least be derivable, not typed."""
    assert abs(nr.kinematic_factor(184) - ROADMAP_F_W) < ROADMAP_F_TOL
    assert abs(nr.kinematic_factor(40) - ROADMAP_F_CA) < ROADMAP_F_TOL
    assert abs(nr.kinematic_factor(16) - ROADMAP_F_O) < ROADMAP_F_TOL
    # and the "~2.5x" of the roadmap is the f ratio
    assert abs(nr.f_natural() / nr.kinematic_factor(184) - 2.49) < 0.02


def test_lethargy_flatness_reproduces_the_recorded_value():
    """Independent recomputation of 09-02 Section 5's factor 1.390."""
    lf = nr.lethargy_flatness()
    assert abs(lf["flatness_factor"] - LETHARGY_FLATNESS_RECORDED) \
        <= LETHARGY_FLATNESS_TOL, lf


# --------------------------------------------------------------------------- #
# test-target-ratio-measured                                                    #
# --------------------------------------------------------------------------- #
def test_each_material_uses_its_own_atoms_per_kg():
    """Reusing Ge's atoms/kg would manufacture the whole comparison."""
    seen = {}
    for name, t in nr.COMPARISON_TARGETS.items():
        n = t.total_atoms_per_kg()
        assert n > 0
        seen[name] = n
    assert len({round(v, 6) for v in seen.values()}) == len(seen)
    ge = nr.COMPARISON_TARGETS["Ge"]
    assert abs(ge.total_atoms_per_kg() / nr.n_ge_per_kg() - 1.0) \
        < ATOMS_PER_KG_CROSSCHECK_TOL
    # oxygen is the lightest and must therefore be the densest per kg
    assert seen["O"] == max(seen.values())
    assert seen["W"] == min(seen.values())


def test_pure_1overE_ratio_equals_the_atoms_per_kg_ratio():
    """The decisive mechanism check: with f cancelling, only atoms/kg is left."""
    c = nr.target_comparison(_T_PROBE)
    for name, v in c["targets"].items():
        n_ratio = v["atoms_per_kg_ratio_Ge_over_target"]
        dev = np.abs(v["ratio_pure_1overE"] / n_ratio - 1.0)
        assert dev.max() <= KINEMATIC_PART_TOL, (name, dev.max())


def test_target_ratio_is_attributed_and_the_parts_sum():
    """An unattributed ratio fails: SC4's whole content is the mechanism."""
    c = nr.target_comparison(_T_PROBE)
    for name, v in c["targets"].items():
        if name == "Ge":
            continue
        # residual after atoms/kg is accounted for, to second order, by the
        # flux-shape part plus the (tiny) finite-ceiling kinematic part
        lhs = 1.0 + v["residual_after_atoms_per_kg"]
        rhs = (1.0 + v["flux_shape_part"]) * (1.0 + v["kinematic_part"])
        assert np.max(np.abs(lhs / rhs - 1.0)) < 1.0e-6, name
        # the kinematic part is negligible everywhere and is the FINITE-CEILING
        # truncation, not the compression mechanism
        assert np.max(np.abs(v["kinematic_part"])) < KINEMATIC_PART_TOL, name


def test_comparison_legs_use_a_common_constant_sigma():
    """Otherwise 'Ge has more structure' would be true BY CONSTRUCTION."""
    assert nr.COMPARISON_SIGMA_B > 0
    c = nr.target_comparison(np.array([10.0, 100.0]))
    # the resonance-structure factor is reported SEPARATELY and is not 1
    assert np.all(c["ge_resonance_structure_factor"] > 2.0)
    # ...and it cancels from the Ge/Ge ratio, i.e. it entered no ratio
    assert np.allclose(c["targets"]["Ge"]["ratio_real_flux"], 1.0)


# --------------------------------------------------------------------------- #
# test-cawo4-not-w                                                              #
# --------------------------------------------------------------------------- #
def test_oxygen_dominates_the_cawo4_atom_count_and_carries_the_largest_f():
    cw = nr.COMPARISON_TARGETS["CaWO4"]
    fr = cw.atom_fractions()
    kf = cw.kinematic_factors()
    assert abs(fr[16] - 4.0 / 6.0) < 1e-12
    assert fr[16] > fr[184] and fr[16] > fr[40]
    assert kf[16] == max(kf.values())
    assert kf[16] / nr.f_natural() > 4.0     # oxygen's f is >4x germanium's
    # and CaWO4 is DENSER per kg than Ge, which is what flips the direction
    assert cw.total_atoms_per_kg() > nr.COMPARISON_TARGETS["Ge"].total_atoms_per_kg()


def test_the_cawo4_substitution_changes_the_direction():
    """A finding, not a footnote: Ge vs W and Ge vs CaWO4 point opposite ways."""
    c = nr.target_comparison(_T_PROBE)
    r_w = c["targets"]["W"]["ratio_real_flux"][_ROI_MASK]
    r_cw = c["targets"]["CaWO4"]["ratio_real_flux"][_ROI_MASK]
    assert np.all(r_w > 1.0), r_w      # Ge worse than W per kg
    assert np.all(r_cw < 1.0), r_cw    # Ge BETTER than CaWO4 per kg


# --------------------------------------------------------------------------- #
# test-sc4-verdict-recorded / test-void-rationale-not-reused                     #
# --------------------------------------------------------------------------- #
def test_sc4_verdict_is_recorded_in_the_phase12_vocabulary():
    assert os.path.exists(_REPORT), _REPORT
    text = open(_REPORT, encoding="utf-8").read()
    assert "SUPERSEDED BY MEASUREMENT" in text
    assert re.search(r"SC4\s+verdict", text, flags=re.IGNORECASE)
    # the verdict must not be the f ratio quoted back at itself
    assert "fp-assert-compression" in text
    assert "2.49" in text and "2.533" in text   # both, and distinguished


def test_void_rationale_is_never_used_as_a_justification():
    """EXECUTED grep, per the plan. The void rationale may appear only as a record."""
    marks = ("void", "VOID", "does not exist", "no shield", "NOT applied",
             "not applied", "removed and inverted", "never used", "forbidden",
             "fp-inherit-void-rationale", "is recorded", "guard")
    pattern = re.compile(r"shield attenuation|5-7x|5–7|overburden|"
                         r"building moderation|post-shield", re.IGNORECASE)
    # This test file is deliberately NOT scanned: the two lines that define the
    # search pattern would match themselves, which says nothing about whether the
    # rationale is used as a justification anywhere.
    paths = [_REPORT, nr.COMPRESSION_CSV, nr.OMISSION_CSV, nr.__file__]
    bad = []
    for p in paths:
        if not os.path.exists(p):
            continue
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            if pattern.search(line) and not any(m in line for m in marks):
                bad.append(f"{os.path.basename(p)}:{i}: {line.strip()[:120]}")
    assert bad == [], bad


# --------------------------------------------------------------------------- #
# test-sigma-slope-measured                                                     #
# --------------------------------------------------------------------------- #
def test_sigma_slope_at_the_ceiling_is_measured_before_the_continuation():
    s = nr.sigma_slope_at_ceiling()
    assert s["n_points"] > 100
    # the TREND approaching the ceiling is decreasing -- that is what licenses a
    # flat continuation as an estimate
    assert s["ols_slope_b_per_MeV"] < 0.0
    assert s["ols_slope_last_half_decade_b_per_MeV"] < 0.0
    assert s["sigma_hi_b"] < s["sigma_lo_b"]
    # ...but the band is NOT monotone, so the flat-at-ceiling value is NOT an
    # upper bound on its own, and the module must know that.
    assert not s["monotone_non_increasing"]
    assert not s["sigma_at_ceiling_is_band_max"]
    assert s["sigma_max_in_band_b"] > s["sigma_hi_b"]


def test_two_continuations_are_reported_and_the_upper_one_bounds():
    b = nr.high_energy_omission_bound()
    cs = b["continuations"]
    assert set(cs) == {"flat_at_ceiling", "flat_at_band_max"}
    assert cs["flat_at_band_max"]["sigma_b"] > cs["flat_at_ceiling"]["sigma_b"]
    for k in ("omission_fraction_in_roi", "omission_fraction_total"):
        assert cs["flat_at_band_max"][k] > cs["flat_at_ceiling"][k]


# --------------------------------------------------------------------------- #
# test-omission-split / test-omission-direction                                 #
# --------------------------------------------------------------------------- #
def test_in_roi_and_total_fractions_are_reported_separately():
    """fp-single-omission-number: one number would let the flattering one stand."""
    b = nr.high_energy_omission_bound()
    for label, v in b["continuations"].items():
        assert v["omission_fraction_in_roi"] > 0.0
        assert v["omission_fraction_total"] > 0.0
        # they must differ by orders of magnitude -- that IS the result
        assert v["omission_fraction_total"] / v["omission_fraction_in_roi"] > 1.0e3
    # and both are in the emitted artifact as separate columns
    head = open(nr.OMISSION_CSV, encoding="utf-8").read()
    assert "omission_fraction_in_roi" in head
    assert "omission_fraction_total" in head


def test_omission_direction_is_flatters_SB_and_nothing_is_netted():
    b = nr.high_energy_omission_bound()
    assert b["elastic_only"] is True
    assert b["elastic_only_direction"] == "flatters_SB"
    text = open(nr.OMISSION_CSV, encoding="utf-8").read()
    assert "flatters_SB" in text
    assert "fp-net-omissions" in text
    assert "penalizes_SB" in text     # named, in the "not netted against" sense


# --------------------------------------------------------------------------- #
# test-ceiling-subsumption                                                      #
# --------------------------------------------------------------------------- #
def test_the_two_declared_ceilings_are_resolved_against_each_other():
    s = nr.ceiling_subsumption()
    assert s["flux_table_top_edge_eV"] > s["sigma_el_ceiling_eV"]
    assert s["subsumed"] is True
    assert s["flux_ceiling_is_an_independent_omission_here"] is False
    assert abs(s["fraction_of_gt10MeV_above_flux_table_ceiling"]
               - RECORDED_ABOVE_197MEV_FRACTION) < RECORDED_FRACTION_TOL


# --------------------------------------------------------------------------- #
# test-calc24-conditional                                                       #
# --------------------------------------------------------------------------- #
def test_calc24_branch_is_taken_explicitly_against_the_measured_bound():
    d = nr.calc24_disposition()
    assert d["branch"] in ("deferral_sustained_on_the_measured_bound",
                           "escalate_to_user")
    assert d["inside_label"] == (d["worst_total_fraction"]
                                 <= d["label_as_fraction"])
    assert d["branch"] == ("deferral_sustained_on_the_measured_bound"
                           if d["inside_label"] else "escalate_to_user")
    # the replacement rationale must cite the measurement, not a shield
    assert "in-RoI" in d["replacement_rationale"]
    assert "total rate" in d["replacement_rationale"]
    assert d["multiplier_needed_to_break_it"] > 1.0


# --------------------------------------------------------------------------- #
# Artifacts                                                                     #
# --------------------------------------------------------------------------- #
def test_emitted_13_02_tables_exist_and_carry_the_label():
    for p in (nr.COMPRESSION_CSV, nr.OMISSION_CSV):
        assert os.path.exists(p), p
        text = open(p, encoding="utf-8").read()
        assert "accuracy_label = order_of_magnitude" in text
        assert "phi_lo NOT USED" in text
        assert text.rstrip().splitlines()[-1].endswith("order_of_magnitude")


def test_no_shielded_token_applied_in_the_13_02_artifacts():
    import sys
    sys.path.insert(0, os.path.join(_ROOT, "tests"))
    from test_env_v1_identity import is_not_applied, scan_paths  # noqa: E402

    hits = [h for h in scan_paths([nr.COMPRESSION_CSV, nr.OMISSION_CSV])
            if not is_not_applied(h[3])]
    assert hits == [], hits


def test_no_mass_scaled_nucleus_residual_anywhere():
    """fp-mass-scaled-target: retained as a standing prohibition.

    What the proxy forbids is SCALING a NUCLEUS CaWO4 or Al2O3 measured residual
    rate to germanium by a mass argument. Naming NUCLEUS as context -- "neutrons
    were ~91% of their shielded RoI budget" -- is not that, so the guard is
    written against the things that would actually constitute the proxy: reading
    one of their data files, or a rescale/residual quantity entering the channel.
    """
    banned = ("nucleus2019", "nucleus_", "data/external/nucleus", "table 5",
              "rescale", "residual rate", "mass-scal", "mass scal")
    for p in (nr.COMPRESSION_CSV, nr.OMISSION_CSV, nr.__file__):
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            low = line.lower()
            for b in banned:
                context_ok = any(c in low for c in (
                    "fp-mass-scaled-target", "no nucleus", "never", "leakage",
                    "renormaliz", "conserv", "not netted", "hidden rescale"))
                if b in low and not context_ok:
                    raise AssertionError(f"{p}:{i}: {b!r}: {line.strip()[:120]}")
    # ...and no NUCLEUS measured quantity is importable from this channel at all
    src = open(nr.__file__, encoding="utf-8").read()
    assert "veto_credit" not in src and "veto_envelope" not in src
    assert "nucleus2019_fig1_ge" not in src
