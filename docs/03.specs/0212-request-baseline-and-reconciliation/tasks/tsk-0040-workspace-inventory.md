---
title: "Workspace Inventory Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-01"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0040"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-01"
---

# Workspace Inventory Task

## Overview

Implement P01.01–P01.05 through W56–W60 and criteria 51–55. This Task owns
workspace census, evidence classification, writer leases and owner handoffs.
Service code and P12 final user-function acceptance remain with their leaf owners.

## Inputs and Authorization

The direct user request on 2026-11-01 approves the displayed P01 implementation
plan, bounded local source/document/test/CI changes and local logical commits.
The input workspace is `/home/hyunyoun/data/hy-home.docker`; the initial HEAD is
`ac573aaa1c0db602e16cdb6e68678ea4d6cfb14d`, with a clean tracked worktree.
Read-only remote main comparison now succeeded with the same HEAD; the planning
DNS failure is historical, not the current comparison result. The implementation
branch is `codex/p01-workspace-inventory`. No clone, reset or pull is authorized.

The available local dependencies include the execution contract, official research,
baseline/corrections, requirements crosscheck, ownership and scope coverage.
Historical unavailable originals and private operator state remain unavailable.
The bootstrap/provider, REQ-0027, AD-0031 and this Spec/Plan govern the local unit.

## Work Log

### Initial lifecycle boundary

This new Task starts at `draft` under the Registry's initial-state contract.
The direct user request authorizes the local implementation independently of
this metadata state. Later direct lifecycle edges must be observed against an
issued source revision; no multi-edge shortcut or acceptance is fabricated.

### Work allocation

W56 captures source identity; W57 implements and verifies the inventory; W58
reconciles acceptance scope; W59 binds writer leases and handoffs; W60 records
official applicability. These form one bounded Task execution, with one
frontmatter state. No separate execution-item lifecycle is issued.

### Single writers and source evidence

The qa-engineer owns the CLI/library/tests; the doc-writer owns this package,
DATA-0096 and its Registry allocation; the ci-cd-engineer owns manifest/selector
registration and related tests. Shared-path before-fingerprints are retained in
local analysis receipts. Service Compose, env, Secret catalogs, version pins,
common optimization files and existing acceptance records are not edited by this
unit. Independent reviewers have no authoring lease. Data owners, actual operators
and final accepters are not inferred from role names.

DATA-0096's current consumers were designated before generation: this Task and
P02–P12 exact downstream handoffs. The public payload holds safe file/service
observations, curated dispositions, research and ownership. Private per-path
metadata and sanitized command receipts stay under local analysis. Secret values,
authentication bodies, value hashes and raw operational logs are not collected.

### Research and acceptance scope readback

The doc-writer directly consulted fifteen official pages: Compose profiles,
startup order, include and config; Git status/worktree; Python 3.12 filesystem
APIs; Sigstore/SLSA; Storybook upgrade and release pages; n8n/Ollama/Valkey
release pages; and the exact Valkey advisory. The unversioned Python page
resolved to 3.15, so the 3.12 API manual was consulted for local Python 3.12.3.
No 3.15-only behavior is adopted. Per-product support, license, compatibility and
backup details outside these inventory changes remain research residuals.

Readback of the five existing Task records confirms n8n C19/C22, storage C1–C6
and Storybook C1–C5 acceptance. OpenBao global C20 and Hermes global C23 remain
pending despite the preserved narrower operational receipts. Storybook's current
package declaration is 10.6.3; historical Task prose naming 10.6.1 is not used as
the current pin. n8n's native accepted image 2.43.6 and historical HOME 2.41.6
are distinct. No previous operator result is represented as a new direct run.

The 9.1.3 Valkey release and GHSA-f4q9-j22m-xqq9 identify an incremental P08
research handoff from source 9.1.2. That advisory affects cluster-enabled servers;
non-cluster servers are unaffected by this specific issue. The current source
version alone does not prove that a HOME server is vulnerable. Queue/cache,
RDB/AOF, client and restore compatibility remain with P02/P05/P08.

### Observed verification and correction chronology

Initial doc-writer changed-metadata checks reported 147 findings: the new Plan's
empty dependency syntax, combined Work Unit cells and premature Task initial state
made this package invalid; the resulting alias-resolution short circuit produced
145 secondary archive type mismatches. These were not established baseline debt.
The local authoring errors were corrected without changing an archived body.
The isolated initial HEAD and current full-contract checks both report zero
violations; the final changed-metadata check selects five records with zero
violations. Initial calls were captured in the tool transcript only; the final
sanitized receipts are retained in local analysis.

Independent source/security review found private-path, output-descriptor and YAML
merge/path issues in the new tool. The source writer corrected them with negative
regressions. The initial isolated renderer produced only one PASS among 203 cases;
that is preserved as an unsuccessful earlier attempt. After correction, a bounded
attempt gave 52 PASS, 21 FAIL, one ERROR and 129 NOT_RUN. Resumption checked the
same 69 configuration fingerprints and retained prior successful receipts; the
final 203 attempted cases give 182 PASS and 21 FAIL, zero ERROR/NOT_RUN. The
21 source examples/overlays require exact synthetic inputs or their base context;
their individual rows remain `TEST_RESIDUAL` and are not hidden as renderer PASS.
The root-included base configuration and all 112 explicit root-service cases
pass. The remaining cases are six examples, nine LAB declarations and six
standalone infrastructure/ACL-overlay contexts; local render-residuals.json
retains their exact identities. Static LAB inspection does not authorize LAB runtime.

The source snapshot observed at `2026-11-01T13:03:21.476711Z` lists 40,977 file
entries, with 2,247 public rows and 38,730 excluded local rows. It distinguishes
seven complete body reviews and six partial reviews among 2,240 eligible text
files. These are dated observations; the final refresh may add local evidence
files and must retain its own actual counts. There are 223 source/service rows,
112 root services, 69 Compose sources and 17 entrypoints. Runtime and independent
restore for this execution are each 0/112. Neither service declarations nor
configuration cases prove installed versions, readiness, product registration or
user-function acceptance.

Forty-five focused tests pass, with combined new-code coverage 92% (inventory
92%, service analysis 91%, renderer 93%, CLI 90%). Tests cover normal Git/non-Git
and separate projects, private/symlink refusal, stale/partial review, duplicate and
merged services, interruption, permission/output errors, atomic preservation and
same-source render resumption. The manifest suite passes 51 tests; the manifest
checker and the two P01 selector/mutation tests pass. The broader CI-plan suite is
56 PASS and one ERROR among 57 tests: installed Git appears UID 65534 while its
trust guard requires UID 0. It is not reported as an all-PASS CI result.

The first normal-hook local commit attempt was rejected by one formatter finding
in a CI test and three gitleaks matches on public Compose network labels in the
DATA projection. Independent security review confirmed the labels were actual
public source names, not credentials. The CI test formatting was corrected. The
P01 projection now names that metadata field `network_reference` instead of
`network_key`, preserving the existing port parser and values through a narrow
immutable projection. A regression first reproduced `KeyError`; the corrected
45-test suite is being rerun. The normal hooks will be retried without a bypass;
no commit success is recorded yet.

The registered full local gate remains `BLOCKED`: system Python 3.12.3 differs
from required 3.14.8, and the installed 3.14.8 build lacks `F_ADD_SEALS`. No bypass
or substitute hosted-controller success is claimed. Remote CI is NOT_RUN.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial identity | 51 | W56 | Read-only Git and workspace inspection | Initial HEAD above | PASS | Inputs and Authorization | required | - |
| Boundary verification | 51 | W56 | Git/non-Git, private/symlink and fingerprint regression | Final authored source/test fingerprints | PASS | 45 focused tests; verification-summary.json under local P01 analysis | required | - |
| Inventory verification | 52 | W57 | Unit, integration and CLI boundary/coverage checks | Final authored source/test fingerprints | PASS | 45 tests, 92% combined coverage; verification-summary.json | required | - |
| Scoped render matrix | 52 | W57 | Isolated public-copy Compose config matrix | Same 69 configuration source hashes | PASS | 203 attempted: 182 PASS, 21 FAIL; payload retains per-case TEST_RESIDUAL; no all-config PASS claim | required | - |
| Acceptance reuse | 53 | W58 | Existing Task/criterion scope readback | Current bytes of five canonical Task records | PASS | DATA-0096 acceptance_reuse: bounded accepted scopes and narrower recorded operational cuts | required | - |
| Ownership verification | 54 | W59 | Single-writer and metadata refusal regressions | Current assigned path leases and synthetic conflicting input | PASS | Focused 45 tests; DATA-0096 ownership/handoffs | required | - |
| Official research | 55 | W60 | Direct official-page consultation | Fifteen official URLs and current source declarations | PASS | DATA-0096 research; exact retrieval times and adoption/deferral limits | required | - |
| Document boundary contracts | 51 | W56 | Metadata, links and Registry checks | Current bounded source unit | PASS | Current and isolated baseline full contracts 0; changed metadata 5 selected/0; links 0 failures, 1 historical warning | required | - |
| Document inventory contracts | 52 | W57 | Metadata, links and Registry checks | Current bounded source unit | PASS | Same actual document checks; no archive modification or baseline-debt claim | required | - |
| Document reuse contracts | 53 | W58 | Metadata, links and Registry checks | Current bounded source unit | PASS | Same actual document checks; existing completed Task bytes preserved | required | - |
| Document ownership contracts | 54 | W59 | Metadata, links and Registry checks | Current bounded source unit | PASS | Same actual document checks; Registry diff is DATA allocation only | required | - |
| Document research contracts | 55 | W60 | Metadata, links and Registry checks | Current bounded source unit | PASS | Same actual document checks; external facts remain bounded evidence | required | - |
| Manifest and P01 selection | 52 | W57 | Manifest checker, 51 manifest tests and 2 selector/mutation tests | Current registration | PASS | verification-summary.json; no full CI-plan PASS claimed | required | - |
| Broader CI plan | 52 | W57 | Unfiltered CI-plan suite | System Git UID/trust environment | ERROR | 57 cases: 56 PASS, 1 ERROR; exact Git environment needs correction | required | - |
| Full local boundary gate | 51 | W56 | Registered full local gate | Required Python 3.14.8 with memfd sealing support unavailable | NOT_RUN | BLOCKED; system 3.12.3 mismatch, installed 3.14.8 lacks F_ADD_SEALS | required | - |
| Full local inventory gate | 52 | W57 | Registered full local gate | Same exact interpreter requirement | NOT_RUN | Same scoped environment block; no bypass | required | - |
| Full local reuse gate | 53 | W58 | Registered full local gate | Same exact interpreter requirement | NOT_RUN | Same scoped environment block; no bypass | required | - |
| Full local ownership gate | 54 | W59 | Registered full local gate | Same exact interpreter requirement | NOT_RUN | Same scoped environment block; no bypass | required | - |
| Full local research gate | 55 | W60 | Registered full local gate | Same exact interpreter requirement | NOT_RUN | Same scoped environment block; no bypass | required | - |
| Hosted CI | 51 | W56 | Remote CI execution | Local branch | NOT_RUN | No remote publication; applies to all P01 units | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 51 | pending | Initial identity, Boundary verification, Document boundary contracts | SOURCE_READY; required exact local gate remains blocked | SPEC-0212 TSK-0040 |
| 52 | pending | Inventory verification, Scoped render matrix, Document inventory contracts, Manifest and P01 selection | SOURCE_READY; 21 configuration cases are TEST_RESIDUAL; broader CI error and full gate remain unresolved | SPEC-0212 TSK-0040 |
| 53 | pending | Acceptance reuse, Document reuse contracts | SOURCE_READY; preserved acceptance does not close the required local gate or operational residuals | SPEC-0212 TSK-0040 |
| 54 | pending | Ownership verification, Document ownership contracts | SOURCE_READY; source leases are assigned, operator identities remain explicit unknowns and required gate is blocked | SPEC-0212 TSK-0040 |
| 55 | pending | Official research, Document research contracts | SOURCE_READY for inventory changes; product-specific research residuals and required gate remain explicit | SPEC-0212 TSK-0040 |

## Review and Completion

The bounded source, tests, CI registration and reusable ledger are implemented.
Seven authored source/test fingerprints match the independent APPROVED code review.
The security recheck found no remaining material issue in its final scoped input
before the subsequent service-merge serialization fix; do not enlarge that review
receipt to a later unreviewed change. The coordinator verified all seven final
code-review fingerprints; a later source edit invalidates its affected receipt.
The normal-hook local commit remains pending and will be reported from its actual
result.

The final `graphify update .` completed with exit 0 and 27,503 nodes. Missing SQL
and HCL grammars remain an explicit AST coverage limit; this is not full semantic
source or document validation.

Task metadata remains at its required initial `draft` state; that does not classify
implemented source as absent. All five criteria remain pending because required
broader CI/local-gate checks are unresolved. No artificial state-only commits or
remote action is introduced. Final local delivery uses the ordinary hooks; if the
exact environment prevents that, retain the concrete patch and mark delivery blocked.

Source, static, isolated, historical operator, this execution's direct operation,
credential rotation, independent restore, remote CI and final acceptance remain
separate. Current direct operation, rotation and independent restore are NOT_RUN.
Historical OpenBao P01 is SPEC-0204; this Task's P01 is workspace inventory.

## Handoff

| Target | Disposition | Current writer/owner | Resume condition and recovery |
| --- | --- | --- | --- |
| P01 full local gate | BLOCKED | Coordinator/QA | Provide the exact Python 3.14.8 build and memfd sealing capability; rerun registered gate without weakening it |
| Broader CI-plan error | BLOCKED | CI owner | Restore the required trusted Git execution environment; rerun the unfiltered 57-case suite |
| 21 failed configuration cases | TEST_RESIDUAL | Exact leaf writer remains unassigned until path lease; P02–P12 routes in payload | Use each payload case's source fingerprints and supply explicit synthetic inputs/base context; rerun only affected cases |
| Current operation, rotation and full independent restore | TEST_RESIDUAL | Actual data owner/operator not inferred | Name consumer, target, approved operator/window, backup and recovery boundary; no P01 runtime mutation |
| P08 image/package candidates | IMPROVEMENT_CANDIDATE | Future exact image/package writer | Preserve accepted functions; verify installed/image/peer/lock/queue/cache/restore applicability before any update |
| Spec Package README | NO_CHANGE | doc-writer | No registered package README profile; existing Spec/Plan links and DATA index supply navigation |
| Learning apps, new external projects and LAB runtime | OUT_OF_SCOPE | Respective external/leaf owner | Handoff contract only; Wiki stays preparation only |

DATA-0096 contains exact source paths/fingerprints for downstream P02–P12 handoffs,
including per-product support/license/compatibility/backup research residuals.
Preserve user changes and initial fingerprints. Revert only this local logical
source unit; no data, credential or service recovery is claimed from a Git revert.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace census and applicability](../../../90.references/data/0096-workspace-inventory/README.md)
