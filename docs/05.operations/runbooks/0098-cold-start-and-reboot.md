---
title: "Cold Start and Reboot Runbook"
version: "0.3.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0098"
parent_ids:
- "SPEC-0182"
created: "2026-09-25"
---

# Cold Start and Reboot Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

호스트를 계획된 이유로 재부팅하기 전과 재부팅 직후, HOME Docker Compose 스택과
같은 호스트의 hy-home.k8s(k3d) 컨테이너를 안전한 순서로 다시 세우고, 각 단계
사이의 health gate를 확인할 때 사용한다. 정전이나 예정에 없던 재부팅 뒤 같은
순서로 상태를 점검할 때도 쓴다. 이 런북은 unseal share, SecretID, root token,
KV 값을 출력하거나 요청하지 않는다; 실제 재부팅 실행은 owner가 감독 아래
수행하며 이 문서의 범위가 아니다.

Unseal 방식은 [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)의
결정을 따른다: 수동 Shamir unseal 유지, share 3개 threshold 2개,
`secrets/security/openbao/openbao_unseal_keys.txt`(SEC-003)에 보관. auto-unseal은
채택되지 않았으므로 이 런북의 모든 단계는 owner가 직접 unseal과 SecretID 전달을
수행한다고 전제한다.

## Procedure

### Procedure

실행 중인 checkout의 저장소 root에서 명령을 수행한다. secret file, unseal share,
SecretID, token, 렌더링된 Compose model을 출력하지 않는다. 현재 Task에 host·project·
승인된 profile/service와 재부팅 전 expected container 집합을 기록한다.

### 0. Preconditions (재부팅 전, owner-run)

재부팅 전에 pgBackRest 백업, Restic 백업, `restic check`을 새로 남긴다.
[RUN-0021](0021-backup-and-restore.md) step 4의
`hyhome-backup.service`가 세 가지를 모두 한 번에 수행한다: pgBackRest 백업,
Restic 백업, 그리고 `restic check`(`infra/09-platform-ops/restic/bin/hyhome-backup.sh`
안의 `restic check` 호출).

명령과 기대 결과는 [RUN-0021 step 4](0021-backup-and-restore.md#4-run-or-verify-a-backup)를
그대로 사용한다. 실패하면 재부팅을 진행하지 않고
[RUN-0021](0021-backup-and-restore.md)의 문제 해결
절차를 따른다(잠금, 디스크 공간, 5 GiB 예산 초과 등).

### 1. Docker와 Compose 컨테이너 (재부팅 직후)

지속 실행 service는 선택한 template의 `restart: unless-stopped` 등 실제 선언을
따른다. 초기화·migration 같은 one-shot job의 `restart: "no"`는 자동 복귀 대상이
아니다. Docker daemon은 각 container의 실제 restart policy와 이전 중지 상태에
따라 복귀시킨다. 전체 선언이나 과거 실행 수를 현재 expected 집합으로 간주하지 않는다.

Docker 자체의 부팅 활성화는 이 저장소가 아니라 host systemd 설정에 있다.

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, RUN-0098 step1, 2026-09-25.
> 2026-09-25 host에서 `systemctl is-enabled docker.service docker.socket`은 둘 다
> `enabled`였다.

재부팅 전에 같은 명령으로 다시 확인한다.

Daemon이 개별 컨테이너를 되살리는 방식은 각 서비스의 `depends_on: condition:
service_healthy`(예: `openbao-agent`가 `openbao`를, `mng-pg-exporter`가
`mng-pg`를 기다리는 것)를 다시 평가하지 않는다; 그 조건은 `docker compose up`이
새로 컨테이너를 만들 때만 적용된다. 재부팅 뒤에는 아래 순서대로 각 service의 health와 readiness를
확인한다. `docker compose up -d`는 단순 순서 검사가 아니라 생성·시작·재생성 및
선택에 따라 init job 실행을 일으킬 수 있다. missing/failed service는 해당 owner가
정확한 project/profile/service와 dependency를 확인하고 service RUN의 승인된
mutation 분기로 처리한다. 저장소에 재부팅 직후 전체 `up -d`를 실행하는 systemd
단위는 없다.

```bash
docker compose ps -a --format json
```

예상 결과: 현재 project의 예상 지속 실행 service가 복귀하고 job은 의도한 종료
상태다. 누락·추가·Exited·반복 재시작은 owner와 확인한다. `start_period`는 실패
계수의 유예 기간이며 시작 완료 SLA가 아니다. 상태 JSON의 이름·상태만 기록한다.

### 2. 데이터와 인증 기반: `mng-pg`, `mng-valkey`, Traefik, Keycloak

이 service들은 이후 OpenBao OIDC·hy-home.k8s 기능의 기반이다. `mng-pg`는
`mng_data_net`의 관리 DB 경로를 사용한다. 모든 기반 service가 `secrets_net`과
`edge_net`을 공유한다고 가정하지 않고 해당 Compose membership을 확인한다.

```bash
docker exec mng-pg sh -c 'pg_isready -h 127.0.0.1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
docker inspect --format '{{.State.Health.Status}}' mng-valkey traefik keycloak
```

예상 결과: `mng-pg`는 `accepting connections`; 나머지 세 컨테이너는
`healthy`. Keycloak의 healthcheck는 `interval 15s`/`timeout 30s`로
`/health/ready`를 확인한다. 이 단계가 안정되지 않으면 이후의 OIDC 로그인
단계(4)가 실패한다.

### 3. OpenBao: sealed 상태와 Agent 재시작 상태 확인

`infra/03-security/openbao/docker-compose.yml`의 `openbao` healthcheck는
`bao status`의 종료 코드 0(unsealed)만 healthy로 본다
(`interval 15s`, `timeout 10s`, `retries 10`, `start_period 20s`).
sealed(2) 상태에서는 새 `docker compose up`의 `openbao-agent`가 `service_healthy` 의존성을 통과하지 못한다. Docker daemon의 기존 컨테이너 자동 재시작은 이 의존성을 재평가하지 않아 Agent가 먼저 시작할 수 있다.

```bash
docker inspect --format '{{.State.Health.Status}}' openbao
docker compose exec -T openbao bao status
```

예상 결과: OpenBao가 시작한 뒤 `bao status`로 sealed/unsealed를 구분한다.
sealed의 종료2는 서버가 살아 있어도 `unhealthy`인 상태다. 4단계의 owner unseal 뒤
서버 health가 회복되어야 새 Compose 기동의 Agent가 시작된다. 기존 Agent의 daemon 자동 재시작은 먼저 일어날 수 있고, 남은 token 파일로 health를 통과할 수 있으므로
현재 인증·renewal·렌더링을 별도로 검증한다. 재부팅 뒤 새 SecretID 필요 여부는 RUN-0085로 판단한다.

### 4. Owner unseal (대화형, hidden input)

[RUN-0085](0085-openbao.md)의 수동 unseal 계약을 따른다. 기존
초기화된 storage를 사용하며 bootstrap/init·root 재발급을 시작하지 않는다: share 2개(threshold)를 대화형 터미널의 숨김 프롬프트에
붙여넣는다. share를 인자로 넘기지 않는다.

```bash
docker compose exec openbao bao operator unseal
docker compose exec openbao bao operator unseal
docker compose exec -T openbao bao status
```

예상 결과: 두 번째 명령 뒤 `Sealed  false`. 이 단계는 owner가 직접 수행하며
시간(시작·종료)을 아래 Rehearsal Record에 기록한다.

### 5. Owner OIDC 로그인

[RUN-0085 Human Login](0085-openbao.md#human-login-and-normal-root-recovery)의
[guide](../guides/0085-openbao.md)를 따라 role `home-admin`으로
OIDC 로그인한다. 결과 정책이 `default`와 `hy-home-operator`뿐이고 `root`가
아님을 확인한다. Keycloak(2단계)이 `healthy`가 아니면 이 로그인은 실패한다.

### 6. SecretID 발급과 Agent 전달 (owner-run, 10분 이내)

[RUN-0085 Renderer SecretID Delivery](0085-openbao.md#renderer-secretid-delivery)의
현재 절차와 검증 항목 전체를 실행한다. 5단계의 UI 로그인과 별개로, 그 절차의 1단계에서 CLI
OIDC 로그인을 한 번 더 한다. SecretID는 발급 후 10분, 1회용이며 Agent가 읽은 뒤
파일을 지운다. 10분 안에 끝내지 못하면 그 절차의 2단계부터 새 SecretID를 발급한다.

```bash
docker logs --since 2m openbao-agent 2>&1 | grep -c 'authentication successful'
docker exec openbao-agent sh -c 'test -e /openbao/agent/secret_id && echo not-consumed || echo consumed'
```

위 개수와 `consumed`는 보조 신호이며 통과 조건 전체가 아니다. SecretID 파일의
부재만으로 성공을 판정하지 않는다. RUN-0085에 따라 새 auth 성공, unsealed,
renewal, 허용/금지 읽기, 두 renderer 출력과0600 권한·일치 boolean을 확인한다.
발급 시각과 결과를 현재 Task에 기록한다. 이전 token으로 health만 통과하는 경우를
현재 렌더링 성공으로 기록하지 않는다.

### 7. hy-home.k8s(k3d) 컨테이너

k3d 클러스터 노드는 같은 호스트의 Docker 컨테이너(`k3d-hyhome-*`)로 돈다.
이 저장소에는 k3d 노드의 시작을 규정하는 문서나 systemd 단위가 없다.

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, RUN-0098 step7, 2026-09-25.
> 2026-09-25
> host에서 `k3d-hyhome-server-0`, `agent-0`~`agent-2`, `serverlb`의 재시작 정책은
> 모두 `unless-stopped`였으므로 Docker daemon이 시작하면 함께 돌아온다.

 재부팅 전
`docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' <name>`으로 다시 확인하고,
재부팅 뒤 아래로 확인한다.

```bash
docker ps --format '{{.Names}} {{.Status}}' | grep '^k3d-hyhome-'
```

없으면 현재 cluster inventory와 이전 stop 의도를 확인하고 중단한다. 기존 cluster
시작이 승인된 경우에만 hy-home.k8s owner가 그 저장소 절차에 따라
`k3d cluster start hyhome`을 실행한다. 이는 상태 변경이며 cluster 재구축 권한은 아니다.
클러스터가 떠 있으면, [hy-home.k8s 통합 runbook](0096-k8s-integration.md)의
읽기 전용 확인을 사용해 External Secrets 동기화를 확인한다. ADR-0042에 따르면
hy-home.k8s의 External Secrets는 Kubernetes auth로 OpenBao를 읽으므로, 4단계
unseal 전에는 동기화하지 못한다.

```bash
# 이미 승인된 KUBECONFIG/context를 사용한다. kubeconfig write는 실행하지 않는다.
kubectl get pods -A | grep -i external-secrets
docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'
```

예상 결과: External Secrets Operator pod가 `Running`이고, 이후 owner가
[0096 runbook](0096-k8s-integration.md)의 7단계
(fresh ESO 인증/동기화와 선택 consumer 검증)을 이어서 확인한다.
Prometheus 시리즈 count나 pod Running만으로 클러스터 전체 건강을 선언하지 않는다. `k3d-hyhome` 네트워크에는 `k3d-hyhome-*` 컨테이너만 있어야
한다.

### 타이밍 요약

| 단계 | 근거 | 예상 소요 |
| --- | --- | --- |
| 1. Docker/Compose 컨테이너 복귀 | 각 서비스 healthcheck `start_period` | 현재 선택·host 상태에 따라 달라짐. 2026-09-30 리허설의 약16.5분 daemon 복귀/약19분 healthy는 아래 과거 기록에만 적용되며 현재 SLA가 아님 |
| 3. OpenBao sealed 및 Agent 상태 확인 | `openbao` healthcheck `interval 15s`, `start_period 20s` | health 상태와 실제 unsealed/auth 결과를 각각 관찰; 고정 완료 시간 없음 |
| 4. Owner unseal | 대화형, 소요 시간은 owner 입력 속도에 좌우 | **owner 확인 필요**; Rehearsal Record에 기록 |
| 6. SecretID 발급과 전달 | SecretID 유효기간 10분, 1회용 | 10분 이내에 끝나야 함 |
| 7. hy-home.k8s 확인 | k3d 컨테이너 자체 기동 시간 문서화 안 됨 | **owner 확인 필요** |

## Verification

### Evidence

각 단계의 실행 시각, `docker ps`/`docker inspect`/`bao status`의 상태 문자열,
grep 결과(개수만)를 현재 Task에 기록한다. 원문 로그, secret 값, unseal share,
SecretID, token 값은 기록하지 않는다.

### Verification Record

아래 표는 2026-09-30 실행 기록을 원문 그대로 보존한 것이다. 새로운 리허설은
현재 Task에 별도 기록하며 이 표가 현재 readiness나 실행 권한을 제공하지 않는다.

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, RUN-0098 Verification Record, 2026-09-30.

<!-- Historical evidence table (not current authority; source: Git history). -->

| Date | Stage | Start | End | Result |
| --- | --- | --- | --- | --- |
| 2026-09-30 | 0. Preconditions | 09:37:52 KST | 09:39:07 KST | PASS: pgBackRest diff, two Restic snapshots, `restic check` no errors |
| 2026-09-30 | 1. Docker and containers | 09:44:30 KST (boot) | 10:03:53 KST | PASS: `docker.service` active at 10:01:23 (started 09:44:47; the API did not answer while it restored containers); the 54 containers running before are back, none missing or extra; five dependants of Keycloak and the DB restarted 4-5 times, then all healthy |
| 2026-09-30 | 2. `mng-pg`, `mng-valkey`, Traefik, Keycloak | 10:03:53 KST | 10:03:53 KST | PASS: accepting connections; three healthy |
| 2026-09-30 | 3. OpenBao sealed start | 09:45:14 KST | 10:03:53 KST | PASS: `openbao` and `openbao-agent` healthy, `Sealed true` |
| 2026-09-30 | 4-5. Unseal and OIDC login (owner) | not recorded | before 10:10:05 KST | PASS: `Sealed false`, active leader; owner reported the `home-admin` login |
| 2026-09-30 | 6. SecretID delivery (owner, RUN-0085) | before 10:30:27 KST | 10:30:29 KST | PASS: Agent restarted 10:30:27, `authentication successful` 10:30:29, SecretID `consumed`, token renewed, no error after the restart |
| 2026-09-30 | 7. k3d | 10:03:53 KST | 10:31 KST | PASS: five `k3d-hyhome-*` Up, 38 pods Running; `vault-backend` revalidated `Ready=True` at 10:11:17 after the unseal, and all six ExternalSecrets `SecretSynced` |

## Rollback and Escalation

### Rollback or Recovery

- 4단계(unseal)가 실패하면 중단하고 [RUN-0085](0085-openbao.md)의 credential·
  cluster 상태 진단과 owner escalation을 따른다. unseal 실패만으로 Raft snapshot을
  복원하지 않는다. 데이터 손상 근거와 별도 복구 승인이 있을 때만 격리된 restore를 사용한다.
- 6단계(SecretID 전달)가 실패하거나 시간을 넘기면
  [RUN-0085](0085-openbao.md#renderer-secretid-delivery)의 실패 처리를 따라 새
  SecretID를 발급한다. CLI 세션이 끝났으면 그 절차의 1단계부터 다시 시작한다.
  Agent volume의 `role_id`와 이전 token 파일은 지우지 않는다.
- 0단계의 백업이 실패한 상태로 재부팅을 강행하지 않는다: 재부팅 전 backup과
  `restic check`이 성공할 때까지 재시도한다.
- 데이터베이스나 OpenBao의 복구(스냅샷 복원)는 각각
  [RUN-0021](0021-backup-and-restore.md)과
  [RUN-0085](0085-openbao.md)가 소유한다.

### Escalation

Unseal share, SecretID, root token 발급 승인이 필요하거나, k3d 자동 시작
여부처럼 이 런북이 owner 확인으로 남긴 항목이 실제로 막히면 @buenhyden에게
알린다.

### Traceability

- 과거 구현·리허설 근거: [SPEC-0182](../../03.specs/0182-home-residual-backlog/spec.md)
  criterion 11, [Plan W11](../../03.specs/0182-home-residual-backlog/plan.md),
  [Task 0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
- 현재 결정: [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)
- 관련 runbook: [RUN-0085 OpenBao](0085-openbao.md),
  [RUN-0021 Backup and Restore](0021-backup-and-restore.md),
  [RUN hy-home.k8s Integration](0096-k8s-integration.md)

## Related Documents

- [Operations index](../README.md)
- [00 Workspace domain](../README.md)
- [Implementation: root Compose](../../../docker-compose.yml),
  [OpenBao Compose](../../../infra/03-security/openbao/docker-compose.yml),
  [common optimizations](../../../infra/common-optimizations.yml)
