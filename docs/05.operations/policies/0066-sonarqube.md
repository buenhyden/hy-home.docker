---
title: "SonarQube Operations Policy"
version: "1.1.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0066"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# SonarQube Operations Policy

## Overview

이 정책은 추적 중인 SonarQube Community Build 배포를 다루며 유료 에디션 기능,
네이티브 Keycloak 통합, 범용 CI 게이트는 가정하지 않는다.

## Scope

활성화, gateway/애플리케이션 인증, 토큰, 데이터베이스/인덱스/로그 데이터, 리소스
제한, 백업/복구, 업그레이드, 제거.

## Rules

- **Activation:** `sast` 또는 일반 `tooling`을 사용한다. HOME 밖에 유지한다.
- **Authentication:** gateway ForwardAuth가 진입을 보호하고, SonarQube가
  애플리케이션 사용자, 그룹, 권한, 토큰을 소유한다. 네이티브 위임 인증은
  구성 및 테스트되기 전까지는 존재하지 않는다. IdP 비활성화만으로는 기존
  SonarQube 토큰이 자동으로 폐기되지 않으며, SonarQube에서 직접 폐기해야 한다.
- **Tokens:** 최소 범위의 만료 토큰을 발급하고, 승인된 CI 시크릿 소유자에게
  저장하며, 값을 로깅하지 않고 회전/폐기한다.
- **Data:** PostgreSQL이 권위 있는 데이터다. 로컬 검색 인덱스는 재구축 가능하며,
  로그는 사고/증거 보존 정책을 따른다. 데이터 볼륨만으로 백업으로 간주하지
  않는다.
- **Backup/restore:** 데이터베이스 네이티브 백업을 사용하고 이를 검증하며,
  격리된 복구와 재인덱싱을 리허설한다. 추적 중인 설정과 외부 플러그인
  인벤토리를 함께 캡처한다.
- **Resources:** 추적 중인 heap 및 stateful-high 제한을 준수한다. 측정된
  queue/heap/index 증거와 호스트 용량에 근거해서만 변경한다.
- **Upgrade:** 에디션/버전 호환성, DB/호스트 요구사항, 플러그인 호환성을
  검토한다. 복원된 데이터에서 테스트한다. 이미지와 DB를 함께 롤백한다.
- **Removal:** 데이터베이스/스키마 또는 볼륨을 삭제하기 전에 프로젝트, 설정,
  이슈, 사용자, 토큰, 백업 증거를 보존하거나 명시적으로 폐기한다.

### 운영 책임

승인·예외·데이터 복구 책임자는 `@buenhyden`이다. 스캐너 토큰과 gateway 인증은
별개이며 인증 실패를 해결하기 위해 middleware를 완화할 수 없다. 공유 PostgreSQL
전체를 복원하는 변경은 다른 데이터 소유자의 영향 검토와 별도 승인을 요구한다.

## Exceptions

유료 기능, 네이티브 SAML/OIDC 프로비저닝, 더 넓은 품질 게이트 요구사항은
각자의 소유 requirement/policy가 필요하며 여기서 유추할 수 없다.

### Verification

헬스는 부분적이다. 런타임 수용 기준에는 DB 접근, gateway와 앱 권한 부여,
백그라운드 작업 완료, 대표 분석이 포함되며 백업/복구를 주장하는 경우 그
증거도 포함된다.

### Review Cadence

릴리스, DB/플러그인/인증/토큰, 리소스, 보존 정책 변경 시 검토한다.

### Traceability

- [가이드](../guides/0066-sonarqube.md) (`GDE-0066`)
- [런북](../runbooks/0066-sonarqube.md) (`RUN-0066`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [SonarQube Compose 소스](../../../infra/11-quality/sonarqube/docker-compose.yml)
- [Community Build 인증](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [SonarQube 토큰 관리](https://docs.sonarsource.com/sonarqube-community-build/user-guide/managing-tokens)
