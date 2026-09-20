---
title: "Communication Tier (10-communication)"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-12"
---

# Communication Tier (10-communication)

## Overview

실제 메일 서버 Stalwart와 개발용 SMTP 캡처 Mailpit을 별도 leaf·profile·운영 subject로 관리한다. Stalwart는 선택형 `mail-server`, Mailpit은 `dev`, `local`, `mail-dev`에서 선택된다.

## Audience

애플리케이션 개발자, 메일 서비스 운영자와 인프라 담당자.

## Scope

메일 서비스 선택, 네트워크·영속성 선언과 운영 문서 연결을 소유한다. 메일 내용, 비밀 원문 및 도메인 공급자의 설정 변경은 이 README의 범위 밖이다.

## Structure

| Leaf | Profile | 운영 소유자 |
| --- | --- | --- |
| [stalwart/](stalwart/README.md) | `mail-server` | [0070-mail — 문서 인덱스](../../docs/README.md) (`GDE-0070`): 실제 송수신 |
| [mailpit/](mailpit/README.md) | `dev`, `local`, `mail-dev` | [0084-mailpit — 문서 인덱스](../../docs/README.md) (`GDE-0084`): 개발 캡처 |

## How to Work in This Area

1. 개발 SMTP는 Mailpit을 사용하고 외부 배달 경로와 분리한다.
2. Stalwart는 DNS·TLS·인증·포트·백업 복구 준비를 확인한 뒤 선택한다.
3. 루트 Compose의 network·secret·공통 template 맥락을 유지해 검증한다.
4. 이미지와 포트 기본값은 [Stalwart Compose](stalwart/docker-compose.yml), [Mailpit Compose](mailpit/docker-compose.yml)를 참조한다. [Derived Compose image projection](../tech-stack.versions.json)은 drift 검증 자료다.

## Configuration

Mailpit UI/SMTP 호스트 바인딩은 loopback이며 수신 데이터는 `/data/mailpit.db`에 영속화한다. 내부 애플리케이션은 `mailpit` 서비스 DNS를 사용한다. Stalwart는 실제 메일 프로토콜 포트를 호스트에 게시하고 `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`를 보존한다. 관리 UI SSO는 SMTP/IMAP의 별도 인증·TLS를 대신하지 않는다.

## Testing

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile mail-dev config --services
docker compose --env-file .env.example --profile mail-server config --services
bash scripts/hardening/check-all-hardening.sh 10-communication
```

정적 통과는 실제 메일 배달·수신 또는 데이터 복원 성공의 증거가 아니다.

## Related Documents

- [Stalwart 정책 — 문서 인덱스](../../docs/README.md) (`POL-0070`), [런북 — 문서 인덱스](../../docs/README.md) (`RUN-0070`).
- [Mailpit 정책 — 문서 인덱스](../../docs/README.md) (`POL-0084`), [런북 — 문서 인덱스](../../docs/README.md) (`RUN-0084`).
- [Stalwart 공식 Docker 설치](https://stalw.art/docs/install/platform/docker/), [Mailpit 공식 문서](https://mailpit.axllent.org/docs/).
- [Infrastructure index](../README.md).
