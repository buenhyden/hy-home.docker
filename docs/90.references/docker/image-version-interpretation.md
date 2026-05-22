---
status: active
---
<!-- Target: docs/90.references/docker/image-version-interpretation.md -->

# Reference: Docker Image and Version Interpretation

## Overview (KR)

이 문서는 `hy-home.docker`에서 Docker image와 version 정보를 어떻게 해석해야 하는지 정리한 reference다. 최신 image 값이나 rollout 절차를 복제하지 않고, Compose 선언과 registry 파일을 읽는 기준만 설명한다.

## Purpose

Docker image/version 관련 문서와 검증 결과를 읽을 때 어떤 파일을 source로 삼아야 하는지 명확히 한다.

## Repository Role

이 reference는 Docker image drift, floating tag 예외, tech-stack registry를 해석하는 stable context로 사용한다. 최신 runtime truth는 `infra/**/docker-compose*.yml`, `infra/tech-stack.versions.json`, `infra/image-tag-policy.exceptions.json`, 그리고 validation scripts가 담당한다.

## Scope

### In Scope

- Compose image declaration 해석 기준
- tech-stack registry와 Compose source의 역할 구분
- floating tag exception의 reference 경계
- Docker image/version 문서 작성 시 source 우선순위

### Out of Scope

- 현재 image tag inventory 복사본
- image upgrade rollout plan
- deployment procedure 또는 rollback runbook
- secret 값, credential, token
- 최신 외부 registry release 상태의 무검증 복사본

## Definitions / Facts

- **Compose image declaration**: Docker Compose 파일에 선언된 service image 값이다. 현재 실행 구성의 1차 source다.
- **Tech-stack registry**: `infra/tech-stack.versions.json`에 있는 검증 대상 image registry다. 주요 image가 Compose에 남아 있는지 확인하는 기준으로 사용한다.
- **Floating tag exception**: `latest`, branch tag, mutable tag처럼 고정되지 않은 tag가 의도적으로 허용된 경우다. 허용 근거는 `infra/image-tag-policy.exceptions.json`에 둔다.
- **Version drift**: registry나 policy가 기대하는 image 선언과 Compose source가 달라진 상태다. drift 판단은 validator 결과와 tracked source 파일을 함께 확인한다.

## Source Rules

- Docker image의 현재 선언은 Compose 파일에서 확인한다.
- 중요한 image의 검증 등록 여부는 `infra/tech-stack.versions.json`에서 확인한다.
- floating tag 허용 여부는 `infra/image-tag-policy.exceptions.json`에서 확인한다.
- validator 결과는 해석을 돕는 evidence이며, 원문 source 파일을 대체하지 않는다.
- 외부 registry, release note, vendor page의 최신 상태가 필요한 경우에는 현재 시점에 다시 확인한다.

## Sources

- [Docker reference category](./README.md) - Docker reference category role and working rules
- [tech stack versions](../../../infra/tech-stack.versions.json) - tracked registry for important Docker images
- [image tag exceptions](../../../infra/image-tag-policy.exceptions.json) - tracked floating tag exception registry
- [repo contract checker](../../../scripts/validation/check-repo-contracts.sh) - repository contract validation for Docker image/tag policy and version drift

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Docker image policy, registry validation, or Compose source ownership changes
- **Update Trigger**: Update when Docker image interpretation rules change, not when an individual image tag changes

## Related Documents

- [Docker references](./README.md)
- [90.references](../README.md)
- [docs index](../../README.md)
- [reference template](../../99.templates/reference.template.md)
