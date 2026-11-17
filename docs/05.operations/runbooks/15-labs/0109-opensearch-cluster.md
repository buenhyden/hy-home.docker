---
title: "OpenSearch Cluster LAB Runbook"
version: "0.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0109"
parent_ids:
- "GDE-0109"
created: "2026-11-05"
next_review_at: "2027-05-13"
---

# OpenSearch Cluster LAB Runbook

## Trigger and Scope

### Trigger

OpenSearch LAB([`labs/opensearch-cluster/docker-compose.yml`](../../../../labs/opensearch-cluster/docker-compose.yml), project `hy-home-lab-opensearch`)의
정적 점검, `lab.py` 기동·정지, cluster 진단과 복구 계획을 다룬다.

OpenSearch LAB의 정적 검증, 승인된 실험 기동, node·Dashboards 이상 진단, 승격 전 readiness 확인에
쓴다.

### Targets

- Runtime source: [OpenSearch LAB Compose](../../../../labs/opensearch-cluster/docker-compose.yml).
- Artifact: `RUN-0109`; parent guide: `GDE-0109`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

- [OpenSearch LAB guide](../../guides/15-labs/0109-opensearch-cluster.md)
- [LAB promotion runbook](0107-lab-promotion.md)
- [Domain catalog](../../README.md)

## Preflight

### Authority

- 기동 전 Docker context, network·volume, 가용 CPU·memory·disk(high watermark 90% 미만), bind
  디렉터리 소유와 정리 대상을 owner가 승인한다.
- 이 런북의 모든 runtime 단계는 별도 승인이 필요하다. 이 문서 작성에서는 아무것도 실행하지 않았다.

### Environment

- `labs/.env`에 `LAB_DATA_DIR`, `LAB_SECRET_DIR`, `LAB_OPENSEARCH_CERT_DIR`가 있다. 현재 HOME 입력의
  render는 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면 `LAB_OPENSEARCH_CERT_DIR`가 없다. owner가 LAB 전용 CA와 node
  인증서를 준비하고 값을 넣는다.
- `secrets/labs/opensearch-cluster/`에 네 LAB secret 사본이 있다. owner가 준비하며 agent는 읽지 않는다.

#### Static check

repository root에서 합성 경로로 render한다.

```bash
LAB_DATA_DIR=/tmp/synthetic-lab-data LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --services
```

네 서비스 `opensearch-node1`, `opensearch-node2`, `opensearch-node3`, `lab-opensearch-dashboards`가
나와야 한다. 다르면 멈춘다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | Start and stop: 승인된 경우에만 `lab.py check/up/down opensearch-cluster` 실행 | 문서에 기록 없음 | `down -v`와 volume prune은 쓰지 않음 |
| 2 | Diagnosis: 활성 lease에서 세 node와 Dashboards 상태(`ps`) 확인 | 세 node와 Dashboards가 healthy | 중단하고 @buenhyden에게 보고 |
| 3 | Diagnosis: node unhealthy 시 log에서 인증서 subject/CA 불일치, `nodes_dn` 거부, memory lock, disk watermark, bind 디렉터리 권한(uid 1000) 확인 | 문서에 기록 없음 | log 원문은 evidence에 붙이지 않음 |
| 4 | Diagnosis: Dashboards unhealthy 시 세 node healthy, `rootCA.pem` mount, dashboard secret 확인 | 문서에 기록 없음 | 문서에 기록 없음 |
| 5 | Diagnosis: LAB network 안에서 `_cluster/health`와 `_cat/nodes`로 cluster 상태 확인 | `_cluster/health`와 `_cat/nodes`로 cluster 상태가 확인됨 | 비밀번호는 명령 인자에 넣지 않음 |
| 6 | Planned backup and isolated restore: 승인된 window에서 snapshot repository를 정하고 index 목록/mapping/문서 수 기록 | 문서에 기록 없음 | 데이터 소유가 불명확하면 멈추고 @buenhyden에게 보고 |
| 7 | Planned backup and isolated restore: snapshot 생성 후 새 격리 cluster에 복원 | 문서에 기록 없음 | 이전 node data 디렉터리를 재사용하지 않음 |
| 8 | Planned backup and isolated restore: index별 문서 수와 mapping을 비교하고 Task에 기록 | 결과를 Task에 기록 | 문서에 기록 없음 |
| 9 | Readiness: 승격 전 RUN-0107의 readiness 검사를 `opensearch-cluster`로 실행 | 문서에 기록 없음 | RUN-0107에 따름 |

기동·정지, 진단, 복구 계획, readiness 확인은 다음과 같다.

#### Start and stop

승인된 경우에만 `lab.py`로 기동·정지한다.

```bash
python3 scripts/operations/lab.py check opensearch-cluster
python3 scripts/operations/lab.py up opensearch-cluster --purpose "<목적>" --lease <기간>
python3 scripts/operations/lab.py down opensearch-cluster
```

`down -v`와 volume prune은 쓰지 않는다.

#### Diagnosis

1. 활성 lease와 승인된 Docker context에서 세 node와 Dashboards의 상태를 확인한다.
   `LAB_ENV_FILE`은 그 lease를 시작할 때 사용한 LAB 환경 파일의 경로다.

   ```bash
   docker compose --project-name hy-home-lab-opensearch --env-file "$LAB_ENV_FILE" -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster ps
   ```

2. node가 unhealthy이면 log에서 인증서 subject·CA 불일치, `nodes_dn` 거부, memory lock, disk
   watermark, bind 디렉터리 권한(uid 1000)을 찾는다. log 원문은 evidence에 붙이지 않는다.
3. Dashboards가 unhealthy이면 세 node가 healthy인지, `rootCA.pem` mount와 dashboard secret이 있는지
   확인한다.
4. cluster 상태는 LAB network 안에서 `_cluster/health`와 `_cat/nodes`로 확인한다. 비밀번호는
   명령 인자에 넣지 않는다.

#### Planned backup and isolated restore

1. 승인된 window에서 snapshot repository를 정하고 index 목록, mapping, 문서 수를 기록한다.
2. snapshot을 만들고 새 격리 cluster에 복원한다. 이전 node data 디렉터리를 재사용하지 않는다.
3. index별 문서 수와 mapping을 비교하고 결과를 Task에 기록한다.

이 절차는 계획이며 현재 layout에서 실행된 적이 없다.

#### Readiness

승격 전 [RUN-0107](0107-lab-promotion.md)의 readiness 검사를 `opensearch-cluster`로 실행한다.

### Stop Conditions

render된 서비스가 Static check에 나열한 네 서비스와 다르면 멈춘다. HOME 경로가 render에 나타나거나 데이터 소유가 불명확하면 멈추고 @buenhyden에게 보고한다.

## Verification

### Expected Results

#### Service Checks

Static check render에 네 서비스가 나오고 세 node와 Dashboards가 healthy이며, `_cluster/health`와 `_cat/nodes`로 cluster 상태가 확인되어야 한다.

#### Evidence

source revision, 실행한 명령과 종료 코드, node·Dashboards health, cluster 상태 요약, 미검증 gap을
기록한다. secret, 인증서 내용, raw log와 rendered private 설정은 기록하지 않는다.

### Unverified Conditions

이 runbook이 아직 관찰하지 못한 항목은 다음과 같다. 문서는 복구 절차가 현재 layout에서 실행된 적이 없는 계획이라고 적고 있다.

- Planned backup and isolated restore: 이 문서에는 실행 결과가 기록되어 있지 않다. 격리 cluster에서 index별 문서 수와 mapping 일치가 관찰되면 검증된다.
- `lab.py up/down opensearch-cluster`와 진단 명령(`ps`, `_cluster/health`, `_cat/nodes`): 승인된 lease가 필요하며 실행 결과가 기록되어 있지 않다. 세 node와 Dashboards healthy 및 cluster 상태가 관찰되면 검증된다.
- readiness 검사: `opensearch-cluster`에 대한 실행 결과가 기록되어 있지 않다.

## Escalation

### Next Owner

HOME secret·인증서 경로가 render에 나타나거나, disk가 watermark를 넘거나, 데이터 소유가 불명확하면
멈추고 @buenhyden에게 보고한다.

### Recovery or Forward Repair

LAB은 HOME 소비자가 없으므로 `lab.py down opensearch-cluster`로 멈추면 HOME에 영향이 없다. 데이터는
`${LAB_DATA_DIR}/opensearch-cluster/`에 남는다. 삭제는 별도 승인이다.
