<!-- Target: docs/07.guides/09-tooling/locust.md -->

# Locust Load Testing Guide

> `hy-home.docker` 환경에서 Locust를 사용한 부하 테스트 시나리오 작성 및 실행 가이드입니다.

---

## Overview (KR)

이 문서는 Locust를 사용하여 플랫폼의 서비스를 벤치마킹하는 방법을 설명합니다. 특히, `influxdb-client`를 통한 성능 지표의 영구 저장 및 분산 워커 노드 환경 구성에 초점을 맞춥니다.

## Guide Type

`system-guide | troubleshooting-guide`

## Target Audience

- QA Engineer
- Performance Engineer
- SRE

## Purpose

플랫폼 서비스의 가용성 임계치를 식별하고, 인프라 증설 또는 성능 최적화의 정량적 근거를 확보하기 위한 로드 테스팅 절차를 안내합니다.

## Prerequisites

- **Python 지식**: 테스트 시나리오 작성을 위한 기초적인 Python 문법 이해.
- **네트워크 연결**: `infra_net` 내에서 `locust-master`와 `influxdb` 간의 가시성 확보.
- **Secrets**: InfluxDB 전송을 위한 API 토큰이 `secrets/influxdb_api_token`에 준비되어 있어야 함.

## Step-by-step Instructions

### 1. 테스트 시나리오 작성 (Scripting)
`locustfile.py` 파일을 생성하고 테스트 로직을 정의합니다.
```python
from locust import HttpUser, task, between

class BenchmarkUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_endpoint(self):
        self.client.get("/api/v1/health")
```

### 2. 인프라 실행 (Deployment)
1. `infra/09-tooling/locust` 디렉토리로 이동합니다.
2. 서비스 시작: `docker-compose --profile tooling up -d`
3. 워커 확장 (최대 부하 시): `docker compose up --scale locust-worker=5 -d`

### 3. 테스트 실행 및 UI 관리 (Execution)
1. 브라우저에서 `https://locust.${DEFAULT_URL}` (또는 `18089` 포트)로 접속합니다.
2. **Setup**: 수행할 가상 사용자 수(Users)와 초당 증가율(Spawn rate)을 입력합니다.
3. **Run**: `Start swarming`을 클릭하여 시나리오를 가동합니다.

### 4. 지표 수집 확인 (Monitoring)
- 지표는 실시간으로 InfluxDB에 전송됩니다.
- Grafana의 `Load Testing Dashboard`를 연동하여 시계열 추이를 확인하십시오.

## Common Pitfalls

- **Token 인식 실패**: `docker-compose.yml`의 `secrets` 경로 및 `locust-master`의 환경 변수 매핑을 확인하십시오.
- **Worker 미연결**: 워커는 `locust-master` 컨테이너 명칭을 호스트로 인식해야 하므로, 네트워크 설정에 유의하십시오.
- **InfluxDB v2 연동**: `influxdb-client` 라이브러리가 포함된 커스텀 이미지를 사용하는지 확인하십시오.

## Related Documents

- **Infrastructure**: [Locust Infra Layer](../../../infra/09-tooling/locust/README.md)
- **Operation**: [Locust Operations Policy](../../08.operations/09-tooling/locust.md)
- **Runbook**: [Locust Recovery Runbook](../../09.runbooks/09-tooling/locust.md)
