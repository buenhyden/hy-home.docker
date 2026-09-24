---
title: "Tooling Services Selection and Configuration"
version: "2.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "architecture"
artifact_id: "ADR-0009"
parent_ids:
- "AD-0009"
created: "2026-03-26"
---
# ADR-0009: Tooling Services Selection and Configuration

## Context

이 문서는 해당 아키텍처 결정의 배경, 선택, 결과를 추적하기 위한 ADR이다. 2026-09-19의 정정은 제거된 Syncthing 의무와 현재 OpenTofu 실행 소유자를 반영하며 원래 결정은 Git 이력에 보존된다.

`09-tooling` 계층은 개발 및 운영 효율성을 극대화하기 위한 보조 도구들을 포함한다. 인프라 자동화(IaC), 코드 품질 분석, 성능 테스트, 내부 이미지 보관 등 다양한 요구사항을 충족하기 위해 검증된 오픈소스 솔루션들을 선정하고 통합해야 한다.

## Decision

다음과 같은 서비스 스택을 `09-tooling`의 표준 도구로 선정한다.

1. **IaC Automation**: **OpenTofu / Terrakube**
   - 이유: 현재 CLI helper는 OpenTofu이며 Terrakube는 workspace 상태와 실행을 관리한다. Terraform workspace의 기존 state/provider 계약은 migration handoff에서 검토한다.
2. **Code Quality**: **SonarQube**
   - 이유: 다중 언어 지원 및 정밀한 정적 분석 기능을 통해 프로젝트의 전반적인 코드 품질과 보안 취약점을 중앙에서 관리한다.
3. **Performance Testing**: **Locust**
   - 이유: Python 기반의 시나리오 정의가 가능하여 확장이 용이하며, 분산 아키텍처를 통해 대규모 부하를 생성할 수 있다.
4. **OCI Registry**: **OCI Distribution Registry**
   - 이유: 내부 서비스 배포를 위한 경량화된 사설 이미지 저장소를 제공한다.
5. **Withdrawn selection**: Syncthing runtime과 해당 파일 동기화 의무는 제거되었다. 이 항목은 과거 선택의 철회 기록이며 현재 서비스나 다른 기능으로 대체한 요구사항이 아니다.

### Rationale

- **통합성**: SonarQube/Terrakube 관리 UI는 선언된 gateway+SSO 경계를 사용한다. CLI 작업, 부하 생성기와 registry 프로토콜에 동일한 브라우저 SSO 경계가 있다고 가정하지 않는다.
- **지속성**: IaC 상태 정보 및 분석 데이터는 선언된 backend에 보관한다. 단일 호스트 persistence는 독립 백업이 아니며 데이터 유실 방지나 복구 성공은 검증된 백업/복구 증거 없이는 보장하지 않는다.
- **표준화**: 각 서비스는 Docker Compose 및 사전에 정의된 환경 변수를 통해 일관된 방식으로 배포된다.

### Decision Record

Accepted (2026-03-26). Amended on 2026-09-19 to withdraw Syncthing and align the CLI helper with OpenTofu; no runtime deployment or recovery success is asserted.

## Consequences

- **Positive**:
  - 인프라 변경 이력이 투명하게 관리된다.
  - 코드 품질 게이트를 통해 결함 있는 코드의 배포를 사전에 차단할 수 있다.
  - 성능 병목 지점을 데이터 기반으로 파악할 수 있다.
- **Negative**:
  - 다양한 도구 운영에 따른 유지보수 리소스(메모리, CPU) 점유율이 증가한다.
  - 도구 간의 복잡한 네트워크 권한 설정이 필요하다.

### Explicit Non-goals

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

## Options Considered

Existing alternatives, rationale, or rejected options in this ADR remain the alternative analysis. This alignment section does not add new alternatives.

## Traceability

이 결정의 확인 근거는 `Related Documents`에 연결된 Architecture Description, Spec, Operations 문서와 현재 저장소 구성으로 한정한다. 별도 실행 증거가 없는 런타임 상태는 주장하지 않는다.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- [Tooling PRD](../../01.requirements/0010-tooling.md)
- [Tooling Architecture Description](../descriptions/0009-tooling-architecture.md)
- [Current convergence Spec](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [OpenTofu operations](../../05.operations/catalog/09-tooling/0082-opentofu/guide.md)
- [Terraform migration handoff](../../05.operations/catalog/09-tooling/0068-terraform/guide.md)
