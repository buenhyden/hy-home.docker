# Task: Standardize `infra_net` Implementation

## Overview (KR)

이 문서는 모든 인프라 서비스에 `infra_net` 네트워크를 적용하기 위한 구역이다. Spec과 Plan에서 정의된 각 단계를 추적 가능한 태스크 단위로 분할하여 관리하며, 현재 모든 작업이 완료되었다.

## Inputs

- **Parent Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Parent Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
- **Parent PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`

## Working Rules

- 모든 작업은 `docker compose config`를 통해 구문 오류가 없음을 검증함.
- 기존의 `k3d-hyhome` 네트워크 설정은 보존되었음.
- 9개 디렉터리의 문서화 작업이 완료됨.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DOC-01 | PRD, ARD, ADR, Spec, Plan 작성 | doc | SPC-GOV | Phase 1 | `ls docs/` 및 컨텐츠 확인 | Antigravity | Done |
| T-DOC-02 | Task, Guide, Oper, Runbook 작성 | doc | SPC-GOV | Phase 1 | `ls docs/` 및 컨텐츠 확인 | Antigravity | Done |
| T-DOC-03 | 9개 디렉터리 README 업데이트 | doc | SPC-GOV | Phase 1 | README 내용 확인 | Antigravity | Done |
| T-IMP-01 | 루트 `docker-compose.yml` 수정 | impl | SPC-CFG | Phase 2 | `docker compose config` | Antigravity | Done |
| T-IMP-02 | 21개 서비스 Compose 파일 수정 | impl | SPC-CFG | Phase 2 | `grep "infra_net" infra/**/docker-compose.yml` | Antigravity | Done |
| T-VAL-01 | 전체 네트워크 병합 결과 검증 | test | SPC-VAL | Phase 3 | `docker compose config` | Antigravity | Done |
| T-DOC-04 | 외부 수동 할당 IP 명세 동기화 | doc | SPC-GOV | Phase 3 | Spec 내 IP 매핑 테이블 업데이트 | Antigravity | Done |

## Verification Summary

- **Test Commands**:
  - `docker compose config`
  - `grep -r "infra_net" infra/`
  - `grep -r "k3d-hyhome" infra/`
- **Logs / Evidence Location**: `docs/06.tasks/2026-04-01-standardize-infra-net.md` (Update status)

## Phase View

### Phase 1: Documentation

- [x] T-DOC-01 Create core SSoT docs (PRD-Plan)
- [x] T-DOC-02 Create support docs (Task-Runbook)
- [x] T-DOC-03 Update folder READMEs

### Phase 2: Implementation

- [x] T-IMP-01 Modify root docker-compose.yml
- [x] T-IMP-02 Modify individual service files (21+ files)

### Phase 3: Verification

- [x] T-VAL-01 Final verification and config check

## Related Documents

- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
- **Guide**: `[../07.guides/0012-standardize-infra-net.md]`
- **Runbook**: `[../09.runbooks/0012-standardize-infra-net.md]`
- **ARD**: `[../02.ard/2026-04-01-standardize-infra-net.md]`
- **ADR**: `[../03.adr/2026-04-01-standardize-infra-net.md]`
- **Operation**: `[../08.operations/standardize-infra-net.md]`
- **PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`
