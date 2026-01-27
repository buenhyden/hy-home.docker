# 🔍 Debugging Guide

인프라의 장애를 진단하고 해결하기 위한 체계적인 절차와 명령어를 설명합니다.

## 1. Container Diagnostics

### 로그 확인의 중요성

가장 먼저 확인해야 할 것은 서비스의 표준 출력 로그입니다.

```bash
# 특정 서비스 로그 확인
docker compose logs -f <service_name>

# 특정 시점 이전의 로그 예시
docker compose logs --until=1h <service_name>
```

### 컨테이너 내부 진입

설정 파일 확인이나 로컬 도구 실행이 필요할 때 사용합니다.

```bash
docker exec -it <container_name> sh (또는 bash)
```

## 2. Service Specific Debugging

### Database (PostgreSQL)

- **연결 확인**: `psql -h localhost -p 5432 -U postgres`
- **클러스터 상태**: `patronictl list` (Patroni 이미지 내부)

### Messaging (Kafka)

- **연결 확인**: `kafka-topics --bootstrap-server kafka-1:9092 --list`
- **UI 활용**: `kafka-ui` 대시보드에서 브로커 상태가 **Online**인지 확인.

### Reverse Proxy (Traefik)

- **Dashboard**: `http://traefik.127.0.0.1.nip.io/dashboard/` 에서 서비스의 건강 상태(Health check) 점검.
- **Access Logs**: `infra/traefik/logs/access.log` 에서 4xx, 5xx 에러 패턴 분석.

## 3. Network Troubleshooting

인프라 레이어의 네트워크 이슈를 해결합니다.

- **DNS 확인**: `docker exec <container> nslookup <target_service>`
- **포트 개방 확인**: `docker exec <container> nc -zv <target_service> <port>`
- **IP 대역 충돌**: `docker network inspect infra_net` 명령으로 컨테이너들의 IP 할당 상태 확인.

## 4. Resource Bottlenecks

- **CPU/RAM**: `docker stats` 명령으로 실시간 리소스 점유율 확인.
- **Disk**: `docker system df`로 볼륨 및 이미지 용량 점유 확인.
- **Zombies**: 좀비 프로세스 발생 시 컨테이너 재시작 권장.

## 5. Reporting for Help

스스로 해결할 수 없는 경우, 다음 정보를 포함하여 이슈를 생성하십시오:

1. **환경**: OS, Docker 버전.
2. **재현 방법**: 어떤 명령을 내렸을 때 에러가 발생하는가.
3. **로그**: 관련 서비스의 에러 로그 (`docker compose logs` 결과).
4. **시도한 내용**: 이미 확인해 본 사항들.
