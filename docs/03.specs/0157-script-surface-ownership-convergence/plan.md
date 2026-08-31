---
profile_id: plan
status: active
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
then decompose the four measured multi-responsibility files along their named
domain and mode boundaries.

Reduction precedes restructuring. Moving unreachable code into a cleaner
directory produces a tidier version of the same excess.

## Dependencies

- SPEC-0155 is completed and merged. Its plan rulings 1 to 11 carry forward and are restated below.
- `main` is the merge base for every `--base-ref` computation. It is computed, never pinned.
- The changed-document Gate compares lifecycle endpoints at the merge base. If
  `main` still contains SPEC-0157 as `draft`, this branch may finish with the
  Spec `active`, but it must not claim `completed`. Land the activation and
  implementation first; close the Spec from an updated `main` where its base
  state is already `active`.
- This repository runs `python3 -m unittest`. `pytest` is not installed. Several modules require `PYTHONPATH=.`; the registered gate supplies it.
- `run-ci-gate.py --profile full` takes roughly 12 minutes. Run it at task boundaries, not per step.

## Execution Sequence

### Task 0: Restore an honest execution chain

**Files:**

- Create: `docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md`
- Modify: `docs/03.specs/0157-script-surface-ownership-convergence/spec.md`
- Modify: `docs/03.specs/0157-script-surface-ownership-convergence/plan.md`
- Modify: `docs/03.specs/README.md`

**Interfaces:**

- Consumes: the actual branch commit range and the already-authored Spec and Plan.
- Produces: legal `draft -> active` parents and one current Task before any new
  production mutation.
- Does not produce: a claim that earlier work was approved before it occurred.

- [x] **Step 1: Measure the discovered work**

```bash
git status --short --branch
git log --oneline --no-merges "$(git merge-base main HEAD)"..HEAD
git diff --stat "$(git merge-base main HEAD)"...HEAD
```

Record the exact output in the new Task as discovered branch work. Do not call
the earlier commits approved; approval begins at this recovery boundary.

- [x] **Step 2: Create the current Task and activate both parents**

Create `tasks/tsk-0001-convergence.md` from the registered Task template with
this frontmatter and opening contract:

```markdown
---
profile_id: task
status: active
artifact_id: task-0157-0001
artifact_type: task
parent_ids: [SPEC-0157, plan-0157]
created: 2026-08-31
updated: 2026-08-31
---

# Recover and Complete Script Surface Ownership Convergence

## Objective

Revalidate the implementation discovered on the branch, complete the remaining
approved work, and close SPEC-0157 without asserting retroactive approval.
```

Populate every required Task section. Set `status: active` in `spec.md` and
`plan.md`, add the Tasks link to the Stage 03 index, and leave verification and
review entries explicitly pending until observed.

This activation repairs current truth but does not erase the merge-base rule.
Do not use a transition override to collapse `draft -> active -> completed`
into one branch endpoint.

- [x] **Step 3: Revalidate Tasks 1 through 3**

Run the focused commands already specified at the end of Tasks 1, 2, and 3.
For each passing task, record its actual logical commits and observed result in
the current Task, then mark only its completed checkboxes. A mismatch reopens
that task; it is not explained away as historical.

- [x] **Step 4: Verify the lifecycle recovery**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
```

Expected: `violations=0`, `violations=0`, and `failures=0`.

- [x] **Step 5: Commit**

```bash
git add docs/03.specs/0157-script-surface-ownership-convergence docs/03.specs/README.md
git commit -m "docs(spec): Activate script surface convergence with recovered evidence"
```

---

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

- [x] **Step 1: Record every consumer of every mode, before deleting anything**

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

- [x] **Step 2: Write the failing test for the reduced tuple**

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

- [x] **Step 4: Retire the three non-gating workflow steps**

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

- [x] **Step 5: Reduce `MODES` and delete the unreachable mode bodies**

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

- [x] **Step 6: Delete `provenance_policy.py` and its test**

```bash
git rm scripts/lib/document_governance/provenance_policy.py tests/lib/document_governance/test_provenance_policy.py
grep -rn "provenance_policy" scripts tests .github scripts/manifest.yaml
```

Expected: the only remaining hit is the `check-recovery` call site in
`check-document-corpus-lifecycle.py` around line 6054. Delete that line and the
`policy_findings` it feeds; `check-recovery` keeps `recovery_findings`, which is
the tuple-to-blob proof the mode exists for.

- [x] **Step 7: Remove the manifest and suite rows for the deleted module**

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

- [x] **Step 8: Register `check-recovery` as a gate leaf**

In `.github/workflow-contract.yml`, copy the `leaf.local-document-corpus-promoted`
block and change exactly three fields:

```json
    {
      "gate_id": "leaf.local-document-corpus-recovery",
      "kind": "leaf",
      "entrypoint": "scripts/validation/check-document-corpus-lifecycle.py",
      "argv": [
        "--mode",
        "check-recovery"
      ],
      "suite_key": "local-document-corpus-recovery",
```

Leave `cwd`, `allowed_env_keys`, `timeout_minutes`, and `profiles` identical to
the block you copied. The recovery leaf must have the unique suite key
`local-document-corpus-recovery`: the gate contract requires
`gate_id == leaf.{suite_key}`. Add `leaf.local-document-corpus-recovery` as a
child of the existing `local.document-corpus-lifecycle` aggregate.

- [x] **Step 9: Repoint the three mode matrices**

The matrices at lines 4463, 4500, and 4634 exclude `check-public` and
`check-recovery` and assert the rest. With four modes the remainder is
`check-contract` and `check-promoted`. Rename each test from
`test_all_sixteen_modes_*` to `test_every_shaped_mode_*` and delete the rows for
removed modes. The name carried a count, which SPEC-0155 recorded as the
failure mode that made
`test_all_188_preservation_decisions_are_unique_and_reviewed` need renaming.

- [x] **Step 10: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle 2>&1 | grep -E "^(Ran |OK|FAILED)"
for m in check-public check-contract check-promoted check-recovery; do
  PYTHONPATH=. python3 scripts/validation/check-document-corpus-lifecycle.py --mode "$m" >/dev/null 2>&1
  echo "$m exit=$?"
done
PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
```

Expected: `OK`, four `exit=0`, `PASS`.

Revalidated at `dd665618`: the lifecycle suite, all four modes, and the
GitHub workflow contract are GREEN. The shared manifest bundle remains RED
only for the five Task 3-owned unregistered package markers
(`scripts/lib/{agent_governance,gate,ops,supply_chain,target_surface}/__init__.py`);
do not register or remove them in Task 1.

- [x] **Step 11: Reconcile the discovered commit**

Do not create a duplicate commit while revalidating the already-landed work.
Record the actual logical commit and its focused results in the current Task.
If a failed check reopens this Task, stage only the exact repaired paths named
in that Task evidence, inspect `git diff --cached --name-only`, and commit the
repair separately.

---

### Task 2: Derive the census counts

**Files:**

- Modify: `tests/lib/document_governance/test_archive.py` — targeted guard for the
  current-repository Spec Package coverage test
- Modify: `tests/lib/document_governance/test_spec_packages.py` — derive the
  current package surface from Spec directories

**Interfaces:**

Task 2's archive and lifecycle relations already landed in discovered commits
`dd41a675` and `342863ff`; their focused suites were revalidated GREEN. The
only remaining mismatch directly observed in this Task is the literal current
Spec Package count (`34 != 35`).

- [x] **Step 1: Reproduce the remaining current-repository failure**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
```

Observed: `test_current_repository_has_exact_canonical_spec_surface` failed
with `34 != 35` while the loader and on-disk `spec.md` directories both exposed
the same 35-package set.

- [x] **Step 2: Add and witness the narrow regression guard**

Add a test that parses only `test_current_repository_*` methods in
`test_spec_packages.py` and rejects an integer literal compared with
`len(packages)`. This deliberately does not scan the whole file: fixture tests
legitimately assert their one-package fixture cardinality.

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_no_current_repository_spec_package_cardinality_pin
```

Observed before the repair: the guard failed with
`test_current_repository_has_exact_canonical_spec_surface:34`.

- [x] **Step 3: Derive the current Spec Package surface**

Rename the current-repository test for coverage rather than cardinality and
replace its literal with this set relation:

```python
        expected_paths = {
            path
            for path in (ROOT / "docs/03.specs").iterdir()
            if path.is_dir() and (path / "spec.md").is_file()
        }
        self.assertEqual(expected_paths, {package.path for package in packages})
```

Keep the existing prefix, Stage 04, and legacy-role assertions unchanged.

- [x] **Step 4: Verify the repair and existing derived relations**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
```

Observed: archive (22 tests), lifecycle (116 tests), and Spec Package (16 tests)
all report `OK`.

- [x] **Step 5: Record the repair boundary**

Keep `dd41a675` and `342863ff` as discovered archive/lifecycle evidence; record
the new current-Spec-Package repair separately in the active Task. Neither
record retroactively approves the discovered commits.

---

### Task 3: Reconcile library package ownership

The library move is discovered work, not a new action to repeat. The logical
move commit is `d6b7eafe`; `e23d93f1` is its operations ordering follow-up.
They moved seven Python modules to `scripts/lib/<domain>/` and two shell-only
files to `scripts/lib/ops/`. This Task does not retroactively approve, move, or
recommit that work.

**Files and interfaces:**

- Discovered library modules: `gate/{ci_gate_contract,ci_gate_adapters,github_workflow_contract}.py`, `supply_chain/grype_db_seed.py`, `target_surface/{target_surface_contract,target_surface_delta_contract}.py`, and `agent_governance/agent_governance_contract.py`.
- Discovered operations files: `ops/rehearse-postgres-logical-upgrade.sh` and `ops/validate-harness.sh`.
- Repair only: delete `__init__.py` from `agent_governance`, `gate`, `ops`, `supply_chain`, and `target_surface`; retain `scripts/lib/document_governance/__init__.py`.
- The ownership rule is `scripts/lib/<domain>` importability plus no manifest `execution_contexts`. An `if __name__ == "__main__"` guard alone is irrelevant. The directories are implicit namespace packages; `ops` remains shell-only.

- [x] **Step 1: Measure the discovered-work mismatch**

`check-script-manifest.py` reported exactly these five RED rows before the
repair: `scripts/lib/{agent_governance,gate,ops,supply_chain,target_surface}/__init__.py`, each `manifest-record-missing`. Each marker contained only a
one-line docstring. A complete dependency search found no package attributes,
side effects, exports, or wildcard consumers; module-level imports use the
exact `from scripts.lib.<domain> import module` form.

- [x] **Step 2: Apply the marker repair without changing the manifest**

Delete only those five markers with `apply_patch`; do not add manifest rows or
repeat the discovered moves. Repair commit: `58981986`
`refactor(scripts): Drop redundant package markers`.

- [x] **Step 3: Revalidate the library boundary**

~~~text
namespace_packages=5
python_modules=7
exact_package_imports=7
ops_namespace=PASS
ops_shell_files=2

PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
Ran 3 tests in 0.102s
OK

PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
PASS: script manifest is valid

PYTHONPATH=. python3 scripts/validation/check-github-workflow-contract.py
PASS: GitHub workflow contract (workflows=7, jobs=9, actions=8)
~~~

The moved-library focused suite ran 224 tests and was RED only on the three
subcases of `test_mutable_task_token_evidence_is_statement_bounded` in the
currently unregistered agent-governance test module:
`case='evidence-only-edit'`, `case='new-active-authority'`, and
`case='altered-statement'`. Each failed when `copy2` read the absent SPEC-0153
Task fixture. This is Task 5 measured-unregistered repair work, outside this
package-marker repair.

- [x] **Step 4: Record the full-Gate boundary**

~~~text
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full
Ran 251 tests in 148.982s
FAILED (failures=3, errors=2)
FULL exit=1
~~~

All five full-Gate results are already-registered
`tests.validation.test_document_metadata.ChangedBodyDeficitGitTests` cases,
owned by Task 6 fixed-workspace/recovery-fixture work, not by package markers:

1. Error: `test_registered_operations_catalog_move_uses_migration_0003_body_baseline`
2. Error: `test_registered_operations_profile_transition_holds_the_registry_boundary`
3. Failure: `test_preexisting_target_cannot_borrow_registered_source_baseline`
4. Failure: `test_registered_operations_move_requires_its_exact_source_at_base`
5. Failure: `test_unrelated_operations_readme_does_not_receive_transition_authorization`

No Task 6 production change is authorized here. Packaging/Python review is
APPROVED. The Task review has Spec FAIL and quality CHANGES_REQUESTED solely
for attribution. Round 2 adds the exact parameterized subcase identities and is
pending re-review; SPEC-0157 remains active and is not completed by this Task.

---

### Task 4: Mirror the responsibility structure into `tests/`

**Files:**

- Create as implicit namespace directories: `tests/lib/gate/`,
  `tests/lib/supply_chain/`, `tests/lib/target_surface/`,
  `tests/lib/agent_governance/`, and `tests/lib/ops/`.
- Move exactly the eight measured library-unit tests listed in Step 2.
- Delete with `apply_patch`: `tests/docs/README.md`, `tests/qa/README.md`, and
  `tests/setup/README.md`. The empty directories then disappear; do not leave a
  redirect or Stage 98 tombstone.
- Modify the current machine wiring, ownership documentation, runbook command,
  and live link destinations enumerated in Steps 3 through 5.

**Interfaces:**

- Consumes: Task 3's `scripts/lib/<domain>/` packages.
- Produces: library-unit test module paths under `tests.lib.<domain>.*`.
- Preserves: validation and execution-context tests, including
  `agent_output_eval` and `audit_criterion_contract`, under
  `tests.validation.*`.
- Does not create: `__init__.py` in any new test directory. The test mirror uses
  implicit namespace packages, so every registered moved suite is invoked by
  its exact dotted module name.

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
            name for name in packages if not (ROOT / "tests/lib" / name).is_dir()
        )
        self.assertEqual([], missing)

    def test_no_placeholder_test_directory_remains(self) -> None:
        for name in ("docs", "qa", "setup"):
            self.assertFalse(
                (ROOT / "tests" / name).exists(),
                f"tests/{name} described a structure that was never built",
            )
```

Run the focused ownership test before implementing. It must fail only on the
missing mirror directories and the three placeholder roots.

- [ ] **Step 2: Move exactly the measured primary-owner set**

The preflight primary-owner census is the execution authority for this Task:

| From | To |
| :--- | :--- |
| `tests/validation/test_agent_governance_contract.py` | `tests/lib/agent_governance/test_agent_governance_contract.py` |
| `tests/validation/test_ci_gate_adapters.py` | `tests/lib/gate/test_ci_gate_adapters.py` |
| `tests/validation/test_ci_gate_contract.py` | `tests/lib/gate/test_ci_gate_contract.py` |
| `tests/validation/test_github_workflow_contract.py` | `tests/lib/gate/test_github_workflow_contract.py` |
| `tests/validation/test_grype_db_seed.py` | `tests/lib/supply_chain/test_grype_db_seed.py` |
| `tests/validation/test_postgres_logical_upgrade_rehearsal.py` | `tests/lib/ops/test_postgres_logical_upgrade_rehearsal.py` |
| `tests/validation/test_target_surface_contracts.py` | `tests/lib/target_surface/test_target_surface_contracts.py` |
| `tests/validation/test_target_surface_delta_contracts.py` | `tests/lib/target_surface/test_target_surface_delta_contracts.py` |

Use `git mv` for exactly these eight files. Do not move
`test_validator_entrypoints.py`, `test_agent_output_eval_fixtures.py`, or any
audit/agentic test. Do not add `__init__.py`.

Seven moved modules derive `ROOT` from `Path(__file__).resolve().parents[2]`;
change those to `parents[3]`. `test_ci_gate_adapters.py` has no `ROOT` constant
and needs no depth edit.

- [ ] **Step 3: Replace generated-prefix runner wiring with exact modules**

`ci_gate_runner.py` currently stores bare stems and prepends
`tests.validation`. A generic old-to-new string replacement cannot rewrite that
shape. Replace the generated-prefix block with an exact dotted-module tuple:

```python
**{
    ("run-unittest", module_name, "-v"): _ALL_EXECUTION_CONTEXTS
    for module_name in (
        "tests.validation.test_agent_output_eval_fixtures",
        "tests.lib.gate.test_ci_gate_contract",
        "tests.validation.test_ci_gate_runner",
        "tests.lib.gate.test_ci_gate_adapters",
        "tests.lib.gate.test_github_workflow_contract",
        "tests.validation.test_agent_governance_ci_routing",
        "tests.validation.test_document_corpus_lifecycle",
        "tests.validation.test_document_metadata",
        "tests.validation.test_hook_rules",
        "tests.lib.target_surface.test_target_surface_contracts",
        "tests.lib.target_surface.test_target_surface_delta_contracts",
        "tests.validation.test_compose_baseline_gates",
    )
},
```

Keep the tuple's contract order. In
`tests/validation/test_ci_gate_runner.py`, update the negative PostgreSQL module
name to `tests.lib.ops.test_postgres_logical_upgrade_rehearsal`.

- [ ] **Step 4: Rewire every current machine contract**

Update these six workflow-contract leaves without changing their ownership or
other arguments:

| Gate leaf | Moved module(s) |
| :--- | :--- |
| `leaf.ci-gate-adapter-regressions` | `tests.lib.gate.test_ci_gate_adapters` |
| `leaf.ci-gate-contract-regressions` | `tests.lib.gate.test_ci_gate_contract` |
| `leaf.workflow-contract-regressions` | `tests.lib.gate.test_github_workflow_contract` |
| `leaf.local-target-surface-regressions` | `tests.lib.target_surface.test_target_surface_contracts` |
| `leaf.local-target-delta-regressions` | `tests.lib.target_surface.test_target_surface_delta_contracts` |
| `leaf.supply-chain-fixture-policy` | `tests.lib.ops.test_postgres_logical_upgrade_rehearsal` and `tests.lib.supply_chain.test_grype_db_seed`; preserve its other modules |

Then update the two supply-chain semantic strings in
`scripts/lib/gate/github_workflow_contract.py` and in the moved
`tests/lib/gate/test_github_workflow_contract.py`.

Rewrite every moved test path in `scripts/manifest.yaml`, preserving every row
and sorting each `tests:` list. In particular, the CI runner row's relevant
ordered values are:

```yaml
tests:
- tests/lib/target_surface/test_target_surface_delta_contracts.py
- tests/validation/test_ci_gate_runner.py
- tests/validation/test_validator_entrypoints.py
```

Also update:

- `scripts/validation/check-script-manifest.py`: accepted test roots are exactly
  `tests/lib/` and `tests/validation/`;
- `tests/validation/test_script_manifest.py`: the PostgreSQL expected path and
  regressions that reject the retired placeholder roots;
- `tests/validation/test_document_metadata.py`: the unclassified test README
  set is exactly `tests/lib/README.md` and `tests/validation/README.md`;
- `scripts/lib/gate/ci_gate_contract.py`: its current test-path comment;
- `.github/CODEOWNERS`: the agent-governance test path; and
- `tests/lib/test_surface_ownership.py`: the mirror and placeholder-absence
  invariants from Step 1.

The moved agent-governance module remains unregistered in Task 4. Task 5 owns
its measured fixture repair and registration.

- [ ] **Step 5: Update only current documentation and future instructions**

Delete the three placeholder READMEs with `apply_patch`. Update:

- `tests/README.md`, `tests/lib/README.md`, and
  `tests/validation/README.md` to describe the actual two-surface ownership;
- the two target-surface test commands in `scripts/README.md`;
- the PostgreSQL command in
  `docs/05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md`;
- only the three live Markdown link destinations: the CI gate contract link in
  `docs/90.references/research/0002-agentic-engineering-research-pack/quality-ci-formatting.md`
  becomes `../../../../tests/lib/gate/test_ci_gate_contract.py`, while the
  governance contract links in `scope-application-matrix.md` and
  `workspace-baseline.md` become
  `../../../../tests/lib/agent_governance/test_agent_governance_contract.py`;
  keep their dated prose and historical literals unchanged; and
- every forward instruction in draft SPEC-0158's `plan.md` that names
  `tests/validation/test_agent_governance_contract.py`, including its dotted
  unittest command, to the new agent-governance test path. Keep SPEC-0158 draft
  and do not execute it.

Completed Spec/Task evidence, Stage 90 dated observations, Stage 98 recovery
records, and generated historical datasets preserve their old-path literals.
Only current commands, machine wiring, current comments, ownership declarations,
and clickable link destinations move.

- [ ] **Step 6: Prove the seven already-registered moved suites**

```bash
PYTHONPATH=. python3 -m unittest \
  tests.lib.gate.test_ci_gate_adapters \
  tests.lib.gate.test_ci_gate_contract \
  tests.lib.gate.test_github_workflow_contract \
  tests.lib.ops.test_postgres_logical_upgrade_rehearsal \
  tests.lib.supply_chain.test_grype_db_seed \
  tests.lib.target_surface.test_target_surface_contracts \
  tests.lib.target_surface.test_target_surface_delta_contracts
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
PYTHONPATH=. python3 -m unittest tests.validation.test_ci_gate_runner
PYTHONPATH=. python3 -m unittest tests.validation.test_script_manifest
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_document_metadata.ReadmeProfileTests
PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
PYTHONPATH=. python3 scripts/validation/check-github-workflow-contract.py
```

Expected: all seven registered moved suites and every ownership/wiring check are
GREEN. Run the eighth suite explicitly:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.lib.agent_governance.test_agent_governance_contract
```

It may remain RED only on the three Task 5-owned missing-SPEC-0153 fixture
subcases already measured in Task 3. Record their exact identities; do not
repair or register that module here.

- [ ] **Step 7: Verify documents, stale paths, and the full-Gate boundary**

Run metadata contracts, changed-document metadata, all links, and an
untruncated old-path sweep. Classify every remaining old-path hit: historical
evidence may remain, but no current machine reference, command, comment,
ownership declaration, future instruction, or clickable link destination may
use an old path.

```bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
git diff --check
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full \
  > /tmp/g-task4.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task4.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task4.txt
```

The full Gate may report `FULL exit=1` only for these five Task 6-owned
`ChangedBodyDeficitGitTests` results already measured in Task 3:

1. Error: `test_registered_operations_catalog_move_uses_migration_0003_body_baseline`
2. Error: `test_registered_operations_profile_transition_holds_the_registry_boundary`
3. Failure: `test_preexisting_target_cannot_borrow_registered_source_baseline`
4. Failure: `test_registered_operations_move_requires_its_exact_source_at_base`
5. Failure: `test_unrelated_operations_readme_does_not_receive_transition_authorization`

No moved-module import, registration, manifest, workflow-contract, metadata, or
link failure is allowed.

- [ ] **Step 8: Commit**

Stage only the exact moved, deleted, and current-reference paths recorded in
this Task; inspect `git diff --cached --name-only` before committing.

```bash
git commit -m "refactor(tests): Mirror library ownership in the test surface"
```

---

### Task 5: Register every measured test module and repair failures

**Files:**

- Modify: `scripts/validation/ci_gate_runner.py`, `.github/workflow-contract.yml`
- Modify or delete: only the measured post-Task-4 unregistered modules that fail

**Interfaces:**

- Consumes: Task 4's module paths.
- Produces: the set of test modules on disk equals the set the full gate runs.

- [ ] **Step 1: Write the coverage invariant**

Add to `tests/lib/test_surface_ownership.py`:

```python
    def test_every_test_module_is_registered_in_a_gate(self) -> None:
        """No module sits on disk unreached. The current measured gap is the
        authority; do not rely on a predecessor count or module-name list.
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

- [ ] **Step 4: Disposition each measured failing module**

For every failing module reported by Step 3, inspect its current path and
failure. Rebuild only a fixture that has a live-corpus subject; otherwise remove
the module and its manifest row, recording why its current subject is absent.

- [ ] **Step 5: Repair the remaining measured failures, one commit each**

For each current failure from Step 3, read the failure, name its root cause in
the commit message, and fix the production defect rather than the assertion.
Where the assertion is wrong, state that and change it. Do not reintroduce a
historical module name or failure count.

- [ ] **Step 6: Register the now-green modules**

In `scripts/validation/ci_gate_runner.py`, add each measured current module name to the tuple
that already lists `tests.lib.document_governance.*` and the validation modules,
keeping the list alphabetically sorted so a later addition is a one-line diff.

- [ ] **Step 7: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership 2>&1 | grep -E "^(Ran |OK|FAILED)"
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-task5.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task5.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task5.txt
```

Expected: the registration invariant is `OK`. The full Gate may remain RED only
for the same five Task 6-owned `ChangedBodyDeficitGitTests` results recorded in
Task 4; no unregistered module, moved-path import, or newly registered suite may
fail. The gate will now run noticeably longer because the modules are no longer
invisible.

- [ ] **Step 8: Commit**

```bash
git status --short
git add -- scripts/validation/ci_gate_runner.py .github/workflow-contract.yml \
  tests/lib/test_surface_ownership.py \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md
# Add each measured repair or deletion by its exact recorded path; never stage
# the entire worktree.
git diff --cached --name-only
git commit -m "test(gate): Register every test module and repair the ones nothing ran"
```

---

### Task 6: Retire fixed-workspace historical document fixtures

**Files:**

- Modify: `tests/validation/test_document_metadata.py`
- Modify: `tests/validation/test_document_corpus_lifecycle.py`
- Modify: `tests/lib/target_surface/test_target_surface_contracts.py`
- Modify: `tests/lib/document_governance/test_spec_packages.py`
- Modify: `tests/lib/document_governance/test_operations_catalog.py`
- Modify: `tests/lib/test_surface_ownership.py`

**Interfaces:**

- Consumes: Task 5's registration, so a regression here is caught rather than silent.
- Produces: current Registry/template fixtures for document contracts and
  temporary-Git or current-row fixtures for Stage 98 recovery.
- Preserves: `HistoricalDocument` only where regular-blob recovery is the
  behavior under test.

- [ ] **Step 1: Write the fixed-workspace invariant**

Add to `tests/lib/test_surface_ownership.py`:

```python
    def test_document_contract_tests_do_not_read_fixed_workspace_history(self) -> None:
        """Current contracts never depend on a deleted taxonomy or pinned clone history."""

        contract_tests = (
            ROOT / "tests/validation/test_document_metadata.py",
            ROOT / "tests/validation/test_document_corpus_lifecycle.py",
            ROOT / "tests/lib/target_surface/test_target_surface_contracts.py",
            ROOT / "tests/lib/document_governance/test_spec_packages.py",
        )
        forbidden = (
            "HISTORICAL_COMMIT",
            "LEGACY_CONTRACT_FIXTURE_COMMIT",
            "docs/99.templates/support/",
        )
        offenders = [
            f"{path.relative_to(ROOT)}: {token}"
            for path in contract_tests
            for token in forbidden
            if token in path.read_text(encoding="utf-8")
        ]
        self.assertEqual([], offenders)
```

- [ ] **Step 2: Run it and record the current offenders**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership.SurfaceOwnershipTests.test_document_contract_tests_do_not_read_fixed_workspace_history
```

Expected: FAIL naming the current historical constants and retired support
paths. Record the exact files in the current Task; do not copy their bodies.

- [ ] **Step 3: Replace document-contract fixtures with current sources**

For positive cases, load `docs/99.templates/registry.json` and the template path
declared by its `template_roles` row. For a negative case, copy that current
value into a temporary directory and mutate exactly one field or section. Reuse
the existing `registry_fixture` and `fixture` helpers in
`test_document_metadata.py`; do not create a second profile registry under
`tests/fixtures/`.

Delete assertions whose only subject is the removed
`docs/99.templates/support/` taxonomy. Replace an assertion only when the same
behavior is still declared by the current Registry or a current template.

- [ ] **Step 4: Keep recovery tests recovery-specific**

`test_operations_catalog.py` may read the current Migration 0003 recovery row.
Any other `HistoricalDocument` test creates a temporary Git repository, commits
one regular file, deletes it from the worktree, and reads that exact
`commit:path`. It must also reject a tree, missing object, or non-regular blob.
No recovery test embeds a workspace commit literal.

- [ ] **Step 5: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
PYTHONPATH=. python3 -m unittest tests.lib.target_surface.test_target_surface_contracts
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_operations_catalog
rg -n "HISTORICAL_COMMIT|LEGACY_CONTRACT_FIXTURE_COMMIT|docs/99.templates/support/" \
  tests/validation/test_document_metadata.py \
  tests/validation/test_document_corpus_lifecycle.py \
  tests/lib/target_surface/test_target_surface_contracts.py \
  tests/lib/document_governance/test_spec_packages.py
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full \
  > /tmp/g-task6.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task6.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task6.txt
```

Expected: every unit command exits 0, the search has no output, the five
deferred `ChangedBodyDeficitGitTests` results are repaired, and the full Gate
reports `FULL exit=0`.

- [ ] **Step 6: Commit**

```bash
git add -- tests/validation/test_document_metadata.py \
  tests/validation/test_document_corpus_lifecycle.py \
  tests/lib/target_surface/test_target_surface_contracts.py \
  tests/lib/document_governance/test_spec_packages.py \
  tests/lib/document_governance/test_operations_catalog.py \
  tests/lib/test_surface_ownership.py \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md
git diff --cached --name-only
git commit -m "test(fixtures): Derive document contracts from current authority"
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
git add -- scripts/lib/document_governance/identity_history.py \
  tests/lib/document_governance/test_identity_history.py \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md
git diff --cached --name-only
git commit -m "perf(identity): Scan path names instead of every diff in history"
```

---

### Task 8: Split the two production responsibility surfaces

**Files:**

- Create: `scripts/lib/document_governance/metadata/{profile,lifecycle,heading,identity,reference}.py`
- Modify: `scripts/lib/document_governance/metadata_validator.py` into a thin compatibility re-export
- Create: `scripts/lib/document_governance/lifecycle/{public,contract,promoted,recovery}.py`
- Modify: `scripts/validation/check-document-corpus-lifecycle.py` into a thin entrypoint

**Interfaces:**

- Consumes: Task 1's four modes, Task 2's derived census, Task 6's fixtures. Splitting before those would divide code that is about to be deleted and would do it without a working safety net.
- Produces: the public names `load_registry`, `build_registry_profiles`, `validate_record`, `validate_repository_contracts`, `load_transition_overrides`, `collect_issued_identities` remain importable from `scripts.lib.document_governance.metadata_validator`, so no caller changes.

- [ ] **Step 1: Record live consumers before moving anything**

```bash
rg -n \
  "from scripts\.lib\.document_governance\.metadata_validator import|metadata_validator\." \
  scripts tests
```

Record the untruncated result in the current Task. Incidental module globals are
not an API merely because `dir()` exposes them; the compatibility surface is
the set that tracked consumers import or access.

Before moving code, also record the focused suite counts and prove that all four
registered lifecycle modes exit 0. These observations are the behavioral
baseline for Step 5; file length is not the acceptance oracle.

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata 2>&1 | grep -E "^Ran "
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle 2>&1 | grep -E "^Ran "
for mode in check-public check-contract check-promoted check-recovery; do
  PYTHONPATH=. python3 scripts/validation/check-document-corpus-lifecycle.py \
    --mode "$mode" >/dev/null 2>&1
  echo "$mode exit=$?"
done
```

- [ ] **Step 2: Write the declared compatibility test**

```python
    def test_metadata_validator_declares_its_compatibility_api(self) -> None:
        """The split preserves live imports, not every incidental module global."""

        from scripts.lib.document_governance import metadata_validator

        self.assertTrue(metadata_validator.__all__)
        missing = [
            name for name in metadata_validator.__all__
            if not hasattr(metadata_validator, name)
        ]
        self.assertEqual([], missing)
```

The test fails before `__all__` exists. Build `__all__` from the live-consumer
inventory in Step 1, then use explicit re-exports from the new modules. Do not
use wildcard imports or a temporary-file snapshot as a permanent test oracle.

- [ ] **Step 3: Move one responsibility at a time**

For each of profile, lifecycle, heading, identity, reference: cut the functions
that belong to it into the new module, add explicit imports for the names in
`metadata_validator.__all__`, and run the compatibility test plus
`PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata`
before starting the next one. Five separate commits.

- [ ] **Step 4: Split the lifecycle checker the same way**

One module per surviving mode: `public.py`, `contract.py`, `promoted.py`,
`recovery.py`. `check-document-corpus-lifecycle.py` keeps `_parser`,
`_validate_cli_shape`, and a `main` that dispatches on `args.mode`.

- [ ] **Step 5: Verify**

```bash
PYTHONPATH=. python3 -m unittest tests.validation.test_document_metadata
PYTHONPATH=. python3 -m unittest tests.validation.test_document_corpus_lifecycle
for mode in check-public check-contract check-promoted check-recovery; do
  PYTHONPATH=. python3 scripts/validation/check-document-corpus-lifecycle.py \
    --mode "$mode" >/dev/null 2>&1
  echo "$mode exit=$?"
done
PYTHONPATH=. python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-task8.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-task8.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-task8.txt
```

Expected: the declared compatibility API remains importable, both focused suite
counts equal their Step 1 baselines, all four modes exit 0, and the full Gate
reports `FULL exit=0`.

- [ ] **Step 6: Commit each move separately**

```bash
git add -A -- scripts/lib/document_governance/metadata \
  scripts/lib/document_governance/lifecycle \
  scripts/lib/document_governance/metadata_validator.py \
  scripts/validation/check-document-corpus-lifecycle.py \
  tests/validation/test_document_metadata.py \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md
git diff --cached --name-only
git commit -m "refactor(metadata): Split the validator by responsibility"
```

---

### Task 9: Split the corresponding test responsibility surfaces and close the Spec Packages

**Files:**

- Split: `tests/validation/test_document_metadata.py` and `tests/validation/test_document_corpus_lifecycle.py` to match Task 8's responsibility modules
- Modify: `scripts/README.md`
- Modify: `scripts/validation/ci_gate_runner.py`, `.github/workflow-contract.yml`, and `scripts/manifest.yaml` whenever split test module names change
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
implements no domain logic; `tests/lib/<domain>/` mirrors `lib/<domain>/`, while
`tests/validation/` retains validation and entrypoint tests.

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
git add -A -- tests/lib/document_governance/metadata \
  tests/validation/lifecycle \
  tests/validation/test_document_metadata.py \
  tests/validation/test_document_corpus_lifecycle.py \
  scripts/README.md \
  docs/03.specs/0154-validation-surface-reduction/spec.md \
  docs/03.specs/0155-validation-surface-reduction/spec.md \
  docs/03.specs/0157-script-surface-ownership-convergence/spec.md \
  docs/03.specs/0157-script-surface-ownership-convergence/plan.md \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md \
  docs/03.specs/README.md
python3 scripts/knowledge/generate-llm-wiki.py --write
git add -- docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md \
  docs/90.references/data/0082-llm-wiki-index/README.md
git diff --cached --name-only
python3 scripts/knowledge/generate-llm-wiki.py
python3 scripts/validation/run-ci-gate.py --profile full > /tmp/g-final.txt 2>&1; echo "FULL exit=$?" >> /tmp/g-final.txt
grep -nE "^(Ran [0-9]+ tests|OK|FAILED)|FULL exit=" /tmp/g-final.txt
```

Expected: both wiki outputs are fresh, the two post-split test-count sums equal
their pre-split baselines, and the full Gate reports `FULL exit=0`.
Regenerate after the last document is authored, not before; the gate checks
freshness and a Task that writes its own record after regenerating leaves it red.

- [ ] **Step 7: Commit**

```bash
git diff --cached --check
git diff --cached --name-only
git commit -m "docs(spec): Close the script surface ownership convergence"
```

## Risk and Rollback

| Risk | Guardrail | Rollback |
| :--- | :--- | :--- |
| A mode is deleted that a gate reaches | Step 1 of Task 1 prints the registered modes before any deletion | `git revert` the Task 1 commit |
| A move breaks an import that no test covers | Task 3 Step 4 greps for stale paths and the full gate runs at the task boundary | `git revert`; `git mv` is reversible in one commit |
| Registering a red module makes the gate red for an unrelated reason | Task 5 measures every module before registering it and repairs first | Unregister the single module; its repair commit stands alone |
| A retired historical test encoded a still-current guarantee | Task 6 replaces it only when the current Registry or template declares the same behavior | `git revert`; restore the test and classify its current owner before retrying |
| A split loses a test | Task 9 Step 1 records the counts and Step 3 compares the sums | `git revert` the single split commit |
| A count is repinned instead of derived | Task 2 compares current path sets and source relations rather than a literal | `git revert` the Task 2 commit |

## Verification

Every task boundary runs `run-ci-gate.py --profile full` and records the
`FULL exit=` line rather than inferring it from `tail -1`. A boundary may retain
only an explicitly measured RED owned by a later Task; the owning Task must
remove it, and the final boundary reports `FULL exit=0`. The final state
additionally satisfies:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-script-manifest.py
bash scripts/operations/sync-provider-surfaces.sh --check && git diff --exit-code
rg -n "HISTORICAL_COMMIT|LEGACY_CONTRACT_FIXTURE_COMMIT|docs/99.templates/support/" \
  tests/validation/test_document_metadata.py \
  tests/validation/test_document_corpus_lifecycle.py \
  tests/lib/target_surface/test_target_surface_contracts.py \
  tests/lib/document_governance/test_spec_packages.py
grep -rn "NON_STANDALONE_VALIDATOR_PATHS" scripts tests
```

Expected: `violations=0`, `failures=0`, `PASS`, `drift=0` with a clean diff,
`FULL exit=0`, and no output from the final two searches.

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
6. **A document-contract test judges the current corpus, never a deleted
   taxonomy.** Current contracts derive from the Registry or registered
   template. Recovery tests use temporary Git or a current Stage 98 row and do
   not pin an unrelated workspace commit.
7. **Discovered implementation is revalidated, never retroactively approved.**
   Task 0 records the actual earlier commit range, activates the legal parent
   chain, and reruns the affected checks before any new production mutation.
8. **File length is diagnostic evidence, not an ownership contract.** The four
   selected files are split because each contains measured, independently
   testable responsibilities. A repository-wide source-size policy or exception
   mechanism requires its own approved Requirement, ADR, and Spec; this Plan
   does not create one implicitly.

## Related Documents

- [Specification](spec.md)
- [Validation surface reduction](../0155-validation-surface-reduction/spec.md)
- [Governance consistency convergence](../0154-governance-consistency-convergence/spec.md)
- [Quality standards](../../00.agent-governance/policies/quality-standards.md)
