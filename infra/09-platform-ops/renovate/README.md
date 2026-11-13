---
title: "Renovate Implementation"
version: "0.3.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Renovate

## Purpose

### Service Role

HOME 호스트의 self-hosted 버전 업데이트 작업입니다. 설치된 주간 systemd timer가 기본 실행이고, 온디맨드 실행(rebase·재시도)은 `docker compose -p hy-home-infra --profile dependency-update run --rm --no-deps renovate`입니다. 업데이트 규칙은 `POL-0086`(`docs/05.operations/policies/10-platform-and-backup/0086-dependency-version-management.md`)이 소유합니다. 저장소 정책은 renovate.json5이며
config/config.js가 self-host 명령 allowlist를 소유합니다. renovate_token은
Docker Secret으로 마운트됩니다. 캐시 볼륨은 일회용이며 게시되는 호스트 포트는
없습니다.

#### Audience

서비스 설정을 검토하는 운영자와 개발자.

#### Scope

Lifecycle: **DEV maintenance job**. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/guides/10-platform-and-backup/0083-renovate.md`, `docs/05.operations/policies/10-platform-and-backup/0083-renovate.md`, `docs/05.operations/runbooks/10-platform-and-backup/0083-renovate.md`(ID: `GDE-0083`, `POL-0083`, `RUN-0083`)가 담당합니다.

#### Structure

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

### Supported Environment

런타임 고정 값은 [Compose](docker-compose.yml)에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션이며 배포 매니페스트가 아닙니다.

2026-10-12 [공식 릴리스](https://github.com/renovatebot/renovate/releases/tag/44.151.3)와 <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
[공식 배포 안내](https://docs.renovatebot.com/getting-started/running/)를 대조하고, Docker `full` channel과
명시적 패치 태그의 OCI index가 같은지 확인했습니다. GitLab tag digest 조회의 실패 캐시와 ref 인코딩을
수정한 패치이며 기존 full 변형·설정·예약 실행·토큰 참조를 보존합니다. 실제 유지보수 실행과
원격 변경은 미실행입니다. 복구 시 이전 검토된 이미지 고정을 되돌리고, 실패한 실행의 캐시 처리와
이미 생성된 원격 변경을 별도로 확인해야 합니다.

## Interfaces

### Inputs and Outputs

프로필: `dependency-update`. 루트 Compose가 이 정의를 include하지만 include 자체만으로는 서비스가 시작되지 않습니다. 프로젝트 기본 네트워크를 사용합니다. 비공개 값을 출력하지 않고 [공개 환경 변수 키](../../../.env.example)와 [시크릿 참조](../../../secrets/README.md)를 검토합니다.

### Security Boundary

호스트 포트를 게시하지 않으며 프로젝트 기본 네트워크를 사용한다. `renovate_token`은 Docker Secret으로만 마운트하고 값은 문서에 쓰지 않는다. 실행 가능한 명령은 `config/config.js` allowlist가 제한한다.

## Development

### Local Workflow

변경 작업 중에는 데이터와 자격 증명을 보존합니다. 배포 전에 정확한 런타임 대상을 검토합니다. 운영 절차는 기존 운영 주제(operations subject) 안에 유지합니다.

### Checks

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 실행합니다. 런타임 확인은 소유 Runbook을 사용합니다. 설정 검증만으로는 유지보수 작업의 성공이나 원격 저장소 업데이트를 증명하지 못합니다.

## Operations

### Runbook Links

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [RUN-0083 renovate](../../../docs/05.operations/runbooks/10-platform-and-backup/0083-renovate.md)

- [RUN-0086 dependency-version-management](../../../docs/05.operations/runbooks/10-platform-and-backup/0086-dependency-version-management.md)

### Observability and Recovery

주간 systemd timer가 `hyhome-renovate.service`(oneshot)를 실행하므로 실행 결과는 해당 unit 상태로 확인한다. 실패 시 이전 검토된 이미지 고정으로 되돌리고 이미 생성된 원격 변경을 별도로 확인하며, 절차는 [Renovate Runbook](../../../docs/05.operations/runbooks/10-platform-and-backup/0083-renovate.md)을 따른다.
