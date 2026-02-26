# Operations Index

이 문서는 `hy-home.docker`의 운영 정책 및 실행 체계의 중앙 인덱스입니다.

- **Design Reference**: [`ARCHITECTURE.md`](ARCHITECTURE.md) (설계 원칙)
- **Product Vision**: [`docs/prd/README.md`](docs/prd/README.md) (제품 목표)
- **Executable Manuals**: [`runbooks/README.md`](runbooks/README.md) (역할별 장애 대응)
- **Historical Memory**: [`operations/README.md`](operations/README.md) (장애 기록물)

---

## 1. Environment Tiers

| Tier | Name | Target Hardware | Purpose |
| :--- | :--- | :--- | :--- |
| **L1** | Local Dev | Host Laptop | Individual service testing & spec validation |
| **L2** | Home-Lab | Dedicated NUC/Server | Multi-tier cluster integration & 24/7 availability |
| **L3** | Pro-Lab | High-spec Host | Performance benchmarking & HA recovery drills |

## 2. 운영 원칙

1. **Runbook-First**: 모든 실행 명령은 [`runbooks/`](runbooks/)에 정의된 문서를 최우선으로 따릅니다.
2. **Validate-Then-Apply**: 변경 전후 [`scripts/validate-docker-compose.sh`](scripts/validate-docker-compose.sh) 실행 필수.
3. **Secrets Hygiene**: 100% Docker Secrets를 통해 `/run/secrets/` 경로로 주입합니다.
4. **Blameless Culture**: 모든 SEV-1/2 장애는 비난 없는 사후 분석([operations/postmortems/](operations/postmortems/))을 수행합니다.

## 3. Incident Severity & Response

| Severity | Impact | Action | Tracking Hub |
| :--- | :--- | :--- | :--- |
| **SEV-1** | Core failure (Gateway/Auth) | Immediate response via `runbooks/core/` | [Incident History](operations/incidents/) |
| **SEV-2** | Critical degradation (DB/Data) | Response within 4 hours | [Incident History](operations/incidents/) |
| **SEV-3** | Minor/Intermittent issue | Log to GitHub Issues | N/A |

## 4. Change & Release Gates

모든 인프라 변경(Change)은 아래 관문을 통과해야 합니다.

1. **Spec Sync**: 해당 PRD/ARD에 대응하는 [`specs/`](specs/) 업데이트 완료.
2. **Preflight**: [`scripts/preflight-compose.sh`](scripts/preflight-compose.sh) 통과 여부 확인.
3. **Risk Scoring**: 중대한 아키텍처 변경 시 `[REQ-RSK-04]`에 따른 위험도 평가 수행.

## 5. References

- **Infra Lifecycle**: [`docs/context/core/infra-lifecycle-ops.md`](docs/context/core/infra-lifecycle-ops.md)
- **Security Policy**: [`.github/SECURITY.md`](.github/SECURITY.md)
- **RCA Hub**: [`operations/postmortems/README.md`](operations/postmortems/README.md)

---
> [!TIP]
> 운영 절차의 상세 로직은 본 문서에 직접 작성하지 않고 반드시 `runbooks/` 디렉토리를 활용하십시오.
