---
profile_id: plan
status: draft
artifact_id: plan-0157
artifact_type: plan
parent_ids:
  - SPEC-0157
created: 2026-08-31
updated: 2026-08-31
---

# Script Surface Ownership Convergence Plan

## Objective

Converge `scripts/` and `tests/` on one ownership rule, in the order that keeps
every step measurable: reduce what no gate reaches, derive the counts that break
on legitimate change, restructure the directories, register every test module,
then split the four monoliths.

Reduction precedes restructuring. Moving unreachable code into a cleaner
directory produces a tidier version of the same excess.

## Dependencies

- SPEC-0155 merged at `703e3cf6`. Its plan rulings 1 to 11 carry forward and are restated below.
- `main` is the merge base for every `--base-ref` computation. It is computed, never pinned.
- This repository runs `python3 -m unittest`. `pytest` is not installed. Several modules require `PYTHONPATH=.`; the registered gate supplies it.
- `run-ci-gate.py --profile full` takes roughly 12 minutes. Run it at task boundaries, not per step.

## Execution Sequence

### Task 1: Reduce the corpus-lifecycle modes

**Files:**

- Modify: `scripts/validation/check-document-corpus-lifecycle.py` — `MODES` at line 96
- Modify: `scripts/lib/document_governance/suite_registry.py` — the `check-public` binding
- Modify: `.github/workflow-contract.yml` — add a `check-recovery` leaf beside the existing contract and promoted leaves
- Modify: `tests/validation/test_document_corpus_lifecycle.py` — `test_modes_are_the_exact_fixed_tuple` at line 1109, and the three `test_all_sixteen_modes_*` matrices at 4463, 4500, 4634
- Modify: `.github/workflows/document-corpus-lifecycle.yml` — remove the three non-gating steps
- Delete: `scripts/lib/document_governance/provenance_policy.py`, `tests/lib/document_governance/test_provenance_policy.py`

**Interfaces:**

- Consumes: nothing from earlier tasks.
- Produces: `MODES = ("check-public", "check-contract", "check-promoted", "check-recovery")`, a four-element tuple every later task may assume.

- [ ] **Step 1: Record every consumer of every mode, before deleting anything**

A mode has three possible consumers and all three are searched. An earlier
version of this step read only the first two, reported three reachable modes,
and authorised deleting three that a scheduled workflow invokes. A partial
search cannot prove absence.

```bash
echo "=== suite registry ==="
grep -n "check-document-corpus-lifecycle" scripts/lib/document_governance/suite_registry.py
echo "=== workflow contract leaves ==="
python3 - <<'PY'
import re, pathlib
t = pathlib.Path(".github/workflow-contract.yml").read_text()
for g, e, a in re.findall(
    r'"gate_id": "([^"]+)",\s*\n\s*"kind": "leaf",\s*\n\s*"entrypoint": "([^"]+)",\s*\n\s*"argv": \[([^\]]*)\]', t
):
    if "corpus-lifecycle" in e:
        print(g, "->", " ".join(re.findall(r'"([^"]+)"', a)))
PY
echo "=== workflow run: lines ==="
grep -rn "check-document-corpus-lifecycle.py" .github/workflows/
echo "=== every other caller in the repository ==="
grep -rn "check-document-corpus-lifecycle.py" --include='*.sh' --include='*.py' --include='*.yml' --include='*.yaml' . \
  | grep -vE "^\./(\.git|graphify-out|docs)/"
```

Expected at the time of writing: `check-public` from the suite registry,
`check-contract` and `check-promoted` from the workflow contract, and
`check-contract`, `check-promoted`, `check-impacted`, `report-full`,
`report-duplicates` from `.github/workflows/document-corpus-lifecycle.yml`.
Six distinct modes. Write every line of output into the Task.

If a mode appears that this step does not list, stop and reconcile before
deleting it. `main` at the time of writing has exactly these; anything else is
new information.

- [ ] **Step 2: Write the failing test for the reduced tuple**

In `tests/validation/test_document_corpus_lifecycle.py`, replace the body of
`test_modes_are_the_exact_fixed_tuple`:

```python
    def test_modes_are_the_exact_fixed_tuple(self) -> None:
        """Four modes, each reachable from a registered gate.

        Eighteen modes existed and three were registered. `check-recovery` is
        kept and registered because re-proving that every tombstone's
        `commit:path` resolves to a regular Git blob is a real guarantee; the
        other fourteen had no consumer at all.
        """

        self.assertEqual(
            ("check-public", "check-contract", "check-promoted", "check-recovery"),
            lifecycle.MODES,
        )
```

- [ ] **Step 3: Run it and confirm it fails**

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle.PublicContractTests.test_modes_are_the_exact_fixed_tuple
```

Expected: FAIL, an 18-tuple against the 4-tuple.

- [ ] **Step 4: Retire the three non-gating workflow steps**

`.github/workflows/document-corpus-lifecycle.yml` invokes `check-impacted`,
`report-full`, and `report-duplicates` on a weekly schedule. None of them
gates: the two reports print debt into a log with no artifact upload and no
failure condition, and `check-impacted --base-ref HEAD~1` on a scheduled run
compares the tip against its parent, which is not what the week changed.
Delete those three steps. Keep `Checkout repository`, `Set up Python`,
`Install repository contract Python dependencies`, `Check lifecycle contract`,
and `Check promoted lifecycle waves`.

`.github/workflows/**` is a protected surface under
`docs/00.agent-governance/policies/approval-boundaries.md:49`. The operator
approved this specific retirement; do not extend the edit beyond those three
steps.

```bash
python3 scripts/validation/check-github-workflow-contract.py
```

Expected: exit 0. The contract pins the workflow's name, triggers, permissions,
jobs, and timeout, none of which this edit touches.

- [ ] **Step 5: Reduce `MODES` and delete the unreachable mode bodies**

Replace lines 96 to 115 of `scripts/validation/check-document-corpus-lifecycle.py`:

```python
MODES = (
    "check-public",
    "check-contract",
    "check-promoted",
    "check-recovery",
)
```

Then delete every `if args.mode == "<removed>"` branch and every helper reached
only from one. After each deletion run
`python3 -c "import ast,pathlib; ast.parse(pathlib.Path('scripts/validation/check-document-corpus-lifecycle.py').read_text())"`
so a broken parse is caught immediately rather than at the end.

- [ ] **Step 6: Delete `provenance_policy.py` and its test**

```bash
git rm scripts/lib/document_governance/provenance_policy.py tests/lib/document_governance/test_provenance_policy.py
grep -rn "provenance_policy" scripts tests .github scripts/manifest.yaml
```

Expected: the only remaining hit is the `check-recovery` call site in
`check-document-corpus-lifecycle.py` around line 6054. Delete that line and the
`policy_findings` it feeds; `check-recovery` keeps `recovery_findings`, which is
the tuple-to-blob proof the mode exists for.

- [ ] **Step 7: Remove the manifest and suite rows for the deleted module**

```bash
python3 - <<'PY'
import re, pathlib
p = pathlib.Path("scripts/manifest.yaml")
t = p.read_text(encoding="utf-8")
pattern = re.compile(r"^- path: scripts/lib/document_governance/provenance_policy\.py\n(?:  .*\n|  - .*\n)*", re.M)
t, n = pattern.subn("", t)
assert n == 1, n
p.write_text(t, encoding="utf-8")
print("manifest rows removed:", n)
PY
grep -n "provenance_policy" scripts/lib/document_governance/suite_registry.py scripts/validation/ci_gate_runner.py .github/workflow-contract.yml
```

Delete every line the `grep` prints.

- [ ] **Step 8: Register `check-recovery` as a gate leaf**

In `.github/workflow-contract.yml`, copy the `leaf.local-document-corpus-promoted`
block and change exactly two fields:

```json
    {
      "gate_id": "leaf.local-document-corpus-recovery",
      "kind": "leaf",
      "entrypoint": "scripts/validation/check-document-corpus-lifecycle.py",
      "argv": [
        "--mode",
        "check-recovery"
      ],
```

Leave `cwd`, `allowed_env_keys`, `timeout_minutes`, `profiles`, and `suite_key`
identical to the block you copied.

- [ ] **Step 9: Repoint the three mode matrices**

The matrices at lines 4463, 4500, and 4634 exclude `check-public` and
`check-recovery` and assert the rest. With four modes the remainder is
`check-contract` and `check-promoted`. Rename each test from
`test_all_sixteen_modes_*` to `test_every_shaped_mode_*` and delete the rows for
removed modes. The name carried a count, which SPEC-0155 recorded as the
failure mode that made `test_all_188_preservation_decisions_...` need renaming.

- [ ] **Step 10: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle 2>&1 | grep -E "^(Ran |OK|FAILED)"
for m in check-public check-contract check-promoted check-recovery; do
  PYTHONPATH=. python3 scripts/validation/check-document-corpus-lifecycle.py --mode "$m" >/dev/null 2>&1
  echo "$m exit=$?"
done
PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
```

Expected: `OK`, four `exit=0`, `PASS`.

- [ ] **Step 11: Commit**

```bash
git add -A
git commit -m "refactor(validation): Reduce the corpus lifecycle to its four reachable modes"
```

---

### Task 2: Derive the census counts

**Files:**

- Modify: `scripts/lib/document_governance/archive.py` — `TASK10_RECOVERY_REFERENCE_COUNT` at line 797 and its check at 810
- Modify: `tests/lib/document_governance/test_archive.py` — the tombstone and recovery-row pins
- Modify: `tests/validation/test_document_corpus_lifecycle.py` — `tombstones=`, `recovery_rows=`, `decisions=` string assertions

**Interfaces:**

- Consumes: Task 1's four-mode tuple, because `check-recovery` prints the counts these tests read.
- Produces: no literal count of tombstones, recovery rows, or decisions anywhere under `scripts/` or `tests/`.

- [ ] **Step 1: Write the invariant that proves the pins are gone**

Add to `tests/lib/document_governance/test_archive.py`:

```python
    def test_no_census_literal_pins_archive_content(self) -> None:
        """A count that describes repository content is computed from it.

        Authoring one tombstone during SPEC-0157's design broke eleven
        hand-maintained counts, one of them encoded in a test's name. Each had
        to be found and advanced by hand, and finding them was the expensive
        part.
        """

        sources = (
            pathlib.Path("scripts/lib/document_governance/archive.py"),
            pathlib.Path("tests/lib/document_governance/test_archive.py"),
            pathlib.Path("tests/validation/test_document_corpus_lifecycle.py"),
        )
        offenders = []
        for source in sources:
            text = (ROOT / source).read_text(encoding="utf-8")
            for pattern in (
                r"tombstones\s*=\s*\d+",
                r"recovery_rows\s*=\s*\d+",
                r"decisions\s*=\s*\d+",
                r"TASK10_RECOVERY_REFERENCE_COUNT\s*=\s*\d+",
            ):
                offenders.extend(
                    f"{source}:{match}" for match in re.findall(pattern, text)
                )
        self.assertEqual([], offenders)
```

- [ ] **Step 2: Run it and confirm it fails**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_no_census_literal_pins_archive_content
```

Expected: FAIL listing the four literals.

- [ ] **Step 3: Derive the constant in `archive.py`**

Replace `TASK10_RECOVERY_REFERENCE_COUNT = 277` and the check that reads it:

```python
def _expected_recovery_reference_count(root: pathlib.Path) -> int:
    """Legacy change deletions plus one row per tombstone, counted from both.

    This replaced a frozen literal that every legitimate tombstone broke, along
    with three test literals that moved with it.
    """

    change_rows = sum(
        1
        for row in task10_rows(root)
        if row.get("action") == "delete"
        and str(row.get("source_path", "")).startswith("docs/98.archive/changes/")
    )
    return change_rows + len(load_archive(root / "docs/98.archive").tombstones)
```

In `load_task10_recovery_references`, replace the constant comparison:

```python
    expected = _expected_recovery_reference_count(root)
    if len(references) != expected:
        raise ValueError(
            f"Task 10 must expose exactly {expected} artifact recovery tuples"
        )
```

The check still fails closed: it now catches a reference list that disagrees
with the ledger and the archive, which is the real invariant, rather than
disagreeing with a number someone typed.

- [ ] **Step 4: Replace the three test literals with relations**

In `tests/validation/test_document_corpus_lifecycle.py`,
`test_check_recovery_mode_uses_minimal_archive_authority` asserts
`tombstones=43`, `recovery_rows=277`, and `decisions=189` as substrings.
Replace them:

```python
        inventory = archive_authority.load_archive(ROOT / "docs/98.archive")
        rows = archive_authority.load_task10_recovery_references(ROOT)
        decisions = archive_authority.load_task10_preservation_decisions(ROOT)
        self.assertIn(f"tombstones={len(inventory.tombstones)}", result.stdout)
        self.assertIn(f"recovery_rows={len(rows)}", result.stdout)
        self.assertIn(f"decisions={len(decisions)}", result.stdout)
```

In `tests/lib/document_governance/test_archive.py`, replace
`self.assertEqual(43, len(inventory.tombstones))` and
`self.assertEqual(277, len(rows))` with the relation each was approximating:

```python
        self.assertEqual(
            len(inventory.tombstones),
            sum(1 for item in rows if item.commit),
        )
```

- [ ] **Step 5: Verify, including that a new tombstone changes nothing**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle 2>&1 | grep -E "^(Ran |OK|FAILED)"
cp docs/98.archive/tombstones/90.references/0158-agentic-research-pack-refresh.md /tmp/probe.md
sed -e 's/tombstone-0158/tombstone-0159/' -e 's/^# .*/# Probe Tombstone/' /tmp/probe.md \
  > docs/98.archive/tombstones/90.references/0159-probe.md
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive 2>&1 | grep -E "^(Ran |OK|FAILED)"
rm docs/98.archive/tombstones/90.references/0159-probe.md
```

Expected: `OK` before the probe, `OK` with the probe present, `OK` after removal.
The middle run is the point: it is the check that the census is derived. Remove
the probe before committing.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor(archive): Derive the recovery census instead of pinning it"
```

---

### Task 3: Create the library packages

**Files:**

- Create: `scripts/lib/gate/__init__.py`, `scripts/lib/agent_eval/__init__.py`, `scripts/lib/supply_chain/__init__.py`, `scripts/lib/target_surface/__init__.py`
- Move: `ci_gate_contract.py` (1,452), `ci_gate_adapters.py` (996), `github_workflow_contract.py` (2,818) into `scripts/lib/gate/`
- Move: `agent_output_eval.py` (1,944), `audit_criterion_contract.py` (352) into `scripts/lib/agent_eval/`
- Move: `grype_db_seed.py` (731) into `scripts/lib/supply_chain/`
- Move: `target_surface_contract.py` (615), `target_surface_delta_contract.py` (495) into `scripts/lib/target_surface/`
- Move: `agent_governance_contract.py` (1,016) into `scripts/lib/agent_governance/`
- Modify: `scripts/manifest.yaml`, `scripts/lib/document_governance/suite_registry.py`, `scripts/validation/ci_gate_runner.py`, `.github/workflow-contract.yml`

**Interfaces:**

- Consumes: nothing from Tasks 1 and 2; this task is independent of them and is sequenced after only so the moved files are already smaller.
- Produces: import paths `scripts.lib.gate.*`, `scripts.lib.agent_eval.*`, `scripts.lib.supply_chain.*`, `scripts.lib.target_surface.*`, `scripts.lib.agent_governance.*`. Every later task uses these.

- [ ] **Step 1: Write the ownership invariant first**

Create `tests/lib/test_surface_ownership.py`:

```python
from __future__ import annotations

import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENTRYPOINT_DIRS = ("validation", "gate", "security", "operations", "knowledge", "hooks")


def _defines_entrypoint(path: pathlib.Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
        ):
            return True
    return False


class SurfaceOwnershipTests(unittest.TestCase):
    """A directory states what its files are, and no constant restates it."""

    def test_no_library_defines_a_command_entrypoint(self) -> None:
        offenders = [
            str(path.relative_to(ROOT))
            for path in (ROOT / "scripts/lib").rglob("*.py")
            if _defines_entrypoint(path)
        ]
        self.assertEqual([], offenders)

    def test_the_non_standalone_list_is_gone(self) -> None:
        from scripts.lib.document_governance import suite_registry

        self.assertFalse(hasattr(suite_registry, "NON_STANDALONE_VALIDATOR_PATHS"))
```

- [ ] **Step 2: Run it and confirm both fail**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
```

Expected: FAIL on both. The first lists library modules that still define
`if __name__ == "__main__"`; the second reports the constant still present.

- [ ] **Step 3: Move the files with `git mv`, one package per command**

```bash
mkdir -p scripts/lib/gate scripts/lib/agent_eval scripts/lib/supply_chain scripts/lib/target_surface scripts/lib/agent_governance
for d in gate agent_eval supply_chain target_surface agent_governance; do
  printf '"""%s domain modules."""\n' "$d" > "scripts/lib/$d/__init__.py"
done
git mv scripts/validation/ci_gate_contract.py scripts/validation/ci_gate_adapters.py scripts/validation/github_workflow_contract.py scripts/lib/gate/
git mv scripts/validation/agent_output_eval.py scripts/validation/audit_criterion_contract.py scripts/lib/agent_eval/
git mv scripts/validation/grype_db_seed.py scripts/lib/supply_chain/
git mv scripts/validation/target_surface_contract.py scripts/validation/target_surface_delta_contract.py scripts/lib/target_surface/
git mv scripts/validation/agent_governance_contract.py scripts/lib/agent_governance/
```

- [ ] **Step 4: Rewrite every import**

```bash
python3 - <<'PY'
import pathlib, re
moves = {
    "ci_gate_contract": "gate", "ci_gate_adapters": "gate",
    "github_workflow_contract": "gate", "agent_output_eval": "agent_eval",
    "audit_criterion_contract": "agent_eval", "grype_db_seed": "supply_chain",
    "target_surface_contract": "target_surface",
    "target_surface_delta_contract": "target_surface",
    "agent_governance_contract": "agent_governance",
}
changed = 0
for path in list(pathlib.Path("scripts").rglob("*.py")) + list(pathlib.Path("tests").rglob("*.py")):
    text = original = path.read_text(encoding="utf-8")
    for module, package in moves.items():
        text = re.sub(rf"\bscripts\.validation\.{module}\b", f"scripts.lib.{package}.{module}", text)
        text = re.sub(rf"\bscripts/validation/{module}\.py\b", f"scripts/lib/{package}/{module}.py", text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed += 1
print("files rewritten:", changed)
PY
grep -rn "scripts/validation/\(ci_gate_contract\|ci_gate_adapters\|github_workflow_contract\|agent_output_eval\|audit_criterion_contract\|grype_db_seed\|target_surface_contract\|target_surface_delta_contract\|agent_governance_contract\)" scripts tests .github || echo "no stale path reference"
```

- [ ] **Step 5: Rewrite the registrations**

Apply the same substitution to `scripts/manifest.yaml`,
`scripts/lib/document_governance/suite_registry.py`, and
`.github/workflow-contract.yml`:

```bash
python3 - <<'PY'
import pathlib
moves = {
    "ci_gate_contract": "gate", "ci_gate_adapters": "gate",
    "github_workflow_contract": "gate", "agent_output_eval": "agent_eval",
    "audit_criterion_contract": "agent_eval", "grype_db_seed": "supply_chain",
    "target_surface_contract": "target_surface",
    "target_surface_delta_contract": "target_surface",
    "agent_governance_contract": "agent_governance",
}
for name in ("scripts/manifest.yaml", "scripts/lib/document_governance/suite_registry.py", ".github/workflow-contract.yml"):
    path = pathlib.Path(name)
    text = path.read_text(encoding="utf-8")
    for module, package in moves.items():
        text = text.replace(f"scripts/validation/{module}.py", f"scripts/lib/{package}/{module}.py")
    path.write_text(text, encoding="utf-8")
    print("rewritten:", name)
PY
```

- [ ] **Step 6: Delete `NON_STANDALONE_VALIDATOR_PATHS` and derive it**

Every path it listed now lives under `scripts/lib/`. Replace each read of the
constant with the directory test:

```python
def _is_standalone(path: PurePosixPath) -> bool:
    """A library is not standalone. The directory says so; no list restates it."""

    return not path.as_posix().startswith("scripts/lib/")
```

Then delete the constant. Run
`grep -rn "NON_STANDALONE_VALIDATOR_PATHS" scripts tests` and expect no output.

- [ ] **Step 7: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-task3.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task3.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task3.txt
```

Expected: `OK`, `PASS`, and `FULL exit=0`. Read the verdict from the `FULL exit=`
line, never from `tail -1`; a module under test prints to stdout after its own
summary.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "refactor(scripts): Give each domain a library package and drop the standalone list"
```

---

### Task 4: Mirror the responsibility structure into `tests/`

**Files:**

- Create: `tests/gate/`, `tests/agent_eval/`, `tests/supply_chain/`, `tests/target_surface/`, `tests/agent_governance/`
- Move: the eleven test modules named in Step 2
- Delete: `tests/docs/README.md`, `tests/qa/README.md`, `tests/setup/README.md` and their directories
- Modify: `scripts/validation/ci_gate_runner.py`, `.github/workflow-contract.yml`, `scripts/manifest.yaml`, `tests/README.md`

**Interfaces:**

- Consumes: Task 3's `scripts/lib/<domain>/` packages.
- Produces: test module paths `tests.gate.*`, `tests.agent_eval.*`, `tests.supply_chain.*`, `tests.target_surface.*`, `tests.agent_governance.*`.

- [ ] **Step 1: Write the mirror invariant**

Add to `tests/lib/test_surface_ownership.py`:

```python
    def test_every_library_package_has_a_test_directory(self) -> None:
        packages = {
            path.name
            for path in (ROOT / "scripts/lib").iterdir()
            if path.is_dir() and not path.name.startswith("__")
        }
        missing = sorted(
            name for name in packages if not (ROOT / "tests" / name).is_dir()
        )
        self.assertEqual([], missing)

    def test_no_placeholder_test_directory_remains(self) -> None:
        for name in ("docs", "qa", "setup"):
            self.assertFalse(
                (ROOT / "tests" / name).exists(),
                f"tests/{name} described a structure that was never built",
            )
```

- [ ] **Step 2: Run it, then move the modules**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership 2>&1 | grep -E "^(Ran |OK|FAILED)"
mkdir -p tests/gate tests/agent_eval tests/supply_chain tests/target_surface tests/agent_governance
git mv tests/validation/test_ci_gate_contract.py tests/validation/test_ci_gate_adapters.py tests/validation/test_ci_gate_runner.py tests/validation/test_github_workflow_contract.py tests/gate/
git mv tests/validation/test_agent_output_eval_fixtures.py tests/validation/test_audit_criterion_contract.py tests/agent_eval/
git mv tests/validation/test_grype_db_seed.py tests/validation/test_supply_chain_policy.py tests/supply_chain/
git mv tests/validation/test_target_surface_contracts.py tests/validation/test_target_surface_delta_contracts.py tests/target_surface/
git mv tests/validation/test_agent_governance_contract.py tests/validation/test_agent_governance_ci_routing.py tests/agent_governance/
git rm -r tests/docs tests/qa tests/setup
```

Expected before the moves: FAIL on both new tests.

- [ ] **Step 3: Rewrite the module names in the gate wiring**

```bash
python3 - <<'PY'
import pathlib
moves = {
    "tests.validation.test_ci_gate_contract": "tests.gate.test_ci_gate_contract",
    "tests.validation.test_ci_gate_adapters": "tests.gate.test_ci_gate_adapters",
    "tests.validation.test_ci_gate_runner": "tests.gate.test_ci_gate_runner",
    "tests.validation.test_github_workflow_contract": "tests.gate.test_github_workflow_contract",
    "tests.validation.test_agent_output_eval_fixtures": "tests.agent_eval.test_agent_output_eval_fixtures",
    "tests.validation.test_audit_criterion_contract": "tests.agent_eval.test_audit_criterion_contract",
    "tests.validation.test_grype_db_seed": "tests.supply_chain.test_grype_db_seed",
    "tests.validation.test_supply_chain_policy": "tests.supply_chain.test_supply_chain_policy",
    "tests.validation.test_target_surface_contracts": "tests.target_surface.test_target_surface_contracts",
    "tests.validation.test_target_surface_delta_contracts": "tests.target_surface.test_target_surface_delta_contracts",
    "tests.validation.test_agent_governance_contract": "tests.agent_governance.test_agent_governance_contract",
    "tests.validation.test_agent_governance_ci_routing": "tests.agent_governance.test_agent_governance_ci_routing",
}
for name in ("scripts/validation/ci_gate_runner.py", ".github/workflow-contract.yml", "scripts/manifest.yaml"):
    path = pathlib.Path(name)
    text = path.read_text(encoding="utf-8")
    for old, new in moves.items():
        text = text.replace(old, new)
        text = text.replace(old.replace(".", "/") + ".py", new.replace(".", "/") + ".py")
    path.write_text(text, encoding="utf-8")
    print("rewritten:", name)
PY
```

- [ ] **Step 4: Correct `tests/README.md`'s Structure block**

Replace the fenced block with the directories that now exist:

```text
tests/
├── README.md          # This file
├── fixtures/          # 검증기 입력 fixture
├── lib/               # scripts/lib/document_governance/ 대응
├── validation/        # scripts/validation/ 진입점 테스트
├── gate/              # scripts/lib/gate/ 대응
├── agent_eval/        # scripts/lib/agent_eval/ 대응
├── supply_chain/      # scripts/lib/supply_chain/ 대응
├── target_surface/    # scripts/lib/target_surface/ 대응
└── agent_governance/  # scripts/lib/agent_governance/ 대응
```

- [ ] **Step 5: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-task4.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task4.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task4.txt
```

Expected: `OK`, `PASS`, `FULL exit=0`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor(tests): Mirror the library packages and drop the placeholder directories"
```

---

### Task 5: Register every test module and repair the eight that fail

**Files:**

- Modify: `scripts/validation/ci_gate_runner.py`, `.github/workflow-contract.yml`
- Modify or delete: the eight failing modules named below
- Delete: `tests/validation/test_agentic_audit_semantic_freshness.py` if its fixture cannot be rebuilt from the live corpus

**Interfaces:**

- Consumes: Task 4's module paths.
- Produces: the set of test modules on disk equals the set the full gate runs.

- [ ] **Step 1: Write the coverage invariant**

Add to `tests/lib/test_surface_ownership.py`:

```python
    def test_every_test_module_is_registered_in_a_gate(self) -> None:
        """No module sits on disk unreached. Nineteen did, and eight of those
        were failing, including one whose thirty-three tests all failed because
        their fixture copied a document out of a deleted Spec Package.
        """

        import re

        registered: set[str] = set()
        for source in (
            ROOT / "scripts/validation/ci_gate_runner.py",
            ROOT / ".github/workflow-contract.yml",
        ):
            registered |= set(
                re.findall(r'"(tests\.[a-z0-9_.]+)"', source.read_text(encoding="utf-8"))
            )
        on_disk = {
            str(path.relative_to(ROOT).with_suffix("")).replace("/", ".")
            for path in (ROOT / "tests").rglob("test_*.py")
        }
        self.assertEqual(set(), on_disk - registered)
```

- [ ] **Step 2: Run it and record the gap**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership.SurfaceOwnershipTests.test_every_test_module_is_registered_in_a_gate
```

Expected: FAIL listing the unregistered modules. Write the list into the Task.

- [ ] **Step 3: Measure each unregistered module before registering it**

```bash
for m in $(PYTHONPATH=. python3 - <<'PY'
import re, pathlib
ROOT = pathlib.Path(".")
registered = set()
for source in ("scripts/validation/ci_gate_runner.py", ".github/workflow-contract.yml"):
    registered |= set(re.findall(r'"(tests\.[a-z0-9_.]+)"', pathlib.Path(source).read_text()))
for path in ROOT.joinpath("tests").rglob("test_*.py"):
    name = str(path.with_suffix("")).replace("/", ".")
    if name not in registered:
        print(name)
PY
); do
  r=$(PYTHONPATH=. timeout 300 python3 -m unittest "$m" 2>&1 | grep -E "^(Ran [0-9]+ tests|OK|OK \(|FAILED)" | tr '\n' ' ')
  printf "%-56s %s\n" "$m" "${r:-TIMEOUT}"
done
```

Record every line. A module that fails is diagnosed and dispositioned before it
is registered; registering a red module turns the gate red for a reason that is
not this task's change.

- [ ] **Step 4: Disposition `test_agentic_audit_semantic_freshness`**

Its `setUp` copies `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0010-archive.md`,
and SPEC-0153 was deleted; `docs/98.archive/migrations/0003` is its record. All
thirty-three of its tests error on that one missing file.

```bash
sed -n '130,150p' tests/validation/test_agentic_audit_semantic_freshness.py
```

If the fixture list can be rebuilt from documents that exist, rebuild it and
keep the module. If it cannot, delete the module and its manifest row, and
record in the Task that a test bound to a deleted Spec Package has no subject.

- [ ] **Step 5: Repair the remaining seven, one commit each**

For each of `test_supply_chain_policy`, `test_sample_service_delivery_rehearsal`,
`test_agent_governance_contract`, `test_script_manifest`,
`test_compose_core_readiness`, and any module Step 3 newly reports red: read the
failure, name the root cause in the commit message, and fix the production
defect rather than the assertion. Where the assertion itself is wrong, say so
and change it, as SPEC-0155 did for `test_generate_llm_wiki`'s stale 43-script
pin.

- [ ] **Step 6: Register the now-green modules**

In `scripts/validation/ci_gate_runner.py`, add each module name to the tuple
that already lists `tests.lib.document_governance.*` and the validation modules,
keeping the list alphabetically sorted so a later addition is a one-line diff.

- [ ] **Step 7: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-task5.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task5.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task5.txt
```

Expected: `OK` and `FULL exit=0`. The gate will now run noticeably longer; that
is the cost of the modules no longer being invisible.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "test(gate): Register every test module and repair the ones nothing ran"
```

---

### Task 6: Retire the resurrected taxonomy from the test harness

**Files:**

- Modify: `tests/validation/test_document_metadata.py` — `PROFILES` at line 30, `HISTORICAL_COMMIT`, and the 43 references that read through them
- Modify: `tests/lib/document_governance/test_links.py`, `test_spec_packages.py`, `test_operations_catalog.py`
- Create: `tests/fixtures/document_metadata/profiles.yaml` and any other fixture the removed reads need

**Interfaces:**

- Consumes: Task 5's registration, so a regression here is caught rather than silent.
- Produces: no caller of `HistoricalDocument` under `tests/`.

- [ ] **Step 1: Write the invariant**

Add to `tests/lib/test_surface_ownership.py`:

```python
    def test_no_test_resurrects_a_deleted_document(self) -> None:
        """A fixture states what the repository is now.

        Five modules read deleted documents out of pinned commits, and all seven
        resurrected paths are absent from the working tree along with the
        `docs/99.templates/support/` directory that held them. That is why
        `load_transition_overrides` required a Task path shape this repository
        has zero of: the validator was matching the harness, not the corpus.
        """

        offenders = [
            str(path.relative_to(ROOT))
            for path in (ROOT / "tests").rglob("*.py")
            if "HistoricalDocument(" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual([], offenders)
```

- [ ] **Step 2: Run it and confirm it fails with five modules**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership.SurfaceOwnershipTests.test_no_test_resurrects_a_deleted_document
```

- [ ] **Step 3: Commit the resurrected profile blob as a real fixture**

```bash
mkdir -p tests/fixtures/document_metadata
git show "$(python3 -c "
import re, pathlib
t = pathlib.Path('tests/validation/test_document_metadata.py').read_text()
print(re.search(r'HISTORICAL_COMMIT = \"([0-9a-f]{40})\"', t).group(1))
")":docs/99.templates/support/document-metadata-profiles.yaml \
  > tests/fixtures/document_metadata/profiles.yaml
git add tests/fixtures/document_metadata/profiles.yaml
```

The blob is now a tracked fixture with a name that says what it is. Nothing is
read out of Git at test time, and the file no longer disappears when history is
rewritten or a shallow clone is used.

- [ ] **Step 4: Repoint `PROFILES` and delete the resurrection helper**

```python
PROFILES = ROOT / "tests/fixtures/document_metadata/profiles.yaml"
```

Delete `_materialised_profiles` and its `_PROFILES_FILE` global; `run_checker`
passes `PROFILES` directly. Repeat for the other six resurrected paths, giving
each a fixture file under `tests/fixtures/` named for what it holds.

- [ ] **Step 5: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata 2>&1 | grep -E "^(Ran |OK|FAILED)"
grep -rn "HistoricalDocument(" tests || echo "no resurrection under tests/"
```

Expected: `OK`, `OK`, and no output from the `grep`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "test(fixtures): Commit the pinned profile blobs instead of reading them from Git"
```

---

### Task 7: Bound the identity scan by what it needs

**Files:**

- Modify: `scripts/lib/document_governance/identity_history.py` — `MAX_GIT_OUTPUT_BYTES` at line 21, `GIT_HISTORY_QUERIES` at line 33, `collect_issued_identities`
- Modify: `tests/lib/document_governance/test_identity_history.py`

**Interfaces:**

- Consumes: nothing from earlier tasks.
- Produces: `collect_issued_identities(root, refs=("--all",)) -> IssuedIdentities`, unchanged in signature and return type. Only its cost changes.

- [ ] **Step 1: Measure what the scan reads today**

```bash
for d in docs/01.requirements docs/02.architecture docs/03.specs docs/05.operations docs/90.references docs/98.archive; do
  n=$(git log --all -p --format="%H" -- "$d" | wc -c)
  printf "%-24s %12s bytes\n" "$d" "$n"
done
```

Record every number. At SPEC-0155's close `docs/03.specs` was 17.4 MB and
`docs/90.references` 20.6 MB, both past the 16 MiB bound that was then raised to
64 MiB as an explicit stopgap. The scan reads full patch text, so these only
grow, and deleting a large document adds its bytes to the total.

- [ ] **Step 2: Write the failing test**

```python
    def test_identity_scan_does_not_read_patch_text(self) -> None:
        """Cost must not grow with history.

        The scan read each stage directory's complete patch history and grepped
        it for identifiers, so every commit made it more expensive and deleting
        a 2.4 MB document made it more expensive still. Identifiers are in paths
        and in current frontmatter; neither needs a diff.
        """

        source = (
            ROOT / "scripts/lib/document_governance/identity_history.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn('"-p"', source)
        self.assertNotIn('"--patch"', source)
        self.assertNotIn("64 * 1024 * 1024", source)
```

- [ ] **Step 3: Run it and confirm it fails**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_identity_history.IdentityHistoryTests.test_identity_scan_does_not_read_patch_text
```

Expected: FAIL on the patch flag and on the stopgap bound.

- [ ] **Step 4: Read identifiers from paths, not diffs**

Every issued identifier appears in a document path, because the registry's
`path_pattern` binds the number into the filename and the checker already
enforces that binding. Replace the patch scan with a name scan:

```python
def _historical_paths(
    repo: pathlib.Path, prefix: str, refs: tuple[str, ...]
) -> frozenset[str]:
    """Every path that ever existed under one stage, without reading a diff.

    `--name-only` emits paths; `-p` emitted the full patch text of every commit
    that touched the stage, which is why the scan cost grew with history and
    grew again with each deletion.
    """

    output = _run_git(
        repo,
        ("log", *refs, "--name-only", "--format=", "--", prefix),
    )
    return frozenset(
        line
        for line in output.stdout.decode("utf-8", "replace").splitlines()
        if line
    )
```

`collect_issued_identities` then applies the existing `HISTORICAL_ID_PATTERN` to
the path set rather than to patch text, plus the current frontmatter it already
reads through `_read_identity_source`.

- [ ] **Step 5: Restore a bound that is a bound**

```python
# Path listings, not patch text. `docs/90.references` is the largest stage at
# roughly 20 MB of patch text and well under a megabyte of path names, so this
# is a real ceiling rather than the stopgap it replaced.
MAX_GIT_OUTPUT_BYTES = 8 * 1024 * 1024
```

- [ ] **Step 6: Verify the identifier set is unchanged**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_identity_history 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 scripts/validation/check-document-metadata.py --mode check-contracts --history-scope full 2>&1 | tail -2
```

Expected: `OK` and `violations=0`. The second command is the registered gate's
own route, and it is the one that failed at SPEC-0155's close when the bound was
exceeded.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "perf(identity): Scan path names instead of every diff in history"
```

---

### Task 8: Split the two production monoliths

**Files:**

- Create: `scripts/lib/document_governance/metadata/{profile,lifecycle,heading,identity,reference}.py`
- Modify: `scripts/lib/document_governance/metadata_validator.py` (6,774) into a thin re-export
- Create: `scripts/lib/document_governance/lifecycle/{public,contract,promoted,recovery}.py`
- Modify: `scripts/validation/check-document-corpus-lifecycle.py` into an entrypoint

**Interfaces:**

- Consumes: Task 1's four modes, Task 2's derived census, Task 6's fixtures. Splitting before those would divide code that is about to be deleted and would do it without a working safety net.
- Produces: the public names `load_registry`, `build_registry_profiles`, `validate_record`, `validate_repository_contracts`, `load_transition_overrides`, `collect_issued_identities` remain importable from `scripts.lib.document_governance.metadata_validator`, so no caller changes.

- [ ] **Step 1: Record the public surface before moving anything**

```bash
PYTHONPATH=. python3 - <<'PY'
import inspect, sys
sys.path.insert(0, ".")
from scripts.lib.document_governance import metadata_validator as m
names = sorted(n for n in dir(m) if not n.startswith("_"))
print(len(names))
open("/tmp/metadata-surface-before.txt", "w").write("\n".join(names))
PY
```

- [ ] **Step 2: Write the surface-preservation test**

```python
    def test_metadata_validator_public_surface_is_unchanged_by_the_split(self) -> None:
        """The split moves code, never the interface its callers import."""

        from scripts.lib.document_governance import metadata_validator

        expected = set(
            pathlib.Path("/tmp/metadata-surface-before.txt").read_text().split()
        )
        actual = {n for n in dir(metadata_validator) if not n.startswith("_")}
        self.assertEqual(set(), expected - actual)
```

- [ ] **Step 3: Move one responsibility at a time**

For each of profile, lifecycle, heading, identity, reference: cut the functions
that belong to it into the new module, add
`from scripts.lib.document_governance.metadata.<name> import *  # noqa: F401,F403`
to `metadata_validator.py`, and run the surface test plus
`PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata`
before starting the next one. Five separate commits.

- [ ] **Step 4: Split the lifecycle checker the same way**

One module per surviving mode: `public.py`, `contract.py`, `promoted.py`,
`recovery.py`. `check-document-corpus-lifecycle.py` keeps `_parser`,
`_validate_cli_shape`, and a `main` that dispatches on `args.mode`.

- [ ] **Step 5: Verify**

```bash
for f in $(find scripts/lib/document_governance -name '*.py'); do
  n=$(wc -l < "$f"); [ "$n" -gt 800 ] && echo "OVER 800: $n $f"
done
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-task7.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task7.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task7.txt
```

Expected: no `OVER 800` line and `FULL exit=0`.

- [ ] **Step 6: Commit each move separately**

```bash
git add -A
git commit -m "refactor(metadata): Split the validator by responsibility"
```

---

### Task 9: Split the test monoliths and close the Spec Packages

**Files:**

- Split: `tests/validation/test_document_metadata.py` (8,426) and `tests/validation/test_document_corpus_lifecycle.py` (7,022) to match Task 8's modules
- Modify: `scripts/README.md`
- Modify: `docs/03.specs/0154-*/spec.md`, `docs/03.specs/0155-*/spec.md`, `docs/03.specs/0157-*/spec.md`

**Interfaces:**

- Consumes: Task 8's module boundaries.
- Produces: nothing later depends on this task.

- [ ] **Step 1: Record the test count before splitting**

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata 2>&1 | grep -E "^Ran "
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle 2>&1 | grep -E "^Ran "
```

Write both numbers into the Task. The split preserves them; a lost test is a
lost assertion, not a tidier file.

- [ ] **Step 2: Split into one module per production module**

`tests/lib/document_governance/metadata/test_{profile,lifecycle,heading,identity,reference}.py`
and `tests/validation/lifecycle/test_{public,contract,promoted,recovery}.py`.
Move whole `TestCase` classes; do not re-author assertions.

- [ ] **Step 3: Confirm the count is preserved**

```bash
PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance/metadata 2>&1 | grep -E "^Ran "
PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle 2>&1 | grep -E "^Ran "
```

The two sums must equal the two numbers from Step 1.

- [ ] **Step 4: Update `scripts/README.md` to the new structure**

Replace its script table with one row per entrypoint under the new directories,
and add a short section stating the ownership rule: `lib/<domain>/` holds
importable modules and defines no entrypoint; `<surface>/` holds entrypoints and
implements no domain logic; `tests/<domain>/` mirrors `lib/<domain>/`.

- [ ] **Step 5: Complete the three Spec Packages**

SPEC-0154 and SPEC-0155 are `active` at `main` and complete with a single legal
hop. SPEC-0157 goes `draft` to `active` in its first commit and to `completed`
here only if it is `active` at the merge base; otherwise it stays `active` and
completes in the change after this branch merges, which is what SPEC-0155 Task 8
measured.

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
```

Expected: `violations=0`. If it reports `draft -> completed`, the endpoint rule
is refusing the hop and the status stays `active`.

- [ ] **Step 6: Final verification**

```bash
git add -A
python3 scripts/knowledge/generate-llm-wiki.py --write
git add -A
python3 scripts/knowledge/generate-llm-wiki.py
python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-final.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-final.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-final.txt
find scripts tests -name '*.py' -exec wc -l {} + | awk '$1>800 && $2!="total"'
```

Expected: both wiki outputs fresh, `FULL exit=0`, and no file over 800 lines.
Regenerate after the last document is authored, not before; the gate checks
freshness and a Task that writes its own record after regenerating leaves it red.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "docs(spec): Close the script surface ownership convergence"
```

## Risk and Rollback

| Risk | Guardrail | Rollback |
| :--- | :--- | :--- |
| A mode is deleted that a gate reaches | Step 1 of Task 1 prints the registered modes before any deletion | `git revert` the Task 1 commit |
| A move breaks an import that no test covers | Task 3 Step 4 greps for stale paths and the full gate runs at the task boundary | `git revert`; `git mv` is reversible in one commit |
| Registering a red module makes the gate red for an unrelated reason | Task 5 measures every module before registering it and repairs first | Unregister the single module; its repair commit stands alone |
| A fixture rebuilt from Git changes what a test asserts | Task 6 commits the exact blob rather than re-authoring it | `git revert`; the blob is byte-identical to what the test read before |
| A split loses a test | Task 8 Step 1 records the counts and Step 3 compares the sums | `git revert` the single split commit |
| A count is repinned instead of derived | Task 2's probe writes a tombstone and re-runs; a derived census is unmoved | `git revert` the Task 2 commit |

## Verification

Every task ends with `run-ci-gate.py --profile full` reporting `FULL exit=0`,
read from that line and never from `tail -1`. The final state additionally
satisfies:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-script-manifest.py
bash scripts/operations/sync-provider-surfaces.sh --check && git diff --exit-code
find scripts tests -name '*.py' -exec wc -l {} + | awk '$1>800 && $2!="total"'
grep -rn "HistoricalDocument(" tests
grep -rn "NON_STANDALONE_VALIDATOR_PATHS" scripts tests
```

Expected: `violations=0`, `failures=0`, `PASS`, `drift=0` with a clean diff, and
no output from the last three.

## Rulings

SPEC-0155's plan rulings 1 to 11 carry forward. Four apply so directly that they
are restated:

1. **The merge base is computed, never pinned.** `$(git merge-base main HEAD)`.
   A pinned base hid six violations across an entire Spec Package.
2. **A plan step is measured before it is executed.** SPEC-0155's plan named
   1,499 dead lines; two of the three modules ran on every gate. A plan is
   evidence of intent, not of fact.
3. **Absence is never inferred from a passing run or a truncated search.** A
   check that reports nothing passed; it was not skipped. A `grep` piped through
   `head` proves nothing about what it did not print.
4. **Generated outputs are regenerated after the last document is authored.**
   The gate verifies freshness, so a Task that writes its own record after
   regenerating leaves the gate red.

Two are new to this Spec Package:

5. **A directory states what its files are, and no constant restates it.** The
   ownership rule is enforced by `tests/lib/test_surface_ownership.py`, not by a
   list someone maintains.
6. **A test judges the corpus, never a deleted taxonomy.** Where a past state
   must be asserted, the fixture is committed as a fixture.

## Related Documents

- [Specification](spec.md)
- [Validation surface reduction](../0155-validation-surface-reduction/spec.md)
- [Governance consistency convergence](../0154-governance-consistency-convergence/spec.md)
- [Quality standards](../../00.agent-governance/policies/quality-standards.md)
