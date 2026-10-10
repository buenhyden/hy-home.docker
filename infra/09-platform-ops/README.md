---
title: "09-platform-ops: Platform Operations Tier"
version: "1.2.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# 09-platform-ops: Platform Operations Tier

## Overview

IaC·아티팩트 배포·의존성 유지보수·플랫폼 공통 백업을 소유합니다.
소프트웨어·설정 검증은 [11 Quality](../11-quality/README.md)가 담당합니다.
루트 Compose 프로젝트가 모든 leaf를 include하며 프로필로 실제 작업을 선택합니다. 현재 매핑은 다음과 같습니다.

| Profile | Services | Runtime class |
| --- | --- | --- |
| `tooling` | `registry`, Quality의 `sonarqube` | 여러 tier에 걸친 기존 선택 조합 |
| `registry` | `registry` | OCI 저장소 |
| `iac` | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | 명시적 인프라 도구 |
| `dependency-update` | `renovate` | 1회성 원격 저장소 유지보수 |
| `backup` | `restic`, `restic-offsite`, `backup-sqlite-export` | 호스트 타이머로 구동되는 1회성 백업 작업 |

`tooling`은 IaC나 부하 생성을 선택하지 않습니다. Terraform과 Syncthing 런타임은
제거되었으며 OpenTofu가 현재 CLI 엔진입니다. `tooling` 프로필 자체는 HOME을
선택하지 않지만 `registry` 서비스는 별도의 `registry` 프로필을 통해 HOME
선택에 포함됩니다(루트 [infra/README.md](../README.md) 참고).

dbt 변환 작업은 [12 Analytics](../12-analytics/README.md)에서 관리합니다.

## Audience

플랫폼 운영자, 이 도구들을 사용하는 개발자, 보안 검토자, tooling 프로필 계약을
담당하는 문서화 agent.

이 tier는 공통 플랫폼의 IaC, 아티팩트 배포, 의존성 유지보수와 백업·복구
조율을 담당합니다. 애플리케이션 Workflow, 소프트웨어 Quality, Data 저장 엔진,
Security·Auth 및 Observability의 역할은 각 tier에 유지합니다. `tooling`은
Registry와 SonarQube를 선택하는 기존 Compose 프로필이므로 이름을 바꾸지 않습니다.

## Scope

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
- [Renovate](renovate/README.md)는 Docker Secret 토큰과 일회용 캐시를
  사용합니다. 실제 작업은 원격 브랜치/PR을 생성할 수 있으므로 명시적 승인이
  필요합니다.
- [Restic](restic/README.md)은 데이터 디스크 파일, 일관된 내보내기 결과,
  `secrets/`, `.env`를 호스트 타이머 아래 두 개의 서로 다른 디스크에 있는
  저장소로 스냅샷합니다.
- [Security updates](security-updates/README.md)는 공급자 stable/security 조사와
  source 검증 장부를 보관합니다. 장부와 isolated 시험은 실제 이미지 배포,
  HOME 복구 또는 scanner acceptance를 뜻하지 않습니다.

## Structure

```text
09-platform-ops/
├── opentofu/    # IaC CLI job
├── terrakube/   # IaC automation API/UI/executor
├── registry/    # OCI Distribution storage
├── renovate/    # dependency-update job
├── restic/      # backup jobs, exclude lists, host orchestrator and timer
├── security-updates/ # stable/security source ledger and verification records
└── README.md
```

## Usage

[documentation index](../../docs/README.md)를 사용한 뒤, `docs/05.operations/README.md`
아래의 정확한 Stage 05 대상(`0021`, `0065`, `0069`, `0082`, `0083`)을 확인합니다. 저장소 루트에서 실행합니다.

```bash
bash scripts/hardening/check-all-hardening.sh 09-platform-ops
HYHOME_COMPOSE_PROFILES=iac bash scripts/validation/validate-docker-compose.sh
```

정적 검증은 부하 테스트, IaC apply, 백업/복구, 원격 업데이트, 서비스 준비
상태의 근거가 되지 않습니다. Compose/Dockerfile 선언이 런타임 고정 값을
소유하며 [tech-stack.versions.json](../tech-stack.versions.json)은 파생된
이미지 프로젝션입니다.

## Related Documents

- [Documentation index](../../docs/README.md)
- [Infrastructure index](../README.md)
- Stage 05 Platform Operations 문서: `docs/05.operations/README.md`
