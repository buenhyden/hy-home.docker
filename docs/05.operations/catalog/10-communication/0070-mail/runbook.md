---
title: "Stalwart Mail Recovery Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0070"
parent_ids:
- "GDE-0070"
created: "2026-05-17"
---

# Stalwart Mail Recovery Runbook

## Overview

`mail-server` profile의 Stalwart 실제 메일 서비스 장애를 진단하는 절차다. 개발 트랩은 [Mailpit 런북](../0084-mailpit/runbook.md)이 소유한다.

## When to Use

Stalwart 관리 UI, SMTP/Submission/SMTPS, IMAPS 또는 외부 배달이 실패하거나 정적 검증이 실패할 때 사용한다.

## Procedure

1. 저장소 루트에서 정적 선언을 확인한다.

   ```bash
   docker compose --env-file .env.example --profile mail-server config --services
   bash scripts/hardening/check-all-hardening.sh 10-communication
   ```

2. 실제 서비스가 선택·기동된 운영 환경이면 `docker compose --profile mail-server ps stalwart`로 상태를 확인한다.
3. 최근 DNS, 인증서 참조, host 포트, Compose, secret 참조 변경을 식별한다. 메일 내용, 패스워드 또는 private key를 열어 수집하지 않는다.
4. 관리 UI 문제는 `mail.${DEFAULT_URL}`의 Traefik/SSO 경로를 확인한다. SMTP/IMAP 문제는 Compose의 게시 포트와 프로토콜 TLS·인증을 따로 확인한다.
5. 외부 배달 실패는 DNS(MX/SPF/DKIM/DMARC), 송수신 정책과 ISP의 SMTP 제한을 확인한다. 승인된 테스트 수신자만 사용한다.
6. 로그가 필요하면 운영자가 `docker compose --profile mail-server logs --tail=100 stalwart`를 제한된 환경에서 검토하고 메일 주소·내용·비밀을 제거한 요약만 공유한다.

## Evidence

실행 명령·시간·종료 상태, profile, 서비스 상태, 공개 구성 변경, DNS/TLS/port 시험 요약과 실패 범위를 기록한다. 컨테이너 TCP healthcheck와 실제 배달 결과는 구분한다.

## Rollback or Recovery

확인된 공개 구성 변경만 영향 범위와 이전 검증 결과에 따라 복구한다. 재시작이 승인되면 `docker compose --profile mail-server restart stalwart`로 단일 서비스만 대상으로 한다. 메일함 데이터 복원·서버 downgrade·DNS rollback은 검증된 별도 계획이 필요하며 현재 문서는 성공을 보장하지 않는다. 볼륨 삭제 및 개발 트랩의 큐 초기화는 이 절차에 포함하지 않는다.

## Escalation

메일 손실, 실제 배달 변경, DNS/방화벽 변경, 자격 증명 회전, 저장소 복원 또는 원인이 확인되지 않은 TLS 오류는 운영 책임자에게 인계한다. 마지막 성공 상태, 영향 도메인, 실패 증거와 복구 선택지를 포함한다.

## Traceability

- Declared parent: [Mail Usage Guide](guide.md) (`GDE-0070`)
- Governing authority: [Communication Tier Architecture Description](../../../../02.architecture/descriptions/0010-communication-architecture.md) (`AD-0010`)
- Subject peers: [Guide](guide.md) (`GDE-0070`), [Policy](policy.md) (`POL-0070`)

## Related Documents

- [Stalwart Compose](../../../../../infra/10-communication/stalwart/docker-compose.yml): 서비스·profile·포트·데이터 선언 원본.
- [Curated version projection](../../../../../infra/tech-stack.versions.json): 선언 drift 확인.
- [Mailpit 개발 트랩 가이드](../0084-mailpit/guide.md), [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md).
- [Stalwart 공식 Docker 설치 문서](https://stalw.art/docs/install/platform/docker/).
- [Mailpit 공식 기능 문서](https://mailpit.axllent.org/docs/).
