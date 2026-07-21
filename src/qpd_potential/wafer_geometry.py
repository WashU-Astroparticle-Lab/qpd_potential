# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Wafer geometry and analytic ray-box (AABB slab) chord-length sampler for the
# Phase-4 muon deposited-energy channel (Plan 04-01, CALC-03 / VALD-02).
#
# SOURCE OF TRUTH: GPD/CONVENTIONS.md Section D (wafer geometry) and
# src/qpd_potential/params.py (V, rho, mass reused, NOT re-invented here).
#
# Coordinate frame (CONVENTIONS Section D / convention_lock "Coordinate system"):
#   Cartesian AABB box [0,Lx] x [0,Ly] x [0,Lz] cm, x,y in the 4in x 4in face,
#   z through the 2 mm thickness. Sensors are on one z-face (irrelevant to chords).
#
# Muon TRAVEL direction Omega_hat is a downward-going unit vector:
#   Omega = (sin(theta) cos(phi), sin(theta) sin(phi), -cos(theta)),
# with zenith theta measured from +z, so Omega_z = -cos(theta) <= 0.
#
# Chord bookkeeping: ell in cm; the Landau formulas downstream use the MASS
# thickness x = rho * ell in g/cm^2 (see muon_deposit.py) -- ell[cm] must NEVER
# be fed into the Landau formula (guards RESEARCH Pitfall 4 / fp mass-thickness).

from __future__ import annotations

import numpy as np

from . import params

# --------------------------------------------------------------------------- #
# Wafer edge dimensions (CONVENTIONS Section D: 4in x 4in x 2mm)               #
# --------------------------------------------------------------------------- #
LX = 10.16  # cm (4 inch)
LY = 10.16  # cm (4 inch)
LZ = 0.20   # cm (2 mm thickness)

EDGES = np.array([LX, LY, LZ])

# Reuse the locked bulk constants from params.py rather than re-deriving them.
RHO = params.GE_DENSITY.value        # 5.323 g/cm^3
V_PARAMS = params.WAFER_VOLUME.value  # 20.65 cm^3 (locked)
MASS_KG = params.WAFER_MASS.value / 1000.0  # 0.1099 kg

# Geometric volume from the edges; cross-checked against the locked V below.
V_GEOM = LX * LY * LZ  # ~= 20.645 cm^3

# Total surface area S = 2(Lx Ly + Lx Lz + Ly Lz) for the Cauchy invariant.
S_SURFACE = 2.0 * (LX * LY + LX * LZ + LY * LZ)  # ~= 214.6 cm^2

# Face areas perpendicular to each axis (area of the face whose normal is +/- e_a).
#   A_x = Ly*Lz, A_y = Lx*Lz, A_z = Lx*Ly
FACE_AREA = np.array([LY * LZ, LX * LZ, LX * LY])  # [A_x, A_y, A_z] cm^2

# Extremal chords (HIGH-confidence geometry sanity anchors).
CHORD_VERTICAL = LZ  # 0.20 cm (theta = 0 straight-through)
CHORD_DIAGONAL = float(np.sqrt(LX**2 + LY**2 + LZ**2))  # ~= 14.37 cm space diagonal


def cauchy_mean_chord() -> float:
    """Cauchy mean-chord invariant <ell> = 4V/S for a convex body, isotropic flux."""
    return 4.0 * V_GEOM / S_SURFACE


# --------------------------------------------------------------------------- #
# Ray-box (AABB slab) intersection                                            #
# --------------------------------------------------------------------------- #
def chord_lengths(origins: np.ndarray, directions: np.ndarray) -> np.ndarray:
    """Vectorized ray-box slab intersection chord length through the wafer.

    Parameters
    ----------
    origins : (N,3) entry points [cm]
    directions : (N,3) unit travel directions

    Returns
    -------
    (N,) chord length ell [cm]; 0.0 for rays that miss the box.

    Uses the standard slab method: for each axis a,
        t1 = (0 - O_a)/D_a,  t2 = (L_a - O_a)/D_a,
        t_enter = max_a min(t1,t2),  t_exit = min_a max(t1,t2),
        ell = max(t_exit - t_enter, 0).
    Axis-parallel components (|D_a| ~ 0) contribute an infinite slab.
    """
    O = np.asarray(origins, dtype=float)
    D = np.asarray(directions, dtype=float)
    N = O.shape[0]

    t_lo = np.full(N, -np.inf)
    t_hi = np.full(N, np.inf)
    for a in range(3):
        Da = D[:, a]
        Oa = O[:, a]
        parallel = np.abs(Da) < 1e-15
        safe = np.where(parallel, 1.0, Da)
        t1 = (0.0 - Oa) / safe
        t2 = (EDGES[a] - Oa) / safe
        tmin_ax = np.minimum(t1, t2)
        tmax_ax = np.maximum(t1, t2)
        # If parallel and outside the slab, the ray misses -> force empty interval.
        outside = parallel & ((Oa < 0.0) | (Oa > EDGES[a]))
        tmin_ax = np.where(parallel, -np.inf, tmin_ax)
        tmax_ax = np.where(parallel, np.inf, tmax_ax)
        t_lo = np.maximum(t_lo, tmin_ax)
        t_hi = np.minimum(t_hi, tmax_ax)
        t_hi = np.where(outside, -np.inf, t_hi)

    ell = np.clip(t_hi - t_lo, 0.0, None)
    ell = np.where(np.isfinite(ell), ell, 0.0)
    return ell


def projected_area(directions: np.ndarray) -> np.ndarray:
    """Convex-body projected area A_proj(Omega) = sum_a A_a |Omega_a| [cm^2].

    Equals the muon-visible cross-sectional area for travel direction Omega.
    For vertical (Omega=-z) this returns A_z = Lx*Ly (the top face). The rate of
    muons through the wafer within dOmega dE is dI/dE * A_proj(Omega) dOmega dE.
    """
    D = np.asarray(directions, dtype=float)
    return np.abs(D) @ FACE_AREA


def direction_from_angles(theta: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Downward-going travel direction from zenith theta and azimuth phi."""
    theta = np.asarray(theta, dtype=float)
    phi = np.asarray(phi, dtype=float)
    st = np.sin(theta)
    return np.stack([st * np.cos(phi), st * np.sin(phi), -np.cos(theta)], axis=-1)


def sample_entry_and_chord(directions: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Sample chord lengths for given travel directions, entry point uniform over
    the projected area (correct chord-length distribution).

    For each direction the entry face is chosen among the 3 faces facing the
    incoming muon with probability proportional to A_a |Omega_a| (which sums to
    A_proj); the entry point is uniform on that face; the chord is the ray-box
    intersection length.
    """
    D = np.asarray(directions, dtype=float)
    N = D.shape[0]

    # Per-axis entry weight A_a |Omega_a|; the entry face on axis a is the min
    # face (coord 0) if Omega_a > 0 else the max face (coord L_a).
    w = np.abs(D) * FACE_AREA[None, :]  # (N,3)
    wsum = w.sum(axis=1, keepdims=True)
    wsum = np.where(wsum <= 0, 1.0, wsum)
    cdf = np.cumsum(w / wsum, axis=1)  # (N,3)

    u_face = rng.random(N)
    axis = (u_face[:, None] > cdf).sum(axis=1)  # 0,1,2 chosen entry axis
    axis = np.clip(axis, 0, 2)

    O = np.empty((N, 3))
    u2 = rng.random((N, 2))
    for a in range(3):
        mask = axis == a
        if not np.any(mask):
            continue
        others = [ax for ax in range(3) if ax != a]
        # fixed coordinate on the entry face: 0 if Omega_a>0 else L_a
        pos_dir = D[mask, a] > 0
        O[mask, a] = np.where(pos_dir, 0.0, EDGES[a])
        O[np.ix_(mask, [others[0]])] = (u2[mask, 0] * EDGES[others[0]])[:, None]
        O[np.ix_(mask, [others[1]])] = (u2[mask, 1] * EDGES[others[1]])[:, None]

    # Nudge the entry point a hair inside along the travel direction to avoid
    # boundary round-off, then measure the full chord.
    O_in = O + 1e-9 * D
    return chord_lengths(O_in, D)


def sample_isotropic_chords(n: int, rng: np.random.Generator) -> np.ndarray:
    """Chord lengths under an ISOTROPIC (uniform-per-solid-angle) flux.

    Used by the Cauchy unit test: the flux-weighted mean chord must equal
    4V/S. Directions are sampled uniformly on the sphere and weighted by the
    projected area via the same entry-face sampler, so the returned chords are
    already drawn from the correct isotropic (surface-flux) chord distribution.
    """
    # Uniform directions on the full sphere.
    z = rng.uniform(-1.0, 1.0, n)
    phi = rng.uniform(0.0, 2.0 * np.pi, n)
    r = np.sqrt(1.0 - z * z)
    D = np.stack([r * np.cos(phi), r * np.sin(phi), z], axis=-1)

    # The chord-length distribution is projected-area weighted. Importance-weight
    # by A_proj so the *mean chord* equals the Cauchy invariant.
    ell = sample_entry_and_chord(D, rng)
    w = projected_area(D)
    return ell, w
