---
title: "Renovate Guide"
version: "0.2.3"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0083"
parent_ids:
- "POL-0083"
implementation_services:
  infra/09-platform-ops/renovate/docker-compose.yml:
  - renovate
created: "2026-09-19"
---

# Renovate Guide

## Overview

Renovate는 `infra/09-platform-ops/renovate/`의 `renovate` service로 실행하는 의존성 갱신 작업이다.
`dependency-update` profile에서만 선택된다.

## Audience and Goal

대상 독자는 의존성 갱신 PR을 승인하고 운영하는 담당자다. 목표는 job의 경계, 정적 검증 방법,
systemd timer 동작을 확인하는 것이다. live run과 복구 절차는 [Renovate Runbook](../runbooks/0083-renovate.md)이 맡는다.

## Usage

Renovate는 `dependency-update`에서만 선택하는 **DEV** one-shot repository
유지보수 작업이다. HOME과 일반 `tooling` 시작에서는 제외된다. root Compose
project는 `renovate.json5`, self-host 설정, `renovate_token` Docker Secret,
cache volume을 제공한다. live run은 원격 repository를 읽고 branch와 pull
request를 생성하거나 갱신할 수 있다.

### 구현 원본

- [Renovate Compose](../../../infra/09-platform-ops/renovate/docker-compose.yml)
- [Self-host configuration](../../../infra/09-platform-ops/renovate/config/config.js)
- [Repository configuration](../../../renovate.json5)
- [Dependency-version policy](../policies/0086-dependency-version-management.md) (`POL-0086`)

`renovate.json5`의 `docker-compose` manager는 `labs/*.yml`, `infra/07-workflow/n8n`, `infra/08-ai/crawl4ai`,
`infra/08-ai/ollama`, `infra/08-ai/open-webui`의 Compose 파일을 추적한다. 추적 목록은 [renovate.json5](../../../renovate.json5)가 소유한다.

`POL-0086`은 manager, release age, security update, automerge, updater
overlap을 관장한다. 이 package는 job 경계를 관장한다. `allowScripts: false`와
좁은 global command allowlist가 실행을 제한한다. cache는 다시 만들 수 있으며 Git
policy, 원격 repository 상태, token owner가 authoritative하다.

### 일반적인 사용

1. token이나 원격 변경 없이 repository와 global 설정을 확인한다.
   명령은 [Renovate Runbook 절차](../runbooks/0083-renovate.md#procedure)의 1단계를 따른다.

2. token repository scope, branch protection, dry-run 출력, 대상 repository를
   검토한다. validation은 token 권한을 증명하지 않는다.
3. live run은 외부 write 행위이므로
   [Renovate runbook](../runbooks/0083-renovate.md#procedure)에 있는 승인된
   절차로만 실행한다.

### 복구와 업그레이드

실행 순서와 실패·복구 판단은 [런북](../runbooks/0083-renovate.md)의 `캐시·원격 변경 복구와 업그레이드` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### systemd 예약 실행

repository는 `infra/09-platform-ops/renovate/`에 systemd unit 파일 두 개를
제공한다.

| File | Purpose |
|---|---|
| [`hyhome-renovate.service`](../../../infra/09-platform-ops/renovate/systemd/hyhome-renovate.service) | oneshot service — Renovate Compose job을 실행 |
| [`hyhome-renovate.timer`](../../../infra/09-platform-ops/renovate/systemd/hyhome-renovate.timer) | weekly timer — service unit을 트리거 |

#### Timer 동작

- **Schedule**: 월요일 00:00 KST에 최대 60분의 random jitter
  (`RandomizedDelaySec=3600`)를 둔다. 이 값은 `renovate.json5`의 schedule window
  (`Asia/Seoul` timezone의 `"* 0-5 * * 1"`)와 일치해서 host trigger와 in-app
  schedule guard가 같은 maintenance window를 쓰게 된다.
- **Missed fires**: `Persistent=true` 덕분에 월요일 trigger 시각에 host가
  오프라인이었다면 다음 boot 때 timer가 실행된다. 그 catch-up run은
  `renovate.json5` window를 벗어날 수 있다. 그 경우 Renovate는 Dependency
  Dashboard는 갱신하지만 window가 될 때까지 새 branch를 열지 않는다.
- **Start dependency**: timer에 `Requires=`가 없고 service에 `[Install]`이 없어도
  `Persistent=true`는 놓친 실행을 timer 활성화 때 재개할 수 있다. 설정된 random
  지연이 적용되므로 enable/start/reboot를 원격 쓰기 없는 조치로 취급하지 않는다.
- **Timezone**: `OnCalendar`는 `Asia/Seoul`을 지정한다. 설치된 systemd 버전과
  timer 해석은 승인된 호스트 점검에서 확인하며 과거 관측을 현재 상태로 인용하지 않는다.

#### Service 흐름

```text
Timer fires
  └─ ExecStartPre (1): assert renovate_token secret non-empty
  └─ ExecStartPre (2): docker compose pull --quiet renovate
  └─ ExecStart:        docker compose --profile dependency-update run --rm --no-deps renovate
```

run 이후에는 prune을 실행하지 않는다. `docker image prune`은 host 전역이다.
대체된 Renovate image tag는 정확한 reference로 수동 제거한다.

pre-flight check가 하나라도 실패하면 container를 만들기 전에 run이
중단된다. service는 자동 재시작하지 않으며(`Restart=no`), 실패한 run은 다음
시도 전에 사람이 log를 검토해야 한다.

#### 설치

호스트 설치·timer 활성화·수동 실행·중지는 [런북](../runbooks/0083-renovate.md)의 승인된 systemd 절차를 따른다.

### Common Checks

- repository와 self-host 설정에 대한 strict validation.
- `bash scripts/operations/sync-tech-stack-versions.sh --check`.
- 승인된 live job의 경우, sanitized 결과를 생성된 모든 branch/PR과 대조하고
  이 job 승인으로는 merge가 일어나지 않았는지 확인한다.

### 과거 호스트 관측

원본 위치: `docs/05.operations/guides/0083-renovate.md`, SPEC-0198 이전 Git 기록. 아래는 현재 호스트 상태의 근거가 아니다.

> Historical evidence (not current authority; source: Git history):
>
> - **Schedule**: 월요일 00:00 KST에 최대 60분의 random jitter
>   (`RandomizedDelaySec=3600`)를 둔다. 이 값은 `renovate.json5`의 schedule window
>   (`Asia/Seoul` timezone의 `"* 0-5 * * 1"`)와 일치해서 host trigger와 in-app
>   schedule guard가 같은 maintenance window를 쓰게 된다.
> - **Missed fires**: `Persistent=true` 덕분에 월요일 trigger 시각에 host가
>   오프라인이었다면 다음 boot 때 timer가 실행된다. 그 catch-up run은
>   `renovate.json5` window를 벗어날 수 있다. 그 경우 Renovate는 Dependency
>   Dashboard는 갱신하지만 window가 될 때까지 새 branch를 열지 않는다.
> - **Start dependency**: timer는 service에 `Requires=`를 선언하지 않고
>   service에는 `[Install]` section이 없으므로, timer를 enable하거나
>   start하거나 reboot해도 그 자체로 즉시 run이 시작되지는 않는다.
> - **Timezone**: `OnCalendar`는 `Asia/Seoul` suffix를 사용한다(systemd ≥ 242,
>   이 host는 255를 실행 중).

> Historical evidence (not current authority; source: Git history):
>
> host unit을 설치하거나 교체하는 것은 별도 승인이 필요한 host 변경이다.
> symlink 대신 검토된 파일을 복사해 checkout이나 branch 전환, pull이 systemd가
> 실행하는 내용을 조용히 바꾸지 못하게 한다. 2026-09-21에 확인한 설치된
> 복사본은 이 repository보다 오래된 revision이었다.

### 작업 신호와 상태 경계

작업에는 HTTP health가 없다. exit·정제된 실행 요약·생성된 PR을 함께 확인한다.
시작 shell은 token 파일 누락·빈 값을 거부하며 cache는 다시 만들 수 있는 지속
영역이다. 선언된 CPU·메모리 상한과 timeout 안에서 끝나는지 관찰하되 timeout을
원격 변경의 자동 취소로 해석하지 않는다. 캐시 삭제는 repository나 PR을 복구하지 않는다.

### Traceability

- 설계 근거: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- 동일 주제 문서: [Policy](../policies/0083-renovate.md), [Runbook](../runbooks/0083-renovate.md)

## Related Documents

- [hyhome-renovate.service](../../../infra/09-platform-ops/renovate/systemd/hyhome-renovate.service)
- [hyhome-renovate.timer](../../../infra/09-platform-ops/renovate/systemd/hyhome-renovate.timer)
- [Renovate self-hosted configuration](https://docs.renovatebot.com/self-hosted-configuration/)
- [Renovate configuration validation](https://docs.renovatebot.com/config-validation/)
- [systemd.timer(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)
- [systemd.time(7) — OnCalendar](https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html)
- [Operations index](../README.md)
