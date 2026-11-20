---
title: "Renovate Implementation"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Renovate

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

HOME 호스트의 self-hosted 버전 업데이트 작업입니다. 설치된 주간 systemd timer가 기본 실행이고, 온디맨드 실행(rebase·재시도)은 `docker compose -p hy-home-infra --profile dependency-update run --rm --no-deps renovate`입니다. 업데이트 규칙은 `POL-0086`(`docs/05.operations/02.policies/10.platform-and-backup/0086-dependency-version-management.md`)이 소유합니다. 저장소 정책은 renovate.json5이며
config/config.js가 self-host 명령 allowlist를 소유합니다. renovate_token은
Docker Secret으로 마운트됩니다. 캐시 볼륨은 일회용이며 게시되는 호스트 포트는
없습니다.

###### Audience
<!-- core-payload-level:4 -->

서비스 설정을 검토하는 운영자와 개발자.

###### Scope
<!-- core-payload-level:4 -->

Lifecycle: **DEV maintenance job**. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/01.guides/10.platform-and-backup/0083-renovate.md`, `docs/05.operations/02.policies/10.platform-and-backup/0083-renovate.md`, `docs/05.operations/03.runbooks/10.platform-and-backup/0083-renovate.md`(ID: `GDE-0083`, `POL-0083`, `RUN-0083`)가 담당합니다.

###### Structure
<!-- core-payload-level:4 -->

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

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `hyhome-renovate.timer` -> `hyhome-renovate.service` | 주간 systemd timer | `renovate` 서비스(`dependency-update` profile) | 주간 oneshot 실행이 기본이며 온디맨드는 `docker compose -p hy-home-infra --profile dependency-update run --rm --no-deps renovate`이다 | 실행 결과는 unit 상태로 확인하고 RUN-0083 Renovate Runbook을 따른다 |
| 원격 저장소 업데이트 변경 | `renovate` | 원격 저장소 | `renovate_token` Docker Secret과 renovate.json5, POL-0086 규칙으로 버전 업데이트를 만든다 | 실패 시 이전 검토된 이미지 고정으로 되돌리고 이미 생성된 원격 변경을 별도로 확인한다 |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

프로필: `dependency-update`. 루트 Compose가 이 정의를 include하지만 include 자체만으로는 서비스가 시작되지 않습니다. 프로젝트 기본 네트워크를 사용합니다. 비공개 값을 출력하지 않고 [공개 환경 변수 키](../../../.env.example)와 [시크릿 참조](../../../secrets/README.md)를 검토합니다.

###### Security Boundary
<!-- core-payload-level:4 -->

호스트 포트를 게시하지 않으며 프로젝트 기본 네트워크를 사용한다. `renovate_token`은 Docker Secret으로만 마운트하고 값은 문서에 쓰지 않는다. 실행 가능한 명령은 `config/config.js` allowlist가 제한한다.

#### Usage

##### Prerequisites

런타임 고정 값은 [Compose](docker-compose.yml)에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션이며 배포 매니페스트가 아닙니다.

2026-10-12 [공식 릴리스](https://github.com/renovatebot/renovate/releases/tag/44.151.3)와 <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
[공식 배포 안내](https://docs.renovatebot.com/getting-started/running/)를 대조하고, Docker `full` channel과
명시적 패치 태그의 OCI index가 같은지 확인했습니다. GitLab tag digest 조회의 실패 캐시와 ref 인코딩을
수정한 패치이며 기존 full 변형·설정·예약 실행·토큰 참조를 보존합니다. 실제 유지보수 실행과
원격 변경은 미실행입니다. 복구 시 이전 검토된 이미지 고정을 되돌리고, 실패한 실행의 캐시 처리와
이미 생성된 원격 변경을 별도로 확인해야 합니다.

##### Selected Start

변경 작업 중에는 데이터와 자격 증명을 보존합니다. 배포 전에 정확한 런타임 대상을 검토합니다. 운영 절차는 기존 운영 주제(operations subject) 안에 유지합니다.

#### Checks

##### Readiness

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 실행합니다. 런타임 확인은 소유 Runbook을 사용합니다. 설정 검증만으로는 유지보수 작업의 성공이나 원격 저장소 업데이트를 증명하지 못합니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [10-platform-and-backup runbooks](../../../docs/05.operations/03.runbooks/10.platform-and-backup/README.md): RUN-0083 renovate, RUN-0086 dependency-version-management

###### Observability and Recovery
<!-- core-payload-level:4 -->

주간 systemd timer가 `hyhome-renovate.service`(oneshot)를 실행하므로 실행 결과는 해당 unit 상태로 확인한다. 실패 시 이전 검토된 이미지 고정으로 되돌리고 이미 생성된 원격 변경을 별도로 확인하며, 절차는 [10-platform-and-backup runbooks](../../../docs/05.operations/03.runbooks/10.platform-and-backup/README.md)의 RUN-0083 Renovate Runbook을 따른다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
