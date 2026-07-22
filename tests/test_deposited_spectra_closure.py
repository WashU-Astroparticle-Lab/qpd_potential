# Tests for the Phase-4 deposited-energy ASSEMBLY (Plan 04-03).
#
# Covers the three plan acceptance tests:
#   test-shared-grid    : muon and Compton CSVs on the identical log E_dep grid
#   test-energy-closure : per-channel int dR/dE_dep dE == rate*86400/mass_kg
#   test-pileup         : total-rate x pulse-duration occupancy << 1 vs 50 kHz
#
# Deposited energy only (no E_rec fold) -- guards fp-reconstructed-not-deposited,
# fp-grid-mismatch, fp-pileup-unchecked.
import numpy as np
import pytest

from qpd_potential import deposited_spectra as ds
from qpd_potential import wafer_geometry as wg


@pytest.fixture(scope="module")
def result():
    return ds.assemble()


# --- test-shared-grid --------------------------------------------------------

def test_shared_grid_identical(result):
    """Both channels are on the identical shared log E_dep grid."""
    muon = result["muon"].E_dep_keV
    compton = result["compton"].E_dep_keV
    assert muon.shape == compton.shape == (584,)
    # byte-identical grids in these CSVs; assert exact equality then rel tol.
    assert np.array_equal(muon, compton)
    assert result["grid_max_rel"] <= 1e-9


def test_grid_matches_canonical_shared_grid(result):
    """CSV bin centers are the geometric means of the canonical shared edges."""
    edges, centers, dE = ds.bin_edges_and_widths()
    assert centers.shape == result["E_dep_keV"].shape
    max_rel = np.max(np.abs(result["E_dep_keV"] - centers) / centers)
    assert max_rel < 1e-5          # 6-sig-fig CSV rounding
    # grid span: 0.01 keV -> 200 MeV
    assert edges[0] == pytest.approx(1.0e-2, rel=1e-12)
    assert edges[-1] == pytest.approx(2.0e5, rel=1e-12)


def test_grid_mismatch_is_rejected():
    """assert_shared_grid must raise on a perturbed grid (fp-grid-mismatch)."""
    a = np.array([1.0, 2.0, 3.0])
    b = a.copy()
    b[1] *= 1.001
    with pytest.raises(ValueError):
        ds.assert_shared_grid(a, b, rtol=1e-9)
    with pytest.raises(ValueError):
        ds.assert_shared_grid(a, a[:-1])   # length mismatch


# --- test-energy-closure -----------------------------------------------------

def test_energy_closure_muon(result):
    """Muon int dR/dE_dep dE == rate*86400/mass_kg within MC error."""
    c = result["closures"]["muon"]
    # ratio consistent with 1 within ~3x the MC error band, and <0.5% absolute.
    band = 3.0 * c.count_integral_err / c.expected
    assert abs(c.ratio - 1.0) < max(band, 5e-3)


def test_energy_closure_compton(result):
    """Compton int dR/dE_dep dE == rate*86400/mass_kg within MC error."""
    c = result["closures"]["compton"]
    assert abs(c.ratio - 1.0) < 5e-3


def test_closure_uses_correct_mass_normalization(result):
    """The closure expectation uses the per-kg wafer mass (0.1099 kg)."""
    c = result["closures"]["muon"]
    expected = result["muon"].rate_Hz * ds.SECONDS_PER_DAY / wg.MASS_KG
    assert c.expected == pytest.approx(expected, rel=1e-12)
    assert wg.MASS_KG == pytest.approx(0.1099, rel=1e-3)


def test_deposited_power_first_moment_physical(result):
    """Mean deposit per event is physical: muon few-MeV, Compton few-hundred-keV.

    The angular-averaged muon mean deposit exceeds the 1.459 MeV vertical-chord
    mean (04-01) because inclined chords are longer; the Compton continuum mean
    sits below its ~2.4 MeV max edge. Both are deposited (phonon) energy.
    """
    mu = result["closures"]["muon"].mean_deposit_keV
    co = result["closures"]["compton"].mean_deposit_keV
    assert 1.459e3 < mu < 1.0e4        # above vertical mean, below 10 MeV
    assert 100.0 < co < 2.4e3          # below the 2382 keV max Compton edge


# --- co-addition -------------------------------------------------------------

def test_total_is_sum_of_channels(result):
    """Total spectrum is exactly muon + Compton on the shared grid."""
    total = result["total"]
    recon = result["muon"].dRdEdep + result["compton"].dRdEdep
    assert np.allclose(total, recon, rtol=0, atol=0)
    assert np.all(total >= 0)


def test_total_rate_closure(result):
    """Integral of the TOTAL spectrum equals the summed independent rate."""
    _, _, dE = ds.bin_edges_and_widths()
    C_tot = np.sum(result["total"] * dE)
    R_tot = result["muon"].rate_Hz + result["compton"].rate_Hz
    expected = R_tot * ds.SECONDS_PER_DAY / wg.MASS_KG
    assert C_tot / expected == pytest.approx(1.0, abs=5e-3)


# --- test-pileup -------------------------------------------------------------

def test_pileup_occupancy_far_below_bandwidth(result):
    """Event-level occupancy << 1: a few Hz against the 50 kHz bandwidth."""
    pu = result["pileup"]
    assert pu.total_rate_Hz == pytest.approx(1.634, abs=2e-3)
    assert pu.occupancy_sample < 1e-3          # 50 kHz / 20 us slot
    assert pu.occupancy_resolve < 1e-3         # 25 kHz / 40 us resolving
    assert pu.rate_over_bandwidth < 1e-3
    assert not pu.stop_condition_triggered     # stop-condition NOT triggered
    # mean interval between events >> pulse duration
    assert pu.mean_interval_s > 0.1
    assert pu.mean_interval_s / ds.RESOLVE_TIME_S > 1e3


def test_pileup_deadtime_and_livetime_consistent(result):
    """Non-paralyzable dead-time and paralyzable live-time agree at small R*tau."""
    pu = result["pileup"]
    # to first order both reduce to R*tau ~ 6.5e-5
    assert pu.deadtime_frac_nonparalyzable == pytest.approx(pu.occupancy_resolve, rel=1e-3)
    assert pu.livetime_frac_paralyzable == pytest.approx(1.0 - pu.occupancy_resolve, rel=1e-3)


def test_pileup_stop_condition_triggers_when_rate_high():
    """A hypothetical ~10 kHz rate must flip the stop-condition flag ON."""
    pu = ds.pileup_occupancy({"muon": 1.0e4, "compton": 5.0e3})
    assert pu.stop_condition_triggered
    assert pu.occupancy_resolve > 1e-2


# --- deposited (not reconstructed) -------------------------------------------

def test_deliverable_is_deposited_energy(result):
    """No E_rec mapping applied here; axis is deposited (phonon) energy.

    The muon high-E deposit tail must survive to ~200 MeV (the Phase-5
    saturation input); a reconstructed-energy fold would compress it.
    Guards fp-reconstructed-not-deposited.
    """
    E = result["E_dep_keV"]
    muon = result["muon"].dRdEdep
    tail = E[muon > 0].max()
    assert tail > 1.0e5           # > 100 MeV, i.e. the raw deposited tail is intact
