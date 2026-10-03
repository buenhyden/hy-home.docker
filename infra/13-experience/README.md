---
title: "13 경험 자산"
version: "0.1.0"
type: "common/package-readme"
status: "review"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-10-03"
---

# 13 경험 자산

## Overview

공유 UI 구성요소를 검토하는 정적 Storybook origin을 소유한다. 폴더 번호는
기동 순서가 아니며 새 업무 앱의 저장 위치도 아니다.

## Audience

UI 개발자, 디자인 검토자와 인프라 운영자를 위한 인덱스다.

## Scope

선택형 `storybook` 서비스의 Compose 선언과 운영 설명을 포함한다.
컴포넌트 코드·story·정적 빌드는 기존 `projects/storybook/nextjs`가 소유한다.
로컬 문서 MCP와 외부 업무 앱은 이 tier의 서비스가 아니다.

## Structure

| Package | 역할 | 분류·profile | 의존성 |
| --- | --- | --- | --- |
| [storybook](storybook/README.md) | 정적 Storybook 문서 origin | OPTIONAL / `experience` | Traefik·OAuth2 Proxy·Keycloak은 브라우저 접근 시 별도 선택 |

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| 정적 origin | 비특권 NGINX image | 정확한 image는 [Storybook 패키지 문서](storybook/README.md)에서 연결한 Compose가 소유 |
| 브라우저 ingress | 기존 Traefik + OAuth2 Proxy | 관리자 `/admins`만 허용 |
| 내부 연결 | `experience_ingress_net` | Storybook과 Traefik만 연결하는 internal network |

## Configuration

root [Compose](../../docker-compose.yml)가 leaf를 include하고 전용망을 선언한다.
`experience`는 HOME 선택에 포함되지 않는다. static origin에는 secret,
영속 volume, host port가 없다. `DEFAULT_URL`은 기존 공개 route 이름만
제공한다. 이미지 빌드 소스·revision과 MCP는
[Storybook 프로젝트](../../projects/storybook/nextjs/README.md)를 따른다.

## Validation

```bash
docker compose --env-file .env.example --profile experience config --quiet
python3 scripts/validation/check-operations-catalog.py
```

정적 render는 HOME 기동, DNS/TLS, 로그인이나 브라우저 사용성을 증명하지 않는다.

## How to Work in This Area

1. 소스 revision과 image label·manifest revision을 대조한다.
2. root와 Traefik의 전용망 연결, `sso-auth@file` 및 profile 분류를 함께 검토한다.
3. 실제 기동·재시작은 별도 운영 승인 이후에만 수행한다.

## Related Documents

- [상위 인프라](../README.md)
- [서비스 패키지](storybook/README.md)
- [문서 진입점](../../docs/README.md)에서 GDE-0101, POL-0101, RUN-0101 확인
