"""Acceptance tests for the frozen flux table, split band, and Billard variant (Plan 02-02).

Covers test-csv-schema, test-band-split, and test-billard-variant, and guards the
forbidden proxy fp-uniform-band.
"""
import os

import numpy as np
import pytest

from src.flux.assemble_spectrum import assemble, SEAM_LO, SEAM_HI
from src.flux import build_flux_table as bt
from src.flux import normalization as norm

_DATADIR = os.path.join(bt._ROOT, "data", "flux")
FROZEN = os.path.join(_DATADIR, "reactor_flux_v1.0.csv")
BILLARD = os.path.join(_DATADIR, "reactor_flux_billard_variant.csv")
FIG = os.path.join(bt._FIGDIR, "flux_overlay.png")

EXPECTED_COLS = [
    "E_nu_MeV", "flux_nu_per_cm2_per_s_per_MeV", "flux_fission_HM",
    "flux_fission_summation", "flux_ncapture_238U", "rel_uncertainty", "region_flag",
]


def _read_csv(path):
    header, data, comments = None, [], []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                comments.append(line)
            elif header is None:
                header = line.strip().split(",")
            else:
                data.append(line.strip().split(","))
    return header, data, comments


@pytest.fixture(scope="module")
def frozen():
    # regenerate to guarantee freshness against the current code
    spec = assemble()
    bt.write_frozen_csv(spec, FROZEN)
    return _read_csv(FROZEN)


# --------------------------------------------------------------------------------
# test-csv-schema
# --------------------------------------------------------------------------------
def test_csv_schema_columns(frozen):
    header, data, _ = frozen
    assert header == EXPECTED_COLS
    assert len(data) > 50
    for row in data:
        assert len(row) == 7


def test_csv_region_flags(frozen):
    header, data, _ = frozen
    flags = {row[6] for row in data}
    assert flags <= {"above_2MeV", "seam", "below_1p8MeV"}
    assert flags == {"above_2MeV", "seam", "below_1p8MeV"}


def test_csv_rel_uncertainty_every_row(frozen):
    header, data, _ = frozen
    for row in data:
        u = float(row[5])
        assert 0.0 < u < 1.0


def test_csv_provenance_header(frozen):
    _, _, comments = frozen
    blob = "".join(comments).lower()
    assert "v1.0" in blob
    assert "git_sha" in blob
    assert "gw_th" in blob
    assert "205.8" in blob or "<e_f>" in blob          # effective thermal energy documented
    assert "huber" in blob and "mueller" in blob        # per-source provenance
    assert "kopeikin" in blob                            # sub-1.8 grounding cited
    assert "7-8e12" in blob or "7.5" in blob             # integral check recorded
    assert "hayes-vogel" in blob or "2e20" in blob       # emission cross-check recorded


def test_csv_component_additivity(frozen):
    header, data, _ = frozen
    tot = np.array([float(r[1]) for r in data])
    hm = np.array([float(r[2]) for r in data])
    summ = np.array([float(r[3]) for r in data])
    cap = np.array([float(r[4]) for r in data])
    assert np.allclose(tot, hm + summ + cap, rtol=1e-5)


# --------------------------------------------------------------------------------
# test-band-split  (+ fp-uniform-band guard)
# --------------------------------------------------------------------------------
def test_band_split_widens_across_seam(frozen):
    header, data, _ = frozen
    E = np.array([float(r[0]) for r in data])
    u = np.array([float(r[5]) for r in data])
    flag = np.array([r[6] for r in data])
    above = u[flag == "above_2MeV"]
    below = u[flag == "below_1p8MeV"]
    assert above.max() <= 0.05 + 1e-9 and above.min() >= 0.02 - 1e-9   # ~2-5%
    assert below.min() >= 0.15                                          # model-only >=15%
    assert below.max() <= 0.30
    # NOT uniform: the below-seam band is strictly wider than the above-seam band
    assert below.min() > above.max()


def test_fp_uniform_band_rejected(frozen):
    """The band is genuinely split, not a single constant carried across the spectrum."""
    header, data, _ = frozen
    u = np.array([float(r[5]) for r in data])
    assert u.max() / u.min() >= 3.0        # >=3x spread -> demonstrably non-uniform


def test_overlay_235U_agrees_with_published_huber_above_2MeV():
    """Above 2 MeV the computed 235U flux matches published Huber within the band."""
    spec = assemble()
    K, _ = norm.normalization_constant(spec.fractions)
    f235 = spec.fractions["235U"]
    computed = spec.per_isotope["235U"] * f235 * K
    E = spec.E
    # published Huber 235U tabulation
    bench = []
    with open(os.path.join(_DATADIR, "huber_U235_benchmark.csv")) as bf:
        for line in bf:
            if line.startswith("#") or line.startswith("E_nu"):
                continue
            a, b = line.strip().split(",")
            bench.append((float(a), float(b)))
    for Eb, Spub in bench:
        if Eb < 2.0 or Eb > 7.0:
            continue
        pub_flux = Spub * f235 * K
        comp = float(np.interp(Eb, E, computed))
        band = bt.rel_uncertainty(np.array([Eb]))[0]
        assert abs(comp - pub_flux) / pub_flux <= max(band, 0.06)


def test_overlay_figure_exists():
    spec = assemble()
    bt.make_overlay_figure(spec, FIG)
    assert os.path.exists(FIG) and os.path.getsize(FIG) > 5000


# --------------------------------------------------------------------------------
# test-billard-variant
# --------------------------------------------------------------------------------
def test_billard_variant_constant_below_2MeV():
    spec = assemble()
    bt.write_billard_variant_csv(BILLARD, grid=spec.E)
    header, data, comments = _read_csv(BILLARD)
    E = np.array([float(r[0]) for r in data])
    # per-isotope columns are S_235U_constbelow2 ... : held flat below 2 MeV
    for j, iso in enumerate(["235U", "238U", "239Pu", "241Pu"]):
        col = np.array([float(r[2 + j]) for r in data])
        below = col[E < SEAM_HI]
        assert np.allclose(below, below[0], rtol=1e-9)     # constant below 2 MeV


def test_billard_variant_fractions_isotope_labelled():
    _, _, comments = _read_csv(BILLARD)
    blob = "".join(comments)
    # Billard fractions correctly isotope-labelled (no 238U<->239Pu swap):
    # 235U 55.6, 239Pu 32.6, 238U 7.1, 241Pu 4.7
    assert "'235U': 0.556" in blob
    assert "'239Pu': 0.326" in blob
    assert "'238U': 0.071" in blob
    assert "'241Pu': 0.047" in blob
    assert "billard" in blob.lower()


def test_billard_variant_distinct_from_flagship():
    """The Billard variant integral flux differs from the flagship (constant vs summation)."""
    spec = assemble()
    phi_flag = norm.absolute_flux(spec.total(), spec.fractions)
    F_flag = norm.integral_flux(spec.E, phi_flag)
    bchecks = bt.write_billard_variant_csv(BILLARD, grid=spec.E)
    F_bill = bchecks["integral_flux"]
    assert abs(F_bill - F_flag) / F_flag > 0.20     # materially distinct
