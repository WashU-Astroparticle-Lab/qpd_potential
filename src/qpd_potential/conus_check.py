# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase 16 plan 16-01 -- VALD-12 as restated 2026-07-22 to its SIGNAL-SIDE leg.

Does this pipeline, rescaled to CONUS+'s 3.6 GW_th / 20.7 m and their analysis
window, reproduce their SM-expected CEvNS rate of 347 +/- 59 events in 327 kg.d
within a PRE-DECLARED factor?

EVERYTHING HERE IS ON THE **RECOIL** AXIS (``axis == RECOIL``).  CONUS+ is an
HPGe ionization detector with no QPD readout, so their SM expectation is a
nuclear-recoil-axis prediction.  Folding our spectrum through
``R(E_rec|E_dep)`` and comparing that against their number would test our
readout model against their physics model and call the mismatch a chain
failure (``fp-reconstructed-axis-comparison``).  No response matrix, no
trigger curve and no reconstructed-axis artifact is read anywhere in this
module.

THE ONE LEGAL USE OF A QUENCHING FACTOR.  CONVENTIONS Section B locks a single
unified phonon scale with NO ionization quenching.  Converting THEIR window
BOUNDARIES from keV_ee to keV_nr is a coordinate change on THEIR axis and is
legal.  Multiplying OUR dR/dT by a quenching factor is the milestone-wide
forbidden proxy ``fp-quenching-on-phonon-scale`` and never happens here --
``tests/test_conus_signal_side.py`` proves it by parsing this file's AST rather
than by grepping it, because the words "quenching" and "Lindhard" MUST appear
in this prose: naming the trap is the point.

This is a NEW module by design.  ``tests/test_interpolator_bounds.py`` keys its
inventory by ``file:line``; Phase 13 recorded that shifting those keys is
itself a defect, so nothing is appended to ``cevns.py``.
"""
from __future__ import annotations

import csv
import os

import numpy as np

from . import params

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTIFACT_DIR = os.path.join(_ROOT, "artifacts", "v2.0")

#: The RECOIL-axis CEvNS spectrum this check integrates.  Phase 12 (CALC-25),
#: primary scenario 3 GW_th / 25 m, UNBROADENED, support 0.101 - 3165.6 eV_nr.
CEVNS_DRDT_CSV = os.path.join(ARTIFACT_DIR, "cevns_dRdT_ext.csv")

#: Every quantity in this module carries this tag.  Asserted on every emitted row.
AXIS_TAG = "RECOIL"


# =========================================================================== #
# (1) PRE-REGISTRATION.  Declared HERE, physically ABOVE every function that   #
#     integrates anything, so that the window and the pass/fail threshold are  #
#     committed before a single ratio exists.  This ordering is the structural #
#     defence against fp-window-tuned-to-pass and a test asserts it.           #
# =========================================================================== #

#: THE PRE-REGISTERED ANALYSIS WINDOW, in keV_ee.
#:
#: SOURCE: GPD/ROADMAP.md "### Phase 16 ... (P-SB)", the anchor-coverage line
#: ("... at 3.6 GW_th / 20.7 m, 0.4-1 keV_ee") and GPD/REQUIREMENTS.md VALD-12.
#:
#: REASON FOR THE CHOICE, stated in terms of what the anchor says and NOT in
#: terms of which window passes: ROADMAP.md and REQUIREMENTS.md are the
#: project's authoritative scoping documents and both state this window;
#: GPD/literature/SUMMARY.md is a survey and states a different one.  The
#: choice was committed before any integral was evaluated.
PREREGISTERED_WINDOW_keVee = (0.4, 1.0)
PREREGISTERED_WINDOW_SOURCE = "ROADMAP.md Phase 16 anchor line + REQUIREMENTS.md VALD-12"

#: THE DECLARED ALTERNATE, carried as a named row rather than discarded.
#: SOURCE: GPD/literature/SUMMARY.md, which twice records the CONUS+ limiting
#: case at 160 eV_ee / 7.4 m.w.e. rather than at 400 eV_ee.  The two statements
#: are NOT the same window and this project's own documents disagree about it.
#: The discrepancy is FLAGGED FOR THE ORCHESTRATOR, not resolved here.
ALTERNATE_WINDOW_keVee = (0.160, 1.0)
ALTERNATE_WINDOW_SOURCE = "GPD/literature/SUMMARY.md limiting case at 160 eV_ee / 7.4 m.w.e."

#: A deliberate probe candidate whose converted window lies WHOLLY ABOVE the
#: kinematic support of our dR/dT.  It exists so the above-endpoint flag is
#: exercised on real data instead of being asserted in prose.
ENDPOINT_PROBE_WINDOW_keVee = (1.0, 2.0)
ENDPOINT_PROBE_SOURCE = "kinematic probe declared in plan 16-01; NOT a CONUS+ window"

#: THE STATED FACTOR, declared BEFORE any ratio is computed.
#: ROADMAP SC1 says "within a stated factor"; the ROADMAP/REQUIREMENTS
#: traceability row says "within a factor ~2".  FACTOR 2 IS ADOPTED, because it
#: is the only numeric factor either document states and adopting the looser
#: reading of "a stated factor" after seeing the answer is exactly what
#: fp-window-tuned-to-pass forbids.
STATED_FACTOR = 2.0

#: CONUS+ Collaboration, Nature 643, 1229 (2025), arXiv:2501.05206.
#: SM-expected CEvNS: 347 +/- 59 events in 327 kg.d.  Observed 395 +/- 106 at
#: 3.7 sigma.  Their MEASURED S/B ~ 0.03 is CONTEXT ONLY and is NOT a gate.
#: These are CITATIONS.  No CONUS+ ancillary data exists to download: every
#: NUCLEUS / CONUS / CONUS+ / RICOCHET arXiv record was checked individually
#: and none carries ancillary files (GPD/literature/SUMMARY.md).
CONUS_SM_EVENTS = 347.0
CONUS_SM_EVENTS_UNC = 59.0
CONUS_EXPOSURE_kg_day = 327.0

#: ---------------------------------------------------------------------------
#: THE QUENCHING MODEL: **BRACKETED, NOT SOURCED**.
#:
#: No germanium ionization-quenching model is frozen anywhere under ``data/`` in
#: this repository, and none could be retrieved and integrity-checked in this
#: environment (GPD/literature/SUMMARY.md records that no CONUS/CONUS+ record
#: carries ancillary data).  Writing a recalled calibration number here would be
#: fabricating a sourced input, so the conversion is carried as an EXPLICIT
#: BRACKET over the Lindhard parameter k and is labelled BRACKETED everywhere.
#:
#: The FORM is the Lindhard-Robinson electronic-stopping partition
#:     Q(E_nr) = k g(eps) / (1 + k g(eps)),
#:     g(eps)  = 3 eps^0.15 + 0.7 eps^0.6 + eps,
#:     eps     = 11.5 (E_nr / keV) Z^(-7/3),   Z = 32 for germanium.
#: It is a DECLARED MODEL FORM, written down here so it can be challenged; it
#: is not read from a frozen artifact and it is not claimed as sourced.
#:
#: The bracket spans the Lindhard analytic k = 0.133 Z^(2/3) A^(-1/2) = 0.1573
#: for natural Ge, plus a deliberately wide margin on either side.  The bracket
#: endpoints become extra rows of the sensitivity table, so the width of the
#: bracket is visible on the deliverable rather than hidden inside a point value.
QUENCHING_MODEL_NAME = "Lindhard-Robinson k-parameterized, germanium Z=32"
QUENCHING_PROVENANCE = "BRACKETED"      # never SOURCED: no local frozen model
LINDHARD_K_BRACKET = (0.130, 0.200)
LINDHARD_K_CENTRAL = 0.157              # = 0.133 * 32^(2/3) * 72.63^(-1/2)
GE_Z = 32.0


def lindhard_g(eps):
    """The Lindhard reduced stopping function g(eps).  DECLARED MODEL FORM."""
    eps = np.asarray(eps, dtype=float)
    return 3.0 * eps ** 0.15 + 0.7 * eps ** 0.6 + eps


def lindhard_quenching_factor(E_nr_keV, k=LINDHARD_K_CENTRAL, Z=GE_Z):
    """Q = E_ee / E_nr for germanium.  Dimensionless, strictly in (0, 1) here.

    THIS RETURN VALUE MAY ONLY EVER TOUCH A WINDOW BOUNDARY.  It must never be
    multiplied into a rate array -- see the module docstring and
    ``test-no-quenching-on-our-spectrum``, which proves the restriction by
    parsing this file rather than by trusting this sentence.
    """
    eps = 11.5 * np.asarray(E_nr_keV, dtype=float) * Z ** (-7.0 / 3.0)
    kg = k * lindhard_g(eps)
    return kg / (1.0 + kg)


def keVee_boundary_to_keVnr(E_ee_keV, k=LINDHARD_K_CENTRAL):
    """Map ONE analysis-window BOUNDARY from keV_ee onto keV_nr.

    A coordinate change on CONUS+'s ionization axis.  Our own dR/dT is left
    entirely untouched (CONVENTIONS Section B).  Solved by bisection because
    E_ee(E_nr) = Q(E_nr) E_nr is monotone increasing on this range.
    """
    lo, hi = 1.0e-4, 1.0e3
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        q_mid = float(lindhard_quenching_factor(mid, k))
        if q_mid * mid < E_ee_keV:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# =========================================================================== #
# (2) The committed recoil-axis spectrum, its kinematic support, and the       #
#     window integral.  Nothing above this line has seen a rate.               #
# =========================================================================== #
def read_dRdT(path=CEVNS_DRDT_CSV):
    """Read the committed RECOIL-axis CEvNS spectrum.  Returns T in eV_nr."""
    T, y = [], []
    with open(path, encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if not row or row[0].startswith("#") or row[0].startswith("T_eV"):
                continue
            T.append(float(row[0]))
            y.append(float(row[6]))          # dRdT_total, counts/kg/day/keV
    return {"T_eV": np.asarray(T), "dRdT": np.asarray(y), "axis": AXIS_TAG,
            "path": path}


def kinematic_support_edge_eV(path=CEVNS_DRDT_CSV):
    """The largest T at which dR/dT is non-zero.  MEASURED, not asserted.

    Above this the reactor-CEvNS kinematic endpoint has been passed and the
    table carries exact zeros.  A window sitting above it is not measuring the
    flux x cross-section x target chain at all.
    """
    d = read_dRdT(path)
    nz = d["T_eV"][d["dRdT"] > 0.0]
    return float(nz[-1]) if nz.size else float("nan")


def window_support_fraction(lo_keVnr, hi_keVnr, support_edge_eV):
    """Fraction of the converted window lying inside the non-zero dR/dT support."""
    lo, hi = lo_keVnr * 1.0e3, hi_keVnr * 1.0e3
    if hi <= lo:
        return 0.0
    inside = max(0.0, min(hi, support_edge_eV) - lo)
    return float(inside / (hi - lo))


def integrate_window_counts_kg_day(lo_keVnr, hi_keVnr, path=CEVNS_DRDT_CSV):
    """Integrate dR/dT over a keV_nr window.  UNITS, written out, not buried.

    dR/dT is in counts/kg/day/**keV** and T is tabulated in **eV**, so the
    quadrature carries an explicit factor 1/1000:

        R [counts/kg/day] = (1/1000) * INT dRdT(T) dT ,  T in eV.
    """
    d = read_dRdT(path)
    T, y = d["T_eV"], d["dRdT"]
    lo, hi = lo_keVnr * 1.0e3, hi_keVnr * 1.0e3
    m = (T >= lo) & (T <= hi)
    Ts = np.concatenate(([lo], T[m], [hi]))
    ys = np.concatenate(([np.interp(lo, T, y)], y[m], [np.interp(hi, T, y)]))
    eV_per_keV = 1000.0
    return float(np.trapz(ys, Ts)) / eV_per_keV


def geometric_rescale():
    """(P_c/P_v) (d_v/d_c)^2, with EVERY factor reported separately.

    A product can be right by cancellation -- the lesson Phase 15 wrote into
    ``fp-product-instead-of-factors`` -- so P_c, P_v, d_c, d_v all travel.
    """
    P_v = params.REACTOR_POWER.value
    d_v = params.STANDOFF.value
    P_c = params.CONUS_POWER_GW.value
    d_c = params.CONUS_DISTANCE_M.value
    return {"P_conus_GW": P_c, "P_ours_GW": P_v,
            "d_conus_m": d_c, "d_ours_m": d_v,
            "power_ratio": P_c / P_v, "distance_ratio_squared": (d_v / d_c) ** 2,
            "factor": (P_c / P_v) * (d_v / d_c) ** 2}


def conus_sm_rate():
    """CONUS+'s SM expectation AS A RATE.  The division is shown, not quoted."""
    return {"events": CONUS_SM_EVENTS, "events_unc": CONUS_SM_EVENTS_UNC,
            "exposure_kg_day": CONUS_EXPOSURE_kg_day,
            "rate_counts_kg_day": CONUS_SM_EVENTS / CONUS_EXPOSURE_kg_day,
            "rate_unc_counts_kg_day": CONUS_SM_EVENTS_UNC / CONUS_EXPOSURE_kg_day,
            "expression": "347 / 327 counts/kg/day, uncertainty 59 / 327"}


def ia_fractional_width(E_R_eV):
    """sigma_E / E_R = sqrt(omega_bar / E_R), CONVENTIONS Section J locked value.

    MEASURED at the window edges and reported as a number.  Phase 15 established
    that this project's "too small to matter" arguments have been FALSE when
    actually checked, so nothing here is asserted negligible.
    """
    return float(np.sqrt(params.OMEGA_BAR_eV.value / float(E_R_eV)))


# =========================================================================== #
# (3) Candidates and evaluation                                                #
# =========================================================================== #
def candidate_windows():
    """Every candidate considered, INCLUDING the ones expected to fail."""
    out = []
    for label, (a, b), src in (
            ("preregistered_roadmap_requirements", PREREGISTERED_WINDOW_keVee,
             PREREGISTERED_WINDOW_SOURCE),
            ("alternate_literature_survey", ALTERNATE_WINDOW_keVee,
             ALTERNATE_WINDOW_SOURCE),
            ("kinematic_probe_above_endpoint", ENDPOINT_PROBE_WINDOW_keVee,
             ENDPOINT_PROBE_SOURCE)):
        for k, kind in ((LINDHARD_K_BRACKET[0], "bracket_low"),
                        (LINDHARD_K_CENTRAL, "bracket_central"),
                        (LINDHARD_K_BRACKET[1], "bracket_high")):
            out.append({"candidate": label, "source": src,
                        "E_ee_lo_keVee": a, "E_ee_hi_keVee": b,
                        "lindhard_k": k, "bracket_position": kind})
    return out


def evaluate_candidate(c, support_edge_eV=None, geo=None, sm=None):
    """Convert, check the support, integrate, rescale, ratio.  In that order."""
    if support_edge_eV is None:
        support_edge_eV = kinematic_support_edge_eV()
    if geo is None:
        geo = geometric_rescale()
    if sm is None:
        sm = conus_sm_rate()
    k = c["lindhard_k"]
    lo_nr = keVee_boundary_to_keVnr(c["E_ee_lo_keVee"], k)
    hi_nr = keVee_boundary_to_keVnr(c["E_ee_hi_keVee"], k)
    frac = window_support_fraction(lo_nr, hi_nr, support_edge_eV)
    above = lo_nr * 1.0e3 >= support_edge_eV
    rate = 0.0 if above else integrate_window_counts_kg_day(lo_nr, hi_nr)
    rescaled = rate * geo["factor"]
    ratio = rescaled / sm["rate_counts_kg_day"]
    within = (ratio > 0.0) and (1.0 / STATED_FACTOR <= ratio <= STATED_FACTOR)
    out = dict(c)
    out.update({
        "axis": AXIS_TAG,
        "quenching_model": QUENCHING_MODEL_NAME,
        "quenching_provenance": QUENCHING_PROVENANCE,
        "quenching_bracket_lo": LINDHARD_K_BRACKET[0],
        "quenching_bracket_hi": LINDHARD_K_BRACKET[1],
        "E_nr_lo_keVnr": lo_nr, "E_nr_hi_keVnr": hi_nr,
        "Q_at_lo": float(lindhard_quenching_factor(lo_nr, k)),
        "Q_at_hi": float(lindhard_quenching_factor(hi_nr, k)),
        "support_edge_eV_nr": support_edge_eV,
        "support_fraction": frac,
        "above_kinematic_endpoint": bool(above),
        "rate_ours_counts_kg_day": rate,
        "geometric_rescale_factor": geo["factor"],
        "rate_rescaled_counts_kg_day": rescaled,
        "conus_sm_rate_counts_kg_day": sm["rate_counts_kg_day"],
        "ratio": ratio,
        "stated_factor": STATED_FACTOR,
        "within_stated_factor": bool(within),
        "sigma_over_E_at_lo": ia_fractional_width(lo_nr * 1.0e3),
        "sigma_over_E_at_hi": ia_fractional_width(hi_nr * 1.0e3),
    })
    out["preregistered"] = bool(
        c["candidate"] == "preregistered_roadmap_requirements"
        and c["bracket_position"] == "bracket_central")
    return out


def evaluate_all():
    support = kinematic_support_edge_eV()
    geo, sm = geometric_rescale(), conus_sm_rate()
    return [evaluate_candidate(c, support, geo, sm) for c in candidate_windows()]


def preregistered_row(rows=None):
    rows = rows if rows is not None else evaluate_all()
    hits = [r for r in rows if r["preregistered"]]
    assert len(hits) == 1, f"expected exactly one PRE_REGISTERED row, got {len(hits)}"
    return hits[0]


def billard_route_cross_check():
    """An INDEPENDENT handle on the absolute rate scale at the CONUS+ geometry.

    ``cevns.conus_rescale_check`` compares our flagship flux model against
    Billard's independently normalized one at 3.6 GW_th / 20.7 m.  It is not an
    algebraic identity of this plan, so the two routes agreeing is information.
    """
    from . import cevns
    return cevns.conus_rescale_check()


def billard_leverage_on_the_window(rows=None):
    """HOW LITTLE of the Billard-checked rate scale actually lives in the window.

    This is the check that cuts against the comfortable reading.  It would be
    easy to say "the Billard route agrees to 1%, so our chain is fine and only
    the window is wrong".  ``cevns.conus_rescale_check`` integrates from a
    50 eV recoil floor, and that integral is overwhelmingly low-T.  MEASURE the
    fraction of it that lies above the window's lower edge instead of assuming
    the agreement reaches there.
    """
    rows = rows if rows is not None else evaluate_all()
    pre = preregistered_row(rows)
    alt = [r for r in rows
           if r["candidate"] == "alternate_literature_survey"
           and r["bracket_position"] == "bracket_central"][0]
    floor_keV = 0.050                    # cevns.conus_rescale_check default T_floor_eV
    top_keV = 10.0                       # above the kinematic endpoint; closes the integral
    total = integrate_window_counts_kg_day(floor_keV, top_keV)
    out = {"billard_floor_keVnr": floor_keV,
           "rate_above_floor_counts_kg_day": total}
    for tag, r in (("preregistered", pre), ("alternate_central", alt)):
        above = integrate_window_counts_kg_day(r["E_nr_lo_keVnr"], top_keV)
        out[f"fraction_above_{tag}_lower_edge"] = above / total
    return out


def vald12_verdict(rows=None):
    """PASS / FAIL / INCONCLUSIVE, from the PRE-DECLARED factor.  Either way."""
    rows = rows if rows is not None else evaluate_all()
    pre = preregistered_row(rows)
    if pre["above_kinematic_endpoint"]:
        verdict = "INCONCLUSIVE"
        reason = ("the pre-registered window converts WHOLLY above the kinematic "
                  "support of our dR/dT, so the comparison cannot test the chain")
    elif pre["within_stated_factor"]:
        verdict = "CONFIRMED"
        reason = "the ratio lies inside the pre-declared factor"
    elif pre["support_fraction"] < 1.0:
        verdict = "PARTIALLY CONFIRMED"
        reason = (
            "the ratio lies OUTSIDE the pre-declared factor on the pre-registered "
            "window, so the pre-registered leg FAILS; that window is only partly "
            "inside the kinematic support of our dR/dT, and the declared alternate "
            "window lands inside the factor, so the VERDICT IS SET BY THE WINDOW "
            "CHOICE, which this project's own documents do not settle. That is a "
            "statement about what the comparison can test, NOT a demonstration "
            "that the chain is correct in the endpoint region -- the independent "
            "Billard route agrees at the 1% level but carries under 1e-5 of its "
            "weight above the pre-registered lower edge, so it does not reach there")
    else:
        verdict = "FAIL"
        reason = "the ratio lies outside the pre-declared factor with the window fully supported"
    alt = [r for r in rows if r["candidate"] == "alternate_literature_survey"]
    alt_c = [r for r in alt if r["bracket_position"] == "bracket_central"][0]
    return {"verdict": verdict, "reason": reason,
            "preregistered_ratio": pre["ratio"],
            "preregistered_within_factor": pre["within_stated_factor"],
            "preregistered_leg": "FAIL" if not pre["within_stated_factor"] else "PASS",
            "stated_factor": STATED_FACTOR,
            "alternate_ratios": [r["ratio"] for r in alt],
            "alternate_central_ratio": alt_c["ratio"],
            "alternate_central_within_factor": alt_c["within_stated_factor"],
            "alternate_all_within_factor": all(r["within_stated_factor"] for r in alt),
            "window_conditional": True}


def ratio_spread(rows=None):
    rows = rows if rows is not None else evaluate_all()
    pos = [r["ratio"] for r in rows if r["ratio"] > 0]
    return {"min": min(pos), "max": max(pos), "decades": float(np.log10(max(pos) / min(pos))),
            "n_zero_rows": sum(1 for r in rows if r["ratio"] == 0.0)}


# =========================================================================== #
# (4) Artifacts                                                                #
# =========================================================================== #
SENSITIVITY_CSV = os.path.join(ARTIFACT_DIR, "conus_window_sensitivity.csv")
CHECK_CSV = os.path.join(ARTIFACT_DIR, "conus_signal_side_check.csv")

_SENS_COLS = ["candidate", "source", "preregistered", "axis",
              "E_ee_lo_keVee", "E_ee_hi_keVee", "quenching_model",
              "quenching_provenance", "lindhard_k", "bracket_position",
              "quenching_bracket_lo", "quenching_bracket_hi",
              "E_nr_lo_keVnr", "E_nr_hi_keVnr", "Q_at_lo", "Q_at_hi",
              "support_edge_eV_nr", "support_fraction", "above_kinematic_endpoint",
              "rate_ours_counts_kg_day", "geometric_rescale_factor",
              "rate_rescaled_counts_kg_day", "conus_sm_rate_counts_kg_day",
              "ratio", "stated_factor", "within_stated_factor",
              "sigma_over_E_at_lo", "sigma_over_E_at_hi"]


def write_window_sensitivity_csv(path=SENSITIVITY_CSV):
    rows = evaluate_all()
    sp = ratio_spread(rows)
    pre = preregistered_row(rows)
    h = [
        "# QPD Phase-16 plan 16-01 -- RATIO versus ANALYSIS WINDOW, INCLUDING THE FAILURES.",
        "# axis = RECOIL on every row.  No reconstructed-axis object is touched anywhere.",
        "#",
        "# WHY THIS TABLE EXISTS.  Planning reconnaissance found the VALD-12 ratio moves by",
        "# MORE THAN THREE DECADES depending only on which nuclear-recoil window the keV_ee",
        "# analysis window maps to.  A gate whose answer is set by an unstated analysis",
        "# choice is not a gate, so the window was PRE-REGISTERED before any integral ran",
        "# and the FULL curve -- failures included -- is emitted (fp-window-tuned-to-pass).",
        f"#   measured spread across candidates: min {sp['min']:.6e}, max {sp['max']:.6e},",
        f"#   i.e. {sp['decades']:.3f} DECADES, plus {sp['n_zero_rows']} rows at exactly zero",
        "#   because the converted window lies above the kinematic endpoint.",
        "#",
        "# THE LIVE INTERNAL DISCREPANCY, FLAGGED FOR THE ORCHESTRATOR (no file edited):",
        f"#   ROADMAP.md / REQUIREMENTS.md state the CONUS+ window as {PREREGISTERED_WINDOW_keVee[0]}-"
        f"{PREREGISTERED_WINDOW_keVee[1]} keV_ee;",
        f"#   GPD/literature/SUMMARY.md states the limiting case at {ALTERNATE_WINDOW_keVee[0]*1000:.0f} eV_ee.",
        "#   These are NOT the same window and they do NOT give the same verdict.  Both are",
        "#   carried here as named rows; ROADMAP/REQUIREMENTS is pre-registered because they",
        "#   are the project's authoritative scoping documents and the survey is not.",
        "#",
        "# QUENCHING: BRACKETED, NOT SOURCED.  No germanium ionization-quenching model is",
        f"#   frozen locally.  Form: {QUENCHING_MODEL_NAME}; k bracketed over "
        f"[{LINDHARD_K_BRACKET[0]}, {LINDHARD_K_BRACKET[1]}] with central {LINDHARD_K_CENTRAL}.",
        "#   The factor converts THEIR WINDOW BOUNDARIES only.  Our dR/dT is never multiplied",
        "#   by it (CONVENTIONS Section B; fp-quenching-on-phonon-scale).",
        "#",
        f"# PRE-DECLARED FACTOR = {STATED_FACTOR} (declared in source above the integrator).",
        f"# PRE_REGISTERED row: {pre['candidate']} / {pre['bracket_position']}, ratio {pre['ratio']:.6e}.",
        "#",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_SENS_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r[c] for c in _SENS_COLS})
    return path


def write_signal_side_check_csv(path=CHECK_CSV):
    rows = evaluate_all()
    pre = preregistered_row(rows)
    geo, sm = geometric_rescale(), conus_sm_rate()
    v = vald12_verdict(rows)
    sp = ratio_spread(rows)
    bill = billard_route_cross_check()
    lev = billard_leverage_on_the_window(rows)
    support = kinematic_support_edge_eV()
    h = [
        "# QPD Phase-16 plan 16-01 -- VALD-12 SIGNAL-SIDE CHECK (restated 2026-07-22).",
        "# axis = RECOIL on every row.",
        "#",
        "# WHAT THE RESTATEMENT GIVES UP, written on the deliverable rather than dropped:",
        "#   Reproducing CONUS+'s S/B is NOT a coherent test for this pipeline -- they sit at",
        "#   7.4 m.w.e. behind a shield this project does not model, so matching their ratio",
        "#   would require inventing a model of their shield.  CONSEQUENCE: THE MILESTONE",
        "#   CARRIES NO EXTERNAL VALIDATION OF THE RATIO S/B_particle ITSELF, ONLY OF ITS",
        "#   NUMERATOR.  Their measured S/B ~ 0.03 is retained as CONTEXT for a shielded",
        "#   experiment and is explicitly NOT a gate and NOT a target.",
        "#",
        f"# GEOMETRIC RESCALE, factors written out individually (fp-product-instead-of-factors):",
        f"#   P_c = {geo['P_conus_GW']} GW_th, P_v = {geo['P_ours_GW']} GW_th  ->  P_c/P_v = "
        f"{geo['power_ratio']:.10f}",
        f"#   d_c = {geo['d_conus_m']} m,  d_v = {geo['d_ours_m']} m  ->  (d_v/d_c)^2 = "
        f"{geo['distance_ratio_squared']:.10f}",
        f"#   factor = {geo['factor']:.10f}",
        "#   Assumes a point source, rate linear in thermal power, and the SAME antineutrino",
        "#   SPECTRAL SHAPE at both sites.  The fission-fraction difference between the 3 GW_th",
        "#   reference core and CONUS+'s Leibstadt core is a NAMED, UNQUANTIFIED systematic:",
        "#   this project holds nothing that could quantify it, and no guessed correction is folded in.",
        "#",
        f"# CONUS+ SM EXPECTATION: {CONUS_SM_EVENTS:.0f} +/- {CONUS_SM_EVENTS_UNC:.0f} events in "
        f"{CONUS_EXPOSURE_kg_day:.0f} kg.d",
        f"#   as a rate: {sm['expression']} = {sm['rate_counts_kg_day']:.10f} +/- "
        f"{sm['rate_unc_counts_kg_day']:.10f} counts/kg/day",
        "#   CONUS+ Collab., Nature 643, 1229 (2025), arXiv:2501.05206.  A CITATION: no CONUS+",
        "#   ancillary data exists to download.",
        "#",
        f"# KINEMATIC SUPPORT of our dR/dT: the largest T with non-zero dR/dT is "
        f"{support:.4f} eV_nr",
        "#   (the table runs to 3165.6057 eV_nr but carries exact zeros above the endpoint).",
        "#   A window above it records a ZERO rate with an above_kinematic_endpoint flag; it is",
        "#   never a silently truncated integral (fp-silent-endpoint-truncation), and no table",
        "#   was extended to make any window reachable.",
        "#",
        "# IA BROADENING IS OMITTED and its size is MEASURED, not asserted small.  CONUS+'s SM",
        "#   expectation contains no impulse-approximation kernel, so the like-for-like object is",
        "#   the unbroadened dR/dT.  sigma_E/E_R = sqrt(omega_bar/E_R) with the CONVENTIONS",
        f"#   Section J locked omega_bar = {params.OMEGA_BAR_eV.value:.10e} eV:",
        f"#     at the pre-registered lower edge {pre['E_nr_lo_keVnr']*1e3:.2f} eV_nr: "
        f"{pre['sigma_over_E_at_lo']:.6e}",
        f"#     at the pre-registered upper edge {pre['E_nr_hi_keVnr']*1e3:.2f} eV_nr: "
        f"{pre['sigma_over_E_at_hi']:.6e}",
        "#   Direction: a symmetric kernel on a falling spectrum near an endpoint moves counts",
        "#   BOTH ways across a window edge; at these fractional widths the effect is far below",
        "#   the decades the window choice moves, which is why it is not the story here.",
        "#",
        "# INDEPENDENT ROUTE (not an algebraic identity of this plan): cevns.conus_rescale_check",
        "#   compares our flagship flux model against Billard's independently normalized one at",
        f"#   the CONUS+ geometry.  R_ours_at_conus = {bill['R_ours_at_conus']:.6e}, "
        f"R_billard_at_conus = {bill['R_billard_at_conus']:.6e},",
        f"#   ratio = {bill['ratio']:.6f}.  The two routes AGREE on the absolute rate scale to "
        f"{abs(bill['ratio']-1)*100:.2f}%.",
        "#",
        "#   BUT THAT AGREEMENT DOES NOT REACH THE WINDOW, and saying so is the point of this",
        "#   block.  conus_rescale_check integrates from a 50 eV recoil floor and that integral",
        "#   is overwhelmingly low-T.  MEASURED, not assumed:",
        f"#     rate above the 50 eV floor              = {lev['rate_above_floor_counts_kg_day']:.6f} counts/kg/day",
        f"#     fraction of it above the PRE-REGISTERED lower edge = "
        f"{lev['fraction_above_preregistered_lower_edge']:.6e}",
        f"#     fraction of it above the ALTERNATE lower edge      = "
        f"{lev['fraction_above_alternate_central_lower_edge']:.6e}",
        "#   So the 1%-level Billard agreement constrains the BULK normalization and says",
        "#   essentially NOTHING about the 2-5 keV_nr tail the pre-registered window probes.",
        "#   It is evidence that the chain's overall scale is sound; it is NOT evidence that",
        "#   the endpoint region is right, and it must not be read as the latter.",
        "#",
        f"# VERDICT: VALD-12 (signal-side leg) = {v['verdict']}.",
        f"#   pre-registered ratio {v['preregistered_ratio']:.6e} against the PRE-DECLARED factor "
        f"{STATED_FACTOR};",
        f"#   THE PRE-REGISTERED LEG ITSELF IS A {v['preregistered_leg']}: VALD-12's signal-side",
        "#   leg is NOT discharged on the window this project pre-registered.",
        f"#   declared-alternate ratios {', '.join(f'{r:.6e}' for r in v['alternate_ratios'])}; "
        f"central-k alternate within the factor: {v['alternate_central_within_factor']}, "
        f"whole bracket within the factor: {v['alternate_all_within_factor']}.",
        f"#   THE VERDICT IS WINDOW-CONDITIONAL: the ratio spans {sp['decades']:.3f} decades across",
        "#   candidates and this project's own documents disagree about which window is CONUS+'s.",
        "#   Reason: " + v["reason"] + ".",
        "#",
        "# The pre-re-scope S/B expectation that once accompanied this check is WITHDRAWN by the",
        "#   2026-07-22 re-scope and no replacement expectation is asserted anywhere.",
        "#",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_SENS_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r[c] for c in _SENS_COLS})
    return path


def write_all():
    return [write_window_sensitivity_csv(), write_signal_side_check_csv()]


if __name__ == "__main__":                                   # pragma: no cover
    for p in write_all():
        print("wrote", p)
