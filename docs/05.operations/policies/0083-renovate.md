---
title: "Renovate Policy"
version: "0.1.2"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0083"
parent_ids:
- "AD-0009"
created: "2026-09-19"
---

# Renovate Policy

## Overview

### Overview

Renovate는 원격 저장소 쓰기 권한을 가지며 명시적으로 선택하는 `dependency-update` job이다.
HOME이나 일반 도구 기동에는 절대 포함되지 않는다.

## Scope

### Policy Scope

이 정책은 `renovate`와 그 Docker Secret, 설정, 캐시, 원격 변경사항, 업그레이드, 증거를
다룬다. 업데이트 전략의 권위는 `POL-0086`에 있다.

### Traceability

- 설계 근거: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- 동일 주제 문서: [Guide](../guides/0083-renovate.md), [Runbook](../runbooks/0083-renovate.md)

## Rules

### Controls

- `renovate_token`은 선언된 secret으로만 마운트하고 최소한의 저장소와 권한만 부여한다.
  토큰 파일이나 렌더링된 secret을 절대 출력하지 않는다.
- `allowScripts: false`와 명시적 명령어 allowlist를 유지한다. 둘 중 하나라도 확장하려면
  보안 검토와 범위가 명확한 정당화가 필요하다.
- 실행 전 저장소와 self-host 설정을 엄격히 검증한다. validator PASS는 구문 증거로만
  취급한다.
- 브랜치와 pull request를 생성할 수 있으므로 실제 job 실행 전에 승인을 받는다. 머지,
  닫기, 토큰 회전은 별도로 승인되는 작업이다.
- 캐시는 일회성으로 유지한다. 저장소의 진실로 취급하거나 비즈니스 상태로 백업하지
  않는다. 지속적인 설정과 생성된 변경사항은 Git과 원격 호스팅 서비스가 소유한다.
- 이미지의 불변 선언, 공식 마이그레이션/릴리스 검토, 엄격한 검증, dry-run/discovery,
  범위가 제한된 하나의 canary 저장소를 통해 업그레이드한다.
- job 실행 시각, 설정 커밋, 대상 저장소, 이미지 선언, sanitize된 결과, secret 값 없이
  생성된 PR을 기록한다.

### Verification

[Runbook step 1](../runbooks/0083-renovate.md#procedure)에 따라 실제 실행 전에 저장소와
self-host 설정 검증을 반드시 통과해야 한다.

### Review Cadence

매월, 그리고 이미지, 토큰 범위, 저장소 목록, manager, 허용 명령어, `POL-0086`이 변경될
때마다 검토한다.

### 예약 실행 책임

timer가 시작한 실행과 수동 실행에는 같은 승인·근거 규칙이 적용된다.
`Persistent=true`의 catch-up도 원격 변경 승인 범위에 포함해야 한다. 책임자는
`@buenhyden`이며 host unit 설치·교체는 검토된 사본으로만 수행한다. 이미지 태그는
resolved digest와 같지 않으므로 불변성 통제의 충족 여부를 따로 확인한다.

## Exceptions

### Exceptions

토큰 권한, 저장소 범위, 허용 명령어, 스크립트 실행, 원격 변경의 확대는 기록된 owner,
만료일, 롤백, 보안 검토가 필요하다. 구문 검증을 통과해도 실제 실행 승인은 면제되지 않는다.

## Related Documents

- [Renovate Compose source](../../../infra/09-platform-ops/renovate/docker-compose.yml)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Renovate security and permissions](https://docs.renovatebot.com/security-and-permissions/)
- [Operations index](../README.md)
