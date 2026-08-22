---
profile_id: architecture-description
status: active
artifact_id: AD-0025
artifact_type: architecture-description
parent_ids:
  - REQ-0022
created: 2026-03-28
updated: 2026-08-10
---
# 11-Laboratory Optimization Hardening Architecture Description

## Context and Stakeholders

이 문서는 `11-laboratory` 계층 최적화/하드닝 참조 아키텍처를 정의한다. 관리 UI를 gateway 보안 체인, SSO 인증, IP allowlist 경계 뒤에 배치하고 실험성 서비스 운영 드리프트를 CI 게이트로 통제하는 아키텍처 계약을 명시한다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

Laboratory tier는 운영자 생산성을 위한 관리 도구 계층이지만, 권한이 큰 UI를 다루므로 "보안 경계 우선" 설계가 필요하다.

- Dashboard: homer
- Container/Log Admin UI: portainer, dozzle
- Data Admin UI: redisinsight
- Local notebook lab: open-notebook, surrealdb

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - Laboratory UI ingress 경계 계약(gateway chain + SSO + allowlist)
  - `infra_net` external 네트워크 경계 계약
  - dashboard direct host exposure 금지 계약
  - dozzle 최소권한(socket read-only) 계약
  - open-notebook UI route SSO/allowlist/large-body 경계와 Docker Secret 주입 계약
  - laboratory hardening CI 정책 게이트
- **Consumes**:
  - `01-gateway` Traefik middleware
  - `02-auth` SSO middleware
  - Docker Engine / Valkey-Redis endpoints
- **Does Not Own**:
  - Keycloak realm 상세 정책
  - Traefik global entrypoints
- **Non-goals**:
  - 실험성 서비스를 프로덕션 워크로드 계층으로 승격
  - 관리 도구 전체 재플랫폼

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Security**: direct host 노출 제거, allowlist+SSO 이중 경계 적용
- **Reliability**: compose 계약 및 healthcheck 기반 최소 런타임 안정성 확보
- **Operability**: CI hardening gate와 runbook 기반 회귀 복구 표준화
- **Scalability**: 카탈로그 기반 정책(만료/승인/감사)을 단계적으로 확장

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

- **Ingress path**:
  - Operator -> Traefik(websecure) -> homer/dozzle/portainer/redisinsight/open-notebook
- **Control path**:
  - dozzle/portainer -> Docker socket
  - redisinsight -> valkey/redis endpoints
  - open-notebook -> surrealdb

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

This hardening Architecture Description does not introduce production data ownership for the laboratory tier. Data access remains limited to management metadata, Docker socket visibility, log streams, Valkey/Redis endpoint inspection, and Open Notebook local laboratory state described in the control path.

## Deployment View

- **Runtime / Platform**: Docker Compose (`infra/11-laboratory/*`)
- **Deployment Model**:
  - Service별 compose + 공통 template(`infra/common-optimizations.yml`)
- **Operational Evidence**:
  - compose static checks
  - `scripts/hardening/check-all-hardening.sh 11-laboratory`
  - CI `infrastructure-hardening` job

## Catalog-aligned Expansion Targets

- **dashboard**: SSO+allowlist 유지, 실험성 서비스 자동 만료 정책(태그 기반 정리) 적용
- **dozzle**: 로그 열람 범위 제한(운영 로그 접근 차단 규칙), 권한 최소화 지속 점검
- **portainer**: 관리자 계정/세션 정책 강화, 엔드포인트 등록 승인 절차 문서화
- **redisinsight**: 접근권한 최소화, 운영 캐시 직접 변경 금지와 감사로그 정책 강화
- **open-notebook**: secret-file credential 주입 유지, notebook data retention/expiration policy, direct API/DB host-port exposure review before production promotion

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [../01.requirements/0022-laboratory-optimization-hardening.md](../../01.requirements/0022-laboratory-optimization-hardening.md)
- **Spec**: [../03.specs/012-laboratory/spec.md](../../03.specs/spec-0012-laboratory/spec.md)
- **Plan**: ../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md
- **ADR**: [../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Tasks**: ../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md
- **Guide**: [../../05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md](../../05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/guide.md)
- **Operation**: [../../05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md](../../05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/policy.md)
- **Runbook**: [../../05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md](../../05.operations/catalog/11-laboratory/ops-0074-optimization-hardening/runbook.md)
