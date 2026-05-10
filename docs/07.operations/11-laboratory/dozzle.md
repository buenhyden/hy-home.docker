# Dozzle Operations Policy

> 관리 도구 로그 노출 및 접근 통제 정책.

---

## Overview (KR)

이 문서는 Dozzle 서비스의 운영 정책을 정의한다. 시스템 로그는 민감한 정보를 포함할 수 있으므로, 엄격한 인증 및 노출 범위를 규정하여 보안 사고를 예방한다.

## Policy Scope

Dozzle 서비스의 노출 범위, 인증 방식 및 리소스 접근 통제.

## Applies To

- **Systems**: Dozzle
- **Agents**: AI-Ops Agents
- **Environments**: Production-Management Area

## Controls

- **Required**:
  - 모든 UI 접근은 Traefik `sso-auth` 미들웨어를 통해 승인된 관리자만 가능해야 한다.
  - `/var/run/docker.sock`은 읽기 전용으로 연결하거나 내부 네트워크에서만 통제된 방식으로 사용되어야 한다 (Dozzle 설정 준수).
- **Allowed**:
  - 개발 및 트러블슈팅 목적의 실시간 로그 스트리밍.
- **Disallowed**:
  - 인증 없이 외부 인터넷(Public)에 Dozzle UI를 노출하는 행위.
  - 로그 데이터를 외부 서비스로 무단 반출하는 설정.

## Exceptions

- 긴급 장애 복구 상황에서 SSO 서버 장애 시, 로컬 포트 포워딩을 통한 일시적 접근을 허용하되 작업 완료 후 즉시 차단한다.

## Verification

- Traefik `Host` 룰 및 미들웨어 설정(`sso-auth`)이 `docker-compose.yml`에 올바르게 적용되었는지 정기적으로 검토한다.

## Review Cadence

- Quarterly (보안 감사 주기와 동기화)

## Related Documents

- **ARD**: `[../../02.ard/03-security.md]`
- **Usage**: `[../../07.operations/11-laboratory/dozzle.md]`
- **Procedure**: `[../../07.operations/11-laboratory/dozzle.md]`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/11-laboratory/dozzle.md` during the 2026-05-10 operations taxonomy consolidation.

### Dozzle Usage

> Real-time log viewer for Docker containers.

---

#### Overview (KR)

이 문서는 Dozzle을 사용하여 Docker 컨테이너의 로그를 실시간으로 모니터링하고 검색하는 방법을 설명하는 가이드다. 별도의 복잡한 설정 없이 웹 UI를 통해 모든 컨테이너의 로그 스트림에 접근할 수 있다.

#### Usage Type

`how-to | system-guide`

#### Target Audience

- Developer (Service debugging and log analysis)
- Operator (Health monitoring)

#### Purpose

Dozzle을 통해 인프라 내 컨테이너 로그를 효율적으로 확인하고 문제 발생 시 빠르게 원인을 파악한다.

#### Prerequisites

- [Traefik](../01-gateway/README.md) 활성화 및 로컬 도메인 설정.
- [SSO Auth](../02-auth/README.md)를 통한 인증 및 인가 완료.

#### Step-by-step Instructions

1. **Access Dozzle**: 브라우저에서 `https://dozzle.${DEFAULT_URL}`에 접속한다.
2. **Select Container**: 왼쪽 사이드바에서 로그를 확인하고 싶은 컨테이너를 선택한다.
3. **Real-time Monitoring**: 자동 스크롤(Auto-scroll) 기능을 활성화하여 실시간으로 유입되는 로그를 모니터링한다.
4. **Search and Filter**: 상단 검색창을 사용하여 특정 키워드(예: `ERROR`, `Exception`, `GET /api/v1`)가 포함된 로그를 필터링한다.
5. **Clear Logs**: UI 상의 'Clear' 버튼을 눌러 현재 화면의 로그를 비운다 (실제 로그 파일은 삭제되지 않음).

#### Common Pitfalls

- **Stale Connection**: 장시간 브라우저를 켜둘 경우 로그 스트림 연결이 끊어질 수 있다. 이 경우 페이지를 새로고침한다.
- **Large Log Volume**: 로그 유입량이 매우 많을 경우 브라우저 성능에 영향을 줄 수 있다. 필요한 경우 검색 필터를 적극 활용하라.

#### Related Documents

- **Implementation**: `[../../../infra/11-laboratory/dozzle/README.md]`
- **Operation**: `[../../07.operations/11-laboratory/dozzle.md]`
- **Procedure**: `[../../07.operations/11-laboratory/dozzle.md]`

## Procedure

> Migrated from `docs/07.operations/11-laboratory/dozzle.md` during the 2026-05-10 operations taxonomy consolidation.

### Dozzle Procedure

: Dozzle (Real-time Log Viewer)

---

#### Overview (KR)

이 런북은 Dozzle 서비스의 장애 대응 및 유지보수 절차를 정의한다. 로그 스트림 끊김, UI 응답 없음 등 발생 가능한 일반적인 문제에 대한 해결 단계를 제공한다.

#### Purpose

Dozzle 서비스의 가용성을 유지하고 로그 기반의 트러블슈팅 역량을 보존한다.

#### Canonical References

- `[../../../infra/11-laboratory/dozzle/README.md]`
- `[../../07.operations/11-laboratory/dozzle.md]`
- `[../../07.operations/11-laboratory/dozzle.md]`

#### When to Use

- Dozzle UI에 접속이 불가능한 경우.
- 특정 컨테이너의 로그가 Dozzle에서 보이지 않거나 업데이트되지 않는 경우.
- `/var/run/docker.sock` 관련 권한 오류가 발생하는 경우.

#### Procedure or Checklist

##### Checklist

- [ ] Dozzle 컨테이너가 `Up` 상태인가?
- [ ] `/var/run/docker.sock` 볼륨 마운트가 정상인가?
- [ ] Traefik 라우팅 및 SSO 인증이 정상인가?

##### Procedure

###### Case 1: 로그 스트림 업데이트 중단

1. 브라우저 페이지를 새로고침한다.
2. 해결되지 않을 경우 도커 컴포즈 명령으로 서비스를 재시작한다.

   ```bash
   cd infra/11-laboratory/dozzle
   docker compose restart dozzle
   ```

###### Case 2: 특정 컨테이너 로그 미노출

1. 해당 컨테이너가 실행 중인지 확인한다 (`docker ps`).
2. Dozzle 컨테이너의 로그를 확인하여 접근 거부(Permission Denied) 오류가 있는지 검사한다.

   ```bash
   docker logs dozzle
   ```

#### Verification Steps

- [ ] `https://dozzle.${DEFAULT_URL}` 접속 후 실시간 로그가 흐르는지 확인.
- [ ] 사이드바에서 여러 컨테이너를 전환하며 정상 응답 여부 확인.

#### Safe Rollback or Recovery Procedure

- 이미지 업데이트 후 장애 발생 시, 이전 태그(`v10.2.0`)로 명시적으로 롤백한 후 재배포한다.
- 설정 파일 오류 시 백업본(`.bak` 등)에서 복원한다.

#### Related Operational Documents

- **Incident Record**: `[../../10.incidents/README.md]`
- **Postmortem**: `[../../10.incidents/README.md]`

---

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
