---
title: "09-tooling: Tooling Tier"
version: "1.2.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# 09-tooling: Tooling Tier

## Overview

루트 Compose 프로젝트는 모든 tooling leaf를 include하며 프로필만으로 실제
작업을 선택합니다. 현재 매핑은 다음과 같습니다.

| Profile | Services | Runtime class |
| --- | --- | --- |
| `tooling` | `registry`, `sonarqube` | 선택적 관리 서비스 |
| `registry` | `registry` | OCI 저장소 |
| `sast` | `sonarqube` | 코드 품질 서비스 |
| `testing` | `k6`, `locust-master`, `locust-worker` | 명시적 부하 테스트 작업/서비스 |
| `iac` | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | 명시적 인프라 도구 |
| `dependency-update` | `renovate` | 1회성 원격 저장소 유지보수 |
| `analytics-engineering` | `dbt-db-provision`, `dbt` (`mng-pg`, `mng-pg-init` 포함) | 1회성 변환 작업; `run`/`build`가 대상 스키마에 기록함 |
| `backup` | `restic`, `backup-sqlite-export` | 호스트 타이머로 구동되는 1회성 백업 작업 |
| `api-mock` | `wiremock` | 개발/테스트용 HTTP 스텁 서버; 관리 API는 loopback 전용 |
| `contract-testing` | `pact-broker-db-provision`, `pact-broker` (`mng-pg`, `mng-pg-init` 포함) | 계약 저장소; basic auth, loopback 전용 |
| `policy-check` | `conftest` | `infra/`에 대한 1회성 Rego 정책 테스트; 네트워크 없음 |

`tooling`은 IaC나 부하 생성을 선택하지 않습니다. Terraform과 Syncthing 런타임은
제거되었으며 OpenTofu가 현재 CLI 엔진입니다. `tooling` 프로필 자체는 HOME을
선택하지 않지만 `registry` 서비스는 별도의 `registry` 프로필을 통해 HOME
선택에 포함됩니다(루트 [infra/README.md](../README.md) 참고).

## Audience

플랫폼 운영자, 이 도구들을 사용하는 개발자, 보안 검토자, tooling 프로필 계약을
담당하는 문서화 agent.

## Scope

- [k6](k6/README.md)와 [Locust](locust/README.md)는 대상 소유자의 승인을 받은
  후에만 트래픽을 생성합니다. k6는 1회성이며 Locust는 master/worker 서비스로
  구성됩니다.
- [OpenTofu](opentofu/README.md)는 워크스페이스 상태와 읽기 전용 provider
  자격 증명 마운트를 사용하는 로컬 CLI 작업입니다. Plan과 apply는 별도로
  승인됩니다.
- [Terrakube](terrakube/README.md)는 메타데이터를 management PostgreSQL에,
  상태 오브젝트를 SeaweedFS에, 일시적 조정 정보를 Valkey에 저장합니다. 한
  호스트의 세 고정 서비스는 HA 배포가 아닙니다.
- [Registry](registry/README.md)는 `${DEFAULT_REGISTRY_DIR}` 아래에 OCI
  오브젝트를 영속화합니다. 현재 Compose는 포트 5000을 `127.0.0.1`에만
  게시하며 TLS/인증을 추적하지 않으므로 사용 전에 노출 범위를 제한해야
  합니다.
- [SonarQube](sonarqube/README.md)는 권한 정보를 PostgreSQL과 선언된
  데이터/로그 볼륨에 영속화합니다. 검색 인덱스는 파생 값이지만 데이터베이스와
  확장/설정은 일관되게 복구해야 합니다.
- [Renovate](renovate/README.md)는 Docker Secret 토큰과 일회용 캐시를
  사용합니다. 실제 작업은 원격 브랜치/PR을 생성할 수 있으므로 명시적 승인이
  필요합니다.
- [Restic](restic/README.md)은 데이터 디스크 파일, 일관된 내보내기 결과,
  `secrets/`, `.env`를 호스트 타이머 아래 두 개의 서로 다른 디스크에 있는
  저장소로 스냅샷합니다.
- [WireMock](wiremock/README.md)은 추적되는 합성 HTTP 스텁을 제공합니다.
  관리 API는 인증이 없으므로 호스트 포트는 loopback에만 바인딩됩니다.
- [Pact Broker](pact-broker/README.md)는 pact와 검증 결과를 기능 전용
  `mng-pg` 데이터베이스에 basic auth와 loopback 포트로 보호하여 저장합니다.
- [Conftest](conftest/README.md)는 `infra/` 아래의 Compose 파일과
  Dockerfile에 대해 읽기 전용, 네트워크 없이 Rego 정책 테스트를 실행합니다.

## Structure

```text
09-tooling/
├── k6/          # one-shot load job
├── locust/      # master/worker load service
├── opentofu/    # IaC CLI job
├── terrakube/   # IaC automation API/UI/executor
├── registry/    # OCI Distribution storage
├── sonarqube/   # code-quality/SAST service
├── renovate/    # dependency-update job
├── dbt/         # analytics-engineering transformation job
├── restic/      # backup jobs, exclude lists, host orchestrator and timer
├── wiremock/    # HTTP stub server and tracked mappings
├── pact-broker/ # contract broker and its database provisioning
├── conftest/    # Rego policy tests over infra/
└── README.md
```

## How to Work in This Area

[documentation index](../../docs/README.md)를 사용한 뒤, `docs/05.operations/README.md`
아래의 정확한 Stage 05 대상(`0061`, `0062`, `0065`, `0066`, `0069`, `0082`, `0083`, `0090`, `0092`, `0093`, `0095`)을 확인합니다. 저장소 루트에서 실행합니다.

```bash
bash scripts/hardening/check-all-hardening.sh 09-tooling
HYHOME_COMPOSE_PROFILES=testing bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=iac bash scripts/validation/validate-docker-compose.sh
```

정적 검증은 부하 테스트, IaC apply, 백업/복구, 원격 업데이트, 서비스 준비
상태의 근거가 되지 않습니다. Compose/Dockerfile 선언이 런타임 고정 값을
소유하며 [tech-stack.versions.json](../tech-stack.versions.json)은 파생된
이미지 프로젝션입니다.

## Related Documents

- [Documentation index](../../docs/README.md)
- [Infrastructure index](../README.md)
- Stage 05 tooling package: `docs/05.operations/README.md`
