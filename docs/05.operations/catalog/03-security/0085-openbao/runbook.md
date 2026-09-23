---
title: "OpenBao Runbook"
version: "0.5.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0085"
parent_ids:
- "POL-0085"
created: "2026-09-19"
---

# OpenBao Runbook

## When to Use

Use for `openbao openbao-agent` readiness checks and approved targeted deployment or recovery. Work from the repository root. Confirm configuration commit, image source, existing data location and a protected backup before runtime changes.

## Procedure

1. Validate the selected profile with the existing Compose validator; never print a private rendered model.
2. Run this bounded read-only check:

   ```bash
   docker compose exec -T openbao bao status
   ```

3. Confirm initialized/unsealed status separately, then verify destination existence and permissions without reading contents. AppRole provisioning and unseal require the owner-controlled credential procedure.
4. If deployment is approved, name only these services and verify initialization jobs and daemon readiness separately. Stop on an unexpected mount or failed check; do not broaden to the whole stack.

[Implementation](../../../../../infra/03-security/openbao/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

### Initial Bootstrap and Credential Recovery

The owner-approved initial bootstrap uses three Shamir unseal shares with a
threshold of two. Keep shares in separate offline custody after the temporary
handoff; a single file containing all shares is not separation of custody.
Never print initialization output, put credentials in command arguments, or
commit recovery material. Initial root credentials must be revoked only after human OIDC login, the
expected non-root policy, authenticated recovery, Agent authentication/rendering
and a protected Raft snapshot succeed. A failed setup retains protected recovery material for operator recovery.

Owner decision (2026-09-22): the three shares are kept together in
`secrets/security/openbao_unseal_keys.txt` (SEC-003, one share per line, `0600`,
Git-ignored, never mounted into a container). This is an explicit exception to
separate custody: anyone who can read that file can unseal OpenBao. Unseal from
an interactive terminal (`docker compose exec openbao bao operator unseal`) and
paste one share at the hidden prompt; never pass a share as an argument. The
private registry keeps only a placeholder for SEC-003; the file is the single
copy. The legacy Vault files cannot unseal OpenBao and were moved out of the
live tree to `secrets/.retired/2026-09-23/security/` pending disposal.

The `hy-home-renderer` AppRole uses the
[renderer policy](../../../../../infra/03-security/openbao/config/policies/renderer.hcl):
read only the two configured KV v2 data paths, with no write/list/admin grants.
The standard default policy supplies token self-renewal. Agent tokens have a
24-hour renewable period; SecretIDs expire after ten minutes and permit one use.
The Agent deletes the SecretID file after reading it. Existing Docker Secret
consumers continue using their current files; rendered outputs do not switch
application mounts automatically.

### Prometheus Metrics Credential

Use this procedure only after approval names the OpenBao policy/token change and
the Prometheus recreation as exact targets.

1. Confirm OpenBao is initialized and unsealed, the reviewed
   `prometheus.hcl` contains only `read` on `sys/metrics`, an authorized
   administrator is available, and rollback uses the current configuration
   commit. Do not use the renderer AppRole, a renderer sink token, a human
   operator token or a root token as the Prometheus credential.
2. Apply the policy and issue a new orphan service token without the default
   policy. Give it a finite TTL within the effective system maximum, record its
   expiry and accessor in protected custody, and deliver only the token value
   directly to `secrets/security/openbao_token.txt` at mode `0600`. Do not
   print it, pass it as an argument or stage it in another file.
3. Through protected input, verify the new token can read `sys/metrics` and
   is denied on an unrelated secret path and administrative path. Record only
   boolean allow/deny results and effective TTL, never the token or raw response.
4. Validate Compose and Prometheus configuration before the approved recreation.
   Recreate only Prometheus, confirm the configuration load/reload succeeded,
   then require the `openbao` target to report `UP` without recording raw
   target responses or logs.
5. Rotate by creating and validating a replacement first, atomically replacing
   the `0600` file, recreating only Prometheus, confirming the new target, and
   revoking the previous token by accessor. Never restore the legacy Vault root
   token grant or scrape job.

If policy application, token validation, configuration loading or target health
fails, keep the previous source/runtime configuration available, revoke the new
token by accessor, and remove its local file only within the approved credential
disposition. Recreate only Prometheus from the reviewed rollback commit. A
source rollback must not reintroduce `vault_token`; leave OpenBao metrics
disabled until the dedicated credential path can be repaired.

Before an Agent restart, an authorized operator must deliver a fresh SecretID
through a protected channel. Stop only the Agent while placing RoleID/SecretID
files (0600, container UID 100/GID 1000), then start it. Do not test-login with
that same single-use SecretID before the Agent consumes it. A server restart
requires the unseal ceremony; loss or expiry of the Agent token also requires
fresh AppRole credentials. An authorized operator identity is needed for
issuance; if none has been established, use the separately approved loopback recovery
procedure below. Ordinary generate-root also requires authenticated permission
in the current API; quorum keys alone do not authorize that endpoint. Do not store
an active permanent root token as an automation shortcut.

Verify unsealed status, Agent health, periodic token renewal capability, exact
read/deny capabilities and both output files (0600). Compare output bytes to the
authorized source privately, recording only a boolean result. Preserve original
Docker Secret values. Backup creation alone does not prove restore readiness.

### OIDC Configuration Contract

| Surface | Required setting |
| --- | --- |
| Keycloak realm/client | `hy-home.realm` / `home-openbao`, confidential client-secret authentication |
| Flows | Authorization Code enabled; S256 PKCE required; implicit/password/service-account flows disabled |
| Claim mapper | `oidc-group-membership-mapper`; claim `groups`; full group paths in ID token |
| Membership | Existing operator `hyunyoun` belongs to `/openbao-admins`; no automatic grant to all realm users |
| OpenBao mount/role | `oidc` / `home-admin`, role type `oidc`, user claim `sub`, groups claim `groups` |
| Binding | Exact `bound_claims.groups=["/openbao-admins"]`, audience `home-openbao` |
| Issuer | `https://keycloak.hy.home.arpa/realms/hy-home.realm`; verified CA supplied through `oidc_discovery_ca_pem` |
| UI callback | `https://openbao.hy.home.arpa/ui/vault/auth/oidc/oidc/callback` |
| CLI callback | `http://localhost:8250/oidc/callback` |
| Human token | `hy-home-operator` plus standard `default`; TTL 1h, max TTL 4h; no root or periodic token |

The hostnames above are the current HOME default. If the domain changes, update
issuer, certificates and exact redirects together; do not introduce wildcard
redirects. Keycloak stores its client secret and OpenBao stores its configured
copy in protected backend state; no new plaintext `.env` client-secret key is
needed. [Official Keycloak integration](https://openbao.org/docs/auth/jwt/oidc-providers/keycloak/)
provides provider setup context; this contract deliberately uses exact callbacks
and group binding rather than granting every authenticated user admin access.

### Human Login and Normal Root Recovery

1. Use the [guide](guide.md) to sign in through OIDC, role `home-admin`. Confirm
   the resulting policies are `default` and `hy-home-operator`, never `root`.
2. The operator policy allows authenticated `/sys/generate-root-token/attempt`
   and `/sys/generate-root-token/update` only for a quorum ceremony. Starting an
   attempt returns sensitive OTP/nonce material; capture it directly into
   protected custody, never the terminal or chat. Supply two distinct shares
   through a protected input channel. Do not pass shares or OTPs as arguments.
3. Decode the returned encoded token using the original OTP inside the protected
   process. Base64 output may omit padding; use the supported client or validated
   decoder. Persist the encoded response before decoding so a decoding failure
   cannot lose the newly issued root token.
4. Use root only for the approved operation. Confirm normal OIDC access still
   works, cancel incomplete attempts, revoke the temporary root, and confirm its
   lookup is rejected. Never revoke the last working administrative path early.

The current CLI `bao operator generate-root` uses the authenticated API. The
[official command reference](https://openbao.org/docs/commands/operator/generate-root/)
and [authenticated API](https://openbao.org/docs/api/system/generate-root-token/)
explain this compatibility boundary. Routine unseal is distinct from login and
must not be confused with administrator authorization.

### hy-home.k8s Kubernetes Auth

External Secrets Operator (ESO) in the hy-home.k8s cluster logs in with the
Kubernetes auth method and reads only `secret/data/platform/*` through
[eso-read-platform](../../../../../infra/03-security/openbao/config/policies/eso-read-platform.hcl).
The cluster reaches OpenBao at `https://openbao.hy.home.arpa` through Traefik;
do not add SSO or an IP allowlist to that route. OpenBao reaches the k3d API
server at `https://192.168.0.13:6550`.

| When | Steps | Identity |
| --- | --- | --- |
| First setup, or a lost auth mount, policy or role | 1, 2, 3, 4, 6 | temporary root (quorum), then OIDC operator |
| Every hy-home.k8s cluster rebuild (new API server CA) | 1, 2, 3, 5, 6 | OIDC operator (`home-admin`) |

Rules for every step: type each command on one line (a pasted line
continuation can silently drop arguments); secret values go through a file or
the hidden prompt, never an argument or the screen; record only names,
booleans and non-secret fields.

#### Prerequisites

- OpenBao is initialized and unsealed (`docker compose exec -T openbao bao status`).
- The operator can complete the OIDC browser login for role `home-admin`. When
  the browser runs on another machine, forward port 8250 first:
  `ssh -L 8250:localhost:8250 <host>`.
- The k3d cluster `hyhome` exists and `k3d`/`kubectl` work on the host.
- For step 4 only: an approved root session and two distinct unseal shares
  from `secrets/security/openbao_unseal_keys.txt`.

#### Step 1. Prepare the host

Run from the repository root. This writes the new cluster CA (public) into a
private working directory.

```bash
umask 077; mkdir -p /tmp/bao-k8s
KUBECONFIG=$(k3d kubeconfig write hyhome) kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d >/tmp/bao-k8s/k3d-ca.crt
```

#### Step 2. Start the client container

The host has no `bao` CLI. Run a throwaway client as the host user, so it can
read the mounted files and write into `/tmp/bao-k8s`, on the host network, so
the OIDC callback on `localhost:8250` and the host's `/etc/hosts` work.

```bash
docker run --rm -it --network host --user "$(id -u):$(id -g)" -e HOME=/tmp -e BAO_ADDR=https://openbao.hy.home.arpa -e BAO_CACERT=/ca.pem -v "$PWD/secrets/certs/rootCA.pem:/ca.pem:ro" -v "$PWD/infra/03-security/openbao/config/policies:/policies:ro" -v "$PWD/secrets/db/valkey/mng_password.txt:/s/valkey:ro" -v /tmp/bao-k8s:/s/k8s --entrypoint sh openbao/openbao:2.6.2
```

All remaining commands run inside this container.

#### Step 3. Log in as the operator and take a snapshot

```sh
umask 077; mkdir -p /tmp/c
bao login -no-print -method=oidc -path=oidc role=home-admin
bao operator raft snapshot save /s/k8s/pre-change.snap
```

Open the printed URL and finish the Keycloak login. Do not continue without
the snapshot.

#### Step 4. One-time setup with a temporary root

4.1 Generate a temporary root. At each hidden prompt paste a different share;
an empty Enter fails with `key is required`.

```sh
bao operator generate-root -init -format=json > /tmp/c/init.json
NONCE=$(sed -n 's/.*"nonce": *"\([^"]*\)".*/\1/p' /tmp/c/init.json); OTP=$(sed -n 's/.*"otp": *"\([^"]*\)".*/\1/p' /tmp/c/init.json)
bao operator generate-root -nonce="$NONCE" -format=json > /tmp/c/p1.json
bao operator generate-root -nonce="$NONCE" -format=json > /tmp/c/p2.json
ENC=$(sed -n 's/.*"encoded_token": *"\([^"]*\)".*/\1/p' /tmp/c/p2.json); bao operator generate-root -decode="$ENC" -otp="$OTP" > /tmp/c/root
R() { BAO_TOKEN="$(cat /tmp/c/root)" bao "$@"; }
```

`R` passes the root per command, so it is never exported into the shell.

4.2 Enable the method and write policies, roles and the required KV entry.

```sh
R auth list -format=json | grep -q '"kubernetes/"' || R auth enable kubernetes
R policy write eso-read-platform /policies/eso-read-platform.hcl
R policy write k8s-bootstrap /policies/k8s-bootstrap.hcl
R policy write hy-home-operator /policies/operator.hcl
R write auth/kubernetes/role/eso-read-platform bound_service_account_names=external-secrets bound_service_account_namespaces=external-secrets audience=vault token_policies=eso-read-platform token_ttl=1h
R write auth/token/roles/k8s-bootstrap allowed_policies=k8s-bootstrap orphan=true token_explicit_max_ttl=2h
R kv put secret/platform/argocd valkey_password=@/s/valkey
```

`secret/platform/argocd` (the Argo CD Valkey password, from the mng-valkey
secret file) is required. Add `secret/platform/postgres-app`
`{db_name,username,password}` and `secret/platform/notifications`
`{slack_token}` in the same way only when k8s apps use them.

4.3 Verify, then revoke the root.

```sh
R read -field=bound_service_account_namespaces auth/kubernetes/role/eso-read-platform
R read -field=token_explicit_max_ttl auth/token/roles/k8s-bootstrap
R token revoke -self
R token lookup >/dev/null 2>&1 && echo "ROOT STILL VALID" || echo "root revoked"
bao operator generate-root -status | grep -i started
```

Expect `[external-secrets]`, `7200`, `root revoked` and `Started false`.
Continue with step 5 to point the method at the cluster.

#### Step 5. Point Kubernetes auth at the cluster and issue a bootstrap token

5.1 Configure the method with the CA from step 1.

```sh
bao write auth/kubernetes/config kubernetes_host=https://192.168.0.13:6550 kubernetes_ca_cert=@/s/k8s/k3d-ca.crt disable_local_ca_jwt=true
bao read -field=kubernetes_host auth/kubernetes/config
```

Expect `https://192.168.0.13:6550`.

5.2 Issue the bootstrap token into a file. The request also asks for two
hours, which holds even if the role cap is missing.

```sh
bao write -field=token auth/token/create/k8s-bootstrap ttl=2h explicit_max_ttl=2h > /s/k8s/k8s-bootstrap.token
```

5.3 Verify as the token itself (the operator has no `auth/token/lookup`).

```sh
T="$(cat /s/k8s/k8s-bootstrap.token)"
BAO_TOKEN="$T" bao token lookup -format=json | grep -E '"(policies|orphan|ttl|explicit_max_ttl)"' -A2
BAO_TOKEN="$T" bao read -format=json secret/data/platform/argocd >/dev/null 2>&1 && echo "argocd read: allowed" || echo "argocd read: DENIED"
BAO_TOKEN="$T" bao read -format=json secret/data/hy-home/02-auth/keycloak >/dev/null 2>&1 && echo "keycloak read: LEAK" || echo "keycloak read: denied"
unset T
exit
```

Expect policies `default` and `k8s-bootstrap`, orphan `true`, `ttl` and
`explicit_max_ttl` at most `7200`, `argocd read: allowed` and
`keycloak read: denied`. If any differ, revoke the token (see
Troubleshooting) and stop.

#### Step 6. Hand off and clean up

On the host:

1. Give `/tmp/bao-k8s/k8s-bootstrap.token` to hy-home.k8s through a protected
   channel; it must be used within two hours.
2. Move `/tmp/bao-k8s/pre-change.snap` to protected custody.
3. `rm -f /tmp/bao-k8s/k8s-bootstrap.token`, then `rmdir` the directory once
   it is empty.
4. Record in the current Task: date, which steps ran, and the expected
   outputs from 4.3 and 5.3; never the token, shares or KV values.

The cluster side owns three prerequisites: the ESO service account
(`external-secrets/external-secrets`) needs a `system:auth-delegator`
ClusterRoleBinding, because without `token_reviewer_jwt` OpenBao reviews each
login with the client's own JWT; cluster DNS must resolve
`openbao.hy.home.arpa` to `192.168.0.13`; and the cluster must trust the mkcert
root CA. Confirm an ESO login from the cluster and record only allow/deny.
The UI equivalent of 5.1 is Access → Auth Methods → kubernetes → Configure.

#### Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `permission denied` on `/s/k8s/...` | the container ran as its own user | restart it with `--user "$(id -u):$(id -g)"` (step 2) |
| `key is required` | empty input at the share prompt | rerun the same `-nonce` command and paste a share |
| `bound_service_account_namespaces can not be empty` | a line continuation dropped arguments | rerun the role write as one line |
| `Must supply data or use -force` | `auth/token/create/<role>` without parameters | include `ttl=2h explicit_max_ttl=2h` (step 5.2) |
| `403 permission denied` on `bao token lookup <token>` | the operator cannot look up other tokens | look up as the token itself (step 5.3) |
| bootstrap token TTL about 32 days | token roles ignore `token_ttl`/`token_max_ttl` | revoke it: `BAO_TOKEN="$(cat /s/k8s/k8s-bootstrap.token)" bao token revoke -self`; reissue with step 5.2; fix the role with `token_explicit_max_ttl=2h` in the next root session |
| `ROOT STILL VALID` | revocation failed | stop and escalate; do not close the session |

### No Administrative Identity: Explicit Break-glass Recovery

This procedure is only for a confirmed lockout with preserved data and quorum
shares. Obtain explicit approval for the exact restart and temporary listener.
Do not initialize again, replace volumes, restore a snapshot over live data or
weaken the existing network listener.

1. Record image ID, cluster ID and all existing mount identities. Preserve a
   protected snapshot if available; keep the same image, storage and seal config.
2. In a temporary Compose override, add only a container-loopback listener at
   `127.0.0.1:18200` with `disable_unauthed_generate_root_endpoints=false`.
   Explicitly keep that flag true on the ordinary listener. Publish no extra port.
3. Recreate only OpenBao with `--no-deps --pull never --no-build`, then unseal the
   same cluster. Through `docker exec` and protected stdin, use the legacy
   `/sys/generate-root/attempt` and `/sys/generate-root/update` APIs with quorum.
   The ordinary generate-root CLI targets a different authenticated API.
4. Save the response and decoded rescue token directly as 0600 files. Remove the
   temporary override immediately once root is recovered, recreate only OpenBao,
   and unseal again. Confirm the auxiliary listener is gone, the ordinary legacy
   endpoint rejects unauthenticated access, and mount/cluster identities match.
5. Configure the approved native OIDC client, exact group-bound role and operator
   policy. Trust the issuer CA; never disable TLS checks. Record a targeted
   Keycloak rollback receipt before changing the client or group membership.
6. Require a real human OIDC login and confirm its non-root policy. With that
   policy, test capability denies, snapshot reading and authenticated root
   recovery start/cancel without submitting shares. Recheck Agent rendering.
7. Take a fresh protected snapshot, revoke the rescue root and verify rejection.
   If human acceptance fails, keep rescue custody protected and repair access;
   do not leave the loopback listener enabled while waiting.

This uses the [deprecated API](https://openbao.org/docs/api/system/generate-root/)
only during the explicitly approved recovery window. Normal operation must keep
it disabled, as required by the [listener contract](https://openbao.org/docs/configuration/listener/tcp/).

## Evidence

Record date, configuration commit, service names, exit statuses and sanitized health/resource results in the current Task. Do not capture secret values, raw environment, state, token files or message/database contents. Dated runtime results and recovery-custody handoff belong to the current Task.

## Rollback or Recovery

Capture a protected Raft snapshot with the non-root operator identity, record its
checksum, cluster ID, image declaration, seal configuration and custody receipt,
then rehearse restoration on a new data volume with network egress and consumers
disabled. Start the supported image against only the restored volume, complete the
threshold unseal ceremony, and verify cluster ID, mounts, policies, auth methods,
Agent authentication/rendering and denial tests without disclosing secret values.
Destroy the isolated copy after evidence acceptance; never restore over live Raft
data. This isolated restore remains planned and was not executed during the
2026-09-20 correction.

A snapshot contains token state at capture time: restoring a snapshot taken before
root revocation can restore that credential state. Recheck and revoke restored
bootstrap/recovery tokens during isolated recovery validation; take routine
backups using the operator identity after temporary roots have been revoked. Do not initialize over existing Raft data or downgrade storage in place.

## Escalation

Stop and contact @buenhyden when credentials, destructive storage changes, remote mutations or unavailable backups prevent safe progress.

## Traceability

- Governing architecture: [AD-0003](../../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
