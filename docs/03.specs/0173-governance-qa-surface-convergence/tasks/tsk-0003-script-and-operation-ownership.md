---
title: "Script and Operation Ownership Task"
version: "0.8.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-08"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0003"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Script and Operation Ownership Task

## Objective

Remove obsolete wrappers and one-off validation surfaces, relocate operational
entrypoints to their canonical domain, and resolve self-successor lifecycle
residue in the script inventory.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the gate
  composition established by Task 0002.
- `scripts/validation/`, `scripts/lib/`, `scripts/operations/`,
  `scripts/hardening/`, `scripts/hooks/`, `scripts/knowledge/`, and the script
  manifest.
- The wrapper, compatibility, mutation-mode, report, and transition findings
  enumerated in the Plan.

## Work Log

Task 2 converged executable composition at `93a26645` and recorded its focused
evidence at `da88af1d`. Task 3 became ready at `41145af4` and started at
`083eed03`. The initial manifest RED reproduced seven self-successor records;
the bounded cutover then moved every current consumer before deleting a public
wrapper or semantic owner.

Implementation commit `174c29d9` removes the two document-link shell wrappers,
the local QA and harness compatibility dispatchers, the target-surface
executable subsystem, and the standalone audit coverage report. Document graph
validation now has one Python owner, the typed gate is the only public aggregate
CLI, and audit coverage is generated and checked by the audit implementation
matrix owner.

The Compose readiness implementation moved to a non-executable
`scripts/lib/ops/` library behind an executable `scripts/operations/`
entrypoint. The PostgreSQL rehearsal also moved to `scripts/operations/`; its
registered aggregate route is restricted to `--check-config-only`, so no
runtime mutation mode is reachable from validation. Current Requirement,
Architecture, Operations, Research, and Audit consumers were cut over, and the
two affected generated reference outputs were refreshed through their owners.

A later round returned to `scripts/hooks/post-tool-validate.sh`, the one hook
this Task retains, and measured it against the formatting owner rather than
against its own description. Three disagreements reproduced on a clean tree at
`41e83d25e`. The hook ran `shfmt`, which `.pre-commit-config.yaml` does not
register: 19 of 49 tracked shell files are not shfmt-clean, so `shfmt -w`
silently rewrote them on any edit, and because the `shfmt -d` call carried no
`check_only` guard, `--check` failed on all 19. It called `shellcheck` with no
severity while the registered hook passes `--severity=warning`, so six
info-level findings in four files failed the hook and none of them failed the
gate. Its whitespace normalizer performs exactly the trailing-whitespace and
end-of-file fixes that the registered mutators exclude for the frozen archive
payloads, but shared none of that boundary, and a probe under
`docs/98.archive/completed/` was rewritten in both respects.

The convergence removed the unregistered formatter rather than registering it.
`.prettierignore` already records `shellcheck` as the sole owner of `*.sh`, and
adopting shfmt would have reformatted 19 tracked files in a corpus-wide commit
that no request covers. The hook now passes the registered severity and reads
the `frozen_archive_payloads` anchor from `.pre-commit-config.yaml` instead of
restating it, failing closed when a present owner declares no anchor and
excluding nothing when no owner file exists, which is what keeps the temporary
repositories in the hook regressions working.

A second round corrected two statements about the execution surface. The
verification surface map described `--profile full` as the complete local
surface while `_LOCAL_EXCLUDED_GATE_IDS` withholds nine leaves from the local
context, and listed those leaves among the suite roots with nothing to mark
them. The scripts inventory described the CI-only pre-commit entrypoint as
carrying a frontend-lint skip; the script skips the two gate-owned
`public-validation-*` hooks, and `eslint-nextjs` is not a registered hook id.

A third round closed the two items the previous round deferred and the stale
generated graph. The tech-stack drift command has two owners on purpose, and
removing the standalone workflow was rejected on evidence rather than on
policy alone: it is the only tracked workflow with a `paths:` trigger, and the
contract regressions copy the real `.github` tree, so the `path-widening` case
would have lost its vehicle and the validator would have kept no coverage for a
widened path filter. The duplication is now stated at both owners and pinned by
two regressions instead of left implicit.

The two Stage 90 research modules were not stale but wrong when written. The
skip changed to the two gate-owned hooks in `3989da584` on 2026-09-03, which is
an ancestor of `6201fa043`, the commit that set the `observed_at` of 2026-09-05
both modules carry; `eslint-nextjs` had already left `.pre-commit-config.yaml`
in `1c620dd07`. Both declare `review_cycle: on-source-change`, so the correction
is that review, recorded with its own date beside the earlier claim. `AUD-0030`
records the same finding with an `observed_at` that precedes the change, so it
was accurate when written and stays as written.

The tracked knowledge graph was built at `f8a72211` under the project name
`audit-harness-consolidation`, and only 4635 of its 22689 nodes still had an
existing `source_file`. The post-commit hook had refused every rebuild on a
fewer-nodes heuristic, which was protecting a graph that was 80 percent
dangling. The rebuild used the documented `--force` for that case and ran no
labeling, so it cost no tokens.

A fourth round closed the audit and retention items. `AUD-0030` was
re-observed rather than re-dated wholesale: `QAF-04` and `QAF-11` each cited an
`eslint-nextjs` skip, and `QAF-04` also cited a ShellCheck exclusion for a
script Task 3 itself removed. The re-observation found twenty registered hook
IDs rather than twenty-four, no `exclude` on the ShellCheck hook, and no
ESLint hook at all. Both criteria are still met by current behavior, so both
statuses stand and only the evidence changed; each revised cell carries its own
date, the pack keeps `observed_at` at 2026-07-05 because the other rows were
not re-observed, and the matrix was regenerated through its own generator.

The `graphify-out/` retention asymmetry was resolved toward the rule that
already existed. `.gitignore` had listed the directory since it was written
while forty-seven files under it stayed tracked, so the rule governed new
content and not old, which cost 148 MiB of tracked blobs and replaced most of
that on every graph-touching commit. All forty-seven left the index with the
working copy untouched. Nothing in CI depended on them: no gate node or
validator reads the directory, and the health reporter already read the
untracked `manifest.json`. The three documents that described the tracked
arrangement now describe this one.

A fifth round is the first with hosted evidence, and it found what no local run
could. Pull request #146 ran `validation-changed` twice and failed both times on
seventeen `missing-link-target` findings, while the same `check-document-links.py
--mode all` reported zero failures locally. The checker resolves a target against
the filesystem, so the seventeen research modules linking to
`graphify-out/GRAPH_REPORT.md` still resolved on a working copy where that
untracked file sits on disk and resolved nowhere on a fresh checkout. Untracking
the directory is what exposed it; the links had been pointing at a tracked file
until then.

The repository owner merged #146 at 00:20:12Z from `a00f0bb46`, a merge of `main`
into the branch whose branch parent is `6603ef8fc`. The link repair was pushed to
the branch after that merge was cut, so it is not in the merged result: `main` at
`b5293a067` carries the untracking and the seventeen broken links together. This
Task did not merge and did not choose to merge past a failing required check;
`enforce_admins` is false, which is what makes that possible.

Two independent breaks were then measured on `main`. The seventeen links are the
first. The second is unrelated to this package: three Dependabot pull requests
merged compose image bumps for ten components without the curated registry, so
`sync-tech-stack-versions.sh --check` exits 1 on `main`. That is the drift gate
catching real drift, and it is the strongest evidence yet for the earlier
decision not to weaken it. Both are repaired on a branch cut from the merged
`main` rather than by touching `main`.

The repair pull request then produced the finding that matters most. #147 moved
`validation-changed` from failing at one minute thirty-six to failing at nine
minutes forty-seven: the seventeen links are gone, `drift-gate` passes, CodeQL,
GitGuardian, the labeler and the greeting all pass, every unit batch reports OK,
and Compose validation renders twenty-eight selections and two hundred
thirty-two services. It then exits 10 at `leaf.postgres-logical-upgrade-config`
with `status=failed failure_class=preflight reason=source-image-not-local` and
`cleanup_status=passed`.

That failure is not this package's. `assert_exact_local_image_identity` refuses
to proceed unless the pinned image is already present locally with matching
repository, target and config digests, which is a deliberate supply-chain
boundary that forbids an implicit pull. A hosted runner has no such image, so
the leaf cannot pass there. Task 6 already recorded this exact string. The
merged Dependabot pull requests #143 and #145 failed `validation-changed` with
the identical `reason=source-image-not-local` and exit code 10 before this
session began, and #145's `drift-gate` failed with the same `changes=10` this
package repaired.

The last thirty `ci-quality.yml` runs, reaching back to 2026-09-06, are failures
on both `push` and `pull_request` without a single success. Required checks have
therefore been red throughout, and every merge in that window passed by
administrator bypass rather than by a green check. The boundary was left intact:
weakening the identity assertion, reporting an unavailable tool as a pass, or
pulling an image inside the gate would each trade a real guarantee for a green
square. Restoring a truthful hosted gate is an owner decision between preparing
the pinned image in the workflow before the gate runs and excluding the leaf
from CI contexts the way the local context already excludes nine others.

## Verification Evidence

| Check | Result |
| --- | --- |
| Manifest RED | Seven self-successor records reproduced before implementation |
| Script manifest | `check-script-manifest.py` passed; 58 focused tests passed |
| Gate contract and runner | 16 contract tests and 32 runner tests passed; each public plan retained unique normalized invocations |
| GitHub workflow contract | 47 tests passed with 11 intentional Wave-C skips; executable modes and static gate routes passed |
| Document graph | 37 focused tests passed and `check-document-links.py --mode all` reported 689 documents, 5,748 links, and 0 failures |
| Operation boundaries | 46 Compose readiness tests and 51 PostgreSQL rehearsal tests passed; shell syntax passed for both operation entrypoints and the source-only library |
| Entrypoints and audit matrix | 3 validator-entrypoint tests and 9 audit-criterion tests passed; matrix `--check` passed after regeneration |
| Generated references | Audit matrix and both LLM Wiki outputs passed their canonical freshness checks |
| Typed changed profile | `run-ci-gate.py --profile changed --explain` listed each selected canonical entrypoint once and executed none |
| Current residue | Zero current references to deleted Task 3 paths outside the four Task 5 target-surface DATA packages and their registry mapping |
| Metadata and whitespace | Changed metadata selected 25 documents with 0 violations; `git diff --check` passed |
| Hook baseline (2026-09-08) | Clean tree at `41e83d25e`: `run-ci-gate.py --profile full` exit 0 and `unittest discover -s tests` 1183 tests OK with 11 skips |
| Hook RED | `post-tool-validate.sh --check` exit 1 on `gen-secrets.sh` demanding a 483-line reindent; bare `shellcheck` exit 1 on `check-all-hardening.sh` where `--severity=warning` exits 0; a `docs/98.archive/completed/` probe changed SHA-256 across the hook |
| Hook GREEN | The same three reproductions exit 0, 0, and byte-identical; a non-frozen control document is still normalized, so the boundary did not over-exclude |
| Hook regressions | Six new cases in `PostToolFormattingOwnershipTests`; four fail against the previous hook, and the mutator-parity case fails when one `docs/98.archive/` root is dropped from the markdownlint ignore list |
| Local exclusion regressions | Three new cases in `LocalExclusionDocumentationTests`; the identifier comparison fails when `leaf.zizmor` is removed from the transcribed table |
| Post-change full gate | `run-ci-gate.py --profile full` exit 0 at `4c02e73fa` on a clean tree |
| Post-change unit suite | `unittest discover -s tests -p 'test_*.py'` 1192 tests OK with 11 skips, exit 0 |
| Registered shell regressions | `test_run_ci_precommit.sh`, `test_run_agent_precommit_all_files.sh`, and `test_hardening_lib.sh` exit 0; `run-agent-output-eval-fixtures.sh` exits 2 with no arguments by its fail-closed argument contract and exits 0 with its registered argv |
| Generated freshness | `generate-llm-wiki.py --check` and `provider_surface_renderer.py --check` passed on the staged tree; `--check` and `--write` are the renderer's only modes |
| Action provenance | All eight `uses:` references are 40-character SHAs and each resolves to a commit in its upstream repository through a read-only `gh api` lookup |
| Remote protection read-back (2026-09-08) | `branches/main/protection` returns required contexts `validation-changed` and `validation-full`, both bound to app 15368, with `strict=true`, matching the tracked ruleset record |
| Drift-command reach | A plan built for `pull_request`, `push`, and `local` on the declared fallback contains `leaf.local-tech-stack-version-drift` in all three; the workflow and the leaf resolve to one command |
| Drift-command pinning RED | Changing the workflow `run:` to `--dry-run` fails the new comparison; restoring it passes |
| Workflow contract after the change | `check-github-workflow-contract.py` PASS with workflows=6, jobs=8, actions=8; 51 workflow-contract tests OK with 11 skips; 21 tech-stack tests OK |
| Research correction provenance | `3989da584` (2026-09-03) already carried the current skip and is an ancestor of `6201fa043` (2026-09-05), the commit that set both modules' `observed_at` |
| Document contracts after the corrections | `check-document-metadata.py --mode check-changed` selected 6 with 0 violations; `check-document-links.py --mode all` reported 713 documents, 6,155 links, 0 failures; LLM Wiki and audit matrix freshness PASS |
| Graph dangling ratio | Before: 4,635 of 22,689 nodes had an existing `source_file`. After: 16,761 of 18,014 |
| Graph rebuild | 18,014 nodes, 25,229 edges, 1,726 communities, `built_at_commit` equal to HEAD, token cost 0 input and 0 output |
| Graph health after rebuild | `report-graphify-health.sh` keeps contamination, volume, gitlink, generated and god-node counts at 0; `graph_source_files_total` fell from 1,596 to 1,279; status stays advisory for cross-root inferred edges |
| Audit re-observation | `.pre-commit-config.yaml` registers 20 hook IDs (18 `pre-commit`, 1 `pre-push`, 1 `commit-msg`), 13 with an explicit filter, no ShellCheck `exclude`, and no ESLint hook; `recommend-qa-gates.sh` is absent from the tracked tree |
| Audit contract and matrix | `audit_criterion_contract.py` PASS with 11 reports, 161 rows, 161 unique IDs; the matrix was stale before regeneration, `--write` rewrote it, and `--check` reports fresh |
| Retention change safety | No gate node or validator names `graphify-out`; `git rm -r --cached` removed 47 files totalling 155,898,680 bytes while 237 MB stayed on disk; every probed path under the directory is now ignored |
| Inventories after untracking | LLM Wiki `--check` fresh, `check-document-links.py --mode all` 713 documents and 6,155 links with 0 failures, `check-script-manifest.py` PASS |
| Untracked-graph steady state | The post-commit rebuild during `f8ea14c08` left the working tree clean, which the tracked arrangement could not do |
| Round-3 local verification | `run-ci-gate.py --profile full` exit 0 and `unittest discover -s tests` 1194 tests OK with 11 skips at `f8ea14c08` |
| Pull-request identity dry run | `_check_git_flow` accepts the branch `fix/0173-hook-formatting-ownership` with the planned Conventional-Commit title and rejects a non-conforming title, so the pull-request-only leaf was exercised before pushing |
| Hosted run 1 (34172567197) | `pull_request` at `6603ef8fc`: `validation-changed` FAILED in 1m49s with 17 `missing-link-target` findings; `validation-full` skipped by its `if` condition, as designed for a pull request |
| Hosted run 2 (34172977726) | `pull_request` at `a00f0bb46`, the owner's merge of `main` into the branch: `validation-changed` FAILED identically with `links=6155`, so it did not contain the repair pushed afterwards |
| Local versus hosted divergence | `check-document-links.py --mode all` reported `failures=0` locally and 17 missing targets on the runner, because the target existed on disk as untracked output and not in the checkout |
| Repair and guard | Removing the 17 links moved `links` from 6,155 to 6,138 with `failures=0`; the new `IgnoredLinkTargetTests` fails with the offending document and target when one link is restored |
| Main breakage measured | At `b5293a067`, `git grep` finds the 17 links and `sync-tech-stack-versions.sh --check` exits 1 for 10 components; `git ls-tree` confirms zero tracked files under `graphify-out/` |
| Drift repair | The script's own remedy rewrote the registry, the provenance snapshot was regenerated through its generator, and `test_direct_current_docs_use_registry_versions` then required Traefik, Ollama, and Dozzle README citations to follow |
| Round-5 local verification | On the repair branch at `cca15d647`: `run-ci-gate.py --profile full` exit 0 and `unittest discover -s tests` 1195 tests OK with 11 skips |
| Generated outputs on the repair branch | LLM Wiki, audit matrix, security readiness, supply-chain summary, provider renderer, and tech-stack provenance all report fresh |
| Hosted run 3 (34178910270) | PR #147: `validation-changed` FAILED after 9m47s with zero `missing-link-target`, all unit batches OK, Compose validation passing 28 selections and 232 services, then exit 10 at the PostgreSQL rehearsal preflight |
| Hosted checks that passed on #147 | `drift-gate`, `Analyze (actions)`, `Analyze (javascript-typescript)`, `Analyze (python)`, `CodeQL`, `GitGuardian Security Checks`, `triage`, `pull-request-greeting`; `validation-full` and `issue-greeting` skipped by their conditions |
| Pre-existing hosted failure | Runs 34160561874 (#143) and 34164770210 (#145) both failed with `failure_class=preflight reason=source-image-not-local` and exit code 10, before this session |
| Hosted history | The last 30 `ci-quality.yml` runs, back to 2026-09-06, are failures on both `push` and `pull_request`, with no success in the window |
| Main push after #146 | Run 34172984899 at `b5293a067` fails on `missing-link-target`, which `7cd7c8ab4` repairs |
| Main push after both repairs | Run 34180222230 at `edab4a89b` passes every unit batch and Compose validation with 28 selections and 232 services, then fails only at the preflight; the link and drift failures are gone |
| One environment-dependent case | `test_post_tool_checks_each_changed_shell_file_for_syntax` asserted on stderr while ShellCheck rejects the same file first on stdout, so it passed where shellcheck sits outside the restricted PATH and failed on a runner carrying `/usr/bin/shellcheck`; the pre-change hook reproduces it identically, so it is the case being environment-dependent |
| Hosted convergence | Across runs the failure moved 1m36s, 6m04s, 9m47s, 13m29s as each cause was removed; run 34182514443 reaches the same single preflight that `main` reaches, with every unit batch OK |

## Review Evidence

Focused mutation tests reject duplicate public invocations, runtime validator
rebinding, executable manifest composition, untracked entrypoints, self-
successors, and operation authority drift. The final independent repository
review remains assigned to Task 0006 and must recheck that retired paths have
no current consumer and that operational write modes are not reachable from
validation profiles.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `083eed03` | Start Task 3 from the accepted Task 2 milestone |
| `174c29d9` | Align command ownership, relocate operation entrypoints, remove obsolete wrappers and target-surface executables, and cut over current consumers |
| `69b131ad0` | Converge the retained PostToolUse hook on the registered formatting owner: no unregistered shell formatter, the registered ShellCheck severity, and the frozen payload boundary read from its anchor |
| `4c02e73fa` | State the nine leaves the local context withholds and correct the CI-only pre-commit skip description, with the regressions that keep both from drifting |
| `eddaf6545` | State that the required gate leaf runs the tech-stack drift command first and pin the workflow to it |
| `e023c14bf` | Correct the CI pre-commit skip the two Stage 90 research modules transcribed |
| `228b7e6a4` | Rebuild the knowledge graph from the current tree as its own generated-artifact unit |
| `21ed0d434` | Re-observe and rewrite the two audit rows that named a removed hook id, and regenerate the matrix |
| `f8ea14c08` | Remove every tracked file under `graphify-out/` so its existing ignore rule governs the whole directory |
| `6603ef8fc` | Record the audit revalidation and the retention change |
| `7cd7c8ab4` | Stop tracked documents from linking into an ignored path, and add the regression that catches the class |
| `cca15d647` | Re-point the tech-stack registry to the merged compose tags and carry the three README citations with it |

This evidence checkpoint does not predict its own commit identity.

## Rulings

- Keep a wrapper only when it is a documented public compatibility boundary
  with a current consumer.
- Validation profiles may call operation check modes but never operation write
  modes.
- Resolve transition records to a real successor or a terminal lifecycle; a
  script cannot be its own successor.
- A hook formats only what `.pre-commit-config.yaml` registers. Where a tool
  cannot read that file, it restates the boundary in its own configuration and a
  registered test compares the two by what they select.
- A document that names a verification surface names what that surface does not
  cover, and a registered test compares the claim against a built plan.

## Deferred Items

- `leaf.postgres-logical-upgrade-config` cannot pass on a hosted runner. Its
  preflight requires the pinned image to be present locally with matching
  digests and refuses an implicit pull, which is the supply-chain guarantee and
  is not weakened here. Restoring a truthful hosted gate means either preparing
  that image in the workflow before the gate runs, which the workflow contract
  admits one bootstrap step for, or excluding the leaf from CI contexts as the
  local context already excludes nine leaves. Both change registered
  composition and belong to the owner.

- `main` at `b5293a067` carries seventeen broken links and a ten-component
  registry drift. Both are repaired on `fix/0173-ignored-link-targets`, cut from
  that commit, and reaching `main` needs a merge this Task does not perform.
- Pull request #146 was merged while its required `validation-changed` check was
  failing. Whether to require administrators to pass required checks is a remote
  control-plane decision recorded in `.github/rulesets/main-protection.md`, and
  changing `enforce_admins` needs owner approval and a new read-back.
- The hosted runs surfaced two checks no tracked file declares: CodeQL default
  setup, which contributes `Analyze (actions)`, `Analyze (javascript-typescript)`
  and `Analyze (python)`, and a GitGuardian app check. `.github/workflow-contract.yml`
  knows six workflows and neither of these, so the tracked surface does not
  describe everything a pull request runs.

- Historical Git blobs and immutable archive evidence are not rewritten.
- New general-purpose script frameworks are outside the bounded convergence
  scope.
- Task 0005 completed retirement of the four target-surface DATA packages and
  their registry mapping in `37a756f2`; they are not current executable
  consumers. The earlier residue count above remains Task 3's execution
  snapshot. See the
  [Task 0005 ledger](tsk-0005-document-and-provider-residue.md#commit-ledger).
- `.github/workflows/tech-stack-version-sync.yml` runs
  `scripts/operations/sync-tech-stack-versions.sh --check`, and
  `leaf.local-tech-stack-version-drift` runs the same entrypoint with the same
  argv as a root of `repository-integrity`, which is the declared changed-profile
  fallback and is withheld from neither the local nor the pull-request context.
  Every pull request to `main` therefore executes that command inside the
  required `validation-changed` job, and a compose-touching pull request executes
  it a second time. It was not removed: `github-governance.md` registers the
  workflow in its Non-Gating GitHub Automation table with a stated purpose and
  `quality-standards.md` names it as non-gating remote automation, and because
  it is the only tracked workflow declaring a `paths:` trigger while
  `workflow_fixture` copies the real `.github` tree, so the `path-widening`
  regression would lose its vehicle and no coverage would remain for a widened
  path filter. Resolved in `eddaf6545` by making the duplication deliberate
  rather than accidental: the workflow header and the governance row both state
  that the required leaf runs first, and two regressions compare the workflow
  run step against the leaf entrypoint and argv and assert the leaf is in a
  built pull-request plan.
- The `eslint-nextjs` skip claim was corrected in `e023c14bf` for
  `m0001-platform-mechanics.md` and `m0014-quality-ci-formatting.md`, which were
  wrong at their own `observed_at` rather than overtaken later, and which
  declare `review_cycle: on-source-change`. `AUD-0030` and its generated matrix
  mirror still carry the finding in `QAF-04` and `QAF-11`. That report's
  `observed_at` of 2026-07-05 precedes the change, so the finding was accurate
  when recorded. The revalidation ran in `21ed0d434` and did not move either row
  to `Needs Revalidation`, because re-observing found both criteria still met;
  the evidence was rewritten with its own date instead, and the matrix was
  regenerated through its generator.
- The rebuilt graph keeps 1,050 nodes whose `source_file` is an absolute path
  under a former checkout location and the retired `docs/00.agent-governance`
  layout. They are LLM-extracted document nodes, and `graphify update`
  re-extracts code files only, so a semantic re-extraction with an LLM backend
  is what would drop them. Editing the generated artifact by hand is not a
  substitute.
- The `graphify-out/` retention asymmetry is closed in `f8ea14c08`. The
  directory is untracked in full, Git history holds the removed snapshots, and
  `graphify update .` rebuilds the current graph without API tokens. Re-tracking
  anything under it needs `git add -f` and a stated reason.
- Reverting `174c29d9` is the Task 3 rollback boundary. Restoring only a wrapper
  or target-surface library would recreate split ownership and is not a valid
  partial rollback.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Gate composition Task](tsk-0002-gate-composition-convergence.md)
