# n8n Operations Policy

: Apache n8n (07-workflow)

---

## Overview (KR)

이 문서는 n8n 서비스의 안정적인 운영을 위한 정책과 통제 항목을 정의한다. 워크플로우 실행 이력 관리, 데이터 백업, 보안 자격 증명 관리 지침을 포함한다.

## Operational Controls

- **Resource Monitoring**: 워커(`n8n-worker`)의 CPU 및 메모리 사용량을 Grafana 알람을 통해 모니터링한다.
- **Data Retention**: 실행 이력(`Execution History`)은 DB 용량 관리를 위해 30일 경과 시 자동 삭제되도록 설정한다 (`EXECUTIONS_DATA_RETENTION_MAX_AGE_HOURS`).
- **Secret Rotation**: 외부 서비스용 `Credentials`는 분기별로 갱신을 권장하며, 변경 시 n8n UI를 통해 즉시 업데이트한다.

## Compliance and Security

- **Encryption**: `N8N_ENCRYPTION_KEY`는 Vault를 통해 관리되며, 유출 시 모든 저장된 자격 증명을 사용할 수 없게 되므로 엄격히 보호한다.
- **Access Control**: 관리자 계정에 대해 강력한 패스워드 정책을 적용하고, 필요한 경우에만 관리자 권한을 부여한다.
- **Workflow Integrity**: 프로덕션 워크플로우를 수정하기 전, 반드시 테스트 환경 또는 로컬에서 검증을 완료해야 한다.

## Maintenance and Updates

### Backup and Restore

- PostgreSQL 메타데이터 DB는 매일 자정에 스냅샷 백업을 수행한다.
- 주요 워크플로우는 `n8n-cli` 또는 UI의 `Export` 기능을 사용하여 주기적으로 JSON 백업을 수행한다.

### Version Upgrades

- n8n 이미지 업데이트 전, 현재 활성화된 워크플로우를 일시 중지하거나 작업이 없는 시간을 확인하여 진행한다.
- 업그레이드 후 `healthz` 엔드포인트를 통해 서비스 정상 여부를 확인한다.

## Exception Handling

- 긴급 장애 복구 상황에서는 `07.operations/07-workflow/n8n.md`의 절차를 따른다.
- 인프라 수준의 변경이 필요한 경우 `02-auth` 및 `04-data` 티어 담당자와 협의한다.

## Verification Checklist

- [ ] [ ] `docker compose ps` 상의 모든 서비스가 `healthy` 상태인가?
- [ ] [ ] n8n Web UI에 성공적으로 로그인이 가능한가?
- [ ] [ ] Prometheus 메트릭 엔드포인트(`:5678/metrics`)가 활성 상태인가?

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../07.operations/README.md](../../07.operations/README.md)

## Usage

> Migrated from `docs/07.operations/07-workflow/n8n.md` during the 2026-05-10 operations taxonomy consolidation.

### n8n System Usage

: Apache n8n (07-workflow)

---

#### Overview (KR)

이 가이드는 n8n 로우코드 자동화 시스템의 아키텍처, UI 접근 방식 및 핵심 운영 절차를 설명한다. n8n은 워크플로우를 노드 기반으로 시각화하여 설계하며, 외부 서비스와의 통합을 가속화하는 역할을 한다.

#### Architecture and Components

n8n은 확장성을 위해 분산형 큐 아키텍처를 사용하며, 주요 컴포넌트는 다음과 같다:

- **n8n Main**: 사용자 인터페이스(UI), API 서버, 워크플로우 엔진.
- **n8n Worker**: 대규모 비동기 작업 처리를 담당하는 작업 실행기.
- **n8nio/runners**: 특정 복잡한 연산을 격리 수행하여 메인 프로세스의 안정성을 확보.
- **Valkey Broker**: 메인과 워커 간의 메시지 전달을 위한 메시지 브로커.
- **Metadata DB**: 워크플로우 레시피 및 사용자 자격 증명(`Credentials`)을 저장하는 PostgreSQL 데이터베이스.

#### Access and Integration

- **Web UI**: `https://n8n.${DEFAULT_URL}` 에 접속하여 시각적으로 자동화 로직을 설계한다.
- **Public API**: 필요한 경우 `N8N_PUBLIC_API_BASE_URL`을 통해 프로그래밍 방식으로 워크플로우를 제어할 수 있다.
- **Webhook**: 외부 서비스로부터의 이벤트를 수신할 수 있도록 `WEBHOOK_URL`이 명시적으로 구성되어 있다.

#### Critical Procedures

##### 1. 워크플로우 배포 및 테스트

- 새 워크플로우 설계 시 `Manual Execution`으로 개별 노드의 데이터 입출력을 검증한다.
- 검증 완료 후 `Active` 모드로 전환하여 자동 실행되도록 설정한다.

##### 2. 자격 증명(Credentials) 관리

- 모든 인증 정보는 n8n 내부의 `Credentials` 탭에서 관리한다.
- 자격 증명은 메타데이터 DB에 암호화되어 저장되며, `N8N_ENCRYPTION_KEY`를 통해 보호된다.

##### 3. 노드 라이브러리 확장

- 필요한 경우 `./custom` 디렉터리에 사용자 정의 노드를 추가하여 엔진 기능을 확장할 수 있다.

#### Development and Verification

- **Local Runner**: 새로운 노드나 복잡한 JS 코드는 n8n 내부의 `Code` 노드에서 직접 실행하여 즉시 결과를 확인할 수 있다.
- **Instance Report**: `Admin > Settings`에서 인스턴스의 상태와 리소스 사용 현황을 모니터링한다.

#### Operational Controls

- **Resource Monitoring**: 워커(`n8n-worker`)의 CPU 및 메모리 사용량을 Grafana 알람을 통해 모니터링한다.

#### Known Limitations and Context

- 대규모 병렬 데이터 처리가 필요한 경우 Airflow 사용을 권장하며, n8n은 주로 API 기반의 경량 연동 자동화에 활용한다.
- 워크플로우가 너무 많은 노드를 포함할 경우 `Sub-workflows`로 분리하여 유지보수성을 높여야 한다.

#### AI Agent Guidance

1. **Modularization**: 복잡한 로직은 `Sub-workflows`를 활용하여 분리하고 재사용성을 확보하십시오.

#### Appendix: Links

- ARD: [07-workflow Architecture](../../02.ard/0007-workflow-architecture.md)
- Recovery: [n8n Recovery Procedure](../../07.operations/07-workflow/n8n.md)
- Specialized Usage: [02.n8n-automation.md](./02.n8n-automation.md) (Detailed usage)

---

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../07.operations/README.md](../../07.operations/README.md)

## Procedure

> Migrated from `docs/07.operations/07-workflow/n8n.md` during the 2026-05-10 operations taxonomy consolidation.

### n8n Recovery Procedure

: Apache n8n (07-workflow)

---

#### Overview (KR)

이 런북은 n8n 서비스 장애 발생 시 운영자가 신속하게 서비스를 복구하기 위한 단계별 절차를 제공한다. 워커 중단, 데이터베이스 연결 오류, 암호화 키 분실 등 주요 장애 시나리오에 대응한다.

#### Purpose

- n8n 서비스의 가용성 조기 회복
- 자동화 워크플로우 중단 시간 최소화
- 시스템 정상 작동 여부 검증

#### Canonical References

- ARD: [07-workflow Architecture](../../02.ard/0007-workflow-architecture.md)
- Usage: [n8n System Usage](../../07.operations/07-workflow/n8n.md)
- Policy: [n8n Operations Policy](../../07.operations/07-workflow/n8n.md)

#### When to Use

- n8n UI 접근 시 "Connection lost" 또는 50x 에러가 발생할 때.
- 워크플로우가 실행되지 않고 `Pending` 또는 `Waiting` 상태에 멈춰 있을 때.
- 워커 컨테이너가 반복적으로 재시작(`Restarting`)될 때.

#### Procedure or Checklist

##### Checklist

- [ ] [ ] `docker compose ps` 결과 모든 n8n 서비스가 `Up` 인가?
- [ ] [ ] `n8n-valkey` 서비스가 정상이며 워커가 연결되어 있는가?
- [ ] [ ] `n8n_db_password` 시크릿이 올바르게 로드되었는가?

##### Procedure

###### 시나리오 1: 워커 노드 중단 (Worker Down)

1. 워커 로그 확인: `docker compose logs --tail=50 n8n-worker`
2. 워커 재시작: `docker compose restart n8n-worker`
3. Valkey 큐 상태 확인: `docker compose exec n8n-valkey valkey-cli info keyspace`

###### 시나리오 2: 데이터베이스 연결 오류

1. DB 호스트(`POSTGRES_MNG_HOSTNAME`)가 가용한지 확인.
2. n8n 메인 서비스 재시작: `docker compose restart n8n`
3. 시크릿 파일 권한 확인: `docker compose exec n8n ls -l /run/secrets/n8n_db_password`

###### 시나리오 3: 텐서플로우/Task Runner 오류

1. Task Runner 로그 확인: `docker compose logs n8n-task-runner`
2. Task Runner 재시작: `docker compose restart n8n-task-runner`

#### Verification Steps

- [ ] `https://n8n.${DEFAULT_URL}/healthz` 호출 시 `200 OK` 응답 확인.
- [ ] UI 로그인 후 `Executions` 탭에서 최근 작업의 성공 여부 확인.

#### Observability and Evidence Sources

- **Signals**: Grafana n8n Dashboard (Error Rate), Valkey Queue Depth.
- **Evidence**: `docker compose logs --tail=100 n8n`, `n8n-worker`.

#### Safe Rollback or Recovery Procedure

- [ ] 서비스를 재시작하기 전, `database` 볼륨의 데이터 유실 가능성이 낮으므로 안심하고 재시작을 시도하십시오.
- [ ] 만약 `N8N_ENCRYPTION_KEY`가 변경되어 이전 데이터 복호화가 불가능한 경우, 이전 키로 롤백하거나 자격 증명을 재설정해야 합니다.

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../10.incidents/README.md](../../10.incidents/README.md)
