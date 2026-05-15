# 10-communication Specifications

> 커뮤니케이션 서비스 기술 사양

## Overview

`docs/03.specs/10-communication`는 이메일(Stalwart Mail) 등 커뮤니케이션 서비스의 기술 사양을 포함합니다.

## Scope

### In Scope

- 메일 서버 인터페이스, SMTP/IMAP 경계, 도메인 설정 사양
- 시크릿 주입 및 인증 흐름

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/10-communication/` 담당)

## Structure

```text
10-communication/
├── spec.md      # Communication services technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/10-communication/README.md](../../../infra/10-communication/README.md)
- [docs/05.operations/guides/10-communication/](../../05.operations/guides/10-communication/)
