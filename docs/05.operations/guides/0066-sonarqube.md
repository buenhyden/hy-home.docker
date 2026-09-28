---
title: "SonarQube Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0066"
parent_ids:
- "POL-0066"
implementation_services:
  infra/09-tooling/sonarqube/docker-compose.yml:
  - sonarqube
created: "2026-05-10"
---

# SonarQube Usage Guide

## Usage

### 목적과 분류

SonarQube Community Build는 `tooling`과 `sast` 하위의 온디맨드 **OPTIONAL**
코드 품질/SAST 서비스이며 HOME에서 제외된다. 이 저장소는 이 서비스 가이드에서
범용 병합 품질 게이트를 정의하지 않는다. 분석 결과로 배포를 어떻게 게이팅할지는
프로젝트/CI 소유자가 정한다.

### 현재 구현과 흐름

- [SonarQube Compose](../../../infra/09-tooling/sonarqube/docker-compose.yml)가
  런타임 이미지, profile, DB secret, JVM heap, 라우트, 볼륨, health를 정의한다.
- 브라우저/스캐너 -> Traefik -> SonarQube 순으로 흐른다. 라우트는 OAuth2 Proxy
  ForwardAuth를 사용한다. 추적되는 SonarQube SAML/OIDC 설정이 없으므로 네이티브
  Keycloak 로그인이나 그룹 프로비저닝은 증명되지 않는다. SonarQube 사용자, 권한,
  분석 토큰은 여전히 애플리케이션 소유 영역이다.
- `${POSTGRES_MNG_HOSTNAME}`의 PostgreSQL이 권위 있는 프로젝트, 설정, 이슈,
  사용자, 분석 상태를 저장한다. `/opt/sonarqube/data`는 로컬 검색 인덱스를,
  `/opt/sonarqube/logs`는 로그를 저장한다. Compose leaf에는 영속적인
  extensions/plugins/config 볼륨이 없다.
- `sonarqube_db_password`는 파일로 마운트된다. 분석 토큰은 SonarQube에서
  생성되며 Compose나 증거에는 절대 포함되지 않는다.
- 추적되는 환경변수가 web과 search JVM의 heap을 모두 512 MiB로 제한한다.
  이 서비스는 `template-stateful-high`를 상속한다.
- `/api/system/health`는 프로세스 health만 증명한다. DB 백업, 인덱스 일관성,
  스캐너 인가, 게이트웨이 로그인을 증명하지 않는다.

### 일반적인 사용

1. 루트에서 `docker compose --profile sast config --quiet`로 검증하고 management
   PostgreSQL 의존성을 별도로 확인한다.
2. SonarQube만 시작하고 system health를 기다린 다음, 게이트웨이 접근과 SonarQube
   권한을 별도 통제로 검증한다.
3. 최소 권한의 만료 가능한 프로젝트/글로벌 분석 토큰을 사용한다. 토큰이 shell history와
   로그에 남지 않게 한다.
4. 대상 프로젝트에 스캐너를 실행하고 토큰이나 소스 콘텐츠 없이 프로젝트 키,
   커밋, 품질 결과, task ID를 기록한다.

### 백업, 복원, 업그레이드

데이터베이스가 백업 권한을 갖는다. 공식 가이드는 데이터베이스 네이티브 백업을
사용하고 복원 후 Elasticsearch 인덱스를 재구축한다. 일관되게 복구하려면 추적되는 설정,
DB secret 보관, 여기 표현되지 않은 외부 설치 plugin/config도 보존해야 한다.
격리된 DB로 복원하고, 로컬 인덱스가 없는 상태로 SonarQube를 시작하여 재인덱싱을
허용한 다음, 프로젝트/설정/사용자와 대표 스캔을 검증한다. 활성 인덱스 삭제는
절대 1차 복구 방법으로 삼지 않는다.

업그레이드 전에는 DB를 백업/검증하고, 모든 release/업그레이드 노트를 읽고, DB와
호스트 전제 조건을 확인하고, plugin 인벤토리를 작성하고, 복원된 사본에서
테스트한다. 롤백에는 이전 이미지와 업그레이드 이전 데이터베이스가 모두 필요하다.
이미지 롤백만으로는 스키마 마이그레이션을 되돌릴 수 없다. 여기서는 백업/복원/
업그레이드를 실행하지 않았다.

## Common Checks

- `docker compose --profile sast config --quiet`
- `docker compose --profile sast config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

DB 장애, 인덱싱 복구, 분석 큐, 업그레이드에는 [runbook](../runbooks/0066-sonarqube.md)을
사용한다.

## Traceability

- [Policy](../policies/0066-sonarqube.md) (`POL-0066`)
- [Runbook](../runbooks/0066-sonarqube.md) (`RUN-0066`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [SonarQube backup and restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade guide](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
- [Community Build authentication capabilities](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [Community Build Web API authentication](https://docs.sonarsource.com/sonarqube-community-build/extension-guide/web-api)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
