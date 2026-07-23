# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Phase-9 Plan 09-02: executable checks for the sea-level ambient neutron flux.

These close Phase-7 verification gap D2 -- "No PARMA driver committed; the
decisive 3.55e-3 and 1.317e-2 integrals cannot be recomputed" -- by recomputing
BOTH anchor integrals AND data/ambient_neutron_flux_v1.1.csv's own phi_default
column from committed code at the pinned PARMA commit.

Order matters and is enforced by the test names and docstrings: the UNTUNED
(k = 1) comparison against Gordon is the honest cross-check and is reported
BEFORE the anchor rescale.  An agreement that only appears after tuning is not a
cross-check at all.

Guards:
  * fp-neutron-from-memory     -- every number comes from committed code or a frozen file
  * fp-gordon-as-shape         -- Sato/PARMA is the shape, Gordon the integral anchor only
  * fp-lethargy-double-divide  -- proved by an integral identity, not by inspection
  * fp-indoor-band-as-central  -- phi_lo is never used as a central value or an error bar
  * fp-precision-inflation     -- every emitted quantity carries order_of_magnitude
  * fp-thermal-zero            -- Phi_th is a named, strictly positive scalar
"""
from __future__ import annotations

import os
import re

import numpy as np
import pytest

from qpd_potential import parma_neutron_flux as pn

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V11_CSV = os.path.join(REPO, "data", "ambient_neutron_flux_v1.1.csv")
THERMAL_CSV = os.path.join(REPO, "data", "ambient_neutron_thermal_v2.0.csv")
MANIFEST = os.path.join(REPO, "data", "external", "parma", "MANIFEST.md")
DECLARATION = os.path.join(
    REPO, "GPD", "phases", "09-sea-level-surface-environment-lock-p-env",
    "09-02-NEUTRON-DECLARATION.md",
)

#: Tolerances -- STATED BEFORE the checks run (Plan 09-02 acceptance tests) and
#: never loosened afterwards.
TOL_NATIVE_FRAC = 0.02       # untuned Phi(10 MeV-10 GeV) vs 3.239e-3
TOL_NODE_DOUBLING = 0.005    # quadrature convergence on node doubling
TOL_ANCHORED_FRAC = 0.01     # anchored Phi vs 3.550e-3, and solved k vs 1.09610
TOL_BROAD_FRAC = 0.05        # Phi(0.01 eV-10 GeV) vs 1.317e-2
TOL_JOINT_MEDIAN = 0.01      # driver vs committed phi_default, median
TOL_JOINT_MAX = 0.05         # driver vs committed phi_default, max
TOL_LETHARGY = 0.01          # INT phi dE vs INT (E phi) dlnE

requires_parma = pytest.mark.skipif(
    not pn.parma_available(),
    reason=("frozen PARMA source or c++ absent -- run `sh data/external/parma/"
            "fetch_parma.sh` (Plan 09-02 Task 1). NOT a pass: the anchor "
            "integrals are then NOT reproducible in-repo and Phase-7 gap D2 "
            "persists."),
)


def _v11_table():
    e_kev, phi_def, phi_lo, phi_hi = [], [], [], []
    with open(V11_CSV, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("E_n_lo"):
                continue
            a = line.split(",")
            e_kev.append(float(a[1]))
            phi_def.append(float(a[3]))
            phi_lo.append(float(a[4]))
            phi_hi.append(float(a[5]))
    return (np.array(e_kev), np.array(phi_def), np.array(phi_lo), np.array(phi_hi))


# --------------------------------------------------------------------------- #
# Cache integrity                                                              #
# --------------------------------------------------------------------------- #
def test_cache_integrity_manifest():
    """The frozen PARMA cache records commit, command, hashes and verdicts."""
    text = open(MANIFEST, encoding="utf-8").read()
    assert pn.PINNED_COMMIT in text
    assert "codeload.github.com/WeiMXi/PARMA" in text
    assert text.count("real source") + text.count("real coefficient") >= 10
    assert "WebFetch" in text and "NOT used" in text
    assert "U+2009" in text
    # every artifact row carries a 64-hex SHA-256
    assert len(re.findall(r"`[0-9a-f]{64}`", text)) >= 12

    coeff_dir = os.path.join(REPO, "data", "external", "parma", "neutro_coefficients")
    assert os.path.isfile(os.path.join(coeff_dir, "fitting-lowspec.inp")), (
        "the input/neutro coefficient files the committed CSV header names must "
        "be committed -- they are the part the Sato-2015 article does not tabulate"
    )
    # ...and the recorded hashes are the hashes on disk
    import hashlib
    for name in sorted(os.listdir(coeff_dir)):
        digest = hashlib.sha256(open(os.path.join(coeff_dir, name), "rb").read()).hexdigest()
        assert digest in text, f"{name}: on-disk SHA-256 {digest} not in MANIFEST"


def test_shape_vs_anchor_roles():
    """Sato/PARMA = differential SHAPE; Gordon = >10 MeV INTEGRAL anchor only."""
    for path in (MANIFEST, DECLARATION, pn.__file__):
        text = open(path, encoding="utf-8").read()
        assert "PARMA" in text and "Sato" in text
        assert "Gordon" in text
        low = text.lower()
        assert "paywall" in low, f"{path}: the Gordon paywall statement is missing"
        assert "shape" in low and "integral" in low
    # the module's own metadata cannot be read the other way round
    assert "Sato" in pn.NeutronFlux.__dataclass_fields__["shape_source"].default
    assert "Gordon" in pn.NeutronFlux.__dataclass_fields__["norm_anchor"].default
    assert "gt10MeV_only" in pn.NeutronFlux.__dataclass_fields__["norm_anchor"].default


# --------------------------------------------------------------------------- #
# 1. UNTUNED FIRST                                                             #
# --------------------------------------------------------------------------- #
@requires_parma
def test_untuned_native_integral_reported_first():
    """k = 1: Phi(10 MeV-10 GeV) reproduces PARMA's native 3.239e-3.

    This is the UNTUNED cross-check against Gordon -- ~9% agreement with NO
    fitting.  It is the only independent validation the channel has.
    """
    lo = pn.integral_flux(10.0, 1.0e4, k=1.0, per_decade=200)
    hi = pn.integral_flux(10.0, 1.0e4, k=1.0, per_decade=400)

    assert lo == pytest.approx(pn.PHI_NATIVE_10MEV_10GEV,
                               rel=TOL_NATIVE_FRAC)
    # quadrature convergence under node doubling
    assert abs(hi - lo) / lo < TOL_NODE_DOUBLING

    # ...and the untuned-vs-Gordon agreement really is ~10%, not a tuned match
    untuned_vs_gordon = (lo - pn.PHI_GORDON_10MEV_10GEV) / pn.PHI_GORDON_10MEV_10GEV
    assert -0.15 < untuned_vs_gordon < 0.0


# --------------------------------------------------------------------------- #
# 2. ANCHORED                                                                  #
# --------------------------------------------------------------------------- #
@requires_parma
def test_anchored_integral_and_solved_k():
    """k = 1.09610 lands on Gordon 3.550e-3; the solved k reproduces 1.09610."""
    phi = pn.integral_flux(10.0, 1.0e4, k=pn.K_GORDON_ANCHOR, per_decade=400)
    assert phi == pytest.approx(pn.PHI_GORDON_10MEV_10GEV, rel=TOL_ANCHORED_FRAC)

    k = pn.solve_anchor_scalar(per_decade=400)
    assert k == pytest.approx(pn.K_GORDON_ANCHOR, rel=TOL_ANCHORED_FRAC)


@requires_parma
def test_broad_integral():
    """Phi(0.01 eV-10 GeV) reproduces the committed header's 1.317e-2."""
    phi = pn.integral_flux(pn.E_PARMA_FLOOR_MEV, 1.0e4,
                           k=pn.K_GORDON_ANCHOR, per_decade=200)
    assert phi == pytest.approx(pn.PHI_BROAD_0P01EV_10GEV, rel=TOL_BROAD_FRAC)


# --------------------------------------------------------------------------- #
# 3. JOINT IDENTITY -- the D2 closure                                          #
# --------------------------------------------------------------------------- #
@requires_parma
def test_driver_reproduces_committed_table_pointwise():
    """THE Phase-7 gap-D2 check: the committed table vs its recorded provenance.

    The two had only ever been validated separately.  Here the recompiled pinned
    source is evaluated at the table's OWN bin centres and compared pointwise.
    """
    e_kev, phi_committed, _, _ = _v11_table()
    phi_driver = pn.differential_flux(e_kev / 1.0e3,
                                      k=pn.K_GORDON_ANCHOR).phi_cm2_s_mev
    rel = np.abs(phi_driver - phi_committed) / phi_committed

    assert np.median(rel) <= TOL_JOINT_MEDIAN, (
        f"median deviation {np.median(rel):.3%} -- the committed table may not be "
        "what its recorded provenance describes")
    assert rel.max() <= TOL_JOINT_MAX, (
        f"max deviation {rel.max():.3%} at E_n = {e_kev[rel.argmax()]:.6g} keV")


# --------------------------------------------------------------------------- #
# 4. LETHARGY                                                                  #
# --------------------------------------------------------------------------- #
@requires_parma
@pytest.mark.parametrize("lo,hi", [
    (1e-8, 1e-7),    # thermal
    (1e-6, 1e-5),    # epithermal, eV
    (1e-3, 1e-2),    # keV
    (1.0, 10.0),     # MeV, evaporation
    (100.0, 1000.0),  # cascade
])
def test_lethargy_divided_exactly_once(lo, hi):
    """INT phi dE == INT (E phi) d(ln E) iff the /E was applied exactly once.

    A systematic factor of E or 1/E between the two means the lethargy division
    was applied zero times or twice.  Either fails.
    """
    e = pn.log_grid(lo, hi, per_decade=2000)
    phi = pn.differential_flux(e, k=1.0).phi_cm2_s_mev
    per_energy = np.trapz(phi, e)
    lethargy = np.trapz(e * phi, np.log(e))
    assert per_energy > 0
    assert abs(lethargy - per_energy) / per_energy < TOL_LETHARGY


# --------------------------------------------------------------------------- #
# 5. MORPHOLOGY                                                                #
# --------------------------------------------------------------------------- #
@requires_parma
def test_spectral_morphology_four_features():
    """All four canonical ground-level features.  A feature-free spectrum is a bug.

    thermal Maxwellian peak / 1/E epithermal plateau / 1-3 MeV evaporation hump /
    ~100 MeV cascade peak.
    """
    e = pn.log_grid(1e-8, 1e4, per_decade=120)
    phi = pn.differential_flux(e, k=pn.K_GORDON_ANCHOR).phi_cm2_s_mev
    lethargy = e * phi   # E*phi on a log-E axis

    # (a) thermal peak.  phi(E) itself peaks at PARMA's E_th = 2.5e-8 MeV
    # = 0.025 eV ~= kT at 293.6 K (0.0253 eV): phi ~ E exp(-E/E_th).  The
    # LETHARGY representation E*phi peaks one factor of E higher, at 2*E_th
    # = 0.05 eV.  Both describe the SAME feature; check the phi peak, which is
    # the "~0.03 eV" of the standard description.
    m = e < 1e-6
    e_peak_ev = e[m][np.argmax(phi[m])] * 1e6
    assert 0.01 < e_peak_ev < 0.10, f"thermal peak at {e_peak_ev:.4f} eV"
    assert e_peak_ev == pytest.approx(0.025, rel=0.2)

    # (b) 1/E epithermal plateau over ~1 eV - 10 keV: E*phi flat to a factor ~2
    m2 = (e >= 1e-6) & (e <= 1e-2)
    assert lethargy[m2].max() / lethargy[m2].min() < 2.0

    # (c) evaporation hump in 1-3 MeV
    m3 = (e >= 0.3) & (e <= 10.0)
    e_evap = e[m3][np.argmax(lethargy[m3])]
    assert 1.0 <= e_evap <= 3.0, f"evaporation hump at {e_evap:.3g} MeV"

    # (d) cascade peak near 100 MeV
    m4 = (e >= 20.0) & (e <= 1000.0)
    e_casc = e[m4][np.argmax(lethargy[m4])]
    assert 50.0 <= e_casc <= 300.0, f"cascade peak at {e_casc:.3g} MeV"

    # (e) NOT monotone: a feature-free spectrum would have no interior extrema
    turns = int(np.sum(np.diff(np.sign(np.diff(lethargy))) != 0))
    assert turns >= 3, "monotone / feature-free spectrum is a bug, not a result"


# --------------------------------------------------------------------------- #
# 6. THERMAL COMPONENT                                                         #
# --------------------------------------------------------------------------- #
@requires_parma
def test_thermal_named_and_positive():
    """Phi_th is a named, STRICTLY POSITIVE scalar with STATED bounds."""
    phi_th, meta = pn.thermal_flux(per_decade=800)
    assert phi_th > 0.0
    assert meta["quantity"] == "Phi_th"
    assert meta["e_lo_mev"] == pn.E_PARMA_FLOOR_MEV
    assert meta["e_cut_mev"] == pn.E_THERMAL_CUTOFF_MEV
    assert "cadmium" in meta["cutoff_convention"].lower()
    assert meta["accuracy_label"] == "order_of_magnitude"
    assert meta["on_shared_energy_grid"] is False


def test_thermal_table_header_and_grid():
    """The sub-eV table names Phi_th, its bounds, and its NOT-shared grid."""
    assert os.path.isfile(THERMAL_CSV), (
        "data/ambient_neutron_thermal_v2.0.csv missing -- ROADMAP SC4 requires "
        "either a named Phi_th or a NAMED GAP, never a silent omission")
    text = open(THERMAL_CSV, encoding="utf-8").read()

    m = re.search(r"Phi_th = ([0-9.eE+-]+) cm\^-2 s\^-1", text)
    assert m, "the header must name Phi_th with its value"
    value = float(m.group(1))
    assert value > 0.0, "Phi_th must never be zero (ROADMAP SC4, fp-thermal-zero)"

    assert "integration bounds" in text
    assert "cadmium cutoff" in text
    assert "NOT the project shared_energy_grid()" in text
    assert "INCIDENT NEUTRON KINETIC ENERGY" in text
    assert "accuracy_label = order_of_magnitude" in text.replace(
        "ACCURACY_LABEL = order_of_magnitude", "accuracy_label = order_of_magnitude")

    # every data row carries the label at its own point of use
    rows = [ln for ln in text.splitlines()
            if ln and not ln.startswith("#") and not ln.startswith("E_n_keV")]
    assert len(rows) > 100
    assert all(ln.endswith(",order_of_magnitude") for ln in rows)

    # The grid really is not shared_energy_grid(), for EITHER version.  Checked by
    # SPACING rather than by span: Phase 10 (Plan 10-03) extended the shared axis
    # two decades downward, so "below the shared floor" is no longer a valid test
    # of independence -- but the spacing still is.  This table is 100 nodes/decade
    # (ratio 10^(1/100)); the shared grid is ~79.99 bins/decade.
    from qpd_potential import muon_deposit as md
    e_kev = np.array([float(ln.split(",")[0]) for ln in rows])
    ratio = e_kev[1] / e_kev[0]
    assert ratio == pytest.approx(10.0 ** (1.0 / 100.0), rel=1e-9)
    for version in md.GRID_VERSIONS:
        shared = md.shared_energy_grid(version=version)
        assert not np.isclose(ratio, shared[1] / shared[0], rtol=1e-6), (
            f"the sub-eV table shares the {version} grid spacing -- Phase 10 owns "
            "the shared-grid extension and runs in parallel with Phase 9")


@requires_parma
def test_thermal_table_matches_driver():
    """The committed sub-eV table is what the committed driver produces."""
    rows = [ln for ln in open(THERMAL_CSV, encoding="utf-8").read().splitlines()
            if ln and not ln.startswith("#") and not ln.startswith("E_n_keV")]
    e_kev = np.array([float(ln.split(",")[0]) for ln in rows])
    phi_tab = np.array([float(ln.split(",")[1]) for ln in rows])
    phi_drv = pn.differential_flux(e_kev / 1.0e3,
                                   k=pn.K_GORDON_ANCHOR).phi_cm2_s_mev
    assert np.max(np.abs(phi_drv - phi_tab) / phi_tab) < 1e-6


# --------------------------------------------------------------------------- #
# 7. BAND SEMANTICS AND THE ORDER-OF-MAGNITUDE LABEL                           #
# --------------------------------------------------------------------------- #
def test_band_semantics_phi_lo_is_indoor_not_an_error_bar():
    """phi_default = phi_hi is operative; phi_lo is INDOOR and NOT an error bar."""
    _, phi_def, phi_lo, phi_hi = _v11_table()
    # the committed table's own structure: phi_hi IS phi_default (outdoor upper)
    assert np.allclose(phi_hi, phi_def, rtol=1e-12)
    assert np.allclose(phi_lo, phi_def / 5.0, rtol=1e-6)

    text = open(DECLARATION, encoding="utf-8").read()
    low = text.lower()
    assert "indoor" in low
    assert "not an error bar" in low
    assert "factor 5" in low or "factor-5" in low or "fivefold" in low
    # the operative value must be named
    assert "phi_default = phi_hi" in text or "`phi_default` = `phi_hi`" in text

    # No code path in this plan uses phi_lo or a band midpoint as a central value.
    src = open(pn.__file__, encoding="utf-8").read()
    assert "phi_lo" not in src.replace("phi_lo = phi_default/5", "")
    thermal = open(THERMAL_CSV, encoding="utf-8").read()
    data_rows = [ln for ln in thermal.splitlines()
                 if ln and not ln.startswith("#") and not ln.startswith("E_n_keV")]
    assert all(len(ln.split(",")) == 4 for ln in data_rows), (
        "the sub-eV table emits no phi_lo column at all")


def test_order_of_magnitude_label_everywhere():
    """Every emitted neutron quantity carries the label at its point of definition."""
    assert pn.ACCURACY_LABEL == "order_of_magnitude"
    assert pn.NeutronFlux.__dataclass_fields__["accuracy_label"].default == "order_of_magnitude"

    thermal = open(THERMAL_CSV, encoding="utf-8").read()
    assert "ACCURACY_LABEL = order_of_magnitude" in thermal

    text = open(DECLARATION, encoding="utf-8").read()
    assert text.count("order_of_magnitude") >= 5
    assert "no downstream acceptance test" in text.lower()

    # the two carried truncation omissions, QUANTIFIED, for Phase 13
    assert "20 MeV" in text and "ENDF" in text
    flat = re.sub(r"\s+", "", text)
    assert "197MeV" in flat and "21%" in flat


def test_no_shielded_quantity_in_neutron_channel():
    """No NUCLEUS attenuation / overburden / veto credit anywhere in the channel."""
    import sys
    sys.path.insert(0, os.path.join(REPO, "tests"))
    from test_env_v1_identity import (NOT_APPLIED_MARKERS, scan_paths,  # noqa: E402
                                      scan_text)

    from test_env_v1_identity import is_not_applied  # noqa: E402

    hits = [h for h in scan_paths([pn.__file__, THERMAL_CSV])
            if not is_not_applied(h[3])]
    assert hits == [], f"shielded token APPLIED in the neutron channel: {hits}"

    text = open(DECLARATION, encoding="utf-8").read()
    assert NOT_APPLIED_MARKERS  # the marker list is the audited exemption record
    bad = [h for h in scan_text(text, skip_fenced=True) if not is_not_applied(h[2])]
    assert bad == [], f"declaration applies a shielded quantity: {bad}"
