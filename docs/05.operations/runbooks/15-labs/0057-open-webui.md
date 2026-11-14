---
title: "Open WebUI Runbook"
version: "1.2.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "operations"
artifact_id: "RUN-0057"
parent_ids:
- "GDE-0057"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Open WebUI Runbook

## Purpose

### Trigger and Outcome

이 런북은 독립 LAB `labs/open-webui/docker-compose.yml`(profile `lab-open-webui`)의 준비·기동·장애 대응과,
2026-11-10 ADR-0062 개정으로 HOME에 남은 Open WebUI 컨테이너·volume의 퇴역 절차를 다룬다.

- LAB을 lease 안에서만 기동하고 정리한다.
- HOME 잔여 상태를 승인 단계별로 퇴역한다.
- 같은 장애가 반복될 때 일관된 증적을 남긴다.

- LAB 실험 준비 또는 `lab.py check open-webui` 실패.
- LAB 로그인 실패, 모델 목록 미표시, RAG 인덱싱 실패, healthcheck 실패.
- HOME 퇴역 단계 중 하나가 승인됨.

### Scope

> 범위: Open WebUI LAB과 HOME 잔여 상태

- Declared parent: [Open WebUI Usage Guide](../../guides/15-labs/0057-open-webui.md) (`GDE-0057`)
- Governing decision: [ADR-0062](../../../02.architecture/decisions/0062-home-lab-membership.md)
- Subject peers: [Guide](../../guides/15-labs/0057-open-webui.md) (`GDE-0057`), [Policy](../../policies/15-labs/0057-open-webui.md) (`POL-0057`)

- [Operations index](../../README.md)
- [Usage guide](../../guides/15-labs/0057-open-webui.md)
- [Operations policy](../../policies/15-labs/0057-open-webui.md)

## Preconditions

### Authority and Access

LAB과 HOME 명령의 실행 경계와 승인 조건은 다음과 같다.

#### Execution Boundary

LAB 명령은 `python3 scripts/operations/lab.py`의 목적·lease·충돌·예산 규칙을 따른다. `down`은 `-v` 없이
그 LAB project만 정지한다. HOME 명령은 이 런북의 퇴역 단계가 각각 승인된 경우에만 실행한다. 예상 밖 출력,
backup 누락, 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. 공통 절차는
[LAB 승격](0107-lab-promotion.md), [백업](../10-platform-and-backup/0021-backup-and-restore.md),
[계정](../03-identity-and-access/0014-keycloak.md), [gateway·인증서](../02-gateway-and-networking/0013-traefik.md)가 소유한다.

### Safety Checks

기동 전 확인할 LAB 설정, 비밀 파일 이름, data 경로 전제는 다음과 같다.

#### Service lifecycle prerequisites

- `labs/.env`에 `LAB_DATA_DIR`, `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`, `LAB_OPEN_WEBUI_DEFAULT_URL`,
  `LAB_OPEN_WEBUI_CA_FILE`이 있고, 소유자가 LAB network에서 도달 가능한 Ollama endpoint를 승인했다.
- `${LAB_SECRET_DIR}/open-webui/oidc_client_secret.txt`(`LAB-037`) LAB 사본이 별도 승인으로 준비되었다.
  값은 출력하거나 증거로 남기지 않는다.
- `${LAB_DATA_DIR}/open-webui/data`가 있고 HOME data 경로와 겹치지 않는다.
- LAB origin redirect의 Keycloak 등록 여부를 확인했다. 등록 전에는 로그인 성공을 주장하지 않는다.

## Steps

### Actions

LAB 기동·점검과 데이터 보존, HOME 퇴역 단계는 다음 순서를 따른다.

#### LAB start and triage

```bash
python3 scripts/operations/lab.py check open-webui
docker logs --tail 200 open-webui
```

활성 lease 안에서는 같은 LAB project(`labs/open-webui/docker-compose.yml`, profile `lab-open-webui`, 운영자
`labs/.env`)로 `exec open-webui curl -f http://localhost:8080/health`를 실행한다.

health는 로그인·RAG의 증거가 아니다. 승인된 lease 안에서 Keycloak 로그인, 모델 목록, 통제된 RAG 질의를
따로 확인한다. entrypoint는 secret이 비었거나 두 줄 이상이거나 CA 파일이 없으면 기동을 멈춘다.

#### LAB data backup and recovery

LAB data root는 HOME Restic 범위 밖이다. 보존할 실험 data가 있으면 쓰기를 멈추고 LAB을 정지한 뒤
`${LAB_DATA_DIR}/open-webui/data` 전체(SQLite·upload·로컬 vector·`.webui_secret_key`)를 같은 시점으로
복사한다. 실행 중인 SQLite를 복사하지 않는다. 임베딩 모델을 바꾸면 재색인한다.

#### HOME retirement steps

이 source 이동은 실행 중인 HOME 컨테이너와 volume을 바꾸지 않았다. 아래 단계는 순서대로, 각각 별도 승인
아래에서만 실행한다.

1. **최종 backup**: 쓰기를 멈추고 HOME `open-webui`를 정지한 뒤 `${DEFAULT_AI_MODEL_DIR}/open-webui`의
   SQLite·upload·`.webui_secret_key`를 일관 backup한다. HOME Restic은 이 경로를 더 이상 포함하지 않는다.
2. **컨테이너 제거**: root include에서 빠졌으므로 `docker compose`가 아닌 정확한 이름으로 정지·제거한다
   (`docker stop open-webui`, `docker rm open-webui`). 이미지(약 16.5 GB) 제거도 별도 승인이다.
3. **volume 처리**: `hy-home-infra_open-webui`를 LAB data root로 이전할지, 보관할지, 삭제할지 소유자가
   정한다. 이전은 data를 `${LAB_DATA_DIR}/open-webui/data`로 복사하고 원본 checksum을 남긴다. 삭제는 되돌릴 수 없다.
4. **Keycloak client**: `home-openwebui` client를 LAB용으로 유지하며 LAB origin redirect를 등록할지,
   비활성화·삭제할지 정한다. HOME OpenBao의 `08-ai/open-webui` 출력과 `IAM-011`은 그 결정 전까지 유지한다.
5. **DNS·router**: Traefik router는 컨테이너 label이었으므로 컨테이너 제거와 함께 사라진다.
   `chat.${DEFAULT_URL}` DNS 기록과 인증서 SAN 정리는 별도 변경이다.

### Stop Conditions

예상 밖 출력, backup 누락, 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. 검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상과 다른 상태이면 중단하고 @buenhyden에게 넘긴다.

## Validation

### Service Checks

- [ ] `python3 scripts/operations/lab.py check open-webui` 성공
- [ ] lease 안에서 container-internal health 성공
- [ ] 승인된 경우 Keycloak 로그인, 모델 목록, 통제된 RAG 질의 성공
- [ ] 퇴역 단계마다 대상 상태와 backup checksum 기록

### Evidence

기록할 신호와 증거는 다음과 같다.

#### Observability and Evidence Sources

- **Signals**: LAB healthcheck 실패, 로그인 실패, 인덱싱 실패.
- **Evidence to Capture**: 비식별 로그 스니펫, 수행 명령과 결과, 퇴역 단계별 승인과 상태. 실패 검사와
  최종 상태는 관련 Task에 남긴다.

## Recovery

### Rollback

- LAB 문제는 `lab.py down open-webui`로 정지하고 data root를 보존한다.
- HOME으로 되돌리려면 [POL-0107](../../policies/15-labs/0107-lab-promotion.md) 승격 절차를 따른다. 퇴역
  단계 2 이전이라면 HOME 컨테이너는 아직 남아 있다.
- 격리 복원 rehearsal은 계획만 있고 실행되지 않았다. 복원 성공을 주장하지 않는다.

### Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상과 다른 상태이면 중단하고 @buenhyden에게 넘긴다.
정제된 증거, 시도한 단계와 현재 상태를 함께 전달한다.
