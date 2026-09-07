---
title: "Script and Operation Ownership Task"
version: "0.3.0"
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
  workflow in its Non-Gating GitHub Automation table with a stated purpose,
  `quality-standards.md` names it as non-gating remote automation, and the
  repository's own anti-duplication rule forbids a second *required* leaf with
  the same command rather than a non-gating standalone check. Removing it means
  changing both policies, the machine contract, the workflow-name tuple in
  `github_workflow_contract.py`, six test sites, the repository surface, the
  script manifest, and a generated index, which is an owner decision rather than
  a convergence step.
- Stage 90 research still describes the CI pre-commit skip as `eslint-nextjs`,
  in `m0001-platform-mechanics.md` and `m0014-quality-ci-formatting.md`. Those
  are dated observations under a non-authoritative stage and were left as
  written; the current owner in `scripts/README.md` was corrected instead.
- Reverting `174c29d9` is the Task 3 rollback boundary. Restoring only a wrapper
  or target-surface library would recreate split ownership and is not a valid
  partial rollback.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Gate composition Task](tsk-0002-gate-composition-convergence.md)
