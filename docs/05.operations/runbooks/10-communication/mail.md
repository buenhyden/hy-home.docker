---
status: active
---
<!-- Target: docs/05.operations/runbooks/10-communication/mail.md -->

# Mail Runbook

## Overview (KR)

이 런북은 Stalwart 메일 서버와 MailHog 개발 트랩에 장애가 발생했을 때 운영자가 즉시 따라 할 수 있는 단계별 절차와 검증 기준을 정의합니다.

## Mail Recovery Procedure

> Scope: Stalwart Mail Server & MailHog

> 메일 서비스 장애 시 즉각적으로 대응하여 서비스를 복구하기 위한 수동 실행 지침입니다.

---

### Purpose

메일 서버 서비스 불능(P2), 메일 발송/수신 실패, 인증서 만료 등의 운영 문제를 해결하는 데 목적이 있습니다.

### Canonical References

- **ARD**: [Communication Infrastructure](../../../02.architecture/requirements/0010-communication-architecture.md) (If exists)
- **Operation**: [Mail Operations Policy](../../policies/10-communication/mail.md)

## When to Use

- 사용자가 메일을 보내거나 받을 수 없을 때.
- 메일 서버 UI(Stalwart/MailHog)에 접속할 수 없을 때.
- SMTP/IMAP 포트가 응답하지 않을 때.

## Procedure

### 1. 서비스 상태 확인 Checklist

- [ ] 컨테이너 실행 여부 확인: `docker ps | grep -E 'stalwart|mailhog'`
- [ ] 호스트 네트워크 포트 가용성 확인: `nc -zv localhost 25 465 587 993`
- [ ] 호스트 디스크 여유 공간 확인: `df -h`

#### 2. 일반 장애 복구 Procedure

##### 서비스 불능 시 (Hang or Crash)

1. 메일 서비스 티어 디렉토리로 이동: `cd infra/10-communication/mail`
2. 서비스 상태 확인: `docker-compose ps`
3. 로그 분석: `docker-compose logs -f stalwart` (인증 오류, DB 오류 확인)
4. 재시작 시도: `docker-compose restart stalwart`

##### 메일 발송/수신 실패 시 (Delivery Issues)

1. Stalwart 로그에서 "Delivery Error" 또는 "Spam filter" 관련 키워드를 검색합니다.
2. 외부 DNS 전파 상태 및 SPF/DKIM 유효성을 확인합니다.
3. 인증서 만료 여부를 확인합니다: `ls -l ../../../secrets/certs`

##### MailHog 성능 저하 시

1. MailHog는 인메모리 저장소를 사용하여 큐가 포화될 경우 UI가 느려질 수 있습니다.
2. 서비스를 재시작하여 큐를 비웁니다: `docker-compose restart mailhog`

### Verification Steps

- [ ] `telnet mail.${DEFAULT_URL} 25` 를 통해 SMTP 배너 응답을 확인합니다.
- [ ] 캡처 UI(`https://mailhog.${DEFAULT_URL}`)에 접속하여 테스트 메일이 들어오는지 확인합니다.

### Safe Rollback or Recovery Procedure

- [ ] 설정 변경 후 실패 시 Git checkout을 통해 `infra/10-communication/mail` 내의 설정을 이전 상태로 되돌립니다.
- [ ] 주요 서비스 재시작 전 `docker-compose stop`을 권장합니다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/10-communication/mail.md)
- [Operations policy](../../policies/10-communication/mail.md)
