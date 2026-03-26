# Gateway Tier Guides

> Comprehensive guides for understanding and setting up the entry point infrastructure.

## Overview

This directory contains architectural guides, initial setup instructions, and general usage patterns for the `01-gateway` tier. Our goal is the harmonious operation of Traefik and Nginx acting as the dual-gateways for the `hy-home.docker` ecosystem.

## Overview (KR)

이 디렉토리는 `01-gateway` 티어의 아키텍처 이해, 초기 설정, 그리고 일반적인 사용법에 대한 가이드 문서를 포함합니다. `hy-home.docker`의 관문 역할을 하는 Traefik과 Nginx의 조화로운 운영을 목표로 합니다.

## Audience

이 문서의 주요 독자:

- Infrastructure Operators
- Backend Developers
- AI Agents

## Documentation Standards

- All guides must follow the `guide.template.md`.
- Ensure Single Source of Truth by referencing the `infra/` configuration directly when explaining setups.
- Maintain traceability to PRDs and ARDs.

## Guide Table

| Document | Purpose |
| :--- | :--- |
| [01.setup.md](./01.setup.md) | Step-by-step instructions for initial gateway deployment |
| [traefik.md](./traefik.md) | Deep dive into Traefik configuration and service discovery |
| [nginx.md](./nginx.md) | Detailed guide for Nginx path-based routing and SSO |

## Related References

- [Infrastructure Source](../../../infra/01-gateway/README.md)
- [Operational Policies](../../../docs/08.operations/01-gateway/README.md)
- [Troubleshooting Runbooks](../../../docs/09.runbooks/01-gateway/README.md)

---

## AI Agent Guidance

1. Read this README first to understand the guide structure.
2. When creating a new guide, use `docs/99.templates/guide.template.md`.
3. Ensure all internal links are relative and validated.
