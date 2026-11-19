---
title: "Open WebUI Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0057"
parent_ids:
- "GDE-0057"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Open WebUI Runbook

## Trigger and Scope

### Trigger

이 런북은 독립 LAB `labs/open-webui/docker-compose.yml`(profile `lab-open-webui`)의 준비·기동·장애 대응과,
2026-11-10 ADR-0062 개정으로 HOME에 남은 Open WebUI 컨테이너·volume의 퇴역 절차를 다룬다.

- LAB을 lease 안에서만 기동하고 정리한다.
- HOME 잔여 상태를 승인 단계별로 퇴역한다.
- 같은 장애가 반복될 때 일관된 증적을 남긴다.

- LAB 실험 준비 또는 `lab.py check open-webui` 실패.
- LAB 로그인 실패, 모델 목록 미표시, RAG 인덱싱 실패, healthcheck 실패.
- HOME 퇴역 단계 중 하나가 승인됨.

### Targets

> 범위: Open WebUI LAB과 HOME 잔여 상태

- Declared parent: [Open WebUI Usage Guide](../../01.guides/15.labs/0057-open-webui.md) (`GDE-0057`)
- Governing decision: [ADR-0062](../../../02.architecture/02.decisions/0062-home-lab-membership.md)
- Subject peers: [Guide](../../01.guides/15.labs/0057-open-webui.md) (`GDE-0057`), [Policy](../../02.policies/15.labs/0057-open-webui.md) (`POL-0057`)

- [Operations index](../../README.md)
- [Usage guide](../../01.guides/15.labs/0057-open-webui.md)
- [Operations policy](../../02.policies/15.labs/0057-open-webui.md)

## Preflight

### Authority

LAB과 HOME 명령의 실행 경계와 승인 조건은 다음과 같다.

#### Execution Boundary

LAB 명령은 `python3 scripts/operations/lab.py`의 목적·lease·충돌·예산 규칙을 따른다. `down`은 `-v` 없이
그 LAB project만 정지한다. HOME 명령은 이 런북의 퇴역 단계가 각각 승인된 경우에만 실행한다. 예상 밖 출력,
backup 누락, 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. 공통 절차는
[LAB 승격](0107-lab-promotion.md), [백업](../10.platform-and-backup/0021-backup-and-restore.md),
[계정](../03.identity-and-access/0014-keycloak.md), [gateway·인증서](../02.gateway-and-networking/0013-traefik.md)가 소유한다.

### Environment

기동 전 확인할 LAB 설정, 비밀 파일 이름, data 경로 전제는 다음과 같다.

#### Service lifecycle prerequisites

- `labs/.env`에 `LAB_DATA_DIR`, `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`, `LAB_OPEN_WEBUI_DEFAULT_URL`,
  `LAB_OPEN_WEBUI_CA_FILE`이 있고, 소유자가 LAB network에서 도달 가능한 Ollama endpoint를 승인했다.
- `${LAB_SECRET_DIR}/open-webui/oidc_client_secret.txt`(`LAB-037`) LAB 사본이 별도 승인으로 준비되었다.
  값은 출력하거나 증거로 남기지 않는다.
- `${LAB_DATA_DIR}/open-webui/data`가 있고 HOME data 경로와 겹치지 않는다.
- LAB origin redirect의 Keycloak 등록 여부를 확인했다. 등록 전에는 로그인 성공을 주장하지 않는다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | LAB start and triage: `lab.py check open-webui` 실행 | `python3 scripts/operations/lab.py check open-webui` 성공 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | LAB start and triage: 활성 lease에서 LAB project 로그와 container-internal health 확인 | lease 안에서 container-internal health 성공 (health는 로그인/RAG의 증거가 아님) | 예상 밖 출력이면 중단하고 @buenhyden에게 escalation |
| 3 | LAB data backup and recovery: 쓰기를 멈추고 LAB 정지 후 `${LAB_DATA_DIR}/open-webui/data` 전체를 같은 시점으로 복사 | 문서에 기록 없음 | 실행 중인 SQLite는 복사하지 않으며, backup 누락 시 중단하고 @buenhyden에게 escalation |
| 4 | HOME retirement steps: 승인된 Docker context에서 HOME project/service label이 맞는 컨테이너 ID 확인 | 결과가 정확히 하나일 때만 그 ID를 사용 | 이름만 같거나 label이 없거나 후보가 없으면 중단 |
| 5 | HOME retirement steps - 최종 backup: HOME 컨테이너 정지 후 SQLite/upload/`.webui_secret_key`를 일관 backup | 퇴역 단계마다 대상 상태와 backup checksum 기록 | backup 누락 시 중단하고 @buenhyden에게 escalation |
| 6 | HOME retirement steps - 컨테이너 제거: HOME ID 재확인 후 컨테이너 제거 (이미지 제거는 별도 승인) | 퇴역 단계마다 대상 상태 기록 | 승인되지 않은 부작용이면 중단하고 @buenhyden에게 escalation |
| 7 | HOME retirement steps - volume 처리: `hy-home-infra_open-webui`의 이전/보관/삭제를 소유자가 결정 | 이전 시 원본 checksum을 남김 | 삭제는 되돌릴 수 없으므로 소유자 결정 전에는 중단 |
| 8 | HOME retirement steps - Keycloak client: `home-openwebui` client를 LAB용으로 유지하거나 비활성화/삭제 결정 | 문서에 기록 없음 | 결정 전까지 HOME OpenBao `08-ai/open-webui` 출력과 `IAM-011` 유지 |
| 9 | HOME retirement steps - DNS/router: `chat.${DEFAULT_URL}` DNS 기록과 인증서 SAN 정리는 별도 변경 | Traefik router는 컨테이너 제거와 함께 사라짐 | 별도 변경으로 분리하며 예상 밖 상태면 중단하고 @buenhyden에게 escalation |

LAB 기동·점검과 데이터 보존, HOME 퇴역 단계는 다음 순서를 따른다.

#### LAB start and triage

```bash
python3 scripts/operations/lab.py check open-webui
```

활성 lease와 승인된 Docker context에서 LAB project를 명시해 진단한다. `LAB_ENV_FILE`은
그 lease를 시작할 때 사용한 LAB 환경 파일의 경로다.

```bash
docker compose --project-name hy-home-lab-open-webui --env-file "$LAB_ENV_FILE" -f labs/open-webui/docker-compose.yml --profile lab-open-webui logs --tail 200 open-webui
docker compose --project-name hy-home-lab-open-webui --env-file "$LAB_ENV_FILE" -f labs/open-webui/docker-compose.yml --profile lab-open-webui exec -T open-webui curl -f http://localhost:8080/health
```

health는 로그인·RAG의 증거가 아니다. 승인된 lease 안에서 Keycloak 로그인, 모델 목록, 통제된 RAG 질의를
따로 확인한다. entrypoint는 secret이 비었거나 두 줄 이상이거나 CA 파일이 없으면 기동을 멈춘다.

#### LAB data backup and recovery

LAB data root는 HOME Restic 범위 밖이다. 보존할 실험 data가 있으면 쓰기를 멈추고 LAB을 정지한 뒤
`${LAB_DATA_DIR}/open-webui/data` 전체(SQLite·upload·로컬 vector·`.webui_secret_key`)를 같은 시점으로
복사한다. 실행 중인 SQLite를 복사하지 않는다. 임베딩 모델을 바꾸면 재색인한다.

#### HOME retirement steps

이 source 이동 당시 HOME 컨테이너와 volume은 퇴역 대기였다. 현재 host 상태는 별도 승인으로 확인한다.
LAB도 같은 `open-webui` 컨테이너 이름을 사용한다. 정지·제거 전 승인된 Docker context에서 HOME
project와 service label이 모두 맞는 컨테이너를 찾고 ID를 확인한다.

```bash
docker ps -aq --no-trunc --filter 'label=com.docker.compose.project=hy-home-infra' --filter 'label=com.docker.compose.service=open-webui' --filter 'name=^/open-webui$'
```

결과가 정확히 하나일 때만 그 ID를 아래 단계의 `HOME_OPEN_WEBUI_ID`로 사용한다. 이름만 같거나 label이
없거나 후보가 없으면 중단한다. 아래 단계는 순서대로, 각각 별도 승인 아래에서만 실행한다.

1. **최종 backup**: 쓰기를 멈추고 `docker stop "$HOME_OPEN_WEBUI_ID"`로 HOME 컨테이너를 정지한 뒤
   `${DEFAULT_AI_MODEL_DIR}/open-webui`의 SQLite·upload·`.webui_secret_key`를 일관 backup한다.
   HOME Restic은 이 경로를 더 이상 포함하지 않는다.
2. **컨테이너 제거**: root include에서 빠졌으므로, 앞에서 정지한 HOME ID를 재확인한 뒤
   `docker rm "$HOME_OPEN_WEBUI_ID"`를 실행한다. 이미지 제거도 별도 승인이다.
3. **volume 처리**: `hy-home-infra_open-webui`를 LAB data root로 이전할지, 보관할지, 삭제할지 소유자가
   정한다. 이전은 data를 `${LAB_DATA_DIR}/open-webui/data`로 복사하고 원본 checksum을 남긴다. 삭제는 되돌릴 수 없다.
4. **Keycloak client**: `home-openwebui` client를 LAB용으로 유지하며 LAB origin redirect를 등록할지,
   비활성화·삭제할지 정한다. HOME OpenBao의 `08-ai/open-webui` 출력과 `IAM-011`은 그 결정 전까지 유지한다.
5. **DNS·router**: Traefik router는 컨테이너 label이었으므로 컨테이너 제거와 함께 사라진다.
   `chat.${DEFAULT_URL}` DNS 기록과 인증서 SAN 정리는 별도 변경이다.

### Stop Conditions

예상 밖 출력, backup 누락, 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. 검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상과 다른 상태이면 중단하고 @buenhyden에게 넘긴다.

## Verification

### Expected Results

#### Service Checks

- [ ] `python3 scripts/operations/lab.py check open-webui` 성공
- [ ] lease 안에서 container-internal health 성공
- [ ] 승인된 경우 Keycloak 로그인, 모델 목록, 통제된 RAG 질의 성공
- [ ] 퇴역 단계마다 대상 상태와 backup checksum 기록

#### Evidence

기록할 신호와 증거는 다음과 같다.

#### Observability and Evidence Sources

- **Signals**: LAB healthcheck 실패, 로그인 실패, 인덱싱 실패.
- **Evidence to Capture**: 비식별 로그 스니펫, 수행 명령과 결과, 퇴역 단계별 승인과 상태. 실패 검사와
  최종 상태는 관련 Task에 남긴다.

### Unverified Conditions

이 runbook이 아직 관찰하지 못한 항목은 다음과 같다. 퇴역 단계는 각각 별도 승인 아래에서만 실행하도록 되어 있다.

- `lab.py check open-webui`와 container-internal health: 이 문서에는 실행 결과가 기록되어 있지 않다. 활성 lease에서 두 확인의 성공이 관찰되면 검증된다.
- Keycloak 로그인, 모델 목록, 통제된 RAG 질의: 문서가 health는 이들의 증거가 아니라고 밝히며 별도 확인을 요구한다. 승인된 lease 안에서 각 항목의 성공이 관찰되면 검증된다.
- LAB data backup과 복구: 실행 결과가 기록되어 있지 않다. backup 세트의 checksum과 복원 후 data 확인이 관찰되면 검증된다.
- HOME 퇴역 5단계(최종 backup, 컨테이너 제거, volume 처리, Keycloak client, DNS/router): 단계별 승인이 필요하며 실행 결과가 기록되어 있지 않다. 단계별 대상 상태와 backup checksum 기록이 관찰되면 검증된다. 문서는 현재 host 상태를 별도 승인으로 확인하라고 한다.

## Escalation

### Next Owner

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상과 다른 상태이면 중단하고 @buenhyden에게 넘긴다.
정제된 증거, 시도한 단계와 현재 상태를 함께 전달한다.

### Recovery or Forward Repair

- LAB 문제는 `lab.py down open-webui`로 정지하고 data root를 보존한다.
- HOME으로 되돌리려면 [POL-0107](../../02.policies/15.labs/0107-lab-promotion.md) 승격 절차를 따른다. 복구 후보인
  기존 HOME 컨테이너가 있는지는 HOME retirement steps의 project·service·ID 확인을 사용한다.
- 격리 복원 rehearsal은 계획만 있고 실행되지 않았다. 복원 성공을 주장하지 않는다.
