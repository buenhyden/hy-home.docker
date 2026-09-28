---
title: "Mailpit Implementation"
version: "0.2.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
---

# Mailpit

## Overview

개발용 SMTP 트래픽을 캡처합니다. UI와 SMTP 호스트 포트는 loopback에
바인딩되며 UI는 인증된 Traefik을 통해 라우팅됩니다. `MAILPIT_UI_PORT`와
`MAILPIT_SMTP_PORT`는 컨테이너 리스너를 소유하고 `HOST_PORT` 변형은 게시를
소유합니다. `mailpit-data`는 `/data/mailpit.db`를 영속화합니다. 테스트 SMTP는
임의의 인증을 허용하므로 외부에 노출해서는 안 됩니다.

## Audience

서비스 설정을 검토하는 운영자와 개발자.

## Scope

Lifecycle: **DEV**. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/guides/0084-mailpit.md`, `docs/05.operations/policies/0084-mailpit.md`, `docs/05.operations/runbooks/0084-mailpit.md`(ID: `GDE-0084`, `POL-0084`, `RUN-0084`)가 담당합니다.

## Structure

[Compose](docker-compose.yml)가 서비스, 마운트, 네트워크 권한, 엔트리포인트를 소유합니다.

## Tech Stack

런타임 고정 값은 [Compose](docker-compose.yml)에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션이며 배포 매니페스트가 아닙니다.

## Configuration

프로필: `mail-dev / local / dev`. 루트 Compose가 이 정의를 include하지만, include 자체만으로는 서비스가 시작되지 않습니다. 네트워크는 `edge_net`입니다. 비공개 값을 출력하지 않고 [공개 환경 변수 키](../../../.env.example)와 [시크릿 참조](../../../secrets/README.md)를 검토합니다.

## Validation

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 실행합니다. 런타임 확인은 소유 Runbook을 사용합니다. 설정 검증만으로는 유지보수 작업의 성공이나 SMTP 캡처를 증명하지 못합니다.

## How to Work in This Area

변경 작업 중에는 데이터와 자격 증명을 보존합니다. 배포 전에 정확한 런타임 대상을 검토합니다. 운영 절차는 기존 운영 주제(operations subject) 안에 유지합니다.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
