---
title: "Communication Tier (10-communication)"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# Communication Tier (10-communication)

## Overview

운영 메일 서버 Stalwart와 설정 helper를 소유한다. 개발용 SMTP 캡처 Mailpit은 [11 Quality](../11-quality/README.md)에서 별도 profile·운영 subject로 관리한다. Stalwart는 선택형 `mail-server`, Mailpit은 `dev`, `local`, `mail-dev`에서 선택된다.

## Audience

애플리케이션 개발자, 메일 서비스 운영자와 인프라 담당자.

## Scope

메일 서비스 선택, 네트워크·영속성 선언과 운영 문서 연결을 소유한다. 메일 내용, 비밀 원문 및 도메인 공급자의 설정 변경은 이 README의 범위 밖이다.

## Structure

| Leaf | Profile | 운영 소유자 |
| --- | --- | --- |
| [stalwart/](stalwart/README.md) | `mail-server` | [0070-mail — 문서 인덱스](../../docs/README.md) (`GDE-0070`): 내부 전용 메일, host port·relay 없음 |
| [Mailpit — Quality](../11-quality/mailpit/README.md) | `dev`, `local`, `mail-dev` | [0084-mailpit — 문서 인덱스](../../docs/README.md) (`GDE-0084`): 개발 캡처 |

## Usage

1. 개발 SMTP는 Mailpit을 사용하고 외부 배달 경로와 분리한다.
2. Stalwart의 허용 용도는 내부 메일 제출이다. 현재 `edge_net` peer 접근도 가능한 선언이므로 `mail_net` 전용 통제가 완성됐다고 보지 않는다. 외부 송수신은 DNS·평판을 포함한 새 요구사항이 필요하다.
3. 루트 Compose의 network·secret·공통 template 맥락을 유지해 검증한다.
4. 이미지와 포트 기본값은 각 leaf의 Compose 파일([Stalwart](stalwart/README.md), [Mailpit](../11-quality/mailpit/README.md))을 참조한다. [Derived Compose image projection](../tech-stack.versions.json)은 drift 검증 자료다.

## Configuration

Mailpit UI/SMTP 호스트 바인딩은 loopback이며 수신 데이터는 `/data/mailpit.db`에 영속화한다. 내부 애플리케이션은 `mailpit` 서비스 DNS를 사용한다. Stalwart는 호스트 포트를 게시하지 않지만 서버가 `mail_net`과 `edge_net`에 연결되고 listener가 wildcard 주소에 바인딩되어 peer 접근 범위 보완이 필요하다. 데이터는 `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`에 보존한다. Mailpit도 `mail_net`에 있어 컨테이너가 캡처로 보낼 수 있다. 관리 UI SSO는 SMTP/IMAP의 별도 인증·TLS를 대신하지 않는다.

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
