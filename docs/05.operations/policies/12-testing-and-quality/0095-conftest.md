---
title: "Conftest Operations Policy"
version: "1.0.4"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-27"
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

## Scope

규칙, 그 allowlist, job의 접근 범위, 실패의 해결 방식.

## Rules

- 모든 규칙은 같은 디렉터리에 unit test를 가지며, job은 소스를 테스트하기
  전에 `conftest verify`를 실행한다. 등록된 `verify`·`corpus` lane은 분리되며
  기본 `all`은 두 단계를 순서대로 실행한다. 실패·통과 케이스가 모두 없는 규칙은
  병합하지 않는다.
- allowlist 항목(예: privileged에 대한 `cadvisor`)은 정책 파일에 서비스명과
  이유를 명시한다. allowlist는 검토된 변경으로만 늘어난다.
- 새 `deny`는 병합되기 전에 현재 소스에서 통과해야 한다. 소스가 충족할 수
  없는 규칙은 `warn`으로 시작한다.
- job은 공개 `infra/`·`labs/`와 wrapper가 준비한 공개 파생 입력만 읽기 전용으로
  마운트하고 네트워크 없이 non-root 사용자로 실행한다. `secrets/`, `.env`,
  Docker socket, 호스트 root·Git·scripts는 마운트하지 않는다.
- corpus 권위는 기존 canonical Git 추적 소스 목록이다. 무시된 설치 산출물은
  읽지 않으며 무시되지 않은 미추적 소스 후보는 Docker 전에 실패한다.
  wrapper는 POL-0078로 검증한 overlay의 원본 base profile만 정책 입력에
  보충한다. 실행용 Compose나 다른 정책 필드를 바꾸는 예외가 아니다.
- `corpus`·기본 `all`에는 wrapper의 완전한 두 소스 목록과 digest가 필요하다.
  준비가 없거나 잘못되면 실패하며 raw fallback은 없다. 직접 job `verify`는
  유지한다. 원본·기존 권한을 변경하지 않고 임시 입력만 종료 후 정리한다.
- `deny`가 발동하면 규칙이 아니라 선언을 고친다.

### 적용 범위와 책임

책임자는 `@buenhyden`이다. raw 파일 탐색으로 선택되지 않는 inline Dockerfile과
최종 Compose·실행 상태의 통제도 여전히 요구된다. 이 도구의 PASS는 전체 인프라 보안
준수 판정이 아니다. 새 규칙의 단계적 warn 도입 조건은 기존 강제 통제를 약화할
허가가 아니며 정책 단위 테스트·검토된 예외 근거를 유지한다.

## Exceptions

정책 파일의 allowlist를 넘어서는 예외는 없다.

### Review Cadence

컨테이너 baseline 통제가 바뀔 때, Conftest 또는 OPA major 업그레이드 시,
allowlist 항목이 추가될 때마다 검토한다.

### Traceability

- [가이드](../../guides/12-testing-and-quality/0095-conftest.md) (`GDE-0095`)
- [런북](../../runbooks/12-testing-and-quality/0095-conftest.md) (`RUN-0095`)
- [Compose profile vocabulary](../01-common/0078-compose-profile-vocabulary.md)

## Verification

`conftest verify`(정책 unit test)와 모든 Compose 파일 및 Dockerfile에 대한
깨끗한 `conftest test`. 의도적으로 잘못된 파일은 모든 규칙에서 실패해야
한다.

## Related Documents

- [Conftest Compose source](../../../../infra/11-quality/conftest/docker-compose.yml)
- [Dependency version management](../10-platform-and-backup/0086-dependency-version-management.md)
