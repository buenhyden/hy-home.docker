# Service Runbook: Core Infra Bootstrap (Docker Compose)

_Target Directory: `runbooks/core/infra-bootstrap-runbook.md`_
_Scope: root `docker-compose.yml` include된 Core stack의 “첫 부팅(boot-ready)” 절차._

---

## 1. Service Overview & Ownership

- **Description**: 로컬/개발 환경에서 core infra stack을 `docker compose up -d` 한 번으로 기동하기 위한 prerequisites 준비 및 검증 절차.
- **Owner Team**: Infra / Platform
- **Primary Contact**: `N/A` (프로젝트 정책에 맞게 채워주세요)

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Docker Engine | Tooling | 전체 부팅 불가 | `runbooks/core/deployment-runbook.md` |
| Docker Compose v2 | Tooling | `docker compose` 명령 불가 | `runbooks/core/deployment-runbook.md` |
| mkcert | Tooling | 로컬 TLS 인증서 생성 불가 | N/A |

## 3. Observability & Dashboards

- **Core UIs (Traefik 라우팅 기준)**:
  - Traefik dashboard: `https://dashboard.${DEFAULT_URL}`
  - Grafana: `https://grafana.${DEFAULT_URL}`
  - Prometheus: `https://prometheus.${DEFAULT_URL}`
  - Alertmanager: `https://alertmanager.${DEFAULT_URL}`
- **SLOs/SLIs**: N/A (로컬 부팅 runbook)
- **Alert Definitions**: N/A (로컬 부팅 runbook)

## 4. Alerts & Common Failures

### Scenario A: PostgreSQL HA(Patroni) secret 파일 누락으로 실패

- **Symptoms**: PostgreSQL cluster 관련 secret 파일 누락 또는 preflight 실패
- **Investigation Steps**:
  1. `ls -la secrets/db/postgres/patroni_superuser_password.txt`
  2. `ls -la secrets/db/postgres/patroni_replication_password.txt`
- **Remediation Action**:
  - [ ] `secrets/db/postgres/patroni_superuser_password.txt`에 superuser 비밀번호를 설정 (커밋 금지)
  - [ ] `secrets/db/postgres/patroni_replication_password.txt`에 replication 비밀번호를 설정 (커밋 금지)
- **Expected Outcome**: `bash scripts/preflight-compose.sh`와 `docker compose config`가 통과한다.

### Scenario B: Traefik TLS 인증서 파일 누락

- **Symptoms**: `secrets/certs/cert.pem` 또는 `key.pem`가 없어서 TLS 라우팅이 실패하거나 로그에 오류가 발생
- **Investigation Steps**:
  1. `ls -la secrets/certs`
  2. Traefik TLS 설정 확인: `infra/01-gateway/traefik/dynamic/tls.yaml`
- **Remediation Action**:
  - [ ] `bash scripts/generate-local-certs.sh`
  - [ ] 또는 수동 생성: 아래 “Bootstrap Steps” 참고
- **Expected Outcome**: `secrets/certs/{rootCA.pem,cert.pem,key.pem}` 3개 파일이 존재한다.

### Scenario C: 호스트 bind mount 디렉토리/권한 문제로 컨테이너가 CrashLoop/Unhealthy

- **Symptoms**: 특정 서비스가 `permission denied`, `no such file or directory`로 종료하거나 healthcheck가 실패
- **Investigation Steps**:
  1. `.env`에서 `${DEFAULT_DATA_DIR}`, `${DEFAULT_OBSERVABILITY_DIR}` 등 실제 경로 확인
  2. 해당 경로가 존재하는지 확인: `ls -la <path>`
- **Remediation Action**:
  - [ ] 필요한 디렉토리 생성: `mkdir -p <path>`
  - [ ] UID/GID 정합(가이드): `chown -R 1000:1000 <path>` (로컬 정책에 맞게 조정)
- **Expected Outcome**: 서비스가 정상 기동하고 healthcheck가 통과한다.

## 5. Safe Rollback Procedure

- [ ] **Step 1**: 현재 상태 확인: `docker compose ps`
- [ ] **Step 2**: core stack 종료: `docker compose down`
- [ ] **Step 3**: 필요 시 볼륨 정리(데이터 삭제 주의): `docker compose down -v`
- [ ] **Step 4**: 재시도 전 prerequisites 재검증: `docker compose config`

## 6. Data Safety Notes (If Stateful)

- Core stack에는 상태 저장 서비스(PostgreSQL/Valkey/OpenSearch/MinIO/Prometheus/Grafana 등)가 포함된다.
- `docker compose down -v`는 데이터를 삭제할 수 있다. 실수 방지를 위해 기본 rollback은 `docker compose down`만 사용한다.

## 7. Escalation Path

1. **Primary On-Call**: `N/A` (프로젝트 정책에 맞게 채워주세요)
2. **Secondary Escalation**: `N/A`
3. **Management Escalation (SEV-1)**: `N/A`

## 8. Verification Steps (Post-Fix)

### Bootstrap Steps (Deterministic)

1. **Secrets 확인**
   - [ ] 루트 secrets registry 기준으로 파일이 존재해야 한다: `docker-compose.yml`의 `secrets:` 섹션
   - [ ] 대표적으로 다음은 “core 부팅”에서 자주 필요하다:
     - `secrets/common/{smtp_username.txt,smtp_password.txt,slack_webhook.txt}`
     - `secrets/auth/{keycloak_admin_password.txt,oauth2_proxy_client_secret.txt,oauth2_proxy_cookie_secret.txt,traefik_basicauth_password.txt,traefik_opensearch_basicauth_password.txt}`
     - `secrets/observability/grafana_admin_password.txt`
     - `secrets/storage/{minio_root_username.txt,minio_root_password.txt,minio_app_username.txt,minio_app_user_password.txt}`
     - `secrets/data/{opensearch_admin_password.txt,opensearch_dashboard_password.txt,opensearch_exporter_password.txt}`
     - `secrets/db/postgres/{service_password.txt,mng_password.txt,keycloak_password.txt,...}`

2. **PostgreSQL cluster env_file 준비**
   - [ ] `.env.postgres`는 더 이상 사용하지 않는다.
   - [ ] Patroni 비밀번호 secret 파일 2개를 준비한다:
     - `secrets/db/postgres/patroni_superuser_password.txt`
     - `secrets/db/postgres/patroni_replication_password.txt`

3. **로컬 TLS 인증서 준비 (mkcert)**
   - [ ] 목표 파일: `secrets/certs/rootCA.pem`, `secrets/certs/cert.pem`, `secrets/certs/key.pem`
   - [ ] 권장: `bash scripts/generate-local-certs.sh`
   - [ ] 수동 생성이 필요하면 mkcert 설치 후:
     - `mkcert -install`
     - `mkdir -p secrets/certs`
     - `mkcert -cert-file secrets/certs/cert.pem -key-file secrets/certs/key.pem \"*.${DEFAULT_URL}\" \"${DEFAULT_URL}\"`
     - `cp \"$(mkcert -CAROOT)/rootCA.pem\" secrets/certs/rootCA.pem`

4. **(필요 시) 외부 네트워크 생성**
   - [ ] `project_net`, `kind`는 core 부팅에 필수로 강제하지 않는다.
   - [ ] 만약 `docker compose config` 또는 `up`에서 external network 관련 오류가 나면:
     - `docker network create project_net`
     - `docker network create kind`

5. **구성 렌더링 검증**
   - [ ] 사전 점검: `bash scripts/preflight-compose.sh`
   - [ ] `docker compose config`

6. **부팅**
   - [ ] `docker compose up -d`
   - [ ] 상태 확인: `docker compose ps`

7. **Core health smoke checks**
   - [ ] Traefik: `docker exec traefik traefik healthcheck --ping`
   - [ ] Keycloak: `docker compose ps`에서 healthy 표기 확인 (또는 해당 서비스 healthcheck)
   - [ ] MinIO: `docker compose ps`에서 healthy 표기 확인
   - [ ] PostgreSQL cluster: `docker compose ps`에서 `pg-0/1/2` healthy 표기 확인
   - [ ] OpenSearch: `docker compose ps`에서 healthy 표기 확인 (yellow 허용 정책은 spec에 따름)
   - [ ] Prometheus/Grafana/Alertmanager: `docker compose ps`에서 healthy 표기 확인
