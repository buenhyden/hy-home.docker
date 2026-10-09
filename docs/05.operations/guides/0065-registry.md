---
title: "Docker Registry Usage Guide"
version: "1.2.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0065"
parent_ids:
- "POL-0065"
implementation_services:
  infra/09-platform-ops/registry/docker-compose.yml:
  - registry
created: "2026-05-10"
---

# Docker Registry Usage Guide

## Overview

Registry는 `infra/09-platform-ops/registry/`의 `registry` service로 운영하는 HOME OCI 이미지 저장소다.
`registry` 또는 `tooling` profile에서 선택된다.

## Audience and Goal

대상 독자는 이미지를 push·pull하고 저장소를 유지하는 운영자다. 목표는 현재 구현의 노출·인증 한계를
이해하고, 일반 사용과 백업·업그레이드 경계를 확인하는 것이다. 실행 절차는
[Registry Runbook](../runbooks/0065-registry.md)이 맡는다.

## Usage

### 분류와 저장소 범위

Registry는 `registry`(HOME)와 `tooling`이 선택하는 `HOME` OCI 이미지 저장소이다.
push된 매니페스트와 blob을 `${DEFAULT_REGISTRY_DIR}`에 저장한다. 로컬에서 빌드한
이미지는 추적되는 Dockerfile로부터 재현할 수 있지만, push된 서드파티나 고유
아티팩트는 digest/콘텐츠가 백업되어 있거나 신뢰할 수 있는 업스트림에서 여전히
구할 수 있을 때만 복구할 수 있다.

### 현재 구현과 보안 격차

- [Registry Compose](../../../infra/09-platform-ops/registry/docker-compose.yml)가
  이미지, profile, 호스트 게시, healthcheck, 스토리지 마운트를 정의한다.
- 호스트 포트 `${REGISTRY_PORT:-5000}`은 `127.0.0.1`에만 게시되며, 컨테이너 포트
  5000으로 연결된다. 추적되는 서비스 설정에는 Registry TLS나 인증 설정, Traefik
  라우트가 없다. 그 결과 이 endpoint는 로컬 호스트 사용자와 `obs_net`의
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

실행 순서와 실패·복구 판단은 [런북](../runbooks/0065-registry.md)의 `로컬 이미지 이관과 제거` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### 백업과 업그레이드

실행 순서와 실패·복구 판단은 [런북](../runbooks/0065-registry.md)의 `계획된 저장소 유지보수` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `docker compose --profile registry config --quiet`
- `docker compose --profile registry config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`

### Runbook Handoff

push/pull 실패, 스토리지 복구, 계획된 업그레이드, 별도로 승인된 garbage collection에는
[runbook](../runbooks/0065-registry.md)을 사용한다.

### 신호와 자원

내부 debug listener의 `/metrics`는 Registry API와 별도 관측 경로이며 호스트에
직접 게시되지 않는다. 접근 경계는 [Compose](../../../infra/09-platform-ops/registry/docker-compose.yml)의
네트워크와 listener 선언을 기준으로 확인한다. 파일시스템 사용량·쓰기 오류·digest
불일치를 함께 확인하며 `/v2/` 성공만으로 용량이나 복구 가능성을 판정하지 않는다.

### Traceability

- [Policy](../policies/0065-registry.md) (`POL-0065`)
- [Runbook](../runbooks/0065-registry.md) (`RUN-0065`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [CNCF Distribution deployment and security](https://distribution.github.io/distribution/about/deploying/)
- [Registry configuration](https://distribution.github.io/distribution/about/configuration/)
- [Registry garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Registry project and Apache license](https://distribution.github.io/distribution/)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
