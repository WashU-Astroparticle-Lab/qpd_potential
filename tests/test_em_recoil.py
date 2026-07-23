# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Plan 15-01: the electron-recoil applicability verdict and the validity floors.

Executable counterpart of ``src/qpd_potential/em_recoil.py`` and
``artifacts/v2.0/em_validity_floors.csv``.
"""
import csv
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from qpd_potential import compton_source as cs
from qpd_potential import em_recoil as er
from qpd_potential import muon_deposit as md
from qpd_potential import params

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FLOORS = os.path.join(_ROOT, "artifacts", "v2.0", "em_validity_floors.csv")
_REPORT = os.path.join(
    _ROOT, "GPD", "phases",
    "15-v1-0-muon-and-gamma-channels-on-the-extended-grid-p-em",
    "15-01-BROADENING-APPLICABILITY.md")


def _floor_rows():
    with open(_FLOORS, newline="") as fh:
        return list(csv.DictReader(r for r in fh if not r.startswith("#")))


def _floor_header():
    out = []
    with open(_FLOORS, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                break
            out.append(line)
    return "".join(out)


# --------------------------------------------------------------------------- #
# claim-broadening-verdict                                                      #
# --------------------------------------------------------------------------- #
def test_verdict_declared():
    """test-verdict-declared. Both channels carry a vocabulary verdict with a
    non-empty reason and a non-empty consequence."""
    assert set(er.ELECTRON_RECOIL_CHANNELS) == {"muon", "compton"}
    for ch in er.ELECTRON_RECOIL_CHANNELS:
        v = er.ia_verdict(ch)
        assert v.verdict in er.IA_VERDICT_VOCABULARY
        assert v.channel == ch
        for field in ("recoiling_body", "initial_state_momentum_distribution",
                      "reason", "consequence_for_spectra", "falsifier"):
            assert len(str(getattr(v, field)).strip()) > 40, f"{ch}: thin {field}"
    # The absence of a verdict is NOT a default to does_not_apply.
    with pytest.raises(KeyError):
        er.ia_verdict("neutron")


def test_verdict_vocabulary_is_closed():
    with pytest.raises(ValueError):
        er.IAVerdict("muon", "probably_not", "a", "b", "c", "d", "e")
    with pytest.raises(ValueError):
        er.IAVerdict("muon", "does_not_apply", "a", "b", "", "d", "e")


def test_guard_raises():
    """test-guard-raises. A request contradicting the recorded verdict raises a
    NAMED catchable exception carrying the verdict and its reason; a consistent
    request returns."""
    for ch in er.ELECTRON_RECOIL_CHANNELS:
        v = er.ia_verdict(ch)
        assert v.verdict == "does_not_apply"          # what this plan determined
        with pytest.raises(er.ElectronRecoilBroadeningError) as exc:
            er.assert_nuclear_kernel_use(ch, True)
        msg = str(exc.value)
        assert "does_not_apply" in msg
        assert "REASON:" in msg and "CONSEQUENCE FOR SPECTRA:" in msg
        assert "fp-transplant-nuclear-width" in msg
        # the consistent call RETURNS, and returns the verdict
        assert er.assert_nuclear_kernel_use(ch, False) is v


def test_guard_is_not_a_warning_or_a_flag():
    """The codebase precedent is fold.DoubleBroadeningError, which raises. A
    guard that warns, clamps, or returns a flag would FAIL the plan."""
    assert issubclass(er.ElectronRecoilBroadeningError, ValueError)
    src = open(os.path.join(_ROOT, "src", "qpd_potential", "em_recoil.py")).read()
    assert "warnings.warn" not in src
    assert "np.clip" not in src


def test_electron_analogue_is_evaluated_with_numbers():
    """test-electron-analogue-evaluated. The Compton-profile analogue must be
    EVALUATED, with a width scale and an explicit bound -- an unexamined 'no'
    fails even if the verdict is right (fp-unexamined-no)."""
    sc = er.electron_ia_scale_eV()
    # The lower bound is rigorous and derives only from the committed lattice
    # constant: sigma_pz >= hbar / (2 * bond length).
    d_ang = er.GE_LATTICE_CONSTANT_ANGSTROM * np.sqrt(3.0) / 4.0
    assert sc["bond_length_angstrom"] == pytest.approx(d_ang, rel=1e-12)
    assert sc["sigma_pz_lower_bound_au"] == pytest.approx(
        0.5 * er.BOHR_ANGSTROM / d_ang, rel=1e-12)
    assert sc["omega_bar_e_lower_bound_eV"] == pytest.approx(0.634740, rel=1e-5)
    # It is BIGGER than the nuclear scale, not smaller -- that is the finding.
    assert sc["omega_bar_e_lower_bound_eV"] > params.OMEGA_BAR_eV.value
    assert sc["ratio_lower_bound_to_nuclear"] == pytest.approx(35.5404, rel=1e-4)
    assert sc["width_ratio_lower_bound"] == pytest.approx(5.96158, rel=1e-4)
    assert sc["width_ratio_whole_atom"] == pytest.approx(362.977, rel=1e-4)

    # And the analogue is NOT negligible against the response chain: at the
    # extended floor its width is >2.5x the deposit, ~86 extended grid bins.
    s = er.electron_side_summary(er.EXT_FLOOR_eV)
    assert s["sigma_T_over_T_lower_bound"] == pytest.approx(2.5202, rel=1e-3)
    assert s["sigma_T_in_bins_lower_bound"] > 50.0
    # But it is OUTSIDE ITS OWN VALIDITY DOMAIN there: 2W_e < 1.
    assert s["two_W_e_lower_bound"] < 1.0
    assert s["two_W_e_whole_atom_envelope"] < 1.0e-3
    # sigma_T = sqrt(T * omega_bar_e) exactly, by construction of the estimator
    assert er.electron_side_sigma_T_eV(4.0, 9.0) == pytest.approx(6.0, rel=1e-14)


_IDENTITY_FORMS = ("1/sqrt(2w)", "1/√(2w)", "e_r/omega_bar", "e_r/ω̄")
_DISCLAIMERS = ("identit", "construction", "corroborat", "fp-identity",
                "never cites", "is not evidence", "units check")


def test_no_section_J_identity_is_cited_as_evidence():
    """fp-identity-as-corroboration. The Section-J identities may appear ONLY
    inside an explicit disclaimer, never as support for a claim."""
    for path in (os.path.join(_ROOT, "src", "qpd_potential", "em_recoil.py"),
                 _REPORT):
        text = open(path, encoding="utf-8").read()
        assert "fp-identity-as-corroboration" in text
        lines = text.split("\n")
        for i, raw in enumerate(lines):
            if any(f in raw.lower() for f in _IDENTITY_FORMS):
                ctx = " ".join(lines[max(0, i - 3):i + 4]).lower()
                assert any(d in ctx for d in _DISCLAIMERS), (
                    f"{path}:{i + 1}: a Section-J identity appears with no "
                    f"disclaimer in its neighbourhood:\n{raw}")


def test_report_names_the_recoiling_body_and_a_falsifier():
    """test-verdict-argued (automatable part). The argument must name the
    recoiling body and the momentum distribution per channel, and state a
    falsifier. 'nuclear is not electron' with no further content FAILS."""
    text = open(_REPORT, encoding="utf-8").read()
    low = text.lower()
    for token in ("compton profile", "j(p_z)", "recoiling body",
                  "falsif", "omega_bar_e", "2w_e", "named gap"):
        assert token in low, f"report is missing {token!r}"
    assert "0.634740" in text or "0.6347" in text
    assert "does_not_apply" in text


def test_no_relocation_quantity_in_this_plans_code_or_report():
    """fp-shielded-quantity-leak, applied to the Plan 15-01 surface.

    The token list is IMPORTED via ``surface_environment.shielded_token_guard()``,
    never re-typed: two divergent copies of a guard list is how a guard silently
    stops guarding, and the digit-boundary matching that keeps the Ge lattice
    constant 5.658 from false-positiving on the 5.65 Bq/kg 238U ambience lives
    there.  A hit is only a leak if it is an APPLIED quantity; the negative
    enumeration ROADMAP SC4 demands is recognised via NOT_APPLIED_MARKERS.
    """
    import test_env_v1_identity as ev
    # SHIELDED_TOKENS in full, plus the two SHIELDED_TOKENS_EXTRA entries that
    # name a relocation artefact rather than an English word.  "residual" is
    # DELIBERATELY EXCLUDED here and the exclusion is justified rather than
    # convenient: SHIELDED_TOKENS_EXTRA is scoped by its own docstring to the
    # ASSEMBLED ENVIRONMENT SET (Plan 09-03), and Plan 09-01 scanned SOURCE
    # MODULES with SHIELDED_TOKENS alone. In a source module "residual" is the
    # Phase-12 counts-budget field name (residual_retained_plus_leaked,
    # residual_fold) and an ordinary English word in a falsifier clause, neither
    # of which is a post-veto quantity. Plan 15-04 applies the FULL list,
    # including "residual" and "Table 5", to the environment-set surface where
    # it belongs, and audits the muon Table-5 residual by name and value there.
    tokens = ev.SHIELDED_TOKENS + tuple(
        t for t in ev.SHIELDED_TOKENS_EXTRA if t[0] in ("dru", "Table 5"))
    local_allow = ()
    for path in (os.path.join(_ROOT, "src", "qpd_potential", "em_recoil.py"),
                 _FLOORS):
        text = ev.normalize_unicode(open(path, encoding="utf-8").read())
        for lineno, name, line in ev.scan_text(text, tokens):
            ok = (any(m.lower() in line.lower() for m in ev.NOT_APPLIED_MARKERS)
                  or any(a in line for a in local_allow))
            assert ok, (
                f"{path}:{lineno}: shielded token {name!r} appears as an APPLIED "
                f"quantity:\n{line}")


# --------------------------------------------------------------------------- #
# claim-muon-validity-floor                                                     #
# --------------------------------------------------------------------------- #
def test_reference_point_reproduces_the_09_01_scalars():
    """The floor is computed at the SAME reference point the verified v1.0
    vertical-chord scalars were verified at."""
    bg = er.reference_beta_gamma()
    dp, xi = md.mpv_deposit(md.RHO * 0.20, bg)
    assert float(xi) == pytest.approx(0.072069, abs=5e-7)     # 09-01 Sec 2.3
    assert float(dp) == pytest.approx(1.230614, abs=5e-6)     # 09-01 Sec 2.3
    assert float(md.kappa(md.RHO * 0.20, bg)) == pytest.approx(6.727e-5, rel=1e-3)
    assert float(dp) < 1.458502                               # Delta_p < <Delta>


def test_mpv_with_I_reproduces_committed_path():
    """The I-exposed re-expression must be the committed formula, exactly, at
    the committed I -- otherwise the sensitivity study is measuring a different
    model from the floor."""
    bg = er.reference_beta_gamma()
    for ell in (1e-7, 1e-5, 1e-3, 0.20):
        a, xa = er._mpv_deposit_with_I(md.RHO * ell, bg, md.I_GE)
        b, xb = md.mpv_deposit(md.RHO * ell, bg)
        assert float(a) == pytest.approx(float(b), rel=1e-14)
        assert float(xa) == pytest.approx(float(xb), rel=1e-14)


def test_muon_floor_computed():
    """test-muon-floor-computed. The frozen floor reproduces from the committed
    code path to better than 1%, and I carries a named source."""
    lv = er.landau_validity_floor()
    assert lv["xi_at_crossing_eV"] == pytest.approx(er.I_GE_eV, rel=1e-12)
    assert lv["floor_eV"] == pytest.approx(4111.8165, rel=1e-6)
    assert lv["chord_um"] == pytest.approx(9.712913, rel=1e-6)
    assert er.I_GE_eV == 350.0
    assert "muon_deposit.py" in er.I_GE_PROVENANCE and "PDG" in er.I_GE_PROVENANCE
    row = [r for r in _floor_rows()
           if r["criterion_name"] == "landau_vavilov_xi_le_I"][0]
    assert float(row["floor_eV[eV]"]) == pytest.approx(lv["floor_eV"], rel=1e-2)
    assert float(row["I_eV[eV]"]) == 350.0


def test_floor_reported_against_v1_bins():
    """test-floor-reported-against-v1-bins. THE DISCONFIRMING CHECK. The count
    is computed and recorded whatever it is; no criterion was tuned."""
    lv = er.landau_validity_floor()
    ind = er.indicted_v1_bins(lv["floor_eV"])
    assert ind["n_v1_bins_total"] == 584
    assert ind["n_v1_bins_below_floor"] == 209
    assert ind["n_ext_bins_below_floor"] == 369
    assert lv["floor_eV"] > er.V1_FLOOR_eV, (
        "the floor lies ABOVE the v1.0 grid floor -- that is the finding")
    row = [r for r in _floor_rows()
           if r["criterion_name"] == "landau_vavilov_xi_le_I"][0]
    assert int(row["n_v1_bins_below_floor[count]"]) == 209
    assert row["floor_above_v1_grid_floor[bool]"] == "True"
    # and the report says so in words, without softening
    text = open(_REPORT, encoding="utf-8").read()
    assert "209" in text and "584" in text
    assert "fp-floor-softened" in text


def test_floor_sensitivity_to_I_never_reaches_zero():
    """No plausible I makes the indicted count vanish, so the finding cannot be
    an artefact of the adopted mean excitation energy."""
    rows = er.landau_floor_sensitivity_to_I()
    counts = [r["n_v1_bins_below_floor"] for r in rows]
    assert min(counts) >= 200 and max(counts) <= 220
    committed = [r for r in rows if r["is_committed_value"]]
    assert len(committed) == 1
    assert committed[0]["floor_eV"] == pytest.approx(4111.8165, rel=1e-6)


def test_chord_map_lattice():
    """test-chord-map-lattice. Both chord lengths computed; the extended-floor
    chord reported in Ge lattice constants and under ~10 of them."""
    ell_v1 = er.chord_cm_of_deposit_eV(er.V1_FLOOR_eV)
    ell_ext = er.chord_cm_of_deposit_eV(er.EXT_FLOOR_eV)
    assert float(er.deposit_eV_of_chord_cm(ell_v1)) == pytest.approx(
        er.V1_FLOOR_eV, rel=1e-9)
    assert float(er.deposit_eV_of_chord_cm(ell_ext)) == pytest.approx(
        er.EXT_FLOOR_eV, rel=1e-9)
    n_v1 = er.chord_in_lattice_constants(ell_v1)
    n_ext = er.chord_in_lattice_constants(ell_ext)
    assert n_v1 == pytest.approx(78.268, rel=1e-4)
    assert n_ext == pytest.approx(1.8689, rel=1e-4)
    assert n_ext < 10.0
    text = open(_REPORT, encoding="utf-8").read()
    assert "lattice constant" in text.lower()
    assert "atomic layer" in text.lower(), (
        "if the extended-floor chord is under ~10 lattice constants the report "
        "must say in words that it is a path of a few atomic layers")


# --------------------------------------------------------------------------- #
# claim-compton-validity-floor                                                  #
# --------------------------------------------------------------------------- #
def test_S_domain_covers_floor():
    """test-S-domain-covers-floor. x at the extended floor is inside the
    committed table domain, with the margin stated."""
    s = er.compton_S_suppression(er.EXT_FLOOR_eV)
    assert s["inside_table_domain"] is True
    assert s["x_inv_angstrom"] == pytest.approx(1.288806e-2, rel=1e-5)
    assert s["margin_above_table_floor"] == pytest.approx(12.888, rel=1e-3)
    # no interpolator raises anywhere on the extended axis for this channel
    ext = md.shared_energy_grid("v2.0-ext")
    centres_eV = np.sqrt(ext[:-1] * ext[1:]) * 1.0e3
    x = er.compton_x_of_recoil_inv_angstrom(centres_eV)
    S = cs.incoherent_S(x)
    assert np.all(np.isfinite(S)) and np.all(S > 0.0)


def test_momentum_transfer_variable_is_the_momentum_transfer():
    """Independent cross-check that x really is a momentum transfer:
    4 pi x a_0 must equal sqrt(2 m_e T) in atomic units."""
    for T in (er.EXT_FLOOR_eV, 1.0, er.V1_FLOOR_eV, 100.0):
        x = float(er.compton_x_of_recoil_inv_angstrom(T))
        q_from_x = 4.0 * np.pi * x * er.BOHR_ANGSTROM
        q_direct = np.sqrt(2.0 * (T / er.HARTREE_eV))
        assert q_from_x == pytest.approx(q_direct, rel=1e-6)
    # and it is line-energy independent at small transfer, as a momentum
    # transfer must be
    for Eg in (241.997, 1460.822, 2614.511):
        x_line = float(er.compton_x_of_recoil_inv_angstrom(er.EXT_FLOOR_eV, Eg))
        x_lim = float(er.compton_x_of_recoil_inv_angstrom(er.EXT_FLOOR_eV))
        assert x_line == pytest.approx(x_lim, rel=1e-6)


def test_S_suppression_computed():
    """test-S-suppression-computed. Both suppression factors reproduce from the
    committed table to better than 1% and are frozen with their energies."""
    s_ext = er.compton_S_suppression(er.EXT_FLOOR_eV)
    s_v1 = er.compton_S_suppression(er.V1_FLOOR_eV)
    assert s_ext["S_over_Z"] == pytest.approx(2.185858e-3, rel=1e-5)
    assert s_ext["suppression_vs_free_KN"] == pytest.approx(457.486, rel=1e-4)
    assert s_v1["S_over_Z"] == pytest.approx(0.1235564, rel=1e-5)
    assert s_v1["suppression_vs_free_KN"] == pytest.approx(8.0935, rel=1e-4)
    rows = {r["criterion_name"]: r for r in _floor_rows()}
    assert float(rows["S_suppression_at_ext_grid_floor"]["S_over_Z[dimensionless]"]) \
        == pytest.approx(s_ext["S_over_Z"], rel=1e-2)
    assert float(rows["S_suppression_at_v1_grid_floor"]["S_over_Z[dimensionless]"]) \
        == pytest.approx(s_v1["S_over_Z"], rel=1e-2)


def test_compton_physical_floor_is_named_not_assumed():
    """test-compton-physical-floor-stated (automatable part)."""
    pf = er.compton_physical_floor()
    assert pf["adopted_floor_eV"] == pytest.approx(0.73955, rel=1e-9)
    assert "UNVERIFIED" in pf["provenance"]
    assert "300 K" in pf["alternatives_named"]
    # the adopted floor sits ABOVE the extended grid floor -- the whole point
    assert pf["adopted_floor_eV"] > er.EXT_FLOOR_eV
    text = open(_REPORT, encoding="utf-8").read()
    assert "fp-suppressed-means-valid" in text
    low = text.lower()
    assert "band gap" in low and "exciton" in low
    assert "not the same" in low or "is not a rate" in low


# --------------------------------------------------------------------------- #
# test-dimensions                                                               #
# --------------------------------------------------------------------------- #
def test_dimensions():
    """test-dimensions. Every emitted quantity carries its declared dimension
    and every CSV column header names its units."""
    with open(_FLOORS, newline="") as fh:
        header = next(csv.reader(r for r in fh if not r.startswith("#")))
    for col in header:
        if col in ("channel", "criterion_name", "accuracy_label", "note"):
            continue
        assert col.endswith("]") and "[" in col, f"{col} carries no units"
    units = {c.split("[")[0]: c.split("[")[1][:-1] for c in header if "[" in c}
    assert units["floor_eV"] == "eV"
    assert units["xi_at_floor_eV"] == "eV"
    assert units["chord_at_floor_cm"] == "cm"
    assert units["x_inv_angstrom"] == "1/angstrom"
    assert units["S_over_Z"] == "dimensionless"
    assert units["I_eV"] == "eV"

    # scaling checks: sigma has the dimension of energy and scales as sqrt
    assert er.electron_side_sigma_T_eV(4.0, 1.0) / \
        er.electron_side_sigma_T_eV(1.0, 1.0) == pytest.approx(2.0, rel=1e-14)
    # xi is linear in the chord, and in MeV internally / eV on the emitted axis
    assert float(er.xi_eV_of_chord_cm(2.0e-4)) / \
        float(er.xi_eV_of_chord_cm(1.0e-4)) == pytest.approx(2.0, rel=1e-12)
    assert er.xi_coefficient_MeV_per_cm() == pytest.approx(0.3603450, rel=1e-6)
    assert float(er.xi_eV_of_chord_cm(1.0)) == pytest.approx(
        er.xi_coefficient_MeV_per_cm() * 1e6, rel=1e-12)


def test_floors_table_is_registered_and_headed():
    """The frozen table exists, has a disposition row, and its header records
    the verdict, the indicted count, and the reproduction command."""
    from qpd_potential import legacy_grid as lg
    d = lg.disposition_for("artifacts/v2.0/em_validity_floors.csv")
    assert d.disposition in lg.DISPOSITION_VALUES
    assert len(d.reason) > 40
    h = _floor_header()
    assert "does_not_apply" in h
    assert "209 of the 584" in h
    assert "reproduce =" in h
    assert "exp(-2W)" in h
    assert len(_floor_rows()) == 6
