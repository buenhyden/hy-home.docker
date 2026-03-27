<!-- Target: docs/09.runbooks/08-ai/open-webui.md -->

# Open WebUI Maintenance & Recovery Runbook

: Open WebUI Service

---

## Overview (KR)

이 런북은 Open WebUI 서비스 장애 또는 성능 저하 시의 대응 절차를 정의한다. 데이터베이스 손상 복구, RAG 인덱스 초기화, 그리고 백엔드(Ollama/Qdrant) 연결 이슈를 즉시 해결하기 위한 단계별 가이드를 제공한다.

## Purpose

UI 접속 불가, 문서 검색(RAG) 응답 없음, 또는 컨테이너 충돌 시 서비스 연속성을 확보하는 것을 목표로 한다.

## Canonical References

- **PRD**: `[../../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD**: `[../../02.ard/0013-open-webui-architecture.md]`
- **ADR**: `[../../03.adr/0016-open-webui-implementation.md]`
- **Spec**: `[../../04.specs/08-ai/open-webui.md]`
- **Guide**: `[../../07.guides/08-ai/open-webui.md]`
- **Operations Policy**: `[../../08.operations/08-ai/open-webui.md]`

## When to Use

- UI 로딩 실패 (`502 Bad Gateway` 또는 무한 로딩).
- 문서 업로드 후 인덱싱이 완료되지 않음.
- 모델 리스트가 표시되지 않음 (Ollama 연결 실패).

## Procedure or Checklist

### Checklist

- [ ] `open-webui` 컨테이너 로그 확인 (`docker logs open-webui`)
- [ ] `ollama` 및 `qdrant` 서비스 상태 확인
- [ ] 브라우저 캐시 및 SSO 세션 증명 확인

### Procedure

#### 1. Database Corruption Recovery (SQLite)

1. 컨테이너 중지: `docker compose down open-webui`
2. 데이터 디렉토리 백업: `cp -r ${DEFAULT_AI_MODEL_DIR}/open-webui ${DEFAULT_AI_MODEL_DIR}/open-webui.bak`
3. SQLite 데이터베이스 복구 (필요시 전용 도구 사용) 또는 이전 백업본에서 `webui.db` 교체.
4. 컨테이너 재시작: `docker compose up -d open-webui`

#### 2. Reset RAG Index

1. UI 내에서 'Document' 섹션의 모든 인덱스 삭제 시도.
2. 강제 초기화 필요 시: Qdrant의 해당 컬렉션을 삭제하고 Open WebUI 내부에서 인덱스 재스캔 수행.

#### 3. Fix Connection to Ollama/Qdrant

1. `docker-compose.yml` 내 `OLLAMA_BASE_URL` 및 `VECTOR_DB_URL` 환경 변수 값 확인.
2. `infra_net` 내에서 각 서비스로의 `curl` 명령어를 통한 네트워크 도달성 확인.

## Verification Steps

- [ ] `https://chat.${DEFAULT_URL}` 접속 후 로그인 성공 여부 확인.
- [ ] `/api/v1/models` 엔드포인트 응답 확인.
- [ ] 테스트 문서 업로드 및 RAG 응답 수신 확인.

## Observability and Evidence Sources

- **Signals**: 컨테이너 CPU/Memory 급증, `5xx` 에러 빈도 증가.
- **Evidence to Capture**: `open-webui` 에러 로그 스니펫, Qdrant 원격 측정 데이터.

## Safe Rollback or Recovery Procedure

- [ ] 비정상 상태 지속 시 `open-webui.bak` 디렉토리를 원위치시킨 후 재시작.
- [ ] Ollama 임베딩 모델을 이전 버전으로 롤백하여 호환성 확인.

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: Ollama에서 기본 모델(`qwen3`) 외 스페어 모델로 전환.
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: RAG 성능 저하 시 테스트 데이터셋 재평가.
- **Trace Capture**: Open WebUI 디버그 로그 활성화 및 수집.

## Related Operational Documents

- **Incident examples**: `[../10.incidents/]`
