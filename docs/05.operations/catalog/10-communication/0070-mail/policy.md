---
title: "Stalwart Mail Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0070"
parent_ids:
- "AD-0010"
created: "2026-05-17"
---

# Stalwart Mail Operations Policy

## Overview

실제 메일 송수신 서비스 Stalwart의 선택적 운영, 접근 제어, 데이터 보존 기준을 정의한다. 개발용 Mailpit 운영은 POL-0084가 소유한다.

## Policy Scope

- `infra/10-communication/stalwart/docker-compose.yml`의 `stalwart` 서비스와 `mail-server` profile.
- 실제 메일 도메인, 메일함 데이터, 프로토콜 TLS·인증 및 관리 UI.

## Controls

- 기본 HOME/DEV 기동에 실제 메일 서버를 포함하지 않는다. `mail-server`는 송수신 책임자와 운영 준비 증거를 확보한 뒤 선택한다.
- MX/SPF/DKIM/DMARC, TLS, 인증된 submission, host 노출 포트를 검증하며 open relay를 허용하지 않는다.
- 관리자 비밀은 Docker Secret 참조로 주입하고 원문을 문서·로그에 남기지 않는다.
- 관리 UI의 SSO와 메일 프로토콜의 인증·TLS를 별도로 검증한다.
- `stalwart-data`는 `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`에 보존한다. 현재 Compose는 백업 스케줄이나 검증된 복원을 제공하지 않으므로 운영 전 별도 증거가 필요하다.
- 서비스 로컬 standalone render를 루트 network/secret/template 맥락의 검증으로 대체하지 않는다.
- 개발 메일은 [Mailpit 정책](../0084-mailpit/policy.md)을 따른다. 테스트 데이터를 실제 배달 경로로 보내지 않는다.

## Exceptions

현재 승인된 예외는 없다. 공개 배달, 데이터 보존 또는 인증 경계 변경은 소유자와 작업 기록을 통해 관리한다.

## Verification

```bash
docker compose --env-file .env.example --profile mail-server config --services
bash scripts/hardening/check-all-hardening.sh 10-communication
```

DNS·TLS·인증·host 포트·복구 증거는 실제 운영 시험에서 별도 수집한다. 정적 구성 통과는 송수신 readiness를 의미하지 않는다.

## Review Cadence

분기별 및 DNS, 인증서, 메일 서버 이미지·저장소·포트 변경 시 검토한다.

## Traceability

- Declared parent: [Communication Tier Architecture Description](../../../../02.architecture/descriptions/0010-communication-architecture.md) (`AD-0010`)
- Subject peers: [Guide](guide.md) (`GDE-0070`), [Runbook](runbook.md) (`RUN-0070`)

## Related Documents

- [Stalwart Compose](../../../../../infra/10-communication/stalwart/docker-compose.yml): 서비스·profile·포트·데이터 선언 원본.
- [Curated version projection](../../../../../infra/tech-stack.versions.json): 선언 drift 확인.
- [Mailpit 개발 트랩 가이드](../0084-mailpit/guide.md), [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md).
- [Stalwart 공식 Docker 설치 문서](https://stalw.art/docs/install/platform/docker/).
- [Mailpit 공식 기능 문서](https://mailpit.axllent.org/docs/).
