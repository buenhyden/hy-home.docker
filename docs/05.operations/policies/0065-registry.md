---
title: "Docker Registry Operations Policy"
version: "1.2.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0065"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Docker Registry Operations Policy

## Overview

### Overview

Registry는 `HOME` 아티팩트 저장소다. 현재 추적 중인 엔드포인트는 네이티브
TLS/인증을 갖추지 않았으므로 명시적으로 격리된 신뢰 네트워크에서만 서비스할 수 있다.

## Scope

### Policy Scope

활성화, 노출, 이미지 출처/digest, 파일시스템 보존, 백업, 가비지 컬렉션, 업그레이드,
제거.

### Traceability

- [가이드](../guides/0065-registry.md) (`GDE-0065`)
- [런북](../runbooks/0065-registry.md) (`RUN-0065`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Rules

### Controls

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

### Verification

`/v2/` 헬스만으로는 충분하지 않다. 런타임 수용 기준에는 네트워크 경계, 필요 시
TLS/인증, push, pull, digest 일치가 포함된다.

### Review Cadence

노출, 인증, 저장소, 삭제, 이미지, 아티팩트 보존이 변경될 때 검토한다.

## Exceptions

### Exceptions

신뢰할 수 없는 평문 자격 증명 전송, 작성자(writer)가 있는 상태의 GC, 아티팩트의
유일한 사본 삭제를 허용하는 예외는 없다.

## Related Documents

- [Registry Compose 소스](../../../infra/09-platform-ops/registry/docker-compose.yml)
- [CNCF Distribution 배포](https://distribution.github.io/distribution/about/deploying/)
- [가비지 컬렉션](https://distribution.github.io/distribution/about/garbage-collection/)
