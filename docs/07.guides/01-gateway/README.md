# Gateway Tier Guides

> Comprehensive guides for understanding and setting up the entry point infrastructure.

## Overview

This directory contains architectural guides, initial setup instructions, and general usage patterns for the `01-gateway` tier. Our goal is the harmonious operation of Traefik and Nginx acting as the dual-gateways for the `hy-home.docker` ecosystem.

## Overview (KR)

이 디렉토리는 `01-gateway` 티어의 아키텍처 이해, 초기 설정, 그리고 일반적인 사용법에 대한 가이드 문서를 포함합니다. `hy-home.docker`의 관문 역할을 하는 Traefik과 Nginx의 조화로운 운영을 목표로 합니다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- AI Agents

## Scope

### In Scope

- Service onboarding guides
- Nginx & Traefik configuration tutorials
- SSO integration patterns for gateway

### Out of Scope

- Operational policies (handled in `docs/08.operations`)
- Step-by-step recovery procedures (handled in `docs/09.runbooks`)

## Structure

```text
01-gateway/
├── nginx.md       #- [Nginx](nginx.md): Nginx Gateway guide.
- [Traefik](traefik.md): Traefik Edge Router guide.
└── README.md       # This file
```

## Related Documents

- [01-gateway Root README](../../../infra/01-gateway/README.md)
- [Gateway Operations](../../../docs/08.operations/01-gateway/README.md)
- [Gateway Runbooks](../../../docs/09.runbooks/01-gateway/README.md)

---

## AI Agent Guidance

1. Read this README first to understand the guide structure.
2. When creating a new guide, use `docs/99.templates/guide.template.md`.
3. Ensure all internal links are relative and validated.
