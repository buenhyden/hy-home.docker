<!-- Target: docs/09.runbooks/08-ai/open-webui.md -->

# Open WebUI Maintenance & Recovery Runbook

: Open WebUI Service

---

## Overview (KR)

이 런북은 Open WebUI 장애 및 성능 저하 상황에서 즉시 실행 가능한 복구 절차를 제공한다. SQLite 데이터 복구, RAG 인덱스 재동기화, Ollama/Qdrant 연결 복구를 표준화한다.

## Purpose

- Open WebUI 가용성을 신속히 복구한다.
- RAG 기능(인덱싱/검색) 정상 상태를 재확인한다.
- 동일 장애 재발 시 일관된 증적을 남긴다.

## Canonical References

- `[../../02.ard/0013-open-webui-architecture.md]`
- `[../../03.adr/0016-open-webui-implementation.md]`
- `[../../04.specs/08-ai/open-webui.md]`
- `[../../05.plans/2026-03-27-08-ai-open-webui-plan.md]`

## When to Use

- `https://chat.${DEFAULT_URL}` 접속 실패 또는 5xx 증가.
- 모델 목록 미표시, 채팅 응답 실패.
- 문서 업로드 후 RAG 인덱싱 실패.
- Open WebUI healthcheck 실패.

## Procedure or Checklist

### Checklist

- [ ] `open-webui` 컨테이너 상태/로그 확인
- [ ] `ollama`, `qdrant` 상태 및 health 확인
- [ ] 인증(SSO) 경로 정상 여부 확인
- [ ] 데이터 디렉터리 백업 가능 여부 확인

### Procedure

#### 1. Initial Triage

```bash
docker ps --filter name=open-webui
docker logs --tail 200 open-webui
curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
```

#### 2. Dependency Connectivity Check

```bash
# Open WebUI -> Ollama
docker exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

# Open WebUI -> Qdrant
docker exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
```

#### 3. SQLite Backup and Recovery

```bash
# 1) 데이터 백업
cp -a ${DEFAULT_AI_MODEL_DIR}/open-webui ${DEFAULT_AI_MODEL_DIR}/open-webui.bak.$(date +%Y%m%d%H%M%S)

# 2) 서비스 재기동
docker restart open-webui
```

- DB 손상 의심 시, 최신 백업본으로 `webui.db` 복구 후 재기동한다.

#### 4. RAG Index Re-sync

1. Open WebUI 문서 관리에서 실패한 인덱스를 식별한다.
2. 문제 문서를 삭제 후 재업로드하여 재인덱싱한다.
3. 필요 시 Qdrant 해당 컬렉션 상태를 점검하고 재동기화한다.

#### 5. Service Restart Path

```bash
docker restart ollama
docker restart open-webui
```

- 의존 서비스 정상화 후 Open WebUI를 마지막에 재시작한다.

## Verification Steps

- [ ] `curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health` 성공
- [ ] UI 로그인 및 모델 목록 조회 성공
- [ ] 테스트 채팅 응답 성공
- [ ] 테스트 문서 업로드 후 RAG 질의 성공

## Observability and Evidence Sources

- **Signals**:
  - Open WebUI healthcheck 실패율
  - 5xx 응답률 상승
  - 인덱싱 실패율 증가
- **Evidence to Capture**:
  - `open-webui`/`ollama`/`qdrant` 로그 스니펫
  - 수행 명령 및 결과
  - 복구 전후 확인 화면/지표

## Safe Rollback or Recovery Procedure

- [ ] Open WebUI 변경 직후 이상 발생 시 이전 설정으로 되돌린다.
- [ ] 데이터 손상 시 최신 백업 디렉터리에서 DB 복구한다.
- [ ] 재기동 후 최소 기능(로그인/채팅/인덱싱) 확인까지 완료한다.

## Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 프롬프트/설정 변경을 직전 안정 버전으로 복원
- **Model Fallback**: 고부하 모델에서 안정 모델로 임시 전환
- **Tool Disable / Revoke**: 문서 업로드/자동 인덱싱 기능 임시 비활성
- **Eval Re-run**: 기본 채팅 + RAG smoke test 재실행
- **Trace Capture**: 장애 시간대 로그/지표를 증적으로 보존

## Related Operational Documents

- **Operations Policy**: `[../../08.operations/08-ai/open-webui.md]`
- **Guide**: `[../../07.guides/08-ai/open-webui.md]`
- **Incident examples**: `[../../10.incidents/README.md]`
- **Postmortem examples**: `[../../11.postmortems/README.md]`
