---
status: active
---

<!-- Target: docs/05.operations/guides/new-service-onboarding.md -->

# New Service Onboarding Guide

> 새 컨테이너 서비스를 워크스페이스 표준에 맞게 추가하는 방법을 설명한다.

## Usage

### Overview (KR)

이 가이드는 새 컨테이너 서비스를 `hy-home.docker`에 추가할 때 참조한다.
복사 가능한 시드(`examples/sample-web-service/`)와 service scaffold 템플릿
(`docs/99.templates/service.template.md`)을 사용해, 보안 하드닝·이미지 핀·
healthcheck 표준을 처음부터 갖춘 서비스를 만든다.

### Usage Type

`onboarding`

### Target Audience

- Operator
- Developer
- Contributor
- AI Agent

### Purpose

독자가 표준 하드닝과 Compose 규약을 누락 없이 적용한 새 서비스를 정의하고,
런타임 계약을 `service.md`로 문서화할 수 있게 한다.

### Prerequisites

- Docker Engine과 Docker Compose v2 사용 가능 환경.
- `infra/image-tag-policy.exceptions.json`과 `infra/tech-stack.versions.json`의 이미지 핀 정책 숙지.

### Step-by-step Instructions

1. `examples/sample-web-service/`를 새 서비스 디렉터리로 복사한다.
2. 이름, base image(핀된 태그/digest), 포트, 네트워크, 볼륨을 서비스에 맞게 수정한다.
3. 하드닝 기본값을 유지한다: non-root 실행, `read_only: true` + `tmpfs`, `cap_drop: [ALL]`, `no-new-privileges:true`, 리소스 제한, healthcheck, 로그 회전.
4. secret은 `env_file`/Docker secrets/Vault 참조로만 주입한다. `docker-compose.yml`에 plaintext secret을 두지 않는다.
5. 런타임 계약을 `docs/99.templates/service.template.md`를 복사해 해당 feature의 `docs/03.specs/` 스펙 디렉터리 아래 `service.md`로 문서화한다.
6. service README에 Service Readiness evidence를 기록한다.

### Common Pitfalls

- Floating tag(`latest`, `stable`) 사용 — 반드시 태그나 digest를 핀한다.
- root 사용자 실행 또는 불필요한 capability 유지 — 최소 권한 원칙을 지킨다.
- `docker-compose.yml`에 secret 값을 직접 작성 — 참조 메커니즘만 사용한다.

## Common Checks

- `docker compose config` — compose 정의가 오류 없이 파싱된다.
- `docker compose ps` — start period 이후 `healthy` 상태가 보고된다.
- `bash scripts/validation/check-repo-contracts.sh` — 서비스를 `infra/`에 편입할 때 contract가 동기화 상태를 유지한다.

## Runbook Handoff

반복 실행 배포·롤백·장애 대응 절차는 해당 서비스 도메인의
[recovery runbook](../runbooks/release-management.md)을 따른다.

## Related Documents

- [Operations index](../README.md)
- [Service scaffold template](../../99.templates/service.template.md)
- [Reference service seed](../../../examples/sample-web-service/README.md)
