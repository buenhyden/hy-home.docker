---
title: "SonarQube Usage Guide"
version: "1.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "operations"
artifact_id: "GDE-0066"
parent_ids:
- "POL-0066"
implementation_services:
  labs/sonarqube.yml:
  - sonarqube
created: "2026-05-10"
---

# SonarQube Usage Guide

## Overview

SonarQube Community Build는 독립 LAB `labs/sonarqube.yml`(project `hy-home-lab-sonarqube`)의
`sonarqube` service로 운영하는 코드 품질·SAST 도구다. LAB profile `sast`에서만
선택되며 root Compose와 HOME에는 포함되지 않는다(SPEC-0262).

## Scope

### Audience and Goal

대상 독자는 코드 분석을 실행하는 개발자와 서비스를 운영하는 담당자다. 목표는 현재 구현의 인증 경계와
데이터 위치를 이해하고, 분석 토큰으로 스캐너를 안전하게 실행하는 것이다. DB 복구와 업그레이드는
[SonarQube Runbook](../../runbooks/15-labs/0066-sonarqube.md)이 맡는다.

## Concepts

### 분류와 범위

SonarQube Community Build는 LAB profile `sast` 하위의 온디맨드 **LAB**
코드 품질/SAST 서비스이며 HOME에서 제외된다. HOME network에 합류하지 않는다. 이 저장소는 이 서비스 가이드에서
범용 병합 품질 게이트를 정의하지 않는다. 분석 결과로 배포를 어떻게 게이팅할지는
프로젝트/CI 소유자가 정한다.

## Usage

### 현재 구현과 흐름

- [SonarQube Compose](../../../../labs/sonarqube.yml)가
  런타임 이미지, profile, DB secret, JVM heap, host port, 볼륨, health를 정의한다.
- gateway route와 SSO는 없다. 브라우저와 스캐너는
  `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_SONARQUBE_HOST_PORT:-18094}`로 SonarQube에 직접 접속한다.
  OAuth2 Proxy ForwardAuth는 더 이상 적용되지 않는다. 추적되는 SonarQube SAML/OIDC 설정이
  없으므로 SonarQube 자체 로그인과 사용자, 권한, 분석 토큰만이 접근 통제다.
- 권위 있는 프로젝트, 설정, 이슈, 사용자, 분석 상태는 HOME `mng-pg`에 있다. LAB은 필수 입력
  `LAB_SONARQUBE_DB_HOST`(`_PORT`, `_NAME`, `_USER` 포함, [공개 예시](../../../../labs/.env.example))로만
  접속한다. HOME은 기본적으로 mng-pg를 LAB network에 게시하지 않으므로 소유자가 도달 가능한
  endpoint를 승인하기 전까지 이 LAB은 render-only이다(미결정, 별도 승인). role과 DB는 계속 HOME
  `mng-pg-init`이 준비한다.
- `/opt/sonarqube/data`(로컬 검색 인덱스)와 `/opt/sonarqube/logs`는
  `${LAB_DATA_DIR}/sonarqube/{data,logs}` bind다. 이전 `${DEFAULT_TOOLING_DIR}/sonarqube/...`의
  데이터는 옮기지 않았으며, 옮기려면 별도 승인 아래 수동으로 이전한다. Compose에는 영속적인
  extensions/plugins/config 볼륨이 없다.
- DB 비밀번호는 LAB 전용 secret(`lab_sonarqube_*`, 파일은 `${LAB_SECRET_DIR:-../secrets/labs}/sonarqube/` 아래)으로
  원래 `/run/secrets/` 대상 경로에 mount되며 group은 `LAB_SECRETS_GID`다. HOME 값은 복사하지 않았다.
  HOME mng-pg `sonarqube` role 비밀번호의 LAB 사본 준비는 별도 승인 대상이다(미결정). 분석 토큰은 SonarQube에서
  생성되며 Compose나 증거에는 절대 포함되지 않는다.
- 추적되는 환경변수가 web과 search JVM의 heap을 모두 512 MiB로 제한한다.
  이 서비스는 `template-stateful-high`를 상속한다.
- `/api/system/health`는 프로세스 health만 증명한다. DB 백업, 인덱스 일관성,
  스캐너 인가, 게이트웨이 로그인을 증명하지 않는다.

### 일반적인 사용

1. 루트에서 `docker compose --env-file labs/.env -f labs/sonarqube.yml --profile sast config --quiet`로
   렌더링만 검증한다(부수 효과 없음). 승인된 mng-pg endpoint와 role/DB 준비를 별도로 확인한다.
2. 기동은 `python3 scripts/operations/lab.py check|up|down sonarqube`의 목적·lease 규칙만 따른다.
   system health를 기다린 다음 SonarQube 로그인과 권한을 확인한다.
3. 최소 권한의 만료 가능한 프로젝트/글로벌 분석 토큰을 사용한다. 토큰이 shell history와
   로그에 남지 않게 한다.
4. 대상 프로젝트에 스캐너를 실행하고 토큰이나 소스 콘텐츠 없이 프로젝트 키,
   커밋, 품질 결과, task ID를 기록한다.

### 백업, 복원, 업그레이드

실행 순서와 실패·복구 판단은 [런북](../../runbooks/15-labs/0066-sonarqube.md)의 `보존 대상과 사전 검토` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Runbook Handoff

DB 장애, 인덱싱 복구, 분석 큐, 업그레이드에는 [runbook](../../runbooks/15-labs/0066-sonarqube.md)을
사용한다.

### 준비 상태와 접근 제한

LAB Compose는 다른 project의 PostgreSQL을 기다리는 의존성을 선언할 수 없다. DB 소유자와
실제 database/role 준비를 별도로 확인한다. 공통 초기화 SQL의 고정 이름과 LAB 입력 변수를
바꾸는 작업은 같지 않다. 게시된 port 앞에 gateway SSO가 없으므로 SonarQube 로그인과 토큰이
유일한 인증 경계다. `LAB_HOST_BIND_IP`를 loopback 밖으로 바꾸는 것은 별도 보안 검토 대상이다.

### 버전 적용 한계

과거 Server 9.8/9.9 참고 링크는 현재 Community Build의 실행 절차를 보증하지 않는다. 업그레이드와 재인덱싱 복구 전 확인 사항은 [런북](../../runbooks/15-labs/0066-sonarqube.md)의 `버전 적용 한계`를 따른다.

### Traceability

- [Policy](../../policies/15-labs/0066-sonarqube.md) (`POL-0066`)
- [Runbook](../../runbooks/15-labs/0066-sonarqube.md) (`RUN-0066`)
- [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md)
- SPEC-0262 Analytics labs migration(LAB 이전)

## Troubleshooting

### Common Checks

- `docker compose --env-file labs/.env -f labs/sonarqube.yml --profile sast config --quiet`
- `docker compose --env-file labs/.env -f labs/sonarqube.yml --profile sast config --services`
- `python3 -m unittest tests.validation.test_lab_isolation`

## Related Documents

- [SonarQube backup and restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade guide](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
- [Community Build authentication capabilities](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [Community Build Web API authentication](https://docs.sonarsource.com/sonarqube-community-build/extension-guide/web-api)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)
