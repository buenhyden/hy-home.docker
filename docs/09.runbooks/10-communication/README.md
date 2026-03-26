<!-- [ID:docs:09:communication:root] -->
# 🆘 Communication Recovery Runbooks

> 이 폴더는 메일 서비스 및 통신 장애 시 즉각적으로 대응하여 서비스를 복구하기 위한 단계별 실행 지침(Runbooks)을 관리합니다.

## Overview

Stalwart 메일 서버의 중단, 메일 수신 불능, SMTP 전송 지연 등 운영 중 발생할 수 있는 주요 장애 시나리오에 대한 복구 절차를 포함합니다.

## Audience

이 README의 주요 독자:

- Operators
- Incident Responders
- AI Agents

## Scope

### In Scope

- **Runbook**: [Mail Recovery Runbook](./mail.md)
- **Troubleshooting**: 서비스 재시작, 로그 분석, 인증서 전파 점검 지침.

### Out of Scope

- **Standard Guide**: 가용 가이드는 [07.guides](../07.guides/10-communication/README.md)에서 관리합니다.
- **Operations Policy**: 운영 정책은 [08.operations](../08.operations/10-communication/README.md)에서 관리합니다.

## Structure

```text
10-communication/
├── mail.md            # [Runbook] Mail Service Recovery (Stalwart, MailHog)
└── README.md          # This file
```

## How to Work in This Area

1. 장애 발생 시 [Mail Recovery Runbook](./mail.md)의 체크리스트를 즉시 확인합니다.
2. 런북 작성 시 [runbook.template.md](../../99.templates/runbook.template.md)를 준수합니다.

## Related References

- **Infra Layer**: [infra/10-communication/mail/](../../../infra/10-communication/mail/README.md)
- **Guide**: [07.guides/10-communication/mail.md](../07.guides/10-communication/mail.md)
- **Operation**: [08.operations/10-communication/mail.md](../08.operations/10-communication/mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.
