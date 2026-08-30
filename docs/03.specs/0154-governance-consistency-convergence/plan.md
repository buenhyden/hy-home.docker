---
profile_id: plan
status: draft
artifact_id: plan-0154
artifact_type: plan
parent_ids: [SPEC-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Governance Consistency Convergence Plan

## Objective

Execute SPEC-0154 as five reviewable Tasks that leave Stage 00 free of
contradicting statements, give the `spec` profile a terminal status, remove the
retired Stage 04 taxonomy from active documents, resolve 817 dead links, and
widen the link gate to the corpus it is supposed to protect.

The plan adds no validator, fixture, or gate node. Every change is a document
edit, a Stage 99 registry edit, or a selection constant.

## Dependencies

**Spec.** `spec.md` in this package. Executors read both documents.

**Global constraints, copied from the Spec and from Stage 00.**

- Stage 00 is English-only. Stage 03 documents in this repository are English.
- Agents never invoke `pre-commit run`, `npm run lint`, or an ad hoc formatter.
  The only approved all-files path is
  `bash scripts/validation/run-agent-precommit-all-files.sh`.
- `.agents/`, `.claude/`, and `.codex/` are generated. Never hand-edit them;
  regenerate with `bash scripts/operations/sync-provider-surfaces.sh`.
- Documentation-only work has no red-green cycle. `roles/qa.md` states that TDD
  is N/A for governance-only work and that the Task still needs
  repository-contract, traceability, diff hygiene, and manual evidence. Each
  Task below therefore captures validator output before and after the change.
- Commits are Conventional Commits, one logical unit each.
- Evidence fields are `command`, `result`, `rollback`, `skipped_checks`. Never
  record secret values, raw logs, tokens, or shell history.

**Task order.** Tasks 1 to 5 are sequential. Task 5 depends on Task 1 because
`check-document-links.py` `SUPPORT_DOCS` names `roles/qa.md`, which Task 1
deletes. Task 4 depends on Task 3 because the dispositions it applies need the
`completed` status Task 3 registers.

**Out of scope for every Task.** Validator internals, the taxonomy-wave
enforcement state, the `docs/04.execution` literals inside
`metadata_validator.py`, and everything owned by SPEC-0155 and SPEC-0156.

## Execution Sequence

### Task 1: Stage 00 canonical repair

**Files:**

- Modify: `docs/00.agent-governance/policies/quality-standards.md`
- Modify: `docs/00.agent-governance/policies/environment-constraints.md`
- Modify: `docs/00.agent-governance/policies/approval-boundaries.md`
- Modify: `docs/00.agent-governance/policies/standards.md`
- Delete: `docs/00.agent-governance/roles/{agentic,architecture,common,docs,infra,ops,qa,security}.md`

**Produces:** a `roles/` directory holding only the 14 agent roles, and policy
documents that carry every normative statement those eight files held.

- [ ] **Step 1: Capture the baseline**

```bash
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all > /tmp/0154-t1-before.txt 2>&1; echo "exit=$?"
grep -c '' docs/00.agent-governance/roles/*.md
```

Record the exit code and the per-file line counts in the Task Work Log.

- [ ] **Step 2: Move the QA content into the quality policy**

Append to `policies/quality-standards.md`, after `## 2. Security Baseline`,
these sections copied verbatim from `roles/qa.md`: the coverage floor and
applicability rule from section 2, the local-versus-remote execution boundary
including the `run-ci-precommit.sh` contract and the anti-duplication rule,
`## 3.1 Change-Type Verification Matrix`, `## 3.2 Generated-Artifact Freshness`,
and `## 3.3 Local QA/CI Orchestration`. Renumber the destination headings to
continue the destination's own numbering. Change no wording.

- [ ] **Step 3: Move the infrastructure content into the environment policy**

Append to `policies/environment-constraints.md`, after `## 1. Hard Constraints`,
copied verbatim from `roles/infra.md`: the `infra_net` and external-exposure
rule, the `[Service]-[Data]-[Volume]` naming convention, the
`no-new-privileges` and Docker Secrets requirement, the container-build review
criteria, the Compose review criteria, `### 3.1 Approved Runtime Mutation
Protocol`, and the `docker system prune` consent rule.

- [ ] **Step 4: Move the security content**

Append the identity, secrets, container-hardening, and network-hardening
constraints from `roles/security.md` section 2 to
`policies/quality-standards.md` section 2, and `### 3.1 Approved Secrets Work
Protocol` to `policies/environment-constraints.md`. Append the SEV1 and SEV2
mandatory-postmortem rule from `roles/ops.md` to
`policies/quality-standards.md`.

- [ ] **Step 5: Move the documentation permission rule**

Add to `policies/approval-boundaries.md` the three sentences from
`roles/docs.md` `## Permissions`: `doc-writer` may edit approved documentation,
all other roles are read-only unless their Task explicitly includes a
documentation update, and policy changes require `rules-engineer` review.

- [ ] **Step 6: Delete the unverified claims rather than move them**

Do not carry these into any policy. Record each in the Task as deleted with the
reason `no registered check or runbook supports the claim`:

- `roles/ops.md`: `Verified daily off-site backups for 04-data volumes`
- `roles/ops.md`: `Periodically perform disaster recovery drills (Chaos Engineering)`
- `roles/ops.md`: `Conduct quarterly architectural reviews`
- `roles/infra.md`: `Maintain a gateway-level LATENCY_SLO < 200ms`
- `roles/infra.md`: `Ensure automated backup tags are present for all persistent data volumes`

- [ ] **Step 7: Drop the retired artifact vocabulary**

In `policies/standards.md`, replace `PRD, SRS, Interface Requirement,
Architecture Description, ADR, Spec, Plan, Task, Guide, Policy, and Runbook`
with `Requirement Package, Architecture Description, ADR, Spec, Plan, Task,
Guide, Policy, and Runbook`. Remove the thin-root-shim restatement from
`policies/standards.md` section 1 and from
`policies/environment-constraints.md` section 1; `policies/bootstrap.md`
keeps the single statement.

- [ ] **Step 8: Delete the eight layer documents**

```bash
git rm docs/00.agent-governance/roles/{agentic,architecture,common,docs,infra,ops,qa,security}.md
```

- [ ] **Step 9: Repair references to the deleted files**

```bash
grep -rn "roles/\(agentic\|architecture\|common\|docs\|infra\|ops\|qa\|security\)\.md" docs .agents .claude .codex scripts AGENTS.md CLAUDE.md README.md
```

Repoint each hit at the policy that now owns the content. Leave
`scripts/validation/check-document-links.py` `SUPPORT_DOCS` for Task 5.

- [ ] **Step 10: Verify**

```bash
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all; echo "exit=$?"
python3 scripts/validation/check-document-metadata.py > /tmp/0154-t1-after.txt 2>&1; echo "exit=$?"
grep -rn "File Ownership SSOT\|Subagent Bridge\|@import" docs/00.agent-governance
```

Expected: both validators exit 0, and the third command returns no match.

- [ ] **Step 11: Commit**

```bash
git add docs/00.agent-governance
git commit -m "docs(governance): Move layer-document rules into the policies that own them"
```

### Task 2: Role and skill canonicalization

**Files:**

- Modify: `docs/99.templates/registry.json` (`profiles[governance-role]`)
- Rename: `docs/00.agent-governance/skills/code-reviewer.md` to `change-review-execution.md`
- Rename: `docs/00.agent-governance/skills/test-automator.md` to `test-authoring.md`
- Modify: `docs/00.agent-governance/roles/{code-reviewer,qa-engineer}.md`
- Regenerate: `.agents/skills/`, `.claude/skills/`

**Consumes:** a `roles/` directory holding only agent roles, from Task 1.

- [ ] **Step 1: Confirm the precondition**

```bash
for f in docs/00.agent-governance/roles/*.md; do grep -q '^agent_id:' "$f" || echo "MISSING agent_id: $f"; done
```

Expected: no output. If any file prints, Task 1 is incomplete; stop.

- [ ] **Step 2: Narrow the profile**

In `docs/99.templates/registry.json`, move `agent_id`, `scope`, `tier`,
`status`, `work_profile`, `permission_profile`, and `skill_ids` from
`profiles[governance-role].optional_frontmatter` into
`required_frontmatter`, leaving `optional_frontmatter` empty.

- [ ] **Step 3: Verify the profile change fails nothing**

```bash
python3 scripts/validation/check-document-metadata.py; echo "exit=$?"
```

Expected: exit 0, and no `governance-role` document reported under a
missing-required-key finding.

- [ ] **Step 4: Rename the colliding skills**

```bash
git mv docs/00.agent-governance/skills/code-reviewer.md docs/00.agent-governance/skills/change-review-execution.md
git mv docs/00.agent-governance/skills/test-automator.md docs/00.agent-governance/skills/test-authoring.md
```

Update the `function_id` frontmatter value inside each renamed file to match its
new slug.

- [ ] **Step 5: Update the referring roles**

In `roles/code-reviewer.md`, change the `skill_ids` entry `code-reviewer` to
`change-review-execution` and the Related Documents link
`../skills/code-reviewer.md` to `../skills/change-review-execution.md`. In
`roles/qa-engineer.md`, change `test-automator` to `test-authoring` and
`../skills/test-automator.md` to `../skills/test-authoring.md`.

- [ ] **Step 6: Regenerate the projections**

```bash
git rm -r .agents/skills/code-reviewer .agents/skills/test-automator .claude/skills/code-reviewer .claude/skills/test-automator
bash scripts/operations/sync-provider-surfaces.sh
git status --porcelain
```

Expected: the two new skill directories appear under `.agents/skills/` and
`.claude/skills/`, and no other generated file changes.

- [ ] **Step 7: Verify**

```bash
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all; echo "exit=$?"
bash scripts/operations/sync-provider-surfaces.sh && git diff --exit-code; echo "exit=$?"
grep -rn "code-reviewer\b" docs/00.agent-governance/skills .claude/skills .agents/skills
```

Expected: the first two exit 0; the third returns only role references, never a
skill identifier.

- [ ] **Step 8: Commit**

```bash
git add -A docs/00.agent-governance docs/99.templates .agents .claude
git commit -m "docs(governance): Give the runtime-routing role fields a required contract"
```

### Task 3: Lifecycle completion

**Files:**

- Modify: `docs/99.templates/registry.json` (`lifecycles`, `transitions`, `profiles[*].optional_sections`)
- Modify: `docs/00.agent-governance/providers/registry.yaml:249`
- Modify: `scripts/validation/agent_governance_contract.py:33` (`EXPECTED_GENERATED_ROOTS`)
- Modify: `docs/98.archive/migrations/000{1,2}-*.md`

**Produces:** a `completed` status for Spec Packages, a `Related Documents`
section registered on the 16 content profiles that omit it, a complete
`generated_roots` list, and a Stage 98 corpus with no invalid status.

- [ ] **Step 1: Add the lifecycle**

In `docs/99.templates/registry.json`, add to `lifecycles`:

```json
"spec-package": {
  "statuses": ["draft", "active", "completed", "superseded", "retired"],
  "transitions": {
    "draft": ["active", "retired"],
    "active": ["completed", "superseded", "retired"],
    "completed": [],
    "superseded": [],
    "retired": []
  }
}
```

Then set `transitions.spec` to `"spec-package"` and
`profiles[spec].lifecycle_id` to `"spec-package"`.

- [ ] **Step 2: Verify the lifecycle is accepted**

```bash
python3 scripts/validation/check-document-metadata.py; echo "exit=$?"
python3 -m pytest tests/lib/document_governance/test_registry.py -q; echo "exit=$?"
```

Expected: both exit 0. If the registry test pins the lifecycle set, extend that
test in the same commit and record the change in the Task.

- [ ] **Step 3: Register the missing section**

Add `"Related Documents"` to `optional_sections` for the 16 profiles that omit
it: `requirements-package`, `architecture-description`, `adr`, `spec`, `plan`,
`task`, `guide`, `policy`, `runbook`, `incident`, `postmortem`, `research`,
`audit`, `data`, `migration`, `tombstone`.

- [ ] **Step 4: Correct the Stage 98 statuses**

In `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md` and
`0002-operations-catalog-convergence.md`, change `status: archived` to
`status: completed`, matching `0003-workspace-governance-simplification.md`.

- [ ] **Step 5: Complete `generated_roots`**

In `docs/00.agent-governance/providers/registry.yaml`, extend the
`generated_roots` list to include `.agents/README.md`, `.agents/rules`,
`.agents/workflows`, `.claude/CLAUDE.md`, and `.codex/README.md`, which
`scripts/operations/provider_surface_renderer.py` lines 289 to 293 write.

- [ ] **Step 6: Verify**

```bash
python3 scripts/validation/check-document-metadata.py 2>&1 | grep -c invalid-status
bash scripts/operations/sync-provider-surfaces.sh && git diff --exit-code; echo "exit=$?"
python3 scripts/validation/run-ci-gate.py --profile full; echo "exit=$?"
```

Expected: the first prints `0`; the second and third exit 0. The renderer
compares `generated_roots` against `EXPECTED_GENERATED_ROOTS`, defined at
`scripts/validation/agent_governance_contract.py:33` and imported by
`scripts/operations/provider_surface_renderer.py:31`. If step 5 makes either
raise, extend that tuple in the same commit and update
`tests/validation/test_agent_governance_contract.py` if it pins the value.

- [ ] **Step 7: Commit**

```bash
git add docs/99.templates docs/98.archive docs/00.agent-governance scripts
git commit -m "feat(registry): Give a Spec Package a way to be finished"
```

### Task 4: Retired taxonomy removal and link repair

**Files:**

- Modify: `docs/03.specs/{0093,0094,0103,0105,0131,0134}-*/spec.md`
- Modify: `docs/README.md` (`## Migration Map`)
- Modify: `docs/90.references/audits/*/README.md`
- Modify: the 28 active `docs/03.specs/*/spec.md` frontmatter

**Consumes:** the `completed` status registered by Task 3.

- [ ] **Step 1: Capture the dead-link baseline**

```bash
python3 - <<'PY' > /tmp/0154-links-before.txt
import pathlib, re, collections
pat = re.compile(r'\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)')
dead = collections.defaultdict(list)
for p in pathlib.Path('docs').rglob('*.md'):
    for m in pat.finditer(p.read_text(errors='ignore')):
        t = m.group(1)
        if t.startswith(('http', 'mailto:')):
            continue
        if not (p.parent / t).resolve().exists():
            dead[str(p)].append(t)
print(sum(len(v) for v in dead.values()), 'dead links in', len(dead), 'files')
for k in sorted(dead):
    for t in dead[k]:
        print(k, t)
PY
head -1 /tmp/0154-links-before.txt
```

Expected first line: `817 dead links in 93 files`.

- [ ] **Step 2: Rewrite the Stage 04 passages**

In each of `0093`, `0094`, `0103`, `0105`, `0131`, and `0134`, replace every
statement that describes `Stage 04` or `docs/04.execution` as current procedure
with the co-located model: Plans live at
`docs/03.specs/####-<slug>/plan.md` and Tasks at
`docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md`. Where a passage records
what was true at the time, keep it and mark it as historical evidence using the
blockquote form that `policies/documentation-protocol.md` defines.

- [ ] **Step 3: Delete the parallel redirect table**

Remove the `## Migration Map` section and its eleven rows from
`docs/README.md`. Replace it with one sentence pointing at
`docs/98.archive/migrations/`.

- [ ] **Step 4: Repair links by pattern, one commit per class**

```bash
grep -rln 'ref-[0-9]\{4\}-[a-z0-9-]*\.md' docs/90.references
```

Apply each class separately and review its diff before the next:
`ref-####-*.md` to `####-*/README.md` (300),
`00.agent-governance/rules/` to `00.agent-governance/policies/` (96),
`03.specs/spec-####-` to `03.specs/####-` (18),
`99.templates/support/` to `99.templates/` (15).

- [ ] **Step 5: Repair the remaining links by inspection**

Re-run the step 1 script. For each surviving entry, either repoint it at the
current path or, when the target is genuinely gone, remove the link and state
what it referenced. The 72 repository-file targets and the 316 individual cases
belong here.

- [ ] **Step 6: Apply the Stage 90 and Spec Package dispositions**

For each of the 38 Stage 90 audit packs and the 28 active Spec Packages, apply
the SPEC-0154 disposition rule: `completed` when every Task is `completed` or
`cancelled` and the outcome is in canonical documents, `superseded` with
`superseded_by` when a successor absorbed it, `retired` when neither, and
`active` only when work is in flight. Record the judgement per package in the
Task.

- [ ] **Step 7: Verify**

```bash
python3 - <<'PY'
import pathlib, re
pat = re.compile(r'\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)')
n = 0
for p in pathlib.Path('docs').rglob('*.md'):
    text = p.read_text(errors='ignore')
    if re.search(r'^status:\s*superseded', text, re.M):
        continue
    for m in pat.finditer(text):
        t = m.group(1)
        if t.startswith(('http', 'mailto:')):
            continue
        if not (p.parent / t).resolve().exists():
            n += 1
            print('DEAD', p, t)
print('remaining:', n)
PY
grep -rn "Stage 04\|docs/04.execution" docs --include='*.md'
python3 scripts/validation/check-document-metadata.py; echo "exit=$?"
```

Expected: `remaining: 0`; the `Stage 04` grep returns hits only inside
`superseded` or `completed` documents; the validator exits 0.

- [ ] **Step 8: Commit**

Commit each pattern class from step 4 separately, then the inspection repairs,
then the dispositions.

```bash
git commit -m "docs(references): Repoint retired reference paths at their current leaves"
git commit -m "docs(specs): Replace the retired Stage 04 model with the co-located package"
git commit -m "docs(lifecycle): Retire the packages that finished"
```

### Task 5: Gate scope correction

**Files:**

- Modify: `scripts/validation/check-document-links.py:25-40`
- Modify: `tests/lib/document_governance/test_links.py`

**Consumes:** a corpus with zero dead links, from Task 4.

- [ ] **Step 1: Write the failing test**

Add to `tests/lib/document_governance/test_links.py`:

`check-document-links.py` has a hyphen in its name, so it cannot be imported by
module name. `tests/lib/document_governance/test_links.py` already loads
hyphenated CLIs with `importlib.util.spec_from_file_location`; follow that
pattern and reuse the module-level `CLI` constant at line 18.

```python
def load_links_cli():
    spec = importlib.util.spec_from_file_location("task10_document_links", CLI)
    if spec is None or spec.loader is None:
        raise RuntimeError("link validator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class LinkSelectionScopeTests(unittest.TestCase):
    def test_selection_covers_every_tracked_markdown_root(self) -> None:
        module = load_links_cli()
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            expected = (
                "docs/00.agent-governance/policies/x.md",
                "docs/90.references/audits/0001-a/README.md",
                "docs/98.archive/migrations/0001-a.md",
            )
            for relative in expected:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# x\n")
            selected = {
                path.relative_to(root).as_posix() for path in module._paths(root)
            }
            for relative in expected:
                self.assertIn(relative, selected)

    def test_selection_skips_superseded_documents(self) -> None:
        module = load_links_cli()
        with tempfile.TemporaryDirectory() as raw:
            root = pathlib.Path(raw)
            target = root / "docs/90.references/audits/0002-b/README.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("---\nstatus: superseded\n---\n\n# b\n")
            selected = {
                path.relative_to(root).as_posix() for path in module._paths(root)
            }
            self.assertNotIn("docs/90.references/audits/0002-b/README.md", selected)
```

- [ ] **Step 2: Run it and confirm it fails**

```bash
python3 -m pytest tests/lib/document_governance/test_links.py -k LinkSelectionScope -q
```

Expected: both tests FAIL. `test_selection_covers_every_tracked_markdown_root`
fails because `DOC_ROOTS` names only `docs/01.requirements`,
`docs/02.architecture`, `docs/03.specs`, and `docs/05.operations`.
`test_selection_skips_superseded_documents` fails because `_paths` reads no
frontmatter.

- [ ] **Step 3: Widen the selection**

In `scripts/validation/check-document-links.py`, replace `DOC_ROOTS` and
`SUPPORT_DOCS` with a single selection over `docs/**/*.md` plus the tracked
root-level `README.md` and `scripts/README.md`, and skip any document whose
frontmatter carries `status: superseded`.

- [ ] **Step 4: Run the test and confirm it passes**

```bash
python3 -m pytest tests/lib/document_governance/test_links.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the gate at full scope**

```bash
python3 scripts/validation/check-document-links.py --mode all; echo "exit=$?"
```

Expected: the `documents=` count is the full non-superseded corpus rather than
345, and `failures=0`.

- [ ] **Step 6: Run the registered gate**

```bash
python3 scripts/validation/run-ci-gate.py --profile full; echo "exit=$?"
python3 scripts/validation/run-ci-gate.py --profile changed; echo "exit=$?"
```

Expected: both exit 0.

- [ ] **Step 7: Commit**

```bash
git add scripts/validation/check-document-links.py tests/lib/document_governance/test_links.py
git commit -m "fix(validation): Read the corpus the link gate is supposed to protect"
```

## Risk and Rollback

| Risk | Detection | Rollback |
| :--- | :--- | :--- |
| A normative statement is lost when a layer document is deleted | Task 1 step 10 greps the destination policies for each moved heading before the delete lands | `git revert` the Task 1 commit; the source files return intact |
| Task 1 breaks the link gate through `SUPPORT_DOCS` | Task 1 step 10 runs `check-document-metadata.py`; the link gate is repaired in Task 5 | Restore the `roles/qa.md` entry until Task 5 lands |
| Narrowing `governance-role` fails an agent role that lacks a field | Task 2 step 3 runs the metadata validator before any rename | Revert the registry hunk; the fields return to optional |
| The renderer rejects the extended `generated_roots` | Task 3 step 6 runs the renderer and diffs | Revert the registry hunk and update `EXPECTED_GENERATED_ROOTS` first |
| A bulk pattern rewrite corrupts a correct link | Each class is its own commit with its own diff review | `git revert` that one commit |
| A package is marked `completed` while work remains | Step 6 requires a per-package judgement recorded in the Task | Transition back to `active`; `spec-package` allows no exit from `completed`, so the revert is a commit revert |
| Widening the link gate turns the gate red | Task 5 runs only after Task 4 reports zero dead links | Revert the selection change; the gate returns to its prior scope |

## Verification

Run at the end of Task 5, in this order.

```bash
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
python3 scripts/validation/check-document-metadata.py
python3 scripts/validation/check-document-links.py --mode all
bash scripts/operations/sync-provider-surfaces.sh && git diff --exit-code
python3 -m pytest tests/lib/document_governance -q
python3 scripts/validation/run-ci-gate.py --profile full
python3 scripts/validation/run-ci-gate.py --profile changed
```

All must exit 0. Then confirm the Spec's acceptance items that no command
covers:

```bash
grep -rn "PRD, SRS" docs/00.agent-governance
grep -rn "Stage 04\|docs/04.execution" docs --include='*.md'
for f in docs/00.agent-governance/roles/*.md; do grep -q '^agent_id:' "$f" || echo "MISSING $f"; done
```

Expected: no match, matches only inside `superseded` or `completed` documents,
and no missing `agent_id`.

## Rulings

1. **Documentation-only work has no red-green cycle.** `roles/qa.md` states this
   and the content moves to `policies/quality-standards.md` in Task 1. Tasks 1
   to 4 capture validator output before and after instead. Task 5 changes code
   and does follow red-green.
2. **Moved content is copied verbatim.** Rewording during a move makes the
   review unable to tell a move from an edit. Wording changes, if any, are a
   separate commit after the move lands.
3. **Unverified claims are deleted, not relocated.** A claim with no registered
   check and no runbook is not policy. Each deletion is named in the Task.
4. **The link gate widens last.** It is the measurement of the other four Tasks,
   so it changes only after they are done.

## Related Documents

- [Specification](spec.md)
- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
- [Task checklists](../../00.agent-governance/policies/task-checklists.md)
- [Stage 99 registry](../../99.templates/registry.json)
