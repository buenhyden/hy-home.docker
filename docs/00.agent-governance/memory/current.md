---
layer: agentic
status: active
---

# Current Project Memory

## Current objective

- Current task: none. This work has **no valid Stage 04 Task record**, because
  the repository is mid-migration and no conformant location exists for a new
  one. See Blockers.
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

- Branch `codex/agentic-research-vv-gha` in worktree
  `.worktrees/agentic-research-vv-gha`, based on `4122cecf`.
- Covered: two new pack leaves, five sibling leaves cross-linked, the pack
  README, the scope matrix, the two generated LLM Wiki artifacts, and the
  frontmatter of all 19 pre-existing pack leaves.
- Push, PR, merge, remote mutation, Stage 00 policy body changes, runtime and
  Compose changes, full external source re-verification, and the controlled
  all-files wrapper all stay outside this work.
- Independent review has not happened.

## Verified state

- Verified commit: `4fde01f8`
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
- Six logical-unit commits span `26906ee6` to `4fde01f8`.
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
  confinement, are mutually incompatible. Nothing was changed;
  `scripts/validation/` is a guarded surface and the remedy is a design choice.
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
- One reviewer claim was itself wrong and was corrected rather than copied:
  `test_run_agent_precommit_all_files.sh` is registered in no gate node.
- The `review_cycle` migration is complete for every document that can be
  completed. Fifteen documents outside the research pack carried the key;
  twelve audit-pack documents are migrated and their violations fall to zero.

## Blockers and unverified facts

- **No conformant Stage 04 Task location exists.** The task profile in
  `docs/99.templates/support/document-metadata-profiles.yaml` now globs
  `docs/03.specs/spec-*/task.md`, and every existing file under
  `docs/04.execution/tasks/` resolves to profile `unsupported` and fails
  validation. The new location would require creating a numbered Spec, which
  this work deliberately avoided, and the one existing co-located task sits in
  `docs/03.specs/136-sdlc-taxonomy-convergence/` whose directory name does not
  match the declared `spec-*` glob either. No Task record was invented; this
  needs a decision.
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
- `implementation-overview.md` in the audit pack retains two
  `invalid-parent-type` findings, one for a spec that moved to archive and one
  for a task that resolves to `unsupported`. Both predate this work.
- `agent-catalog.yaml` declares `evaluation.input_roots` pointing at two
  directories that do not exist. Both gates pass, so this is a dangling
  declaration rather than a broken gate.
- ISO/IEC/IEEE 12207, 15288, and the paywalled 29119 parts could not be
  retrieved. `iso.org` returns HTTP 403 to automated clients and the publicly
  available standards page now redirects to the paid webstores. No definition
  from them is quoted or paraphrased anywhere.
- IEEE 1012-2024 was not retrieved; only the 1012-2016 abstract was read.
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

- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Verification and validation leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/verification-validation.md)
- [GitHub Actions platform leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/github-actions-platform.md)
- [Scope application matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/scope-application-matrix.md)
- [Predecessor extension record](../../04.execution/tasks/2026-08-07-agentic-research-pack-extension.md)

## Next handoff

- The branch is kept as-is by decision: not merged, not pushed, worktree
  preserved at `.worktrees/agentic-research-vv-gha`. Integration was deliberately
  not offered because the QA suite is not green, and it is not green on the base
  branch either.
- Three follow-ups are worth more than they cost and none belongs to this work:
  decide how to reconcile the descriptor root with the `O_NOFOLLOW` reader,
  make `provider_surface_renderer.py` print the exception message it currently
  discards, and migrate the operations document paths so the remaining three
  `review_cycle` documents can be completed.
- Independent review of both new leaves is done and its findings are applied.
  Neither reviewer re-reviewed the corrections, so a confirming pass is still
  open if one is wanted.
- Keep the result on the local branch and do not push. Decide where a Stage 04
  Task record for this work belongs before treating it as complete, since the
  governance verification gate expects one and none can currently be written
  conformantly. Independent review of the two new leaves has not happened. The
  `review_cycle` migration for the remaining thirteen documents and the
  `agent-catalog.yaml` dangling path both need separate approval.
