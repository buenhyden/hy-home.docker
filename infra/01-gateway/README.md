---
title: "Gateway Tier (01-gateway)"
version: "1.1.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-10"
created: "2025-11-12"
---

# Gateway Tier (01-gateway)

> 라우팅, TLS, 보안을 조율하는 모든 트래픽의 단일 진입점입니다.

## Overview

`01-gateway` tier는 `hy-home.docker` 생태계로 들어오는 트래픽의 단일 진입점입니다. 루트 스택은 `traefik` leaf를 무조건 include하며, profile이 실제로 기동되는 서비스를 결정합니다: `traefik`은 `core`, `dev`, `local`에 속합니다. profile이 선택되지 않으면 기동되지 않습니다. 대안 gateway였던 Nginx는 2026-11-10 소유자 결정으로 저장소에서 퇴역했습니다.

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- Backend Developers
- Security Auditors

## Scope

### In Scope

- Traefik(에지 라우터) 설정과 루트 스택 배포.
- TLS 종료와 인증서 관리.
- Docker provider를 통한 동적 서비스 탐색.

### Out of Scope

- 애플리케이션 수준의 비즈니스 로직.
- 장기 로그 저장 또는 분석(Observability tier가 담당).
- Identity provider 관리(Auth tier가 담당).

## Structure

```text
01-gateway/
├── traefik/         # 동적 서비스 탐색을 갖춘 주 에지 라우터
└── README.md        # 이 파일
```

## Tech Stack

런타임 이미지 고정 값은 각 서비스의 compose 파일이 소유합니다: [traefik/](traefik/). [버전 레지스트리](../tech-stack.versions.json)는 파생된 Compose 이미지 투영입니다.

| Category   | Technology                        | Notes                     |
| ---------- | --------------------------------- | ------------------------- |
| Router     | Traefik                    | 주 동적 라우터    |
| Discovery  | Docker Provider                   | 컨테이너 자동 탐지 |
| Security   | OAuth2 Proxy / Keycloak           | 통합 SSO 제공자   |

## Networking (Ports)

정확한 포트 번호와 프로토콜은 각 서비스의 서비스 준비성 정보가 소유합니다: [traefik/](traefik/). Traefik은 HTTP/HTTPS 진입점과 메트릭 진입점을 게시합니다.

## Usage

1. [문서 인덱스](../../docs/README.md)와 subject package `docs/05.operations/README.md`를 검토해 트래픽 흐름을 이해합니다.
2. 배포 전 `scripts/operations/gen-secrets.sh`로 secret을 생성했는지 확인합니다.
3. 초기 배포 경계는 `docs/05.operations/README.md`의 subject `0012-edge-routing-stack`을 따릅니다.
4. `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`와 `bash scripts/hardening/check-all-hardening.sh 01-gateway`로 정적 준비성을 확인합니다. runtime 헬스 명령은 승인된 실행 중 스택에 대해서만 사용합니다.

## Related Documents

- [Agent 거버넌스](../../AGENTS.md)
- 시스템 아키텍처 (`docs/02.architecture/descriptions/README.md`)
- [Secret 관리](../../secrets/README.md)
- Gateway 가이드 (`docs/05.operations/guides/README.md`)
- 운영 정책 (`docs/05.operations/policies/README.md`)
- 비상 런북 (`docs/05.operations/runbooks/README.md`)
- [문서 인덱스](../../docs/README.md)
