# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Plan 10-01: boundary tests for every guarded tabulated-input interpolator.

ROADMAP Phase 10 success criterion 3. Every test in this file is written so that
it FAILS against the pre-guard code -- that is the point. Phase 7 gap D3 already
shipped a guard test that passed on a vacuous metric; the ``PREFIX_*`` constants
below are the measured pre-guard return values (recorded in
``10-01-INTERPOLATOR-INVENTORY.md``), and the tests assert they are no longer
obtainable.

Structure per guarded site:
  * raises just OUTSIDE each declared bound  (lo*(1-1e-9), hi*(1+1e-9))
  * returns a finite, non-NaN value exactly AT each declared bound
  * the recorded pre-fix clamped / extrapolated value is unreachable
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import cevns
from qpd_potential import compton_source as cs
from qpd_potential import fold
from qpd_potential import wafer_self_veto as wsv
from qpd_potential.interp_guard import Domain, InterpolationDomainError, check_domain

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TAAL_NPZ = os.path.join(_ROOT, "artifacts", "stage1", "response_matrix_TaAl.npz")

# --------------------------------------------------------------------------- #
# Measured PRE-FIX return values (10-01-INTERPOLATOR-INVENTORY.md).            #
# These are what the UNGUARDED code returned just outside each table span.     #
# --------------------------------------------------------------------------- #
PREFIX_REL_UNC_BELOW = 0.25            # clamped to rel[0]
PREFIX_REL_UNC_ABOVE = 0.05            # clamped to rel[-1]
PREFIX_NUCLEUS_FIG1_BELOW = 494.7631   # clamped to R_fig[0]
PREFIX_NUCLEUS_FIG1_ABOVE = 0.5185263  # clamped to R_fig[-1]
PREFIX_EREC_AT_0P1_eV = 4.899065996392436   # THE load-bearing witness
PREFIX_TAIL_INTEGRAL_AT_1e_4 = 1073307.7521947508
PREFIX_TAIL_INTEGRAL_ABOVE = 0.0            # silent zero above the ceiling
PREFIX_INCOHERENT_S_AT_NEG = 0.0            # negative x clamped to 1e-300


def _just_below(v):
    return v * (1.0 - 1e-9)


def _just_above(v):
    return v * (1.0 + 1e-9)


# --------------------------------------------------------------------------- #
# The guard helper itself                                                      #
# --------------------------------------------------------------------------- #
def _toy_domain(**kw):
    base = dict(quantity="toy", lo=1.0, hi=10.0, units="eV",
                table="<toy>", table_lo=1.0, table_hi=10.0)
    base.update(kw)
    return Domain(**base)


def test_guard_raises_named_exception_not_bare_valueerror():
    """The guard exception is a NAMED type, distinguishable from other ValueErrors."""
    d = _toy_domain()
    with pytest.raises(InterpolationDomainError):
        check_domain(0.5, d)
    assert issubclass(InterpolationDomainError, ValueError)
    assert InterpolationDomainError is not ValueError


def test_guard_message_carries_value_domain_and_table():
    d = _toy_domain(table="data/some_frozen_table.csv", units="MeV")
    with pytest.raises(InterpolationDomainError) as ei:
        check_domain(42.0, d)
    msg = str(ei.value)
    assert "42" in msg                      # the offending value
    assert "1.0" in msg and "10.0" in msg   # the declared domain
    assert "data/some_frozen_table.csv" in msg  # the table provenance
    assert "MeV" in msg                     # the units of THIS abscissa


def test_guard_rejects_arrays_and_does_not_mask_or_drop():
    d = _toy_domain()
    with pytest.raises(InterpolationDomainError):
        check_domain(np.array([2.0, 3.0, 0.5]), d)
    # in-domain arrays pass through unchanged
    out = check_domain(np.array([1.0, 5.0, 10.0]), d)
    assert np.array_equal(out, np.array([1.0, 5.0, 10.0]))


def test_guard_rejects_nan_and_inf():
    """fp-nan-instead-of-raise: a NaN abscissa compares False against both
    bounds and would otherwise slip through every comparison."""
    d = _toy_domain()
    for bad in (np.nan, np.inf, -np.inf):
        with pytest.raises(InterpolationDomainError):
            check_domain(bad, d)


def test_declared_extension_without_witness_is_rejected():
    """fp-domain-widening: a domain wider than its table needs a named witness."""
    with pytest.raises(ValueError, match="no witness"):
        _toy_domain(lo=0.1)
    with pytest.raises(ValueError, match="no witness"):
        _toy_domain(hi=100.0)
    # ... and is accepted once a witness is named
    ok = _toy_domain(lo=0.1, witness_lo="some v1.0 anchor evaluates 0.5")
    assert ok.extends_below and not ok.extends_above


# --------------------------------------------------------------------------- #
# 1-2. cevns.ReactorFlux                                                       #
# --------------------------------------------------------------------------- #
def test_reactor_flux_pchip_raises_instead_of_returning_nan():
    """fp-nan-instead-of-raise. PRE-FIX: PchipInterpolator(extrapolate=False)
    returned NaN just outside the knots; NaN is not 'not extrapolating'."""
    fx = cevns.ReactorFlux()
    with pytest.raises(InterpolationDomainError):
        fx.log_phi_guarded(_just_below(fx.E_min))
    with pytest.raises(InterpolationDomainError):
        fx.log_phi_guarded(_just_above(fx.E_max))
    for e in (fx.E_min, fx.E_max):
        v = float(fx.log_phi_guarded(e))
        assert np.isfinite(v)


def test_reactor_flux_zero_support_truncation_is_preserved():
    """The zero returned by flux() OUTSIDE the tabulated support is a declared
    v1.0 truncation of the flux support applied BEFORE the interpolator, not a
    clamp of it. Plan 10-01 deliberately does not change it -- changing it would
    move v1.0 physics. Recorded here so the distinction is testable."""
    fx = cevns.ReactorFlux()
    assert fx.flux(_just_below(fx.E_min)) == 0.0
    assert fx.flux(_just_above(fx.E_max)) == 0.0
    assert fx.flux(fx.E_min) > 0.0
    assert fx.flux(fx.E_max) > 0.0


def test_rel_uncertainty_raises_and_prefix_clamp_unreachable():
    fx = cevns.ReactorFlux()
    with pytest.raises(InterpolationDomainError):
        fx.rel_uncertainty(_just_below(fx.E_min))
    with pytest.raises(InterpolationDomainError):
        fx.rel_uncertainty(_just_above(fx.E_max))
    # PRE-FIX these returned the clamped end values; assert unreachable.
    for probe in (fx.E_min * 0.5, fx.E_max * 2.0):
        with pytest.raises(InterpolationDomainError):
            fx.rel_uncertainty(probe)
    assert float(fx.rel_uncertainty(fx.E_min)) == pytest.approx(PREFIX_REL_UNC_BELOW)
    assert float(fx.rel_uncertainty(fx.E_max)) == pytest.approx(PREFIX_REL_UNC_ABOVE)


# --------------------------------------------------------------------------- #
# 3. cevns._interp_loglog on the NUCLEUS Fig.1 digitization                    #
# --------------------------------------------------------------------------- #
def test_nucleus_fig1_loglog_raises_outside_the_digitized_span():
    E_fig, R_fig = cevns.load_nucleus_fig1()
    lo, hi = float(E_fig[0]), float(E_fig[-1])
    for probe in (_just_below(lo), lo * 0.5, _just_above(hi), hi * 2.0):
        with pytest.raises(InterpolationDomainError):
            cevns._interp_loglog(probe, E_fig, R_fig)
    assert float(cevns._interp_loglog(lo, E_fig, R_fig)) == pytest.approx(
        PREFIX_NUCLEUS_FIG1_BELOW, rel=1e-9)
    assert float(cevns._interp_loglog(hi, E_fig, R_fig)) == pytest.approx(
        PREFIX_NUCLEUS_FIG1_ABOVE, rel=1e-9)


def test_nucleus_fig1_anchor_points_stay_in_domain():
    """reproduce_nucleus_fig1 evaluates 10-500 eV; the digitized span is
    1.020494-1578.476 eV, so the v1.0 anchor is comfortably inside."""
    E_fig, _ = cevns.load_nucleus_fig1()
    for T in (10.0, 20.0, 50.0, 100.0, 150.0, 200.0, 300.0, 500.0):
        assert float(E_fig[0]) <= T <= float(E_fig[-1])


# --------------------------------------------------------------------------- #
# 4. compton_source.mu_over_rho -- a WITNESSED extension                       #
# --------------------------------------------------------------------------- #
def test_xcom_raises_outside_the_declared_domain():
    d = cs.XCOM_DOMAIN
    with pytest.raises(InterpolationDomainError):
        cs.mu_over_rho(_just_below(d.lo))
    with pytest.raises(InterpolationDomainError):
        cs.mu_over_rho(_just_above(d.hi))
    for e in (d.lo, d.hi):
        v = float(cs.mu_over_rho(e))
        assert np.isfinite(v) and v > 0.0


def test_xcom_declared_extension_has_a_witness_inside_it():
    """test-domain-extension-witness: the declared domain is wider than the
    table on both sides, and both extensions carry a named v1.0 witness."""
    d = cs.XCOM_DOMAIN
    assert d.extends_below and d.extends_above
    assert d.witness_lo and d.witness_hi
    # The witnesses are real gamma lines that the v1.0 Compton channel folds.
    lines = np.array([float(r.energy_keV) for r in cs.load_gamma_lines()])
    assert lines.min() < d.table_lo, "no witness below the table floor"
    assert lines.max() > d.table_hi, "no witness above the table ceiling"
    assert d.lo <= lines.min() and lines.max() <= d.hi
    # and the extension actually evaluates there
    assert float(cs.mu_over_rho(lines.min())) > 0.0
    assert float(cs.mu_over_rho(lines.max())) > 0.0


def test_xcom_low_energy_extrapolation_is_no_longer_unbounded():
    """PRE-FIX the slope extrapolation ran to arbitrarily low energy, silently
    returning a Compton-regime mu/rho where Ge is photoabsorption-dominated."""
    for e_keV in (100.0, 10.0, 1.0):
        with pytest.raises(InterpolationDomainError):
            cs.mu_over_rho(e_keV)


# --------------------------------------------------------------------------- #
# 5. compton_source.incoherent_S -- an HONESTLY VACUOUS bounds guard           #
# --------------------------------------------------------------------------- #
def test_incoherent_S_declared_domain_is_unbounded_and_witnessed():
    """This site's declared domain is [0, inf). Stated plainly: the bounds guard
    is VACUOUS for every finite non-negative x, because exact forward scatter
    genuinely produces x = 0 and S(x -> inf) = Z = 32 is the exact asymptote.
    Both extensions are witnessed; neither can be narrowed without breaking the
    v1.0 Compton channel."""
    d = cs.SF_DOMAIN
    assert d.lo == 0.0 and d.hi == float("inf")
    assert d.witness_lo and d.witness_hi
    # the witness is real: exact forward scatter gives x == 0 identically
    assert float(cs.momentum_transfer_x(1460.822, 1.0)) == 0.0
    assert float(cs.incoherent_S(0.0)) == 0.0


def test_incoherent_S_rejects_negative_momentum_transfer():
    """The ONE silent failure this site actually had: negative x was mapped to
    1e-300 by np.maximum and returned S = 0.0. PRE-FIX value 0.0, now a raise."""
    for bad in (-1.0, -1e-9, np.array([0.1, -0.1])):
        with pytest.raises(InterpolationDomainError):
            cs.incoherent_S(bad)
    with pytest.raises(InterpolationDomainError):
        cs.incoherent_S(np.nan)


# --------------------------------------------------------------------------- #
# 6. fold._erec_of_edep -- THE load-bearing witness of the phase               #
# --------------------------------------------------------------------------- #
def _erec_curve():
    z = np.load(_TAAL_NPZ, allow_pickle=True)
    return z["E_dep_centers_eV"], z["E_rec_median_non_paralyzable_eV"]


def test_erec_of_edep_raises_below_the_response_floor():
    cen, med = _erec_curve()
    lo, hi = float(cen.min()), float(cen.max())
    for probe in (_just_below(lo), 1.0, 0.5, 0.1):
        with pytest.raises(InterpolationDomainError):
            fold._erec_of_edep(probe, cen, med)
    with pytest.raises(InterpolationDomainError):
        fold._erec_of_edep(_just_above(hi), cen, med)
    for e in (lo, hi):
        v = float(fold._erec_of_edep(e, cen, med))
        assert np.isfinite(v) and v > 0.0


def test_erec_of_edep_prefix_clamped_plateau_is_unreachable():
    """THE decisive pre-fix witness. Before the guard, asking for the
    reconstructed energy of a 0.1 eV deposit returned 4.899065996392436 eV --
    the E_rec of a 10.144970 eV deposit -- overstating E_rec by a factor ~49
    with no error and no NaN. The SAME value came back for 0.5 eV and 1 eV: a
    flat invented plateau exactly where plan 10-03 extends the axis."""
    cen, med = _erec_curve()
    at_floor = float(fold._erec_of_edep(float(cen.min()), cen, med))
    assert at_floor == pytest.approx(PREFIX_EREC_AT_0P1_eV, rel=1e-12)
    # the SAME number is what 0.1 / 0.5 / 1 eV used to return; now unreachable
    for probe in (0.1, 0.5, 1.0):
        with pytest.raises(InterpolationDomainError) as ei:
            fold._erec_of_edep(probe, cen, med)
        assert "out of declared evaluation domain" in str(ei.value)


def test_erec_of_edep_v1_anchor_points_unchanged():
    """No physics number may move. The saturation onset / plateau deposits that
    fold.make_spectra_figure evaluates are inside the domain and unchanged."""
    z = np.load(_TAAL_NPZ, allow_pickle=True)
    cen = z["E_dep_centers_eV"]
    med = z["E_rec_median_non_paralyzable_eV"]
    onset = float(z["saturation_onset_Edep_eV"])
    plateau = float(z["whole_array_plateau_Edep_eV"])
    for e in (onset, plateau):
        assert float(cen.min()) <= e <= float(cen.max())
        assert np.isfinite(float(fold._erec_of_edep(e, cen, med)))


# --------------------------------------------------------------------------- #
# 7. wafer_self_veto._tail_integral                                            #
# --------------------------------------------------------------------------- #
def test_tail_integral_raises_outside_the_frozen_grid():
    g, _ = wsv.frozen_spectrum()
    lo, hi = float(g[0]), float(g[-1])
    for probe in (_just_below(lo), 1e-4, _just_above(hi), hi * 10.0):
        with pytest.raises(InterpolationDomainError):
            wsv._tail_integral(probe)
    for e in (lo, hi):
        v = float(wsv._tail_integral(e))
        assert np.isfinite(v)


def test_tail_integral_prefix_values_unreachable():
    """PRE-FIX: _tail_integral(1e-4 keV) returned 1073307.7521947508 -- a
    finite, nearly-right, fabricated number built from the clamped floor rate
    16.01101 extended over a decade with no data. Above the ceiling it returned
    exactly 0.0, a silent zero rather than an error."""
    with pytest.raises(InterpolationDomainError):
        wsv._tail_integral(1e-4)
    g, _ = wsv.frozen_spectrum()
    with pytest.raises(InterpolationDomainError):
        wsv._tail_integral(float(g[-1]) * 2.0)
    # the true full integral is essentially the pre-fix number: that is exactly
    # why the pre-fix return was so hard to notice.
    _, rate = wsv.frozen_spectrum()
    denom = float(wsv._trapz(rate, g))
    assert denom == pytest.approx(PREFIX_TAIL_INTEGRAL_AT_1e_4, rel=2e-7)


def test_a_self_direct_short_circuits_are_unchanged():
    """a_self_direct's documented floor/ceiling short-circuits sit BEFORE
    _tail_integral, so the guard changes nothing about the v1.0 acceptance."""
    g, _ = wsv.frozen_spectrum()
    assert wsv.a_self_direct(float(g[0])) == 1.0
    assert wsv.a_self_direct(float(g[0]) * 0.5) == 1.0
    assert wsv.a_self_direct(float(g[-1])) == 0.0
    assert wsv.a_self_direct(float(g[-1]) * 2.0) == 0.0
    # and the physically interesting thresholds still evaluate
    for e_cut in (0.01014497 * 1.0000001, 1.0, 100.0):
        v = wsv.a_self_direct(e_cut)
        assert 0.0 <= v <= 1.0


# --------------------------------------------------------------------------- #
# test-inventory-closure: the enumeration is reproducible, not remembered      #
# --------------------------------------------------------------------------- #
_GREP_PATTERN = r"np\.interp\|PchipInterpolator\|CubicSpline\|interp1d\|_interp_loglog\|loglog_interp"
_INVENTORY = os.path.join(
    _ROOT, "GPD", "phases",
    "10-sub-ev-grid-extension-and-the-trigger-observable-p-grid",
    "10-01-INTERPOLATOR-INVENTORY.md",
)


def _grep_hits():
    import subprocess
    out = subprocess.run(
        ["grep", "-rn", _GREP_PATTERN, "--include=*.py", "src/"],
        cwd=_ROOT, capture_output=True, text=True,
    ).stdout.strip().splitlines()
    return out


def test_inventory_closure_grep_hits_equal_inventory_rows():
    """fp-grep-by-recall: the enumeration must be re-runnable, and every hit the
    recorded command returns must appear exactly once in the inventory table."""
    assert os.path.exists(_INVENTORY), "the interpolator inventory is missing"
    text = open(_INVENTORY).read()
    hits = _grep_hits()
    # 33 at the close of Phase 10; 34 after plan 11-01 registered
    # phonon_scale.vdos_weight_quantile_meV; 35 after plan 11-03 registered the
    # analytic one-phonon add-back in impulse_limit.structure_factor; 41 after plan
    # 13-01 registered the six sites in neutron_recoil.py (the frozen ENDF sigma_el
    # evaluation, the two ln-E maps of the smoothed-sigma control, the control's own
    # node evaluation, the per-isotope cross-check fold and the a1 diagnostic).
    # Bumping this number is the ONLY sanctioned response to a new hit, and it must
    # come with an inventory row.
    assert len(hits) == 41, f"grep hit count changed: {len(hits)}"
    rows = [ln for ln in text.splitlines()
            if ln.startswith("| `src/") and ln.count("|") >= 6]
    assert len(rows) == len(hits), (
        f"inventory has {len(rows)} rows for {len(hits)} grep hits")
    for h in hits:
        path, line, _ = h.split(":", 2)
        key = f"`{path}:{line}`"
        assert text.count(key) >= 1, f"grep hit {key} missing from the inventory"


def test_inventory_every_row_has_a_verdict_and_a_justification():
    text = open(_INVENTORY).read()
    rows = [ln for ln in text.splitlines()
            if ln.startswith("| `src/") and ln.count("|") >= 6]
    for ln in rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        verdict = cells[-2]
        justification = cells[-1]
        assert verdict in ("GUARDED", "excluded"), f"bad verdict {verdict!r} in {ln}"
        assert len(justification) > 20, f"empty/short justification in {ln}"


def test_inventory_records_a_finite_prefix_return_outside_a_table_span():
    """test-witness-pre-fix pass condition: at least one call site must be shown
    to have previously returned a finite non-error value OUTSIDE its table span.
    If none did, the guard would be vacuous and the phase would have to say so."""
    text = open(_INVENTORY).read()
    assert "4.899065996392436" in text, "the load-bearing fold.py witness is missing"
    assert "1073307.7521947508" in text
    assert "0.11879" in text and "0.036064" in text  # XCOM slope extrapolation
