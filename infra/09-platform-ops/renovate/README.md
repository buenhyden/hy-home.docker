---
title: "Renovate Implementation"
version: "0.2.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
---

# Renovate

## Overview

명시적 버전 업데이트 작업입니다. 저장소 정책은 renovate.json5이며
config/config.js가 self-host 명령 allowlist를 소유합니다. renovate_token은
Docker Secret으로 마운트됩니다. 캐시 볼륨은 일회용이며 게시되는 호스트 포트는
없습니다.

## Audience

서비스 설정을 검토하는 운영자와 개발자.

## Scope

Lifecycle: **DEV maintenance job**. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/guides/0083-renovate.md`, `docs/05.operations/policies/0083-renovate.md`, `docs/05.operations/runbooks/0083-renovate.md`(ID: `GDE-0083`, `POL-0083`, `RUN-0083`)가 담당합니다.

## Structure

[Compose](docker-compose.yml)가 서비스, 마운트, 네트워크 권한, 엔트리포인트를 소유합니다.

```text
renovate/
├── config/
│   └── config.js          # self-host command allowlist
├── systemd/
│   ├── hyhome-renovate.service  # oneshot service unit
│   └── hyhome-renovate.timer   # weekly schedule trigger
└── docker-compose.yml
```

## Tech Stack

런타임 고정 값은 [Compose](docker-compose.yml)에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션이며 배포 매니페스트가 아닙니다.

## Configuration

프로필: `dependency-update`. 루트 Compose가 이 정의를 include하지만 include 자체만으로는 서비스가 시작되지 않습니다. 프로젝트 기본 네트워크를 사용합니다. 비공개 값을 출력하지 않고 [공개 환경 변수 키](../../../.env.example)와 [시크릿 참조](../../../secrets/README.md)를 검토합니다.

## Validation

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 실행합니다. 런타임 확인은 소유 Runbook을 사용합니다. 설정 검증만으로는 유지보수 작업의 성공이나 원격 저장소 업데이트를 증명하지 못합니다.

## How to Work in This Area

변경 작업 중에는 데이터와 자격 증명을 보존합니다. 배포 전에 정확한 런타임 대상을 검토합니다. 운영 절차는 기존 운영 주제(operations subject) 안에 유지합니다.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
