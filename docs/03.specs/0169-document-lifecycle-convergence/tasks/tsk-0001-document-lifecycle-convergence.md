---
title: Document Lifecycle Convergence Task
version: 1.0.0
type: sdlc/task
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0169-TSK-0001
parent_ids: [SPEC-0169, SPEC-0169-PLAN-0001]
created: 2026-09-03
updated: 2026-09-03
---

# Document Lifecycle Convergence Task

## Objective

Execute the five phases of SPEC-0169 and record the evidence for each.

## Inputs

- `docs/99.templates/registry.json` section contracts and identity spaces.
- `scripts/lib/document_governance/metadata/heading.py` enforcement branch.
- The 349 stage documents measured in the survey below.
- REQ-0026, AD-0030, ADR-0030 as the retention owners to update in place.

## Work Log

### Survey baseline (2026-09-03, commit d129870f)

| Profile | Docs | Missing required | Unregistered headings |
| :--- | ---: | ---: | ---: |
| `guide` | 66 | 66 | 66 |
| `policy` | 64 | 64 | 64 |
| `runbook` | 62 | 62 | 62 |
| `spec` | 33 | 0 | 6 |
| `adr` | 27 | 0 | 23 |
| `requirements-package` | 26 | 0 | 23 |
| `architecture-description` | 26 | 0 | 20 |
| **Total** | **349** | **192** | **272** |

Enforcement gap proven by mutation on `docs/03.specs/0002-auth/spec.md`:
adding an unregistered `## Totally Unregistered Heading` passed the contract
check, and renaming the required `## Traceability` to `## Trace` also passed.
Cause: `validate_body_contract` enforces sections only where `template_id` is
`None` or the type is outside the typed target set.

## Verification Evidence

### Closing measurement (2026-09-04, commit 493a4d0e)

| Profile | Docs | Missing required | Unregistered headings |
| :--- | ---: | ---: | ---: |
| `guide` | 66 | 0 | 0 |
| `policy` | 64 | 0 | 0 |
| `runbook` | 62 | 0 | 0 |
| `adr` | 27 | 0 | 0 |
| `architecture-description` | 26 | 0 | 0 |
| `spec` | 22 | 0 | 0 |
| `requirements-package` | 17 | 0 | 0 |
| `operations-domain-readme` | 13 | 0 | 0 |
| `readme` | 8 | 0 | 0 |
| `plan` | 2 | 0 | 0 |
| `task` | 2 | 0 | 0 |
| **Total** | **309** | **0** | **0** |

The measurement tool was rebuilt on `extract_markdown_headings`, the function
the gate itself uses, after a first pass counted shell comments inside fenced
blocks as headings and reported four documents that had no defect.

Gate results at each commit boundary: `run-ci-gate.py --profile full` exits 0
with 17 unittest suites reporting `OK`. `check-document-links.py --mode all`
reports 590 documents and 4846 links with zero failures, up from 4357 links as
the generated `Traceability` sections added their own.
`check-document-metadata.py --mode check-contracts` reports zero violations
under the newly enforced contract.

Final all-files QA on a clean linked worktree:
`scripts/validation/run-agent-precommit-all-files.sh` reports
`hook_result=passed hook_exit=0` with `changed_count=0` and
`unexpected_count=0`. Its first run rewrote 93 documents to remove a double
blank line the section transforms left before each heading, plus two
outstanding `ruff-format` wraps; those are commit `32939f20` and the rerun above
is clean.

One load-dependent test failure was observed twice across five full-gate runs
and is not attributed to this work:
`tests.lib.ops.test_postgres_logical_upgrade_rehearsal.test_timeout_still_cleans`
expects exit code 20 and gets 60 when cleanup misses its budget. The test fixes
a wall-clock budget — `IOR_TEST_TOTAL_TIMEOUT=5` with
`IOR_TEST_CLEANUP_RESERVE=2` — so under full-gate parallel load the owned
cleanup exceeds its two-second reserve and `owned-cleanup-failed` escalates the
exit code. It passes three times out of three in isolation. The working tree
held no change under `tests/` or `scripts/` when it first appeared.

## Review Evidence

Mutation evidence, by claim:

| Claim | Mutation | Result |
| :--- | :--- | :--- |
| The parent chain is now checked | Repoint a guide at `AD-0004` | `invalid-parent-type` |
| The parent chain resolves | Repoint a guide at `POL-9999` | `unresolved-parent` |
| Required sections are enforced | Drop one required section, all 23 profiles | `body-heading-missing` |
| Unregistered sections are rejected | Add `## Totally Unregistered Heading` | `body-heading-forbidden` |
| Repeats are rejected | Duplicate one required section | `body-heading-duplicate` |
| One H1 per document | Append a second H1 | `body-h1-count` |
| The new tests are load-bearing | Restore the `template_id` bypass | 74 subtest failures |
| The transform converges | Re-run the catalog normalizer twice | byte-identical tree |

Two findings are recorded rather than acted on, because each needs a decision
this Task does not carry authority to make:

1. The `changed_boundary` route in `validate_body_contract` — template-role
   headings, `template-instruction-in-target`, `template-body-token-in-target`
   — never executes: both production call sites in
   `scripts/lib/document_governance/metadata/reference.py` pass `False`.
2. `<!-- Target: ... -->` appears in 184 tracked documents and is declared a
   forbidden target residue by `TARGET_TEMPLATE_LITERALS`, yet no current
   template emits it yet `check-document-metadata.py` still writes it into its
   own generated audit README. The evidence points both ways.

Pre-existing and left alone under surgical-change discipline:
`scripts/lib/document_governance/metadata/heading.py` imports `ProfileError`
without using it; `ruff check` reports the same `F401` against the file as it
stood before this work.

## Commit Ledger

| Commit | Phase |
| :--- | :--- |
| `53ed31b7` | Package opened |
| `f7b74987` | Phase 1 — reconcile the declarations with the corpus |
| `10812b7a` | Phase 2 — retire the Stage 01 hardening layer |
| `33b541c5` | Phase 3 — place three homeless domain facts |
| `275011db` | Phase 3 — retire the twelve standing domain packages |
| `bc1980fc` | Phase 4 — populate the declared catalog parent chain |
| `aafb8bd3` | Phase 4 — normalize the catalog to its section contract |
| `7b96bf77` | Phase 4 — remove the duplicate sections that normalizer left |
| `68bda236` | Phase 4 — fold the remaining catalog sections |
| `b3437c26` | Phase 5 — retire the stacked Stage 01/02 vocabulary |
| `493a4d0e` | Phase 5 — enforce the declared section contract |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
