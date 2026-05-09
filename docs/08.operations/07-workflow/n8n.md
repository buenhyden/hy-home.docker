# n8n Operations Policy

: Apache n8n (07-workflow)

---

## Overview (KR)

이 문서는 n8n 서비스의 안정적인 운영을 위한 정책과 통제 항목을 정의한다. 워크플로우 실행 이력 관리, 데이터 백업, 보안 자격 증명 관리 지침을 포함한다.

## Operational Controls

- **Resource Monitoring**: 워커(`n8n-worker`)의 CPU 및 메모리 사용량을 Grafana 알람을 통해 모니터링한다.
- **Data Retention**: 실행 이력(`Execution History`)은 DB 용량 관리를 위해 30일 경과 시 자동 삭제되도록 설정한다 (`EXECUTIONS_DATA_RETENTION_MAX_AGE_HOURS`).
- **Secret Rotation**: 외부 서비스용 `Credentials`는 분기별로 갱신을 권장하며, 변경 시 n8n UI를 통해 즉시 업데이트한다.

## Compliance and Security

- **Encryption**: `N8N_ENCRYPTION_KEY`는 Vault를 통해 관리되며, 유출 시 모든 저장된 자격 증명을 사용할 수 없게 되므로 엄격히 보호한다.
- **Access Control**: 관리자 계정에 대해 강력한 패스워드 정책을 적용하고, 필요한 경우에만 관리자 권한을 부여한다.
- **Workflow Integrity**: 프로덕션 워크플로우를 수정하기 전, 반드시 테스트 환경 또는 로컬에서 검증을 완료해야 한다.

## Maintenance and Updates

### Backup and Restore

- PostgreSQL 메타데이터 DB는 매일 자정에 스냅샷 백업을 수행한다.
- 주요 워크플로우는 `n8n-cli` 또는 UI의 `Export` 기능을 사용하여 주기적으로 JSON 백업을 수행한다.

### Version Upgrades

- n8n 이미지 업데이트 전, 현재 활성화된 워크플로우를 일시 중지하거나 작업이 없는 시간을 확인하여 진행한다.
- 업그레이드 후 `healthz` 엔드포인트를 통해 서비스 정상 여부를 확인한다.

## Exception Handling

- 긴급 장애 복구 상황에서는 `09.runbooks/07-workflow/n8n.md`의 절차를 따른다.
- 인프라 수준의 변경이 필요한 경우 `02-auth` 및 `04-data` 티어 담당자와 협의한다.

## Verification Checklist

- [ ] [ ] `docker compose ps` 상의 모든 서비스가 `healthy` 상태인가?
- [ ] [ ] n8n Web UI에 성공적으로 로그인이 가능한가?
- [ ] [ ] Prometheus 메트릭 엔드포인트(`:5678/metrics`)가 활성 상태인가?

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../README.md)
- [../../07.guides/README.md](../../07.guides/README.md)
- [../../09.runbooks/README.md](../../09.runbooks/README.md)
