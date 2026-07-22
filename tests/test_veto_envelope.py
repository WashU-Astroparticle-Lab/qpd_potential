# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-8 Plan 08-03, Task 1 unit tests: NUCLEUS veto-envelope geometry.

Guards:
  * wafer closure against GPD/CONVENTIONS.md section D (109.9 g, 103.23 cm^2)
  * the five orientation quantities against their closed forms
  * `space_diagonal` against the independently unit-tested wafer_geometry.CHORD_DIAGONAL
  * the TRUE SO(3) minima by uniform rotation sampling, as ONE-SIDED LOWER BOUNDS
    plus exact evaluation at the attaining orientations
  * provenance: every registered constant carries a source string AND a precision
    interval
  * area_ratio() refuses to answer without an explicit basis
  * the four named comparison bases compute (they are not transcribed)

RETRACTED LEMMA -- DO NOT REINSTATE.
  08-RESEARCH.md section F1 claimed min_{R in SO(3)} b2(R) = a = 10.16 cm.
  That is FALSE. The superseded one-sided assertion against `a` (i.e. bounding the
  sampled min b2 below by the wafer edge) must never appear in this
  file: a 45 degree in-plane tilt gives a bounding box of 10.160 x 7.326 x 7.326 cm,
  so it would fail deterministically. The true minimum is (a+t)/sqrt(2) = 7.3256 cm.

SAMPLING DISCIPLINE.
  Uniform SO(3) sampling approaches an attained infimum FROM ABOVE and never
  reaches it (a 2e5-sample reference run gave min b2 = 7.4210 cm and min projected
  diameter = 10.2039 cm against analytic 7.3256 and 10.1620). Every sampled
  assertion here is therefore a ONE-SIDED LOWER BOUND. No equality-against-a-
  sampled-value assertion appears anywhere in this file.

Reproducibility: numpy 1.26.4, scipy 1.17.1, Python 3.11.7, Darwin 25.3.0
(osx-arm64). Rotation seed 20260722, fixed below.
"""
import math

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from qpd_potential import params
from qpd_potential import veto_envelope as ve
from qpd_potential import wafer_geometry as wg

A = 10.16  # cm, wafer in-plane edge (CONVENTIONS section D)
T = 0.20   # cm, wafer thickness

# One-sided-bound tolerance for the sampled SO(3) minima, in cm.
TOL_CM = 1e-3

ROTATION_SEED = 20260722
N_ROTATIONS = 200_000  # >= 1e5 as required by test-orientation-invariance


# --------------------------------------------------------------------------- #
# Wafer closure (CONVENTIONS section D)                                        #
# --------------------------------------------------------------------------- #


def test_wafer_closure_against_conventions_section_d():
    """10.16 x 10.16 x 0.20 cm at rho_Ge = 5.323 g/cm^3 -> 109.9 g, 103.23 cm^2."""
    assert wg.LX == pytest.approx(A, abs=1e-12)
    assert wg.LY == pytest.approx(A, abs=1e-12)
    assert wg.LZ == pytest.approx(T, abs=1e-12)

    volume_cm3 = wg.LX * wg.LY * wg.LZ
    assert volume_cm3 == pytest.approx(20.6451, abs=1e-3)

    rho = params.GE_DENSITY.value
    assert rho == pytest.approx(5.323, abs=1e-9)
    assert rho * volume_cm3 == pytest.approx(109.9, abs=0.05)

    assert ve.WAFER_FACE_AREA_CM2 == pytest.approx(103.23, abs=5e-3)


# --------------------------------------------------------------------------- #
# Closed forms of the five orientation quantities (test-dmin-arithmetic)       #
# --------------------------------------------------------------------------- #


def test_five_orientation_quantities_match_closed_forms():
    assert ve.cover_diameter_face_parallel(A) == pytest.approx(14.3684, abs=1e-4)
    assert ve.cover_diameter_min_over_orientations(A, T) == pytest.approx(
        10.1620, abs=1e-4
    )
    assert ve.space_diagonal(A, T) == pytest.approx(14.3698, abs=1e-4)
    assert ve.min_bbox_second_side(A, T) == pytest.approx(7.3256, abs=1e-4)
    assert ve.min_bbox_largest_side(A) == pytest.approx(9.5789, abs=1e-4)

    # Closed forms, independently of the numerals above.
    assert ve.cover_diameter_face_parallel(A) == pytest.approx(math.sqrt(2.0) * A)
    assert ve.cover_diameter_min_over_orientations(A, T) == pytest.approx(
        math.sqrt(A * A + T * T)
    )
    assert ve.space_diagonal(A, T) == pytest.approx(math.sqrt(2 * A * A + T * T))
    assert ve.min_bbox_second_side(A, T) == pytest.approx((A + T) / math.sqrt(2.0))
    assert ve.min_bbox_largest_side(A) == pytest.approx(A / (3 * math.sqrt(2.0) / 4))


def test_space_diagonal_matches_independent_chord_diagonal():
    """The enclosing-SPHERE quantity, cross-checked against Phase-4's constant."""
    assert ve.space_diagonal(A, T) == pytest.approx(wg.CHORD_DIAGONAL, abs=1e-9)


def test_coverage_requirement_is_not_the_space_diagonal():
    """The minimum enclosing CYLINDER (axis normal to the face) is the FACE diagonal.

    Guards the retired misnomer `min_enclosing_cylinder_diameter`: the two
    quantities differ by 0.0014 cm, which is how the misnomer survived unnoticed.
    """
    face = ve.cover_diameter_face_parallel(A)
    space = ve.space_diagonal(A, T)
    assert space > face
    assert space - face == pytest.approx(0.0014, abs=2e-4)


def test_retracted_helper_is_absent():
    """`required_cavity_dims()` returned an orientation-invariant floor of `a`. Gone."""
    assert not hasattr(ve, "required_cavity_dims")
    assert not hasattr(ve, "min_enclosing_cylinder_diameter")


# --------------------------------------------------------------------------- #
# Orientation invariance by uniform SO(3) sampling (test-orientation-invariance)#
# --------------------------------------------------------------------------- #


def _plate_vertices(a: float, t: float) -> np.ndarray:
    """The 8 vertices of an a x a x t plate centred on the origin."""
    hx, hy, hz = a / 2.0, a / 2.0, t / 2.0
    return np.array(
        [
            [sx * hx, sy * hy, sz * hz]
            for sx in (-1.0, 1.0)
            for sy in (-1.0, 1.0)
            for sz in (-1.0, 1.0)
        ]
    )


def _bbox_sides_sorted(vertices: np.ndarray) -> np.ndarray:
    """Axis-aligned bounding-box side lengths, sorted DESCENDING (b1 >= b2 >= b3)."""
    extents = vertices.max(axis=-2) - vertices.min(axis=-2)
    return np.sort(extents, axis=-1)[..., ::-1]


def _projected_diameter(vertices: np.ndarray) -> np.ndarray:
    """Diameter of the footprint projected onto the xy (cap) plane.

    The projection of a convex polytope is the convex hull of the projected
    vertices, so its diameter is the maximum pairwise distance among them.
    """
    xy = vertices[..., :2]
    diff = xy[..., :, None, :] - xy[..., None, :, :]
    return np.sqrt((diff**2).sum(axis=-1)).max(axis=(-2, -1))


def test_so3_sampled_minima_are_bounded_below_by_the_true_infima():
    """One-sided lower bounds only. tol = 1e-3 cm, stated numerically.

    A sampled value BELOW the analytic infimum would falsify the closed forms.
    A sampled value above it is expected and carries no information by itself,
    which is why the attaining orientations are checked exactly, separately.
    """
    verts = _plate_vertices(A, T)
    rots = Rotation.random(N_ROTATIONS, random_state=ROTATION_SEED)
    mats = rots.as_matrix()  # (N, 3, 3)
    rotated = np.einsum("nij,vj->nvi", mats, verts)  # (N, 8, 3)

    sides = _bbox_sides_sorted(rotated)
    b1_min = float(sides[:, 0].min())
    b2_min = float(sides[:, 1].min())
    proj_min = float(_projected_diameter(rotated).min())

    analytic_b2 = ve.min_bbox_second_side(A, T)       # 7.3256
    analytic_proj = ve.cover_diameter_min_over_orientations(A, T)  # 10.1620
    analytic_b1_zero_t = ve.min_bbox_largest_side(A)  # 9.5789, zero-thickness bound

    # -- the two binding one-sided lower bounds -----------------------------
    assert b2_min >= analytic_b2 - TOL_CM, (
        f"sampled min b2 = {b2_min:.4f} cm fell below the analytic infimum "
        f"{analytic_b2:.4f} cm - {TOL_CM} cm"
    )
    assert proj_min >= analytic_proj - TOL_CM, (
        f"sampled min projected diameter = {proj_min:.4f} cm fell below the "
        f"analytic infimum {analytic_proj:.4f} cm - {TOL_CM} cm"
    )

    # -- the Prince-Rupert bound is ZERO-THICKNESS: the real plate stays above
    assert b1_min >= analytic_b1_zero_t - TOL_CM
    # ...and demonstrably does not attain it at t = 0.20 cm.
    assert b1_min > analytic_b1_zero_t + 0.05
    # The demonstrated cube side: <~ 9.72 cm, NOT 9.58 cm.
    assert b1_min < 9.75

    # -- the sampled minima approach FROM ABOVE (records the discipline) -----
    assert b2_min > analytic_b2
    assert proj_min > analytic_proj


def test_exact_values_at_the_attaining_orientations():
    """The infima are attained: 45 deg in-plane tilt, and edge-on."""
    verts = _plate_vertices(A, T)

    # 45 degrees about the x axis: box is a x (a+t)/sqrt(2) x (a+t)/sqrt(2).
    tilt = Rotation.from_euler("x", 45.0, degrees=True)
    sides = _bbox_sides_sorted(tilt.apply(verts))
    assert sides[0] == pytest.approx(A, abs=1e-9)
    assert sides[1] == pytest.approx(ve.min_bbox_second_side(A, T), abs=1e-9)
    assert sides[2] == pytest.approx(ve.min_bbox_second_side(A, T), abs=1e-9)
    assert sides[1] == pytest.approx(7.3256, abs=1e-4)

    # Edge-on: rotate the face normal (z) into the cap plane -> shadow is a x t.
    edge_on = Rotation.from_euler("x", 90.0, degrees=True)
    assert _projected_diameter(edge_on.apply(verts)) == pytest.approx(
        ve.cover_diameter_min_over_orientations(A, T), abs=1e-9
    )
    assert _projected_diameter(edge_on.apply(verts)) == pytest.approx(10.1620, abs=1e-4)

    # Face-parallel: shadow is the a x a face, diameter sqrt(2)*a.
    identity = Rotation.identity()
    assert _projected_diameter(identity.apply(verts)) == pytest.approx(
        ve.cover_diameter_face_parallel(A), abs=1e-9
    )


def test_reorientation_does_relax_the_bounding_box():
    """The explicit counterexample to the retracted section-F1 lemma."""
    assert ve.min_bbox_second_side(A, T) < A  # 7.3256 < 10.16
    tilt = Rotation.from_euler("x", 45.0, degrees=True)
    sides = _bbox_sides_sorted(tilt.apply(_plate_vertices(A, T)))
    assert sides[1] < A - 2.0  # not marginally smaller: 2.83 cm smaller


# --------------------------------------------------------------------------- #
# Provenance: source string AND precision interval on every constant           #
# --------------------------------------------------------------------------- #


def test_every_geometry_constant_carries_source_and_precision():
    assert ve.GEOMETRY_CONSTANTS, "registry must not be empty"
    for name, c in ve.GEOMETRY_CONSTANTS.items():
        assert c.source and c.source.strip(), f"{name}: empty source string"
        assert ("arXiv:" in c.source), f"{name}: source names no arXiv id"
        assert any(
            tok in c.source
            for tok in ("section", "caption", "Fig.", "08-01")
        ), f"{name}: source names no section/caption/evidence entry"
        assert c.precision_half_width_cm > 0.0, f"{name}: no stated precision interval"
        assert c.native and c.native.strip(), f"{name}: no native published token"
        assert c.sig_figs >= 1
    for name, c in ve.AREA_CONSTANTS.items():
        assert c.source and c.source.strip(), f"{name}: empty source string"
        assert c.precision_half_width_cm2 > 0.0, f"{name}: no precision interval"


def test_float_aliases_all_trace_to_the_registry():
    """No bare geometry float may exist in the module without a registry entry."""
    for name, c in ve.GEOMETRY_CONSTANTS.items():
        assert getattr(ve, name) == pytest.approx(c.cm, abs=1e-12)
    for name, c in ve.AREA_CONSTANTS.items():
        assert getattr(ve, name) == pytest.approx(c.cm2, abs=1e-12)


def test_holder_scale_estimate_is_not_attributed_to_nucleus():
    note = ve.AREA_CONSTANTS["HOLDER_SCALE_FOOTPRINT_CM2"]
    assert "NOT a NUCLEUS number" in note.source
    assert "PROJECT" in note.note


# --------------------------------------------------------------------------- #
# Cavity bounds: two separate constants, never merged                          #
# --------------------------------------------------------------------------- #


def test_tight_and_loose_cavity_bounds_are_separate():
    assert ve.COV_CAVITY_TIGHT_CM == pytest.approx(5.0, abs=1e-9)
    assert ve.COV_CAVITY_LOOSE_CM == pytest.approx(16.7, abs=1e-9)
    # Derivations reproduce from the published constants.
    assert ve.COV_CAVITY_TIGHT_CM == pytest.approx(
        ve.COV_CRYSTAL_DIAMETER_CM - 2 * ve.COV_CRYSTAL_THICKNESS_CM, abs=1e-12
    )
    assert ve.COV_CAVITY_LOOSE_CM == pytest.approx(
        ve.INTERNAL_SHIELD_DIAMETER_CM
        - 2 * ve.B4C_THICKNESS_CM
        - 2 * ve.COV_CRYSTAL_THICKNESS_CM,
        abs=1e-12,
    )
    # No merged cavity constant exists.
    merged = [
        n
        for n in dir(ve)
        if "CAVITY" in n.upper()
        and not n.startswith("_")
        and n not in ("COV_CAVITY_TIGHT_CM", "COV_CAVITY_LOOSE_CM")
    ]
    assert merged == [], f"merged cavity constant(s) found: {merged}"
    # The loose bound does NOT exclude the wafer -- assert the positive clearance.
    assert ve.clearance(ve.COV_CAVITY_LOOSE_CM, ve.cover_diameter_face_parallel()) > 0


# --------------------------------------------------------------------------- #
# Clearances and sign robustness                                               #
# --------------------------------------------------------------------------- #


def test_clearance_sign_convention():
    assert ve.clearance(5.0, 10.16) == pytest.approx(-5.16, abs=1e-9)
    assert ve.clearance(16.7, 14.368409793710647) == pytest.approx(2.3316, abs=1e-3)


def test_four_comparison_bases_compute_with_provenance():
    bases = ve.comparison_bases()
    assert set(bases) == {"coverage", "edge", "cavity_in_plane", "cavity_diagonal"}
    for b in bases.values():
        assert b.premise.strip()
        assert b.d_source.strip()
        assert b.w_source.strip()
        # clearance() is the single definition; each basis must agree with it.
        assert b.clearance_cm == pytest.approx(
            ve.clearance(b.d_available_cm, b.w_required_cm), abs=1e-12
        )
    assert bases["coverage"].clearance_cm == pytest.approx(-4.3684, abs=1e-3)
    assert bases["edge"].clearance_cm == pytest.approx(-0.1600, abs=1e-6)
    assert bases["cavity_in_plane"].clearance_cm == pytest.approx(-5.1600, abs=1e-6)
    assert bases["cavity_diagonal"].clearance_cm == pytest.approx(-9.3684, abs=1e-3)
    # The coverage ratio: the cap is ~30% smaller than required.
    ratio = bases["coverage"].d_available_cm / bases["coverage"].w_required_cm
    assert ratio == pytest.approx(0.6960, abs=1e-3)


def test_sign_robustness_of_the_coverage_basis():
    d_cover = ve.cover_diameter_face_parallel()
    for hw in (0.05, 0.1, 0.5):
        r = ve.clearance_sign_robust(ve.COV_CRYSTAL_DIAMETER_CM, d_cover, hw)
        assert r.sign_preserved, f"coverage lost its sign at half-width {hw}"
        assert r.low_cm < 0 and r.high_cm < 0
    r = ve.clearance_sign_robust(ve.COV_CRYSTAL_DIAMETER_CM, d_cover, 0.2)
    assert r.high_cm == pytest.approx(-4.1684, abs=1e-3)  # cap at 10.2 cm
    assert r.half_width_to_flip_cm == pytest.approx(4.3684, abs=1e-3)


def test_sign_robustness_of_the_edge_basis():
    """The edge clearance is smaller than its own input precision. Not the verdict."""
    r05 = ve.clearance_sign_robust(ve.COV_CRYSTAL_DIAMETER_CM, ve.WAFER_EDGE_CM, 0.05)
    assert r05.sign_preserved
    assert r05.high_cm == pytest.approx(-0.11, abs=1e-9)

    r10 = ve.clearance_sign_robust(ve.COV_CRYSTAL_DIAMETER_CM, ve.WAFER_EDGE_CM, 0.1)
    # Computed, not presupposed: at +/-0.1 the sign IS preserved, but only by
    # 0.06 cm -- less than the half-width itself.
    assert r10.sign_preserved
    assert r10.high_cm == pytest.approx(-0.06, abs=1e-9)
    assert abs(r10.high_cm) < r10.half_width_cm

    # The 1-s.f. reading of the 2019 "a diameter of 10 cm" is +/-0.5 cm: it FLIPS.
    r50 = ve.clearance_sign_robust(ve.COV_CRYSTAL_DIAMETER_CM, ve.WAFER_EDGE_CM, 0.5)
    assert not r50.sign_preserved
    assert r50.high_cm > 0

    # The exact flip threshold on the cap diameter.
    assert r50.flip_at_d_cm == pytest.approx(10.16, abs=1e-9)
    assert r50.half_width_to_flip_cm == pytest.approx(0.16, abs=1e-9)
    # A cap of 10.2 cm would give +0.04 cm.
    assert ve.clearance(10.2, ve.WAFER_EDGE_CM) == pytest.approx(0.04, abs=1e-9)


def test_sign_robustness_of_the_orientation_invariant_coverage_floor():
    """The mounting-free coverage requirement is NOT sign-robust."""
    floor = ve.cover_diameter_min_over_orientations()
    r = ve.clearance_sign_robust(ve.COV_CRYSTAL_DIAMETER_CM, floor, 0.5)
    assert not r.sign_preserved
    assert r.nominal_cm == pytest.approx(-0.1620, abs=1e-4)
    assert r.half_width_to_flip_cm == pytest.approx(0.1620, abs=1e-4)


def test_clearance_sign_robust_rejects_negative_half_width():
    with pytest.raises(ValueError):
        ve.clearance_sign_robust(10.0, 14.37, -0.1)


# --------------------------------------------------------------------------- #
# Area ratio                                                                   #
# --------------------------------------------------------------------------- #


def test_area_ratio_requires_an_explicit_basis():
    with pytest.raises(ValueError):
        ve.area_ratio()
    with pytest.raises(ValueError):
        ve.area_ratio(None)
    with pytest.raises(ValueError):
        ve.area_ratio("whatever")


def test_area_ratio_both_bases():
    assert ve.area_ratio("published_array_crystal_footprint") == pytest.approx(
        45.9, abs=0.05
    )
    assert ve.area_ratio("project_holder_scale_estimate") == pytest.approx(11.5, abs=0.05)
    # The two bases differ by a factor of 4 -- the reason a basis is mandatory.
    assert ve.area_ratio("published_array_crystal_footprint") / ve.area_ratio(
        "project_holder_scale_estimate"
    ) == pytest.approx(4.0, abs=1e-9)


# --------------------------------------------------------------------------- #
# Dimensional / unit discipline                                                #
# --------------------------------------------------------------------------- #


def test_units_are_cm_throughout_and_ratios_are_dimensionless():
    """All published mm values converted exactly once; cm values internally consistent."""
    assert ve.COV_CRYSTAL_DIAMETER_CM == pytest.approx(100.0 / 10.0)
    assert ve.COV_CRYSTAL_THICKNESS_CM == pytest.approx(25.0 / 10.0)
    assert ve.INTERNAL_SHIELD_DIAMETER_CM == pytest.approx(297.0 / 10.0)
    assert ve.CRYOSTAT_BORE_CM == pytest.approx(430.0 / 10.0)
    assert ve.B4C_THICKNESS_CM == pytest.approx(4.0)
    assert ve.ARRAY_CRYSTAL_FOOTPRINT_CM2 == pytest.approx(9 * 0.5 * 0.5)
    # Every length quantity is O(1-50) cm; a stray mm/cm slip would be 10x off.
    for c in ve.GEOMETRY_CONSTANTS.values():
        assert 1.0 < c.cm < 100.0
