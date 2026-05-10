# Management Database Operations Policy

> This document defines policy, controls, and approval rules for the mng-db system.

---

## Overview (KR)

이 문서는 `mng-db` (Management Database)에 대한 운영 정책을 정의한다. 플랫폼 핵심 메타데이타의 보호와 가용성을 유지하기 위한 통제 기준 및 검증 방법을 규정한다.

## Policy Scope

이 정책은 `infra/04-data/operational/mng-db` 및 해당 서비스가 제공하는 모든 논리적 데이타베이스(n8n, keycloak, airflow 등)를 대상으로 한다.

## Applies To

- **Systems**: mng-pg, mng-valkey, mng-pg-init
- **Agents**: AI Agent (자동화 관리 및 메타데이터 접근 시)
- **Environments**: 모든 구현 및 운영 환경 (dev, staging, prod)

## Controls

- **Required**:
  - 모든 패스워드는 `/run/secrets/`를 통해 주입되어야 한다.
  - 정기적인 연결 상태 점검(`pg_isready`)을 수행해야 한다.
- **Allowed**:
  - `01-gateway` 계층에서의 읽기 권한을 허용한다.
  - 메타데이타 백업 시 `shared_net`을 통한 비 HA 전송을 허용한다.
- **Internal Only**: 외부 IP에서의 직접 접근은 엄격히 금지됩니다.
- **Credential Rotation**: 90일 주기로 Secrets 변경 수행.
- **Audit Logging**: DDL 변경 사항에 대한 로그 보존 (180일).
- **Disallowed**:
  - 대규모 비즈니스 데이타의 직접 저장을 금지한다.
  - 허가되지 않은 계정의 `postgres` 루트 DB 직접 접근을 금지한다.

## Exceptions

- 긴급 복구 작업은 사후 승인 기록을 남긴다.

## Related Documents

- **Procedure**: [mng-db.md](./mng-db.md)
- **Plan**: [2026-03-26-04-data-standardization.md](../../../../04.execution/plans/2026-03-26-04-data-standardization.md)

Copyright (c) 2026. Licensed under the MIT License.

---

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

## Usage

> Migrated from `docs/05.operations/04-data/operational/mng-db.md` during the 2026-05-10 operations taxonomy consolidation.

### Management Database (mng-db) Usage

> This document explains how to understand and use the Management Database system.

---

#### Overview (KR)

이 문서는 `mng-db` (Management Database) 시스템에 대한 가이드다. `mng-db`는 플랫폼 핵심 서비스(Identity, Automation, Workflow 등)의 메타데이타를 관리하는 PostgreSQL 및 Valkey 인스턴스로 구성되어 있다.

#### Usage Type

`system-guide`

#### Target Audience

- **Developers**: 플랫폼 서비스 개발 및 DB 연동
- **Operators**: 초기 부트스트랩 및 서비스 상태 가이드 점검
- **AI Agents**: 하위 시스템 의존성 분석

#### Purpose

이 가이드는 사용자가 `mng-db`의 구조를 이해하고, 제공되는 각 데이타베이스에 안전하게 연결 및 활용하는 것을 돕는다.

#### Prerequisites

- **Docker & Docker Compose**: 로컬 또는 인프라 노드에서 실행 환경 필요.
- **psql / valkey-cli**: 데이타베이스 접속을 위한 클라이언트 도구.
- **Credentials**: `/run/secrets/` 또는 환경 변수에 설정된 패스워드 정보.

#### Step-by-step Instructions

##### 1. 서비스 가동 및 상태 확인

`mng-db`는 플랫폼 초기화 시 가장 먼저 가동되어야 하는 서비스 중 하나이다.

```bash
### infra/04-data/operational/mng-db 경로에서 실행
docker-compose up -d
docker-compose ps
```

##### 2. PostgreSQL 데이타베이스 접근

`mng-pg` 인스턴스 내에는 다음과 같은 논리적 데이타베이스가 생성된다.

- `postgres`: 관리용 루트 DB
- `n8n`: 워크플로우 자동화용
- `keycloak`: 자격 증명 관리용
Copyright (c) 2026. Licensed under the MIT License.

---

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../README.md)
- [../../05.operations/README.md](../../../README.md)
- [../../05.operations/README.md](../../../README.md)

## Procedure

> Migrated from `docs/05.operations/04-data/operational/mng-db.md` during the 2026-05-10 operations taxonomy consolidation.

### Management Database (mng-db) Procedure

: Infrastructure Recovery and Maintenance

---

#### Overview (KR)

이 런북은 `mng-db` (Management Database)의 가동, 초기화, 건강 상태 점검 및 긴급 복구 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 명령어와 검증 단계를 제공한다.

#### Purpose

`mng-db` 서비스의 부재로 인해 상위 관리 서비스(auth, automation 등)가 기동되지 않을 때의 복구 및 사후 관리를 목적으로 한다.

#### Canonical References

- **ARD**: [../02.architecture/requirements/0004-data-architecture.md](../../../../02.architecture/requirements/0004-data-architecture.md)
- **Spec**: [../03.specs/04-data/spec.md](../../../../03.specs/04-data/spec.md)
- **Repo**: `infra/04-data/operational/mng-db/`

#### When to Use

- 초기 플랫폼 설치 및 부트스트랩 시
- 관리용 DB 또는 캐시 서비스의 불능(unhealthy) 상태 발생 시
- 신규 플랫폼 서비스 추가로 인한 DB 초기화(`mng-pg-init`)가 필요할 때

#### Procedure or Checklist

##### Checklist

- [ ] `infra_net` 네트워크가 생성되어 있는가?
- [ ] `/run/secrets/` 하위에 필수 비밀번호 파일들이 존재하는가?
- [ ] `${DEFAULT_MANAGEMENT_DIR}` 데이터 볼륨 경로 권한이 올바른가?

##### Procedure

1. **서비스 가동**

   ```bash
   cd infra/04-data/operational/mng-db
   docker-compose up -d
   ```

2. **초기화 작업 강제 실행**
   기존에 생성되지 않은 DB 유저나 스키마를 동기화해야 하는 경우 `mng-pg-init`을 재실행한다.

   ```bash
   docker-compose run --rm mng-pg-init
   ```

3. **서비스 로그 감시**

   ```bash
   docker-compose logs -f mng-pg
   docker-compose logs -f mng-valkey
   ```

#### Related Operational Documents

- **Operation**: [mng-db.md](./mng-db.md)
- **Plan**: [2026-03-26-04-data-standardization.md](../../../../04.execution/plans/2026-03-26-04-data-standardization.md)

Copyright (c) 2026. Licensed under the MIT License.

---

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
