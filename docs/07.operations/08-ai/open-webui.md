<!-- Target: docs/07.operations/08-ai/open-webui.md -->

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
  - 변경 시 관련 Usage/Procedure 동시 갱신
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
- **Usage**: `[../../07.operations/08-ai/open-webui.md]`
- **Procedure**: `[../../07.operations/08-ai/open-webui.md]`
- **Postmortem**: `[../../10.incidents/README.md]`

## Usage

> Migrated from `docs/07.operations/08-ai/open-webui.md` during the 2026-05-10 operations taxonomy consolidation.

### Open WebUI Interface & RAG Usage

> Open WebUI 기반 로컬 LLM 채팅 및 RAG 운영 가이드.

---

#### Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Open WebUI를 통해 Ollama 모델과 대화하고, 문서 기반 RAG를 사용하는 방법을 설명한다. 운영자가 재현 가능한 절차로 접근/인증, 모델 선택, 문서 인덱싱, 기본 점검을 수행할 수 있도록 정리한다.

#### Usage Type

`system-guide`

#### Target Audience

- AI Engineer
- Operator
- Internal User
- Agent-tuner

#### Purpose

- Open WebUI의 핵심 사용 흐름(접속, 인증, 모델 선택, 채팅)을 표준화한다.
- RAG 인덱싱 및 질의 흐름을 `OLLAMA_BASE_URL`, `VECTOR_DB_URL`, `RAG_EMBEDDING_MODEL` 기준으로 이해한다.
- 장애 징후를 빠르게 식별하고 런북으로 연결한다.

#### Prerequisites

- `open-webui` 컨테이너가 기동 가능해야 한다.
- `ollama` 컨테이너가 `http://ollama:${OLLAMA_PORT:-11434}`로 접근 가능해야 한다.
- `qdrant` 컨테이너가 `http://qdrant:${QDRANT_PORT:-6333}`로 접근 가능해야 한다.
- Open WebUI 환경변수 확인:
  - `OLLAMA_BASE_URL`
  - `VECTOR_DB_URL`
  - `RAG_EMBEDDING_MODEL` (기본값: `qwen3-embedding:0.6b`)
- SSO 환경(예: Keycloak + `sso-auth@file`)이 정상이어야 한다.

#### Step-by-step Instructions

##### 1. Access & Authentication

1. 브라우저에서 `https://chat.${DEFAULT_URL}` 접속.
2. SSO 로그인 완료 후 Open WebUI 대시보드 진입 확인.
3. 로그인 루프 또는 401 발생 시 먼저 인증 계층 상태를 확인한다.

##### 2. Model Selection & Chat

1. 상단 모델 선택기에서 Ollama 모델을 선택한다.
2. 간단한 프롬프트(예: `hello`)로 응답 확인.
3. 모델 목록이 비어 있으면 Open WebUI에서 Ollama 연결 상태를 점검한다.

##### 3. RAG Document Indexing

1. 문서 업로드 메뉴에서 PDF/TXT 문서를 업로드한다.
2. Open WebUI가 `RAG_EMBEDDING_MODEL`로 임베딩 생성 후 Qdrant에 저장하는지 확인한다.
3. 업로드된 문서를 지정하여 질의하고, 답변에 문서 근거가 반영되는지 확인한다.

##### 4. Quick Connectivity Checks

```bash
### Open WebUI health
curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health

### Open WebUI -> Ollama connectivity (컨테이너 내부)
docker exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

### Open WebUI -> Qdrant connectivity (컨테이너 내부)
docker exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
```

##### 5. Advanced Settings

1. 모델별 시스템 프롬프트(System Prompt)를 워크로드에 맞게 분리한다.
2. Temperature, Top-K, Top-P를 모델 특성에 맞춰 조정한다.
3. 임베딩 모델 변경 시 기존 인덱스 재생성 계획을 먼저 수립한다.

#### Common Pitfalls

- **Ollama 연결 실패**: `OLLAMA_BASE_URL` 오타 또는 `ollama` 비정상 상태.
- **Qdrant 연결 실패**: `VECTOR_DB_URL` 오타, 네트워크 미연결, Qdrant 다운.
- **임베딩 모델 누락**: `RAG_EMBEDDING_MODEL`이 Ollama에 준비되지 않아 인덱싱 실패.
- **VRAM OOM**: 동시 인덱싱/추론 증가로 응답 지연 또는 실패.
- **SSO 문제**: 인증 미들웨어/리디렉션 설정 불일치로 접근 실패.

#### Related Documents

- **PRD (Open WebUI)**: `[../../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD (Open WebUI)**: `[../../02.ard/0013-open-webui-architecture.md]`
- **ADR (Open WebUI)**: `[../../03.adr/0016-open-webui-implementation.md]`
- **Spec (Open WebUI)**: `[../../04.specs/08-ai/open-webui.md]`
- **Plan (Open WebUI)**: `[../../05.plans/2026-03-27-08-ai-open-webui-plan.md]`
- **Task (Open WebUI)**: `[../../06.tasks/2026-03-27-08-ai-open-webui-tasks.md]`
- **Operation**: `[../../07.operations/08-ai/open-webui.md]`
- **Procedure**: `[../../07.operations/08-ai/open-webui.md]`

## Procedure

> Migrated from `docs/07.operations/08-ai/open-webui.md` during the 2026-05-10 operations taxonomy consolidation.

### Open WebUI Maintenance & Recovery Procedure

: Open WebUI Service

---

#### Overview (KR)

이 런북은 Open WebUI 장애 및 성능 저하 상황에서 즉시 실행 가능한 복구 절차를 제공한다. SQLite 데이터 복구, RAG 인덱스 재동기화, Ollama/Qdrant 연결 복구를 표준화한다.

#### Purpose

- Open WebUI 가용성을 신속히 복구한다.
- RAG 기능(인덱싱/검색) 정상 상태를 재확인한다.
- 동일 장애 재발 시 일관된 증적을 남긴다.

#### Canonical References

- `[../../02.ard/0013-open-webui-architecture.md]`
- `[../../03.adr/0016-open-webui-implementation.md]`
- `[../../04.specs/08-ai/open-webui.md]`
- `[../../05.plans/2026-03-27-08-ai-open-webui-plan.md]`

#### When to Use

- `https://chat.${DEFAULT_URL}` 접속 실패 또는 5xx 증가.
- 모델 목록 미표시, 채팅 응답 실패.
- 문서 업로드 후 RAG 인덱싱 실패.
- Open WebUI healthcheck 실패.

#### Procedure or Checklist

##### Checklist

- [ ] `open-webui` 컨테이너 상태/로그 확인
- [ ] `ollama`, `qdrant` 상태 및 health 확인
- [ ] 인증(SSO) 경로 정상 여부 확인
- [ ] 데이터 디렉터리 백업 가능 여부 확인

##### Procedure

###### 1. Initial Triage

```bash
docker ps --filter name=open-webui
docker logs --tail 200 open-webui
curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
```

###### 2. Dependency Connectivity Check

```bash
### Open WebUI -> Ollama
docker exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

### Open WebUI -> Qdrant
docker exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
```

###### 3. SQLite Backup and Recovery

```bash
### 1) 데이터 백업
cp -a ${DEFAULT_AI_MODEL_DIR}/open-webui ${DEFAULT_AI_MODEL_DIR}/open-webui.bak.$(date +%Y%m%d%H%M%S)

### 2) 서비스 재기동
docker restart open-webui
```

- DB 손상 의심 시, 최신 백업본으로 `webui.db` 복구 후 재기동한다.

###### 4. RAG Index Re-sync

1. Open WebUI 문서 관리에서 실패한 인덱스를 식별한다.
2. 문제 문서를 삭제 후 재업로드하여 재인덱싱한다.
3. 필요 시 Qdrant 해당 컬렉션 상태를 점검하고 재동기화한다.

###### 5. Service Restart Path

```bash
docker restart ollama
docker restart open-webui
```

- 의존 서비스 정상화 후 Open WebUI를 마지막에 재시작한다.

#### Verification Steps

- [ ] `curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health` 성공
- [ ] UI 로그인 및 모델 목록 조회 성공
- [ ] 테스트 채팅 응답 성공
- [ ] 테스트 문서 업로드 후 RAG 질의 성공

#### Observability and Evidence Sources

- **Signals**:
  - Open WebUI healthcheck 실패율
  - 5xx 응답률 상승
  - 인덱싱 실패율 증가
- **Evidence to Capture**:
  - `open-webui`/`ollama`/`qdrant` 로그 스니펫
  - 수행 명령 및 결과
  - 복구 전후 확인 화면/지표

#### Safe Rollback or Recovery Procedure

- [ ] Open WebUI 변경 직후 이상 발생 시 이전 설정으로 되돌린다.
- [ ] 데이터 손상 시 최신 백업 디렉터리에서 DB 복구한다.
- [ ] 재기동 후 최소 기능(로그인/채팅/인덱싱) 확인까지 완료한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 프롬프트/설정 변경을 직전 안정 버전으로 복원
- **Model Fallback**: 고부하 모델에서 안정 모델로 임시 전환
- **Tool Disable / Revoke**: 문서 업로드/자동 인덱싱 기능 임시 비활성
- **Eval Re-run**: 기본 채팅 + RAG smoke test 재실행
- **Trace Capture**: 장애 시간대 로그/지표를 증적으로 보존

#### Related Operational Documents

- **Operations Policy**: `[../../07.operations/08-ai/open-webui.md]`
- **Usage**: `[../../07.operations/08-ai/open-webui.md]`
- **Incident examples**: `[../../10.incidents/README.md]`
- **Postmortem examples**: `[../../10.incidents/README.md]`
