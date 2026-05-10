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

- 단계별 복구 커맨드 (07.operations)
- 사용/학습 가이드 (07.operations)

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

- [AI Usages](../../07.operations/08-ai/README.md)
- [AI Procedures](../../07.operations/08-ai/README.md)
- [AI Spec (공통)](../../04.specs/08-ai/spec.md)
- [Open WebUI Spec](../../04.specs/08-ai/open-webui.md)
- [AI Optimization PRD](../../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- [AI Optimization Plan](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [AI Optimization Tasks](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)

## Usage

> Migrated from `docs/07.operations/08-ai/README.md` during the 2026-05-10 operations taxonomy consolidation.

### AI Tier Usages (08-ai)

> `08-ai` 계층의 사용/설정/이해를 위한 가이드 문서 모음.

#### Overview

이 디렉터리는 AI 계층의 사용자·엔지니어 가이드를 관리한다. 서비스 운영 정책(08)이나 장애 복구 절차(09)가 아니라, 기능 이해와 재현 가능한 사용 방법을 제공하는 것이 목적이다.

#### Audience

이 README의 주요 독자:

- AI Engineer
- Operator
- Developer
- Internal User
- AI Agent

#### Scope

##### In Scope

- Open WebUI 사용 및 RAG 활용 가이드
- Ollama 추론 엔진 사용 가이드
- AI 계층 공통 학습/운영 준비용 가이드 문서

##### Out of Scope

- 정책/통제 기준 정의 (07.operations)
- 장애 대응/복구 절차 (07.operations)
- 사고 기록/회고 문서

#### Structure

```text
08-ai/
├── 01.llm-inference.md
├── 02.rag-workflow.md
├── local-llm-setup.md
├── ollama.md
├── open-webui.md
├── optimization-hardening.md
└── README.md
```

#### Documents

- [Open WebUI Interface & RAG Usage](./open-webui.md)
- [Ollama Inference Engine Usage](./ollama.md)
- [01. LLM Inference Usage](./01.llm-inference.md)
- [02. RAG Workflow Usage](./02.rag-workflow.md)
- [Local LLM Setup](./local-llm-setup.md)
- [08-AI Optimization Hardening Usage](./optimization-hardening.md)

#### How to Work in This Area

1. 새 가이드는 `docs/99.templates/operation.template.md` 구조를 따른다.
2. Open WebUI와 Ollama의 역할을 분리해서 문서를 작성한다.
3. 가이드 변경 시 대응 Operation/Procedure 링크를 함께 점검한다.
4. 상대 경로만 사용하고 깨진 링크를 남기지 않는다.
5. 최적화/하드닝 변경 시 `optimization-hardening.md`와 상위 Plan/Task 문서를 함께 갱신한다.

#### Related References

- [AI PRD (공통)](../../01.prd/2026-03-26-08-ai.md)
- [Open WebUI PRD](../../01.prd/2026-03-27-08-ai-open-webui.md)
- [AI ARD (공통)](../../02.ard/0008-ai-architecture.md)
- [Open WebUI ARD](../../02.ard/0013-open-webui-architecture.md)
- [AI Optimization PRD](../../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- [AI Optimization Plan](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [AI Optimization Tasks](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- [AI Operations](../../07.operations/08-ai/README.md)
- [AI Procedures](../../07.operations/08-ai/README.md)
- [AI Infra](../../../infra/08-ai/README.md)

## Procedure

> Migrated from `docs/07.operations/08-ai/README.md` during the 2026-05-10 operations taxonomy consolidation.

### AI Tier Procedures (08-ai)

> `08-ai` 계층의 실행형 복구/유지보수 런북 모음.

#### Overview

이 디렉터리는 AI 계층 운영 중 발생하는 장애/성능 저하 상황에서 즉시 실행 가능한 절차를 제공한다. 서비스 단위 런북과 하드웨어 공통 복구 런북의 역할을 분리해 관리한다.

#### Audience

이 README의 주요 독자:

- On-call Engineer
- AI Operator
- Platform Engineer
- AI Agent

#### Scope

##### In Scope

- 서비스 런북:
  - Open WebUI 장애/복구 절차
  - Ollama 추론 장애/복구 절차
- 공통 런북:
  - GPU 드라이버/런타임 복구 절차

##### Out of Scope

- 정책 기준 정의 (07.operations)
- 기능 사용 가이드 (07.operations)
- 사고 분석/회고 (10/11)

#### Structure

```text
08-ai/
├── gpu-recovery.md
├── ollama.md
├── open-webui.md
├── optimization-hardening.md
└── README.md
```

#### Documents

- [Open WebUI Maintenance & Recovery Procedure](./open-webui.md)
- [Ollama Maintenance & Recovery Procedure](./ollama.md)
- [GPU Recovery Procedure](./gpu-recovery.md)
- [08-AI Optimization Hardening Procedure](./optimization-hardening.md)

#### How to Work in This Area

1. 새 런북은 `docs/99.templates/operation.template.md` 구조를 따른다.
2. 모든 런북은 체크리스트/절차/검증/롤백 단계를 포함한다.
3. Canonical References에 ARD/ADR/Spec/Plan을 명시한다.
4. 관련 정책(08)과 가이드(07) 링크를 항상 유지한다.
5. 최적화/하드닝 회귀 복구 시 `check-ai-hardening.sh` 결과를 증적으로 남긴다.

#### Related Operational Documents

- [AI Operations](../../07.operations/08-ai/README.md)
- [AI Usages](../../07.operations/08-ai/README.md)
- [Incidents](../../10.incidents/README.md)
- [Postmortems](../../10.incidents/README.md)
- [AI Optimization Plan](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [AI Optimization Tasks](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
