---
title: "Image, Supply-Chain and Storybook Compatibility Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0047"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-03"
---

# Image, Supply-Chain and Storybook Compatibility Task

## Overview

### Objective

Implement the approved local P08 source and isolated compatibility work:
reconcile the public image/package ledger, evaluate selected Valkey 9.1.3 and
n8n 2.45.7 candidates, preserve and recheck Storybook 10.6.3, and bind supply
chain evidence to the exact artifact it concerns. This is not the historical
SPEC-0204 P08 operations-document-layout Task; neither its accepted records
nor its ownership are reopened.

## Inputs and Authorization

The direct P08 plan authorizes local source changes, bounded candidate artifact
preparation, synthetic and isolated validation, independent review, graph
refresh and a normal local logical commit. It excludes operating services,
host changes, actual credentials, external mail, remote integration, LAB
runtime and external repositories. Existing user changes remain preserved.

The observed clean starting HEAD is
`c9c497056f194b34b84df4297a0ad8016e5ced06`. The root Compose census of 44
inputs and 112 service declarations is a source observation, not a fixed
acceptance target. The supplied `dependencies` package was not found, so this
Task cannot claim a complete historical crosscheck.

Governing inputs are REQ-0027, AD-0031, SPEC-0212 and its Plan, P02 Valkey
topology, P03 Runner policy and P05 queue/notifier recovery boundaries. The
historic SPEC-0204 P08 task concerns operations-document layout only. Existing
C19/C22, Storybook and OpenBao records retain their recorded version, actor,
environment, consumer and date scope.

## Work Log

### Single-writer leases

Writers preserve one integration writer per path. Acceptance owner, writer,
reviewer, data owner and operational accepter are separate; agent labels do
not grant operational authority. Data owner and operational accepter are
UNASSIGNED unless a leaf contract names them.

| Scope | Single writer | Independent review | Boundary |
| --- | --- | --- | --- |
| Public update ledger, source-binding records and their direct tests | `/root/p08_supply` | independent security/code reviewer | `infra/09-platform-ops/security-updates/` and owned supply-chain tests only |
| Valkey/n8n candidate declarations, shared Compose/build inputs and directly related checks | `/root/p08_candidates` | independent IaC/security reviewer | Current non-LAB source; preserve P02/P03/P05 contracts and no service operation |
| Storybook isolated regression evidence and project-local compatibility changes | `/root/p08_storybook` | independent code/security reviewer | `projects/storybook/nextjs` and direct tests only; no remote-device acceptance |
| SPEC-0212, this Task, DATA-0096 and P08 research narrative | `/root/p08_docs` | independent document reviewer | Current Task/spec/plan/data documentation; preserve completed Task bodies |
| CI or manifest registration | assigned CI writer | independent CI reviewer | No selector weakening; P03 parity residual remains independent |

Public document baseline SHA-256 values are SPEC
`dfdf3f8cb764d2fc3c0fa54c668afb198754cf6d4a8160e9cdcab536a7cc892e`, Plan
`966505ded3110267940801a43f2d9c2770ace7b50c6cf7cf98033dc694d4a3b8`, DATA
README `0298d87567b8c9bdf74949b6d9204643902bcf866761c3463548a5999c5fe9cf`
and DATA payload
`eea4d87d069450239481900951d5889eedf1eca7b320cde660e76fa0b562e060`.
This Task was absent at that baseline. Those hashes are source identity only,
not runtime, artifact or credential evidence.

### Current dispositions

| Item | Criterion | Work Unit | Initial disposition | Current boundary |
| --- | --- | --- | --- | --- |
| P08.01 | 86 | W91 | IMPLEMENT_GAP | Public ledger omitted `blog-ingestion`; source fingerprints and candidate lookup status require reconciliation |
| P08.02 | 87 | W92 | IMPROVEMENT_CANDIDATE | Valkey 9.1.3 and n8n 2.45.7 are selected candidates; source/isolated proof and recovery evidence decide activation |
| P08.03 | 88 | W93 | REUSE_ACCEPTED | Storybook 10.6.3 remains selected; the local 10.6.2 installation is not tracked-lock evidence |
| P08.04 | 89 | W94 | TEST_RESIDUAL | Existing sample-service receipts cannot prove actual service/custom image signatures or provenance |

### Official applicability and safety boundaries

On 2026-11-03, the official [Valkey 9.1.3 release](https://github.com/valkey-io/valkey/releases/tag/9.1.3)
and GHSA-f4q9-j22m-xqq9 were read as an update candidate. The advisory is
conditional on cluster mode; source declarations for shared MNG, DEV and
dedicated broker must not be labelled vulnerable merely from their 9.1.2
version. P02 owns topology and consumer/ACL contracts; this Task owns the
version/advisory decision and evidence.

The official [n8n 2.45.7 release](https://github.com/n8n-io/n8n/releases/tag/n8n%402.45.7)
and [GHSA-prmc-fg87-r4gh](https://github.com/n8n-io/n8n/security/advisories/GHSA-prmc-fg87-r4gh)
identify a fixed release family for a credential cross-origin redirect issue.
Public Hermes source fixes its internal endpoint and disables redirects, while
private workflow applicability remains uninspected. The exact n8n 2.45.7
source declares `n8n-workflow` 2.45.4; Main, Worker, Runner, custom image and
peer/lock evidence form one bundle. A registry image, platform, signature or
recovery gap keeps the candidate unactivated. The tracked Compose source does
not declare `N8N_SSRF_PROTECTION_ENABLED`; that is a source observation, not a
claim about effective runtime setting or exposure. A deferred n8n decision
requires private-workflow and SSRF/egress review before any activation.

The tracked Storybook lock declares 10.6.3. Its clean isolated installation
is distinct from the local 10.6.2 installation and from prior remote-device
acceptance. The official [upgrade guidance](https://storybook.js.org/docs/releases/upgrading)
and releases 10.6.4/10.6.5 were consulted as compatibility inputs. No current
consumer-specific reason to adopt either later patch is recorded here.

Per-artifact verification follows the official [Sigstore verification
guidance](https://docs.sigstore.dev/cosign/verifying/verify/) and [SLSA
artifact-verification guidance](https://slsa.dev/spec/v1.2/verifying-artifacts).
Every subject needs its own digest plus publisher/identity-or-key and available
provenance/SBOM/license evidence. A GHCR image receipt, a base image receipt,
or the sample-service policy never validates Docker Hub or custom images.
Absent material is `NOT_RUN` or `BLOCKED`, never a verification PASS.

The source-ledger gate now separates submission metadata from declaration
verification. `matches_target_latest` means only that a candidate's version
format is valid and its submitted target equals submitted latest;
`evidence_complete` means the submitted freshness/stable-channel/release-URL
material is complete. `matches_declared_latest` is `null`, rather than the old
boolean, because that gate does not inspect the active declaration. `ready`
retains only candidate-ledger completeness semantics. This compatibility change
is deliberately not source, deployment, registry-artifact or operational
acceptance.

## Evidence

| Evidence | Criteria | Check | Input | Result | Boundary |
| --- | --- | --- | --- | --- | --- |
| Initial source census | 86 | Root Compose declaration inventory | Public root sources | Observed: 44 inputs, 112 declarations | Source-only observation; separate projects, Dockerfiles and locks have their own denominators |
| Ledger repair regression | 86 | Public update-ledger/source-binding tests and Ruff | Owned ledger and synthetic records | PASS: 43/45 scoped tests; 2 existing candidate cases SKIP; Ruff PASS. A CLI public fixture demonstrated the new field semantics. `blog-ingestion`, 48 changed-input and 5 prior-stale history rows were retained | Fresh official lookups remain incomplete; not an overall support PASS |
| Ledger changed-line coverage | 86 | Stdlib trace over new gate execution paths | Five new executable lines; subprocess/existing lines excluded | PASS: 5/5 (100%). `LatestVersionGateTests` plus synthetic CLI: 12 PASS | Broad trace was interrupted during parsing (exit 130); system Python lacks the coverage module |
| P08 local integration | 86–89 | Update-gates, workflow-version-bundle, P08 routing and workflow contract | Current public P08 source | PASS: 51 tests, 2 skipped; workflow-contract PASS | Does not replace broad selector integration, remote CI or operation |
| Latest-version gate | 86 | Current lookup-status gate | Public ledger | Exit 2: no missing/unexpected rows, but fresh lookups incomplete | `ledger_complete: false`; `ready` is ledger completeness only and no candidate is declared current solely from this gate |
| Supply-chain gate | 89 | Existing gate against public ledger | Public source records | Exit 2: coverage checked, ledger incomplete | Does not prove a service image, signature, provenance or SBOM |
| Storybook clean lock install | 88 | Offline isolated `npm ci` | Tracked 10.6.3 lock, cached packages | PASS: 550 packages | Local installation was not overwritten |
| Storybook isolated regressions | 88 | lint/typecheck, Storybook/Next/MCP build, synthetic auth and browser checks | Isolated copy and synthetic credentials | PASS: lint/typecheck/build; auth/MCP 9/9; browser 14/14 incl. 320px; static image 7/7; `renderToString` Button/AsyncState 6 states | Next prerender and synthetic SSR only, no HTTP SSR request; remote auth is NOT_RUN |
| Storybook audit | 88 | `npm audit` | Isolated dependency metadata | NOT_RUN: DNS `EAI_AGAIN` | Network failure is not absence of advisories |
| P08 CI routing | 86–89 | P08 routing and workflow-contract checks | Current P08 selector source | PASS: six routing checks and workflow contract | Separate full CI failures remain below |
| Documentation and registry checks | 86–89 | Operations catalog, DATA metadata/YAML and changed-document lifecycle validation | Current P08 documents and public DATA | PASS: operations catalog; DATA metadata validator and YAML parse; diff check. `check-document-metadata --mode check-changed` and corpus lifecycle began from explicit baseline but exceeded the local 30-second execution window without a result. | Timed-out document checks are NOT_RUN, not a PASS; rerun in a sufficient local window before final acceptance |
| Existing CI residuals | 86–89 | Broad CI / exact-selector checks | 145-test public-plan contract | BLOCKED for selector integration: one run of `test_ci_gate_plan` had 7 failures/321 errors and an independent 145-test public-plan review had 8 failures/326 errors, both from existing `leaf.p03-hermes` `ci-gate-public-execution-parity`. That leaf itself had 62 PASS/1 skip. A separate exact-selector list check had one failure. | P03/CI owner must reconcile parity and selector expectation; remote CI is NOT_RUN. Do not relabel either as a P08 leaf failure or mask it with local PASS |
| Supply-ledger candidate metadata | 86, 87, 89 | Public Valkey/n8n candidate and registry-metadata review | Five Valkey and four n8n selected source rows | Official release/advisory and registry metadata observations corrected; custom-image digest `UNKNOWN`; candidate signature/SBOM/compatibility/native/operation remain NOT_RUN and applicability UNKNOWN | No cross-artifact verification or activation follows |
| Valkey candidate isolation | 87 | Reported exact Docker Hub index/amd64 inspect and owned-container proof | Valkey 9.1.3, internal network; shared/default 6379, dedicated/nondefault 16379 and restore 17379; synthetic named ACL and separate cold-copy volume | LIMITED_ISOLATED_PASS (reported summary): server version; named-key allow/other-key+DEL denial; AOF/RDB; current n8n 2.43.6 ioredis LPUSH/RPOP shared roundtrip; current Airflow 3.3.2 redis-client dedicated roundtrip; read-only source-volume cold copy to separate restore volume with restored value/new Airflow queue roundtrip. Static P02/config/URI 69/69 and candidate/mount 13/13 passed; reported owned cleanup left zero residuals. | Raw command log and exact timestamp are not retained in this Task, so this is not independently reproducible evidence. The separate cold-copy volume is a narrow fixture restore, not complete independent backup recovery; Celery/Bull lifecycle, Compose secret/exporter parity and supply-chain verification remain untested. |
| P08 list refresh recovery | 86 | `workspace-inventory.py scan --connections` then `validate` | Public inputs and a local merged review file reconstructed from 98 retained public review receipts | PASS for list/metadata only: 41,985/41,985 listed files; whole-body 6/2,320 and partial 78/2,320; render 0/17, runtime 0/112 and restore 0/112. The initial P01-only review input was rejected as a replacement because it would have reduced the retained review denominator. The scan was repeated after the final supply-ledger correction with the same result. | This preserves review history in the local input; it is not a semantic, live-runtime or restore result. |
| n8n candidate preparation | 87, 89 | Exact Main/Runner index and platform lookup followed by bounded pulls | Selected n8n 2.45.7 and Runner candidates | Index/platform lookup PASS; both pulls interrupted at the five-minute boundary (exit 130), leaving only partial cache | Custom build/peer/native Queue/Runner/SMTP/restore and all artifact verification remain NOT_RUN; no source pin activation |
| Selected candidate verification | 87, 89 | Exact registry artifact, platform, digest, identity/key, provenance/SBOM/license and bounded isolated tests | Candidate writer packet | TEST_RESIDUAL | Valkey functional isolation is narrow; n8n and per-artifact verification are incomplete, so no operating deployment or rollback claim |

## Criterion Acceptance

| Criterion | Acceptance | Decision | Current Owner |
| --- | --- | --- | --- |
| 86 | Public inventory and research applicability | IMPLEMENT_GAP: corrected ledger tests do not close incomplete fresh lookups | SPEC-0212 TSK-0047 |
| 87 | Valkey/n8n compatibility bundle | IMPROVEMENT_CANDIDATE pending exact source, candidate artifact and isolated/recovery evidence; a deferred n8n update resumes with private-workflow plus SSRF/egress review | SPEC-0212 TSK-0047 with P02/P03/P05 handoffs |
| 88 | Storybook 10.6.3 compatibility | SOURCE_READY: isolated lock regression passed; current runtime, remote device and audit remain separate | SPEC-0212 TSK-0047 |
| 89 | Artifact-specific supply-chain verification | TEST_RESIDUAL: no cross-artifact inference; unavailable material remains explicit | SPEC-0212 TSK-0047 |

## Review and Completion

Before final acceptance, refresh DATA-0096 only after source changes freeze;
compare its start/end fingerprint, preserve changed-review invalidation and
record only the affected observations. Run documentation, registry, relevant
QA and CI selector checks without converting a local check into hosted CI.
Run `graphify update .` after the final source diff. Independent code,
security, IaC and document reviewers report their own evidence without
editing another writer's lease.

Current operation, credential rotation, independent restore, remote CI and
final operational acceptance are `NOT_RUN` unless separately evidenced and
authorized. Candidate image activation and any host/service recreation remain
outside this Task's local source evidence.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
- [P02 service connection Task](tsk-0041-service-connection-contracts.md)
- [P03 models and Runner Task](tsk-0042-models-runners-wiki.md)
- [P05 notifier recovery Task](tsk-0044-opsflow-notifier-recovery.md)
- [Historic P08 operations-document-layout Task](../../0204-service-integration-security-and-operations/tasks/tsk-0015-p08-operations-document-layout.md)
