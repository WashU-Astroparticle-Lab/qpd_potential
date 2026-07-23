# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
#
# Landau-Vavilov most-probable-value (MPV) deposit per chord and assembly of the
# sea-level muon deposited-energy spectrum dR/dE_dep for the thin Ge wafer
# (Plan 04-01, CALC-03 / VALD-02).
#
# ENERGY SCALE: unified phonon E_dep scale, NO ionization quenching, NO
# keVee/keVnr split (CONVENTIONS Section B; the muon deposit is an electron
# recoil with zero Frenkel-defect correction). Guards fp-quenching-muon.
#
# KEY PHYSICS (guards the forbidden proxies):
#  * Per-chord deposit sampled from the LANDAU-VAVILOV distribution using the
#    most-probable value Delta_p (NOT the mean <dE/dx>*ell, NOT Moyal).
#    Guards fp-mean-not-mpv / RESEARCH Pitfall 2.
#  * Landau formulas use MASS THICKNESS x = rho*ell [g/cm^2], carried explicitly.
#    Guards RESEARCH Pitfall 4.
#  * Surface-flux measure I(theta)*A_proj*sin(theta) (muon_flux/wafer_geometry),
#    NOT bare cos^2(theta). Guards fp-angular-bias / RESEARCH Pitfall 3.
#  * Near-horizontal long chords resolved by sampling zenith uniformly in
#    [0, pi/2] (oversamples the horizon relative to the physical sin*cos^2
#    measure) so the tens-of-MeV Phase-5 saturation tail is populated.
#
# Delta_p is COMPUTED here from the PDG "Passage of Particles Through Matter"
# formula; nothing is hard-coded from memory. The custom Landau sampler is a
# numerical inverse-CDF of the Landau density built from its integral definition
# (mode lambda = -0.22278, textbook/PDG value) and is validated against the PDG
# Delta_p and xi(vertical) ~= 0.072 MeV. pylandau is an optional second opinion.

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
from scipy import integrate

from . import muon_flux, wafer_geometry

# --------------------------------------------------------------------------- #
# Physical constants (PDG)                                                     #
# --------------------------------------------------------------------------- #
M_MU = 105.6583745      # muon mass [MeV]
M_E = 0.51099895        # electron mass [MeV]
K_MEV = 0.307075        # 4 pi N_A r_e^2 m_e c^2 [MeV mol^-1 cm^2] (PDG K)
Z_OVER_A_GE = 0.4406    # Ge <Z/A> = 32 / 72.63
I_GE = 350.0e-6         # Ge mean excitation energy I [MeV] (350 eV)
J_LANDAU = 0.200        # PDG MPV constant j
DEDX_MEAN = 1.370       # Ge minimum-ionizing <dE/dx> [MeV cm^2/g] (CONVENTIONS G)

RHO = wafer_geometry.RHO  # 5.323 g/cm^3

# Sternheimer density-effect parameters for germanium
# (Sternheimer, Berger & Seltzer, At. Data Nucl. Data Tables 30, 261 (1984);
#  ICRU-37 elemental table). MEDIUM confidence: standard tabulated coefficients;
#  the density effect is a modest (<~ few) correction to the MPV log-bracket.
_STERN = dict(x0=0.3376, x1=3.6096, a=0.07188, m=3.3306, cbar=5.3299, d0=0.14)
_LAM_MODE = -0.22278  # mode of the standard Landau density phi(lambda)


# --------------------------------------------------------------------------- #
# Kinematics and Landau-Vavilov MPV / width                                   #
# --------------------------------------------------------------------------- #
def beta_gamma(e_mu_gev: np.ndarray) -> np.ndarray:
    """beta*gamma from the muon TOTAL energy E_mu [GeV]."""
    g = np.asarray(e_mu_gev, dtype=float) * 1000.0 / M_MU  # gamma = E/m
    g = np.maximum(g, 1.0 + 1e-9)
    return np.sqrt(g * g - 1.0)


def density_effect(bg: np.ndarray) -> np.ndarray:
    """Sternheimer density-effect correction delta(beta*gamma) for Ge."""
    p = _STERN
    x = np.log10(np.asarray(bg, dtype=float))
    # clip (x1 - x) to >= 0 so the fractional power is never evaluated on a
    # negative base (that branch is only selected for x0 <= x < x1 anyway).
    x1_minus = np.clip(p["x1"] - x, 0.0, None)
    d = np.where(
        x >= p["x1"],
        2.0 * np.log(10.0) * x - p["cbar"],
        np.where(
            x >= p["x0"],
            2.0 * np.log(10.0) * x - p["cbar"] + p["a"] * x1_minus ** p["m"],
            p["d0"] * 10.0 ** (2.0 * (x - p["x0"])),
        ),
    )
    return np.clip(d, 0.0, None)


def t_max(bg: np.ndarray) -> np.ndarray:
    """Max single-collision energy transfer T_max [MeV] (PDG)."""
    bg = np.asarray(bg, dtype=float)
    g = np.sqrt(bg * bg + 1.0)
    r = M_E / M_MU
    return 2.0 * M_E * bg * bg / (1.0 + 2.0 * g * r + r * r)


def xi_width(x_gcm2: np.ndarray, beta2: np.ndarray) -> np.ndarray:
    """Landau width xi = (K/2)(Z/A)(x/beta^2) [MeV], x = rho*ell in g/cm^2."""
    return 0.5 * K_MEV * Z_OVER_A_GE * np.asarray(x_gcm2, dtype=float) / beta2


def mpv_deposit(x_gcm2: np.ndarray, bg: np.ndarray):
    """Most-probable energy loss Delta_p [MeV] and width xi [MeV] (PDG formula).

    Delta_p = xi[ ln(2 m_e c^2 beta^2 gamma^2 / I) + ln(xi/I) + j - beta^2 - delta ].
    """
    bg = np.asarray(bg, dtype=float)
    g2 = bg * bg + 1.0
    beta2 = (bg * bg) / g2
    xi = xi_width(x_gcm2, beta2)
    delta = density_effect(bg)
    dp = xi * (
        np.log(2.0 * M_E * bg * bg / I_GE)
        + np.log(xi / I_GE)
        + J_LANDAU
        - beta2
        - delta
    )
    return dp, xi


def kappa(x_gcm2: np.ndarray, bg: np.ndarray) -> np.ndarray:
    """Vavilov regime parameter kappa = xi / T_max (Landau <~0.01, Gaussian >~10)."""
    bg = np.asarray(bg, dtype=float)
    beta2 = (bg * bg) / (bg * bg + 1.0)
    return xi_width(x_gcm2, beta2) / t_max(bg)


# --------------------------------------------------------------------------- #
# Custom Landau sampler: numerical inverse-CDF of the standard Landau density  #
#   phi(lambda) = (1/pi) int_0^inf exp(-t ln t - lambda t) sin(pi t) dt        #
# built once and cached. Tail phi ~ 1/lambda^2 -> F ~ 1 - c/lambda.            #
# --------------------------------------------------------------------------- #
_LANDAU_TABLE = None


def _phi_landau(lam: float) -> float:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        val, _ = integrate.quad(
            lambda t: np.exp(-t * np.log(t) - lam * t) * np.sin(np.pi * t),
            0.0, 60.0, limit=400,
        )
    return max(val / np.pi, 0.0)


def _build_landau_table():
    global _LANDAU_TABLE
    if _LANDAU_TABLE is not None:
        return _LANDAU_TABLE
    lam_hi = 300.0
    grid = np.concatenate([np.linspace(-4.0, 20.0, 700),
                           np.linspace(20.5, lam_hi, 300)])
    pdf = np.array([_phi_landau(l) for l in grid])
    cdf = np.concatenate([[0.0], integrate.cumulative_trapezoid(pdf, grid)])
    c_tail = lam_hi * (1.0 - cdf[-1])  # match F = 1 - c/lambda beyond the grid
    _LANDAU_TABLE = (grid, cdf, lam_hi, c_tail)
    return _LANDAU_TABLE


def sample_standard_landau(u: np.ndarray) -> np.ndarray:
    """Sample the standard Landau variate lambda (mode -0.22278) from uniforms u."""
    grid, cdf, lam_hi, c_tail = _build_landau_table()
    lam = np.interp(u, cdf, grid)
    hi = u > cdf[-1]
    lam = np.where(hi, c_tail / np.clip(1.0 - u, 1e-12, None), lam)
    return lam


def sample_deposit(x_gcm2: np.ndarray, bg: np.ndarray, rng: np.random.Generator):
    """Sample the per-chord energy deposit [MeV] from Landau-Vavilov straggling.

    Landau/mild-Vavilov (kappa < 10): deposit = Delta_p + xi*(lambda - lambda_mode)
    with lambda ~ standard Landau, so the mode sits exactly at Delta_p.
    Gaussian (kappa >= 10): deposit ~ Normal(mean, sqrt(xi*T_max*(1-beta^2/2))).
    Each deposit is capped at the muon kinetic energy (energy conservation).
    """
    x_gcm2 = np.asarray(x_gcm2, dtype=float)
    bg = np.asarray(bg, dtype=float)
    n = x_gcm2.shape[0]
    dp, xi = mpv_deposit(x_gcm2, bg)
    kap = kappa(x_gcm2, bg)

    u = rng.random(n)
    lam = sample_standard_landau(u)
    dep = dp + xi * (lam - _LAM_MODE)

    # Gaussian (thick-absorber) branch for the rare kappa >= 10 chords.
    gauss = kap >= 10.0
    if np.any(gauss):
        beta2 = (bg * bg) / (bg * bg + 1.0)
        mean = DEDX_MEAN * x_gcm2
        sigma = np.sqrt(np.clip(xi * t_max(bg) * (1.0 - beta2 / 2.0), 0.0, None))
        dep_g = rng.normal(mean, sigma)
        dep = np.where(gauss, dep_g, dep)

    # Physical bounds: 0 < deposit <= muon kinetic energy.
    e_kin_mev = (bg * bg + 1.0) ** 0.5 * M_MU - M_MU
    dep = np.clip(dep, 0.0, e_kin_mev)
    return dep


# --------------------------------------------------------------------------- #
# Shared logarithmic deposited-energy grid (identical to the Compton plan)     #
# --------------------------------------------------------------------------- #
#: The v1.0 grid parameters, frozen. Every archived v1.x deposit spectrum lives
#: on the edge array these produce.
_V1_0_LO_keV = 1.0e-2
_V1_0_HI_keV = 2.0e5
_V1_0_BINS_PER_DECADE = 80

#: Number of bins PREPENDED at the v1.0 spacing to reach 0.1 eV. UNIQUE:
#:   159 -> floor 0.1028536 eV, ABOVE 0.1 eV, fails success criterion 1
#:   160 -> floor 0.0999350 eV, 744 bins  <-- the only value satisfying both
#:   161 -> floor 0.0970993 eV but 745 bins, breaking "~744 bins"
_EXT_PREPENDED_BINS = 160

GRID_VERSIONS = ("v1.0", "v2.0-ext")

#: DELIBERATELY "v1.0" -- see DEVIATION D1 in 10-03-GRID-CONSTRUCTION.md.
#:
#: Plan 10-03 as written instructed making "v2.0-ext" the default so that
#: `shared_energy_grid()` "runs from 0.1 eV" literally. That instruction assumed
#: Phase 10 owns every call site. It does not: Phase 9 was executing
#: CONCURRENTLY in this worktree and adding its own unpinned callers, and
#: flipping the default made `tests/test_env_v1_identity.py::
#: test_no_photopeak_above_edge` fail with
#:     ValueError: operands could not be broadcast together with shapes (744,) (584,)
#: -- a Phase-9 file this phase is not permitted to edit.
#:
#: That failure is not an inconvenience, it is the FORBIDDEN PROXY ITSELF
#: (`fp-default-change`) caught in the act: a caller that does not state its
#: version silently receives a different axis. A v1.0 default makes silent
#: re-binning IMPOSSIBLE rather than merely pinned-against, and it fails in the
#: safe direction -- a caller that forgets to ask for the extension gets the
#: v1.0 axis and then trips the plan 10-01 `_erec_of_edep` guard if it tries to
#: evaluate sub-eV, instead of quietly re-binning an archived artifact.
#:
#: ROADMAP success criterion 1 is therefore discharged by
#: `shared_energy_grid("v2.0-ext")`, and criterion 2 is discharged more strongly
#: than the plan's own construction would have discharged it.
DEFAULT_GRID_VERSION = "v1.0"


def _v1_0_edges() -> np.ndarray:
    """The v1.0 edge array, byte-for-byte what v1.0 shipped."""
    n_dec = np.log10(_V1_0_HI_keV / _V1_0_LO_keV)
    nbins = int(round(n_dec * _V1_0_BINS_PER_DECADE))          # 584
    return np.logspace(np.log10(_V1_0_LO_keV), np.log10(_V1_0_HI_keV), nbins + 1)


def v1_0_dex_per_bin() -> float:
    """Realised decades per bin of the v1.0 grid = log10(2e7)/584.

    = 0.0125017637 dex/bin = **79.988714 bins/decade**, NOT exactly 80. The
    `round(n_dec * bins_per_decade)` in the original definition is what makes
    "80 bins/decade" nominal rather than exact, and the extension must inherit
    THIS number rather than re-solve the rounding over a wider range.
    """
    n_dec = np.log10(_V1_0_HI_keV / _V1_0_LO_keV)
    return n_dec / int(round(n_dec * _V1_0_BINS_PER_DECADE))


def shared_energy_grid(version: str = DEFAULT_GRID_VERSION) -> np.ndarray:
    """Shared log deposited-energy grid EDGES [keV]. Plan 10-03.

    ``version="v1.0"``      585 edges / 584 bins, 0.01 keV -> 2e5 keV.
                            Floor exactly 10 eV, first bin centre
                            **10.144972680282425 eV** (the "10.14 eV" quoted
                            throughout the project). This is byte-for-byte what
                            v1.0 shipped.

    ``version="v2.0-ext"``  745 edges / **744 bins**.  **NOT the default** --
                            ``DEFAULT_GRID_VERSION`` reads ``"v1.0"`` and is
                            authoritative; the extension is opt-in at every call
                            site (see the ``DEFAULT_GRID_VERSION`` note above and
                            DEVIATION D1 in 10-03-GRID-CONSTRUCTION.md).  Built by
                            **PREPENDING 160 bins at the v1.0 spacing**, NOT by
                            re-running ``logspace`` over the wider range. Floor
                            **0.0999350 eV** (<= 0.1 eV, so the axis reaches
                            0.1 eV), first bin centre **0.1013838 eV**, and
                            ``np.array_equal(edges[160:], v1_0_edges)`` is True
                            with maximum absolute difference **exactly 0.0**.

    WHY PREPEND RATHER THAN REBUILD (ROADMAP Phase 10 success criterion 2, and
    ``fp-naive-logspace``). ``np.logspace(log10(1e-4), log10(2e5), 745)`` also
    gives 744 bins and a first centre of 0.1014497 eV that looks entirely
    correct. But its spacing is log10(2e9)/744 = 0.0125013844 dex/bin against
    the v1.0 log10(2e7)/584 = 0.0125017637, so its overlapping edges drift from
    the v1.0 edges by up to **5.101629e-04 relative**. Every archived v1.x
    spectrum placed on that axis would be silently reinterpolated --- which is
    exactly the failure success criterion 2 forbids. Both constructions pass a
    bin-count check, so only ``np.array_equal`` distinguishes them; a tolerance
    check would let the drift through.

    The realised spacing is 79.988714 bins/decade, not 80 --- see
    ``v1_0_dex_per_bin``.
    """
    if version not in GRID_VERSIONS:
        raise ValueError(
            f"unknown grid version {version!r}; expected one of {GRID_VERSIONS}. "
            "Pass the version EXPLICITLY at every call site: an implicit default "
            "is how an archived v1.x product gets silently re-binned "
            "(ROADMAP Phase 10 success criterion 2)."
        )
    v1 = _v1_0_edges()
    if version == "v1.0":
        return v1
    dex = v1_0_dex_per_bin()
    prepended = _V1_0_LO_keV * 10.0 ** (
        -np.arange(_EXT_PREPENDED_BINS, 0, -1) * dex)
    ext = np.concatenate([prepended, v1])
    # In-code assertion: the tail IS the v1.0 array, exactly. Not allclose.
    assert np.array_equal(ext[_EXT_PREPENDED_BINS:], v1), (
        "extended grid tail is not bit-identical to the v1.0 edge array"
    )
    assert ext.size == 745 and ext[0] * 1.0e3 <= 0.1
    return ext


# --------------------------------------------------------------------------- #
# Full Monte-Carlo assembly of dR/dE_dep                                       #
# --------------------------------------------------------------------------- #
@dataclass
class MuonSpectrum:
    edges_kev: np.ndarray      # (Nb+1,) bin edges [keV]
    centers_kev: np.ndarray    # (Nb,) log-bin centers [keV]
    dRdE: np.ndarray           # (Nb,) counts / kg / day / keV
    dRdE_err: np.ndarray       # (Nb,) MC statistical error, same units
    rate_hz: float             # integral muon rate through the wafer [Hz]
    rate_err_hz: float         # MC error on the rate [Hz]
    vertical_mpv_mev: float    # sampled MPV for near-vertical chords [MeV]
    vertical_mean_mev: float   # mean deposit for the vertical chord [MeV]
    n_samples: int
    #: RAW, UNWEIGHTED Monte-Carlo entry count per bin.  Plan 15-02 addition:
    #: purely diagnostic, it consumes no random numbers and enters no rate, and
    #: it exists so that a bin with NO estimator support can be distinguished
    #: from a bin whose rate is genuinely small.  Defaulted so no existing
    #: constructor call site changes.
    mc_entries: np.ndarray = None  # type: ignore[assignment]
    grid_version: str = "v1.0"


# Near-vertical MPV accumulation grid (theta < 5 deg deposits, MeV).
_VERT_MPV_NBINS = 400
_VERT_MPV_RANGE = (0.3, 2.5)


def _mc_batch(n: int, rng: np.random.Generator, edges: np.ndarray,
              e_min_gev: float, e_max_gev: float):
    """Sample one batch of n muons and return its (partial) accumulators.

    Returns sumw, sumw2 (weighted histograms on `edges`), the running weight
    sums (Sum W, Sum W^2 over VALID samples), and the near-vertical fine
    histogram (theta < 5 deg deposits) with its count -- all extensive, so the
    caller simply adds batch results together. Only this batch is held in memory.
    """
    # --- sample (theta, phi, E) from the proposal ------------------------- #
    theta = rng.uniform(0.0, np.pi / 2.0, n)  # q_theta = 2/pi
    phi = rng.uniform(0.0, 2.0 * np.pi, n)    # q_phi = 1/2pi
    E, pdfE = muon_flux.sample_energy(n, rng, e_min_gev, e_max_gev)

    cth = np.cos(theta)
    sth = np.sin(theta)
    directions = wafer_geometry.direction_from_angles(theta, phi)

    intensity = muon_flux.dI_dE(E, cth)            # cm^-2 s^-1 sr^-1 GeV^-1
    a_proj = wafer_geometry.projected_area(directions)  # cm^2

    q = (2.0 / np.pi) * (1.0 / (2.0 * np.pi)) * pdfE
    weight = intensity * a_proj * sth / q          # Hz per sample

    # --- chord and deposit ------------------------------------------------- #
    ell = wafer_geometry.sample_entry_and_chord(directions, rng)  # cm
    x_gcm2 = RHO * ell
    bg = beta_gamma(E)
    dep_mev = sample_deposit(x_gcm2, bg, rng)      # MeV

    valid = (ell > 0) & (dep_mev > 0) & np.isfinite(weight)
    weight = weight[valid]
    dep_kev = dep_mev[valid] * 1.0e3
    theta_v = theta[valid]

    sumw, _ = np.histogram(dep_kev, bins=edges, weights=weight)
    sumw2, _ = np.histogram(dep_kev, bins=edges, weights=weight ** 2)
    # RAW entry count -- Plan 15-02.  Consumes no random numbers (np.histogram is
    # deterministic given the samples), so the RNG stream is unchanged and the
    # v1.0 result is bit-identical with or without this line.
    entries, _ = np.histogram(dep_kev, bins=edges)
    sum_w = float(weight.sum())
    sum_w2 = float((weight ** 2).sum())

    # near-vertical (theta < 5 deg) fine histogram over the MPV peak region.
    near_vert = theta_v < np.deg2rad(5.0)
    dv = dep_kev[near_vert] / 1.0e3  # MeV
    vhist, _ = np.histogram(dv, bins=_VERT_MPV_NBINS, range=_VERT_MPV_RANGE)
    n_near_vert = int(near_vert.sum())

    return sumw, sumw2, sum_w, sum_w2, vhist, n_near_vert, entries


def run_muon_mc(n_samples: int = 2_000_000, seed: int = 20260720,
                e_min_gev: float = 0.2, e_max_gev: float = 1.0e5,
                batch_size: int = 5_000_000,
                grid_version: str = "v1.0") -> MuonSpectrum:
    """Fold Gaisser-Guan flux (x) ray-box chord (x) Landau-Vavilov MPV deposit
    into the muon dR/dE_dep on the shared grid [counts/kg/day/keV].

    Importance-sampling measure:
      integrand of R = int I(E,theta) A_proj(Omega) sin(theta) dtheta dphi dE
      proposal q = q(theta) q(phi) q(E), q(theta)=2/pi (uniform in [0,pi/2],
      oversamples the horizon), q(phi)=1/2pi, q(E) ~ E^{-2.7}.
      weight W_i = I A_proj sin(theta) / q  -> R = mean(W_i) [Hz].
    Each muon deposits D_i(ell_i) [MeV]; the W_i-weighted histogram is dR/dE_dep.

    BATCHED ACCUMULATION (memory-bounded, reproducible at large N): the samples
    are drawn in batches of at most `batch_size`, holding only one batch in
    memory at a time, while the extensive accumulators (weighted histograms,
    Sum W, Sum W^2, near-vertical fine histogram) are summed across batches. Per-
    batch RNG streams are spawned deterministically from the master `seed` via
    np.random.SeedSequence(seed).spawn(n_batches), so the full result for a given
    (n_samples, seed, batch_size) is exactly reproducible. The histogram, rate,
    and MC errors are IDENTICAL in construction to the single-pass estimator
    (all accumulators are sums), only the sampling is chunked -- the physics,
    weighting, grid, and Landau/chord/flux models are unchanged.

    ``grid_version`` (Plan 15-02).  DEFAULTS TO ``"v1.0"``, which preserves the
    Plan 10-03 caller pin exactly: this function writes ``data/muon_dRdEdep.csv``
    and a caller that does not ask for the extension still gets the v1.0 axis.
    Pass ``"v2.0-ext"`` EXPLICITLY for the 744-bin extended run.  The RNG stream
    is independent of the histogram edges -- every random draw in ``_mc_batch``
    precedes ``np.histogram`` -- so for a given ``(n_samples, seed, batch_size)``
    the extended run's bins ``160..743`` are BIT-IDENTICAL to the v1.0 run
    (``np.array_equal``), which is what licenses the exact-re-drive route
    (``tests/test_em_extended.py::test_smallN_bit_identity_muon``).
    """
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")
    batch_size = int(batch_size)
    n_batches = int(np.ceil(n_samples / batch_size))
    child_seeds = np.random.SeedSequence(seed).spawn(n_batches)

    # PLAN 10-03 CALLER PIN, KEPT LITERALLY (Plan 15-02 leaves it in place because
    # this function writes data/muon_dRdEdep.csv -- 1e9 MC samples, validated).
    # The branch is deliberately explicit rather than collapsed to
    # `shared_energy_grid(grid_version)`: the literal v1.0 pin is what
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
    nb = edges.size - 1

    sumw = np.zeros(nb)
    sumw2 = np.zeros(nb)
    sum_w = 0.0
    sum_w2 = 0.0
    vhist = np.zeros(_VERT_MPV_NBINS)
    n_near_vert = 0
    entries = np.zeros(nb, dtype=np.int64)

    remaining = n_samples
    for b in range(n_batches):
        n_b = int(min(batch_size, remaining))
        remaining -= n_b
        rng = np.random.default_rng(child_seeds[b])
        bw, bw2, sw, sw2, bvh, bnv, bent = _mc_batch(
            n_b, rng, edges, e_min_gev, e_max_gev
        )
        sumw += bw
        sumw2 += bw2
        sum_w += sw
        sum_w2 += sw2
        vhist += bvh
        n_near_vert += bnv
        entries += bent

    # --- integral rate ----------------------------------------------------- #
    rate_hz = float(sum_w / n_samples)
    rate_err_hz = float(np.sqrt(sum_w2) / n_samples)

    # --- histogram -> dR/dE_dep [counts/kg/day/keV] ----------------------- #
    per_sample = 86400.0 / (n_samples * wafer_geometry.MASS_KG)  # Hz -> cts/kg/day
    dRdE = sumw * per_sample / dwidth
    dRdE_err = np.sqrt(sumw2) * per_sample / dwidth

    # --- near-vertical MPV (theta < 5 deg -> chord ~ 0.20 cm) -------------- #
    if n_near_vert > 1000:
        be = np.linspace(_VERT_MPV_RANGE[0], _VERT_MPV_RANGE[1], _VERT_MPV_NBINS + 1)
        bc = 0.5 * (be[1:] + be[:-1])
        # Fine histogram over the peak region + light smoothing for a stable mode.
        kernel = np.ones(7) / 7.0
        smooth = np.convolve(vhist, kernel, mode="same")
        vertical_mpv = float(bc[np.argmax(smooth)])
    else:
        vertical_mpv = float("nan")
    vertical_mean = DEDX_MEAN * RHO * wafer_geometry.CHORD_VERTICAL  # 1.46 MeV

    return MuonSpectrum(
        edges_kev=edges,
        centers_kev=centers,
        dRdE=dRdE,
        dRdE_err=dRdE_err,
        rate_hz=rate_hz,
        rate_err_hz=rate_err_hz,
        vertical_mpv_mev=vertical_mpv,
        vertical_mean_mev=vertical_mean,
        n_samples=n_samples,
        mc_entries=entries,
        grid_version=grid_version,
    )


def write_csv(spec: MuonSpectrum, path: str) -> None:
    """Write dR/dE_dep to CSV: E_dep_keV, dRdEdep_cts_per_kg_day_keV, mc_err."""
    import csv

    header_lines = [
        "# Muon deposited-energy spectrum dR/dE_dep for the 4in x 4in x 2mm Ge wafer",
        "# Plan 04-01 (CALC-03/VALD-02). Gaisser-Guan flux (x) ray-box chord (x)",
        "# Landau-Vavilov MPV deposit. UNIFIED PHONON SCALE, NO quenching (CONVENTIONS B).",
        f"# integral_muon_rate_Hz = {spec.rate_hz:.4f} +/- {spec.rate_err_hz:.4f}",
        f"# vertical_chord_MPV_MeV = {spec.vertical_mpv_mev:.4f} "
        f"(mean = {spec.vertical_mean_mev:.4f}; MPV < mean by construction)",
        f"# n_mc_samples = {spec.n_samples}; seed fixed for reproducibility",
        "# units: E_dep_keV [keV]; dRdEdep [counts/kg/day/keV]; mc_err [counts/kg/day/keV]",
        "# grid: shared log E_dep, 0.01 keV -> 2e5 keV (200 MeV), ~80 bins/decade",
    ]
    with open(path, "w", newline="") as f:
        for line in header_lines:
            f.write(line + "\n")
        w = csv.writer(f)
        w.writerow(["E_dep_keV", "dRdEdep_cts_per_kg_day_keV", "mc_err"])
        for c, y, e in zip(spec.centers_kev, spec.dRdE, spec.dRdE_err):
            w.writerow([f"{c:.6e}", f"{y:.6e}", f"{e:.6e}"])
