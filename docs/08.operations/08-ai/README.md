# AI Tier Operations (08-ai)

> `08-ai` 계층 운영 정책과 통제 기준 문서 모음.

## Overview

이 디렉터리는 AI 계층의 정책 문서를 관리한다. 모델/자원/보안/변경 통제를 정의하며, 실행 절차 자체는 런북으로 분리한다.

## Audience

이 README의 주요 독자:

- SRE / Platform Engineer
- AI Operator
- Security Reviewer
- AI Agent

## Scope

### In Scope

- Ollama 운영 정책 (모델/VRAM/승격 기준)
- Open WebUI 운영 정책 (SSO, RAG 데이터 취급, 변경 게이트)
- AI Agent 변경 통제 및 증적 보존 기준

### Out of Scope

- 단계별 복구 커맨드 (09.runbooks)
- 사용/학습 가이드 (07.guides)

## Structure

```text
08-ai/
├── ollama.md
├── open-webui.md
├── optimization-hardening.md
└── README.md
```

## Documents

- [Ollama Operations Policy](./ollama.md)
- [Open WebUI Operations Policy](./open-webui.md)
- [08-AI Optimization Hardening Operations Policy](./optimization-hardening.md)

## How to Work in This Area

1. 새 정책 문서는 `docs/99.templates/operation.template.md`를 따른다.
2. 정책 변경 시 해당 런북/가이드를 동시 점검한다.
3. 예외 규칙은 승인 경로와 종료 조건을 함께 기록한다.
4. AI Agent 정책 섹션(변경 프로세스/가드레일/보존/안전 임계치)을 누락하지 않는다.
5. 최적화/하드닝 변경 시 `optimization-hardening.md`와 상위 Plan/Task를 동시 갱신한다.

## Related References

- [AI Guides](../../07.guides/08-ai/README.md)
- [AI Runbooks](../../09.runbooks/08-ai/README.md)
- [AI Spec (공통)](../../04.specs/08-ai/spec.md)
- [Open WebUI Spec](../../04.specs/08-ai/open-webui.md)
- [AI Optimization PRD](../../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- [AI Optimization Plan](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [AI Optimization Tasks](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
