---
title: "Stalwart Mail Server"
version: "2.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-12-03"
---

# Stalwart Mail Server

## Overview

Stalwart는 내부 전용 메일 서버를 목표로 하며 host port와 외부 relay를 선언하지 않는다.
다만 현재 서버는 `mail_net`과 `edge_net` 양쪽에 연결되고 listener는 wildcard 주소에
바인딩된다. 따라서 `mail_net` 전용 접근 통제가 구현됐다고 볼 수 없다. 정책은 유지하며
네트워크 제한 보완은 별도 구현 과제로 남는다. `mail-server` profile에서만 선택되며 운영 subject는 `0070-mail`이다. 개발 캡처는 [Mailpit](../../11-quality/mailpit/README.md) 및 subject `0084-mailpit`이 담당한다.

## Audience

메일 운영자, DNS/TLS 담당자와 인프라 엔지니어.

## Scope

Stalwart의 SMTP/IMAP/JMAP, 관리 UI, 비밀 참조와 데이터 저장 선언을 설명한다. 개발 SMTP 트랩과 DNS 공급자 변경 절차는 포함하지 않는다.

## Structure

```text
stalwart/
├── README.md
├── docker-compose.yml     # stalwart, stalwart-config
└── config/
    ├── config.json        # datastore only (RocksDB in /var/lib/stalwart)
    ├── plan.ndjson        # domain, four listeners, no relaying
    ├── start.sh           # recovery admin from the secret, then the server
    ├── apply-plan.sh      # renders DEFAULT_URL and applies the plan
    └── Dockerfile         # server image plus the pinned stalwart-cli
```

루트 [docker-compose.yml](../../../docker-compose.yml)이 leaf를 include한다.

## Usage

[가이드 — 문서 인덱스](../../../docs/README.md) (`GDE-0070`), [정책 — 문서 인덱스](../../../docs/README.md) (`POL-0070`), [런북 — 문서 인덱스](../../../docs/README.md) (`RUN-0070`)을 따른다. 운영 시작 전 DNS, TLS, 인증, host 포트와 데이터 복구 증거를 확보한다.

## Configuration

| Setting | Source / behavior |
| --- | --- |
| Profile | `mail-server` |
| Image | [Compose](docker-compose.yml); [derived Compose image projection](../../tech-stack.versions.json) |
| Data | `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` → `/var/lib/stalwart` (소스가 기대하는 사용자 UID는 2000; 첫 기동 전 실제 경로의 소유권·권한을 별도 확인하고 자동 보정을 가정하지 않음) |
| Configuration | `config/plan.ndjson`을 `stalwart-config`가 적용; listener 변경은 다음 재시작부터 |
| Secret | `stalwart_password` (COMM-006) → recovery admin; Compose에 credential 없음. 한 줄, `:` 없는 값이어야 함(`user:password`로 조합) |
| Host ports | 없음. SMTP 25·submission 587·IMAPS 993은 wildcard listener이며 `mail_net`·`edge_net` peer 접근을 구분해 검토해야 함 |
| Relay | 없음 (`allowRelaying = false`); 설정 도메인 밖 수신자는 SMTP `550`(`Relay not allowed`) |
| UI | `mail.${DEFAULT_URL}` → 8080, Traefik SSO 보호 |

## Service Readiness

서비스와 healthcheck는 [Compose](docker-compose.yml)에 선언되어 있다. `/healthz/live` healthcheck는 배달·TLS·인증 검증을 대신하지 않는다. 실제 메일함 데이터, 백업 및 복원 성공 여부는 별도 운영 증거가 필요하다. 개발 테스트는 [Mailpit 가이드 — 문서 인덱스](../../../docs/README.md) (`GDE-0084`)를 따른다.

## Validation

저장소 루트에서 공개 예시 환경으로 검사한다.

```bash
docker compose --env-file .env.example --profile mail-server config --services
bash scripts/hardening/check-all-hardening.sh 10-communication
```

별도 실행 승인이 있는 경우에만 `HYHOME_MAIL_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.StalwartRehearsalTests`로 런타임 리허설을 수행한다. 정적 검사 결과는 배달·복구 성공을 뜻하지 않는다.

## Troubleshooting

기동된 운영 인스턴스의 상태는 `docker compose --profile mail-server ps stalwart`로 확인한다. 관리 UI 경로와 메일 프로토콜 오류를 분리하고 개인 메일·비밀을 제거한 증거만 런북에 기록한다. 데이터 삭제나 검증되지 않은 downgrade를 일반 복구로 실행하지 않는다.

## Related Documents

- [Communication tier](../README.md).
- [Stalwart 공식 Docker 설치 문서](https://stalw.art/docs/install/platform/docker/).
