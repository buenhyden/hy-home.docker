---
title: "Dependency Version Management Policy"
version: "0.1.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0086"
parent_ids:
- "AD-0031"
created: "2026-09-19"
---

# Dependency Version Management Policy

## Overview

인프라 버전 변경은 하나의 HOME/DEV 호스트에서 검토 가능하고 재현 가능해야 한다. 버전
업데이트가 배포나 데이터 마이그레이션을 승인하지는 않는다.

## Policy Scope

Compose, Dockerfile 및 인라인 빌드 소스, derived registry, Renovate, Dependabot, 현재
구현/운영 문서의 런타임 버전 참조.

## Controls

| Surface | Update owner | Authority and review |
| --- | --- | --- |
| Compose 이미지와 일반 Dockerfile | Renovate | 활성화된 Docker manager; 소스 pin 변경 검토됨 |
| OpenTofu 인라인 Dockerfile | Renovate custom manager | 좁게 선언된 소스 패턴, 임의의 regex 범위 없음 |
| GitHub Actions 및 활성화된 인프라 manager | Renovate | 인프라 automerge 비활성화 |
| Storybook npm | Dependabot | 설정된 프로젝트 디렉터리에서만; Renovate npm과 중복 없음 |
| OpenTofu provider/module 의존성 | operator가 검토하는 workspace owner | tooling 패키지에 현재 추적되는 provider/module manifest가 없음; 그런 manifest가 처음 생길 때 범위가 제한된 manager를 활성화 |
| Python 검증 도구와 pre-commit hook | maintainer 검토 | pin된 requirements/hook revision; 현재 활성화된 자동 manager 범위 밖 |
| Derived Compose 이미지 registry | synchronization script | 추적되는 모든 인프라 Compose 저장소를 정확히 한 번씩, 명시적인 local/custom 분류와 파일별 정확한 소스 그룹으로 |
| 설명형 문서 | human/agent 검토와 기존 metadata validator | authority 링크; 정당화된 정확 리터럴 예외만 |

datasource가 릴리스 timestamp를 제공할 때, 정기적인 patch/minor 업데이트는 설정된
7일 soak window를 따른다. `timestamp-optional`이 있어 timestamp가 없는 registry에서도 무한정
기다리지 않는다. 그런 업데이트는 Monday 일정과 필수 수동 검토를 유지하며 7일 age를
주장하지 않는다. Major 업데이트는 별도로 다룬다. 보안 경고는
일반 대기를 우회하고 명시적 검토를 받는다. 긴급하더라도 마이그레이션이나 롤백 증거를
건너뛰지 않는다. 이 fast path는 설정된 manager가 실제로 수신하는 취약점 경고에
적용되며, 컨테이너 이미지 CVE 스캐닝이나 설치된 이미지의 취약점 범위를 확립하지 않는다.
infra automerge를 활성화하거나 self-host allowedCommands를 넓히지 않는다. 설정 구문은
저장소/전역 모드를 분리한 공식 strict validator를 통과해야 한다.

이미지 태그는 소스 pin이지만 변경 가능한 상태로 남을 수 있다. 존재하는 digest는
유지한다. 플랫폼 manifest, 업데이트 동작, 롤백 identity를 검증한 뒤 컴포넌트별로 digest
고정을 제안한다. 현재 정책은 Renovate digest pinning을 전역적으로 활성화하거나 일반
태그를 불변으로 취급하지 않는다. 예외 종료 조건은 검증된 digest를 요구할 수 있다. 의도된
아키텍처와 이미지 소스를 확인하지 않은 채 digest를 임의로 만들거나 다른 registry의
digest로 대체하지 않는다.

## Exceptions

변경 가능한 이미지 예외는 owner, reason, risk, review cadence, exit condition과 함께
`infra/image-tag-policy.exceptions.json`에 둔다. 서술식 예외로는 source-image
검증을 면제할 수 없다. 예외를 제거하기 전에 이미지 호환성을 검토한다. 태그 변경이
GPU나 데이터 형식 호환성의 증거가 되지는 않는다.

## Verification

기존 synchronization `--check`가 registry drift gate다. 추가, 제거, 중복 저장소와
소스/분류 drift를 거부한다. write 모드는 derived 항목을 원자적으로 재조정한다. Compose,
수정된 빌드 소스, 문서 계약, 공식 Renovate 설정은 독립적으로 검증한다. registry 출력을
런타임 health나 backup/restore의 증거로 받아들이지 않는다.

## Review Cadence

매월, 그리고 manager 범위, 소스 parser, 이미지 예외, major 업데이트가 변경될 때
검토한다.

## Traceability

- [Home/Dev architecture](../../02.architecture/descriptions/0031-home-development-host.md) (`AD-0031`)
- [Guide](../guides/0086-dependency-version-management.md), [Policy](0086-dependency-version-management.md), [Runbook](../runbooks/0086-dependency-version-management.md)

## Related Documents

- [Operations index](../README.md)
- [Runtime version projection](../../../infra/tech-stack.versions.json)
- [Repository Renovate policy](../../../renovate.json5)
- [Dependabot scope](../../../.github/dependabot.yml)
