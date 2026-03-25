# Workflow Operations Policy (07-workflow)

> Scaling Standards, Metadata Cleanup & Task Governance

## Overview

이 정책은 `hy-home.docker` 워크플로우 계층(07-workflow)의 운영 탄력성과 메타데이터 관리 기준을 정의한다.

## Scaling Policy

- **Airflow Workers**: CPU 부하가 지속적으로 80%를 초과하거나 큐 대기 시간이 5분을 넘길 경우 워커 노드를 점진적으로 증설(Scale-out)한다.
- **Valkey Broker**: 워크로드 증가에 따라 전용 Valkey 인스턴스의 메모리 할당량을 조정한다.

## Data & Metadata Governance

### 1. 작업 이력 관리 (History Retention)

- **Airflow Log Cleanup**: 30일이 지난 태스크 실행 로그는 메타데이터 DB에서 삭제하거나 콜드 스토리지로 보관한다.
- **n8n Execution History**: 데이터 팽창 방지를 위해 14일 초과된 실행 기록은 자동 삭제하도록 설정 권장.

### 2. 자원 할당 정책

- 각 워커 노드는 컨테이너당 최대 메모리 사용량을 제한하여 인접 서비스에 영향을 주지 않도록 한다.
- 동시 실행 작업(Parallelism) 수는 메타데이터 DB의 커넥션 풀 크기에 맞춰 설정한다.

## Maintenance Checklist

- [ ] 워커 노드 가동률 및 큐 적체 상태 주기적 점검.
- [ ] 메타데이터 DB(PostgreSQL) 인덱스 최적화 및 크기 모니터링.
- [ ] Valkey 브로커의 Persistent 모드 작동 여부 확인.

## Related Documents

- [07. Guides](../../docs/07.guides/07-workflow/README.md)
- [09. Runbooks](../../docs/09.runbooks/07-workflow/README.md)
