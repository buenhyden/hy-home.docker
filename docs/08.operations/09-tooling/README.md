# Tooling Tier Operations (09-tooling)

> `09-tooling` 계층 운영 정책과 통제 기준 문서 모음.

## Overview

이 디렉터리는 Tooling 계층의 운영 거버넌스를 관리한다. 도구별 정책(terraform, terrakube, registry, sonarqube, k6, locust, syncthing)과 최적화/하드닝 기준을 정의하며, 실행 절차는 runbook으로 분리한다.

## Documents

- [Performance Testing Operations Policy](./performance-testing.md)
- [Locust Operations Policy](./locust.md)
- [k6 Operations Policy](./k6.md)
- [Registry Operations Policy](./registry.md)
- [SonarQube Operations Policy](./sonarqube.md)
- [Syncthing Operations Policy](./syncthing.md)
- [Terraform Operations Policy](./terraform.md)
- [Terrakube Operations Policy](./terrakube.md)
- [Optimization Hardening Operations Policy](./optimization-hardening.md)

## Operational Standards

- 공개 tooling 라우터는 gateway 표준 체인 + SSO 체인을 강제한다.
- compose 네트워크 경계(`infra_net` external)를 유지한다.
- tooling 하드닝 회귀는 script/CI 게이트로 차단한다.
- 카탈로그 확장 항목은 승인 게이트와 함께 단계적으로 도입한다.

## Related References

- [Tooling Guide Index](../../07.guides/09-tooling/README.md)
- [Tooling Runbook Index](../../09.runbooks/09-tooling/README.md)
- [Tooling PRD](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- [Tooling Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tooling Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- [Optimization Catalog](../12-infra-service-optimization-catalog.md)
