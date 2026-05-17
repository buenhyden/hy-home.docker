# 08-ai Specifications

> AI 추론 및 인터페이스 서비스 기술 사양

## Overview

`docs/03.specs/08-ai`는 Ollama, Open WebUI 등 AI 서비스 계층의 기술 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

## Scope

### In Scope

- 모델 서빙 인터페이스, API 사양, GPU 리소스 경계
- Open WebUI 연동 및 인증 흐름 사양

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/08-ai/` 담당)

## Structure

```text
08-ai/
├── spec.md          # AI services technical specification
├── open-webui.md    # Open WebUI integration spec
└── README.md        # This file
```

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. Open WebUI 변경은 [open-webui.md](./open-webui.md)를 함께 확인합니다.
3. 상위 요구사항과 아키텍처 맥락은 Related Documents의 PRD/ARD/ADR 링크에서 추적합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [open-webui.md](./open-webui.md)
- [docs/03.specs/README.md](../README.md)
- [infra/08-ai/README.md](../../../infra/08-ai/README.md)
- [docs/05.operations/guides/08-ai/](../../05.operations/guides/08-ai/)
