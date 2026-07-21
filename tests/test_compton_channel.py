"""Phase-4 Plan 04-02, Task 2 unit tests: Klein-Nishina angle-sampled electron
continuum and the Compton dR/dE_dep assembly with the VALD-03 checks.

Guards:
  * edges self-validate: max sampled T_e = E_edge = 2E^2/(m_e c^2+2E)  (VALD-03)
  * CONTINUUM only, NO photopeaks (deposit = T_e < E_gamma)   -> fp-full-absorption
  * deposit = electron recoil T_e, not E_gamma / not E'       -> fp-electron-not-photon
  * total rate within factor ~2 of flux x sigma_KN x N_e      (VALD-03)
  * SHARED E_dep grid identical to the muon channel (04-01 co-add)
  * convergence: edges + edge-adjacent bins stable < 5% under 2x samples
"""
import numpy as np
import pytest

from qpd_potential import compton_deposit as cd
from qpd_potential import compton_source as cs
from qpd_potential.muon_deposit import shared_energy_grid

# Module-scoped baseline run (kept modest for test speed; edges are seed-robust).
_SPEC = cd.run_compton_mc(n_per_line=120_000, seed=20260720)


def _y_at(spec, e_kev):
    i = int(np.argmin(np.abs(spec.centers_kev - e_kev)))
    return spec.dRdE[i]


# --------------------------------------------------------------------------- #
# VALD-03 / test-compton-edges: self-validating Klein-Nishina edges            #
# --------------------------------------------------------------------------- #
def test_edges_at_klein_nishina_energies():
    """Each line's max sampled T_e equals the closed-form Compton edge."""
    for eg, ed, eds in zip(_SPEC.line_energies, _SPEC.line_edges,
                           _SPEC.line_edges_sampled):
        assert eds == pytest.approx(ed, abs=0.5)               # kinematic edge
        assert float(cs.compton_edge_kev(eg)) == pytest.approx(ed, rel=1e-9)


def test_vald03_target_edges():
    """The named VALD-03 targets: 40K->1243.4, 208Tl->2381.7, 214Bi->1541.3 keV."""
    edges = {round(eg): ed for eg, ed in zip(_SPEC.line_energies, _SPEC.line_edges)}
    assert edges[1461] == pytest.approx(1243.4, abs=1.0)       # 40K 1460.8
    assert edges[2615] == pytest.approx(2381.7, abs=1.0)       # 208Tl 2614.5
    assert edges[1764] == pytest.approx(1541.3, abs=1.0)       # 214Bi 1764.5


# --------------------------------------------------------------------------- #
# Continuum, NOT photopeaks (fp-full-absorption, fp-electron-not-photon)        #
# --------------------------------------------------------------------------- #
def test_no_photopeaks_continuum_only():
    """No full-energy absorption: zero signal above the max Compton edge and at
    the highest line energy; every deposit is below its line's E_gamma."""
    max_edge = float(_SPEC.line_edges.max())                   # 2381.8 keV
    c, y = _SPEC.centers_kev, _SPEC.dRdE
    assert np.all(y[c > max_edge * 1.02] == 0.0)               # nothing above max edge
    assert _y_at(_SPEC, _SPEC.line_energies.max()) == 0.0      # no peak at 2614.5 keV
    # structurally: max deposit per line is the edge, strictly below E_gamma.
    assert np.all(_SPEC.line_edges_sampled < _SPEC.line_energies)


def test_deposit_is_electron_recoil():
    """Deposit = T_e = E_gamma - E', bounded in [0, E_edge] (electron, not photon)."""
    rng = np.random.default_rng(3)
    eg = 1460.822
    te = cd.sample_electron_recoil(eg, 200_000, rng)
    assert te.min() >= 0.0
    assert te.max() <= float(cs.compton_edge_kev(eg)) + 1e-6
    assert te.max() < eg                                       # never full-energy
    # continuum: spans a broad range, not a spike at one value.
    assert te.std() > 0.15 * te.mean()


# --------------------------------------------------------------------------- #
# VALD-03 total rate within factor ~2 of flux x Compton cross section          #
# --------------------------------------------------------------------------- #
def test_total_rate_within_factor_two():
    """Total single-scatter rate vs the independent flux x sigma_KN x N_e anchor."""
    ratio = _SPEC.rate_hz / _SPEC.rate_anchor_hz
    assert 0.5 < ratio < 2.0                                   # VALD-03 factor ~2
    assert ratio == pytest.approx(1.0, abs=0.1)                # actually ~few %
    assert _SPEC.rate_hz > 0.0


def test_energy_closure():
    """int dR/dE_dep dE = total_rate * 86400 / mass_kg (counts/kg/day).

    Closure holds to ~1e-5: a negligible fraction of near-forward-scatter deposits
    have T_e below the 0.01 keV shared-grid floor and correctly drop from the
    histogram (sub-threshold, physically ~zero-energy deposits)."""
    expected = _SPEC.rate_hz * 86400.0 / cs.MASS_KG
    assert _SPEC.counts_per_kg_day == pytest.approx(expected, rel=1e-4)
    assert _SPEC.counts_per_kg_day <= expected                 # only sub-floor loss


# --------------------------------------------------------------------------- #
# Shared grid + convergence (test-compton-convergence)                         #
# --------------------------------------------------------------------------- #
def test_shared_grid_matches_muon():
    assert np.array_equal(_SPEC.edges_kev, shared_energy_grid())


def test_convergence_edges_and_bins():
    """Edges and edge-adjacent bins stable < 5% under a 2x sample increase; the
    total rate is analytic (seed-independent), so it is exactly stable."""
    s1 = cd.run_compton_mc(n_per_line=100_000, seed=11)
    s2 = cd.run_compton_mc(n_per_line=200_000, seed=11)
    # edges: kinematic, stable to well under a keV.
    assert np.max(np.abs(s1.line_edges_sampled - s2.line_edges_sampled)) < 0.5
    # total interaction rate is analytic -> identical.
    assert s1.rate_hz == pytest.approx(s2.rate_hz, rel=1e-12)
    # edge-adjacent spectral content (window below the strong 40K edge) stable.
    c = s1.centers_kev
    wd = np.diff(s1.edges_kev)
    win = (c > 1000.0) & (c < 1243.0)
    I1 = float((s1.dRdE[win] * wd[win]).sum())
    I2 = float((s2.dRdE[win] * wd[win]).sum())
    assert abs(I1 - I2) / I2 < 0.05
    # edge-adjacent bins are statistically resolved (non-empty, small MC error).
    i = int(np.argmin(np.abs(c - 1200.0)))
    assert s2.dRdE[i] > 0.0
    assert s2.dRdE_err[i] / s2.dRdE[i] < 0.1


def test_per_bin_mc_error_column_present():
    """The CSV-facing spectrum carries a per-bin MC error, small where populated."""
    y, e = _SPEC.dRdE, _SPEC.dRdE_err
    pop = y > 0
    assert np.all(e[pop] >= 0.0)
    assert np.median((e[pop] / y[pop])) < 0.2
