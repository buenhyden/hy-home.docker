<!-- Target: docs/03.specs/095-infra-secrets-docs-refresh/README.md -->

# infra-secrets-docs-refresh Specifications

> 인프라 시크릿 및 문서 갱신 사양

## Overview

`docs/03.specs/095-infra-secrets-docs-refresh`는 Docker Secrets 패턴 표준화, 시크릿 마운트 계약, 관련 문서 갱신 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- Documentation Writers
- Security Reviewers
- AI Agents

## Status

이 사양은 P0–P15 기간에 수행된 시크릿·문서 계약 정비 작업의 설계 사양을 보존합니다.

## Scope

### In Scope

- 완료된 infra/secrets/docs refresh 구현 계약 보존
- Docker Secrets, mount boundary, documentation update 기준
- secret-handling 관련 stage 추적성 링크

### Out of Scope

- secret 값, credential, token, 인증서 원문
- 신규 secret rotation 절차 구현
- 실행 계획 또는 작업 evidence 작성

## Structure

```text
infra-secrets-docs-refresh/
├── spec.md      # Infra secrets and docs refresh specification
└── README.md    # This file
```

## How to Work in This Area

1. 새 작업을 시작하기 전에 [spec.md](./spec.md)에서 secret/documentation contract를 확인합니다.
2. secret 경로나 mount 정책 변경은 `secrets/README.md`, `infra/README.md`, 관련 operations 문서를 함께 확인합니다.
3. 민감값은 절대 문서에 쓰지 않고 경로, 정책명, secret reference만 기록합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [secrets/README.md](../../../secrets/README.md)
- [infra/README.md](../../../infra/README.md)
