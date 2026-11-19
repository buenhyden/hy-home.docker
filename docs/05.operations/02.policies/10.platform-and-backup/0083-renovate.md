---
title: "Renovate Policy"
version: "0.5.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0083"
parent_ids:
- "AD-0009"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# Renovate Policy

## Purpose and Scope

### Objective

Renovate는 HOME 호스트에서 self-hosted로 실행하는 Compose job(`dependency-update` profile)이며 설치된 주간 systemd timer(월요일, 일정 창 00–05시 KST)가 기본 실행이고 Compose `run --rm`은 rebase·재시도용 온디맨드 실행이며
원격 저장소 쓰기 권한을 가진다. HOME이나 일반 도구 기동에는 절대 포함되지 않는다.
상시 서비스가 아니며 메모리 상한은 2 GiB다.

#### Authority

- 설계 근거: [AD-0009](../../../02.architecture/01.descriptions/0009-tooling-architecture.md)

- [Renovate Compose source](../../../../infra/09-platform-ops/renovate/docker-compose.yml)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)

### Applies To

이 정책은 `renovate`와 그 Docker Secret, 설정, 캐시, 원격 변경사항, 업그레이드, 증거를
다룬다. 업데이트 규칙(그룹, 보류, digest pin, ledger 재결합, PR 처리)의 권위는 `POL-0086`에 있다. 추적하는 manager와 파일 목록(`infra/` 아래 Compose와 `requirements.txt`, `labs/**` 제외)은 `renovate.json5`가 소유한다.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0083-R1 | 항상 | 필수: `renovate_token`은 선언된 secret으로만 마운트한다 | 수동 | none |
| POL-0083-R2 | 항상 | 필수: 최소한의 저장소와 권한만 부여한다 | 수동 | none |
| POL-0083-R3 | 항상 | 금지: 토큰 파일이나 렌더링된 secret 출력 | 수동 | none |
| POL-0083-R4 | 항상 | 필수: `allowScripts: false`와 명시적 명령어 allowlist를 유지한다 | 수동 | none |
| POL-0083-R5 | `allowScripts` 또는 allowlist 확장 시 | 필수: 보안 검토와 범위가 명확한 정당화를 갖춘다 | 수동 | none |
| POL-0083-R6 | 실제 실행 전 | 필수: 저장소와 self-host 설정을 엄격히 검증한다 | Runbook step 1의 저장소/self-host 설정 검증 | none |
| POL-0083-R7 | validator PASS 시 | 필수: PASS를 구문 증거로만 취급한다 | none | validator 결과 |
| POL-0083-R8 | 실제 job 실행 전 | 필수: 브랜치와 pull request 생성에 대한 승인을 받는다 | 수동 | none |
| POL-0083-R9 | 머지, 닫기, 토큰 회전 시 | 필수: 별도로 승인한다 | 수동 | none |
| POL-0083-R10 | 항상 | 필수: 캐시를 일회성으로 유지한다 | 수동 | none |
| POL-0083-R11 | 항상 | 금지: 캐시를 저장소의 진실로 취급하거나 비즈니스 상태로 백업 | 수동 | none |
| POL-0083-R12 | 이미지 업그레이드 시 | 필수: 불변 선언, 공식 마이그레이션/릴리스 검토, 엄격한 검증, dry-run/discovery, 범위가 제한된 하나의 canary 저장소를 거친다 | 수동 | none |
| POL-0083-R13 | job 실행 시 | 필수: 실행 시각, 설정 커밋, 대상 저장소, 이미지 선언, sanitize된 결과, secret 값 없이 생성된 PR을 기록한다 | none | none |
| POL-0083-R14 | timer가 시작한 실행과 수동 실행 | 필수: 같은 승인·근거 규칙을 적용한다 | none | none |
| POL-0083-R15 | `Persistent=true` catch-up 시 | 필수: 원격 변경 승인 범위에 포함한다 | 수동 | none |
| POL-0083-R16 | host unit 설치·교체 시 | 필수: 검토된 사본으로만 수행한다 | none | none |
| POL-0083-R17 | 이미지 태그를 불변성 근거로 삼을 때 | 필수: 태그가 resolved digest와 같지 않으므로 불변성 통제의 충족 여부를 따로 확인한다 | none | none |

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

#### 예약 실행 책임

설치된 주간 systemd timer가 기본 실행이고 Compose `run --rm`은 온디맨드 실행이다.
timer가 시작한 실행과 수동 실행에는 같은 승인·근거 규칙이 적용된다.
`Persistent=true`의 catch-up도 원격 변경 승인 범위에 포함해야 한다. 책임자는
`@buenhyden`이며 host unit 설치·교체는 검토된 사본으로만 수행한다. 이미지 태그는
resolved digest와 같지 않으므로 불변성 통제의 충족 여부를 따로 확인한다.

### Exceptions

#### Exception Conditions

토큰 권한, 저장소 범위, 허용 명령어, 스크립트 실행, 원격 변경의 확대는 기록된 owner,
만료일, 롤백, 보안 검토가 필요하다. 구문 검증을 통과해도 실제 실행 승인은 면제되지 않는다.

#### Approval and Review

매월, 그리고 이미지, 토큰 범위, 저장소 목록, manager, 허용 명령어, `POL-0086`이 변경될
때마다 검토한다.

## Enforcement

### Mechanisms

[Runbook step 1](../../03.runbooks/10.platform-and-backup/0083-renovate.md#steps)에 따라 실제 실행 전에 저장소와
self-host 설정 검증을 반드시 통과해야 한다.

### Limits

정책 본문이 기계적 강제를 명시하지 않는 항목은 다음과 같다.

- token·권한: 수동 검토/승인에 의존: `POL-0083-R1`, `POL-0083-R2`, `POL-0083-R3`
- 스크립트·allowlist: 수동 검토/승인에 의존: `POL-0083-R4`, `POL-0083-R5`
- 실행 전 검증: 지정된 검사 없음: `POL-0083-R7`
- 실행 승인: 수동 검토/승인에 의존: `POL-0083-R8`, `POL-0083-R9`
- 캐시: 수동 검토/승인에 의존: `POL-0083-R10`, `POL-0083-R11`
- 이미지 업그레이드: 수동 검토/승인에 의존: `POL-0083-R12`
- 실행 기록: 지정된 검사 없음: `POL-0083-R13`
- 예약 실행: 수동 검토/승인에 의존: `POL-0083-R15` / 지정된 검사 없음: `POL-0083-R14`, `POL-0083-R16`, `POL-0083-R17`
- validator PASS는 구문 증거일 뿐이며 실제 실행 승인을 대신하지 않는다.
- 이미지 태그는 resolved digest와 같지 않아 불변성 통제 충족 여부를 따로 확인해야 한다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- 동일 주제 문서: [Guide](../../01.guides/10.platform-and-backup/0083-renovate.md), [Runbook](../../03.runbooks/10.platform-and-backup/0083-renovate.md)

- [Renovate security and permissions](https://docs.renovatebot.com/security-and-permissions/)
- [Operations index](../../README.md)
