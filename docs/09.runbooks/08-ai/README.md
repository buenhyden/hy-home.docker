# AI Tier Runbooks (08-ai)

> NVIDIA Driver Issues, VRAM OOM & Inference Recovery

## Overview

이 디렉터리는 `08-ai` 계층에서 발생할 수 있는 긴급 장애 대응 및 반복적인 유지보수 절차를 정의한다. 실행 중심의 문서(Actionable Document)를 관리한다.

## Audience

이 README의 주요 독자:

- **On-call Engineers**: 서비스 장애 대응 및 긴급 복구
- **AI Operators**: 모델 배포 및 인프라 점검
- **AI Agents**: 장애 자동 탐지 및 복구 시나리오 실행

## Documents

- [Ollama Runbook](./ollama.md) - GPU recovery, OOM mitigation, and API troubleshooting.
- [Open WebUI Runbook](./open-webui.md) - DB recovery, RAG maintenance, and connection fixes.
- [GPU Recovery Guide](./gpu-recovery.md) - Specialized GPU driver/toolkit recovery.

## How to Work in This Area

1. 모든 런북은 즉시 실행 가능한 단계(`Procedure`)를 반드시 포함해야 한다.
2. 실행 전후의 검증 단계(`Verification`)를 명시한다.
3. 복구 실패 시의 대응(`Rollback/Recovery`)을 정의한다.

## Related Operational Documents

- [Operations Policy](../../08.operations/08-ai/README.md) - Resource management rules.
- [Inference Guide](../../07.guides/08-ai/ollama.md) - System context and details.
