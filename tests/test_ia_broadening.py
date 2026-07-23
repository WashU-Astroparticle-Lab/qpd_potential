# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 11-02 (CALC-15): the impulse-approximation quantum broadening width.

The oracle here is ``test_debye_mean_ratio_oracle``: it validates the moment
diagnostics against an analytic spectrum before they are applied to Ge.
"""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import ia_broadening as ia
from qpd_potential import params as p
from qpd_potential import phonon_scale as ps

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TABLE = os.path.join(_ROOT, "artifacts", "v2.0", "ia_broadening_widths.csv")
_FIGURE = os.path.join(_ROOT, "artifacts", "v2.0", "ia_width_vs_counting_floor.png")
_DERIV = os.path.join(
    _ROOT, "GPD", "phases",
    "11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv",
    "11-02-IA-WIDTH-DERIVATION.md")

ROADMAP_ENERGIES = (0.1, 0.5, 1.0, 10.0, 100.0)
SC3_BANDS = {0.1: (0.35, 0.46), 0.5: (0.155, 0.205), 1.0: (0.11, 0.15), 100.0: (0.011, 0.015)}


# --------------------------------------------------------------------------- #
# claim-sigma-derivation                                                       #
# --------------------------------------------------------------------------- #
def test_sigma_derivation():
    """test-sigma-derivation. Build sigma_E the LONG way -- from q = sqrt(2 m_N E_R)
    and sigma_p = sqrt(m_N omega_bar/2) -- and demand the closed form sqrt(E_R
    omega_bar) back.  m_N must cancel identically.  Also verify the mean of the IA
    energy transfer is exactly E_R."""
    for E in ROADMAP_ENERGIES:
        assert ia.sigma_E_from_momentum_distribution(E) == pytest.approx(
            ia.sigma_E_eV(E), rel=1e-15)
        assert ia.mean_energy_transfer_eV(E) == pytest.approx(E, rel=1e-15)
    # m_N cancellation, explicitly
    m0 = ps.ge_nuclear_mass_eV()
    for m in (m0, 0.25 * m0, 7.0 * m0):
        assert ia.sigma_E_from_momentum_distribution(0.5, m_N_eV=m) == pytest.approx(
            ia.sigma_E_eV(0.5), rel=1e-14)


def test_sigma_dimensions():
    """test-sigma-dimensions. sigma_E scales as sqrt(E_R) and as sqrt(omega_bar)
    under deliberate factor-2 perturbations; the fractional width is dimensionless."""
    a = ia.sigma_E_eV(1.0)
    assert ia.sigma_E_eV(4.0) == pytest.approx(2.0 * a, rel=1e-14)
    assert ia.sigma_E_eV(1.0, 4.0 * p.OMEGA_BAR_eV.value) == pytest.approx(2.0 * a, rel=1e-14)
    # sigma_E at 1 eV IS sqrt(omega_bar) in eV, so it must be at the 0.1 eV scale
    assert 0.10 < a < 0.20
    assert ia.fractional_width(1.0) == pytest.approx(a / 1.0, rel=1e-14)
    # sigma_p is a momentum: sigma_p^2 = m_N omega_bar/2
    m = ps.ge_nuclear_mass_eV()
    sigma_p = math.sqrt(m * p.OMEGA_BAR_eV.value / 2.0)
    assert ia.sigma_E_eV(0.5) == pytest.approx(
        math.sqrt(2 * m * 0.5) * sigma_p / m, rel=1e-14)


def test_identity_flag():
    """test-identity-flag. sigma_E/E_R = 1/sqrt(2W) holds to machine precision AND is
    labelled an identity in the derivation artifact.

    It is TRUE BY CONSTRUCTION for ANY omega_bar, because 2W is DEFINED as
    E_R/omega_bar.  The test proves that by checking it for a deliberately wrong
    omega_bar: if the relation were evidence about germanium, it would fail there.
    """
    for E in ROADMAP_ENERGIES:
        tw = ps.two_W_from_omega_bar(E, p.OMEGA_BAR_eV.value)
        assert ia.fractional_width(E) * math.sqrt(tw) == pytest.approx(1.0, rel=1e-14)
    for bogus in (1e-4, 0.5, 12.0):          # nonsense omega_bar values, in eV
        for E in (0.1, 3.0):
            tw = ps.two_W_from_omega_bar(E, bogus)
            assert ia.fractional_width(E, bogus) * math.sqrt(tw) == pytest.approx(1.0, rel=1e-14)

    text = open(_DERIV).read().lower()
    assert "identity" in text
    assert "true by construction" in text
    assert "fp-identity-as-evidence" in text


# --------------------------------------------------------------------------- #
# claim-mean-systematic                                                        #
# --------------------------------------------------------------------------- #
def test_debye_mean_ratio_oracle():
    """test-debye-mean-ratio-oracle. On the ANALYTIC Debye VDOS the moment
    diagnostics must return omega_bar_p = 3 w_D/4 and omega_bar_u = 2 w_D/3, ratio
    exactly 9/8.  This validates the diagnostic BEFORE it touches the Ge spectrum."""
    d = ia.debye_vdos_means()
    w_D = d["omega_D_eV"]
    assert d["omega_bar_p_eV"] == pytest.approx(0.75 * w_D, rel=1e-6)
    assert d["omega_bar_u_eV"] == pytest.approx(2.0 * w_D / 3.0, rel=1e-6)
    assert abs(d["ratio"] - 9.0 / 8.0) < 1e-3
    assert abs(d["ratio"] - 9.0 / 8.0) < 1e-9        # far better than required
    assert d["sigma_correction"] == pytest.approx(math.sqrt(9.0 / 8.0), rel=1e-9)


def test_mean_ratio_on_ge():
    """test-mean-ratio. omega_bar_u must equal the LOCKED omega_bar (they are the same
    quantity -- a mismatch means one of the two quadratures is wrong), Cauchy-Schwarz
    requires omega_bar_p >= omega_bar_u, and the correction is ONE-SIDED."""
    g = ia.vdos_means()
    assert g["omega_bar_u_eV"] == pytest.approx(p.OMEGA_BAR_eV.value, rel=1e-9)
    assert g["omega_bar_p_eV"] >= g["omega_bar_u_eV"]
    assert g["omega_bar_p_eV"] == pytest.approx(p.OMEGA_BAR_ARITHMETIC_eV.value, rel=1e-6)
    assert g["ratio"] == pytest.approx(1.354758, abs=1e-5)
    assert g["sigma_correction"] == pytest.approx(1.163941, abs=1e-5)
    # DISCONFIRMING CHECK, and it fired: real Ge is materially WORSE than Debye.
    assert g["ratio"] > 9.0 / 8.0
    # one-sided: the corrected width is never smaller than the headline
    for E in ROADMAP_ENERGIES:
        assert ia.sigma_E_upper_moment_eV(E) > ia.sigma_E_eV(E)


# --------------------------------------------------------------------------- #
# claim-width-table                                                            #
# --------------------------------------------------------------------------- #
def _table():
    rows = []
    with open(_TABLE) as fh:
        hdr = None
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if hdr is None:
                hdr = s.split(",")
                continue
            rows.append(dict(zip(hdr, [float(x) for x in s.split(",")])))
    return rows


def test_width_bands():
    """test-width-bands. Every ROADMAP SC3 energy gets an EXPLICIT verdict.

    The bands were generated from the survey's omega_bar = 12-21 meV. The locked
    omega_bar = 17.860 meV sits inside that band, so agreement here is EXPECTED and is
    weak evidence -- agreement by shared ancestry, not independent confirmation.
    """
    verdicts = {}
    for E, band in SC3_BANDS.items():
        f = float(ia.fractional_width(E))
        verdicts[E] = band[0] <= f <= band[1]
    assert verdicts == {0.1: True, 0.5: True, 1.0: True, 100.0: True}
    # the actual values, re-derived here and NOT transcribed from GPD/literature/
    assert ia.fractional_width(0.1) == pytest.approx(0.42261, abs=1e-5)
    assert ia.fractional_width(0.5) == pytest.approx(0.18900, abs=1e-5)
    assert ia.fractional_width(1.0) == pytest.approx(0.13364, abs=1e-5)
    assert ia.fractional_width(10.0) == pytest.approx(0.042261, abs=1e-6)
    assert ia.fractional_width(100.0) == pytest.approx(0.013364, abs=1e-6)


def test_moment_corrected_widths_leave_the_sc3_bands():
    """The finding that cuts against the comfortable answer.

    With the physically correct ARITHMETIC mean governing <p_x^2>, the width exceeds
    the UPPER edge of every ROADMAP SC3 band. The bands are therefore not a ceiling
    the phase confirmed; they are a floor the single-frequency approximation produced.
    """
    corr = ia.vdos_means()["sigma_correction"]
    for E, band in SC3_BANDS.items():
        assert float(ia.fractional_width(E)) * corr > band[1], (
            f"moment-corrected width at {E} eV unexpectedly inside the band")


def test_sub_bin_crossing():
    """test-sub-bin-crossing. Solve sigma_E/E_R = one extended-grid bin (2.9205%)."""
    assert ia.ONE_BIN_FRACTIONAL_WIDTH == pytest.approx(0.0292047, abs=1e-6)
    xc = ia.sub_bin_crossing_energy_eV()
    assert 10.0 < xc < 100.0, "the crossing must fall between 10 and 100 eV"
    assert xc == pytest.approx(20.9396, abs=1e-3)
    assert ia.fractional_width(xc) == pytest.approx(ia.ONE_BIN_FRACTIONAL_WIDTH, rel=1e-12)


def test_table_exists_and_is_self_consistent():
    rows = _table()
    assert len(rows) > 700
    assert os.path.exists(_FIGURE) and os.path.getsize(_FIGURE) > 20_000
    corr = ia.vdos_means()["sigma_correction"]
    for r in rows[::37]:
        E = r["E_R_eV"]
        assert r["sigma_E_eV"] == pytest.approx(math.sqrt(E * p.OMEGA_BAR_eV.value), rel=1e-9)
        assert r["frac_width"] == pytest.approx(r["sigma_E_eV"] / E, rel=1e-9)
        assert r["two_W"] == pytest.approx(E / p.OMEGA_BAR_eV.value, rel=1e-9)
        assert r["frac_width_upper_moment"] == pytest.approx(r["frac_width"] * corr, rel=1e-9)
        assert r["quadrature_TaAl"] == pytest.approx(
            math.hypot(r["frac_width"], ia.COUNTING_FLOOR_05eV["Ta->Al"]), rel=1e-9)
    assert sum(int(r["is_roadmap_energy"]) for r in rows) == 5


# --------------------------------------------------------------------------- #
# claim-quadrature                                                             #
# --------------------------------------------------------------------------- #
def test_quadrature():
    """test-quadrature. Combined smearing at the 0.5 eV trigger threshold, per design,
    against the ROADMAP band 22-26%.  QUADRATURE, never a linear sum."""
    f = float(ia.fractional_width(0.5))
    q = {d: ia.quadrature_with_counting_floor(f, d) for d in ("Ta->Al", "Al->Hf")}
    assert q["Ta->Al"] == pytest.approx(0.247686, abs=1e-5)
    assert q["Al->Hf"] == pytest.approx(0.236824, abs=1e-5)
    for d, v in q.items():
        assert 0.22 <= v <= 0.26, f"{d} quadrature {v} outside the ROADMAP 22-26% band"
        # never a linear sum
        assert v < f + ia.COUNTING_FLOOR_05eV[d]
    # the same conclusion using the ROADMAP comparison floors rather than the
    # pipeline-derived ones -- so the verdict does not hinge on which is used
    qr = {d: ia.quadrature_with_counting_floor(f, d, ia.COUNTING_FLOOR_05eV_ROADMAP)
          for d in ("Ta->Al", "Al->Hf")}
    for v in qr.values():
        assert 0.22 <= v <= 0.26


def test_counting_floor_is_labelled_best_case_everywhere_it_is_used():
    """fp-poisson-as-resolution. The best-case caveat must travel with the floor."""
    assert "BEST CASE WITH NO NOISE SOURCES" in ia.COUNTING_FLOOR_CAVEAT
    assert "fp-poisson-as-resolution" in ia.COUNTING_FLOOR_CAVEAT
    assert ia.COUNTING_FLOOR_CAVEAT in ia.quadrature_with_counting_floor.__doc__
    header = "".join(ln for ln in open(_TABLE) if ln.startswith("#"))
    assert "BEST CASE WITH NO NOISE SOURCES" in header
    text = open(_DERIV).read()
    assert text.count("best case") + text.count("BEST CASE") >= 4
    assert "fp-poisson-as-resolution" in text
    # never a linear sum, stated
    assert "quadrature" in text.lower() and "never" in text.lower()


def test_no_electron_recoil_leak():
    """fp-electron-recoil-leak. This plan must neither apply the NUCLEAR-recoil width
    to the muon/Compton channels nor rule it out for them."""
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "ia_broadening.py")).read()
    for forbidden in ("muon_deposit", "compton_deposit", "compton_source"):
        assert forbidden not in src, f"ia_broadening imports/touches {forbidden}"
    assert "Phase 15" in src and "OPEN" in src
    text = open(_DERIV).read()
    assert "Phase 15" in text
