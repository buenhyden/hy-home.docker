---
title: "Capacity Search and Backup Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0270-TSK-0001"
parent_ids:
- "SPEC-0270-PLAN-0001"
created: "2026-11-10"
---

# Capacity Search and Backup Task

## Overview

### Objective

Implement W1-W6 without operating the real shared-memory store or backups.

## Inputs and Authorization

On 2026-11-10 the user explicitly requested implementation of the complete
plan presented in this chat. That request authorizes the bounded local
source, synthetic tests, documentation and registration changes in this
Spec/Plan. It does not authorize the excluded live/private/remote actions.
Initial observed source: clean main `648a78a261cdd058f6c5ed94f560aca73fba145b`.

Exact writer leases:

- Memory writer: `scripts/operations/agent_memory.py`,
  `scripts/lib/ops/memory_capacity.py`, `scripts/lib/ops/memory_search.py`,
  `scripts/lib/ops/memory_cli.py`, `scripts/lib/ops/memory_local.py`,
  and their direct tests under `tests/lib/ops/` and `tests/validation/`,
  including `tests/validation/test_agent_memory_capacity.py`.
- Backup writer: `scripts/lib/ops/memory_backup.py`, existing shell callers
  `infra/09-platform-ops/restic/backup.sh`, `offsite.sh` and
  `bin/hyhome-backup.sh` in that directory, its README, and direct backup tests,
  including the scoped existing offsite and Compose backup contract cases.
- Documentation writer: this package and existing Stage 05 memory/backup
  guidance. Parent integration writer owns `scripts/manifest.yaml`,
  `.github/workflow-contract.yml` and current `.agents/` policy changes.
- Independent code/security and governance reviewers are read-only.

No worker stages, commits or reverts another writer's changes. Unknown provider
request/token/cost ceilings stay UNKNOWN; no paid model API is introduced.

## Work Log

### Owner-approved local execution

The trusted user approved the Spec/Plan behaviour and requested implementation
on 2026-11-10. The lifecycle table records that approval, not an independently
authenticated permission or operational acceptance.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0270 | draft | approved | #owner-approved-local-execution |
| SPEC-0270-PLAN-0001 | draft | approved | #owner-approved-local-execution |
| SPEC-0270-TSK-0001 | draft | ready | #owner-approved-local-execution |
| SPEC-0270-TSK-0001 | ready | in-progress | #owner-approved-local-execution |

### Verification boundary

No operational memory inventory, native provider, backup or recovery has run.

### Implementation and witnessed regressions

The memory writer witnessed failing capacity/search expectations before their
implementation. The backup writer witnessed three producer contract failures
and the absent helper before its first GREEN. Integration routing witnessed
nine missing narrow routes, then two additional local-copy routes, before
the corresponding registrations passed.

Independent code and security review required changes before approval. The
corrected regressions cover reconciliation/settlement races, exact snapshot
identity rather than tree equivalence, actual producer inventory, legacy
read-only retrieval, sanitized failures, and restore-input accounting. Further
cases bind exact local temporary files and producer locks, retain uncertain
Docker dispatch until a successful exact-container/full-request receipt,
preserve unobserved repository allocations, reconcile confirmed retention,
and refuse every SQLite/control-file output alias. A structurally valid but
wrong ledger schema first produced five uncaught IndexErrors in two tests;
the final narrow correction produces sanitized CapacityError results and
preserves the original bytes.

### Final local validation and tools

At main `c463e4ae5807b68fa63d9ff1859ab22cb5b85428` plus the task-owned
working-tree diff, the parent ran coverage 7.17.2 with CPython 3.12.3 and
PyYAML 6.0.3 in an isolated `/tmp` test environment. The first combined run
had one import ERROR because that environment lacked markdown-it. Enabling
the existing host test packages corrected that environment; no production
dependency or global configuration changed. The same selected suite then
ran 138 tests in 8.933 seconds: 135 PASS and three opt-in Docker rehearsals
SKIPPED/NOT_RUN. No Docker command was run by this validation.

The selected modules were the existing memory suite; capacity, search, local
copy and backup library suites; memory CLI and backup contract suites; existing
offsite and Compose BackupContractTests; focused workflow routing; and surface
ownership. Their exact invocation was `coverage run --branch` with source
modules `scripts.operations.agent_memory` and
`scripts.lib.ops.memory_capacity`, `memory_cli`, `memory_local`,
`memory_search` and `memory_backup`, followed by `python -m unittest` for those
modules/classes. Statement coverage is 1102/1202 (91.68 percent), branch
coverage is 324/398 (81.41 percent), and combined coverage is 89.125 percent.
Each production module's combined result is at least 84 percent.

The code reviewer approved the final working-tree source. The security
reviewer independently ran 108 tests and approved the production snapshot,
then re-reviewed the last IndexError guard and ran 15 affected tests to bind
the final capacity hash. The governance reviewer approved the policy,
ownership, immutable-body and documentation boundaries. No reviewer edited
the implementation or authenticated an operational acceptance.

Final SHA-256 bindings:

| Source | SHA-256 |
| --- | --- |
| agent_memory.py | fac399eed0a1caaee935382ef67aff36e12b40452c3b3c340643a8c141d3c748 |
| memory_capacity.py | 5ef3fa6313221f3603d224cd3953731430fcac0432e2e09b3dd8cabd577a915c |
| memory_cli.py | a7ff4fcc4bdcce16b614e282bd1a472b1ec677436b6a620e63646602660c2b88 |
| memory_local.py | d9dedf23e45a78edd423234729485bca1ea9f0cead08b66f3b2cb027211cd733 |
| memory_search.py | 80dd2bcf3977b9f35272b615570a9d82a28d9a8c25c43b842114cf775a39aa02 |
| memory_backup.py | 1277ad240023b211185eb4f3ff0efbd54f9c8e5cdf6045759ff2fe5f47604575 |

`graphify update .` completed without a model API: 26334 nodes and 54294 edges.
Nineteen SQL and nine HCL files lacked their optional parsers and five inputs
yielded no symbols; this is bounded AST freshness, not semantic or runtime
coverage. Graph output remains ignored. No semantic-labeling command ran.

Script Manifest, GitHub workflow contract, agent governance contract and
provider renderer parity checks passed. The workflow contract still has five
workflows, seven jobs and nine pinned actions; provider drift is zero. New
files were registered with Git intent-to-add after independent source review.
At that initial validation checkpoint this execution had made no source commit,
push, pull request, merge or runtime action.

The final changed-document check selected 13 documents with zero violations
and zero transition overrides. Corpus lifecycle and active occupancy each had
zero violations; alignment checked 912 documents and 8269 links with zero
failures or warnings. A redacted Gitleaks scan consumed the full unfiltered
541168-byte source diff and found no leaks. Result-only evidence below adds
no link target or authority change. Commit hooks/local-staged and hosted CI
had not run at that checkpoint. A subsequent Stop event requested verified
logical commits; these use normal installed hooks without skipping checks.
No remote delivery or runtime execution is authorized by that checkpoint.
Supply-chain gate failures and owner acceptance remain explicitly outstanding.
The last parent-inclusive result-only metadata check selected six documents
with zero violations and zero overrides. Scoped markdownlint first found one
extra blank line in the Runbook; removing that line produced six clean files.
The result-only record changes no status, link target, script or contract.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Capacity implementation verification | 1 | W1 | focused-capacity-tests | Approved local source | NOT_RUN | Awaiting memory writer receipt | required | - |
| Final capacity regressions | 1 | W1 | focused-capacity-tests | Final capacity hash in Work Log | PASS | Coupled 110 tests; final parent selected suite 135 PASS, three native NOT_RUN; concurrency, corruption and retention regressions included | required | Capacity implementation verification |
| Writer compatibility verification | 2 | W2 | focused-writer-tests | Approved local source | NOT_RUN | Awaiting memory writer receipt | required | - |
| Final writer regressions | 2 | W2 | focused-writer-tests | Final memory and local-copy hashes in Work Log | PASS | Legacy schema, preserved bytes, protected paths, copy interruption and source allocation cases in the passing selected suite | required | Writer compatibility verification |
| Search verification | 3 | W3 | focused-search-tests | Approved local source | NOT_RUN | Awaiting memory writer receipt | required | - |
| Final search regressions | 3 | W3 | focused-search-tests | Final search and CLI hashes in Work Log | PASS | Deterministic lexical, Unicode, source eligibility, bounds and no-write cases; search combined coverage95 percent | required | Search verification |
| Backup integration verification | 4 | W4 | focused-backup-tests | Approved local source | NOT_RUN | Awaiting backup writer receipt | required | - |
| Final backup regressions | 4 | W4 | focused-backup-tests | Final backup hash in Work Log and unchanged network declarations | PASS | Exact terminal/request proof, capacity/CAS, producer routing, failure metrics and 14 existing backup contracts; three native rehearsals NOT_RUN | required | Backup integration verification |
| Documentation verification | 6 | W5 | documentation-checks | Approved local source | NOT_RUN | Awaiting documentation and policy receipt | required | - |
| Current document checks | 6 | W5 | documentation-checks | Scoped Spec/Plan/Task and current Runbook after c463e4ae5 reconciliation | PASS | Metadata selected12 violations0; lifecycle/occupancy0; alignment908 documents/8253 links failures0, warnings0 | required | Documentation verification |
| Final document checks | 6 | W5 | documentation-checks | Final source documents before this result-only entry | PASS | Metadata selected13 violations0; lifecycle/occupancy0; alignment912 documents/8269 links failures0, warnings0 | required | - |
| Independent source verification | 5 | W6 | independent-review-and-registration | Final source diff | NOT_RUN | Awaiting integration and review | required | - |
| Final source and registration review | 5 | W6 | independent-review-and-registration | Final hashes in Work Log and registered script/test routes | PASS | Code and exact-hash security APPROVED; manifest, workflow contract, governance, renderer parity and ownership checks PASS | required | Independent source verification |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | Final capacity regressions | Source verified; owner acceptance pending | SPEC-0270 TSK-0001 |
| 2 | pending | Final writer regressions | Source verified; owner acceptance pending | SPEC-0270 TSK-0001 |
| 3 | pending | Final search regressions | Source verified; owner acceptance pending | SPEC-0270 TSK-0001 |
| 4 | pending | Final backup regressions | Source verified; operational adoption remains NOT_RUN | SPEC-0270 TSK-0001 |
| 5 | pending | Final source and registration review | Source review approved; owner acceptance and hosted CI remain separate | SPEC-0270 TSK-0001 |
| 6 | pending | Final document checks | Current guidance verified; owner acceptance pending | SPEC-0270 TSK-0001 |

## Review and Completion

Local implementation and independent source review are complete. This Task
remains in progress pending the owner's criterion acceptance. Real inventory
adoption, native provider behavior, Docker/Restic/R2 operation, backup/restore
and hosted CI remain NOT_RUN and are not inferred from isolated checks.
Local logical commits are source checkpoints, not criterion acceptance.
Required supply-chain evidence and the other owners' acceptance remain
separate outstanding work.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
