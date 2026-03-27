<!-- Target: docs/08.operations/08-ai/open-webui.md -->

# Open WebUI Operations Policy

> Open WebUI 접근 통제, RAG 데이터 취급, 운영 변경 게이트 정책.

---

## Overview (KR)

이 문서는 Open WebUI 운영 정책을 정의한다. 인증/접근 통제, 문서 업로드 및 RAG 처리 기준, 구성 변경 승인 절차를 명확히 하여 서비스 안정성과 보안을 유지한다.

## Policy Scope

Open WebUI 서비스 운영 전반:
- 사용자 접근 및 세션 관리
- 문서 업로드/인덱싱/삭제 기준
- Open WebUI와 Ollama/Qdrant 연동 구성 변경 관리

## Applies To

- **Systems**: `open-webui`, `ollama`, `qdrant`, `traefik`, `oauth2-proxy`, `keycloak`
- **Agents**: Open WebUI 운영 자동화 에이전트, 문서 인덱싱/정리 에이전트
- **Environments**: `prod`, `staging`, `lab` (`dev`는 예외 조항 적용)

## Controls

- **Required**:
  - 외부 노출 경로는 반드시 SSO 미들웨어(`sso-auth@file`)를 통과해야 한다.
  - `OLLAMA_BASE_URL`, `VECTOR_DB_URL`, `RAG_EMBEDDING_MODEL` 변경은 사전 영향도 검토를 수행해야 한다.
  - 인덱싱 실패/지연, 연결 실패 로그를 운영 증적으로 보관해야 한다.
- **Allowed**:
  - 문서 수명주기 관리(업로드, 재인덱싱, 삭제).
  - 성능 개선 목적의 모델 파라미터 조정(승인된 범위 내).
- **Disallowed**:
  - 승인 없는 SSO 우회/비활성화.
  - 검증 없이 프로덕션 임베딩 모델 변경.
  - 출처 불명 모델/문서 처리 파이프라인 적용.

## Exceptions

- 로컬 단독 개발 환경(`dev`)에서만 일시적 SSO 비활성 허용.
- 단, 외부 네트워크 노출은 금지하며, 작업 종료 즉시 기본 보안 구성을 복구해야 한다.

## Verification

- 배포 전 체크:
  - `open-webui` health endpoint 응답 확인
  - Open WebUI -> Ollama/Qdrant 연결성 확인
- 운영 중 체크:
  - 인증 실패율, 5xx 비율, 인덱싱 실패율 모니터링
- 증적:
  - 변경 티켓(또는 PR), 검증 로그, 롤백 결과

## Review Cadence

- **Quarterly**: 정책/권한/데이터 취급 기준 검토
- **Per Release**: 모델/임베딩/연동 구성 변경 시 사전 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
  - 변경 요청 등록 -> 영향도 분석 -> staging 검증 -> 운영 반영
  - 변경 시 관련 Guide/Runbook 동시 갱신
- **Eval / Guardrail Threshold**:
  - 배포 게이트: 연결성(OLLAMA/Qdrant), 인증(SSO), 핵심 질의 성공률 모두 통과 시에만 반영
- **Log / Trace Retention**:
  - 운영 로그/추적 증적은 최소 90일 보관
- **Safety Incident Thresholds**:
  - SSO 우회, 민감 데이터 외부 유출 정황, 무단 설정 변경은 즉시 `Sev1`로 분류

## Related Documents

- **PRD**: `[../../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD**: `[../../02.ard/0013-open-webui-architecture.md]`
- **ADR**: `[../../03.adr/0016-open-webui-implementation.md]`
- **Spec**: `[../../04.specs/08-ai/open-webui.md]`
- **Guide**: `[../../07.guides/08-ai/open-webui.md]`
- **Runbook**: `[../../09.runbooks/08-ai/open-webui.md]`
- **Postmortem**: `[../../11.postmortems/README.md]`
