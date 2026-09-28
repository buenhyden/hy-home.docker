---
title: "hy-home.k8s Integration Runbook"
version: "1.2.2"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0096"
parent_ids:
- "GDE-0096"
created: "2026-09-23"
---

# hy-home.k8s Integration Runbook

## When to Use

| Situation | Phases |
| --- | --- |
| 통합 최초 설정 | 1 → 8, 순서대로 |
| hy-home.k8s 클러스터 재구축(새 API 서버 CA) | 1, 5 (5.1–5.3 단계와 5.6–5.7 단계), 6, 7, 8 |
| Prometheus API 비밀번호 교체 | 1, [교체](#rotating-the-prometheus-api-credential), 7, 8 |
| Prometheus API나 Grafana KV 항목이 존재하기 전에 수행된 설정 | 1, 5 (5.1a를 포함한 5.1–5.3, 5.4.2를 포함한 5.4, 5.4.3), 7, 8 |
| Kiali Grafana 토큰 만료 예정 | 1, [재발급](#reissuing-the-kiali-grafana-token), 8 |
| Argo CD notifications Slack 토큰 설정 또는 교체 | 1, [Slack 토큰](#setting-or-replacing-the-slack-notifications-token), 8 |
| OpenBao auth mount, policy, role 유실 | 1, 5 (모든 단계), 6, 7, 8 |

모든 단계에 적용되는 규칙:

- HOME 호스트의 저장소 루트에서 작업한다.
- 각 명령은 한 줄로 입력한다. 붙여넣은 줄 연속(line continuation)은
  인자를 조용히 빠뜨릴 수 있다.
- secret 값은 파일이나 숨겨진 프롬프트로만 전달한다. 인자, 채팅, 로그로는
  절대 넘기지 않는다.
- 이름, 불리언, 비-secret 필드만 기록한다.
- 각 단계는 예상 결과로 끝난다. 결과가 일치할 때까지 다음 단계를 시작하지
  않는다.

## Procedure

### Phase 1. Prepare the repository

1.1 로컬 작업을 잃지 않고 `main`을 최신으로 갱신한다:

```bash
git status --short
git switch main && git pull --ff-only
```

`git status`에 만들지 않은 변경 사항이 나오면 폐기하기 전에 멈추고 그
소유자에게 확인한다.

1.2 추적 소스를 검증한다:

```bash
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
```

예상 결과: 둘 다 통과한다.

### Phase 2. Secrets and environment

2.1 private registry와 `.env`(Git-ignored)를 백업한다:

```bash
umask 077; B=secrets/.backup-$(date +%Y%m%d); mkdir -p "$B" && cp -p secrets/SENSITIVE_ENV_VARS.md .env "$B"/
```

2.2 공개 메타데이터를 private registry와 `.env`로 동기화한다:

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata-check
bash scripts/operations/gen-secrets.sh --sync-metadata
```

`METADATA rejected: unsafe, ambiguous, changed or unreadable input`은 private
행이 잘못되었거나(예: 값이 여러 줄에 걸쳐 있음) registry 모드가 `0600`이
아니라는 뜻이다. Troubleshooting을 참고한다. `--sync-metadata` 이후에는 이
점검이 반드시 0으로 종료되어야 한다.

2.3 사용자 이름을 확인하고 누락된 파일을 생성한다:

```bash
grep -c '^PROMETHEUS_API_USERNAME=' .env
bash scripts/operations/gen-secrets.sh
stat -c '%n %s %a' secrets/observability/prometheus_api_password.txt secrets/auth/traefik_prometheus_api_htpasswd.txt
```

예상 결과: `1`, 그리고 두 파일 모두 크기가 0이 아니고 모드가 `640`이다.

### Phase 3. Gateway and Prometheus

3.1 두 consumer를 재생성한다. 단일 파일 secret은 기존 inode를 유지하므로
`INFRA-007` 변경 이후에는 Traefik을 반드시 재생성해야 한다.

```bash
docker compose up -d --no-deps --force-recreate traefik prometheus
docker ps --format '{{.Names}} {{.Status}}' | grep -E '^(traefik|infra-prometheus) '
```

예상 결과: 둘 다 1분 이내에 `Up … (healthy)` 상태가 된다. 컨테이너가
`Created` 상태에 머물거나 기존 컨테이너가 `Exited` 상태이면 `docker compose
up -d --no-deps traefik prometheus`를 다시 실행하고 출력을 확인한다.

3.2 호스트에서 Prometheus API를 검증한다. `prom_auth`는 credential을 curl의
stdin(`-K -`)으로 전달하므로 프로세스 인자에는 절대 나타나지 않는다:

```bash
prom_auth() { printf 'user = "%s:%s"\n' "$(grep '^PROMETHEUS_API_USERNAME=' .env | cut -d= -f2 | tr -d '"')" "$(cat secrets/observability/prometheus_api_password.txt)"; }
curl -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/api/v1/status/buildinfo
prom_auth | curl -K - -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/api/v1/status/buildinfo
curl -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/graph
```

예상 결과: `401`, `200`, 그리고 UI 경로에서는 `401`이다(SSO 체인이 인증되지
않은 요청에 응답하며, 브라우저는 이후 SSO 로그인 페이지를 거친다).

### Phase 4. Host endpoints

4.1 k3d 네트워크에 남은 것이 없는지, 게시된 포트가 응답하는지 확인한다:

```bash
docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'
for p in 443 3100 3200 26379; do timeout 2 bash -c "</dev/tcp/192.168.0.13/$p" && echo "$p open" || echo "$p closed"; done
```

예상 결과: 해당 네트워크에 Compose 컨테이너가 없고(`k3d-hyhome-*` 노드만
있거나, 클러스터와 네트워크가 사라진 경우 오류가 발생), 네 포트 모두 열려
있다. 여기에 아직 남아 있는 Compose 컨테이너는 k3d 제거 이전의 것이므로
`docker network disconnect k3d-hyhome <name>`으로 분리한다(재시작은 하지
않는다).

### Phase 5. OpenBao Kubernetes auth

5.1 새 클러스터 CA(public)를 private 작업 디렉터리에 기록한다:

```bash
umask 077; mkdir -p /tmp/bao-k8s
KUBECONFIG=$(k3d kubeconfig write hyhome) kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d >/tmp/bao-k8s/k3d-ca.crt
```

5.1a Kiali Grafana 토큰을 같은 디렉터리에 발급한다(최초 설정, Session 3, 또는
[재발급](#reissuing-the-kiali-grafana-token)). Grafana는 익명 접근을 허용하지
않으므로 Kiali는 Viewer service account `k8s-kiali`의 토큰을 전송한다.
`graf_auth`는 3.2의 `prom_auth`와 마찬가지로 admin credential을 curl의
stdin으로 전달한다:

```bash
graf_auth() { printf 'user = "%s:%s"\n' "$(grep '^GRAFANA_ADMIN_USERNAME=' .env | cut -d= -f2 | tr -d '"')" "$(cat secrets/observability/grafana_admin_password.txt)"; }
SA=$(graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem 'https://grafana.hy.home.arpa/api/serviceaccounts/search?query=k8s-kiali' | jq -r '.serviceAccounts[] | select(.name=="k8s-kiali") | .id')
[ -n "$SA" ] || SA=$(graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem -H 'Content-Type: application/json' -d '{"name":"k8s-kiali","role":"Viewer"}' https://grafana.hy.home.arpa/api/serviceaccounts | jq -r '.id')
graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem -H 'Content-Type: application/json' -d "{\"name\":\"k8s-kiali-$(date +%Y%m%d)\",\"secondsToLive\":7776000}" "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens" | jq -j '.key' >/tmp/bao-k8s/grafana-kiali.token
printf 'header = "Authorization: Bearer %s"\n' "$(cat /tmp/bao-k8s/grafana-kiali.token)" | curl -K - -s -o /dev/null -w '%{http_code}\n' --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://grafana.hy.home.arpa/api/search
curl -s -o /dev/null -w '%{http_code}\n' --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://grafana.hy.home.arpa/api/search
```

예상 결과: 토큰이 있으면 `200`, 없으면 `401`이다. 토큰 수명은 90일이다.
값이 아니라 만료일만 기록한다. 이 service account는 Viewer 역할만 유지한다.

5.2 호스트 네트워크에서 호스트 사용자로 임시(throwaway) client를 기동한다.
호스트에는 `bao` CLI가 없고, 마운트된 파일은 호스트 uid가 필요하며, OIDC
콜백은 `localhost:8250`에서 대기한다. 이미지는
[OpenBao Compose 파일](../../../infra/03-security/openbao/docker-compose.yml)이
고정한 것을 사용한다. 브라우저가 다른 곳에서 실행되면 먼저
`ssh -L 8250:localhost:8250 <host>`로 포트를 포워딩한다.

```bash
IMG=$(docker compose config --images openbao)
docker run --rm -it --network host --user "$(id -u):$(id -g)" -e HOME=/tmp -e BAO_ADDR=https://openbao.hy.home.arpa -e BAO_CACERT=/ca.pem -v "$PWD/secrets/certs/rootCA.pem:/ca.pem:ro" -v "$PWD/infra/03-security/openbao/config/policies:/policies:ro" -v "$PWD/secrets/db/valkey/mng_password.txt:/s/valkey:ro" -v "$PWD/secrets/observability/prometheus_api_password.txt:/s/prom:ro" -e PROM_API_USER="$(grep '^PROMETHEUS_API_USERNAME=' .env | cut -d= -f2 | tr -d '"')" -v /tmp/bao-k8s:/s/k8s --entrypoint sh "$IMG"
```

이 단계의 나머지 절차는 컨테이너 내부에서 실행한다.

5.3 OIDC operator로 로그인하고 스냅샷을 생성한다:

```sh
umask 077; mkdir -p /tmp/c
bao login -no-print -method=oidc -path=oidc role=home-admin
bao operator raft snapshot save /s/k8s/pre-change.snap   # or a name for the change, e.g. pre-prometheus-api.snap
```

예상 결과: 브라우저 로그인이 성공하고 스냅샷 파일이 존재한다. 이 파일 없이는
진행하지 않는다. `/s/k8s`는 호스트의 `/tmp/bao-k8s`이므로 스냅샷은 Phase 8이
옮기기 전까지 그곳에만 있다. 해당 디렉터리 전체는 절대 삭제하지
않는다.

5.4 **임시 root**(최초 설정, 또는 추가 애플리케이션). 승인된 root 세션과
`secrets/security/openbao_unseal_keys.txt`에서 가져온 서로 다른 unseal
share 두 개가 필요하며, 각각 숨겨진 프롬프트에 붙여넣는다. `R`은 명령마다
root를 전달하므로 절대 export되지 않는다.

```sh
bao operator generate-root -init -format=json > /tmp/c/init.json
NONCE=$(sed -n 's/.*"nonce": *"\([^"]*\)".*/\1/p' /tmp/c/init.json); OTP=$(sed -n 's/.*"otp": *"\([^"]*\)".*/\1/p' /tmp/c/init.json)
bao operator generate-root -nonce="$NONCE" -format=json > /tmp/c/p1.json
bao operator generate-root -nonce="$NONCE" -format=json > /tmp/c/p2.json
ENC=$(sed -n 's/.*"encoded_token": *"\([^"]*\)".*/\1/p' /tmp/c/p2.json); bao operator generate-root -decode="$ENC" -otp="$OTP" > /tmp/c/root
R() { BAO_TOKEN="$(cat /tmp/c/root)" bao "$@"; }
R token lookup -format=json | grep -c '"root"'
```

예상 결과: `1` 이상이다. 다음 `R` 명령에서 `0`이나 `403`이 나오면
`/tmp/c/root`가 없거나 비어 있고 `bao`가 operator 로그인 토큰으로 대체된
것이다. `generate-root -status`로 확인하고 `bao operator generate-root -cancel`로 오래된 시도를 취소한 다음 절차를 다시 실행한다.

client 컨테이너는 자신을 시작한 체크아웃의 policy를 마운트한다. 적용할 policy
변경이 병합되고 pull된 이후에만 세션을 시작한다. 그렇지 않으면 `R policy write`가 이전 파일을 적용한다.

그다음 5.4.1(최초 설정) 또는 5.4.2(추가 애플리케이션)를 실행하고, 항상
5.4.3을 실행한다.

5.4.1 최초 설정: method를 활성화하고 policy, role, KV 항목을 작성한다.

```sh
R auth list -format=json | grep -q '"kubernetes/"' || R auth enable kubernetes
R policy write eso-read-platform /policies/eso-read-platform.hcl
R policy write k8s-bootstrap /policies/k8s-bootstrap.hcl
R policy write hy-home-operator /policies/operator.hcl
R write auth/kubernetes/role/eso-read-platform bound_service_account_names=external-secrets bound_service_account_namespaces=external-secrets audience=vault token_policies=eso-read-platform token_ttl=1
R write auth/token/roles/k8s-bootstrap allowed_policies=k8s-bootstrap orphan=true token_explicit_max_ttl=2h
R kv put secret/platform/argocd valkey_password=@/s/valkey
R kv put secret/platform/prometheus-api username="$PROM_API_USER" password=@/s/prom
R kv put secret/platform/grafana-api token=@/s/k8s/grafana-kiali.token
R read -field=bound_service_account_namespaces auth/kubernetes/role/eso-read-platform
```

예상 결과: `[external-secrets]`. `secret/platform/argocd`(Argo CD Valkey
비밀번호)와 `secret/platform/prometheus-api`(Prometheus API credential,
`INFRA-007`과 같은 출처: `PROMETHEUS_API_USERNAME`과
`prometheus_api_password.txt`), `secret/platform/grafana-api`(5.1a의 Kiali
Grafana 토큰)가 필요하다. k8s 앱이 사용하는 경우에만 같은 방식으로
`secret/platform/postgres-app` `{db_name,username,password}`와
`secret/platform/notifications` `{slack_token}`을 추가한다.

5.4.2 추가 애플리케이션(Session 3): Prometheus API와 Grafana 항목, role
상한이 존재하기 전에 설정된 환경에 적용한다. 먼저 5.1a를 실행한다:

```sh
R policy write eso-read-platform /policies/eso-read-platform.hcl
R policy write hy-home-operator /policies/operator.hcl
R policy read eso-read-platform | grep -cE 'platform/(prometheus|grafana)-api'
R policy read hy-home-operator | grep -cE 'platform/(prometheus|grafana)-api'
R kv put secret/platform/prometheus-api username="$PROM_API_USER" password=@/s/prom
R kv put secret/platform/grafana-api token=@/s/k8s/grafana-kiali.token
R kv metadata get -format=json secret/platform/prometheus-api | grep '"current_version"'
R kv metadata get -format=json secret/platform/grafana-api | grep '"current_version"'
R write auth/token/roles/k8s-bootstrap allowed_policies=k8s-bootstrap orphan=true token_explicit_max_ttl=2h
```

예상 결과: `4`, `4`, 그리고 각 `current_version`이 최소 `1`이다.

5.4.3 token role을 검증한 다음 root를 폐기한다:

```sh
R read -field=token_explicit_max_ttl auth/token/roles/k8s-bootstrap
R token revoke -self
R token lookup >/dev/null 2>&1 && echo "ROOT STILL VALID" || echo "root revoked"
bao operator generate-root -status | grep -i started
```

예상 결과: `7200`, `root revoked`, `Started false`이다. 추가 애플리케이션
이후에는 클러스터 구성이 바뀌지 않았으므로 Phase 7로 진행한다.

5.5 method를 클러스터로 지정한다:

```sh
bao write auth/kubernetes/config kubernetes_host=https://192.168.0.13:6550 kubernetes_ca_cert=@/s/k8s/k3d-ca.crt disable_local_ca_jwt=true
bao read -field=kubernetes_host auth/kubernetes/config
```

예상 결과: `https://192.168.0.13:6550`.

5.6 bootstrap 토큰을 파일로 발급한다:

```sh
bao write -field=token auth/token/create/k8s-bootstrap ttl=2h explicit_max_ttl=2h > /s/k8s/k8s-bootstrap.token
```

5.7 토큰 자신으로 검증한 다음(operator는 다른 토큰을 조회할 수 없다),
컨테이너를 나간다:

```sh
T="$(cat /s/k8s/k8s-bootstrap.token)"
BAO_TOKEN="$T" bao token lookup -format=json | grep -E '"(policies|orphan|ttl|explicit_max_ttl)"' -A2
BAO_TOKEN="$T" bao read -format=json secret/data/platform/argocd >/dev/null 2>&1 && echo "argocd read: allowed" || echo "argocd read: DENIED"
BAO_TOKEN="$T" bao read -format=json secret/data/hy-home/02-auth/keycloak >/dev/null 2>&1 && echo "keycloak read: LEAK" || echo "keycloak read: denied"
unset T
exit
```

예상 결과: policy는 `default`와 `k8s-bootstrap`, orphan은 `true`, `ttl`과
`explicit_max_ttl`은 최대 `7200`, `argocd read: allowed`,
`keycloak read: denied`이다. 하나라도 다르면 토큰을 폐기하고(Troubleshooting
참고) 중단한다.

### Phase 6. Hand off to hy-home.k8s

다음을 클러스터 소유자에게 전달한다. 두 secret 파일은 보호된 채널로
보낸다.

| Item | Source |
| --- | --- |
| Bootstrap 토큰(2시간 이내 사용) | `/tmp/bao-k8s/k8s-bootstrap.token` |
| Prometheus API credential | OpenBao `secret/platform/prometheus-api`(`username`, `password`), ESO가 동기화; 출처는 `.env`의 `PROMETHEUS_API_USERNAME`과 `secrets/observability/prometheus_api_password.txt` |
| Kiali Grafana 토큰 | OpenBao `secret/platform/grafana-api`(`token`), ESO가 동기화; 5.1a에서 발급 |
| Gateway CA(public) | `secrets/certs/rootCA.pem` |
| Endpoints | [가이드](../guides/0096-k8s-integration.md)의 contract 표 |

이후 클러스터 소유자가 자기 쪽 변경을 적용한다:

- ESO service account에 대한 `system:auth-delegator` 바인딩
- `openbao.hy.home.arpa`, `prometheus.hy.home.arpa`, `grafana.hy.home.arpa`의 DNS → `192.168.0.13`
- CA 신뢰
- 443, 3100, 3200, 26379 포트로의 egress
- Basic Auth credential과 `cluster` external label을 사용하는 Alloy remote write 및 Kiali
- bearer 토큰을 사용하는 Kiali의 Grafana 연결

### Phase 7. Verify from both sides

7.1 클러스터 측에서 소유자는 ESO `SecretStore`가 유효하고 Argo CD
`ExternalSecret`이 동기화되었는지 확인한다. ready 상태만 기록한다.

7.2 호스트 측에서 클러스터의 샘플이 도착하는지 확인한다(3.2의 `prom_auth`
사용):

```bash
prom_auth | curl -K - -s --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem --data-urlencode 'query=count by (job) (up{cluster="k3d-hyhome"})' https://prometheus.hy.home.arpa/api/v1/query
```

예상 결과: 클러스터 job마다 결과가 하나씩(예: `kubernetes-pods`,
`kubelet`) 나온다. 이는 hy-home.k8s가 metrics NodePort를 폐지하기 전에
필요한 증거다.

### Phase 8. Clean up and record

```bash
rm -f /tmp/bao-k8s/k8s-bootstrap.token /tmp/bao-k8s/grafana-kiali.token /tmp/bao-k8s/slack.token /tmp/bao-k8s/metrics.token /tmp/bao-k8s/secret_id /tmp/bao-k8s/*.custody /tmp/bao-k8s/*.hcl
install -d -m 700 secrets/backup/openbao
mv /tmp/bao-k8s/*.snap secrets/backup/openbao/
rmdir /tmp/bao-k8s 2>/dev/null || ls -l /tmp/bao-k8s
```

`secrets/backup/`는 소유자 전용이며, `.gitignore`가 그 안의 `*.txt`와
`*.snap` 파일을 제외한다. 여기 둔 파일은 같은 호스트의 임시 사본이다. 스냅샷을
[backup and restore policy](../policies/0021-backup-and-restore.md)가
요구하는 별도의 오프라인 custody로 복사한 다음, 그 policy의 retention에 따라
호스트 사본을 보관하거나 삭제한다.

결과 확인 후 Phase 2 백업 디렉터리를 삭제한다. 현재 Task에 날짜, 실행한
단계, 그리고 3.2, 4.1, 5.4, 5.5, 5.7, 7.2의 예상 출력을 기록한다. 토큰,
share, 비밀번호, KV 값은 절대 기록하지 않는다.

### Rotating the Prometheus API credential

이 비밀번호는 세 곳에 있고 세 곳 모두 함께 바꿔야 한다:

- `OBS-013`, 파일 자체
- `INFRA-007`, 여기서 파생된 Traefik htpasswd
- 클러스터가 읽는 OpenBao 항목

OpenBao를 갱신하지 않으면 클러스터의 remote write가 `401`을 받는다. OIDC
operator는 root 세션 없이 해당 항목을 갱신할 수 있다.

1. 기존 파일을 옮기고 새 파일을 생성한다. 기존 해시가 더 이상 검증되지
   않으므로 `gen-secrets.sh`가 `INFRA-007`을 다시 파생시킨다:

   ```bash
   umask 077; B=secrets/.backup-$(date +%Y%m%d); mkdir -p "$B" && mv secrets/observability/prometheus_api_password.txt "$B"/
   bash scripts/operations/gen-secrets.sh
   ```

2. Traefik을 재생성하고 3.2 점검(`401`, `200`)을 반복한다:

   ```bash
   docker compose up -d --no-deps --force-recreate traefik
   ```

3. operator로 OpenBao를 갱신한 다음(5.2 client 컨테이너, 5.3 로그인)
   컨테이너를 나간다:

   ```sh
   bao kv put secret/platform/prometheus-api username="$PROM_API_USER" password=@/s/prom
   bao kv metadata get -format=json secret/platform/prometheus-api | grep '"current_version"'
   ```

   예상 결과: `current_version`이 이전보다 1 높다.
4. 클러스터 소유자에게 Prometheus secret의 ESO refresh를 강제하도록 요청한
   다음 7.2를 실행한다.
5. 7.2가 통과하면 백업에서 기존 파일을 삭제한다.

### Reissuing the Kiali Grafana token

5.1a의 토큰은 90일 동안 유효하다. OIDC operator는 root 세션 없이 해당
항목을 교체할 수 있다.

1. 새 토큰 이름으로 5.1a를 실행한다(날짜 접미사로 충분하다).
2. operator로 OpenBao를 갱신한 다음(5.2 client 컨테이너, 5.3 로그인)
   컨테이너를 나간다:

   ```sh
   bao kv put secret/platform/grafana-api token=@/s/k8s/grafana-kiali.token
   bao kv metadata get -format=json secret/platform/grafana-api | grep '"current_version"'
   ```

   예상 결과: `current_version`이 이전보다 1 높다.
3. ESO refresh를 강제한 다음 Kiali pod를 재생성한다. Kiali는 시작할 때
   토큰을 읽으므로 Secret만 갱신해서는 기존 토큰이 그대로 남는다.

   ```bash
   kubectl -n istio-system annotate externalsecret kiali-grafana-auth force-sync="$(date +%s)" --overwrite
   kubectl -n istio-system delete pod -l app=kiali
   kubectl -n istio-system rollout status deploy/kiali --timeout=180s
   ```

   pod를 삭제해도 Deployment spec은 변경되지 않으므로 Argo CD에는 drift가
   나타나지 않는다. Kiali를 한 번 열거나(또는 `/kiali/api/grafana`를
   호출) 토큰 목록을 조회해 새 토큰의 `lastUsedAt`이 가장 최근인지
   확인한다:

   ```bash
   graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens" | jq -r '.[] | "\(.id) \(.name) expires=\(.expiration) lastUsed=\(.lastUsedAt)"'
   graf_auth | curl -K - -s -o /dev/null -w '%{http_code}\n' -X DELETE --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens/<old id>"
   ```

   예상 결과: 새 토큰이 가장 최근에 사용되었고 이전 토큰은 `200`이다.

### Setting or replacing the Slack notifications token

`secret/platform/notifications`(`slack_token`)는 hy-home.k8s의
`argocd-notifications-secret`에 값을 공급한다. 이 항목은 COMM-004의
incoming-webhook URL이 아니라 Slack bot 토큰(`xoxb-`)을 사용한다. operator
policy는 SPEC-0181부터 이 경로를 허용한다. `hy-home-operator` policy가 그
이전인 환경에서는 먼저 root 세션 하나(5.4)로 `R policy write hy-home-operator
/policies/operator.hcl`을 실행해야 한다.

1. 호스트에서 `umask 077` 상태로 편집기를 열어 `/tmp/bao-k8s/slack.token`을
   생성한다. 토큰을 `echo`하지 않는다.
2. operator로 OpenBao를 갱신한다(5.2 client 컨테이너, 5.3 로그인):

   ```sh
   bao kv put secret/platform/notifications slack_token=@/s/k8s/slack.token
   bao kv metadata get -format=json secret/platform/notifications | grep '"current_version"'
   ```

   예상 결과: `current_version`이 이전보다 1 높다(최초에는 `1`).
3. `/tmp/bao-k8s/slack.token`을 삭제한 다음 ESO refresh를 강제하고 Argo CD
   application을 확인한다:

   ```bash
   kubectl -n argocd annotate externalsecret argocd-notifications-secret force-sync="$(date +%s)" --overwrite
   kubectl -n argocd get externalsecret argocd-notifications-secret
   kubectl -n argocd get application platform-argocd-config -o jsonpath='{.status.sync.status} {.status.health.status}{"\n"}'
   ```

   예상 결과: `SecretSynced`, `True`, 그다음 `Synced Healthy`이다.

### Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| 2.2에서 `METADATA rejected` | private 행이 잘못됨(값이 여러 줄에 걸침) 또는 registry 모드가 `0600`이 아님 | 백업하고 값이 해당 파일과 일치하는지 확인하고 행을 예시 행으로 교체하고 `chmod 600` 후 2.2를 다시 실행 |
| 2.3 이후 secret 파일이 0바이트 | 해당 ID가 private registry에 없음 | 먼저 2.2를 완료한 다음 2.3을 다시 실행 |
| `curl`이 `000`을 출력 | 이름이 해석되지 않거나 gateway가 다운됨 | `--resolve` 사용; 3.1 확인 |
| credential과 함께 `401` | Traefik이 여전히 기존 `usersFile` inode를 사용 중 | Traefik 재생성(3.1) |
| `/s/k8s/...`에서 `permission denied` | client가 자체 사용자로 실행됨 | `--user "$(id -u):$(id -g)"`로 재시작(5.2) |
| `key is required` | share 프롬프트에 빈 입력 | 같은 `-nonce` 명령을 다시 실행하고 share를 붙여넣기 |
| `bound_service_account_namespaces can not be empty` | 줄 연속으로 인자가 누락됨 | role write를 한 줄로 다시 실행 |
| `Must supply data or use -force` | 파라미터 없이 token create 실행 | `ttl=2h explicit_max_ttl=2h`를 포함(5.6) |
| `bao token lookup <token>`에서 `403` | operator는 다른 토큰을 조회할 수 없음 | 토큰 자신으로 조회(5.7) |
| bootstrap 토큰 TTL이 약 32일 | token role이 `token_ttl`/`token_max_ttl`을 무시하여 role에 상한이 없었음 | `BAO_TOKEN="$(cat /s/k8s/k8s-bootstrap.token)" bao token revoke -self`를 실행하고 5.6으로 재발급한 다음, 다음 root 세션에서 role에 `token_explicit_max_ttl=2h`를 설정 |
| `ROOT STILL VALID` | 폐기 실패 | 중단하고 에스컬레이션, 세션은 열어 둠 |
| 교체 이후 클러스터 remote write가 `401` | OpenBao `secret/platform/prometheus-api`가 여전히 이전 비밀번호를 보유 | 교체 3단계, 그다음 ESO refresh |
| Kiali가 Grafana에 연결할 수 없거나 `401`을 표시 | `secret/platform/grafana-api`가 없거나, 만료되었거나, 토큰이 삭제됨 | 토큰 재발급, 그다음 ESO refresh |
| 7.2에서 `cluster="k3d-hyhome"` 시리즈가 없음 | 클러스터 sender가 구성되지 않았거나 443에 도달할 수 없음 | 클러스터 소유자가 Alloy 로그, DNS, CA, egress를 확인 |

## Evidence

Phase 8에 나열된 단계 출력, 소스 커밋, "When to Use"에서 적용된 상황을
기록한다.

## Rollback or Recovery

- **Prometheus API:** `prometheus-api` router label을 제거하고 Prometheus를
  재생성한다. UI 경로는 영향을 받지 않는다.
- **OpenBao:** 5.3의 스냅샷(`secrets/backup/openbao/` 또는 그 오프라인
  사본)이 복구 지점이다. 복원은 OpenBao 런북의 격리된 절차로만 한다.
- **Bootstrap 토큰:** 단독으로 폐기한다(Troubleshooting 참고).
- **Private registry와 `.env`:** Phase 2 백업에서 복원한다.

## Escalation

`ROOT STILL VALID`, `secret/platform/*` 밖을 읽는 토큰, 클러스터를 위해
OpenBao 앞에 SSO나 허용목록을 두라는 요청, 또는 인증 없이 Prometheus나
Grafana를 게시하라는 요청이 있으면 중단하고 @buenhyden에게 연락한다.

## Traceability

- [Guide](../guides/0096-k8s-integration.md) (`GDE-0096`)
- [Policy](../policies/0096-k8s-integration.md) (`POL-0096`)
- [OpenBao runbook](0085-openbao.md)

## Related Documents

- [Prometheus guide](../guides/0045-prometheus.md)
- [Secrets README](../../../secrets/README.md)
