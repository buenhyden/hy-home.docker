---
title: "Image, Supply-Chain and Storybook Compatibility Task"
version: "0.1.8"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-10"
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

The frozen upstream observations use Cosign 3.1.3 pinned at
`sha256:9e5c2f2edc34351160407ca3416c61855bdf9403c3c5936e0f0be7fc261611b8`,
with `--pull never`, read-only filesystem, dropped capabilities and
no-new-privileges. The exact issuer was
`https://token.actions.githubusercontent.com`; the exact certificate identity
was `https://github.com/n8n-io/n8n/.github/workflows/docker-build-push.yml@refs/heads/release/2.45.7`.
It supersedes the earlier regexp-only observation while preserving that history
in the ledger. Command payload files are not retained (`/dev/null` was used);
the sanitized transcript and recorded UTC windows bound, but do not turn these
into reusable artifact receipts.

The source-ledger gate now separates submission metadata from declaration
verification. `matches_target_latest` means only that a candidate's version
format is valid and its submitted target equals submitted latest;
`evidence_complete` means the submitted freshness/stable-channel/release-URL
material is complete. `matches_declared_latest` is `null`, rather than the old
boolean, because that gate does not inspect the active declaration. `ready`
retains only candidate-ledger completeness semantics. This compatibility change
is deliberately not source, deployment, registry-artifact or operational
acceptance.

The supply ledger separately records a bounded public-release observation
window of `2026-11-02T22:15:52Z`–`2026-11-02T22:16:20Z`: 61 public source
queries, with 60 responses and one access failure. Ninety-nine of the 112 root
service rows map to an existing source owner/release URL and thirteen remain
unmapped; nine Valkey/n8n rows are instead covered by their separate direct
candidate records. Each row is `PUBLIC_SOURCE_OBSERVATION_ONLY`, retains no raw
receipt and sets `freshness_verified`, `stable_channel_verified` and
`oci_availability_verified` to `false`. Public tags and pages do not
prove OCI availability, stable-channel support, security applicability,
compatibility, license, runtime or deployment acceptance.

### D09 evidence 2026-11-10

Recorded 2026-11-10; no criterion is accepted.

1. Superseded candidates: n8n 2.45.7 and Storybook 10.6.3. Current n8n is
   2.46.6; npm latest stable is 2.46.7 (published 2026-11-09, inside the 7-day
   soak) and the `next` channel 2.47.3 is rejected as non-stable. Storybook
   10.6.5 is current; 10.6.6 (published 2026-11-05) and next 16.4.6 (published
   2026-11-09) are in soak; vitest 5.1.0 (published 2026-11-02) is eligible,
   pending a Renovate group. Valkey 9.1.3-alpine (pushed 2026-10-27) is
   eligible; the 9.2 release candidates are rejected.
2. Merged changes: #859 Ollama 0.40.15 (`921276b53`; HOME applied, GPU 100%,
   33/33 layers); #865 redis_exporter v1.96.0 (`3bce085dd`; HOME applied);
   #854 alpine 3.24.3 (`4528c1ea7`; oauth2-proxy rebuilt and applied); #892
   dcgm-exporter 4.9.0 metric names (`161fbdf3f`; HOME applied, Prometheus rules
   reloaded, dashboard checked by the owner); #895 n8n font-noto pin so the
   image rebuilds (`0b7ffe8bc`; n8n and n8n-worker rebuilt and recreated); #891
   Renovate CI-toolchain and SurrealDB v2 rules (`bf922ad6c`). Open: #897
   Renovate digest pinning and grouping; #898 codeql-action 4.39.1.
3. Bitnami: 0 active images.
4. Remaining NOT_RUN: cgroup/resource measurement, Storybook a11y/MCP
   regression, rollback rehearsal.

### Owner review 2026-11-10

The owner asked for the Storybook audit and the n8n candidate verification to be
analyzed and reviewed. No criterion is accepted by this review.

- Storybook audit: `npm audit --package-lock-only --json` ran on copies of
  `projects/storybook/nextjs/package.json` and `package-lock.json` (Storybook
  10.6.5 lock) at `27cd872ea`, without touching `node_modules`. It completed
  with exit 1: 744 dependencies, 13 moderate, 0 high, 0 critical. All 13 trace
  to two advisories in development tooling (eslint and the Storybook Vite build
  chain): `glob` GHSA-3g3m-2fjr-6pw4 and `minimatch` GHSA-g3hv-75wg-m249; the
  `eslint` and `typescript-eslint` chain has a fix (`eslint@9.39.5`), the
  Storybook chain has none yet. The earlier ERROR was the isolated
  environment's DNS failure, not an advisory result. The 10.6.3 clean install
  and isolated regression PASS rows describe the superseded lock; the 10.6.5
  lock has only this audit.
- n8n candidate: 2.45.7 existed for GHSA-prmc-fg87-r4gh. The advisory's
  patched ranges are `>= 2.45.5`, `>= 2.46.1` and `>= 3.0.1`; the repository pin
  and both HOME containers run 2.46.6, which #895 rebuilt and recreated, so the
  2.45.7 bounded pulls and candidate verification no longer have a subject. The
  private-workflow and SSRF/egress review that the boundaries above require
  before an activation did not precede the 2.46.6 deployment; it stays open and
  applies to the next n8n activation (2.46.7 after its soak).
- Storybook audit decision (owner, 2026-11-10): the owner accepted the
  Storybook-chain findings as development-tooling risk until an upstream fix
  ships, and asked for the eslint chain to be fixed. No eslint fix exists: the
  suggested `eslint@9.39.5` is a major downgrade from the pinned 10.13.0, and
  the newest `@eslint/config-array` (0.23.5) still requires `minimatch ^10`,
  while the patched releases are `minimatch` 11.0.1 and `glob` 14.0.2. The
  eslint chain therefore stayed open; later on 2026-11-10 the owner accepted it
  as development-tooling risk as well and asked for eslint to move to the
  newest 10.x release, which does not change the advisory exposure.
- OpenBao r2 material rehearsal (2026-11-10): after the owner approved a
  one-time fetch from github.com, dl-cdn.alpinelinux.org, alpinelinux.org,
  cgr.dev and the Sigstore public-good endpoints, the preparing agent contacted
  two hosts outside that approval: `go version` inside the source tree
  auto-downloaded a Go toolchain from proxy.golang.org into `~/go/pkg/mod`, and
  documentation was read through raw.githubusercontent.com. Neither fetched a
  build material. The owner then approved proxy.golang.org and sum.golang.org,
  deleted the three rehearsal directories under `/tmp`, and the next run sets
  `GOTOOLCHAIN=local` and uses only the approved hosts.

### OpenBao r3 owner acceptance 2026-11-10

r2 failed the RUN-0105 SEC01 gate (x/net, go-jose v4 and klauspost Highs with fixed releases, and OpenBao v2.7.2 as a newer security release), so the owner approved r3 on v2.7.2. Its scan has Critical 0 and one High, GHSA-mgcc-cww5-fp2q in go-jose/v3 v3.0.5 with no fixed release; the owner accepted that residual risk with the two go-jose/v3 Mediums on 2026-11-10, recorded in POL-0085. The HOME cutover still needs the RUN-0105 window.

### Owner decisions 2026-11-10

The owner (@buenhyden) decided three items on 2026-11-10. For criterion 86
the owner accepts the latest-version gate FAIL as the record of missing lookups
the criterion asks for; acceptance waits for a passing gate row, since a FAIL
resolves only through a later PASS and a same-day rerun still fails. Criterion 87 is re-targeted to the deployed n8n
2.46.6, so the cancelled 2.45.7 pulls and the unrun 2.45.7 verification no
longer bind it. For criterion 88 the accepted moderate findings are recorded
by a high-threshold audit that passes.

### HOME image deployments 2026-11-10

The owner approved two HOME image deployments on 2026-11-10; neither changes
a criterion acceptance. #905: mailpit v1.33.0, crawl4ai sidecars on Python
3.15.2, ollama 0.40.16, oauth2-proxy v7.15.6, mlflow 3.18.0 and n8n and
n8n-worker 2.46.6; mng-valkey and dev-valkey run 9.1.3. #858: grafana 13.3.0,
alloy v1.21.3, pyroscope 2.4.3, dozzle v11.4.2, alertmanager v0.34.2, and loki
and tempo rebuilt on bases 3.7.9 and 3.1.1 (local tags keep their old names).
Before the Grafana recreate its data volume was copied to
`hy-home-infra_grafana-data-pre-13.3.0` (525.4 MB) with Grafana stopped. All
seven services are healthy with no restart; Prometheus shows 31 of 32 active
targets up, the down one being the opt-in `flower`. Alerts that were firing
before the deploy stay as they were; Grafana updated its bundled cloudwatch
plugin from the network at start. openbao and openbao-agent still run 2.7.1 r1
until the RUN-0105 window.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial source census | 86 | W91 | Root Compose declaration inventory | Public root sources | PASS | Observed 44 inputs and 112 declarations; this is source-only, and separate projects, Dockerfiles and locks keep independent denominators. | required | - |
| Ledger repair regression | 86 | W91 | Public update-ledger/source-binding tests and Ruff | Owned ledger and synthetic records | PASS | 43/45 scoped tests, 2 existing candidate skips and Ruff passed; `blog-ingestion`, 48 changed-input and 5 prior-stale rows were retained. Fresh lookups remain incomplete. | required | - |
| Ledger changed-line coverage | 86 | W91 | Stdlib trace over new gate paths | Five new executable lines | PASS | 5/5 (100%); `LatestVersionGateTests` plus synthetic CLI 12 pass. Broad trace was interrupted (exit 130) and system Python lacks coverage. | required | - |
| Public release observation bookkeeping | 86 | W91 | Incomplete-observation bookkeeping | 61 public queries in 28 seconds | PASS | All 61 outcomes were recorded: 60 responses, one access failure; 99/112 mapped and 13 unmapped. Raw receipts were not saved; freshness, stable-channel and OCI fields are false. | required | - |
| Public-observation regression | 86 | W91 | Observation and malformed-record rejection suite | Frozen public ledger | PASS | 37 tests and independent review passed; this validates bookkeeping only, not release-body or artifact facts. | required | - |
| P08 local integration | 86 | W91 | Update gates, workflow bundle, routing and contract checks | Current public P08 source | PASS | Earlier packet had 52 tests (50 pass/2 skip); frozen packet had 55 (53 pass/2 skip), with workflow contract and diff check passing. This does not replace broad selector integration, remote CI or operation. | required | - |
| P08 CI routing | 86 | W91 | P08 routing and workflow contract checks | Current P08 selector source | PASS | Six routing checks and workflow contract passed; the separate broad CI failure remains recorded under its own criterion row. | required | - |
| Documentation and registry checks | 86 | W91 | Catalog, DATA metadata/YAML and diff checks | Current P08 documents and public DATA | PASS | Catalog, DATA metadata/YAML and diff checks passed. Metadata and corpus lifecycle are separate P10 validator results and are not implied by this source check. | required | - |
| Latest-version gate | 86 | W91 | Lookup-status gate | Public ledger | FAIL | Exit 2: no missing/unexpected rows, but fresh lookups are incomplete; `ledger_complete` is false. | required | - |
| P08 list refresh recovery | 86 | W91 | Inventory scan then validate | Public inputs and 98 retained review receipts | PASS | 41,985/41,985 files listed; whole-body 6/2,320, partial 78/2,320, render 0/17, runtime/restore 0/112. Metadata/listing only. | required | - |
| Valkey candidate isolation | 87 | W92 | Owned candidate isolation | Valkey 9.1.3, synthetic ACL and cold-copy volume | PASS | Reported ACL denial, AOF/RDB and shared/dedicated roundtrips passed; this is a narrow fixture restore, not complete recovery or Compose parity. | required | - |
| n8n candidate preparation | 87 | W92 | Main/Runner index and platform lookup | n8n 2.45.7 candidates | PASS | Exact index/platform lookup passed; this is source/artifact metadata only. | required | - |
| n8n candidate bounded pulls | 87 | W92 | Bounded candidate pull | n8n 2.45.7 candidates | CANCELLED | Both pulls stopped at the five-minute boundary (exit 130); custom build, peer, Queue, Runner, SMTP and restore remain unrun. | optional | - |
| Supply-ledger candidate metadata | 87 | W92 | Candidate and registry-metadata review | Five Valkey and four n8n source rows | PASS | Release/advisory and registry observations were corrected; this is not candidate signature, SBOM, compatibility, native or operational evidence. | required | - |
| Candidate runtime and artifact verification | 87 | W92 | Isolated runtime and per-artifact review | Selected candidates | NOT_RUN | Custom-image digest is unknown; candidate signature, SBOM, compatibility, native and operation evidence remains unrun or unknown. | optional | - |
| Storybook clean lock install | 88 | W93 | Offline isolated `npm ci` | Tracked 10.6.3 lock and cached packages | PASS | 550 packages installed; local installation was not overwritten. | required | - |
| Storybook isolated regressions | 88 | W93 | Lint/typecheck/build and synthetic UI/auth checks | Isolated copy and synthetic credentials | PASS | lint/typecheck/build; auth/MCP 9/9; browser 14/14 including 320px; static image 7/7; six Button/AsyncState render states. Remote auth is not run. | required | - |
| Storybook audit | 88 | W93 | `npm audit` | Isolated dependency metadata | ERROR | DNS `EAI_AGAIN`; this does not establish absence of advisories. | required | - |
| Supply-chain gate | 89 | W94 | Existing gate against public ledger | Public source records | FAIL | Exit 2: coverage checked but ledger incomplete; it does not prove an image, signature, provenance or SBOM. | required | - |
| Upstream n8n/runners supply observations | 89 | W94 | Exact-identity Cosign observation | Exact GHCR index digests | PASS | Reported n8n signature/SLSA and runners CycloneDX/OpenVEX exit 0; raw receipts absent and unreviewed SLSA/SBOM semantics do not verify custom image, native behavior, restore or deployment. | required | - |
| Upstream supply negative observations | 89 | W94 | Exact-subject absence/error observation | Runners image/SLSA and n8n CycloneDX | FAIL | Runners signature exit 10, SLSA exit 1 and n8n CycloneDX exit 1; Valkey signing identity/issuer was not assessable. | required | - |
| Valkey local SBOM observation | 89 | W94 | Offline Syft scan | Canonical amd64 candidate | PASS | CycloneDX 1.7 SBOM, Alpine 3.24.3 and 716 components, exit 0. Locally generated SBOM is not publisher attestation; Grype lacked offline DB. | required | - |
| Selected candidate verification | 89 | W94 | Registry artifact and bounded isolated test review | Candidate writer packet | NOT_RUN | Valkey functional isolation is narrow; n8n and per-artifact verification are incomplete, so no deployment or rollback conclusion follows. | required | - |
| Storybook audit rerun | 88 | W93 | `npm audit` | Copies of the Storybook 10.6.5 `package.json` and `package-lock.json` at `27cd872ea` | FAIL | Exit 1: 13 moderate, 0 high, 0 critical over 744 dependencies; two development-tooling advisories (`glob` GHSA-3g3m-2fjr-6pw4, `minimatch` GHSA-g3hv-75wg-m249). See Owner review 2026-11-10. | required | - |
| n8n advisory fixed-range readback | 87 | W92 | Official advisory patched-range readback | GHSA-prmc-fg87-r4gh and the n8n 2.46.6 pin and HOME containers at `27cd872ea` | PASS | Patched `>= 2.46.1`; repository and HOME run 2.46.6, so the 2.45.7 candidate is superseded. SSRF/egress and private-workflow review stays open. | required | - |
| Storybook audit high threshold | 88 | W93 | `npm audit` | Copies of the Storybook `package.json` and `package-lock.json` at `59d1fe69f`, `--audit-level=high` | PASS | Exit 0: 0 high, 0 critical over 744 dependencies. 17 moderate packages trace to the two advisories the owner accepted as development-tooling risk (`glob` GHSA-3g3m-2fjr-6pw4, `minimatch` GHSA-g3hv-75wg-m249). | required | Storybook audit, Storybook audit rerun |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 86 | pending | Ledger repair regression, Latest-version gate | The owner decided on 2026-11-10 to accept this as recorded: the criterion records missing lookups, and the latest-version gate FAIL is that record. Acceptance stays pending because a FAIL row resolves only through a later PASS: a 2026-11-10 rerun still exits 2 with all 89 entries `blocked-evidence` (no fresh review or reviewed decision). Fresh lookups and artifact evidence are not claimed. | SPEC-0212 TSK-0047 |
| 87 | accepted | Valkey candidate isolation, n8n candidate preparation, n8n advisory fixed-range readback | The owner re-targeted the n8n evaluation from the superseded 2.45.7 candidate to the deployed 2.46.6 on 2026-11-10, so the 2.45.7 pull and verification rows are optional. 2.46.6 is in the advisory patched range; its signature and scan stay open under TSK-0041 criterion 60. No required observation is unresolved; owner @buenhyden accepted on 2026-11-10. | SPEC-0212 TSK-0047 with P02/P03/P05 handoffs |
| 88 | accepted | Storybook clean lock install, Storybook isolated regressions, Storybook audit, Storybook audit rerun, Storybook audit high threshold | The high-threshold audit passes with 0 high and 0 critical; the remaining moderate findings are the two development-tooling advisories the owner accepted on 2026-11-10. No required observation is unresolved; owner @buenhyden accepted on 2026-11-10. | SPEC-0212 TSK-0047 |
| 89 | pending | Supply-chain gate, Selected candidate verification | No cross-artifact inference; unavailable signing, provenance and SBOM material remains explicit. | SPEC-0212 TSK-0047 |

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
