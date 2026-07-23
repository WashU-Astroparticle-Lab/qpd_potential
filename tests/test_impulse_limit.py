# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 11-03 (ROADMAP SC5): the bounded impulse-limit justification.

The three EXACT checks gate everything else: the zeroth moment, the f-sum rule, and
the gamma(0) = 2W reduction back onto the CONVENTIONS.md Section J lock.  They catch
implementation bugs without needing any physics judgement.
"""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import ia_broadening as ia
from qpd_potential import impulse_limit as il
from qpd_potential import params as p
from qpd_potential import phonon_scale as ps

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(
    _ROOT, "GPD", "phases",
    "11-phonon-scale-conventions-and-ia-quantum-broadening-p-conv",
    "11-03-IMPULSE-LIMIT-JUSTIFICATION.md")
_M_N = ps.ge_nuclear_mass_eV()
E5 = il.BOUNDED_RECOIL_ENERGIES_eV


# --------------------------------------------------------------------------- #
# claim-sum-rules -- the three exact checks                                    #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("E_R", E5)
def test_zeroth_moment(E_R):
    """test-zeroth-moment. int S dw = 1 (elastic delta included) to < 1e-6."""
    m = il.converged_numeric_moments(E_R)
    assert abs(m["zeroth_moment"] - 1.0) < 1e-6, (
        f"E_R = {E_R} eV: zeroth moment {m['zeroth_moment']!r} -- FFT normalization or "
        "w-grid range is wrong")
    assert m["converged"]


@pytest.mark.parametrize("E_R", E5)
def test_f_sum_rule(E_R):
    """test-f-sum-rule. int w S dw = q^2/(2 m_N) = E_R, to < 1e-4 relative.

    EXACT for any interaction, so a failure here is an implementation bug, not a
    tolerance question.  Note the elastic line sits at w = 0 and contributes exactly
    nothing, so the INELASTIC CONTINUUM ALONE carries the whole first moment -- which
    is the quantitative core of the e^(-2W) prohibition.
    """
    m = il.converged_numeric_moments(E_R)
    assert abs(m["first_moment_eV"] / E_R - 1.0) < 1e-4
    # q^2/(2 m_N) really is E_R, in the units actually used
    qk, q_invA = ps.momentum_transfer(E_R, _M_N)
    q_eV = q_invA * ps.HBAR_C_eV_ANGSTROM
    assert q_eV ** 2 / (2.0 * _M_N) == pytest.approx(E_R, rel=1e-14)


@pytest.mark.parametrize("E_R", E5)
def test_2W_reduction(E_R):
    """test-2W-reduction. gamma(0) at T->0 must reproduce 2W = q^2<u_x^2> from
    CONVENTIONS.md Section J.  Two independent quadratures over the same VDOS; a
    mismatch means one of them is wrong."""
    a = il.two_W(E_R)
    b = float(ps.two_W(E_R, p.U_X_SQ_ANGSTROM2.value, _M_N))
    assert a == pytest.approx(b, rel=1e-9)
    assert a == pytest.approx(E_R / p.OMEGA_BAR_eV.value, rel=1e-9)


def test_delta_convergence():
    """test-delta-convergence. S must narrow onto delta(w - E_R) as E_R rises.

    The width is quoted from the EXACT variance E_R * <w> (arithmetic mean), not from
    the locked-omega_bar Gaussian, because that is the true width of the harmonic S.
    """
    fr = [il.analytic_moments(E)["sigma_eV"] / E for E in E5]
    assert all(fr[i] > fr[i + 1] for i in range(len(fr) - 1)), "width must fall monotonically"
    # exact 1/sqrt(E_R) scaling: a decade in E_R is a factor sqrt(10) in width
    for i in range(len(E5) - 1):
        assert fr[i] / fr[i + 1] == pytest.approx(math.sqrt(E5[i + 1] / E5[i]), rel=1e-12)
    # the honest verdict: the bottom bin is NOT a delta
    assert fr[0] == pytest.approx(0.491890, abs=1e-5)     # 49.2 % at 100 meV
    assert fr[-1] == pytest.approx(0.0155549, abs=1e-6)   # 1.56 % at 100 eV
    assert fr[0] > 0.40, "if the bottom-bin width were small the IA claim would be strong"


# --------------------------------------------------------------------------- #
# claim-residual-correction                                                    #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("E_R", E5)
def test_second_moment(E_R):
    """test-second-moment -- THE DECISIVE CROSS-CHECK ON PLAN 11-02.

    The exact second central moment of the harmonic S is E_R * omega_bar_p, the VDOS
    ARITHMETIC mean, NOT the locked harmonic-mean omega_bar.  Reached here from the
    correlation function; plan 11-02 reached the same conclusion from the momentum
    distribution.  Had this matched E_R * omega_bar_u instead, plan 11-02's systematic
    would be wrong and plan 11-04 would be blocked.
    """
    w_p = ia.vdos_means()["omega_bar_p_eV"]
    w_u = ia.vdos_means()["omega_bar_u_eV"]
    num = il.converged_numeric_moments(E_R)["second_central_eV2"]
    assert num == pytest.approx(E_R * w_p, rel=1e-3)
    assert il.analytic_moments(E_R)["variance_eV2"] == pytest.approx(E_R * w_p, rel=1e-12)
    # and it is emphatically NOT the harmonic mean -- 35 % away
    assert not (abs(num / (E_R * w_u) - 1.0) < 0.05)


@pytest.mark.parametrize("E_R", E5)
def test_skewness(E_R):
    """test-skewness. The quantified O(1/2W) departure from the symmetric Gaussian.

    Exactly proportional to 1/sqrt(2W): skew = <w^2>/(<w>^{3/2} sqrt(omega_bar_u)) x
    1/sqrt(2W), a CONSTANT 1.3972 times 1/sqrt(2W) at every energy.
    """
    an = il.analytic_moments(E_R)
    tw = il.two_W(E_R)
    assert an["skewness"] > 0, "the harmonic S is skewed toward HIGH energy transfer"
    assert an["skewness"] * math.sqrt(tw) == pytest.approx(1.39718, abs=1e-4)
    assert 1.0 < an["skewness"] * math.sqrt(tw) < 3.0, "skew must scale as 1/sqrt(2W)"
    num = il.converged_numeric_moments(E_R)["skewness"]
    assert num == pytest.approx(an["skewness"], rel=2e-3)


def test_bottom_bin_residual_is_large():
    """The number that must travel as the O(1/2W) caveat on every 100 meV result."""
    an = il.analytic_moments(0.1)
    assert an["skewness"] == pytest.approx(0.590461, abs=1e-5)
    assert an["excess_kurtosis"] == pytest.approx(0.381132, abs=1e-5)
    assert 1.0 / il.two_W(0.1) == pytest.approx(0.178597, abs=1e-5)
    # a skewness of 0.59 is NOT a small perturbation on a Gaussian (skew = 0)
    assert an["skewness"] > 0.5


def test_negative_energy_weight():
    """test-negative-energy-weight. The matched symmetric Gaussian puts weight where
    the true T->0 S cannot go (w < 0: no phonons to absorb), and puts a large fraction
    below the extended-grid floor -- the leakage plan 11-04 must account for."""
    g = il.gaussian_offgrid_weights(0.1)
    assert g["weight_below_zero"] == pytest.approx(0.0089843, abs=1e-6)      # 0.90 %
    assert g["weight_below_floor"] == pytest.approx(0.499386, abs=1e-5)      # 49.9 %
    assert g["n_sigma_to_zero"] == pytest.approx(2.36626, abs=1e-4)

    c = il.gaussian_offgrid_weights(il.EXT_GRID_FIRST_CENTRE_eV)
    assert c["weight_below_zero"] == pytest.approx(0.0085959, abs=1e-6)      # 0.86 %
    assert c["weight_below_floor"] == pytest.approx(0.486420, abs=1e-5)      # 48.6 %

    # with the TRUE (arithmetic-mean) width the unphysical tail more than doubles
    t = il.gaussian_offgrid_weights(0.1, il.analytic_moments(0.1)["sigma_eV"])
    assert t["weight_below_zero"] == pytest.approx(0.0210268, abs=1e-6)      # 2.10 %
    assert t["weight_below_zero"] > 2 * g["weight_below_zero"]

    # count conservation on the retained grid therefore CANNOT be automatic
    assert g["weight_below_floor"] > 0.4, (
        "a clean sub-1e-3 residual for plan 11-04 would be evidence of hidden "
        "renormalization, not of a correct convolution")


# --------------------------------------------------------------------------- #
# claim-no-dw-suppression                                                      #
# --------------------------------------------------------------------------- #
def test_elastic_weight():
    """test-elastic-weight. e^(-2W) computed from the frozen VDOS, not transcribed."""
    vals = {E: il.elastic_weight(E) for E in E5}
    assert vals[0.1] == pytest.approx(3.7008e-3, rel=1e-3)
    # survey magnitude ~1e-2 at 100 meV: within a factor 2.7, i.e. within an order
    assert 0.1 < vals[0.1] / 1e-2 < 10.0
    # at 1 eV the survey said ~1e-20; we get 4.82e-25. This is a REAL, EXPLAINED
    # disagreement, not a bug: e^(-2W) is exponentially sensitive to omega_bar, and
    # the survey used the Debye value ~21.5 meV (2W = 46.5) rather than the locked
    # measured 17.86 meV (2W = 55.99). The test asserts the honest outcome.
    assert vals[1.0] == pytest.approx(4.8190e-25, rel=1e-3)
    assert vals[1.0] / 1e-20 < 0.1, "the 1 eV survey magnitude is NOT reproduced"
    assert math.exp(-1.0 / 21.5e-3) == pytest.approx(6.4e-21, rel=0.05), (
        "the survey number is recovered by the Debye omega_bar, which is the explanation")
    # monotone extinction of the coherent channel
    assert vals[0.1] > vals[0.5] > vals[1.0] > vals[10.0] >= vals[100.0]


@pytest.mark.parametrize("E_R", (0.1, 0.5, 1.0))
def test_strength_partition(E_R):
    """test-strength-partition. Elastic + inelastic = 1, and the INELASTIC continuum
    alone carries the entire f-sum rule (the elastic delta sits at w = 0)."""
    m = il.converged_numeric_moments(E_R)
    assert m["elastic_weight"] + m["inelastic_weight"] == pytest.approx(1.0, abs=2e-6)
    assert m["first_moment_eV"] == pytest.approx(E_R, rel=1e-4)
    # the numbers behind the prohibition
    e2w = il.elastic_weight(E_R)
    assert 1.0 - e2w > 0.99, (
        f"at E_R = {E_R} eV, multiplying the RATE by e^(-2W) would discard "
        f"{100*(1-e2w):.4f} % of the strength")


def test_nothing_here_multiplies_a_rate_by_exp_minus_2W():
    """fp-dw-rate-suppression, milestone-wide. Machine check that no module in this
    phase applies e^(-2W) as a multiplicative rate factor."""
    for mod in ("impulse_limit.py", "ia_broadening.py", "phonon_scale.py"):
        src = open(os.path.join(_ROOT, "src", "qpd_potential", mod)).read()
        for bad in ("* np.exp(-two_W", "*np.exp(-two_W", "* elastic_weight(",
                    "*elastic_weight(", "rate * np.exp(-", "dRdT * np.exp("):
            assert bad not in src, f"{mod} appears to apply exp(-2W) as a rate factor: {bad}"


def test_bounded_scope():
    """fp-scope-creep. ROADMAP SC5 caps this at five q values and one FFT each, and
    forbids a coherent backbone or a phonon-order expansion."""
    assert len(il.BOUNDED_RECOIL_ENERGIES_eV) == 5
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "impulse_limit.py")).read()
    calls = [ln for ln in src.splitlines()
             if "np.fft." in ln and not ln.strip().startswith("#")]
    assert len(calls) == 1, f"more than one FFT call: scope creep -- {calls}"
    for banned in ("bragg", "Bragg", "coherent_structure", "phonon_order"):
        assert banned not in src
    # no tracked artifact was added under artifacts/v2.0/ by this plan
    assert not os.path.exists(os.path.join(_ROOT, "artifacts", "v2.0", "impulse_limit_moments.csv"))


def test_artifact_is_honest():
    """fp-ia-overclaim, and the 'what this does not establish' requirement."""
    t = open(_ART).read()
    low = t.lower()
    assert "bounded" in low and "not a milestone pillar" in low
    assert "what this artifact does not establish" in low
    assert "necessary" in low and "sufficient" in low
    assert "fp-dw-rate-suppression" in t
    assert "fp-ia-overclaim" in t
    # the verdict must not upgrade beyond the numbers
    assert "order-of-magnitude" in low
    assert "49.19" in t and "0.5904" in t
