---
title: "Conftest Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0095"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# Conftest Operations Policy

## Overview

`infra/11-quality/conftest/policy/` 아래의 Rego 규칙은 저장소 컨테이너
baseline의 실행 가능한 부분집합이다. 새 규칙을 추가하지 않으며 각 규칙은
다른 정책이 이미 소유한 통제를 그대로 다시 적은 것이다.

## Policy Scope

규칙, 그 allowlist, job의 접근 범위, 실패의 해결 방식.

## Controls

- 모든 규칙은 같은 디렉터리에 unit test를 가지며, job은 소스를 테스트하기
  전에 `conftest verify`를 실행한다. 실패 케이스와 통과 케이스가 모두 없는
  규칙은 병합하지 않는다.
- allowlist 항목(예: privileged에 대한 `cadvisor`)은 정책 파일에 서비스명과
  이유를 명시한다. allowlist는 검토된 변경으로만 늘어난다.
- 새 `deny`는 병합되기 전에 현재 소스에서 통과해야 한다. 소스가 충족할 수
  없는 규칙은 `warn`으로 시작한다.
- job은 `infra/`만 읽기 전용으로 마운트하고, 네트워크 없이 non-root
  사용자로 실행한다. `secrets/`, `.env`, Docker 소켓은 절대 마운트하지
  않는다.
- `deny`가 발동하면 규칙이 아니라 선언을 고친다.

## Exceptions

정책 파일의 allowlist를 넘어서는 예외는 없다.

## Verification

`conftest verify`(정책 unit test)와 모든 Compose 파일 및 Dockerfile에 대한
깨끗한 `conftest test`. 의도적으로 잘못된 파일은 모든 규칙에서 실패해야
한다.

## Review Cadence

컨테이너 baseline 통제가 바뀔 때, Conftest 또는 OPA major 업그레이드 시,
allowlist 항목이 추가될 때마다 검토한다.

### 적용 범위와 책임

책임자는 `@buenhyden`이다. raw 파일 탐색으로 선택되지 않는 inline Dockerfile과
최종 Compose·실행 상태의 통제도 여전히 요구된다. 이 도구의 PASS는 전체 인프라 보안
준수 판정이 아니다. 새 규칙의 단계적 warn 도입 조건은 기존 강제 통제를 약화할
허가가 아니며 정책 단위 테스트·검토된 예외 근거를 유지한다.

## Traceability

- [가이드](../guides/0095-conftest.md) (`GDE-0095`)
- [런북](../runbooks/0095-conftest.md) (`RUN-0095`)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)

## Related Documents

- [Conftest Compose source](../../../infra/11-quality/conftest/docker-compose.yml)
- [Dependency version management](0086-dependency-version-management.md)
