<!-- README Target: docs/05.operations/policies/04-data/backup/README.md -->

# 04-Data Backup Policies

> 04-data 백업, 보존, 검증 기준을 목적별 하위 폴더에서 관리한다.

## Overview

이 폴더는 `04-data` 계층의 backup policy 문서를 보관한다. 데이터 tier root의 파일/폴더 혼재를 막기 위해 backup 관련 leaf policy는 이 폴더 아래에 둔다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 백업 주기, 보존 기간, 검증 evidence 기준
- backup exception approval and review cadence
- 관련 runbook과 guide index로 이동하기 위한 navigation

### Out of Scope

- 서비스 사용 온보딩
- emergency storage cleanup 절차 본문
- secret 값, credential, token, 인증서 원문

## Structure

```text
backup/
├── backup-policy.md
└── README.md
```

## How to Work in This Area

1. 새 policy leaf는 `docs/99.templates/templates/operations/policy.template.md`를 따른다.
2. policy 변경 시 `../README.md`와 paired runbook/reference link를 함께 갱신한다.
3. backup evidence에는 secret 값을 기록하지 않는다.

## Related Documents

- [04-data policies index](../README.md)
- [Backup policy](./backup-policy.md)
- [Storage exhaustion runbook](../../../runbooks/04-data/storage/storage-exhaustion.md)
