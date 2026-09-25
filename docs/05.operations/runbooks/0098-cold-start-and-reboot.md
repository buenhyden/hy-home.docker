---
title: "Cold Start and Reboot Runbook"
version: "0.1.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
artifact_id: "RUN-0098"
parent_ids:
- "SPEC-0182"
created: "2026-09-25"
---

# Cold Start and Reboot Runbook

## When to Use

호스트를 계획된 이유로 재부팅하기 전과 재부팅 직후, HOME Docker Compose 스택과
같은 호스트의 hy-home.k8s(k3d) 컨테이너를 안전한 순서로 다시 세우고, 각 단계
사이의 health gate를 확인할 때 사용한다. 정전이나 예정에 없던 재부팅 뒤 같은
순서로 상태를 점검할 때도 쓴다. 이 런북은 unseal share, SecretID, root token,
KV 값을 출력하거나 요청하지 않는다; 실제 재부팅 실행은 owner가 감독 아래
수행하며 이 문서의 범위가 아니다.

Unseal 방식은 [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)의
결정을 따른다: 수동 Shamir unseal 유지, share 3개 threshold 2개,
`secrets/security/openbao_unseal_keys.txt`(SEC-003)에 보관. auto-unseal은
채택되지 않았으므로 이 런북의 모든 단계는 owner가 직접 unseal과 SecretID 전달을
수행한다고 전제한다.

## Procedure

Run commands from the repository root of the running checkout. Never print
secret files, unseal shares, SecretIDs, tokens or the rendered Compose model.

### 0. Preconditions (재부팅 전, owner-run)

재부팅 전에 pgBackRest 백업, Restic 백업, `restic check`을 새로 남긴다.
[RUN-0021](0021-backup-and-restore.md) step 4의
`hyhome-backup.service`가 세 가지를 모두 한 번에 수행한다: pgBackRest 백업,
Restic 백업, 그리고 `restic check`(`infra/09-tooling/restic/bin/hyhome-backup.sh`
안의 `restic check` 호출).

명령과 기대 결과는 [RUN-0021 step 4](0021-backup-and-restore.md#4-run-or-verify-a-backup)를
그대로 사용한다. 실패하면 재부팅을 진행하지 않고
[RUN-0021](0021-backup-and-restore.md)의 문제 해결
절차를 따른다(잠금, 디스크 공간, 5 GiB 예산 초과 등).

### 1. Docker와 Compose 컨테이너 (재부팅 직후)

모든 서비스는 `infra/common-optimizations.yml`의 `restart-default`
(`restart: unless-stopped`)를 상속하므로, Docker daemon이 systemd로 시작하면
직전에 실행 중이던 컨테이너를 daemon이 각자 자동으로 다시 시작한다.

Docker 자체의 부팅 활성화는 이 저장소가 아니라 host systemd 설정에 있다.
2026-09-25 host에서 `systemctl is-enabled docker.service docker.socket`은 둘 다
`enabled`였다. 재부팅 전에 같은 명령으로 다시 확인한다.

Daemon이 개별 컨테이너를 되살리는 방식은 각 서비스의 `depends_on: condition:
service_healthy`(예: `openbao-agent`가 `openbao`를, `mng-pg-exporter`가
`mng-pg`를 기다리는 것)를 다시 평가하지 않는다; 그 조건은 `docker compose up`이
새로 컨테이너를 만들 때만 적용된다. 재부팅 뒤에는 대신 아래 순서대로 각 서비스
자체의 healthcheck로 게이트를 건다. 순서를 강제하려면 재부팅 뒤 `docker compose
up -d`를 다시 실행해 Compose가 依存 그래프를 재확인하게 할 수 있다(**owner
확인 필요**: 현재 이 저장소는 재부팅 직후 `docker compose up -d`를 자동으로
실행하는 systemd 단위를 갖고 있지 않다).

```bash
docker ps --format '{{.Names}} {{.Status}}'
```

Expected: 이전에 실행 중이던 컨테이너가 모두 나열되고, 일부는 `(health:
starting)`에서 각자의 `start_period` 동안 안정화된다.

### 2. 데이터와 인증 기반: `mng-pg`, `mng-valkey`, Traefik, Keycloak

이 서비스들은 `secrets_net`/`edge_net`을 통해 이후 단계(OpenBao OIDC 로그인,
hy-home.k8s)가 의존한다.

```bash
docker exec mng-pg pg_isready -h 127.0.0.1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"
docker inspect --format '{{.State.Health.Status}}' mng-valkey traefik keycloak
```

Expected: `mng-pg`는 `accepting connections`; 나머지 세 컨테이너는
`healthy`. Keycloak의 healthcheck는 `interval 15s`/`timeout 30s`로
`/health/ready`를 확인한다. 이 단계가 안정되지 않으면 이후의 OIDC 로그인
단계(4)가 실패한다.

### 3. OpenBao: sealed 상태로 시작, Agent는 즉시 시작

`infra/03-security/openbao/docker-compose.yml`의 `openbao` healthcheck는
`bao status`의 종료 코드 0(unsealed)과 2(sealed)를 모두 healthy로 본다
(`interval 15s`, `timeout 10s`, `retries 10`, `start_period 20s`). 그래서
`openbao-agent`는 `depends_on: condition: service_healthy`를 곧바로 통과해
sealed 상태의 OpenBao 옆에서 시작한다.

```bash
docker inspect --format '{{.State.Health.Status}}' openbao openbao-agent
docker compose exec -T openbao bao status
```

Expected: 두 컨테이너 모두 `healthy`; `bao status`는 `Sealed  true`를 보여준다.
`openbao-agent`는 이전 재시작에서 남은 토큰 파일이 있으면 자체 healthcheck
(`test -s /openbao/agent/token`)를 통과할 수 있지만, sealed OpenBao에는 아직
인증하지 못한 상태다.

### 4. Owner unseal (대화형, hidden input)

[RUN-0085](0085-openbao.md#initial-bootstrap-and-credential-recovery)의
절차를 따른다: share 2개(threshold)를 대화형 터미널의 숨김 프롬프트에
붙여넣는다. share를 인자로 넘기지 않는다.

```bash
docker compose exec openbao bao operator unseal
docker compose exec openbao bao operator unseal
docker compose exec -T openbao bao status
```

Expected: 두 번째 명령 뒤 `Sealed  false`. 이 단계는 owner가 직접 수행하며
시간(시작·종료)을 아래 Rehearsal Record에 기록한다.

### 5. Owner OIDC 로그인

[RUN-0085 Human Login](0085-openbao.md#human-login-and-normal-root-recovery)의
[guide](../guides/0085-openbao.md)를 따라 role `home-admin`으로
OIDC 로그인한다. 결과 정책이 `default`와 `hy-home-operator`뿐이고 `root`가
아님을 확인한다. Keycloak(2단계)이 `healthy`가 아니면 이 로그인은 실패한다.

### 6. SecretID 발급과 Agent 전달 (owner-run, 10분 이내)

[RUN-0085 delivery 절차](0085-openbao.md#initial-bootstrap-and-credential-recovery)의
명령을 그대로 쓴다. SecretID는 발급 후 10분, 1회용이며 Agent가 읽은 뒤 파일을
지운다. SecretID 전달을 10분 안에 끝내지 못하면 다시 5단계부터 새 SecretID를
발급한다.

### 7. hy-home.k8s(k3d) 컨테이너

k3d 클러스터 노드는 같은 호스트의 Docker 컨테이너(`k3d-hyhome-*`)로 돈다.
이 저장소에는 k3d 노드의 시작을 규정하는 문서나 systemd 단위가 없다. 2026-09-25
host에서 `k3d-hyhome-server-0`, `agent-0`~`agent-2`, `serverlb`의 재시작 정책은
모두 `unless-stopped`였으므로 Docker daemon이 시작하면 함께 돌아온다. 재부팅 전
`docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' <name>`으로 다시 확인하고,
재부팅 뒤 아래로 확인한다.

```bash
docker ps --format '{{.Names}} {{.Status}}' | grep '^k3d-hyhome-'
```

없으면 owner가 `k3d cluster start hyhome`으로 시작한다(hy-home.k8s 저장소 절차를 따른다).
클러스터가 떠 있으면, [hy-home.k8s 통합 runbook](0096-k8s-integration.md)의
읽기 전용 확인을 사용해 External Secrets 동기화를 확인한다. ADR-0042에 따르면
hy-home.k8s의 External Secrets는 Kubernetes auth로 OpenBao를 읽으므로, 4단계
unseal 전에는 동기화하지 못한다.

```bash
KUBECONFIG=$(k3d kubeconfig write hyhome) kubectl get pods -A | grep -i external-secrets
docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'
```

Expected: External Secrets Operator pod가 `Running`이고, 이후 owner가
[0096 runbook](0096-k8s-integration.md)의 7단계
(Prometheus `up{cluster="k3d-hyhome"}`) 확인으로 클러스터 전체 상태를
이어서 검증한다. `k3d-hyhome` 네트워크에는 `k3d-hyhome-*` 컨테이너만 있어야
한다.

### 타이밍 요약

| 단계 | 근거 | 예상 소요 |
| --- | --- | --- |
| 1. Docker/Compose 컨테이너 복귀 | 각 서비스 healthcheck `start_period` | 서비스마다 20~30초 안정화; 전체 시간은 **owner 확인 필요**(호스트마다 다름) |
| 3. OpenBao sealed 시작, Agent 시작 | `openbao` healthcheck `interval 15s`, `start_period 20s` | 약 20~35초 |
| 4. Owner unseal | 대화형, 소요 시간은 owner 입력 속도에 좌우 | **owner 확인 필요**; Rehearsal Record에 기록 |
| 6. SecretID 발급과 전달 | SecretID 유효기간 10분, 1회용 | 10분 이내에 끝나야 함 |
| 7. hy-home.k8s 확인 | k3d 컨테이너 자체 기동 시간 문서화 안 됨 | **owner 확인 필요** |

## Evidence

각 단계의 실행 시각, `docker ps`/`docker inspect`/`bao status`의 상태 문자열,
grep 결과(개수만)를 현재 Task에 기록한다. 원문 로그, secret 값, unseal share,
SecretID, token 값은 기록하지 않는다.

## Rollback or Recovery

- 4단계(unseal)가 실패하면 [RUN-0085](0085-openbao.md)의
  Rollback or Recovery(protected Raft snapshot 복구)를 따른다; 이 런북은 새
  unseal 절차를 만들지 않는다.
- 6단계(SecretID 전달)가 실패하거나 시간을 넘기면 이전 SecretID는 이미
  소모되었으므로 5단계부터 다시 시작한다; Agent volume의 이전 토큰 파일을
  지우지 않는다.
- 0단계의 백업이 실패한 상태로 재부팅을 강행하지 않는다: 재부팅 전 backup과
  `restic check`이 성공할 때까지 재시도한다.
- 데이터베이스나 OpenBao의 복구(스냅샷 복원)는 각각
  [RUN-0021](0021-backup-and-restore.md)과
  [RUN-0085](0085-openbao.md)가 소유한다.

## Escalation

Unseal share, SecretID, root token 발급 승인이 필요하거나, k3d 자동 시작
여부처럼 이 런북이 owner 확인으로 남긴 항목이 실제로 막히면 @buenhyden에게
알린다.

## Verification Record

Owner가 감독하는 재부팅 리허설마다 아래 표에 한 행씩 기록한다. 리허설
실행 자체는 owner-run이며 이 문서의 범위가 아니다.

| Date | Stage | Start | End | Result |
| --- | --- | --- | --- | --- |
| | | | | |

## Traceability

- Governing spec: [SPEC-0182](../../03.specs/0182-home-residual-backlog/spec.md)
  criterion 11, [Plan W11](../../03.specs/0182-home-residual-backlog/plan.md),
  [Task 0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
- Decision: [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)
- Subject runbooks: [RUN-0085 OpenBao](0085-openbao.md),
  [RUN-0021 Backup and Restore](0021-backup-and-restore.md),
  [RUN hy-home.k8s Integration](0096-k8s-integration.md)

## Related Documents

- [Operations index](../README.md)
- [00 Workspace domain](../README.md)
- [Implementation: root Compose](../../../docker-compose.yml),
  [OpenBao Compose](../../../infra/03-security/openbao/docker-compose.yml),
  [common optimizations](../../../infra/common-optimizations.yml)
