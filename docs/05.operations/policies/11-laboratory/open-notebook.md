---
status: active
---
<!-- Target: docs/05.operations/policies/11-laboratory/open-notebook.md -->

# Open Notebook Operations Policy

## Overview

이 문서는 `open-notebook` 서비스의 운영 정책을 정의한다. Open Notebook은 노트북형 지식 작업과 로컬 실험을 지원하지만 인증, secret, 데이터 볼륨, Traefik 노출 경계를 지켜야 하는 관리 계층 서비스다.

## Policy Scope

이 정책은 `open_notebook` 애플리케이션, `surrealdb` 의존 서비스, 관련 Docker Secrets, Traefik 라우팅, 관리 데이터 볼륨을 관리한다.

- **Systems**: Open Notebook, SurrealDB, Traefik
- **Agents**: Infra/DevOps agents, Operations agents, AI Agents
- **Environments**: Local, Dev, Production-like management plane

## Controls

- **Required**:
  - `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password`는 Docker Secrets로만 주입해야 한다.
  - UI 접근은 `open-notebook.${DEFAULT_URL}` Traefik route와 `gateway-standard-chain@file,open-notebook-admin-ip@docker,large-body@file,sso-errors@file,sso-auth@file` chain 뒤에 둔다.
  - `OPEN_NOTEBOOK_ENCRYPTION_KEY`는 컨테이너 시작 시 `/run/secrets/open_notebook_encryption_key`에서만 export한다.
  - Open Notebook 데이터와 SurrealDB 데이터는 `DEFAULT_MANAGEMENT_DIR` 하위 bind-backed named volume에 저장한다.
- **Allowed**:
  - `admin` 또는 `dev` profile에서 로컬 실험/관리 목적으로 실행한다.
  - SurrealDB healthcheck 결과를 서비스 준비 상태 판단에 사용한다.
- **Disallowed**:
  - password, encryption key, SurrealDB credential을 문서, 로그, PR 설명, commit message에 노출하지 않는다.
  - Traefik 인증/allowlist 경계 없이 공개 인터넷에 직접 노출하지 않는다.
  - 운영 데이터 볼륨을 승인 없이 삭제하거나 volume-removal 옵션으로 제거하지 않는다.

## Exceptions

- SSO/gateway 장애로 긴급 접근이 필요한 경우, 사용자가 승인한 로컬 포트 접근만 일시 허용하고 작업 후 즉시 차단한다.
- 이미지 pull이 제한된 오프라인 환경에서는 기존 로컬 이미지를 사용하되, drift와 보안 검토 결과를 작업 기록에 남긴다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- `bash scripts/validation/check-template-security-baseline.sh`
- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Review Cadence

- 월 1회
- Open Notebook 이미지, secret, Traefik middleware, SurrealDB schema/storage 변경 시 즉시

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/11-laboratory/open-notebook.md)
- [Recovery runbook](../../runbooks/11-laboratory/open-notebook.md)
