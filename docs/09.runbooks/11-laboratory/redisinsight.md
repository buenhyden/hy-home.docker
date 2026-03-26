# RedisInsight Runbook

> RedisInsight 연결 장애 및 설정 복구 절차.

---

## Overview (KR)

이 런북은 RedisInsight의 연결 오류, 설정 초기화, 그리고 서비스 성능 저하 상황 발생 시 조치 방법을 안내한다.

## Procedure or Checklist

### 1. Connection Failure Troubleshooting

Redis 서버에 연결할 수 없는 경우:

1. 네트워크 확인: `docker exec redisinsight ping <redis_service_name>`.
2. Redis 서버 상태 확인: `docker logs redis`.
3. RedisInsight 설정에서 호스트명과 포트(6379)가 올바른지 재확인한다.

### 2. Configuration Reset

잘못된 설정으로 인해 UI가 비정상적인 경우:

1. 서비스를 중단한다: `docker compose down`.
2. `${DEFAULT_MANAGEMENT_DIR}/redisinsight` 내의 설정 파일을 백업한 뒤 삭제한다.
3. 서비스를 다시 시작하여 설정을 초기화한다: `docker compose up -d`.

### 3. Log Inspection

작업 중 오류 발생 시:

1. `docker logs -f redisinsight`를 통해 실시간 에러 로그를 확인한다.
2. 브라우저 개발자 도구의 'Console' 섹션에서 JS 에러 여부를 확인한다.

## Verification Steps

- [ ] `https://redisinsight.${DEFAULT_URL}` 접속 및 메인 대시보드 로드 확인.
- [ ] 'Browser' 탭에서 키 목록이 지연 없이 조회되는지 확인.

## Related Documents

- **Operations**: `[../../08.operations/11-laboratory/redisinsight.md]`
- **System Guide**: `[../../07.guides/11-laboratory/redisinsight.md]`
