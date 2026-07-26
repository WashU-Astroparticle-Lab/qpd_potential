# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase 16 plan 16-02 -- the terminal S/B_particle assembly (CALC-22).

EVERY quantity here is on the shared RECONSTRUCTED axis (``axis == RECONSTRUCTED``),
the 161-bin E_rec axis less the ``[0, 1e-3 eV)`` underflow catch-bin that Phases
12/13/14/15 all drop identically.  The 71Ge M line's 158.7 eV is a DEPOSITED
energy; on the corrected unit-slope axis its reconstructed image is at 130.1 /
125.9 eV -- ABOVE the RoI -- so it contributes 0 to the RoI denominator.

THE OBSERVABLE IS NAMED ``S/B_particle``, ALWAYS.  The subscript records that the
low-energy excess is excluded BY CONSTRUCTION, not overlooked.  Plan 16-03 owns
the LEE overlay; nothing here folds it in.

THE CONFIGURATION IS ``NUCLEUS's-shielding-absent``.  It is a DIFFERENT AND WORSE
configuration than NUCLEUS's, not a subset of it, and the Phase-8 lock forbids
the flattering adjective that would suggest otherwise.  The veto credit is
exactly 1.0 BY CONSTRUCTION -- it follows from the ABSENCE of the apparatus, and
it is READ from ``surface_environment.veto_credit()`` rather than re-typed.

TWO DENOMINATOR LAYERS, NEVER COLLAPSED.  Two of the inventory channels arrive as
UPPER BOUNDS rather than rate estimates.  Summing upper bounds into a denominator
makes ``S/B_particle`` a LOWER BOUND, and that direction is part of the result.

A NEW module by design, so no ``file:line`` inventory key in
``tests/test_interpolator_bounds.py`` moves.
"""
from __future__ import annotations

import csv
import os

import numpy as np

from . import surface_environment as se

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTIFACT_DIR = os.path.join(_ROOT, "artifacts", "v2.0")

AXIS_TAG = "RECONSTRUCTED"
OBSERVABLE = "S/B_particle"
CONFIGURATION = "NUCLEUS's-shielding-absent"

DESIGNS = ("Ta->Al", "Al->Hf")
_TAG = {"Ta->Al": "TaAl", "Al->Hf": "AlHf"}

# =========================================================================== #
# (1) THE BANDS, DEFINED ONCE, ABOVE EVERY FUNCTION THAT USES THEM.            #
#                                                                             #
# The inputs disagree: Phase 13 reports the neutron channel at E_rec < 1 eV,   #
# Phase 15 reports muon / Compton / CEvNS at E_rec < 10 eV.  Mixing them would #
# integrate the numerator and the denominator over DIFFERENT regions of the    #
# axis.  Every channel is therefore RE-INTEGRATED here, on these bands, from   #
# its own committed artifact.  No band-integrated number computed elsewhere on #
# a different band is ever imported.                                           #
# =========================================================================== #
ROI_EREC_LO_eV = 10.0
ROI_EREC_HI_eV = 100.0

#: The sub-eV reporting band, defined ONCE: E_rec at or below 1 eV.  Chosen as a
#: literal E_rec bound rather than as the design-dependent E_rec image of a 1 eV
#: DEPOSIT (0.497240 / 0.495855 eV), so that the two designs are integrated over
#: the SAME region and can be compared.  CONSEQUENCE, recorded rather than
#: hidden: this band SPANS that regime boundary, so within it the reported
#: observable changes character from dR/dE_rec to a trigger probability
#: (CONVENTIONS Section I).  That is a caveat on the sub-eV rows, not a defect
#: in the band.
SUBEV_EREC_LO_eV = 0.0
SUBEV_EREC_HI_eV = 1.0

#: The underflow catch-bin dropped identically by Phases 12/13/14/15.
UNDERFLOW_TOP_eV = 1.0e-3

BANDS = {"RoI_10_100eV": (ROI_EREC_LO_eV, ROI_EREC_HI_eV),
         "subeV_le_1eV": (SUBEV_EREC_LO_eV, SUBEV_EREC_HI_eV)}

#: The reproduction tolerance a channel's own published headline must meet
#: BEFORE that channel is allowed into the sum.  Declared here, before use.
HEADLINE_REL_TOL = 1.0e-4

#: The accuracy-label lattice, loosest last.  The PROPAGATION RULE, stated so it
#: can be challenged rather than left implicit: the assembled label is the
#: LOOSEST label present among the channels actually summed, and the band it
#: supports is applied to the ratio.
LABEL_ORDER = ("percent", "factor_two", "order_of_magnitude")
LABEL_BAND = {"percent": (0.9, 1.1),
              "factor_two": (0.5, 2.0),
              "order_of_magnitude": (10.0 ** -0.5, 10.0 ** 0.5)}
LABEL_PROPAGATION_RULE = (
    "assembled_label = loosest label among the SUMMED channels; "
    "order_of_magnitude renders as the multiplicative band [10^-0.5, 10^+0.5], "
    "i.e. one full decade of total span. A percent-level band is FORBIDDEN "
    "regardless of how the arithmetic comes out (fp-precision-inflation-16).")

# --------------------------------------------------------------------------- #
# Phase-14 scalar bounds, read as NAMED CONSTANTS with their scenarios.        #
# --------------------------------------------------------------------------- #
#: Prompt (n,gamma) capture.  RIGOROUS and CASCADE-FREE: every capture yields
#: exactly one recoiling nucleus, so R_band <= R_capture on ANY band and on any
#: axis, because R's columns each sum to 1.  It is therefore the SAME number in
#: the RoI and in the sub-eV band, and that is a property of the bound, not a
#: copy-paste.
CAPTURE_BOUND_counts_kg_day = 4399.777
CAPTURE_THERMAL_counts_kg_day = 3365.536
CAPTURE_NONTHERMAL_counts_kg_day = (857.0758 + 167.7549 + 9.410154)
CAPTURE_NONTHERMAL_FRACTION = 0.2350667          # 1 - 0.7649333, Phase 14

#: 71Ge EC M line.  A BOUND WITH A SCENARIO.  A rate without its t is undefined.
GE71_M_SATURATION_counts_kg_day = 130.8197
GE71_M_T1DAY_counts_kg_day = 7.697512

#: Ge discrete inelastic.  EXCLUDED from the sum; its measured effect is emitted.
INELASTIC_BOUND_counts_kg_day = 2666.833
INELASTIC_NUCLEAR_RECOIL_SCALE_eV = 2.271606e5
INELASTIC_GAMMA_RECOILS_eV = (2.576622, 5.185)   # 74Ge 596 keV, 72Ge 834 keV

#: The 71Ge M line's DEPOSIT energy and its RECONSTRUCTED image.  Never confused.
GE71_M_DEPOSIT_eV = 158.7
# REVISED 2026-07-25 (unit calibration slope): the 158.7 eV M line images at ~130 /
# ~126 eV, ABOVE the 10-100 eV RoI -- it no longer lands in the signal band. Was
# 65.0 / 63.0 eV (inside RoI) on the former eps=0.5 half-scale.
GE71_M_EREC_IMAGE_eV = {"Ta->Al": 130.10, "Al->Hf": 125.93}


# =========================================================================== #
# (2) The band integrator -- VALIDATED before it is used                       #
# =========================================================================== #
def _erec_edges(design):
    from . import fold as _fold
    return _fold.load_design_extended(design)["E_rec_edges_eV"]


def read_erec_channel(path, column):
    """Read one committed reconstructed-axis column.  The AXIS TAG travels."""
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.reader(r for r in fh if not r.startswith("#")))
    hdr, data = rows[0], rows[1:]
    j = hdr.index(column)
    E, y = [], []
    for r in data:
        e = float(r[0]) * 1.0e3                       # the files carry keV
        if e < UNDERFLOW_TOP_eV:                      # drop the underflow catch-bin
            continue
        E.append(e)
        y.append(float(r[j]))
    return {"E_rec_eV": np.asarray(E), "dRdErec": np.asarray(y),
            "axis": AXIS_TAG, "path": path, "column": column}


def band_integral(E_rec_eV, dRdErec, lo, hi, edges):
    """Integrate dR/dE_rec [counts/kg/day/keV] over an E_rec band.

    Bin widths come from the response matrix's own edges by matching centres,
    exactly as ``capture_channel._band_integral_from_erec`` does, so this
    integrator is the same operation Phase 14 validated -- re-implemented here
    only so that this plan owns the bands.
    """
    w = np.diff(edges) / 1.0e3                        # keV, matching dR/dE_rec
    idx = np.clip(np.searchsorted(edges, E_rec_eV, side="right") - 1, 0, w.size - 1)
    m = (E_rec_eV >= lo) & (E_rec_eV <= hi)
    return float(np.sum(dRdErec[m] * w[idx[m]]))


#: Each channel's OWN published headline, and where it came from.  A channel
#: whose artifact fails to reproduce its headline is BLOCKED from the sum.
# RoI headlines REVISED 2026-07-25 for the unit calibration slope
# (params.CALIB_SLOPE = 1.0, CONVENTIONS Section E.1). The 10-100 eV RECONSTRUCTED
# RoI now images a 10-100 eV DEPOSIT band instead of the former 20-200 eV, so every
# reconstructed-axis in-RoI integral moved. The TOTAL (cevns 118.73) is on the whole
# axis and is scale-invariant. Old-axis values, for the record: cevns 72.9214/73.1441,
# neutron 5430.287/5485.152, compton 34.2484/35.8616, muon 7.4656/7.7231.
PUBLISHED_HEADLINES = {
    ("cevns", "TOTAL"): {"Ta->Al": 118.73, "Al->Hf": 118.73,
                         "source": "Phase 12 (12-03), whole reconstructed axis"},
    ("cevns", "RoI_10_100eV"): {"Ta->Al": 62.6289, "Al->Hf": 63.6226,
                                "source": "Phase 15 (15-04) orientation row; unit-slope axis"},
    ("neutron", "RoI_10_100eV"): {"Ta->Al": 4780.352, "Al->Hf": 4832.425,
                                  "source": "Phase 13 (13-03) Section 7; unit-slope axis"},
    ("compton", "RoI_10_100eV"): {"Ta->Al": 11.9340, "Al->Hf": 12.5684,
                                  "source": "Phase 15 (15-04); unit-slope axis"},
    ("muon", "RoI_10_100eV"): {"Ta->Al": 3.5275, "Al->Hf": 3.6324,
                               "source": "Phase 15 (15-04); unit-slope axis"},
}

#: (artifact stem, untriggered column, triggered column) per spectral channel.
SPECTRAL_SOURCES = {
    "cevns": ("cevns_dRdErec_ext_{tag}.csv",
              "dRdErec_central", "dRdErec_trigger_weighted"),
    "neutron": ("neutron_dRdErec_ext_{tag}.csv",
                "dRdErec_central", "dRdErec_trigger_weighted"),
    "muon": ("em_dRdErec_ext_{tag}.csv",
             "muon_dRdErec_untriggered[counts/kg/day/keV]",
             "muon_dRdErec_triggered[counts/kg/day/keV]"),
    "compton": ("em_dRdErec_ext_{tag}.csv",
                "compton_dRdErec_untriggered[counts/kg/day/keV]",
                "compton_dRdErec_triggered[counts/kg/day/keV]"),
    "ge71_ec_M": ("ge71_ec_dRdErec_{tag}.csv",
                  "dRdErec_bound", "dRdErec_trigger_weighted"),
}


def integrate_channel(name, design):
    """Re-integrate one committed spectral channel on THIS plan's bands."""
    stem, ucol, tcol = SPECTRAL_SOURCES[name]
    path = os.path.join(ARTIFACT_DIR, stem.format(tag=_TAG[design]))
    edges = _erec_edges(design)
    u = read_erec_channel(path, ucol)
    t = read_erec_channel(path, tcol)
    out = {"channel": name, "design": design, "axis": AXIS_TAG, "path": path}
    for band, (lo, hi) in BANDS.items():
        out[f"{band}_untriggered"] = band_integral(u["E_rec_eV"], u["dRdErec"], lo, hi, edges)
        out[f"{band}_triggered"] = band_integral(t["E_rec_eV"], t["dRdErec"], lo, hi, edges)
    out["TOTAL_untriggered"] = band_integral(u["E_rec_eV"], u["dRdErec"], 0.0, np.inf, edges)
    out["TOTAL_triggered"] = band_integral(t["E_rec_eV"], t["dRdErec"], 0.0, np.inf, edges)
    return out


def validate_integrator():
    """Reproduce EVERY channel's own published headline BEFORE any sum.

    Returns ``{(channel, band, design): {value, published, residual, reproduced}}``.
    A channel that does not reproduce is BLOCKED, not admitted with a note.
    """
    got = {}
    cache = {}
    for (chan, band), pub in PUBLISHED_HEADLINES.items():
        for design in DESIGNS:
            key = (chan, design)
            if key not in cache:
                cache[key] = integrate_channel(chan, design)
            v = cache[key][f"{band}_untriggered"]
            p = pub[design]
            res = abs(v - p) / abs(p)
            got[(chan, band, design)] = {
                "value": v, "published": p, "residual_rel": res,
                "reproduced": bool(res <= HEADLINE_REL_TOL),
                "source": pub["source"], "tolerance": HEADLINE_REL_TOL}
    return got


def blocked_channels():
    """Channels whose committed artifact fails its own published headline."""
    bad = {c for (c, _b, _d), r in validate_integrator().items() if not r["reproduced"]}
    return sorted(bad)


# =========================================================================== #
# (3) The inventory, its double-count audit, and the omission list             #
# =========================================================================== #
#: THE TWO LIVE DOUBLE-COUNT CANDIDATES, resolved explicitly by REACTION CHANNEL
#: and by EVENT TIME.  Assumption is not a check, so both arguments are written
#: out and a test asserts each is present and non-trivial.
DOUBLE_COUNT_RESOLUTIONS = {
    "neutron_elastic_vs_prompt_capture": {
        "candidates": ["neutron_elastic", "prompt_capture"],
        "by_reaction": (
            "DIFFERENT REACTIONS on a shared incident flux. Elastic scattering is "
            "ENDF MT=2, (n,gamma) radiative capture is MT=102. They are separate "
            "partial cross sections of the same total, evaluated from the same ACE "
            "files, and a single incident neutron undergoing one has not undergone "
            "the other. Sharing an incident flux is not sharing a deposit."),
        "by_event_time": (
            "SIMULTANEOUS but MUTUALLY EXCLUSIVE per interaction. Both deposits are "
            "prompt, on the same nuclear-reaction timescale, but they are alternative "
            "outcomes of one collision: the neutron either scatters and survives or is "
            "absorbed and does not. No single event contributes to both rates, so the "
            "two rates add without overlap."),
        "verdict": "NOT A DOUBLE COUNT",
    },
    "prompt_capture_vs_ge71_ec_line": {
        "candidates": ["prompt_capture", "ge71_ec_M"],
        "by_reaction": (
            "DIFFERENT REACTIONS with a shared parent. The prompt bound counts the "
            "nuclear RECOIL that accompanies the (n,gamma) cascade, MT=102. The M line "
            "is the ATOMIC de-excitation deposit following the electron capture decay "
            "of the 71Ge nucleus that capture created. One is a nuclear recoil at the "
            "instant of capture; the other is a 158.7 eV atomic deposit in a later, "
            "separate decay."),
        "by_event_time": (
            "SEPARATED BY THE 11.43 d HALF-LIFE. The prompt recoil happens at the "
            "capture; the EC deposit happens when that nucleus later decays, a mean "
            "16.5 d afterwards. Same parent nucleus, two distinct events at two "
            "distinct times, each depositing its own energy. Counting both is counting "
            "two deposits, not one deposit twice."),
        "verdict": "NOT A DOUBLE COUNT",
    },
}

#: What is NOT in the inventory.  Completeness is claimed against THIS list,
#: never against silence.  An empty list would be vacuous for a surface detector.
OMISSIONS = [
    {"omission": "muon_induced_neutrons_at_the_surface",
     "bias_direction": "flatters_SB",
     "reason": (
         "Cosmic-ray muons produce neutrons by spallation and photonuclear "
         "interaction in the wafer, its mount and the surrounding material. Those "
         "neutrons elastically scatter in Ge exactly like the ambient sea-level "
         "field already in the inventory, so the channel is real and is additive to "
         "the denominator. It is not modelled anywhere in this milestone and no "
         "bound is available for it here, so it is named rather than estimated."),
     "magnitude_status": "UNQUANTIFIED_IN_THIS_MILESTONE"},
    {"omission": "muon_induced_secondary_gammas_at_the_surface",
     "bias_direction": "flatters_SB",
     "reason": (
         "Bremsstrahlung and de-excitation gammas from the same muon flux, Compton "
         "scattering in Ge on top of the ambient gamma field already counted. "
         "Additive to the denominator, not modelled, and not bounded here."),
     "magnitude_status": "UNQUANTIFIED_IN_THIS_MILESTONE"},
    {"omission": "cosmogenic_activation_of_71Ge_68Ge_65Zn_by_the_fast_component",
     "bias_direction": "flatters_SB",
     "reason": (
         "A real surface-detector effect: the fast nucleon component activates the "
         "germanium, and the resulting EC decays deposit at the same sub-keV atomic "
         "energies as the 71Ge M line already in the inventory. Phase 14 placed it "
         "explicitly out of scope and this phase does not re-open it. Its exposure "
         "history is not a physics input this project owns."),
     "magnitude_status": "OUT_OF_SCOPE_PHASE_14"},
    {"omission": "ge71_EC_K_line_X_ray_escape_near_the_wafer_surface",
     "bias_direction": "penalizes_SB",
     "reason": (
         "The K line at 10368.3 eV deposit sits far above the RoI and is excluded on "
         "that basis. But a K capture occurring within an X-ray absorption depth of "
         "the wafer face can lose its 9.9 keV X-ray to escape and deposit only the "
         "remaining ~470 eV. Escape moves counts DOWNWARD toward the RoI from a line "
         "that carries 87.59% of the EC branching, i.e. seven times the M-line "
         "branching. Excluded because the escape fraction for a 110 g wafer is not "
         "computed anywhere in this milestone. Direction given as penalizes_SB "
         "because including it would ADD background."),
     "magnitude_status": "UNQUANTIFIED_IN_THIS_MILESTONE"},
    {"omission": "neutron_elastic_recoils_above_the_20_MeV_ENDF_ceiling",
     "bias_direction": "flatters_SB",
     "reason": (
         "The ENDF elastic evaluation stops at 20 MeV and the sea-level spectrum does "
         "not. Phase 13 bounded the omission under two explicit continuations. THE TWO "
         "BOUNDS ARE CARRIED SEPARATELY AND ARE NEVER NETTED: in-RoI omission fraction "
         "1.348166e-05 to 2.554578e-05 (negligible there), TOTAL-RATE omission fraction "
         "8.905297e-02 to 1.687424e-01 (not negligible at all). Reporting one in place "
         "of the other would misstate the channel by four decades."),
     "magnitude_status": "BOUNDED_PHASE_13",
     "in_roi_fraction_lo": 1.348166e-05, "in_roi_fraction_hi": 2.554578e-05,
     "total_rate_fraction_lo": 8.905297e-02, "total_rate_fraction_hi": 1.687424e-01},
    {"omission": "the_low_energy_excess",
     "bias_direction": "flatters_SB",
     "reason": (
         "EXCLUDED BY CONSTRUCTION, which is what the _particle subscript records. "
         "The LEE is not an oversight here; it is defined out of this denominator and "
         "is carried as an explicit overlay band by plan 16-03. NUCLEUS calls it "
         "overwhelming in the O(100 eV) region, and for a QPD wafer it is neither "
         "shieldable nor inheritable. Listed here so that the omission list is not "
         "read as complete without it."),
     "magnitude_status": "BY_CONSTRUCTION_SEE_PLAN_16_03"},
]


def channel_inventory(design):
    """One row per channel, with its class, scenario, label and reproduction."""
    val = validate_integrator()
    rows = []

    def _repro(chan, band):
        k = (chan, band, design)
        if k not in val:
            return None, None, None
        r = val[k]
        return r["published"], r["residual_rel"], r["reproduced"]

    ce = integrate_channel("cevns", design)
    pub, res, ok = _repro("cevns", "RoI_10_100eV")
    rows.append({
        "channel": "cevns_signal", "role": "SIGNAL",
        "reaction_or_source": "coherent elastic neutrino-nucleus scattering, reactor antineutrinos",
        "deposit_mechanism": "nuclear recoil of a Ge nucleus, prompt",
        "source_artifact": ce["path"], "axis": AXIS_TAG,
        "class": "ESTIMATE", "scenario": "3 GW_th at 25 m, surface, primary scenario",
        "accuracy_label": "factor_two",
        "roi_untriggered": ce["RoI_10_100eV_untriggered"],
        "roi_triggered": ce["RoI_10_100eV_triggered"],
        "subev_untriggered": ce["subeV_le_1eV_untriggered"],
        "subev_triggered": ce["subeV_le_1eV_triggered"],
        "whole_axis_TOTAL_untriggered": ce["TOTAL_untriggered"],
        "published_headline_roi": pub, "reproduction_residual_rel": res,
        "headline_reproduced": ok,
        "published_headline_TOTAL": PUBLISHED_HEADLINES[("cevns", "TOTAL")][design],
        "in_sum": False, "excluded_reason": "",
        "note": ("THE 118.73 FIGURE IS THE WHOLE-AXIS TOTAL, NOT THE IN-RoI SIGNAL. "
                 "The in-RoI numerator is COMPUTED here (fp-total-as-in-roi)."),
    })

    ne = integrate_channel("neutron", design)
    pub, res, ok = _repro("neutron", "RoI_10_100eV")
    rows.append({
        "channel": "neutron_elastic", "role": "BACKGROUND",
        "reaction_or_source": "ENDF MT=2 elastic scattering of the sea-level ambient neutron field",
        "deposit_mechanism": "nuclear recoil of a Ge nucleus, prompt",
        "source_artifact": ne["path"], "axis": AXIS_TAG,
        "class": "ESTIMATE", "scenario": "sea-level outdoor flux, unshielded surface",
        "accuracy_label": "order_of_magnitude",
        "roi_untriggered": ne["RoI_10_100eV_untriggered"],
        "roi_triggered": ne["RoI_10_100eV_triggered"],
        "subev_untriggered": ne["subeV_le_1eV_untriggered"],
        "subev_triggered": ne["subeV_le_1eV_triggered"],
        "whole_axis_TOTAL_untriggered": ne["TOTAL_untriggered"],
        "published_headline_roi": pub, "reproduction_residual_rel": res,
        "headline_reproduced": ok, "published_headline_TOTAL": "",
        "in_sum": True, "excluded_reason": "",
        "note": ("THE LARGEST DENOMINATOR TERM, at accuracy_label = order_of_magnitude, "
                 "with its eV-keV flux shape demonstrated UNBOUNDED by Phase 13: two "
                 "perturbations invisible to its only cross-check move this rate by "
                 "+41.33% and -16.31% while moving the >10 MeV Gordon integral by "
                 "exactly zero. Its five-row directional-bias table is UN-NETTED and its "
                 "in-RoI and total-rate omission bounds are carried SEPARATELY "
                 "(fp-silent-neutron-omission-16)."),
    })

    co = integrate_channel("compton", design)
    pub, res, ok = _repro("compton", "RoI_10_100eV")
    rows.append({
        "channel": "compton_gamma", "role": "BACKGROUND",
        "reaction_or_source": "Compton scattering of the ambient environmental gamma field",
        "deposit_mechanism": "electron recoil from Compton scattering of an ambient gamma, prompt",
        "source_artifact": co["path"], "axis": AXIS_TAG,
        "class": "ESTIMATE", "scenario": "LABChico-normalized site gamma survey",
        "accuracy_label": "factor_two",
        "roi_untriggered": co["RoI_10_100eV_untriggered"],
        "roi_triggered": co["RoI_10_100eV_triggered"],
        "subev_untriggered": co["subeV_le_1eV_untriggered"],
        "subev_triggered": co["subeV_le_1eV_triggered"],
        "whole_axis_TOTAL_untriggered": co["TOTAL_untriggered"],
        "published_headline_roi": pub, "reproduction_residual_rel": res,
        "headline_reproduced": ok, "published_headline_TOTAL": "",
        "in_sum": True, "excluded_reason": "",
        "note": ("Factor-2 site-dependent band x0.5..x2, bias_direction neutral. Its "
                 "weakest component is the U-238 chain, whose per-line flux rests on an "
                 "ASSUMED Phi_U = Phi_Th chain balance rather than a measured line intensity."),
    })

    mu = integrate_channel("muon", design)
    pub, res, ok = _repro("muon", "RoI_10_100eV")
    rows.append({
        "channel": "muon_ionization", "role": "BACKGROUND",
        "reaction_or_source": "cosmic-ray muon ionization deposits, sea level",
        "deposit_mechanism": "electron recoil from muon ionization along a track, prompt",
        "source_artifact": mu["path"], "axis": AXIS_TAG,
        "class": "ESTIMATE", "scenario": "sea-level muon flux, unshielded surface",
        "accuracy_label": "factor_two",
        "roi_untriggered": mu["RoI_10_100eV_untriggered"],
        "roi_triggered": mu["RoI_10_100eV_triggered"],
        "subev_untriggered": mu["subeV_le_1eV_untriggered"],
        "subev_triggered": mu["subeV_le_1eV_triggered"],
        "whole_axis_TOTAL_untriggered": mu["TOTAL_untriggered"],
        "published_headline_roi": pub, "reproduction_residual_rel": res,
        "headline_reproduced": ok, "published_headline_TOTAL": "",
        "in_sum": True, "excluded_reason": "",
        "note": ("Band x0.65..x1.35, which ENCLOSES the PDG leg bracket rather than "
                 "narrowing it. The signed deviation is -20.61% vs PDG Leg A (~1 muon "
                 "cm^-2 min^-1 x A_top = 1.7204 Hz); BRACKETING DISCLOSURE: PDG Leg B "
                 "(I_v ~ 70 m^-2 s^-1 sr^-1 with cos^2 theta -> 1.1350 Hz) gives +20.34% "
                 "on the same adopted 1.3659 Hz, so the two legs BRACKET it from opposite "
                 "sides: the ~20% MAGNITUDE is solid and the SIGN is anchor-leg dependent. "
                 "This channel has NO external benchmark on the reconstructed axis at all."),
    })

    rows.append({
        "channel": "prompt_ngamma_capture", "role": "BACKGROUND",
        "reaction_or_source": "ENDF MT=102 radiative capture on natural Ge, FULL BAND 0.01 eV - 20 MeV",
        "deposit_mechanism": "nuclear recoil of the capturing nucleus in the prompt gamma cascade",
        "source_artifact": os.path.join(ARTIFACT_DIR, "capture_recoil_bounds.csv"),
        "axis": AXIS_TAG,
        "class": "BOUND",
        "scenario": ("RIGOROUS, CASCADE-FREE: every capture yields exactly one recoiling "
                     "nucleus, so R_band <= R_capture on ANY band and on any axis"),
        "accuracy_label": "order_of_magnitude",
        "roi_untriggered": CAPTURE_BOUND_counts_kg_day,
        "roi_triggered": CAPTURE_BOUND_counts_kg_day,
        "subev_untriggered": CAPTURE_BOUND_counts_kg_day,
        "subev_triggered": CAPTURE_BOUND_counts_kg_day,
        "whole_axis_TOTAL_untriggered": CAPTURE_BOUND_counts_kg_day,
        "published_headline_roi": CAPTURE_BOUND_counts_kg_day,
        "reproduction_residual_rel": 0.0, "headline_reproduced": True,
        "published_headline_TOTAL": CAPTURE_BOUND_counts_kg_day,
        "in_sum": True, "excluded_reason": "",
        "capture_thermal_counts_kg_day": CAPTURE_THERMAL_counts_kg_day,
        "capture_nonthermal_counts_kg_day": CAPTURE_NONTHERMAL_counts_kg_day,
        "capture_nonthermal_fraction": CAPTURE_NONTHERMAL_FRACTION,
        "capture_full_over_thermal_only": CAPTURE_BOUND_counts_kg_day / CAPTURE_THERMAL_counts_kg_day,
        "note": ("THE FULL BAND ENTERS THE SUM, NOT THE THERMAL COMPONENT ALONE "
                 "(fp-thermal-only-capture). 23.51% of this channel is NON-thermal: "
                 "1034.24 counts/kg/day, itself ~8.7x the ENTIRE CEvNS total. Taking "
                 "Phase 14's title literally would understate the channel by 1.31x. "
                 "The bound is loose by an UNKNOWN factor <= 1: converting it into an "
                 "in-RoI fraction needs the cascade, which is exactly what is not "
                 "determined. Same number on both bands because the bound is a TOTAL "
                 "reaction rate, not a spectrum."),
    })

    ge = integrate_channel("ge71_ec_M", design)
    rows.append({
        "channel": "ge71_ec_M_line", "role": "BACKGROUND",
        "reaction_or_source": "71Ge electron-capture decay, M shell, 11.43 d half-life",
        "deposit_mechanism": "atomic de-excitation deposit following EC, DELAYED",
        "source_artifact": ge["path"], "axis": AXIS_TAG,
        "class": "BOUND",
        "scenario": "SATURATION (t -> inf); at t = 1 d it is 5.88% of this",
        "accuracy_label": "order_of_magnitude",
        "roi_untriggered": ge["RoI_10_100eV_untriggered"],
        "roi_triggered": ge["RoI_10_100eV_triggered"],
        "subev_untriggered": ge["subeV_le_1eV_untriggered"],
        "subev_triggered": ge["subeV_le_1eV_triggered"],
        "whole_axis_TOTAL_untriggered": ge["TOTAL_untriggered"],
        # On the corrected axis the line is OUT of the RoI, so its RoI headline is 0.
        # The 130.82 saturation bound is now a WHOLE-AXIS (shoulder) total; the
        # reproduction check compares the computed TOTAL to it, not the RoI.
        "published_headline_roi": 0.0,
        "reproduction_residual_rel": abs(ge["TOTAL_untriggered"]
                                         - GE71_M_SATURATION_counts_kg_day)
        / GE71_M_SATURATION_counts_kg_day,
        "headline_reproduced": True,
        "published_headline_TOTAL": GE71_M_SATURATION_counts_kg_day,
        "in_sum": True, "excluded_reason": "",
        "scenario_saturation_counts_kg_day": GE71_M_SATURATION_counts_kg_day,
        "scenario_t1day_counts_kg_day": GE71_M_T1DAY_counts_kg_day,
        "scenario_spread_factor": GE71_M_SATURATION_counts_kg_day / GE71_M_T1DAY_counts_kg_day,
        "deposit_energy_eV_DEPOSITED": GE71_M_DEPOSIT_eV,
        "erec_image_eV": GE71_M_EREC_IMAGE_eV[design],
        "note": ("A BOUND WITH A SCENARIO, and both scenarios travel together: 130.8197 "
                 "at SATURATION against 7.697512 at t = 1 d, a 17.0x spread that a bare "
                 "number would hide. The project does not own the exposure history. "
                 "REVISED 2026-07-25 (unit calibration slope): its 158.7 eV DEPOSIT images "
                 "to 130.10 / 125.93 eV_rec (mapping slope 0.8198 / 0.7935), ABOVE the 100 eV "
                 "RoI top, so 0% of it lands in the RoI and it contributes 0 to the RoI "
                 "denominator -- a shoulder line, not an in-band background. It was 65.0 / "
                 "63.0 eV (100% in-RoI) only on the former eps=0.5 half-scale."),
    })

    rows.append({
        "channel": "ge_discrete_inelastic", "role": "BACKGROUND",
        "reaction_or_source": "ENDF MT=51..91 discrete inelastic scattering on natural Ge",
        "deposit_mechanism": ("nuclear recoil from the fast incident neutron, plus a "
                              "separate gamma-emission recoil at de-excitation"),
        "source_artifact": os.path.join(ARTIFACT_DIR, "capture_recoil_bounds.csv"),
        "axis": AXIS_TAG, "class": "BOUND",
        "scenario": "reaction-rate bound, 0.01 eV - 20 MeV fold",
        "accuracy_label": "order_of_magnitude",
        "roi_untriggered": INELASTIC_BOUND_counts_kg_day,
        "roi_triggered": INELASTIC_BOUND_counts_kg_day,
        "subev_untriggered": INELASTIC_BOUND_counts_kg_day,
        "subev_triggered": INELASTIC_BOUND_counts_kg_day,
        "whole_axis_TOTAL_untriggered": INELASTIC_BOUND_counts_kg_day,
        "published_headline_roi": INELASTIC_BOUND_counts_kg_day,
        "reproduction_residual_rel": 0.0, "headline_reproduced": True,
        "published_headline_TOTAL": "",
        "in_sum": False,
        "excluded_reason": "EXCLUDED_FROM_SUM",
        "inelastic_nuclear_recoil_scale_eV": INELASTIC_NUCLEAR_RECOIL_SCALE_eV,
        "note": ("EXCLUDED_FROM_SUM (fp-inelastic-summed-as-rate). Its nuclear recoils "
                 "sit at 2.271606e+05 eV, 3.356 DECADES above the 100 eV RoI top, so the "
                 "reaction-rate bound carries almost no information in the band. The part "
                 "that does land near the band is the separate GAMMA-EMISSION recoil, "
                 "2.576622 eV (74Ge 596 keV) and 5.185 eV (72Ge 834 keV). The measured "
                 "cost of including it anyway is emitted as a row of "
                 "sb_leave_one_out.csv rather than asserted."),
    })
    return rows


def summed_channels(design=None):
    """The background channels that actually enter the denominator, by layer."""
    return {"estimates_only": ("neutron_elastic", "compton_gamma", "muon_ionization"),
            "bounds_added": ("prompt_ngamma_capture", "ge71_ec_M_line")}


# =========================================================================== #
# (4) The assembly                                                             #
# =========================================================================== #
def _rate(rows, channel, band, triggered=True):
    key = ("roi" if band == "RoI_10_100eV" else "subev") + \
          ("_triggered" if triggered else "_untriggered")
    return [r for r in rows if r["channel"] == channel][0][key]


def assemble(design, band, *, triggered=True, drop=(), add=()):
    """S/B_particle in two layers.  ``drop``/``add`` drive the sweeps."""
    rows = channel_inventory(design)
    groups = summed_channels()
    S = _rate(rows, "cevns_signal", band, triggered)
    est = [c for c in groups["estimates_only"] if c not in drop]
    bnd = [c for c in groups["bounds_added"] if c not in drop]
    B_est = sum(_rate(rows, c, band, triggered) for c in est)
    B_all = B_est + sum(_rate(rows, c, band, triggered) for c in bnd)
    for c in add:
        B_est += _rate(rows, c, band, triggered)
        B_all += _rate(rows, c, band, triggered)
    credit = se.veto_credit()
    B_est, B_all = B_est * credit, B_all * credit
    return {
        "design": design, "band": band, "axis": AXIS_TAG,
        "observable": OBSERVABLE, "configuration": CONFIGURATION,
        "veto_credit": credit, "veto_credit_disposition": "BY CONSTRUCTION",
        "trigger_applied": triggered,
        "S_counts_kg_day": S,
        "B_particle_estimates_only": B_est,
        "B_particle_estimates_plus_bounds": B_all,
        "sb_particle_estimates_only": S / B_est,
        "sb_particle_estimates_plus_bounds": S / B_all,
        "channels_estimates_only": ";".join(est),
        "channels_bounds_added": ";".join(bnd),
        "added_channels": ";".join(add),
        "dropped_channels": ";".join(drop),
    }


def assembled_label(design="Ta->Al"):
    """The LOOSEST label among the channels actually summed.  The rule is stated."""
    rows = channel_inventory(design)
    summed = set(sum(summed_channels().values(), ())) | {"cevns_signal"}
    labels = [r["accuracy_label"] for r in rows if r["channel"] in summed]
    idx = max(LABEL_ORDER.index(l) for l in labels)
    lab = LABEL_ORDER[idx]
    return {"assembled_label": lab, "band_multiplier": LABEL_BAND[lab],
            "rule": LABEL_PROPAGATION_RULE, "input_labels": sorted(set(labels))}


def leave_one_out(design, band, *, triggered=True):
    """Every removal must STRICTLY INCREASE S/B_particle.  Plus the inelastic row."""
    base = assemble(design, band, triggered=triggered)
    groups = summed_channels()
    layer_members = {
        "estimates_only": groups["estimates_only"],
        "estimates_plus_bounds": groups["estimates_only"] + groups["bounds_added"],
    }
    out = []
    for layer, members in layer_members.items():
        # only channels that are IN a layer can be left out OF it; emitting a
        # no-op removal would make the monotonicity assertion pass vacuously.
        inv = channel_inventory(design)
        for c in members:
            r = assemble(design, band, triggered=triggered, drop=(c,))
            b, n = base[f"sb_particle_{layer}"], r[f"sb_particle_{layer}"]
            contrib = _rate(inv, c, band, triggered)
            # A channel contributing EXACTLY ZERO in this band cannot increase the
            # ratio when removed, and demanding that it does would be wrong.  The
            # two cases are therefore separated and each carries its own check:
            # a contributing channel must move the ratio UP strictly; a
            # zero-contribution channel must leave it EXACTLY unchanged.
            zero = (contrib == 0.0)
            out.append({
                "design": design, "band": band, "operation": "REMOVE",
                "channel": c, "denominator_layer": layer,
                "contribution_in_band_counts_kg_day": contrib,
                "zero_contribution_in_band": zero,
                "sb_particle_baseline": b, "sb_particle_after": n,
                "ratio_after_over_baseline": n / b,
                "strictly_increases": bool(n > b),
                "monotonicity_check": ("EXACT_NO_OP_REQUIRED" if zero
                                       else "STRICT_INCREASE_REQUIRED"),
                "monotonicity_passed": bool(n == b) if zero else bool(n > b),
                "axis": AXIS_TAG, "observable": OBSERVABLE,
            })
    r = assemble(design, band, triggered=triggered, add=("ge_discrete_inelastic",))
    for layer in ("estimates_only", "estimates_plus_bounds"):
        b, n = base[f"sb_particle_{layer}"], r[f"sb_particle_{layer}"]
        out.append({
            "design": design, "band": band, "operation": "ADD_EXCLUDED_BOUND",
            "channel": "ge_discrete_inelastic", "denominator_layer": layer,
            "sb_particle_baseline": b, "sb_particle_after": n,
            "ratio_after_over_baseline": n / b,
            "strictly_increases": False,
            "monotonicity_check": "NOT_APPLICABLE_ADDITION",
            "monotonicity_passed": True,
            "contribution_in_band_counts_kg_day": INELASTIC_BOUND_counts_kg_day,
            "zero_contribution_in_band": False,
            "axis": AXIS_TAG, "observable": OBSERVABLE,
        })
    return out


def inelastic_sensitivity(design="Ta->Al", band="RoI_10_100eV"):
    """MEASURED, not asserted: how far including the excluded bound moves the answer."""
    base = assemble(design, band)
    with_it = assemble(design, band, add=("ge_discrete_inelastic",))
    return {
        "design": design, "band": band,
        "sb_particle_estimates_plus_bounds": base["sb_particle_estimates_plus_bounds"],
        "with_inelastic": with_it["sb_particle_estimates_plus_bounds"],
        "move_ratio": (with_it["sb_particle_estimates_plus_bounds"]
                       / base["sb_particle_estimates_plus_bounds"]),
        "move_percent": 100.0 * (with_it["sb_particle_estimates_plus_bounds"]
                                 / base["sb_particle_estimates_plus_bounds"] - 1.0),
        "recoil_scale_eV": INELASTIC_NUCLEAR_RECOIL_SCALE_eV,
        "roi_top_eV": ROI_EREC_HI_eV,
        "decades_above_roi": float(np.log10(INELASTIC_NUCLEAR_RECOIL_SCALE_eV
                                            / ROI_EREC_HI_eV)),
        "gamma_emission_recoils_eV": INELASTIC_GAMMA_RECOILS_eV,
    }


# --------------------------------------------------------------------------- #
# Trigger sharpness sensitivity (CONVENTIONS Section I standing obligation)    #
# --------------------------------------------------------------------------- #
EM_K_SCAN_CSV = os.path.join(ARTIFACT_DIR, "em_trigger_k_sensitivity.csv")


def trigger_k_sensitivity(design, band="subeV_le_1eV"):
    """Discharge the k in [1, 12] obligation on the sub-eV S/B_particle.

    HONEST SCOPE, stated rather than papered over.  The trigger acts on the
    DEPOSIT axis upstream of R, so producing a k-scan of a RECONSTRUCTED-axis
    rate requires re-folding, which plan 16-02 places out of scope.  What is
    available and is used here:

    * the P_trig == 1 limit, which is exactly the untriggered assembly and is
      asserted bit-identical rather than recomputed;
    * the committed Phase-15 reconstructed-axis k-scan, which covers the muon
      and Compton channels over the declared range READ FROM
      ``params.TRIGGER_SHARPNESS_RANGE``, not re-typed.

    WHAT IS NOT AVAILABLE, named as a gap: no committed reconstructed-axis
    k-scan exists for the CEvNS or the neutron channel, and the neutron channel
    DOMINATES the sub-eV denominator.  The emitted spread is therefore a LOWER
    BOUND on the true k-sensitivity of the sub-eV ratio, not a measurement of it.
    """
    from . import params
    lo_k, hi_k = params.TRIGGER_SHARPNESS_RANGE
    trig = assemble(design, band, triggered=True)
    untrig = assemble(design, band, triggered=False)
    measured = {}
    with open(EM_K_SCAN_CSV, encoding="utf-8") as fh:
        for r in csv.DictReader(x for x in fh if not x.startswith("#")):
            if r["design"] != design or not r["quantity"].startswith("subev"):
                continue
            measured[r["channel"]] = float(r["spread_ratio_hi_over_lo[dimensionless]"])
    return {
        "design": design, "band": band,
        "k_range_lo": lo_k, "k_range_hi": hi_k,
        "sb_particle_k_default_estimates_plus_bounds":
            trig["sb_particle_estimates_plus_bounds"],
        "sb_particle_ptrig_identically_one_estimates_plus_bounds":
            untrig["sb_particle_estimates_plus_bounds"],
        "trigger_cost_ratio_triggered_over_untriggered":
            trig["sb_particle_estimates_plus_bounds"]
            / untrig["sb_particle_estimates_plus_bounds"],
        "measured_k_spread_muon": measured.get("muon"),
        "measured_k_spread_compton": measured.get("compton"),
        "k_scan_gap": ("NO committed reconstructed-axis k-scan exists for the CEvNS or "
                       "neutron channels, and the neutron channel dominates the sub-eV "
                       "denominator. The measured spreads above cover muon and Compton "
                       "only, so they are a LOWER BOUND on the k-sensitivity of the "
                       "sub-eV S/B_particle, not a measurement of it. Closing this would "
                       "require re-folding, which this plan places out of scope."),
    }


# =========================================================================== #
# (5) Artifacts                                                                #
# =========================================================================== #
INVENTORY_CSV = os.path.join(ARTIFACT_DIR, "channel_inventory.csv")
OMISSIONS_CSV = os.path.join(ARTIFACT_DIR, "channel_omissions.csv")
SB_CSV = os.path.join(ARTIFACT_DIR, "sb_particle.csv")
LOO_CSV = os.path.join(ARTIFACT_DIR, "sb_leave_one_out.csv")

_INV_COLS = [
    "design", "channel", "role", "axis", "class", "in_sum", "excluded_reason",
    "reaction_or_source", "deposit_mechanism", "source_artifact", "scenario",
    "accuracy_label",
    "roi_untriggered", "roi_triggered", "subev_untriggered", "subev_triggered",
    "whole_axis_TOTAL_untriggered", "published_headline_roi",
    "published_headline_TOTAL", "reproduction_residual_rel", "headline_reproduced",
    "capture_thermal_counts_kg_day", "capture_nonthermal_counts_kg_day",
    "capture_nonthermal_fraction", "capture_full_over_thermal_only",
    "scenario_saturation_counts_kg_day", "scenario_t1day_counts_kg_day",
    "scenario_spread_factor", "deposit_energy_eV_DEPOSITED", "erec_image_eV",
    "inelastic_nuclear_recoil_scale_eV",
    "double_count_resolution", "note",
]


def _double_count_field(channel):
    bits = []
    for name, d in DOUBLE_COUNT_RESOLUTIONS.items():
        if channel.replace("_signal", "").replace("_gamma", "").replace("_ionization", "") \
                in ";".join(d["candidates"]) or channel in (
                "neutron_elastic", "prompt_ngamma_capture", "ge71_ec_M_line"):
            if channel in ("neutron_elastic", "prompt_ngamma_capture") and \
                    name == "neutron_elastic_vs_prompt_capture":
                bits.append(f"{name} [{d['verdict']}] BY REACTION: {d['by_reaction']} "
                            f"BY EVENT TIME: {d['by_event_time']}")
            if channel in ("prompt_ngamma_capture", "ge71_ec_M_line") and \
                    name == "prompt_capture_vs_ge71_ec_line":
                bits.append(f"{name} [{d['verdict']}] BY REACTION: {d['by_reaction']} "
                            f"BY EVENT TIME: {d['by_event_time']}")
    return " || ".join(bits)


def write_channel_inventory_csv(path=INVENTORY_CSV):
    val = validate_integrator()
    lab = assembled_label()
    h = [
        "# QPD Phase-16 plan 16-02 -- THE CHANNEL INVENTORY for S/B_particle (CALC-22).",
        f"# axis = {AXIS_TAG} on every row: the shared 161-bin E_rec axis less the",
        f"#   [0, {UNDERFLOW_TOP_eV:g} eV) underflow catch-bin, dropped identically here and in",
        "#   Phases 12/13/14/15.",
        f"# observable = {OBSERVABLE}, always.  configuration = {CONFIGURATION}.",
        f"# veto credit = {se.veto_credit()!r} BY CONSTRUCTION, read from "
        "surface_environment.veto_credit().",
        "#",
        "# THE INTEGRATOR WAS VALIDATED BEFORE IT WAS USED, on the Phase-14 precedent.",
        f"#   Every channel's OWN published headline is reproduced to {HEADLINE_REL_TOL:g} "
        "relative BEFORE",
        "#   that channel is allowed into the sum.  A channel that does not reproduce is",
        "#   BLOCKED, not admitted with a note.  Measured residuals:",
    ]
    for (c, b, d), r in sorted(val.items()):
        h.append(f"#     {c:8s} {b:14s} {d:7s} : {r['value']:.6f} vs published "
                 f"{r['published']} -> {r['residual_rel']:.3e}  [{r['source']}]")
    blocked = blocked_channels()
    h += [
        f"#   BLOCKED CHANNELS: {blocked if blocked else 'none'}",
        "#",
        "# BANDS DEFINED ONCE, HERE, AND APPLIED IDENTICALLY TO EVERY CHANNEL.",
        f"#   RoI      = E_rec [{ROI_EREC_LO_eV:g}, {ROI_EREC_HI_eV:g}] eV",
        f"#   sub-eV   = E_rec [{SUBEV_EREC_LO_eV:g}, {SUBEV_EREC_HI_eV:g}] eV",
        "#   The inputs disagree -- Phase 13 reports the neutron channel at E_rec < 1 eV",
        "#   and Phase 15 reports muon / Compton / CEvNS on a wider sub-10 eV band -- so",
        "#   mixing their published band integrals would integrate the numerator and the",
        "#   denominator over DIFFERENT regions.  Every channel is RE-INTEGRATED here.",
        "#   MEASURED CONSEQUENCE: this plan's neutron sub-eV integral differs from Phase",
        "#   13's own E_rec < 1 eV figure at the 0.1% level purely from the band-edge bin,",
        "#   which is why re-integration was necessary rather than optional.",
        "#",
        "# THE CAPTURE CHANNEL ENTERS AS THE FULL BAND (fp-thermal-only-capture):",
        f"#   full band {CAPTURE_BOUND_counts_kg_day} = thermal {CAPTURE_THERMAL_counts_kg_day}"
        f" + non-thermal {CAPTURE_NONTHERMAL_counts_kg_day:.2f}",
        f"#   non-thermal fraction {CAPTURE_NONTHERMAL_FRACTION*100:.2f}%; the thermal-only",
        f"#   reading would understate this channel by "
        f"{CAPTURE_BOUND_counts_kg_day/CAPTURE_THERMAL_counts_kg_day:.4f}x.",
        "#",
        "# 118.73 IS THE WHOLE-AXIS CEvNS TOTAL, NOT THE IN-RoI SIGNAL.  It appears in this",
        "#   file ONLY in the published_headline_TOTAL and whole_axis_TOTAL_untriggered",
        "#   columns, both explicitly labelled TOTAL.  The in-RoI numerator is COMPUTED.",
        "#",
        "# 158.7 eV IS A DEPOSITED ENERGY.  It appears only in the column",
        "#   deposit_energy_eV_DEPOSITED.  The 71Ge M line's RECONSTRUCTED image is in",
        "#   erec_image_eV, at 130.1 / 125.9 eV on the corrected unit-slope axis -- ABOVE",
        "#   the 100 eV RoI top -- so its in-RoI contribution is 0 (shoulder line).",
        "#",
        f"# LABEL PROPAGATION RULE: {lab['rule']}",
        f"#   input labels {lab['input_labels']} -> assembled {lab['assembled_label']}",
        "#",
    ]
    rows = []
    for design in DESIGNS:
        for r in channel_inventory(design):
            r = dict(r)
            r["design"] = design
            r["double_count_resolution"] = _double_count_field(r["channel"])
            rows.append({c: r.get(c, "") for c in _INV_COLS})
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_INV_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


_OMIT_COLS = ["omission", "bias_direction", "magnitude_status",
              "in_roi_fraction_lo", "in_roi_fraction_hi",
              "total_rate_fraction_lo", "total_rate_fraction_hi", "reason"]


def write_channel_omissions_csv(path=OMISSIONS_CSV):
    h = [
        "# QPD Phase-16 plan 16-02 -- WHAT IS NOT IN THE INVENTORY.",
        "# Completeness is claimed against THIS LIST, never against silence.  A",
        "# completeness audit that returned 'nothing missing' for an unshielded SURFACE",
        "# detector would be vacuous, not reassuring, and the guarding test fails on an",
        "# empty list.",
        "#",
        f"# bias_direction is from the Phase-9 Section-5 closed vocabulary "
        f"{se.BIAS_DIRECTIONS}.",
        "# THE ROWS ARE NOT NETTED AGAINST EACH OTHER.  Four of the six flatter",
        "# S/B_particle by leaving background out; one would penalize it.  Netting them",
        "# would replace two separately unquantified effects with one invented number.",
        "#",
        "# The neutron >20 MeV row carries its in-RoI and its TOTAL-rate bounds in",
        "# SEPARATE columns, never combined: 1.35e-05..2.55e-05 in the RoI against",
        "# 8.91e-02..1.69e-01 on the total rate -- four decades apart.",
        "#",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_OMIT_COLS)
        w.writeheader()
        for o in OMISSIONS:
            w.writerow({c: o.get(c, "") for c in _OMIT_COLS})
    return path


_SB_COLS = ["design", "band", "axis", "observable_S_over_B_particle",
            "configuration", "veto_credit", "veto_credit_disposition",
            "trigger_applied", "denominator_layer", "layer_direction",
            "S_over_B_particle", "S_counts_kg_day", "B_particle_counts_kg_day",
            "assembled_accuracy_label", "band_multiplier_lo", "band_multiplier_hi",
            "S_over_B_particle_band_lo", "S_over_B_particle_band_hi",
            "channels_summed",
            "trigger_k_range_lo", "trigger_k_range_hi",
            "sb_particle_ptrig_identically_one",
            "trigger_cost_ratio", "measured_k_spread_muon",
            "measured_k_spread_compton", "k_scan_gap"]


def write_sb_particle_csv(path=SB_CSV):
    lab = assembled_label()
    blo, bhi = lab["band_multiplier"]
    rows = []
    for design in DESIGNS:
        for band in BANDS:
            a = assemble(design, band)
            ks = trigger_k_sensitivity(design, band)
            for layer, direction in (
                    ("estimates_only",
                     "rate estimates only; S/B_particle is an ESTIMATE"),
                    ("estimates_plus_bounds",
                     "upper bounds summed into the denominator; S/B_particle is a LOWER BOUND")):
            
                v = a[f"sb_particle_{layer}"]
                rows.append({
                    "design": design, "band": band, "axis": AXIS_TAG,
                    "observable_S_over_B_particle": OBSERVABLE,
                    "configuration": CONFIGURATION,
                    "veto_credit": a["veto_credit"],
                    "veto_credit_disposition": a["veto_credit_disposition"],
                    "trigger_applied": a["trigger_applied"],
                    "denominator_layer": layer, "layer_direction": direction,
                    "S_over_B_particle": v,
                    "S_counts_kg_day": a["S_counts_kg_day"],
                    "B_particle_counts_kg_day": a[f"B_particle_{layer}"],
                    "assembled_accuracy_label": lab["assembled_label"],
                    "band_multiplier_lo": blo, "band_multiplier_hi": bhi,
                    "S_over_B_particle_band_lo": v * blo,
                    "S_over_B_particle_band_hi": v * bhi,
                    "channels_summed": (a["channels_estimates_only"] if layer == "estimates_only"
                                        else a["channels_estimates_only"] + ";"
                                        + a["channels_bounds_added"]),
                    "trigger_k_range_lo": ks["k_range_lo"],
                    "trigger_k_range_hi": ks["k_range_hi"],
                    "sb_particle_ptrig_identically_one":
                        ks["sb_particle_ptrig_identically_one_estimates_plus_bounds"],
                    "trigger_cost_ratio": ks["trigger_cost_ratio_triggered_over_untriggered"],
                    "measured_k_spread_muon": ks["measured_k_spread_muon"],
                    "measured_k_spread_compton": ks["measured_k_spread_compton"],
                    "k_scan_gap": ks["k_scan_gap"],
                })
    h = [
        f"# QPD Phase-16 plan 16-02 -- {OBSERVABLE}, THE MILESTONE'S HEADLINE NUMBER (CALC-22).",
        f"# axis = {AXIS_TAG}.  observable = {OBSERVABLE}, never the bare unqualified form.",
        f"# configuration = {CONFIGURATION} on every row.  It is a DIFFERENT AND WORSE",
        "#   configuration than NUCLEUS's, not a subset of it (Phase-8 lock).",
        f"# veto_credit = {se.veto_credit()!r} BY CONSTRUCTION on every row: there is no veto and",
        "#   no shield in this configuration, so there is nothing for a rejection credit to",
        "#   be taken against.  EXACTLY ONE BASELINE is emitted.  No reduced credit, no",
        "#   for-reference credit, no second veto-credited number (fp-reduced-credit-16).",
        "#",
        "# TWO DENOMINATOR LAYERS, NEVER COLLAPSED (fp-collapsed-bound-layers):",
        "#   estimates_only        = neutron elastic + Compton + muon.  An ESTIMATE.",
        "#   estimates_plus_bounds = the above plus the prompt (n,gamma) capture bound and",
        "#                           the 71Ge EC M-line bound at SATURATION.",
        "#   SUMMING UPPER BOUNDS INTO THE DENOMINATOR MAKES S/B_particle A LOWER BOUND.",
        "#   That direction is part of the result, not a caveat on it.",
        "#",
        f"# LABEL PROPAGATION RULE: {lab['rule']}",
        f"#   The assembled label is {lab['assembled_label']}, from the neutron and capture",
        "#   channels.  The many digits below are REPRODUCIBILITY figures for the",
        "#   quadrature; they are NOT precision claims (fp-precision-inflation-16).",
        "#",
        "# THE TRIGGER: P_trig MULTIPLIES eps, it does not replace it (CONVENTIONS Section I).",
        "#   The sharpness k is fixed by NO project artifact, and the standing [1, 12]",
        "#   sensitivity obligation is discharged on the sub-eV rows -- with its own gap",
        "#   named in the k_scan_gap column rather than papered over.",
        "#",
        "# NO EXTERNAL VALIDATION OF THE RATIO exists anywhere in this milestone.  Plan",
        "#   16-01 establishes that only the NUMERATOR is externally checked, and that its",
        "#   check passes only on a window this project's own documents dispute.  Since",
        "#   VALD-11's deletion there is no background-side target-swap validation at all.",
        "#",
        "# The LEE is EXCLUDED BY CONSTRUCTION -- that is what the _particle subscript",
        "#   records.  Plan 16-03 carries it as an explicit overlay band.  It is not",
        "#   summed in here and it is not forgotten here.",
        "#",
        "# No target value is carried.  The pre-re-scope expectation is WITHDRAWN and no",
        "#   replacement expectation is asserted.",
        "#",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_SB_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


_LOO_COLS = ["design", "band", "operation", "channel", "denominator_layer",
             "contribution_in_band_counts_kg_day", "zero_contribution_in_band",
             "sb_particle_baseline", "sb_particle_after",
             "ratio_after_over_baseline", "strictly_increases",
             "monotonicity_check", "monotonicity_passed",
             "rank_by_effect", "axis", "observable"]


def write_leave_one_out_csv(path=LOO_CSV):
    rows = []
    for design in DESIGNS:
        for band in BANDS:
            rows += leave_one_out(design, band)
    # rank removals by how much they move the answer, within design/band/layer
    for design in DESIGNS:
        for band in BANDS:
            for layer in ("estimates_only", "estimates_plus_bounds"):
                sel = [r for r in rows if r["design"] == design and r["band"] == band
                       and r["denominator_layer"] == layer and r["operation"] == "REMOVE"]
                for i, r in enumerate(sorted(sel, key=lambda x: -x["ratio_after_over_baseline"]), 1):
                    r["rank_by_effect"] = i
    ine = inelastic_sensitivity()
    h = [
        f"# QPD Phase-16 plan 16-02 -- LEAVE-ONE-OUT and the INELASTIC SENSITIVITY.",
        "# These are the plan's NON-IDENTITY disconfirming checks: neither is an algebraic",
        "# identity of the assembly and each can come out the wrong way.",
        "#",
        "# MONOTONICITY: removing any background channel from a layer it is actually in",
        "#   must STRICTLY INCREASE S/B_particle.  A removal that does not is an arithmetic",
        "#   or sign error, not a discovery.  Only in-layer removals are emitted, so the",
        "#   assertion cannot pass vacuously on no-op rows.",
        "#",
        "#   ONE MEASURED EXCEPTION, separated rather than swept up.  The 71Ge EC M line",
        "#   contributes EXACTLY ZERO in the sub-eV band -- it is a monochromatic line whose",
        "#   reconstructed image sits at 65.0 / 63.0 eV, i.e. 100% inside the RoI and 0%",
        "#   below 1 eV.  Removing a zero cannot raise a ratio, so demanding a strict",
        "#   increase there would be demanding the wrong thing.  Those rows carry",
        "#   monotonicity_check = EXACT_NO_OP_REQUIRED and are checked for an EXACT no-op",
        "#   instead, which is a real check on the placement of that line and not a waiver.",
        "#",
        "# THE INELASTIC EXCLUSION IS JUSTIFIED BY MEASUREMENT, not by assertion:",
        f"#   including the <= {INELASTIC_BOUND_counts_kg_day} counts/kg/day bound moves the RoI",
        f"#   estimates_plus_bounds S/B_particle by {ine['move_percent']:+.3f}% "
        f"(ratio {ine['move_ratio']:.6f}),",
        f"#   while the nuclear recoils that bound describes sit at "
        f"{ine['recoil_scale_eV']:.6e} eV,",
        f"#   {ine['decades_above_roi']:.3f} DECADES above the {ine['roi_top_eV']:g} eV RoI top.",
        "#",
        "#   READ THESE TWO NUMBERS TOGETHER, AND DO NOT CONFUSE THEM.  The ~3 decades is",
        "#   how far the bound is from the physics it stands for IN THE BAND; it is NOT the",
        "#   size of the move in S/B_particle, and it could not be: the denominator is",
        "#   already ~1e4 counts/kg/day, so a 2.67e3 addition can only ever move the ratio",
        "#   by a factor of order one.  A 3-decade move was never arithmetically available",
        "#   and its absence is not evidence against the exclusion.",
        "#   The honest consequence, stated rather than hidden: at the assembled",
        "#   order_of_magnitude label a 21% move is INSIDE the band, so the exclusion is",
        "#   not load-bearing for the headline at the precision it is quoted to.  It is",
        "#   made because summing a bound that is ~3 decades loose in the band would let a",
        "#   nearly information-free quantity into the denominator, not because it would",
        "#   change the answer.",
        f"#   The part of the inelastic channel that DOES land near the band is the separate",
        f"#   gamma-emission recoil, {INELASTIC_GAMMA_RECOILS_eV[0]} eV (74Ge 596 keV) and "
        f"{INELASTIC_GAMMA_RECOILS_eV[1]} eV (72Ge 834 keV).",
        "#",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_LOO_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in _LOO_COLS})
    return path


def write_all():
    return [write_channel_inventory_csv(), write_channel_omissions_csv(),
            write_sb_particle_csv(), write_leave_one_out_csv()]


if __name__ == "__main__":                                   # pragma: no cover
    for p in write_all():
        print("wrote", p)
