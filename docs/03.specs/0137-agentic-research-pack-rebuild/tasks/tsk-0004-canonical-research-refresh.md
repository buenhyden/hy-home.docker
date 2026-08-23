---
profile_id: task
status: active
artifact_id: task-0137-0004
artifact_type: task
parent_ids:
  - SPEC-0137
  - plan-0137
created: 2026-08-23
updated: 2026-08-23
---

# Task: Canonical Agentic Engineering Research Refresh

## Objective

Author and verify the canonical `RES-0002` research pack after SPEC-0153 Task 9
has independently established and merged its Stage 90 structure into `main`.
This Task owns research content and its evidence only; it never owns Task 9,
Stage 90 migration mechanics, protected runtime or remote observation, or the
cleanup of another worktree.

## Inputs

| Input | Observed state on 2026-08-23 |
| --- | --- |
| Corrected specification | `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` at `11fda02484c78df957156bfd27228851e764116d`; independently reviewed C0/I0/M0 by both rules/specification and documentation-quality reviewers. |
| Active execution plan | `docs/03.specs/0137-agentic-research-pack-rebuild/plan.md`; this Plan and Task are the same authority-correction unit, so their commit identity is intentionally not self-claimed and is recorded by a later Task update. |
| Structural dependency | `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0009-references.md`; independently owned in another worktree and not accepted or editable here. |
| Content destination | `docs/90.references/research/0002-agentic-engineering-research-pack/`; absent from this branch, so content authoring is blocked. |
| Branch baseline | Task-8-derived commit `0c841b086cd1e6adc2c1ca53ce14eec309fe8f47`, plus the corrected Spec commit above. |
| Graph evidence | `graphify-out/GRAPH_REPORT.md` was built from `f8a72211`; it is stale and advisory and requires corroboration against tracked sources and current governance. |
| External-source cutoff | 2026-08-23. External research was read-only and did not observe secrets, provider entitlement, live runtime state, or remote enforcement. Authoring uses only these preserved observations and fixed pins; any later access requires a separately corrected/reviewed Spec and Plan carrying its actual access date. |

## Work Log

| Date | Unit | Observed result |
| --- | --- | --- |
| 2026-08-23 | External research | Five read-only research clusters completed for harness/loop/providers, agents/models/memory, SDLC/docs/wiki, delivery/QA/V&V, and Compose/infra/security. No research file was authored or modified. |
| 2026-08-23 | Spec correction | Commit `11fda02484c78df957156bfd27228851e764116d` aligned SPEC-0137 with `RES-0002`, the eight-scope axis, Stage 03 ownership, and the independent Task 9 boundary. |
| 2026-08-23 | Spec review | Independent rules/specification and documentation-quality reviews both returned C0/I0/M0. |
| 2026-08-23 | Dependency check | The Task 9 worktree remained uncommitted and independently owned; `RES-0002` was absent from this branch. Content authoring is `BLOCKED` pending an accepted Task 9 merge to `main`. |
| 2026-08-23 | User scheduling ruling | The user approved eventual research integration and cleanup, but scheduled main-branch integration and cleanup only after the Task 9 worktree is completed and merged to `main`. No merge or cleanup was performed. |
| 2026-08-23 | Authority-correction validation | Focused metadata and diff check passed. Traceability remained FAIL on one inherited over-size historical Task finding; no PASS claim was made. |
| 2026-08-23 | Plan/Task review R1 — initial | Rules C0/I2/M0; quality C0/I4/M0. Failed, did not authorize commit, and its findings were corrected before R2. |
| 2026-08-23 | Plan/Task review R2 — corrected | Rules C0/I1/M0; quality C0/I2/M0. Failed, did not authorize commit, and its findings were corrected before R3. |
| 2026-08-23 | Plan/Task review R3 — next | Rules C0/I1/M0; quality C0/I0/M0. Failed because the pair was nonzero, did not authorize commit, and its findings were corrected before R4. |
| 2026-08-23 | Plan/Task review R4 — acceptance | Rules C0/I0/M0; quality C0/I1/M0. The round label did not make the nonzero pair approved; it failed, did not authorize commit, and its findings were corrected before R5. |
| 2026-08-23 | Plan/Task review R5 — absolute-final preliminary | Rules C0/I0/M0; quality C0/I3/M0. Failed, did not authorize commit, and its findings were corrected before R6. |
| 2026-08-23 | Plan/Task review R6 — terminal attempt | Rules C0/I1/M0; quality C0/I0/M0. Failed, did not authorize commit, and its findings are corrected by this evidence-only update. The next fresh terminal review remains `Not Run` in-tree and external. |

## Verification Evidence

| Check | Observed result |
| --- | --- |
| Focused corrected-Spec metadata | PASS; zero violations. |
| Corrected-Spec whitespace check | `git diff --check` PASS. |
| Full repository contract on the Task-8-derived branch | FAIL, `failures=13`; this is a pre-existing baseline result and is not called PASS. |
| Research-content file census | No `RES-0002` content exists in this branch; content phase remains `BLOCKED`. |
| Authority-correction focused metadata | PASS, exit 0: base `11fda02484c78df957156bfd27228851e764116d`, `selected=5 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Authority-correction traceability | FAIL, exit 1: exactly `document-not-regular` for `tasks/tsk-0001-rebuild.md`; summary `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`. Classified inherited because the base blob was 2,242,358 bytes and already exceeded the 2 MiB checker ceiling; the current file is 2,242,656 bytes after only metadata/Overview disposition edits. This is not PASS. |
| Authority-correction whitespace check | `git diff --check` exit 0. |
| Post-Task9 synchronization and public suites | Not Run; Task 9 is not yet accepted or merged to `main`. |

Later evidence is appended only after execution. Each result records the exact
command, baseline or range, exit status, selected path count, and attributable
versus inherited findings. A tracked workflow or configuration proves only
repository adoption; it does not prove remote enforcement or a successful run.

## Review Evidence

| Review | Verdict |
| --- | --- |
| Corrected SPEC-0137 rules/specification review | C0/I0/M0. |
| Corrected SPEC-0137 documentation-quality review | C0/I0/M0. |
| Plan/Task R1 — initial | Failed pair: rules C0/I2/M0; quality C0/I4/M0. No commit authority; findings corrected before R2. |
| Plan/Task R2 — corrected | Failed pair: rules C0/I1/M0; quality C0/I2/M0. No commit authority; findings corrected before R3. |
| Plan/Task R3 — next | Failed pair: rules C0/I1/M0; quality C0/I0/M0. No commit authority; findings corrected before R4. |
| Plan/Task R4 — acceptance | Failed pair: rules C0/I0/M0; quality C0/I1/M0. Not approved despite the round label; no commit authority; findings corrected before R5. |
| Plan/Task R5 — absolute-final preliminary | Failed pair: rules C0/I0/M0; quality C0/I3/M0. No commit authority; findings corrected before R6. |
| Plan/Task R6 — terminal attempt | Failed pair: rules C0/I1/M0; quality C0/I0/M0. No commit authority; findings corrected by the current evidence-only update. |
| Next fresh Plan/Task terminal publication review | Not Run at this in-tree publication point; the required verdict stays external to the reviewed tree and is not written back before commit. |
| Research unit reviews | Not Run; research files have not been authored. |
| Final exact-range rules/specification/quality review | Not Run. |
| Branch-readiness terminal publication review | Not Run; the final-tree verdict and resulting readiness commit ID are external handoff evidence. |
| Main-completion terminal publication review | Not Run; the final Task-only verdict is external handoff evidence. |

No implementation unit advances when a Critical, Important, or Minor finding
remains. Review evidence never substitutes for validator evidence.

For every Task 0004 evidence publication, validators rerun after the tracked
evidence is finalized, then fresh reviewers inspect that exact final tree. The
terminal verdict is reported only in the external execution handoff/commit
evidence, and no file mutation follows before commit. A tracked `Not Run` row is
therefore truthful and does not weaken the external C0/I0/M0 commit gate.

Path-scoped validators must exit zero. Repository- and corpus-wide validators
retain raw status: a non-final logical unit may advance only with zero
attributable findings, while inherited findings remain explicitly FAIL/non-PASS.
On the exact readiness commit and on the final merged tree, every applicable
full-ladder command must exit zero. An inherited nonzero blocks main merge,
completion, and cleanup pending its owner or a separately approved boundary
change.

## Commit Ledger

| Logical unit | Commit | State |
| --- | --- | --- |
| Correct canonical research Spec | `11fda02484c78df957156bfd27228851e764116d` — `docs(spec): align canonical agentic research contract` | Committed and dual-reviewed C0/I0/M0. |
| Read-only external research | No commit | Complete as advisory input; no content authored. |
| Reset Plan/Task authority | Commit identity intentionally not self-claimed by this same commit | Expected title `docs(plan): reset canonical research execution`; the next authorized Task update records the resolved identity. |
| Bind accepted post-Task9 main baseline | No commit | Blocked pending Task 9 completion and merge. |
| Research content and integration units | No commits | Blocked pending the baseline gate. |
| Record research-branch readiness | No commit | Not Run; Task remains active; expected title `docs(task): record canonical research readiness`. The resulting self-identity and terminal verdict are recorded externally, not by mutating this Task after review. |
| Readiness-HEAD finishing gate | No commit by design | Not Run; invoke `superpowers:finishing-a-development-branch` and require every applicable full-ladder command to exit zero on the exact readiness commit before main merge. |
| Record post-merge completion on main | No commit | Not Run; only after merged-tree gates; expected title `docs(task): complete canonical research integration`. |
| Terminal completion-HEAD cleanup gate | No commit by design | Not Run; the full applicable ladder must exit zero on the Task completion commit, and results are reported without creating a self-recording evidence commit. |
| Research branch/worktree cleanup | No commit | Explicitly deferred until the terminal completion-HEAD gate is green. |

## Rulings

- This Task is active as the sole prospective SPEC-0137 execution ledger, while
  its content phase is `BLOCKED`; active status does not imply executable
  content authority before the dependency gate passes.
- Tasks 0001, 0002, and 0003 are cancelled historical records. Their retained
  bodies do not authorize future work and are not reclassified as completed.
- After Task 9 is independently accepted and merged, merge that post-Task9
  `main` into this branch. Rebase, reset, checkout-based restoration, history
  rewriting, and changes to Task 9 are forbidden.
- If the accepted `main` does not contain both the Task 9 acceptance evidence
  and the canonical `RES-0002` destination, stop. Do not create the destination
  from this Task.
- Any conflict while merging post-Task9 `main` is terminal before the research
  baseline is frozen. Do not resolve any conflicted path; request a new
  synchronization Plan and authority. Content edits begin only after a
  conflict-free merge and recorded baseline.
- `RES-0002/README.md` selects the Stage 99 research profile and owns navigation
  plus the aggregate claim, source, requirement, and eight-scope matrices.
  Leaf rows own detail and must reconcile exactly with the README aggregates.
- Research claims distinguish upstream capability, tracked local adoption, and
  observed runtime or remote proof. Documentation availability never proves
  provider entitlement, model availability, execution, or enforcement.
- Stage 90 is advisory. Stage 04 has no authority, Operations paths are
  prefixless, and ordinary delivery evidence belongs to Task plus Git/PR rather
  than a standalone Release document role.
- No container, remote, provider, secret, credential, or private state is
  accessed by this Task. Unavailable evidence is recorded as `UNVERIFIED`.
- Parent Stage 90 routers, generators, dated packs, and Task 9 remain outside
  this Task after synchronization; this Task never absorbs their ownership.
- Each logical content cluster has one implementer, independent rules/spec and
  quality review, exact focused validation, and its own Conventional Commit.
- Evidence publication is finalized before the terminal fresh exact-tree
  review. That verdict and the resulting commit identity stay in the external
  Task 0004 execution handoff; no file mutation occurs between review and
  commit, and this Task never self-records its own commit hash.
- The conflict-free post-Task9 synchronized commit freezes every selected
  repository/corpus-wide command, exact expanded argv, raw exit/status, and
  deterministic finding identity set. Later exact five-field matches are
  inherited; new identities or changed detail on the same
  validator/code/path core are attributable.
- If the ADR-0029 suite runner is absent, the synchronized baseline freezes
  `bash scripts/validation/check-repo-contracts.sh` as the current full
  aggregate, including its exact argv, raw exit/status, summary, and
  deterministic finding identities; the seven focused commands remain
  diagnostic components and are frozen separately. The known Task-8-derived
  `FAIL failures=13` is not a bypass or PASS claim.
- Task 0004 remains active through research-branch merge. Main integration is
  allowed only after `superpowers:finishing-a-development-branch` verifies the
  exact readiness commit, post-Task9 main ancestry, clean state, and an actually
  green full ladder. An inherited nonzero remains FAIL and blocks before merge
  pending its owner or a separately approved boundary. Main integration is
  followed by merged-tree gates and a separate main-worktree Task evidence
  commit that records the merge and transitions Task 0004 to completed. Only
  after the full ladder also exits zero on that completion commit may the
  finishing-development-branch workflow remove this research worktree/branch.
  The terminal result is reported without another Task evidence commit. A
  terminal nonzero blocks cleanup and requires a separately reviewed lifecycle
  correction or approved revert. Task 9 and the legacy delta worktrees are
  preserved.
- Immediately before merge, the main worktree must already be on clean `main`.
  Controller-side literal comparisons require main HEAD to equal this Task's
  accepted/frozen main ID and the research branch tip to equal the external
  readiness handoff ID; main must be an ancestor of that tip. Any mismatch
  stops before merge, with no placeholder shell evaluation or inferred ID.
- The 2026-08-23 external observations and fixed pins are the closed research
  evidence snapshot. No content unit re-accesses mutable external sources. A
  missing fact or needed later access stops and requires a separately corrected
  and reviewed Spec and Plan with the actual access date.

## Deferred Items

- SPEC-0153 Task 9 completion, acceptance, structural migration, parent routing,
  generator updates, and dated-pack cleanup remain with its existing owner.
- The accepted post-Task9 `main` commit and new research baseline have not been
  frozen because the dependency is not yet complete. The future freeze includes
  exact command argv, raw statuses, and deterministic finding identity sets for
  every later-compared repository/corpus-wide validator.
- The twenty-one `RES-0002` files are not authored until the dependency gate
  passes.
- Terminal publication reviews for this authority correction and every later
  evidence commit remain external to the tree they review. Their current
  tracked state is `Not Run`; a commit still requires external C0/I0/M0 and no
  subsequent file mutation.
- Any external evidence not present in the preserved 2026-08-23 observations or
  fixed pins is deferred. Later external access is forbidden under the current
  cutoff until a separately corrected/reviewed Spec and Plan records its actual
  date.
- Public-suite execution is deferred until synchronization establishes whether
  the ADR-0029 suite runner has been implemented. An absent runner is recorded
  as a skipped gate with rationale, never as PASS. In that case the current
  full aggregate `bash scripts/validation/check-repo-contracts.sh` and all seven
  focused diagnostics are run and frozen. The currently known aggregate
  `failures=13` remains FAIL and blocks readiness-HEAD integration, merged-main
  completion, and terminal cleanup until an actual strict run exits zero.
- Main merge and current research branch/worktree cleanup are deferred exactly
  as scheduled by the user. Main merge first waits for the readiness-HEAD
  finishing gate to exit zero. Cleanup additionally waits for the terminal
  completion-HEAD full ladder to exit zero and never includes the Task 9 or
  legacy delta worktrees.
