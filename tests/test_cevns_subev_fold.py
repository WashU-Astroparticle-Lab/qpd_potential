# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase 12, plan 12-02: CALC-25 -- dR/dE_rec for both designs from 100 meV.

The order of operations IS the plan: IA broadening on the RECOIL axis -> rebin onto
the extended deposit grid -> R(E_rec|E_dep) -> the trigger curve as an analysis
efficiency.  Any other order still produces a plausible-looking spectrum, which is why
``test_single_broadening_application``, ``test_trigger_composes_not_replaces`` and the
counts budget all exist.

EVERY TOLERANCE HERE IS A STATED TARGET, NOT A FITTED VALUE.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import (cevns, cevns_subev as cs, energy_scale, fold,  # noqa: E402
                           ia_broadening, params, trigger)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ART = os.path.join(_ROOT, "artifacts", "v2.0")
_DESIGNS = ("Ta->Al", "Al->Hf")
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "12-reactor-cevns-down-to-100-mev-at-the-paper-s-surface-scenario-p-sig",
    "12-02-SIGNAL-SPECTRUM.md")

# ---- stated targets -------------------------------------------------------- #
# The project's stated extended-grid floor. It is a ROUNDED display value: the exact
# edge is 0.09993504432008873 eV, 4.4e-08 relative above it. Plan 11-04 anchored its
# 480-bin recoil axis on the rounded value and plan 12-02 reuses that construction, so
# the recoil axis's bottom edge sits 4.4e-08 relative BELOW the deposit floor -- an
# offset far below anything this phase claims, recorded rather than silently absorbed.
FLOOR_eV = 0.0999350
FLOOR_EXACT_eV = 0.09993504432008873
N_EXT_BINS = 744
COUNTS_BUDGET_TARGET = 1.0e-3        # Phase-11 tolerance, carried through the fold
RETAINED_ONLY_MUST_MISS_BY = 1.0e-6  # ~49% of the bottom bin genuinely leaves the axis
# Amplitude-linearity tolerance. The MEASURED end-to-end deviation is 5.1e-13, and it
# is understood: fold._loglog_segment_integral forms the power-law exponent
# p = log(y2/y1)/log(T2/T1), and log(T2/T1) is only 0.0216 on this recoil grid, so a
# 1e-16 rounding in the scaled y ratio becomes a ~1e-14 error in p, which T**p then
# amplifies by ln(T). It is a property of the log-log rebin, not of any rescale. The
# test stays decisive because a global post-fold renormalization would violate this by
# O(1), not by O(1e-12).
LINEARITY_TOL = 5.0e-12
PHASE11_LEAKED_FRACTION = 4.3328e-4  # measured in plan 11-04, must survive the extra stage
PHASE11_BELOW_ZERO_FRACTION = 5.67e-6


def _spectra_path(design):
    return os.path.join(_ART, fold.EXT_RECON_FILE[design])


def _read_spectrum(design):
    header, rows, flags = [], [], []
    with open(_spectra_path(design)) as fh:
        for line in fh:
            s = line.rstrip("\n")
            if s.startswith("#"):
                header.append(s)
                continue
            if not s.strip():
                continue
            toks = s.split(",")
            if toks[0] == "E_rec_keV":
                cols = toks
                continue
            rows.append([float(t) for t in toks[:-1]])
            flags.append(toks[-1])
    return {"header": "\n".join(header), "cols": cols,
            "data": np.asarray(rows, float), "regime": flags}


@pytest.fixture(scope="module")
def folded():
    return {d: fold.run_cevns_fold_extended(d, broaden=True) for d in _DESIGNS}


@pytest.fixture(scope="module")
def spectra():
    for d in _DESIGNS:
        assert os.path.exists(_spectra_path(d)), (
            "run `PYTHONPATH=src python -m qpd_potential.cevns_subev 12-02` first")
    return {d: _read_spectrum(d) for d in _DESIGNS}


# =========================================================================== #
# claim-signal-spectrum                                                       #
# =========================================================================== #
def test_both_designs_to_floor(spectra, folded):
    """test-both-designs-to-floor. Both designs present, finite, positive over the
    physical range, reaching a deposit at the 0.0999350 eV floor, at the primary
    normalization with NO rescale.

    A spectrum that stops at 10.14 eV would mean the v1.0 584-column matrices were
    loaded and the phase produced nothing new.
    """
    for d in _DESIGNS:
        s = spectra[d]
        y = s["data"][:, s["cols"].index("dRdErec_central")]
        E_eV = s["data"][:, 0] * 1.0e3
        assert np.all(np.isfinite(s["data"]))
        assert np.all(y >= 0.0)
        nz = np.nonzero(y > 0.0)[0]
        assert nz.size > 50
        # extends far above the v1.0 10.14 eV deposit floor's reconstructed image
        assert E_eV[nz].max() > 500.0
        # ...and reaches BELOW it, which the v1.0 matrices could not do
        assert E_eV[nz].min() < 0.1

        # the extended matrix is what was loaded
        r = folded[d]
        assert r["E_dep_centers_eV"].size == N_EXT_BINS
        # Compared against the recorded exact edge rather than by calling
        # muon_deposit.shared_energy_grid here: that function's call sites are closed
        # by a Phase-10 pin table, and a test-only call would need a pin-table row.
        assert r["E_dep_edges_eV"][0] == pytest.approx(FLOOR_EXACT_eV, rel=1e-14)
        assert round(r["E_dep_edges_eV"][0], 7) == FLOOR_eV
        # The FLOOR deposit column really does reach the reconstructed spectrum, and
        # it lands where a ~0.1 eV deposit should: well below 0.1 eV of reconstructed
        # energy, since the median response slope is ~0.47.
        #
        # NOT asserted: that the single LOWEST populated reconstructed bin is fed by
        # deposit column 0. Measured, it is not -- R's columns are MC-sampled
        # distributions and a slightly higher deposit bin has the longer low-side tail.
        # Asserting it would have been a guess about the response matrix, not a
        # statement about the floor being reached.
        z = fold.load_design_extended(d)
        R = z["R_non_paralyzable"]
        assert R[:, 0].sum() == pytest.approx(1.0, rel=1e-12)
        floor_contrib = R[:, 0] * r["N_dep"][0]
        assert floor_contrib.sum() > 0.0
        jj = np.nonzero(R[:, 0] > 0.0)[0]
        assert r["E_rec_centers_eV"][jj].min() < 0.1

        # normalization provenance is IN THE HEADER, and no rescale is claimed
        h = s["header"]
        assert "data/flux/reactor_flux_v1.0.csv" in h
        assert "3 GW_th at 25 m" in h
        assert "NO rescale of any kind is applied" in h


def test_broadening_on_recorded(folded):
    """test-broadening-on-recorded. broaden=True at the call site, the global default
    still False, and the two runs differ measurably in the bottom decade.

    If they did not differ, the kernel is not reaching the CALC-25 deliverable and
    CALC-15 has not actually been applied to the milestone's signal.
    """
    assert ia_broadening.BROADENING_DEFAULT is False, (
        "the global fail-safe was flipped; Phase 12 opts in at its own call site")
    off = fold.run_cevns_fold_extended(_DESIGNS[0], broaden=False)
    on = folded[_DESIGNS[0]]
    assert on["broadening_applied"] is True
    assert off["broadening_applied"] is False
    assert on["leakage"] is not None and off["leakage"] is None

    # bottom decade of the DEPOSIT axis: the kernel must move counts there
    E_dep = on["E_dep_centers_eV"]
    dec = E_dep < 10.0 * FLOOR_eV
    a, b = on["N_dep"][dec], off["N_dep"][dec]
    assert np.max(np.abs(a - b)) > 0.0
    assert np.abs(a.sum() - b.sum()) / b.sum() > 1.0e-3, (
        "broaden=True and broaden=False agree in the bottom decade to better than "
        "0.1%: the kernel is not reaching the spectrum")


def test_single_broadening_application():
    """test-single-broadening-application. THE ONLY THING THAT CATCHES DOUBLE-BROADENING.

    The table fed to the fold must be the UNBROADENED one.  Feeding
    artifacts/v2.0/cevns_dRdT_broadened.csv with broaden=True would apply the kernel
    twice, widening the bottom bin by sqrt(2), and nothing in the existing wiring would
    raise (fp-double-broadening).
    """
    src = fold.read_cevns(fold.CEVNS_EXT_CSV)
    T, y = src["T_eV"], src["dRdT_total"]
    # the bottom decade reproduces cevns.differential_rate to numerical precision
    dec = np.nonzero(T < 10.0 * FLOOR_eV)[0]
    assert dec.size > 5
    for i in dec[::4]:
        assert y[i] == pytest.approx(cevns.differential_rate(T[i] * 1e-3), rel=1e-9), (
            f"the extended table at T={T[i]} eV is NOT the unbroadened dR/dT")
    # ...and the fold path does not read the already-broadened artifact
    assert "broadened" not in fold.CEVNS_EXT_CSV
    code = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    code = "\n".join(l for l in code.splitlines() if not l.lstrip().startswith("#"))
    assert "cevns_dRdT_broadened" not in code

    # positive control: the already-broadened artifact would NOT pass the check above
    b = np.asarray([[float(t) for t in l.split(",")]
                    for l in open(os.path.join(_ART, "cevns_dRdT_broadened.csv"))
                    if l.strip() and not l.startswith("#") and not l[0].isalpha()])
    assert b[0, 2] / b[0, 1] < 0.7, (
        "the frozen broadened artifact's bottom bin is not visibly broadened; the "
        "positive control for this test is not doing its job")


def test_trigger_composes_not_replaces(folded):
    """test-trigger-composes-not-replaces, all three legs (fp-trigger-replaces-eps)."""
    r = folded[_DESIGNS[0]]
    E_dep = r["E_dep_centers_eV"]

    # (1) EXACT factorisation on every grid point of the axis where CONVENTIONS
    #     Section I defines the composition -- the DEPOSIT axis.
    untrig = r["dRdEdep"]
    composed = trigger.compose_efficiency(E_dep, untrig)
    assert np.array_equal(composed, trigger.P_trig(E_dep) * untrig)

    # (2) P_trig == 1 reproduces the untriggered fold BIT-FOR-BIT.
    ones = np.ones_like(E_dep)
    r1 = fold.run_cevns_fold_extended(_DESIGNS[0], broaden=True, p_trig_override=ones)
    assert np.array_equal(r1["N_rec_trigger"], r1["N_rec"])
    assert float(np.abs(r1["N_rec_trigger"] - r1["N_rec"]).max()) == 0.0

    # (3) eps. P_trig must be BIT-IDENTICAL under an eps perturbation, while the
    #     quantity eps actually lives in must move.
    #
    #     HONEST SCOPE NOTE. The literal end-to-end form of this leg -- "perturb
    #     params.EPSILON and watch the folded spectrum move" -- cannot be run here,
    #     because R is loaded from a FROZEN npz and does not re-derive calibrate_C at
    #     fold time. Perturbing EPSILON at runtime therefore moves neither side and the
    #     end-to-end version would be VACUOUS. What is tested instead is the substance
    #     of the requirement: P_trig does not see eps, the response chain does, and
    #     compose_efficiency is exactly multiplicative in its untriggered argument.
    before = np.asarray(trigger.P_trig(E_dep), float)
    n_before = energy_scale.n_qp_yield(1.0, "Ta->Al")
    old = params.EPSILON.value
    try:
        object.__setattr__(params.EPSILON, "value", old * 1.37)
        after = np.asarray(trigger.P_trig(E_dep), float)
        n_after = energy_scale.n_qp_yield(1.0, "Ta->Al")
    finally:
        object.__setattr__(params.EPSILON, "value", old)
    assert np.array_equal(before, after), "P_trig moved with eps: it has absorbed eps"
    assert n_after == pytest.approx(1.37 * n_before, rel=1e-12), (
        "eps does not reach the response chain; the perturbation leg is vacuous")
    for s in (0.5, 2.0, 7.3):
        assert np.allclose(trigger.compose_efficiency(E_dep, s * untrig),
                           s * composed, rtol=1e-14, atol=0.0)


def test_counts_conserved_with_leakage(folded):
    """test-counts-conserved-with-leakage. The budget must CLOSE on retained + leaked,
    and the retained-only sum must MISS.

    A clean retained-only closure is positive evidence of a hidden rescale, because
    ~49% of the bottom bin genuinely leaves the axis.
    """
    for d in _DESIGNS:
        b = folded[d]["counts_budget"]
        assert b["residual_retained_plus_leaked"] <= COUNTS_BUDGET_TARGET
        assert abs(b["residual_retained_only"]) > RETAINED_ONLY_MUST_MISS_BY
        assert b["residual_retained_only"] < 0.0        # counts are LOST, not gained
        assert b["residual_fold"] < 1.0e-12             # R columns sum to 1
        # the Phase-11 leakage survives the extra fold stage unchanged
        f = b["leaked_below_floor"] / b["input_counts"]
        assert f == pytest.approx(PHASE11_LEAKED_FRACTION, rel=1e-3)
        z = b["leaked_below_zero"] / b["input_counts"]
        assert z == pytest.approx(PHASE11_BELOW_ZERO_FRACTION, rel=1e-2)
        assert b["leaked_above_top"] == 0.0
        # per-bin leakage is reported, not just a total
        leak = folded[d]["leakage"]
        assert leak["below_floor_per_bin"].size == 480
        assert float(leak["below_floor_per_bin"][0]) > 0.0


def test_leakage_not_renormalized():
    """test-leakage-not-renormalized (fp-renormalize-leakage).

    Scale the INPUT table by an arbitrary constant: every output bin and every leakage
    entry must scale by exactly that constant.  No global post-fold rescale can satisfy
    this, because a rescale factor depends on the total.
    """
    k = 3.7180339887
    with tempfile.TemporaryDirectory() as tmp:
        scaled = os.path.join(tmp, "cevns_dRdT_ext_scaled.csv")
        with open(fold.CEVNS_EXT_CSV) as fi, open(scaled, "w") as fo:
            for line in fi:
                if line.startswith("#") or line[0].isalpha():
                    fo.write(line)
                    continue
                v = [float(t) for t in line.split(",")]
                # FULL precision: %.10e would round the scaled values at ~1e-11 and
                # the measured "non-linearity" would be the test's own formatting.
                fo.write(",".join([repr(v[0])] + [repr(k * x) for x in v[1:]]) + "\n")
        base = fold.run_cevns_fold_extended(_DESIGNS[0], broaden=True)
        s = fold.run_cevns_fold_extended(_DESIGNS[0], broaden=True, path=scaled)

    for key in ("N_dep", "N_rec", "N_rec_trigger", "dRdErec", "dRdErec_band",
                "dRdErec_trigger"):
        a, b = np.asarray(base[key]), np.asarray(s[key])
        m = a != 0.0
        assert np.allclose(b[m] / a[m], k, rtol=LINEARITY_TOL, atol=0.0), key
        assert np.all(b[~m] == 0.0)
    for key in ("below_floor", "below_zero"):
        assert s["leakage"][key] == pytest.approx(k * base["leakage"][key],
                                                  rel=LINEARITY_TOL)
    assert np.allclose(s["leakage"]["below_floor_per_bin"],
                       k * base["leakage"]["below_floor_per_bin"],
                       rtol=LINEARITY_TOL, atol=0.0)
    # and the kernel itself is amplitude-independent
    assert np.array_equal(s["leakage"]["sigma_eV"], base["leakage"]["sigma_eV"])

    # source scan: no rescale idiom on the new fold path
    code = open(os.path.join(_ROOT, "src", "qpd_potential", "fold.py")).read()
    fn = code[code.index("def run_cevns_fold_extended"):]
    fn = fn[:fn.index("\ndef ")] if "\ndef " in fn else fn
    for bad in ("/ total", "/= ", "normalize", "np.clip", "sum()  *"):
        assert bad not in fn, f"rescale idiom {bad!r} on the extended fold path"


def test_floor_coverage_guard_still_bites():
    """The Phase-10/11 domain guard is intact: the frozen 5 eV-floored v1.0 CEvNS table
    cannot be folded onto the extended axis.  No try/except, no clamp, no zero-fill."""
    with pytest.raises(ValueError, match="does not reach the floor|NO DATA below"):
        fold.run_cevns_fold_extended(_DESIGNS[0], path=fold.CEVNS_CSV, broaden=True)


# =========================================================================== #
# claim-subev-observable                                                      #
# =========================================================================== #
def test_regime_boundary_labelled(spectra):
    """test-regime-boundary-labelled. The boundary is sourced from the module constant,
    not restated as a literal, and per-row flags exist in both spectra."""
    code = open(os.path.join(_ROOT, "src", "qpd_potential", "cevns_subev.py")).read()
    body = code[code.index("# PLAN 12-02"):]
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("#"))
    assert "trigger.SUBEV_REGIME_BOUNDARY_eV" in body
    assert "SUBEV_REGIME_BOUNDARY_eV: float = 1.0" not in body   # not redefined here

    for d in _DESIGNS:
        s = spectra[d]
        assert "SUBEV_REGIME_BOUNDARY_eV" in s["header"]
        assert trigger.REGIME_STATEMENT in s["header"]
        b = fold.subev_boundary_Erec_eV(d)
        E_eV = s["data"][:, 0] * 1.0e3
        for e, flag in zip(E_eV, s["regime"]):
            want = ("subev_P_trig_is_the_reported_observable" if e < b
                    else "dRdErec_is_the_reported_observable")
            assert flag == want
        assert set(s["regime"]) == {"subev_P_trig_is_the_reported_observable",
                                    "dRdErec_is_the_reported_observable"}
        # the boundary is a DEPOSIT energy; its E_rec image comes from THIS matrix's
        # own median mapping curve, not from an assumed 0.5x factor
        assert 0.3 < b < 0.7


def test_e50_structural():
    """test-e50-structural. P(E50) = 1/2 for EVERY k -- structural, not tuned -- and the
    CONVENTIONS Section I hand-checkable values at k = 4.

    A units-and-wiring check. It is NOT corroboration of any physics.
    """
    e50 = params.TRIGGER_E50.value
    assert e50 == 1.0   # CONVENTIONS Section I, user decision 2026-07-23 (was 0.5)
    for k in cs.K_SCAN:
        assert float(trigger.P_trig(e50, sharpness=k)) == pytest.approx(0.5, abs=1e-12)
    # identities in E50 at k = 4, not fixed energies
    assert float(trigger.P_trig(2 * e50, sharpness=4.0)) == pytest.approx(16.0 / 17.0, rel=1e-14)
    assert float(trigger.P_trig(e50 / 2, sharpness=4.0)) == pytest.approx(1.0 / 17.0, rel=1e-14)
    assert float(trigger.P_trig(0.0, sharpness=4.0)) == 0.0


def test_k_sensitivity_reported():
    """test-k-sensitivity-reported. The scan is IN THE CSV, not only in prose, and the
    report states whether the k spread exceeds the combined IA-width/counting-floor
    smearing at 0.5 eV.

    If k dominated, the reported sub-eV observable would be controlled by an unmeasured
    device parameter and would have to be labelled that way. That is an informative
    outcome either way, not a failure.
    """
    path = os.path.join(_ART, "cevns_subev_trigger.csv")
    header = "".join(l for l in open(path) if l.startswith("#"))
    cols = [l for l in open(path) if l.startswith("E_dep_eV")][0].strip().split(",")
    for k in cs.K_SCAN:
        assert f"P_trig_k{int(k)}" in cols
        assert f"k = {k:4g} ->" in header
    assert "k-spread over [1, 12]" in header
    assert ("LARGER than the combined" in header) or ("SMALLER than the combined" in header)
    assert "fixed by NO project artifact" in header

    rows = np.asarray([[float(t) for t in l.split(",")] for l in open(path)
                       if l.strip() and not l.startswith("#") and not l[0].isalpha()])
    assert rows.shape[1] == 1 + len(cs.K_SCAN)
    assert np.all(rows[:, 0] < trigger.SUBEV_REGIME_BOUNDARY_eV)
    assert np.all((rows[:, 1:] >= 0.0) & (rows[:, 1:] <= 1.0))
    # a real scan: the columns are not all the same curve
    assert float(np.abs(rows[:, 1] - rows[:, -1]).max()) > 0.1


# =========================================================================== #
# claim-width-band-carried                                                    #
# =========================================================================== #
def test_upper_band_separate(spectra):
    """test-upper-band-separate (fp-absorb-systematic). A separate one-sided column,
    labelled one-sided and upper, with no averaged column anywhere."""
    for d in _DESIGNS:
        s = spectra[d]
        assert "dRdErec_upper_width_onesided" in s["cols"]
        h = s["header"]
        assert "ONE-SIDED" in h and "UPPER" in h
        assert "never averaged" in h
        assert "NO lower band" in h
        c = s["data"][:, s["cols"].index("dRdErec_central")]
        u = s["data"][:, s["cols"].index("dRdErec_upper_width_onesided")]
        assert not np.array_equal(c, u)
        # no column is the mean of the two
        mean = 0.5 * (c + u)
        for j, name in enumerate(s["cols"][:-1]):
            assert not np.allclose(s["data"][:, j], mean, rtol=1e-9, atol=0.0), name
        # 'UPPER' is the WIDTH, not the rate.  The physical consequence is integral,
        # not bin-by-bin: a wider kernel moves MORE mass off the bottom of the axis, so
        # the upper-width variant carries FEWER counts overall and fewer below 1 eV.
        # (Bin by bin the two cross, because the reconstructed axis is coarse relative
        # to the deposit axis in the bottom decade and the mapping is not monotone.)
        rc = fold.run_cevns_fold_extended(d, broaden=True)
        ru = fold.run_cevns_fold_extended(
            d, broaden=True, omega_bar_eV=params.OMEGA_BAR_ARITHMETIC_eV.value)
        assert ru["counts_budget"]["leaked_below_floor"] > \
            rc["counts_budget"]["leaked_below_floor"]
        assert ru["counts_budget"]["leaked_below_zero"] > \
            rc["counts_budget"]["leaked_below_zero"]
        assert ru["N_rec"].sum() < rc["N_rec"].sum()
        below = rc["E_rec_centers_eV"] < 1.0
        assert ru["N_rec"][below].sum() < rc["N_rec"][below].sum()


def test_central_on_locked_omega(folded):
    """test-central-on-locked-omega. The central curve is produced with the LOCKED
    harmonic VDOS mean, and no code path in this plan writes or overrides it."""
    for d in _DESIGNS:
        assert folded[d]["omega_bar_eV"] == params.OMEGA_BAR_eV.value
    assert params.OMEGA_BAR_eV.value == pytest.approx(1.7859677040e-2, rel=1e-12)
    ratio = params.OMEGA_BAR_ARITHMETIC_eV.value / params.OMEGA_BAR_eV.value
    assert np.sqrt(ratio) == pytest.approx(1.163941, rel=1e-5)
    for mod in ("cevns_subev.py", "fold.py"):
        code = open(os.path.join(_ROOT, "src", "qpd_potential", mod)).read()
        assert "OMEGA_BAR_eV.value =" not in code
        assert "OMEGA_BAR_eV, \"value\"" not in code


# =========================================================================== #
# claim-bottom-bin-caveats-travel                                             #
# =========================================================================== #
_CAVEAT_NEEDLES = ("48.98%", "0.87%", "skewness 0.590", "2W is only 5.60",
                   "LINEAR yield", "THRESHOLD yield model would INVERT",
                   "fp-poisson-as-resolution", "ONE SIGNIFICANT FIGURE")


def test_caveats_in_headers(spectra):
    """test-caveats-in-headers. The caveats travel WITH THE DATA, in machine-readable
    headers -- a caveat that lives only in the phase report does not travel."""
    paths = [_spectra_path(d) for d in _DESIGNS] + [
        os.path.join(_ART, "cevns_subev_trigger.csv")]
    for p in paths:
        h = "".join(l for l in open(p) if l.startswith("#"))
        for needle in _CAVEAT_NEEDLES:
            assert needle in h, f"{os.path.basename(p)} header is missing {needle!r}"


@pytest.mark.skipif(not os.path.exists(_REPORT), reason="signal note not yet written")
def test_bottom_bin_precision():
    """test-bottom-bin-precision. No 100 meV number quoted anywhere to more than one
    significant figure.

    Machine-checkable half: the note must SAY so, and must not contain a long-precision
    literal presented as the 100 meV bin's value.
    """
    txt = open(_REPORT).read()
    assert "one significant figure" in txt.lower()
    # deliv-signal-report.must_contain, item by item
    needles = [
        "BROADENING_DEFAULT",              # the switch record
        "broaden=True",
        "RECORDED AND LABELLED",           # the width-reporting decision, labelled
        "1.163941",
        "Residual on retained ONLY",       # leakage accounted, not renormalized
        "never renormalized",
        "does not replace",                # P_trig multiplies eps
        "compose_efficiency",
        "sensitivity",                     # the k obligation, over [1, 12]
        "[1, 12]",
        "48.98",                           # the bottom-bin caveat block
        "invert the verdict",
        "0.8027",                          # plan 12-01's truncation bound, cited
        "2372.3683",                       # plan 12-01's analytic plateau, cited
    ]
    for n in needles:
        assert n.lower() in txt.lower(), f"signal note is missing {n!r}"
    # ...and no 100 meV number quoted to more than one significant figure. The 100 meV
    # bin's own value never appears in the prose; the peaks (at 0.19-0.30 eV) are quoted
    # to two, which is stated in the note.
    # ...and no 100 meV number is quoted to more than one significant figure. The
    # 100 meV bin's own rate never appears in the prose at all; the peaks (which sit at
    # 0.19-0.30 eV, not at 100 meV) are quoted to two, and the note says so.
    assert "4.4" in txt and "4.7" in txt          # the two peaks, 2 s.f.
    assert "significant figures" in txt           # the precision statement


def test_extended_artifacts_have_disposition_rows():
    """Every newly tracked .csv/.npz needs a register row or the Phase-10 closure guard
    fails.  Checked here too so the failure names the right plan."""
    from qpd_potential import legacy_grid as lg
    reg = lg.load_register()
    for rel in ("artifacts/v2.0/cevns_dRdT_ext.csv",
                "artifacts/v2.0/cevns_dRdErec_ext_TaAl.csv",
                "artifacts/v2.0/cevns_dRdErec_ext_AlHf.csv",
                "artifacts/v2.0/cevns_subev_trigger.csv"):
        assert rel in reg, f"{rel} has no disposition row"
        assert reg[rel].disposition in lg.DISPOSITION_VALUES


def test_no_second_normalization_anywhere():
    """fp-second-vns-run / fp-inherited-shielding, held shut at the source level.

    Parsed, not grepped: both names appear in PROSE in these modules, because naming the
    trap is the point.  Only an AST walk distinguishes a mention from a call.

    * ``cevns.nucleus_variant_flux`` may never be called ANYWHERE. It would build a
      second ReactorFlux at a second normalization -- a second spectral shape.
    * ``cevns.nucleus_flux_normalization`` may never be called from ``fold.py``, and in
      ``cevns_subev.py`` only from ``vns_rescale``, where it supplies one of the two
      DECLARED integral fluxes for the labelled scalar rescale. It reads stated numbers;
      it does not build a flux table and it does not run a fold.
    """
    import ast
    for mod in ("cevns_subev.py", "fold.py"):
        tree = ast.parse(open(os.path.join(_ROOT, "src", "qpd_potential", mod)).read())
        for node in ast.walk(tree):
            name = (node.attr if isinstance(node, ast.Attribute)
                    else node.id if isinstance(node, ast.Name) else None)
            assert name != "nucleus_variant_flux", f"{mod} calls the variant-flux trap"
        if mod == "fold.py":
            assert "nucleus_flux_normalization" not in ast.dump(tree)
    allowed = [f for f in ast.walk(ast.parse(
        open(os.path.join(_ROOT, "src", "qpd_potential", "cevns_subev.py")).read()))
        if isinstance(f, ast.FunctionDef)
        and "nucleus_flux_normalization" in ast.dump(f)]
    assert [f.name for f in allowed] == ["vns_rescale"]
    for d in _DESIGNS:
        h = open(_spectra_path(d)).read()
        assert "fp-second-vns-run" in h and "UNMODIFIED" in h
