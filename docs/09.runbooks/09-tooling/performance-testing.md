<!-- Target: docs/09.runbooks/09-tooling/performance-testing.md -->

# Performance Testing Recovery Runbook

> Locust 부하 테스트 인프라 장애 시 대응 및 복구 절차를 정의합니다.

---

## Overview (KR)

이 문서는 Locust 마스터/워커 노드의 연결 끊김, InfluxDB 지표 수집 장애 또는 성능 테스트로 인한 타 서비스 과부하 발생 시의 긴급 조치 방법을 안내합니다.

## Target Audience

- Operator
- Performance Engineer
- SRE

## Alerting & Monitoring

- **Locust UI Error**: 웹 인터페이스에서 `Worker disconnected` 경고 발생 시.
- **Metric Loss**: InfluxDB로의 데이터 전송 실패가 Locust 콘솔에 출력될 때.
- **Target Down**: 부하 테스트 시작 후 대상 서비스의 가용성 지표(SLI)가 급격히 하락할 때.

## Recovery Procedures

### 1. 테스트 강제 중단 (Emergency Stop)
가장 우선적으로 부하 생성을 즉시 중단합니다.
- **Locust UI**: UI에서 `Stop` 버튼을 클릭합니다.
- **CLI**: `docker-compose -f infra/09-tooling/k6/docker-compose.yml stop` 명령을 실행합니다.

### 2. 마스터-워커 연결 복구 (Master-Worker Sync)
워커 노드가 마스터를 찾지 못하는 경우:
1. 마스터 활성 상태 확인: `docker-compose ps locust-master`
2. 환경 변수 확인: 워커의 `LOCUST_MASTER_NODE_HOST`가 올바른지 확인합니다.
3. 서비스 재시작: `docker-compose restart locust-master locust-worker`

### 3. InfluxDB 데이터 전송 오류 (Data Link Recovery)
1. InfluxDB 서비스 상태 확인: `docker-compose ps influxdb`
2. 네트워크 가시성 확인: `docker-compose exec locust-master ping influxdb`
3. Locust 설정 확인: `locustfile.py` 내의 InfluxDB 엔드포인트 설정을 점검합니다.

### 4. 타 서비스 영향 복구 (Cascading Failure Clean-up)
부하 테스트로 인해 다른 서비스가 마비된 경우:
- Gateway 캐시를 플러시하거나 서비스를 재시작하여 정상 상태로 돌려놓습니다.
- 테스트 결과 데이터를 분석하여 어느 지점에서 연쇄 장애가 시작되었는지 파악합니다.

## Post-Mortem Tasks

- 장애 원인이 테스트 시나리오 설계 오류인지, 인프라 용량 부족인지 분석하여 보고서를 작성합니다.
- 재발 방지를 위해 테스트 스케일링 정책을 조정합니다.

## Related Documents

- **Guide**: [Performance Testing Guide](../07.guides/09-tooling/performance-testing.md)
- **Operation**: [Performance Testing Operations Policy](../08.operations/09-tooling/performance-testing.md)
