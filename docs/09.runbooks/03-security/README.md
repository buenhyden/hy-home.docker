# 03-security Runbooks

> Incident response and maintenance runbooks for the security tier.

---

## Overview (KR)

이 디렉토리는 보안 계층(Vault 등)의 장애 대응 및 정기 유지보수를 위한 실행 지침서를 포함한다.

## Structure

```text
03-security/
├── vault.md    # Vault Runbook (Seal Recovery, Raft Maintenance)
└── README.md   # This file
```

## Available Runbooks

- **[Vault Runbook](vault.md)**: 예기치 않은 봉인 해제 절차, Raft 클러스터 복구, 그리고 스냅샷 백업 방법.

## AI Agent Guidance

1. **Urgency**: `Sealed: true` 상태 감지 시 즉시 이 런북의 봉인 해제 섹션을 가이드하시오.
2. **Safety**: 스냅샷 복구(Restore) 작업은 데이터 유실 위험이 크므로 반드시 수동 확인 절차를 거치시오.
