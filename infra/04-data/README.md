# Data Tier (04-data)

> Central repository for databases, object storage, and persistence engines.

## Overview

`infra/04-data`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/04-data/
├── analytics/  # 하위 구성 영역
├── cache-and-kv/  # 하위 구성 영역
├── lake-and-object/  # 하위 구성 영역
├── nosql/  # 하위 구성 영역
├── operational/  # 하위 구성 영역
├── relational/  # 하위 구성 영역
├── specialized/  # 하위 구성 영역
└── README.md  # This file
```

## How to Work in This Area

1. 먼저 대상 하위 폴더 README와 `docker-compose*.yml` 또는 설정 파일을 확인한다.
2. 데이터 변경, 백업, 복구, 보존 절차는 대응 operations guide/policy/runbook으로 이동한다.
3. runtime 또는 데이터 파괴 작업은 이 인덱스가 아니라 승인된 runbook 경계를 따른다.
4. secret 값, token, 인증서 원문은 열람하거나 문서에 쓰지 않는다.

## Related Documents

- [infra/README.md](../README.md)
- [docs/05.operations/README.md](../../docs/05.operations/README.md)
