---
title: "Qdrant Health and Recovery Triage Runbook"
version: "2.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-28"
layer: "operations"
artifact_id: "RUN-0034"
parent_ids:
- "GDE-0034"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Qdrant Health and Recovery Triage Runbook

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the runbook payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

범위: root에 포함된 Qdrant 서비스의 상태, SSO 뒤의 REST route 전제, 영속 경로, 증거 수집을 파괴적 데이터 작업 없이 점검한다.

이 런북은 health triage와 별도 승인 후 수행할 Qdrant snapshot의 격리 복원 rehearsal 계약을 제공한다. 이번 변경에서 snapshot create/recover API나 storage mutation은 실행하지 않았다.

Qdrant single unprivileged service의 상태, `/readyz` healthcheck, SSO 뒤의 REST Traefik route, snapshot path evidence를 수집하고 compose가 보장하는 범위 안에서만 비파괴 조치를 수행한다.

- `qdrant`가 unhealthy, stopped 또는 missing 상태일 때
- `/readyz`가 200을 반환하지 않을 때
- REST route `qdrant.${DEFAULT_URL}`(SSO 뒤) 경계를 확인해야 할 때
- Qdrant operations 문서와 현재 compose evidence를 함께 갱신해야 할 때

##### Targets

- Declared parent: [Qdrant Usage Guide](../../01.guides/09.ai-and-search/0034-qdrant.md) (`GDE-0034`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../02.architecture/01.descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../../01.guides/09.ai-and-search/0034-qdrant.md) (`GDE-0034`), [Policy](../../02.policies/09.ai-and-search/0034-qdrant.md) (`POL-0034`)

- [Compose implementation: infra/04-data/qdrant/docker-compose.yml](../../../../infra/04-data/qdrant/docker-compose.yml)

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)

- [Operations index](../../README.md)
- [Usage guide](../../01.guides/09.ai-and-search/0034-qdrant.md)
- [Operations policy](../../02.policies/09.ai-and-search/0034-qdrant.md)
- [Infra README](../../../../infra/04-data/qdrant/README.md)

#### Preflight

##### Authority

대상 service는 `qdrant`이며 운영 checkout의 repository root와 승인된 Docker context를 확인한다. API key 파일은 `secrets/data/qdrant/qdrant_api_key.txt`와 `secrets/data/qdrant/qdrant_read_only_api_key.txt`이며 값은 읽지 않고 존재만 확인한다. 책임자는 저장소 소유자 @buenhyden이다.

대상 service는 `qdrant`이며 승인된 Docker context 확인과 기동·정지·upgrade 승인은 Stop Conditions의 `Execution and stop boundary`에 있다. API key 파일은 `secrets/data/qdrant/qdrant_api_key.txt`와 `secrets/data/qdrant/qdrant_read_only_api_key.txt`이며 값은 읽지 않고 존재만 확인한다(Environment). 에스컬레이션 대상은 저장소 소유자 @buenhyden이다(Escalation).

##### Environment

먼저 다음을 확인한다.

- [ ] 루트 compose에서 `infra/04-data/qdrant/docker-compose.yml`가 active include인지 확인한다.
- [ ] `secrets/data/qdrant/qdrant_api_key.txt`와 `secrets/data/qdrant/qdrant_read_only_api_key.txt`가 있고 비어 있지 않은지 값을 읽지 않고 확인한다(`test -s`).
- [ ] collection delete, snapshot recovery, volume replacement, cluster repair가 필요한 경우 이 런북을 중단하고 에스컬레이션한다.
- [ ] 모든 명령 출력은 요약으로 기록하고 application data payload는 기록하지 않는다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | compose 렌더링을 확인한다 | `docker compose --profile qdrant config --quiet`가 통과한다 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | 서비스 상태를 확인한다 | `qdrant`가 running 또는 healthy 상태다 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 3 | 최근 로그를 확인한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 4 | REST readiness를 확인한다 | `/readyz`가 200 response evidence를 제공한다 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 5 | read-only collection inventory를 확인한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 6 | 컨테이너가 stopped이고 데이터 작업이 불필요하면 compose로 재기동한다 | 문서에 기록 없음 | 데이터/소유권/credential이 불명확하면 중단하고 @buenhyden에게 escalation |
| 7 | Planned Isolated Restore Rehearsal: 사전 승인 후 source version, collection, alias, point count, snapshot 범위, free disk를 기록한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 8 | Planned Isolated Restore Rehearsal: snapshot을 생성하고 manifest/checksum과 함께 보호한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 9 | Planned Isolated Restore Rehearsal: production과 분리된 fresh target을 준비하고 free disk와 target collection 부재를 확인한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 10 | Planned Isolated Restore Rehearsal: snapshot type에 맞는 upstream recovery 절차 하나만 사용한다 | 문서에 기록 없음 | `force`는 별도 승인 없이 쓰지 않고 중단하여 @buenhyden에게 escalation |
| 11 | Planned Isolated Restore Rehearsal: `/readyz`, collection status/config, alias, point count, search invariant를 검증한다 | 문서에 기록 없음 | version/checksum/count mismatch면 승격하지 않는다 |
| 12 | Planned Isolated Restore Rehearsal: 실패 시 target을 보존하고 정확한 소유 target 삭제는 별도 승인 후 수행한다 | 문서에 기록 없음 | 실패한 target과 증거를 보존하고 @buenhyden에게 escalation |

1. compose 렌더링을 확인한다.

   ```bash
   docker compose --profile qdrant config --quiet
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps qdrant
   ```

3. 최근 로그를 확인한다.

   ```bash
   docker compose logs --tail=120 qdrant
   ```

4. REST readiness를 확인한다.

   ```bash
   # 6333 is the default QDRANT_PORT; substitute it if changed.
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /readyz HTTP/1.0\r\n\r\n" >&3; cat <&3'
   ```

5. read-only collection inventory를 확인한다.

   ```bash
   docker compose exec qdrant bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333; printf "GET /collections HTTP/1.0\r\napi-key: %s\r\n\r\n" "$(tr -d "\r\n" </run/secrets/qdrant_api_key)" >&3; cat <&3'
   ```

6. 컨테이너가 stopped 상태이고 데이터 작업이 필요하지 않은 경우 compose로 재기동한다.

   ```bash
   docker compose --profile qdrant up -d --no-deps qdrant
   ```

###### Remote Program Access (blog-data `vault-notes`)
<!-- core-payload-level:4 -->

서버 B의 blog-data는 `qdrant-api` router로만 들어온다. Ollama는 기존 `ollama-api` 계정(`AI-012`·`AI-013`, [RUN-0056](0056-ollama.md))을 그대로 쓴다.

1. 자격(`AI-015`)과 Traefik hash(`INFRA-010`)는 owner가 만든다. 사용자 이름은 `.env`의 `QDRANT_API_USERNAME`(`AI-014`)이다.
   값은 화면·인자·로그에 내지 않는다. Traefik 재생성으로 모든 route가 몇 초 끊기고, Qdrant 재생성은 JWT RBAC를 켠다.

   ```bash
   umask 077
   mkdir -p secrets/tools/qdrant
   f=secrets/tools/qdrant/qdrant_api_password.txt
   h=secrets/auth/traefik/traefik_qdrant_api_htpasswd.txt
   u=$(sed -n 's/^QDRANT_API_USERNAME="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' .env)
   [ -n "$u" ] && openssl rand -hex 24 | tr -d '\n' > "$f" &&
     htpasswd -iBn "$u" < "$f" | head -1 > "$h.new" && chmod 640 "$h.new" && mv "$h.new" "$h" &&
     docker compose --profile core up -d --no-deps --force-recreate traefik &&
     docker compose --profile qdrant up -d --no-deps --force-recreate qdrant
   ```

2. 플러그인용 `vault-notes` 읽기 전용 JWT를 만든다. JWT RBAC는 token을 `qdrant_api_key`로 서명해 확인하므로 새로 저장할 secret이 없다.
   token은 출력하지 않고 0700 임시 디렉터리의 0600 파일로만 쓴 뒤 OpenBao에 넣고 그 디렉터리를 지운다. `qdrant_api_key`를 회전하면 token도 다시 만든다.

   ```bash
   t=$(mktemp -d) && python3 - secrets/data/qdrant/qdrant_api_key.txt "$t/vault-notes-read.jwt" <<'PY'
   import base64, hashlib, hmac, json, os, sys
   b = lambda x: base64.urlsafe_b64encode(x).rstrip(b"=")
   key = open(sys.argv[1], "rb").read().strip()
   head = b(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
   body = b(json.dumps({"access": [{"collection": "vault-notes", "access": "r"}]}, separators=(",", ":")).encode())
   sig = b(hmac.new(key, head + b"." + body, hashlib.sha256).digest())
   fd = os.open(sys.argv[2], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
   os.write(fd, head + b"." + body + b"." + sig)
   os.close(fd)
   PY
   ```

3. blog-data에는 OpenBao로만 전달한다. 받는 쪽 환경변수는 `VAULT_SEARCH_OLLAMA_BASIC_AUTH`(`AI-012`:`AI-013`),
   `VAULT_SEARCH_QDRANT_BASIC_AUTH`(`AI-014`:`AI-015`), `VAULT_SEARCH_QDRANT_API_KEY`(`AI-008`), `VAULT_RELATED_QDRANT_API_KEY`(2번 JWT)다.
   회신에는 OpenBao 경로와 계정 이름만 남긴다.
4. 서버 B에서 확인한다. 맞는 Basic과 `api-key`로 `GET /collections/vault-notes`는 404(처음) 또는 200, 틀린 Basic은 401,
   읽기 전용 JWT로 `PUT /collections/vault-notes/points`는 403, `GET /collections`(목록)는 SSO로 302, 서버 B가 아닌 출발지는 403이다.
   서버 A에서는 Prometheus의 Qdrant target이 계속 `up`이고 기존 `api-key` 호출이 그대로 되는지도 본다.

Rollback: `qdrant-api` label, `qdrant-api-auth` middleware, `traefik_qdrant_api_htpasswd` secret과 `QDRANT__SERVICE__JWT_RBAC`를 되돌리고
Traefik과 Qdrant를 다시 만든다. `vault-notes` collection은 blog-data가 다시 만들 수 있다.

###### Planned Isolated Restore Rehearsal
<!-- core-payload-level:4 -->

1. 사전 승인 후 source engine minor version, collection list/config/status, aliases, point-count invariants, snapshot scope/identifier와 free disk를 기록한다. API key가 켜져 있는지도 기록한다.
2. approved collection or full-storage snapshot을 생성하고 `/qdrant/storage/snapshots`에서 manifest/checksum과 함께 보호한다. snapshot API response나 vector payload를 evidence에 복사하지 않는다.
3. production network/route/volume을 공유하지 않는 fresh target을 same minor 또는 upstream이 허용하는 next minor로 준비한다. snapshot 크기의 약 2배 free disk와 absent target collection을 확인한다.
4. collection snapshot recovery API 또는 full-storage startup recovery 중 snapshot type에 맞는 upstream procedure 하나만 사용한다. `force`는 target collision이 명시적으로 검토된 경우에만 별도 승인한다.
5. `/readyz`, collection status/config, aliases, point counts와 representative search invariants를 검증한다. version, checksum 또는 count mismatch면 승격하지 않는다.
6. 실패하면 target을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. production route switch, API key 교체, collection deletion과 volume replacement는 별도 승인 사항이다.

##### Stop Conditions

중단 조건은 아래 항목에 기록한다.

###### Execution and stop boundary
<!-- core-payload-level:4 -->

대상: `qdrant`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../../01.guides/01.common/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../../02.policies/01.common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

서비스 점검은 아래 항목에 따른다.

###### Verification Steps
<!-- core-payload-level:4 -->

- `docker compose ps qdrant`에서 `qdrant`가 running 또는 healthy 상태인지 확인한다.
- `/readyz`가 200 response evidence를 제공하는지 확인한다.
- `docker compose --profile qdrant config --quiet`가 통과하는지 확인하고, source Compose에서 `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`가 유지되는지 비교한다.

###### Evidence
<!-- core-payload-level:4 -->

- 명령 이름, pass/fail 상태, service 상태, image tag, 민감 정보를 제거한 log, route label과 readiness 요약을 기록한다.
- vector payload, collection data, credential 또는 mutation API body는 기록하지 않는다.
- 문제가 container health, REST route, network 내부 gRPC, 영속성 또는 snapshot-path 증상 중 어디와 관련되는지 기록한다.

###### Observability and Evidence Sources
<!-- core-payload-level:4 -->

- **Logs**: `docker compose logs --tail=120 qdrant`
- **Health**: `/readyz` and compose healthcheck
- **Route**: Traefik HTTP labels on `qdrant` with SSO; no gRPC route
- **Config**: `docker compose --profile qdrant config --quiet`

##### Unverified Conditions

이 런북이 아직 관찰하지 못한 항목은 다음과 같다. 문서는 이번 변경에서 snapshot create/recover API나 storage mutation을 실행하지 않았다고 기록하며, static source 점검만 승인된 경우 모든 runtime command는 `NOT_RUN`이다.

- Planned Isolated Restore Rehearsal 전체(snapshot 생성, fresh target 복원): 별도 승인 후 격리 target에서 `/readyz`, collection status/config, alias, point count가 source와 일치하는 증거가 필요하다.
- compose 재기동(6단계): owner 승인 후 `docker compose ps qdrant`에서 running 또는 healthy를 관찰해야 한다.
- 1~5단계 runtime 점검: 이 문서에는 실행 결과가 기록되어 있지 않다. `docker compose --profile qdrant config --quiet` 통과와 `/readyz` 200 기록이 필요하다.

#### Escalation

##### Next Owner

restart 후에도 `/readyz`가 실패하거나, log에 storage 손상이 나타나거나, route label이 예상한 compose와 다르거나, API key가 없어 client가 401을 받거나, data 작업이 필요하면 저장소 소유자 @buenhyden에게 에스컬레이션한다. 민감 정보를 제거한 log, 렌더링된 compose evidence, service 상태와 시도한 단계를 포함한다.

##### Recovery or Forward Repair

데이터 복구는 위 planned isolated rehearsal로만 검증한다. 이번 변경에서는 snapshot mutation, collection restore/delete, volume replacement와 route change를 실행하지 않았다.

1. 이 Runbook의 runtime 복구는 evidence 수집 후 `docker compose --profile qdrant up -d --no-deps qdrant`를 실행하는 범위로 제한한다.
2. 실패한 isolated target과 전용 volume을 보존하고, 정확한 소유 target의 삭제는 별도 승인 후 수행한다. source service, snapshot과 tracked volume은 변경하지 않는다.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
