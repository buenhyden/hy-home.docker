---
title: "SonarQube Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0066"
parent_ids:
- "AD-0009"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# SonarQube Operations Policy

## Purpose and Scope

### Objective

이 정책은 독립 LAB `labs/sonarqube/docker-compose.yml`의 SonarQube Community Build 배포를 다루며 유료 에디션 기능,
네이티브 Keycloak 통합, 범용 CI 게이트는 가정하지 않는다.

#### Authority

- [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md)
- SPEC-0262 Analytics labs migration(LAB 이전)
- [SonarQube Compose 소스](../../../../labs/sonarqube/docker-compose.yml)

### Applies To

활성화, 애플리케이션 인증, LAB 노출, 토큰, 데이터베이스/인덱스/로그 데이터, 리소스
제한, 백업/복구, 업그레이드, 제거.

#### Exclusions

유료 에디션 기능, 네이티브 Keycloak 통합, 범용 CI 게이트는 이 정책이 가정하지 않는다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0066-R1 | LAB 기동 시 | 필수: LAB profile `sast`를 `labs/sonarqube/docker-compose.yml`에서만 쓰고 `scripts/operations/lab.py` lease로 기동하며 root에 include하지 않고 HOME 밖에 둔다 | `scripts/operations/lab.py` lease | none |
| POL-0066-R2 | 항상 | 필수: gateway route/SSO 없이 UI를 `${LAB_HOST_BIND_IP:-127.0.0.1}`의 `LAB_SONARQUBE_HOST_PORT`에만 게시하고(loopback 밖은 보안 검토) HOME network에 합류하지 않으며 mng-pg는 승인된 `LAB_SONARQUBE_DB_HOST` endpoint로만 접근한다(endpoint 승인 미결정) | 수동 | none |
| POL-0066-R3 | 항상 | 필수: SonarQube가 유일한 진입 인증이며 사용자/그룹/권한/토큰을 소유하고 IdP 비활성화로 기존 토큰이 폐기되지 않으므로 SonarQube에서 직접 폐기한다 | 수동 | none |
| POL-0066-R4 | 토큰 발급 시 | 필수: 최소 범위 만료 토큰을 발급해 승인된 CI 시크릿 소유자에게 저장하고 값을 로깅하지 않고 회전/폐기한다 | 수동 | none |
| POL-0066-R5 | 항상 | 필수: PostgreSQL이 권위 있는 데이터이며 검색 인덱스(`sonarqube-data`)는 재구축 가능, 로그(`sonarqube-logs`)는 사고/증거 보존 정책을 따르고 데이터 볼륨만으로 백업으로 간주하지 않는다 | 수동 | none |
| POL-0066-R6 | backup 시 | 필수: DB 네이티브 백업을 쓰고 검증하며 격리 복구와 재인덱싱을 리허설하고 추적 설정과 외부 플러그인 인벤토리를 함께 캡처한다 | 수동 | 백업/복구 증거 |
| POL-0066-R7 | 자원 변경 시 | 필수: 추적 중인 heap과 stateful-high 제한을 준수하고 측정된 queue/heap/index 증거와 호스트 용량에 근거해서만 변경한다 | 수동 | queue/heap/index 측정 증거 |
| POL-0066-R8 | upgrade 시 | 필수: 에디션/버전/DB/호스트/플러그인 호환성을 검토하고 복원 데이터에서 테스트하며 이미지와 DB를 함께 롤백한다 | 수동 | 복원 데이터 테스트 결과 |
| POL-0066-R9 | removal 시 | 필수: DB/스키마/볼륨 삭제 전 프로젝트/설정/이슈/사용자/토큰/백업 증거를 보존하거나 명시적으로 폐기한다 | 수동 | 백업 증거 |

- **Activation:** LAB profile `sast`를 `labs/sonarqube/docker-compose.yml`에서만 사용하고
  `scripts/operations/lab.py` lease로 기동한다. root에 include하지 않고 HOME 밖에 유지한다.
- **Exposure:** gateway route와 SSO가 없다. UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}` bind의
  `LAB_SONARQUBE_HOST_PORT`에만 게시하며 loopback 밖 bind는 별도 보안 검토가 필요하다. LAB은
  HOME network에 합류하지 않고 mng-pg는 승인된 `LAB_SONARQUBE_DB_HOST` endpoint로만 접근한다.
  그 endpoint 승인은 미결정이다.
- **Authentication:** SonarQube가 유일한 진입 인증이며 애플리케이션 사용자, 그룹, 권한,
  토큰을 소유한다. 네이티브 위임 인증은
  구성 및 테스트되기 전까지는 존재하지 않는다. IdP 비활성화만으로는 기존
  SonarQube 토큰이 자동으로 폐기되지 않으며, SonarQube에서 직접 폐기해야 한다.
- **Tokens:** 최소 범위의 만료 토큰을 발급하고, 승인된 CI 시크릿 소유자에게
  저장하며, 값을 로깅하지 않고 회전/폐기한다.
- **Data:** PostgreSQL이 권위 있는 데이터다. 로컬 검색 인덱스(named volume `sonarqube-data`)는 재구축 가능하며,
  로그(`sonarqube-logs`)는 사고/증거 보존 정책을 따른다. 데이터 볼륨만으로 백업으로 간주하지
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

#### 운영 책임

승인·예외·데이터 복구 책임자는 `@buenhyden`이다. 인증 실패를 해결하기 위해 SonarQube
인증을 완화하거나 port를 넓게 게시할 수 없다. 공유 PostgreSQL
전체를 복원하는 변경은 다른 데이터 소유자의 영향 검토와 별도 승인을 요구한다.

### Exceptions

#### Exception Conditions

유료 기능, 네이티브 SAML/OIDC 프로비저닝, 더 넓은 품질 게이트 요구사항은
각자의 소유 requirement/policy가 필요하며 여기서 유추할 수 없다.

#### Approval and Review

릴리스, DB/플러그인/인증/토큰, 리소스, 보존 정책 변경 시 검토한다.

## Enforcement

### Mechanisms

헬스는 부분적이다. 런타임 수용 기준에는 승인된 endpoint로의 DB 접근, 앱 권한 부여,
백그라운드 작업 완료, 대표 분석이 포함되며 백업/복구를 주장하는 경우 그
증거도 포함된다.

### Limits

이 정책은 요구사항별 이름 붙은 검사를 지정하지 않으며, 아래 항목은 기계적으로 강제되지 않는다.

- 헬스는 부분적이며, runtime 수용 기준(DB 접근, 앱 권한 부여, 백그라운드 작업 완료, 대표 분석, 백업/복구 증거)은 실행 시 기록에 의존한다.
- `LAB_SONARQUBE_DB_HOST` endpoint 승인은 미결정이다.
- 네이티브 SAML/OIDC 위임 인증은 구성/테스트되기 전까지 존재하지 않는다.
- 토큰 관리, 백업/복구 리허설, upgrade, removal은 수동 검토에 의존한다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [가이드](../../guides/15-labs/0066-sonarqube.md) (`GDE-0066`)
- [런북](../../runbooks/15-labs/0066-sonarqube.md) (`RUN-0066`)
- [Community Build 인증](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [SonarQube 토큰 관리](https://docs.sonarsource.com/sonarqube-community-build/user-guide/managing-tokens)
