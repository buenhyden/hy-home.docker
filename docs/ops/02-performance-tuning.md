# 🚀 Performance Tuning Guide

인프라의 응답 속도를 개선하고 리소스 사용을 최적화하기 위한 가이드입니다.

## 1. Docker Engine Optimization

### Resource Limits

각 컨테이너가 시스템의 모든 자원을 점유하지 않도록 상한선을 설정합니다.

```yaml
# docker-compose.yml 예시
services:
  heavy-service:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Logging Driver

많은 로그가 발생하면 디스크 I/O 성능이 저하될 수 있습니다. `json-file` 드라이버의 크기 제한을 설정하십시오.

## 2. Java Virtual Machine (JVM) Tuning

Keycloak, Kafka, Airflow 등 Java 기반 서비스의 힙 메모리를 시스템 환경에 맞춰 조정합니다.

- **Option**: `-Xms`(최소 힙), `-Xmx`(최대 힙).
- **Rule of Thumb**: 컨테이너 할당 메모리의 약 50~75%를 힙 메모리에 할당하여 OS 캐시 영역을 확보하십시오.

## 3. Database (PostgreSQL) Optimization

- **Shared Buffers**: 전체 RAM의 25% 정도로 설정.
- **Connection Pooling**: `pgbouncer`를 도입하거나 애플리케이션 단의 커넥션 풀을 최적화하십시오.
- **Index Management**: 슬로우 쿼리 로그를 수집하여 필요한 인덱스를 생성하십시오 (`pg_stat_statements` 활용).

## 4. Reverse Proxy (Traefik) Cache

정적 자원에 대한 캐싱 레이어를 추가하거나, 압축(`gzip`, `br`) 기능을 활성화하여 네트워크 트래픽을 줄입니다.

## 5. Storage Performance

- **Bind Mounts vs Volumes**: 고성능 처리가 필요한 데이터(DB 파일 등)에는 명명된 볼륨(Named Volumes)을 사용하십시오.
- **IOPS**: SSD 환경에서 가동 중인지 확인하고, 로그 파일과 데이터 파일의 경로를 물리적으로 분리하는 것도 방법입니다.

## 6. Monitoring & Profiling

- **Grafana Dashboards**: 배포된 오버저버빌리티 스택을 통해 지속적으로 병목 지점을 추적하십시오.
- **Alloy Graphs**: 데이터 수집 에이전트의 부하가 높은지 확인하십시오.
- **Py-spy / Go tool pprof**: 소스 코드 레벨의 튜닝이 필요한 경우 프로파일링 도구를 사용하십시오.
