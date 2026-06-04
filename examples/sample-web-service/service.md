# sample-web-service Service Scaffold

> Example instance of `docs/99.templates/service.template.md`. When authoring a
> real service, copy the template to `docs/03.specs/<feature-id>/service.md`.

## Overview (KR)

이 문서는 `sample-web-service`의 컨테이너 런타임 계약 예시다. 이미지/빌드, 보안
하드닝, 네트워크, 볼륨, secret 참조, healthcheck, 검증 절차를 보여준다.

## Scope & Non-goals

- **Covers**: a single static web container and its hardened runtime contract.
- **Does Not Cover**: TLS termination, ingress routing, and persistence (handled
  by gateway and data stacks under `infra/`).

## Image & Build

- **Base image (pinned)**: `nginxinc/nginx-unprivileged:1.27.3-alpine`, build stage `alpine:3.21` — no floating tags.
- **Build strategy**: multi-stage; the runtime stage carries static assets and config only.
- **Build args**: none; no secrets in build args or layers.

## Security & Hardening

- **User**: non-root (uid 101 via the unprivileged image).
- **Filesystem**: `read_only: true` with `tmpfs` for `/tmp`, `/var/cache/nginx`, `/var/run`.
- **Capabilities**: `cap_drop: [ALL]`.
- **Privilege**: `no-new-privileges:true`; no `privileged`.
- **Resource limits**: `cpus: "0.50"`, `memory: 128M`.

## Networking & Volumes

- **Networks**: `sample-internal` (bridge); only the web port is published.
- **Ports**: `${WEB_HOST_PORT:-8080}:8080`.
- **Volumes**: none (stateless); state-bearing services use named volumes.

## Secrets

- **Mechanism**: `env_file` (`.env`); no plaintext secrets in compose.
- **Referenced keys**: `WEB_HOST_PORT` (non-secret port selector).

## Healthcheck & Operations

- **Healthcheck**: `wget --spider http://127.0.0.1:8080/`, interval 30s, timeout 3s, retries 3, start period 5s.
- **Restart policy**: `unless-stopped`.
- **Logging**: `json-file`, `max-size: 10m`, `max-file: 3`.

## Validation

- `docker compose config` — parses without error.
- `docker compose ps` — reports `healthy` after the start period.

## Related Documents

- [Service README](./README.md)
- [Service scaffold template](../../docs/99.templates/service.template.md)
- [New-service onboarding guide](../../docs/05.operations/guides/00-workspace/new-service-onboarding.md)
