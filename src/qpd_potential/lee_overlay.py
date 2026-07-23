# ASSERT_CONVENTION: natural_units=internal_cevns_only, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=cevns_4pi_QW, renormalization_scheme=tree_level_SM_sin2thetaW_0.2387, gauge_choice=not_applicable
"""Phase 16 plan 16-03 -- the LEE overlay band, SC4's adjudication, and closeout.

THE LEE IS CARRIED AS AN OVERLAY BAND, NEVER SUMMED IN.  ``dR/dE_LEE =
A (E/E0)^(-alpha)`` is evaluated directly on the committed RECONSTRUCTED energy
axis.  It is NEVER folded through ``R(E_rec|E_dep)`` and it is never multiplied
by the trigger curve: the LEE anchors are quoted in MEASURED (reconstructed)
energy, so a detector response is already inside them, and folding would apply
one twice.  ``tests/test_lee_overlay.py`` proves the no-fold guarantee by
parsing this file's AST rather than by grepping it, because the words
"response" and "fold" MUST appear in this prose -- naming the trap is the point.

NOTHING HERE IS A PREDICTION.  No LEE measurement exists below ~10 eV in
germanium, or at 100 meV in any material; the lowest genuine LEE dataset
anywhere is CRESST-III from 29.6 eV, on CaWO4, a different target.  Every
amplitude row is marked ``UNMEASURED_FOR_THIS_DETECTOR``.  This module does NOT
claim the QPD architecture is LEE-free -- there is no evidence either way, and
the LEE mechanism and the QPD signal mechanism are the SAME phenomenon,
quasiparticle poisoning, so the LEE is a direct competitor to the readout
rather than merely a background.

THE OBSERVABLE ``S/B_particle`` IS LEFT NUMERICALLY UNTOUCHED.  Any ratio that
INCLUDES the LEE carries a different name.

A NEW module, so no ``file:line`` inventory key moves.
"""
from __future__ import annotations

import csv
import os

import numpy as np

from . import sb_assembly as sba

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTIFACT_DIR = os.path.join(_ROOT, "artifacts", "v2.0")

AXIS_TAG = "RECONSTRUCTED"
UNMEASURED = "UNMEASURED_FOR_THIS_DETECTOR"
NOT_FOLDED_FLAG = True

# =========================================================================== #
# (1) The parameterization.  E0 declared ONCE.                                 #
# =========================================================================== #
#: The reference energy at which the amplitude A is quoted, declared ONCE and
#: stated on every artifact and on the figure.  It is set to 1 keV because that
#: is one of the two EDELWEISS RED20 anchor points, so ``A(E0)`` for the anchor
#: curve is the anchor value itself with no arithmetic in between.
E0_keV = 1.0

#: EDELWEISS RED20 germanium amplitude anchors, ABOVE GROUND.  The above-ground
#: values are the relevant ones for a surface wafer; the survey's /3 underground
#: values are NOT used.  P. Adari et al., SciPost Phys. Proc. 9, 001 (2022),
#: arXiv:2202.05097, as compiled in GPD/literature/SUMMARY.md.  These are
#: PROSE-SOURCED survey citations, not a locally frozen artifact -- the same
#: class of provenance as the 407.7 dru closure, though used here as the
#: parameter space of an overlay rather than as a validation.
RED20_ANCHORS_dru = ((0.200, 1.0e5), (1.000, 1.0e4))     # (E in keV, dru)

#: The two anchors are quoted to ONE significant figure, so their RATIO carries
#: at least a factor-2 uncertainty.  alpha is therefore carried as a RANGE, not
#: as a point, over ratio in [10/2, 10*2] = [5, 20].  DECLARED, not sourced.
ALPHA_RATIO_BRACKET = (5.0, 20.0)

#: The lowest germanium LEE amplitude measurement available anywhere, in keV.
#: Everything this module evaluates below it is EXTRAPOLATION.
LOWEST_GE_LEE_MEASUREMENT_keV = 0.200

#: The reconstructed-axis band floor, identical to the underflow-catch-bin top
#: that plan 16-02 drops.  The LEE integral needs a finite lower edge because a
#: power law with alpha > 1 diverges at zero, and using anything OTHER than the
#: band the particle channels were integrated on would compare two different
#: regions of the axis.
BAND_FLOOR_keV = sba.UNDERFLOW_TOP_eV / 1.0e3


def alpha_from_anchors(anchors=RED20_ANCHORS_dru):
    """DERIVE alpha from the two RED20 points.  Never quoted."""
    (e1, a1), (e2, a2) = anchors
    return float(np.log(a1 / a2) / np.log(e2 / e1))


def alpha_range(anchors=RED20_ANCHORS_dru, ratio_bracket=ALPHA_RATIO_BRACKET):
    """alpha over the declared anchor-ratio bracket.  A RANGE, not a point."""
    (e1, _a1), (e2, _a2) = anchors
    lo = float(np.log(ratio_bracket[0]) / np.log(e2 / e1))
    hi = float(np.log(ratio_bracket[1]) / np.log(e2 / e1))
    return (lo, hi)


#: The 100 meV deposit-grid floor, which is where the terminal figure starts.
DISPLAY_FLOOR_keV = 1.0e-4


def extrapolation_span_decades(floor_keV=None):
    """How far BELOW the lowest germanium LEE measurement this overlay reaches.

    TWO numbers, because there are two floors and quoting one would understate
    the other: the figure starts at the 100 meV grid floor, but the sub-eV band
    INTEGRAL runs down to the reconstructed-axis floor, three more decades
    lower, and that is where most of the sub-eV LEE integral actually lives.
    """
    floor = BAND_FLOOR_keV if floor_keV is None else floor_keV
    return float(np.log10(LOWEST_GE_LEE_MEASUREMENT_keV / floor))


def extrapolation_spans():
    return {
        "to_display_floor_100meV_decades":
            extrapolation_span_decades(DISPLAY_FLOOR_keV),
        "to_reconstructed_axis_floor_decades":
            extrapolation_span_decades(BAND_FLOOR_keV),
        "lowest_ge_lee_measurement_keV": LOWEST_GE_LEE_MEASUREMENT_keV,
        "note": ("No LEE measurement exists below ~10 eV in germanium or at 100 meV "
                 "in ANY material; the lowest genuine LEE dataset anywhere is "
                 "CRESST-III from 29.6 eV on CaWO4, a different target."),
    }


# =========================================================================== #
# (2) The two contradictory device scalings, as NAMED band edges               #
# =========================================================================== #
#: Romani Al-film AREA scaling.  R. K. Romani, J. Appl. Phys. 136, 124502
#: (2024), arXiv:2406.15425.  The LEE is modelled as Al-film dislocation
#: relaxation scaling with film AREA, predicting meV-eV phonons -- which is
#: exactly this geometry, a wafer carrying ~10,300 films.
ROMANI_N_FILMS = 10300
WAFER_SURFACE_TO_MASS_cm2_per_kg = 1950.0
CAWO4_6G8_SURFACE_TO_MASS_cm2_per_kg = 955.0

#: Chang bulk VOLUME scaling.  C. L. Chang et al., Appl. Phys. Lett. 127,
#: 263502 (2025).  Sub-meV bursts at eps = 0.68 +/- 0.38 meV in bulk substrate.
CHANG_DEVICE_MASS_g = 0.93
WAFER_MASS_g = 110.0


def device_scalings():
    """The two band edges, with their extrapolation factors written out.

    A FINDING THAT CUTS AGAINST THE SURVEY'S FRAMING, stated here rather than
    buried: dru is ALREADY MASS-NORMALIZED (counts/kg/day/keV).  A model in
    which the LEE scales with VOLUME therefore predicts a rate per unit mass
    that is INVARIANT under the mass extrapolation, so Chang's x118.3 mass
    factor CANCELS in dru and its band edge is exactly 1.000.  The x120 that
    the survey quotes is a TOTAL-rate extrapolation and is not an amplitude
    factor.  A model in which the LEE scales with AREA predicts dru
    proportional to surface-to-mass, which for this wafer against a 6.8 g CaWO4
    crystal is 1950/955 = 2.042 -- and that is BEFORE counting the ~10,300
    films at all, which is the lever area scaling makes design-controllable and
    volume scaling does not.

    CONSEQUENCE, reported rather than repaired: the disagreement between the
    two models is only a factor ~2 IN dru, much narrower than the survey's
    framing suggests.  The width of the overlay band is set instead by the
    alpha extrapolation over more than three decades and by the factor-2
    uncertainty on the anchors themselves.
    """
    area = WAFER_SURFACE_TO_MASS_cm2_per_kg / CAWO4_6G8_SURFACE_TO_MASS_cm2_per_kg
    mass = WAFER_MASS_g / CHANG_DEVICE_MASS_g
    return {
        "romani_al_film_area": {
            "scaling": "AREA (Al-film dislocation relaxation)",
            "extrapolation_factor_written_out":
                f"surface-to-mass {WAFER_SURFACE_TO_MASS_cm2_per_kg:g} cm^2/kg (wafer) / "
                f"{CAWO4_6G8_SURFACE_TO_MASS_cm2_per_kg:g} cm^2/kg (6.8 g CaWO4 crystal) "
                f"= {area:.4f}, BEFORE counting the ~{ROMANI_N_FILMS} films",
            "dru_factor": area,
            "n_films": ROMANI_N_FILMS,
            "reference": "Romani, J. Appl. Phys. 136, 124502 (2024), arXiv:2406.15425",
            "status": UNMEASURED,
        },
        "chang_bulk_volume": {
            "scaling": "VOLUME (bulk-substrate phonon bursts, eps = 0.68 +/- 0.38 meV)",
            "extrapolation_factor_written_out":
                f"mass {CHANG_DEVICE_MASS_g:g} g -> {WAFER_MASS_g:g} g = x{mass:.4f}, "
                f"which CANCELS in dru because dru is already per kg; the dru factor is "
                f"therefore exactly 1.000 and the x{mass:.0f} is a TOTAL-rate "
                f"extrapolation, not an amplitude factor",
            "dru_factor": 1.0,
            "mass_extrapolation": mass,
            "reference": "Chang et al., Appl. Phys. Lett. 127, 263502 (2025)",
            "status": UNMEASURED,
        },
    }


def band_edge_amplitudes():
    """A at E0 for each named edge, from the RED20 above-ground anchor."""
    a_ref = dict(RED20_ANCHORS_dru)[E0_keV]
    return {k: {"A_at_E0_dru": a_ref * v["dru_factor"], **v}
            for k, v in device_scalings().items()}


def scalings_bracket_the_anchor():
    """Do the two edges BRACKET the RED20 anchor?  Recorded either way.

    They do NOT strictly bracket it: the volume edge coincides with the anchor
    exactly, by construction, because volume scaling is dru-invariant.  That is
    reported rather than repaired by quietly widening the band.
    """
    a_ref = dict(RED20_ANCHORS_dru)[E0_keV]
    amps = [v["A_at_E0_dru"] for v in band_edge_amplitudes().values()]
    return {"anchor_A_at_E0_dru": a_ref,
            "band_lo_dru": min(amps), "band_hi_dru": max(amps),
            "strictly_brackets": bool(min(amps) < a_ref < max(amps)),
            "note": ("The RED20 above-ground anchor sits exactly ON the volume-scaling "
                     "edge, because volume scaling leaves a mass-normalized rate "
                     "unchanged. The band therefore CONTAINS the anchor but does not "
                     "strictly bracket it. Recorded, not widened.")}


# =========================================================================== #
# (3) Evaluation on the committed reconstructed axis -- NEVER FOLDED           #
# =========================================================================== #
def lee_dRdE(E_keV, A_dru, alpha, E0=E0_keV):
    """dR/dE_LEE = A (E/E0)^(-alpha), in dru, on the RECONSTRUCTED axis.

    No response matrix, no fold and no trigger curve is applied here or anywhere
    downstream of here.  The anchors are quoted in measured energy.
    """
    E = np.asarray(E_keV, dtype=float)
    return A_dru * (E / E0) ** (-alpha)


def lee_band_integral(A_dru, alpha, lo_keV, hi_keV, E0=E0_keV):
    """Closed-form integral of the power law over an E_rec band, in counts/kg/day.

    INT_lo^hi A (E/E0)^(-alpha) dE
      = A E0^alpha (hi^(1-alpha) - lo^(1-alpha)) / (1 - alpha)      alpha != 1
      = A E0 ln(hi/lo)                                              alpha == 1
    with E in keV, so the result is already counts/kg/day.
    """
    lo = max(float(lo_keV), BAND_FLOOR_keV)
    hi = float(hi_keV)
    if abs(alpha - 1.0) < 1e-12:
        return float(A_dru * E0 * np.log(hi / lo))
    return float(A_dru * E0 ** alpha
                 * (hi ** (1.0 - alpha) - lo ** (1.0 - alpha)) / (1.0 - alpha))


def crossover_amplitude(target_counts_kg_day, alpha, lo_keV, hi_keV, E0=E0_keV):
    """Solve A such that the band-integrated LEE equals a named target."""
    unit = lee_band_integral(1.0, alpha, lo_keV, hi_keV, E0)
    return float(target_counts_kg_day / unit)


# =========================================================================== #
# (4) SC4, EVALUATED AS LITERALLY WRITTEN -- BEFORE any replacement            #
# =========================================================================== #
#: ROADMAP Phase 16 SC4's decisive number, quoted VERBATIM beside its evaluation.
SC4_WORDING = "the LEE amplitude at which S/B_particle = 1"


def sb_total_with_lee(design, band, A_dru, alpha, layer="estimates_only"):
    """A DIFFERENTLY NAMED ratio that DOES include the LEE.

    ``S/B_total``.  It exists only so that SC4's criterion can be evaluated as
    written; it is never called ``S/B_particle`` and it is never emitted as the
    headline.  The particle-side numbers are read from the committed plan-16-02
    assembly and are not modified.
    """
    asm = sba.assemble(design, band)
    lo, hi = BAND_EDGES_keV[band]
    lee = lee_band_integral(A_dru, alpha, lo, hi)
    return asm["S_counts_kg_day"] / (asm[f"B_particle_{layer}"] + lee)


def evaluate_sc4_as_written(design="Ta->Al", band="RoI_10_100eV"):
    """Evaluate SC4's criterion AS WRITTEN.  Record the outcome EITHER WAY.

    A finding that the criterion IS solvable is an equally acceptable outcome
    and would refute the planning note in 16-CONTEXT.md.  Both determinations
    are COMPUTED against the committed plan-16-02 assembly, not asserted.
    """
    import inspect

    base = sba.assemble(design, band)
    alpha = alpha_from_anchors()

    # (1) DOES S/B_particle DEPEND ON A AT ALL?  Demonstrated by CONTRAST rather
    #     than by repetition: the differently-named S/B_total is evaluated at two
    #     widely separated amplitudes and MOVES, while S/B_particle -- which has
    #     no LEE amplitude in its signature and no LEE channel in its summed set
    #     -- is bit-identical at both, because the _particle subscript defines the
    #     LEE OUT of that denominator (ROADMAP SC3).
    A_small, A_large = 1.0e-6, 1.0e6
    total_small = sb_total_with_lee(design, band, A_small, alpha)
    total_large = sb_total_with_lee(design, band, A_large, alpha)
    particle = base["sb_particle_estimates_only"]
    sig = inspect.signature(sba.assemble)
    has_amplitude_param = any("lee" in p.lower() or p.lower() in ("a", "amplitude")
                              for p in sig.parameters)
    summed = set(sum(sba.summed_channels().values(), ()))
    has_lee_channel = any("lee" in c.lower() for c in summed)
    depends = bool(has_amplitude_param or has_lee_channel)

    # (2) CAN IT REACH 1 FOR ANY NON-NEGATIVE A?  Solve directly.  Under the
    #     charitable reading S/B_total = 1 the required LEE contribution is
    #     S - B_particle, which is NEGATIVE here, so no A >= 0 satisfies it.
    best = max(base["sb_particle_estimates_only"],
               base["sb_particle_estimates_plus_bounds"])
    required_lee = base["S_counts_kg_day"] - base["B_particle_estimates_only"]
    reachable = bool(best >= 1.0 or required_lee > 0.0)

    return {
        "criterion_verbatim": SC4_WORDING,
        "design": design, "band": band,
        "determination_1_question":
            "does S/B_particle depend on the LEE amplitude A under this milestone's "
            "own definitions?",
        "determination_1_answer": depends,
        "determination_1_numbers":
            f"CONTRAST, computed: the differently-named S/B_total moves from "
            f"{total_small:.6e} at A = {A_small:g} dru to {total_large:.6e} at "
            f"A = {A_large:g} dru, a factor {total_small/total_large:.4e}; over the "
            f"same range S/B_particle is {particle:.6e} at BOTH, because assemble() "
            f"takes no LEE amplitude and its summed channel set "
            f"{sorted(summed)} contains no LEE term. "
            f"d(S/B_particle)/dA = 0 exactly.",
        "determination_2_question":
            "can S/B_particle reach 1 for any non-negative A?",
        "determination_2_answer": reachable,
        "determination_2_numbers":
            f"the supremum of S/B_particle over the emitted layers is {best:.6e}, a "
            f"factor {1.0/best:.4f} BELOW 1 before any LEE is added; and under the "
            f"charitable reading S/B_total = 1 the required LEE band integral is "
            f"S - B_particle = {base['S_counts_kg_day']:.4f} - "
            f"{base['B_particle_estimates_only']:.4f} = {required_lee:.4f} "
            f"counts/kg/day, which is NEGATIVE, so no A >= 0 satisfies it.",
        "solvable": bool(depends and reachable),
        "verdict": ("CONFIRMED" if (depends and reachable)
                    else "SUPERSEDED BY MEASUREMENT"),
        "verdict_reason": (
            "The criterion has NO solution, and both independent reasons are "
            "measured rather than asserted: S/B_particle does not depend on A at "
            "all, and its value is already far below 1 before any LEE is added. "
            "The criterion was written when the milestone expected a ratio near "
            "unity at the shielded VNS, where 'S/B = 1' and 'the LEE erases the "
            "signal' nearly coincided; the 2026-07-22 re-scope withdrew that "
            "expectation and carried the wording forward unchanged. FLAGGED FOR "
            "THE ORCHESTRATOR as a wording problem in ROADMAP.md and "
            "REQUIREMENTS.md. Neither file is edited here."),
        "replaced_by": ["lee_equals_B_particle", "lee_equals_S"],
        "replacement_note": (
            "lee_equals_S is the formulation GPD/literature/PITFALLS.md Pitfall 7 "
            "actually specifies -- the LEE level that would erase the signal. It is "
            "NOT the same quantity as SC4's wording and is never reported under "
            "SC4's name (fp-sc4-silent-substitution)."),
    }


# --------------------------------------------------------------------------- #
BAND_EDGES_keV = {"RoI_10_100eV": (sba.ROI_EREC_LO_eV / 1e3, sba.ROI_EREC_HI_eV / 1e3),
                  "subeV_le_1eV": (BAND_FLOOR_keV, sba.SUBEV_EREC_HI_eV / 1e3)}


def crossovers():
    """The two well-defined crossovers, each under its OWN explicit name."""
    a_lo, a_hi = alpha_range()
    a_c = alpha_from_anchors()
    edges = band_edge_amplitudes()
    rows = []
    for design in sba.DESIGNS:
        for band, (lo, hi) in BAND_EDGES_keV.items():
            asm = sba.assemble(design, band)
            targets = [
                ("lee_equals_B_particle", "estimates_only",
                 asm["B_particle_estimates_only"]),
                ("lee_equals_B_particle", "estimates_plus_bounds",
                 asm["B_particle_estimates_plus_bounds"]),
                ("lee_equals_S", "not_applicable", asm["S_counts_kg_day"]),
            ]
            for qname, layer, target in targets:
                for atag, alpha in (("alpha_lo", a_lo), ("alpha_central", a_c),
                                    ("alpha_hi", a_hi)):
                    A = crossover_amplitude(target, alpha, lo, hi)
                    row = {
                        "quantity_name": qname,
                        "is_sc4_as_written": False,
                        "design": design, "band": band,
                        "denominator_layer": layer,
                        "axis": AXIS_TAG,
                        "not_folded_through_response": NOT_FOLDED_FLAG,
                        "status": UNMEASURED,
                        "E0_keV": E0_keV,
                        "alpha_tag": atag, "alpha": alpha,
                        "band_lo_keV": lo, "band_hi_keV": hi,
                        "target_counts_kg_day": target,
                        "A_crossover_dru_at_E0": A,
                        "extrapolation_span_decades": extrapolation_span_decades(),
                    }
                    for ename, e in edges.items():
                        row[f"ratio_{ename}_over_crossover"] = e["A_at_E0_dru"] / A
                    row["ratio_red20_above_ground_anchor_over_crossover"] = \
                        dict(RED20_ANCHORS_dru)[E0_keV] / A
                    row["subev_regime_caveat"] = (
                        "CONVENTIONS Section I: below the E_rec image of a 1 eV deposit "
                        "the reported observable is a TRIGGER PROBABILITY, not "
                        "dR/dE_rec, so this row's band spans a boundary where the "
                        "observable changes character"
                        if band == "subeV_le_1eV" else "")
                    rows.append(row)
    return rows


def sc4_as_written_row(design="Ta->Al", band="RoI_10_100eV"):
    d = evaluate_sc4_as_written(design, band)
    return {
        "quantity_name": SC4_WORDING,
        "is_sc4_as_written": True,
        "design": design, "band": band, "denominator_layer": "n/a",
        "axis": AXIS_TAG, "not_folded_through_response": NOT_FOLDED_FLAG,
        "status": "NO_SOLUTION" if not d["solvable"] else "SOLVED",
        "E0_keV": E0_keV, "alpha_tag": "n/a", "alpha": "",
        "band_lo_keV": BAND_EDGES_keV[band][0], "band_hi_keV": BAND_EDGES_keV[band][1],
        "target_counts_kg_day": "", "A_crossover_dru_at_E0": "",
        "extrapolation_span_decades": extrapolation_span_decades(),
        "sc4_verdict": d["verdict"],
        "sc4_determination_1": f"{d['determination_1_question']} -> "
                               f"{d['determination_1_answer']}. {d['determination_1_numbers']}",
        "sc4_determination_2": f"{d['determination_2_question']} -> "
                               f"{d['determination_2_answer']}. {d['determination_2_numbers']}",
        "sc4_reason": d["verdict_reason"],
        "replaced_by": ";".join(d["replaced_by"]),
    }


# =========================================================================== #
# (5) Artifacts                                                                #
# =========================================================================== #
LEE_BAND_CSV = os.path.join(ARTIFACT_DIR, "lee_overlay_band.csv")
CROSSOVER_CSV = os.path.join(ARTIFACT_DIR, "lee_crossover_amplitudes.csv")
FIGURE_PDF = os.path.join(ARTIFACT_DIR, "sb_particle_with_lee.pdf")

_BAND_COLS = ["E_rec_keV", "band_edge", "scaling", "A_at_E0_dru", "E0_keV",
              "alpha_tag", "alpha", "dRdE_LEE_dru", "axis",
              "not_folded_through_response", "status",
              "extrapolation_factor_written_out",
              "extrapolation_span_to_100meV_decades",
              "extrapolation_span_to_axis_floor_decades",
              "alpha_source", "reference"]


def overlay_axis_keV():
    """The committed reconstructed axis, from the 100 meV display floor up."""
    src = sba.read_erec_channel(
        os.path.join(ARTIFACT_DIR, "cevns_dRdErec_ext_TaAl.csv"), "dRdErec_central")
    E = src["E_rec_eV"] / 1.0e3
    return E[E >= DISPLAY_FLOOR_keV]


def write_lee_overlay_band_csv(path=LEE_BAND_CSV):
    E = overlay_axis_keV()
    edges = band_edge_amplitudes()
    a_lo, a_hi = alpha_range()
    a_c = alpha_from_anchors()
    spans = extrapolation_spans()
    br = scalings_bracket_the_anchor()
    alpha_src = (f"DERIVED from the EDELWEISS RED20 ABOVE-GROUND germanium anchors "
                 f"{RED20_ANCHORS_dru[0][1]:.0e} dru at {RED20_ANCHORS_dru[0][0]*1e3:.0f} eV "
                 f"and {RED20_ANCHORS_dru[1][1]:.0e} dru at {RED20_ANCHORS_dru[1][0]*1e3:.0f} eV: "
                 f"alpha = ln(A1/A2)/ln(E2/E1) = {a_c:.6f}")
    h = [
        "# QPD Phase-16 plan 16-03 -- THE LEE OVERLAY BAND on the RECONSTRUCTED axis.",
        f"# axis = {AXIS_TAG}; not_folded_through_response = True on every row.",
        "# The LEE is MEASURED in reconstructed energy, so a detector response is",
        "#   already inside the anchors. Folding through R(E_rec|E_dep) would apply one",
        "#   TWICE and would move amplitude across the sub-eV regime boundary where the",
        "#   reported observable itself changes (fp-lee-folded-through-response).",
        "#",
        f"# PARAMETERIZATION: dR/dE_LEE = A (E/E0)^(-alpha), with E0 = {E0_keV:g} keV",
        "#   declared ONCE and stated on every row and on the figure.",
        f"# {alpha_src}",
        f"#   alpha is carried as a RANGE, not a point: [{a_lo:.6f}, {a_hi:.6f}], from a",
        f"#   declared factor-2 bracket on the anchor RATIO (the anchors are quoted to one",
        f"#   significant figure). DECLARED, not sourced.",
        "#",
        "# BOTH CONTRADICTORY DEVICE SCALINGS ARE CARRIED AS NAMED EDGES, and neither is",
        "#   ever emitted without the other (fp-lee-single-value):",
    ]
    for name, e in edges.items():
        h.append(f"#   {name}: {e['scaling']}; {e['extrapolation_factor_written_out']}; "
                 f"dru factor {e['dru_factor']:.4f} -> A(E0) = {e['A_at_E0_dru']:.6e} dru")
    h += [
        "#",
        "# A FINDING THAT CUTS AGAINST THE SURVEY'S FRAMING, reported rather than",
        "#   repaired: dru is ALREADY MASS-NORMALIZED, so a VOLUME-scaling model predicts",
        "#   a dru that is INVARIANT under the mass extrapolation. Chang's x118.28 mass",
        "#   factor therefore CANCELS in dru and that band edge is exactly 1.000; the",
        "#   x120 in the survey is a TOTAL-rate extrapolation, not an amplitude factor.",
        "#   CONSEQUENCE: the disagreement between the two models is only ~2x IN dru,",
        "#   much narrower than the survey's framing suggests. The real width of this",
        "#   overlay comes from the alpha extrapolation and from the anchors themselves.",
        "#",
        f"# DO THE TWO SCALINGS BRACKET THE RED20 ANCHOR? {br['strictly_brackets']}. "
        f"{br['note']}",
        "#",
        f"# EXTRAPOLATION SPAN BELOW THE LOWEST GERMANIUM LEE MEASUREMENT "
        f"({LOWEST_GE_LEE_MEASUREMENT_keV*1e3:.0f} eV):",
        f"#   {spans['to_display_floor_100meV_decades']:.4f} decades to the 100 meV grid floor "
        f"(where the figure starts),",
        f"#   {spans['to_reconstructed_axis_floor_decades']:.4f} decades to the "
        f"reconstructed-axis floor (where the sub-eV band integral ends).",
        f"#   {spans['note']}",
        "#",
        f"# EVERY AMPLITUDE ROW IS MARKED {UNMEASURED}. Nothing here is a prediction, in",
        "#   either direction. This file does NOT claim the QPD architecture is free of",
        "#   the LEE: there is no evidence either way, and the LEE mechanism and the QPD",
        "#   SIGNAL mechanism are the same phenomenon -- quasiparticle poisoning -- so the",
        "#   LEE is a direct competitor to the readout, not merely a background.",
        "#",
        "# 'particle backgrounds only; LEE not modelled in the headline'",
        "#",
    ]
    rows = []
    for name, e in edges.items():
        for atag, alpha in (("alpha_lo", a_lo), ("alpha_central", a_c),
                            ("alpha_hi", a_hi)):
            y = lee_dRdE(E, e["A_at_E0_dru"], alpha)
            for Ei, yi in zip(E, y):
                rows.append({
                    "E_rec_keV": f"{Ei:.10e}", "band_edge": name,
                    "scaling": e["scaling"], "A_at_E0_dru": e["A_at_E0_dru"],
                    "E0_keV": E0_keV, "alpha_tag": atag, "alpha": alpha,
                    "dRdE_LEE_dru": f"{yi:.10e}", "axis": AXIS_TAG,
                    "not_folded_through_response": NOT_FOLDED_FLAG,
                    "status": UNMEASURED,
                    "extrapolation_factor_written_out":
                        e["extrapolation_factor_written_out"],
                    "extrapolation_span_to_100meV_decades":
                        f"{spans['to_display_floor_100meV_decades']:.4f}",
                    "extrapolation_span_to_axis_floor_decades":
                        f"{spans['to_reconstructed_axis_floor_decades']:.4f}",
                    "alpha_source": alpha_src, "reference": e["reference"],
                })
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_BAND_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


_CROSS_COLS = ["quantity_name", "is_sc4_as_written", "design", "band",
               "denominator_layer", "axis", "not_folded_through_response",
               "status", "E0_keV", "alpha_tag", "alpha",
               "band_lo_keV", "band_hi_keV", "target_counts_kg_day",
               "A_crossover_dru_at_E0",
               "ratio_romani_al_film_area_over_crossover",
               "ratio_chang_bulk_volume_over_crossover",
               "ratio_red20_above_ground_anchor_over_crossover",
               "extrapolation_span_decades", "subev_regime_caveat",
               "sc4_verdict", "sc4_determination_1", "sc4_determination_2",
               "sc4_reason", "replaced_by"]


def write_crossover_csv(path=CROSSOVER_CSV):
    d = evaluate_sc4_as_written()
    rows = [sc4_as_written_row()] + crossovers()
    h = [
        "# QPD Phase-16 plan 16-03 -- SC4 AS WRITTEN, ADJUDICATED, and the NAMED crossovers.",
        f"# axis = {AXIS_TAG}; not_folded_through_response = True on every row.",
        "#",
        "# ============ ROADMAP PHASE 16 SC4, EVALUATED AS LITERALLY WRITTEN ==========",
        f'# The criterion, quoted VERBATIM: "{SC4_WORDING}".',
        f"# VERDICT: {d['verdict']}.",
        f"#   DETERMINATION 1 -- {d['determination_1_question']}",
        f"#     ANSWER: {d['determination_1_answer']}.",
        f"#     {d['determination_1_numbers']}",
        f"#   DETERMINATION 2 -- {d['determination_2_question']}",
        f"#     ANSWER: {d['determination_2_answer']}.",
        f"#     {d['determination_2_numbers']}",
        f"#   {d['verdict_reason']}",
        "#",
        "# A finding that the criterion IS solvable would have been an equally acceptable",
        "#   outcome and would have refuted the planning note in 16-CONTEXT.md. It came",
        "#   out unsolvable, and BOTH determinations are recorded with their numbers.",
        "#",
        "# ============ THE REPLACEMENTS, EACH UNDER ITS OWN EXPLICIT NAME ============",
        "#   lee_equals_B_particle -- the LEE-DOMINANCE crossover: the amplitude at which",
        "#     the band-integrated LEE equals B_particle, i.e. the point beyond which the",
        "#     LEE rather than particles sets the denominator.",
        "#   lee_equals_S -- the SIGNAL-ERASURE level: the amplitude at which the",
        "#     band-integrated LEE equals the signal S. This is the formulation",
        "#     GPD/literature/PITFALLS.md Pitfall 7 actually specifies, and it is NOT the",
        "#     same quantity as SC4's wording.",
        "#   NEITHER is reported under SC4's name. SC4's phrasing appears on exactly one",
        "#     row, the as-written evaluation (fp-sc4-silent-substitution).",
        "#",
        f"# Every amplitude is in dru at E0 = {E0_keV:g} keV and is marked {UNMEASURED}.",
        "# Nothing here is a prediction for this detector, in either direction.",
        "#",
        "# The many digits are REPRODUCIBILITY figures for the closed-form solve. The",
        "#   particle-side denominator they are measured against carries the assembled",
        "#   label order_of_magnitude and an UNBOUNDED flux systematic on its largest",
        "#   term (fp-precision-inflation-lee).",
        "#",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(h) + "\n")
        w = csv.DictWriter(fh, fieldnames=_CROSS_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in _CROSS_COLS})
    return path


# =========================================================================== #
# (6) The terminal figure                                                      #
# =========================================================================== #
FIGURE_ANNOTATION = "particle backgrounds only; LEE not modelled in the headline"

#: The E_rec image of a 1 eV DEPOSIT, per design (Phase 13, median statistic).
#: Drawn on the figure as an IMAGE, never as a literal 1 eV line.
SUBEV_BOUNDARY_EREC_eV = {"Ta->Al": 0.497240, "Al->Hf": 0.495855}

_FIG_CHANNELS = (
    ("cevns", "dRdErec_central", "CEvNS signal", "tab:blue", 2.2, "-"),
    ("neutron", "dRdErec_central", "neutron elastic", "tab:red", 1.6, "-"),
    ("compton", "compton_dRdErec_untriggered[counts/kg/day/keV]",
     "Compton gamma", "tab:green", 1.4, "-"),
    ("muon", "muon_dRdErec_untriggered[counts/kg/day/keV]",
     "muon ionization", "tab:orange", 1.4, "-"),
    ("ge71_ec_M", "dRdErec_bound", "71Ge EC M line (bound, saturation)",
     "tab:purple", 1.4, "--"),
)


def make_terminal_figure(path=FIGURE_PDF, design="Ta->Al"):
    """All particle channels, the signal, and the LEE band as a SHADED OVERLAY.

    The LEE curve is NEVER folded and NEVER summed into any plotted total; it is
    drawn on top, as a band between its two named device-scaling edges.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # UNCOMPRESSED text stream, so the annotation audit can read the label OUT of
    # the file rather than settling for "the figure exists".
    matplotlib.rcParams["pdf.compression"] = 0

    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    tag = sba._TAG[design]
    for name, col, label, colour, lw, ls in _FIG_CHANNELS:
        stem = sba.SPECTRAL_SOURCES[name][0]
        src = sba.read_erec_channel(
            os.path.join(ARTIFACT_DIR, stem.format(tag=tag)), col)
        E = src["E_rec_eV"] / 1.0e3
        y = src["dRdErec"]
        m = (E >= DISPLAY_FLOOR_keV) & (y > 0)
        ax.plot(E[m] * 1.0e3, y[m], ls, color=colour, lw=lw, label=label, zorder=3)

    E = overlay_axis_keV()
    edges = band_edge_amplitudes()
    a_lo, a_hi = alpha_range()
    a_c = alpha_from_anchors()
    curves = []
    for e in edges.values():
        for alpha in (a_lo, a_c, a_hi):
            curves.append(lee_dRdE(E, e["A_at_E0_dru"], alpha))
    lee_lo = np.min(np.vstack(curves), axis=0)
    lee_hi = np.max(np.vstack(curves), axis=0)
    ax.fill_between(E * 1.0e3, lee_lo, lee_hi, color="0.35", alpha=0.30,
                    zorder=2,
                    label="LEE overlay BAND - never summed in, never folded")
    for name, e in edges.items():
        ax.plot(E * 1.0e3, lee_dRdE(E, e["A_at_E0_dru"], a_c), ":", lw=1.4,
                color="0.15", zorder=2)
        ax.annotate(name, xy=(E[len(E) // 3] * 1.0e3,
                              lee_dRdE(E[len(E) // 3], e["A_at_E0_dru"], a_c)),
                    fontsize=7, color="0.15")

    ax.axvspan(sba.ROI_EREC_LO_eV, sba.ROI_EREC_HI_eV, color="tab:blue",
               alpha=0.07, zorder=0)
    ax.annotate("RoI 10-100 eV", xy=(11.0, 1.0e-3), fontsize=8, color="tab:blue")
    for d, b in SUBEV_BOUNDARY_EREC_eV.items():
        ax.axvline(b, color="0.4", lw=0.9, ls="-.", zorder=1)
    ax.annotate("sub-eV regime boundary:\nE_rec IMAGE of a 1 eV DEPOSIT\n"
                "(0.497240 / 0.495855 eV, not 1 eV)",
                xy=(0.50, 3.0e10), fontsize=7, color="0.25")

    spans = extrapolation_spans()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(DISPLAY_FLOOR_keV * 1.0e3, 120.0)
    ax.set_xlabel("reconstructed energy E_rec [eV]   (axis = RECONSTRUCTED)")
    ax.set_ylabel("dR/dE_rec [counts/kg/day/keV = dru]")
    ax.set_title("Phase 16 terminal: particle channels, CEvNS signal and the LEE "
                 "overlay band\nNUCLEUS's-shielding-absent, veto credit 1.0 BY "
                 "CONSTRUCTION", fontsize=10)
    ax.grid(True, which="both", alpha=0.15)
    ax.legend(loc="lower left", fontsize=7.5, framealpha=0.92)

    ax.text(0.015, 0.985, FIGURE_ANNOTATION, transform=ax.transAxes,
            fontsize=9, va="top", ha="left",
            bbox=dict(boxstyle="round", fc="lightyellow", ec="0.3"))
    ax.text(0.985, 0.985,
            "accuracy_label = order_of_magnitude\n"
            f"E0 = {E0_keV:g} keV; alpha in [{a_lo:.4f}, {a_hi:.4f}]\n"
            "LEE band edges: romani_al_film_area / chang_bulk_volume\n"
            f"LEE EXTRAPOLATION: {spans['to_display_floor_100meV_decades']:.3f} decades "
            f"below the lowest Ge LEE measurement (200 eV)\n"
            f"({spans['to_reconstructed_axis_floor_decades']:.3f} decades to the "
            "reconstructed-axis floor used by the sub-eV band)\n"
            "every LEE amplitude is UNMEASURED_FOR_THIS_DETECTOR",
            transform=ax.transAxes, fontsize=6.6, va="top", ha="right",
            bbox=dict(boxstyle="round", fc="white", ec="0.5"))
    ax.text(0.015, 0.015,
            "prompt (n,gamma) capture and the 71Ge M line enter S/B_particle as "
            "BOUNDS;\nthe capture bound is a total reaction rate, not a spectrum, "
            "so it is not drawn here.",
            transform=ax.transAxes, fontsize=6.4, va="bottom", ha="left",
            color="0.25")

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def write_all():
    return [write_lee_overlay_band_csv(), write_crossover_csv(),
            make_terminal_figure()]


if __name__ == "__main__":                                   # pragma: no cover
    for p in write_all():
        print("wrote", p)
