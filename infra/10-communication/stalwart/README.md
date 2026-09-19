---
title: "Stalwart Mail Server"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-12-03"
---

# Stalwart Mail Server

## Overview

Stalwart는 실제 메일 송수신을 위한 선택형 서비스다. `mail-server` profile에서만 선택되며 운영 subject는 `0070-mail`이다. 개발 캡처는 [Mailpit](../mailpit/README.md) 및 subject `0084-mailpit`이 담당한다.

## Audience

메일 운영자, DNS/TLS 담당자와 인프라 엔지니어.

## Scope

Stalwart의 SMTP/IMAP/JMAP, 관리 UI, 비밀 참조와 데이터 저장 선언을 설명한다. 개발 SMTP 트랩과 DNS 공급자 변경 절차는 포함하지 않는다.

## Structure

[docker-compose.yml](docker-compose.yml)이 단일 `stalwart` 서비스를 정의한다. 루트 [docker-compose.yml](../../../docker-compose.yml)이 leaf를 include한다.

## How to Work in This Area

[가이드 — 문서 인덱스](../../../docs/README.md) (`GDE-0070`), [정책 — 문서 인덱스](../../../docs/README.md) (`POL-0070`), [런북 — 문서 인덱스](../../../docs/README.md) (`RUN-0070`)을 따른다. 운영 시작 전 DNS, TLS, 인증, host 포트와 데이터 복구 증거를 확보한다.

## Configuration

| Setting | Source / behavior |
| --- | --- |
| Profile | `mail-server` |
| Image | [Compose](docker-compose.yml); [curated projection](../../tech-stack.versions.json) |
| Data | `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` → `/opt/stalwart` |
| Certificates | `${DEFAULT_CERT_DIR}` → `/opt/stalwart/certs:ro` |
| Secret | `stalwart_password` → `/run/secrets/stalwart_password`; 원문 출력 금지 |
| Host ports | `SMTP_HOST_PORT`, `SUBMISSION_HOST_PORT`, `SMTPS_HOST_PORT`, `IMAPS_HOST_PORT`, `MANAGESIEVE_HOST_PORT` |
| UI | `mail.${DEFAULT_URL}` → `${STALWART_PORT:-8080}`, Traefik SSO 보호 |

## Service Readiness

서비스와 healthcheck는 [Compose](docker-compose.yml)에 선언되어 있다. SMTP TCP healthcheck는 외부 배달·TLS·인증 검증을 대신하지 않는다. 실제 메일함 데이터, 백업 및 복원 성공 여부는 별도 운영 증거가 필요하다. 개발 테스트는 [Mailpit 가이드 — 문서 인덱스](../../../docs/README.md) (`GDE-0084`)를 따른다.

## Validation

저장소 루트에서 공개 예시 환경으로 검사한다.

```bash
docker compose --env-file .env.example --profile mail-server config --services
bash scripts/hardening/check-all-hardening.sh 10-communication
```

## Troubleshooting

기동된 운영 인스턴스의 상태는 `docker compose --profile mail-server ps stalwart`로 확인한다. 관리 UI 경로와 메일 프로토콜 오류를 분리하고, 개인 메일·비밀을 제거한 증거만 런북에 기록한다. 데이터 삭제나 검증되지 않은 downgrade를 일반 복구로 실행하지 않는다.

## Related Documents

- [Communication tier](../README.md).
- [Stalwart 공식 Docker 설치 문서](https://stalw.art/docs/install/platform/docker/).
