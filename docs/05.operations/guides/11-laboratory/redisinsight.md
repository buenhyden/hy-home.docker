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

- **System Usage**: `[../../05.operations/11-laboratory/redisinsight.md]`
- **Procedure**: `[../../05.operations/11-laboratory/redisinsight.md]`

---

## Overview (KR)

이 문서는 `docs/05.operations/11-laboratory/redisinsight.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/11-laboratory/redisinsight.md` during the 2026-05-10 operations taxonomy consolidation.

### RedisInsight System Usage

> Redis 데이터 시각화 및 분석 도구 활용 가이드.

---

#### Overview (KR)

이 문서는 RedisInsight를 사용하여 Redis 데이터를 탐색하고 분석하는 방법을 설명한다. 키 브라우징, 메모리 분석기, 그리고 웹 기반 CLI 사용 절차를 포함한다.

#### Usage Type

`system-guide | how-to`

#### Step-by-step Instructions

##### 1. Connection Setup

1. `https://redisinsight.${DEFAULT_URL}`에 접속한다.
2. 'Add Redis Database'를 클릭한다.
3. 호스트명(같은 네트워크 내의 경우 서비스 이름, 예: `redis`)과 포트(6379)를 입력한다.
4. 연결이 성공하면 대시보드에서 데이터 요약을 확인할 수 있다.

##### 2. Key Analysis & Browser

1. 'Browser' 탭에서 필터링 기능을 사용하여 특정 패턴의 키를 검색한다.
2. 'Key Analyzer'를 실행하여 어떤 키 타입이 메모리를 가장 많이 점유하는지 분석한다.
3. 데이터의 TTL(Time-to-Live)을 실시간으로 확인하고 수정할 수 있다.

##### 3. Using Profiler

1. 'Profiler' 기능을 활성화하여 특정 애플리케이션의 쿼리 부하를 실시간으로 캡처한다.
2. 느린 쿼리를 식별하고 최적화 포인트를 찾는다.

#### Best Practices

- **Read-Only Mode**: 운영 환경의 데이터를 조회할 때는 실수로 데이터가 변경되지 않도록 주의하라.
- **TTL Management**: 메모리 부족 방지를 위해 모든 키에 적절한 TTL이 설정되어 있는지 주기적으로 점검하라.
- **Sampling**: 대규모 데이터셋 분석 시에는 성능 저하를 막기 위해 샘플링 기능을 활용하라.

#### Common Pitfalls

- **Network reachability**: `infra_net` 외부의 Redis에 연결하려면 적절한 네트워크 브릿지 또는 호스트 매핑이 필요하다.
- **Version Compatibility**: Redis 모듈(JSON, Search 등) 사용 시 RedisInsight의 버전과 호환되는지 확인하라.

#### Related Documents

- **Implementation**: `[../../../infra/11-laboratory/redisinsight/README.md]`
- **Operation**: `[../../05.operations/11-laboratory/redisinsight.md]`
- **Procedure**: `[../../05.operations/11-laboratory/redisinsight.md]`

---

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

## Procedure

> Migrated from `docs/05.operations/11-laboratory/redisinsight.md` during the 2026-05-10 operations taxonomy consolidation.

### RedisInsight Procedure

> RedisInsight 연결 장애 및 설정 복구 절차.

---

#### Overview (KR)

이 런북은 RedisInsight의 연결 오류, 설정 초기화, 그리고 서비스 성능 저하 상황 발생 시 조치 방법을 안내한다.

#### Procedure or Checklist

##### 1. Connection Failure Troubleshooting

Redis 서버에 연결할 수 없는 경우:

1. 네트워크 확인: `docker exec redisinsight ping <redis_service_name>`.
2. Redis 서버 상태 확인: `docker logs redis`.
3. RedisInsight 설정에서 호스트명과 포트(6379)가 올바른지 재확인한다.

##### 2. Configuration Reset

잘못된 설정으로 인해 UI가 비정상적인 경우:

1. 서비스를 중단한다: `docker compose down`.
2. `${DEFAULT_MANAGEMENT_DIR}/redisinsight` 내의 설정 파일을 백업한 뒤 삭제한다.
3. 서비스를 다시 시작하여 설정을 초기화한다: `docker compose up -d`.

##### 3. Log Inspection

작업 중 오류 발생 시:

1. `docker logs -f redisinsight`를 통해 실시간 에러 로그를 확인한다.
2. 브라우저 개발자 도구의 'Console' 섹션에서 JS 에러 여부를 확인한다.

#### Verification Steps

- [ ] `https://redisinsight.${DEFAULT_URL}` 접속 및 메인 대시보드 로드 확인.
- [ ] 'Browser' 탭에서 키 목록이 지연 없이 조회되는지 확인.

#### Related Documents

- **Operations**: `[../../05.operations/11-laboratory/redisinsight.md]`
- **System Usage**: `[../../05.operations/11-laboratory/redisinsight.md]`

---

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
