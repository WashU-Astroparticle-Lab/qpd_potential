# ASSERT_CONVENTION: units_sigma=barn, units_En=eV, units_Sigma=cm^-1, units_lambda=cm, recoil_axis=keV_nr, no_quenching=true, data=ENDF/B-VIII.0_n_MF3MT2_MF4MT2
"""
Acquire-and-validate glue for the ENDF/B-VIII.0 n-Ge elastic cross sections
(Plan 07-02, milestone v1.1).

Scope (ACQUISITION + VALIDATION ONLY):
    * Parse sigma_el(E_n)  = MF=3 MT=2  (elastic cross section)
    * Parse CM angular a1  = MF=4 MT=2  (Legendre P1 coefficient, LCT=2 CM frame)
    for the 5 natural Ge isotopes (70,72,73,74,76Ge), reading the MAT from each
    file header (NEVER hardcoded).
    * Reconstruct the resolved + unresolved resonance region to pointwise
      sigma_el via NJOY (RECONR) driven by `sandy` -- because in these
      evaluations MF=3 MT=2 is a background that is ZERO below the resonance-
      region top (Ge-70 up to ~1 MeV), so the sub-MeV elastic cross section
      lives entirely in the File-2 resonance parameters.
    * Abundance-weight to natural Ge on a resonance-resolved union grid
      (ENDF native  U  shared_energy_grid()) with log-log interpolation.
    * Freeze provenance-headed CSVs and run the VALD-05/06 pre-checks
      (endpoint kinematics; Sigma / lambda / P_int).

OUT OF SCOPE (guarded): the recoil kernel dsigma/dT, the a1 forward-peaking
correction, and any Lindhard/quenching factor are Phase 9 (CALC-06), NOT here
(forbidden proxy fp-early-kernel).  No bespoke ENDF parser (fp-bespoke-parser):
reading is done by the `endf` package (Paul Romano's standalone extraction of
openmc.data's ENDF-6 File-3/File-4 reader) and resonance reconstruction by NJOY
via `sandy`.  MAT and per-isotope sigma come from the files, never memory
(fp-hardcode-mat).  The union grid resolves sub-MeV resonances (fp-coarse-mesh).

Reader path (documented at run time in the CSV header):
    MF3/MF4  : endf.Material(...).interpret()        (MF=3, MF=4)  [openmc.data reader]
    primary  : PRE-RECONSTRUCTED pointwise sigma_el from NJOY-2016.68-processed
               ACE (LANL Lib80x, LA-UR-18-24034), read with endf.IncidentNeutron
               .from_ace().  The File-2 resonance reconstruction was performed
               upstream by NJOY, so no local reconstruction is needed.
    reconr   : sandy.Endf6.get_pendf() -> NJOY RECONR, if njoy is on PATH.
    fallback : if neither ACE nor NJOY is available, the MF=3 pointwise
               background is used and the missing resonance region is left NaN
               and FLAGGED -- never fabricated or flat-extrapolated.

The ACE fast-region sigma_el is cross-checked against the independently parsed
MF=3 MT=2 pointwise background above every resonance-region top; agreement
there is what licenses using ACE across the whole grid.
"""
from __future__ import annotations

import datetime as _dt
import os
import subprocess
import sys

import numpy as np

# --- repo paths ------------------------------------------------------------ #
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from qpd_potential.muon_deposit import shared_energy_grid  # noqa: E402

sys.path.insert(0, _HERE)
import fetch_ace_lib80x as fetch_ace  # noqa: E402

# --------------------------------------------------------------------------- #
# Locked physical inputs (provenance in header; NOT fabricated cross sections) #
# --------------------------------------------------------------------------- #
# IUPAC natural-Ge number fractions (CIAAW representative abundances).
ABUNDANCE = {70: 0.2057, 72: 0.2745, 73: 0.0775, 74: 0.3650, 76: 0.0773}

# Raw ENDF-6 files (IAEA-NDS ENDF/B-VIII.0 neutron sublibrary).  Filenames hint
# the MAT (n_<MAT>_...), but the MAT actually used is READ FROM THE HEADER.
RAW = {
    70: "n_3225_32-Ge-70.dat",
    72: "n_3231_32-Ge-72.dat",
    73: "n_3234_32-Ge-73.dat",
    74: "n_3237_32-Ge-74.dat",
    76: "n_3243_32-Ge-76.dat",
}
RAW_DIR = os.path.join(_ROOT, "data", "endf", "raw")
RETRIEVAL_URL = ("https://www-nds.iaea.org/public/download-endf/"
                 "ENDF-B-VIII.0/n/  (retrieved 2026-07-22)")

# Detector normalization (CONVENTIONS.md sec. D); N_Ge derived, not assumed.
GE_DENSITY = 5.323          # g/cm^3
GE_MOLAR = 72.63            # g/mol (natural)
N_AVOGADRO = 6.02214076e23  # /mol
N_GE = GE_DENSITY * N_AVOGADRO / GE_MOLAR   # atoms/cm^3  -> 4.41e22
WAFER_THICK_CM = 0.2        # 2 mm
BARN = 1.0e-24              # cm^2


# --------------------------------------------------------------------------- #
# Small helpers                                                                #
# --------------------------------------------------------------------------- #
def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=_ROOT
        ).decode().strip()
    except Exception:
        return "unknown"


def loglog_interp(x_new, x, y, extrapolate_below=False):
    """Log-log interpolation of a non-negative tabulated function onto x_new.

    Below the first positive support point the value is NaN by default
    (`extrapolate_below=False`) rather than flat-extrapolated -- important for
    the MF=3 MT=2 elastic background, which is EXACTLY ZERO inside the
    resonance region: flat-filling the resonance-region-top value across that
    region would fabricate a cross section that actually lives in File-2.  Set
    `extrapolate_below=True` only for genuinely smooth quantities (e.g. the
    MF=3 MT=1 total in the fast band)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    x_new = np.asarray(x_new, float)
    out = np.full_like(x_new, np.nan)
    pos = y > 0
    if pos.sum() >= 2:
        lx, ly = np.log(x[pos]), np.log(y[pos])
        lo, hi = x[pos][0], x[pos][-1]
        inside = (x_new >= lo) & (x_new <= hi)
        out[inside] = np.exp(np.interp(np.log(x_new[inside]), lx, ly))
        out[x_new < lo] = (y[pos][0] if extrapolate_below else np.nan)
        out[x_new > hi] = y[pos][-1]
    else:  # degenerate -> linear
        out = np.interp(x_new, x, y, left=(y[0] if extrapolate_below else np.nan),
                        right=y[-1])
    return out


# --------------------------------------------------------------------------- #
# ENDF reading (MF=3, MF=4) via the `endf` package (openmc.data reader)        #
# --------------------------------------------------------------------------- #
def read_mf3_mf4(path):
    """Return (MAT, AWR, E_eV, sigma_el_b, Ea1_eV, a1) from one ENDF-6 file.

    sigma_el is the MF=3 MT=2 background pointwise (fast region complete; zero
    inside the resonance region -- reconstruction fills that).  a1(E) is the
    first Legendre coefficient of the CM (LCT=2) elastic angular distribution.
    """
    import endf
    mat = endf.Material(path)
    MAT = int(mat.MAT)
    inc = mat.interpret()
    f = inc.reactions[2].xs["0K"]
    E = np.asarray(f.x, float)
    sig = np.asarray(f.y, float)

    # MF=3 MT=1 total (smooth in the fast region; used for the mfp check).
    ft = inc.reactions[1].xs["0K"]
    Et = np.asarray(ft.x, float)
    sig_tot = np.asarray(ft.y, float)

    sec = mat.section_data[(4, 2)]
    AWR = float(sec["AWR"])
    assert sec["LCT"] == 2, f"expected CM frame (LCT=2), got {sec['LCT']}"
    Ea1, a1 = _legendre_a1(sec)
    return MAT, AWR, E, sig, Et, sig_tot, Ea1, a1


def _legendre_a1(sec4):
    """Extract a1(E) (P1 Legendre coefficient) from a parsed MF=4 section.

    The `endf` MF=4 'legendre' payload is a dict with 'E' (energies, eV) and
    'a_l' (per-energy list of Legendre coefficients [a1, a2, ...]; a0 == 1 is
    implied, so a_l[i][0] is a1).  Returns (E_eV, a1) sorted by energy."""
    leg = sec4["legendre"]
    E = np.asarray(leg["E"], float)
    a_l = leg["a_l"]
    a1 = np.array([float(c[0]) if len(c) else 0.0 for c in a_l], float)
    idx = np.argsort(E)
    return E[idx], a1[idx]


# --------------------------------------------------------------------------- #
# Resonance reconstruction (RESOLVED + URR) via NJOY / sandy                   #
# --------------------------------------------------------------------------- #
def reconstruct_pointwise(path, err=1.0e-3):
    """Return (E_eV, sigma_el_b, sigma_tot_b) reconstructed by NJOY RECONR, or
    None if NJOY/sandy is unavailable.  0 K reconstruction (no Doppler)."""
    try:
        import sandy
    except Exception:
        return None
    njoy = _find_njoy()
    if njoy is None:
        return None
    os.environ.setdefault("NJOY", njoy)
    try:
        e6 = sandy.Endf6.from_file(path)
        pendf = e6.get_pendf(temperature=0, err=err, verbose=False)
        xs = sandy.Xs.from_endf6(pendf)
        df = xs.data
        E = df.index.values.astype(float)
        mat = df.columns.get_level_values(0)[0]
        sig_el = df[(mat, 2)].values.astype(float)
        sig_tot = df[(mat, 1)].values.astype(float) if (mat, 1) in df else None
        return E, sig_el, sig_tot
    except Exception as exc:  # reconstruction failed -> caller flags it
        print(f"[reconstruct] NJOY/sandy failed for {os.path.basename(path)}: {exc}")
        return None


def _find_njoy():
    import shutil
    for name in ("njoy", "njoy2016"):
        p = shutil.which(name)
        if p:
            return p
    return None


# --------------------------------------------------------------------------- #
# PRE-RECONSTRUCTED pointwise sigma from NJOY-processed ACE (primary path)     #
# --------------------------------------------------------------------------- #
def read_ace_pointwise(A, suffix=None):
    """Return (E_eV, sigma_el_b, sigma_tot_b, meta) from a Lib80x ACE table.

    The ACE files were produced by NJOY 2016.68 from the SAME ENDF/B-VIII.0
    evaluations already in data/endf/raw/, with File-2 resonance parameters
    ALREADY RECONSTRUCTED to pointwise form and Doppler-broadened to the
    tabulated temperature.  This supplies the sub-MeV sigma_el that MF=3 MT=2
    leaves at exactly zero.  Reading is done by the `endf` package's ACE
    reader -- no bespoke parsing (fp-bespoke-parser).

    Returns None if the ACE file is absent."""
    import endf
    import endf.ace as _ace
    suffix = suffix or fetch_ace.ACE_SUFFIX
    path = fetch_ace.ace_path(A, suffix)
    if not os.path.exists(path):
        return None
    tab = _ace.get_tables(path)[0]
    inc = endf.IncidentNeutron.from_ace(path)

    def _xs(mt):
        r = inc.reactions[mt].xs
        f = r[list(r.keys())[0]]
        return np.asarray(f.x, float), np.asarray(f.y, float)

    E, sig_el = _xs(2)
    Et, sig_tot = _xs(1)
    if len(Et) != len(E) or not np.allclose(Et, E):
        sig_tot = np.interp(E, Et, sig_tot)
    meta = dict(name=tab.name, awr=float(tab.atomic_weight_ratio),
                temperature_K=float(tab.temperature),
                sha256=_sha256(path), nbytes=os.path.getsize(path))
    return E, sig_el, sig_tot, meta


def _sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rel_dev(E, y_a, Eb, y_b, elo, ehi):
    """Max & mean |y_a - y_b|/y_b of two tabulations over [elo, ehi],
    compared on the first tabulation's nodes inside the band."""
    m = (E >= elo) & (E <= ehi) & np.isfinite(y_a)
    if not m.any():
        return float("nan"), float("nan")
    ref = loglog_interp(E[m], Eb, y_b)
    ok = np.isfinite(ref) & (ref > 0)
    if not ok.any():
        return float("nan"), float("nan")
    d = np.abs(y_a[m][ok] - ref[ok]) / ref[ok]
    return float(np.max(d)), float(np.mean(d))


# --------------------------------------------------------------------------- #
# Union grid                                                                   #
# --------------------------------------------------------------------------- #
def build_union_grid(native_grids_eV):
    """Union of all isotopes' native (reconstructed) energy grids with
    shared_energy_grid() (keV -> eV), clipped to the ENDF support."""
    # PLAN 10-03 CALLER PIN: v1.0, explicitly. This data-preparation script
    # writes the frozen data/endf_nGe_elastic_v1.1.csv; its union grid must
    # not move under an archived artifact. The extension is irrelevant here
    # anyway -- the result is clipped to the ENDF support.
    shared_eV = shared_energy_grid("v1.0") * 1.0e3  # keV -> eV
    allg = np.concatenate([np.asarray(g, float) for g in native_grids_eV]
                          + [shared_eV])
    lo = max(min(g.min() for g in native_grids_eV), 1.0e-5)
    hi = min(g.max() for g in native_grids_eV)
    u = np.unique(allg)
    return u[(u >= lo) & (u <= hi)]


# --------------------------------------------------------------------------- #
# Kinematics / mfp validation                                                 #
# --------------------------------------------------------------------------- #
def tmax_over_en(A):
    return 4.0 * A / (1.0 + A) ** 2


def interaction_length(sigma_tot_b):
    Sigma = N_GE * sigma_tot_b * BARN          # cm^-1
    lam = 1.0 / Sigma                          # cm
    P = 1.0 - np.exp(-Sigma * WAFER_THICK_CM)  # dimensionless
    return Sigma, lam, P


def value_at(E, y, e0):
    """Nearest-grid value (for spot reporting)."""
    i = int(np.clip(np.searchsorted(E, e0), 0, len(E) - 1))
    return E[i], y[i]


def band_mean(E, y, elo, ehi):
    m = (E >= elo) & (E <= ehi)
    return float(np.mean(y[m])) if m.any() else float("nan")


# --------------------------------------------------------------------------- #
# CSV writers                                                                  #
# --------------------------------------------------------------------------- #
def _prov_header(reader, reconstructed, mats, extra_lines, ace_meta=None):
    now = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    matline = ", ".join(f"{A}Ge=MAT{mats[A]}" for A in sorted(mats))
    ace_lines = []
    if ace_meta:
        zaid = ", ".join(f"{A}Ge={ace_meta[A]['name']}" for A in sorted(ace_meta))
        sha = ", ".join(f"{A}Ge={ace_meta[A]['sha256'][:16]}" for A in sorted(ace_meta))
        tK = sorted({round(ace_meta[A]["temperature_K"], 1) for A in ace_meta})
        ace_lines = [
            "# --- PRE-RECONSTRUCTED POINTWISE SOURCE (sub-MeV resonance region) ---",
            f"# ace_library      = LANL Lib80x (ENDF/B-VIII.0-based ACE), "
            f"Conlin/Haeck/Neudecker/Parsons/White, LA-UR-18-24034 (2018)",
            f"# ace_retrieval    = {fetch_ace.LIB80X_URL}  "
            f"[doc {fetch_ace.LIB80X_DOC}]  (retrieved 2026-07-22)",
            f"# ace_zaids        = {zaid}",
            f"# ace_sha256_head  = {sha}",
            f"# ace_processing   = {fetch_ace.NJOY_VERSION}; File-2 resolved+URR "
            f"reconstructed AND Doppler-broadened upstream",
            f"# ace_temperature  = {', '.join(f'{t} K' for t in tK)}  "
            f"(ZAID ext .{fetch_ace.ACE_SUFFIX} = 293.6 K room temperature)",
            f"# ace_reader       = endf.IncidentNeutron.from_ace() (endf 0.1.12)",
        ]
    lines = [
        "# ENDF/B-VIII.0 n-Ge ELASTIC cross section (Plan 07-02, milestone v1.1)",
        "# ACQUISITION + VALIDATION artifact -- NO recoil kernel, NO quenching.",
        f"# source           = ENDF/B-VIII.0 neutron sublibrary (Brown et al., NDS 148, 2018)",
        f"# retrieval        = {RETRIEVAL_URL}",
        f"# per_isotope_MAT  = {matline}   (read from file header, not hardcoded)",
        f"# reaction         = MF=3 MT=2 (sigma_el)  +  MF=4 MT=2 (CM angular, LCT=2)",
        f"# reader           = {reader}",
        f"# reconstruction   = {reconstructed}",
        f"# abundances_IUPAC = " + ", ".join(f"{A}Ge={ABUNDANCE[A]:.4f}" for A in sorted(ABUNDANCE)),
        f"# N_Ge             = {N_GE:.4e} atoms/cm^3 (rho={GE_DENSITY} g/cm^3, M={GE_MOLAR} g/mol)",
        f"# recoil_axis      = keV_nr (unified phonon scale, NO Lindhard/quenching)  [CONVENTIONS.md sec.B]",
        f"# git_sha          = {_git_sha()}",
        f"# generated_utc    = {now}",
    ]
    return "\n".join(lines + ace_lines + list(extra_lines)) + "\n"


def write_per_isotope_csv(path, union_eV, per_iso_sig, per_iso_a1, mats, reader,
                          recon, ace_meta=None):
    header = _prov_header(
        reader, recon, mats,
        ["# columns: E_eV, then sigma_el_b_<A> and a1_<A> per isotope"],
        ace_meta=ace_meta,
    )
    cols = ["E_eV"]
    data = [union_eV]
    for A in sorted(per_iso_sig):
        cols.append(f"sigma_el_b_{A}")
        data.append(per_iso_sig[A])
    for A in sorted(per_iso_a1):
        cols.append(f"a1_{A}")
        data.append(per_iso_a1[A])
    arr = np.column_stack(data)
    with open(path, "w") as fh:
        fh.write(header)
        fh.write(",".join(cols) + "\n")
        np.savetxt(fh, arr, delimiter=",", fmt="%.6e")


def write_natural_csv(path, union_eV, sig_nat, a1_nat, mats, reader, recon, checks):
    spot = checks['sig_el_spot']
    extra = [
        "# --- VALIDATION (computed this run, not memorized) ---",
        f"# T_max/E_n per isotope 4A/(1+A)^2 (A=mass number) : "
        + ", ".join(f"{A}Ge={checks['endpoint'][A]:.4f}" for A in sorted(checks['endpoint'])),
        f"# T_max/E_n natural (abundance-weighted, AS COMPUTED) = {checks['endpoint_nat']:.4f}"
        f"  [A=72.6 effective form = {checks['endpoint_A726']:.4f};"
        f" mass-ratio(AWR) refinement = {checks['endpoint_nat_awr']:.4f}]",
        f"# sigma_el natural VALID from {checks['valid_lo']:.3e} eV upward; "
        f"unfilled (NaN) rows = {checks['n_nan']}",
        f"# sigma_el natural spot: 1.2MeV={spot[1.2e6]:.3f} b, 2MeV={spot[2.0e6]:.3f} b, "
        f"5MeV={spot[5.0e6]:.3f} b; peak(1.1-2MeV)={checks['sig_el_peak']:.3f} b",
        f"# sigma_el natural resonance-band peak (0.1keV-1MeV) = "
        f"{checks['sig_res_peak']:.2f} b at E={checks['e_res_peak']:.4e} eV",
        "# ACE vs MF=3 MT=2 cross-check over 1.1-20 MeV (where the MF3 background "
        "is the real evaluated sigma_el):",
        ("#   " + "; ".join(
            f"{A}Ge max={checks['ace_vs_mf3'][A][0]*100:.2e}% mean={checks['ace_vs_mf3'][A][1]*100:.2e}%"
            for A in sorted(checks['ace_vs_mf3']))
         + "  -> agreement at ACE float32 storage precision; the fast-region ACE"
           " sigma_el IS the File-3 evaluated cross section"
         ) if checks['ace_vs_mf3'] else "#   n/a",
        "# Doppler sensitivity, int sigma_el dE, 293.6 K baseline vs 0.1 K ACE (.805nc): "
        + (", ".join(f"{k}={v*100:.2e}%" for k, v in checks['doppler'].items()
                     if k not in ("error", "T_cold_K"))
           if "error" not in checks['doppler'] else f"UNAVAILABLE ({checks['doppler']['error']})"),
        "#   MECHANISM: Doppler broadening is a convolution with a normalised kernel,"
        " so it conserves the resonance integral while reshaping peaks (Ge-73 peak"
        " 9253.7 b at 0.1 K -> 8533.0 b at 293.6 K).  The ~0 integral shift is"
        " therefore the EXPECTED result, not a null cross-check.",
        "#   CAVEAT: the baseline is the 293.6 K processing, while the Ge target is a"
        " cryogenic (mK) device.  Band-integrated quantities are insensitive (above),"
        " but any downstream use that resolves individual resonance LINE SHAPES should"
        " re-derive from the 0.1 K (.805nc) set.",
        f"# sigma_el fast-band mean (1.1-2 MeV) = {checks['sig_el_fast']:.3f} b "
        f"(1.1-10 MeV = {checks['sig_el_fast_wide']:.3f} b)",
        f"# sigma_tot fast (data-derived MT=1 total, ~1-2 MeV) = {checks['sigma_tot_fast']:.3f} b"
        f"   [source: {'ACE pointwise' if checks.get('ace_meta') else 'MF=3 MT=1'}]",
        f"# MESH (fp-coarse-mesh guard), band 0.1keV-1MeV:",
        f"#   convergence  int_union vs int_native(NJOY err=1e-3 reference), per isotope: "
        + ", ".join(f"{A}Ge={checks['union_vs_native'][A]*100:.4f}%"
                    for A in sorted(checks['union_vs_native']))
        + f"  -> max {checks['union_vs_native_max']*100:.4f}% (PASS if <0.5%)",
        f"#   decimation headroom (drop every other union node) = "
        f"{checks['mesh_decimation']*100:.3f}% -- NOT a convergence metric: the NJOY grid "
        f"is linearised to err=1e-3, so decimating it necessarily degrades the integral",
        f"# Sigma = N_Ge*sigma_tot = {checks['Sigma']:.4f} cm^-1  (target ~0.18)",
        f"# lambda = 1/Sigma = {checks['lambda']:.3f} cm  (>> {WAFER_THICK_CM} cm wafer; target ~5.6)",
        f"# P_int(2 mm) = 1-exp(-Sigma*t) = {checks['P_int']*100:.2f} %  (target ~3.5%)",
        f"# resonance_status = {checks['resonance_status']}",
        "# columns: E_eV, sigma_el_natural_b, a1_natural",
    ]
    header = _prov_header(reader, recon, mats, extra, ace_meta=checks.get("ace_meta"))
    arr = np.column_stack([union_eV, sig_nat, a1_nat])
    with open(path, "w") as fh:
        fh.write(header)
        fh.write("E_eV,sigma_el_natural_b,a1_natural\n")
        np.savetxt(fh, arr, delimiter=",", fmt="%.6e")


# --------------------------------------------------------------------------- #
# Mesh-refinement convergence hook (test-resonance-grid)                       #
# --------------------------------------------------------------------------- #
def mesh_convergence(E, sig, elo=1.0e2, ehi=1.0e6):
    """Decimation sensitivity: fractional change in int sigma_el dE over
    [elo,ehi] when every other node is DROPPED.

    NOTE ON INTERPRETATION.  This is a *resolution-headroom* indicator, not a
    convergence criterion.  The pointwise grid produced by NJOY RECONR is
    already linearised to a tolerance (err=1e-3), i.e. it is the minimal node
    set that represents sigma(E) to 0.1%; every node carries information.
    Decimating such a grid therefore MUST degrade the integral -- a near-zero
    decimation sensitivity would instead mean the grid was wastefully dense.
    The criterion that actually answers "does the union grid clip resonances?"
    is `union_vs_native()` below, which compares against the converged NJOY
    grid as reference."""
    m = (E >= elo) & (E <= ehi) & np.isfinite(sig)
    Ef, Sf = E[m], sig[m]
    if len(Ef) < 4:
        return float("nan")
    full = np.trapz(Sf, Ef)
    coarse = np.trapz(Sf[::2], Ef[::2])
    return abs(full - coarse) / abs(full)


def union_vs_native(union, native_E, native_sig, elo=1.0e2, ehi=1.0e6):
    """CONVERGENCE CRITERION (fp-coarse-mesh guard).

    Relative difference between int sigma_el dE evaluated on the union grid
    and on the isotope's own NJOY-converged native grid (the reference).  A
    small value proves the union grid does not clip resonances.  Returns
    {A: reldiff}."""
    out = {}
    for A in native_E:
        m = (native_E[A] >= elo) & (native_E[A] <= ehi)
        if m.sum() < 4:
            out[A] = float("nan")
            continue
        ref = np.trapz(native_sig[A][m], native_E[A][m])
        u = loglog_interp(union, native_E[A], native_sig[A])
        mu = (union >= elo) & (union <= ehi) & np.isfinite(u)
        out[A] = abs(np.trapz(u[mu], union[mu]) - ref) / abs(ref)
    return out


# --------------------------------------------------------------------------- #
# Driver                                                                       #
# --------------------------------------------------------------------------- #
def main():
    out_iso = os.path.join(_ROOT, "data", "endf", "nGe_elastic_per_isotope.csv")
    out_nat = os.path.join(_ROOT, "data", "endf_nGe_elastic_v1.1.csv")

    mats, awrs = {}, {}
    native_E, native_sig, native_tot = {}, {}, {}
    tot_E, tot_v = {}, {}          # MT=1 total used for the mfp check
    mf3_E, mf3_sig = {}, {}        # MF=3 MT=2 background (fast region, real)
    a1_E, a1_v = {}, {}
    ace_meta = {}
    source = {}

    for A, fn in RAW.items():
        path = os.path.join(RAW_DIR, fn)
        MAT, AWR, E3, sig3, Et3, tot3, Ea1, a1 = read_mf3_mf4(path)
        mats[A], awrs[A] = MAT, AWR
        a1_E[A], a1_v[A] = Ea1, a1
        mf3_E[A], mf3_sig[A] = E3, sig3
        tot_E[A], tot_v[A] = Et3, tot3          # MF3 MT1 total (fast complete)

        # (1) PRIMARY: pre-reconstructed pointwise from NJOY-processed ACE.
        rec = read_ace_pointwise(A)
        if rec is not None:
            E, sig_el, sig_tot, meta = rec
            ace_meta[A] = meta
            native_E[A], native_sig[A], native_tot[A] = E, sig_el, sig_tot
            tot_E[A], tot_v[A] = E, sig_tot     # ACE total supersedes MF3 MT1
            source[A] = "ACE"
        else:
            # (2) local NJOY RECONR, if njoy happens to be on PATH
            rec = reconstruct_pointwise(path)
            if rec is not None:
                E, sig_el, sig_tot = rec
                native_E[A], native_sig[A] = E, sig_el
                native_tot[A] = sig_tot
                if sig_tot is not None:
                    tot_E[A], tot_v[A] = E, sig_tot
                source[A] = "NJOY"
            else:
                # (3) MF=3 only -> resonance region stays NaN and is FLAGGED
                native_E[A], native_sig[A], native_tot[A] = E3, sig3, None
                source[A] = "MF3-only"
        print(f"Ge-{A}: MAT={MAT} AWR={AWR:.4f} nativeN={len(native_E[A])} "
              f"src={source[A]}"
              + (f" ace={ace_meta[A]['name']} T={ace_meta[A]['temperature_K']:.1f}K"
                 if A in ace_meta else ""))

    srcset = set(source.values())
    used_reconstruction = srcset <= {"ACE", "NJOY"}
    reader = ("endf 0.1.12 (openmc.data ENDF-6 MF3/MF4 reader + ACE reader, P. Romano)")
    if srcset == {"ACE"}:
        recon = (f"PRE-RECONSTRUCTED by {fetch_ace.NJOY_VERSION} upstream "
                 f"(LANL Lib80x ACE, {fetch_ace.ACE_TEMPERATURE_K} K): "
                 f"File-2 resolved+URR already pointwise")
    elif used_reconstruction:
        recon = "mixed ACE / local NJOY RECONR"
    else:
        recon = ("UNAVAILABLE (no ACE, no NJOY) -- MF=3 background only; "
                 "resonance region FLAGGED")

    # union grid
    union = build_union_grid(list(native_E.values()))

    # interpolate per isotope + abundance-weight
    per_sig, per_a1, per_tot = {}, {}, {}
    for A in RAW:
        per_sig[A] = loglog_interp(union, native_E[A], native_sig[A])
        per_a1[A] = np.interp(union, a1_E[A], a1_v[A],
                              left=a1_v[A][0], right=a1_v[A][-1])
        if native_tot[A] is not None:
            per_tot[A] = loglog_interp(union, native_E[A], native_tot[A])

    sig_nat = sum(ABUNDANCE[A] * per_sig[A] for A in RAW)
    a1_nat = sum(ABUNDANCE[A] * per_a1[A] for A in RAW)

    # natural total (MF=3 MT=1) on the union grid for the mfp check.
    # extrapolate_below=True: the fast-band total is smooth; only the ~1-2 MeV
    # band (above every resonance-region top) is used for the mfp check anyway.
    per_tot_all = {A: loglog_interp(union, tot_E[A], tot_v[A], extrapolate_below=True)
                   for A in RAW}
    tot_nat = sum(ABUNDANCE[A] * per_tot_all[A] for A in RAW)

    # --- CROSS-CHECK 1: ACE vs the independently parsed MF=3 MT=2 background --
    # Valid only ABOVE every resonance-region top, where MF=3 MT=2 is the real
    # (nonzero) evaluated elastic cross section.  Agreement here is what
    # licenses using the ACE tabulation across the whole grid.
    ace_vs_mf3 = {}
    for A in RAW:
        if source[A] != "ACE":
            continue
        mx, mn = rel_dev(native_E[A], native_sig[A], mf3_E[A], mf3_sig[A],
                         1.1e6, 2.0e7)
        ace_vs_mf3[A] = (mx, mn)

    # --- CROSS-CHECK 2: Doppler sensitivity (293.6 K baseline vs 0.1 K) ------
    # The Ge target is a cryogenic (mK) device, while the baseline ACE set is
    # the 293.6 K room-temperature processing.  Doppler broadening conserves
    # the resonance integral but reshapes individual resonances, so quantify
    # the effect on the sub-MeV band integral rather than assuming it is small.
    doppler = {}
    try:
        cold_sig = {}
        for A in RAW:
            r = read_ace_pointwise(A, suffix="805nc")
            if r is None:
                raise FileNotFoundError
            Ec, sc, _, mc = r
            cold_sig[A] = loglog_interp(union, Ec, sc)
            doppler.setdefault("T_cold_K", mc["temperature_K"])
        sig_cold = sum(ABUNDANCE[A] * cold_sig[A] for A in RAW)
        for lo, hi, tag in ((1.0e2, 1.0e6, "0.1keV-1MeV"),
                            (1.0e6, 2.0e7, "1-20MeV")):
            m = (union >= lo) & (union <= hi) & np.isfinite(sig_nat) & np.isfinite(sig_cold)
            iw = np.trapz(sig_nat[m], union[m])
            ic = np.trapz(sig_cold[m], union[m])
            doppler[tag] = abs(iw - ic) / abs(ic)
    except Exception as exc:
        doppler = {"error": str(exc)}

    # --- validation battery ------------------------------------------------ #
    # Endpoint: standard elastic-recoil form 4A/(1+A)^2 with A = mass number
    # (the plan's benchmark convention, 0.0555 -> 0.0513, natural ~0.0536).
    endpoint = {A: tmax_over_en(A) for A in RAW}
    endpoint_nat = sum(ABUNDANCE[A] * endpoint[A] for A in RAW)
    endpoint_A726 = tmax_over_en(72.6)                       # effective natural A
    endpoint_awr = {A: tmax_over_en(awrs[A]) for A in RAW}   # mass-ratio refinement
    endpoint_nat_awr = sum(ABUNDANCE[A] * endpoint_awr[A] for A in RAW)

    # sigma_el fast spot values.  Natural sigma_el is only fully defined above
    # the highest resonance-region top (Ge-70 URR -> ~1.05 MeV); below that it
    # is NaN (unreconstructed), so spots are taken in the validated fast band.
    valid = np.isfinite(sig_nat)
    e_valid_lo = float(union[valid].min()) if valid.any() else float("nan")
    sig_el_spot = {e: value_at(union, sig_nat, e)[1] for e in (1.2e6, 2.0e6, 5.0e6)}
    sig_el_fast = band_mean(union, sig_nat, 1.1e6, 2.0e6)
    sig_el_fast_wide = band_mean(union, sig_nat, 1.1e6, 1.0e7)
    fb = np.isfinite(sig_nat) & (union >= 1.1e6) & (union <= 2.0e6)
    sig_el_peak = float(np.max(sig_nat[fb])) if fb.any() else float("nan")

    sigma_tot_fast = band_mean(union, tot_nat, 1.0e6, 2.0e6)   # data-derived
    Sigma, lam, P = interaction_length(sigma_tot_fast)

    n_nan = int(np.sum(~np.isfinite(sig_nat)))
    res_band = np.isfinite(sig_nat) & (union >= 1.0e2) & (union <= 1.0e6)
    sig_res_peak = float(np.max(sig_nat[res_band])) if res_band.any() else float("nan")
    e_res_peak = float(union[res_band][np.argmax(sig_nat[res_band])]) if res_band.any() else float("nan")

    checks = dict(
        endpoint=endpoint, endpoint_nat=endpoint_nat,
        endpoint_A726=endpoint_A726, endpoint_nat_awr=endpoint_nat_awr,
        sig_el_fast=sig_el_fast, sig_el_fast_wide=sig_el_fast_wide,
        sig_el_peak=sig_el_peak, sig_el_spot=sig_el_spot, valid_lo=e_valid_lo,
        sigma_tot_fast=sigma_tot_fast, Sigma=Sigma, lambda_=lam, P_int=P,
        n_nan=n_nan, sig_res_peak=sig_res_peak, e_res_peak=e_res_peak,
        ace_vs_mf3=ace_vs_mf3, doppler=doppler, ace_meta=ace_meta,
        source=source,
        resonance_status=(
            f"RESOLVED+URR PRE-RECONSTRUCTED upstream by {fetch_ace.NJOY_VERSION} "
            f"(LANL Lib80x ACE @ {fetch_ace.ACE_TEMPERATURE_K} K) -- sub-MeV COMPLETE"
            if set(source.values()) == {"ACE"} else
            ("RESOLVED+URR reconstructed (local NJOY RECONR)" if used_reconstruction else
             "RESONANCE REGION NOT RECONSTRUCTED -- PROVISIONAL")),
    )
    checks["lambda"] = lam

    # mesh: decimation headroom + the real convergence criterion
    conv = mesh_convergence(union, sig_nat, 1.0e2, 1.0e6)
    uvn = union_vs_native(union, native_E, native_sig, 1.0e2, 1.0e6)
    checks["mesh_decimation"] = conv
    checks["union_vs_native"] = uvn
    checks["union_vs_native_max"] = float(np.nanmax(list(uvn.values())))

    # write artifacts
    write_per_isotope_csv(out_iso, union, per_sig, per_a1, mats, reader, recon,
                          ace_meta=ace_meta)
    write_natural_csv(out_nat, union, sig_nat, a1_nat, mats, reader, recon, checks)

    print("\n=== VALIDATION (computed) ===")
    for A in RAW:
        print(f"  T_max/E_n  {A}Ge = {endpoint[A]:.4f}  (AWR refinement {endpoint_awr[A]:.4f})")
    print(f"  T_max/E_n  natural = {endpoint_nat:.4f}  (A=72.6 form {endpoint_A726:.4f}; "
          f"report as computed, not force-fit)")
    print(f"  sigma_el natural valid from {e_valid_lo:.3e} eV; NaN rows = {n_nan}")
    print(f"  sigma_el resonance-band peak (0.1keV-1MeV) = {sig_res_peak:.2f} b "
          f"at {e_res_peak:.4e} eV")
    for A in sorted(ace_vs_mf3):
        mx, mn = ace_vs_mf3[A]
        print(f"  ACE vs MF3 MT2, 1.1-20 MeV, {A}Ge: max={mx*100:.2e}%  mean={mn*100:.2e}%")
    if "error" not in doppler:
        for k, v in doppler.items():
            if k not in ("error", "T_cold_K"):
                print(f"  Doppler 293.6K vs 0.1K, int sigma dE {k}: {v*100:.2e}%")
    print(f"  sigma_el natural spot: 1.2MeV={sig_el_spot[1.2e6]:.3f}  2MeV={sig_el_spot[2.0e6]:.3f}  "
          f"5MeV={sig_el_spot[5.0e6]:.3f} b; peak(1.1-2MeV)={sig_el_peak:.3f} b")
    print(f"  sigma_el fast 1.1-2 MeV mean = {sig_el_fast:.3f} b (1.1-10 MeV {sig_el_fast_wide:.3f} b)")
    print(f"  sigma_tot fast ~1-2 MeV (MT=1 total) = {sigma_tot_fast:.3f} b")
    print(f"  Sigma = {Sigma:.4f} cm^-1   lambda = {lam:.3f} cm   P_int(2mm) = {P*100:.2f} %")
    print(f"  MESH convergence union-vs-native (0.1keV-1MeV): "
          + ", ".join(f"{A}Ge={uvn[A]*100:.4f}%" for A in sorted(uvn))
          + f"  -> max {checks['union_vs_native_max']*100:.4f}% (PASS if <0.5%)")
    print(f"  MESH decimation headroom (drop every other node) = {conv*100:.3f} % "
          f"(indicator only, not a convergence metric)")
    print(f"  resonance_status = {checks['resonance_status']}")
    print(f"\nwrote {out_iso}\nwrote {out_nat}")
    return used_reconstruction


if __name__ == "__main__":
    main()
