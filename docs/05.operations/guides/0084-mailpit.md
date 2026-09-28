---
title: "Mailpit Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0084"
parent_ids:
- "POL-0084"
implementation_services:
  infra/10-communication/mailpit/docker-compose.yml:
  - mailpit
created: "2026-09-19"
---

# Mailpit Guide

## Usage

### Purpose and classification

Mailpit은 application과 integration test를 위한 DEV mail-capture
service이다. delivery MTA가 아니며 선택적인 Stalwart를 대체하지 않는다.
`dev`, `local`, `mail-dev`에 속하며 HOME에서는 제외된다. UI와 SMTP host
port는 `127.0.0.1`에 바인딩되고, UI는 Traefik을 통해서도 라우팅된다.

### Current implementation

- [Mailpit Compose](../../../infra/10-communication/mailpit/docker-compose.yml)가
  image, profile, port, environment, healthcheck, volume을 관장한다.
- SMTP는 `edge_net` 내부와 loopback host port
  `${MAILPIT_SMTP_HOST_PORT:-1025}`에서 listen한다. UI는 loopback
  `${MAILPIT_UI_HOST_PORT:-8025}`와 gateway middleware chain을 통한
  `mailpit.${DEFAULT_URL}`을 사용한다.
- `${DEFAULT_COMMUNICATION_DIR}/mailpit/data`가 `/data`에 bind로 연결되고
  `MP_DATABASE=/data/mailpit.db`가 영구 SQLite를 지정한다.
  `MP_MAX_MESSAGES=5000`은 개수 기준으로 오래된 메시지를 정리한다.
- `MP_SMTP_AUTH_ACCEPT_ANY=1`과 `MP_SMTP_AUTH_ALLOW_INSECURE=1`은 테스트
  호환성을 위해 plaintext SMTP로 임의의 credential을 의도적으로 수락한다.
  이 listener를 외부에 공개하거나 외부 메일로 라우팅하지 않는다.
- `/mailpit readyz` healthcheck는 process readiness만 증명하며, 메시지
  capture, UI 인증, retention, restoration은 증명하지 않는다.

### Normal use

1. root에서 `docker compose --profile mail-dev config --quiet`로
   validate한다.
2. 개발용 application이 `edge_net`의
   `mailpit:${MAILPIT_SMTP_PORT:-1025}`로 전송하도록 설정한다. host tool은
   loopback host port를 사용한다.
3. 합성 또는 승인된 test mail만 전송한다. database에는 본문, header, 주소,
   첨부가 들어 있으므로 민감한 test data로 취급해야 한다.
4. 인증된 UI나 제한된 API query로 capture를 확인한 뒤, retention policy에
   따라 test data를 삭제/만료시킨다.

### Backup and upgrade

Mailpit은 `mailpit dump`로 live message export를, `mailpit ingest`로
restore 방식의 ingestion을 지원한다. 활성 SQLite/WAL 파일을 복사하기보다
live HTTP dump를 우선 사용한다. database를 복사해야 한다면 Mailpit을 멈추고
database와 SQLite sidecar를 일관되게 함께 복사한다. 이미지 upgrade 전에는
메시지를 export하고, database checksum을 기록하고, Mailpit만 재생성한 뒤
capture와 메시지 수를 검증한다. restore는 먼저 격리된 Mailpit instance에서
수행한다. 이 절차는 문서로 남겼지만 이 task에서 실행하지는 않았다.

## Common Checks

- `docker compose --profile mail-dev config --quiet`
- `docker compose --profile mail-dev config --services`
- `bash scripts/hardening/check-all-hardening.sh 10-communication`

## Runbook Handoff

capture 실패, 일관된 export/restore, retention incident, 이미지 upgrade에는
[runbook](../runbooks/0084-mailpit.md)을 사용한다.

## Traceability

- [Policy](../policies/0084-mailpit.md) (`POL-0084`)
- [Runbook](../runbooks/0084-mailpit.md) (`RUN-0084`)
- [Communication architecture](../../02.architecture/descriptions/0010-communication-architecture.md)

## Related Documents

- [Mailpit email storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [Mailpit SMTP security](https://mailpit.axllent.org/docs/configuration/smtp/)
- [Mailpit import and export](https://mailpit.axllent.org/docs/usage/import-export/)
- [Operations index](../README.md)
