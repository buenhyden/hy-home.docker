---
title: "Terrakube Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0069"
parent_ids:
- "AD-0009"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Terrakube Operations Policy

## Purpose and Scope

### Objective

Terrakube는 명시적인 `iac` 컨트롤 플레인이다. Apache-2.0 프로젝트 라이선스가
이 단일 호스트 배포의 지원, SLA, 엔터프라이즈 기능, HA를 보장하지는
않는다.

#### Authority

- [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md)

- [Terrakube Compose 소스](../../../../infra/09-platform-ops/terrakube/docker-compose.yml)

### Applies To

API/UI/executor 활성화, 네이티브/gateway 인증, Docker 소켓 및 provider 권한,
PostgreSQL/SeaweedFS/Valkey 데이터, 협조된 복구, 업그레이드, 제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0069-R1 | `iac` 활성화 시 | 필수: 이름이 지정된 세 Terrakube 서비스만 시작한다 | none | none |
| POL-0069-R2 | 항상 | 금지: HOME/tooling에서 Terrakube 시작 | none | none |
| POL-0069-R3 | 항상 | 필수: 추적 중인 gateway 미들웨어와 애플리케이션 OIDC 동작을 모두 검증한다 | 수동 | none |
| POL-0069-R4 | 항상 | 금지: 환경 변수 레이블만으로 네이티브 OIDC나 그룹 권한 부여를 주장 | none | none |
| POL-0069-R5 | plan과 apply 시 | 필수: 리포지토리/ref, workspace, 계정, 예상 리소스, 승인자를 명시한다 | none | none |
| POL-0069-R6 | apply/destroy 시 | 필수: 별도 승인을 받는다 | 수동 | none |
| POL-0069-R7 | 항상 | 필수: 선언된 시크릿 파일만 사용한다 | 수동 | none |
| POL-0069-R8 | 항상 | 금지: 로그, 스크린샷, Task, 지원 번들에 시크릿/상태/plan 출력 포함 | 수동 | none |
| POL-0069-R9 | 항상 | 필수: 보존 정책에 일관된 복구 지점을 포함한다 | none | none |
| POL-0069-R10 | 백업/복구 시 | 필수: 스케줄링/실행을 정지하고 PostgreSQL과 SeaweedFS를 일관되게 캡처한다 | 수동 | none |
| POL-0069-R11 | 백업/복구 시 | 필수: config/client/custody 메타데이터를 보존한다 | 수동 | none |
| POL-0069-R12 | 복구 시 | 필수: 외부 실행을 비활성화한 상태로 리허설한다 | 수동 | none |
| POL-0069-R13 | 항상 | 금지: 컨테이너 재시작을 HA나 재해 복구로 묘사 | none | none |
| POL-0069-R14 | 업그레이드 시 | 필수: 복원된 사본에서 마이그레이션을 테스트한다 | none | none |
| POL-0069-R15 | 업그레이드 시 | 필수: API/UI/executor를 호환 세트로 함께 이동한다 | none | none |
| POL-0069-R16 | 호환되지 않는 다운그레이드 시 | 필수: 데이터베이스/상태 롤백을 동반한다 | none | none |
| POL-0069-R17 | 제거 시 | 필수: 승인된 후속 시스템이 소유하기 전까지 workspace, run, 상태, 출력, VCS 매핑, 복구 보관을 유지한다 | none | none |
| POL-0069-R18 | 항상 | 필수: 현재 gateway 통제를 유지한다 | none | none |
| POL-0069-R19 | 항상 | 금지: 로그인·health 성공을 실행 가능 증거로 기록 | none | none |

- **Activation:** `iac`에서는 이름이 지정된 세 가지 Terrakube 서비스만 시작하고
  정확한 의존성은 별도로 선택한다. HOME/tooling에서는 제외한다.
- **Authentication:** 추적 중인 gateway 미들웨어와 애플리케이션 OIDC 동작을 모두
  검증한다. 환경 변수 레이블만으로 네이티브 OIDC나 그룹 권한 부여를 주장하지
  않는다.
- **Execution:** executor의 Docker 소켓 접근과 provider 자격 증명은 특권이다.
  plan과 apply는 리포지토리/ref, workspace, 계정, 예상 리소스, 승인자를
  명시한다. apply/destroy는 별도 승인을 받아야 한다.
- **Secrets:** 선언된 시크릿 파일만 사용한다. 로그, 스크린샷, Task, 지원 번들에
  시크릿/상태/plan 출력이 포함되어서는 안 된다.
- **Data:** PostgreSQL 메타데이터와 SeaweedFS `tfstate`는 공동으로 권위를
  갖는다. Valkey는 조정 상태다. 보존 정책은 일관된 복구 지점을 포함해야 한다.
- **Backup/recovery:** 스케줄링/실행을 정지하고, PostgreSQL과 SeaweedFS를
  일관되게 캡처하며, config/client/custody 메타데이터를 보존하고, 외부 실행을
  비활성화한 상태로 리허설한다. 단일 저장소 복구는 불완전하다.
- **Resources/availability:** 단일 호스트, 단일 replica DEV 배포로
  취급한다. 컨테이너 재시작을 HA나 재해 복구로 묘사하지 않는다.
- **Upgrade:** 복원된 사본에서 마이그레이션을 테스트하고 API/UI/executor를
  호환 세트로 함께 이동한다. 호환되지 않는 다운그레이드에는 데이터베이스/상태
  롤백이 동반된다.
- **Removal:** 승인된 후속 시스템이 소유하기 전까지 workspace, run, 상태, 출력,
  VCS 매핑, 복구 보관을 유지한다. 컨테이너 삭제만으로는 충분하지 않다.

#### 현재 실행 경로의 제한

현재 gateway 통제를 유지하고 로그인·health 성공을 실행 가능 증거로 기록하지 않는다. 인증 경로 제한의 세부 내용은 [Guide](../../guides/10-platform-and-backup/0069-terrakube.md#현재-실행-경로의-제한)를 따른다.

### Exceptions

#### Exception Conditions

예외는 provider/apply 승인, Docker 소켓 검토, 시크릿 취급, 협조된 백업을
우회할 수 없다. 만료 시점과 복구 담당자를 기록한다.

#### Approval and Review

각 릴리스, 인증 변경, 저장소/백엔드 변경, Docker 소켓 권한 변경 전에
검토한다.

## Enforcement

### Mechanisms

정적 Compose와 컴포넌트 헬스는 부분적인 신호다. 엔드투엔드 증거에는
로그인/권한 부여, DB/객체 접근 가능성, executor 등록, 그리고 검토된
비적용(non-applying) plan이 필요하다. 복구는 리허설하기 전까지 검증되지
않은 상태로 남는다.

### Limits

정책은 정적 Compose와 헬스를 부분 신호로만 인정하며 아래 규칙은 지정된 검사가 없거나 수동에 의존한다.

- 활성화: 지정된 검사 없음: `POL-0069-R1`, `POL-0069-R2`
- 인증: 지정된 검사 없음: `POL-0069-R4`
- 실행: 수동 검토/승인에 의존: `POL-0069-R6` / 지정된 검사 없음: `POL-0069-R5`
- 시크릿: 수동 검토/승인에 의존: `POL-0069-R7`, `POL-0069-R8`
- 데이터: 지정된 검사 없음: `POL-0069-R9`
- 백업·복구: 수동 검토/승인에 의존: `POL-0069-R10`, `POL-0069-R11`, `POL-0069-R12`
- 가용성: 지정된 검사 없음: `POL-0069-R13`
- 업그레이드: 지정된 검사 없음: `POL-0069-R14`, `POL-0069-R15`, `POL-0069-R16`
- 제거: 지정된 검사 없음: `POL-0069-R17`
- 실행 경로 제한: 지정된 검사 없음: `POL-0069-R18`, `POL-0069-R19`
- 엔드투엔드 증거(로그인/권한 부여, DB/객체 접근, executor 등록, 검토된 non-applying plan)에 대한 전용 명령은 지정되어 있지 않다.
- 복구는 리허설하기 전까지 검증되지 않은 상태로 남는다.
- 단일 호스트 단일 replica DEV 배포이며 HA/재해 복구는 제공되지 않는다.
- POL-0069-R3: 수동 검증에 맡겨진다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- [가이드](../../guides/10-platform-and-backup/0069-terrakube.md) (`GDE-0069`)
- [런북](../../runbooks/10-platform-and-backup/0069-terrakube.md) (`RUN-0069`)

- [Terrakube 문서](https://docs.terrakube.io/)
- [Terrakube 라이선스](https://github.com/terrakube-io/terrakube/blob/main/LICENSE)
- [운영 인덱스](../../README.md)
