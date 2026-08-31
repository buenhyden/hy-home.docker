---
profile_id: plan
status: active
artifact_id: plan-0158
artifact_type: plan
parent_ids: [SPEC-0158]
created: 2026-08-31
updated: 2026-09-01
---

# Document Governance Lifecycle Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to execute this plan one task at a time.

**Goal:** Converge the current documentation corpus on one lifecycle, one owner
per rule, minimal historical recovery, and a smaller validation surface after
SPEC-0157 is honestly completed.

**Architecture:** Apply lifecycle-first staged convergence. Restore the active
execution chain, classify the measured corpus with non-overlapping rules,
repair canonical owners before deleting evidence, then simplify Gates,
fixtures, and Git provenance without changing the six public suite
responsibilities.

**Tech Stack:** Markdown and YAML/JSON governance sources, Python 3.12
`unittest`, shell entrypoints, Git regular-blob recovery, and the repository's
registered `changed` and `full` validation profiles.

**Spec:** [SPEC-0158](spec.md)

## Objective

### Global Constraints

- SPEC-0157 must be `completed` and its Plan and Task terminal before
  SPEC-0158 changes from `draft` to `active`.
- Treat the SPEC-0157 merge boundary as a lifecycle boundary: land its
  `draft -> active` implementation first, then close it from an updated base
  with `active -> completed`. Do not use an override to collapse the endpoints.
- Do not add a stage, document lifecycle, disposition lifecycle, public suite,
  public Gate profile, audit pack, progress file, redirect, or body copy.
- Keep the ADR-0029 public suites and the `changed|full` profiles stable.
- Treat `keep`, `rewrite`, `consolidate`, `supersede`, `delete`, and
  `tombstone` as Task-local decisions, never Registry statuses.
- Cover unchanged documents by deterministic cohort rule. List every
  non-`keep` path explicitly; do not create a 1-row-per-file corpus copy.
- Before any Stage 90 disposition, assign the Task-local preservation class
  `PROTECT_LATEST` atomically to every baseline file in
  `docs/90.references/research/0002-agentic-engineering-research-pack/`.
  This user override survives zero consumers and is not a Registry status.
- Before the current Task can be compressed or removed, Task 6 must migrate its
  dynamic protected path inventory into the `RES-0002` package README and make
  the existing reference/document-governance test oracle GREEN.
- Treat every other execution-baseline Stage 90 Research, Audit, or Data
  package as a mandatory terminal disposition. Migrate current consumers,
  unique needed meaning, citations, or generated outputs to canonical owners,
  then delete the package. Completion requires zero unresolved or pending
  dispositions and a package-root set containing only `RES-0002`; root and
  category READMEs are structural indexes and are excluded from that set.
- Treat Migration 0001--0003 as temporary historical inputs. Move every current
  consumer to its canonical owner, then delete the documents and
  `docs/98.archive/migrations/` before completion.
- Keep supply-chain digests, CI event SHAs, regular-blob recovery commits, and
  actual logical Task commits. Remove expected lineage and test-only pins.
- Preserve policy-required ephemeral digest comparison for concurrent
  worktrees; do not persist it as a document lineage ledger.
- When predecessor content conflicts with current canonical governance, prefer
  the current owner and discard the obsolete rule after recovery review.
- Treat tracked implementation as the observation source for current truth:
  implemented obligations map to Stage 01, implemented structures and durable
  decisions map to Stage 02, and neither Stage 03 execution detail nor Stage 05
  procedure nor Stage 90 evidence may remain their sole durable owner.
- Run focused tests before aggregate Gates. Record observed output in the
  current Task and never infer a pass from missing or truncated output.
- Make no runtime, deployment, remote, secret, credential, or infrastructure
  mutation.
- Use logical Conventional Commits and compute the base with
  `git merge-base main HEAD`; never pin an expected branch tip.

---

### Intended Outcome

Audit and converge the tracked documents under Stages 00, 01, 02, 03, 05, 90,
98, and 99, including work in progress. Current owners are repaired first.
Duplicate, contradictory, obsolete, Legacy, and Deprecated material is then
rewritten, consolidated, superseded, or deleted. Stage 98 retains only its
structural index and minimal archive/Tombstone records required by an explicit
preservation need or measured live recovery-navigation consumer; it retains no
Migration package. Validators retain one source for inventory and one predicate
per guarantee.

The result must make SDLC state honest: an active Task has active parents,
terminal parents have no active children, only actual work remains active, and
completed change packets write their outcomes to current owners rather than
remaining a second authority. Stage 01 and Stage 02 also describe the current
implemented system rather than only desired future state: every implemented
obligation and structure has one canonical owner, and every statement presented
as current agrees with tracked implementation.

## Dependencies

- [SPEC-0157](../0157-script-surface-ownership-convergence/spec.md) and its
  [corrected Plan](../0157-script-surface-ownership-convergence/plan.md).
- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md),
  [REQ-0025](../../01.requirements/0025-operational-readiness-closure.md), and
  [ADR-0029](../../02.architecture/decisions/0029-workspace-governance-authority.md).
- Stage 00 bootstrap, approval, workflow, documentation, authoring, and SDLC
  policies.
- Stage 99 Registry, schemas, and registered templates.
- `scripts/manifest.yaml` for validator inventory and suite membership.
- `.github/workflow-contract.yml` for CI routing and execution context.
- Current tracked implementation under `infra/`, `examples/`, `scripts/`,
  provider adapters, registries, manifests, workflows, tests, and Stage 05
  operational commands.
- Current Git-tracked consumers and regular-blob recovery measured at execution
  time.

### Conflict Review Baseline

| Confirmed conflict | Corrected ruling used by this Plan |
| :--- | :--- |
| SPEC-0157 implementation exists while its Spec and Plan are `draft` and no Task exists | Activate through the legal transition, record earlier commits as discovered and revalidated, and never claim retroactive approval |
| SPEC-0157 proposed copying historical document blobs into fixtures | Current contract fixtures derive from Stage 99 and recovery fixtures use temporary Git; no current contract test reads an archive document |
| A one-row-per-document disposition ledger would become another large audit pack | Ordered cohort rules cover `keep`; every non-`keep` path is explicit |
| The earlier Stage 98 design made six Migration sections a permanent contract | Treat Migration documents as temporary convergence inputs, remove their active Registry contract, and delete them after consumer handoff |
| Stage 05 membership delegates current truth to an Operations migration manifest | Derive current membership from Stage 05 plus Stage 99; remove every Migration dependency before deletion |
| Provider registry workflow states grant mutation to read-only roles and restate provider-neutral policy | Keep neutral workflow order in Stage 00 and provider runtime translation in the provider registry |
| Generated `.agents/rules` and `.agents/workflows` have no tracked consumer | Remove those projections and their managed roots; retain only proven native or navigation projections |
| `suite_registry.py` repeats a Task-numbered immutable validator map | Derive validator rows and membership from `scripts/manifest.yaml` |
| Lifecycle and Operations expose overlapping modes and routes | Retain one complete CLI behavior per validator after equivalence tests; keep recovery as part of lifecycle validation |
| Persistent digest removal could weaken concurrent-worktree safety | Remove lineage ledgers, not ephemeral policy-required comparison |
| A later link-only Git touch can be mistaken for the latest saved external research | Classify each relevant diff as content authoring or mechanical path/link correction; do not select preservation by maximum timestamp |
| Current Stage 90 existence is coupled to Migration 0003's frozen historical target set | Decouple current retention in `references.py` before deletion; Git owns the retired Migration history and no deleted package receives a Tombstone without a live recovery-navigation consumer |
| ADR-0029 and Stage 99 still register Migration 0003 as a structural authority | Move the review boundary to current Registry, Task, and validator evidence, correct ADR-0029, remove the active Migration profile/template/allocation surface, then delete the Migration package |
| Current Stage 00/01/02/03/05/90 documents and generated indexes cite or link to Stage 98 files | Move current meaning to canonical owners, remove every inbound archive-file citation/link, and keep recovery navigation one-way from retained archive records to current replacements |
| Current implementation is described only by code, a completed Spec, an Operations procedure, a validator, or Stage 90 evidence while Stage 01/02 is absent or stale | Build a subject-level bidirectional coverage inventory; promote obligations to Stage 01 and structures or durable decisions to Stage 02, then correct any current claim that contradicts implementation |
| Preliminary Stage 90 classification found 25 deletion candidates and 39 migration-dependent packages | Treat both counts as discovery evidence only; Task 2 remeasures the current tree and acceptance never pins either count |
| Task 2 is the only source for the protected path inventory even though Task 8 retires Task bodies | Before retirement, write the dynamic set to a package-local non-normative README declaration and derive the existing reference-test oracle from it |

### Role and Evidence Assignment

| Responsibility | Owner | Boundary |
| :--- | :--- | :--- |
| Approval | user or operator | Grants the named scope; no agent substitutes for approval |
| Sequence, stop conditions, and handoff | `workflow-supervisor` | Read-only coordination |
| Canonical documentation edits | `doc-writer` | Approved document paths only |
| Deterministic tests and Gate implementation | `qa-engineer` | Approved test and validation paths |
| Task evidence | actual Task owner | Records its own observed work and commits |
| Evaluation | `eval-engineer` | Read-only verdict; no evidence impersonation |
| Governance conformity | `rules-engineer` | Read-only policy verdict; not approval |
| Exact diff review | `code-reviewer` | Independent and read-only |
| Hooks, CI, or security review | relevant protected-surface role | Only when that surface changes |

### File and Ownership Map

| Area | Primary files | Target ownership |
| :--- | :--- | :--- |
| Execution recovery | `docs/03.specs/0157-*/` | Existing SPEC-0157 Plan and current Task |
| Current work packet | `docs/03.specs/0158-*/` | SPEC-0158 Spec, Plan, and one current Task |
| Neutral governance | `docs/00.agent-governance/{policies,roles,skills}/` | Stage 00 prose contracts |
| Provider facts | `docs/00.agent-governance/providers/registry.yaml` | Provider, model, permission translation, hook, and projection routing |
| Document mechanics | `docs/99.templates/registry.json`, schemas, templates | Stage 99 typed document authority |
| Current solution truth | Stages 01, 02, 03, and 05 plus tracked implementation subjects | Stage 01 owns implemented obligations, Stage 02 owns implemented structure and durable decisions, Stage 03 owns change deltas, and Stage 05 owns procedures with Stage 01/02 prerequisites |
| Evidence | `docs/90.references/` | The atomic user-protected latest external-research pack plus structural indexes matching the resulting tree; all other baseline evidence packages migrate and retire |
| Protected research declaration | `docs/90.references/research/0002-agentic-engineering-research-pack/README.md` | Persistent non-normative protected path selector and user-decision record; SPEC-0158 acceptance owns the retention rule |
| Recovery | `docs/98.archive/` | Minimal approved archive/Tombstone records plus the structural index; no Migration directory at completion |
| Validator inventory | `scripts/manifest.yaml` | Validator path, suite, argv, context, tests, and consumers |
| Execution routing | `.github/workflow-contract.yml` | CI profiles and routing only |
| Predicates | `scripts/lib/**`, `scripts/validation/**` | One implementation per guarantee |

## Execution Sequence

### Prerequisite P0: Complete SPEC-0157 before activating SPEC-0158

**Files:**

- Execute: `docs/03.specs/0157-script-surface-ownership-convergence/plan.md`
- Create during that execution:
  `docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md`
- Modify only the files owned by Tasks 0 through 9 in that Plan.

**Steps:**

1. Execute SPEC-0157 Task 0 to create the legal active parent chain and record
   the earlier branch commits as discovered work.
2. Reopen Task 2 to replace the fixed Spec Package count exposed by SPEC-0158
   with the directory-to-loader set relation specified in the corrected Plan.
3. Revalidate the already-landed Tasks 1 through 3; mark them complete only
   after their focused checks pass.
4. Execute corrected Tasks 4 through 9. Task 6 must not copy a historical body
   into `tests/fixtures/` and must preserve regular-blob recovery tests.
5. Obtain independent governance and exact-diff review and run the full
   profile. If the merge base still contains SPEC-0157 as `draft`, complete its
   Plan and Task but leave its Spec `active`.
6. Stop at the merge boundary. Merge only with explicit user authorization.
   After the activation and implementation land, start from the updated
   `main`, transition SPEC-0157 from `active` to `completed` in a dedicated
   closure commit, and rerun the focused and full checks.
7. Continue to Task 1 only after the current tree contains completed SPEC-0157
   and the changed-document Gate observes the legal `active -> completed`
   endpoint.

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/run-ci-gate.py --profile full
```

Expected: every command exits 0. Stop here if SPEC-0157 or its execution
children remain non-terminal, or if the closure base did not already contain
the Spec as `active`.

---

### Task 1: Activate SPEC-0158 with one bounded current Task

**Files:**

- Modify: `docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md`
- Modify: `docs/03.specs/0158-document-governance-lifecycle-convergence/plan.md`
- Create: `docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md`
- Modify: `docs/03.specs/README.md`

**Step 1: Verify the prerequisite state**

```bash
rg -n "^status:|^artifact_id:" \
  docs/03.specs/0157-script-surface-ownership-convergence/spec.md \
  docs/03.specs/0157-script-surface-ownership-convergence/plan.md \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks/*.md
```

Expected: the Spec, Plan, and every Task are terminal and no Task is `active`.

**Step 2: Create the Task from the registered template**

Use this exact frontmatter and required section envelope:

```markdown
---
profile_id: task
status: active
artifact_id: task-0158-0001
artifact_type: task
parent_ids: [SPEC-0158, plan-0158]
created: 2026-08-31
updated: 2026-08-31
---

# Converge Document Governance by Lifecycle

## Objective

Classify the approved target corpus, repair current owners, remove obsolete
authority, simplify validation, and close the packet with observed evidence.

## Inputs

- SPEC-0158 and plan-0158.
- Completed SPEC-0157 evidence.
- Current Stage 00, Stage 99, manifest, workflow, and Git recovery authorities.

## Work Log

Execution has not started. The first entry records the clean baseline and the
complete disposition rule coverage before corpus mutation.

## Verification Evidence

Pending focused RED/GREEN and aggregate Gate observations.

## Review Evidence

Pending independent governance and exact-diff review.

## Commit Ledger

No SPEC-0158 implementation commit recorded yet.

## Rulings

Disposition values are Task-local decisions and do not extend Registry
lifecycle values.

## Deferred Items

Runtime, deployment, remote, secret, and infrastructure state are out of scope.
```

Set the Spec and Plan from `draft` to `active`. Add the Plan and Tasks links to
the Stage 03 index. Do not create a second Task, audit pack, or progress file.

**Step 3: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
git diff --check
```

Expected: `violations=0`, `violations=0`, `failures=0`, and no diff error.

```bash
git add docs/03.specs/0158-document-governance-lifecycle-convergence docs/03.specs/README.md
git commit -m "docs(spec): Activate document governance convergence"
```

---

### Task 2: Establish complete disposition-rule coverage before mutation

**Files:**

- Modify only:
  `docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md`

**Step 1: Re-derive the target set**

Measure tracked Markdown under the eight approved stage roots. Record the
per-stage counts and total in the Task as observed evidence, not constants.

```bash
git ls-files \
  'docs/00.agent-governance/**' \
  'docs/01.requirements/**' \
  'docs/02.architecture/**' \
  'docs/03.specs/**' \
  'docs/05.operations/**' \
  'docs/90.references/**' \
  'docs/98.archive/**' \
  'docs/99.templates/**' | rg '\.md$' | sort -u
```

Do not copy the full output into the Task. Record the command, revision, stage
counts, total, and the rule coverage summary.

Before constructing any Stage 90 disposition cohort, enumerate every tracked
file currently under
`docs/90.references/research/0002-agentic-engineering-research-pack/` and
assign the Task-local preservation class `PROTECT_LATEST` to the entire set as
one atomic selector. The design baseline observes 21 files, but execution must
record the actual path set and must not turn `21` into a frozen count Gate or
acceptance pin. A protected path may receive a `keep`, `rewrite`, `supersede`,
or non-lossy integration disposition, but never `delete`, `tombstone`, archive,
or substantive body/source/claim reduction.

Classify relevant Git touches by inspecting their diffs and purpose, not by
choosing `max(timestamp)`. The design evidence distinguishes draft promotion
and activation at `95142c3a`; the later restore-and-merge of substantive
content across all 21 files at `07b94403`; later claim-bearing corrections at
`3bf50f94`; the last new-leaf addition at `65e8dfde`; and the three-link-only
destination correction at `6663f02c`. Other later governance or path edits may
exist. Record these as illustrative provenance only, never as final protected
content, a restore target, expected branch SHA, checksum, retention baseline,
or new Gate input. The sole preservation subject is the entire tracked current
execution-baseline package remeasured by this Task. Likewise, the preliminary
25 `DELETE_CANDIDATE` and 39 `NEEDS_MIGRATION` package observations seed review
only; remeasure the current tree and do not freeze either count.

Every dynamically remeasured Stage 90 package outside `PROTECT_LATEST` is a
non-`keep` path set. A package root is a category child directory under
`docs/90.references/{audits,data,research}/`; Stage 90 root/category READMEs
are structural indexes rather than packages. Current consumers or unique needed
meaning make migration a deletion precondition, not a reason to retain the
package. Assign an explicit replacement and `delete` disposition to every such
package leaf and README. The final package-root set must contain only the
protected root, with zero unresolved or pending dispositions. Structural root
and category READMEs are not packages and are regenerated or removed to reflect
that final set.

The Task 2 path inventory is execution evidence, not the durable oracle. Record
that Task 6 must migrate the measured set to a clearly owned package-local
preservation declaration in the `RES-0002` README before this Task body can be
compressed or removed.

In the same Task, build a subject-level implementation-truth inventory from
the current tracked implementation surfaces named in Dependencies. Do not add
one row per source file: group files only when they implement the same observed
behavior or structure and have the same canonical owner. Record:

```markdown
| Implementation subject | Observed current fact | Classification | Canonical Stage 01/02 owner | Mismatch or gap | Disposition | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
```

Classify required behavior, obligations, invariants, and guarantees as Stage
01 Requirements. Classify components, boundaries, data flow, and integration
shape as Stage 02 Architecture Descriptions; classify a durable adopted
architectural decision and its rationale as a Stage 02 ADR. Stage 03 describes
the change, Stage 05 describes operation, and Stage 90 records observation;
none substitutes for a missing Stage 01 or Stage 02 owner. A future requirement
or proposed architecture may remain only when it is explicitly distinguishable
from implemented current truth. Record zero unclassified implementation
subjects and zero current Stage 01/02 claims that contradict observed
implementation before mutation begins.

**Step 2: Record ordered `keep` cohorts**

Add a Task table with these columns:

```markdown
| Order | Selector | Disposition | Covered count | Exceptions | Evidence |
| :--- | :--- | :--- | ---: | :--- | :--- |
```

Selectors must be executable path/profile/status predicates and mutually
exclusive by order. A `keep` cohort is valid only when its members have one
owner, current terminology, valid lifecycle, a current consumer when required,
and no duplicate purpose. `PROTECT_LATEST` is the first-priority preservation
classification and overrides only the current-consumer requirement; it remains
inside the same target total rather than becoming a second disposition row.
No non-protected Stage 90 package belongs to a `keep` cohort.

**Step 3: Record every non-`keep` path explicitly**

Add a second Task table:

```markdown
| Path | Owner | Current consumers | Finding | Disposition | Replacement | Recovery | Reviewer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
```

Use untruncated searches for retired routes, fixed commits, duplicate purpose,
and current consumers:

```bash
rg -n -i \
  'docs/04\.execution|docs/00\.agent-governance/(support|memory|rules)|docs/99\.templates/support|spec-[a-z]|legacy|deprecated' \
  docs/00.agent-governance docs/01.requirements docs/02.architecture \
  docs/03.specs docs/05.operations docs/90.references docs/98.archive \
  docs/99.templates -g '*.md'
rg -n '\b[0-9a-f]{7,40}\b|branch-tip|blob digest|diff digest|SHA lineage' \
  docs/03.specs docs/98.archive scripts tests
rg -n --glob '*.md' \
  'docs/98\.archive/.+\.(md|json|ya?ml)|\]\([^)]*98\.archive/[^)]*\)' \
  docs/00.agent-governance docs/01.requirements docs/02.architecture \
  docs/03.specs docs/05.operations docs/90.references
```

Historical quotations and supply-chain material are classified by purpose, not
by token alone. Missing owner, consumer, replacement, recovery, or reviewer
blocks mutation rather than defaulting the path to deletion, and the Task and
Specification cannot complete while that disposition remains unresolved.

For a `PROTECT_LATEST` path, list any permitted path, metadata, stale-owner, or
link correction explicitly and prove that the research body, sources, and
claims remain semantically present. Do not use byte equality, checksums, or Git
SHA equality as that proof.

**Step 4: Prove coverage and obtain read-only review**

The sum of ordered cohort counts plus explicit exceptions must equal the target
total, with zero overlap and zero omission. `rules-engineer` reviews the rule
set, and `code-reviewer` reviews the exact Task diff. Neither grants approval.
The review must also prove that every dynamically measured `PROTECT_LATEST`
path is covered exactly once and that no destructive disposition includes it.
It also proves that every other measured Stage 90 package has an explicit
delete-after-migration path and that no package is unresolved or silently kept.
Every inbound Stage 98 file citation or cross-link receives an explicit current
owner and removal disposition; a historical quotation does not create an
exception to archive isolation. The review also checks the implementation-truth
inventory in both directions: every observed current obligation or structure
has the correct Stage 01/02 owner, and every Stage 01/02 statement presented as
current agrees with the observed implementation. The inventory is Task evidence
and never becomes a fixed count, manifest mirror, or new Gate.

**Step 5: Commit the bounded baseline**

```bash
git add docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md
git commit -m "docs(task): Record governance disposition coverage"
```

No corpus mutation is allowed before this commit.

---

### Task 3: Separate Stage 00 policy from provider runtime projection

**Files:**

- Modify: `docs/00.agent-governance/policies/workflows.md`
- Modify: `docs/00.agent-governance/policies/approval-boundaries.md`
- Modify: `docs/00.agent-governance/policies/bootstrap.md`
- Modify: `docs/00.agent-governance/policies/environment-constraints.md`
- Modify: `docs/00.agent-governance/policies/github-governance.md`
- Modify: `docs/00.agent-governance/policies/provider-capability-matrix.md`
- Modify as required: `docs/00.agent-governance/roles/*.md`
- Modify: `docs/00.agent-governance/providers/README.md`
- Modify: `docs/00.agent-governance/providers/registry.yaml`
- Modify: `scripts/manifest.yaml`
- Modify: `scripts/lib/agent_governance/agent_governance_contract.py`
- Modify: `scripts/operations/provider_surface_renderer.py`
- Modify: `scripts/validation/report-provider-hook-parity.sh`
- Modify: `tests/lib/agent_governance/test_agent_governance_contract.py`
- Modify: `tests/validation/test_provider_surface_renderer.py`
- Modify: `tests/validation/test_provider_native_surfaces.py`
- Modify: `tests/validation/test_provider_hook_parity.py`
- Modify: `tests/validation/test_agent_output_eval_fixtures.py`
- Delete after consumer proof: `.agents/rules/workspace.md`,
  `.agents/workflows/documentation.md`, and `.codex/README.md`
- Regenerate retained `.agents/**`, `.claude/**`, and `.codex/**` projections.

**Step 1: Write the policy/registry boundary regression**

Add to `tests/lib/agent_governance/test_agent_governance_contract.py`:

```python
    def test_provider_registry_does_not_restate_neutral_workflow_policy(self) -> None:
        registry = yaml.safe_load(
            (ROOT / "docs/00.agent-governance/providers/registry.yaml").read_text()
        )
        neutral_keys = {
            "workflow_states",
            "harness_layers",
            "harness_loops",
            "evidence_fields",
            "prohibited_evidence",
        }
        self.assertEqual(set(), neutral_keys & set(registry))

    def test_read_only_review_roles_remain_read_only(self) -> None:
        state = contract.load_agent_governance(ROOT)
        permissions = {role.agent_id: role.permission_profile for role in state.roles}
        for role_id in (
            "workflow-supervisor",
            "eval-engineer",
            "rules-engineer",
            "code-reviewer",
        ):
            self.assertEqual("read-only", permissions[role_id])
```

Run the first test and witness RED because the neutral keys currently live in
the provider registry. The permission test must stay GREEN throughout.

**Step 2: Make Stage 00 the one workflow owner**

Keep the discover through handoff order, approval boundary, role separation,
retry bounds, prohibited evidence, and stop behavior in the concise Stage 00
workflow and approval policies. Remove the same neutral semantics and their
hard-coded `EXPECTED_HARNESS_*` mirrors from the provider registry and agent
contract.

State the authority namespaces explicitly: Stage 99 owns document paths and
profiles; the Provider Registry owns runtime projection paths and provider
translation facts only. Put Stage 00 skills and Provider Registry facts into
bootstrap precedence without allowing either to override Stage 00 policy.
Describe tracked native runtime controls as consumers, not policy sources.

Remove every Stage 00 citation or cross-link to a Stage 98 document or file.
Stage 00 may define the archive stage's role, but no policy, role, skill, or
provider document may use archive evidence as its source or related-document
destination.

The provider registry retains only provider identities, native paths, canonical
role/skill patterns, work profiles, model translations, permission
translations, semantic hook events, hook commands, evaluation runtime facts,
and explicit projection routes.

Remove the fixed `14` role and `23` skill census from production and tests.
Compare the loaded identities with the safe tracked role and skill paths
instead; uniqueness and registered references are the invariant. Apply the same
derived relation to native projection tests.

**Step 3: Move static projection routes into typed provider data**

Retain only proven static projections as rows under `projections`; remove the
renderer-local `static` tuple. The retained rows are:

```yaml
projections:
  - provider_id: shared
    path: .agents/README.md
    source: docs/00.agent-governance/README.md
  - provider_id: claude
    path: .claude/CLAUDE.md
    source: docs/00.agent-governance/providers/claude.md
```

Remove consumerless `.agents/rules`, `.agents/workflows`, and `.codex/README`
routes. Keep managed roots in the provider registry as the deletion safety
boundary, but remove `EXPECTED_GENERATED_ROOTS`; the contract validates the
registered rows for uniqueness, relative paths, approved prefixes, and tracked
canonical sources rather than comparing them with a second tuple.

**Step 4: Decouple rendering from Stage 99 document validation**

Split Stage 00/provider input validation from the repository-wide cross-check.
The renderer consumes Stage 00 sources only. The repository agent-governance
Gate still verifies that Stage 99 registers the governance document profiles,
but `test_provider_surface_renderer.copy_fixture` no longer copies
`docs/99.templates/registry.json`.

Correct the renderer row in `scripts/manifest.yaml`: its authority is the
Stage 00 role/skill sources plus the Provider Registry, not Stage 99. Keep the
repository Gate cross-check as a separate consumer instead of mislabeling the
renderer input owner.

**Step 5: Narrow provider parity**

`report-provider-hook-parity.sh` validates provider event and hook translation,
not workflow ownership or neutral harness loops. Derive the expected hook
command inventory from the Provider Registry and compare it with
provider-native configuration; remove the second hard-coded command list from
the contract and parity script. Update agent-output evaluation fixtures to
assess role separation from Stage 00 sources while retaining the representative
oracle and thresholds.

**Step 6: Separate approved regeneration from ordinary validation**

Update the provider and environment policies so `--write` is permitted only
after an approved canonical Stage 00 or Provider Registry change. Ordinary
postflight and CI use `--check`. Then regenerate once and immediately prove
freshness:

```bash
PYTHONPATH=. python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_surface_renderer
PYTHONPATH=. python3 -m unittest tests.validation.test_provider_hook_parity
PYTHONPATH=. python3 -m unittest tests.validation.test_agent_output_eval_fixtures
bash scripts/operations/sync-provider-surfaces.sh --write
bash scripts/operations/sync-provider-surfaces.sh --check
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
python3 scripts/validation/check-script-manifest.py
git diff --check
```

Expected: every unit command is `OK`, provider drift is 0, and the repository
contract passes.

```bash
git add docs/00.agent-governance/policies/workflows.md \
  docs/00.agent-governance/policies/approval-boundaries.md \
  docs/00.agent-governance/policies/bootstrap.md \
  docs/00.agent-governance/policies/environment-constraints.md \
  docs/00.agent-governance/policies/github-governance.md \
  docs/00.agent-governance/policies/provider-capability-matrix.md \
  docs/00.agent-governance/providers/README.md \
  docs/00.agent-governance/providers/registry.yaml \
  docs/00.agent-governance/roles \
  scripts/manifest.yaml \
  scripts/lib/agent_governance/agent_governance_contract.py \
  scripts/operations/provider_surface_renderer.py \
  scripts/validation/report-provider-hook-parity.sh \
  tests/lib/agent_governance/test_agent_governance_contract.py \
  tests/validation/test_provider_surface_renderer.py \
  tests/validation/test_provider_native_surfaces.py \
  tests/validation/test_provider_hook_parity.py \
  tests/validation/test_agent_output_eval_fixtures.py
git add -u -- .agents/rules .agents/workflows .codex/README.md
git add .agents/README.md .agents/agents .agents/skills \
  .claude/CLAUDE.md .claude/agents .claude/skills .codex/agents
git commit -m "refactor(governance): Separate policy from provider projection"
```

---

### Task 4: Make Stage 99 and Stage 05 current structural authorities

**Files:**

- Modify: `docs/99.templates/registry.json`
- Modify as required: `docs/99.templates/schemas/*.json`
- Modify, consolidate, or delete: `docs/99.templates/templates/**`
- Modify: `docs/99.templates/README.md`
- Modify: `scripts/lib/document_governance/operations_catalog.py`
- Modify: `scripts/validation/check-operations-catalog.py`
- Modify: `tests/lib/document_governance/test_registry.py`
- Modify: `tests/lib/document_governance/test_operations_catalog.py`
- Modify: `tests/lib/document_governance/test_operations_taxonomy.py`
- Modify affected Stage 05 indexes and current Operations documents.

**Step 1: Write authority and template-consumption regressions**

Add to `tests/lib/document_governance/test_registry.py`:

```python
    def test_operations_profiles_do_not_delegate_current_membership_to_archive(self) -> None:
        registry = load_registry()
        for profile_id in ("guide", "policy", "runbook"):
            traceability = registry.profiles[profile_id]["traceability"]
            self.assertNotIn("membership_authority", traceability)

    def test_every_copy_template_is_registered(self) -> None:
        registry = load_registry()
        registered = {
            pathlib.Path(value["source"])
            for value in registry.template_roles.values()
        }
        actual = {
            path.relative_to(ROOT)
            for path in (ROOT / "docs/99.templates/templates").rglob("*")
            if path.is_file() and ".template." in path.name
        }
        self.assertEqual(actual, registered)
```

The first test is RED at the baseline because three profiles name an Operations
migration manifest. The second identifies unused or unregistered copy
templates without pinning a count.

**Step 2: Derive current Operations from the current tree**

Remove Migration 0002 and Migration 0003 as membership sources for current
Stage 05 validation. The current set is the safe, tracked directory tree under
`docs/05.operations/catalog/`, interpreted through Stage 99 profiles. No
current Operations, Registry, generator, or validator path may require a
Migration row after this Task.

Keep `validate_current_operations` as the public library predicate. Remove
historical row-count and exact-rename assertions from current Operations tests;
move any true regular-blob guarantee to archive recovery tests.

**Step 3: Audit templates against the Registry**

Clarify in the Stage 99 README that its path authority covers registered
document paths and profiles. Provider runtime projection paths belong to the
Provider Registry and are not a second Stage 99 template namespace.

For every template source, choose exactly one:

- keep and reconcile with its registered profile;
- consolidate unique content into the registered template and delete the
  duplicate; or
- delete it when no profile or current consumer exists.

Do not retain redirect templates. Update the Registry, schema, README, and all
consumers in the same logical change. Do not add a template role only to make an
unused file pass the test.

**Step 4: Verify protected Stage 99 and Operations surfaces**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_registry
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_operations_catalog
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_operations_taxonomy
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-operations-catalog.py --mode complete
python3 scripts/validation/check-document-links.py --mode all
```

Expected: all units `OK`, metadata `violations=0`, Operations `PASS`, and links
`failures=0`.

**Step 5: Commit**

```bash
git add docs/99.templates docs/05.operations \
  scripts/lib/document_governance/operations_catalog.py \
  scripts/validation/check-operations-catalog.py \
  tests/lib/document_governance
git commit -m "refactor(docs): Make current contracts independent of archive ledgers"
```

---

### Task 5: Normalize current Stage 01, 02, 03, and 05 owners and lifecycle

**Files:**

- Modify, consolidate, or delete paths explicitly listed by Task 2 under:
  `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, and
  `docs/05.operations/`.
- Modify affected stage indexes.
- Modify: `tests/lib/document_governance/test_requirements.py`
- Modify: `tests/lib/document_governance/test_architecture.py`
- Modify: `tests/lib/document_governance/test_spec_packages.py`
- Modify only if the existing predicate needs strengthening:
  `scripts/validation/check-doc-implementation-alignment.sh` and its existing
  document-graph tests; do not add a public Gate or fixed subject count.
- Modify current-path regression tests that encode deleted duplicates.

**Step 1: Add lifecycle-parent regression cases**

Extend `_write_package` with `plan_status: str = "active"` and
`task_status: str = "active"`, and pass those values to `_document_text` when
it writes the two children. Then add this temporary-package regression:

```python
    def test_current_execution_states_require_consistent_parents(self) -> None:
        spec_packages = _spec_packages_module()
        cases = (
            ("completed", "active", "active", "active Task requires active Spec"),
            ("active", "completed", "active", "active Task requires active Plan"),
            ("completed", "active", "completed", "active Plan requires active Spec"),
        )
        for spec_status, plan_status, task_status, message in cases:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                stage = pathlib.Path(directory) / "docs/03.specs"
                _write_package(
                    stage,
                    spec_status=spec_status,
                    plan=True,
                    plan_status=plan_status,
                    task=True,
                    task_status=task_status,
                )
                with self.assertRaisesRegex(spec_packages.SpecPackageError, message):
                    spec_packages.load_spec_packages(stage)
```

Implement these with the existing `_write_package` and one-field mutation
helpers; do not copy a real historical package. Witness RED for the known
non-conforming current packages before changing their statuses.

**Step 2: Promote observed current implementation truth**

For every Task 2 implementation-truth row:

1. verify the observed behavior or structure directly from tracked code,
   configuration, manifests, workflows, tests, and operated Stage 05 commands;
2. write an implemented obligation, invariant, or guarantee into exactly one
   registered Stage 01 Requirement owner;
3. write an implemented component structure, boundary, data flow, or
   integration shape into exactly one registered Stage 02 Architecture
   Description owner, and write a durable adopted architectural decision and
   its rationale into exactly one active ADR owner;
4. link a Stage 05 procedure to its Stage 01 behavior and Stage 02 structural
   prerequisites without copying the procedure into either owner; and
5. remove completed Stage 03 bodies, validators, tests, or Stage 90 evidence as
   sole current owners only after the Stage 01/02 promotion is complete.

Use current implementation as observation, not as permission to invent a
requirement. A genuine future requirement or proposed architecture must be
clearly distinguishable from implemented current truth. If the approved
documentation cannot match implementation without changing runtime behavior,
stop and create a separately approved behavior-change packet rather than
silently changing code. Translate facts into the registered Requirement,
Architecture Description, or ADR form; do not copy implementation listings,
fixtures, generated output, or execution logs.

Strengthen the existing implementation-alignment predicate only where a
measured gap proves it necessary. The existing `document-graph` responsibility
owns the check; this Task adds no suite, Gate, Task-numbered inventory, or fixed
count. Completion requires zero implementation subjects without the correct
Stage 01/02 owner and zero Stage 01/02 statements presented as current that
contradict implementation.

**Step 3: Resolve the known lifecycle contradictions**

Apply these deterministic decisions:

- SPEC-0136 is `superseded`; its active Plan and Task become `cancelled`.
- SPEC-0154 and SPEC-0155 must be `completed` when their completed Plans and
  Tasks are verified; P0 may already have closed them.
- SPEC-0102, SPEC-0123, SPEC-0134, and SPEC-0135 stay active only if Task 2
  proves a current owner and unfinished acceptance work. Otherwise terminalize
  their Tasks and Plans, write any still-current outcome to its canonical
  owner, and set the Spec to the legal terminal state supported by evidence.
- Delete terminal Plan and Task bodies after current outcomes, inbound
  consumers, and Git recovery are resolved. Add no Tombstone for a package
  member with no stable current consumer.

An ambiguous status stops this step; it is not inferred from age or line count.

**Step 4: Consolidate duplicate current owners**

For each explicit non-`keep` path in Stages 01, 02, and 05:

1. move unique current obligations into the one canonical owner;
2. update inbound links and traceability;
3. delete the duplicate body;
4. retain superseded ADRs in the ADR log; and
5. use a Tombstone only when Task 2 proves a stable recovery-navigation need.

Never merge documents merely because their titles are similar. Purpose,
normative scope, consumers, and acceptance must overlap.

**Step 5: Remove retired current-sounding routes**

Active documents must not publish retired Stage 04, predecessor support,
memory, rules, Spec-path, Task-path, or template routes as current procedure.
Historical evidence outside `PROTECT_LATEST` first moves any needed quotation,
finding, citation, generated output, or current consumer to its canonical
owner, then is deleted under Task 6. A current consumer delays deletion only
until migration; it never authorizes package retention. The protected pack may
receive stale-path corrections but not substantive research loss.

Remove every Stage 98 document/file citation and cross-link from retained Stage
01, 02, 03, and 05 documents. If a citation carries still-current meaning,
write that meaning to its canonical owner first. A retained minimal archive
record may point outward to a current replacement; the current document never
points back. Add focused existing-suite regressions for both Markdown links and
explicit archive-file path literals without creating a new public Gate.

**Step 6: Verify and commit by stage**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_requirements
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_architecture
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_spec_packages
bash scripts/validation/check-doc-implementation-alignment.sh
python3 scripts/validation/check-document-metadata.py --mode check-active
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-links.py --mode all
```

Expected: all units `OK`, implementation alignment reports no uncovered or
contradictory current truth, both metadata modes report `violations=0`, and
links report `failures=0`.

Commit Stage 01/02, Stage 03, and Stage 05 as separate logical changes when
more than one stage changes:

```bash
git commit -m "docs(requirements): Consolidate duplicate current owners"
git commit -m "docs(spec): Normalize active execution lifecycles"
git commit -m "docs(operations): Consolidate current procedures"
```

Stage only the files belonging to each commit; do not use these commands to
create empty commits.

---

### Task 6: Retire non-protected Stage 90 evidence and remove temporary Stage 98 Migrations

**Files:**

- Modify the protected `RES-0002` package and structural indexes; migrate then
  delete every other Task 2 package under `docs/90.references/`.
- Modify or remove every generator, manifest row, workflow route, test, and
  current document consumer that points to a non-protected Stage 90 package.
- Delete after consumer handoff:
  `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md`,
  `docs/98.archive/migrations/0002-operations-catalog-convergence.md`, and
  `docs/98.archive/migrations/0003-workspace-governance-simplification.md`.
- Remove the empty `docs/98.archive/migrations/` directory.
- Delete or retain explicitly reviewed paths under
  `docs/98.archive/tombstones/`.
- Modify: `docs/90.references/README.md`, `docs/98.archive/README.md`
- Modify:
  `docs/90.references/research/0002-agentic-engineering-research-pack/README.md`
- Modify: `scripts/lib/document_governance/references.py`
- Modify: `scripts/lib/document_governance/archive.py`
- Modify: `docs/02.architecture/decisions/0029-workspace-governance-authority.md`
- Modify: `docs/99.templates/registry.json` and remove the unused Migration
  template route and source.
- Modify: `tests/lib/document_governance/test_references.py`
- Modify: `tests/lib/document_governance/test_archive.py`
- Modify recovery-focused lifecycle tests.

**Step 1: Write Stage 90 retention relations**

Use the Task 2 current execution-baseline inventory to write a clearly labeled
package-local preservation declaration in the `RES-0002` README before any
Stage 90 deletion. The declaration owns a protected-content path list or
selector and records the user preservation decision. It contains no pinned
count, checksum, body digest, byte-equality claim, expected Git SHA, or
historical restore target. Stage 90 remains non-normative research evidence:
the declaration records the decision, while SPEC-0158 acceptance supplies its
authority and no research claim becomes policy.

Extend `test_references.py` on the existing reference/document-governance test
surface so every path derived from the persistent `RES-0002` README declaration
remains retained even when its consumer set is empty. The test asserts that the
declared protected path set equals the protected files on disk and that every
declared path exists. Concretely, it compares the declared set with the safe
tracked file set below the package root. The Task 2 execution evidence and
completion review separately prove that every other baseline Research, Audit,
or Data package migrated and was deleted; no current consumer or superseded
status is a retention exception. The test does not load the transient Task as
its durable source and does not pin a document count, checksum, body digest,
byte equality, or expected Git SHA. Keep this within
`tests/lib/document_governance/test_references.py` and the existing document-
governance suite; do not add a top-level Gate, public suite, manifest validator,
or Stage 99 schema.

Keep external citations as sources, never as instructions. Outside the atomic
user-protected latest research pack, a source with no consumer is deleted and a
source with a consumer first migrates needed meaning and that consumer, then is
deleted rather than relabeled as useful history.

Before any Stage 90 deletion, add a RED relation proving that current package
existence does not depend on Migration 0003's frozen historical target set.
Then decouple `scripts/lib/document_governance/references.py`: protected
Research retention derives from the current tree, Registry profile, and the
persistent package-local declaration, while current consumers are migration
preconditions for every other package. Migration 0003 is temporary source
evidence only until that coupling is removed. This repair must land before a
deletion so the old coupling cannot force one Tombstone per removed package.

Add a protected-content regression that exercises a zero-consumer
`PROTECT_LATEST` package through the README declaration and verifies the
presence of its substantive research sections, source citations, and claim-
bearing findings. The deterministic oracle covers declared path equality and
presence; semantic preservation remains an explicit reviewer obligation.
Stale current paths, metadata, owners, and links may be corrected, and no byte-
for-byte or hash comparison is permitted.

**Step 2: Write minimal archive-shape regressions**

Extend `test_archive.py` to prove the completion shape:

- `docs/98.archive/migrations/` is absent;
- Stage 98 contains only its structural README and the archive/Tombstone paths
  selected by the Task 2 explicit-preservation and live-consumer inventory;
- every retained record has only its registered minimal sections plus an
  optional Related Documents section, uses safe paths, and has no Migration
  parent or link;
- every retained `commit:path` resolves to a regular Git blob when recovery is
  claimed; and
- no test compares a recovered historical body byte-for-byte with current
  governance.

Delete Migration section, body, digest, row-count, exact-topology, and current-
membership checks. Do not replace them with a line count or a new census pin.

**Step 3: Reduce Stage 90**

For every source outside `PROTECT_LATEST`, migrate needed provenance, findings,
citations, generated outputs, and current consumers to the recorded canonical
owner, then delete the package and update inbound links in the same logical
change. A consumerless package can be deleted directly after profile, identity,
and high-water validation. Do not retain, shorten in place, or merely
supersede a non-protected package. Regenerate or remove Stage 90 root/category
indexes to match the resulting tree. Completion requires the dynamically
measured package-root set to contain only `RES-0002`, with zero unresolved or
pending dispositions.

For `PROTECT_LATEST`, retain the complete package even at zero consumers.
Correct stale current paths, metadata, lifecycle, owners, and links when
necessary, and integrate findings into current owners only non-lossily. Do not
delete, archive, or reduce its research body, sources, or claims. Remove every
Stage 98 document/file citation and cross-link, including stale measurements,
while preserving the surrounding research claim and external source meaning.
Regenerated or retained Stage 90 indexes must not enumerate or link Stage 98.

**Step 4: Remove temporary Stage 98 Migrations**

- Enumerate every tracked code, test, generator, manifest, workflow, Registry,
  ADR, and document consumer of Migration 0001--0003.
- Move current structural truth and review evidence to Stage 99, current owners,
  the current Task, or focused validators as appropriate. Git remains the
  full-content recovery boundary.
- Correct ADR-0029 so Migration 0003 is no longer a structural review boundary;
  remove the active Stage 99 Migration profile, template route/source,
  lifecycle binding, and allocation surface after the final consumer moves.
- Delete all three Migration documents and remove `migrations/` only after the
  consumer inventory reaches zero.
- Reclassify every existing Stage 98 record by explicit preservation need and
  live recovery-navigation consumer. Delete records with neither; retain only
  the registered minimal shape for a proven need and remove all Migration
  parents and links.
- Never place retired bodies, redirects, raw ledgers, snapshots, digests, frozen
  membership, or historical topology in a retained record or README.

**Step 5: Prove recovery before and after Migration deletion**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_references
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_archive
PYTHONPATH=. python3 -m unittest discover \
  -s tests/validation/lifecycle -p 'test_*.py'
python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-recovery
python3 scripts/validation/check-document-links.py --mode all
```

Expected: unit tests `OK`, recovery `violations=0`, links `failures=0`, zero
current Migration consumers, and no `docs/98.archive/migrations/` directory.
The reference tests must additionally derive the persistent README declaration,
prove exact on-disk protected-path equality and presence, and preserve the
zero-consumer override. Independent review proves that substantive research
body, sources, and claims remain while allowing reviewed stale current-path
corrections and avoiding checksum or SHA enforcement. Do not proceed to Task 8
until both the declaration and these tests are GREEN, every non-protected
baseline package is absent, and unresolved and pending dispositions are zero.

**Step 6: Commit evidence and archive reductions separately**

```bash
git commit -m "docs(references): Retire non-protected evidence packages"
git commit -m "docs(archive): Remove temporary migration records"
```

Stage only the paths for the corresponding logical change.

---

### Task 7: Simplify Gate ownership, modes, fixtures, and SHA tracking

**Files:**

- Modify: `scripts/lib/document_governance/suite_registry.py`
- Modify: `scripts/manifest.yaml`
- Modify: `scripts/validation/ci_gate_runner.py`
- Modify: `scripts/lib/gate/ci_gate_adapters.py`
- Modify: `.github/workflow-contract.yml`
- Delete after equivalence proof: `.github/workflows/document-corpus-lifecycle.yml`
- Modify: `scripts/validation/check-document-corpus-lifecycle.py`
- Modify: `scripts/validation/check-operations-catalog.py`
- Modify corresponding tests under `tests/lib/document_governance/`,
  `tests/gate/`, and `tests/validation/`.
- Modify active Plans and tests explicitly classified for SHA or fixture cleanup.

**Step 1: Remove the duplicate validator inventory**

Add a RED test to `test_suite_registry.py` that asserts the implementation has
no `IMMUTABLE_RETAINED_VALIDATOR_OWNERSHIP` and that changing one valid manifest
row changes the loaded membership without editing Python. Then:

- delete the Task-numbered immutable map;
- derive validator path, suite, argv, context, tests, and consumers only from
  `scripts/manifest.yaml`;
- retain the six `PUBLIC_SUITE_NAMES` fixed by ADR-0029; and
- replace filename-specific `validate_execution_argv` rows with bounded generic
  argument validation.

The manifest remains data; each validator remains the predicate.

**Step 2: Remove the internal adapter command inventory**

Move admission grammar to `ci_gate_adapters.py`: it recognizes the bounded
adapter verbs and validates their argv shapes. `ci_gate_runner.py` consumes the
workflow contract route and this grammar; it no longer repeats every test
module and command tuple in `_INTERNAL_ADAPTER_CONTEXTS`.

Test registration derives from manifest `tests` paths. The full profile must
run every `test_*.py` module exactly once or explicitly remove the unowned
module.

**Step 3: Collapse lifecycle modes after equivalence proof**

Before changing the CLI, run `check-public`, `check-contract`,
`check-promoted`, and `check-recovery` on the same tree and record their finding
sets in the Task. Add a test proving the replacement default contains the union
of current lifecycle and regular-blob recovery findings.

Then make `check-document-corpus-lifecycle.py` one complete default CLI with no
mode inventory. Remove the duplicate contract/promoted/recovery leaves and the
non-gating scheduled workflow. The manifest-owned document-lifecycle validator
is the one executable route; focused recovery remains a library unit test.

Keep the archive-isolation predicate in this existing route: tracked Markdown
under Stages 00, 01, 02, 03, 05, and 90 fails when it links to or explicitly
cites a Stage 98 file. Test a resolved Markdown link and a code-form path
citation. Do not create a new validator, public suite, Gate profile, or frozen
match count.

**Step 4: Collapse Operations modes**

`check-operations-catalog.py` validates the complete current Stage 05 tree by
default. Remove `manifest`, `structure`, `executed`, and `consumers` CLI modes,
the compatibility-only `--domains`, and fixed output counts. Keep diagnostic
library functions only when a current caller remains.

Update the manifest argv to the new default and remove duplicate local leaves
from the workflow contract. Do not change the public `operations` suite
responsibility.

**Step 5: Converge document-contract fixtures**

Document-contract tests use only:

1. the current Registry or registered template;
2. a one-field mutation of that current value; or
3. a temporary-Git recovery case.

Delete fixed workspace commits, historical full-body fixtures, corpus and
fixture count pins, and count-bearing test names. Preserve agent-output and
supply-chain oracles because their subject is not document taxonomy history.

**Step 6: Remove persistent SHA lineage controls**

Classify every remaining commit or digest use. Retain only:

- supply-chain integrity;
- CI event and merge-base selection;
- retained minimal Stage 98 regular-blob recovery;
- actual logical commits in the current Task; and
- policy-required ephemeral concurrent-worktree comparison.

Remove branch-tip equality, expected design/implementation SHA chains,
persistent blob or diff digest ledgers, historical byte equality, and test-only
workspace commit pins. Do not edit supply-chain rehearsal digests merely because
the token `SHA256` appears.

**Step 7: Verify the stable public interface**

```bash
PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_suite_registry
PYTHONPATH=. python3 -m unittest tests.validation.test_ci_gate_runner
PYTHONPATH=. python3 -m unittest tests.lib.gate.test_ci_gate_adapters
PYTHONPATH=. python3 -m unittest discover \
  -s tests/validation/lifecycle -p 'test_*.py'
PYTHONPATH=. python3 scripts/validation/check-script-manifest.py
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-operations-catalog.py
python3 scripts/validation/run-ci-gate.py --profile changed
```

Expected: all units `OK`, manifest `PASS`, both complete validators pass, and
the changed profile exits 0. Assert separately that the six public suite names
and `changed|full` CLI choices are unchanged.

**Step 8: Commit in three reviewable changes**

```bash
git commit -m "refactor(gate): Derive validation ownership from the manifest"
git commit -m "refactor(validation): Collapse duplicate document Gate modes"
git commit -m "test(fixtures): Remove historical document resurrection"
```

Stage only the files belonging to each change and rerun its focused checks
before continuing.

---

### Task 8: Verify current truth, close the packet, and remove transient execution bodies

**Files:**

- Modify: all affected stage indexes and current owners.
- Modify: `docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md`
- Modify then remove after terminal recovery proof:
  `docs/03.specs/0158-document-governance-lifecycle-convergence/plan.md`
- Modify then remove after terminal recovery proof:
  `docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md`
- Remove other terminal Plan and Task bodies, including SPEC-0157 execution
  bodies, only after their last current consumer is removed in this closure.
- Regenerate any Task 2-recorded replacement for generated indexes formerly
  stored as non-protected Stage 90 Data packages; do not recreate a deleted
  Stage 90 output.
- Regenerate retained provider projections.

**Step 1: Run focused and aggregate verification**

First read the persistent package-local preservation declaration from the
`RES-0002` README, not the transient Task 2 body. Prove that its declared path
set equals the safe tracked on-disk package set and that every protected path
exists. Independently review that the substantive research findings, source
citations, and claims remain. This semantic review permits approved stale path,
metadata, owner, and link corrections; do not compare checksums, body hashes,
byte equality, or expected Git SHAs. Re-derive all other Stage 90 disposition
totals from the current tree rather than asserting the preliminary 25/39
discovery counts. Prove that the resulting package-root set contains only the
protected `RES-0002` root and that unresolved and pending dispositions are
zero. Structural root/category READMEs are excluded from the package-root set
but must match the resulting tree.

```bash
python3 scripts/validation/check-document-metadata.py --mode check-active
python3 scripts/validation/check-document-metadata.py --mode check-contracts
python3 scripts/validation/check-document-metadata.py \
  --mode check-changed \
  --base-ref "$(git merge-base main HEAD)"
python3 scripts/validation/check-document-links.py --mode all
bash scripts/validation/check-doc-implementation-alignment.sh
python3 scripts/validation/check-document-corpus-lifecycle.py
python3 scripts/validation/check-operations-catalog.py
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
bash scripts/operations/sync-provider-surfaces.sh --check
PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validation/run-ci-gate.py --profile full
git diff --check
```

Expected: zero metadata violations, zero link failures, zero current
implementation-alignment gaps or contradictions, lifecycle and Operations
pass, provider drift 0, unit discovery `OK`, full profile exit 0, and no diff
error.

**Step 2: Obtain independent review**

- `rules-engineer`: one owner per rule, bidirectional current implementation to
  Stage 01/02 coverage, legal lifecycle, no Stage 90/98 current authority, and
  no agent verdict presented as user approval.
- `code-reviewer`: exact diff, deletion recovery, test adequacy, and acceptance
  item coverage.
- `ci-cd-engineer` and `security-auditor`: only if workflow or protected CI
  changes remain in the final diff.

Resolve Critical and Important findings, rerun affected checks, and record the
observed verdicts in the Task.

**Step 3: Write current outcomes and complete the packet**

Update canonical owners with durable outcomes. In the current Task, record the
actual commands, results, review verdicts, logical commit ledger, rollback, and
any genuinely deferred external item. Set Task, Plan, and Spec from `active` to
`completed` in one legal lifecycle change.

Do not compress or remove the Task 2 protected-path evidence until the
package-local README declaration exists, the existing reference tests derive
it without reading the Task, the declared set equals the safe tracked on-disk
package set, and the zero-consumer override is GREEN.

Regenerate the LLM Wiki at the Task 2-recorded canonical replacement output
after the last document edit. The generator and its consumers must no longer
write or link a non-protected Stage 90 Data package:

```bash
python3 scripts/knowledge/generate-llm-wiki.py --write
python3 scripts/knowledge/generate-llm-wiki.py
```

Expected: generated output is fresh.

```bash
git add docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md \
  docs/03.specs/0158-document-governance-lifecycle-convergence/plan.md \
  docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md \
  docs/03.specs/README.md
git commit -m "docs(spec): Complete document governance convergence"
```

Stage the exact Task 2-recorded generated-output replacement paths in the same
commit; never stage or regenerate the retired Stage 90 Data destination.
Before setting the Specification terminal, rewrite its transitional archive-
file names and paths as a concise outcome statement. The completed Spec may
describe the Stage 98 role and the fact that its temporary Migration layer was
removed, but it must not cite or cross-link any Stage 98 document or file.

**Step 4: Remove transient completed execution bodies**

After the completion commit is a regular Git recovery boundary and no current
consumer needs the Plan or Task body, delete the completed Plan and Task, update
the Stage 03 index to link only the completed Spec, and regenerate the LLM Wiki
without enumerating or linking Stage 98 files.
Do not add a Tombstone unless a stable inbound consumer was discovered after
the completion commit. The `RES-0002` package-local preservation declaration
and its GREEN existing-test oracle are mandatory preconditions; Task retirement
must not remove the only protected path source.

Run metadata, links, wiki freshness, and the full profile again, then commit:

```bash
git add -u -- \
  docs/03.specs/0157-script-surface-ownership-convergence/plan.md \
  docs/03.specs/0157-script-surface-ownership-convergence/tasks \
  docs/03.specs/0158-document-governance-lifecycle-convergence/plan.md \
  docs/03.specs/0158-document-governance-lifecycle-convergence/tasks
git add docs/03.specs/README.md
git commit -m "docs(spec): Retire completed convergence execution bodies"
```

Stage the regenerated canonical replacement output by its exact Task 2 path;
the retired Stage 90 Data path must remain absent.

## Risk and Rollback

| Risk | Guardrail | Rollback |
| :--- | :--- | :--- |
| Earlier SPEC-0157 work is presented as approved | P0 records discovered commits and current revalidation | Revert the activation commit; keep the branch evidence unchanged |
| A complete audit becomes a second corpus copy | Cohort rules plus explicit non-`keep` exceptions only | Revert the Task evidence commit and rewrite the rule summary |
| A current obligation is deleted with a duplicate | Move unique obligations and update consumers before deletion | Revert the logical stage commit |
| Stage 01/02 documents describe only intent or stale design while current implementation has no matching owner | Require the Task 2 subject inventory and Task 5 bidirectional promotion before evidence retirement | Revert the Stage 01/02 documentation commit, re-observe implementation, and correct the canonical owner without changing runtime behavior |
| A non-protected Stage 90 package survives because it still has a consumer | Treat the consumer as a migration dependency, require the final package-root set to contain only `RES-0002`, and require unresolved/pending counts of zero | Revert the incomplete cohort change, finish owner migration, then delete the package |
| Latest external research is lost because consumers reach zero or a link-only commit appears newer | Apply the atomic current-baseline protection set, persistent README declaration, and purpose-based Git classification | Revert the rejected mutation commit or restore its paths from the immediately reviewed pre-mutation current Git state; never restore a named historical pack snapshot |
| Task retirement removes the only protection oracle | Require the package-local declaration and existing reference tests to be GREEN first | Restore the Task body only long enough to complete the declaration handoff, then rerun the retirement checks |
| Stage 98 reduction breaks required recovery navigation | Inventory explicit preservation needs and live consumers, then verify every retained recovery `commit:path` as a regular blob before and after | Revert the archive commit; never reconstruct from memory |
| A current stage still cites an archive file | Require zero inbound Stage 98 file citations and cross-links in Stages 00/01/02/03/05/90 and keep the check in the existing lifecycle/link suite | Restore the current-owner text if meaning was lost, then remove the archive dependency rather than restoring the inbound link |
| Provider projection becomes a policy source | Stage 00 owns neutral workflow; registry owns runtime translation only | Revert the source change and regenerate projections |
| Gate reduction drops a guarantee | Compare finding sets and add replacement regression before deleting a route | Revert the single Gate commit |
| Fixture cleanup removes a real oracle | Scope historical removal to document taxonomy; preserve agent-output and supply-chain fixtures | Restore the specific oracle and classify its real owner |
| SHA cleanup weakens concurrency or supply-chain safety | Retain approved ephemeral and integrity uses by category | Revert only the misclassified SHA removal |
| Concurrent edits make a path owner ambiguous | Stop the current Wave and reclassify against a clean exact diff | Preserve all dirty state; do not reset or overwrite |

## Verification

The final state must satisfy all of the following:

- every target is covered once by ordered disposition rules and exceptions;
- every non-`keep` path has owner, consumer, replacement, recovery, and review;
- every implemented required behavior has one current Stage 01 owner, every
  implemented structure or durable decision has one current Stage 02 owner,
  and no current Stage 01/02 statement contradicts tracked implementation;
- future requirements or proposed architectures are explicitly distinguishable
  from implemented current truth, and Stage 03/05/90 or validator/test surfaces
  are never the sole durable owners of current requirement or architecture;
- active documents publish no retired path as current procedure;
- active lifecycle parents and children are mutually consistent;
- the persistent `RES-0002` README declaration equals the safe tracked on-disk
  package set, every declared path exists, and the zero-consumer override stays
  GREEN; independent review confirms substantive research findings, sources,
  and claims remain semantically preserved;
- after consumer and needed-meaning migration, the dynamically measured Stage
  90 package-root set contains only `RES-0002`, unresolved and pending
  dispositions are zero, and structural indexes match the resulting tree;
- every non-protected Stage 90 deletion follows consumer migration and profile,
  identity, and high-water validation, with no redirect/body clone and no
  Tombstone unless a live recovery-navigation consumer requires one minimal
  package README;
- Stage 98 has no Migration document, temporary Migration directory, active
  Migration Registry/template surface, or current consumer; it contains only
  its structural index and minimal records backed by an explicit preservation
  need or measured live recovery-navigation consumer;
- retained Stage 98 records contain no body copy, redirect, raw execution
  ledger, snapshot, duplicate digest, frozen topology, or current-membership
  authority;
- Stages 00, 01, 02, 03, 05, and 90 contain zero Stage 98 document/file
  citations or cross-links, including generated indexes and code-form path
  literals; archive navigation is one-way toward current replacements;
- Stage 99 has no unused copy template or archive-backed current membership;
- provider adapters are fresh and contain no policy;
- manifest validator inventory has no Task-numbered Python mirror;
- lifecycle and Operations each have one complete executable behavior;
- document fixtures do not resurrect fixed workspace history;
- persistent SHA lineage is absent while recovery, CI, concurrency, and
  supply-chain integrity remain;
- six public suite names and `changed|full` profiles are unchanged; and
- the full CI profile exits 0.

## Rulings

1. **Lifecycle precedes location.** A document is classified by current role,
   state, owner, consumer, and recovery before its directory influences the
   disposition.
2. **Current owners are repaired before evidence is reduced.** Otherwise a
   stale reference can be the only surviving description of a still-current
   obligation.
3. **Complete coverage does not require a corpus copy.** Ordered selectors and
   explicit exceptions are smaller, rerunnable, and easier to review.
4. **Stage 98 minimum is smaller than the retired Migration contract.** The
   Registry and tests allow the Migration directory to be absent; only a
   retained minimal record receives safe-path, shape, and regular-blob recovery
   validation appropriate to its proven need.
5. **Provider facts and neutral policy are different authorities.** Stage 00
   owns workflow behavior; provider data translates native runtime mechanics.
6. **Migration records are temporary convergence inputs.** Current Stage 05,
   Stage 99, ADR, generator, and validator truth moves first; Git retains the
   deleted history after all Migration documents and their directory are gone.
7. **Public interfaces remain stable while internal routes shrink.** The six
   suites and `changed|full` profiles stay; duplicate modes and inventories do
   not.
8. **Fixture history and recovery history are different.** Current document
   contracts derive from current sources; temporary Git proves recovery.
9. **SHA is retained by purpose, not token.** Integrity and recovery uses stay;
   documentary lineage and test-only workspace pins go.
10. **Deletion is fail-closed.** Ambiguous ownership, consumer, recovery, or
    concurrent state blocks mutation, and unresolved disposition blocks Task
    and Specification completion rather than becoming a retained exception.
11. **The latest saved external research is an atomic user-preserved unit.**
    Every execution-baseline file in `RES-0002` receives `PROTECT_LATEST` before
    consumer classification, and the override survives zero consumers without
    becoming a Registry status.
12. **Git recency is classified by purpose.** Content authoring and activation
    are distinct from later claim, governance, path, or link maintenance. The
    sole preservation subject is the Task 2 current execution-baseline package;
    observed commit identifiers remain illustrative provenance only and never
    become final protected content, a restore target, checksum, expected branch
    SHA, or Gate input.
13. **Historical topology does not own current retention.** `references.py`
    must be independent of Migration 0003's frozen target set before deletion,
    and no current consumer may remain when the Migration package is removed.
    Zero-consumer removal uses Git recovery without a Tombstone; only a live
    recovery-navigation consumer justifies one minimal package README
    Tombstone.
14. **Preliminary disposition totals are not contracts.** The observed 25
    deletion candidates and 39 migration-dependent packages are discovery
    evidence only; Task 2 and final verification remeasure the current tree.
15. **Protection outlives Task evidence.** Before Task retirement, Task 6 writes
    the dynamically measured path set and user decision to the non-normative
    `RES-0002` README without hashes or a pinned count. Existing reference tests
    derive that declaration and enforce on-disk equality, presence, and the
    zero-consumer override; SPEC acceptance remains authoritative and semantic
    body/source/claim preservation remains a review contract.
16. **Archive navigation is one-way.** Stage 98 may point to a current
    replacement, but Stages 00, 01, 02, 03, 05, and 90 never cite or cross-link
    a Stage 98 document or file. Existing lifecycle/link validation owns this
    predicate without a new Gate or fixed census.
17. **Current implementation is promoted, not copied.** Implemented behavior
    and guarantees map to Stage 01; implemented structure, boundaries, data
    flow, and durable decisions map to Stage 02. The Task proves bidirectional
    coverage with the existing implementation-alignment responsibility, while
    source listings, fixtures, generated data, and execution history stay in
    their proper implementation or evidence owners.

## Related Documents

- [Specification](spec.md)
- [SPEC-0157 Plan](../0157-script-surface-ownership-convergence/plan.md)
- [SDLC](../../00.agent-governance/sdlc.md)
- [Documentation Protocol](../../00.agent-governance/policies/documentation-protocol.md)
- [Approval Boundaries](../../00.agent-governance/policies/approval-boundaries.md)
- [Stage Authoring Matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 Registry](../../99.templates/registry.json)
