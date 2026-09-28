---
title: "Docker Registry Usage Guide"
version: "1.2.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0065"
parent_ids:
- "POL-0065"
implementation_services:
  infra/09-tooling/registry/docker-compose.yml:
  - registry
created: "2026-05-10"
---

# Docker Registry Usage Guide

## Usage

### 목적과 분류

Registry는 `tooling`과 `registry` 하위의 온디맨드 OPTIONAL OCI 이미지 저장소이다.
push된 매니페스트와 blob을 `${DEFAULT_REGISTRY_DIR}`에 저장한다. 로컬에서 빌드한
이미지는 추적되는 Dockerfile로부터 재현할 수 있지만, push된 서드파티나 고유
아티팩트는 digest/콘텐츠가 백업되어 있거나 신뢰할 수 있는 업스트림에서 여전히
구할 수 있을 때만 복구할 수 있다.

### 현재 구현과 보안 격차

- [Registry Compose](../../../infra/09-tooling/registry/docker-compose.yml)가
  이미지, profile, 호스트 게시, healthcheck, 스토리지 마운트를 정의한다.
- 호스트 포트 `${REGISTRY_PORT:-5000}`은 `127.0.0.1`에만 게시되며, 컨테이너 포트
  5000으로 연결된다. 추적되는 서비스 설정에는 Registry TLS나 인증 설정, Traefik
  라우트가 없다. 그 결과 이 endpoint는 로컬 호스트 사용자와 프로젝트 기본 네트워크의
  모든 컨테이너(`registry:5000`)에게 인증되지 않은 HTTP로 열려 있다. Docker는
  기본적으로 `127.0.0.0/8` registry를 HTTP로 신뢰하므로 insecure-registry 데몬
  설정이 필요 없다.
- 컨테이너는 `${DEFAULT_REGISTRY_DIR}`의 소유자인 `1000:1000`으로 실행된다.
  모든 capability가 제거된 root는 해당 디렉터리에 쓸 수 없다.
- `/v2/` 헬스체크는 HTTP 응답만 증명한다. 인가, digest 무결성, push/pull, 스토리지
  내구성, 클라이언트 신뢰를 증명하지 않는다.
- bind 기반의 `/var/lib/registry`가 권위 있는 파일시스템 스토리지다. 삭제 기능은
  활성화되어 있지 않으며 garbage collection은 정상적인 정리 절차가 아니다.

### 일반적인 사용

1. 루트에서 `docker compose --profile registry config --quiet`로 검증한다.
2. push 전에 endpoint가 승인된 신뢰 네트워크로 한정되어 있는지 확인한다. TLS와
   접근 제어가 구현되고 테스트되기 전까지는 민감하거나 독점적인 아티팩트를
   저장하지 않는다.
3. 불변 release/digest 정책에 따라 태그를 지정하고 push한 다음, digest로 pull하여
   매니페스트 digest를 검증한다. repository, tag, digest, 출처 권한을 기록한다.
4. 파일시스템과 digest 인벤토리를 하나의 백업 단위로 다룬다.

### 로컬에서 빌드한 이미지 보관

실행 중이 아닌 로컬 빌드 이미지는 Registry에 보관해 두고 `/`의 Docker 이미지 저장소에서는
빼 둘 수 있다. `${DEFAULT_REGISTRY_DIR}`는 데이터 디스크에
있다.

1. 이미지를 `localhost:${REGISTRY_PORT:-5000}/<repository>:<tag>`로 태그하고
   push한다.
2. push된 참조를 digest로 pull하고 push 출력의 digest와 비교한다. repository,
   tag, digest, 출처 Dockerfile을 Task에 기록한다.
3. 2단계가 성공한 후에만 로컬 태그를 제거한다. 실행 중이든 중지되었든 컨테이너가
   여전히 사용하는 이미지는 절대 제거하지 않는다.
4. 다시 사용하려면 Registry 참조를 pull하여 Compose 파일이 기대하는 이름으로
   재태깅하거나, 추적되는 Dockerfile에서 재빌드한다.

### 백업과 업그레이드

추적되는 설정에는 읽기 전용 유지보수 모드가 없다. 일관된 파일시스템 백업을 위해
클라이언트를 차단하고 Registry를 중지한 다음, 전체 bind 디렉터리를 스냅샷/복사하고
카탈로그/태그/digest 인벤토리를 기록한다. 격리된 Registry로 복원하고, 승격 전에
`/v2/`, 카탈로그/태그, 선택된 digest의 pull을 검증한다. garbage collection을
하려면 Registry가 읽기 전용이거나 중지된 상태여야 하고 파괴적 데이터 작업에 대한 별도
승인도 받아야 한다. 업그레이드 전에는 일관된 백업을 확보하고 Distribution의 release/스토리지
변경 사항을 검토하고 복원된 사본으로 새 이미지를 테스트하고 push/pull/digest를
검증한다. 이 문서 작업에서는 백업, 복원, GC, 업그레이드를 실행하지 않았다.

## Common Checks

- `docker compose --profile registry config --quiet`
- `docker compose --profile registry config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

push/pull 실패, 스토리지 복구, 계획된 업그레이드, 별도로 승인된 garbage collection에는
[runbook](../runbooks/0065-registry.md)을 사용한다.

## Traceability

- [Policy](../policies/0065-registry.md) (`POL-0065`)
- [Runbook](../runbooks/0065-registry.md) (`RUN-0065`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [CNCF Distribution deployment and security](https://distribution.github.io/distribution/about/deploying/)
- [Registry configuration](https://distribution.github.io/distribution/about/configuration/)
- [Registry garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Registry project and Apache license](https://distribution.github.io/distribution/)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
