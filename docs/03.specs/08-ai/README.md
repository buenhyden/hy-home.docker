# 08-ai Specifications

> AI 추론 및 인터페이스 서비스 기술 사양

## Overview

`docs/03.specs/08-ai`는 Ollama, Open WebUI 등 AI 서비스 계층의 기술 사양을 포함합니다.

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

## Related Documents

- [spec.md](./spec.md)
- [open-webui.md](./open-webui.md)
- [docs/03.specs/README.md](../README.md)
- [infra/08-ai/README.md](../../../infra/08-ai/README.md)
- [docs/05.operations/guides/08-ai/](../../05.operations/guides/08-ai/)
