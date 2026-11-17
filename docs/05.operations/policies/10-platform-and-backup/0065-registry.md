---
title: "Docker Registry Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0065"
parent_ids:
- "AD-0009"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Docker Registry Operations Policy

## Purpose and Scope

### Objective

Registry는 `HOME` 아티팩트 저장소다. 현재 추적 중인 엔드포인트는 네이티브
TLS/인증을 갖추지 않았으므로 명시적으로 격리된 신뢰 네트워크에서만 서비스할 수 있다.

#### Authority

- [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md)

- [Registry Compose 소스](../../../../infra/09-platform-ops/registry/docker-compose.yml)

### Applies To

활성화, 노출, 이미지 출처/digest, 파일시스템 보존, 백업, 가비지 컬렉션, 업그레이드,
제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0065-R1 | 활성화 시 | 필수: `registry` 또는 일반 `tooling`으로 활성화한다 | 수동 | none |
| POL-0065-R2 | 항상 | 필수: 호스트 포트는 `127.0.0.1`에만 바인딩한다 | 수동 | none |
| POL-0065-R3 | 항상 | 금지: `obs_net` 무인증 접근에 대해 방화벽이나 데몬 제한을 가정 | 수동 | none |
| POL-0065-R4 | 민감한 용도나 더 넓은 접근 전 | 필수: TLS와 인증, 또는 신뢰할 수 있는 인증 리버스 프록시를 구현하고 검증한다 | 수동 | none |
| POL-0065-R5 | 안전하지 않은 registry 클라이언트 설정 | 허용: 경계가 정해진 DEV 네트워크에서만 사용한다 | 수동 | none |
| POL-0065-R6 | 항상 | 필수: 필요한 각 이미지마다 소스 권위와 digest를 보존한다 | 수동 | none |
| POL-0065-R7 | 항상 | 금지: 변경 가능한 태그를 복구 증거로 취급 | 수동 | none |
| POL-0065-R8 | 항상 | 필수: `/var/lib/registry` 콘텐츠와 digest 인벤토리를 하나의 복구 단위로 취급한다 | 수동 | none |
| POL-0065-R9 | 삭제를 활성화하기 전 | 필수: 보존 정책을 정의한다 | 수동 | none |
| POL-0065-R10 | 백업/복구 시 | 필수: registry를 중지하거나 읽기 전용으로 만들고 전체 파일시스템을 스냅샷한다 | 수동 | none |
| POL-0065-R11 | 복구에 의존하기 전 | 필수: 격리된 catalog/tag/digest pull을 리허설한다 | 수동 | 승인과 수행 기록 |
| POL-0065-R12 | garbage collection 실행 시 | 필수: 명시적인 파괴적 승인을 받고 registry를 중지하거나 읽기 전용으로 둔다 | 수동 | 승인과 수행 기록 |
| POL-0065-R13 | 업로드가 발생할 수 있는 동안 | 금지: GC 실행 | 수동 | none |
| POL-0065-R14 | 항상 | 필수: `${DEFAULT_REGISTRY_DIR}` 파일시스템을 모니터링하고 백업/복구 및 업그레이드 테스트에 충분한 용량을 남긴다 | 수동 | none |
| POL-0065-R15 | 항상 | 금지: 임의로 만든 임계값을 정책 기준으로 취급 | 수동 | none |
| POL-0065-R16 | 활성 이미지 변경 전 | 필수: 복원된 사본에서 저장소 호환성과 digest 기준 push/pull을 검증한다 | 수동 | 승인과 수행 기록 |
| POL-0065-R17 | registry 제거 시 | 필수: 필요한 모든 아티팩트를 재현 가능 또는 백업 완료로 분류한다 | 수동 | none |
| POL-0065-R18 | 저장소를 삭제하기 전 | 필수: 후속 시스템을 검증한다 | 수동 | none |

- **Activation:** `registry` 또는 일반 `tooling`을 사용한다. SPEC-0182 W6에서 소유자가 `registry`를 HOME에 추가했다(POL-0078).
- **Exposure/auth:** 호스트 포트는 `127.0.0.1`에 바인딩되지만, `obs_net`
  네트워크의 컨테이너는 인증 없이도 여전히 접근할 수 있다. 방화벽이나 데몬
  제한을 가정하지 않는다. 민감한 용도나 더 넓은 접근 전에는 TLS와 인증, 또는
  신뢰할 수 있는 인증 리버스 프록시를 구현하고 검증한다. 안전하지 않은 registry
  클라이언트 설정은 경계가 정해진 DEV 네트워크에서만 허용되며 프로덕션 통제가
  아니다.
- **Artifacts:** 필요한 각 이미지마다 소스 권위와 digest를 보존한다. 변경 가능한
  태그는 복구 증거가 아니다.
- **Data/retention:** `/var/lib/registry` 콘텐츠와 digest 인벤토리는 하나의 복구
  단위다. 삭제를 활성화하기 전에 보존 정책을 정의한다. 삭제는 현재 꺼져 있다.
- **Backup/restore:** registry를 중지하거나 읽기 전용으로 만들고, 전체 파일시스템을
  스냅샷하며, 의존하기 전에 격리된 catalog/tag/digest pull을 리허설한다.
- **Garbage collection:** 명시적인 파괴적 승인이 있어야 하고 registry는 중지되거나
  읽기 전용이어야 한다. 업로드가 발생할 수 있는 동안에는 GC를 실행하지 않는다.
- **Resources:** `${DEFAULT_REGISTRY_DIR}` 파일시스템을 모니터링하고 백업/복구 및
  업그레이드 테스트에 충분한 용량을 남긴다. 임의로 만든 임계값은 정책이 아니다.
- **Upgrade:** 활성 이미지를 변경하기 전에 복원된 사본에서 저장소 호환성과
  digest 기준 push/pull을 검증한다.
- **Removal:** 필요한 모든 아티팩트를 재현 가능 또는 백업 완료로 분류하고,
  저장소를 삭제하기 전에 후속 시스템을 검증한다.

### Exceptions

#### Exception Conditions

신뢰할 수 없는 평문 자격 증명 전송, 작성자(writer)가 있는 상태의 GC, 아티팩트의
유일한 사본 삭제를 허용하는 예외는 없다.

#### Approval and Review

노출, 인증, 저장소, 삭제, 이미지, 아티팩트 보존이 변경될 때 검토한다.

## Enforcement

### Mechanisms

`/v2/` 헬스만으로는 충분하지 않다. 런타임 수용 기준에는 네트워크 경계, 필요 시
TLS/인증, push, pull, digest 일치가 포함된다.

### Limits

정책은 런타임 수용 기준을 요구하지만 전용 검사를 지정하지 않으며 아래 항목은 수동에 의존한다.

- 노출·인증: 수동 검토/승인에 의존: `POL-0065-R1`, `POL-0065-R3`, `POL-0065-R5`
- 아티팩트: 수동 검토/승인에 의존: `POL-0065-R6`, `POL-0065-R7`
- 데이터·보존: 수동 검토/승인에 의존: `POL-0065-R8`, `POL-0065-R9`
- 백업·복구: 수동 검토/승인에 의존: `POL-0065-R10`, `POL-0065-R11`
- GC: 수동 검토/승인에 의존: `POL-0065-R12`, `POL-0065-R13`
- 자원: 수동 검토/승인에 의존: `POL-0065-R14`, `POL-0065-R15`
- 제거: 수동 검토/승인에 의존: `POL-0065-R17`, `POL-0065-R18`
- `/v2/` 헬스만으로는 충분하지 않고 TLS/인증은 현재 추적 엔드포인트에 없으며 `obs_net` 컨테이너는 인증 없이 접근할 수 있다.
- 용량 임계값은 정책이 정하지 않는다.
- POL-0065-R2, POL-0065-R4, POL-0065-R16: 수동 검증에 맡겨진다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- [가이드](../../guides/10-platform-and-backup/0065-registry.md) (`GDE-0065`)
- [런북](../../runbooks/10-platform-and-backup/0065-registry.md) (`RUN-0065`)

- [CNCF Distribution 배포](https://distribution.github.io/distribution/about/deploying/)
- [가비지 컬렉션](https://distribution.github.io/distribution/about/garbage-collection/)
