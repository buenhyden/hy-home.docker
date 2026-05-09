<!-- Target: docs/08.operations/10-communication/mail.md -->

# Mail Operations Policy

> 메일 인프라(Stalwart, MailHog)의 안정성과 보안을 유지하기 위한 운영 정책입니다.

---

## Overview (KR)

이 문서는 `10-communication` 티어의 메일 서비스 운영 정책을 정의합니다. 시스템 가용성, 데이터 보존, 보안 통제 기준 및 검증 방법을 포함합니다.

## Policy Scope

메일 서버(Stalwart)의 보안 설정, 계정 관리, 데이터 백업 및 개발용 트랩(MailHog)의 운영 범위를 규정합니다.

## Applies To

- **Systems**: Stalwart, MailHog
- **Agents**: Kubernetes/Docker Operator
- **Environments**: Production (Stalwart), Development (MailHog)

## Controls

- **Required**:
  - 모든 발신 도메인에 대해 SPF, DKIM, DMARC 레코드를 DNS에 유지해야 함.
  - SMTP Submission(587) 및 IMAPS(993) 연결은 반드시 TLS 암호화를 사용해야 함.
  - 관리자 패스워드는 Docker Secrets를 통해 관리해야 함.
- **Allowed**:
  - 개발 환경에서의 MailHog를 통한 자유로운 메일 캡처 및 테스트.
- **Disallowed**:
  - 인증되지 않은 릴레이(Open Relay) 설정은 엄격히 금지됨.

## Persistence & Backups

- **Data Retention**: Stalwart의 메일 데이터는 `${DEFAULT_COMMUNICATION_DIR}` 볼륨에 영구 보존됩니다.
- **Backup Schedule**: `stalwart-data` 볼륨에 대한 주간 스냅샷 백업이 의무 사항입니다.
- **MailHog Data**: MailHog는 인메모리 저장소를 사용하므로 별도의 데이터 보존 정책을 두지 않습니다.

## Verification

- **Compliance Check**: 주기적인 SPF/DKIM 테스트 및 릴레이 점검 도구를 사용하여 보안 상태를 확인합니다.

## Review Cadence

- Quarterly (분기별 보안 및 운영 정책 검토)

## Related Documents

- **ARD**: [Communication Infrastructure](../../02.ard/0010-communication-architecture.md) (If exists)
- **Guide**: [Mail Services Guide](../../07.guides/10-communication/mail.md)
- **Runbook**: [Mail Recovery Runbook](../../09.runbooks/10-communication/mail.md)

---

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
