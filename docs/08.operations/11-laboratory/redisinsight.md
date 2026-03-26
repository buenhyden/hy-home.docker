# RedisInsight Operations Policy

> Redis 관리 UI의 운영 및 보안 정책 정의.

---

## Policy Scope

RedisInsight의 접근 권한, 연결 메타데이터 관리, 그리고 운영 가드레일.

## Applies To

- **Systems**: RedisInsight (Database GUI)
- **Environments**: Laboratory/Management Tier

## Controls

- **Authentication**:
  - Traefik `sso-auth`를 통한 외부 접근 차단이 필수적이다.
- **Data Security**:
  - Redis 서버의 패스워드 정보를 RedisInsight에 저장할 때 'Save' 옵션 사용 여부는 팀의 보안 정책에 따른다 (가급적 매치 세션마다 입력을 권장).
- **Persistence**:
  - 연결 설정 및 튜닝 데이터는 `${DEFAULT_MANAGEMENT_DIR}/redisinsight` 볼륨에 안전하게 보관되어야 한다.

## Disallowed Actions

- RedisInsight를 퍼블릭 망에 노출하거나 SSO 없이 접근 가능하게 설정하는 행위.
- 고부하 환경에서 `keys *` 명령을 Profiler 없이 직접 실행하는 행위 (Scan 명령 권장).

## Verification

- **Audit Logs**: 관리자 로그를 통해 비정상적인 데이터 대량 삭제 행위가 있는지 모니터링한다.
- **Access Check**: `https://redisinsight.${DEFAULT_URL}` 접속 시 SSO 인증이 강제되는지 확인한다.

## Review Cadence

- Semi-annually (데이터 접근 권한 감사와 병행)

## Related Documents

- **System Guide**: `[../../07.guides/11-laboratory/redisinsight.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/redisinsight.md]`
