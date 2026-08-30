---
profile_id: plan
status: active
artifact_id: plan-0155
artifact_type: plan
parent_ids: [SPEC-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Validation Surface Reduction Plan

## Objective

Execute SPEC-0155 in eight sequential Tasks, then merge the branch to `main`.

Two Tasks come first because they unblock verification for everything after
them: the full gate profile does not currently run to completion, and the
blocking metadata mode reports four violations that SPEC-0154 closed without
resolving. No reduction Task may be verified against a gate that is already
failing for an unrelated reason.

## Dependencies

| Task | Depends on | Reason                                                             |
| :--- | :--------- | :----------------------------------------------------------------- |
| 1    | none       | Restores `--profile full` so later Tasks can verify                |
| 2    | none       | Independent of Task 1; ordered second because it is smaller        |
| 3    | 1, 2       | Gate retirement must be verified by a working full profile         |
| 4    | 3          | Corpus-lifecycle predicates overlap the retired old-path gate      |
| 5    | 4          | Provenance narrowing removes what Task 4 stops calling             |
| 6    | 2          | Removing the advisory guard requires the blocking mode to be clean |
| 7    | none       | Data-only; ordered late to keep gate churn separate                |
| 8    | 3, 4, 5    | Sweeps for nodes those Tasks left without an implementation        |

SPEC-0154 is `completed` and supplies the corrected lifecycle vocabulary,
the widened link gate, and the four routed findings.

## Execution Sequence

### Task 1: Restore the full gate profile

**Files:**

- Modify: `tests/validation/test_document_metadata.py` — `init_git` at line 1110, `copy_registry_contract_fixture` at line 1289
- Modify: `scripts/lib/document_governance/identity_history.py` — `_run_git` at line 88, call sites at lines 425, 454, 471, 472
- Test: `tests/validation/test_document_metadata.py::ChangedModeRolloutTests::test_reverse_transition_without_override_is_blocked`

**Interfaces:**

- Produces: a `--profile full` that exits 0, which Tasks 3 to 8 use as their acceptance gate.

Three distinct defects stack in this one failure. SPEC-0154 measured and
rejected the deadline and the output cap; neither is involved. Fix them in the
order they surface, because each masks the next.

- [ ] **Step 1: Reproduce and capture the current failure**

```bash
python3 -m unittest tests.validation.test_document_metadata.ChangedModeRolloutTests.test_reverse_transition_without_override_is_blocked 2>&1 | head -20
```

Expected: `ERROR`, a `RuntimeError` raised from `copy_registry_contract_fixture`
line 1310 whose payload begins `[ECC pre-commit] Potential secret detected`.
Runtime about 114 seconds. Record the runtime; it is part of the evidence.

- [ ] **Step 2: Neutralize the operator's hook path in the fixture**

Defect A. `core.hooksPath` is set globally to `/home/hy/.codex/git-hooks`, so
every fixture repository inherits the operator's blocking pre-commit hook. The
hook's findings are `${VAR}` interpolations and `secrets.GITHUB_TOKEN`
references in `infra/` and `.github/`, not plaintext secrets, but a fixture
must not run the operator's commit hooks at all. `init_git` already defends
against one global-config leak, `init.defaultBranch`; this is the same class.

In `init_git`, immediately after the `git init -q` self-check:

```python
    # Do not inherit the operator's hooks. `core.hooksPath` is a global
    # setting here, so a fixture commit would run the operator's pre-commit
    # hook against a tree the fixture does not own. Same class as the
    # `init.defaultBranch` defense below.
    git(root, "config", "core.hooksPath", "")
```

- [ ] **Step 3: Re-run and confirm the failure changed shape**

```bash
python3 -m unittest tests.validation.test_document_metadata.ChangedModeRolloutTests.test_reverse_transition_without_override_is_blocked 2>&1 | tail -6
```

Expected: `FAILED (failures=1)` rather than `errors=1`, runtime about 23 seconds
rather than 114. The assertion now reports
`configuration-error: bounded Git identity scan failed`. Record both numbers.

- [ ] **Step 4: Write a failing test for the Git predicate**

Defect B. `git merge-base --is-ancestor A B` exits 0 for true and **1 for
false**; only 2 and above are errors. `_run_git` treats every non-zero return
as a scan failure, and all five of its failure branches raise the identical
message while discarding Git's stderr, which is why this was undiagnosable.

Add to `tests/lib/document_governance/test_identity_history.py`:

```python
def test_predicate_false_is_not_a_scan_failure(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "core.hooksPath", ""], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "t@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
        (root / "a.txt").write_text("a", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "one"], cwd=root, check=True)
        first = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        subprocess.run(["git", "checkout", "-q", "--orphan", "other"], cwd=root, check=True)
        (root / "b.txt").write_text("b", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "two"], cwd=root, check=True)
        result = identity_history.git_predicate(
            root, ("merge-base", "--is-ancestor", first, "HEAD")
        )
        self.assertFalse(result)
```

- [ ] **Step 5: Run it and confirm it fails**

```bash
python3 -m unittest tests.lib.document_governance.test_identity_history.-k test_predicate_false_is_not_a_scan_failure -v
```

Expected: FAIL with `AttributeError: module has no attribute 'git_predicate'`.

- [ ] **Step 6: Separate the predicate from the scan**

In `identity_history.py`, give `_run_git` an explicit set of return codes that
are answers rather than failures, and add a predicate wrapper. Also carry Git's
stderr into the message so the next reader is not blind.

```python
def _run_git(
    repo: pathlib.Path,
    arguments: tuple[str, ...],
    *,
    max_output_bytes: int = MAX_GIT_OUTPUT_BYTES,
    timeout_seconds: float = MAX_GIT_SCAN_SECONDS,
    answer_codes: frozenset[int] = frozenset({0}),
) -> _GitOutput:
```

At the return-code branch, replace the bare raise with:

```python
        if returncode not in answer_codes:
            detail = bytes(stderr).decode("utf-8", "replace").strip()
            raise IdentityHistoryError(
                f"bounded Git identity scan failed: git {' '.join(arguments)}"
                f" exited {returncode}{': ' + detail if detail else ''}"
            )
```

This requires `_run_git` to retain stderr; it currently discards every stderr
chunk. Extend the `stderr` bytearray alongside `stdout` in the read loop and
carry the return code on `_GitOutput`.

Then add:

```python
def git_predicate(repo: pathlib.Path, arguments: tuple[str, ...]) -> bool:
    """Run a Git predicate where exit 1 is the answer `false`, not a failure."""

    output = _run_git(repo, arguments, answer_codes=frozenset({0, 1}))
    return output.returncode == 0
```

- [ ] **Step 7: Run the new test and confirm it passes**

```bash
python3 -m unittest tests.lib.document_governance.test_identity_history -v 2>&1 | tail -5
```

Expected: OK.

- [ ] **Step 8: Decide Defect C by measurement**

Defect C. `copy_registry_contract_fixture` calls `init_git(root)` with the
default `descend_from_head=False`. `init_git` then runs
`git symbolic-ref HEAD refs/heads/main`, which in a repository cloned from this
one repoints HEAD at an **unborn** `main` and discards the cloned ancestry. The
next `commit_all` therefore writes a root commit, and the pinned allocation
predecessor `889d3868ecd0913cddac79a718584a54a8453525` cannot be its ancestor.
`init_git`'s own `descend_from_head` comment describes exactly this failure.

The test at line 8509 clones this repository specifically so the CLI validates
"against real Git history", which `init_git` then throws away. Two repairs are
available; measure both rather than choosing on reasoning.

Option 1, pass the existing defense:

```python
    init_git(root, descend_from_head=True)
```

Option 2, preserve the clone's own history and only rename its branch. In
`init_git`, replace the unconditional `symbolic-ref` with:

```python
    has_commits = git(root, "rev-parse", "--verify", "-q", "HEAD").returncode == 0
    if has_commits:
        # A fixture built on a clone already has the ancestry the checker
        # reads. Renaming keeps it; repointing HEAD at an unborn branch would
        # discard it and make every pinned predecessor unreachable.
        renamed = git(root, "branch", "-M", "main")
        if renamed.returncode != 0:
            raise RuntimeError(renamed.stderr)
    else:
        named = git(root, "symbolic-ref", "HEAD", "refs/heads/main")
        if named.returncode != 0:
            raise RuntimeError(named.stderr)
```

Apply each in turn, run the command in Step 9, and record both results in the
Task before keeping one. Prefer the option that leaves the fixture independent
of `ROOT`'s current HEAD; if both pass, that is Option 2.

- [ ] **Step 9: Verify the target test**

```bash
python3 -m unittest tests.validation.test_document_metadata.ChangedModeRolloutTests.test_reverse_transition_without_override_is_blocked 2>&1 | tail -5
```

Expected: OK.

- [ ] **Step 10: Verify no fixture regressed**

```bash
python3 -m unittest tests.validation.test_document_metadata 2>&1 | tail -5
python3 -m unittest tests.lib.document_governance.test_identity_history 2>&1 | tail -5
```

Expected: OK for both. `init_git` serves many fixtures; a change to its branch
handling must be measured across the whole module, not only the target test.

- [ ] **Step 11: Run the registered profiles**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/run-ci-gate.py --profile changed
```

Expected: exit 0 for both. This is the first time in this branch that
`--profile full` exits 0; record it.

- [ ] **Step 12: Commit**

```bash
git add tests/validation/test_document_metadata.py \
        tests/lib/document_governance/test_identity_history.py \
        scripts/lib/document_governance/identity_history.py \
        docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0001-full-gate-restoration.md
git commit -m "fix(tests): Stop three defects from masking each other in one gate failure"
```

---

### Task 2: Close the blocking metadata mode

**Files:**

- Modify: `docs/99.templates/registry.json` — the `governance-policy` profile
- Modify: `scripts/lib/document_governance/metadata_validator.py` — heading branch at line 2437, `load_transition_overrides` at line 6135
- Modify: `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md`, `0002-operations-catalog-convergence.md`
- Test: `tests/lib/document_governance/test_metadata_validator.py`

**Interfaces:**

- Consumes: nothing from Task 1.
- Produces: `check-document-metadata.py --mode check-changed` at zero violations, which every later Task uses as its acceptance gate.

- [ ] **Step 1: Record the starting count**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
```

Expected: `violations=4`. Two `body-heading-forbidden` and two
`invalid-transition: archived -> completed`.

- [ ] **Step 2: Measure the `governance-policy` heading vocabulary**

```bash
python3 - <<'PY'
import pathlib, re, collections
root = pathlib.Path("docs/00.agent-governance/policies")
docs = [p for p in root.rglob("*.md")
        if re.search(r"^profile_id:\s*governance-policy\s*$", p.read_text(), re.M)]
counts = collections.Counter()
for p in docs:
    for h in re.findall(r"^## (.+)$", p.read_text(), re.M):
        counts[h] += 1
print("documents:", len(docs))
print("distinct headings:", len(counts))
for h, n in counts.most_common():
    print(f"{n:3d}  {h}")
PY
```

Record the output in the Task. A heading present in every document is a
candidate contract; a heading present in one is evidence the profile is
free-form.

- [ ] **Step 3: Choose the disposition from that table**

If a shared vocabulary covers every document, register it as
`required_sections` and conform the outliers. If it does not, the profile is
free-form and Steps 4 to 6 apply.

Registering only the headings of `quality-standards.md` and
`environment-constraints.md` is prohibited. It whitelists the two documents
SPEC-0154 changed and leaves the rest of the profile unregistered, which is the
asymmetry this Task exists to remove.

- [ ] **Step 4: Write a failing test for the free-form declaration**

Only if Step 3 selects free-form. In
`tests/lib/document_governance/test_metadata_validator.py`:

```python
def test_free_form_profile_permits_unregistered_headings(self) -> None:
    findings = self.validate_body(
        profile_id="governance-policy",
        headings=["## Anything At All", "## Related Documents"],
    )
    self.assertEqual([], [f for f in findings if f.code == "body-heading-forbidden"])
```

- [ ] **Step 5: Run it and confirm it fails**

```bash
python3 -m unittest tests.lib.document_governance.test_metadata_validator -k test_free_form_profile_permits_unregistered_headings -v
```

Expected: FAIL, one `body-heading-forbidden` finding.

- [ ] **Step 6: Declare the profile free-form at the branch that reads it**

The emission site is `metadata_validator.py:2442`, inside
`if isinstance(registry, DocumentRegistry)`, reading `registry.profiles`. A
declaration placed anywhere else has no effect; SPEC-0154 lost a commit to
exactly that mistake.

In `registry.json`, add to the `governance-policy` profile:

```json
      "free_form_sections": true,
```

At line 2437, guard the forbidden-heading loop:

```python
            if not profile.get("free_form_sections"):
                for heading in sorted(set(h2) - required - optional):
                    findings.append(
                        _finding(
                            record,
                            "body-heading-forbidden",
                            f"profile {record.artifact_type} contains unregistered heading: {heading}",
                        )
                    )
```

`required_sections: ["Related Documents"]` stays, so the one obligation the
Output Style Contract places on every document is still enforced.

- [ ] **Step 7: Verify the heading findings are gone for the whole profile**

```bash
python3 -m unittest tests.lib.document_governance.test_metadata_validator 2>&1 | tail -3
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
```

Expected: OK, and `violations=2`. Both remaining are the transition findings.

- [ ] **Step 8: Write a failing test for the override path contract**

```python
def test_override_accepts_a_co_located_task(self) -> None:
    overrides = load_transition_overrides(
        self.root,
        [{
            "path": "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md",
            "previous_status": "archived",
            "new_status": "completed",
            "evidence_task": "docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0003-lifecycle-completion.md",
            "approval": "workspace owner",
            "reason": "correction from a status the lifecycle never defined",
        }],
        self.profiles,
    )
    self.assertEqual(1, len(overrides))
```

- [ ] **Step 9: Run it and confirm it fails**

```bash
python3 -m unittest tests.lib.document_governance.test_metadata_validator -k test_override_accepts_a_co_located_task -v
```

Expected: FAIL with
`ProfileError: transition override row 0 evidence_task must be an existing co-located Task`.

- [ ] **Step 10: Repair the unreachable path contract**

The repository holds 0 directories matching `docs/03.specs/spec-*` and 0 files
named `task.md`, against 15 named `tsk-*.md`. No document can use the override.

At `metadata_validator.py:6135`, replace the prefix and basename test:

```python
        if (
            evidence is None
            or not re.fullmatch(
                r"docs/03\.specs/\d{4}-[a-z0-9-]+/tasks/tsk-\d{4}-[a-z0-9-]+\.md",
                evidence.as_posix(),
            )
            or not (root / evidence).is_file()
        ):
```

- [ ] **Step 11: Run it and confirm it passes**

```bash
python3 -m unittest tests.lib.document_governance.test_metadata_validator -k test_override_accepts_a_co_located_task -v
```

Expected: OK.

- [ ] **Step 12: Record the two migration transitions through the repaired mechanism**

Add both rows to the registered override source with `approval` and `reason`
naming the correction, and `evidence_task` pointing at
`docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0003-lifecycle-completion.md`.
Do not relax the lifecycle to make the transition legal; these documents are
being corrected from a status their lifecycle never defined, which is the case
the override exists to carry.

- [ ] **Step 13: Verify the blocking mode is clean**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/run-ci-gate.py --profile full
```

Expected: `violations=0` with `transition_overrides=2`, and exit 0.

- [ ] **Step 14: Commit**

```bash
git add docs/99.templates/registry.json \
        scripts/lib/document_governance/metadata_validator.py \
        tests/lib/document_governance/test_metadata_validator.py \
        docs/98.archive/migrations/ \
        docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0002-blocking-mode-closure.md
git commit -m "fix(validation): Make one contract enforceable and the other reachable"
```

---

### Task 3: SPEC-0137 disposition and gate retirement

**Files:**

- Modify: `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` and its Tasks
- Delete: `scripts/validation/agentic-research-gate9-evidence.py`, `scripts/validation/gate2_claim_review_contract.py`, `scripts/validation/carry_owner_contract.py` and their tests
- Modify: `scripts/manifest.yaml`, `scripts/lib/document_governance/suite_registry.py`, `scripts/validation/ci_gate_contract.py`
- Modify: `scripts/validation/check-document-links.py` — remove `DEFERRED_PREFIXES`

**Interfaces:**

- Consumes: the working `--profile full` from Task 1.
- Produces: a gate set with no node lacking an implementation, consumed by Task 8.

- [ ] **Step 1: Record SPEC-0137's actual state**

```bash
grep -l "^status:" docs/03.specs/0137-agentic-research-pack-rebuild/tasks/*.md \
  | xargs grep -H "^status:"
ls docs/90.references/research/0002-agentic-engineering-research-pack/ | head
```

Expected: three `cancelled`, one `active`, and the old pack still present.
Record all four states verbatim in the Task.

- [ ] **Step 2: Decide the disposition and write it down before deleting anything**

Read the `active` Task. If it has real remaining work, SPEC-0137 stays `active`
and only the gate modules bound to the cancelled Tasks retire. Otherwise
transition the Spec under the SPEC-0154 rule and retire all four modules.
Record the judgement and the evidence for it in the Task first.

- [ ] **Step 3: Measure each module's consumers before removing it**

```bash
for m in agentic-research-gate9-evidence gate2_claim_review_contract carry_owner_contract; do
  echo "=== $m ==="
  grep -rln "$m" scripts tests docs | grep -v "^docs/03.specs/0137" || echo "(none)"
done
```

Record the result per module. A module with a consumer outside its own tests,
its manifest row, and SPEC-0137 is not retired in this Task.

- [ ] **Step 4: Remove the gate node before the module**

`carry_owner_contract` is registered in `--profile full`. Removing the module
first leaves the profile pointing at an absent implementation.

```bash
grep -n "carry_owner_contract" scripts/validation/ci_gate_contract.py
```

Delete the node, then run `python3 scripts/validation/run-ci-gate.py --profile full`
and expect exit 0 with the node absent from `--explain`.

- [ ] **Step 5: Remove the modules, their tests, and their registrations**

```bash
git rm scripts/validation/agentic-research-gate9-evidence.py \
       scripts/validation/gate2_claim_review_contract.py \
       scripts/validation/carry_owner_contract.py
git rm tests/validation/test_agentic_research_gate9_evidence.py \
       tests/validation/test_gate2_claim_review_contract.py \
       tests/validation/test_carry_owner_contract.py
```

Then remove their `scripts/manifest.yaml` entries and `suite_registry.py`
bindings. Confirm the exact test filenames with `ls tests/validation/` before
running the command; do not assume them.

- [ ] **Step 6: Verify the manifest and the gate contract**

```bash
python3 scripts/validation/check-script-manifest.py
python3 -m unittest tests.validation.test_ci_gate_contract 2>&1 | tail -3
python3 scripts/validation/run-ci-gate.py --profile full
```

Expected: exit 0, OK, exit 0.

- [ ] **Step 7: Rewrite the SPEC-0137 passages that cite the retired gates**

The Spec must describe what was built, not a control that no longer exists.
Every removed gate named in its prose is replaced by a statement of what
actually happened, or the passage is deleted.

- [ ] **Step 8: Remove the link-gate exemption and repair what it hid**

```bash
grep -n "DEFERRED_PREFIXES" scripts/validation/check-document-links.py
```

Delete the constant and the `_deferred` filter, then:

```bash
python3 scripts/validation/check-document-links.py --mode all
```

Expected: failures reported for the 158 links the exemption was hiding. Repair
or delink each with the `(retired path: ...)` form SPEC-0154 used, then re-run
and expect `failures=0`. If Step 2 retired the old research pack outright, the
links go with it and this step is a deletion instead.

- [ ] **Step 9: Verify the link tests still hold**

```bash
python3 -m unittest tests.lib.document_governance.test_links 2>&1 | tail -3
```

Expected: OK. The three `LinkSelectionScopeTests` added by SPEC-0154 must still
pass; if one asserted the deferred rule, update it to assert its absence.

- [ ] **Step 10: Verify and commit**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
git add -A
git commit -m "refactor(validation): Retire the gates for a deletion that never happened"
```

Expected: exit 0 and `violations=0`.

---

### Task 4: Corpus lifecycle and old-path reduction

**Files:**

- Modify: `scripts/validation/check-document-corpus-lifecycle.py` and its tests
- Modify or delete: the old-path gate and its tests

**Interfaces:**

- Consumes: the reduced gate set from Task 3.
- Produces: the narrowed predicate set that Task 5 stops calling.

- [ ] **Step 1: Enumerate every invariant the two modules enforce**

Read both modules and write one row per invariant into the Task: the invariant,
the Spec that introduced it, and the documents it currently binds. Do not
delete anything in this step.

- [ ] **Step 2: Classify each invariant against the corpus**

For each row, run the predicate against the current corpus and record whether
it binds a live document or is vacuous. A predicate whose inputs no longer
exist is retired; a predicate that still resolves a live document is retained.
Archive recovery-tuple resolution is retained by the Spec.

- [ ] **Step 3: Remove the vacuous predicates and their tests**

One commit per invariant group, each naming the migration that made it vacuous.
`docs/98.archive/migrations/0001` through `0003` are the executed record.

- [ ] **Step 4: Verify after each removal**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
python3 -m unittest discover -s tests 2>&1 | tail -5
```

Expected: exit 0 and OK after every commit, not only at the end.

- [ ] **Step 5: Record the line-count delta**

```bash
find scripts -name '*.py' | xargs wc -l | tail -1
find tests -name '*.py' | xargs wc -l | tail -1
```

Record before and after. The Task's measure of success is the list of retired
guarantees; the line count is a secondary observation.

---

### Task 5: Provenance narrowing

**Files:**

- Modify: `scripts/lib/document_governance/git_provenance.py`, `identity_history.py`, `provenance_policy.py`
- Modify: `docs/98.archive/README.md`

- [ ] **Step 1: Enumerate every caller of the three modules**

```bash
for m in git_provenance identity_history provenance_policy; do
  echo "=== $m ==="; grep -rln "$m" scripts tests | sort
done
```

Record the list. Task 4 will already have removed some callers.

- [ ] **Step 2: Identify the one behavior that survives**

Only two documents carry `archived_commit` and `archived_blob`. The surviving
behavior is resolving that tuple to a Git blob. Everything else in 1,499 lines
exists for a design the Spec records as already superseded.

- [ ] **Step 3: Write the collapsed module against a failing test**

Write the test for tuple resolution first, run it against the new module and
expect failure, then implement.

- [ ] **Step 4: Remove the commit literal from `docs/98.archive/README.md`**

State the recovery procedure in terms of the frontmatter tuple the tombstone
carries. A normative document may not pin a commit as a permanent procedure;
that is the SHA-tracking complexity this Spec removes.

- [ ] **Step 5: Verify**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
grep -rn "f259c139" docs || echo "no commit literal in docs"
```

Expected: exit 0 and no match.

---

### Task 6: Taxonomy-wave enforcement and Stage 04 literals

**Files:**

- Modify: `scripts/lib/document_governance/metadata_validator.py` — the advisory `ProfileError` guard and `planned_partitions`

- [ ] **Step 1: Confirm the corpus is clean before deciding the migration complete**

```bash
python3 scripts/validation/check-document-metadata.py 2>&1 | tail -3
```

Expected: exit 0 with zero `invalid-status`. SPEC-0154 delivered this; confirm
it still holds rather than assuming it.

- [ ] **Step 2: Remove the advisory guard**

```bash
grep -n "remains advisory until corpus migration" scripts/lib/document_governance/metadata_validator.py
```

Delete the guard so the full inventory blocks. Record the completion judgement
and its evidence in the Task.

- [ ] **Step 3: Replace the Stage 04 partition literals**

```bash
grep -n "planned_partitions" -A 8 scripts/lib/document_governance/metadata_validator.py
```

Replace `docs/04.execution/plans` and `docs/04.execution/tasks` with the
co-located Spec Package paths that replaced them.

- [ ] **Step 4: Verify**

```bash
grep -rn "04.execution" scripts || echo "no Stage 04 literal in scripts"
python3 scripts/validation/check-document-metadata.py
python3 scripts/validation/run-ci-gate.py --profile full
```

Expected: no match, exit 0, exit 0. The full inventory now blocks; if it
reports anything, fix the corpus rather than restoring the guard.

---

### Task 7: Generated evidence deduplication

**Files:**

- Modify or merge: six files under `docs/90.references/data/`
- Modify: the generators that write them

- [ ] **Step 1: Diff each pair before merging**

```bash
for pair in "0066-foundation-summary 0067-foundation" \
            "0068-target-surface-convergence-summary 0069-target-surface-convergence" \
            "0073-target-surface-delta-manifest 0074-target-surface-delta-summary"; do
  set -- $pair
  echo "=== $1 vs $2 ==="
  ls docs/90.references/data/ | grep -E "^($1|$2)"
done
```

Record what each file measures. A pair that measures different things is not
merged; the Spec's list is a hypothesis to verify, not an instruction.

- [ ] **Step 2: Regenerate the merged snapshot and diff it against both sources**

Confirm no measurement is lost before removing either source.

- [ ] **Step 3: Add `generated_by` to every generator-written snapshot**

```bash
grep -L "generated_by" docs/90.references/data/*.md
```

Record which of those a generator actually writes; a hand-authored file does
not gain the field.

- [ ] **Step 4: Verify**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/check-document-links.py --mode all
```

Expected: exit 0 for both.

---

### Task 8: Gate framework sweep and merge

**Files:**

- Modify: `scripts/validation/ci_gate_contract.py`, `scripts/validation/ci_gate_runner.py`, and their tests, only where Tasks 3 to 5 left a node without an implementation

- [ ] **Step 1: Find nodes without an implementation**

```bash
python3 scripts/validation/run-ci-gate.py --profile full --explain
python3 scripts/validation/check-script-manifest.py
```

Record the node and leaf counts. SPEC-0154 measured 53 leaf nodes and 28 job
nodes; record the new figures.

- [ ] **Step 2: Remove orphaned nodes and the tests that assert them**

No orchestration redesign. Only nodes and assertions left dangling by the
earlier Tasks.

- [ ] **Step 3: Run the full acceptance set**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/check-script-manifest.py
python3 -m unittest discover -s tests 2>&1 | tail -5
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
bash scripts/operations/sync-provider-surfaces.sh --check && git diff --exit-code
```

Expected: exit 0 for every command.

- [ ] **Step 4: Record the final line-count delta**

```bash
find scripts -name '*.py' | xargs wc -l | tail -1
find tests -name '*.py' | xargs wc -l | tail -1
```

Against the Spec's recorded 50,640 and 58,553.

- [ ] **Step 5: Close both Spec Packages**

Transition SPEC-0155 to `completed` and record the retired-guarantee ledger in
its Tasks.

- [ ] **Step 6: Merge to `main` and clean up**

```bash
python3 scripts/validation/run-ci-gate.py --profile full
git checkout main
git merge --no-ff docs/0154-governance-consistency-convergence
python3 scripts/validation/run-ci-gate.py --profile full
```

Merge only after the pre-merge gate exits 0, and re-run it on `main` after the
merge. If the post-merge run fails, the merge is reverted rather than patched
forward. Deleting the branch and pruning worktrees happens after the post-merge
gate passes, and the push to `main` is the operator's, not the agent's.

## Risk and Rollback

| Risk                                                          | Guardrail                                                                                                        | Rollback                                                        |
| :------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| A gate node loses its implementation mid-Task                 | `check-script-manifest.py` and the gate contract tests run after every removal, not only at Task end             | `git revert` the single removal commit                          |
| A removal drops a guarantee a live document needs             | Every removal names its guarantee and the document set it covered before the deletion commit                     | `git revert`; the guarantee row identifies what to restore      |
| `init_git` changes break unrelated fixtures                   | Task 1 Step 10 runs the whole module, not the target test                                                        | `git revert` Task 1 Steps 6 and 8 independently                 |
| The free-form declaration hides a real contract violation     | `required_sections: ["Related Documents"]` is retained, so the one universal obligation still blocks             | Remove `free_form_sections` from the profile                    |
| A transition override is used to paper over a lifecycle error | Every override row carries `approval` and `reason` naming the correction, and its `evidence_task` is a real Task | Remove the row; the finding returns                             |
| SPEC-0137 is retired while its `active` Task still has work   | Disposition is read from Task evidence and written down before any module is deleted                             | `git revert` the disposition commit before the deletion commits |
| `main` receives a failing tree                                | Task 8 Step 6 gates the merge and re-runs on `main` after it                                                     | `git revert -m 1` the merge commit                              |

## Verification

Each Task ends with `python3 scripts/validation/run-ci-gate.py --profile full`
at exit 0 and `python3 scripts/validation/check-document-metadata.py --mode
check-changed --base-ref "$(git merge-base main HEAD)"` at `violations=0`.
Neither is satisfied by the advisory inventory.

SPEC-0155 acceptance items 1 to 14 are the Spec Package's completion condition.
Tasks 1 and 2 satisfy items 1, 2, 11, 12, and 13; Task 3 satisfies items 3 and
14; Tasks 4 and 5 satisfy items 5 and 9; Task 6 satisfies items 6 and 7; Task 7
satisfies item 8; Task 8 satisfies items 4 and 10.

## Rulings

1. **The blocking mode is the acceptance condition.** Carried from SPEC-0154
   Task 6. `check-document-metadata.py` with no mode is advisory and exits 0
   while CI fails. Every step in this plan that verifies metadata names
   `--mode check-changed` explicitly.
2. **A fix that cannot be measured is not a fix.** Carried from SPEC-0154 Task 6. Every registry or validator change records the failing count before and
   after in the same Task row. A commit message may not claim an effect that no
   measurement showed.
3. **Registry edits are targeted text replacements.** Carried from SPEC-0154.
   `json.dumps` re-serialization reformats 2,021 lines and buries the change.
4. **`sync-provider-surfaces.sh` is never called bare.** Carried from
   SPEC-0154. Its default is `--check`, which exits 1 on drift and writes
   nothing. Use `--write` to regenerate and `--check` to verify.
5. **This repository runs `unittest`.** `pytest` is not installed. Every test
   command in this plan uses `python3 -m unittest`.
6. **A gate node is removed before its module.** A profile pointing at an
   absent implementation fails in a way that hides whatever came next, which is
   the failure mode Task 1 spends three defects untangling.
7. **Generated snapshots are regenerated after staging, never before.**
   `generate-llm-wiki.py` reads the files Git tracks, so a document written but
   not yet staged is absent from the index it writes, and the same document is
   present the moment it is committed. Every Task ends
   `git add -A`, then `generate-llm-wiki.py --write`, then `git add -A`, then
   commit. Regenerating before staging produces a snapshot that the freshness
   gate rejects on the very next run.

8. **A unittest verdict is read from its summary, never from `tail -1`.**
   A module under test prints to stdout, so the last line of a run is often the
   checker's own output rather than `OK` or `FAILED`. Read the `Ran N tests`
   line and the verdict beneath it. Task 4 recorded a failing module as passing
   for exactly this reason.

9. **The old content yields.** Where a retired gate, predicate, or literal
   conflicts with the current corpus, the gate is retired rather than the
   corpus reshaped to satisfy it.

## Related Documents

- [Specification](spec.md)
- [Governance consistency convergence](../0154-governance-consistency-convergence/spec.md)
- [Agentic research pack rebuild](../0137-agentic-research-pack-rebuild/spec.md)
- [Quality standards](../../00.agent-governance/policies/quality-standards.md)
- [Task checklists](../../00.agent-governance/policies/task-checklists.md)
