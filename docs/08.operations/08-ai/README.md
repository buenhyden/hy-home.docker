# AI Tier Operations (08-ai)

> GPU Management, Model Governance & Capacity Planning

## Overview

이 디렉터리는 `hy-home.docker` AI 계층(08-ai)의 운영 정책 및 거버넌스 표준을 관리한다. 하드웨어 리소스 최적화와 모델 라이프사이클 통제를 목적으로 한다.

## Audience

이 README의 주요 독자:

- **Site Reliability Engineers (SRE)**: 시스템 안정성 및 리소스 관리
- **AI Operators**: 모델 배포 및 성능 모니터링
- **AI Agents**: 운영 정책 준수 및 자동화 대응

## Documents

- [Ollama Operations Policy](./ollama.md) - Model governance and VRAM management.
- [Open WebUI Operations Policy](./open-webui.md) - User access and document management standards.
- [AI Resource Policy](./README.md#gpu-resource-management) - Base GPU allocation rules.

## How to Work in This Area

1. 모든 운영 정책은 `operation.template.md`를 준수해야 한다.
2. 정책 변경 시 관련 런북([09.runbooks](../../09.runbooks/08-ai/README.md))과의 정렬을 확인한다.

## Related References

- [07. Guides](../../07.guides/08-ai/README.md) - Technical implementation details.
- [09. Runbooks](../../09.runbooks/08-ai/README.md) - Emergency procedures and tasks.
