# Tooling Tier Guides (09-tooling)

> `09-tooling` 계층의 사용/설정/운영 준비를 위한 가이드 문서 모음.

## Overview

이 디렉터리는 Tooling 계층(terraform, terrakube, registry, sonarqube, k6, locust, syncthing)의 사용 방법과 하드닝 적용 절차를 제공한다. 운영 정책은 `08.operations`, 장애 대응은 `09.runbooks`에서 관리한다.

## Documents

- [01. IaC Automation Guide](./01.iac-automation.md)
- [02. Performance Testing Guide](./performance-testing.md)
- [03. Locust Guide](./locust.md)
- [04. k6 Guide](./k6.md)
- [05. Registry Guide](./registry.md)
- [06. SonarQube Guide](./sonarqube.md)
- [07. Syncthing Guide](./syncthing.md)
- [08. Terraform Guide](./terraform.md)
- [09. Terrakube Guide](./terrakube.md)
- [10. Optimization Hardening Guide](./optimization-hardening.md)

## How to Work in This Area

1. 새 가이드는 `docs/99.templates/guide.template.md`를 사용한다.
2. 실행 절차 변경 시 대응 Operation/Runbook 링크를 함께 갱신한다.
3. 최적화/하드닝 변경은 `optimization-hardening.md`와 Plan/Tasks를 동시 갱신한다.

## Related References

- [Tooling Infra](../../../infra/09-tooling/README.md)
- [Tooling PRD](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- [Tooling Spec](../../04.specs/09-tooling/spec.md)
- [Tooling Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tooling Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- [Tooling Operations](../../08.operations/09-tooling/README.md)
- [Tooling Runbooks](../../09.runbooks/09-tooling/README.md)
