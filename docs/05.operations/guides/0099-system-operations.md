---
title: "System Operations Guide"
version: "0.1.0"
type: "operation/guide"
status: "review"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0099"
parent_ids:
- "POL-0006"
created: "2026-10-01"
---

# System Operations Guide

## Usage

### Reader purpose and boundaries

이 문서는 한 호스트에서 HOME 서비스와 개발 작업을 함께 운영하는 사람이
요청 경로, 공통 의존성, 장애 영향과 다음 절차를 이해하기 위한 설명이다.
목표는 필요한 선택과 점검을 찾는 것이며, 서비스 기동이나 복구 성공을 선언하는
것이 아니다. 구조와 단일 호스트 한계는 [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)이
소유한다. 실행 전에는 해당 서비스 Guide의 구현 경로와 Policy, Runbook을 확인한다.

[루트 Compose](../../../docker-compose.yml)는 파일 병합과 공통 network·secret
선언을, 각 fragment는 서비스 선택·mount·접속·의존 조건을 소유한다. 이 Guide는
서비스 소유권을 다시 등록하지 않는다. [역할 인덱스](README.md)에서 티어를
고른 뒤 subject 행의 세 역할을 따라간다. 서비스가 여러 개 묶인 subject의
초기화·exporter·worker도 같은 소유 문서에서 확인한다.

### Selection and readiness

HOME의 이름 있는 profile 조합, 각 selector의 목적과 동반 선택·제외 조건은
[POL-0078](../policies/0078-compose-profile-vocabulary.md#home-activation)이
소유한다. `core`만으로 AI와 workflow를 포함한 HOME 전체가 선택되지는 않는다.
DEV·OPTIONAL·LAB 분류와 실제 profile 이름을 혼동하지 않으며, 필요한 소비자가
있는 기능만 선택한다. update·IaC·backup·부하 작업은 해당 목적의 명시적 실행이다.

현재 root에 포함된 서비스는 모두 profile을 선언한다. profile과 서비스 대상을
모두 지정하지 않으면 서비스가 선택되지 않는다. 여러 profile은 합집합이며,
서비스를 직접 지정하면 profile을 켜지 않아도 그 서비스가 실행 대상이 될 수
있다. 따라서 좁은 profile만으로 실행 부수 효과를 차단했다고 보지 않는다.
선택 의미는 [Docker Compose 공식 설명](https://docs.docker.com/compose/how-tos/profiles/)과
POL-0078을 함께 확인한다. profile은 보안 격리나 별도 호스트가 아니다.

| 확인 수준 | 확인하는 사실 | 아직 증명하지 못하는 것 |
| --- | --- | --- |
| 정적 선택·구성 검증 | include, profile, 참조 경로와 선언된 의존성의 일관성 | 실제 mount, credential, 자원 여유, 애플리케이션 동작 |
| 초기화 작업 완료 | 대상 작업의 종료 코드와 완료 조건 | 이후 daemon의 가용성 또는 데이터 복구 |
| 컨테이너 실행·health | 각 소스가 정의한 검사 통과 | 인증·권한·업무 요청의 성공 |
| 인증된 기능 점검 | 허용 사용자와 대상 기능의 실제 결과 | 다른 기능, 부하 여유 또는 복구 가능성 |
| 보호된 백업과 격리 복원 | 명시한 범위·복구 시점의 복원 및 앱 검증 | 다른 데이터와 전체 호스트 장애 복구 |

티어 번호는 기동 순서가 아니다. 예를 들어 [Airflow](../../../infra/07-workflow/airflow/docker-compose.yml)는
`airflow-init`의 `service_completed_successfully`를, [Open WebUI](../../../infra/08-ai/open-webui/docker-compose.yml)는
Ollama의 `service_healthy`를 기다린다. 관리 DB·broker의 주소를 사용하는 것과
Compose의 `depends_on`으로 기동을 기다리는 것은 별개다. Keycloak과 OAuth2 Proxy,
workflow의 실제 관리 DB·broker 연결도 각 선언에서 확인한다. 조건 의미는
[Compose 기동 순서](https://docs.docker.com/compose/how-tos/startup-order/)를 따른다.
재부팅 뒤에는 [RUN-0098](../runbooks/0098-cold-start-and-reboot.md)의 단계별 확인을
사용하며, 이전 날짜의 리허설을 현재 상태의 증거로 대신하지 않는다.

### Request and authentication paths

브라우저의 서비스 도메인 요청은 호스트에 게시된 [Traefik](../../../infra/01-gateway/traefik/docker-compose.yml)
진입점으로 들어간다. [정적 설정](../../../infra/01-gateway/traefik/config/traefik.yml)의
웹 진입점은 TLS 진입점으로 전환하며, 명시적으로 활성화한 router가 `edge_net`의
앱으로 보낸다. 실제 hostname·port·인증 middleware는 대상 서비스의 labels와
[동적 middleware](../../../infra/01-gateway/traefik/dynamic/middleware.yml)가 결정한다.
모든 host 게시 포트가 이 경로를 통과하는 것은 아니다. 예를 들어 관리 PostgreSQL은
loopback, 관리 Valkey는 설정된 LAN 주소에 게시된다. 직접 접속도 서비스 Policy의
접근 경계를 확인한다. Nginx는 별도 선택 대안이며 ingress 중복은 POL-0078에서 다룬다.

- **Proxy 인증 경로**: n8n·ComfyUI처럼 SSO middleware를 붙인 요청은
  Traefik → OAuth2 Proxy의 인증 확인 → 앱으로 흐른다. 로그인은 Keycloak으로
  이동하고 OAuth2 Proxy callback으로 돌아온다. [OAuth2 Proxy 선언](../../../infra/02-auth/oauth2-proxy/docker-compose.yml)은
  기본 session 저장소를 관리 Valkey로 지정한다. 공통 middleware는 사용자 식별
  헤더만 전달하므로 이것만으로 앱 고유 권한이나 API token 인증을 대신하지 않는다.
- **앱 자체 로그인 경로**: Open WebUI와 Grafana는 Compose에 선언된 Keycloak
  OIDC/OAuth 설정을 사용한다. gateway 통과와 앱 내부 로그인·role 승인을 따로
  확인한다. 적용 차이는 [앱 인증 통합](0079-application-auth-integration.md),
  [Open WebUI](0057-open-webui.md), [Grafana](0041-grafana.md)가 소유한다.
- **인증의 데이터 의존성**: [Keycloak 선언](../../../infra/02-auth/keycloak/docker-compose.yml)은
  관리 PostgreSQL을 사용한다. 여러 앱의 로그인이 함께 실패하면 gateway만
  재시작하지 말고 Keycloak과 관리 DB, proxy 경로라면 Valkey까지 영향 범위를 좁힌다.

[OpenBao 선언](../../../infra/03-security/openbao/docker-compose.yml)의 healthcheck는
`bao status` 종료 코드 0과 2를 모두 허용한다. 공식 [status 설명](https://openbao.org/docs/2.6.x/commands/status/)에서
2는 sealed 상태다. Agent 검사는 token 파일의 비어 있지 않음만 확인한다.
따라서 두 컨테이너가 healthy여도 unseal·Agent 재인증·출력 갱신이 별도로 필요하다.
[Agent 설정](../../../infra/03-security/openbao/config/agent.hcl)의 출력 mount와
root Docker Secret 파일 소비 경로도 별개다. 자동 전달이나 모든 credential의
자동 회전을 추론하지 않는다. bootstrap·사람 로그인·SecretID 전달은
[OpenBao Runbook](../runbooks/0085-openbao.md), 재기동 연결은 RUN-0098이 소유한다.

### Data paths and shared resources

[관리 PostgreSQL·Valkey](../../../infra/04-data/mng-db/docker-compose.yml)는 인증과
workflow가 공유하는 상태·queue 기반이다. [Airflow](../../../infra/07-workflow/airflow/docker-compose.yml)는
PostgreSQL metadata, Valkey broker, DAG·plugin·log mount를 사용하고,
[n8n](../../../infra/07-workflow/n8n/docker-compose.yml)은 PostgreSQL과 queue broker,
worker·외부 runner를 함께 사용한다. UI가 열리는 것과 작업 완료는 다르다.
전용 Valkey 대안은 profile 추가만으로 연결이 바뀌지 않으며 HOST와 secret 매핑을
함께 검토한다. 이 공유 상태를 중단하면 여러 소비자에게 영향이 간다.

Open WebUI는 Ollama를 `ai_net`으로 호출하고 자체 데이터를 mount에 보존한다.
Qdrant는 별도 vector 저장소이며 `ai` 선택에 포함된다는 사실만으로 모든 앱의
검색 요청이 Qdrant를 거친다고 해석하지 않는다. [Ollama](../../../infra/08-ai/ollama/docker-compose.yml)와
[ComfyUI](../../../infra/08-ai/comfyui/docker-compose.yml)는 같은 호스트 GPU를
사용한다. Ollama의 병렬·적재·queue 설정과 ComfyUI 자원 선언은 동시 처리의
안전성을 증명하지 않는다. model·cache와 재생성 불가능한 입력·출력도 구분한다.

[SeaweedFS](../../../infra/04-data/seaweedfs/docker-compose.yml)의 master → volume·filer →
S3와 bucket 준비는 [Loki·Tempo](../../../infra/06-observability/docker-compose.yml)의
object 저장 경로와 [lakehouse](0094-lakehouse.md)의 기반이다. Loki·Tempo는 bucket
작업 성공을 기다리지만 이것만으로 과거 데이터 조회·보존·복구가 검증되지는 않는다.
메트릭·로그·가용성 신호는 같은 호스트와 저장소에 의존하므로 관측 장애와 앱
장애를 구분한다. Grafana 화면 하나의 실패를 전체 앱 장애로 확대하지 않는다.

호스트 전원·Docker daemon·디스크·GPU는 공통 실패 영역이다. mount와 engine별
보존 범위는 [백업 Policy](../policies/0021-backup-and-restore.md), network별 peer는
[0077](0077-ip-address-management.md)이 소유한다. 컨테이너 자원 상한은
[공통 template](../../../infra/common-optimizations.yml)과 서비스 override에서 읽는다.
같은 디스크의 복사본, 여러 컨테이너 또는 별도 profile은 물리적 장애 격리가 아니다.

### Tier responsibilities and impact

아래는 책임과 의존성 탐색표다. 서비스 명단이나 기동 순서를 다시 정의하지 않는다.
각 링크의 subject에서 구현·Policy·Runbook을 확인한다. 티어 안에서도 HOME과
선택 기능이 섞이므로 선택은 POL-0078에서 확인한다.

| 티어 | 운영 책임과 대표 subject | 주요 의존성과 장애 영향 |
| --- | --- | --- |
| 01 Gateway | [Traefik](0013-traefik.md), [Nginx 대안](0011-nginx.md): 도메인 요청 진입 | 인증 경로와 대상 앱의 network·readiness; ingress 실패는 여러 웹 앱에 영향 |
| 02 Auth | [Keycloak](0014-keycloak.md), [OAuth2 Proxy](0015-oauth2-proxy.md): 로그인과 세션 | 관리 PostgreSQL·Valkey, gateway·CA; 여러 앱 로그인에 공통 영향 |
| 03 Security | [OpenBao](0085-openbao.md): secret authority와 renderer | owner unseal·인증, 보존된 Raft·Agent 상태; healthy만으로 소비자 갱신 불명 |
| 04 Data | [관리 DB](0028-management-database.md), [객체 저장소](0024-seaweedfs.md), [Qdrant](0034-qdrant.md), [RedisInsight](0076-redisinsight.md) | 공유 상태와 선택적 DB 관리; 대상 데이터와 관리 UI 상태를 구분 |
| 05 Messaging | [Kafka](0036-kafka.md): 메시지·schema·connector | broker와 초기화; CDC 선택은 관리 DB 준비도 필요, 재처리 여부는 서비스 판단 |
| 06 Observability | [LGTM](0042-lgtm-stack.md), [Dozzle](0072-dozzle.md) | 공유 객체 저장소·host/GPU 가시성; Dozzle leaf는 기존 admin 선택 유지 |
| 07 Workflow | [Airflow](0050-airflow.md), [n8n](0053-n8n.md): 스케줄·작업 실행 | 관리 DB·broker·초기화·worker·runner; 화면 성공은 작업 성공이 아님 |
| 08 AI | [Ollama](0056-ollama.md), [Open WebUI](0057-open-webui.md), [ComfyUI](0081-comfyui.md), [Open Notebook](0073-open-notebook.md), [MLflow](0088-mlflow.md) | 추론·이미지·지식 앱·실험 상태; SurrealDB·관리 DB·객체 저장소·GPU 경계 |
| 09 Platform Operations | [Terrakube](0069-terrakube.md), [OpenTofu](0082-opentofu.md), [Registry](0065-registry.md), [Renovate](0083-renovate.md), [백업](0021-backup-and-restore.md) | IaC·아티팩트·의존성·공통 복구 작업; 공유 데이터 의존성 |
| 10 Communication | [Stalwart](0070-mail.md) | 내부 메일과 설정 helper; 외부 배달은 별도 범위 |
| 11 Quality | [성능 검사](0064-performance-testing.md), [SonarQube](0066-sonarqube.md), [WireMock](0092-wiremock.md), [Pact](0093-pact-broker.md), [Conftest](0095-conftest.md), [Mailpit](0084-mailpit.md) | 승인된 대상·합성 데이터·계약·정책 검사; 개발 캡처와 운영 메일 구분 |
| 12 Analytics | [Lakehouse](0094-lakehouse.md), [Superset](0097-superset.md), [dbt](0090-dbt.md), [JupyterLab](0089-jupyterlab.md) | 공유 객체·catalog·관리 DB와 명시적 분석 작업; 선택이 전체 파이프라인 기동을 뜻하지 않음 |

## Common Checks

| 운영 필요 | 공통 소유자와 점검 범위 | 확인되지 않았을 때의 경계 |
| --- | --- | --- |
| 기동·재부팅 | [RUN-0098](../runbooks/0098-cold-start-and-reboot.md), [선택 Policy](../policies/0078-compose-profile-vocabulary.md) | owner unseal·인증·각 앱 확인 없이 무인 복귀를 주장하지 않는다 |
| 인증·secret | [앱 인증 Policy](../policies/0079-application-auth-integration.md), [OpenBao Policy](../policies/0085-openbao.md) | route 통과, 사용자 권한, renderer 전달을 각각 확인; 미구현 통합은 @buenhyden이 구현 변경을 별도 결정 |
| 백업·복구 | [0021 Guide](0021-backup-and-restore.md), [Policy](../policies/0021-backup-and-restore.md), [Runbook](../runbooks/0021-backup-and-restore.md) | snapshot 존재·원격 copy·정적 검사만으로 전체 export·앱 복원 성공을 주장하지 않는다. 호환되는 격리 복원 증거가 없으면 @buenhyden과 해당 상태 소유자가 별도 리허설을 준비 |
| 버전·구성 변경 | [0086 Guide](0086-dependency-version-management.md), [Policy](../policies/0086-dependency-version-management.md), [Runbook](../runbooks/0086-dependency-version-management.md), [공통 적용 통제](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary) | 선언 pin과 실제 실행 버전은 별도; Git rollback은 DB migration rollback이 아님 |
| 용량·경합 | [공통 자원 통제](../policies/0006-infrastructure-optimization-governance.md), [저장소 진단](../runbooks/0035-storage-exhaustion.md), [GPU 진단](../runbooks/0055-gpu-recovery.md) | 자동 전체 부하 조정이나 용량 보장은 미검증; @buenhyden이 측정·대상별 제한 조정을 결정 |
| 여러 서비스 동시 장애 | [시스템 진단](../runbooks/0099-system-operations.md), [network Policy](../policies/0077-ip-address-management.md) | 공통 원인 후보를 구분한 뒤 기존 서비스 절차로 전달; 근거 없는 전체 restart·복원 금지 |

이 표가 공통 통제의 진입점이므로 별도 시스템 Policy는 두지 않는다. 실제 통제는
연결된 기존 Policy가 소유한다. 출력에는 secret 값, 인증 헤더·cookie, raw payload,
비공개 resolved path를 넣지 않는다. 읽지 않았거나 실행하지 않은 항목은 `NOT_RUN`으로
남긴다. source와 공식 문서 비교는 정적 근거이며 현재 운영·복구 결과가 아니다.

## Runbook Handoff

장애 원인이 여러 티어에 걸치면 [RUN-0099](../runbooks/0099-system-operations.md)의
관찰 → 분기 → 서비스 절차 흐름을 사용한다. 예정된 재부팅은 RUN-0098,
백업과 복원은 RUN-0021, 업데이트는 RUN-0086에서 시작한다. 인증·data·network
변경이나 파괴적 복구는 대상, 승인, 중단 조건을 해당 절차에서 다시 확인한다.

## Traceability

- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md): 시스템 구조와 단일 호스트 한계.
- [REQ-0027](../../01.requirements/0027-home-development-host.md): 운영 문서·검증·복구 요구.
- [루트 구현](../../../docker-compose.yml), [공통 template](../../../infra/common-optimizations.yml): 선언의 원본.
- [POL-0006](../policies/0006-infrastructure-optimization-governance.md), [POL-0078](../policies/0078-compose-profile-vocabulary.md): 공통 통제와 선택의 원본.

## Related Documents

- [Operations](../README.md), [서비스별 Guide](README.md), [정책](../policies/README.md), [절차](../runbooks/README.md)
- [Incident 탐색](../incidents/README.md): 실제 영향과 사건 증거 기록.
