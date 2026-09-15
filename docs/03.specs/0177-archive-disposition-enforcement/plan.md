---
title: "Archive Disposition Enforcement Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0177-PLAN-0001"
parent_ids:
- "SPEC-0177"
created: "2026-09-15"
---

# Archive Disposition Enforcement Implementation Plan

## Objective

Move the registered checks onto the Stage 98 model the policy already states,
without rewriting a sealed record and without an integration in which the policy
and a check disagree without a named transition.

## Dependencies

- The policy section, the Stage 98 README, `REQ-0026`, `AD-0030`, and
  `ADR-0035` land in the change that opens this package.
- The Spec's three Open Questions are answered before W2 starts.
- Each document admits one lifecycle transition per integration, so the package
  walks `draft` to `completed` across several integrations.

## Execution Sequence

1. W1: Open the package, allocate `ADR-0035` and `SPEC-0177`, apply the policy
   text with its transition paragraph, and record the measured link graph.
2. W2: Answer the Open Questions and amend the Spec.
3. W3: Move the link boundary to admit `resolved/` and route every other class
   through the index, with tests.
4. W4: Define and register the Retention Envelope and its check.
5. W5: Drop the ledger fields and the Tombstone pairing for records created after
   acceptance, keeping every sealed record valid.
6. W6: Register the `resolved/` profile and admit it in the Stage 98 loader and
   the link graph, with a fixture test.
7. W7: Accept `ADR-0035`, resolve its relation to `ADR-0033`, and remove the
   transition paragraph and its restatements.
8. W8: Run the changed profile, obtain an independent review, and complete and
   preserve the package.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| A sealed record fails after the contract change | W5 runs the corpus check over every existing Tombstone and Migration before the commit | Revert W5; the policy transition paragraph still describes the enforced subset |
| The pairing is released with no withdrawal owner | W4 precedes W5 | Revert W5 |
| Acceptance lands while a check still lags | W7 removes the transition paragraph only after W3 to W6 are integrated | Leave `ADR-0035` at `proposed` |

## Verification

The Task records every command, exit code, review finding, and PASS, FAIL,
BLOCKED, NOT_RUN, or N/A state. Completion requires every acceptance criterion
in the Spec to have a receipt row per criterion and work-unit pair.

## Rulings

- No sealed Tombstone, Migration, or frozen body is edited.
- A guard that fires is treated as correct until proven otherwise.
- No `resolved/` directory is created without a closed Incident to hold.
