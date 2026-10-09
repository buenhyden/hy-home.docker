---
title: "OpenSearch Recovery Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "operations"
artifact_id: "RUN-0019"
parent_ids:
- "GDE-0019"
created: "2026-05-17"
---

# OpenSearch Recovery Runbook

## Overview

정상 단일 OpenSearch의 준비 상태 점검과 별도 standalone LAB의 정적·운영 경계를 다룬다. 정상 root는 `opensearch` profile의 `opensearch`와 `opensearch-dashboards`를 선택한다. 세 노드와 `lab-opensearch-dashboards`는 standalone `labs/opensearch-cluster.yml`의 별도 project이며 HOME 서비스가 아니다. 소스 검증만 승인된 경우 서비스 기동·중단·복구는 `NOT_RUN`으로 기록한다.

- HTTPS와 Docker Secret 기반 healthcheck를 사용한다.
- 정상 root와 별도 LAB project를 혼동하지 않는다.
- index/shard 작업 전 snapshot이나 escalation evidence를 확보한다.

## Trigger and Preconditions

- primary `opensearch` healthcheck가 실패할 때
- Dashboards가 OpenSearch에 연결할 수 없을 때
- `opensearch-cluster` topology에 unhealthy node나 shard allocation 문제가 있을 때

### Execution and stop boundary

대상: 정상 `opensearch`, `opensearch-dashboards`; LAB `opensearch-node1..3`, `lab-opensearch-dashboards`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

Dockerfile의 OpenSearch 기본 이미지와 exporter plugin 선언 버전의 실제 빌드 호환성은 확인되지 않았으므로 (미검증), 정상과 LAB의 build/start/restore 성공을 가정하지 않는다. LAB 인증서의 node/관리자 DN·SAN·신뢰와 Dashboards 연결도 별도 검증 전이다.

사전 확인:

- [ ] 정상 root `opensearch`인지 standalone LAB `opensearch-cluster`인지 Compose 파일과 project 이름까지 기록했습니다. 각 project의 Dashboard는 별개입니다.
- [ ] admin password는 안전하게 읽고 저장하지 않는다.
- [ ] index나 shard 변경에는 owner 승인이 필요하다.

절차:

1. primary compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/opensearch/docker-compose.yml
   test -f labs/opensearch-cluster.yml
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. primary health를 HTTPS로 확인한다.

   실제 TTY를 가진 비공개 운영 terminal에서만 client 자체 password prompt를 사용한다. tracing/verbose/terminal recording과 redirected stdin, `exec -T`를 금지한다. 승인된 custody에서 받은 credential을 prompt에만 입력하며 shell 변수·환경·argv·URL로 전달하지 않는다. prompt/권한/CA/endpoint가 없거나 인증이 실패하면 중단한다. root/Docker 관리자의 메모리 관찰까지 차단한다고 주장하지 않는다.

   ```bash
   docker compose exec opensearch curl -fsS --user admin --cacert /usr/share/opensearch/config/certs/rootCA.pem "https://opensearch:9200/_cluster/health?filter_path=status"
   ```

3. Logs를 확인한다.

   ```bash
   docker compose --profile opensearch logs --tail 100 opensearch opensearch-dashboards
   ```

4. LAB 구성은 별도 파일로 정적 확인합니다. LAB 기동이나 로그 조회는
   명시적 LAB 실행 승인 후에만 합니다.

   ```bash
   docker compose --env-file labs/.env.example -f labs/opensearch-cluster.yml --profile opensearch-cluster config --quiet
   ```

   `${LAB_SECRET_DIR}`과 `${LAB_OPENSEARCH_CERT_DIR}`는 승인된 LAB 전용 경로여야 합니다. 정적 render에는 합성 경로를 사용할 수 있지만 비밀 파일 원문을 출력하지 않습니다.

현재 healthcheck와 시작 스크립트는 비밀값을 command argv에 싣지 않도록 수정했습니다. 실제 이미지 빌드·인증·health는 격리 실행 전까지 NOT_RUN입니다. source image가 제공하는 client를 쓰며 실제 packaged prompt 동작이 다르면 우회하지 않는다. 예시는 primary만 해당한다. certificate SAN/CA가 위 hostname과 일치하지 않으면 `-k`로 우회하지 않는다. LAB는 승인된 별도 target/CA/project를 지정하며 현재 custom 이미지의 기본 엔진·plugin 빌드 호환성과 인증서 신뢰가 미검증이므로 operational acceptance는 보류합니다.

### Planned isolated snapshot restore

이 절차는 실행 결과가 아닌 계획이며 실제 snapshot·복구 증거는 해당 실행 Task에 기록합니다.

1. 선택한 topology, cluster UUID/version, index inventory, shard health, repository plugin/configuration, encryption과 credential owner, 가용 disk, 승인된 restore 목적지를 기록한다. tracked security configuration과 certificate는 별도로 보존한다.
2. least-privilege credential로 live data volume 밖의 repository를 등록하거나 검증한다. `.opendistro_security`를 제외한 named snapshot을 만들고 `SUCCESS`를 기다린 뒤 포함된 index와 실패 내역을 기록한다. live data-directory copy에 의존하지 않는다.
3. 빈 volume, 별도의 cluster 이름, production router 없이 호환되는 새 isolated primary 또는 cluster topology를 준비한다. credential을 노출하지 않고 동일한 repository를 등록한다.
4. 선택한 application index를 임시 이름으로 또는 빈 target에 복원한다. 검토된 security configuration은 별도로 적용하며, security index를 맹목적으로 복원하지 않는다.
5. 상황에 맞게 green/yellow cluster health, shard allocation, 예상 index/document count, 대표 검색, Dashboards 연결성, TLS, role, 예기치 않은 write alias 부재를 확인한다.
6. restore 또는 security validation이 실패하면 isolated volume만 중지하고 보존하고 별도 승인된 새 target에서 변경되지 않은 snapshot에서 재시도한다. 강제 복구를 위해 shard를 reroute하거나 active index를 덮어쓰지 않는다.
7. cutover, alias 변경, snapshot 삭제, active-cluster restore는 별도 approval이 필요하다. rehearsal이 성공을 기록하기 전까지 restore는 검증되지 않은 상태다.

## Verification

- [ ] health endpoint가 primary stack에 대해 최소 yellow 상태를 반환한다.
- [ ] Dashboards health endpoint가 compose healthcheck가 허용하는 `200` 또는 `401`을 반환한다.
- [ ] 최종 evidence에 정상 또는 LAB의 Compose 파일·project·service를 명시합니다. 관측하지 않은 runtime 결과는 `NOT_RUN`으로 기록합니다.

### Observability and Evidence Sources

- **Logs**: OpenSearch와 Dashboards compose log
- **Metrics**: 별도 exporter가 실행 중이지 않으면 N/A
- **Evidence**: health 응답, 선택한 compose file, service log 요약, secret boundary 확인

### 증거 기록

- compose file, service 이름, health 상태, 로그 요약, escalation 결정을 기록한다.
- password 값은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

rehearsal의 rollback은 source cluster와 snapshot을 변경하지 않은 채 isolated topology를 보존하고 원본을 계속 사용하는 것이다. cutover plan은 source를 유지하고 alias/DNS 전환을 별도로 정의해야 한다.

### Escalation

health가 계속 red/unavailable이거나, shard 변경이 필요하거나, secret이나 cert가 없거나, primary와 cluster variant evidence가 충돌할 때 escalation한다.

## Related Documents

### Traceability

- Declared parent: [OpenSearch Usage Guide](../guides/0019-opensearch.md) (`GDE-0019`)
- Governing authority: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](../guides/0019-opensearch.md) (`GDE-0019`), [Policy](../policies/0019-opensearch.md) (`POL-0019`)

- [Compose implementation: infra/04-data/opensearch/docker-compose.yml](../../../infra/04-data/opensearch/docker-compose.yml)
- [Standalone LAB Compose](../../../labs/opensearch-cluster.yml) 및 [LAB 설명](../../../labs/opensearch-cluster.md)
- [Custom image source: infra/04-data/opensearch/Dockerfile](../../../infra/04-data/opensearch/Dockerfile)

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Operations runbooks index](../README.md)
- [Usage guide](../guides/0019-opensearch.md)
- [Operations policy](../policies/0019-opensearch.md)
