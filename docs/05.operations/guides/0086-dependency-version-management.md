---
title: "Dependency Version Management Guide"
version: "0.1.1"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0086"
parent_ids:
- "POL-0086"
created: "2026-09-19"
---

# Dependency Version Management Guide

## Usage

운영자는 버전 변경 전에 해당 선언의 소유자를 찾는다. Compose `image`와
Dockerfile `FROM`/`ARG`가 실행 원본이며 `infra/tech-stack.versions.json`은
Git으로 추적하는 `infra/**/{compose,docker-compose}*.{yml,yaml}` 서비스 이미지 전체의
파생 drift 투영이다. 로컬/커스텀 저장소도 명시적으로 분류하지만 빌드 전용
서비스, Dockerfile의 상속 단계와 전체 의존성을 레지스트리가 완전히
나열한다고 해석하지 않는다.
전체 서비스 분류는 기존 Stage 90 연구의 날짜가 있는 inventory를 따른다.

문서는 patch pin을 복제하지 않고 구현 원본으로 연결한다. 의미 있는
호환성·보안 공지·workaround·migration·history 설명에만 같은 줄의
`runtime-version-exception: <category> — <reason>` 주석을 사용한다.
문서 frontmatter version과 API/프로토콜 버전은 실행 이미지 pin이 아니다.

## Common Checks

변경 파일이 어떤 updater의 manager에 속하는지, 빌드 이미지와 로컬 이미지
태그가 일치하는지, registry check 및 공식 Renovate strict validator가 통과하는지
확인한다. 알려진 게시 시각은 7일 안정화 기간을 거치고, 게시 시각이 없는
release는 무기한 대기하지 않도록 schedule과 수동 검토를 적용한다. Green
registry check만으로 Dockerfile pin 검증을 대체하지 않는다.

## Runbook Handoff

[Runbook](../runbooks/0086-dependency-version-management.md)이 검증 순서와 rollback을 소유하며 [Policy](../policies/0086-dependency-version-management.md)가
update ownership와 예외를 소유한다.

## Traceability

- [Home/Dev architecture](../../02.architecture/descriptions/0031-home-development-host.md) (`AD-0031`)
- [Guide](0086-dependency-version-management.md), [Policy](../policies/0086-dependency-version-management.md), [Runbook](../runbooks/0086-dependency-version-management.md)

## Related Documents

- [Operations index](../README.md)
- [Runtime version projection](../../../infra/tech-stack.versions.json)
- [Repository Renovate policy](../../../renovate.json5)
- [Dependabot scope](../../../.github/dependabot.yml)
