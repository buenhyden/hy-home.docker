# Laboratory Dashboard Operations Policy

> This document defines the operations policy, security controls, and governance for the laboratory dashboard (Homer).

---

## Overview (KR)

이 문서는 `11-laboratory` 티어의 서비스 대시보드(Homer)에 대한 운영 정책을 정의한다. 대시보드의 공개 범위, 신규 서비스 추가 프로세스, 보안 통제 기준을 규정하여 인프라 가시성과 안전성을 동시에 확보한다.

## Policy Scope

- Homer 대시보드 서비스 가용성.
- 대시보드 노출 서비스 선정 기준 및 관리 프로세스.
- 대시보드 접근 제어 및 보안 가드레일.

## Applies To

- **Systems**: Homer (Laboratory Dashboard)
- **Agents**: AI-Ops Agents (대시보드 업데이트 수행 시)
- **Environments**: Production-Management Area

## Controls

- **Required**:
  - 모든 대시보드 접근은 Traefik `sso-auth` 미들웨어를 통해 인증되어야 한다.
  - `config.yml` 변경 전 반드시 로컬에서 구문 검증(`yq` 등)을 거쳐야 한다.
  - 대시보드에 신규 관리 도구 추가 시 해당 도구의 인증 설정 여부를 선제적으로 확인해야 한다.
- **Allowed**:
  - 실험적 서비스의 일시적 등록 (단, 'Lab' 태그 부착 필수).
  - 테마 및 레이아웃의 자유로운 변경 (UI Usagelines 준수 범위 내).
- **Disallowed**:
  - 인증이 없는 데이터베이스 유틸리티나 민감 정보가 포함된 UI를 대시보드에 직접 노출하는 행위.
  - 공개 망(Internet)으로의 정적 배포 (인프라 전용 대시보드 용도 제한).

## Exceptions

- 초기 설정 및 긴급 복구 단계에서의 일시적 비인증 접근은 30분 이내로 제한하며, 작업 완료 후 반드시 인증을 활성화한다.

## Verification

- `yq eval . config/config.yml` 명령을 통한 설정 파일 무결성 확인.
- Traefik 라우터 설정에서 `sso-auth` 적용 여부 교차 검증.

## Review Cadence

- Quarterly (매 분기 대시보드 링크 유효성 및 보안 정책 리뷰).

## Related Documents

- **ARD**: `[../../02.architecture/requirements/03-security.md]`
- **Procedure**: `[../../05.operations/11-laboratory/dashboard.md]`
- **Implementation**: `[../../../infra/11-laboratory/dashboard/README.md]`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/11-laboratory/dashboard.md` during the 2026-05-10 operations taxonomy consolidation.

### Laboratory Dashboard (Homer) Usage

> This guide explains how to manage and customize the static service dashboard (Homer) in the 11-laboratory tier.

---

#### Overview (KR)

이 문서는 Homer 대시보드의 서비스 링크 관리, 테마 커스터마이징, 레이아웃 변경 방법을 설명한다. 하이홈 인프라의 모든 도구에 대한 접근성을 유지하고 관리하는 중앙 관리 지침을 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Operator
- Developer
- Agent-tuner

#### Purpose

- 신규 인프라 서비스의 대시보드 등록 자동화 및 표준화.
- 대시보드의 가독성 및 가시성 향상을 위한 스타일링 관리.
- 서비스 메타데이터(아이콘, 태그) 관리 표준 확립.

#### Prerequisites

- `infra/11-laboratory/dashboard/config/config.yml` 파일 접근 권한.
- FontAwesome 아이콘 이름 지식.
- Traefik 서비스 도메인 정보.

#### Step-by-step Instructions

##### 1. Adding New Services

신규 서비스를 대시보드에 추가하려면 다음 절차를 따른다.

1. `infra/11-laboratory/dashboard/config/config.yml` 파일을 연다.
2. `services` 배열 아래 적절한 그룹을 찾거나 새 그룹을 생성한다.
3. `items` 리스트에 다음 형식으로 서비스를 추가한다:

   ```yaml
   - name: "Service Name"
     icon: "fa-solid fa-server" # FontAwesome 아이콘
     subtitle: "Brief description"
     tag: "monitoring" # 색상 구분을 위한 태그
     url: "https://service.${DEFAULT_URL}"
   ```

4. 파일을 저장한다 (볼륨 바인딩을 통해 즉시 반영된다).

##### 2. Customizing Icons and Logos

- **Icons**: [FontAwesome v6](https://fontawesome.com/icons) 클래스명을 사용한다 (예: `fa-solid fa-cube`).
- **Logos**: `dashboard/config/` 폴더에 이미지 파일을 두고 `logo: "my-logo.png"`와 같이 참조한다.

##### 3. Layout and Theming

- **Columns**: `columns: "3"` 옵션을 통해 한 줄에 표시될 카드 개수를 조정한다.
- **Theme**: `theme: default` 섹션에서 색상이나 스타일을 정의할 수 있다.

#### Common Pitfalls

- **YAML Indentation**: 들여쓰기 오류 발생 시 대시보드가 로드되지 않는다. 수정 후 `yq` 등으로 검증을 권장한다.
- **URL Syntax**: `${DEFAULT_URL}` 변수 사용 시 따옴표(`${DEFAULT_URL}`) 유의.

#### Related Documents

- **Implementation**: `[../../../infra/11-laboratory/dashboard/README.md]`
- **Operation**: `[../../05.operations/11-laboratory/dashboard.md]`
- **Procedure**: `[../../05.operations/11-laboratory/dashboard.md]`

## Procedure

> Migrated from `docs/05.operations/11-laboratory/dashboard.md` during the 2026-05-10 operations taxonomy consolidation.

### Laboratory Dashboard Procedure: Homer

: Homer Dashboard Recovery and Configuration Service

---

#### Overview (KR)

이 런북은 `11-laboratory` 티어의 서비스 대시보드(Homer)에 대한 장애 복구 및 설정 검증 절차를 정의한다. 설정 오류로 인한 페이지 렌더링 실패나 서비스 접근 불가 상황을 즉시 해결하기 위한 단계별 지침을 제공한다.

#### Purpose

- Homer 설정 파일(`config.yml`)의 구문 오류 복구.
- 대시보드 서비스 재시작 및 갱신.
- 대시보드 내 링크 유효성 검사.

#### Canonical References

- `[../../../infra/11-laboratory/dashboard/README.md]`
- `[../../05.operations/11-laboratory/dashboard.md]`
- `[../../05.operations/11-laboratory/dashboard.md]`

#### When to Use

- Homer 접속 시 "Internal Server Error" 또는 빈 화면이 출력되는 경우.
- `config.yml` 수정 후 변경 사항이 실시간으로 반영되지 않는 경우.
- 대시보드 내 특정 아이콘이 깨지거나 링크가 동작하지 않는 경우.

#### Procedure or Checklist

##### Checklist

- [ ] `infra/11-laboratory/dashboard/config/config.yml` 파일 존재 여부 확인.
- [ ] Homer 컨테이너 실행 상태 확인 (`docker ps | grep homer`).

##### Procedure

###### 1. Configuration Validation and Recovery

1. 설정 파일의 구문 오류를 확인한다:

   ```bash
   yq eval . infra/11-laboratory/dashboard/config/config.yml
   ```

2. 오류가 발견되면 가장 최근의 백업본으로 복구하거나 오류 지점을 수정한다.
3. 수정 후 파일을 저장한다.

###### 2. Service Refresh

1. Homer는 실시간 반영을 지원하지만, 강제 재시작이 필요한 경우 다음 명령을 수행한다:

   ```bash
   cd infra/11-laboratory/dashboard
   docker compose restart homer
   ```

###### 3. Assets Check

1. 아이콘이나 로고가 표시되지 않는 경우 `dashboard/config/` 폴더 내 이미지 파일의 권한을 확인한다 (644 권한 권장).

#### Verification Steps

- [ ] 브라우저에서 `homer.${DEFAULT_URL}` 접속 및 정상 렌더링 확인.
- [ ] 브라우저 콘솔에서 404/500 에러 발생 여부 확인.

#### Safe Rollback or Recovery Procedure

- 작업 전: `cp config.yml config.yml.bak`
- 복구 시: `mv config.yml.bak config.yml && docker compose restart homer`

#### Related Operational Documents

- **Incident examples**: `[../../05.operations/incidents/2026/03-26-homer-config-corruption.md]`

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
