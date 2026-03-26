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

- **Standard Guide**: 가용 가이드는 [07.guides](../07.guides/10-communication/README.md)에서 관리합니다.
- **Step-by-step Runbooks**: 실행 지침은 [09.runbooks](../09.runbooks/10-communication/README.md)에서 관리합니다.

## Structure

```text
10-communication/
├── mail.md            # [Operations Policy] Mail Infrastructure Security & Governance
└── README.md          # This file
```

## How to Work in This Area

1. 새로운 운영 정책 수립 시 [operation.template.md](../../99.templates/operation.template.md)를 사용합니다.
2. 보안 정책 변경 시 반드시 관련 인프라 설정과 함께 갱신되어야 합니다.

## Related References

- **Infra Layer**: [infra/10-communication/mail/](../../../infra/10-communication/mail/README.md)
- **Guide**: [07.guides/10-communication/mail.md](../07.guides/10-communication/mail.md)
- **Runbook**: [09.runbooks/10-communication/mail.md](../09.runbooks/10-communication/mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.
