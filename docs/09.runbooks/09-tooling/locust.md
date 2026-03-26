<!-- Target: docs/09.runbooks/09-tooling/locust.md -->

# Locust Recovery Runbook

> Locust 로드 테스팅 인프라의 장애 대응 및 복구 절차입니다.

---

## Overview (KR)

이 문서는 Locust 마스터-워커 간의 연결 끊김, InfluxDB 전송 실패 또는 테스트 실행 중 발생하는 연쇄 장애 상황에서의 복구 방법을 안내합니다.

## Target Audience

- Operator
- Performance Engineer
- SRE

## Alerting & Monitoring

- **Connection Failure**: Locust UI 콘솔에 `Worker X disconnected` 메시지 발생 시.
- **Push Failure**: Docker 로그에 `InfluxDB connection timeout` 또는 `Invalid Token` 발생 시.
- **Performance Degradation**: 부하 테스트 수행 중 타 서비스의 응답 지연 시간이 급격히 증가할 때.

## Recovery Procedures

### 1. 즉각 중단 (Emergency Stop)

동작 중인 모든 부하 생성을 중단합니다.

- UI: `Stop` 버튼 클릭.
- CLI: `docker-compose -f infra/09-tooling/locust/docker-compose.yml stop`

### 2. 워커 노드 재동기화 (Worker Resync)

마스터 노드가 재시작된 후 워커가 연결되지 않는 경우:

1. 마스터 상태 확인: `docker compose ps locust-master`
2. 워커 전체 재시공: `docker compose up --force-recreate -d locust-worker`
3. 로그 확인: `docker compose logs -f locust-worker` 에서 마스터 연결 시도 메시지 확인.

### 3. InfluxDB 지표 유실 대응 (Data Link Recovery)

1. InfluxDB 가용성 점검: `mng-db` 또는 InfluxDB 컨테이너 헬스체크 확인.
2. 비밀번호/토큰 유효성 검증: `influxdb_api_token` 시크릿이 최신인지 확인.
3. 데이터 수동 플러시: 테스트 스크립트 내의 Buffer 설정을 조정하여 재시도.

### 4. 테스트 결과 수동 아카이빙 (Manual Archiving)

InfluxDB가 장애일 때 로컬에서 결과를 내려받아야 하는 경우:

- Locust UI의 `Download Data` 메뉴를 사용하여 `Requests`, `Failures`, `Exceptions` CSV를 수동으로 백업함.

## Post-Mortem Tasks

- 로드 테스트 시나리오가 시스템의 병목을 유도한 것인지, 인프라 동적 할당 실패인지 원인 파악.
- 재발 방지를 위한 `locustfile.py` 로직 최적화 및 타임아웃 설정 조정.

## Related Documents

- **Guide**: [Locust Load Testing Guide](../../07.guides/09-tooling/locust.md)
- **Operation**: [Locust Operations Policy](../../08.operations/09-tooling/locust.md)
