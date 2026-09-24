---
title: "hy-home.k8s Integration Runbook"
version: "1.2.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
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
| First setup of the integration | 1 → 8, in order |
| hy-home.k8s cluster rebuilt (new API server CA) | 1, 5 (steps 5.1–5.3 and 5.6–5.7), 6, 7, 8 |
| Prometheus API password rotated | 1, [rotation](#rotating-the-prometheus-api-credential), 7, 8 |
| Setup done before the Prometheus API or Grafana KV entry existed | 1, 5 (5.1–5.3 with 5.1a, 5.4 with 5.4.2, 5.4.3), 7, 8 |
| Kiali Grafana token expiring | 1, [reissue](#reissuing-the-kiali-grafana-token), 8 |
| Argo CD notifications Slack token set or replaced | 1, [Slack token](#setting-or-replacing-the-slack-notifications-token), 8 |
| OpenBao auth mount, policy or role lost | 1, 5 (all steps), 6, 7, 8 |

Rules for every phase:

- Work from the repository root on the HOME host.
- Type each command on one line. A pasted line continuation can silently
  drop arguments.
- Secret values go through files or hidden prompts, never arguments, chat or
  logs.
- Record only names, booleans and non-secret fields.
- Each phase ends with an expected result. Do not start the next phase until
  it matches.

## Procedure

### Phase 1. Prepare the repository

1.1 Bring `main` up to date without losing local work:

```bash
git status --short
git switch main && git pull --ff-only
```

If `git status` lists changes you did not make, stop and ask their owner
before discarding them.

1.2 Validate the tracked source:

```bash
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
```

Expected: both pass.

### Phase 2. Secrets and environment

2.1 Back up the private registry and `.env` (Git-ignored):

```bash
umask 077; B=secrets/.backup-$(date +%Y%m%d); mkdir -p "$B" && cp -p secrets/SENSITIVE_ENV_VARS.md .env "$B"/
```

2.2 Synchronize public metadata into the private registry and `.env`:

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata-check
bash scripts/operations/gen-secrets.sh --sync-metadata
```

`METADATA rejected: unsafe, ambiguous, changed or unreadable input` means a
private row is malformed (for example a value spanning lines) or the registry
mode is not `0600`; see Troubleshooting. After `--sync-metadata`, the check
must exit 0.

2.3 Confirm the username and generate missing files:

```bash
grep -c '^PROMETHEUS_API_USERNAME=' .env
bash scripts/operations/gen-secrets.sh
stat -c '%n %s %a' secrets/observability/prometheus_api_password.txt secrets/auth/traefik_prometheus_api_htpasswd.txt
```

Expected: `1`, then both files with a non-zero size and mode `640`.

### Phase 3. Gateway and Prometheus

3.1 Recreate the two consumers. Traefik must be recreated after `INFRA-007`
changes, because a single-file secret keeps its old inode.

```bash
docker compose up -d --no-deps --force-recreate traefik prometheus
docker ps --format '{{.Names}} {{.Status}}' | grep -E '^(traefik|infra-prometheus) '
```

Expected: both `Up … (healthy)` within a minute. If a container stays in
`Created` or the old one is `Exited`, run `docker compose up -d --no-deps
traefik prometheus` again and read its output.

3.2 Verify the Prometheus API from the host. `prom_auth` writes the credential
to curl's stdin (`-K -`), so it never appears in a process argument:

```bash
prom_auth() { printf 'user = "%s:%s"\n' "$(grep '^PROMETHEUS_API_USERNAME=' .env | cut -d= -f2 | tr -d '"')" "$(cat secrets/observability/prometheus_api_password.txt)"; }
curl -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/api/v1/status/buildinfo
prom_auth | curl -K - -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/api/v1/status/buildinfo
curl -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/graph
```

Expected: `401`, `200`, and `401` for the UI path (the SSO chain answers
unauthenticated requests; a browser then goes through the SSO sign-in page).

### Phase 4. Host endpoints

4.1 Confirm that nothing is left on the k3d network and that the published
ports answer:

```bash
docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'
for p in 443 3100 3200 26379; do timeout 2 bash -c "</dev/tcp/192.168.0.13/$p" && echo "$p open" || echo "$p closed"; done
```

Expected: no Compose container on the network (only `k3d-hyhome-*` nodes, or
an error when the cluster and its network are gone), and all four ports open.
A Compose container still listed there predates the k3d removal; detach it
with `docker network disconnect k3d-hyhome <name>` (no restart).

### Phase 5. OpenBao Kubernetes auth

5.1 Write the new cluster CA (public) into a private working directory:

```bash
umask 077; mkdir -p /tmp/bao-k8s
KUBECONFIG=$(k3d kubeconfig write hyhome) kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d >/tmp/bao-k8s/k3d-ca.crt
```

5.1a Issue the Kiali Grafana token into the same directory (first setup,
Session 3, or a [reissue](#reissuing-the-kiali-grafana-token)). Grafana allows
no anonymous access, so Kiali sends the token of the Viewer service account
`k8s-kiali`. `graf_auth` writes the admin credential to curl's stdin, like
`prom_auth` in 3.2:

```bash
graf_auth() { printf 'user = "%s:%s"\n' "$(grep '^GRAFANA_ADMIN_USERNAME=' .env | cut -d= -f2 | tr -d '"')" "$(cat secrets/observability/grafana_admin_password.txt)"; }
SA=$(graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem 'https://grafana.hy.home.arpa/api/serviceaccounts/search?query=k8s-kiali' | jq -r '.serviceAccounts[] | select(.name=="k8s-kiali") | .id')
[ -n "$SA" ] || SA=$(graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem -H 'Content-Type: application/json' -d '{"name":"k8s-kiali","role":"Viewer"}' https://grafana.hy.home.arpa/api/serviceaccounts | jq -r '.id')
graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem -H 'Content-Type: application/json' -d "{\"name\":\"k8s-kiali-$(date +%Y%m%d)\",\"secondsToLive\":7776000}" "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens" | jq -j '.key' >/tmp/bao-k8s/grafana-kiali.token
printf 'header = "Authorization: Bearer %s"\n' "$(cat /tmp/bao-k8s/grafana-kiali.token)" | curl -K - -s -o /dev/null -w '%{http_code}\n' --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://grafana.hy.home.arpa/api/search
curl -s -o /dev/null -w '%{http_code}\n' --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://grafana.hy.home.arpa/api/search
```

Expected: `200` with the token and `401` without it. The token lives 90 days;
record its expiry date, never its value. The service account keeps the Viewer
role only.

5.2 Start a throwaway client as the host user on the host network. The host has
no `bao` CLI, the mounted files need the host uid, and the OIDC callback
listens on `localhost:8250`. The image is the one the
[OpenBao Compose file](../../../../../infra/03-security/openbao/docker-compose.yml)
pins. If the browser runs elsewhere, forward the port
first with `ssh -L 8250:localhost:8250 <host>`.

```bash
IMG=$(docker compose config --images openbao)
docker run --rm -it --network host --user "$(id -u):$(id -g)" -e HOME=/tmp -e BAO_ADDR=https://openbao.hy.home.arpa -e BAO_CACERT=/ca.pem -v "$PWD/secrets/certs/rootCA.pem:/ca.pem:ro" -v "$PWD/infra/03-security/openbao/config/policies:/policies:ro" -v "$PWD/secrets/db/valkey/mng_password.txt:/s/valkey:ro" -v "$PWD/secrets/observability/prometheus_api_password.txt:/s/prom:ro" -e PROM_API_USER="$(grep '^PROMETHEUS_API_USERNAME=' .env | cut -d= -f2 | tr -d '"')" -v /tmp/bao-k8s:/s/k8s --entrypoint sh "$IMG"
```

The remaining steps of this phase run inside the container.

5.3 Log in as the OIDC operator and take a snapshot:

```sh
umask 077; mkdir -p /tmp/c
bao login -no-print -method=oidc -path=oidc role=home-admin
bao operator raft snapshot save /s/k8s/pre-change.snap   # or a name for the change, e.g. pre-prometheus-api.snap
```

Expected: the browser login succeeds and the snapshot file exists. Do not
continue without it. `/s/k8s` is the host's `/tmp/bao-k8s`, so the snapshot
exists only there until Phase 8 moves it; never delete that directory as a
whole.

5.4 **Temporary root** (first setup, or an additional application). This needs
an approved root session and two distinct unseal shares from
`secrets/security/openbao_unseal_keys.txt`, pasted one per hidden prompt. `R`
passes the root per command, so it is never exported.

```sh
bao operator generate-root -init -format=json > /tmp/c/init.json
NONCE=$(sed -n 's/.*"nonce": *"\([^"]*\)".*/\1/p' /tmp/c/init.json); OTP=$(sed -n 's/.*"otp": *"\([^"]*\)".*/\1/p' /tmp/c/init.json)
bao operator generate-root -nonce="$NONCE" -format=json > /tmp/c/p1.json
bao operator generate-root -nonce="$NONCE" -format=json > /tmp/c/p2.json
ENC=$(sed -n 's/.*"encoded_token": *"\([^"]*\)".*/\1/p' /tmp/c/p2.json); bao operator generate-root -decode="$ENC" -otp="$OTP" > /tmp/c/root
R() { BAO_TOKEN="$(cat /tmp/c/root)" bao "$@"; }
R token lookup -format=json | grep -c '"root"'
```

Expected: `1` or more. `0` or a `403` on the next `R` command means
`/tmp/c/root` is missing or empty and `bao` fell back to the operator login
token; check `generate-root -status`, cancel a stale attempt with
`bao operator generate-root -cancel`, and run the ceremony again.

The client container mounts the policies from the checkout it starts in. Start
the session only after the policy change it applies is merged and pulled;
otherwise `R policy write` applies the old file.

Then run 5.4.1 (first setup) or 5.4.2 (additional application), and always
5.4.3.

5.4.1 First setup: enable the method, write policies, roles and the KV entries.

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

Expected: `[external-secrets]`. `secret/platform/argocd` (the Argo CD Valkey
password) and `secret/platform/prometheus-api` (the Prometheus API credential,
the same source as `INFRA-007`: `PROMETHEUS_API_USERNAME` and
`prometheus_api_password.txt`) and `secret/platform/grafana-api` (the Kiali
Grafana token from 5.1a) are required. Add `secret/platform/postgres-app`
`{db_name,username,password}` and `secret/platform/notifications`
`{slack_token}` the same way, and only when k8s apps use them.

5.4.2 Additional application (Session 3) for an environment set up before the
Prometheus API and Grafana entries and the role cap existed. Run 5.1a first:

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

Expected: `4`, `4`, and each `current_version` at least `1`.

5.4.3 Verify the token role, then revoke the root:

```sh
R read -field=token_explicit_max_ttl auth/token/roles/k8s-bootstrap
R token revoke -self
R token lookup >/dev/null 2>&1 && echo "ROOT STILL VALID" || echo "root revoked"
bao operator generate-root -status | grep -i started
```

Expected: `7200`, `root revoked`, `Started false`. After an additional
application, continue with Phase 7; the cluster configuration is unchanged.

5.5 Point the method at the cluster:

```sh
bao write auth/kubernetes/config kubernetes_host=https://192.168.0.13:6550 kubernetes_ca_cert=@/s/k8s/k3d-ca.crt disable_local_ca_jwt=true
bao read -field=kubernetes_host auth/kubernetes/config
```

Expected: `https://192.168.0.13:6550`.

5.6 Issue the bootstrap token into a file:

```sh
bao write -field=token auth/token/create/k8s-bootstrap ttl=2h explicit_max_ttl=2h > /s/k8s/k8s-bootstrap.token
```

5.7 Verify it as the token itself (the operator cannot look up other tokens),
then leave the container:

```sh
T="$(cat /s/k8s/k8s-bootstrap.token)"
BAO_TOKEN="$T" bao token lookup -format=json | grep -E '"(policies|orphan|ttl|explicit_max_ttl)"' -A2
BAO_TOKEN="$T" bao read -format=json secret/data/platform/argocd >/dev/null 2>&1 && echo "argocd read: allowed" || echo "argocd read: DENIED"
BAO_TOKEN="$T" bao read -format=json secret/data/hy-home/02-auth/keycloak >/dev/null 2>&1 && echo "keycloak read: LEAK" || echo "keycloak read: denied"
unset T
exit
```

Expected: policies `default` and `k8s-bootstrap`, orphan `true`, `ttl` and
`explicit_max_ttl` at most `7200`, `argocd read: allowed`,
`keycloak read: denied`. If anything differs, revoke the token (see
Troubleshooting) and stop.

### Phase 6. Hand off to hy-home.k8s

Give the cluster owner the following. Use a protected channel for the two
secret files.

| Item | Source |
| --- | --- |
| Bootstrap token (use within two hours) | `/tmp/bao-k8s/k8s-bootstrap.token` |
| Prometheus API credential | OpenBao `secret/platform/prometheus-api` (`username`, `password`), synced by ESO; the source is `.env` `PROMETHEUS_API_USERNAME` and `secrets/observability/prometheus_api_password.txt` |
| Kiali Grafana token | OpenBao `secret/platform/grafana-api` (`token`), synced by ESO; issued in 5.1a |
| Gateway CA (public) | `secrets/certs/rootCA.pem` |
| Endpoints | the contract table in the [guide](guide.md) |

The cluster owner then applies their side:

- the `system:auth-delegator` binding for the ESO service account
- DNS for `openbao.hy.home.arpa`, `prometheus.hy.home.arpa` and `grafana.hy.home.arpa` → `192.168.0.13`
- trust in the CA
- egress to ports 443, 3100, 3200 and 26379
- Alloy remote write and Kiali with the Basic Auth credential and a `cluster` external label
- Kiali's Grafana connection with the bearer token

### Phase 7. Verify from both sides

7.1 From the cluster, the owner confirms that an ESO `SecretStore` is valid and
that the Argo CD `ExternalSecret` has synced. Record only the ready status.

7.2 From the host, confirm the cluster's samples arrive (`prom_auth` from 3.2):

```bash
prom_auth | curl -K - -s --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem --data-urlencode 'query=count by (job) (up{cluster="k3d-hyhome"})' https://prometheus.hy.home.arpa/api/v1/query
```

Expected: one result per cluster job (for example `kubernetes-pods` and
`kubelet`). This is the evidence hy-home.k8s needs before it retires its
metrics NodePorts.

### Phase 8. Clean up and record

```bash
rm -f /tmp/bao-k8s/k8s-bootstrap.token /tmp/bao-k8s/grafana-kiali.token /tmp/bao-k8s/slack.token /tmp/bao-k8s/metrics.token /tmp/bao-k8s/secret_id /tmp/bao-k8s/*.custody /tmp/bao-k8s/*.hcl
install -d -m 700 secrets/backup/openbao
mv /tmp/bao-k8s/*.snap secrets/backup/openbao/
rmdir /tmp/bao-k8s 2>/dev/null || ls -l /tmp/bao-k8s
```

`secrets/backup/` is owner-only, and `.gitignore` covers its `*.txt` and
`*.snap` files. It is an interim copy on the
same host: copy the snapshot to separate offline custody as the
[backup and restore policy](../../04-data/0021-backup-and-restore/policy.md)
requires, then keep or delete the host copy by that policy's retention.

After the results check out, delete the Phase 2 backup directory. In the
current Task, record the date, the phases run, and the expected outputs of
3.2, 4.1, 5.4, 5.5, 5.7 and 7.2. Never record the token, shares, passwords or
KV values.

### Rotating the Prometheus API credential

The password lives in three places that must change together:

- `OBS-013`, the file
- `INFRA-007`, the Traefik htpasswd derived from it
- the OpenBao entry the cluster reads

If OpenBao is not updated, the cluster's remote write gets `401`. The OIDC
operator can update the entry without a root session.

1. Move the old file aside and generate a new one. `gen-secrets.sh` rederives
   `INFRA-007` because the old hash no longer verifies:

   ```bash
   umask 077; B=secrets/.backup-$(date +%Y%m%d); mkdir -p "$B" && mv secrets/observability/prometheus_api_password.txt "$B"/
   bash scripts/operations/gen-secrets.sh
   ```

2. Recreate Traefik and repeat the 3.2 checks (`401`, `200`):

   ```bash
   docker compose up -d --no-deps --force-recreate traefik
   ```

3. Update OpenBao as the operator (5.2 client container, 5.3 login), then
   leave the container:

   ```sh
   bao kv put secret/platform/prometheus-api username="$PROM_API_USER" password=@/s/prom
   bao kv metadata get -format=json secret/platform/prometheus-api | grep '"current_version"'
   ```

   Expected: `current_version` one higher than before.
4. Ask the cluster owner to force an ESO refresh of the Prometheus secret, then
   run 7.2.
5. Delete the old file from the backup once 7.2 passes.

### Reissuing the Kiali Grafana token

The token from 5.1a lives 90 days. The OIDC operator can replace the entry
without a root session.

1. Run 5.1a with a new token name (the date suffix does it).
2. Update OpenBao as the operator (5.2 client container, 5.3 login), then
   leave the container:

   ```sh
   bao kv put secret/platform/grafana-api token=@/s/k8s/grafana-kiali.token
   bao kv metadata get -format=json secret/platform/grafana-api | grep '"current_version"'
   ```

   Expected: `current_version` one higher than before.
3. Force the ESO refresh, then recreate the Kiali pod: Kiali reads the token
   when it starts, so a refreshed Secret alone leaves it on the old token.

   ```bash
   kubectl -n istio-system annotate externalsecret kiali-grafana-auth force-sync="$(date +%s)" --overwrite
   kubectl -n istio-system delete pod -l app=kiali
   kubectl -n istio-system rollout status deploy/kiali --timeout=180s
   ```

   Deleting the pod leaves the Deployment spec unchanged, so Argo CD sees no
   drift. Open Kiali once (or call its `/kiali/api/grafana`), then list the
   tokens and confirm the new one has the latest `lastUsedAt`:

   ```bash
   graf_auth | curl -K - -s --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens" | jq -r '.[] | "\(.id) \(.name) expires=\(.expiration) lastUsed=\(.lastUsedAt)"'
   graf_auth | curl -K - -s -o /dev/null -w '%{http_code}\n' -X DELETE --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens/<old id>"
   ```

   Expected: the new token used most recently, then `200` for the old one.

### Setting or replacing the Slack notifications token

`secret/platform/notifications` (`slack_token`) feeds the hy-home.k8s
`argocd-notifications-secret`. It takes a Slack bot token (`xoxb-`), not the
incoming-webhook URL in COMM-004. The operator policy grants this path from
SPEC-0181 on; an environment whose `hy-home-operator` policy predates that
needs one root session (5.4) to run `R policy write hy-home-operator
/policies/operator.hcl` first.

1. On the host, with `umask 077`, create `/tmp/bao-k8s/slack.token` in an
   editor. Do not `echo` the token.
2. Update OpenBao as the operator (5.2 client container, 5.3 login):

   ```sh
   bao kv put secret/platform/notifications slack_token=@/s/k8s/slack.token
   bao kv metadata get -format=json secret/platform/notifications | grep '"current_version"'
   ```

   Expected: `current_version` one higher than before (`1` the first time).
3. Delete `/tmp/bao-k8s/slack.token`, then force the ESO refresh and check
   the Argo CD application:

   ```bash
   kubectl -n argocd annotate externalsecret argocd-notifications-secret force-sync="$(date +%s)" --overwrite
   kubectl -n argocd get externalsecret argocd-notifications-secret
   kubectl -n argocd get application platform-argocd-config -o jsonpath='{.status.sync.status} {.status.health.status}{"\n"}'
   ```

   Expected: `SecretSynced`, `True`, then `Synced Healthy`.

### Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `METADATA rejected` in 2.2 | malformed private row (a value spanning lines) or registry mode not `0600` | back up, confirm the value equals its file, replace the row with the example row, `chmod 600`, rerun 2.2 |
| secret file is 0 bytes after 2.3 | its ID was missing from the private registry | finish 2.2 first, then rerun 2.3 |
| `curl` prints `000` | name not resolved or gateway down | use `--resolve`; check 3.1 |
| `401` with the credential | Traefik still has the old `usersFile` inode | recreate Traefik (3.1) |
| `permission denied` on `/s/k8s/...` | the client ran as its own user | restart it with `--user "$(id -u):$(id -g)"` (5.2) |
| `key is required` | empty input at the share prompt | rerun the same `-nonce` command and paste a share |
| `bound_service_account_namespaces can not be empty` | a line continuation dropped arguments | rerun the role write as one line |
| `Must supply data or use -force` | token create without parameters | include `ttl=2h explicit_max_ttl=2h` (5.6) |
| `403` on `bao token lookup <token>` | the operator cannot look up other tokens | look up as the token itself (5.7) |
| bootstrap token TTL about 32 days | token roles ignore `token_ttl`/`token_max_ttl`, so the role had no cap | `BAO_TOKEN="$(cat /s/k8s/k8s-bootstrap.token)" bao token revoke -self`, reissue with 5.6, and set `token_explicit_max_ttl=2h` on the role in the next root session |
| `ROOT STILL VALID` | revocation failed | stop and escalate; keep the session open |
| cluster remote write gets `401` after a rotation | OpenBao `secret/platform/prometheus-api` still holds the old password | rotation step 3, then an ESO refresh |
| Kiali shows Grafana unreachable or `401` | `secret/platform/grafana-api` missing, expired, or its token deleted | reissue the token, then an ESO refresh |
| no `cluster="k3d-hyhome"` series in 7.2 | the cluster sender is not configured or cannot reach 443 | the cluster owner checks the Alloy logs, DNS, CA and egress |

## Evidence

Record the phase outputs listed in Phase 8, the source commit, and which
situation from "When to Use" applied.

## Rollback or Recovery

- **Prometheus API:** remove the `prometheus-api` router labels and recreate
  Prometheus. The UI route is unaffected.
- **OpenBao:** the snapshot from 5.3 (`secrets/backup/openbao/` or its offline
  copy) is the recovery point; restore it only through the isolated procedure
  in the OpenBao runbook.
- **Bootstrap token:** revoke it by itself (see Troubleshooting).
- **Private registry and `.env`:** restore from the Phase 2 backup.

## Escalation

Stop and contact @buenhyden on `ROOT STILL VALID`, on a token that reads
outside `secret/platform/*`, on any request to put SSO or an allowlist in front
of OpenBao for the cluster, or on a request to publish Prometheus or Grafana
without authentication.

## Traceability

- [Guide](guide.md) (`GDE-0096`)
- [Policy](policy.md) (`POL-0096`)
- [OpenBao runbook](../../03-security/0085-openbao/runbook.md)

## Related Documents

- [Prometheus guide](../../06-observability/0045-prometheus/guide.md)
- [Secrets README](../../../../../secrets/README.md)
