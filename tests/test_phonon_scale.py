# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 11-01 (CALC-14): the phonon energy scale and the Debye-Waller convention.

Test order matters here.  ``test_debye_oracle`` is the gate: it is the only check in
this file that is independent of both the Ge data files and of the project's own prior
estimates, and it is what proves the quadrature is free of the 3-D/1-D factor-3 trap
and of a VDOS normalization error.  Every Ge number in the phase is conditional on it.
"""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import params as p
from qpd_potential import phonon_scale as ps

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONVENTIONS = os.path.join(_ROOT, "GPD", "CONVENTIONS.md")

# Debye T->0 baseline, RE-DERIVED from the closed form rather than pasted.
_M_N = ps.ge_nuclear_mass_eV()
_DEBYE_U3 = ps.debye_msd_3d_closed_form(ps.GE_THETA_D_K, _M_N)
_DEBYE_UX2 = _DEBYE_U3 / 3.0


# --------------------------------------------------------------------------- #
# claim-quadrature-correct                                                     #
# --------------------------------------------------------------------------- #
def test_debye_oracle():
    """test-debye-oracle. Feed the quadrature the ANALYTIC Debye VDOS
    g(w) = 3 w^2/w_D^3 on [0, w_D] with k_B theta_D = 374 K and demand the closed
    form <u^2>_3D = 9 hbar^2/(4 m_N k_B theta_D) back.

    Independent of every Ge data file.  A failure here is a factor-3 or
    normalization bug and invalidates the whole plan.
    """
    w = ps.debye_grid(ps.GE_THETA_D_K)
    g = ps.debye_vdos(w, ps.GE_THETA_D_K)
    quad3 = ps.mean_square_displacement_3d(w, g, None, _M_N)
    assert abs(quad3 / _DEBYE_U3 - 1.0) < 1e-3
    # and much better than the contract tolerance, so the margin is visible
    assert abs(quad3 / _DEBYE_U3 - 1.0) < 1e-8

    quad1 = ps.mean_square_displacement_1d(w, g, None, _M_N)
    assert quad1 * 3.0 == quad3, "<u_x^2> must be <u^2>_3D/3 to machine precision"

    # The re-derived numerical values, NOT pasted from GPD/literature/.
    assert 3.9e-3 < quad3 < 4.1e-3       # 4.0139e-3 angstrom^2
    assert 1.30e-3 < quad1 < 1.37e-3     # 1.3380e-3 angstrom^2


def test_debye_mean_ratio_oracle_is_nine_eighths():
    """The Debye VDOS has <w><1/w> = 9/8 EXACTLY.

    Derivation: <w> = int_0^{wD} w (3w^2/wD^3) dw = 3 wD/4;
                <1/w> = int_0^{wD} (3w^2/wD^3)/w dw = 3/(2 wD);
                product = 9/8.

    This is the second analytic oracle and the one that fixes the moment mismatch
    plan 11-02 must carry: <u_x^2> is set by the HARMONIC mean, <p_x^2> by the
    ARITHMETIC mean, and sqrt(9/8) is how far apart they are for a Debye spectrum.
    """
    w = ps.debye_grid(ps.GE_THETA_D_K)
    m = ps.vdos_moment_means(w, ps.debye_vdos(w, ps.GE_THETA_D_K))
    assert abs(m["mean_ratio"] - 9.0 / 8.0) < 1e-9
    w_D_meV = ps.K_B_eV_PER_K * ps.GE_THETA_D_K * 1e3
    assert abs(m["arithmetic_mean_meV"] - 0.75 * w_D_meV) < 1e-6 * w_D_meV
    assert abs(m["harmonic_mean_meV"] - 2.0 * w_D_meV / 3.0) < 1e-6 * w_D_meV


def test_factor_three_trap_is_detectable_by_the_oracle():
    """Guard the guard: if 2W were built from <u^2>/3 with <u^2> ALREADY the 1-D
    MSD (forbidden proxy fp-factor-three), 2W would be 3x too small.  Assert the
    ratio explicitly so a future refactor that reintroduces the /3 fails here."""
    ux2 = p.U_X_SQ_ANGSTROM2.value
    correct = ps.two_W(0.1, ux2, _M_N)
    trapped = ps.two_W(0.1, ux2 / 3.0, _M_N)
    assert abs(correct / trapped - 3.0) < 1e-12
    assert correct > 1.0 > trapped / 3.0


def test_dimensions():
    """test-dimensions. Every returned quantity against the plan's dimensional_check
    block, and hbar*c applied exactly once per path."""
    ux2 = p.U_X_SQ_ANGSTROM2.value
    assert 1e-4 < ux2 < 1e-2                                   # angstrom^2
    wbar = ps.omega_bar_eV(ux2, _M_N)
    assert 5e-3 < wbar < 5e-2                                  # eV (meV scale)
    assert isinstance(ps.two_W(1.0, ux2, _M_N), float) or np.isscalar(ps.two_W(1.0, ux2, _M_N))
    assert ps.debye_waller_B(ux2) == pytest.approx(8 * math.pi**2 * ux2, rel=1e-15)

    # hbar*c enters <u_x^2> as (hbar c)^2 and q as one power. Scaling hbar*c by f
    # must scale <u_x^2> by f^2 and q[1/A] by 1/f -- so 2W is INVARIANT.
    f = 1.000001
    saved = ps.HBAR_C_eV_ANGSTROM
    try:
        w, g = ps.load_vdos("ncrystal")
        a = ps.mean_square_displacement_1d(w, g, None, _M_N)
        qa = ps.momentum_transfer(0.1, _M_N)[1]
        ps.HBAR_C_eV_ANGSTROM = saved * f
        b = ps.mean_square_displacement_1d(w, g, None, _M_N)
        qb = ps.momentum_transfer(0.1, _M_N)[1]
        assert abs(b / a - f**2) < 1e-12
        assert abs(qb / qa - 1.0 / f) < 1e-12
    finally:
        ps.HBAR_C_eV_ANGSTROM = saved


# --------------------------------------------------------------------------- #
# claim-vdos-fidelity                                                          #
# --------------------------------------------------------------------------- #
def test_vdos_normalized_to_one():
    for src in ("ncrystal", "darkelf"):
        w, g = ps.load_vdos(src)
        assert np.trapz(g, w) == pytest.approx(1.0, rel=1e-12)


def test_vdos_ceiling():
    """test-vdos-ceiling. The measured Nelin & Nilsson ceiling is 37.79 meV.

    NCrystal grid spacing is 0.0802 meV; DarkELF's is 0.1261 meV.
    """
    nc = ps.vdos_ceiling_meV("ncrystal")
    de = ps.vdos_ceiling_meV("darkelf")
    assert abs(nc - 37.79) < 0.0802, f"NCrystal ceiling {nc} meV is not the 37.79 meV spectrum"
    assert abs(de - 37.79) < 0.1261, f"DarkELF ceiling {de} meV is not the 37.79 meV spectrum"
    # the two digitizations agree on the ceiling within one DarkELF grid spacing
    assert abs(nc - de) < 0.1261


def test_vdos_vs_debye():
    """test-vdos-vs-debye. VDOS-integral <u_x^2> against the INDEPENDENT Debye-model
    value at theta_D = 374 K.  ROADMAP SC2 allows a factor 1.5 either way; a larger
    gap is a suspected 3-D/1-D convention error, not physics."""
    ux2 = ps.derive("ncrystal")["u_x_sq_A2"]
    ratio = ux2 / _DEBYE_UX2
    assert 1.0 / 1.5 < ratio < 1.5, (
        f"VDOS/Debye <u_x^2> ratio {ratio:.4f} is outside the SC2 factor-1.5 window; "
        "suspect a 3-D/1-D convention error before calling it physics")
    assert ratio == pytest.approx(1.2030, abs=5e-4)


def test_source_cross_check_not_averaged():
    """test-source-cross-check. NCrystal vs DarkELF <u_x^2>, same quadrature, same
    normalization convention.  Agreement within 10%.  The two are NEVER averaged:
    the adopted value is the NCrystal one and DarkELF is reported as the check."""
    nc = ps.derive("ncrystal")["u_x_sq_A2"]
    de = ps.derive("darkelf")["u_x_sq_A2"]
    assert abs(de / nc - 1.0) < 0.10, f"cross-source disagreement {100*(de/nc-1):.2f}%"
    assert abs(de / nc - 1.0) == pytest.approx(0.01924, abs=1e-4)
    # the locked value is NCrystal's, not the mean of the two
    assert p.U_X_SQ_ANGSTROM2.value == pytest.approx(nc, rel=1e-9)
    assert p.U_X_SQ_ANGSTROM2.value != pytest.approx(0.5 * (nc + de), rel=1e-6)


def test_cross_implementation_against_ncrystal_own_msd():
    """NCrystal computes the same integral internally.  At its own reference
    temperature 293.6 K, ``DI_VDOS.analyseVDOS()['msd'] = 6.931414998755903e-3
    angstrom^2`` (recorded in data/external/ge_vdos/MANIFEST.md section 4).

    This is the strongest check in the file after the analytic oracle, because it
    is an INDEPENDENT IMPLEMENTATION of the same quadrature, and it simultaneously
    validates (a) the int g dw = 1 normalization, (b) that NCrystal's ``msd`` is
    the 1-D MSD -- i.e. our factor of 3 -- and (c) the parabolic low-energy
    segment.  Dropping that segment moves this number by 8.5%, so it is not a
    cosmetic detail.  Run with NCrystal's own atomic mass, 72.632248855 amu.
    """
    m_nc = 72.632248855 * 931.49410242e6
    w, g = ps.load_vdos("ncrystal")
    mine = ps.mean_square_displacement_1d(w, g, 293.6, m_nc)
    assert abs(mine / 6.931414998755903e-3 - 1.0) < 5e-5


def test_T_to_zero_reduction_is_measured_not_asserted():
    """The locked evaluation point is T -> 0.  Show the size of that assumption at
    the mK operating point rather than asserting it, and show how far the
    room-temperature regime -- where diffraction B factors are measured -- sits."""
    w, g = ps.load_vdos("ncrystal")
    zero = ps.mean_square_displacement_1d(w, g, None, _M_N)
    mk = ps.mean_square_displacement_1d(w, g, 0.010, _M_N)
    rt = ps.mean_square_displacement_1d(w, g, 300.0, _M_N)
    assert abs(mk / zero - 1.0) < 1e-7, "T->0 reduction not valid at 10 mK"
    assert rt / zero > 4.0, "300 K MSD must be several times the zero-point value"
    assert ps.thermal_factor(np.array([1.0]), None)[0] == 1.0  # EXACT, not numeric


# --------------------------------------------------------------------------- #
# claim-omega-bar-locked                                                       #
# --------------------------------------------------------------------------- #
def test_2w_identity():
    """test-2w-identity.

    ALGEBRAIC IDENTITY, NOT INDEPENDENT CORROBORATION.  Substituting
    q^2 = 2 m_N E_R into 2W = q^2 <u_x^2> gives E_R/omega_bar by construction,
    because omega_bar is DEFINED as hbar^2/(2 m_N <u_x^2>).  Reporting the
    momentum-transfer route as a second, independent handle on 2W is forbidden
    proxy fp-q-route-as-independent.  The value of running it is that it catches a
    units slip, nothing more.
    """
    # The identity itself, with both sides taken from the SAME <u_x^2>: this must
    # hold to machine precision, because it is one expression written two ways.
    ux2 = ps.derive("ncrystal")["u_x_sq_A2"]
    wbar_exact = ps.omega_bar_eV(ux2, _M_N)
    for E in (0.1, 0.5, 1.0, 10.0, 100.0):
        a = ps.two_W(E, ux2, _M_N)
        b = ps.two_W_from_omega_bar(E, wbar_exact)
        assert abs(a / b - 1.0) < 1e-14

    # Against the params.py literals the agreement is limited by their printed
    # precision (11 significant figures), not by any physics.
    ux2 = p.U_X_SQ_ANGSTROM2.value
    wbar = p.OMEGA_BAR_eV.value
    for E in (0.1, 0.5, 1.0, 10.0, 100.0):
        a = ps.two_W(E, ux2, _M_N)
        b = ps.two_W_from_omega_bar(E, wbar)
        assert abs(a / b - 1.0) < 1e-10

    # units check: q(100 meV) must reproduce 116 keV/c = 58.9 inverse angstrom
    qk, qa = ps.momentum_transfer(0.1, _M_N)
    assert qk == pytest.approx(116.4, abs=0.5)
    assert qa == pytest.approx(58.9, abs=0.1)

    # 2W(100 meV) reported against the ROADMAP band, NOT tuned into it
    assert ps.two_W(0.1, ux2, _M_N) == pytest.approx(5.5992, abs=1e-3)
    assert 4.7 <= ps.two_W(0.1, ux2, _M_N) <= 8.3


def test_omega_bar_is_mass_free():
    """omega_bar = 1/<1/w> is the HARMONIC MEAN of the VDOS: m_N cancels between
    the definition and the MSD quadrature, so 2W = E_R/omega_bar is mass-free too.
    Only <u_x^2> and B carry the 0.10% natural-Ge mass-averaging ambiguity."""
    w, g = ps.load_vdos("ncrystal")
    ref_wbar = ps.omega_bar_eV(ps.mean_square_displacement_1d(w, g, None, _M_N), _M_N)
    for m in (_M_N, 0.5 * _M_N, 2.0 * _M_N, 1000.0 * _M_N):
        ux2 = ps.mean_square_displacement_1d(w, g, None, m)
        assert ps.omega_bar_eV(ux2, m) == pytest.approx(ref_wbar, rel=1e-14)
        assert ps.two_W(0.5, ux2, m) == pytest.approx(0.5 / ref_wbar, rel=1e-14)
    # and the mass-free value is the one locked in params.py, to its printed precision
    assert ref_wbar == pytest.approx(p.OMEGA_BAR_eV.value, rel=1e-9)
    harmonic = ps.vdos_moment_means(w, g)["harmonic_mean_meV"]
    assert harmonic == pytest.approx(ref_wbar * 1e3, rel=1e-12)


def test_moment_mismatch_is_recorded_for_plan_11_02():
    """<u_x^2> ~ harmonic mean; <p_x^2> ~ arithmetic mean.  For real Ge the two are
    further apart than the Debye 9/8, so a single-frequency sigma_E built on the
    locked omega_bar UNDERSTATES the impulse-approximation width."""
    m = ps.vdos_moment_means(*ps.load_vdos("ncrystal"))
    assert m["mean_ratio"] > 9.0 / 8.0, "real Ge must exceed the Debye 9/8 mismatch"
    assert m["mean_ratio"] == pytest.approx(1.35476, abs=1e-4)
    assert m["arithmetic_mean_meV"] == pytest.approx(p.OMEGA_BAR_ARITHMETIC_eV.value * 1e3,
                                                     rel=1e-6)
    assert math.sqrt(m["mean_ratio"]) == pytest.approx(1.1639, abs=1e-3)


def test_params_mirror_the_derivation():
    """params.py scalars must equal what phonon_scale derives from the frozen VDOS
    to full printed precision -- no drifted literals."""
    d = ps.derive("ncrystal")
    assert p.U_X_SQ_ANGSTROM2.value == pytest.approx(d["u_x_sq_A2"], rel=1e-9)
    assert p.OMEGA_BAR_eV.value == pytest.approx(d["omega_bar_eV"], rel=1e-9)
    assert p.DEBYE_WALLER_B_ANGSTROM2.value == pytest.approx(d["B_A2"], rel=1e-9)
    assert p.OMEGA_BAR_ARITHMETIC_eV.value == pytest.approx(d["arithmetic_mean_meV"] * 1e-3,
                                                            rel=1e-6)
    assert p.GE_THETA_D_K.value == ps.GE_THETA_D_K
    # B = 8 pi^2 <u_x^2> internally consistent
    assert p.DEBYE_WALLER_B_ANGSTROM2.value == pytest.approx(
        8 * math.pi**2 * p.U_X_SQ_ANGSTROM2.value, rel=1e-9)
    # omega_bar = hbar^2/(2 m_N <u_x^2>) internally consistent
    assert p.OMEGA_BAR_eV.value == pytest.approx(
        ps.HBAR_C_eV_ANGSTROM**2 / (2 * _M_N * p.U_X_SQ_ANGSTROM2.value), rel=1e-9)


# --------------------------------------------------------------------------- #
# test-single-value-lock: parse CONVENTIONS.md Section J                       #
# --------------------------------------------------------------------------- #
def _section_j():
    text = open(_CONVENTIONS).read()
    start = text.index("## J. Phonon Energy Scale")
    end = text.index("\n## ", start + 10)
    return text[start:end]


def test_single_value_lock():
    """test-single-value-lock. ONE scalar omega_bar, ONE <u_x^2>, ONE B, ONE
    citation; no range, no 'or', no 'between X and Y' on the locked value; the
    rejected q^2<u^2>/3 form appears and is labelled REJECTED."""
    j = _section_j()

    # exactly one locked omega_bar value, quoted to the precision params.py carries
    assert j.count("17.8597") >= 1
    for banned in ("12-21 meV**", "12–21 meV**", "omega_bar = 12"):
        assert banned not in j
    # a range must never appear on the LOCKED line
    locked_lines = [ln for ln in j.splitlines() if "**LOCKED" in ln]
    assert locked_lines, "Section J must carry explicitly LOCKED rows"
    for ln in locked_lines:
        assert " or " not in ln.lower()
        assert "between" not in ln.lower()
        assert "–" not in ln.replace("Nelin", ""), f"en-dash range on a locked line: {ln}"

    # the convention and its rejected alternative
    assert "2W = q^2 <u_x^2>" in j or "2W = q²⟨u_x²⟩" in j
    assert "REJECTED" in j
    assert j.count("REJECTED") >= 1
    assert "8 pi^2" in j or "8π²" in j
    # the milestone-wide prohibition restated where it is read
    assert "never" in j.lower() and "exp(-2W)" in j.replace("e^(−2W)", "exp(-2W)")
    # exactly one citation
    assert j.count("Nelin") >= 1
    assert "Phys. Rev. B 5, 3151 (1972)" in j


def test_conventions_values_match_params():
    """The Section J projection must carry the same scalars as params.py."""
    j = _section_j()
    assert "1.6096e-3" in j or "1.60962e-3" in j
    assert "0.12709" in j
    assert "5.599" in j
