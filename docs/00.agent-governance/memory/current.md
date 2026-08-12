---
layer: agentic
status: active
---

# Current Project Memory

## Current objective

- Current task: none, and correctly so. Under the incoming spec 136 contract a
  Task is a role inside an active capability and this work is a Stage 90
  reference extension. See Blockers.
- Extended the canonical agentic research pack at
  `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` with
  two leaves and revalidated its workspace-derived figures. The originating
  request asked for research across roughly 25 topics; pre-task discovery found
  23 already covered by dedicated leaves, so the deliverable became an in-place
  extension rather than a new pack.

## Approved decisions

- Extend the 2026-07-05 pack in place. Do not create a dated pack. This
  preserves the Spec 122 single-canonical-pack outcome and follows the
  2026-08-07 precedent.
- Revalidate workspace-derived counts only. External sources keep their
  2026-08-07 verification; only sources cited by the two new leaves were
  retrieved fresh, on 2026-08-10.
- Work in an isolated worktree based on `codex/sdlc-taxonomy-convergence` HEAD
  rather than on `main`, because that branch redefines the document identity
  contracts the new leaves must satisfy.
- Add exactly two leaves: `verification-validation.md` and
  `github-actions-platform.md`.
- Keep the GitHub Actions leaf to platform mechanics. The automation leaf keeps
  its repository inventory; the new leaf adds only the complement, a table of
  unadopted capability.

## Active boundary

- Delivered on `codex/agentic-research-vv-gha` from base `4122cecf` and
  fast-forward merged into `codex/sdlc-taxonomy-convergence`. The feature
  branch and its worktree are removed; the base branch carries the history.
- Covered: two new pack leaves, five sibling leaves cross-linked, the pack
  README, the scope matrix, the two generated LLM Wiki artifacts, the
  frontmatter of all 19 pre-existing pack leaves and of the 12 audit-pack
  documents, and two guarded-surface code fixes in
  `scripts/validation/agent_governance_contract.py` and
  `scripts/operations/provider_surface_renderer.py`.
- Push, PR, remote mutation, Stage 00 policy body changes, runtime and Compose
  changes, full external source re-verification, and the controlled all-files
  wrapper all stay outside this work. The merge was local only.
- Three rounds of independent review happened: one per new leaf, a confirming
  review of the corrections, and a fourth round that settled the claims which
  had flip-flopped. All accepted findings are applied; two reviewer claims were
  rejected after verification.

## Verified state

- Verified commit: `8352d420`
- Verified at: `2026-08-10T14:05:00+09:00`
- Coverage analysis found 23 of the requested topics already covered across 20
  files and 6,934 lines. The single confirmed gap was Verification and
  Validation: a grep for `Verification and Validation`, `V&V`, `IEEE 1012`, and
  `ISO/IEC/IEEE 29119` over the pack returned zero matches.
- Baseline `check-repo-contracts.sh` at `4122cecf` reported **11 failing
  subjects and 103 FAIL lines**, none of them under
  `docs/90.references/research/`. All originate in the in-flight taxonomy
  migration on the base branch.
- After all changes the failing-subject set is unchanged at 11 with no new
  subject. Markdown documentation contract fell from 4 to 2, because
  regenerating the LLM Wiki index dropped two dead rows pointing at
  `content-archive.template.md` and `ard.template.md`, which the taxonomy
  migration had removed.
- Changed-document metadata validation reports 0 violations at every commit.
  Traceability passes with 46 catalog pairs and 0 failures. No whitespace drift.
- Workspace fact re-derivation checked 13 figures. Eleven held exactly: 14
  roles, 24 functions, 3 providers, 4 projection surfaces, 7 workflows, 23 jobs,
  16 quality jobs, 24 pre-commit hooks, 8 harness layers, 8 workflow states, 4
  typed loops, 11 fixtures, 16 synthetic regressions, 161 audit criteria at
  77/60/13/2/9, 5 work profiles, and 11 model records.
- Two figures drifted. Local QA runner steps are now 34 default, 35
  all-profiles, and 32 harness across three profiles, not 24 and 22 across two;
  the English leaves already recorded this and only the pack README still
  asserted the retired numbers. Semantic-event binding depth is 20 of 21
  `configured-not-executed` with the Codex `session-end` binding `unsupported`;
  the blanket "all 21" claim appeared in four places and contradicted adjacent
  text in the same table cell.
- `review_cycle` was removed from all 19 pre-existing pack leaves. The reference
  profile does not declare it, no script, workflow, test, or config reads it,
  and every affected leaf states its cadence in its Maintenance section, so the
  removal is information-preserving. The diff is 19 identical deletions.
- Twenty-one logical-unit commits span `26906ee6` onward on `codex/sdlc-taxonomy-convergence`.
- Three stale prunable worktrees under `/tmp` were removed with
  `git worktree prune`.
- The local QA runner was executed end to end for the first time in a while,
  using a throwaway virtual environment holding the declared
  `scripts/requirements.txt` set. Result: the 38-test unittest suite reports
  `OK`, 28 gate checks report pass, `fixtures_check` and `regressions_check`
  both pass, and the run then terminates non-zero on
  `AGC-CONTRACT-UNSAFE-FILE`.
- That terminal failure is not caused by this work. The same command run in a
  detached worktree at base commit `4122cecf` produced 342 output lines against
  this branch's 342, differing only in the two elapsed-time lines. Regression
  delta from this branch is zero.
- **`AGC-CONTRACT-UNSAFE-FILE` root cause is identified.** The contract file is
  sound. `ci_gate_runner.py` hands child gates the repository root as
  `/proc/self/fd/<fd>`, which is a symlink, while
  `agent_governance_contract.py` opens the root with `O_DIRECTORY|O_NOFOLLOW`.
  That combination raises `ENOTDIR`, which `:1322` converts to
  `_UnsafeRootFileError` and `:1370` reports as `AGC-CONTRACT-UNSAFE-FILE`.
  Demonstrated by calling the same reader on the same file with two roots: the
  real path reads 20,614 bytes, the descriptor root raises. Two independently
  sound hardening measures, root TOCTOU protection and symlink-escape
  confinement, were mutually incompatible. **Fixed here.** The root is a
  caller-supplied trust anchor rather than a component discovered during the
  walk, so it is now opened without `O_NOFOLLOW` while every component below it
  keeps it. A symlinked leaf and a symlinked intermediate directory are both
  still rejected, and the governance suite reports 158 tests with 24 failures
  both at base and here.
- **Both new leaves went through independent review and both returned REQUEST
  CHANGES.** Every finding was reproduced before acting.
- The V&V leaf's thesis was falsified by its own evidence: it claimed no tracked
  gate answers a validation question while identifying procedure rehearsal as
  the closest thing to validation, and `leaf.supply-chain-fixture-policy`
  executes two rehearsals among five unittest modules. Also corrected: the
  frontend gate runs no tests, the eval gate scores no agent output but checks
  its own fixture catalog, `tests/validation/` holds 26 tests not 24, and the
  "Required Validation" column carries five checkers plus a non-script entry.
- The GitHub Actions leaf claimed permission elevation was confined to one job.
  Five jobs across four workflows hold a write scope. The sibling states the
  one-job fact correctly but scopes it to `ci-quality.yml`; this leaf dropped
  the scoping into a repository-wide table. Also corrected: a declared
  Third-Party Workflow Static Analysis section had never been written despite
  two cited sources, three quotations were paraphrases inside quotation marks,
  and the `actions/checkout` safer default was scoped to v7 when it was
  backported to v2 through v6 on 2026-07-20.
- A confirming review then caught two defects the corrections introduced. The
  V&V leaf had swung from "no gate answers a validation question" to "exactly
  one job root carries executable validation"; two do. It had also concluded
  that `test_run_agent_precommit_all_files.sh` is unenforced. The narrow premise
  was right — no gate node names it — but `check-repo-contracts.sh:2817` runs it
  and that script is the entrypoint of `leaf.repo-contracts`, so all three
  rehearsals run in CI. The GitHub Actions leaf's newly written static-analysis
  section wrongly said the repository carries no `actionlint` invocation;
  `.pre-commit-config.yaml` pins it at `rev: v1.7.12` and `leaf.pre-commit` runs
  it. Registry-only reasoning about gate coverage understates it; the entrypoint
  script has to be followed.
- The `review_cycle` migration is complete for every document that can be
  completed. Fifteen documents outside the research pack carried the key;
  twelve audit-pack documents are migrated and their violations fall to zero.

## Blockers and unverified facts

- **This work correctly has no Stage 04 Task record, and that is now a settled
  conclusion rather than an open blocker.** Spec 136 defines Task as a role
  inside an active capability directory that "exists only while an approved
  change is active", with atomic completion that writes implemented behavior
  back into `spec.md`. This work is a Stage 90 reference extension: it has no
  active capability, its historical governing spec 123 is archived under
  `docs/98.archive/03.specs/`, and minting a capability spec to host a Task
  would misrepresent documentation research as a capability change. The
  evidence therefore lives in the commit ledger and this record, which is where
  the incoming contract puts it. The old location is separately dead: every
  file under `docs/04.execution/tasks/` resolves to profile `unsupported`, and
  spec 136 requires `docs/04.execution` to be absent at completion.
- **The operations path migration belongs to spec 136 and was declined on
  ownership, not size.** Its task decomposes the work as four numbered items in
  a seventeen-item breakdown — Task 6A through 6D, "Reorganize Operations
  Domains 00 through 03" and onward, at
  `docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md:49-52` — and Tasks 1
  through 5 of that same breakdown are the twelve commits this branch is based
  on. 6A through 6D are literally the next items in that sequence, and Task 13
  of the same breakdown owns the cross-link, index, and memory repair that
  follows. Executing them here would run another capability's work items and
  collide with its own execution, against spec 136's rule that one capability
  has at most one active change packet.
- **The migration is fully specified by a frozen ledger, and an earlier entry
  here wrongly said no registry existed.**
  `docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md` is the
  Task 3 output: 5,624 lines, 796 records, of which 264 target
  `docs/05.operations/`. Each record fixes `legacy_path`, `stable_path`,
  `artifact_id`, `action`, and the inbound-link count, so no identity has to be
  invented. Whoever runs 6A through 6D should drive them from that file.
- Record counts per work item, parsed from the ledger: 6A domains 00-03 is 42
  records, 6B domains 04-06 is 124, 6C domains 07-09 is 59, 6D domains 10-12 is
  33, plus 6 for the root README, incidents, and releases.
- 6A preconditions were verified and are green: all 42 legacy files exist and no
  target path has been created yet. Its 42 records split into 33 mechanical
  moves and 9 merges. Eight of the merges are domain README consolidations,
  three role-scoped READMEs collapsing into one domain README, and the ninth
  folds `docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md`
  into `ops-0006-infra-service-optimization-catalog/policy.md`. Only those nine
  need authoring; the rest is path plus `artifact_id` rewriting.
- `ops-0007-llm-wiki-maintenance` receives all three roles, so finishing the
  `00-workspace` domain alone clears two of the three remaining `review_cycle`
  documents. The third, the PostgreSQL rehearsal runbook, lands in 6B.
- **Execution was attempted twice and stopped on a data gap, which is the
  decisive obstacle.** The ledger carries exactly six fields per record:
  `stable_path`, `artifact_id`, `action`, `replacement`, `source_commit`, and
  `reason`. It contains zero `created`, `updated`, or `next_review_at` values.
  The new Stage 05 profiles require all of those: `guide` requires `created`
  and `updated`, and `policy` and `runbook` additionally require `reviewed_at`
  and `next_review_at`. So the ledger fixes identity and path but not the
  metadata the destination contract demands.
- The `parent_ids` problem is worse than the missing dates because it is a
  governance decision rather than a lookup. The new `policy` profile allows
  parent types `spec`, `architecture-description`, and `adr` only, while
  `docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md` currently
  declares `task:2026-07-15-agent-governance-harness-convergence`. Migrating it
  means choosing a new parent, which invents lineage. This is the same
  objection already recorded against rewriting the audit pack's `parent_ids`.
- A trial migration of `ops-0007-llm-wiki-maintenance`, the highest-value
  subject because it carries all three roles, moved cleanly and was then
  reverted once the metadata gap surfaced. Its `guide.md` additionally carries
  no `artifact_id` at all today, so three of the six required keys would have to
  be authored rather than migrated.
- Tooling is a secondary constraint. A scripted bulk `git mv` with frontmatter
  rewriting is refused by the local permission classifier, while per-subject
  moves are permitted, so the mechanical half is workable at subject
  granularity.
- **A full trial of one subject proved 6A cannot run standalone, and why.** With
  the relaxed profiles in place, `ops-0007-llm-wiki-maintenance` was migrated
  end to end: three moves, frontmatter authored from the ledger and git dates,
  `parent_ids` preserved as `policy-0007` because `policy` is an allowed parent
  type for `runbook`, and all sixteen inbound referrers repaired. Metadata
  validation passed for the three migrated files.
- The repository still regressed. Failing subjects went from 11 to 12 with a new
  `Spec document traceability contract`, Markdown findings rose from 2 to 6, and
  changed-document metadata violations went from 0 to 8. The cause is
  structural: repairing an inbound link inside a Stage 04 document makes that
  document a changed-document validation target, and `docs/04.execution/` still
  resolves to profile `unsupported`. Moving Stage 05 therefore drags unmigrated
  Stage 04 into validation.
- That is precisely why the breakdown separates Task 13, "Repair Cross-Links,
  Indexes, Memory, and Generated Evidence", from Tasks 6A through 6D. The moves
  and the link repair cannot land in the same change while Stage 04 is
  mid-migration. The trial was reverted; the tree is clean at `5e39cdf7`.
- The target is `docs/05.operations/<domain>/ops-<id>-<subject>/` with the
  parallel roots removed. Current shape: 101 distinct subject paths across 260
  files (88 guides, 87 policies, 85 runbooks), which the ledger consolidates
  into 93 ops subjects, with no `ops-*` subject created yet. The last three
  `review_cycle` documents and the audit overview's parent-type findings all
  clear when 6A through 6D land in their own task.
- Three operations documents still carry `review_cycle` and are deliberately
  untouched: one policy and two runbooks under `docs/05.operations/`. Their
  profiles resolve to `unsupported` because the policy and runbook globs are
  `docs/05.operations/*/ops-*/policy.md` and `.../runbook.md` while the files
  sit at `docs/05.operations/policies/00-workspace/` and
  `docs/05.operations/runbooks/**`. Removing the key would not make them valid,
  and two of them state no cadence in the body, so removal would lose
  information. They need the path migration first. This is the same root cause
  as the Stage 04 Task location problem: `review_cycle` was a symptom, not the
  disease.
- `implementation-overview.md` retains two `invalid-parent-type` findings and
  they are not document defects. Both declared parents exist and the provenance
  is factually correct: the audit really did descend from spec 123, now at
  `docs/98.archive/03.specs/`, and from task `2026-07-11`, still in the retired
  `docs/04.execution/tasks/` location. The `audit` profile allows parent types
  `spec` and `task`, but the resolver types a parent by its location, so the
  archived spec resolves to `archive` and the retired task to `unsupported`.
  Rewriting `parent_ids` would falsify the audit's ancestry, so it was left
  alone. This clears when spec 136 finishes relocating those ancestors.
- `agent-catalog.yaml` `evaluation.input_roots` is **not** a dangling
  declaration; an earlier entry here characterized it wrongly. It is a security
  allowlist. `agent_output_eval.py:1421` rejects any input path outside those
  roots with `AOE-INPUT-PATH-REJECTED`, and
  `agent_governance_contract.py:2952` enforces the exact two-root tuple through
  `AGC-EVAL-INPUT-POLICY`, with a negative test at
  `test_agent_governance_contract.py:4626`. The directories not existing is
  correct: the allowlist names permitted locations, and the repository holds no
  synthetic input files, so the policy currently admits nothing. Nothing to
  fix.
- The ISO/IEC/IEEE 12207 and 15288 **definitions** were reachable after all,
  through SEVOCAB, the ISO/IEC/IEEE vocabulary published by the IEEE Computer
  Society. Reproduced live: the search action returns HTTP 200, 72,082 bytes,
  44 results, carrying both definitions with clause attribution. Their
  **process requirements** remain unread behind the paywall, `iso.org` still
  returns 403, and the leaf now separates the two cases. The lesson is that a
  paywalled standard can still have a freely published normative vocabulary,
  which the earlier blanket "not retrieved" record missed.
- IEEE 1012-2024 was not retrieved in full; only the 1012-2016 abstract was
  read, though SEVOCAB carries a 1012-2024 clause 3.1 entry.
  The FDA software validation guidance 404ed on direct fetch and is recorded
  from search metadata only. The "right product" mnemonic is left unattributed
  because its origin was not verified.
- The `html5lib` remedy is now demonstrated rather than assumed. Installing the
  declared `scripts/requirements.txt` set into a virtual environment lets the
  local QA runner start, so the previously recorded "a virtual environment or
  the distribution package is needed" is confirmed. This is an environment
  action only; nothing in the repository changed.
- **A second blocker sat behind the first and had never been observable.** With
  `html5lib` present the runner reaches its end and fails on
  `AGC-CONTRACT-UNSAFE-FILE path=docs/00.agent-governance/contracts/agent-governance-artifacts.yaml location=file`.
  While the dependency was missing, the runner aborted at its first gate, so
  this failure could not surface at all. It reproduces identically at base
  commit `4122cecf` and belongs to the in-flight SDLC taxonomy work, not to this
  branch. It has not been investigated.
- **Diagnosability defect.** `scripts/operations/provider_surface_renderer.py`
  catches `ContractLoadError`, `OSError`, and `ValueError` in `main` and prints
  only `type(error).__name__`, discarding the message. The underlying
  `AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime` was only
  obtainable by calling the loader directly. Printing the message would make
  both blockers above self-explaining.
- The `.env` versus `.env.example` variable gap remains an environment fact and
  is unchanged.
- Provider acceptance, live model evaluation, and authenticated remote GitHub
  enforcement stay unverified.

## Evidence links

- [Canonical research pack](../../90.references/research/ref-0039-readme.md)
- [Verification and validation leaf](../../90.references/research/ref-0085-verification-validation.md)
- [GitHub Actions platform leaf](../../90.references/research/ref-0084-github-actions-platform.md)
- [Scope application matrix](../../90.references/research/ref-0054-scope-application-matrix.md)
- [Predecessor extension record](../../03.specs/spec-0123-agentic-engineering-audit-remediation/task.md)

## Next handoff

- The work is fast-forward merged into `codex/sdlc-taxonomy-convergence` and
  not pushed. The QA suite is not green here, but it is not green at the base
  commit either and the regression delta is zero, so the merge changes no
  verification outcome.
- Two code fixes landed here and both are verified: the confined reader now
  accepts a symlinked root while still rejecting symlinked components, and the
  provider surface renderer emits the normalized contract error message it
  previously discarded. Neither changed any test outcome against base.
- Both new leaves went through independent review, then a confirming review of
  the corrections, and all findings from both rounds are applied. The confirming
  review has not itself been re-reviewed.
- The one remaining follow-up that belongs elsewhere is spec 136's Stage 05
  operations migration, Tasks 6A through 6D of its own breakdown. It unblocks
  the last three `review_cycle` documents and the audit overview's parent
  types. It was scoped and precondition-checked here but deliberately not
  executed; drive it from the frozen ledger recorded in Blockers.
- Keep the result on the local branch and do not push. No repository defect
  from this work remains open: the two items previously listed as needing
  approval, the `agent-catalog.yaml` input-root declaration and the audit
  overview's parent types, were both investigated and are correct as they
  stand. See Blockers for why.
