---
title: "독립 LAB 문서 런북"
version: "0.3.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
---

# 독립 LAB 문서 런북

## Stage Responsibility

### Purpose and Readers

독립 LAB 문서의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

### Inputs and Outputs

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Contents

### Current Items

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Valkey Cluster Health Runbook](0022-valkey-cluster.md) | `RUN-0022` | LAB 전용 Valkey Cluster(`labs/valkey-cluster/docker-compose.yml`)의 정적 점검, 백업 계획, 격리 복원 절차를 다룬다. |
| [Cassandra Health and Recovery Triage Runbook](0025-cassandra.md) | `RUN-0025` | 독립 Cassandra 단일 노드 LAB의 정적 점검과 승인 후 read-only triage 순서다. 이번 변경에서 실제 서비스·데이터를 실행하지 않았다. |
| [CouchDB Cluster Triage Runbook](0026-couchdb.md) | `RUN-0026` | 범위: LAB 전용 CouchDB 3노드 cluster의 상태, cluster-init 결과, membership, 격리 network의 route 한계를 점검한다. 이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 fresh  |
| [MongoDB Replica Set Triage Runbook](0027-mongodb.md) | `RUN-0027` | 범위: LAB 전용 MongoDB replica set의 상태, init job 결과, Mongo Express 접속을 파괴적 데이터 작업 없이 점검한다. 이 런북은 현재 compose에 맞는 점검 순서와, 별도 승인 후 수행할 oplog-consis |
| [PostgreSQL Cluster Health and Recovery Triage Runbook](0031-postgresql-cluster.md) | `RUN-0031` | 범위: LAB 전용 PostgreSQL HA cluster의 상태, etcd quorum 증상, HAProxy routing, Patroni leadership, init job 상태, exporter readiness를 파괴적 데이터 작업 없이 점검 |
| [Open WebUI Runbook](0057-open-webui.md) | `RUN-0057` | Open WebUI LAB의 준비·기동·장애 대응과 HOME 컨테이너·volume 퇴역 단계를 다루는 런북이다. |
| [Locust Recovery Runbook](0062-locust.md) | `RUN-0062` | Locust LAB 실행 중 target 상태가 나빠지거나 worker 연결이 끊길 때 부하를 멈추고 진단하는 절차다. 시나리오 파일 복구와 승인된 upgrade canary도 다룬다. |
| [SonarQube Runbook](0066-sonarqube.md) | `RUN-0066` | SonarQube(`sonarqube` service)의 health·DB 연결 장애, 검색 인덱스 복구, 토큰 사고, DB 복원, 업그레이드 절차다. |
| [Stalwart Mail Runbook](0070-mail.md) | `RUN-0070` | 이 런북은 Stalwart의 listener, 인증, TLS, DNS, queue 장애 진단과 메일박스·설정 복구, 승인된 최초 기동과 업그레이드 절차를 정의한다. |
| [JupyterLab Recovery Runbook](0089-jupyterlab.md) | `RUN-0089` | JupyterLab LAB의 시작 실패, 토큰 노출, 커널 정지, 작업 파일 손실, 이미지 업그레이드를 다루는 복구 런북이다. |
| [dbt Recovery Runbook](0090-dbt.md) | `RUN-0090` | dbt LAB의 프로비저닝 실패, 연결·권한 오류, 잘못된 모델 실행, 크리덴셜 교체를 다루는 런북이다. |
| [Lakehouse Recovery Runbook](0094-lakehouse.md) | `RUN-0094` | lakehouse LAB의 Spark·Trino·Flink·Great Expectations 실패, 카탈로그 오류, 접근 거부, 테이블 롤백을 다루는 런북이다. |
| [Superset Runbook](0097-superset.md) | `RUN-0097` | Superset LAB의 최초 설정, 로그인 실패, 웹 서버 비정상, 업그레이드를 다루는 런북이다. |
| [LAB Promotion Runbook](0107-lab-promotion.md) | `RUN-0107` | readiness 검사 실행과 `add`, `replace-same`, `replace-substitute` 승격 절차를 다룬다. |
| [Kafka Cluster LAB Runbook](0108-kafka-cluster.md) | `RUN-0108` | Kafka LAB의 정적 점검, `lab.py` 기동·정지, broker 진단과 복구 계획이다. |
| [OpenSearch Cluster LAB Runbook](0109-opensearch-cluster.md) | `RUN-0109` | OpenSearch LAB의 정적 점검, `lab.py` 기동·정지, cluster 진단과 복구 계획이다. |

### Classification

이 폴더의 문서는 모두 런북 역할이며 `RUN-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 폴더에 있다.

## Workflow

### Create and Review

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

이동 대상은 LAB 관련 운영 문서다. 서비스 소스는 저장소 루트 `labs/`가 소유한다.
문서 이동은 LAB 서비스 기동, 배포, 비밀번호 변경, 데이터 이동·삭제 또는 복구 실행을 뜻하지 않는다.

### Transition and Exit

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. 종료 상태에 이른 문서는 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다.

## Related Documents

### Upstream and Downstream

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)

### Policy and Templates

- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
- [README 템플릿](../../../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다
