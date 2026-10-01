---
title: "System Operations Diagnostic Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0099"
parent_ids:
- "GDE-0099"
created: "2026-10-01"
---

# System Operations Diagnostic Runbook

## When to Use

여러 앱의 접속·로그인·작업·저장이 함께 실패하거나, 앱과 관측 화면의 장애가
같은 원인인지 모를 때 사용한다. 공유 host·gateway·인증·DB·broker·객체 저장소
후보를 좁히고 기존 서비스 Runbook으로 전달하는 읽기 전용 진단이다.
예정된 재부팅 또는 재부팅 직후의 정해진 확인은
[RUN-0098](0098-cold-start-and-reboot.md)이 소유한다.

운영 checkout과 실제 Docker context를 알고, 대상 daemon의 읽기 권한이 있는
운영자가 저장소 루트에서 실행한다. 승인 범위가 문서·정적 검증뿐이면 아래
runtime 명령을 실행하지 않고 `NOT_RUN`으로 남긴다. 이 절차 자체는 restart,
unseal, credential 발급, 설정 변경, 복원, cleanup 또는 부하 생성을 승인하지
않는다. 영향 범위는 관찰 대상뿐이며 앱 데이터와 인증정보는 읽거나 출력하지 않는다.

## Procedure

### 1. Confirm scope before diagnosis

관찰 시각과 시간대, 처음 실패한 기능, 영향받은 앱, 여전히 되는 기능, 마지막
승인 변경·재부팅 여부를 기록한다. 사용자가 실패했다고 알린 경로와 수집기가
실패한 경로를 구분한다. 기존 운영 기록에서 선택 profile을 확인하고
[POL-0078](../policies/0078-compose-profile-vocabulary.md)에 대조한다.
원문 `.env`, secret 파일, 전체 rendered Compose를 출력해 선택을 확인하지 않는다.

```bash
docker context show
docker ps -a --filter label=com.docker.compose.project=hy-home-infra --format '{{.Names}} {{.Status}}'
```

첫 명령의 context가 승인된 대상과 다르거나 알 수 없으면 멈춘다. 두 번째 명령은
[root project](../../../docker-compose.yml)의 컨테이너 이름과 상태만 보여준다.
목록이 비었다고 서비스가 제거되었다고 판단하지 않는다. context·실행 checkout·
기존 선택을 @buenhyden에게 확인한다. Docker API가 응답하지 않으면 반복적인
재시작이나 앱별 복구를 시작하지 말고 host/daemon 범위로 전달한다.

`Exited (0)`인 초기화 작업은 성공 종료일 수 있다. daemon의 `Up`과 초기화 작업
완료는 구분하며, 선택하지 않은 OPTIONAL/LAB 서비스가 없다는 것은 장애가 아니다.
기존 선택에 있어야 하는 서비스가 없거나 초기화 작업이 실패했으면 해당 Guide에서
구현과 작업 종류를 확인한 뒤 그 서비스 절차로 전달한다.

### 2. Compare the shared dependency boundary

아래 대상은 root의 접근·인증·관리 상태 기반이다. 실제 선택과 1단계 목록에
있는 이름만 대상으로 확인한다. 목록에 없는 이름은 명령에서 제외하고 누락을
증거로 기록한다. 상태 정보만 출력하며 전체 inspect나 healthcheck 원문 로그는
출력하지 않는다.

```bash
docker inspect --format '{{.Name}} state={{.State.Status}} health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}} oom={{.State.OOMKilled}} restarts={{.RestartCount}}' traefik keycloak oauth2-proxy mng-pg mng-valkey openbao openbao-agent
```

정상 daemon의 기대값은 `state=running`, 선언된 healthcheck의 통과,
`oom=false`다. `health=none`은 검사 성공이 아니다. restart 수는 누적값이므로
한 번의 값만으로 현재 반복 실패를 단정하지 않고 기존 기록과 비교한다.
OpenBao와 Agent의 `healthy`는 unseal·인증·렌더링 성공을 증명하지 않는다.
각 소스가 정의한 한계는 [시스템 Guide](../guides/0099-system-operations.md#request-and-authentication-paths)에서 확인한다.

### 3. Choose the next owner from the observed symptom

아래 관찰은 이미 승인된 상태 조회나 운영자가 보고한 결과만 사용한다. 표에
있다는 이유로 새 로그인, API 호출, 데이터 쓰기 또는 테스트 작업을 실행하지
않는다. 한 증상이 여러 행에 해당하면 공유 의존성과 영향을 함께 기록한다.

| 관찰한 증상 | 먼저 비교할 안전한 관찰 | 분기와 기존 절차 |
| --- | --- | --- |
| 여러 웹 도메인 모두 실패 | Docker 응답, Traefik 상태, 보고된 TLS·접속 실패 범위 | daemon부터 응답하지 않으면 host owner에게 전달. gateway만 실패하면 [Traefik](0013-traefik.md); Nginx 대안을 선택했다면 [Nginx](0011-nginx.md). 포트 충돌·network 의문은 [0077](0077-ip-address-management.md) |
| 웹은 열리나 여러 로그인이 실패·반복 | Keycloak·관리 DB 상태; proxy 경로인지 앱 자체 로그인인지 | Keycloak/DB 이상이면 [Keycloak](0014-keycloak.md)과 [관리 DB](0028-management-database.md). proxy 경로만 실패하면 Valkey와 [OAuth2 Proxy](0015-oauth2-proxy.md). 한 앱의 권한 실패만 있으면 [앱 인증 통합](../guides/0079-application-auth-integration.md)을 거쳐 해당 앱 Runbook |
| 재부팅 뒤 secret 의존 기능 실패, OpenBao는 healthy | sealed 여부와 Agent 인증·출력 갱신의 기존 확인 기록 | 기록이 없거나 실패하면 healthy로 통과하지 않는다. [RUN-0098](0098-cold-start-and-reboot.md)에서 [OpenBao](0085-openbao.md) owner-run 단계로 전달; SecretID·token을 여기서 읽지 않음 |
| Airflow·n8n 화면은 열리나 작업 정체 | 관리 DB·Valkey 상태, 초기화 작업 종료, 해당 worker/runner 상태 | 공유 기반 이상이면 [관리 DB](0028-management-database.md), 한 작업 경로만 실패하면 [Airflow](0050-airflow.md) 또는 [n8n](0053-n8n.md); 재실행·queue 삭제는 선택하지 않음 |
| Loki·Tempo 또는 lakehouse가 함께 저장·조회 실패 | SeaweedFS 각 daemon과 bucket 작업 상태; 해당 서비스의 기존 실패 신호 | 공통 S3 기반 이상이면 [SeaweedFS](0024-seaweedfs.md), 그 외 [Loki](0043-loki.md), [Tempo](0049-tempo.md), [lakehouse](0094-lakehouse.md). 저장소 여유 부족 징후는 [용량 진단](0035-storage-exhaustion.md) |
| GPU 작업과 앱 응답이 함께 느려짐·OOM | 기존 host/GPU 대시보드, 컨테이너 OOM 상태, 동시 실행 중인 작업 범위 | host 메모리·디스크도 함께 부족하면 공통 자원 영향으로 전달. GPU에 한정되면 [GPU](0055-gpu-recovery.md), [Ollama](0056-ollama.md), [ComfyUI](0081-comfyui.md); 추가 benchmark나 GPU reset을 하지 않음 |
| 대시보드만 실패하거나 여러 수집 신호가 사라짐 | 사용자가 보고한 앱 상태와 collector·backend 상태의 차이 | 관측 장애 후보로 [Grafana](0041-grafana.md), [Prometheus](0045-prometheus.md), [Alloy](0040-alloy.md), [Gatus](0087-gatus.md)에 전달. 같은 호스트 관측 실패를 앱 가용성 성공·실패로 단정하지 않음 |
| 백업 실패 또는 변경 직후 여러 기능 실패 | 승인 변경 경로, 백업 전체 실행 종료 상태와 단계별 요약, 복원 증거 존재 여부 | 백업은 [0021](0021-backup-and-restore.md), 버전은 [0086](0086-dependency-version-management.md), mount 반영은 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary). snapshot 존재만으로 전체 성공을 판단하지 않음 |

### 4. Verify the handoff boundary

선택한 서비스 Runbook의 전제·승인·중단 조건을 확인하고, 그 절차의 읽기 전용
진단까지만 현재 권한으로 이어간다. 조건이 불명확하거나 실제 관찰이 절차의
기대값과 다르면 중단한다. source에 없는 격리 환경·복구 도구·credential을
만들어 절차를 맞추지 않는다.

별도 승인된 복구 뒤에는 원래 실패했던 사용자 기능과 영향받은 공통 의존성을
다시 확인한다. 컨테이너 healthy만으로 종료하지 않으며, 확인하지 않은 기능과
data integrity·복원 가능성은 미검증으로 남긴다.

## Evidence

현재 Task 또는 실제 사건의 [Incident](../incidents/README.md)에 시각·시간대,
source revision, 대상 context·선택의 확인 여부, 영향·정상 기능, 최소 상태 요약,
선택한 분기·Runbook, 중단 사유와 다음 책임자를 기록한다. 명령마다 종료 상태와
`PASS`/`FAIL`/`NOT_RUN`을 구분하고, 장애 원인 후보는 확정 사실과 분리한다.
원문 로그, secret 값, 인증 헤더·cookie, 사용자 데이터, 비공개 경로는 첨부하지 않는다.

## Rollback or Recovery

읽기 전용 진단은 runtime 상태를 변경하지 않아 되돌릴 조치가 없다. 복구·rollback은
위 표의 해당 서비스 Runbook과 승인된 Task가 소유한다. 공통 장애라는 이유로
전체 Compose 재기동, volume 삭제, queue replay 또는 이전 이미지로의 DB
다운그레이드를 선택하지 않는다. 검증된 격리 복원 경로가 없으면 복원 불가/미검증
상태를 보존하고 별도 작업으로 넘긴다.

## Escalation

Docker 대상 불명, 여러 HOME 기능의 지속 장애, 반복 OOM, 공유 저장소 쓰기 실패,
인증 우회·secret 노출 징후, 필수 복원 증거 부재, 또는 승인된 절차와 실제 상태의
불일치는 @buenhyden에게 전달한다. 새로운 팀이나 SLA를 가정하지 않는다.
영향받은 기능, 관찰 시각, 마지막 변경, 공통 원인 후보, 해당 Runbook, 미검증
항목과 필요한 승인만 전달하며 사건 기록은 기존 Incident 구조를 사용한다.

## Traceability

- [GDE-0099](../guides/0099-system-operations.md): 사용자·데이터 경로와 공통 의존성.
- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md): 호스트 구조와 실패 영역.
- [POL-0006](../policies/0006-infrastructure-optimization-governance.md), [POL-0078](../policies/0078-compose-profile-vocabulary.md): 공통 통제와 선택.

## Related Documents

- [전체 Runbook](README.md), [Operations](../README.md)
- [기동·재부팅](0098-cold-start-and-reboot.md), [백업·복구](0021-backup-and-restore.md), [network](0077-ip-address-management.md), [버전 변경](0086-dependency-version-management.md)
