<!-- Target: docs/05.operations/guides/10-communication/mail.md -->

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

- **ARD**: [Communication Infrastructure](../../../02.architecture/requirements/0010-communication-architecture.md) (If exists)
- **Usage**: [Mail Services Usage](./mail.md)
- **Procedure**: [Mail Recovery Procedure](./mail.md)

---

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/10-communication/mail.md` during the 2026-05-10 operations taxonomy consolidation.

### Mail Services Usage

> `hy-home.docker` 환경에서 메일 서버(Stalwart) 및 개발용 트랩(MailHog)을 관리하고 사용하는 통합 가이드입니다.

---

#### Overview (KR)

이 문서는 시스템의 메일 인프라 구성과 개발 워크플로우에 대한 가이드를 제공합니다. 실제 메일 서비스 운영을 위한 **Stalwart** 설정과 안전한 개발 테스트를 위한 **MailHog** 사용법을 다룹니다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

이 가이드는 사용자가 메일 서버의 운영 환경을 구성하고, 개발 과정에서 안전하게 이메일 발송 기능을 테스트할 수 있도록 돕는 것을 목적으로 합니다.

#### Prerequisites

- **호스트 포트 점검**: 25, 465, 587, 993 포트가 호스트에서 사용 가능해야 합니다.
- **SSL 인증서**: `secrets/certs` 내에 유효한 도메인 인증서가 존재해야 합니다.
- **관리자 암호**: Docker Secret `stalwart_password`가 사전에 생성되어 있어야 합니다.

#### Step-by-step Instructions

##### 1. Stalwart 운영 서버 설정 (Production)

1. `infra/10-communication/mail` 디렉토리로 이동합니다.
2. 서비스를 시작합니다: `docker-compose --profile communication up -d stalwart`
3. 관리자 UI(`https://mail.${DEFAULT_URL}`)에 접속하여 로그인이 정상적으로 수행되는지 확인합니다.
4. **DNS 연동**: 관리자 UI의 `Settings > Domains` 메뉴에서 제공하는 MX, SPF, DKIM, DMARC 레코드를 DNS 공급자에 등록합니다.

##### 2. MailHog 개발 워크플로우 (Development)

1. 안전한 테스트를 위해 애플리케이션의 SMTP 설정을 다음과 같이 구성합니다:
   - **Host**: `mailhog`
   - **Port**: `1025`
   - **Encryption**: None
2. 하위 앱에서 발송된 모든 메일은 외부로 나가지 않고 `https://mailhog.${DEFAULT_URL}` 웹 UI에서 확인할 수 있습니다.
3. **참고**: MailHog는 데이터를 메모리에 저장하므로 컨테이너 재시작 시 큐가 초기화됩니다.

#### Client Configuration (Stalwart)

| Setting | Value |
| :--- | :--- |
| **IMAP Server** | `mail.${DEFAULT_URL}` |
| **IMAP Port** | `993` (SSL/TLS) |
| **SMTP Server** | `mail.${DEFAULT_URL}` |
| **SMTP Port** | `465` (SSL/TLS) or `587` (STARTTLS) |

#### Common Pitfalls

- **ISP 포트 차단**: 많은 웹 호스팅/ISP는 포트 25(SMTP)를 기본적으로 차단합니다. 발송 실패 시 릴레이 서비스를 검토하거나 ISP에 해제를 요청하십시오.
- **인증서 만료**: `secrets/certs` 내의 인증서가 만료되면 SMTP/IMAP 연결이 실패할 수 있습니다.

#### Related Documents

- **Operation**: [Mail Operations Policy](./mail.md)
- **Procedure**: [Mail Recovery Procedure](./mail.md)

## Procedure

> Migrated from `docs/05.operations/10-communication/mail.md` during the 2026-05-10 operations taxonomy consolidation.

### Mail Recovery Procedure

: Stalwart Mail Server & MailHog

> 메일 서비스 장애 시 즉각적으로 대응하여 서비스를 복구하기 위한 수동 실행 지침입니다.

---

#### Overview (KR)

이 런북은 Stalwart 메일 서버와 MailHog 개발 트랩에 장애가 발생했을 때 운영자가 즉시 따라 할 수 있는 단계별 절차와 검증 기준을 정의합니다.

#### Purpose

메일 서버 서비스 불능(P2), 메일 발송/수신 실패, 인증서 만료 등의 운영 문제를 해결하는 데 목적이 있습니다.

#### Canonical References

- **ARD**: [Communication Infrastructure](../../../02.architecture/requirements/0010-communication-architecture.md) (If exists)
- **Operation**: [Mail Operations Policy](./mail.md)

#### When to Use

- 사용자가 메일을 보내거나 받을 수 없을 때.
- 메일 서버 UI(Stalwart/MailHog)에 접속할 수 없을 때.
- SMTP/IMAP 포트가 응답하지 않을 때.

#### Procedure or Checklist

##### 1. 서비스 상태 확인 Checklist

- [ ] 컨테이너 실행 여부 확인: `docker ps | grep -E 'stalwart|mailhog'`
- [ ] 호스트 네트워크 포트 가용성 확인: `nc -zv localhost 25 465 587 993`
- [ ] 호스트 디스크 여유 공간 확인: `df -h`

##### 2. 일반 장애 복구 Procedure

###### 서비스 불능 시 (Hang or Crash)

1. 메일 서비스 티어 디렉토리로 이동: `cd infra/10-communication/mail`
2. 서비스 상태 확인: `docker-compose ps`
3. 로그 분석: `docker-compose logs -f stalwart` (인증 오류, DB 오류 확인)
4. 재시작 시도: `docker-compose restart stalwart`

###### 메일 발송/수신 실패 시 (Delivery Issues)

1. Stalwart 로그에서 "Delivery Error" 또는 "Spam filter" 관련 키워드를 검색합니다.
2. 외부 DNS 전파 상태 및 SPF/DKIM 유효성을 확인합니다.
3. 인증서 만료 여부를 확인합니다: `ls -l ../../../secrets/certs`

###### MailHog 성능 저하 시

1. MailHog는 인메모리 저장소를 사용하여 큐가 포화될 경우 UI가 느려질 수 있습니다.
2. 서비스를 재시작하여 큐를 비웁니다: `docker-compose restart mailhog`

#### Verification Steps

- [ ] `telnet mail.${DEFAULT_URL} 25` 를 통해 SMTP 배너 응답을 확인합니다.
- [ ] 캡처 UI(`https://mailhog.${DEFAULT_URL}`)에 접속하여 테스트 메일이 들어오는지 확인합니다.

#### Safe Rollback or Recovery Procedure

- [ ] 설정 변경 후 실패 시 Git checkout을 통해 `infra/10-communication/mail` 내의 설정을 이전 상태로 되돌립니다.
- [ ] 주요 서비스 재시작 전 `docker-compose stop`을 권장합니다.

#### Related Operational Documents

- **Incident Record**: `[../05.operations/incidents/]`
- **Postmortem**: `[../../05.operations/incidents/README.md]`

---

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
