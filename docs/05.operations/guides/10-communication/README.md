<!-- [ID:docs:08:communication:root] -->
# 🔐 Communication Operations Policies

> 이 폴더는 메일 인프라 및 통신 자산의 운영 정책과 거버넌스를 관리합니다.

## Overview

`10-communication` 티어의 가용성, 보안, 데이터 무결성을 보장하기 위한 정책 기준을 수립합니다.

## Audience

이 README의 주요 독자:

- Operators
- Security Officers
- AI Agents

## Scope

### In Scope

- **Operations Policy**: [Mail Operations Policy](./mail.md)
- **Security Standards**: SPF/DKIM/DMARC 설정 및 인증 정책.

### Out of Scope

- **Standard Usage**: 가용 가이드는 [05.operations](./README.md)에서 관리합니다.
- **Step-by-step Procedures**: 실행 지침은 [05.operations](./README.md)에서 관리합니다.

## Structure

```text
10-communication/
├── mail.md            # [Operations Policy] Mail Infrastructure Security & Governance
└── README.md          # This file
```

## How to Work in This Area

1. 새로운 운영 정책 수립 시 [operation.template.md](../../../99.templates/operation.template.md)를 사용합니다.
2. 보안 정책 변경 시 반드시 관련 인프라 설정과 함께 갱신되어야 합니다.

## Related References

- **Infra Layer**: [infra/10-communication/mail/](../../../../infra/10-communication/mail/README.md)
- **Usage**: [05.operations/10-communication/mail.md](./mail.md)
- **Procedure**: [05.operations/10-communication/mail.md](./mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.

## Usage

> Migrated from `docs/05.operations/10-communication/README.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:docs:07:communication:root] -->
### 📬 Communication Usages

> 이 폴더는 시스템의 메일 서버 및 통신 인프라 구성에 대한 공식 가이드를 관리합니다.

#### Overview

Stalwart 메일 서버의 운영 설정, 보안 강화 작업, 그리고 MailHog를 활용한 개발 워크플로우에 대한 기술 가이드를 포함합니다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

#### Scope

##### In Scope

- **System Usage**: [Mail Services Usage](./mail.md)
- **Technical Procedures**: SMTP/IMAP 설정 및 관리 가이드.

##### Out of Scope

- **Operations Policy**: 운영 정책은 [05.operations](./README.md)에서 관리합니다.
- **Procedures**: 긴급 대응 절차는 [05.operations](./README.md)에서 관리합니다.

#### Structure

```text
10-communication/
├── mail.md            # [System Usage] Mail Services (Stalwart, MailHog)
└── README.md          # This file
```

#### How to Work in This Area

1. 메일 시스템의 전체적인 이해를 위해 [Mail Services Usage](./mail.md)를 먼저 숙지합니다.
2. 가이드 작성 시 [operation.template.md](../../../99.templates/operation.template.md)를 준수합니다.

#### Related References

- **Infra Layer**: [infra/10-communication/mail/](../../../../infra/10-communication/mail/README.md)
- **Operation**: [05.operations/10-communication/mail.md](./mail.md)
- **Procedure**: [05.operations/10-communication/mail.md](./mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.

## Procedure

> Migrated from `docs/05.operations/10-communication/README.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:docs:09:communication:root] -->
### 🆘 Communication Recovery Procedures

> 이 폴더는 메일 서비스 및 통신 장애 시 즉각적으로 대응하여 서비스를 복구하기 위한 단계별 실행 지침(Procedures)을 관리합니다.

#### Overview

Stalwart 메일 서버의 중단, 메일 수신 불능, SMTP 전송 지연 등 운영 중 발생할 수 있는 주요 장애 시나리오에 대한 복구 절차를 포함합니다.

#### Audience

이 README의 주요 독자:

- Operators
- Incident Responders
- AI Agents

#### Scope

##### In Scope

- **Procedure**: [Mail Recovery Procedure](./mail.md)
- **Troubleshooting**: 서비스 재시작, 로그 분석, 인증서 전파 점검 지침.

##### Out of Scope

- **Standard Usage**: 가용 가이드는 [05.operations](./README.md)에서 관리합니다.
- **Operations Policy**: 운영 정책은 [05.operations](./README.md)에서 관리합니다.

#### Structure

```text
10-communication/
├── mail.md            # [Procedure] Mail Service Recovery (Stalwart, MailHog)
└── README.md          # This file
```

#### How to Work in This Area

1. 장애 발생 시 [Mail Recovery Procedure](./mail.md)의 체크리스트를 즉시 확인합니다.
2. 런북 작성 시 [operation.template.md](../../../99.templates/operation.template.md)를 준수합니다.

#### Related References

- **Infra Layer**: [infra/10-communication/mail/](../../../../infra/10-communication/mail/README.md)
- **Usage**: [05.operations/10-communication/mail.md](./mail.md)
- **Operation**: [05.operations/10-communication/mail.md](./mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.
