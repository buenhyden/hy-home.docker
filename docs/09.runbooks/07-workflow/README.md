# Workflow Runbook (07-workflow)

> Workflow Failure Recovery & Orchestrator Troubleshooting

## Overview

이 런북은 `07-workflow` 계층(Airflow, n8n)의 장애 상황에 대한 즉각적인 조치 방법을 설명한다.

## Emergency Procedures

### 1. Airflow 스케줄러 먹통 (Stalled Scheduler)

DAG가 실행되지 않고 'Scheduled' 상태에 머물러 있는 경우.

1. **로그 확인**: `docker logs airflow-scheduler`를 통해 DB 연결 오류나 교착 상태 식별.
2. **프로세스 재시작**: 스케줄러 컨테이너를 재시작하여 메타데이터 파싱 재유도.
3. **DB 상태 확인**: PostgreSQL의 락(Lock) 상태를 점검하고 장시간 지속되는 트랜잭션 종료.

### 2. Celery Worker 연결 오류

워커가 태스크를 가져가지 못하거나 'Lost' 상태인 경우.

1. **Broker 확인**: `valkey-workflow` 서비스의 연결 가능 여부 및 메모리 부족 여부 확인.
2. **Worker 재기동**: Flower (`https://flower.${DEFAULT_URL}`)에서 워커 상태를 확인하고 필요시 강제 재시작.
3. **Queue 정화**: 브로커에 잘못된 메시지가 쌓인 경우 큐를 비우고 재시도 (데이터 유실 주의).

### 3. n8n 워크플로우 중단

특정 자동화 작업이 멈추거나 동작하지 않는 경우.

1. **Execution Log 확인**: n8n 내부의 실행 로그에서 실패한 노드와 에러 메시지 확인.
2. **트레이시 확인**: `06-observability` (Loki/Tempo)를 통해 연동된 외부 API와의 통신 에러 정보 수집.

---

## Verification Steps

- [ ] `airflow db check` 명령을 통한 메타데이터 DB 연결 확인.
- [ ] n8n `/healthz` 엔드포인트 응답 확인.

## Related Operational Documents

- [Operations Policy](../../docs/08.operations/07-workflow/README.md)
- [DAG Development Guide](../../docs/07.guides/07-workflow/01.airflow-dag-dev.md)
