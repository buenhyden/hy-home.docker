---
title: "Document Governance Dead Code Removal"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0186-TSK-0001"
parent_ids:
- "SPEC-0186"
- "SPEC-0186-PLAN-0001"
created: "2026-09-28"
---

# Document Governance Dead Code Removal

## Objective

Execute W0 through W4 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0186](../spec.md).

## Inputs

- The SPEC-0184 Task, Deferred Items, P3 entry.
- The owner's choice of 2026-09-28: P3 first, with Spec and Plan approval
  before execution.
- Baseline: the local `main` at `ac15a6f84`.

## Work Log

- 2026-09-28: Spec, Plan, and Task drafted on branch
  `chore/document-governance-dead-code`.
- 2026-09-28: The owner approved the Spec and Plan. Execution ran on the
  branch while the package stays `draft` against `main`; promotion follows the
  local `main` merge, as SPEC-0184 did.
- 2026-09-28: W0 recorded the twelve changed-profile member summaries.
- 2026-09-28: W1, W2, and W3 each removed one candidate in its own commit.
- 2026-09-28: W4 reran the gate members and both unit suites.

## Verification Evidence

W0 and W4 ran the twelve changed-profile members except
`check-conftest-policy.sh`, which runs `docker compose` and is outside this
request. Every member returned 0 both times, and each member's closing summary
lines match between the two runs, apart from the merge-base hash.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: `git grep load_artifact_contract` found only Stage 03 prose, no code or test caller; removed (`7822e9714`) | [agent_governance_contract.py](../../../../scripts/lib/agent_governance/agent_governance_contract.py) |
| 5 | W1 | PASS: `tests/lib` 944 tests OK after the removal | [agent_governance_contract.py](../../../../scripts/lib/agent_governance/agent_governance_contract.py) |
| 2 | W2 | PASS: `origin/main` and `main` both carry `docs/98.archive/retention-catalog.md`; the README fallback and its one test removed (`6f7ad596b`) | [archive.py](../../../../scripts/lib/document_governance/archive.py) |
| 5 | W2 | PASS: `test_archive` 78 tests OK after the removal | [archive.py](../../../../scripts/lib/document_governance/archive.py) |
| 3 | W3 | PASS: `_reviewed_evidence_findings` has no caller, so the Foundation wave, its Stage 04 paths, the consumer-scan helpers, and six finding codes were unreachable; removed (`d6b8fdb23`) | [lifecycle/contract.py](../../../../scripts/lib/document_governance/lifecycle/contract.py) |
| 5 | W3 | PASS: `tests/validation/lifecycle` and `test_promoted` OK after the removal | [lifecycle/contract.py](../../../../scripts/lib/document_governance/lifecycle/contract.py) |
| 4 | W0 | PASS: twelve members returned 0; summaries recorded, including metadata `selected=4 violations=0`, links `documents=968 failures=0`, lifecycle `violations=0` | [Plan](../plan.md) |
| 4 | W4 | PASS: the same twelve members returned 0 with summaries equal to W0 | [Plan](../plan.md) |
| 5 | W4 | PASS: `tests/lib` 943 tests OK (one removed with W2); `tests/validation` 675 tests OK, 23 skipped | [Plan](../plan.md) |

## Review Evidence

- W3 reachability: the frozen manifest
  `docs/98.archive/retired/90.references/data/0067-foundation/data.yaml`
  declares `wave: foundation`, but it is data. No code path passes any manifest
  to the removed check, because the check itself had no caller.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `59ee35621` | Package | Spec, Plan, and Task drafted |
| `7822e9714` | W1 | `load_artifact_contract` removed |
| `6f7ad596b` | W2 | Stage 98 README base read removed |
| `d6b8fdb23` | W3 | Foundation evidence check removed |

## Rulings

- 2026-09-28: Owner approved the Spec and Plan ("승인").

## Deferred Items

- `KNOWN_FINDING_CODES` in `lifecycle/contract.py` has no consumer. It is
  outside the three named candidates, so it stays for a later package.
