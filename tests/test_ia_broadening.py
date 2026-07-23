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


# =========================================================================== #
# Plan 11-04 (TDD): applying the convolution to dR/dE_R before the response    #
# chain.  Every assertion below was written BEFORE the implementation existed. #
# =========================================================================== #
import subprocess

from qpd_potential import fold
from qpd_potential import impulse_limit as il
from qpd_potential import muon_deposit as md

_APPLY = os.path.join(
    _ROOT, "GPD", "phases",
    "11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv",
    "11-04-BROADENING-APPLICATION.md")
_BROADENED = os.path.join(_ROOT, "artifacts", "v2.0", "cevns_dRdT_broadened.csv")
_LEAKAGE = os.path.join(_ROOT, "artifacts", "v2.0", "ia_broadening_leakage_budget.csv")


def _demo_axis(n=240, lo=0.0999350, hi=3200.0):
    """A log recoil axis reaching the extended-grid floor."""
    return np.geomspace(lo, hi, n + 1)


def _demo_counts(edges):
    """A smooth falling test spectrum in COUNTS per bin (shape only)."""
    c = np.sqrt(edges[:-1] * edges[1:])
    return c ** -1.5 * np.diff(edges)


# --- 1. zero-width identity ------------------------------------------------ #
def test_sigma_zero_identity():
    """test-sigma-zero-identity. omega_bar -> 0 must be the IDENTITY, bit-for-bit.
    A convolution that is not the identity at zero width is wrong regardless of what
    else it reproduces."""
    e = _demo_axis()
    c = _demo_counts(e)
    out, leak = ia.broaden_counts(e, c, omega_bar_eV=0.0)
    assert np.array_equal(out, c)
    assert leak["below_floor"] == 0.0 and leak["below_zero"] == 0.0
    assert leak["above_top"] == 0.0


# --- 2. switch-off bit-identity -------------------------------------------- #
def test_switch_off_bit_identical():
    """test-switch-off-bit-identical. The fold with broadening OFF must reproduce the
    pre-existing v1.0 chain bit-for-bit -- the fail-safe property that lets Phase 12
    turn broadening on deliberately rather than inheriting it."""
    edges = md.shared_energy_grid("v1.0") * 1e3
    ref = fold.rebin_cevns_to_edep_grid(edges)
    off = fold.rebin_cevns_to_edep_grid(edges, broaden=False)
    for k in ("counts", "counts_band", "dRdEdep", "dRdEdep_band", "low_counts"):
        assert np.array_equal(ref[k], off[k]), f"{k} not bit-identical with the switch off"
    assert ia.BROADENING_DEFAULT is False, (
        "the recorded default must be OFF (fail-safe, Phase-10 precedent); "
        "changing it is a Phase-12 decision")


# --- 3. conservation with leakage ------------------------------------------ #
def test_conservation_with_leakage():
    """test-conservation-with-leakage. Retained + leaked must equal the input to
    <= 1e-3.  Conservation across the RETAINED grid alone will NOT hold in the bottom
    decade and is not what is being claimed."""
    e = _demo_axis()
    c = _demo_counts(e)
    out, leak = ia.broaden_counts(e, c, omega_bar_eV=p.OMEGA_BAR_eV.value)
    total_in = c.sum()
    total_out = out.sum() + leak["below_floor"] + leak["above_top"]
    assert abs(total_out / total_in - 1.0) <= 1e-3
    # and the retained-only sum must MISS, or something was renormalized
    assert out.sum() < total_in * (1.0 - 1e-6)
    # E < 0 mass is a subset of the below-floor mass
    assert 0.0 < leak["below_zero"] <= leak["below_floor"]


def test_bottom_decade_leakage_is_nonzero():
    """With sigma_E/E_R ~ 42 % at 100 meV a zero leakage entry means the kernel was
    clipped or the result renormalized."""
    e = _demo_axis()
    c = _demo_counts(e)
    out, leak = ia.broaden_counts(e, c, omega_bar_eV=p.OMEGA_BAR_eV.value)
    per_bin = leak["below_floor_per_bin"]
    bottom = np.sqrt(e[:-1] * e[1:]) < 1.0
    assert per_bin[bottom].sum() > 0.0
    assert per_bin[bottom].sum() / leak["below_floor"] > 0.99, (
        "essentially all sub-floor leakage must come from the bottom decade")


# --- 4. strict linearity (no renormalization) ------------------------------ #
def test_no_renormalization():
    """test-no-renormalization. Scaling the input by c scales EVERY output bin and
    EVERY leakage entry by exactly c.  Any global post-convolution rescale breaks
    this, because the rescale factor would depend on the total."""
    e = _demo_axis()
    c0 = _demo_counts(e)
    k = 7.3125
    a, la = ia.broaden_counts(e, c0, omega_bar_eV=p.OMEGA_BAR_eV.value)
    b, lb = ia.broaden_counts(e, k * c0, omega_bar_eV=p.OMEGA_BAR_eV.value)
    assert np.allclose(b, k * a, rtol=1e-13, atol=0.0)
    for key in ("below_floor", "below_zero", "above_top"):
        assert lb[key] == pytest.approx(k * la[key], rel=1e-13)
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "ia_broadening.py")).read()
    for bad in ("/= out.sum()", "/ out.sum()", "* (total_in / total_out)",
                "renormalize", "renormalise"):
        assert bad not in src, f"post-convolution rescale detected: {bad}"


# --- 5. leakage matches plan 11-03's independent analytic prediction -------- #
def test_leakage_matches_prediction():
    """test-leakage-matches-prediction. Different plan, different code path: the
    measured sub-floor and E<0 fractions for a kernel centred in the bottom bin must
    match plan 11-03's matched-Gaussian weights within 10 %."""
    e = _demo_axis()
    centre = np.sqrt(e[0] * e[1])
    c = np.zeros(e.size - 1)
    c[0] = 1.0                                   # a single unit source in the bottom bin
    out, leak = ia.broaden_counts(e, c, omega_bar_eV=p.OMEGA_BAR_eV.value)
    pred = il.gaussian_offgrid_weights(centre, floor_eV=e[0])
    assert leak["below_floor"] == pytest.approx(pred["weight_below_floor"], rel=0.10)
    assert leak["below_zero"] == pytest.approx(pred["weight_below_zero"], rel=0.10)
    assert leak["below_floor"] > 0.40, "roughly half a bottom-bin kernel falls off the axis"


# --- 6. ordering matters and is correct ------------------------------------ #
def test_order_of_operations():
    """test-order-of-operations. Broaden-then-rebin must DIFFER from rebin-then-
    broaden, so the ordering is a real physical constraint and not cosmetic; and the
    shipped path must be the former, upstream of rebin_cevns_to_edep_grid."""
    edges = md.shared_energy_grid("v1.0") * 1e3
    shipped = fold.rebin_cevns_to_edep_grid(edges, broaden=True)["counts"]
    plain = fold.rebin_cevns_to_edep_grid(edges, broaden=False)["counts"]
    after, _ = ia.broaden_counts(edges, plain, omega_bar_eV=p.OMEGA_BAR_eV.value)
    assert not np.allclose(shipped, after, rtol=1e-6), (
        "broaden-then-rebin and rebin-then-broaden must differ numerically")
    assert not np.array_equal(shipped, plain)
    # the shipped path is upstream: it broadens the native recoil spectrum
    fsrc = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    i_broaden = fsrc.index("broaden_native_spectrum")
    i_rebin = fsrc.index("counts = rebin_counts(T, y, E_dep_edges_eV)")
    assert i_broaden < i_rebin, "broadening must be applied before the rebin"
    for bad in ("R(E_rec", "response_matrix", "energy_scale"):
        assert bad not in fsrc[i_broaden:i_rebin]


# --- 7. no e^(-2W) factor -------------------------------------------------- #
def test_no_dw_factor():
    """test-no-dw-factor. Broadening must be amplitude-preserving up to the reported
    leakage.  A suppression of ~1e-2 at 100 meV or ~1e-20 at 1 eV would be the locked
    forbidden proxy firing."""
    edges = md.shared_energy_grid("v1.0") * 1e3
    on = fold.rebin_cevns_to_edep_grid(edges, broaden=True)["counts"]
    off = fold.rebin_cevns_to_edep_grid(edges, broaden=False)["counts"]
    hi = np.sqrt(edges[:-1] * edges[1:]) > 10.0
    assert on[hi].sum() / off[hi].sum() == pytest.approx(1.0, rel=1e-3)
    for mod in ("ia_broadening.py", "fold.py"):
        src = open(os.path.join(_ROOT, "src", "qpd_potential", mod)).read()
        for bad in ("np.exp(-two_W", "np.exp(-2 * W", "* elastic_weight("):
            assert bad not in src


# --- 8. domain guard intact ------------------------------------------------ #
def test_domain_guard():
    """test-domain-guard. Driving the kernel below a table floor must RAISE or hit an
    explicit documented edge rule.  A try/except returning zero fails this: it is the
    exact failure mode Phase 10 SC3 installed the guard against, and it would make
    leakage silently vanish too."""
    with pytest.raises(Exception):
        fold.read_cevns()  # sanity: the frozen table exists
        c = fold.read_cevns()
        # the frozen v1.0 CEvNS table carries NO data below 5 eV
        ia.broaden_native_spectrum(c["T_eV"], c["dRdT_total"], c["dRdT_band_1sigma"],
                                   omega_bar_eV=p.OMEGA_BAR_eV.value,
                                   floor_eV=0.0999350, require_floor_coverage=True)
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "ia_broadening.py")).read()
    assert "except" not in src or "return 0" not in src
    assert "np.clip" not in src, "no clamping anywhere in the broadening path"


# --- 9. v1.0 regression, with the right SHAPE ------------------------------ #
def test_v1_regression():
    """test-v1-regression. Above 10 eV the broadened spectrum must reproduce the
    frozen v1.0 result to < 1 % -- AND the deviation must FALL with energy.

    A bare < 1 % bound is not enough: a kernel that is uniformly too narrow would pass
    it.  The plan asked that the deviation fall as sqrt(omega_bar/E_R), i.e. with a
    log-log slope of -0.5.

    TWO things about that expectation, both verified here rather than assumed.

    (a) The correct leading order is STEEPER than -0.5, not equal to it.  For a
        mass-conserving kernel with sigma^2 = omega_bar * E, the second-moment
        (Fokker-Planck) expansion gives Delta f = (omega_bar/2) d^2/dE^2 [E f], so for
        a power-law spectrum Delta f / f goes as omega_bar/E -- slope -1.  Measured
        over the smooth region: -0.98.  sqrt(omega_bar/E_R) is the FRACTIONAL WIDTH,
        which is a different quantity from the fractional change in the SPECTRUM.

    (b) A single global power-law fit from 10 eV to the top of the axis is NOT the
        right statistic, and this is asserted rather than claimed: the deviation
        CHANGES SIGN near 300 eV and grows again toward the ~3.2 keV kinematic
        endpoint, where the spectrum cuts off and is not a power law at all.  Fitting
        across the sign change gives -0.31, which measures the sign change and not the
        broadening.  Both numbers are reported in 11-04-BROADENING-APPLICATION.md.
    """
    edges = md.shared_energy_grid("v1.0") * 1e3
    on = fold.rebin_cevns_to_edep_grid(edges, broaden=True)["counts"]
    off = fold.rebin_cevns_to_edep_grid(edges, broaden=False)["counts"]
    c = np.sqrt(edges[:-1] * edges[1:])
    m = (c > 10.0) & (off > 0) & (on > 0)
    E = c[m]
    signed = on[m] / off[m] - 1.0
    dev = np.abs(signed)

    # the bound, over the WHOLE range above 10 eV -- no domain restriction
    assert dev.max() < 0.01, f"max deviation above 10 eV is {dev.max():.4%}, target < 1 %"
    assert dev.max() == pytest.approx(5.1963e-4, rel=0.05)
    # non-vacuous: the kernel must actually have acted
    assert dev.max() > 1e-6, "a zero deviation would mean the kernel never acted"

    # (b) the sign change is REAL and is what breaks a global fit -- asserted, not
    # claimed.  The main crossing is at 233.9 eV: below it the deviation is negative
    # (95 % of bins; the handful of positive ones sit where |dev| ~ 1e-5 and are
    # binning noise), above 300 eV it is positive at EVERY bin without exception.
    assert np.median(signed[E < 200.0]) < 0
    assert np.mean(signed[E < 200.0] < 0) > 0.9
    assert np.all(signed[E > 300.0] > 0), (
        "the deviation must be positive everywhere above 300 eV; if it is not, the "
        "justification for excluding the endpoint region from the trend fit fails")

    # (a) the trend, on ONE side of the crossing and well below the kinematic endpoint
    s = (E >= 20.0) & (E <= 200.0)
    slope = np.polyfit(np.log(E[s]), np.log(dev[s]), 1)[0]
    assert slope < -0.5, (
        f"deviation falls as E^{slope:.3f} in the smooth region; a flat or shallow "
        "trend means a normalization error is masquerading as broadening")
    assert slope == pytest.approx(-0.94, abs=0.10), (
        "the measured slope must match the Fokker-Planck prediction of -1, not the "
        "plan's stated -0.5")

    # and the global fit is recorded as the contaminated statistic it is
    g = np.polyfit(np.log(E), np.log(dev), 1)[0]
    assert -0.45 < g < -0.15, f"global fit slope {g:.3f} unexpectedly changed"


def test_artifacts_and_disposition_rows_exist():
    assert os.path.exists(_BROADENED)
    assert os.path.exists(_LEAKAGE)
    reg = open(os.path.join(_ROOT, "artifacts", "v2.0",
                            "legacy_grid_disposition.csv")).read()
    assert "artifacts/v2.0/cevns_dRdT_broadened.csv" in reg
    assert "artifacts/v2.0/ia_broadening_leakage_budget.csv" in reg


def test_moment_reconciliation():
    """test-moment-reconciliation. Plans 11-02 and 11-03 must AGREE on which VDOS
    moment governs the width, or this plan is BLOCKED."""
    w_p = ia.vdos_means()["omega_bar_p_eV"]
    for E in (0.1, 1.0, 100.0):
        assert il.analytic_moments(E)["variance_eV2"] == pytest.approx(E * w_p, rel=1e-9)
        assert ia.sigma_E_upper_moment_eV(E) == pytest.approx(
            math.sqrt(il.analytic_moments(E)["variance_eV2"]), rel=1e-9)
    t = open(_APPLY).read()
    assert "RECONCILED" in t.upper()
    assert "1.1639" in t
    # the systematic is carried as a BAND, not absorbed
    head = "".join(ln for ln in open(_BROADENED) if ln.startswith("#"))
    assert "upper" in head.lower() and "one-sided" in head.lower()
