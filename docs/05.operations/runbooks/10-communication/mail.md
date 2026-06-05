---
status: active
---
<!-- Target: docs/05.operations/runbooks/10-communication/mail.md -->

# Mail Recovery Runbook

## Mail Recovery Procedure

> Scope: Stalwart and MailHog static/runtime recovery for the optional `10-communication` mail compose.

### Overview

이 런북은 Stalwart 메일 서버와 MailHog 개발 트랩의 검증 실패, UI 접근 실패, SMTP/IMAP 연결 실패가 발생했을 때 운영자가 증거를 보존하고 안전하게 복구 또는 에스컬레이션하기 위한 절차를 정의한다.

### Purpose

메일 서비스 장애 원인을 확인하되, secret 노출, 데이터 삭제, 검증되지 않은 rollback 명령을 피하고 현재 root optional compose 경계에 맞는 evidence를 남긴다.

### Canonical References

- **Spec**: [Communication tier spec](../../../03.specs/10-communication/spec.md)
- **Policy**: [Mail operations policy](../../policies/10-communication/mail.md)
- **Guide**: [Mail usage guide](../../guides/10-communication/mail.md)

## When to Use

- `bash scripts/hardening/check-all-hardening.sh 10-communication`이 실패할 때.
- Stalwart Admin/JMAP UI(`mail.${DEFAULT_URL}`) 또는 MailHog UI(`mailhog.${DEFAULT_URL}`)가 응답하지 않을 때.
- 운영 승격 후 SMTP/Submission/SMTPS/IMAPS 포트가 응답하지 않을 때.
- MailHog가 개발 테스트 메일을 캡처하지 않을 때.

## Procedure

### Checklist

- [ ] root mail include가 optional/commented인지 또는 운영 승격으로 활성화됐는지 기록한다.
- [ ] 최근 compose, `.env*`, secret reference, DNS, 인증서 변경 내역을 기록한다.
- [ ] secret 값 원문은 열람하거나 로그에 남기지 않는다.

### Steps

1. static baseline을 확인한다: `bash scripts/hardening/check-all-hardening.sh 10-communication`.
2. repo stale guard를 확인한다: `bash scripts/validation/check-repo-contracts.sh`.
3. 컨테이너가 실행 중이면 상태를 기록한다: `docker ps --format '{{.Names}}\t{{.Status}}'`.
4. 실행 중인 컨테이너 로그를 확인한다: `docker logs --tail 100 stalwart`, `docker logs --tail 100 mailhog`.
5. 운영 승격 상태에서만 host port를 확인한다: `nc -zv localhost 25 465 587 993 4190`.
6. MailHog 캡처 실패는 애플리케이션 SMTP host가 `mailhog`, port가 `1025`인지 확인한다.
7. Stalwart 외부 전송 실패는 DNS(MX/SPF/DKIM/DMARC), 인증서, ISP/hosting provider의 port 25 정책 evidence를 확인한다.

### Verification Steps

- `bash scripts/hardening/check-all-hardening.sh 10-communication`
- `bash scripts/validation/check-repo-contracts.sh`
- 운영 승격 시 UI route, TLS, DNS, host port evidence가 incident/task 기록에 남아 있어야 한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 100 stalwart`, `docker logs --tail 100 mailhog`
- **Static config**: [mail compose](../../../../infra/10-communication/mail/docker-compose.yml), [infra_net spec](../../../03.specs/standardize-infra-net/spec.md)
- **Runtime signals**: container status, host port probe output, Traefik route response, DNS/TLS probe output

### Safe Rollback or Recovery Procedure

1. static config drift는 current branch에서 compose/doc diff를 되돌리기 전에 변경 원인과 검증 실패를 기록한다.
2. 운영 승격 후 재시작이 필요하면 사전 승인과 영향 범위를 기록한 뒤 Stalwart 또는 MailHog 단위로만 수행한다.
3. MailHog queue 초기화는 개발 캡처 데이터 손실을 의미하므로 관련 개발자에게 알린 뒤 승인된 경우에만 재시작한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: secret exposure risk가 있으면 secret 파일 열람과 로그 공유를 중단한다.
- **Eval Re-run**: hardening, repo contracts, documentation alignment checks를 재실행한다.

## Evidence

- 실행한 명령, 성공/실패 요약, 컨테이너 상태, 관련 로그 tail, DNS/TLS/port probe 결과를 task 또는 incident evidence에 기록한다.
- secret 값, private key, 인증서 원문은 evidence에 포함하지 않는다.

## Rollback or Recovery

N/A — no verified broad rollback or data restore procedure is documented yet. Static config correction, approved service restart, and MailHog development queue reset만 이 runbook의 검증된 복구 범위다.

## Escalation

verification이 실패하거나, 데이터 삭제/복구, production mail delivery 변경, DNS 변경, secret rotation, host firewall 변경이 필요하면 owning operator에게 에스컬레이션한다. 에스컬레이션에는 captured evidence, 최근 변경 내역, optional include 활성화 여부, 현재 rollback/recovery 상태를 포함한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/10-communication/mail.md)
- [Operations policy](../../policies/10-communication/mail.md)
