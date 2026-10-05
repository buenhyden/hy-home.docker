---
title: "Mailpit Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0084"
parent_ids:
- "POL-0084"
implementation_services:
  infra/11-quality/mailpit/docker-compose.yml:
  - mailpit
created: "2026-09-19"
---

# Mailpit Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Purpose and classification

Mailpit은 application과 integration test를 위한 DEV mail-capture
service이다. delivery MTA가 아니며 선택적인 Stalwart를 대체하지 않는다.
`dev`, `local`, `mail-dev`에 속하며 HOME에서는 제외된다. UI와 SMTP host
port는 `127.0.0.1`에 바인딩되고, UI는 Traefik을 통해서도 라우팅된다.

### Current implementation

- [Mailpit Compose](../../../infra/11-quality/mailpit/docker-compose.yml)가
  image, profile, port, environment, healthcheck, volume을 관장한다.
- SMTP는 `edge_net`·`mail_net` 내부와 loopback host port
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
4. gateway 인증 경로 또는 승인된 loopback/peer 경로의 제한된 조회로 capture를
   확인한 뒤, retention policy에
   따라 test data를 삭제/만료시킨다.

### Backup and upgrade

실행 순서와 실패·복구 판단은 [런북](../runbooks/0084-mailpit.md)의 `반출 방식과 업그레이드 사전 검토` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `docker compose --profile mail-dev config --quiet`
- `docker compose --profile mail-dev config --services`
- `bash scripts/hardening/check-all-hardening.sh 11-quality`

### Runbook Handoff

capture 실패, 일관된 export/restore, retention incident, 이미지 upgrade에는
[runbook](../runbooks/0084-mailpit.md)을 사용한다.

### 접근 경계의 의미

gateway 경로만 SSO를 거친다. 직접 loopback UI와 두 네트워크의 peer listener에는
동등한 네이티브 UI 인증이 선언되지 않았다. 테스트용 SMTP의 임의 인증 수락을
실제 인증으로 해석하지 않는다. 책임자 `@buenhyden`은 이 경계와 테스트 데이터
소유자를 확인해야 하며 신뢰하지 않는 consumer의 연결을 허용해서는 안 된다.

### Traceability

- [Policy](../policies/0084-mailpit.md) (`POL-0084`)
- [Runbook](../runbooks/0084-mailpit.md) (`RUN-0084`)
- [Communication architecture](../../02.architecture/descriptions/0010-communication-architecture.md)

## Related Documents

- [Mailpit email storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [Mailpit SMTP security](https://mailpit.axllent.org/docs/configuration/smtp/)
- [Mailpit import and export](https://mailpit.axllent.org/docs/usage/import-export/)
- [Operations index](../README.md)
