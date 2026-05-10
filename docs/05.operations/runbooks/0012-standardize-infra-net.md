---
status: migrated
---
<!-- Target: docs/05.operations/runbooks/0012-standardize-infra-net.md -->

# 0012 Standardize Infra Net Operations

> Migrated from `docs/05.operations/0012-standardize-infra-net.md` during the 2026-05-10 operations taxonomy consolidation.

## Usage

### infra_net Implementation Usage

#### Overview (KR)

이 문서는 모든 인프라 서비스에 `infra_net` 공통 네트워크와 고정 IP를 할당하는 가이드다. 프로젝트의 일관성을 유지하기 위해 표준 딕셔너리 기반의 네트워크 정의 방식을 따른다.

#### Usage Type

`how-to | system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

이 가이드는 시스템 관리자나 개발자가 신규 서비스 또는 기존 서비스를 `hy-home.docker`의 표준 네트워크 구조인 `infra_net`에 올바르게 통합하는 것을 돕는다.

#### Prerequisites

- `hy-home.docker` 프로젝트 루트 디렉터리에 대한 쓰기 권한.
- Docker Compose v2.0 이상.
- `docs/04.execution/plans/2026-04-01-standardize-infra-net.md`의 IP 할당 현황.

#### Step-by-step Instructions

1. **IP 대역 확인**:
   - `docs/04.execution/plans/2026-04-01-standardize-infra-net.md`의 **IP Mapping Strategy** 섹션에서 서비스 그룹에 맞는 IP 가용 범위를 확인한다.
2. **Compose 파일 수정**:
   - `services:` 하위의 대상 서비스에서 `networks:` 섹션을 다음과 같이 딕셔너리 형태로 수정한다.

   ```yaml
   networks:
     infra_net:
       ipv4_address: 172.19.0.XXX
   ```

   - (선택 사항) 만약 K3s 연동을 위해 `k3d-hyhome` 네트워크가 필요한 경우 명시적으로 추가한다.
3. **루트 Docker Compose 수정**:
   - 프로젝트 루트의 `docker-compose.yml` 내 `include:` 섹션에서 해당 파일이 주석 처리되어 있지 않은지 확인한다.
4. **구성 검증**:
   - `docker compose config`를 실행하여 YAML 구문에 오류가 없는지 최종 확인한다.

#### Common Pitfalls

- **IP Conflict**: 이미 할당된 IP를 중복 부여하지 않도록 `grep` 등으로 전체 조사를 수행해야 함.
- **Indentation Error**: YAML 딕셔너리 구조에서의 들여쓰기 오류 주의.
- **Network Scope**: 지정된 주소 대역(`172.19.0.0/16`) 외부의 IP를 입력할 경우 배포 실패.

#### Related Documents

- **Spec**: `[../03.specs/standardize-infra-net/spec.md]`
- **Operation**: `[../05.operations/standardize-infra-net.md]`
- **Procedure**: `[../05.operations/0012-standardize-infra-net.md]`
- **Plan**: `[../04.execution/plans/2026-04-01-standardize-infra-net.md]`

## Procedure

> Migrated from `docs/05.operations/0012-standardize-infra-net.md` during the 2026-05-10 operations taxonomy consolidation.

### infra_net IP Mapping Validation & Update Procedure

#### Overview (KR)

이 런북은 `infra_net` 서브넷 내 신규 서비스 추가 및 기존 서비스 IP 변경 시의 운영 절차를 정의한다. 서브넷 정합성 유지와 충돌 방지가 주 목적이다.

#### Purpose

신속하고 정확하게 서브넷 내 고정 IP를 할당하거나 기존 설정의 오구성을 수정한다.

#### Canonical References

- `[../02.architecture/requirements/2026-04-01-standardize-infra-net.md]`
- `[../02.architecture/decisions/2026-04-01-standardize-infra-net.md]`
- `[../03.specs/standardize-infra-net/spec.md]`
- `[../04.execution/plans/2026-04-01-standardize-infra-net.md]`

#### When to Use

- 서비스의 `networks` 설정을 표준 딕셔너리 포맷으로 전환할 때.
- 신규 인프라 서비스를 인공지능 홈 시스템에 통합할 때.
- 네트워크 충돌 발생 시 원인 분석 및 IP 재배치.

#### Procedure or Checklist

##### Checklist

- [ ] 대상 서비스의 `infra/` 내 `docker-compose.yml` 경로 확인.
- [ ] 현재 서브넷(`172.19.0.0/16`) 내 가용 IP 대역 확인 (Plan/Spec 참조).
- [ ] 중복 사용 여부 사전 검증 (`grep -r "ipv4_address" .`).

##### Procedure

1. **IP 선정**: `docs/04.execution/plans/2026-04-01-standardize-infra-net.md`의 IP 맵핑 리스트에서 비어있는 영역을 선택함.
2. **Compose 파일 수정**:

   ```yaml
   networks:
     infra_net:
       ipv4_address: 172.19.0.XXX
   ```

3. **구문 검증**: `docker compose config` 실행하여 YAML 유효성 확인.
4. **런타임 검증**: `docker compose up -d` (Test/Staging 환경) 실행 후 `docker inspect <container_name>`을 통해 실제 할당 결과 대조.

#### Verification Steps

- [ ] `docker network inspect infra_net` 실행 시 모든 컨테이너가 의도된 고정 IP를 보유하고 있는지 전수 조사.

#### Observability and Evidence Sources

- **Signals**: `docker-compose` 배포 로그의 "Network Conflict" 에러 메시지.
- **Evidence to Capture**: `grep -r "infra_net" infra/` 결과 덤프.

#### Safe Rollback or Recovery Procedure

- [ ] 변경 전 `docker-compose.yml` 백업본으로 복구.
- [ ] 충돌이 심각할 경우 해당 서비스를 `infra_net`에서 일시 제외하고 게이트웨이 서비스만 유지.

#### Related Operational Documents

- **Operations Policy**: `[../05.operations/standardize-infra-net.md]`
- **Spec**: `[../03.specs/standardize-infra-net/spec.md]`

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
