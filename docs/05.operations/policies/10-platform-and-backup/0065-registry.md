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
| POL-0065-R1 | 활성화 시 | 필수: `registry` 또는 일반 `tooling`으로 사용한다 | none | none |
| POL-0065-R2 | 항상 | 필수: 호스트 포트는 `127.0.0.1`에 바인딩하되 `obs_net` 무인증 접근을 가정하고 민감 용도 전 TLS/인증 또는 인증 리버스 프록시를 구현/검증한다 | 런타임 수용 기준(네트워크 경계, TLS/인증) | none |
| POL-0065-R3 | 항상 | 필수: 각 이미지의 소스 권위와 digest를 보존하고 변경 가능 태그를 복구 증거로 보지 않는다 | 수동 | digest 인벤토리 |
| POL-0065-R4 | 항상 | 필수: `/var/lib/registry`와 digest 인벤토리를 하나의 복구 단위로 보고 삭제 활성화 전에 보존 정책을 정의한다 | 수동 | none |
| POL-0065-R5 | 백업/복구 시 | 필수: registry를 중지/읽기 전용으로 하고 전체 파일시스템을 스냅샷하며 격리 catalog/tag/digest pull을 리허설한다 | 런타임 수용 기준(push, pull, digest 일치) | none |
| POL-0065-R6 | GC 시 | 필수: 명시적 파괴적 승인과 중지/읽기 전용 상태가 필요하며 업로드 가능 시 GC를 실행하지 않는다 | 수동 / 파괴적 승인 | 승인 기록 |
| POL-0065-R7 | 항상 | 필수: `${DEFAULT_REGISTRY_DIR}` 파일시스템을 모니터링하고 백업/복구/업그레이드 테스트 용량을 남긴다 | 수동 | none |
| POL-0065-R8 | 업그레이드 시 | 필수: 활성 이미지 변경 전 복원된 사본에서 저장소 호환성과 digest 기준 push/pull을 검증한다 | 런타임 수용 기준(push, pull, digest 일치) | none |
| POL-0065-R9 | 제거 시 | 필수: 모든 아티팩트를 재현 가능/백업 완료로 분류하고 삭제 전 후속 시스템을 검증한다 | 수동 | none |

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

정책은 런타임 수용 기준(네트워크 경계, TLS/인증, push, pull, digest)을 요구하지만 전용 검사를 지정하지 않으며 아래 항목은 수동에 의존한다.

- 모든 규칙에 대해 명령이나 스크립트가 지정되어 있지 않아 수동 검토와 리허설에 의존한다.
- `/v2/` 헬스만으로는 충분하지 않으며 TLS/인증은 현재 추적 엔드포인트에 없고 `obs_net` 컨테이너는 인증 없이 접근할 수 있다.
- 백업 복구 리허설, 업그레이드 검증, GC는 별도 승인과 수행 기록이 필요하다.
- 용량 임계값은 정책이 정하지 않으며 임의 임계값은 정책이 아니다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- [가이드](../../guides/10-platform-and-backup/0065-registry.md) (`GDE-0065`)
- [런북](../../runbooks/10-platform-and-backup/0065-registry.md) (`RUN-0065`)

- [CNCF Distribution 배포](https://distribution.github.io/distribution/about/deploying/)
- [가비지 컬렉션](https://distribution.github.io/distribution/about/garbage-collection/)
