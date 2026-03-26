<!-- Target: docs/08.operations/08-ai/open-webui.md -->

# Open WebUI Operations Policy

> System-wide governance for chat interface and RAG document management.

---

## Overview (KR)

이 문서는 Open WebUI 운영 정책을 정의한다. 사용자 접근 제어, 데이터(대화 기록 및 문서) 보존 기준, 그리고 AI 모델 사용 가이드라인을 규정하여 시스템의 안정성과 보안을 유지한다.

## Policy Scope

Open WebUI 인스턴스 내에서의 사용자 활동, 업로드된 문서의 생명주기, 그리고 로컬 LLM 자원 할당 정책을 관리한다.

## Applies To

- **Systems**: Open WebUI, Ollama (Embedding), Qdrant (Vector DB).
- **Agents**: AI Chat Agents, Data Processing Agents.
- **Environments**: Production Tooling Tier.

## Controls

- **Required**:
  - 모든 사용자는 SSO(Keycloak)를 통해 인증되어야 한다.
  - 업로드되는 모든 문서는 고유 ID로 식별되어야 한다.
- **Allowed**:
  - 개인별 대화 기록 저장 및 삭제.
  - 공용 문서 저장소(Knowledge Base) 생성.
- **Disallowed**:
  - 관리자 승인 없는 익명 접근 및 API 호출.
  - 100MB를 초과하는 단일 문서 업로드 (RAG 성능 저하 방지).

## Exceptions

- 로컬 디버깅 및 개발용 인스턴스는 한시적으로 SSO 없이 운영될 수 있으나, 외부 노출은 금지된다.

## Verification

- **Compliance Check**: 분기별 사용자 리스트 및 문서 사용량 감사.
- **Monitoring**: Grafana 대시보드를 통한 컨테이너 리소스 및 API 응답 시간 모니터링.

## Review Cadence

- **Quarterly**: 매 분기별 운영 효율성 및 보안 준수 여부 검토.

## AI Agent Policy Section

- **Model / Prompt Change Process**: 기본 임베딩 모델 변경 시 기술 사양서(Spec) 업데이트 및 영향도 평가 수행 필수.
- **Log / Trace Retention**: 보안 정책에 따라 최대 90일간 대화 메타데이터를 보관한다.

## Related Documents

- **ARD**: `[../../02.ard/08-ai-infrastructure.md]`
- **Guide**: `[../../07.guides/08-ai/open-webui.md]`
- **Runbook**: `[../../09.runbooks/08-ai/open-webui.md]`
