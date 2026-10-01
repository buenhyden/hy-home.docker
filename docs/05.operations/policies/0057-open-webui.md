---
title: "Open WebUI Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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

- **Systems**: `open-webui`, `ollama`, 로컬 SQLite·Chroma·업로드 저장소, `traefik`, `keycloak`. 현재 native OIDC 경로는 Qdrant나 OAuth2 Proxy에 의존하지 않는다.
- **Environments**: 로컬·개발·홈랩과 운영 환경에 준하는 rehearsal

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

- WebUI를 HOME으로 유지하고 native Keycloak OIDC와 표준 gateway를 요구한다. 검토된 인증 설계 없이 proxy SSO나 password/signup/email-merge/role-management 대안을 켜지 않는다.
- SQLite/application, upload, 로컬 RAG vector와 정확한 auth/OIDC secret 집합을 한 복구 경계로 취급한다. `VECTOR_DB`로 외부 저장소를 선택하면 경계가 분리되고 재인덱싱이 필요하다.
- SQLite/data copy 전에 쓰기를 멈추고 격리 복원에서 identity/chat/upload/OIDC/model access와 시험 RAG를 검증한 뒤 production 교체를 승인한다.
- Upgrade에는 복구 가능한 copy, migration 검토, image identity와 rollback 근거가 필요하다. 선언 한도는 여유 증거가 아니다.
- 제거에는 사용자·내용 export, OIDC client/secret 폐기, route 중지와 영속 데이터 삭제 승인이 필요하다.

### Local data and authentication boundary

선언 릴리스는 `DATA_DIR/vector_db`의 Chroma를 기본으로 쓰며 Compose에는 외부 vector-store나 Qdrant 연결이 없다. SQLite·vector·upload·identity와 embedding-model 출처를 함께 보존한다. CUDA image 이름만으로 GPU가 할당되지는 않으며 WebUI에는 GPU 예약이 없다. 로컬 entrypoint는 한 줄 OIDC secret과 검증된 CA bundle을 읽고 인자가 없으면 upstream `bash start.sh`로 시작한다.

`ENABLE_PASSWORD_AUTH=false`는 폼 숨김과 별도로 password 인증을 막는다. `ENABLE_OAUTH_PERSISTENT_CONFIG=false`는 OAuth 설정만 관장하며 모든 저장 설정을 끄지 않는다. 선언 버전의 `key/value`별 schema에 과거 단일 `id/data` 행 SQL 복구를 적용하지 않는다. Native login, signup/password 거부와 identity 연속성은 승인된 별도 검사로 확인하며 health가 대신하지 않는다.

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

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Review Cadence

- **Quarterly**: 정책/권한/데이터 취급 기준 검토
- **Per Release**: 모델/임베딩/연동 구성 변경 시 사전 검토

## Traceability

- Declared parent: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0057-open-webui.md) (`GDE-0057`), [Runbook](../runbooks/0057-open-webui.md) (`RUN-0057`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0057-open-webui.md)
- [Recovery runbook](../runbooks/0057-open-webui.md)
