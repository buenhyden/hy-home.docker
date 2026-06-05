---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-06-04-docs-implementation-audit.md -->

# Task: docs/01-05 Content-vs-Implementation Audit

## Overview (KR)

이 문서는 `docs/01.requirements`~`docs/05.operations`의 **작성된 내용**을
tracked `infra/**` 구현과 의미 단위로 대조한 감사 리포트다. 판정 기준은 링크/거버넌스/체인
검증 통과가 아니라 "문서 내용 vs 현재 구현" 일치 여부다. 본 리포트는 Phase B(아카이브/수정)
실행 및 검증 evidence이며, cross-cutting 거버넌스 작업으로 parent Spec 대신 거버넌스 문서를
참조한다(`documentation-protocol.md` §8.5).

## Inputs

- **Plan**: 승인된 plan-mode 계획 (docs/01-05 content-vs-implementation reconciliation)
- **Implementation SoT**: tracked `infra/**` (compose, configs, scripts, `infra/tech-stack.versions.json`)
- **Existing signals**: `scripts/validation/check-doc-implementation-alignment.sh`, `docs/98.archive/README.md` ledger

## Working Rules

- 기준은 콘텐츠 vs 구현. 자동 체크 통과는 필요조건일 뿐 성공 기준이 아니다.
- 정확히-완료된 문서를 인위적으로 아카이브 후보로 부풀리지 않는다(정직 보고).
- 파괴적 조치(아카이브/삭제)는 현재 구현과 상충하는 whole-document evidence가 확인될 때만 실행한다.

## Methodology & Coverage

- **Structural mapping (100%)**: Stage 01-05 문서를 stage/tier/service로 인벤토리하고 40개
  compose-bearing implementation root, tier-level compose 서비스 문서, 거버넌스 표면에 매핑.
- **Deep content read**: 후보군(03 프로세스 스펙, 04 stale active 플랜, 05 draft) + tier 대표 샘플.
- **Signal scans**: frontmatter status 분포, legacy/deprecated 용어, operations↔infra 커버리지.
- **한계**: 모든 Stage 01-05 문서의 1:1 전수 정독은 수행하지 않음. 아래 "Open decision"에서 심층
  전수 패스 여부를 확인한다.

## Key Finding

2026-06-02 reconciliation이 **구현과 총체적으로 충돌하는 문서를 이미 아카이브**했다(Airbyte
미구현, Codex Markdown/HADS 상충 등). 이번 pass에서는 추가로 `05-messaging`의 misplaced ksqlDB
guide, `07-workflow`의 duplicate Airflow DAG guide, `08-ai`의 duplicate Ollama setup/inference guides,
`09-tooling`의 duplicate IaC automation guide를
archive tombstone으로 이동했다. 나머지 실질 드리프트는 대부분 구현된 서비스 문서의 current-truth
mismatch, frontmatter status metadata, 완료된 일회성 프로세스 문서의 라이프사이클 처리다.

## Verdict Summary (by stage)

| Stage           | Docs | KEEP (matches impl)                    | FIX (status/content)                       | ARCHIVE candidate   | Notes                                                                         |
| --------------- | ---- | -------------------------------------- | ------------------------------------------ | ------------------- | ----------------------------------------------------------------------------- |
| 01.requirements | 25   | 25 active                              | 23 (status: draft→active)                  | 0                   | tier PRD 23건은 tracked 구현 surface가 있어 active requirements로 유지        |
| 02.architecture | 51   | 51                                     | 0                                          | 0                   | ADR/ARD 전부 현 infra 매핑(traefik/keycloak/vault/kafka/patroni/lgtm 등 실재) |
| 03.specs        | 43   | 15 active / 9 completed / 19 README-like missing status | 7 프로세스 스펙(status active→completed) | 0                   | tier specs 매핑 OK; 프로세스 스펙은 완료된 일회성 작업                        |
| 04.execution    | 125  | 120 completed / 3 active / 2 README-like missing status | stale `active` Open WebUI plan/task → completed; hardening runtime rows deferred | 0 | infra-opt-priority-plan은 ongoing roadmap이라 active 유지                      |
| 05.operations   | 268  | 197 active / 71 README-like missing status | open-notebook draft→active; policy/guide profile 중복 정리; bucket-root leaf 문서를 목적 폴더로 정리; `05-messaging`/`07-workflow`/`08-ai`/`09-tooling` current-truth 정정 | 5 archived | misplaced ksqlDB guide, duplicate Airflow DAG guide, duplicate AI setup/inference guides, duplicate tooling IaC guide는 `docs/98.archive`; 나머지 orphan 없음(`failures=0`) |

## Task Table

### Findings and Disposition

| ID   | Doc(s)                                                                                                                                                                                                                                     | Evidence                                                                                     | Disposition |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ----------- |
| F-01 | `docs/05.operations/{guides,policies}/11-laboratory/open-notebook.md`                                                                                                                                                                      | `infra/11-laboratory/open-notebook` 구현 존재, 내용 일치                                     | status `draft`→`active` 적용 |
| F-02 | `docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md`, `.../tasks/2026-03-27-08-ai-open-webui-tasks.md`                                                                                                                            | Open WebUI 구현 surface 존재(`infra/08-ai/open-webui`); live RAG indexing은 런타임 evidence 필요 | plan/task status `active`→`completed` 적용; task 내부 live RAG row는 `Deferred`로 보정 |
| F-03 | `docs/03.specs/{workspace-consistency-2026-05b,workspace-doc-consistency-2026-05,docs-taxonomy-agent-first-migration,harness-agent-first-engineering,llm-wiki-agent-first-completion,home-docker-revalidation-deferred-follow-up}/spec.md` | 기술된 작업이 현재 구현에 반영됨(R4/R5 규칙·CI taxonomy·LLM Wiki generator·docs taxonomy 등) | status `active`→`completed` 적용; 현재 구현과 상충하지 않아 archive 미적용 |
| F-04 | `docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md`                                                                                                                                                           | Quick Wins는 구현됐지만 2026 Q2/Q3 quarterly roadmap과 운영 기준 코드화 항목은 계획으로 남아 있음 | `active` 유지 |
| F-05 | `docs/01.requirements/2026-03-26-*` 및 관련 tier PRD                                                                                                                                                                                       | tracked tier implementation exists under `infra/**`; requirements remain current inputs rather than completed task evidence | status `draft`→`active` 적용 |
| F-06 | 변경 폴더의 README 및 governance 문서                                                                                                                                                                                                      | folder-level content/status changes require README/governance alignment                       | `docs/01.requirements/README.md`, QA/GitHub/script governance, progress log updated |
| F-07 | `docs/05.operations/policies/**/*.md`                                                                                                                                                                                                       | 여러 policy leaf에 현재 `policy.template.md`와 다른 중복 `## Policy Scope` heading이 남아 있었음 | 두 번째 이후 `## Policy Scope` heading 제거, bullets 보존; `check-repo-contracts.sh`에 exactly-one gate 추가; `policies/README.md` 계약 업데이트 |
| F-08 | `docs/05.operations/guides/{05-messaging/kafka,06-observability/{alertmanager,grafana,prometheus},09-tooling/{sonarqube,terraform,terrakube}}.md`, `docs/05.operations/runbooks/09-tooling/terraform.md` | guide leaf 7개에 중복 `### Usage Type` profile block이 남아 있었고 Terraform runbook에 `<your-profile>` placeholder가 있었음 | guide 중복 profile 제거, service content 보존, repo contract에 duplicate Usage Type gate 추가; Terraform runbook은 env-var based credential refresh로 정리 |
| F-09 | `docs/05.operations/{guides,policies}/09-tooling/{sonarqube,syncthing}.md`                                                                                                                                                                  | 문서는 `09-tooling` 경로/구현에 속하지만 ID 주석이 과거 `07-tooling` 또는 `08-tooling` tier를 가리킴 | ID 주석을 `09-tooling:<service>`로 정정; `check-repo-contracts.sh`에 operations ID tier/path 일치 gate 추가; 09-tooling guide/policy README에 규칙 반영 |
| F-10 | `docs/02.architecture/requirements/0013-open-webui-architecture.md`, `docs/03.specs/{01-gateway,02-auth,03-security,05-messaging,08-ai}`, selected `docs/04.execution/tasks`, selected `docs/05.operations/{guides,policies,runbooks}` | compose 및 `infra/tech-stack.versions.json`의 현재 이미지 태그와 문서 본문에 남은 runtime version literal이 어긋남 | Traefik, Keycloak, OAuth2 Proxy, Vault, Kafka, RabbitMQ, Kafbat UI, Open WebUI, Grafana, Airflow, Pushgateway, Pyroscope, Qdrant, Neo4j 문서 버전을 현재 구현에 맞게 정정; `check-repo-contracts.sh`에 stale runtime version gate 추가 |
| F-11 | `docs/03.specs/standardize-infra-net/spec.md`, `docs/05.operations/{guides,runbooks}/12-infra-net/standardize-infra-net.md` | active docs의 wildcard IPv4 예시가 authoritative mapping table과 달리 복사 가능한 placeholder처럼 남아 있었음 | registry의 실제 구현 IP(`172.19.0.7`) 기반 예시로 정정하고 대상 서비스에는 authoritative table 값을 사용하도록 단계 보강; `check-repo-contracts.sh`에 stage docs IP placeholder gate 추가 |
| F-12 | `docs/03.specs/workspace-audit-2026-05/{spec.md,README.md}`, `docs/03.specs/README.md` | 완료된 2026-05 감사 spec의 gap table이 당시 baseline인지 현재 구현 상태인지 불명확하게 읽힐 수 있었음 | section을 historical snapshot으로 명시하고 README/03.specs index에서 completed historical spec으로 설명 보강 |
| F-13 | `docs/05.operations/guides/00-workspace/{env-key-comparison,sensitive-env-vars-comparison}.md` | metadata-only 비교 문서의 숫자가 현재 `.env.example`, `.env`, `secrets/SENSITIVE_ENV_VARS.md*` 상태와 어긋남 | `.env.example`/`.env` 키 수를 325/325로, sensitive registry line count를 184/184로 정정하고 값 비교 금지 문구를 metadata-only로 정리; `check-repo-contracts.sh`에 조건부 metadata comparison guide drift gate 추가 |
| F-14 | `docs/02.architecture/{decisions/0015-analytics-engine-selection.md,requirements/0012-data-analytics-architecture.md}`, `docs/03.specs/04-data-analytics/{spec.md,README.md}` | analytics 엔진 선택/계약 문서가 현재 `infra/04-data/analytics` compose의 version family와 다르게 InfluxDB primary, OpenSearch, StarRocks 계열을 오래된 기준으로 설명함 | InfluxDB 3.x Core primary + InfluxDB 2.x legacy compose, Confluent ksqlDB 8.x, OpenSearch 3.x, StarRocks 4.x로 정정; InfluxDB primary health check를 `8181`로 정정; stale analytics version-family gate 추가 |
| F-15 | `docs/05.operations/{guides/06-observability/prometheus.md,runbooks/11-laboratory/dozzle.md,runbooks/11-laboratory/README.md}`, `infra/11-laboratory/dozzle/README.md` | Prometheus guide와 Dozzle runbook/infra README가 현재 PostgreSQL image family 및 Dozzle compose tag와 맞지 않는 구현값을 담고 있었음 | Prometheus scrape 대상 설명을 PostgreSQL 17/18 family로 정정; Dozzle 기준 tag를 `amir20/dozzle:v10.6.4`로 맞추고 rollback은 직전 검증 tag evidence를 기록하도록 수정; stale Dozzle/PostgreSQL literal gate 추가 |
| F-16 | `docs/05.operations/{guides,policies,runbooks}/README.md` 및 `00-workspace`, `12-infra-net`, `90-knowledge` 목적 폴더 | bucket root에 leaf 문서와 folder index가 섞여 있어 Stage 05 운영 문서 구조가 목적별 탐색 계약과 맞지 않았음 | root에는 bucket `README.md`만 남기고 workspace, infra_net, knowledge 문서를 목적 폴더로 이동; parent/child README와 cross-link를 갱신; `check-repo-contracts.sh`에 operations bucket-root leaf 금지와 target-path 일치 gate 추가 |
| F-17 | `infra/04-data/operational/README.md`, `infra/04-data/operational/{mng-db,supabase}/README.md`, `docs/05.operations/{guides,policies,runbooks}/04-data/operational/{mng-db,supabase}.md` | `mng-db` docs retained obsolete network/old Compose CLI guidance and template remnants; Supabase docs assumed direct Studio host-port access and contained incomplete policy/runbook template residue; infra README listed a relational cluster under the operational folder and linked the guide index to policies | Corrected in place to current compose truth: `mng-db` services/profiles/networks/init DBs, Supabase data-profile services/Kong ports/runtime mounts, PostgreSQL image family, and operations guide/policy/runbook links; no archive because documents map to implemented services |
| F-18 | `infra/04-data/cache-and-kv/README.md`, `infra/04-data/cache-and-kv/valkey-cluster/README.md`, `docs/05.operations/{guides,policies,runbooks}/04-data/cache-and-kv/valkey-cluster.md` | Valkey docs referenced stale init/container names, direct password variables, stale image tag, unsupported `maxmemory-policy` control, and destructive restore guidance not proven by current runbook evidence | Corrected in place to current compose truth: six `valkey-node-*` services, `valkey-cluster-init`, `valkey-cluster-exporter`, `service_valkey_password`, `valkey/valkey:9.1.0-alpine`, current port/profile/network model, and non-destructive escalation boundary |
| F-19 | `infra/04-data/lake-and-object/{minio,seaweedfs}/README.md`, `docs/05.operations/{guides,policies,runbooks}/04-data/lake-and-object/{minio,seaweedfs}.md` | MinIO docs mixed root-active single-node compose with optional 4-node cluster recovery; SeaweedFS README contained duplicated old/new structures, an obsolete SeaweedFS version literal, unmounted `security.toml` claims, single-container log command, and unverified destructive restore/reshard procedures | Corrected in place to current compose truth: MinIO root-active `minio` + `minio-create-buckets` with optional cluster variant explicitly scoped; SeaweedFS `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`, image `chrislusf/seaweedfs:4.31`, route/health/mount boundaries, and non-destructive escalation boundary |
| F-20 | `infra/04-data/nosql/{README.md,cassandra/README.md,couchdb/README.md,mongodb/README.md}`, `docs/05.operations/{guides,policies,runbooks}/04-data/nosql/{README.md,cassandra.md,couchdb.md,mongodb.md}` | NoSQL docs retained stale image tags, template/profile residue, old service/control names, unsupported replica-set variable guidance, direct secret-style commands, and destructive restore/resync steps not proven by current runbook evidence | Corrected in place to current compose truth: Cassandra optional single node `cassandra-node1` + `cassandra-exporter` (`cassandra:5.0.8`), CouchDB `couchdb-1..3` + `couchdb-cluster-init` (`couchdb:3.5.2`), MongoDB `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, init/UI/exporter (`mongo:8.2.9-noble`), Docker Secret boundaries, purpose-specific guide/policy/runbook separation, and non-destructive escalation boundary |
| F-21 | `infra/04-data/specialized/{README.md,neo4j/README.md,qdrant/README.md}`, `docs/05.operations/{guides,policies,runbooks}/04-data/specialized/{README.md,neo4j.md,qdrant.md}` | Specialized data docs retained stale image tags, a removed `05.analytical-specialized-dbs.md` link, external Bolt/API-key claims not declared by compose, data mutation guide examples, backup/restore schedules, and destructive recovery steps not proven by current runbook evidence | Corrected in place to current compose truth: root-active Neo4j `neo4j:5.26.26-community` with `neo4j_password` secret-aware entrypoint and HTTP Browser route only; root-active Qdrant `qdrant/qdrant:v1.18.1-unprivileged` with REST/gRPC Traefik routes, current no-secret state, snapshot path, purpose-specific guide/policy/runbook separation, and non-destructive escalation boundary |
| F-22 | `infra/04-data/relational/{README.md,postgresql-cluster/README.md}`, `docs/05.operations/{guides,policies,runbooks}/04-data/relational/{README.md,postgresql-cluster.md}` | Relational docs retained removed old relational index links, stale Spilo entrypoint filename, template/profile residue, unproven backup/archive controls, and destructive DCS/leadership guidance not proven by current runbook evidence | Corrected in place to current compose truth: optional/commented PostgreSQL HA cluster include; etcd `3.6.12`, HAProxy `3.3.10`, Spilo `spilo-17:4.0-p3`, init job `postgres:18-alpine`, exporters `v0.19.1`, Docker Secret boundaries, `pg-router` write/read endpoints, `pg-cluster-init` scope, and non-destructive escalation boundary |
| F-23 | `infra/06-observability/{README.md,docker-compose.yml,docker-compose.dev.yml,*/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**06-observability**` | Observability docs retained stale Mimir/version-family wording, generic README counts, service-local compose validation claims, stale Pushgateway/Pyroscope endpoints, and `docker-compose.dev.yml` referenced Pyroscope via Alloy/Grafana without declaring the service; cAdvisor labels used Pyroscope router/service names | Corrected in place to current compose truth: Prometheus `v3.12.0`, Loki `3.6.6-custom`, Tempo `2.10.1-custom`, Alloy `1.16.2`, Grafana `13.0.2`, cAdvisor `0.55.1`, Pyroscope `2.0.2`, Alertmanager `0.32.1`, Pushgateway `1.11.3`; restored Pyroscope in root-included dev compose; separated cAdvisor/Pyroscope Traefik labels; documented root/overlay compose validation boundary and current retention/storage facts |
| F-24 | `infra/05-messaging/{README.md,kafka/README.md,rabbitmq/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**05-messaging**`, `docs/05.operations/guides/05-messaging/ksql-streaming.md` | Messaging docs retained ksqlDB as a 05-messaging-owned service, old Kafka/RabbitMQ version literals, nonexistent `ksql/` structure, service-local compose validation claims without root context, stale `schema-registry.localhost`, wrong RabbitMQ AMQP route guidance, destructive queue purge guidance, and Guide/Policy/Runbook links that all pointed at policy docs | Archived misplaced `ksql-streaming.md` as a central tombstone; redirected active ksqlDB references to `04-data/analytics/ksql`; corrected Kafka/RabbitMQ docs to current images, profiles, root dev vs service-local full compose boundary, Docker Secrets, Traefik route/AMQP separation, and non-destructive runbook escalation; removed the stale active validator exception so a future 05-messaging `ksql-streaming` guide maps to missing implementation and fails alignment |
| F-25 | `infra/07-workflow/{README.md,airflow/README.md,n8n/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**07-workflow**`, `docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md` | Workflow docs retained Airflow 2 webserver-era service names, repo-local DAG path guidance, direct service-local compose validation claims that fail without root `infra_net`, incorrect n8n project ownership wording, duplicate policy/runbook profile residue, and links that pointed Guide/Runbook labels at policy docs | Archived duplicate `01.airflow-dag-dev.md` as a central tombstone; corrected active Airflow/n8n docs to current service names, Airflow 3.2.2, n8n runner 2.23.2, root-included dev `mng-valkey` vs service-local `airflow-valkey`/`n8n-valkey` boundary, root validator commands, template-compliant guide/policy/runbook purpose separation, and stale-literal repo-contract guards |
| F-26 | `infra/08-ai/{README.md,ollama/README.md,open-webui/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**08-ai**`, `docs/05.operations/guides/08-ai/{01.llm-inference.md,local-llm-setup.md}` | AI docs retained stale Ollama/Open WebUI image guidance, duplicate Ollama setup/inference guides with generic template residue, service-local compose validation claims that fail without root `infra_net`, host-local Open WebUI/exporter health checks despite internal-only exposure, a typoed Open WebUI port env var, and Guide/Runbook labels that pointed at policy docs | Archived duplicate setup/inference guides as central tombstones; corrected active Ollama/Open WebUI/RAG docs to current compose image tags, root optional include boundary, `.env.example` exporter port vs compose fallback, container-internal health checks, current embedding model tag, template-compliant guide/policy/runbook separation, and stale-literal repo-contract guards |
| F-27 | `infra/09-tooling/{README.md,*/README.md}`, `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/**09-tooling**`, duplicate tooling IaC guide | Tooling docs retained stale service image/version guidance, optional compose leaves described as direct standalone config targets, unavailable performance-tool worker/route claims, registry storage/backend mismatch, Terraform/Terrakube service-context drift, and a duplicate IaC guide with generic template residue | Archived duplicate IaC guide as a central tombstone; corrected active tooling docs to current compose truth: root optional include boundary, SonarQube/Syncthing/Terraform/Terrakube current images, registry bind mount storage, `k6-master` Locust-wrapper service, Locust host-port UI boundary, root-context runtime commands, template-compliant guide/policy/runbook separation, and stale-literal repo-contract guards |

## Archive Decision

완료된 일회성 **프로세스 스펙/플랜**(F-03/F-04: workspace-audit, docs-taxonomy-migration,
harness-agent-first, llm-wiki-completion 등)은 현재 구현과 **상충하지 않고 정확히 일치**한다.
따라서 archive 기준은 "historical" 여부가 아니라 **현재 구현과 상충하는지**로 적용한다.
이번 pass에서 신규 archive 대상은 발견되지 않았고, 이미 Airbyte 및 구 Codex/HADS 상충 chain은
`docs/98.archive/README.md` ledger로 tombstone 처리되어 있다.
Stage 05 bucket-root 구조 drift(F-16)는 문서 내용 자체가 현재 구현과 상충하지 않고 위치/탐색
계약만 낡은 경우라 archive가 아니라 in-place 이동 및 reference 갱신으로 처리했다.
`04-data/operational` drift(F-17)는 구현된 `mng-db`와 `supabase` 서비스 문서의 current-truth
불일치였으므로 archive가 아니라 template-compliant in-place rewrite와 README reference 갱신으로
처리했다.
`04-data/cache-and-kv` drift(F-18)도 구현된 Valkey cluster 문서의 service-name/command/control
불일치였으므로 archive가 아니라 template-compliant in-place rewrite와 README reference 갱신으로
처리했다.
`04-data/lake-and-object` drift(F-19)는 구현된 MinIO와 SeaweedFS 문서의 active-vs-optional compose
혼동과 stale runtime/control guidance였으므로 archive가 아니라 template-compliant in-place rewrite와
README reference 갱신으로 처리했다.
`04-data/nosql` drift(F-20)는 구현된 Cassandra, CouchDB, MongoDB 문서의 service-name/image/control
불일치와 검증되지 않은 destructive recovery guidance였으므로 archive가 아니라 template-compliant
in-place rewrite와 README reference 갱신으로 처리했다.
`04-data/specialized` drift(F-21)는 구현된 Neo4j와 Qdrant 문서의 active compose truth, route,
secret/no-secret control, stale link, 검증되지 않은 destructive recovery guidance 불일치였으므로 archive가
아니라 template-compliant in-place rewrite와 README reference 갱신으로 처리했다.
`04-data/relational` drift(F-22)는 구현된 PostgreSQL HA cluster 문서의 optional compose truth, stale
links, secret-aware entrypoint filename, 검증되지 않은 backup/DR/destructive recovery guidance 불일치였으므로
archive가 아니라 template-compliant in-place rewrite와 README reference 갱신으로 처리했다.
`06-observability` drift(F-23)는 구현된 observability compose와 문서의 route/service/version/storage
불일치였고, 일부 compose label/service declaration도 명백한 current-truth 결함이었으므로 archive가 아니라
in-place compose correction, template-aligned documentation correction, README reference 갱신으로 처리했다.
`05-messaging` drift(F-24)는 구현된 Kafka/RabbitMQ 문서의 current-truth mismatch와 misplaced ksqlDB guide가
혼재되어 있었다. Kafka/RabbitMQ 문서는 구현된 서비스에 매핑되므로 in-place correction으로 처리했고,
`docs/05.operations/guides/05-messaging/ksql-streaming.md`는 현재 `infra/05-messaging` 구현에 대응하지 않고
`04-data/analytics/ksql` 문서와 충돌하므로 `docs/98.archive` tombstone으로 이동했다.
`07-workflow` drift(F-25)는 구현된 Airflow/n8n 문서의 current-truth mismatch와 duplicate Airflow DAG guide가
혼재되어 있었다. Airflow/n8n 문서는 구현된 서비스에 매핑되므로 in-place correction으로 처리했고,
`docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md`는 현재 `${DEFAULT_WORKFLOW_DIR}/airflow/dags`
bind-mount 기준과 충돌하고 `airflow-dag-basics.md`와 중복되므로 `docs/98.archive` tombstone으로 이동했다.
`08-ai` drift(F-26)는 구현된 Ollama/Open WebUI 문서의 current-truth mismatch와 duplicate Ollama
setup/inference guides가 혼재되어 있었다. Ollama/Open WebUI/RAG/hardening 문서는 구현된 서비스에 매핑되므로
in-place correction으로 처리했고, duplicate setup/inference guides는 active `ollama.md`와 중복되며 runbook
handoff가 불완전해 `docs/98.archive` tombstone으로 이동했다.
`09-tooling` drift(F-27)는 구현된 tooling 서비스 문서의 current-truth mismatch와 duplicate IaC automation
guide가 혼재되어 있었다. Terraform/Terrakube/Registry/SonarQube/Syncthing/Locust/k6 문서는 구현된 서비스에
매핑되므로 in-place correction으로 처리했고, duplicate tooling IaC guide는 active `terraform.md`/`terrakube.md`와
중복되며 runbook handoff가 불완전해 `docs/98.archive` tombstone으로 이동했다.

## Verification Summary

- Stage 01-05 inventory: `docs/01.requirements=25`, `docs/02.architecture=51`, `docs/03.specs=43`, `docs/04.execution=125`, `docs/05.operations=269`, total `513`.
- operations 서비스 커버리지: `check-doc-implementation-alignment.sh` → `operations_service_docs_checked=143`, `failures=0`.
- operations bucket-root scan: `docs/05.operations/{guides,policies,runbooks}` root에는 각 bucket `README.md`만 남음.
- stale operations root-path scan: 이전 bucket-root leaf 형태(`guides/<leaf>.md`, `runbooks/<leaf>.md`, `policies/<leaf>.md`) 0건.
- legacy/orphan 스캔: 신규 미구현-service 문서 없음; Patroni/Spilo/HADS는 현행 구현 또는 historical evidence로 분류.
- policy profile scan: `docs/05.operations/policies/**/*.md` leaf에서 `## Policy Scope` 중복 0건; repo contract가 policy leaf당 exactly one heading을 강제.
- guide profile scan: 중복 `### Usage Type` 0건; 남은 TODO/TBD/placeholder-like hits는 historical evidence 또는 scan command literal로 분류.
- operations ID tier scan: `docs/05.operations/{guides,policies,runbooks}` ID 주석과 path tier 불일치 0건; repo contract가 불일치를 차단.
- runtime version drift scan: stale runtime version literal 0건; repo contract가 현재 compose/tech-stack registry와 어긋나는 문서 버전 재유입을 차단.
- IP placeholder scan: wildcard infra/k3d IPv4 placeholder 0건; repo contract가 concrete-network placeholder 재유입을 차단.
- metadata comparison scan: `.env.example`/`.env` key count 325/325, sensitive registry line count 184/184, secret ID count 107; repo contract가 로컬 파일 존재 시 metadata-only 숫자 drift를 차단.
- analytics/laboratory version-family scan: analytics primary/decision stale phrases, Dozzle old tag, and PostgreSQL old scrape family phrase 0건; repo contract가 exact stale literal 재유입을 차단.
- 04-data operational scan: `mng-db`/`supabase` guide, policy, runbook 문서에서 old Compose CLI command spelling, direct Studio host-port literal, template copyright residue, and obsolete shared-network literal 0건.
- 04-data operational implementation mapping: `mng-db` docs now match compose services `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`; Supabase docs now match data-profile services `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`.
- 04-data cache-and-kv scan: Valkey guide, policy, runbook, and infra README stale init/container names, stale image tag, direct password variable command, unsupported maxmemory policy, and single-container command assumptions 0건.
- 04-data cache-and-kv implementation mapping: Valkey docs now match compose services `valkey-node-0` through `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter`, profiles `data`/`service`, network `infra_net`, and secret `service_valkey_password`.
- 04-data lake-and-object scan: MinIO/SeaweedFS guide, policy, runbook, and infra README stale SeaweedFS version, single-container SeaweedFS log target, unverified reshard command, direct MinIO root credential env references, and root-active/optional cluster confusion 0건 outside the explicitly optional MinIO cluster compose file.
- 04-data lake-and-object implementation mapping: MinIO docs now match root-active `minio` + `minio-create-buckets` and optional `docker-compose.cluster.yaml`; SeaweedFS docs now match services `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`, image `chrislusf/seaweedfs:4.31`, network `infra_net`, and mount privilege boundary.
- 04-data nosql scan: Cassandra/CouchDB/MongoDB guide, policy, runbook, and infra README stale image tags, old service names, old secret-control names, unsupported replica-set variable guidance, direct password examples, and destructive restore/resync commands 0건.
- 04-data nosql implementation mapping: Cassandra docs now match optional `cassandra-node1` + `cassandra-exporter`, image `cassandra:5.0.8`, profiles `data`/`obs`, secret `cassandra_password`; CouchDB docs now match `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init`, image `couchdb:3.5.2`, secrets `couchdb_password`/`couchdb_cookie`; MongoDB docs now match `mongo-key-generator`, `mongodb-rep1`, `mongodb-rep2`, `mongodb-arbiter`, `mongo-init`, `mongo-express`, `mongodb-exporter`, image `mongo:8.2.9-noble`, replica set `MyReplicaSet`, and non-destructive escalation boundary.
- 04-data specialized scan: Neo4j/Qdrant guide, policy, runbook, and infra README stale image tags, removed guide link, unsupported external Bolt/API-key claims, mutation guide examples, backup/restore schedules, and destructive recovery commands 0건.
- 04-data specialized implementation mapping: Neo4j docs now match root-active `neo4j`, image `neo4j:5.26.26-community`, profiles `data`/`graph`, secret `neo4j_password`, secret-aware entrypoint, healthcheck, and HTTP Browser route; Qdrant docs now match root-active `qdrant`, image `qdrant/qdrant:v1.18.1-unprivileged`, profiles `ai`/`data`/`dev`, no-secret state, REST/gRPC Traefik routes, `/readyz` healthcheck, and non-destructive escalation boundary.
- 04-data relational scan: PostgreSQL cluster guide, policy, runbook, and infra README removed old relational index links, stale entrypoint filename, unproven backup/archive controls, manual leadership-mutation instructions, destructive DCS reset command, and old template residue 0건.
- 04-data relational implementation mapping: PostgreSQL cluster docs now match optional/commented root include services `etcd-1..3`, `pg-router`, `pg-cluster-init`, `pg-0..2`, `pg-0-exporter..pg-2-exporter`, image families/tags etcd `3.6.12`, HAProxy `3.3.10`, Spilo `spilo-17:4.0-p3`, init job `postgres:18-alpine`, postgres exporter `v0.19.1`, Docker Secret boundaries, `pg-router` write/read endpoints, and non-destructive escalation boundary.
- 06-observability stale scan: old Prometheus/Grafana/Alloy/Pyroscope/Alertmanager/Pushgateway version literals, old Mimir wording, `pushgateway.local`, stale Pyroscope `/health`, and generated `plus N more` README evidence 0건 in active observability scope.
- 06-observability implementation mapping: root-included `docker-compose.dev.yml` and local `docker-compose.yml` now both render `prometheus`, `loki`, `tempo`, `alloy`, `grafana`, `cadvisor`, `pyroscope`, `alertmanager`, and `pushgateway`; cAdvisor uses `cadvisor` Traefik labels and `${CADVISOR_PORT:-8080}`, Pyroscope uses `pyroscope` Traefik labels and `${PYROSCOPE_PORT:-4040}`.
- 06-observability validation boundary: root profile validation passes with `HYHOME_COMPOSE_PROFILES=obs`; service-local compose validation requires root network/secret context or an explicit temporary validation overlay.
- 05-messaging implementation mapping: root messaging profile renders `kafka-1`, `schema-registry`, `kafka-connect`, `kafka-rest-proxy`, `kafbat-ui`, `kafka-exporter`, `kafka-init`, and `rabbitmq`; `HYHOME_COMPOSE_PROFILES=messaging` validation passes with `services_total=8`, while `HYHOME_COMPOSE_PROFILES='messaging dev'` validation passes with `services_total=46`.
- 05-messaging service-local boundary: direct service-local `--profile messaging config --services` for Kafka full, Kafka dev, and RabbitMQ compose fails without root `infra_net` context (`undefined network infra_net`), so active docs now route normal validation through root profile scripts or explicit overlay context.
- 05-messaging stale scan: outside this audit evidence, archive tombstones, generated indexes, and the current `04-data/analytics` ksqlDB owner docs, active messaging docs no longer retain the old ksql streaming guide path, old Kafka/RabbitMQ version literals, stale Schema Registry host example, destructive queue purge command, or unrelated MinIO CLI definition export command.
- 07-workflow implementation mapping: root workflow profile renders `airflow-init`, `airflow-apiserver`, `airflow-dag-processor`, `airflow-scheduler`, `airflow-statsd-exporter`, `airflow-triggerer`, `flower`, `airflow-worker`, `n8n`, `n8n-worker`, `n8n-task-runner`, and `n8n-task-runner-worker`; `HYHOME_COMPOSE_PROFILES=workflow` validation passes with `services_total=12`, while `HYHOME_COMPOSE_PROFILES='workflow dev'` validation passes with `services_total=45`.
- 07-workflow service-local boundary: direct service-local `--profile workflow config --services` for Airflow and n8n compose fails without root `infra_net` context (`undefined network infra_net`), so active docs now route normal validation through root profile scripts or explicit overlay context.
- 07-workflow stale scan: active workflow docs no longer retain old Airflow webserver service names, incorrect n8n project ownership wording, or repo-local DAG placement guidance; repo contract blocks those exact stale literals in Stage 01-05 docs.
- 08-ai implementation mapping: current tracked AI implementation is optional/commented at root for `ollama`, `ollama-exporter`, and `open-webui`; Qdrant remains root-included under `04-data/specialized` with `ai`/`data`/`dev` profiles.
- 08-ai validation boundary: AI hardening baseline passes, and root-active `core ai` profile validation passes with `services_total=6`; service-local AI compose files fail as standalone checks without root `infra_net` context, so active docs route static validation through the hardening script and root profile validator.
- 08-ai stale scan: active AI docs no longer retain old Ollama/Open WebUI image guidance, typoed Open WebUI port env variable, duplicate setup/inference guide links, host-local Open WebUI/exporter health assumptions, or Guide/Runbook labels that point at policy docs; repo contract blocks exact stale literals and direct service-local AI compose validation commands in Stage 01-05 docs.
- reference.template.md archive 언급: 0건(제약 이미 충족).
- Local QA gate: `bash scripts/validation/run-local-qa-gates.sh` → PASS, repo contracts `failures=0`, generated LLM Wiki fresh.

## Related Documents

- **Archive index/ledger**: [98.archive README](../../98.archive/README.md)
- **Alignment check**: [check-doc-implementation-alignment.sh](../../../scripts/validation/check-doc-implementation-alignment.sh)
- **Documentation protocol**: [documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
