---
title: "SonarQube Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0066"
parent_ids:
- "POL-0066"
implementation_services:
  infra/11-quality/sonarqube/docker-compose.yml:
  - sonarqube
created: "2026-05-10"
---

# SonarQube Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### 목적과 분류

SonarQube Community Build는 `tooling`과 `sast` 하위의 온디맨드 **OPTIONAL**
코드 품질/SAST 서비스이며 HOME에서 제외된다. 이 저장소는 이 서비스 가이드에서
범용 병합 품질 게이트를 정의하지 않는다. 분석 결과로 배포를 어떻게 게이팅할지는
프로젝트/CI 소유자가 정한다.

### 현재 구현과 흐름

- [SonarQube Compose](../../../infra/11-quality/sonarqube/docker-compose.yml)가
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

실행 순서와 실패·복구 판단은 [런북](../runbooks/0066-sonarqube.md)의 `보존 대상과 사전 검토` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `docker compose --profile sast config --quiet`
- `docker compose --profile sast config --services`
- `bash scripts/hardening/check-all-hardening.sh 11-quality`

### Runbook Handoff

DB 장애, 인덱싱 복구, 분석 큐, 업그레이드에는 [runbook](../runbooks/0066-sonarqube.md)을
사용한다.

### 준비 상태와 접근 제한

Compose는 PostgreSQL의 기동·완료를 기다리는 의존성을 선언하지 않는다. DB 소유자와
실제 database/role 준비를 별도로 확인한다. 공통 초기화 SQL의 고정 이름과 서비스의
설정 변수를 바꾸는 작업은 같지 않다. `edge_net`과 `mng_data_net`의 직접 경로도
점검해야 하며 gateway SSO가 모든 연결을 보호한다고 가정하지 않는다. 스캐너의
Sonar 토큰만으로 cookie 기반 ForwardAuth를 통과할 수 있는 것은 아니다. 로그인
경로를 우회하거나 인증을 제거하지 말고 승인된 클라이언트 경계를 먼저 확인한다.

### 버전 적용 한계

아래의 Server 9.8/9.9 링크는 과거 참고 자료이며 현재 Compose가 선택하는 Community
Build의 실행 절차를 보증하지 않는다. 현재 선언과 일치하는 release·DB·plugin 지원
근거를 확보하기 전에는 업그레이드와 재인덱싱 복구를 진행하지 않는다. 과거 명령을
현재 이미지에 그대로 적용하지 않고 `@buenhyden`에게 호환성 확인을 요청한다.

### Traceability

- [Policy](../policies/0066-sonarqube.md) (`POL-0066`)
- [Runbook](../runbooks/0066-sonarqube.md) (`RUN-0066`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [SonarQube backup and restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade guide](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
- [Community Build authentication capabilities](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [Community Build Web API authentication](https://docs.sonarsource.com/sonarqube-community-build/extension-guide/web-api)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
