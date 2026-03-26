# RedisInsight System Guide

> Redis 데이터 시각화 및 분석 도구 활용 가이드.

---

## Overview (KR)

이 문서는 RedisInsight를 사용하여 Redis 데이터를 탐색하고 분석하는 방법을 설명한다. 키 브라우징, 메모리 분석기, 그리고 웹 기반 CLI 사용 절차를 포함한다.

## Guide Type

`system-guide | how-to`

## Step-by-step Instructions

### 1. Connection Setup

1. `https://redisinsight.${DEFAULT_URL}`에 접속한다.
2. 'Add Redis Database'를 클릭한다.
3. 호스트명(같은 네트워크 내의 경우 서비스 이름, 예: `redis`)과 포트(6379)를 입력한다.
4. 연결이 성공하면 대시보드에서 데이터 요약을 확인할 수 있다.

### 2. Key Analysis & Browser

1. 'Browser' 탭에서 필터링 기능을 사용하여 특정 패턴의 키를 검색한다.
2. 'Key Analyzer'를 실행하여 어떤 키 타입이 메모리를 가장 많이 점유하는지 분석한다.
3. 데이터의 TTL(Time-to-Live)을 실시간으로 확인하고 수정할 수 있다.

### 3. Using Profiler

1. 'Profiler' 기능을 활성화하여 특정 애플리케이션의 쿼리 부하를 실시간으로 캡처한다.
2. 느린 쿼리를 식별하고 최적화 포인트를 찾는다.

## Best Practices

- **Read-Only Mode**: 운영 환경의 데이터를 조회할 때는 실수로 데이터가 변경되지 않도록 주의하라.
- **TTL Management**: 메모리 부족 방지를 위해 모든 키에 적절한 TTL이 설정되어 있는지 주기적으로 점검하라.
- **Sampling**: 대규모 데이터셋 분석 시에는 성능 저하를 막기 위해 샘플링 기능을 활용하라.

## Common Pitfalls

- **Network reachability**: `infra_net` 외부의 Redis에 연결하려면 적절한 네트워크 브릿지 또는 호스트 매핑이 필요하다.
- **Version Compatibility**: Redis 모듈(JSON, Search 등) 사용 시 RedisInsight의 버전과 호환되는지 확인하라.

## Related Documents

- **Implementation**: `[../../../infra/11-laboratory/redisinsight/README.md]`
- **Operation**: `[../../08.operations/11-laboratory/redisinsight.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/redisinsight.md]`
