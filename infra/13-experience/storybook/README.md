---
title: "공유 Storybook 정적 origin"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2026-10-03"
---

# 공유 Storybook 정적 origin과 원격 문서 MCP

## Overview

`storybook` 서비스는 검토된 공유 UI story와 문서의 빌드 결과를 내부 8080
포트에서 읽기 전용으로 제공한다. Traefik의 HTTPS 브라우저 route는 기존
OAuth2 Proxy의 Keycloak `/admins` 판정을 사용한다. `storybook-mcp`는 같은
빌드의 manifest를 다른 워크스페이스의 Codex·Claude Code에 문서 tool로 제공하며
Keycloak bearer token만 받는다.

## Audience

공유 UI 사용자, 디자인 검토자, 운영자와 검증 담당자를 위한 패키지다.

## Scope

두 image 선언, 선택형 profile, Traefik route, 망과 health를 소유한다. 컴포넌트
패키지, MCP 서버 코드와 image 빌드는
[Storybook 프로젝트](../../../projects/storybook/nextjs/README.md)가 소유한다.

## Structure

```text
storybook/
├── docker-compose.yml # root에 include되는 정적 origin 선언
└── README.md          # 이 패키지 계약
```

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| 이미지 | `hy-home/storybook:<source-SHA>` | [Compose](docker-compose.yml)의 SHA tag가 소유; `pull_policy: never` |
| 서버 | 비특권 정적 NGINX | [Dockerfile](../../../projects/storybook/nextjs/Dockerfile)과 설정 소유 |
| MCP 이미지 | `hy-home/storybook-mcp:<source-SHA>` | 정적 image와 같은 커밋; `pull_policy: never` |
| 인증 | 정적 origin은 Traefik `sso-auth@file`; MCP는 서버의 bearer 검증 | 비인증 브라우저는 Keycloak으로 302, JSON 요청은 401; MCP는 401/403 |

## Configuration

root [Compose](../../../docker-compose.yml)가 leaf를 include한다. 유일한 선택
profile은 `experience`이며 HOME에는 없다. `storybook`은 `internal: true`
전용 `experience_ingress_net`에만 연결되고 Traefik만 이 망과 `edge_net`에
함께 연결한다. `traefik.docker.network`는 전용망을 가리킨다. host port,
영속 volume, secret mount는 없다. `DEFAULT_URL`은 기존 route host 이름을
정할 뿐 새 환경 키나 비밀값을 요구하지 않는다.

공통 읽기 전용 저자원 템플릿에서 CPU·메모리 한도, capability 제거,
`no-new-privileges`, tmpfs와 로그 제한을 상속한다. 템플릿의 secret 소비용
추가 group은 `!override`로 제거한다. 사용 중인 Compose의
[merge 기능](https://docs.docker.com/reference/compose-file/merge/) 지원을 확인한다.
실행 사용자는 `101:101`
이며 HTTP GET `/` health는 정적 서버 응답만 확인한다. 이 신호는 SSO,
TLS, asset 또는 package 정확성을 증명하지 않는다. image의 OCI revision
label과 `revision.json.sourceRevision`은 승인된 소스 SHA와 같아야 한다.

브라우저 route는 `storybook.${DEFAULT_URL}`의 HTTPS에서만 활성화된다.
비인증 브라우저 요청은 Keycloak 로그인으로 302되고, 어떤 경로도 내용이나 로그인
HTML을 200으로 주지 않는다.

`storybook-mcp`는 `edge_net`에 연결되고 host의 root CA를 읽어
`https://keycloak.${DEFAULT_URL}`의 discovery와 JWKS를 가져온다. route
`storybook-mcp.${DEFAULT_URL}`은 `/mcp`와 `/.well-known/oauth-protected-resource`만
전달하며 `sso-auth@file`을 쓰지 않는다. 서버가 issuer, 자기 URL audience, 만료,
서명과 `/admins` 그룹을 확인한다. 실행 사용자는 `1000:1000`이며 health는 보호 자원
metadata 응답을 확인한다. DNS/TLS와
실제 브라우저 동작은 운영 실행 승인 전까지 미확인이다. Docker daemon
권한으로 전용망에 다른 container를 붙일 수 있는 운영자 신뢰 경계는 남는다.

## Validation

```bash
docker compose --env-file .env.example --profile experience config --quiet
HYHOME_COMPOSE_PROFILES='core experience' bash scripts/validation/validate-docker-compose.sh
python3 scripts/validation/check-operations-catalog.py
```

정적 검증과 격리 image 검사는 HOME 배포의 증거가 아니다. 실행 전 Docker context,
project, port, network, volume, resource와 정리 범위를 확인한다.

## Usage

1. `python3 scripts/operations/storybook_image.py verify`로 두 image의 커밋, OCI label, revision과 manifest hash를 대조한다.
2. `experience` 선택과 HOME 미선택, 전용망의 두 서비스 연결, 관리자 ForwardAuth를 검토한다.
3. 변경 후 정적 검사와 승인된 격리 검사를 수행하고 결과를 승인된 운영 Task와 RUN-0101 evidence handoff에 기록한다.

## Related Documents

- [13 경험 자산](../README.md)
- [인프라 인덱스](../../README.md)
- [문서 진입점](../../../docs/README.md)에서 GDE-0101, POL-0101, RUN-0101 확인
