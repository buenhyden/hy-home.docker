# Portainer Operations Policy

> Docker 관리 도구의 보안 노출 및 운영 정책 정의.

---

## Policy Scope

Portainer 인터페이스의 접근 제어, 데이터 백업, 리소스 관리 가이드라인.

## Applies To

- **Systems**: Portainer (Container Management)
- **Environments**: Infrastructure Management Area

## Controls

- **Access Control**:
  - 반드시 Traefik `sso-auth@file` 미들웨어를 통해 1차 인증을 수행해야 한다.
  - Portainer 내부 RBAC를 활성화하여 불필요한 관리자 권한 부여를 제한한다.
- **Data Persistence**:
  - `portainer_data` 볼륨은 `${DEFAULT_MANAGEMENT_DIR}/portainer`에 매핑되어야 하며, 시스템 백업 대상에 포함되어야 한다.
- **Resource Management**:
  - `sts` (Short Term Support) 이미지를 사용하여 보안 업데이트를 주기적으로 적용한다.

## Disallowed Actions

- Portainer 내부의 `docker.sock`을 외부에 API 형태로 노출하는 행위.
- `admin` 계정의 비밀번호를 평문으로 기록하거나 공유하는 행위.

## Verification

- **Security Scan**: 주기적으로 `docker.sock`에 대한 무단 접근 시도를 로깅하고 분석한다.
- **Connectivity**: `https://portainer.${DEFAULT_URL}` 접속 시 SSO 인증 창이 정상적으로 뜨는지 확인한다.

## Review Cadence

- Semi-annually (6개월 단위 정기 보안 리뷰)

## Related Documents

- **System Usage**: `[../../05.operations/11-laboratory/portainer.md]`
- **Procedure**: `[../../05.operations/11-laboratory/portainer.md]`

---

## Overview (KR)

이 문서는 `docs/05.operations/11-laboratory/portainer.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/11-laboratory/portainer.md` during the 2026-05-10 operations taxonomy consolidation.

### Portainer System Usage

> Docker 환경 관리 및 컨테이너 오케스트레이션 UI 활용 가이드.

---

#### Overview (KR)

이 문서는 Portainer를 사용하여 로컬 및 원격 Docker 환경을 관리하는 방법을 설명한다. 웹 인터페이스를 통한 실시간 모니터링, 로그 분석, 볼륨/네트워크 관리 절차를 포함한다.

#### Usage Type

`system-guide | how-to`

#### Step-by-step Instructions

##### 1. Initial Admin Setup

1. `https://portainer.${DEFAULT_URL}`에 처음 접속하면 관리자 계정 생성 화면이 나타난다.
2. 강력한 비밀번호를 설정한다 (최소 12자 권장).
3. 'Get Started'를 클릭하여 로컬 환경을 자동으로 연결한다.

##### 2. Managing Containers

1. 왼쪽 메뉴에서 'Containers'를 선택한다.
2. 특정 컨테이너를 클릭하여 'Logs', 'Inspect', 'Stats' 기능을 활용한다.
3. 'Add container' 기능을 사용하여 임시 어위(Ad-hoc) 컨테이너를 생성할 수 있다 (운영 시에는 주로 Docker Compose 사용 권장).

##### 3. Stack Deployment

1. 'Stacks' 메뉴에서 Docker Compose 파일을 직접 업로드하거나 붙여넣어 배포할 수 있다.
2. `infra/` 폴더의 서비스 수정 시에는 터미널에서 `docker compose` 명령을 사용하는 것이 형상 관리 측면에서 권장된다.

#### Best Practices

- **Resource Limits**: 컨테이너 생성 시 CPU/Memory 제한을 설정하여 시스템 전체의 안정성을 확보하라.
- **Pruning**: 정기적으로 'Images' 메뉴에서 Unused 이미지를 삭제하여 디스크 공간을 관리하라.
- **Network Isolation**: 서비스 간 통신은 가급적 전용 네트워크를 사용하고 Portainer에서 이를 시각적으로 확인하라.

#### Common Pitfalls

- **Docker Socket Availability**: `/var/run/docker.sock` 볼륨 바인딩이 누락되거나 권한이 없을 경우 Portainer가 로컬 환경을 인식하지 못한다.
- **SSO Double Auth**: Traefik `sso-auth`와 Portainer 내부 인증이 중복되므로, SSO 로그인 후 Portainer 로그인도 수행해야 함을 인지하라.

#### Related Documents

- **Implementation**: `[../../../infra/11-laboratory/portainer/README.md]`
- **Operation**: `[../../05.operations/11-laboratory/portainer.md]`
- **Procedure**: `[../../05.operations/11-laboratory/portainer.md]`

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

> Migrated from `docs/05.operations/11-laboratory/portainer.md` during the 2026-05-10 operations taxonomy consolidation.

### Portainer Procedure

> 관리자 비밀번호 복구 및 서비스 장애 해결 절차.

---

#### Overview (KR)

이 런북은 Portainer 관리 계정 접근 불능 사유 발생 시 비밀번호를 초기화하거나, 서비스 시작 불능 상황을 복구하는 절차를 제공한다.

#### Procedure or Checklist

##### 1. Admin Password Reset

Portainer 내부 DB의 관리자 비밀번호를 수동으로 재설정해야 하는 경우 다음을 수행한다.

1. Portainer 컨테이너 중지:

   ```bash
   docker compose down
   ```

2. 비밀번호 초기화 헬퍼 도구 실행 (데이터 볼륨 사용):

   ```bash
   docker run --rm -v portainer_data:/data portainer/helper-reset-password
   ```

   *참고: 출력되는 임시 비밀번호를 기록한다.*

##### 3. Stack Deployment

1. 'Stacks' 메뉴에서 Docker Compose 파일을 직접 업로드하거나 붙여넣어 배포할 수 있다.

##### Implementation Snippet

##### Service Configuration

 Issues

Portainer가 로컬 Docker 환경에 연결하지 못하는 경우:

1. `docker-compose.yml`의 볼륨 섹션에서 `/var/run/docker.sock` 매핑 여부를 확인한다.
2. 호스트의 socket 권한 확인: `ls -l /var/run/docker.sock`.
3. Portainer 로그 확인: `docker| Storage |`portainer_data` | Persistent volume for config |

##### Traefik Integration

데이터베이스 오염으로 인해 실행되지 않는 경우:

1. 백업된 `${DEFAULT_MANAGEMENT_DIR}/portainer` 데이터를 복원한다.
2. 기존 볼륨을 삭제하고 새 데이터를 배치한 뒤 재시작한다.

#### Verification Steps

- [ ] `https://portainer.${DEFAULT_URL}` 로그인 후 'Home' 대시보드에 로컬 환경이 'Active' 상태인지 확인.
- [ ] 'Containers' 목록이 정상적으로 업데이트되는지 확인.

#### Related Documents

- **Operations**: `[../../05.operations/11-laboratory/portainer.md]`
- **System Usage**: `[../../05.operations/11-laboratory/portainer.md]`

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
