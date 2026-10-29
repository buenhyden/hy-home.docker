---
title: "Deferred and Not-Run Review Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0017"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Deferred and Not-Run Review Task

## Overview

### Objective

Execute W33: review again the items TSK-0016 left deferred or not run. This
Task owns criterion 28 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for the deferred and not-run items to be
reviewed and the work carried through to merge. The input is `main` at merged
PR #613. The authorization covers test edits in this repository, read-only
GitHub API reads, read-only reads of the other three repositories, this
branch, its pull request, and merge. It grants no remote setting change, no
write to another repository, and no runtime start.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0017 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0017 | ready | in-progress | #objective |
| SPEC-0212-TSK-0017 | in-progress | completed | #evidence |

### Past-removal absence checks

| TSK-0016 row | Decision | Current guard |
| --- | --- | --- |
| `infra/11-laboratory`, `infra/09-tooling` (and its per-package loop) | Replaced | `test_infra_has_exactly_the_registered_tiers` asserts `infra/` holds exactly the 13 ADR-0046 tiers; a stale `infra/09-tooling` fails it. |
| `scripts/validation/check-repo-contracts.sh` | Removed | `check-script-manifest.py` reports `manifest-record-missing` for a tracked script without a row, and the same test asserts the manifest does not name it. |
| `infra/10-communication/mailpit` | Kept, reclassified | ADR-0046 and architecture description 0010 place Mailpit in `11-quality`; a second package would duplicate it. This is a current rule. |
| Prefixed `mig-0003` migration path | Kept, reclassified | The frozen migration has one path; a prefixed copy would be a second frozen record. This is a current rule. |

### Remote protection

Read back through the authenticated API on 2026-10-29 for `main`: required
context `candidate-quality` with `strict=true`, zero required approvals,
`require_code_owner_reviews=false`, conversation resolution on,
`enforce_admins=true`, force pushes and deletions off, linear history off, and
no repository rulesets. This matches `.github/rulesets/main-protection.md`.

One gap remains for the owner. The repository allows squash and rebase merges,
but an archive authorization's `decision` names a commit that must stay
reachable from `main`. A squash or rebase merge of a pull request that adds
one would leave that commit unreachable. Restricting the merge methods is a
remote setting change and is not made here.

### Four repositories

Read without writing on 2026-10-29. Project-Template and hy-home.k8s were read
from their local checkouts at `HEAD` without fetching; blog-data was read from
its remote `dev` branch through the API.

| Repository | Branch@revision | `bootstrap.md` | `documentation-protocol.md` | `sdlc.md` | `98.archive/README.md` | `retention-catalog.md` |
| --- | --- | --- | --- | --- | --- | --- |
| hy-home.docker | `main`@`da59f63a7` | 1.5.1 | 3.5.1 | 1.4.3 | 2.6.0 | 1.2.0 |
| Project-Template | `dev`@`9af5c1b6` (local) | 3.4.1 | 11.6.3 | 8.0.1 | 8.2.1 | absent |
| hy-home.k8s | `main`@`69445fca` (local) | absent | absent | 3.0.0 | 0.8.2 | absent |
| blog-data | `dev`@`af40f1417` (remote) | absent | absent | 1.7.0 | 2.1.3 | absent |

Each repository versions these files independently; no shared
`semantic_id@revision` identifies one common edition. Four-repository
adoption therefore stays unclaimed. Any alignment is work in those
repositories under their own approval.

### Native loaders and runtime

This Claude Code session loaded root `CLAUDE.md`, which imported
`.agents/governance/bootstrap.md` and `.claude/provider.md`; that is a direct
observation of the Claude loader for one session. The Codex loader was not
observed. Runtime acceptance needs `docker compose up`, which this work may
not run, so it stays `NOT_RUN`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tier and routing tests | 28 | W33 | `python3 -m unittest tests.validation.test_infra_tier_layout tests.validation.test_agent_governance_ci_routing` | This branch | PASS | Both modules OK | required | - |
| Tier negative check | 28 | W33 | Same tier test with a temporary empty `infra/09-tooling` | This branch | PASS | Fails naming `09-tooling`; directory removed after | required | - |
| Manifest negative check | 28 | W33 | `check-script-manifest.py` with an intent-to-add `check-repo-contracts.sh` | This branch | PASS | `manifest-record-missing`; file removed after | required | - |
| Remote protection read | 28 | W33 | `gh api repos/buenhyden/hy-home.docker/branches/main/protection` and `/rulesets` | 2026-10-29 | PASS | Matches the tracked proposal; merge-method gap recorded | required | - |
| Cross-repository read | 28 | W33 | `git show HEAD:<file>` in two local checkouts; `gh api …/contents?ref=dev` for blog-data | 2026-10-29 | PASS | No shared edition identifier | required | - |
| Codex loader acceptance | 28 | W33 | Native Codex session load | - | NOT_RUN | Not observable from this session | optional | - |
| Runtime acceptance | 28 | W33 | Compose start and health | - | NOT_RUN | Runtime start not authorized | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 28 | accepted | Tier and routing tests, Tier negative check, Manifest negative check, Remote protection read, Cross-repository read | Two past-removal checks replaced by current-rule guards, two reclassified; remote protection matches with one merge-method gap for the owner; four-repository adoption not claimed; Codex loader and runtime stay not run. | SPEC-0212 TSK-0017 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
