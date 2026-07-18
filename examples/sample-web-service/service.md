---
status: active
artifact_id: spec:sample-web-service
artifact_type: spec
parent_ids:
  - spec:133-target-surface-contract-convergence
---

# sample-web-service Service Contract

## Overview

이 문서는 `sample-web-service` 정적 웹 컨테이너의 예제 서비스 계약이다. 빌드
산출물, 런타임 보안, 네트워크, 저장소, secret 경계, 상태 확인과 정적 검증 범위를
현재 예제 파일에 맞춰 설명한다.

## Parent and Scope

이 예제는 [Spec 133](../../docs/03.specs/133-target-surface-contract-convergence/spec.md)의
typed-example 범위와 [로컬 README](./README.md)의 copyable scaffold 역할을 따른다.

- 단일 정적 웹 컨테이너와 hardened runtime 계약을 다룬다.
- TLS termination, ingress routing, 영속 저장소, production SLA와 incident
  response는 다루지 않는다.

## Image and Build

- 빌드 단계는 `alpine:3.21`, 런타임 단계는
  `nginxinc/nginx-unprivileged:1.27.3-alpine`으로 고정한다.
- multi-stage build를 사용하며 런타임 이미지에는 정적 자산과 Nginx 설정만
  포함한다.
- build argument를 사용하지 않으며 build layer에 secret을 전달하지 않는다.

## Security

- unprivileged 이미지의 uid 101로 실행한다.
- root filesystem은 read-only이며 `/tmp`, `/var/cache/nginx`, `/var/run`만
  `tmpfs`로 제공한다.
- 모든 Linux capability를 제거하고 `no-new-privileges:true`를 적용한다.
- CPU는 `0.50`, memory는 `128M`으로 제한한다.

## Networking and Storage

- `sample-internal` bridge network에 연결하고 web port만 host에 공개한다.
- port mapping은 `${WEB_HOST_PORT:-8080}:8080`이다.
- stateless service이므로 volume을 사용하지 않는다.

## Secrets

- Compose는 `.env`를 `env_file`로 참조하지만 plaintext secret을 선언하지 않는다.
- `WEB_HOST_PORT`는 비밀값이 아닌 host port 선택자다.

## Health and Operations

- healthcheck는 container 내부에서 `http://127.0.0.1:8080/`에 `wget --spider`를
  실행하며 interval 30초, timeout 3초, retry 3회, start period 5초를 사용한다.
- restart policy는 `unless-stopped`다.
- `json-file` logging driver의 `max-size: 10m`, `max-file: 3` 제한을 적용한다.

## Validation

- repository root에서 `docker compose -f examples/sample-web-service/docker-compose.yml config`
  명령으로 정적 구성을 검증한다.
- live `healthy` 상태 확인은 서비스를 시작하는 별도 runtime acceptance 범위다.

## Related Documents

- [Service README](./README.md)
- [Service scaffold template](../../docs/99.templates/templates/spec-contracts/service.template.md)
- [New-service onboarding guide](../../docs/05.operations/guides/00-workspace/new-service-onboarding.md)
