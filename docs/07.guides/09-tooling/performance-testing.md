<!-- Target: docs/07.guides/09-tooling/performance-testing.md -->

# Performance Testing Guide

> `hy-home.docker` 환경에서 Locust를 활용한 분산 부하 테스트 및 성능 벤치마킹 통합 가이드입니다.

---

## Overview (KR)

이 문서는 플랫폼의 엔드포인트를 벤치마킹하고 성능 병목 지점을 식별하기 위한 성능 테스트 워크플로우를 설명합니다. **Locust**(Python 기반)를 사용하여 시나리오를 작성하고, **InfluxDB**와 **Grafana**를 연동하여 지표를 분석하는 방법을 다룹니다.

## Guide Type

`system-guide | troubleshooting-guide`

## Target Audience

- Developer
- Operator
- Performance Engineer

## Purpose

이 가이드는 사용자가 초당 수천 명의 가상 사용자를 시뮬레이션하여 시스템의 임계치를 확인하고, 인프라 최적화의 근거 데이터를 확보할 수 있도록 돕는 것을 목적으로 합니다.

## Prerequisites

- **Python 지식**: 테스트 시나리오 작성을 위한 기초적인 Python 문법 이해.
- **네트워크 연결**: 테스트 대상 서비스가 `infra_net` 내에서 `locust-master/worker`와 통신 가능해야 함.
- **InfluxDB**: 지표 저장을 위해 InfluxDB 서비스가 실행 중이어야 함.

## Step-by-step Instructions

### 1. 테스트 시나리오 작성 (Scripting)

성능 테스트 시나리오는 `locustfile.py`에 정의합니다.

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5) # 초 단위 대기 시간

    @task
    def index_page(self):
        self.client.get("/")
```

### 2. 분산 환경 실행 (Orchestration)

1. `infra/09-tooling/k6` 디렉토리로 이동합니다.
2. 서비스를 시작합니다: `docker-compose --profile tooling up -d`
3. 부하량에 따라 워커를 확장합니다: `docker-compose up --scale locust-worker=5 -d`

### 3. 부하 가동 및 모니터링 (Execution)

1. `https://locust.${DEFAULT_URL}` 웹 UI에 접속합니다.
2. **Number of users**(가상 사용자 수)와 **Ramp-up**(초당 증가 수)를 설정하고 `Start swarming`을 클릭합니다.
3. 실시간 통계 및 차트를 확인합니다.

### 4. 결과 분석 (Analysis)
- Locust UI에서 실시간 데이터를 확인하거나, 
- **Grafana**의 `Load Testing Dashboard`를 통해 InfluxDB에 저장된 이력 데이터를 심도 있게 분석합니다.

## Common Pitfalls

- **Ramp-up 설정 미흡**: 순간적인 대량 요청은 운영 시스템에 서지(Surge)를 발생시켜 의도치 않은 장애를 유발할 수 있습니다. 반드시 서서히 부하를 늘리십시오.
- **Worker 연결 실패**: 마스터 컨테이너 명칭(`locust-master`) 및 Docker 네트워크 가시성을 확인하십시오.
- **마스터 노드 과부하**: 마스터 노드는 데이터 수집 역할만 수행하도록 하고, 실제 부하 발생은 전적으로 워커 노드에서 담당해야 합니다.

## Related Documents

- **Operation**: [Performance Testing Operations Policy](../../08.operations/09-tooling/performance-testing.md)
- **Runbook**: [Performance Testing Recovery Runbook](../../09.runbooks/09-tooling/performance-testing.md)
