# Operations Index

이 문서는 `hy-home.docker`의 운영 정책 인덱스입니다.
실행 가능한 절차는 반드시 [`runbooks/`](runbooks/)의 개별 문서를 기준으로 수행합니다.

- 기술 배경/구성 원리: [`docs/context/README.md`](docs/context/README.md)
- 실행 절차 모음: [`runbooks/README.md`](runbooks/README.md)
- 아키텍처 규칙: [`ARCHITECTURE.md`](ARCHITECTURE.md)

## 1. 운영 원칙

1. **Runbook-First**: 장애 대응/복구 절차는 인덱스가 아닌 [`runbooks/`](runbooks/)에서 실행
2. **Validate-Then-Apply**: 변경 전후 [`scripts/validate-docker-compose.sh`](scripts/validate-docker-compose.sh)로 구성 검증
3. **Secrets Hygiene**: 비밀값은 `secrets/**/*.txt` + Docker secrets만 사용
4. **Port Governance**: Host 포트는 `*_HOST_PORT`, 컨테이너 포트는 `*_PORT`로 관리

## 2. Day-0 Bootstrap

초기 기동은 아래 순서를 권장합니다.

```bash
cp .env.example .env
bash scripts/generate-local-certs.sh
bash scripts/preflight-compose.sh
docker compose up -d
```

관련 문서:

- 부트스트랩 런북: [`runbooks/core/infra-bootstrap-runbook.md`](runbooks/core/infra-bootstrap-runbook.md)
- 라이프사이클 개요: [`docs/context/core/infra-lifecycle-ops.md`](docs/context/core/infra-lifecycle-ops.md)

## 3. Day-1 운영 명령

```bash
# Compose 유효성 검증
bash scripts/validate-docker-compose.sh

# 서비스 단위 갱신
docker compose up -d --no-deps <service>

# 로그/상태 점검
docker compose logs -f <service>
docker compose ps

# 종료/정리
docker compose down
```

리소스 정리는 [`runbooks/core/docker-resource-maintenance.md`](runbooks/core/docker-resource-maintenance.md)를 따릅니다.

## 4. Incident Runbook Catalog

| Category | Procedure | Location |
| :--- | :--- | :--- |
| Core | Infra Bootstrap / Preflight | [`runbooks/core/infra-bootstrap-runbook.md`](runbooks/core/infra-bootstrap-runbook.md) |
| Gateway | Traefik Recovery | [`runbooks/01-gateway/traefik-proxy-recovery.md`](runbooks/01-gateway/traefik-proxy-recovery.md) |
| Auth | Keycloak Lockout Recovery | [`runbooks/02-auth/auth-lockout.md`](runbooks/02-auth/auth-lockout.md) |
| Security | Vault Unseal/Recovery | [`runbooks/03-security/vault-sealed.md`](runbooks/03-security/vault-sealed.md) |
| Data | PostgreSQL HA Recovery | [`runbooks/04-data/postgres-ha-recovery.md`](runbooks/04-data/postgres-ha-recovery.md) |
| Data | MinIO Sync Failure Recovery | [`runbooks/04-data/minio-sync-failure.md`](runbooks/04-data/minio-sync-failure.md) |
| Messaging | Kafka Cluster Operations | [`runbooks/05-messaging/kafka-cluster-ops.md`](runbooks/05-messaging/kafka-cluster-ops.md) |
| Observability | LGTM Stack Maintenance | [`runbooks/06-observability/observability-stack-maintenance.md`](runbooks/06-observability/observability-stack-maintenance.md) |
| Workflow | Airflow Celery Recovery | [`runbooks/07-workflow/airflow-celery-recovery.md`](runbooks/07-workflow/airflow-celery-recovery.md) |
| Core | Incident Response | [`runbooks/core/incident-response-runbook.md`](runbooks/core/incident-response-runbook.md) |

런북이 없으면 [`templates/operations/runbook-template.md`](templates/operations/runbook-template.md) 기반으로 신규 작성 후 본 문서에 링크를 추가합니다.

## 5. Incident Severity

- **SEV-1**: 핵심 서비스 불능. 즉시 [`runbooks/core/incident-response-runbook.md`](runbooks/core/incident-response-runbook.md) 실행
- **SEV-2**: 핵심 기능 성능/가용성 저하
- **SEV-3**: 부분 기능 장애 또는 우회 가능한 이슈

## 6. Change & Release Gates

변경 반영 전 최소 게이트:

1. 관련 [`specs/`](specs/)/문서 반영 완료
2. `bash` [`scripts/validate-docker-compose.sh`](scripts/validate-docker-compose.sh) 통과
3. 필요한 시크릿 파일/인증서 존재 확인 ([`scripts/preflight-compose.sh`](scripts/preflight-compose.sh))
4. 운영 영향이 있는 경우 관련 runbook 업데이트

## 7. DR Baseline

- 백업/복구 정책은 [`runbooks/`](runbooks/)와 서비스별 블루프린트 기준으로 운영
- 권고 목표:
  - **RTO**: Tier-1 기준 4시간 이내
  - **RPO**: 1시간 이내

세부 정책은 [`docs/context/core/infra-lifecycle-ops.md`](docs/context/core/infra-lifecycle-ops.md)와 각 데이터 계층 문서를 따릅니다.

## 8. References

- Compose/Env/Secrets 감사 문서: [`docs/context/core/infra-compose-optimization-audit.md`](docs/context/core/infra-compose-optimization-audit.md)
- 보안 정책: [`.github/SECURITY.md`](.github/SECURITY.md)

---

운영 절차의 상세 명령/분기 로직은 본 문서에 직접 쓰지 않고 반드시 [`runbooks/`](runbooks/)에 둡니다.
