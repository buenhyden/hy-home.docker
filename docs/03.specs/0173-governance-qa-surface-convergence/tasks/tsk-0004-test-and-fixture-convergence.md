---
title: "Test and Fixture Convergence Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0004"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Test and Fixture Convergence Task

## Objective

Align test placement with production ownership, replace execution-specific
fixtures with stable contracts or builders, and prevent production code from
depending on the test tree.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the
  canonical owners established by Tasks 0002 and 0003.
- `tests/lib/`, `tests/validation/`, `tests/fixtures/`, test support modules,
  examples, and current fixture consumers.
- The mixed-ownership modules, historical fixed assertions, one-off fixtures,
  and near-duplicate supply-chain cases listed in the Plan.

## Work Log

Task 3 aligned script and operation ownership at `174c29d9` and recorded its
focused evidence at `74a8b05e`. Task 4 became ready at `22759ba6` and started
at `b3b6db74`. The initial production-to-tests RED named the four measured
consumers in Compose readiness, PostgreSQL rehearsal, sample-service delivery,
and supply-chain policy validation.

Implementation commit `85b0fc13` moved 23 reusable operation inputs to
`examples/operations/`, preserving byte identity for 20 pure moves and
replacing completed-Spec identity in three sample-delivery verdict files.
Eleven one-off or negative static fixtures were replaced with deterministic
builders, leaving zero files and zero orphans under `tests/fixtures/`.
Production scripts now have zero references to that tree.

The same commit split CI gate, supply-chain, metadata identity, and script
manifest tests by model/library, plan/policy, wrapper/CLI, execution context,
secure output, current inventory, and historical migration responsibility. It
moved the PostgreSQL test to validation ownership and removed the empty
promoted placeholder. Commit `e8a59d9c` added only the package markers needed
for Python 3.12 recursive discovery and corrected three stale assertions that
full discovery exposed: two operation-route expectations and one dated script
count.

## Verification Evidence

| Check | Result |
| --- | --- |
| Production-to-tests RED/GREEN | Initial RED named four production consumers; the 59-case manifest suite now passes with the new zero-dependency invariant |
| Method preservation | CI gate 32/32, supply-chain 66/66, and metadata identity 10/10 methods preserved; manifest 58/59 with only the new invariant added |
| Operation examples | 151 Compose, PostgreSQL, and sample-delivery tests passed; 20 pure moves matched their pre-move SHA-256 values |
| Supply chain | 66 split policy/wrapper/secure-output tests and 50 library discovery tests passed |
| Metadata and lifecycle | 65 metadata library, 7 metadata CLI, and 15 lifecycle validation tests passed |
| Fixture-pattern suite | 51 tests passed; static test fixtures reduced from 34 to 0 with zero production references and zero `spec126` residue |
| Manifest and workflow | Canonical script manifest passed; 59 manifest current/history tests passed; 47 workflow tests passed with 11 intentional Wave-C skips |
| Document graph | All-mode validation reported 689 documents, 5,748 links, and 0 failures |
| Recursive discovery | The original command first returned 0 tests; package markers then collected 1,085 tests. Three current assertion drifts were corrected and focused tests passed; the remaining two failures are the expected stale DATA-0078 output assigned to Task 0006 |
| Whitespace | Both implementation snapshots passed `git diff --check` before commit |

## Review Evidence

Method-set comparison proves that the large-module splits did not silently
drop tests. The script manifest independently proves direct production-owner
evidence, rather than accepting helper indirection as a test relationship.
The final independent repository review remains assigned to Task 0006 and
must recheck full discovery after generated evidence is refreshed.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `b3b6db74` | Start Task 4 from the accepted Task 3 milestone |
| `85b0fc13` | Converge test placement, builders, operation examples, and production fixture ownership |
| `e8a59d9c` | Enable recursive unittest discovery and remove stale route/count assertions it exposed |

This evidence checkpoint does not predict its own commit identity.

## Rulings

- `tests/lib/<domain>/` verifies library behavior; `tests/validation/` verifies
  CLI, entrypoint, and execution context behavior.
- Production modules must not import from or read `tests/**`.
- Replace completed-Spec names, fixed branch tips, and historical counts with
  generic contract data unless the historical value itself is the contract.

## Deferred Items

- Performance benchmarking and runtime service execution are outside this
  Task.
- Immutable historical evidence remains unchanged.
- The current agentic-audit checker still recovers `T-AER-*` completion tags
  from retired Git evidence. Task 0005 must remove that production compatibility
  path with its contract and consumers; Task 4 removed only its static test
  fixture.
- DATA-0078 is stale because Tasks 1 through 4 changed tracked workflow and
  script inputs. Task 0006 owns generator ordering, freshness checks, and the
  final full-discovery rerun.
- Reverting `85b0fc13` restores the former fixture and test ownership; reverting
  `e8a59d9c` restores the prior non-recursive discovery behavior. Partial
  restoration of production reads from `tests/**` is not a valid rollback.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Script and operation ownership Task](tsk-0003-script-and-operation-ownership.md)
