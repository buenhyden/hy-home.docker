<!-- README Target: docs/05.operations/runbooks/04-data/storage/README.md -->

# 04-Data Storage Runbooks

> 04-data storage pressure와 capacity emergency 절차를 목적별 하위 폴더에서 관리한다.

## Overview

이 폴더는 `04-data` 계층의 storage 관련 runbook 문서를 보관한다. storage exhaustion처럼 여러 데이터 서비스에 걸친 emergency procedure는 데이터 tier root에 두지 않고 이 purpose folder 아래에서 관리한다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- storage exhaustion 대응 절차
- capacity evidence capture, cleanup approval, escalation 기준
- backup policy와 incident record로 이동하기 위한 navigation

### Out of Scope

- 서비스 사용 온보딩
- 장기 백업/보존 정책 본문
- secret 값, credential, token, 인증서 원문

## Structure

```text
storage/
├── storage-exhaustion.md
└── README.md
```

## How to Work in This Area

1. 새 runbook leaf는 `docs/99.templates/templates/operations/runbook.template.md`를 따른다.
2. destructive cleanup은 검증된 backup evidence와 owner approval 경계를 문서에 남긴다.
3. 문서 이동이나 제목 변경 시 이 README와 `../README.md`를 함께 갱신한다.

## Related Documents

- [04-data runbooks index](../README.md)
- [Storage exhaustion runbook](./storage-exhaustion.md)
- [Backup policy](../../../policies/04-data/backup/backup-policy.md)
