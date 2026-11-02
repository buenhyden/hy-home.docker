---
title: "Service Connection Contracts Task"
version: "0.1.15"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-02"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0041"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Service Connection Contracts Task

## Overview

### Objective

Implement P02.01–P02.05 as a bounded local source and isolated-test unit. This
Task owns the current connection-contract routing and evidence. It is distinct
from the completed historical P02 secret catalog in SPEC-0204. It does not
grant operating, host, credential, external-repository or remote-CI authority.

## Inputs and Authorization

The direct user request of 2026-11-02 authorizes the approved P02 plan,
including local source, documentation, test and logical-commit work. The source
starts at `b79cbb9f3f49af8cd0e654c2ca1c4b9ea7632af0`. The issuing observation
was on `codex/p01-workspace-inventory`; implementation is on the separately
observed clean branch `codex/p02-integration-network-auth-valkey`. The current
P01 inventory and DATA-0096 are bounded inputs;
they do not replace canonical Compose, Secret, port or version ownership.

At `2026-11-01T22:20:38Z`, the read-only query
`git ls-remote --exit-code origin refs/heads/main` first failed in the default
sandbox with DNS exit 128. The same query then succeeded through the approved
scoped execution path and returned
`ac573aaa1c0db602e16cdb6e68678ea4d6cfb14d`. No fetch, pull, reset, push or
remote mutation was performed. The remote result is a comparison receipt; P02
implements from the separately recorded local baseline.

Shared MNG Valkey remains the selected default. Existing named n8n ACL and
dedicated broker configurations are opt-in contracts, not a topology change.
The approved Grafana exception is only GET/HEAD on `/favicon.ico` and
`/robots.txt`; unsafe methods must end at `noop@internal` with `418` before the
normal Grafana route. Existing Grafana RBAC and the documented rate limit of
100 requests/second with burst 200 remain unchanged. Its policy owner is
`@buenhyden`; reconsider by 2026-12-02 or immediately after route widening,
authentication changes or a relevant advisory.

## Work Log

### Issued writer leases

This Task is issued before implementation changes. Each writer must compare the
current fingerprint recorded in the P02 local curation receipt before editing;
a changed shared input pauses only its dependent slice.

The registered metadata gate identified a narrow shared-package correction in
the current draft `TSK-0040`: before SHA-256
`a946e47cac814437da5418f941333e76a5bc321548d11d2797d79c07013b7073`.
`p02_docs_impl` changes only the five `FAIL` evidence rows at lines 315–319 and
the five later `PASS` selected-check rows at lines 320–324 so each `Resolves`
value is `-`. A failing row cannot resolve a gate, and a selected-check PASS
cannot resolve a distinct full-gate FAIL. Inputs, locations, results, failure
history and Check labels remain unchanged. This is a metadata correction, not a
P01 acceptance change or validator/baseline waiver.

| Scope | Writer | Review role | Boundary |
| --- | --- | --- | --- |
| All `infra/` source and its exact service READMEs | `p02_infra_impl` | independent code/IaC review | Single integration writer for Compose, gateway, readiness and Valkey source |
| `scripts/operations/workspace-inventory.py`, its library and source tests | `p02_connections_impl` | independent code/security review | Adds public connection evidence only; no private-value read or hash |
| Native, synthetic and contract-test source | `p02_contract_tests` | independent QA/security review | Exercises declared contracts without operating a HOME service |
| This package, DATA-0096 README and local P02 curation/review receipts | `p02_docs_impl` | independent document review | Records evidence and handoffs; DATA-0096 generation remains coordinator-owned |
| CI manifest, selectors, their tests and `scripts/hardening/check-all-hardening.sh` shared-URL assertion | `p02_ci_impl` | independent CI review | Registers only existing verified checks and keeps the OAuth2 Proxy MNG Valkey assertion aligned with the transport contract |

Acceptance owner, data owner and operating accepter are not inferred from these
writer labels. P03 owns model/product registration, P04/P05 own Airflow/n8n
consumer behavior, P06 owns secret issuance and custody, P07 owns observations,
and P08 owns the Valkey update/advisory decision. A service source change stays
under the infra lease even when those owners receive a handoff.

### Contract decisions and residual boundaries

P02 reconciles four port locations separately: process listener, service DNS,
host publication and gateway backend. It rejects using host publications from a
container or adding a public port to repair a private caller. `DEV` and `MNG`
variables must remain separately evidenced. Process liveness, initialization,
dependency readiness and functional/product readiness remain separate results.

No source inspection, route test or connection census proves a stored product
credential, model registration, successful external delivery, a current
operator run, credential rotation, recovery or remote CI result. Those items
remain explicitly routed to their owning task.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Issued baseline and leases | 56 | W61 | Read-only branch, source and ownership readback | Initial HEAD and public P01 ledger | PASS | Inputs and Authorization; Issued writer leases | required | - |
| Port contract regression | 56 | W61 | Focused isolated source/configuration suites | Public changed Compose inputs, listed in local P02 hash packet | PASS | `p02_infra_impl`: contract suite 24/24; port/renderer suite 20/20; root and monitor-overlay rendering selected 57 Traefik/55 Nginx services | required | - |
| Authentication boundary regression | 57 | W62 | Controlled loopback OAuth2 Proxy ID-token verifier and isolated Traefik method check (bounded scope) | Official v7.15.5 asset, checksum and synthetic signed tokens | PASS | `_workspace/repo-support/analysis/p02/oauth2-proxy-oidc-native-20261102.txt`, 2026-11-02T07:23:00+09:00, 2 methods pass; isolated Traefik method check, 1 method passes; stored Keycloak client and API access-token acceptance excluded | required | - |
| Full SSO exact-class rehearsal | 57 | W62 | Browser 302, JSON 401 and group-denial 403 full-stack class | Matching Keycloak test image | NOT_RUN | `_workspace/repo-support/analysis/p02/sso-rehearsal-residual-20261102.txt`: first-start provider build exceeded 300 seconds; cleanup passed. Resume with a pre-built matching Keycloak test image or bounded `kc.sh` build preparation | required | - |
| Environment and readiness regression | 58 | W63 | Focused isolated source/configuration suites (source/isolated scope) | Public changed Compose inputs | PASS | `p02_infra_impl`: contract suite 24/24 and port/renderer suite 20/20; Open Notebook `/health` remains limited liveness/startup evidence | required | - |
| Valkey contract regression | 59 | W64 | Synthetic ACL, secret-delivery and topology source checks (source/isolated scope) | Synthetic values only | PASS | `p02_infra_impl`: contract suite 24/24; hardening suite reports ALL PASS | required | - |
| Native secret-presentation contract | 59 | W64 | Synthetic Compose secret ownership and permission modes | Cached image and synthetic secret only | PASS | `_workspace/repo-support/analysis/p02/compose-secret-native-20261102.txt`, 2026-11-01T22:56:55.947414+00:00; `test_p02_secret_presentation_native.py` SHA-256 `97faf10b437f6ba89ed7c1141a455f7d77574d74096ebe01478440cf8b678e1e`; 1 test, 4 modes, 74.684s | required | - |
| Connection ledger and handoff validation | 60 | W65 | Public extractor and handoff curation (bounded public-source scope) | 67 public sources, 22 connection rows, 1 explicit unknown gap; 10 extracted sources and 1 unhandled source | PASS | Frozen helper `dfefebaa…`, test `261067…`; 50 tests pass with main branch 86%, helper 85% and combined 87%; Superset has four rows, including source-declared Trino with actual registration `UNKNOWN`; generated DATA-0096 records 22 rows and validates | required | - |
| Current direct operation C56 | 56 | W61 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C57 | 57 | W62 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C58 | 58 | W63 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C59 | 59 | W64 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C60 | 60 | W65 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Credential rotation and independent restore | 59 | W64 | Actual credential and state recovery | No approved secret/data owner or recovery window | NOT_RUN | P06 and actual data owner handoff | optional | - |
| Hosted CI C56 | 56 | W61 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C57 | 57 | W62 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C58 | 58 | W63 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C59 | 59 | W64 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C60 | 60 | W65 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 56 | pending | Port contract regression | SOURCE_READY: corrected source passes selected contract/render suites; direct operation, restore and remote CI remain separate | SPEC-0212 TSK-0041 |
| 57 | pending | Authentication boundary regression, Full SSO exact-class rehearsal | SOURCE_READY: current OAuth2 Proxy verifier rejects wrong issuer, audience and expiry without a session cookie, and an isolated Traefik method check passes. This is not a Keycloak stored-client, API access-token, browser 302/JSON 401 or group-denial 403 full-stack result | SPEC-0212 TSK-0041 |
| 58 | pending | Environment and readiness regression | SOURCE_READY: corrected source passes isolated checks; liveness, dependency initialization and product readiness remain separate | SPEC-0212 TSK-0041 |
| 59 | pending | Valkey contract regression | SOURCE_READY: selected shared-MNG/default and opt-in topology source checks pass; credential issue, rotation, queue drain and restore remain unexecuted | SPEC-0212 TSK-0041 |
| 60 | pending | Connection ledger and handoff validation | SOURCE_READY: 67-source census yields 22 connection rows, one explicit unknown gap, 10 extracted sources and one unhandled source; generated DATA-0096 is validated, while broader metadata/QA and final acceptance remain separate | SPEC-0212 TSK-0041 |

## Review and Completion

Independent code, security, IaC and document review must cover the exact changed
fingerprints. Required local tests, metadata, link and changed-file checks must
be recorded here with their actual result. Run `graphify update .` after source
integration. Preserve separate observations for source, static, isolated,
historical operation, current operation, rotation, restore, remote CI and final
acceptance. A logical local commit may follow these checks; push, PR, merge,
release and deployment remain unapproved.

### Bounded review records

The current curation contains 56 `complete: false` partial review records: two
retained P01 records, 29 IaC records, six code records, 13 README records,
five CI records and one generated-operations-catalog record. They record changed-section review only and do not grant a
full-file review result. The CI changed-section review was performed by
`root_ci_review` at `2026-11-01T22:59:14Z` for P02 workflow-contract,
manifest, `test_ci_gate_plan` and hardening source assertions; it reported no
Important or Critical finding. Final metadata, link, registry and selected-leaf
gate results are recorded only after their frozen execution receipts exist.

The authoritative broad Compose baseline regression aggregate timed out at its
ten-minute budget (exit 124) without a captured module result, so unrelated
modules remain unproven. It is not a P02 feature failure and is not promoted
from the P02-owned selected slice: 58/58 pass in 38.607 seconds (service
contracts 24, Prometheus 3, gateway 3, service wiring 20, datastore scrape
labels 5 and route-auth contracts 3).

The restricted repository-integrity run reported 767 tests with 9 failures and
77 errors. Its scoped-permission rerun completed 767 tests in 305.595 seconds
with 763 pass, 4 fail and no errors. P02 native reachability is fixed/passing,
the original three secret-metadata failures were caused by P02's overbroad
dedicated-broker mount, not missing P06 grants. The observed failures remain
historical evidence; after narrowing to the two required read-only files,
`PublicSecretSchemaTests` passed 21/21 in 55.806 seconds. P06 custody,
issuance and rotation remain `NOT_RUN`. P08 must refresh the nested SEC01 n8n
source-binding from `8792a345…` to the current
`afe7eabe63e19a889ec608fb76900ff908b0da32faf261f99099fb0e5b6009f7`
through its owned provenance transaction; its exact test is
`tests/validation/test_workflow_version_bundle.py` SHA-256
`c649be9f22b6dd3e3a4bc94d4ab1f6c6da9e26e8ccea87294d1da57f3e1b91c2`.
These are failures, not `NOT_RUN`, and no actual secret, provenance ledger or
operating service was changed here.

### Lifecycle comparator closure lease

The registered gate exposed a semantic conflict: the schema requires a
non-PASS evidence row to use `Resolves: -`, while the lifecycle comparator was
preserving that later relation cell as part of a failed observation identity.
The approved CI lease is a semantic projection, not a path-specific waiver.
For generation 7 it preserves `row[:8]`; for legacy generation 6 it preserves
`row[:7]`. Thus Criteria, Work Unit, Check, Input, Result, Location and known
Required data remain immutable while only the later-PASS relationship cell is
excluded. The five full-gate FAIL observations remain unresolved and criteria
51–55 stay pending; selected PASS rows have a different Check and do not
resolve or promote those full-gate failures.

`p02_ci_impl` owns the narrow comparator and regression source:
`scripts/lib/document_governance/spec_packages.py` SHA-256
`9f6dd115886c397043052904edbf525ff89d7ade7e110ac37db2c7274dee7a03`
and its generation-7 regression
`tests/lib/document_governance/test_generation7.py` SHA-256
`c0e9ab3a415f5eb8c587c74343d8fbf0f12ad3527d4f11657b0fbe4df237b420`.
The packet against baseline `b79cbb9f3f49af8cd0e654c2ca1c4b9ea7632af0`
is SHA-256 `12c5c0874436b43356a5b9af1e3ac4c4750cc3b1138c0c5ff4a4d5e80655c440`.
Rollback restores the comparator and its regression source together, then
leaves the gate blocked rather than rewriting a historical observation.

At `2026-11-02T08:29:15+09:00`, independent code review recorded 11/11
focused tests passing in 11.768 seconds with no findings; narrow security and
rules reviews also passed. CI focused tests passed. Earlier the changed-profile
run passed 6 leaves, then leaf 7 failed with exactly five failed-observation
differences. The registered routes subsequently ran; they do not form an
uninterrupted aggregate PASS. The metadata fixture leaf passed 152/152. The
original library leaf remains an observed 787-case split of 784 PASS, one FAIL
and two ERROR; the approved taxonomy target reran 1/1 PASS and the
permission-caused identity-history methods reran 2/2 PASS. Those component
receipts do not erase the original leaf failure.

Earlier CI/reachability checks passed workflow contract 45, runner/plan 86 and
GitHub workflow contract 44 at the dated fingerprints `3dfe252…`, `d1bdaa7…`
and `f7894c9…`. After mount-module registration, the current workflow,
plan-test and workflow-contract-test SHA-256 fingerprints are
`46c15badd836003aff16c6da43eb810a030225c9ec2011eb89952e05ccb6ae87`,
`4798f34350767ab35bffae92f5357c4db5f952dd55199b01f6ae7c30f24296d4` and
`6e2c504c7d746aa2a38b1e5d584eb27e0415fb465d6ca96f8f2507d7013eba2a`.
Current CI impact reruns passed gate contract 24/24, plan 60/60, GitHub workflow
44/44 and the executable checker. The mount regression SHA-256 is
`13096d677d46913f8a11795bd14e99f6e759ea4da90ff6b834aa7db5b0e623b8`; its
three new service subtests were RED before the fix and the final QA run was
GREEN at 13 PASS in 28.577 seconds, with full SecretSchema 21 PASS in 55.806
seconds and the P02 static slice 59/59 PASS in 38.091 seconds. `root_ci_review`
at `2026-11-02T00:54:54Z` reviewed the earlier scope. The current selector and
mount/wiring hashes were independently re-reviewed by `p02_code_review` at
`2026-11-02T01:12:52Z` with no findings; this is a partial review, not
full-file credit.

The dated pre-final-mount DATA-0096 scan/validate passed with files
41106/41106, partial reviews 53/2253, body 0/2253, render 0/17 and
runtime/restore 0/112. Its comparison saw 10 changed inputs and no
head/add/remove/connection delta. The final scan/validate then passed with
files 41169/41169, partial reviews 55/2254, body 0/2254, render 0/17 and
runtime/restore 0/112. The 56 ledger records and 54 coverage numerator differ
because self/excluded records do not enter that numerator. These census facts
do not change pending criterion acceptance or any operating, rotation, restore,
remote-CI or final-acceptance status.

The isolated official `pip-audit` 2.10.1 run against the unchanged,
hash-locked `scripts/requirements-controller.lock` is an actual `FAIL` (exit
1), not a P02 package change: two packages have 25 known vulnerabilities.
`filelock` 4.2.0 accounts for 17 findings (fix 4.2.1) and `virtualenv`
21.14.8 accounts for eight: seven reports specify 21.14.9, while
`CVE-2026-113713` specifies 21.14.10. A compatibility-reviewed 21.14.10 is
the minimum candidate covering all reported `virtualenv` IDs. The sanitized receipt
`_workspace/repo-support/analysis/p02/pip-audit-controller-lock-20261102.json`
has SHA-256 `740c466637b62722d779ba143be8503465f67c139c5890b6ebf5e18e8104c717`;
the lock remains byte-identical to baseline at SHA-256
`d05a5fb50e29e3d44587b34abacf2713eaea83c7c88ff84127d9cbfe96a193e2`.
P08 owns the canonical dependency input manifest(s), generated lock and
affected controller-gate transaction. The report states 4 High, 12 Medium and
9 Low findings, with no Critical; P02-specific exploitability and reachability
are not established. The baseline-equal lock establishes no P02-induced
dependency delta. Recovery reverts only the owned input-plus-lock delta,
appends corrective evidence, preserves the original FAIL receipt/history, and
reruns the exact hash audit and controller gates. `npm audit` is separately
`NOT_RUN` because P02 changed no npm dependency tree.

### Catalog synchronization and supply-chain residual

The generated inventory projection in
`docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`
was refreshed only between `current-service-inventory` markers using
`operations_catalog.render_service_inventory(ROOT)`. The prior SHA-256 was
`aa35b5b93c1719d1b3d82eaf18d200ede1b41ac804e99c0a22840c6875833b19` and
the refreshed SHA-256 is
`2e92d2bb86a2515591a29fe4c31ef28192933cb40fa3dcee13f95329ab53a6c7`.
The 25 added/25 removed lines are generated projection fields; authored
narrative remains outside the markers. `check-operations-catalog.py` passed.
The earlier 36-cell review at `2026-11-02T00:34:54Z` is retained as history.
At `2026-11-02T01:08:26Z`, `root_document_review` re-reviewed refreshed
SHA-256 `2e92d2bb86a2515591a29fe4c31ef28192933cb40fa3dcee13f95329ab53a6c7`:
exactly three generated mount-projection cells changed (Airflow, n8n and
OAuth2 Proxy), from the prior catalog SHA
`125c4cbd90f6ee72a9d11859519c361832788b0eb8a6d68d4b822de7e79bf281`.
It is `complete: false`, limited to P02 changed generated catalog cells, and
found no blocker or runtime, restore or acceptance promotion.

The registered supply-chain fixture leaf is an actual residual `FAIL`, not a
P02 feature failure or an unexecuted result: 266 cases ran, 265 passed and
`UpdateEvidencePackageTests.test_current_root_census_excludes_relocated_lab_history`
failed in 48.488 seconds. The test
`tests/lib/supply_chain/test_update_gates.py` and ledger
`infra/09-platform-ops/security-updates/update-ledger.json` both retain their
baseline SHA-256 values
`060dc243c5061c820636dab9429ea3b61505ae013d2c543fe026c783ac538f4e` and
`a25b4092a88dd088a56e97b947bd51f3c5ad206e352edb4fcf57f8e3aa4c1911`.
P05/P08 owns resumption: add a truthful ledger identity/image/provenance entry
or change the owned declaration with evidence, then rerun that exact method.
Rollback affects only that owning ledger/declaration delta. P02 must not alter
the service, invent provenance or operate a runtime; the parsed
`services.blog-ingestion` declaration is unchanged from baseline.

## Handoff

| Target | Disposition | Current owner | Resume condition and recovery |
| --- | --- | --- | --- |
| P03 product/model registration | OUT_OF_SCOPE | P03 acceptance owner | Consume the exact P02 connection row; product-side registration and function proof remain separate |
| P04 Airflow URI encoding and native Celery behavior | TEST_RESIDUAL | P04 acceptance owner | Current frozen `infra/07-workflow/airflow/docker-compose.yml` SHA-256 `b3ddab42b06ae41a332b6b683ffb2846f9a40110903feb6d44727a162e05ecb9` has `_CMD` DSNs that interpolate passwords. Reproduce special-URI-character handling against the actual Celery provider before an encoding change; use a synthetic credential and preserve the current file before rollback. P02 changes only transport ports. The former `0bbb7e…` fingerprint is a dated pre-freeze observation, not current evidence. |
| P05 n8n consumer behavior | TEST_RESIDUAL | P05/P08 acceptance owners | Consume listener, MNG endpoint and Valkey ACL evidence; preserve accepted historical C19/C22 scope. The actual leaf12 supply-chain failure requires a truthful ledger identity/image/provenance entry or an owned declaration change before its exact method is rerun. |
| P06 secret custody and issuance | OUT_OF_SCOPE | P06 acceptance owner | Issue or rotate only with actual secret owner, target and recovery boundary. P02's synthetic presentation contract permits group-readable `0440`/`0640` where the service has the group, or runtime-`999` owned `0400`/`0600`; it rejects `0444`, `0644`, symlinks and hardlinks. The earlier grant finding was corrected in P02 by narrowing an overbroad mount; P06 custody, issuance and rotation remain unexecuted. P02 records no value and does not issue a credential. |
| P07 observations | OUT_OF_SCOPE | P07 acceptance owner | Add measurements only after selected source topology and consumer evidence are stable |
| P08 Valkey 9.1.3 advisory, supply-chain provenance and dependency audit | IMPROVEMENT_CANDIDATE | P08 image/advisory owner | Assess declared 9.1.2 against the official advisory, client compatibility and rollback before any image update. Jointly with P05, own the leaf12 truthful ledger/provenance repair and rollback boundary. Refresh the n8n source-binding transaction, then rerun `WorkflowVersionBundleTests.test_n8n_source_receipt_does_not_reuse_previous_native_acceptance` and its nested SEC01 route check; rollback only that owned receipt transaction. Own the failed controller dependency transaction: update canonical dependency input manifest(s), generated lock and appended evidence together; verify affected controller gates. Recovery reverts only the input-plus-lock delta and preserves the original FAIL receipt/history. |

## Related Documents

- [SPEC-0212](../spec.md)
- [SPEC-0212 Plan](../plan.md)
- [Historical P03 service integration contracts](../../0204-service-integration-security-and-operations/tasks/tsk-0011-p03-service-integration-contracts.md)
- [Application authentication guide](../../../05.operations/guides/03-identity-and-access/0079-application-auth-integration.md)
- [Workspace inventory data](../../../90.references/data/0096-workspace-inventory/README.md)
