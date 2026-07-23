# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# NUCLEUS veto-envelope geometry: sourced dimension constants, wafer coverage /
# bounding-box requirements, and signed clearances with sign-robustness testing.
#
# Phase 8 (Veto-Envelope Geometry Gate, P-VETO), Plan 08-03, Task 1.
#
# PROVENANCE RULE (binding for this module).
#   Every NUCLEUS dimension constant is registered in GEOMETRY_CONSTANTS (lengths)
#   or AREA_CONSTANTS (areas) as a `SourcedLength` / `SourcedArea` carrying
#     (a) a source string naming the arXiv id, version, and section or caption,
#         traced to a numbered entry of
#         GPD/phases/08-veto-envelope-geometry-gate-p-veto/08-01-SOURCE-EVIDENCE.md, and
#     (b) a stated precision half-width derived from the significant figures of
#         the published value.
#   A constant missing either is a defect; tests/test_veto_envelope.py enforces both.
#
# UNIT RULE. Every NUCLEUS value is published in mm or cm; the mm -> cm conversion
# happens EXACTLY ONCE, at the constant definition, and the native published token
# is retained inside the constant's `native` field. All module-facing lengths are cm.
#
# WAFER RULE. The wafer side of every comparison comes from
# src/qpd_potential/wafer_geometry.py (which in turn is locked to
# GPD/CONVENTIONS.md section D). It is not restated or adjusted here.
#
# SIGN CONVENTION. clearance C = D_available - W_required, in cm.
#   C < 0 denotes a SHORTFALL of |C| cm.  C > 0 denotes headroom.
#
# ---------------------------------------------------------------------------
# ORIENTATION NOTE — a retracted result this module deliberately does NOT encode.
#   08-RESEARCH.md section F1 originally asserted min_{R in SO(3)} b2(R) = a,
#   i.e. that no orientation relaxes the two-orthogonal-dimensions requirement.
#   THAT LEMMA IS FALSE and is retracted (see the dated correction at 08-RESEARCH.md
#   section F1 and Pitfall 7). Reorientation DOES relax the bounding box:
#   a 45 deg tilt about an in-plane axis gives a 10.160 x 7.326 x 7.326 cm box.
#   What survives orientation is the PROJECTION floor sqrt(a^2 + t^2), not a.
#   Accordingly there is no `required_cavity_dims()` here returning an
#   orientation-invariant floor of `a`; that helper is deliberately absent.
# ---------------------------------------------------------------------------

from __future__ import annotations

import math
from dataclasses import dataclass

from . import wafer_geometry

# --------------------------------------------------------------------------- #
# Sourced-quantity containers                                                  #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class SourcedLength:
    """A length in cm that cannot exist without provenance and a precision interval.

    Attributes
    ----------
    cm : float
        Value in cm. Converted from the native published unit exactly once, here.
    native : str
        The published token verbatim, in its native unit (e.g. "100 mm").
    source : str
        arXiv id + version + section or caption, plus the 08-01 evidence-block entry.
    sig_figs : int
        Significant figures of the published value as printed.
    precision_half_width_cm : float
        Rounding half-width implied by `sig_figs`. The tightest defensible interval.
    wider_half_width_cm : float | None
        A deliberately wider, more conservative reading, taken where a second
        published statement of a PLAUSIBLY RELATED quantity carries fewer
        significant figures. QUALIFIED 2026-07-22 (Phase-8 gap G3): this field
        does NOT assert that the two statements describe the same object -- see
        COV_CRYSTAL_DIAMETER_CM's note, where that identity is explicitly
        retired. The wider reading is used only to WIDEN a sign-robustness
        interval, which is conservative against the module's own conclusions.
    note : str
        Anything a later reader must know before quoting the number.
    """

    cm: float
    native: str
    source: str
    sig_figs: int
    precision_half_width_cm: float
    wider_half_width_cm: float | None = None
    note: str = ""


@dataclass(frozen=True)
class SourcedArea:
    """An area in cm^2 with the same provenance discipline as SourcedLength."""

    cm2: float
    native: str
    source: str
    sig_figs: int
    precision_half_width_cm2: float
    note: str = ""


# --------------------------------------------------------------------------- #
# NUCLEUS published dimensions                                                 #
# --------------------------------------------------------------------------- #

_COV_CRYSTAL_DIAMETER = SourcedLength(
    cm=100.0 / 10.0,  # 100 mm -> 10.0 cm; the ONLY mm->cm conversion for this value
    native="100 mm diameter",
    source=(
        "arXiv:2508.02488v1 section 2 'Cryogenic Outer Veto' "
        "(08-01-SOURCE-EVIDENCE.md A.1); independently corroborated by "
        "arXiv:1905.10258 (EPJC 79, 1018 (2019)) Fig. 8 caption "
        "'an outer veto (3) with a diameter of 10 cm' (08-01 A.13)"
    ),
    sig_figs=2,
    precision_half_width_cm=0.05,
    wider_half_width_cm=0.5,
    note=(
        "CORRECTED 2026-07-22 (Phase-8 verification gap G3). This note previously "
        "called the 2019 'a diameter of 10 cm' and the 2508 '100 mm diameter' "
        "'two published statements of the same quantity'. THAT IS RETIRED AS "
        "UNSUPPORTED. The 2019 Fig. 8 caption attributes its 10 cm to component "
        "(3), which the SAME paper defines as 'a surrounding kg-scale cryogenic "
        "detector used as outer veto' (08-01 A.19) -- i.e. plausibly the OUTER-VETO "
        "ASSEMBLY, not one cap crystal. The 2508 '100 mm' describes ONE CYLINDRICAL "
        "CRYSTAL. Nothing published establishes that these are the same object. "
        "WHAT CAN HONESTLY BE SAID: two papers six years and two setup generations "
        "apart both place the outer veto's characteristic diameter at 10 cm. "
        "DIRECTION CHECK: if the 2019 10 cm is the ASSEMBLY extent, the cap "
        "crystals and the cavity are STRICTLY SMALLER than 10 cm, so every "
        "clearance becomes more negative -- the ambiguity is CONSERVATIVE for the "
        "no-fit verdict. What it costs is the claim of INDEPENDENT corroboration. "
        "PRECISION: '100 mm' is 2 s.f. (half-width 0.05 cm); 'a diameter of 10 cm' "
        "is 1 s.f. (half-width 0.5 cm), retained as the deliberately wider reading. "
        "WHAT ACTUALLY LICENSES THE 100 mm READ: the 08-01 C.1 mass closure, "
        "rho_Ge * pi * (5.0 cm)^2 * (2.5 cm) = 1045.2 g at rho_Ge = 5.323, "
        "consistent with the published 1-significant-figure '1 kg' -- NOT the 2019 "
        "caption. "
        "SOURCE CAVEAT: arXiv:2508.02488 is a TUM COMMISSIONING paper, not Chooz, "
        "and is not in the GPD/ROADMAP.md Phase-8 anchor list; it is promoted to a "
        "Phase-8 anchor by 08-01 section D. SHARPENED 2026-07-22 (gap G2): the "
        "paper states that its PASSIVE SHIELDING 'is identical to the configuration "
        "planned for Chooz, with just one exception' (08-01 A.18) and makes NO "
        "equivalent statement about the COV. So the 297 mm and 430 mm ARE Chooz "
        "dimensions by the paper's own words, while THIS 100 mm sits OUTSIDE the "
        "only explicit transfer claim the source makes. That points AGAINST the "
        "transfer, and is recorded as a disconfirming observation."
    ),
)

_COV_CRYSTAL_THICKNESS = SourcedLength(
    cm=25.0 / 10.0,  # 25 mm -> 2.5 cm
    native="25 mm height (2508.02488v1) / '2.5 cm thick' (2509.03559v1)",
    source=(
        "arXiv:2508.02488v1 section 2 'Cryogenic Outer Veto' (08-01 A.1) and "
        "arXiv:2509.03559v1 (EPJC 86, 29 (2026)) section 2 (08-01 A.10): "
        "'two cylindrical and four rectangular 2.5 cm thick HPGe crystals'"
    ),
    sig_figs=2,
    precision_half_width_cm=0.05,
    note=(
        "The only COV dimension the ROADMAP's named Success-Criterion-1 source "
        "(EPJC 86, 29) contains. Two papers, one number: 25 mm == 2.5 cm."
    ),
)

_INTERNAL_SHIELD_DIAMETER = SourcedLength(
    cm=297.0 / 10.0,  # 297 mm -> 29.7 cm
    native="a diameter of 297 mm",
    source="arXiv:2508.02488v1 section 2 'Passive shielding' (08-01 A.2)",
    sig_figs=3,
    precision_half_width_cm=0.05,
    note=(
        "The string '297' does NOT occur as a dimension in arXiv:2509.03559v1 "
        "(it appears there only inside bibliography DOI/URL strings; 08-01 F.7). "
        "ADDED 2026-07-22 (Phase-8 verification gap G2): this dimension IS a Chooz "
        "dimension by the source's own explicit statement -- 'the passive shielding "
        "described above -- and commissioned in this work -- is identical to the "
        "configuration planned for Chooz, with just one exception: an additional "
        "boron carbide (B4C) layer surrounding the target detectors' (08-01 A.18). "
        "The named exception is already carried independently as B4C_THICKNESS_CM "
        "(08-01 A.9). Unlike COV_CRYSTAL_DIAMETER_CM, this constant does NOT rest "
        "on an unstated commissioning-to-Chooz transfer."
    ),
)

_B4C_THICKNESS = SourcedLength(
    cm=4.0,
    native="nearly 4pi 4-cm thick boron carbide (B4C) layer",
    source="arXiv:2509.03559v1 (EPJC 86, 29 (2026)) section 2 (08-01 A.9)",
    sig_figs=1,
    precision_half_width_cm=0.5,
    note="1 significant figure as printed; the half-width is correspondingly wide.",
)

_CRYOSTAT_BORE = SourcedLength(
    cm=430.0 / 10.0,  # 430 mm -> 43.0 cm
    native="a cylindrical opening (430 mm in diameter)",
    source="arXiv:2508.02488v1 section 2 'Passive shielding' (08-01 A.3)",
    sig_figs=2,
    precision_half_width_cm=0.5,
    note=(
        "'430 mm' has an ambiguous trailing zero; read as 2 s.f. (nearest 10 mm), "
        "giving a half-width of 5 mm = 0.5 cm. Not used in any clearance; recorded "
        "for completeness of the published envelope stack."
    ),
)

# --- Derived cavity bounds. TWO separately named constants, never merged. ----

_COV_CAVITY_TIGHT = SourcedLength(
    cm=_COV_CRYSTAL_DIAMETER.cm - 2.0 * _COV_CRYSTAL_THICKNESS.cm,
    native="derived: 100 mm - 2 x 25 mm",
    source=(
        "DERIVED from arXiv:2508.02488v1 section 2 (100 mm cap outer diameter, "
        "08-01 A.1) and arXiv:2509.03559v1 section 2 (2.5 cm rectangular-crystal "
        "thickness, 08-01 A.10). Not a published dimension."
    ),
    sig_figs=2,
    precision_half_width_cm=(
        _COV_CRYSTAL_DIAMETER.precision_half_width_cm
        + 2.0 * _COV_CRYSTAL_THICKNESS.precision_half_width_cm
    ),
    note=(
        "TIGHT bound, an ESTIMATE. Derivation: D_cavity <~ D_cyl - 2 t_rect = "
        "10.0 - 2(2.5) = 5.0 cm. ASSUMPTION: the four rectangular 2.5 cm slabs sit "
        "INSIDE the rim of the 10 cm cylindrical caps. If the rectangular crystals "
        "are larger than the caps -- plausible for hermetic coverage of a stacked "
        "two-module payload -- the cavity could exceed 5 cm and this bound fails. "
        "No clearance built on this constant may be presented as decisive."
    ),
)

_COV_CAVITY_LOOSE = SourcedLength(
    cm=(
        _INTERNAL_SHIELD_DIAMETER.cm
        - 2.0 * _B4C_THICKNESS.cm
        - 2.0 * _COV_CRYSTAL_THICKNESS.cm
    ),
    native="derived: 297 mm - 2 x 40 mm - 2 x 25 mm",
    source=(
        "DERIVED from arXiv:2508.02488v1 section 2 (297 mm internal shielding, "
        "08-01 A.2), arXiv:2509.03559v1 section 2 (4 cm B4C layer, 08-01 A.9; "
        "2.5 cm crystal thickness, 08-01 A.10). Not a published dimension."
    ),
    sig_figs=3,
    precision_half_width_cm=(
        _INTERNAL_SHIELD_DIAMETER.precision_half_width_cm
        + 2.0 * _B4C_THICKNESS.precision_half_width_cm
        + 2.0 * _COV_CRYSTAL_THICKNESS.precision_half_width_cm
    ),
    note=(
        "LOOSE bound: an UPPER bound only, strictly weaker than the tight bound. "
        "Derivation: D_cavity <= D_int.shield - 2 t_B4C - 2 t_rect = "
        "29.7 - 8.0 - 5.0 = 16.7 cm. This bound does NOT exclude the wafer: "
        "16.7 cm exceeds the wafer's 14.368 cm face-parallel coverage requirement. "
        "It must never be used as the verdict basis."
    ),
)

# --------------------------------------------------------------------------- #
# Registry -- the provenance test iterates this, not the module namespace.     #
# --------------------------------------------------------------------------- #

GEOMETRY_CONSTANTS: dict[str, SourcedLength] = {
    "COV_CRYSTAL_DIAMETER_CM": _COV_CRYSTAL_DIAMETER,
    "COV_CRYSTAL_THICKNESS_CM": _COV_CRYSTAL_THICKNESS,
    "INTERNAL_SHIELD_DIAMETER_CM": _INTERNAL_SHIELD_DIAMETER,
    "B4C_THICKNESS_CM": _B4C_THICKNESS,
    "CRYOSTAT_BORE_CM": _CRYOSTAT_BORE,
    "COV_CAVITY_TIGHT_CM": _COV_CAVITY_TIGHT,
    "COV_CAVITY_LOOSE_CM": _COV_CAVITY_LOOSE,
}

# Plain float aliases, each read out of the registry so no float can exist
# without its provenance entry.
COV_CRYSTAL_DIAMETER_CM = GEOMETRY_CONSTANTS["COV_CRYSTAL_DIAMETER_CM"].cm      # 10.0
COV_CRYSTAL_THICKNESS_CM = GEOMETRY_CONSTANTS["COV_CRYSTAL_THICKNESS_CM"].cm    # 2.5
INTERNAL_SHIELD_DIAMETER_CM = GEOMETRY_CONSTANTS["INTERNAL_SHIELD_DIAMETER_CM"].cm  # 29.7
B4C_THICKNESS_CM = GEOMETRY_CONSTANTS["B4C_THICKNESS_CM"].cm                    # 4.0
CRYOSTAT_BORE_CM = GEOMETRY_CONSTANTS["CRYOSTAT_BORE_CM"].cm                    # 43.0
COV_CAVITY_TIGHT_CM = GEOMETRY_CONSTANTS["COV_CAVITY_TIGHT_CM"].cm              # 5.0
COV_CAVITY_LOOSE_CM = GEOMETRY_CONSTANTS["COV_CAVITY_LOOSE_CM"].cm              # 16.7

# --------------------------------------------------------------------------- #
# Areas                                                                        #
# --------------------------------------------------------------------------- #

_ARRAY_CRYSTAL_FOOTPRINT = SourcedArea(
    cm2=9 * (0.5 * 0.5),  # 9 crystals x (5 mm)^2, converted once: 5 mm = 0.5 cm
    native="3 x 3 array of (5 mm)^3 crystals -> 9 x (5 mm)^2",
    source=(
        "arXiv:1905.10258 (EPJC 79, 1018 (2019)) Fig. 8 caption 'two 3 x 3 arrays' "
        "(08-01 A.13) and section 3.2.1 '(5 mm)3 Al2O3 cubic crystal' (08-01 A.15); "
        "the 5 mm edge is independently confirmed by the 08-01 C.2/C.3 mass closures "
        "(4.996 mm and 5.008 mm from the published 6.8 g and 4.5 g array totals)"
    ),
    sig_figs=3,
    precision_half_width_cm2=0.05,
    note="PUBLISHED-crystal-footprint basis. A NUCLEUS number.",
)

_HOLDER_SCALE_FOOTPRINT = SourcedArea(
    cm2=9.0,
    native="~9 cm^2",
    source=(
        "THIS PROJECT'S OWN NOTES, marked as computed (a holder-scale estimate "
        "repeated in GPD/ROADMAP.md). NOT a NUCLEUS number and NOT traceable to "
        "any NUCLEUS publication. See 08-01 C.6."
    ),
    sig_figs=1,
    precision_half_width_cm2=0.5,
    note=(
        "PROJECT holder-scale ESTIMATE. It must never be attributed to NUCLEUS. "
        "It is roughly 4x the published crystal footprint, so the area ratio "
        "differs by a factor of 4 between the two bases -- which is exactly why "
        "area_ratio() refuses to answer without an explicit basis."
    ),
)

AREA_CONSTANTS: dict[str, SourcedArea] = {
    "ARRAY_CRYSTAL_FOOTPRINT_CM2": _ARRAY_CRYSTAL_FOOTPRINT,
    "HOLDER_SCALE_FOOTPRINT_CM2": _HOLDER_SCALE_FOOTPRINT,
}

ARRAY_CRYSTAL_FOOTPRINT_CM2 = AREA_CONSTANTS["ARRAY_CRYSTAL_FOOTPRINT_CM2"].cm2  # 2.25
HOLDER_SCALE_FOOTPRINT_CM2 = AREA_CONSTANTS["HOLDER_SCALE_FOOTPRINT_CM2"].cm2    # 9.0

AREA_RATIO_BASES: tuple[str, ...] = (
    "published_array_crystal_footprint",
    "project_holder_scale_estimate",
)

# --------------------------------------------------------------------------- #
# Wafer geometry (imported, never restated)                                    #
# --------------------------------------------------------------------------- #

WAFER_EDGE_CM = wafer_geometry.LX        # 10.16 cm  (CONVENTIONS section D)
WAFER_THICKNESS_CM = wafer_geometry.LZ   # 0.20 cm
WAFER_FACE_AREA_CM2 = wafer_geometry.LX * wafer_geometry.LY  # 103.2256 cm^2


# --------------------------------------------------------------------------- #
# Wafer requirement quantities                                                 #
# --------------------------------------------------------------------------- #


def cover_diameter_face_parallel(a: float = WAFER_EDGE_CM) -> float:
    """Diameter of the circle circumscribing the a x a wafer face, sqrt(2)*a [cm].

    This is the diameter a circular COV cap crystal must have in order to COVER
    the wafer's projected footprint.

    MOUNTING PREMISE (binding, must be stated wherever this number is quoted):
    the wafer face lies PARALLEL to the COV cap plane, as in every planar
    cryogenic detector stack and as implied by the wafer's single instrumented
    face. Under any other mounting the required diameter is smaller, falling
    continuously to the orientation-invariant floor returned by
    `cover_diameter_min_over_orientations`.

    This is also the true MINIMUM ENCLOSING CYLINDER diameter for a cylinder
    whose axis is normal to the wafer face -- NOT `space_diagonal`, which is the
    enclosing-sphere quantity.

    For a = 10.16 cm this returns 14.3684 cm.
    """
    return math.sqrt(2.0) * a


def cover_diameter_min_over_orientations(
    a: float = WAFER_EDGE_CM, t: float = WAFER_THICKNESS_CM
) -> float:
    """Orientation-invariant floor on the projected-footprint diameter, sqrt(a^2+t^2) [cm].

    The minimum over SO(3) of the diameter of the wafer's shadow on the cap
    plane, attained EDGE-ON (wafer face normal lying in the cap plane), where the
    shadow is an a x t rectangle of diagonal sqrt(a^2 + t^2).

    This requires NO mounting assumption at all. It rises to sqrt(2)*a when the
    face is parallel to the cap plane. It is what makes the coverage basis's
    robustness mounting-conditional rather than purely geometric.

    For a = 10.16 cm, t = 0.20 cm this returns 10.1620 cm.
    """
    return math.hypot(a, t)


def space_diagonal(a: float = WAFER_EDGE_CM, t: float = WAFER_THICKNESS_CM) -> float:
    """Space diagonal sqrt(2a^2 + t^2) [cm] -- the ENCLOSING-SPHERE diameter.

    RENAMED from `min_enclosing_cylinder_diameter`, which was a MISNOMER. The
    minimum enclosing cylinder of the wafer (axis normal to the face) has the
    FACE-diagonal diameter sqrt(2)*a = 14.3684 cm, not the space diagonal
    14.3698 cm. The two differ by 0.0014 cm, which is why the misnomer survived
    unnoticed in 08-RESEARCH.md section F1.

    THIS FUNCTION MUST NOT BE USED AS A COVERAGE REQUIREMENT. It is retained
    solely because it is independently unit-tested against
    `wafer_geometry.CHORD_DIAGONAL`, which gives the coverage arithmetic an
    external cross-check.

    For a = 10.16 cm, t = 0.20 cm this returns 14.3698 cm.
    """
    return math.sqrt(2.0 * a * a + t * t)


def min_bbox_second_side(
    a: float = WAFER_EDGE_CM, t: float = WAFER_THICKNESS_CM
) -> float:
    """Minimum over SO(3) of the SECOND-LARGEST axis-aligned bounding-box side, (a+t)/sqrt(2) [cm].

    Attained at a 45 degree tilt about an in-plane axis, where the bounding box is
    a x (a+t)/sqrt(2) x (a+t)/sqrt(2) = 10.160 x 7.326 x 7.326 cm.

    THIS RETRACTS 08-RESEARCH.md section F1, which claimed this minimum equals `a`
    (i.e. that no orientation relaxes the two-orthogonal-dimensions requirement).
    It does not. Reorientation genuinely relaxes the bounding-box requirement.

    Uniform SO(3) sampling approaches this infimum FROM ABOVE without reaching it,
    so any numerical check must be a one-sided lower bound plus an exact evaluation
    at the attaining orientation.

    SAMPLED REFERENCE VALUE, CORRECTED 2026-07-22 (Phase-8 verification gap G4).
    This docstring previously quoted 7.4210 cm. That figure came from a PRE-EXECUTION
    PLANNING reference run, not from the Plan-08-03 execution run. The two are
    different draws, not a transcription slip -- the same planning run reported a
    minimum projected diameter of 10.2039 cm where the execution run gives 10.1623 cm,
    and no transcription error moves that. The CANONICAL run is the one produced by
    the sampling code in tests/test_veto_envelope.py -- Rotation.random(200_000,
    random_state=20260722) -- re-run during the gap closure and reproducing exactly:

        min b1 = 9.7076,  min b2 = 7.3945,  min projected diameter = 10.1623  [cm]
        (numpy 1.26.4, scipy 1.17.1, Python 3.11.7, Darwin 25.3.0 arm64)

    Non-load-bearing either way: no clearance uses a sampled value, and both draws
    satisfy the one-sided lower-bound assertions.

    For a = 10.16 cm, t = 0.20 cm this returns 7.3256 cm.
    """
    return (a + t) / math.sqrt(2.0)


def min_bbox_largest_side(a: float = WAFER_EDGE_CM) -> float:
    """Prince-Rupert ZERO-THICKNESS lower bound on the largest bbox side, a/(3 sqrt(2)/4) [cm].

    IMPORTANT LABELLING. This is the t -> 0 limit: the smallest cube into which a
    zero-thickness a x a square can be fitted has side a/(3 sqrt(2)/4) = 0.9428*a.
    For the REAL wafer at t = 0.20 cm the attained minimum is LARGER.

    BRACKET TIGHTENED 2026-07-22 (Phase-8 verification gap G5). The upper end was
    previously taken from uniform sampling (~9.71-9.72 cm), which approaches an
    infimum from above and is therefore a poor upper bound. DIRECT OPTIMIZATION
    ATTAINS THE MINIMUM: multistart Nelder-Mead over SO(3) (400 random starts,
    xatol=1e-12, fatol=1e-14) converges to

        min b1 = 9.666923 cm

    at an orientation where the bounding box is a CUBE (9.666923^3) -- the expected
    signature of the smallest enclosing cube. The excess over the zero-thickness
    Prince-Rupert bound is +0.0880 cm. Independently reproduced by the Phase-8
    verifier. So:

        the wafer fits inside a cube of side ~ 9.667 cm (attained, by optimization),
        and cannot fit inside a cube of side < 9.5789 cm (Prince-Rupert, t -> 0).

    Quote the cube side as ~ 9.667 cm -- NOT 9.72 cm (a loose sampled value) and
    NOT 9.58 cm (the zero-thickness bound).

    This quantity enters NO clearance and NO assertion in the fit determination.
    It exists only to record honestly how much reorientation buys.

    For a = 10.16 cm this returns 9.5789 cm (the zero-thickness bound, not 9.667).
    """
    return a / (3.0 * math.sqrt(2.0) / 4.0)


# --------------------------------------------------------------------------- #
# Clearance arithmetic                                                         #
# --------------------------------------------------------------------------- #


def clearance(d_available: float, w_required: float) -> float:
    """Signed clearance C = D_available - W_required [cm]; C < 0 is a shortfall."""
    return d_available - w_required


@dataclass(frozen=True)
class SignRobustness:
    """Result of re-evaluating a clearance at the endpoints of its input interval.

    Attributes
    ----------
    nominal_cm, low_cm, high_cm : float
        Clearance at d_available, at d_available - half_width, at d_available + half_width.
    half_width_cm : float
        The rounding half-width applied to `d_available`.
    sign_preserved : bool
        True iff the clearance keeps a single strict sign across the whole interval.
    flip_at_d_cm : float
        The value of `d_available` at which the clearance changes sign (= w_required).
    half_width_to_flip_cm : float
        |flip_at_d_cm - d_available|: the smallest half-width that would break the
        sign. Compare this against `half_width_cm` to see how much margin there is.
    """

    nominal_cm: float
    low_cm: float
    high_cm: float
    half_width_cm: float
    sign_preserved: bool
    flip_at_d_cm: float
    half_width_to_flip_cm: float


def clearance_sign_robust(
    d_available: float, w_required: float, half_width: float
) -> SignRobustness:
    """Re-evaluate a clearance at both endpoints of d_available +/- half_width.

    This is what separates a DECISIVE clearance from one that merely happens to be
    negative at the nominal value. A clearance whose magnitude is comparable to its
    own input rounding interval may not carry a milestone-gating verdict.

    The sign is judged STRICTLY: a clearance that touches zero at an endpoint is
    reported as not sign-preserved.
    """
    if half_width < 0.0:
        raise ValueError("half_width must be non-negative")
    nominal = clearance(d_available, w_required)
    low = clearance(d_available - half_width, w_required)
    high = clearance(d_available + half_width, w_required)
    preserved = (low < 0.0 and high < 0.0) or (low > 0.0 and high > 0.0)
    return SignRobustness(
        nominal_cm=nominal,
        low_cm=low,
        high_cm=high,
        half_width_cm=half_width,
        sign_preserved=preserved,
        flip_at_d_cm=w_required,
        half_width_to_flip_cm=abs(w_required - d_available),
    )


# --------------------------------------------------------------------------- #
# Area ratio -- refuses to answer without an explicit basis                    #
# --------------------------------------------------------------------------- #


def area_ratio(basis: str | None = None) -> float:
    """Wafer face area / reference footprint area [dimensionless].

    `basis` is MANDATORY and must be one of AREA_RATIO_BASES:

      "published_array_crystal_footprint"
          2.25 cm^2 = 9 x (5 mm)^2, the crystal footprint of a published NUCLEUS
          3 x 3 target array (arXiv:1905.10258 Fig. 8 + section 3.2.1, confirmed by
          the 08-01 C.2/C.3 mass closures). Gives ~45.9.

      "project_holder_scale_estimate"
          ~9 cm^2, a HOLDER-SCALE ESTIMATE originating in THIS PROJECT'S OWN NOTES
          marked as computed. It is NOT a NUCLEUS number and must never be
          attributed to NUCLEUS. Gives ~11.5.

    The two bases differ by a factor of 4, so an unlabelled ratio carries false
    provenance. That is why a missing basis is an error rather than a default.
    """
    if basis is None:
        raise ValueError(
            "area_ratio() requires an explicit basis: one of "
            f"{AREA_RATIO_BASES}. An unlabelled wafer-to-array area ratio carries "
            "false provenance (the two bases differ by a factor of 4)."
        )
    if basis == "published_array_crystal_footprint":
        return WAFER_FACE_AREA_CM2 / ARRAY_CRYSTAL_FOOTPRINT_CM2
    if basis == "project_holder_scale_estimate":
        return WAFER_FACE_AREA_CM2 / HOLDER_SCALE_FOOTPRINT_CM2
    raise ValueError(
        f"unknown area-ratio basis {basis!r}; expected one of {AREA_RATIO_BASES}"
    )


# --------------------------------------------------------------------------- #
# The four named comparison bases                                              #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ComparisonBasis:
    """One named clearance comparison, carrying its premise and its provenance."""

    key: str
    label: str
    w_required_cm: float
    w_source: str
    d_available_cm: float
    d_source: str
    premise: str
    clearance_cm: float


def comparison_bases() -> dict[str, ComparisonBasis]:
    """The four named bases of the fit determination, computed (not transcribed).

    Ranked by the strength of their premises: COVERAGE needs only that a cap
    crystal must cover the wafer footprint (plus the face-parallel mounting
    premise); EDGE needs nothing at all; the two CAVITY bases need the cap-rim
    assumption and are therefore estimates.
    """
    d_cap = COV_CRYSTAL_DIAMETER_CM
    cap_src = GEOMETRY_CONSTANTS["COV_CRYSTAL_DIAMETER_CM"].source
    cav_src = GEOMETRY_CONSTANTS["COV_CAVITY_TIGHT_CM"].source
    wafer_src = "GPD/CONVENTIONS.md section D via src/qpd_potential/wafer_geometry.py"

    d_cover = cover_diameter_face_parallel()
    edge = WAFER_EDGE_CM
    d_cav = COV_CAVITY_TIGHT_CM

    bases = [
        ComparisonBasis(
            key="coverage",
            label="Coverage: required cap diameter vs published cap outer diameter",
            w_required_cm=d_cover,
            w_source=f"sqrt(2) * a, {wafer_src}",
            d_available_cm=d_cap,
            d_source=cap_src,
            premise=(
                "THREE premises, corrected 2026-07-22 (Phase-8 verification gap G1); "
                "this string previously stated only two and hid the second. "
                "(i) ASSEMBLY-LEVEL COVERAGE: the COV must cover the wafer footprint. "
                "This is what the published text licenses -- 'The COV is an "
                "arrangement of two cylindrical and four rectangular 2.5 cm thick "
                "HPGe crystals... It hermetically covers the cryogenic target "
                "detectors' (08-01 A.10 + A.11). The grammatical subject of "
                "'hermetically covers' is the SIX-CRYSTAL ARRANGEMENT, not a cap. "
                "(ii) SINGLE-CAP -- AN INFERENCE, NOT PUBLISHED: this requirement is "
                "applied to ONE cylindrical cap. That follows from the published "
                "architecture (six crystals giving nearly-4pi coverage, 08-01 A.20; "
                "two cylindrical + four rectangular, A.10; the crystal installed "
                "'directly above the target detectors' being a CYLINDER, A.1) only "
                "under the further assignment that the two cylinders are the top and "
                "bottom of the enclosure and the four rectangles are its lateral "
                "walls, none overhanging the top. NO PUBLISHED SENTENCE STATES THAT "
                "ASSIGNMENT. It is the SAME assignment COV_CAVITY_TIGHT_CM rests on, "
                "so the two stand or fall together. Derivation with the inferential "
                "step marked: 08-03-FIT-DETERMINATION.md section 3.1. "
                "(iii) MOUNTING: the wafer face is PARALLEL to the cap plane. "
                "No cavity assumption -- that property is unchanged and is why this "
                "basis carries the verdict. "
                "CONSEQUENCE OF (ii) FOR FALSIFIABILITY, NOT DIRECTION: the "
                "overturning threshold has TWO routes, not one. Route A (a published "
                "cap >= 14.3684 cm, implying ~2.06 kg vs a published 1 kg) is "
                "effectively closed by published evidence. Route B (rectangular "
                "crystals projecting over the payload's top face, filling the "
                "24.6858 cm^2 residual out to a 2.1842 cm radial reach beyond the "
                "cap rim) requires NO larger cap and NO anomalous mass, and NOTHING "
                "PUBLISHED EXCLUDES IT -- no source gives the rectangular crystals' "
                "lateral dimensions, placement, or mass. See 08-03 section 9 item 3."
            ),
            clearance_cm=clearance(d_cap, d_cover),
        ),
        ComparisonBasis(
            key="edge",
            label="Edge: wafer in-plane edge vs published cap outer diameter",
            w_required_cm=edge,
            w_source=f"a, {wafer_src}",
            d_available_cm=d_cap,
            d_source=cap_src,
            premise=(
                "None. The wafer is simply wider than an entire cap crystal. "
                "No coverage premise, no mounting premise, no cavity assumption."
            ),
            clearance_cm=clearance(d_cap, edge),
        ),
        ComparisonBasis(
            key="cavity_in_plane",
            label="Cavity, in-plane: wafer edge vs ESTIMATED tight COV cavity",
            w_required_cm=edge,
            w_source=f"a, {wafer_src}",
            d_available_cm=d_cav,
            d_source=cav_src,
            premise=(
                "ESTIMATE. Assumes the four rectangular 2.5 cm slabs sit inside "
                "the rim of the cylindrical caps."
            ),
            clearance_cm=clearance(d_cav, edge),
        ),
        ComparisonBasis(
            key="cavity_diagonal",
            label="Cavity, diagonal: required cap diameter vs ESTIMATED tight COV cavity",
            w_required_cm=d_cover,
            w_source=f"sqrt(2) * a, {wafer_src}",
            d_available_cm=d_cav,
            d_source=cav_src,
            premise=(
                "ESTIMATE. Same cap-rim assumption as the in-plane cavity basis, "
                "plus the face-parallel mounting premise."
            ),
            clearance_cm=clearance(d_cav, d_cover),
        ),
    ]
    return {b.key: b for b in bases}
