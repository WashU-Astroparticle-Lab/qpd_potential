# ASSERT_CONVENTION: natural_units=not_applicable, metric_signature=not_applicable, fourier_convention=not_applicable, coupling_convention=not_applicable, renormalization_scheme=not_applicable, gauge_choice=not_applicable
"""Acceptance tests for the veto-credit sentinels and the taxonomy (Plan 08-04).

Maps to the plan's acceptance-test ids:

    test-taxonomy-complete        -- every catalogued statement is exactly one
                                     taxonomy row, with all required fields.
    test-verbatim-classification  -- sampled row quotes are re-greped against the
                                     frozen source and must match exactly.
    test-l1star-documented        -- the L1* tier is defined, justified, and
                                     documented as a ROADMAP SC2 extension.
    test-credit-sentinel          -- L2_CREDIT and L1STAR_CREDIT are exactly 1.0,
                                     their docstrings cite Phase 8 and VALD-09,
                                     and the tier lookup round-trips against every
                                     taxonomy row id.
    test-no-orphan-veto-factor    -- the two-rule repository guard, DEMONSTRATED
                                     to fire on both violation types and to stay
                                     silent on Plan 08-03's geometry constants.
    test-l2off-framing            -- the baseline is named and is never described
                                     as a conservative subset of NUCLEUS.
    test-pitfalls-factor5         -- no bare factor-5 survives in PITFALLS.md.
    test-pitfalls-footprint       -- the array footprint is basis-labelled.
    test-phase9-handoff-recorded  -- the Fig. 8 trace-selection handoff exists.

THE GUARD IS THE STRUCTURAL DEFENCE FOR ``fp-veto-credit-transfer``.
    It is deliberately built from two DECIDABLE rules. The obvious formulation --
    grep the tree for a bare ``5`` or ``0.2`` -- is not decidable: Plan 08-03
    legitimately introduces ``COV_CRYSTAL_THICKNESS_CM = 2.5``,
    ``B4C_THICKNESS_CM = 4.0`` and the wafer's ``LZ = 0.20``, and a guard that
    false-positives on geometry gets disabled, which is the same failure as
    having none. Rule 1 is therefore restricted to two literals that have no
    legitimate non-veto meaning anywhere in this project, and Rule 2 -- the rule
    with teeth -- keys on the NAME, because a reintroduced veto factor has to be
    named in order to be used.

WHAT THE GUARD DOES NOT CATCH -- stated so it is not mistaken for completeness.
    An anonymous inline literal, e.g. ``rate / 5`` inside a function body, is
    invisible to both rules, because no decidable rule can distinguish it from a
    legitimate arithmetic constant. The guard raises the cost of reintroducing a
    veto credit and makes the reviewable-diff path the path of least resistance;
    it is not a proof that no rejection factor can enter. The reviewable-diff
    property comes from ``veto_credit.credit_for()`` being the only named way to
    obtain a credit at all.
"""
from __future__ import annotations

import ast
import importlib.util
import re
import subprocess
import tokenize
from pathlib import Path

import pytest

from qpd_potential import veto_credit as vc

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = Path(vc.__file__).resolve().parent
MODULE_PATH = Path(vc.__file__).resolve()
TAXONOMY_MD = REPO_ROOT / "GPD" / "analysis" / "VETO-TAXONOMY.md"
PITFALLS_MD = REPO_ROOT / "GPD" / "literature" / "PITFALLS.md"
EVIDENCE_MD = (
    REPO_ROOT
    / "GPD"
    / "phases"
    / "08-veto-envelope-geometry-gate-p-veto"
    / "08-01-SOURCE-EVIDENCE.md"
)
FROZEN_DIR = REPO_ROOT / "data" / "external" / "nucleus"
FROZEN_2509 = FROZEN_DIR / "2509.03559v1.txt"

#: Rule 1. The ONLY two literals on the denylist. Both encode the NUCLEUS
#: MV+COV muon-induced rejection percentage and have no other meaning here.
DENIED_LITERALS = (99.8, 0.998)

#: Rule 2. A module-level numeric constant whose name matches any of these must
#: equal exactly 1.0.
CREDIT_NAME_RE = re.compile(r"CREDIT|REJECTION|VETO_FACTOR", re.IGNORECASE)

_ROW_LINE = re.compile(r"^\|\s*`(row-[a-z0-9-]+)`\s*\|")
_QUOTED = re.compile(r'"([^"]{15,})"')

_TAXONOMY_COLUMNS = (
    "row_id",
    "statement",
    "section",
    "evidence",
    "tier",
    "transfers_as",
    "credit",
    "credit_basis",
    "swap_test",
)


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #
def _unmark(cell: str) -> str:
    """Strip markdown bold/code markers from a table cell."""
    return cell.replace("**", "").replace("`", "").replace("\\*", "*").strip()


def _taxonomy_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for lineno, line in enumerate(TAXONOMY_MD.read_text().splitlines(), start=1):
        m = _ROW_LINE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(cells) == len(_TAXONOMY_COLUMNS), (
            f"{TAXONOMY_MD.name}:{lineno} has {len(cells)} cells, expected "
            f"{len(_TAXONOMY_COLUMNS)}: {_TAXONOMY_COLUMNS}"
        )
        row = dict(zip(_TAXONOMY_COLUMNS, cells))
        row["_lineno"] = str(lineno)
        rows[m.group(1)] = row
    return rows


def _package_modules() -> list[Path]:
    return sorted(PACKAGE_DIR.glob("*.py"))


def _number_literals(path: Path) -> list[tuple[int, str, float]]:
    """Every NUMBER token in ``path`` as (line, text, value).

    Tokenizing partitions the source exactly: any occurrence of ``99.8`` in a
    Python file is either a NUMBER token (a value the interpreter evaluates), or
    it is inside a STRING or COMMENT token, i.e. inside a docstring or a comment.
    Restricting the check to NUMBER tokens is therefore precisely the plan's
    "must not appear outside a docstring or comment" rule, made decidable.
    """
    out: list[tuple[int, str, float]] = []
    with open(path, "rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type != tokenize.NUMBER:
                continue
            try:
                value = float(tok.string.replace("_", ""))
            except ValueError:  # complex literals etc.
                continue
            out.append((tok.start[0], tok.string, value))
    return out


def rule1_violations(path: Path) -> list[str]:
    """RULE 1 -- literal denylist. Returns human-readable violations."""
    bad = []
    for lineno, text, value in _number_literals(path):
        for denied in DENIED_LITERALS:
            if abs(value - denied) < 1e-12:
                bad.append(
                    f"{path}:{lineno}: literal {text} evaluates to {denied} -- a NUCLEUS "
                    "rejection percentage used as a computational value "
                    "(fp-veto-credit-transfer)"
                )
    return bad


def rule2_violations(module, path: Path | None = None) -> list[str]:
    """RULE 2 -- naming convention. Returns human-readable violations.

    Checked by importing the module and inspecting its namespace rather than by
    grep, so that the value actually bound at runtime is what is tested.
    """
    path = path or Path(getattr(module, "__file__", "<unknown>"))
    source = ""
    try:
        source = Path(path).read_text()
    except OSError:
        pass
    bad = []
    for name, value in vars(module).items():
        if not CREDIT_NAME_RE.search(name):
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        if value == 1.0:
            continue
        lineno = "?"
        for i, line in enumerate(source.splitlines(), start=1):
            if re.match(rf"^\s*{re.escape(name)}\s*[:=]", line):
                lineno = str(i)
                break
        bad.append(
            f"{path}:{lineno}: module-level constant {name} = {value!r} != 1.0. "
            "A named credit/rejection/veto factor must be exactly 1.0 unless a "
            "wafer-specific veto geometry and a documented argument are supplied "
            "(VALD-09, fp-veto-credit-transfer)."
        )
    return bad


def _import_from_path(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _attribute_docstrings(path: Path) -> dict[str, str]:
    """PEP-258 attribute docstrings: the string literal following an assignment."""
    tree = ast.parse(path.read_text())
    out: dict[str, str] = {}
    body = tree.body
    for i, node in enumerate(body[:-1]):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        nxt = body[i + 1]
        if (
            isinstance(nxt, ast.Expr)
            and isinstance(nxt.value, ast.Constant)
            and isinstance(nxt.value.value, str)
        ):
            out[target.id] = nxt.value.value
    return out


@pytest.fixture(scope="module")
def rows() -> dict[str, dict[str, str]]:
    return _taxonomy_rows()


# --------------------------------------------------------------------------- #
# test-credit-sentinel                                                         #
# --------------------------------------------------------------------------- #
def test_credit_constants_are_exactly_one():
    """Exact comparison, not a tolerance: 1.0 is the whole claim."""
    assert vc.L2_CREDIT == 1.0
    assert vc.L1STAR_CREDIT == 1.0
    assert vc.L1_REJECTION_CREDIT == 1.0
    for name in vc.CONSTANT_DOC_KEYS:
        value = getattr(vc, name)
        assert type(value) is float, f"{name} is {type(value)}, expected float"
        assert repr(value) == "1.0", f"{name} reprs as {value!r}, expected 1.0"


def test_credit_constant_docstrings_cite_phase_8_and_vald_09():
    docs = _attribute_docstrings(MODULE_PATH)
    for name in vc.CONSTANT_DOC_KEYS:
        assert name in docs, f"{name} has no attribute docstring"
        doc = docs[name]
        assert "Phase 8" in doc, f"{name} docstring does not cite Phase 8"
        assert "VALD-09" in doc, f"{name} docstring does not cite VALD-09"
        assert "REASON" in doc or "transfer" in doc, (
            f"{name} docstring does not state the reason"
        )
    # "1.0 means the background is unchanged" must be stated so nobody reads 1.0
    # as full credit.
    l2 = docs["L2_CREDIT"]
    assert "1.0 MEANS THE BACKGROUND IS UNCHANGED" in l2.upper()
    assert "1.0 MEANS THE BACKGROUND IS UNCHANGED" in docs["L1STAR_CREDIT"].upper()


def test_module_docstring_states_the_change_requirement():
    doc = (vc.__doc__ or "").upper()
    assert "WAFER-SPECIFIC VETO GEOMETRY" in doc
    assert "DOCUMENTED ARGUMENT" in doc
    assert "REVIEWABLE DIFF" in doc
    assert "A CREDIT OF 1.0 MEANS THE BACKGROUND IS UNCHANGED" in doc


def test_tier_lookup_covers_every_taxonomy_row_with_no_gaps_or_extras(rows):
    md_ids = set(rows)
    code_ids = set(vc.TAXONOMY)
    assert md_ids, "no rows parsed out of GPD/analysis/VETO-TAXONOMY.md"
    assert md_ids == code_ids, (
        f"missing from code: {sorted(md_ids - code_ids)}; "
        f"extra in code: {sorted(code_ids - md_ids)}"
    )
    for row_id in sorted(md_ids):
        assert vc.credit_for(row_id) == 1.0
        assert vc.tier_of(row_id) == _unmark(rows[row_id]["tier"])
        assert vc.lookup(row_id).credit_basis == _unmark(rows[row_id]["credit_basis"])


def test_lookup_raises_on_an_uncatalogued_statement():
    with pytest.raises(KeyError) as exc:
        vc.credit_for("row-invented-veto")
    assert "VETO-TAXONOMY" in str(exc.value)


def test_taxonomy_row_constructor_rejects_a_credit_other_than_one():
    """The dataclass itself refuses a partial credit, not only the tests."""
    with pytest.raises(ValueError, match="1.0"):
        vc.TaxonomyRow(
            row_id="row-test",
            tier="L2",
            credit=0.2,
            credit_basis="policy",
            section="5.2.1",
            evidence="B.5",
            subject="test",
            transfers_as="nothing",
            note="test",
        )


def test_rows_in_tier_partitions_the_taxonomy():
    total = sum(len(vc.rows_in_tier(t)) for t in vc.TIERS)
    assert total == len(vc.TAXONOMY)
    assert len(vc.rows_in_tier("L1*")) == 2  # B4C liner + internal shielding
    assert {r.row_id for r in vc.rows_in_tier("L1*")} == {
        "row-a09-internal-shielding-b4c",
        "row-b04-b4c-attenuation-factor5",
    }


# --------------------------------------------------------------------------- #
# The multiplicity row: 1.0 BY DERIVATION                                      #
# --------------------------------------------------------------------------- #
def test_multiplicity_row_basis_is_derivation_and_is_the_only_one(rows):
    row = vc.TAXONOMY["row-b02-multiplicity-cut"]
    assert row.credit_basis == "derivation"
    derived = [r.row_id for r in vc.TAXONOMY.values() if r.credit_basis == "derivation"]
    assert derived == ["row-b02-multiplicity-cut"]
    assert "wafer_self_veto" in row.note
    assert _unmark(rows["row-b02-multiplicity-cut"]["credit_basis"]) == "derivation"


def test_multiplicity_derivation_is_consumed_not_restated():
    """veto_credit calls Plan 08-02's function; it does not re-assert the zero."""
    assert vc.multiplicity_rejection_is_zero() is True
    from qpd_potential import wafer_self_veto as wsv

    assert wsv.mult_rejection(1) == 0.0  # identity comparison, not a tolerance


# --------------------------------------------------------------------------- #
# test-no-orphan-veto-factor -- RULE 1 and RULE 2 across the package           #
# --------------------------------------------------------------------------- #
def test_rule1_literal_denylist_passes_on_the_current_tree():
    violations: list[str] = []
    for path in _package_modules():
        violations += rule1_violations(path)
    assert not violations, "\n".join(violations)


def test_rule2_naming_convention_passes_on_the_current_tree():
    import importlib

    violations: list[str] = []
    for path in _package_modules():
        if path.name == "__init__.py":
            module = importlib.import_module("qpd_potential")
        else:
            module = importlib.import_module(f"qpd_potential.{path.stem}")
        violations += rule2_violations(module, path)
    assert not violations, "\n".join(violations)


def test_rule1_FIRES_on_an_injected_literal(tmp_path):
    """Demonstration, not assumption: the guard must actually catch this."""
    fixture = tmp_path / "orphan_literal.py"
    fixture.write_text(
        '"""A docstring mentioning 99.8% -- this must NOT trip the guard."""\n'
        "# a comment mentioning 0.998 -- this must NOT trip the guard either\n"
        "SURVIVING_FRACTION = 0.998\n"  # <-- the violation
    )
    violations = rule1_violations(fixture)
    assert len(violations) == 1, violations
    assert "orphan_literal.py:3" in violations[0]
    assert "0.998" in violations[0]


def test_rule1_does_not_fire_on_docstring_or_comment_mentions(tmp_path):
    fixture = tmp_path / "quoted_only.py"
    fixture.write_text(
        '"""NUCLEUS predict rejection of more than 99.8% of the muon-induced\n'
        'backgrounds. Quoted for identification; NOT applied. 0.998 likewise."""\n'
        "# 99.8 in a comment\n"
        "COV_REJECTION_CREDIT = 1.0\n"
    )
    assert rule1_violations(fixture) == []


def test_rule2_FIRES_on_an_injected_named_rejection_constant(tmp_path):
    """Demonstration, not assumption: the naming rule is the one with teeth."""
    fixture = tmp_path / "orphan_named.py"
    fixture.write_text(
        "COV_CRYSTAL_THICKNESS_CM = 2.5\n"
        "B4C_THICKNESS_CM = 4.0\n"
        "LZ = 0.20\n"
        "COV_REJECTION = 5.0\n"  # <-- the violation
    )
    module = _import_from_path(fixture, "orphan_named")
    violations = rule2_violations(module, fixture)
    assert len(violations) == 1, violations
    assert "COV_REJECTION" in violations[0]
    assert "orphan_named.py:4" in violations[0]


def test_rule2_FIRES_on_a_partial_credit_too(tmp_path):
    """A reduced credit is not permitted either (explicit user decision)."""
    fixture = tmp_path / "partial_credit.py"
    fixture.write_text("L2_CREDIT = 0.2\n")
    module = _import_from_path(fixture, "partial_credit")
    violations = rule2_violations(module, fixture)
    assert len(violations) == 1 and "L2_CREDIT" in violations[0]


def test_guard_is_SILENT_on_plan_0803_geometry_constants(tmp_path):
    """A guard that false-positives gets disabled -- the same failure as none.

    Checked two ways: against a fixture that replicates the three constants the
    plan names, and against the real modules that define them.
    """
    fixture = tmp_path / "geometry_only.py"
    fixture.write_text(
        "COV_CRYSTAL_THICKNESS_CM = 2.5\n"
        "B4C_THICKNESS_CM = 4.0\n"
        "COV_CRYSTAL_DIAMETER_CM = 10.0\n"
        "LZ = 0.20\n"
        "ARRAY_CRYSTAL_FOOTPRINT_CM2 = 2.25\n"
        "HOLDER_SCALE_FOOTPRINT_CM2 = 9.0\n"
    )
    module = _import_from_path(fixture, "geometry_only")
    assert rule1_violations(fixture) == []
    assert rule2_violations(module, fixture) == []

    from qpd_potential import veto_envelope, wafer_geometry

    for mod in (veto_envelope, wafer_geometry):
        path = Path(mod.__file__)
        assert rule1_violations(path) == []
        assert rule2_violations(mod, path) == []

    # and the values really are the ones the plan names
    assert veto_envelope.COV_CRYSTAL_THICKNESS_CM == 2.5
    assert veto_envelope.B4C_THICKNESS_CM == 4.0
    assert wafer_geometry.LZ == 0.20


def test_veto_credit_module_itself_carries_no_nucleus_rejection_number():
    """No NUCLEUS percentage or factor appears in veto_credit.py at all."""
    source = MODULE_PATH.read_text()
    for token in ("99.8", "0.998"):
        assert token not in source, (
            f"{token} appears in veto_credit.py. The verbatim NUCLEUS sentences "
            "belong in GPD/analysis/VETO-TAXONOMY.md, not in the package."
        )


# --------------------------------------------------------------------------- #
# test-taxonomy-complete                                                       #
# --------------------------------------------------------------------------- #
def test_every_row_carries_every_required_field(rows):
    for row_id, row in rows.items():
        where = f"{TAXONOMY_MD.name}:{row['_lineno']} ({row_id})"
        assert _QUOTED.search(row["statement"]), f"{where}: no verbatim quote"
        assert "§" in row["section"], f"{where}: no section reference"
        assert row["evidence"], f"{where}: no evidence-block reference"
        assert _unmark(row["tier"]) in vc.TIERS, f"{where}: bad tier"
        assert _unmark(row["credit"]) == "1.0", f"{where}: credit is not 1.0"
        assert _unmark(row["credit_basis"]) in vc.CREDIT_BASES, f"{where}: bad basis"
        assert len(row["swap_test"]) > 30, f"{where}: swap-test justification too thin"
        assert row["transfers_as"], f"{where}: no transfers-as entry"


def test_no_statement_appears_twice(rows):
    subjects = [row["statement"] for row in rows.values()]
    assert len(subjects) == len(set(subjects))
    assert len(rows) == len(vc.TAXONOMY)


def test_both_credit_bases_named_by_the_acceptance_test_are_present(rows):
    bases = {_unmark(r["credit_basis"]) for r in rows.values()}
    assert "policy" in bases
    assert "derivation" in bases
    assert bases <= set(vc.CREDIT_BASES)


def test_the_three_factor_five_statements_are_three_separate_rows():
    """Never merged. Three rows, three physical objects, three roles."""
    passive = vc.TAXONOMY["row-b04-b4c-attenuation-factor5"]
    active = vc.TAXONOMY["row-b05-cov-neutron-anticoincidence"]
    modelling = vc.TAXONOMY["row-b03-geant4-quenching-downscale"]
    assert passive.tier == "L1*"
    assert active.tier == "L2" and active.credit_basis == "policy"
    assert modelling.credit_basis == "not-a-rejection-factor"
    assert "NOT A REJECTION FACTOR" in modelling.note
    assert len({passive.evidence, active.evidence, modelling.evidence}) == 3


def test_the_evidence_block_section_b_is_covered(rows):
    """Every §B entry is either a taxonomy row or an explicitly excluded one."""
    evidence_sections = set(
        re.findall(r"^#{3,4} B\.(\d+)", EVIDENCE_MD.read_text(), flags=re.MULTILINE)
    )
    assert evidence_sections, "no B.n headings found in the evidence block"
    classified = {
        r["evidence"].lstrip("B.")
        for r in rows.values()
        if r["evidence"].startswith("B.")
    }
    text = TAXONOMY_MD.read_text()
    for n in sorted(evidence_sections, key=int):
        if n in classified:
            continue
        assert f"**B.{n}**" in text, (
            f"evidence-block §B.{n} is neither a taxonomy row nor explicitly "
            "recorded as carrying no row"
        )


# --------------------------------------------------------------------------- #
# test-verbatim-classification                                                 #
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(
    not FROZEN_2509.exists(), reason="frozen NUCLEUS source not present"
)
def test_sampled_row_quotes_reproduce_from_the_frozen_source(rows):
    """At least five rows spanning all three tiers, re-greped, not assumed."""
    sample = [
        "row-e11-overburden",  # L1
        "row-b10-pb-factor-50",  # L1
        "row-b04-b4c-attenuation-factor5",  # L1*
        "row-a09-internal-shielding-b4c",  # L1*
        "row-b05-cov-neutron-anticoincidence",  # L2
        "row-b09-mv-cov-muon-induced",  # L2
        "row-b03-geant4-quenching-downscale",  # L2
        "row-b02-multiplicity-cut",  # L2
    ]
    assert {_unmark(rows[r]["tier"]) for r in sample} == set(vc.TIERS)
    checked = 0
    for row_id in sample:
        for quote in _QUOTED.findall(rows[row_id]["statement"]):
            proc = subprocess.run(
                ["grep", "-o", "-F", quote, FROZEN_2509.name],
                cwd=FROZEN_DIR,
                capture_output=True,
                text=True,
            )
            assert proc.returncode == 0, (
                f"{row_id}: quote NOT found verbatim in {FROZEN_2509.name} -- this "
                f"row is a paraphrase and is a defect:\n{quote}"
            )
            assert quote in proc.stdout
            checked += 1
    assert checked >= 5


@pytest.mark.skipif(
    not FROZEN_2509.exists(), reason="frozen NUCLEUS source not present"
)
def test_every_recorded_grep_command_in_the_taxonomy_reruns_clean():
    commands = [
        line.strip()
        for line in TAXONOMY_MD.read_text().splitlines()
        if line.startswith("grep -o -F ")
    ]
    assert len(commands) >= 20, f"only {len(commands)} recorded commands"
    failures = [
        cmd
        for cmd in commands
        if subprocess.run(
            cmd, shell=True, cwd=FROZEN_DIR, capture_output=True
        ).returncode
        != 0
    ]
    assert not failures, "recorded commands that no longer reproduce:\n" + "\n".join(
        failures
    )


# --------------------------------------------------------------------------- #
# test-l1star-documented                                                       #
# --------------------------------------------------------------------------- #
def test_l1star_tier_is_defined_justified_and_labelled_an_extension():
    text = TAXONOMY_MD.read_text()
    assert "passive but payload-geometry-coupled" in text
    assert "binary" in text and "Success Criterion 2" in text
    assert "extends that criterion to three tiers" in text
    assert "presented as an\nextension" in text or "as an extension" in text
    assert "flatter the background budget" in text
    assert "nearly-4π" in text
    # both L1* members are named and their credit is 1.0
    for row_id in (
        "row-a09-internal-shielding-b4c",
        "row-b04-b4c-attenuation-factor5",
    ):
        assert row_id in text
        assert vc.TAXONOMY[row_id].tier == "L1*"
        assert vc.TAXONOMY[row_id].credit == 1.0
    # the counter-argument is recorded rather than suppressed
    assert "A reviewer could reasonably say against this" in text or (
        "reviewer could argue" in text
    )


# --------------------------------------------------------------------------- #
# test-l2off-framing                                                           #
# --------------------------------------------------------------------------- #
#: Every line of the taxonomy containing "conservativ" must contain one of these.
_CONSERVATIVE_ALLOWED = (
    "crude but conservative",  # inside the verbatim NUCLEUS quote (row-b03)
    "does not use that word to",  # the explicit prohibition sentence
)


def test_l2off_baseline_is_named_and_never_called_conservative():
    text = TAXONOMY_MD.read_text()
    assert "NUCLEUS's shielding without NUCLEUS's vetoes" in text
    assert "different and worse configuration" in text
    assert "trade-off" in text
    # the section 5.2.2 reasoning is quoted, not paraphrased
    assert "results from a\n> trade-off between (i) the production of secondary particles" in text
    assert "when combined with the COV" in text

    offending = [
        (n, line)
        for n, line in enumerate(text.splitlines(), start=1)
        if "conservativ" in line.lower()
        and not any(a in line for a in _CONSERVATIVE_ALLOWED)
    ]
    assert not offending, (
        "the word 'conservative' appears outside the allowed contexts (a verbatim "
        "NUCLEUS quote and the explicit prohibition):\n"
        + "\n".join(f"{n}: {line}" for n, line in offending)
    )


def test_taxonomy_stands_independently_of_the_fit_verdict():
    text = TAXONOMY_MD.read_text()
    assert "stands independently of the geometry-fit verdict" in text
    assert "Phase 16" in text
    assert "correct either way" in text


# --------------------------------------------------------------------------- #
# test-pitfalls-factor5                                                        #
# --------------------------------------------------------------------------- #
_FACTOR5_RE = re.compile(r"factor[ ~\-]*5\b", re.IGNORECASE)


def _correction_block_range(text: str, heading: str) -> range:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if heading in line)
    end = start + 1
    while end < len(lines) and (lines[end].startswith(">") or not lines[end].strip()):
        end += 1
    return range(start, end)


def test_pitfalls_factor5_correction_is_present_dated_and_sourced():
    text = PITFALLS_MD.read_text()
    assert "PHASE-8 CORRECTION 1" in text
    assert "2026-07-22" in text
    assert "08-01-SOURCE-EVIDENCE.md" in text
    for label in ("[F5-a]", "[F5-b]", "[F5-c]"):
        assert label in text, f"{label} missing"
    # each of the three statements is quoted with its section reference
    assert "further\n> > suppressing the event rates in the \\ceCaWO4 detectors by a factor \\sim 5." in text
    assert "the COV brings a sizable additional reduction of the" in text
    assert "scaled down all\n> > deposited energies in the COV and the MV volumes by a factor 5 and 2 respectively" in text
    assert text.count("§5.2.1, evidence block") == 3
    assert "NOT A REJECTION FACTOR" in text
    assert "summarizer" in text and "modelling conservatism" in text


def test_no_bare_factor5_survives_in_pitfalls():
    text = PITFALLS_MD.read_text()
    exempt = set(_correction_block_range(text, "PHASE-8 CORRECTION 1"))
    offending = [
        (i + 1, line)
        for i, line in enumerate(text.splitlines())
        if _FACTOR5_RE.search(line) and i not in exempt and "[F5-" not in line
    ]
    assert not offending, (
        "a factor-5 occurrence stands as a bare number, with no [F5-a/b/c] label "
        "naming which of the three section-5.2.1 statements it is:\n"
        + "\n".join(f"{n}: {line}" for n, line in offending)
    )


# --------------------------------------------------------------------------- #
# test-pitfalls-footprint                                                      #
# --------------------------------------------------------------------------- #
def test_pitfalls_footprint_correction_is_present_and_basis_labelled():
    text = PITFALLS_MD.read_text()
    assert "PHASE-8 CORRECTION 2" in text
    assert "2.25 cm²" in text
    assert "4.996 mm" in text and "5.008 mm" in text  # the two mass closures
    assert "must not be attributed to NUCLEUS" in text
    assert "holder-scale estimate" in text
    assert re.search(r"It is not a\s+>?\s*NUCLEUS number", text), (
        "the ~9 cm^2 value is not explicitly disowned as a NUCLEUS number"
    )

    offending = [
        (i + 1, line)
        for i, line in enumerate(text.splitlines())
        if ("45.9" in line or "11.5" in line) and "basis" not in line.lower()
    ]
    assert not offending, (
        "an area ratio is quoted without a basis label:\n"
        + "\n".join(f"{n}: {line}" for n, line in offending)
    )


# --------------------------------------------------------------------------- #
# test-phase9-handoff-recorded                                                 #
# --------------------------------------------------------------------------- #
def test_phase9_fig8_trace_selection_handoff_is_recorded():
    text = PITFALLS_MD.read_text()
    assert "PHASE-8 CORRECTION 3" in text
    assert "left panels show the impact of sequentially adding passive shielding layers" in text
    assert "right\n> > panels show how using the different veto detectors complements" in text
    assert "all vetoes" in text
    assert "apply all possible anti-coincidence criteria" in text
    assert "passive-only" in text
    assert "Phase 9" in text
    assert "would import an **L2**" in text
    assert "fp-veto-credit-transfer" in text


@pytest.mark.skipif(
    not FROZEN_2509.exists(), reason="frozen NUCLEUS source not present"
)
def test_fig8_caption_quote_is_verbatim_in_the_frozen_source():
    quote = (
        "The left panels show the impact of sequentially adding passive shielding "
        "layers. The right panels show how using the different veto detectors "
        "complements the passive shields. The “all vetoes” selection criteria "
        "apply all possible anti-coincidence criteria for the rejection of "
        "background events."
    )
    proc = subprocess.run(
        ["grep", "-o", "-F", quote, FROZEN_2509.name],
        cwd=FROZEN_DIR,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, "the Fig. 8 caption quote is not verbatim"
