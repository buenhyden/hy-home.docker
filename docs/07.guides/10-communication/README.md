<!-- [ID:docs:07:communication:root] -->
# 📬 Communication Guides

> 이 폴더는 시스템의 메일 서버 및 통신 인프라 구성에 대한 공식 가이드를 관리합니다.

## Overview

Stalwart 메일 서버의 운영 설정, 보안 강화 작업, 그리고 MailHog를 활용한 개발 워크플로우에 대한 기술 가이드를 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- **System Guide**: [Mail Services Guide](./mail.md)
- **Technical Procedures**: SMTP/IMAP 설정 및 관리 가이드.

### Out of Scope

- **Operations Policy**: 운영 정책은 [08.operations](../08.operations/10-communication/README.md)에서 관리합니다.
- **Runbooks**: 긴급 대응 절차는 [09.runbooks](../09.runbooks/10-communication/README.md)에서 관리합니다.

## Structure

```text
10-communication/
├── mail.md            # [System Guide] Mail Services (Stalwart, MailHog)
└── README.md          # This file
```

## How to Work in This Area

1. 메일 시스템의 전체적인 이해를 위해 [Mail Services Guide](./mail.md)를 먼저 숙지합니다.
2. 가이드 작성 시 [guide.template.md](../../99.templates/guide.template.md)를 준수합니다.

## Related References

- **Infra Layer**: [infra/10-communication/mail/](../../../infra/10-communication/mail/README.md)
- **Operation**: [08.operations/10-communication/mail.md](../08.operations/10-communication/mail.md)
- **Runbook**: [09.runbooks/10-communication/mail.md](../09.runbooks/10-communication/mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.
