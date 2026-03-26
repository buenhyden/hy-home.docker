# Airflow Operations Policy

> Airflow 시스템의 안정적 운영을 위한 정책, 통제 기준 및 관리 절차 정의.

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 운영 정책을 정의한다. 시스템의 가용성, 보안, 리소스 관리 및 변경 제어 절차를 규정하여 안정적인 워크플로 실행 환경을 보장한다.

## Policy Scope

- Airflow 코어 컴포넌트 (`scheduler`, `worker`, `webserver` 등) 관리
- 메타데이터 DB 및 브로커(Valkey) 백업 및 복구 정책
- DAG 배포 및 운영 환경 보안 통제

## Applies To

- **Systems**: Apache Airflow v2.10.x, CeleryExecutor
- **Agents**: CI/CD 배포 에이전트, 모니터링 에이전트
- **Environments**: Production ( workflow 티어)

## Controls

- **Required**:
    - 모든 DAG은 `Idempotent`(멱등성)를 유지해야 함.
    - 민감 정보는 반드시 Secret Backend(Docker Secrets/Vault) 및 Airflow Connections를 통해 관리함.
    - `AIRFLOW__CORE__LOAD_EXAMPLES`는 운영 환경에서 반드시 `false`여야 함.
- **Allowed**:
    - 워커 노드의 동적 확장 (부하에 따른 Replica 조정).
    - 읽기 전용 UI 접근 (GUEST 권한).
- **Disallowed**:
    - Scheduler 노드에서의 직접적인 대용량 외부 API 호출 또는 파일 입출력.
    - 사용자 인증(FAB)이 비활성화된 상태에서의 Web UI 노출.

## Exceptions

- **Emergency Hotfix**: 중대한 파이프라인 중단 시, 사후 보고를 조건으로 수동 DB 수정 또는 워커 강제 재시작 가능 (관리자 승인 필요).

## Verification

- **Compliance Check**: `docker compose run --rm airflow-cli config list` 명령을 통해 설정값 준수 여부 확인.
- **Health Check**: Traefik 및 Docker Healthcheck 로그를 통한 실시간 상태 검증.

## Review Cadence

- **Quarterly**: 매 분기별 리소스 사용량 분석 및 쿼터 조정.
- **Per Release**: 새로운 Airflow 버전 또는 Provider 업데이트 시 정책 재검토.

## Related Documents

- **ARD**: [07-workflow Architecture](../../02.ard/07-workflow.md)
- **Runbook**: [Airflow Recovery Runbook](../../09.runbooks/07-workflow/airflow.md)
