---
title: "Runtime Compatibility and Security Task"
version: "1.0.14"
type: "sdlc/task"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0001"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
branch_integration_receipts:
- {source_commit: "79b42b604b99bcc6712887d29e36f8244ec0f9eb", source_package_path: "docs/03.specs/0201-home-infrastructure-diagnosis-and-work-design", source_artifact_id: "SPEC-0201", preserved_package_path: "docs/98.archive/superseded/03.specs/0201-home-infrastructure-diagnosis-and-work-design", target_package_path: "docs/03.specs/0204-service-integration-security-and-operations", target_artifact_id: "SPEC-0204", disposition: "historical-superseded"}
- {source_commit: "79b42b604b99bcc6712887d29e36f8244ec0f9eb", source_package_path: "docs/03.specs/0202-development-data-and-lab-isolation", source_artifact_id: "SPEC-0202", preserved_package_path: "docs/98.archive/superseded/03.specs/0202-development-data-and-lab-isolation", target_package_path: "docs/03.specs/0204-service-integration-security-and-operations", target_artifact_id: "SPEC-0204", disposition: "historical-superseded"}
- {source_commit: "79b42b604b99bcc6712887d29e36f8244ec0f9eb", source_package_path: "docs/03.specs/0203-quality-results-and-isolated-load-testing", source_artifact_id: "SPEC-0203", preserved_package_path: "docs/98.archive/superseded/03.specs/0203-quality-results-and-isolated-load-testing", target_package_path: "docs/03.specs/0204-service-integration-security-and-operations", target_artifact_id: "SPEC-0204", disposition: "historical-superseded"}
- {source_commit: "79b42b604b99bcc6712887d29e36f8244ec0f9eb", source_package_path: "docs/03.specs/0205-storybook-dependency-refresh", source_artifact_id: "SPEC-0205", preserved_package_path: "docs/98.archive/superseded/03.specs/0205-storybook-dependency-refresh", target_package_path: "docs/03.specs/0204-service-integration-security-and-operations", target_artifact_id: "SPEC-0204", disposition: "historical-superseded"}
---

# Runtime Compatibility and Security Task

## Objective

After owner approval, correct the confirmed n8n compatibility and secret
consumer defects, check Crawl4AI's security pin, and separate OpenBao sealed
status from readiness. Verify Cassandra LAB's already changed official-image
contract without moving data or creating LAB credentials again.

## Inputs

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7` on 2026-10-03;
SPEC-0201 W5, SPEC-0204 criteria 1-4/8 and Plan W1/W2/W5. The original approval-draft boundary below is historical for pre-PR359 planning. Later owner approval authorized the recorded source/document reconciliation only; it still does not authorize image pulls, HOME deployment, secret issuance, credential rotation, data restore or service operations.

## Work Log

### Current Lifecycle Reconciliation

The present Stage 99 reconciliation derives `blocked` from the recorded
exact-image, egress, Agent-renewal, and operational-approval blockers. Earlier
transition anchors are not observed and are not backfilled.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0001 | in-progress | blocked | #current-lifecycle-reconciliation |

### Protected source and archive integration writer ledger — approved reintegration

Protected PR358 delivered the active Spec/Plan and in-progress Tasks at
`79b42b604b99bcc6712887d29e36f8244ec0f9eb` (run37177848208 PASS). This is the captured protected base
for the approved reintegration ledger; verify the actual base and closure source ancestry before source edits.
Prior source/integration/disposition approvals persist; archive records grant no authority. Task1 exclusively writes shared surfaces; Tasks2–4 consume the contract.

Approved source writers: 125 exact paths = 123 closure-only paths + two shared paths (`.github/workflow-contract.yml`,
`tests/validation/test_secret_metadata_sync.py`). The shared table repeats the same Task1 ownership, not another writer.
Actual rename-aware comparison decides add/delete/modify; private contents are excluded.

```text
.env.example
.github/workflow-contract.yml
.gitignore
docs/02.architecture/decisions/0042-openbao-unseal-method.md
docs/02.architecture/descriptions/0004-data-architecture.md
docs/02.architecture/descriptions/0031-home-development-host.md
docs/05.operations/guides/0010-sensitive-env-vars-comparison.md
docs/05.operations/guides/0021-backup-and-restore.md
docs/05.operations/guides/0045-prometheus.md
docs/05.operations/guides/0053-n8n.md
docs/05.operations/guides/0064-performance-testing.md
docs/05.operations/guides/0085-openbao.md
docs/05.operations/guides/0091-crawl4ai.md
docs/05.operations/guides/0096-k8s-integration.md
docs/05.operations/guides/0099-system-operations.md
docs/05.operations/policies/0021-backup-and-restore.md
docs/05.operations/policies/0053-n8n.md
docs/05.operations/policies/0085-openbao.md
docs/05.operations/runbooks/0014-keycloak.md
docs/05.operations/runbooks/0021-backup-and-restore.md
docs/05.operations/runbooks/0034-qdrant.md
docs/05.operations/runbooks/0050-airflow.md
docs/05.operations/runbooks/0053-n8n.md
docs/05.operations/runbooks/0057-open-webui.md
docs/05.operations/runbooks/0085-openbao.md
docs/05.operations/runbooks/0089-jupyterlab.md
docs/05.operations/runbooks/0090-dbt.md
docs/05.operations/runbooks/0091-crawl4ai.md
docs/05.operations/runbooks/0096-k8s-integration.md
docs/05.operations/runbooks/0097-superset.md
docs/05.operations/runbooks/0098-cold-start-and-reboot.md
examples/operations/locust-telemetry/README.md
examples/operations/locust-telemetry/acceptance.py
examples/operations/locust-telemetry/compose.override.yml
examples/operations/locust-telemetry/locustfile.py
examples/operations/quality-metrics/README.md
examples/operations/quality-metrics/acceptance.py
examples/operations/quality-metrics/docker-compose.yml
examples/operations/quality-path-guard/README.md
examples/operations/quality-path-guard/acceptance.py
examples/operations/quality-path-guard/docker-compose.yml
infra/03-security/openbao/docker-compose.yml
infra/04-data/dev-db/README.md
infra/04-data/dev-db/pg/README.md
infra/06-observability/grafana/dashboards/Infrastructure/perf-results.json
infra/06-observability/grafana/provisioning/contracts/perf-db.datasource.yml.example
infra/07-workflow/n8n/Dockerfile
infra/07-workflow/n8n/README.md
infra/07-workflow/n8n/dev.Dockerfile
infra/07-workflow/n8n/docker-compose.yml
infra/07-workflow/n8n/docker-entrypoint.dev.sh
infra/07-workflow/n8n/docker-entrypoint.sh
infra/08-ai/crawl4ai/README.md
infra/08-ai/crawl4ai/docker-compose.yml
infra/08-ai/mlflow/README.md
infra/09-platform-ops/project-registration/README.md
infra/09-platform-ops/project-registration/schema.json
infra/09-platform-ops/renovate/systemd/hyhome-renovate.service
infra/09-platform-ops/restic/backup.sh
infra/09-platform-ops/restic/bin/hyhome-backup.sh
infra/09-platform-ops/restic/docker-compose.yml
infra/11-quality/k6/README.md
infra/11-quality/k6/container_executor.py
infra/11-quality/k6/http_guard.py
infra/11-quality/k6/object_store.py
infra/11-quality/k6/quality_run.py
infra/11-quality/k6/result_import.py
infra/11-quality/k6/result_inspection.py
infra/12-analytics/dbt/README.md
infra/12-analytics/jupyterlab/README.md
labs/locust.md
labs/locust.yml
renovate.json5
scripts/manifest.yaml
scripts/operations/gen-secrets.sh
scripts/validation/check-project-registration.py
scripts/validation/validate-docker-compose.sh
secrets/README.md
secrets/SENSITIVE_ENV_VARS.md.example
secrets/auth/airflow/.gitkeep
secrets/auth/dozzle/.gitkeep
secrets/auth/gatus/.gitkeep
secrets/auth/grafana/.gitkeep
secrets/auth/kafbat/.gitkeep
secrets/auth/keycloak/.gitkeep
secrets/auth/oauth2-proxy/.gitkeep
secrets/auth/open-webui/.gitkeep
secrets/auth/superset/.gitkeep
secrets/auth/traefik/.gitkeep
secrets/automation/airflow/.gitkeep
secrets/automation/n8n/.gitkeep
secrets/backup/mng-pg/.gitkeep
secrets/backup/openbao/.gitkeep
secrets/backup/restic/.gitkeep
secrets/communication/slack/.gitkeep
secrets/communication/smtp/.gitkeep
secrets/communication/stalwart/.gitkeep
secrets/communication/supabase/.gitkeep
secrets/data/opensearch/.gitkeep
secrets/data/qdrant/.gitkeep
secrets/data/supabase/.gitkeep
secrets/db/legacy-app/.gitkeep
secrets/db/mng-pg/.gitkeep
secrets/db/mng-valkey/.gitkeep
secrets/db/n8n-valkey/.gitkeep
secrets/db/surrealdb/.gitkeep
secrets/observability/grafana/.gitkeep
secrets/observability/prometheus/.gitkeep
secrets/security/openbao/.gitkeep
secrets/storage/seaweedfs/.gitkeep
secrets/tools/crawl4ai/.gitkeep
secrets/tools/jupyterlab/.gitkeep
secrets/tools/open-notebook/.gitkeep
secrets/tools/pact-broker/.gitkeep
secrets/tools/renovate/.gitkeep
secrets/tools/superset/.gitkeep
secrets/tools/terrakube/.gitkeep
tests/validation/test_k6_results.py
tests/validation/test_locust_telemetry.py
tests/validation/test_project_registration.py
tests/validation/test_quality_object_store.py
tests/validation/test_quality_observability.py
tests/validation/test_quality_raw_points.py
tests/validation/test_secret_metadata_sync.py
tests/validation/test_service_runtime_compatibility.py
```

#### Shared resolution — 18 exact paths

| Path | Resolution contract |
| --- | --- |
| `.github/workflow-contract.yml` | Keep the approved bounded audit leaf and exact acceptance fields; retain its four registered quality modules once; add service_runtime_compatibility, quality_object_store, quality_raw_points, locust_telemetry to compose suite and project_registration to repository-integrity suite. |
| `docker-compose.yml` | Combine closure secret reference paths with current Storybook root include and dedicated experience_ingress_net; preserve all newer main additions. |
| `docs/03.specs/0204-service-integration-security-and-operations/plan.md` | Keep actual protected active lifecycle; integrate closure work-unit outcomes and current acceptance limits. |
| `docs/03.specs/0204-service-integration-security-and-operations/spec.md` | Keep actual protected active lifecycle and approvals; reconcile existing closure acceptance and source outcomes without weakening runtime criteria. |
| `docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0001-runtime-compatibility-and-security.md` | Retain actual protected in-progress lifecycle, new audit approvals and independent evidence; add typed handoff receipts and criterion/Plan mapping. Do not substitute closure blocked status or claim runtime completion. |
| `docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0002-external-project-integration.md` | Keep actual protected in-progress lifecycle and unchanged approval provenance; integrate closure execution evidence. Task1 owns shared writes; this Task consumes the integration contract. |
| `docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0003-backup-and-cross-tier-operations.md` | Keep actual protected in-progress lifecycle and unchanged approval provenance; integrate closure execution evidence. Task1 owns shared writes; this Task consumes the integration contract. |
| `docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0004-secret-layout-and-environment-parity.md` | Keep actual protected in-progress lifecycle and unchanged approval provenance; integrate closure execution evidence. Task1 owns shared writes; this Task consumes the integration contract. |
| `docs/03.specs/README.md` | Keep SPEC-0206 navigation; remove 0201/0202/0203/0205 current rows only with atomic raw packet handoff and retained records. |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md` | Preserve historical rationale and Storybook membership; regenerate only current-service-inventory projection from combined tracked sources. |
| `docs/99.templates/registry.json` | Keep current ID allocation: operations high_water 101 and next_number 102 or a later actual protected allocation; never revert to closure 99/100. |
| `infra/06-observability/grafana/README.md` | Keep current Storybook coverage and newer resources; add closure perf-results contract and source-only datasource evidence. |
| `infra/tech-stack.versions.json` | Generate from resolved Compose source; retain Storybook and reflect n8n/Crawl4AI declaration changes. Do not select either old JSON wholesale. |
| `projects/storybook/nextjs/package-lock.json` | Preserve current UI/MCP graph; no restoration of the pre-0206 lockfile. Verify approved audit chain remains exact. |
| `projects/storybook/nextjs/package.json` | Keep current prepare/build:ui, UI workspace, MCP package, scripts and dependency graph. Closure pins already match the current package train. |
| `tests/lib/gate/test_github_workflow_contract.py` | Keep current four registrations and complete Storybook fixture inputs; align expected compose selectors with the combined suite without duplicates. |
| `tests/validation/test_compose_baseline_gates.py` | Keep current Compose schema loader, dedicated Storybook ingress tests and pinned Ruff formatting; add closure dev-pg Restic failure/recovery assertions. |
| `tests/validation/test_secret_metadata_sync.py` | Keep candidate _ComposeLoader and schema-tag/unsafe-tag rejection tests; add closure compose_default normalization, public-root metadata checks, regular-empty markers and service/instance-path ownership assertions. |

#### Full packet preservation and consumer cutover

Keep all14 completed closure members from `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` with original raw bytes,
modes/member sets and catalog Source. Preserve each current full packet from the actual protected base into its exact
superseded mirror; do not rewrite statuses, frozen bodies or old audit evidence to manufacture completion.

| Current full packet | Exact superseded mirror | Existing completed closure packet |
| --- | --- | --- |
| `docs/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` | `docs/98.archive/superseded/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` | `docs/98.archive/completed/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` |
| `docs/03.specs/0202-development-data-and-lab-isolation/` | `docs/98.archive/superseded/03.specs/0202-development-data-and-lab-isolation/` | `docs/98.archive/completed/03.specs/0202-development-data-and-lab-isolation/` |
| `docs/03.specs/0203-quality-results-and-isolated-load-testing/` | `docs/98.archive/superseded/03.specs/0203-quality-results-and-isolated-load-testing/` | `docs/98.archive/completed/03.specs/0203-quality-results-and-isolated-load-testing/` |
| `docs/03.specs/0205-storybook-dependency-refresh/` | `docs/98.archive/superseded/03.specs/0205-storybook-dependency-refresh/` | `docs/98.archive/completed/03.specs/0205-storybook-dependency-refresh/` |

Additional exact writers are `docs/98.archive/retention-catalog.md` (preserve existing rows; add actual raw-capture
rows), `docs/03.specs/README.md` (retain 0206/unfinished routes) and `docs/05.operations/guides/0064-performance-testing.md` (cut the0203 link over to completed historical evidence). Task1 is the future typed carrier, one receipt per
source packet, only after real-base capture.

`docs/03.specs/0206-shared-storybook-and-docs-mcp/spec.md` owns the two Traceability consumer cutovers from
current0201/0205 paths to their completed archives. Preserve its active status/criteria/history; if Overview describes
the old braces hold as current, identify the then-observed baseline and route current security behavior to the canonical
quality policy. Increment from its actual future protected version; preserve newer concurrent edits. This extra consumer
writer is outside closure157, not a new functional feature.

Coverage: 123 closure-only +18 shared +14 completed archive members +two separate paths =157 rename-aware closure paths.
The two separate paths are `docs/98.archive/retention-catalog.md` and `docs/03.specs/0203-quality-results-and-isolated-load-testing/tasks/tsk-0001-quality-source-integration.md`; the latter deletion is paired with full raw-packet handoff.
Superseded mirrors and new consumer cutovers are additional handoff work. Verify exact coverage on actual main; new
writers require an exact ledger amendment before editing. Legacy marker rename sources are preserve/verify-only, never
private deletion permission. Keep existing audit acceptance policy/adapter/tests and current Storybook/UI/MCP
declarations; OpenBao2.7 adoption is excluded, only its approved readiness correction is in scope.

`docs/05.operations/policies/0100-development-database.md` is an additional exact consumer writer: metadata parent and inline parent description move to current SPEC-0204; historical SPEC-0202 evidence and all controls remain unchanged. Prior Prompt02 GDE/POL/RUN-0100 handoff and independent policy review cover this correction.

#### Integration, checks and rollback

Normal three-way merge must make closure source commits ce001be7,686b7177, 9f89d0a2 ancestors; no squash, ours strategy,
wholesale tree replacement or frozen-body edits. Preserve all unrelated worker state. Map every criterion and Plan unit
to actual source/checks/current durable owners before disposition; old completed0205 proves dependency refresh, not the
new bounded audit policy.

Use current path-aware selection and exact selector equality; run relevant gate/audit/workflow, secret/schema, Compose,
runtime-compatibility, project-registration and quality/object/raw/Locust regressions. Render root/LAB with public
synthetic inputs; never profile-star up. Regenerate versions and only current-service inventory through their registered
generators. Check changed metadata/corpus/raw-archive bytes,modes,members,reachability/links against actual protected
base, then independent review and hosted required CI. Before remote merge, abandon only this owned clean checkout; after
merge use a scoped revert preserving history, strict audit recovery and runtime state.

This ledger entry records scope only; it performs no source integration or preservation. HOME start, restart, deployment/unseal, real
backup/restore/migration/deletion, secret rotation/private-file operations, image execution and host/network changes
remain separately approved; no historical receipt proves a new deployment.

| Service and source evidence | Proposed exact writer path and variable/consumer | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| n8n main/worker use one older build pin while both runners use a newer image; official n8n documentation requires matching versions. Proposed target is the 2026-10-02 stable `2.41.6`, subject to a fresh release/digest/compatibility check | `infra/07-workflow/n8n/docker-compose.yml`, `Dockerfile`, `dev.Dockerfile`, `renovate.json5`; `N8N_VERSION`, four image declarations; main, worker and two runners | Same-version/render assertion, queue/manual/scheduled/webhook/Code smoke on synthetic metadata; revert version declarations before HOME rollout. A live DB upgrade needs metadata plus encryption-key backup and its own operation approval | Source Task approval; HOME start/restart separately |
| n8n instance has singular timeout key; runner image `_FILE` support is not documented | `infra/07-workflow/n8n/docker-compose.yml`, `docker-entrypoint.sh`, `docker-entrypoint.dev.sh`; `N8N_RUNNERS_TASK_TIMEOUT`, broker token reference `n8n_runner_auth_token`, selected `N8N_VALKEY_SECRET` file; n8n and both runners. A new runner wrapper is excluded until an exact Task amendment | Empty/mismatched file rejection, supported variable render, no secret in argv/log/layer or JS/Python Code-task environment, bounded worker restart; revert scoped wrapper/Compose | Secret **reference** edits in approved source scope; no token reading/rotation |
| Crawl4AI is pinned before the official `0.9.4` security fixes, is opt-in and has no confirmed consumer | `infra/08-ai/crawl4ai/docker-compose.yml`, `renovate.json5` only if matching update rule, existing `docs/05.operations/{guides,policies,runbooks}/0091-crawl4ai.md`; URL/redirect/robots/link preview input | Official advisory and image digest/architecture review, synthetic DNS/redirect/private-destination denial, preserve separate bridge and verify real egress enforcement separately; revert image pin if behavior differs | No new consumer network, HOME activation or crawler payload collection |
| OpenBao health accepts sealed status as healthy | `infra/03-security/openbao/docker-compose.yml`, existing `docs/05.operations/{guides,policies,runbooks}/0085-openbao.md`; `bao status` result | Synthetic sealed/unsealed/Agent-template-current probes and dependency render; revert health semantics if dependency contract fails | No unseal, credential rotation or HOME restart |
| Cassandra official image move already lives in LAB | `labs/cassandra.yml`, `labs/cassandra.md`, existing GDE/POL/RUN-0025 read-only unless a confirmed defect appears; `/var/lib/cassandra` | LAB render, data/auth/UID limits recorded; no duplicate migration or fabricated auth | No old Bitnami data move, LAB up or secret issue |

Version projection `infra/tech-stack.versions.json` is generated from source;
run `bash scripts/operations/sync-tech-stack-versions.sh --check` and the
registered write route only when a declaration changes. Update Korean
`infra/07-workflow/n8n/README.md` and current Stage 05 n8n documents if their
consumer instructions change. Proposed focused regression owner is a single
new `tests/validation/test_service_runtime_compatibility.py` unless an existing
contract test already covers each changed invariant.

Official source evidence checked on 2026-10-03:
[n8n task runners](https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners/),
[n8n queue mode](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode/),
[n8n runner environment](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/task-runners/),
[n8n releases](https://github.com/n8n-io/n8n/releases), and
[Crawl4AI security advisories](https://github.com/unclecode/crawl4ai/security),
and [OpenBao status exit codes](https://openbao.org/docs/commands/status/).
Recheck exact stable image, digest and compatibility at implementation time;
none of these links is a tested HOME deployment.

## Verification Evidence

### Storybook blocker and alternative assessment — 2026-10-04

The user requested investigation and alternatives if no immediate fix exists,
then prioritized main integration and eligible package preservation. This is
read-only research recorded by this Task's protected-delivery owner; npm
implementation remains owned by SPEC-0205 and shared UI/MCP by SPEC-0206.
No package, lint configuration, audit threshold, workflow or archive body is
changed. The earlier braces hold is not withdrawn by a request to integrate.

At protected main `7f939ae802afc1d23f96b8eca4100abfcc2bf629`, the tracked
lockfile contains the dev-only path `eslint-config-next@16.3.8 →
@next/eslint-plugin-next@16.3.8 → fast-glob@3.3.1 → micromatch@4.0.8 →
braces@3.0.3`. Only micromatch directly declares braces in this lockfile.
The ESLint configuration imports both Next core-web-vitals and TypeScript
presets. Removing Storybook alone leaves that Next lint dependency in place.
This is a source-graph finding, not a claim that static assets expose braces.

Read-only official registry JSON queries exited 0 on 2026-10-04: stable
`storybook` is 10.6.1, `eslint-config-next` and `@next/eslint-plugin-next` are
16.3.8, and braces is 3.0.3. The latest Next plugin still declares fast-glob
3.3.1. The [official advisory](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm)
reports affected braces through 3.0.3 with no patched release. Therefore a
supported stable upgrade that removes this path was not found. A handwritten
fork, package alias, lint-rule removal or production-only audit would require
new validation and would not satisfy the existing complete high/critical
check. None is applied or reported as an immediate solution.

| Candidate | Official functional basis and current registry tag | Replacement limits and security finding | Disposition |
| --- | --- | --- | --- |
| Keep Storybook | Existing 10.6.1 source, package exports, isolated static/browser receipts, revision manifests and local documentation MCP | Keep failed audit visible; wait for a patched braces release or upstream Next lint dependency replacement proven with the current rules | Preferred current architecture; merge remains blocked |
| Ladle | [React/Vite workshop](https://ladle.dev/docs/), [static build CLI](https://ladle.dev/docs/cli/) and [meta.json](https://ladle.dev/docs/meta/); @ladle/react latest 5.1.1, MIT, React peer >=18, Vite ^6.0.5 | Declares globby ^14.0.2; compatible globby14.1.0 declares fast-glob ^3.3.3, which declares micromatch ^4.0.8 and hence braces ^3.0.3. meta.json is not the current components/docs manifest contract. React19/Vite8, Next mocks, stories/addons, coverage and MCP need a separate consumer trial | First functional alternative to evaluate after product/contract approval; not a demonstrated audit fix |
| React Styleguidist | [React component documentation/playground](https://react-styleguidist.js.org/); latest13.1.4, MIT, React peer >=18 | Different Markdown/webpack contract; declares react-dev-utils ^12.0.0, whose compatible12.0.1 declares globby ^11.0.4; globby11.1.0 declares fast-glob ^3.2.9. Current story/MCP/test contracts require migration | Secondary documentation alternative; no security-clean graph claimed |
| Histoire | [Official Vite playground](https://histoire.dev/) lists Vue/Svelte; npm latest is1.0.0-beta.1, MIT | No official current React replacement was established; that beta directly declares micromatch ^4.0.8 and is not a stable candidate | Reject for this React workspace |

Candidate dependency paths are declared-range evidence from official registry
metadata, not installed lockfiles or complete security audits. No replacement
was installed, built, benchmarked or connected to HOME. Free self-hosting and
MIT upstream licenses do not grant a distribution license to the existing
private UNLICENSED UI package. Existing Traefik origin/auth/network contracts
would be preserved by an approved alternative; no second gateway is proposed.

Main integration must pass the required protected check before disposition.
PR353 run37162825263 and PR354 run37163965061 have failed required
validation-changed checks while the independent braces hold remains unresolved.
Sanitized `gh run view --log-failed` readbacks report the braces advisory and
five high findings; PR354 metadata selected6/violations0 and corpus/archive
recovery violations0. PR355 run37164906030 also failed, with metadata
selected1/violations0 and corpus/archive recovery violations0 before the same
five-high audit result. These observed failures are not converted into PASS.
PR352 is already merged; PR351 was closed without merge. Closed PR351's
recovery commit `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` preserves14
completed members for SPEC-0201/0202/0203/0205. Their frozen bodies are not
rewritten or presented as completed current-main packages. Once the security
hold clears, deliver the remaining registered protected lifecycle edges,
reconcile the divergent current SPEC-0205 through the existing immutable
handoff contract, integrate source, then prioritize those four whole-package
archives. SPEC-0182 recovery/offline custody, SPEC-0193 live resource/alert
acceptance, SPEC-0204 exact-image synthetic acceptance and SPEC-0206 HOME
TLS/OIDC remain separate uncompleted conditions; never archive individual
completed Tasks from their unfinished packages.

The inspected source inputs were only tracked JSON/ESLint/gate declarations
and public vendor metadata. Output is this assessment and a prioritized
handoff; no runtime, secret or data operation occurred. Rollback is a scoped
documentation revert preserving source recovery commits. Focused metadata `check-document-metadata.py --mode check-changed --base-ref
origin/main --changed-path` on this Task exited0, selected1/violations0/legacy0/
overrides0. Markdownlint-cli2 0.22.1 and `git diff --check` exited0. A Python
comparison proved only the dated research receipt and patch version changed,
exit0; the existing body, lifecycle and acceptance entries are preserved.
Independent review requested precise CI-failure evidence wording, corrected
above; final independent policy/document review returned PASS. Candidate install,
consumer/build/audit, HOME changes and data migration are NOT_RUN.

### OpenDesign assessment — 2026-10-04

The user's named candidate is assessed as [nexu-io/open-design](https://github.com/nexu-io/open-design),
not the separate opendesign.cc design-system catalog or similarly named forks.
Authenticated public-source readback exited0 at main revision
`53231d40b778d88eba23f35547bf99485d3ae9fc`; latest release is
`open-design-v0.24.1` while that source manifest declares 0.23.1. These are
separate artifacts, not a verified runtime pin. Upstream Apache-2.0 permits
self-hosting; BYOK/provider or cloud usage is not thereby free, and imported
brand assets keep their own rights.

Official source describes design/prototype generation, design-system files,
export and Codex/Claude adapters. It is a Claude Design workflow candidate,
not a demonstrated replacement for existing Storybook component interaction,
accessibility/coverage, package consumer and revision-manifest acceptance.
The inspected [live-artifacts MCP source](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/apps/daemon/src/mcp-live-artifacts-server.ts)
exposes create/update/refresh as well as list and connector tools; this is not
the currently approved shared read-only documentation toolset. A supported
read-only subset with audience/reader authorization is not established here.

[Deployment documentation](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/deploy/README.md)
explicitly distinguishes its single-tenant bearer token from per-user access
control. [Adapter documentation](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/docs/agent-adapters.md)
uses non-interactive permission modes, including Claude bypassPermissions;
therefore a preview sandbox is not proof that the agent cannot write or run
code. [Privacy documentation](https://github.com/nexu-io/open-design/blob/53231d40b778d88eba23f35547bf99485d3ae9fc/PRIVACY.md)
describes product analytics enabled by default and separately configured
safety/reliability telemetry not disabled by the general toggle. Local-first
must not be reported as offline or zero outbound data.

Recommendation: keep Storybook's approved package/testing/docs contract;
evaluate OpenDesign only as a separate design-workflow companion using
approved UI tokens and synthetic screens in an isolated external workspace.
Before any trial, review exact release/dependency audit, model destinations,
telemetry configuration, file-write/command authority and the client config
changes. No installer, agent credential import, global MCP registration,
Docker service, model request, repo upload or HOME activation was performed.
Replacing the design tool does not remove the current Next ESLint/braces
path. Main integration and whole-package archival still require the earlier
protected prerequisites and terminal completion evidence; they are not
unblocked by this candidate research. This Task's focused metadata check
exited0, selected1/violations0/legacy0/overrides0; Markdownlint-cli2 0.22.1,
`git diff --check` and exact prior-body preservation comparison exited0.
Independent read-only source/policy review returned PASS. The preceding PR354
head `ed2600286e12d16349345f080244c6966321f273` run37165579521 failed:
metadata selected6/violations0 and corpus violations0, followed by five high
braces findings in sanitized diagnostics. This does not prove the new head's
hosted result. Actual candidate execution remains NOT_RUN.

### Lint substitution and temporary exception proposal — 2026-10-04

The user asked whether removing eslint-config-next in favor of
eslint-plugin-storybook or governing a temporary exception is possible.
This receipt is a reviewed proposal, not approval to alter rules or risk
acceptance. Existing patch-before-merge approval remains binding.

Storybook 10.6.1's [official flat recommended configuration](https://github.com/storybookjs/storybook/blob/v10.6.1/code/lib/eslint-plugin/src/configs/flat/recommended.ts)
limits its rules to stories and .storybook/main; it is already registered in
the current eslint.config.mjs. It supplies neither the current TypeScript
parser/rules nor Next/React/Hooks/accessibility coverage. Actual Next pages
remain in src/pages. The [Next configuration contract](https://nextjs.org/docs/app/api-reference/config/eslint)
separately owns those presets. Current lockfile inspection found only
@next/eslint-plugin-next directly depending on fast-glob. Removing that chain
is a plausible graph change, but retaining the Next plugin directly retains
braces; adding Storybook's already-present plugin alone is not equivalent.
A source redesign would need explicit rule coverage mapping, negative TS,
React/Hooks/a11y/Next fixtures, existing builds/browser coverage and a clean
resolved audit. No lint rule is disabled as this investigation's result.

A narrowly approved temporary risk acceptance is technically possible while
keeping the required validation-changed gate, but current npm audit admission
has no exception consumer. The documentation literal exception contract and
infra hardening exceptions do not authorize dependency-security exclusions.
Do not use continue-on-error, SKIP, omit-dev as the only audit, audit-level
critical, return0 for any audit failure or a blanket package allowlist.

Proposed bounded contract, pending owner approval:

- Accept only GHSA-vfj7-8cjw-p6xm/CVE-2026-93687 for dev-only braces3.0.3
  through the exact Next ESLint chain in this workspace. All five derived
  npm findings must terminate only in that advisory; names alone never grant
  an exception. Preserve the raw audit exit/result as FAIL and report accepted
  risk separately, not zero vulnerabilities or a repaired package.
- Owner @buenhyden; expires at 2026-10-11 00:00:00 KST (2026-10-10T15:00:00Z),
  with no automatic extension. Review earlier if a supported patch appears.
- Fail closed on malformed/missing audit data, tool/network/advisory lookup
  failure, changed path/version, any other high/critical, production finding,
  expiry, or a published patch until removal/update is verified. Run complete
  and production audits; production-only success is insufficient.
- Exit condition: remove acceptance when a supported patched dependency or
  equivalent lint redesign passes full audit and existing source checks.
  The accepted risk is development/CI denial of service from nested patterns,
  not a claim that dev dependencies are harmless.
- Source owner would be amended SPEC-0205 Spec/Plan/Task1. Proposed exact writer
  paths are those three package documents, .agents/governance/quality-standards.md,
  .github/workflow-contract.yml, scripts/lib/gate/ci_gate_contract.py,
  scripts/lib/gate/ci_gate_adapters.py, tests/lib/gate/test_ci_gate_contract.py
  and tests/lib/gate/test_ci_gate_adapters.py. Reuse the current contract and
  adapter; add no independent workflow, generic exception framework or main
  protection change. Register the bounded metadata in the current machine
  contract. A failing test needing another file requires a scoped amendment.
- Before implementation, owner must approve replacing the prior patch-only
  hold with this precise risk contract, amended documents and policy/source
  scope; independent rules/security review and negative fixtures are required.
  Revert the approved policy/adapter receipt to restore strict failure, never
  bypass protection to land either the acceptance or subsequent archives.

Recommendation: preserve Next lint coverage. If protected delivery is now
more urgent than the previous patch wait, seek the above explicit, expiring
risk approval; otherwise keep the hold. No acceptance or dependency removal
is applied here. OpenDesign remains a separate design companion candidate,
not a solution to this lint dependency. Candidate execution and policy/audit
implementation are NOT_RUN. Focused validation: metadata check-changed
selected=1, violations=0 (exit 0); Markdownlint CLI2 0.22.1 (exit 0);
`git diff --check` (exit 0); preceding receipt preservation check (exit 0).
Independent proposal/security/lifecycle review: PASS. Staged classifier:
markdown=1, generated=0; no source or gate change.

### Protected review edge — 2026-10-04

Protected `origin/main` now contains PR352 at
`7f939ae802afc1d23f96b8eca4100abfcc2bf629`, registering all six draft
members. The preceding gate and hold receipts remain dated evidence; their
unmerged PR352 descriptions are historical. The owner closed PR351 without
merging its source. The latest owner request keeps braces on hold and asks
for the remaining Spec/Plan/Task work to proceed.

Existing Prompt 04 design/package/Plan/Task source approvals are carried
forward for this source-only lifecycle edge: Spec draft→review, Plan
draft→approved, Tasks1–4 draft→ready. Only these six package documents
change. No implementation completion, hosted gate waiver, source merge,
image pull, HOME action, secret operation or deployment is approved or
reported by this edge. Runtime checks remain NOT_RUN. A later source
integration must separately reconcile the closed PR351's preserved work;
this receipt does not reopen it or discard its recovery objects.

Local `check-document-metadata.py --mode check-changed --base-ref origin/main`
selected6/violations0/legacy0/overrides0 against the protected baseline above.
Cached installed markdownlint-cli2 0.22.1 and `git diff --check` returned exit0;
all six original bodies are preserved apart from this dated Task1 receipt.
The first formatter attempt used its cache source entrypoint and exited1 for
missing `globby`; the installed package entrypoint resolves that environment
issue without modifying tools or rules. Independent read-only review returned
PASS; hosted checks remain pending for this edge. Domain tests and container
execution are N/A for this edge.

The separate backlog PR353 head `7cfd890dbcd4b262a39ada1b45b5efc51ca332da`
ran hosted CI `37162825263`: metadata selected8/violations0, operations catalog
PASS and formatting hooks PASS, but the gate exited1 with five high findings
under `GHSA-vfj7-8cjw-p6xm`. The owner's braces hold remains; this document
edge adds no security exception and does not merge that PR.

### Protected registration repair — 2026-10-04

### Required gate result and existing security hold — 2026-10-04

PR352 head `0ef17a4a58d0d53f7249f3b0eef7939457e5cb72`, hosted
run `37158568358`, finished failure/exit1. Metadata selected2/violations0/
legacy0/overrides0; the approved fixture and both pinned formatters passed.
The later npm audit reported five high findings in the dependency graph,
including `GHSA-vfj7-8cjw-p6xm`. This is an independent security block,
not a recurrence of the missing fixture or document registration finding.

Authenticated GitHub advisory readback on 2026-10-04 confirms braces
`<= 3.0.3`, severity high, first_patched_version null; official source:
[GitHub Advisory Database](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).
The owner previously chose to wait for a patch rather than grant a security
exception. That decision remains binding. No security exception, dependency
substitution, threshold reduction, manual workflow rerun or protected merge
is authorized by this receipt. No further hosted execution is dispatched.

The registration candidate's metadata has zero findings, but PR352 is not
merged. The original closure PR351 has not received the three protected
prerequisites and is not claimed repaired or merge-ready. The reviewed next
six-document edge remains uncommitted in its owned review worktree. Existing
source and recovery objects remain on their named branches; do not delete
those branches or dirty pending worktrees. Local main and origin/main were
last observed equal at `0460795abf6da9203e38f30291a8f20118c6ab88`.
Resume normal protected delivery only after the approved security hold clears.
HOME/isolated execution/data migration remain NOT_RUN for this repair.

### Pinned Python formatter scope amendment — 2026-10-04

PR352 head `a959826519c77402133bb197c7335747faa3e9bf`, required
run `37156755186`, finished failure/exit1. Metadata selected2/violations0/
legacy0/overrides0 and the markdownlint hook passed. The next ruff-format
hook modified one file and stopped the job; later leaves remain unverified.
Local Ruff 0.16.10 had accepted the approved fixture, but the CI hook pins
0.15.12. The pinned formatter accepts the approved fixture unchanged. Its
read-only check of 152 tracked Python files identifies only the existing
`tests/validation/test_compose_baseline_gates.py` from protected main PR350.

The four-hunk proposal changes only line wrapping, has identical Python AST,
and is idempotent under pinned Ruff 0.15.12. Independent read-only review
returned PASS on neutrality and required exact-path scope approval. The owner
explicitly approved those four formatting hunks and this Task1 record on
2026-10-04. The amended writer ledger adds only that one test file. Applying
pinned formatting modifies those same four hunks; no assertion, validation
condition, threshold, workflow or runtime behavior changes. Revert this
format-only commit for recovery, preserving all prior objects. Required
hosted CI must still pass before protected registration and later edges.

### Hosted fixture validation and document formatting — 2026-10-04

PR352 head `042b9db6d6e86025fc94af8105a18c63440ba071`, required
run `37154950211`, job `111296335212`, finished failure/exit1. Hosted
metadata selected2/violations0/legacy0/overrides0; corpus and archive recovery
violations0. The existing Storybook fixture test passed, retaining all five
negative mutations. The later pinned markdownlint-cli2 hook modified files
and stopped the required job; no later leaf is claimed PASS.

The exact approved Task1 document contained two redundant blank lines.
Direct invocation of cached, pinned markdownlint-cli2 0.22.1 on this one
approved document removed only those two blank lines and returned exit0.
This formatter reconciliation changes no source, fixture assertions,
threshold, workflow, lifecycle edge or frozen archive. Recheck formatting
idempotence, metadata and exact diff before the normal hosted retry. The
fixture implementation itself needs no second correction. Runtime holds
remain unchanged. Raw CI output was not copied into this record; an automatic
approval rejection of raw log printing was honored with bounded diagnostic
extraction of checker results and hook identity.

### Additional fixture scope proposal — 2026-10-04

PR352 head `b240f6150` hosted run `37154044478` returned failure, but
metadata selected2/violations0/overrides0 and links/corpus/recovery passed.
The five failures are the existing Storybook shell regression's baseline
fixture: main0460795's checker also reads `.storybook/main.ts` and the private
UI `package.json`, while the test copied only package.json/vitest.config.ts.
No initial-state finding remains in this registration candidate.

Proposed additional writer is only
`tests/lib/gate/test_github_workflow_contract.py`'s existing Storybook fixture
copy loop: add those two tracked configuration files and create their parent
directories before copying. Preserve all five mutation assertions, thresholds,
checker code, workflow routing and required protection. Exact proposed patch
is staged outside the repository as `/tmp/hyhome-storybook-fixture-proposed.patch`;
the tracked test was unchanged during scope review.
Existing targeted unittest reproduced RED exit1/five failed subcases. Loading
the proposed test source from scratch with the original repository ROOT
returned GREEN exit0/one test covering all five subcases. An initial scratch
loader exited1 because its temporary file depth could not resolve ROOT;
keeping the real repository `__file__` fixes the loader without altering the
proposed test or its assertions. The exact targeted regression and normal
hosted checks must run after approved application. Independent read-only
patch review returned PASS: only fixture completeness changes, all original
negative assertions and checker semantics remain intact. The user approved the exact fixture minimum and Task1 record on 2026-10-04.
`git apply` of the reviewed patch exited0. The same targeted existing unittest
then passed exit0/one test with all five original mutation cases; Ruff check,
Ruff format --check and git diff --check each exited0. No checker or threshold
changed. The scope now includes that single fixture loop in
`tests/lib/gate/test_github_workflow_contract.py` in addition to this Task record.

The package's exact-file approval rule was satisfied by that explicit owner
response. Push the scoped fixture and record to PR352, observe the normal
hosted gate, then resume the reviewed document sequence only after green.
Rollback is a scoped revert of the fixture addition, which returns the known
missing-input failure; it is not a gate bypass or an operational rollback.

The user requested resolution of PR351's six initial-status findings after
explicitly authorizing push, PR merge and cleanup. Original implementation
and completed evidence remain on `codex/spec-0201-0205-closure` at
`451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7`; no final body or frozen
archive is rewound by this document registration.

Initial preparation used `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`
and six original draft bodies (five from `0f67cb297`, Task4 from `d666b6f42`).
Local metadata selected7/violations0/overrides0, links failures0 with one
pre-existing historical warning, and corpus/recovery violations0, each exit0;
independent review approved. The first counter relationship check failed
before correcting high_water and next_number together. Draft commit
`86f65973a6a762952e004994fb5e860d2b7dca8c` remains recoverable.

Authenticated PR readback then exposed concurrent protected main
`0460795abf6da9203e38f30291a8f20118c6ab88` from PR350, which already
registers Spec, Plan and Tasks1-3 as draft. No obsolete registration was
merged. The registration branch merges this latest main and preserves its
Storybook changes, navigation and SPEC high-water206/next207 exactly.
PR352 now adds only the missing original Task4 draft and this Task1 receipt.
Independent review approved the narrowed two-document diff; README and Registry
match the new main exactly. A check before finishing the main merge exited2:
allocation predecessor 0460795 did not yet precede branch HEAD. The normal
merge commit establishes that ancestry; validation must rerun afterward.
After normal main merge `21bf46fdd`, changed metadata against origin/main
0460795 selected2/violations0/overrides0, exit0. Refreshed links mode all
returned failures0/one pre-existing historical warning, exit0; corpus and
archive recovery returned violations0, exit0. `git diff --cached --check`
passed and independent review approved the exact two-document diff.
Registration document scope covers these two package documents; the approved
fixture-loop extension is recorded above. Final independent review approved
this exact three-file PR diff with zero standards/spec findings; normal hosted
checks still decide merge readiness. No runtime,
private values, validator, lifecycle registry rule or transition override changes.

Use three preliminary docs-only protected merges: finish Task4 draft
registration; Spec draft→review, Plan draft→approved and all Tasks draft→ready;
then Spec review→approved, Plan approved→active and Tasks ready→in-progress.
Merge that main into the closure branch without rewriting recovery objects.
PR351 then supplies the fourth edge and final reviewed bodies: Spec active,
Task1 blocked, Tasks2-4 completed, Plan stays active. Every merge requires
normal green protection. PR351's independent security hold remains unchanged;
this registration does not approve HOME, image pulls or service execution.
Rollback is a scoped PR revert with original sources preserved, never archive
rewriting or cancellation of already-completed work.

| Check | Result | Limit |
| --- | --- | --- |
| Historical tracked-source and official-doc comparison | READ_ONLY | n8n version/timeout mismatch and Crawl4AI later advisory confirmed at draft time; no image execution |
| Draft package: `check-document-metadata.py --mode check-changed --base-ref main` | PASS (exit 0, selected 6, violations 0) | Documents only; no service validation |
| Draft package: `check-document-links.py --mode all` | PASS (exit 0, failures 0) | One pre-existing archive provenance warning |
| Draft package: `check-document-corpus-lifecycle.py --base-ref main`; registry JSON parse; `git diff --cached --check` | PASS (each exit 0) | Draft lifecycle and syntax only |
| Current source static/synthetic checks | SOURCE_STATIC PASS; synthetic shell guard PASS / exact-image BLOCKED | n8n/source guards, OpenBao sealed readiness and LAB static checks exist; crawler egress deny, Agent renewal freshness and Cassandra auth remain blocked as stated below |
| HOME n8n DB upgrade, crawler request, OpenBao unseal or service restart | NOT_RUN | Separate exact operational approval required |

| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |
| --- | --- | --- | --- | --- |
| 1 | W1 | in-progress | SOURCE_STATIC PASS; runtime evidence remains pending. | [Task receipt](#verification-evidence) |
| 1 | W5 | blocked | Runtime evidence remains pending. | [Task receipt](#verification-evidence) |
| 2 | W2 | blocked | SOURCE_STATIC PASS and synthetic shell guard PASS; exact-image and Code-task runtime are BLOCKED. | [RUN-0053](../../../05.operations/runbooks/0053-n8n.md) |
| 2 | W5 | blocked | Exact-image and Code-task runtime are BLOCKED. | [RUN-0053](../../../05.operations/runbooks/0053-n8n.md) |
| 3 | W2 | blocked | Crawl4AI egress-deny runtime is blocked and Cassandra authentication is absent by contract. | [RUN-0091](../../../05.operations/runbooks/0091-crawl4ai.md) |
| 3 | W5 | blocked | Crawl4AI egress-deny runtime remains blocked. | [RUN-0091](../../../05.operations/runbooks/0091-crawl4ai.md) |
| 4 | W2 | blocked | Agent-renewal freshness runtime remains blocked. | [RUN-0085](../../../05.operations/runbooks/0085-openbao.md) |
| 4 | W5 | blocked | Agent-renewal freshness and route acceptance remain blocked. | [POL-0079](../../../05.operations/policies/0079-application-auth-integration.md) |
| 8 | W1 | in-progress | Current W1 source checks and review are pending. This avoids duplicating completed Task 0002's criterion 8/W5 receipt; its HOME, runtime, and migration limits remain historical Task 0002 facts. | [Plan W1](../plan.md#execution-sequence); [Task 0002 receipt](tsk-0002-external-project-integration.md#verification-evidence) |

## Review Evidence

Independent source/security review returned PASS for the approved source and document reconciliation recorded below. Runtime and HOME conditions remain pending unless explicitly marked by later exact operational evidence.

## Commit Ledger

Prompt 04 source reconciliation merged through PR359 at `467bd644b071f9dfa02ca1af2d622502c3445d28`; completion receipts merged through PR360 at `ebeb83521c768fedc620380b0c2e92db10a6fcdc`. Earlier “No Prompt 04 commit” wording is historical for the draft phase. This receipt authorizes no HOME operation, restore, image pull, authentication change or private read.

## Rulings

Do not shrink main runners without path evidence. Do not use a generic `_FILE`
assumption for `n8nio/runners`; verify its entrypoint first. If the pinned
runner lacks a safe supported file-consumption path, stop and amend this Task
with the exact wrapper/Dockerfile path before writing one. Existing LAB
Cassandra work is a verification item, not a repeat implementation.

## Deferred Items

### Approved combined protected delivery

The owner authorized commit, push and protected main integration for the
listed SPEC backlog. Read-only policy review found no per-Task PR requirement.
PR #354 carries independently approved changes through ordinary merge commits:
its review-edge head 05a06902af7bd6a3a2f467f2bccdd6600525f2b6,
PR #353 head 14d890700085a38e6c62d0bd2f4cbd008bc18daa, and corrected
PR #355 head 61f0a5c2354a84db77c10a8c809f6070f4f1ac24. All original source
and recovery objects remain ancestors; no rebase, squash or history rewrite.
The observed protected base is bf4b84edffcd8a8ec4a7da27c4b02dbdee9017bd.

The bounded diff contains seventeen files: six SPEC-0204 documents, eight
SPEC-0182/0193 and current-inventory documents, two existing Airflow/Prometheus
configurations, and one SPEC-0206 delivery Task. Each original Task owns its
criteria and evidence. SPEC-0204 advances only Spec draft to review, Plan to
approved and Tasks to ready; subsequent approved/active edges remain separate.
This delivery adds no Prompt 04 runtime execution or new source implementation.

Before-state checks on the constituent heads passed: changed metadata selected
six, eight and one documents respectively, with zero violations/overrides.
PR #353 operations catalog, five ObservabilityDashboardContractTests and public
workflow-airflow Compose render each exited 0; traceability exited 0 and
alignment retained only the existing archive legacy warning. Independent review
passed all constituent diffs after the single SPEC-0206 historical-wording
correction. These receipts do not substitute for aggregate-head checks or CI.

The next command classes are focused aggregate validation, independent review,
feature-branch push, comprehensive PR summary and normal protected merge after
required checks pass. Read-back protection requires strict validation-changed,
zero approving reviews and no enforced CODEOWNER review. No direct main push,
bypass, new risk acceptance or HOME action is authorized by this combination.
After merge, verify the constituent heads are protected-main ancestors before
reporting their delivery; do not infer a separate PR close or branch deletion.
Recovery is a reviewed follow-up correction or scoped revert preserving original
history. Main synchronization is fast-forward only; other workers' state stays
untouched. Aggregate required CI and protected delivery remain pending.

Aggregate local verification on bc7016a9e7259d5f5cd609a9ab2273a275566481
plus this Task receipt: check-document-metadata.py --mode check-changed
--base-ref origin/main selected 15 documents, zero violations/overrides,
exit 0. check-operations-catalog.py passed (exit 0). The five existing
ObservabilityDashboardContractTests passed (exit 0). docker compose --env-file
.env.example --profile workflow-airflow config --quiet passed (exit 0), without
service execution. MarkdownCLI 0.22.1 and git diff --check origin/main passed
(exit 0). git merge-base --is-ancestor for each of the three constituent heads
against HEAD exited 0. Independent exact aggregate review returned PASS,
conditional on recording these completed checks; this paragraph closes that
condition. Final receipt metadata/Markdown checks and required hosted CI still
remain separate from these prior results. No new runtime evidence is claimed.

Task source approval, image/digest acceptance, synthetic container preflight,
HOME version upgrade, management DB/encryption-key backup, real credential
handling and all service operations remain separate.

Protected delivery continuation, 2026-10-04. PR356 merged as
bf4b84edffcd8a8ec4a7da27c4b02dbdee9017bd after required run37174055840
passed. Its merged main-security and channel-tag run37175100677 passed.
PR354 aggregate head5821e257324815acfd2cf08b1bf4c277f5e7546d passed required
run37176029838 and merged as7209cde8b0a2bb18e9d2b7779fca29bb4528844b;
main-security/channel run37176771913 passed. PR353 and PR355 were automatically
reported MERGED and their original heads were verified as main ancestors.
Four independently reviewed clean owned temporary worktrees were removed;
all branch references, the old dirty review worktree and pending work remain.

PR357 delivered only Spec review to approved as
0e792cdff4e13b17af0e514b5519c56c501f04d8, after required run37176990885
and CodeQL passed on dab35a5a2886fddf845e6f7e5b54b27fe950cbdb. The user’s
existing design, written Spec, Plan and execution approvals continue to govern.
This next edge advances Spec/Plan approved to active and ready Tasks to
in-progress without source, runtime or private-state implementation. Source
closure and eligible packet preservation require a fresh exact writer ledger,
actual protected base, focused validation and separate required hosted delivery.
These observed receipts replace previous pending delivery descriptions only;
no historical failure is converted to PASS and no HOME proof is inferred.

### Source reintegration and historical acceptance transfer — 2026-10-04

Normal merge `2de9cd69ad6e2b04d11202ba8f98a0a09f7f9ccb` retains closure
`451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` source commits and frozen records. Task1 source receipt at `a51014aab597cd95bf5db19f00348e1d487ce642`
records n8n2.41.6 matching server/runners, timeout and selected-secret guards;
Crawl4AI0.9.4 security pin; OpenBao2.6.2 sealed readiness; Cassandra LAB render.
Historical 58 static/shell tests and public Compose renders exited0; this is
not a new container or HOME acceptance. Fresh combined source checks follow.
Criteria1/8 map W1/W5 to current source/projections/review; criterion2 maps W2
to n8n sources and GDE/POL/RUN0053; criterion3 maps W2 to Crawl4AI0091/Cassandra
LAB; criterion4 maps W2 to OpenBao0085. Exact-image Code-secret denial, crawler
host/LAN/metadata egress, Agent renewal/freshness and Cassandra auth/data remain
NOT_RUN. Closure's BLOCKED_IMAGE_NOT_AVAILABLE finding is historical; no pull,
image-cache or runtime preflight was repeated here. Existing private-file
move/parity receipts in Task4 remain historical; no new private inspection.

The newer SPEC0205 bounded audit, prepare hook and compatibility registrations
were actually delivered by PR356; canonical policy/contract/adapter owners keep
the exact GHSA path, expiry and fail-closed checks. Frozen completed0205 proves
dependency refresh only. The four current packets are preserved raw through
typed receipts; superseded records are historical input, not runtime authority.

Historical protected QA remains: workflow/secret/gate153 PASS; runtime/project/quality/version118 PASS; DB/Valkey/Influx/LAB35 PASS; baseline94 PASS (21 optional Docker skips); SurfaceOwnership11 PASS; exact backup failure harness1 PASS after check=False. All commands used `python3 -m unittest` with named registered modules; exit0.
Ruff0.15.12 changed21 lint/format (AST-equal formatting/import cleanup), loop binding fixture11 PASS, shell/root render and workflow/version/catalog exited0. Inventory boundary-wrapper failure was corrected; capture POSIX-mode preflight rejected harmless umask, then Git mode/blob/member check was corrected and reviewed. Authored Markdown52, corpus/archive341 and changed metadata77 passed:0 violations, exit0.
Latest fresh source check: 24 tests across four unittest modules/classes passed for RuntimeCompatibility, ObservabilityDashboard, BackupContract and RouteAuth; n8n/Crawl4AI root public render, LAB Cassandra render and version92 check each exited0; no Docker exec/run occurred. Links0 failures/1 legacy warning; prior7 routing/pin findings corrected. PR359 delivery `467bd644b071f9dfa02ca1af2d622502c3445d28` required CI run37180461557 PASS; parity `exit0, files_changed=0, values=preserved, secret_files=untouched`. PR360 completion receipts merged as `ebeb83521c768fedc620380b0c2e92db10a6fcdc`.
Final current preflight reconciliation, 2026-10-04: default local Unix socket inspection found only cached `openbao/openbao:2.6.2` image ID `11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641`; exact declared `hyhome/n8n:2.41.6-local`, `n8nio/runners:2.41.6`, `unclecode/crawl4ai:0.9.4` and `cassandra:5.0.9` were missing from cache. No image pull, container run, HOME start, restore, authentication change, private read or secret issue was performed.
Remaining genuine source/runtime gaps are crawler private/link-local/metadata egress-deny runtime enforcement, OpenBao Agent renewal and rendered secret freshness, and Cassandra authentication absent by explicit LAB contract, not merely unobserved.

### Approved current source reconciliation — 2026-10-04

The owner approved the four-package plan, commit/push/protected merge and eligible branch cleanup. Exact writers are this Task, this package Plan, and existing `tests/validation/test_service_runtime_compatibility.py`; the latter tests Crawl4AI missing/empty/15-character rejection, 16-character acceptance and output/argv non-disclosure using the actual Compose command with synthetic files and a stub launcher. No production command, image or secret reference changes. A minimum-length-guard mutation must be rejected; existing n8n/OpenBao/LAB guards are reused. Baseline runtime module 6 PASS/exit0; minimum-length-guard mutation RED rejected 2 invalid inputs/exit1; current module 7 PASS/exit0 and combined runtime/observability/backup/route suite 25 PASS/exit0. Pinned Ruff0.15.12 lint/format and diff checks exit0. Independent test/security and source/lifecycle reviews PASS. Changed metadata14/corpus/archive recovery/links (one legacy provenance warning)/Markdown14/diff gates exited0; final receipt/parent checks are repeated before commit. Container/HOME/restore/migration remain NOT_RUN.
SPEC-0206 source/static completion and archival are separately approved; its HOME TLS/OIDC/session and remote-MCP follow-ups remain with POL/RUN-0101. This replaces the earlier current package-blocker interpretation, not historical failures or execution receipts. Rollback is a scoped source/doc revert, never frozen-archive rewriting.

Protected completion PR361 merged as `275d708ab797e0c86a30508351666482ebc04907`: required CI run37186133788, CodeQL and GitGuardian PASS; main-security/channel run37187599350 PASS. Approved archive writers are the exact seven source deletions/raw copies for completed0193 (3 members) and completed0206 (4), `docs/03.specs/README.md`, `docs/98.archive/retention-catalog.md` and this receipt. Independent pre-unlink review verified source Git blobs/modes/member sets and unchanged existing catalog rows; catalog records that protected source SHA. Current consumers were promoted by PR361 to Stage05; frozen bodies remain unchanged. Empty source directories caused an initial lifecycle/metadata failure and were removed with exact rmdir; final gates follow in the archive PR. Links PASS/exit0 with the existing 2870 legacy-source warning; no operational authority, HOME action, image pull, secret change, restore or migration is granted by capture.
Final archive pre-commit acceptance: metadata3 violations0, corpus violations0/preserved348, links failures0/one existing warning, authored Markdown3 and diff checks all exit0; independent final cutover/raw-object review PASS. Required archive PR CI remains a separate delivery gate.
