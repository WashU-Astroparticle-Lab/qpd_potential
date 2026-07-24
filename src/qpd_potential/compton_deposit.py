# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Klein-Nishina angle-sampled electron-recoil CONTINUUM and assembly of the
# environmental-gamma Compton deposited-energy spectrum dR/dE_dep for the thin Ge
# wafer (Plan 04-02, CALC-04 / VALD-03).
#
# KEY PHYSICS (guards the forbidden proxies):
#  * DEPOSIT = Compton ELECTRON recoil T_e = E_gamma - E' (the scattered photon
#    escapes the optically-thin 2 mm wafer). NOT E_gamma, NOT E'. This is a
#    CONTINUUM up to each edge E_edge = 2E^2/(m_e c^2 + 2E), with NO photopeaks.
#    Guards fp-full-absorption, fp-electron-not-photon.
#  * The scattering angle theta is sampled from the Klein-Nishina dsigma/dOmega and
#    T_e follows KINEMATICALLY, so the Compton edge falls out automatically
#    (self-validating) -- no error-prone closed-form dsigma/dT_e change of variables.
#  * Each line is weighted by the thin-target SINGLE-SCATTER interaction rate
#    R_i = Phi_i * (S/4) * [1 - exp(-mu(E_i) * ell_bar)] on the ONE pinned Cauchy
#    mean chord ell_bar = 4V/S = 0.385 cm (compton_source). Cross-checked against
#    the independent anchor Phi_i * sigma_KN(E_i) * N_e (flux x Compton cross
#    section x electrons), agreeing to ~few % (VALD-03 factor-2).
#  * Unified phonon E_dep scale, NO quenching (CONVENTIONS Section B). The deposit
#    is an electron recoil with zero defect correction. Guards fp-quenching-compton.
#
# Output dR/dE_dep is on the SHARED log E_dep grid (muon_deposit.shared_energy_grid),
# counts/kg/day/keV, so the muon (04-01) and Compton channels co-add in Phase 5.

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import compton_source as cs
from .muon_deposit import shared_energy_grid   # SHARED grid (identical to 04-01)

M_E_KEV = cs.M_E_KEV
R_E_CM = cs.R_E_CM


# --------------------------------------------------------------------------- #
# Klein-Nishina differential cross section and angle sampling                  #
# --------------------------------------------------------------------------- #
def kn_dsigma_domega(e_gamma_kev: float, cos_theta: np.ndarray) -> np.ndarray:
    """Klein-Nishina dsigma/dOmega [cm^2/sr] per FREE electron vs cos(theta).

    dsigma/dOmega = (r_e^2/2)(E'/E)^2 (E'/E + E/E' - sin^2 theta),
      E'(theta) = E / (1 + alpha(1 - cos theta)),  alpha = E / m_e c^2.
    """
    alpha = e_gamma_kev / M_E_KEV
    ratio = 1.0 / (1.0 + alpha * (1.0 - cos_theta))   # E'/E
    sin2 = 1.0 - cos_theta**2
    return 0.5 * R_E_CM**2 * ratio**2 * (ratio + 1.0 / ratio - sin2)


def incoh_dsigma_domega(e_gamma_kev: float, cos_theta: np.ndarray) -> np.ndarray:
    """BOUND-electron incoherent dsigma/dOmega [cm^2/sr] PER ATOM vs cos(theta).

    dsigma_incoh/dOmega = (dsigma_KN/dOmega) * S(x,Z), the standard bound-Compton
    correction with the incoherent scattering function S(x,Z=32) (Hubbell 1975).
    x = E_gamma[keV]*sin(theta/2)/12.39842 [A^-1]. S->0 forward (low recoil, bound)
    and S->Z backward (the Compton edge, free), so the edge is UNCHANGED.
    """
    x = cs.momentum_transfer_x(e_gamma_kev, cos_theta)
    return kn_dsigma_domega(e_gamma_kev, cos_theta) * cs.incoherent_S(x)


def sigma_incoh_atom(e_gamma_kev: float, n_grid: int = 40001) -> float:
    """Total bound incoherent cross section PER ATOM [cm^2]:
    sigma_incoh = integral (dsigma_KN/dOmega) S(x,Z) dOmega, dOmega = 2pi d(cos).

    Free limit S->Z gives sigma_incoh -> Z * sigma_KN (atom of Z free electrons).
    """
    c = np.linspace(-1.0, 1.0, n_grid)
    integrand = incoh_dsigma_domega(e_gamma_kev, c)
    return float(2.0 * np.pi * np.trapz(integrand, c))


def binding_suppression(e_gamma_kev: float) -> float:
    """Binding suppression f_bind(E) = sigma_incoh_atom / (Z * sigma_KN) in (0,1].

    The fractional reduction of the TOTAL incoherent cross section from electron
    binding; ~1 for the MeV radiogenic lines (binding removes only the small
    near-forward, low-q cross section). Multiplies the free per-line rate to give
    the bound (deliverable) normalization consistent with the S-suppressed shape.
    """
    sig_free_atom = cs.Z_GE * float(cs.sigma_kn(e_gamma_kev))
    return sigma_incoh_atom(e_gamma_kev) / sig_free_atom


def sample_electron_recoil(e_gamma_kev: float, n: int,
                           rng: np.random.Generator) -> np.ndarray:
    """Sample n electron-recoil energies T_e [keV] for a line E_gamma via
    rejection sampling of cos(theta) ~ dsigma_incoh/dOmega = dsigma_KN/dOmega *
    S(x,Z), then T_e = E_gamma - E'.

    The bound incoherent scattering function S(x,Z) SUPPRESSES near-forward (low
    T_e) recoils; the Compton edge T_e(theta=pi)=E_edge (S->Z there) is unchanged
    and still falls out kinematically as the max sampled T_e (self-validating).
    """
    alpha = e_gamma_kev / M_E_KEV
    # Envelope for dsigma_KN/dOmega * S(x,Z): bound on a fine cos grid (the S
    # factor moves the peak off exact forward scatter, so bound the product).
    cgrid = np.linspace(-1.0, 1.0, 4001)
    fmax = incoh_dsigma_domega(e_gamma_kev, cgrid).max() * 1.02

    out = np.empty(n)
    filled = 0
    while filled < n:
        m = int((n - filled) * 1.6) + 64
        c = rng.uniform(-1.0, 1.0, m)
        f = incoh_dsigma_domega(e_gamma_kev, c)
        acc = rng.uniform(0.0, fmax, m) < f
        c_acc = c[acc]
        take = min(c_acc.size, n - filled)
        cos_theta = c_acc[:take]
        e_prime = e_gamma_kev / (1.0 + alpha * (1.0 - cos_theta))
        out[filled:filled + take] = e_gamma_kev - e_prime   # T_e
        filled += take
    return out


# --------------------------------------------------------------------------- #
# Per-line single-scatter interaction rate (thin target, pinned mean chord)    #
# --------------------------------------------------------------------------- #
def line_interaction_rate_hz(flux_cm2_s: float, e_gamma_kev: float) -> float:
    """Single-scatter Compton interaction rate for one line in the whole wafer [s^-1].

    R = Phi * (S/4) * [1 - exp(-mu(E) * ell_bar)], the isotropic-flux entry rate
    Phi*S/4 times the single-crossing interaction probability on the pinned mean
    chord ell_bar = 4V/S. Consistent with the double-scatter and rate bookkeeping.
    """
    P = float(cs.interaction_prob(e_gamma_kev))          # 1 - exp(-mu ell_bar)
    return flux_cm2_s * (cs.S_SURFACE / 4.0) * P


def line_rate_anchor_hz(flux_cm2_s: float, e_gamma_kev: float) -> float:
    """Independent VALD-03 anchor: Phi * sigma_KN(E) * N_e (flux x Compton cross
    section x wafer electrons) [s^-1]. Uses the closed-form KN cross section."""
    return flux_cm2_s * float(cs.sigma_kn(e_gamma_kev)) * cs.N_E_WAFER


# --------------------------------------------------------------------------- #
# Full Compton dR/dE_dep assembly                                              #
# --------------------------------------------------------------------------- #
@dataclass
class ComptonSpectrum:
    edges_kev: np.ndarray
    centers_kev: np.ndarray
    dRdE: np.ndarray            # counts / kg / day / keV
    dRdE_err: np.ndarray        # per-bin MC statistical error, same units
    rate_hz: float              # total BOUND single-scatter interaction rate [Hz]
    rate_free_hz: float         # total FREE-KN single-scatter rate (pre-binding) [Hz]
    rate_anchor_hz: float       # flux x sigma_KN x N_e (free) cross-check [Hz]
    line_energies: np.ndarray   # E_gamma per line [keV]
    line_edges: np.ndarray      # E_edge per line [keV]
    line_edges_sampled: np.ndarray   # max sampled T_e per line [keV]
    line_rates_hz: np.ndarray   # R_i per line [Hz]
    n_per_line: int
    counts_per_kg_day: float    # integral of dR/dE_dep dE (energy closure)
    #: RAW, UNWEIGHTED Monte-Carlo entry count per bin, summed over lines.  Plan
    #: 15-02 addition: purely diagnostic, consumes no random numbers and enters no
    #: rate; it exists so a bin with NO estimator support is distinguishable from
    #: a bin whose rate is genuinely small.  Defaulted so no existing constructor
    #: call site changes.
    mc_entries: np.ndarray = None  # type: ignore[assignment]
    grid_version: str = "v1.0"


def run_compton_mc(n_per_line: int = 400_000, seed: int = 20260720,
                   batch_size: int = 5_000_000,
                   grid_version: str = "v1.0") -> ComptonSpectrum:
    """Assemble the Compton electron-recoil dR/dE_dep on the shared log E_dep grid.

    For each sourced line: sample T_e ~ Klein-Nishina (angle -> kinematics), weight
    by the single-scatter rate R_i, histogram onto the shared grid in counts/kg/day/keV.

    Each line's ``n_per_line`` rejection samples are drawn in batches of at most
    ``batch_size`` and the (per-bin count histogram, sum w, sum w^2) accumulators are
    summed across batches, so only ONE batch is ever held in memory (the same pattern
    as ``muon_deposit.run_muon_mc``). Per-batch RNG streams are spawned deterministically
    from the master ``seed`` via ``np.random.SeedSequence(seed).spawn(...)``, so the full
    result is exactly reproducible for a given ``(n_per_line, seed, batch_size)``. This
    is a STATISTICS-ONLY control: the physics (S(x,Z) binding, kinematics, rates, grid)
    is unchanged; larger ``n_per_line`` only shrinks the per-bin MC error.

    ``grid_version`` (Plan 15-02).  DEFAULTS TO ``"v1.0"``, which preserves the
    Plan 10-03 caller pin exactly: this function writes
    ``data/compton_dRdEdep.csv`` and a caller that does not ask for the extension
    still gets the v1.0 axis.  Pass ``"v2.0-ext"`` EXPLICITLY for the 744-bin
    extended run.  The per-(line, batch) child streams are spawned from
    ``SeedSequence(seed)`` and every draw precedes ``np.histogram``, so for a
    given ``(n_per_line, seed, batch_size)`` the extended run's bins ``160..743``
    are BIT-IDENTICAL to the v1.0 run (``np.array_equal``).
    """
    lines = cs.load_gamma_lines()

    # PLAN 10-03 CALLER PIN, KEPT LITERALLY (Plan 15-02 leaves it in place because
    # this function writes data/compton_dRdEdep.csv). The branch is deliberately
    # explicit rather than collapsed to `shared_energy_grid(grid_version)`: the
    # literal v1.0 pin is what
    # tests/test_energy_grid_extension.py::test_phase4_producers_still_emit_the_584_bin_axis
    # greps for, and it states at the call site that the DEFAULT path is v1.0.
    # Phase 15's extended run reaches the other branch only by naming
    # grid_version="v2.0-ext" explicitly at its own call site.
    if grid_version == "v1.0":
        edges = shared_energy_grid("v1.0")
    else:
        edges = shared_energy_grid(grid_version)
    centers = np.sqrt(edges[:-1] * edges[1:])
    dwidth = np.diff(edges)
    per_day = 86400.0 / cs.MASS_KG           # Hz -> counts/kg/day

    batch_size = int(batch_size)
    n_batches_per_line = int(np.ceil(n_per_line / batch_size))
    # Deterministic child streams for every (line, batch); reproducible for a given
    # (n_per_line, seed, batch_size). Independent of how batching is chunked physically.
    child_seeds = np.random.SeedSequence(seed).spawn(len(lines) * n_batches_per_line)

    sumw = np.zeros(centers.size)
    sumw2 = np.zeros(centers.size)
    entries = np.zeros(centers.size, dtype=np.int64)   # RAW counts, Plan 15-02

    e_g, e_edge, e_edge_s, r_line = [], [], [], []
    total_rate = 0.0
    total_free = 0.0
    total_anchor = 0.0
    for li, ln in enumerate(lines):
        R_free = line_interaction_rate_hz(ln.flux_cm2_s, ln.energy_keV)  # Hz (free KN)
        f_bind = binding_suppression(ln.energy_keV)                     # <= 1
        R_i = R_free * f_bind                                            # Hz (bound incoh)
        A_i = line_rate_anchor_hz(ln.flux_cm2_s, ln.energy_keV)          # Hz (free anchor)
        total_rate += R_i
        total_free += R_free
        total_anchor += A_i

        w = R_i * per_day / n_per_line                                   # cts/kg/day per sample
        remaining = n_per_line
        te_max = 0.0
        for b in range(n_batches_per_line):
            n_b = int(min(batch_size, remaining))
            rng = np.random.default_rng(child_seeds[li * n_batches_per_line + b])
            te = sample_electron_recoil(ln.energy_keV, n_b, rng)         # keV
            h, _ = np.histogram(te, bins=edges)
            h2 = h.astype(float)
            sumw += h2 * w
            sumw2 += h2 * w * w
            entries += h
            te_max = max(te_max, float(te.max()))
            remaining -= n_b

        e_g.append(ln.energy_keV)
        e_edge.append(float(cs.compton_edge_kev(ln.energy_keV)))
        e_edge_s.append(te_max)
        r_line.append(R_i)

    dRdE = sumw / dwidth
    dRdE_err = np.sqrt(sumw2) / dwidth
    counts_per_kg_day = float((dRdE * dwidth).sum())

    return ComptonSpectrum(
        edges_kev=edges,
        centers_kev=centers,
        dRdE=dRdE,
        dRdE_err=dRdE_err,
        rate_hz=float(total_rate),
        rate_free_hz=float(total_free),
        rate_anchor_hz=float(total_anchor),
        line_energies=np.asarray(e_g),
        line_edges=np.asarray(e_edge),
        line_edges_sampled=np.asarray(e_edge_s),
        line_rates_hz=np.asarray(r_line),
        n_per_line=n_per_line,
        counts_per_kg_day=counts_per_kg_day,
        mc_entries=entries,
        grid_version=grid_version,
    )


# --------------------------------------------------------------------------- #
# DETERMINISTIC (noise-free) assembly of the same spectrum                      #
# --------------------------------------------------------------------------- #
# WHY THIS EXISTS.  run_compton_mc samples cos(theta) by rejection and histograms
# the resulting T_e, so every bin carries sampling scatter.  The scatter is
# harmless where the spectrum is dense (rel. err ~1e-3 above 1 keV) but it
# DOMINATES the low-recoil roll-off that the reconstructed-axis deliverable
# actually plots: at 40e6 samples/line the 1-10 eV band holds ~9 entries/bin
# (rel. err ~0.43) and below 1 eV there is ONE entry per bin.  That is the
# visible jaggedness on the combined figure, and it is pure sampling noise, not
# structure.
#
# The change of variable the MC deliberately avoids (see the module header:
# "no error-prone closed-form dsigma/dT_e change of variables") is done here
# EXPLICITLY and is validated against the MC rather than trusted:
#
#   u = 1 - cos(theta),   T = E*alpha*u/(1 + alpha*u),   alpha = E/m_e c^2
#   => u(T) = T / (alpha (E - T)),   dT/du = E*alpha/(1 + alpha*u)^2
#   => dsigma/dT = 2*pi * (dsigma_KN/dOmega)(cos) * S(x) * (1 + alpha*u)^2/(E*alpha)
#
# because dsigma/dT dT = 2*pi (dsigma/dOmega) S du = -2*pi (dsigma/dOmega) S dcos,
# i.e. the SAME measure the MC samples.  The Compton edge is still not asserted:
# u runs to exactly 2 at T = T_edge, so the edge falls out of u(T) as before, and
# S(x) -> Z there, so the edge is unchanged.  At T -> 0, u -> 0 and S(0) = 0, so
# dsigma/dT -> 0 with no integrable singularity to nurse.
#
# THIS IS NOT A SMOOTHING OF THE MC.  No MC output is filtered, fitted, or
# reweighted.  It is the same physics (same S(x,Z) table, same per-line rates
# R_i, same grid, same normalization sigma_incoh_atom) evaluated by quadrature,
# so the result has NO statistical error at all.  tests/ asserts the two agree
# within the MC's own error.
_GAUSS_LEG_N = 24


def dsigma_dT_incoh(e_gamma_kev: float, t_kev: np.ndarray) -> np.ndarray:
    """Bound incoherent dsigma/dT_e [cm^2/keV] PER ATOM at electron recoil T_e.

    Zero outside (0, T_edge]. Derived by change of variable from the SAME
    dsigma_incoh/dOmega the Monte-Carlo path samples, so the two integrate to the
    identical sigma_incoh_atom.
    """
    t = np.asarray(t_kev, dtype=float)
    alpha = e_gamma_kev / M_E_KEV
    t_edge = float(cs.compton_edge_kev(e_gamma_kev))
    out = np.zeros_like(t)
    ok = (t > 0.0) & (t <= t_edge)
    if not np.any(ok):
        return out
    tt = t[ok]
    u = tt / (alpha * (e_gamma_kev - tt))
    cos_theta = np.clip(1.0 - u, -1.0, 1.0)
    x = cs.momentum_transfer_x(e_gamma_kev, cos_theta)
    jac = (1.0 + alpha * u) ** 2 / (e_gamma_kev * alpha)   # du/dT
    out[ok] = (2.0 * np.pi * kn_dsigma_domega(e_gamma_kev, cos_theta)
               * cs.incoherent_S(x) * jac)
    return out


def _bin_probabilities(e_gamma_kev: float, edges: np.ndarray) -> np.ndarray:
    """Fraction of a line's scatters landing in each bin of `edges`.

    Gauss-Legendre on each bin, clipped to the line's kinematic support (0,
    T_edge], normalized by sigma_incoh_atom -- the SAME denominator the MC path
    normalizes to implicitly by sampling that measure.
    """
    t_edge = float(cs.compton_edge_kev(e_gamma_kev))
    lo = np.minimum(edges[:-1], t_edge)
    hi = np.minimum(edges[1:], t_edge)
    width = np.clip(hi - lo, 0.0, None)
    xg, wg = np.polynomial.legendre.leggauss(_GAUSS_LEG_N)
    # map [-1,1] -> [lo,hi] per bin: (nbins, N)
    mid = 0.5 * (lo + hi)[:, None]
    half = 0.5 * width[:, None]
    nodes = mid + half * xg[None, :]
    vals = dsigma_dT_incoh(e_gamma_kev, nodes.ravel()).reshape(nodes.shape)
    integral = (vals * wg[None, :]).sum(axis=1) * half[:, 0]
    return integral / sigma_incoh_atom(e_gamma_kev)


def run_compton_analytic(grid_version: str = "v2.0-ext") -> ComptonSpectrum:
    """Deterministic dR/dE_dep for the environmental-gamma Compton continuum.

    Drop-in replacement for ``run_compton_mc`` returning the same
    ``ComptonSpectrum``, with ``dRdE_err`` identically zero (there is no
    sampling) and ``mc_entries`` set to -1 as a sentinel meaning "not a sampled
    quantity" -- deliberately NOT 0, which downstream code reads as "no
    estimator support in this bin".
    """
    lines = cs.load_gamma_lines()
    edges = shared_energy_grid(grid_version)
    centers = np.sqrt(edges[:-1] * edges[1:])
    dwidth = np.diff(edges)
    per_day = 86400.0 / cs.MASS_KG

    sumw = np.zeros(centers.size)
    e_g, e_edge, e_edge_s, r_line = [], [], [], []
    total_rate = total_free = total_anchor = 0.0

    for ln in lines:
        R_free = line_interaction_rate_hz(ln.flux_cm2_s, ln.energy_keV)
        f_bind = binding_suppression(ln.energy_keV)
        R_i = R_free * f_bind
        total_rate += R_i
        total_free += R_free
        total_anchor += line_rate_anchor_hz(ln.flux_cm2_s, ln.energy_keV)

        sumw += R_i * per_day * _bin_probabilities(ln.energy_keV, edges)

        t_edge = float(cs.compton_edge_kev(ln.energy_keV))
        e_g.append(ln.energy_keV)
        e_edge.append(t_edge)
        # The MC reports the MAX SAMPLED T_e as a self-validation of the edge.
        # There is no sampling here, so report the highest bin edge that carries
        # non-zero probability -- the grid-resolved edge, which is the strongest
        # statement this path can make. It must not be confused with t_edge.
        nz = np.nonzero(_bin_probabilities(ln.energy_keV, edges) > 0)[0]
        e_edge_s.append(float(edges[nz[-1] + 1]) if nz.size else 0.0)
        r_line.append(R_i)

    dRdE = sumw / dwidth
    return ComptonSpectrum(
        edges_kev=edges,
        centers_kev=centers,
        dRdE=dRdE,
        dRdE_err=np.zeros_like(dRdE),
        rate_hz=float(total_rate),
        rate_free_hz=float(total_free),
        rate_anchor_hz=float(total_anchor),
        line_energies=np.asarray(e_g),
        line_edges=np.asarray(e_edge),
        line_edges_sampled=np.asarray(e_edge_s),
        line_rates_hz=np.asarray(r_line),
        n_per_line=0,
        counts_per_kg_day=float((dRdE * dwidth).sum()),
        mc_entries=np.full(centers.size, -1, dtype=np.int64),
        grid_version=grid_version,
    )


def write_csv(spec: ComptonSpectrum, path: str) -> None:
    """Write dR/dE_dep to CSV: E_dep_keV, dRdEdep_cts_per_kg_day_keV, mc_err."""
    import csv as _csv

    header_lines = [
        "# Compton (environmental-gamma) deposited-energy spectrum dR/dE_dep,",
        "# 4in x 4in x 2mm Ge wafer. Plan 04-02 (CALC-04/VALD-03).",
        "# BOUND incoherent scattering: angle sampled from dsigma_KN/dOmega * S(x,Z=32)",
        "# with the Hubbell (1975) incoherent scattering function (data/ge_incoherent_S.csv);",
        "# S(x->0)->0 SUPPRESSES the low-recoil (near-forward) continuum, fixing the",
        "# unphysical free-KN flat-then-cut low edge; S(x->inf)->Z leaves the Compton",
        "# EDGES and the bulk continuum (>~keV) unchanged. ELECTRON recoil T_e (NO",
        "# photopeaks, scattered photon escapes the thin wafer); thin-target single-",
        "# scatter on the pinned Cauchy mean chord ell_bar = 4V/S = 0.385 cm. UNIFIED",
        "# PHONON SCALE, NO quenching (CONVENTIONS Section B): S(x,Z) changes the CROSS",
        "# SECTION, not the energy scale. Gamma flux = sourced tunable input",
        "# (data/gamma_lines.csv, provenance).",
        f"# total_single_scatter_rate_Hz = {spec.rate_hz:.4e} (BOUND incoherent; "
        f"free-KN pre-binding = {spec.rate_free_hz:.4e}, binding f_bind = "
        f"{spec.rate_hz / spec.rate_free_hz:.4f})",
        f"# VALD-03 anchor flux x sigma_KN x N_e (free) = {spec.rate_anchor_hz:.4e}; "
        f"bound/anchor ratio {spec.rate_hz / spec.rate_anchor_hz:.3f} (within factor 2)",
        f"# integral dR/dE_dep = {spec.counts_per_kg_day:.4e} counts/kg/day "
        f"(= total_rate * 86400 / mass_kg; energy closure)",
        f"# n_mc_samples_per_line = {spec.n_per_line}; seed fixed for reproducibility",
        "# units: E_dep_keV [keV]; dRdEdep [counts/kg/day/keV]; mc_err [counts/kg/day/keV]",
        "# grid: shared log E_dep, 0.01 keV -> 2e5 keV (200 MeV), ~80 bins/decade (matches 04-01)",
    ]
    with open(path, "w", newline="") as f:
        for line in header_lines:
            f.write(line + "\n")
        w = _csv.writer(f)
        w.writerow(["E_dep_keV", "dRdEdep_cts_per_kg_day_keV", "mc_err"])
        for c, y, e in zip(spec.centers_kev, spec.dRdE, spec.dRdE_err):
            w.writerow([f"{c:.6e}", f"{y:.6e}", f"{e:.6e}"])
