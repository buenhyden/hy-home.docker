# Data Operations Policy (04-data)

> Persistence, Backup, and Security (04-data) 운영 정책

## Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)의 운영 표준 및 데이터 보호 요구 사항을 정의합니다. 모든 서비스의 지속성, 가용성 및 보안을 보장하는 것이 목적입니다.

## Audience

이 README의 주요 독자:

- 운영 정책을 수립하는 **Operators**
- 보안 통제를 적용하는 **Security Engineers**
- 정책 준수 여부를 확인하는 **AI Agents**

## Scope

### In Scope

- 데이터 저장 표준 및 볼륨 격리 정책
- 백업 전략 및 보관 기간
- 보안 및 규정 준수 통제

## Structure

```text
04-data/
├── cache-and-kv/         # 분산 캐시 및 KV 저장소 운영 정책
├── lake-and-object/       # 데이터 레이크 및 오브젝트 스토리지 운영 정책
├── nosql/                 # NoSQL 데이터베이스 운영 정책
├── operational/           # 운영 및 관리용 데이터베이스 운영 정책
├── backup-policy.md       # 공통 백업 표준
├── relational/            # 관계형 데이터베이스 운영 정책
└── README.md              # This file
```

## How to Work in This Area

1. 전역 시스템 운영 원칙은 [Operations](../../08.operations/README.md) 메인 페이지를 참조합니다.
2. 각 데이터 서비스별 개별 정책은 이 디렉터리의 개별 문서를 따릅니다.
3. 정책 변경 시 아키텍처 팀의 승인이 필요합니다.
4. 관계형 데이터베이스 정책은 [Relational Operation](./relational.md)을 참조합니다.

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/README.md)
- **Runbooks**: [Recovery Runbooks](../../09.runbooks/04-data/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
