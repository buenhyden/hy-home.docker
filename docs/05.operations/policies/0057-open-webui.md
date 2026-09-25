---
title: "Open WebUI Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0057"
parent_ids:
- "AD-0008"
created: "2026-05-17"
---

# Open WebUI Operations Policy

## Overview

이 문서는 Open WebUI 운영 정책을 정의한다. 인증/접근 통제, 문서 업로드 및 RAG 처리 기준, 구성 변경 승인 절차를 명확히 하여 서비스 안정성과 보안을 유지한다.

## Policy Scope

Open WebUI 서비스 운영 전반:

- 사용자 접근 및 세션 관리
- 문서 업로드/인덱싱/삭제 기준
- Open WebUI와 Ollama 연동 구성 변경 관리

- **Systems**: `open-webui`, `ollama`, `qdrant`, `traefik`, `oauth2-proxy`, `keycloak`
- **Agents**: Open WebUI 운영 자동화 에이전트, 문서 인덱싱/정리 에이전트
- **Environments**: Local, Dev, Homelab, Production-like rehearsal

## Controls

- **Required**:
- 현재 구현은 `home-openwebui` Keycloak client의 native OIDC를 사용한다. Traefik router는 TLS와 `gateway-standard-chain@file`만 적용하며 `sso-auth@file`은 적용하지 않는다. 로컬 비밀번호 로그인, signup, email account merge, OAuth role/group management와 group creation은 Compose에서 비활성화한다.
  - `OLLAMA_BASE_URL`, `RAG_EMBEDDING_MODEL` 변경과 `VECTOR_DB` 도입(외부 벡터 DB 선택, 재색인 필요)은 사전 영향도 검토를 수행해야 한다.
  - 인덱싱 실패/지연, 연결 실패 로그를 운영 증적으로 보관해야 한다.
  - `ai` profile 선택으로 AI 서비스를 기동하는 것은 runtime 승인 후 수행해야 한다.
- **Allowed**:
  - 문서 수명주기 관리(업로드, 재인덱싱, 삭제).
  - 성능 개선 목적의 모델 파라미터 조정(승인된 범위 내).
- **Disallowed**:
  - 승인 없는 SSO 우회/비활성화.
  - 검증 없이 프로덕션 임베딩 모델 변경.
  - 출처 불명 모델/문서 처리 파이프라인 적용.

### Lifecycle and data controls

- Open WebUI remains `HOME`; native Keycloak OIDC and `gateway-standard-chain@file` are required. Do not add `sso-auth@file` or enable password/signup/email-merge/role-management fallbacks without a reviewed auth design.
- SQLite/application data, uploads, RAG vectors (the local store in the same volume) and the exact auth/OIDC secret set form one recovery boundary. Selecting an external vector store with `VECTOR_DB` would split that boundary and needs a re-index.
- Stop writes before copying SQLite or the data volume. Restore to isolated storage/project first and verify identities, chats, uploads, OIDC, model access, and controlled RAG retrieval before any production replacement.
- Upgrade only with a prior recoverable copy, migration review, pinned image identity, and rollback evidence. Source resource limits do not prove spare capacity.
- Removal requires exported user/content evidence, revoked OIDC client/secrets, disabled routes, and explicit approval before persistent deletion.

## Exceptions

- 로컬 단독 개발 환경에서 SSO 우회를 검토해야 하면 외부 네트워크 비노출, 명시 승인, 작업 종료 즉시 복구가 필수다.

## Verification

- 배포 전 체크:
  - `bash scripts/hardening/check-all-hardening.sh 08-ai`
  - `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
  - runtime 승인 후 `ai` profile 선택 상태에서 `open-webui` container-internal health endpoint 응답 확인
  - Open WebUI -> Ollama container-internal 연결성 확인
- 운영 중 체크:
  - 인증 실패율, 5xx 비율, 인덱싱 실패율 모니터링
- 증적:
  - 변경 티켓(또는 PR), 검증 로그, 롤백 결과

## Review Cadence

- **Quarterly**: 정책/권한/데이터 취급 기준 검토
- **Per Release**: 모델/임베딩/연동 구성 변경 시 사전 검토

## Traceability

- Declared parent: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0057-open-webui.md) (`GDE-0057`), [Runbook](../runbooks/0057-open-webui.md) (`RUN-0057`)

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Usage guide](../guides/0057-open-webui.md)
- [Recovery runbook](../runbooks/0057-open-webui.md)
