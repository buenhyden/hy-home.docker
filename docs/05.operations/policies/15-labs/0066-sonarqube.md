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
| POL-0066-R1 | 항상 | 필수: LAB profile `sast`를 `labs/sonarqube/docker-compose.yml`에서만 사용한다 | none | none |
| POL-0066-R2 | 기동 시 | 필수: `scripts/operations/lab.py` lease로 기동한다 | none | none |
| POL-0066-R3 | 항상 | 금지: root include, HOME 안 배치 | none | none |
| POL-0066-R4 | 항상 | 금지: gateway route와 SSO 구성 | none | none |
| POL-0066-R5 | 항상 | 필수: UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}` bind의 `LAB_SONARQUBE_HOST_PORT`에만 게시한다 | none | none |
| POL-0066-R6 | loopback 밖 bind 시 | 필수: 별도 보안 검토를 거친다 | 수동 | none |
| POL-0066-R7 | 항상 | 금지: HOME network 합류 | none | none |
| POL-0066-R8 | mng-pg 접근 시 | 필수: 승인된 `LAB_SONARQUBE_DB_HOST` endpoint로만 접근한다 | none | none |
| POL-0066-R9 | 항상 | 필수: SonarQube를 유일한 진입 인증으로 쓰고 애플리케이션 사용자/그룹/권한/토큰을 SonarQube가 소유한다 | none | none |
| POL-0066-R10 | 네이티브 위임 인증이 구성/테스트되기 전 | 금지: 네이티브 위임 인증이 있다고 전제 | none | none |
| POL-0066-R11 | IdP 비활성화 시 | 필수: 기존 SonarQube 토큰을 SonarQube에서 직접 폐기한다 | 수동 | none |
| POL-0066-R12 | 토큰 발급 시 | 필수: 최소 범위의 만료 토큰을 발급한다 | 수동 | none |
| POL-0066-R13 | 토큰 보관 시 | 필수: 승인된 CI 시크릿 소유자에게 저장한다 | 수동 | none |
| POL-0066-R14 | 항상 | 금지: 토큰 값 로깅 | 수동 | none |
| POL-0066-R15 | 항상 | 필수: 토큰을 회전/폐기한다 | 수동 | none |
| POL-0066-R16 | 항상 | 필수: PostgreSQL을 권위 있는 데이터로 취급한다 | none | none |
| POL-0066-R17 | 로그 보관 시 | 필수: `sonarqube-logs`는 사고/증거 보존 정책을 따른다 | none | none |
| POL-0066-R18 | backup 판단 시 | 금지: 데이터 볼륨만으로 백업으로 간주 | none | none |
| POL-0066-R19 | backup 시 | 필수: 데이터베이스 네이티브 백업을 사용하고 검증한다 | 수동 | none |
| POL-0066-R20 | 복구 리허설 시 | 필수: 격리된 복구와 재인덱싱을 리허설한다 | 수동 | none |
| POL-0066-R21 | backup 시 | 필수: 추적 중인 설정과 외부 플러그인 인벤토리를 함께 캡처한다 | 수동 | none |
| POL-0066-R22 | 항상 | 필수: 추적 중인 heap 및 stateful-high 제한을 준수한다 | none | none |
| POL-0066-R23 | 리소스 변경 시 | 필수: 측정된 queue/heap/index 증거와 호스트 용량에 근거해서만 변경한다 | none | none |
| POL-0066-R24 | upgrade 시 | 필수: 에디션/버전 호환성, DB/호스트 요구사항, 플러그인 호환성을 검토한다 | 수동 | none |
| POL-0066-R25 | upgrade 시 | 필수: 복원된 데이터에서 테스트한다 | 수동 | none |
| POL-0066-R26 | rollback 시 | 필수: 이미지와 DB를 함께 롤백한다 | 수동 | none |
| POL-0066-R27 | database/schema 또는 volume 삭제 전 | 필수: 프로젝트, 설정, 이슈, 사용자, 토큰, 백업 증거를 보존하거나 명시적으로 폐기한다 | 수동 | none |
| POL-0066-R28 | 항상 | 필수: 승인/예외/데이터 복구 책임자는 `@buenhyden`이다 | none | none |
| POL-0066-R29 | 인증 실패 해결 시 | 금지: SonarQube 인증 완화, port 넓은 게시 | none | none |
| POL-0066-R30 | 공유 PostgreSQL 전체를 복원하는 변경 시 | 필수: 다른 데이터 소유자의 영향 검토와 별도 승인을 받는다 | 수동 | none |

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

정책은 요구사항별 이름 붙은 검사를 지정하지 않으며, 아래 규칙은 승인/검토에 의존하거나 강제 수단이 없다.

- 격리/노출: 수동 검토 `POL-0066-R6`; 강제 수단 없음 `POL-0066-R1`~`R5`, `POL-0066-R7`~`R8`
- 인증/token: 수동 검토 `POL-0066-R11`~`R15`; 강제 수단 없음 `POL-0066-R9`~`R10`
- data/backup: 수동 검토 `POL-0066-R19`~`R21`; 강제 수단 없음 `POL-0066-R16`~`R18`
- 리소스: 강제 수단 없음 `POL-0066-R22`~`R23`
- upgrade/removal: 수동 검토 `POL-0066-R24`~`R27`
- 책임/승인: 수동 검토 `POL-0066-R30`; 강제 수단 없음 `POL-0066-R28`~`R29`
- `LAB_SONARQUBE_DB_HOST` endpoint 승인은 미결정이다.
- 네이티브 SAML/OIDC 위임 인증은 구성/테스트되기 전까지 존재하지 않는다.
- 헬스는 부분적이며 runtime 수용 기준(DB 접근, 앱 권한 부여, 백그라운드 작업 완료, 대표 분석, 백업/복구 증거)은 실행 시 기록에 의존한다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [가이드](../../guides/15-labs/0066-sonarqube.md) (`GDE-0066`)
- [런북](../../runbooks/15-labs/0066-sonarqube.md) (`RUN-0066`)
- [Community Build 인증](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [SonarQube 토큰 관리](https://docs.sonarsource.com/sonarqube-community-build/user-guide/managing-tokens)
