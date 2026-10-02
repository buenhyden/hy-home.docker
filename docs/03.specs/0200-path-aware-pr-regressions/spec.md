---
title: "Path-Aware Pull Request Regressions"
version: "0.1.1"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0200"
parent_ids:
- "REQ-0024"
- "REQ-0027"
- "AD-0027"
created: "2026-10-02"
---

# Path-Aware Pull Request Regressions

## Overview

Keep the single required pull-request `validation-changed` check introduced by
SPEC-0199, but run expensive document-governance *regression tests* only when
their implementation or contract changes. Document-only pull requests must
still run the current document metadata, lifecycle, link, and repository
contract validators. The manual `full` profile retains every regression test.
No new `dev` branch or second required status is introduced.

The user reviewed and approved the written Spec on 2026-10-02. Repository
lifecycle publication proceeds through each registered state on trusted main.

The observed successful PR run
[`36939016845`](https://github.com/buenhyden/hy-home.docker/actions/runs/36939016845)
took 17 minutes 5 seconds; its single public-gate step took 16 minutes 46
seconds. Two document-governance regression groups reported 129 tests in
248.534 seconds and 628 tests in 415.821 seconds. Their fixtures exercise the
validator implementation, not the content of each documentation change.
This design preserves content validation while removing that repeated test
cost from documentation-only candidates.

## Boundaries and Inputs

The current ownership graph is `.github/workflow-contract.yml`,
`scripts/lib/gate/ci_gate_contract.py`, and
`scripts/validation/ci_gate_runner.py`; the hosted owner is
`.github/workflows/ci-quality.yml`. The current `local.document-corpus-lifecycle`
aggregate mixes document validators with regression tests. The two measured
slow targets are `leaf.local-document-metadata-tests` and
`leaf.document-governance-library-regressions`; inspect their dependencies
before changing their routing. Other leaves retain their current ownership.

In scope: changed-path root selection, the existing gate contract and its
focused mutation tests, CI governance prose, and any stale statement exposed
by the audit. Review `.github` definitions and the script/test manifest for
live consumers. A file is removed only with evidence that it is unreachable
or has a tested canonical replacement; no deletion count is required.

Out of scope: creating `dev`, changing the `validation-changed` required
context, adding workflow-level path filters, weakening main protection,
changing the `main-current` updater, modifying installed global Git hooks,
and marking SPEC-0182 or SPEC-0193 complete before their open acceptance
evidence exists. Existing release tags remain immutable.

## Behavior Contract

| Candidate or boundary | Required behavior |
| --- | --- |
| Commit and feature push | Continue SPEC-0199's cheap local checks and no automatic public gate. |
| Documentation-only PR | Run one required `validation-changed` job with all path-specific validators, including `operations-catalog` for `docs/05.operations/`; omit only the two named document-implementation regression groups. |
| Document validator, registry, gate-contract, or associated test change | Include affected document regression groups in the same required PR job. |
| Mixed or unknown changed paths | Fail closed to the complete relevant roots; never interpret an unknown path as permission to skip a regression. |
| Main push | Keep the distinct merged-SHA security audit and dependent `main-current` update, without replaying PR QA. |
| Manual `full` dispatch | Run all registered suites and regressions exactly once per gate ID. |

A PR title edit still executes the full changed-path selection under the same
required context. Stale-run cancellation must never let a lighter run stand
in for an uncompleted candidate validation. GitHub's required-check behavior
means the workflow itself cannot be skipped by a path filter.

## Technical Approach

Reuse the existing `changed_root_rules` mechanism. Separate the expensive
regression leaves from the `local.document-corpus-lifecycle` aggregate and
register them as roots of the existing document-lifecycle suite. Extend
the parser's bounded optional-root allowlist only for those two named leaves,
with mutation tests that reject any other optional root. Select the named
roots for the changed profile only when a changed path can affect their
implementation or contract. Keep them in `full` unconditionally.

The Plan must enumerate the exact dependency prefixes from imports, fixture
readers, registry use, and current test coverage before fixing the rule list.
At minimum consider `scripts/lib/document_governance/`, document validation
entrypoints, their tests, `docs/99.templates/registry.json`, and
`.github/workflow-contract.yml`. Preserve the present fail-closed fallback
when a path does not match any known suite rule. Avoid a new workflow, new
status context, or second selector framework.

## Interfaces and Data

The public CLI remains `run-ci-gate.py --profile changed|full`. The gate
contract remains the single data owner for roots and changed-path rules. The
hosted workflow invokes the same CLI and uses only existing event fields.
No secret, token, runtime service, or data volume changes.

## Failure Modes and Guardrails

- A missing dependency prefix could skip a regression after its own source
  changes. A focused negative test must mutate every declared owner class and
  prove the relevant regression root is selected; unknown paths keep the
  current fail-closed behavior.
- A document-only route could accidentally lose content checks while losing
  test groups. Compare its selected validator IDs and results with the
  baseline; only the implementation regression leaves may disappear.
- A full audit could silently lose tests if roots are merely removed. Assert
  that the full execution plan still contains each former regression gate ID
  once.
- An edited PR run could cancel a synchronized candidate run. Preserve the
  current full changed-path behavior for `edited` events under the required
  context.
- A future path may span code and documentation. Multiple matching rules
  combine; an unrecognized path selects complete roots rather than an empty
  fast path.

## Acceptance Contract

1. A current execution matrix and hosted timing receipt show that commit,
   push, PR, main push, and manual dispatch retain the SPEC-0199 phase owners,
   with no duplicate public gate or second required PR status.
2. A documentation-only changed plan retains all baseline path-specific
   validators: document metadata, lifecycle, links, repository checks, and
   `operations-catalog` for operations docs. It omits only the two named
   implementation regression groups.
3. Changes to each documented implementation, contract, registry, and test
   owner select the affected regressions. Unknown and mixed-path cases fail
   closed. The bounded optional-root allowlist admits only the two named
   document leaves and the existing frontend roots; mutation tests reject
   unrelated optional roots. Focused route tests and the workflow-contract
   checker pass.
4. The manual full plan includes every original gate leaf exactly once; the
   PR title-edit route and main-push/tag route remain correct.
5. The script/test inventory records consumers and replacements for any
   removal. Active files are retained if deletion evidence is absent.
6. Canonical quality governance and `.github` navigation match the new
   routing, including the corrected `run-ci-precommit.sh` skip-list wording.
   The hosted required PR check passes on the candidate, and its elapsed time
   is compared with run `36939016845` without claiming a guaranteed duration.

## Traceability

- [REQ-0024 agent governance](../../01.requirements/0024-agent-governance-standardization.md): REQ-0024-FR-0007, REQ-0024-FR-0008, REQ-0024-NFR-0011, REQ-0024-NFR-0012, and REQ-0024-NFR-0013.
- [AD-0027 canonical adapter](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md): one policy owner and provider-specific bindings.
- [REQ-0027 host verifiability](../../01.requirements/0027-home-development-host.md): REQ-0027-NFR-0004 requires revision-scoped evidence.
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): required status behavior.
- [GitHub skipped workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs): path-filter skips can leave a required check pending.

## Open Questions

None. The exact owner-prefix list and latency result are verification outputs
of the Plan, not an excuse to weaken required validation.

## Operational Impact

Documentation-only pull requests should finish sooner while still failing on
invalid document content. Code changes that affect validators continue to run
their regression tests in the protected PR. Operators retain the same manual
full-audit command, main security result, and `main-current` recovery path.
