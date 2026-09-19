---
title: "Stalwart Mail Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0070"
parent_ids:
- "POL-0070"
created: "2026-05-10"
---

# Stalwart Mail Usage Guide

## Usage

### Overview

`0070-mail`은 선택형 실제 메일 서버 Stalwart를 소유한다. `mail-server` profile로만 선택하며 HOME 또는 DEV의 기본 SMTP 목적지가 아니다. 개발용 캡처는 별도 [Mailpit subject 0084](../0084-mailpit/guide.md)가 소유한다.

### Prerequisites

저장소 루트에서 실행한다. 실제 송수신을 시작하기 전에 도메인 DNS(MX/SPF/DKIM/DMARC), TLS 인증서, host 포트, `stalwart_password` 참조, 데이터 백업·복구 계획을 확인한다. 개인 메일함·비밀·인증서 원문은 검증 자료로 읽지 않는다.

### Step-by-step Instructions

1. 루트 include와 profile 선택을 정적으로 확인한다.

   ```bash
   docker compose --env-file .env.example --profile mail-server config --services
   bash scripts/hardening/check-all-hardening.sh 10-communication
   ```

2. [Stalwart Compose](../../../../../infra/10-communication/stalwart/docker-compose.yml)의 host-port 변수와 `${DEFAULT_COMMUNICATION_DIR}/stalwart/data` 영속 경로를 확인한다. 관리 UI는 `https://mail.${DEFAULT_URL}`이며 Traefik SSO 체인을 사용한다.
3. 운영 전환을 승인받은 환경에서 SMTP Submission 또는 SMTPS와 IMAPS의 TLS·인증을 검증한다. Compose는 SMTP, Submission, SMTPS, IMAPS, ManageSieve 포트를 호스트에 게시하므로 관리 UI SSO가 메일 프로토콜 인증을 대신하지 않는다.
4. 실행 중인 서비스 상태 점검은 `docker compose --profile mail-server ps stalwart`로 시작한다. SMTP TCP healthcheck만으로 외부 배달, DNS 또는 TLS 성공을 주장하지 않는다.
5. 애플리케이션 개발 테스트는 [Mailpit 가이드](../0084-mailpit/guide.md)의 내부 `mailpit` SMTP 또는 loopback 바인딩을 사용한다. Stalwart를 개발 트랩으로 사용하지 않는다.

## Common Checks

- 루트 profile 구성과 communication 하드닝 검증 통과.
- 실제 운영 readiness는 DNS, TLS, 인증, 승인된 송수신 시험, 복원 검증을 별도로 기록.
- 이미지 버전은 Compose를 참조하며 문서에 현재 pin을 복제하지 않는다.

## Runbook Handoff

UI·SMTP·IMAP 연결 실패나 배달 문제가 발생하면 [Stalwart 런북](runbook.md)을 따른다. 개발 캡처 실패는 [Mailpit 런북](../0084-mailpit/runbook.md)으로 인계한다.

## Traceability

- Declared parent: [Mail Operations Policy](policy.md) (`POL-0070`)
- Governing authority: [Communication Tier Architecture Description](../../../../02.architecture/descriptions/0010-communication-architecture.md) (`AD-0010`)
- Subject peers: [Policy](policy.md) (`POL-0070`), [Runbook](runbook.md) (`RUN-0070`)

## Related Documents

- [Stalwart Compose](../../../../../infra/10-communication/stalwart/docker-compose.yml): 서비스·profile·포트·데이터 선언 원본.
- [Curated version projection](../../../../../infra/tech-stack.versions.json): 선언 drift 확인.
- [Mailpit 개발 트랩 가이드](../0084-mailpit/guide.md), [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md).
- [Stalwart 공식 Docker 설치 문서](https://stalw.art/docs/install/platform/docker/).
- [Mailpit 공식 기능 문서](https://mailpit.axllent.org/docs/).
