# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Transferable veto credits for the 110 g monolithic Ge wafer -- all exactly 1.0.

Phase 8 (Veto-Envelope Geometry Gate, P-VETO), Plan 08-04, Task 2.
Requirement VALD-09. ROADMAP Phase 8 Success Criterion 2.

WHAT THIS MODULE IS FOR
    ``GPD/analysis/VETO-TAXONOMY.md`` classifies every NUCLEUS rejection and
    attenuation statement Phase 8 catalogued into three tiers and fixes each
    row's transferable rejection credit at 1.0. A credit recorded only in a
    markdown table will eventually be typed into a formula by someone, with no
    reviewable trace. This module is where that decision lives in code.

    Any downstream code path that wants a rejection factor must NAME the
    statement -- ``credit_for("row-b05-cov-neutron-anticoincidence")`` -- and
    receives 1.0. There is no way to obtain a number other than 1.0 from this
    module, and no way to obtain any number at all without naming a catalogued
    statement.

A CREDIT OF 1.0 MEANS THE BACKGROUND IS UNCHANGED.
    Read 1.0 as the EMPTY credit, not as full credit. The credit is a
    dimensionless multiplicative factor applied to a background RATE when that
    background is re-folded for the wafer; 1.0 leaves the rate exactly as it
    was, i.e. NO REJECTION IS TAKEN.

CHANGING EITHER CONSTANT AWAY FROM 1.0 REQUIRES A WAFER-SPECIFIC VETO GEOMETRY
AND A DOCUMENTED ARGUMENT, AND IS EXPECTED TO APPEAR AS A REVIEWABLE DIFF.
    That is the whole point of the constants being here. VALD-09 states that
    inherited veto credit defaults to zero unless earned by wafer geometry, and
    the milestone-wide forbidden proxy ``fp-veto-credit-transfer`` prohibits
    inheriting gram-scale rejection factors for a 110 g monolithic wafer. A
    reduced or partial credit is NOT permitted either, even as an interim value
    (explicit user decision, 2026-07-22): a partial credit has no derivation
    behind it and would silently become the project's number.

THE THREE TIERS (full definitions and the swap test in the taxonomy document)
    L1   environmental -- decoupled from payload geometry. The QUANTITY
         transfers, as an environmental input or as material attenuation of the
         incident field re-applied to the wafer's own fold. It never transfers
         as a rejection credit multiplied onto a rate, so ``L1_REJECTION_CREDIT``
         is 1.0 as well.
    L1*  passive but payload-geometry-coupled -- the nearly-4pi 4 cm boron
         carbide liner and the internal shielding. Passive material, but the
         PUBLISHED value is quoted for a liner in the direct vicinity of a
         centimetre-scale payload. Credit 1.0.
    L2   payload-coupled active rejection -- the COV, the MV, the IV and the
         single-target-hit multiplicity requirement. Credit 1.0.

    The taxonomy's three-tier split is an EXTENSION of ROADMAP Success
    Criterion 2, which specifies a binary L1/L2 split. The extension is
    documented as an extension in the taxonomy document, section 2.1.

NO NUCLEUS REJECTION PERCENTAGE OR FACTOR APPEARS AS A VALUE ANYWHERE IN THIS
MODULE.
    Not as a literal, not as a default argument, not as a table entry. The
    verbatim NUCLEUS sentences live in ``GPD/analysis/VETO-TAXONOMY.md`` with
    their recorded grep commands; each row below points at its taxonomy row id
    and its ``08-01-SOURCE-EVIDENCE.md`` section instead of restating the
    number. ``tests/test_veto_credit.py`` enforces this repository-wide with two
    decidable rules (a literal denylist, and a naming rule requiring every
    module-level numeric constant whose name contains CREDIT, REJECTION or
    VETO_FACTOR to equal exactly 1.0).

ONE ROW'S CREDIT IS DERIVED RATHER THAN DEFAULTED.
    ``row-b02-multiplicity-cut``. Plan 08-02 establishes that NUCLEUS's
    "one and only one target detector" conjunct is satisfied identically by a
    single-readout target, so the rejection is exactly zero and the credit is
    1.0 BY DERIVATION -- no policy default is needed. See
    ``src/qpd_potential/wafer_self_veto.py`` and
    ``multiplicity_rejection_is_zero()`` below, which CONSUMES that derivation
    rather than restating its value.
"""
from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "L1_REJECTION_CREDIT",
    "L1STAR_CREDIT",
    "L2_CREDIT",
    "TIERS",
    "CREDIT_BASES",
    "TaxonomyRow",
    "TAXONOMY",
    "lookup",
    "tier_of",
    "credit_for",
    "rows_in_tier",
    "multiplicity_rejection_is_zero",
]

# --------------------------------------------------------------------------- #
# The credits                                                                  #
# --------------------------------------------------------------------------- #

L2_CREDIT = 1.0
"""Transferable rejection credit for L2 (payload-coupled active rejection): 1.0.

Phase 8 (P-VETO), Plan 08-04. Requirement VALD-09. ROADMAP Phase 8 Success
Criterion 2.

REASON. L2 rejection is earned by active detectors operated in anti-coincidence
around the payload -- NUCLEUS's cryogenic outer veto (six 2.5 cm HPGe crystals),
their 5 cm plastic-scintillator muon veto, their TES-instrumented inner-veto
holder, and the requirement of a hit in one and only one target detector. A
110 g monolithic germanium wafer has none of these. Nothing about their measured
efficiencies constrains a payload with 45.9x the array-crystal footprint
(crystal basis; 11.5x on the holder basis) and a single readout channel, and
Plan 08-03 additionally determined the wafer does not fit the published COV
envelope at all.

1.0 MEANS THE BACKGROUND IS UNCHANGED -- no rejection is taken. Raising this
above 1.0 requires a wafer-specific veto geometry and a documented argument
(``fp-veto-credit-transfer``); a reduced or partial credit is not permitted
either.
"""

L1STAR_CREDIT = 1.0
"""Transferable rejection credit for L1* (passive but payload-geometry-coupled): 1.0.

Phase 8 (P-VETO), Plan 08-04. Requirement VALD-09. ROADMAP Phase 8 Success
Criterion 2, extended from its binary L1/L2 split to three tiers -- documented
as an extension in ``GPD/analysis/VETO-TAXONOMY.md`` section 2.1.

REASON. L1* covers passive material attenuation whose PUBLISHED value is coupled
to the payload geometry: the nearly-4pi 4 cm boron carbide liner and the
internal shielding. The material would attenuate anything, but the published
suppression factor is quoted for a nearly-4pi liner in the direct vicinity of a
centimetre-scale payload, i.e. it is coupled to the very payload dimension this
phase disputes. The wafer's face is two orders of magnitude larger in area, so
the geometry the factor was measured in no longer exists.

Silently promoting these rows to L1 because they are "passive" would flatter the
background budget at exactly the point where the wafer's size is the problem
(``fp-l1star-promotion``). L1* records the disagreement rather than resolving it
by fiat; the counter-argument a reviewer could make is stated in the taxonomy
document, section 5.

1.0 MEANS THE BACKGROUND IS UNCHANGED -- no rejection is taken.
"""

L1_REJECTION_CREDIT = 1.0
"""Rejection credit for L1 (environmental) statements: 1.0 -- and L1 DOES transfer.

Phase 8 (P-VETO), Plan 08-04. Requirement VALD-09.

This constant is not a statement that L1 gives nothing. L1 quantities transfer
at full value -- the 2.92 +/- 0.01 m w.e. overburden, the 1.41 +/- 0.02 muon
attenuation factor, the Table 4 surface fluxes with their normalization
uncertainties, the measured VNS gamma ambience, and the passive shield stack's
material attenuation. They transfer as INPUTS to the wafer's own fold, or as
attenuation of the incident field, never as a rejection credit multiplied onto a
background rate. The rejection credit is therefore 1.0 for L1 rows too, and the
distinction is carried in each row's ``transfers_as`` field rather than in the
credit.

Two L1 rows carry a specific caveat: the ~50 (5 cm Pb) and ~10 (other passives)
factors are published as EVENT-RATE reductions in CaWO4 detectors, so they embed
a target response. They may be transferred as attenuation of the incident
fluence and must not be applied as a rate reduction for germanium.
"""

CONSTANT_DOC_KEYS = ("L2_CREDIT", "L1STAR_CREDIT", "L1_REJECTION_CREDIT")
"""Names of the three credit constants, for the test-suite sentinel checks."""

# --------------------------------------------------------------------------- #
# Closed vocabularies                                                          #
# --------------------------------------------------------------------------- #

TIERS = ("L1", "L1*", "L2")
"""The three tiers. See GPD/analysis/VETO-TAXONOMY.md section 2."""

CREDIT_BASES = ("policy", "derivation", "not-a-rejection-factor", "context")
"""Closed vocabulary for how a row's credit was arrived at.

``policy``
    The rejection exists in NUCLEUS's configuration but is not transferable, so
    this project declines to take it (VALD-09 default).
``derivation``
    The rejection is DERIVED to be identically zero for this payload. Exactly
    one row: ``row-b02-multiplicity-cut``, from Plan 08-02.
``not-a-rejection-factor``
    The statement is not a rejection or attenuation factor at all and has no
    credit to give.
``context``
    The statement qualifies another row's factor rather than being an
    independent factor.
"""

# --------------------------------------------------------------------------- #
# Rows                                                                         #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class TaxonomyRow:
    """One classified NUCLEUS statement.

    The verbatim sentence itself is NOT stored here. It lives in
    ``GPD/analysis/VETO-TAXONOMY.md`` under ``row_id``, with its recorded
    ``grep -o -F`` command, and in
    ``GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md``
    under ``evidence``. Keeping the quotes out of code keeps every NUCLEUS
    rejection number out of the package namespace, which is what makes the
    repository guard in ``tests/test_veto_credit.py`` decidable.
    """

    row_id: str
    tier: str
    credit: float
    credit_basis: str
    section: str
    evidence: str
    subject: str
    transfers_as: str
    note: str

    def __post_init__(self) -> None:
        if self.tier not in TIERS:
            raise ValueError(f"{self.row_id}: tier {self.tier!r} not in {TIERS}")
        if self.credit_basis not in CREDIT_BASES:
            raise ValueError(
                f"{self.row_id}: credit_basis {self.credit_basis!r} not in {CREDIT_BASES}"
            )
        if self.credit != 1.0:
            raise ValueError(
                f"{self.row_id}: credit {self.credit!r} != 1.0. Raising a transferable "
                "veto credit above 1.0 requires a wafer-specific veto geometry and a "
                "documented argument (VALD-09, fp-veto-credit-transfer)."
            )


def _row(
    row_id: str,
    tier: str,
    credit_basis: str,
    section: str,
    evidence: str,
    subject: str,
    transfers_as: str,
    note: str,
) -> TaxonomyRow:
    """Build a row. The credit is not an argument -- it is 1.0, always."""
    return TaxonomyRow(
        row_id=row_id,
        tier=tier,
        credit=1.0,
        credit_basis=credit_basis,
        section=section,
        evidence=evidence,
        subject=subject,
        transfers_as=transfers_as,
        note=note,
    )


_ROWS: tuple[TaxonomyRow, ...] = (
    # ---------------- L1: environmental, transfers ---------------------------
    _row(
        "row-e11-overburden",
        "L1",
        "not-a-rejection-factor",
        "4.1",
        "E.1.1",
        "omnidirectional overburden at the VNS (simulated overburden-map average)",
        "environmental input, at its published value with its published uncertainty",
        "Swap the payload and the rock above the VNS is unchanged. Verified verbatim "
        "by Plan 08-01. Note the section also carries a second, MEASURED overburden "
        "value from the cosmic wheel; they are consistent but are not the same "
        "measurement.",
    ),
    _row(
        "row-e12-muon-attenuation",
        "L1",
        "not-a-rejection-factor",
        "4.1",
        "E.1.2",
        "omnidirectional surface-to-VNS muon attenuation factor",
        "environmental input, at its published value; an INTEGRAL-FLUX factor",
        "A measured muon count-rate ratio is a property of the overburden, not of "
        "what sits in the cryostat. Used by wafer_self_veto.r_mu_underground_Hz(). "
        "Caveat carried from Plan 08-02: it is an integral-flux factor while the "
        "angular distribution also hardens with depth, so a deposit-spectrum re-fold "
        "at depth is owed by Phase 15.",
    ),
    _row(
        "row-e13-table4-fluxes",
        "L1",
        "not-a-rejection-factor",
        "Table 4 (in 5.1)",
        "E.1.3",
        "surface-normalized atmospheric muon and neutron fluxes and material "
        "radioactivity, with their normalization uncertainties",
        "environmental inputs, with their published normalization uncertainties",
        "Simulation inputs; replacing the payload does not move them. Verified "
        "verbatim against arXiv v1 only -- the published EPJC HTML serves the Table 4 "
        "numeric body behind a 'Full size table' link (Plan 08-01 section E.2).",
    ),
    _row(
        "row-e13-vns-gamma-ambience",
        "L1",
        "not-a-rejection-factor",
        "Table 4 (in 5.1)",
        "E.1.3",
        "measured environmental gamma-ray ambience at the VNS",
        "environmental input, at its published value with its published uncertainty",
        "A measured room ambience does not know which detector is installed. "
        "Consumed by Phase 15 (CALC-19).",
    ),
    _row(
        "row-a08-external-shield-stack",
        "L1",
        "policy",
        "2",
        "A.8",
        "external shielding stack: plastic-scintillator muon veto, low-radioactivity "
        "Pb, and boron-loaded HDPE, at their published thicknesses",
        "the MATERIAL STACK, as attenuation of the incident field re-applied to the "
        "wafer's own fold",
        "Swap the payload and the same thicknesses of the same materials still "
        "attenuate the incident field; only the resulting rate, which is a target "
        "property, changes. The muon veto's ACTIVE function is a separate row "
        "(row-b09-mv-cov-muon-induced), not this one.",
    ),
    _row(
        "row-b10-pb-factor-50",
        "L1",
        "policy",
        "5.2.2",
        "B.10",
        "the Pb gamma shield's published event-rate reduction, and the additional "
        "reduction from the rest of the setup's passive materials",
        "FLUENCE ATTENUATION ONLY -- never as a rate reduction for germanium",
        "The published factors are EVENT-RATE reductions in CaWO4 target detectors, "
        "so they embed a target response as well as a material attenuation. The "
        "material attenuation transfers; the rate reduction does not. This row is "
        "also the trade-off whose other leg is the COV -- see the baseline framing in "
        "GPD/analysis/VETO-TAXONOMY.md section 6.",
    ),
    # ---------------- L1*: passive but payload-geometry-coupled --------------
    _row(
        "row-a09-internal-shielding-b4c",
        "L1*",
        "policy",
        "2",
        "A.9",
        "the internal shielding, including the nearly-4pi boron carbide layer and the "
        "cold muon veto",
        "nothing",
        "The internal shield sits inside the cryostat and is arranged around the "
        "payload; swap in a 103.23 cm^2 wafer and the arrangement itself would have "
        "to change. Passive material, but its dimensions are set by what it encloses "
        "-- hence L1*, not L1 (fp-l1star-promotion).",
    ),
    _row(
        "row-b04-b4c-attenuation-factor5",
        "L1*",
        "policy",
        "5.2.1",
        "B.4",
        "the boron carbide liner's published suppression of CaWO4 event rates",
        "nothing",
        "This is one of THREE distinct factor-5 statements in section 5.2.1 and is "
        "the PASSIVE one. It is quoted for a nearly-4pi liner in the direct vicinity "
        "of a centimetre-scale payload, so its value is coupled to the very payload "
        "dimension under dispute. Promoting it to L1 would flatter the background "
        "budget at exactly the point where the wafer's size is the problem.",
    ),
    # ---------------- L2: payload-coupled active rejection -------------------
    _row(
        "row-b01-veto-thresholds",
        "L2",
        "policy",
        "5.1",
        "B.1",
        "the energy thresholds defining an MV hit, a COV hit, an IV hit and a target "
        "detector hit",
        "nothing",
        "Thresholds are the operating point of detectors the wafer does not have. The "
        "COV threshold is electron-equivalent (keV_ee), not bare keV; quoting it "
        "without the subscript is a recorded convention trap.",
    ),
    _row(
        "row-b02-multiplicity-cut",
        "L2",
        "derivation",
        "5.1",
        "B.2",
        "the full anti-coincidence selection, including the requirement of a hit in "
        "one and only one target detector",
        "nothing",
        "CREDIT 1.0 BY DERIVATION, NOT BY POLICY DEFAULT. Plan 08-02 establishes that "
        "with a single readout channel the one-and-only-one conjunct is satisfied "
        "identically by every event that triggers at all, so the rejection is exactly "
        "zero and the credit is 1 - 0 = 1.0. See src/qpd_potential/wafer_self_veto.py "
        "(mult_rejection, early return under identity comparison) and "
        "multiplicity_rejection_is_zero() below. NUCLEUS themselves assess this cut's "
        "marginal benefit as very marginal (row-b07-iv-plus-one-hit-marginal), which "
        "bounds the ABSOLUTE cost of the wafer's zero and cuts against this project's "
        "own framing.",
    ),
    _row(
        "row-b03-geant4-quenching-downscale",
        "L2",
        "not-a-rejection-factor",
        "5.2.1",
        "B.3",
        "a Geant4 modelling downscaling of simulated deposited energies inside the COV "
        "and MV volumes, for nuclear-recoil quenching",
        "nothing",
        "NOT A REJECTION FACTOR. This is one of the three distinct factor-5 statements "
        "in section 5.2.1 and it is the one that is not a rejection at all: it REDUCES "
        "the credited veto response in their simulation. An LLM summarizer asked for "
        "'factor 5' during this project's research returned THIS statement, which "
        "would have silently converted a Monte Carlo caveat into a claimed veto "
        "factor. It is catalogued precisely so that mistake is not repeatable.",
    ),
    _row(
        "row-b05-cov-neutron-anticoincidence",
        "L2",
        "policy",
        "5.2.1",
        "B.5",
        "the COV anti-coincidence reduction of neutron-induced backgrounds",
        "nothing",
        "This is the third of the three distinct factor-5 statements in section 5.2.1 "
        "and the genuine L2 one: the cryogenic outer veto operating in anti-coincidence "
        "around gram-scale crystals at an electron-equivalent threshold. The wafer has "
        "no COV. Adopting this number would be asserting a veto that has not been "
        "designed (fp-veto-credit-transfer).",
    ),
    _row(
        "row-b06-cov-threshold-cost",
        "L2",
        "context",
        "5.2.1",
        "B.6",
        "the cost in neutron-rejection performance of raising the COV threshold",
        "nothing",
        "This is the sensitivity of row-b05-cov-neutron-anticoincidence to the COV "
        "operating point, not an independent factor; with that credit at 1.0 there is "
        "nothing for it to act on. Retained because it shows NUCLEUS themselves treat "
        "the rejection as configuration-dependent rather than environmental.",
    ),
    _row(
        "row-b07-iv-plus-one-hit-marginal",
        "L2",
        "context",
        "5.2.1",
        "B.7",
        "NUCLEUS's own assessment of the marginal benefit of the IV plus the "
        "single-target-hit requirement",
        "nothing -- but it BOUNDS the absolute cost of row-b02-multiplicity-cut's zero",
        "Reported because it cuts AGAINST this project's 'we lose their multiplicity "
        "cut' framing: because the handle they gain is itself marginal, the absolute "
        "background cost of the wafer's identically-zero multiplicity handle is small. "
        "The rejection is exactly zero AND its consequence is small; both stand "
        "together.",
    ),
    _row(
        "row-b08-478kev-boron-line",
        "L2",
        "policy",
        "5.2.1",
        "B.8",
        "the 478 keV gamma line from neutron capture on boron-10, described as harmless "
        "because it is shielded and vetoed by the COV crystals",
        "the BACKGROUND transfers; the REJECTION does not",
        "The line is emitted by the boron carbide liner, which would be inherited with "
        "the shield; the COV that makes it harmless would not be. This is the one row "
        "where something transfers in the WRONG direction: an inherited background "
        "with its rejection removed. Phase 14 owns the resulting unrejected Compton "
        "continuum in the wafer.",
    ),
    _row(
        "row-b09-mv-cov-muon-induced",
        "L2",
        "policy",
        "5.2.1",
        "B.9",
        "the combined MV and COV rejection of muon-INDUCED backgrounds in the CEvNS "
        "region of interest",
        "nothing",
        "The phrase 'muon-induced' is inside the source's own quotation. This is "
        "rejection of muon-induced SECONDARIES, not a through-going-muon tagging "
        "efficiency -- a different observable. It is earned by a plastic-scintillator "
        "muon veto plus a six-crystal HPGe outer veto surrounding the target; the "
        "wafer has neither. The wafer's own direct self-tagging acceptance is derived "
        "separately in Plan 08-02 (a_self_direct), and its induced-secondary "
        "acceptance is a named exact zero (A_SELF_INDUCED). Reading this percentage as "
        "a tagging efficiency is what makes it look inheritable; it is not.",
    ),
    _row(
        "row-b11-cov-gamma-essential",
        "L2",
        "policy",
        "5.2.2",
        "B.11",
        "the essential role of the COV in reducing the environmental gamma-ray "
        "contribution",
        "nothing",
        "A statement about the indispensability of a detector the wafer does not have. "
        "It is also load-bearing for the baseline framing: NUCLEUS's passive gamma "
        "shield is thin BECAUSE the COV is there, which is why dropping the vetoes "
        "while keeping the shield is a worse configuration rather than a subset of "
        "theirs.",
    ),
    _row(
        "row-b12-iv-insensitive-to-gammas",
        "L2",
        "policy",
        "5.2.2",
        "B.12",
        "the IV's insensitivity to environmental gamma rays and its lack of "
        "improvement to that rejection",
        "nothing",
        "A statement that one of NUCLEUS's own vetoes contributes nothing against "
        "gammas. It is still an L2-device statement, and its credit was never anything "
        "but 1.0. Catalogued so that the IV is not credited by association with "
        "row-a12-iv-surface-holder.",
    ),
    _row(
        "row-a12-iv-surface-holder",
        "L2",
        "policy",
        "2",
        "A.12",
        "the inner veto's purpose of rejecting surface events and holder-related events",
        "nothing",
        "Surface- and holder-event rejection for gram-scale crystals in a "
        "TES-instrumented silicon holder. The wafer's mounting and its ~10,300 sensor "
        "films on one instrumented face are a different object. The wafer's spatial "
        "handle is named and left explicitly uncredited in v2.0 "
        "(fp-spatial-handle-credit).",
    ),
)

TAXONOMY: dict[str, TaxonomyRow] = {row.row_id: row for row in _ROWS}
"""Every row of GPD/analysis/VETO-TAXONOMY.md, keyed by its stable row id."""


# --------------------------------------------------------------------------- #
# Lookup                                                                       #
# --------------------------------------------------------------------------- #


def lookup(row_id: str) -> TaxonomyRow:
    """Return the taxonomy row for ``row_id``.

    Raises
    ------
    KeyError
        If ``row_id`` is not a catalogued statement. This is deliberate: a
        downstream code path may not obtain a rejection credit without naming a
        statement that Phase 8 actually classified.
    """
    try:
        return TAXONOMY[row_id]
    except KeyError:
        raise KeyError(
            f"{row_id!r} is not a catalogued NUCLEUS rejection or attenuation "
            "statement. A rejection credit may only be requested by naming a row of "
            "GPD/analysis/VETO-TAXONOMY.md. Known ids: "
            + ", ".join(sorted(TAXONOMY))
        ) from None


def tier_of(row_id: str) -> str:
    """Return ``'L1'``, ``'L1*'`` or ``'L2'`` for a catalogued statement."""
    return lookup(row_id).tier


def credit_for(row_id: str) -> float:
    """Return the transferable rejection credit for a catalogued statement.

    Always 1.0, i.e. the background is unchanged and no rejection is taken. The
    function exists so that the 1.0 is retrieved by NAME rather than typed into
    a formula, and so that any future change to a credit is a diff in this file.
    """
    return lookup(row_id).credit


def rows_in_tier(tier: str) -> tuple[TaxonomyRow, ...]:
    """Return every catalogued row in ``tier``."""
    if tier not in TIERS:
        raise ValueError(f"tier {tier!r} not in {TIERS}")
    return tuple(row for row in _ROWS if row.tier == tier)


def multiplicity_rejection_is_zero() -> bool:
    """Re-check Plan 08-02's derivation that a single-readout target has no cut.

    ``row-b02-multiplicity-cut`` is the one row whose credit of 1.0 is derived
    rather than defaulted. This function CONSUMES that derivation -- it calls
    ``wafer_self_veto.mult_rejection(1)`` and compares to 0.0 under identity --
    instead of restating the result here, so the two modules cannot drift apart
    silently.
    """
    from . import wafer_self_veto

    return wafer_self_veto.mult_rejection(1) == 0.0
