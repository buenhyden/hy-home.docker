# Tooling Tier Runbooks (09-tooling)

> `09-tooling` 계층의 실행형 복구/유지보수 런북 모음.

## Overview

이 디렉터리는 Tooling 계층 장애 상황에서 즉시 실행 가능한 절차를 제공한다. 서비스 단위 복구 런북과 최적화/하드닝 회귀 복구 런북을 함께 관리한다.

## Documents

- [Performance Testing Runbook](./performance-testing.md)
- [Locust Runbook](./locust.md)
- [k6 Runbook](./k6.md)
- [Registry Runbook](./registry.md)
- [SonarQube Runbook](./sonarqube.md)
- [Syncthing Runbook](./syncthing.md)
- [Terraform Runbook](./terraform.md)
- [Terrakube Runbook](./terrakube.md)
- [Optimization Hardening Runbook](./optimization-hardening.md)

## Verification Baseline

- `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
- `bash scripts/check-tooling-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`

## Related References

- [Tooling Guides](../../07.guides/09-tooling/README.md)
- [Tooling Operations](../../08.operations/09-tooling/README.md)
- [Tooling Spec](../../04.specs/09-tooling/spec.md)
- [Tooling Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tooling Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
