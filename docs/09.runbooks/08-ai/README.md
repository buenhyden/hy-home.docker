# AI Tier Runbooks (08-ai)

> `08-ai` 계층의 실행형 복구/유지보수 런북 모음.

## Overview

이 디렉터리는 AI 계층 운영 중 발생하는 장애/성능 저하 상황에서 즉시 실행 가능한 절차를 제공한다. 서비스 단위 런북과 하드웨어 공통 복구 런북의 역할을 분리해 관리한다.

## Audience

이 README의 주요 독자:

- On-call Engineer
- AI Operator
- Platform Engineer
- AI Agent

## Scope

### In Scope

- 서비스 런북:
  - Open WebUI 장애/복구 절차
  - Ollama 추론 장애/복구 절차
- 공통 런북:
  - GPU 드라이버/런타임 복구 절차

### Out of Scope

- 정책 기준 정의 (08.operations)
- 기능 사용 가이드 (07.guides)
- 사고 분석/회고 (10/11)

## Structure

```text
08-ai/
├── gpu-recovery.md
├── ollama.md
├── open-webui.md
├── optimization-hardening.md
└── README.md
```

## Documents

- [Open WebUI Maintenance & Recovery Runbook](./open-webui.md)
- [Ollama Maintenance & Recovery Runbook](./ollama.md)
- [GPU Recovery Runbook](./gpu-recovery.md)
- [08-AI Optimization Hardening Runbook](./optimization-hardening.md)

## How to Work in This Area

1. 새 런북은 `docs/99.templates/runbook.template.md` 구조를 따른다.
2. 모든 런북은 체크리스트/절차/검증/롤백 단계를 포함한다.
3. Canonical References에 ARD/ADR/Spec/Plan을 명시한다.
4. 관련 정책(08)과 가이드(07) 링크를 항상 유지한다.
5. 최적화/하드닝 회귀 복구 시 `check-ai-hardening.sh` 결과를 증적으로 남긴다.

## Related Operational Documents

- [AI Operations](../../08.operations/08-ai/README.md)
- [AI Guides](../../07.guides/08-ai/README.md)
- [Incidents](../../10.incidents/README.md)
- [Postmortems](../../11.postmortems/README.md)
- [AI Optimization Plan](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [AI Optimization Tasks](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
