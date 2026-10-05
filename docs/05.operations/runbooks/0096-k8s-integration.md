---
title: "hy-home.k8s Integration Runbook"
version: "1.3.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0096"
parent_ids:
- "GDE-0096"
created: "2026-09-23"
---

# hy-home.k8s Integration Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

| Situation | Phases |
| --- | --- |
| 통합 최초 설정 | 1 → 8, 순서대로 |
| hy-home.k8s 클러스터 재구축(새 API 서버 CA) | 1, 5 (5.1–5.3, **5.5**, 5.6–5.7), 6, 7, 8; 새 CA 기록 이후 ESO 인증 확인 |
| Prometheus API 비밀번호 교체 | 1, [교체의 BLOCKED 조건](#rotating-the-prometheus-api-credential) 확인; 해소 전 consumer/KV 변경 중단 |
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

### Procedure

### Shared prerequisites and result handling

작업 전에 source revision, HOME host, Compose project, 정확한 service/profile,
승인된 기존 kubeconfig/context와 변경 범위를 기록한다. 아래 주소·도메인·port는
기본값이다. 실제 `HOST_LAN_BIND_IP`, `DEFAULT_URL` 및 port 설정에 맞춘다.
별도 승인 없이 문서 점검을 runtime, private 입력 읽기 또는 k8s 변경으로 확장하지
않는다. 모든 credential 분기(5.1a, Grafana 재발급, Slack 포함)는 같은 보호된
작업 디렉터리 준비부터 시작한다. 기존 경로를 재사용하거나 덮어쓰지 않는다.

```bash
umask 077
K8S_WORK=$(mktemp -d /tmp/bao-k8s.XXXXXX)
chmod 700 "$K8S_WORK"
```

각 명령은 성공·실패·판정 불가를 구분한다. 실패 출력은 보호된 파일에 보관하고
Task에는 상태 코드와 비밀이 아닌 판정만 남긴다. DNS/TLS/timeout/sealed/CLI 또는
JSON 오류를 `denied`, `revoked`로 간주하지 않는다. 원시 응답을 로그로 복사하지
않는다. 클라이언트 도구가 구조화된 판정에 필요한 필드를 제공하지 않으면 중단하고
소유자가 같은 요청의 서버 응답을 확인한다.

### Phase 1. Prepare the repository

1.1 로컬 작업을 잃지 않고 `main`을 최신으로 갱신한다:

```bash
git status --short
# 위 상태를 검토하여 예상하지 않은 변경이 없음을 확인한 뒤에만 실행한다.
git switch main
git pull --ff-only
```

`git status`에 만들지 않은 변경 사항이 나오면 폐기하기 전에 멈추고 그
소유자에게 확인한다.

1.2 추적 소스를 검증한다:

```bash
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
```

예상 결과: 둘 다 통과한다. [RUN-0086 정적 검증](0086-dependency-version-management.md#static-configuration-validation)의
private 입력·임시 파일 경계를 먼저 승인한다. PASS는 실제 서비스 건강 증거가 아니다.

### Phase 2. Secrets and environment

2.1 private registry와 `.env`(Git-ignored)를 백업한다:

```bash
umask 077
B=$(mktemp -d secrets/.backup-k8s.XXXXXX)
chmod 700 "$B"
cp secrets/SENSITIVE_ENV_VARS.md .env "$B"/
chmod 600 "$B/SENSITIVE_ENV_VARS.md" "$B/.env"
```

2.2 공개 메타데이터를 private registry와 `.env`로 동기화한다. 먼저 `--dry-run`으로
공개 schema/stat 변경 계획을 확인한다. `--sync-metadata-check`는 private 값을
읽으며 종료0은 일치,1은 drift,2는 입력 거절이다. 기본 sync는 unknown 항목을
보존하며 prune은 별도 승인이다. 2가 나오면 write하지 않는다:

```bash
bash scripts/operations/gen-secrets.sh --dry-run
```

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata-check
bash scripts/operations/gen-secrets.sh --sync-metadata
```

`METADATA rejected: unsafe, ambiguous, changed or unreadable input`은 여러
입력 거절 원인을 포함한다. 지원하지 않는 행 형식·여러 줄 값, unsafe path/symlink,
중복 ID, 읽기 실패, 검사 중 동시 변경이 가능하다. 읽을 수 있는 안전한 일반 파일의
mode만 `0600`과 다른 경우는 거부가 아니라 drift(check 종료1)이며, 승인된
sync 쓰기는 내용을 보존하면서 `0600`으로 정렬한다. 이 진단만으로 원인을 확정하거나 입력을 고치지 않는다. 쓰기 전에
중단하고 기존 파일과 Value를 보존한 상태에서 값이 노출되지 않는 경로·권한·ID·
변경 여부를 확인한다. 확인한 원인의 좁은 수정만 별도 승인 후 수행한다.
예시 행으로 일괄 교체하지 않는다. 기본 sync의 unknown 행 보존과 별도 승인된
prune 경계는 유지한다. Troubleshooting을 참고하며 승인된 수정과
`--sync-metadata` 이후에는 점검이 반드시 0으로 종료되어야 한다.

2.3 사용자 이름을 확인하고 누락된 파일을 생성한다. 인자 없는 generator는 두 ID에
한정되지 않고 전체 registry의 누락 secret을 처리하므로 그 쓰기 범위를 먼저
승인한다. 기존 값 재사용은 회전 증거가 아니다:

```bash
grep -c '^PROMETHEUS_API_USERNAME=' .env
bash scripts/operations/gen-secrets.sh
stat -c '%n %s %a' secrets/observability/prometheus/prometheus_api_password.txt secrets/auth/traefik/traefik_prometheus_api_htpasswd.txt
```

예상 결과: `1`, 그리고 두 파일 모두 크기가 0이 아니고 모드가 `640`이다.

### Phase 3. Gateway and Prometheus

3.1 두 consumer를 재생성한다. 단일 파일 secret은 기존 inode를 유지하므로
`INFRA-007` 변경 이후에는 Traefik을 반드시 재생성해야 한다.

```bash
docker compose up -d --no-deps --no-build --pull never --force-recreate traefik prometheus
docker ps --format '{{.Names}} {{.Status}}' | grep -E '^(traefik|infra-prometheus) '
```

예상 결과: 승인된 두 consumer가 각 healthcheck 기준을 통과한다. 고정된 1분
성공 SLA는 없다. 이 명령은 absent service도 시작할 수 있으므로 기존 target과
ready dependency, local image, 예상 중단을 확인한 뒤 승인된 apply 때만 실행한다.
`Created`/`Exited`는 자동 재실행 근거가 아니다. 상태 원인을 확인하고
[RUN-0086](0086-dependency-version-management.md#runtime-configuration-apply)의
coverage를 갖춘 mount hash 검증까지 마친다.

3.2 호스트에서 Prometheus API를 검증한다. `prom_auth`는 credential을 curl의
stdin(`-K -`)으로 전달하므로 프로세스 인자에는 절대 나타나지 않는다:

```bash
prom_auth() { printf 'user = "%s:%s"\n' "$(grep '^PROMETHEUS_API_USERNAME=' .env | cut -d= -f2 | tr -d '"')" "$(cat secrets/observability/prometheus/prometheus_api_password.txt)"; }
curl -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/api/v1/status/buildinfo
prom_auth | curl -K - -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/api/v1/status/buildinfo
curl -s -o /dev/null -w '%{http_code}\n' --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://prometheus.hy.home.arpa/graph
```

예상 결과: 위 순서대로 `302`, `200`, `302`이다. `/api/v1/`에 Basic header가
없으면 현재 SSO 경로가 선택된다. 별도로 비밀이 아닌 의도적 invalid credential
(`invalid:invalid`)을 curl stdin config로 전달한 API 요청은401이어야 한다.
redirect를 따라가지 않고 상태를 확인하며000,5xx,예상 외 redirect는 중단한다.
Basic header가 있는 API와 UI의 SSO 경로를 혼동하지 않는다.

### Phase 4. Host endpoints

4.1 k3d 네트워크에 남은 것이 없는지, 게시된 포트가 응답하는지 확인한다:

```bash
docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'
# 선택한 trace protocol은 4317 또는 4318을 별도로 검사한다.
for p in 443 3100 3200 26379; do
  if timeout 2 bash -c "</dev/tcp/192.168.0.13/$p"; then
    echo "$p connected"
  else
    echo "$p connection-not-established; diagnose before continuing"
  fi
done
```

예상 결과: 기존 클러스터에는 `k3d-hyhome-*` 노드만 있고 선택한 consumer의
포트 연결이 성립한다. 네트워크가 없는 오류는 정상 membership 증거가 아니다.
예상 외 member는 이름·owner·선택 상태를 확인하고 중단한다. 자동으로
`docker network disconnect`하지 않는다. Tempo3200은 조회/API이고 trace 수집은
Alloy4317/4318이다. PostgreSQL 앱이 선택되면15432/15433도 해당 contract로
확인한다. TCP 성공만으로 인증이나 데이터 수집 성공을 선언하지 않는다.

### Phase 5. OpenBao Kubernetes auth

5.1 새 클러스터 CA(public)를 private 작업 디렉터리에 기록한다:

```bash
# 승인된 기존 KUBECONFIG/context를 사용한다. kubeconfig write는 별도 변경이다.
kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d >"$K8S_WORK/k3d-ca.crt"
openssl x509 -in "$K8S_WORK/k3d-ca.crt" -noout -fingerprint -sha256
```

CA 추출과 certificate parse가 모두 성공하고 대상 클러스터의 public CA fingerprint와
일치해야 한다. 빈 파일이나 다른 context면 중단한다. 전체 kubeconfig는 출력하지 않는다.

5.1a Kiali Grafana 토큰을 같은 디렉터리에 발급한다(최초 설정, 추가 KV 설정, 또는
[재발급](#reissuing-the-kiali-grafana-token)). Grafana는 익명 접근을 허용하지
않으므로 Kiali는 Viewer service account `k8s-kiali`의 토큰을 전송한다.
`graf_auth`는 3.2의 `prom_auth`와 마찬가지로 admin credential을 curl의
stdin으로 전달한다:

```bash
set -e -o pipefail
graf_auth() { printf 'user = "%s:%s"\n' "$(grep '^GRAFANA_ADMIN_USERNAME=' .env | cut -d= -f2 | tr -d '"')" "$(cat secrets/observability/grafana/grafana_admin_password.txt)"; }
graf_auth | curl -K - --fail-with-body -sS --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem 'https://grafana.hy.home.arpa/api/serviceaccounts/search?query=k8s-kiali' >"$K8S_WORK/grafana-search.json"
# HTTP 성공 뒤 JSON을 확인한다. 정확한 이름의 결과가 0 또는 1개여야 한다.
jq -e '[.serviceAccounts[] | select(.name=="k8s-kiali")] | length <= 1' "$K8S_WORK/grafana-search.json" >/dev/null
SA_COUNT=$(jq '[.serviceAccounts[] | select(.name=="k8s-kiali")] | length' "$K8S_WORK/grafana-search.json")
if [ "$SA_COUNT" = 0 ]; then
  graf_auth | curl -K - --fail-with-body -sS --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem -H 'Content-Type: application/json' -d '{"name":"k8s-kiali","role":"Viewer"}' https://grafana.hy.home.arpa/api/serviceaccounts >"$K8S_WORK/grafana-account.json"
  # HTTP 성공과 아래 JSON 검사 성공을 각각 확인한다.
  jq -e '.name=="k8s-kiali" and .role=="Viewer" and (.id | type=="number" and .>0)' "$K8S_WORK/grafana-account.json" >/dev/null
  SA=$(jq -r '.id' "$K8S_WORK/grafana-account.json")
else
  jq -e '[.serviceAccounts[] | select(.name=="k8s-kiali")] | length==1 and (.[0].role=="Viewer") and (.[0].id | type=="number" and .>0)' "$K8S_WORK/grafana-search.json" >/dev/null
  SA=$(jq -r '.serviceAccounts[] | select(.name=="k8s-kiali") | .id' "$K8S_WORK/grafana-search.json")
fi
graf_auth | curl -K - --fail-with-body -sS --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem -H 'Content-Type: application/json' -d "{\"name\":\"k8s-kiali-$(date +%Y%m%d-%H%M%S)\",\"secondsToLive\":7776000}" "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens" >"$K8S_WORK/grafana-issued.json"
# HTTP 성공을 확인한 후에만 token을 추출한다.
jq -e '.key | type=="string" and length>0 and .!="null"' "$K8S_WORK/grafana-issued.json" >/dev/null
jq -j '.key' "$K8S_WORK/grafana-issued.json" >"$K8S_WORK/grafana-kiali.token"
chmod 600 "$K8S_WORK/grafana-kiali.token"
printf 'header = "Authorization: Bearer %s"\n' "$(cat "$K8S_WORK/grafana-kiali.token")" | curl -K - -s -o /dev/null -w '%{http_code}\n' --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://grafana.hy.home.arpa/api/search
curl -s -o /dev/null -w '%{http_code}\n' --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem https://grafana.hy.home.arpa/api/search
```

위 block은 Bash의 `set -e -o pipefail`을 켠 승인된 별도 shell에서 실행하여 HTTP·JSON 검사 실패 시 다음 write를 막는다. 설치된 Grafana pin에서 response schema, 정확한
Viewer 계정 ID와 만료 설정을 확인한다. `.key`가 null/빈 값이면 KV에 쓰지 않는다.
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
docker run --rm -it --network host --user "$(id -u):$(id -g)" -e HOME=/tmp -e BAO_ADDR=https://openbao.hy.home.arpa -e BAO_CACERT=/ca.pem -v "$PWD/secrets/certs/rootCA.pem:/ca.pem:ro" -v "$PWD/infra/03-security/openbao/config/policies:/policies:ro" -v "$PWD/secrets/db/mng-valkey/mng_password.txt:/s/valkey:ro" -v "$PWD/secrets/observability/prometheus/prometheus_api_password.txt:/s/prom:ro" -e PROM_API_USER="$(grep '^PROMETHEUS_API_USERNAME=' .env | cut -d= -f2 | tr -d '"')" -v "$K8S_WORK:/s/k8s" --entrypoint sh "$IMG"
```

이 단계의 나머지 절차는 컨테이너 내부에서 실행한다.

5.3 OIDC operator로 로그인하고 스냅샷을 생성한다:

```sh
umask 077; mkdir -p /tmp/c
bao login -no-print -method=oidc -path=oidc role=home-admin
bao operator raft snapshot save /s/k8s/pre-change.snap   # or a name for the change, e.g. pre-prometheus-api.snap
```

예상 결과: 브라우저 로그인이 성공하고 스냅샷 파일이 존재한다. 이 파일 없이는
진행하지 않는다. `/s/k8s`는 호스트의 `$K8S_WORK`이므로 스냅샷은 Phase 8이
옮기기 전까지 그곳에만 있다. 해당 디렉터리 전체는 절대 삭제하지
않는다.

5.4 **임시 root**(최초 설정, 또는 추가 애플리케이션). 승인된 root 세션과
`secrets/security/openbao/openbao_unseal_keys.txt`에서 가져온 서로 다른 unseal
share 두 개가 필요하며, 각각 숨겨진 프롬프트에 붙여넣는다. `R`은 명령마다
root를 전달하므로 절대 export되지 않는다.

임시 root 발급·decode는 [RUN-0085 Human Login and Normal Root Recovery](0085-openbao.md#human-login-and-normal-root-recovery)의
승인된 절차를 그대로 따른다. OTP·encoded token을 CLI 인자에 넣지 않는다. 생성
결과를 private `/tmp/c/root`에 전달하고 정확한 token의 lookup으로 root 정책을
확인한다. 빈 파일이면 operator token으로 대체하지 않고 중단한다.

```sh
R() { test -s /tmp/c/root || { printf '%s\n' 'missing root token; STOP' >&2; return 1; }; BAO_TOKEN="$(cat /tmp/c/root)" bao "$@"; }
R token lookup -format=json > /tmp/c/root-lookup.json
```

성공한 lookup의 정책이 정확히 root인지 구조화된 JSON으로 확인하고 boolean만
기록한다. 실패·파싱 오류는 중단한다. 진행 중인 generate-root attempt의 취소·재시도도
RUN-0085를 따른다. 서로 다른 share2/3, root 승인과 custody, 작업 뒤 폐기는 필수다.

client 컨테이너는 자신을 시작한 체크아웃의 policy를 마운트한다. 적용할 policy
변경이 병합되고 pull된 이후에만 세션을 시작한다. 그렇지 않으면 `R policy write`가 이전 파일을 적용한다.

그다음 5.4.1(최초 설정) 또는 5.4.2(추가 애플리케이션)를 실행하고, 항상
5.4.3을 실행한다.

5.4.1 최초 설정: method를 활성화하고 policy, role, KV 항목을 작성한다.

```sh
R auth list -format=json > /tmp/c/auth-mounts.json
# 위 요청 및 JSON 파싱 성공 후 kubernetes/가 없을 때만 다음을 실행한다.
# R auth enable kubernetes
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

5.4.2 추가 애플리케이션(추가 KV 설정): Prometheus API와 Grafana 항목, role
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
R token lookup -format=json > /tmp/c/root-before-revoke.json
R token revoke -self
R token lookup -format=json > /tmp/c/root-after-revoke.json 2>/tmp/c/root-after-revoke.err
bao status -format=json > /tmp/c/server-status.json
bao operator generate-root -status
```

명령마다 결과를 확인한다. role 상한은7200이고 폐기 전 동일 token lookup은
성공해야 한다. revoke 요청 성공 뒤 서버가 도달 가능하고 unsealed인 상태에서
**같은 token**의 lookup이 서버의403 invalid-token/permission-denied로 거절된
경우만 폐기 확인으로 기록한다. lookup이 성공하면 `ROOT STILL VALID`로 중단한다.
DNS/TLS/timeout/sealed/CLI/JSON 오류는 `INDETERMINATE`이며 client와 보호된
증거를 유지하여 소유자에게 에스컬레이션한다. `Started false`는 발급 ceremony가
끝났다는 뜻이며 token 폐기 증거가 아니다. 확인 후 root·OTP·share 임시 자료는
RUN-0085 custody 절차에 따라 처리한다.

추가 KV만 갱신하고 클러스터가 동일하면 Phase7로 진행할 수 있다. 클러스터
재구축에서는 반드시5.5를 수행한다.

5.5 method를 클러스터로 지정한다:

```sh
bao write auth/kubernetes/config kubernetes_host=https://192.168.0.13:6550 kubernetes_ca_cert=@/s/k8s/k3d-ca.crt disable_local_ca_jwt=true
bao read -field=kubernetes_host auth/kubernetes/config
```

예상 결과: 승인된 클러스터 API 주소(기본값 `https://192.168.0.13:6550`).
public CA fingerprint와 write 시각을 기록하고 Phase7에서 **이 write 이후 새
Kubernetes auth 로그인과 ESO 동기화**를 확인한다. 이전 Ready 상태는 증거가 아니다.

5.6 bootstrap 토큰을 파일로 발급한다:

```sh
bao write -field=token auth/token/create/k8s-bootstrap ttl=2h explicit_max_ttl=2h > /s/k8s/k8s-bootstrap.token
```

5.7 토큰 자신으로 검증한 다음(operator는 다른 토큰을 조회할 수 없다),
컨테이너를 나간다:

```sh
T="$(cat /s/k8s/k8s-bootstrap.token)"
test -n "$T"
BAO_TOKEN="$T" bao token lookup -format=json > /tmp/c/bootstrap-lookup.json
BAO_TOKEN="$T" bao read -format=json secret/data/platform/argocd > /tmp/c/allowed-before.json 2>/tmp/c/allowed-before.err
BAO_TOKEN="$T" bao read -format=json secret/data/hy-home/02-auth/keycloak > /tmp/c/forbidden.json 2>/tmp/c/forbidden.err
BAO_TOKEN="$T" bao read -format=json secret/data/platform/argocd > /tmp/c/allowed-after.json 2>/tmp/c/allowed-after.err
unset T
```

각 요청 직후 exit와 서버 응답을 확인하고 중단 조건을 적용한다. lookup의 구조화된
필드에서 policy는 정확히 `default`, `k8s-bootstrap`, orphan은true,
`0 < ttl <= 7200`, `explicit_max_ttl=7200`이어야 한다. 허용 읽기는 금지 읽기
전후 모두 성공해야 한다. 그 사이 금지 경로의 서버403 permission denied만
의도한 거절 증거다.404, token 만료, DNS/TLS/timeout/sealed/CLI/파싱 오류는
`INDETERMINATE`로 중단한다. 금지 읽기가 성공하면 `LEAK`이며 token을 즉시
self-revoke하고 에스컬레이션한다. raw KV 응답은 private 임시 파일에서만 처리하고
boolean만 기록한다. client 종료 전 임시 응답 파일의 custody를 정리한다.

### Phase 6. Hand off to hy-home.k8s

다음을 클러스터 소유자에게 전달한다. bootstrap token만 보호된 채널로 보내며 Prometheus/Grafana 값은 ESO로 전달한다. public CA는 비밀이 아니다.

| Item | Source |
| --- | --- |
| Bootstrap 토큰(2시간 이내 사용) | `$K8S_WORK/k8s-bootstrap.token` |
| Prometheus API credential | OpenBao `secret/platform/prometheus-api`(`username`, `password`), ESO가 동기화; 출처는 `.env`의 `PROMETHEUS_API_USERNAME`과 `secrets/observability/prometheus/prometheus_api_password.txt` |
| Kiali Grafana 토큰 | OpenBao `secret/platform/grafana-api`(`token`), ESO가 동기화; 5.1a에서 발급 |
| Gateway CA(public) | `secrets/certs/rootCA.pem` |
| Endpoints | [가이드](../guides/0096-k8s-integration.md)의 contract 표 |

이후 클러스터 소유자가 자기 쪽 변경을 적용한다:

- ESO service account에 대한 `system:auth-delegator` 바인딩
- `openbao.hy.home.arpa`, `prometheus.hy.home.arpa`, `grafana.hy.home.arpa`의 DNS → `192.168.0.13`
- CA 신뢰
- 선택한 consumer에 필요한443,3100,26379 egress; Tempo 조회/API3200, Alloy trace 수집4317 또는4318, 선택 PostgreSQL15432/15433은 각각 별도로 확인
- Basic Auth credential과 `cluster` external label을 사용하는 Alloy remote write 및 Kiali
- bearer 토큰을 사용하는 Kiali의 Grafana 연결

### Phase 7. Verify from both sides

7.1 클러스터 측에서 소유자는 ESO `SecretStore`가 유효하고 Argo CD
`ExternalSecret`이 동기화되었는지 확인한다. 변경 이후의 새 auth 성공과
reconcile 시각·Ready 상태만 기록한다. CA 교체 전의 기존 Ready만으로 통과시키지 않는다.

7.2 호스트 측에서 클러스터의 샘플이 도착하는지 확인한다(3.2의 `prom_auth`
사용):

```bash
prom_auth | curl -K - -s --resolve prometheus.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem --data-urlencode 'query=count by (job) (up{cluster="k3d-hyhome"})' https://prometheus.hy.home.arpa/api/v1/query
```

예상 결과: 선택한 클러스터 job마다 새 시리즈가 도착한다. `count by(job)(up)`은
up값0도 세므로 전체 클러스터 건강을 증명하지 않는다. 예상 job inventory와 fresh
sample, 실제 up값을 별도로 확인한다. Loki 로그·trace 수집/조회·Kiali·선택 DB는
각 consumer 소유자의 제한된 기능 검증으로 확인한다. synthetic 데이터 쓰기는
별도 승인 없이는 실행하지 않는다. metrics NodePort 폐지는 이 증거와 별도
클러스터 변경 승인 이후에만 가능하다.

### Phase 8. Clean up and record

클러스터 bootstrap 소비 완료 후 token 자신으로 self-revoke하고5.4.3과 같은
서버 건강·동일 token lookup 분기로 폐기를 확인한다. 파일 삭제는 서버 폐기가
아니다. 만료까지 보관하기로 승인했다면 최대2시간의 bounded expiry와 custody를
기록하며 `revoked`라고 쓰지 않는다. 폐기/만료 확인 전 파일을 지우지 않는다.

```bash
install -d -m 700 secrets/backup/openbao
# 실제 생성한 snapshot 이름과 대상 충돌 여부를 확인한 뒤 한 파일씩 옮긴다.
mv "$K8S_WORK/pre-change.snap" secrets/backup/openbao/
```

snapshot 존재·크기·권한0600과 offline 인계를 확인한다. 임시 token, 발급 응답JSON,
허용 읽기 응답, root/OTP custody 등은 해당 세션에서 만든 정확한 파일만 확인 후
삭제한다. 광범위한 glob 삭제나 작업 디렉터리 전체 삭제를 실행하지 않는다.

`secrets/backup/`는 소유자 전용이며, `.gitignore`가 그 안의 `*.txt`와
`*.snap` 파일을 제외한다. 여기 둔 파일은 같은 호스트의 임시 사본이다. 스냅샷을
[backup and restore policy](../policies/0021-backup-and-restore.md)가
요구하는 별도의 오프라인 custody로 복사한 다음, 그 policy의 retention에 따라
호스트 사본을 보관하거나 삭제한다.

consumer 검증과 rollback 보존 기간에 대한 owner 확인 후에만 Phase2 백업을 정리한다. 현재 Task에 날짜, 실행한
단계, 그리고 3.2, 4.1, 5.4, 5.5, 5.7, 7.2의 예상 출력을 기록한다. 토큰,
share, 비밀번호, KV 값은 절대 기록하지 않는다.

### Rotating the Prometheus API credential

이 비밀번호는 세 곳에 있고 세 곳 모두 함께 바꿔야 한다:

- `OBS-013`, 파일 자체
- `INFRA-007`, 여기서 파생된 Traefik htpasswd
- 클러스터가 읽는 OpenBao 항목

OpenBao를 갱신하지 않으면 클러스터의 remote write가 `401`을 받는다. OIDC
operator는 root 세션 없이 해당 항목을 갱신할 수 있다.

**BLOCKED — 현재 source에는 이 회전을 보장하는 실행 절차가 없다.**
`gen-secrets.sh`의 인자 없는 생성은 기존 파일이 없더라도 private registry의
non-placeholder `OBS-013` 값을 다시 쓰고, 기존 `INFRA-007` hash가 그 값과
일치하면 유지한다. 파일을 backup으로 이동하고 generator를 실행하는 방법은 새
비밀번호를 만들었다는 증거가 아니므로 실행하지 않는다. KV `current_version+1`도
같은 값의 재기록일 수 있다.

consumer 재생성이나 KV 쓰기 전에 별도 승인된 source 수정 또는 scoped 회전
방법이 필요하다. 승인된 방법은 registry·password file·파생 htpasswd를 일관되게
갱신하고 old/new 차이는 boolean으로 증명해야 한다. 그 뒤의 필수 순서는 보호된
backup/custody → 새 값과 hash 일치 검증 → 승인된 Traefik apply 및 mount 확인 →
새 Basic200/이전 Basic401/invalid Basic401 → operator의
`secret/platform/prometheus-api` 갱신 → KV version과 새 ESO refresh → 실제
remote write/query 검증 → rollback 보존 승인 뒤 이전 자료 정리다. 본 문서는
새 generator 기능이나 임의 credential 값을 만드는 명령을 추가하지 않는다.

### Reissuing the Kiali Grafana token

5.1a의 토큰은 90일 동안 유효하다. OIDC operator는 root 세션 없이 해당
항목을 교체할 수 있다.

1. Shared prerequisites의 private 디렉터리를 준비하고 고유한 새 토큰 이름으로5.1a를 실행한다. 같은 날 재발급도 구분한다. 이전 token은 기능 검증 전까지 유지한다.
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
   graf_auth | curl -K - --fail-with-body -sS --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens" | jq -r '.[] | "\(.id) \(.name) expires=\(.expiration) lastUsed=\(.lastUsedAt)"'
   graf_auth | curl -K - -s -o /dev/null -w '%{http_code}\n' -X DELETE --resolve grafana.hy.home.arpa:443:192.168.0.13 --cacert secrets/certs/rootCA.pem "https://grafana.hy.home.arpa/api/serviceaccounts/$SA/tokens/<old id>"
   ```

   삭제 요청은 새 ESO sync와 Kiali 기능 사용, 새 token의 `lastUsedAt`을 확인한
   후에만 실행한다. 정확한 이전 ID를 확인하고 설치 pin의 API 성공 응답과 목록에서
   이전 ID가 사라졌는지 검증한다. 오류·불명확한 ID면 삭제하지 않는다.

### Setting or replacing the Slack notifications token

`secret/platform/notifications`(`slack_token`)는 hy-home.k8s의
`argocd-notifications-secret`에 값을 공급한다. 이 항목은 COMM-004의
incoming-webhook URL이 아니라 Slack bot 토큰(`xoxb-`)을 사용한다. operator
policy는 SPEC-0181부터 이 경로를 허용한다. `hy-home-operator` policy가 그
이전인 환경에서는 먼저 root 세션 하나(5.4)로 `R policy write hy-home-operator
/policies/operator.hcl`을 실행해야 한다.

1. Shared prerequisites의 private 디렉터리를 준비한 뒤 호스트에서 `umask 077` 상태로 편집기를 열어 `$K8S_WORK/slack.token`을
   생성한다. 토큰을 `echo`하지 않는다.
2. operator로 OpenBao를 갱신한다(5.2 client 컨테이너, 5.3 로그인):

   ```sh
   bao kv put secret/platform/notifications slack_token=@/s/k8s/slack.token
   bao kv metadata get -format=json secret/platform/notifications | grep '"current_version"'
   ```

   예상 결과: `current_version`이 이전보다 1 높다(최초에는 `1`).
3. `$K8S_WORK/slack.token`을 삭제한 다음 ESO refresh를 강제하고 Argo CD
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
| 2.2에서 `METADATA rejected` | 행 형식·여러 줄 값, unsafe path/symlink, 중복 ID, 읽기 실패 또는 동시 변경 등 여러 원인 가능 | 쓰기를 중단하고 입력과 Value를 보존한다. 2.2의 값 없는 진단으로 정확한 원인을 확인한 뒤 승인된 좁은 수정만 수행한다. 예시 행 일괄 교체는 하지 않으며 기본 sync의 unknown 행 보존·별도 prune 승인 경계를 유지한다 |
| 2.3 이후 secret 파일이 0바이트 | 해당 ID가 private registry에 없음 | 먼저 2.2를 완료한 다음 2.3을 다시 실행 |
| `curl`이 `000`을 출력 | HTTP 응답을 얻지 못함; DNS, TLS/CA, 연결 실패, timeout 등 transport 원인 가능 | 상태 코드와 curl 실패 종류를 값 노출 없이 구분하고 승인된 endpoint·이름 해석·CA·연결을 확인한다. 검증된 DNS 원인에만 `--resolve`를 사용하며 원인 불명은 중단한다. 000만으로 재생성·credential 회전을 실행하지 않는다 |
| credential과 함께 `401` | 잘못되거나 이전인 credential, 인증·route 불일치, 기존 `usersFile` inode 등 여러 원인 가능 | 값을 출력하지 않고 선택 route·credential 일치 boolean·usersFile 상태를 확인한다. stale inode가 근거로 확인되고 정확한 project/service 변경이 승인된 경우에만 3.1 재생성 분기를 수행한다. 불명확하면 중단하며 401 자체는 재생성·회전 권한이 아니다 |
| `/s/k8s/...`에서 `permission denied` | client가 자체 사용자로 실행됨 | `--user "$(id -u):$(id -g)"`로 재시작(5.2) |
| `key is required` | share 프롬프트에 빈 입력 | 같은 `-nonce` 명령을 다시 실행하고 share를 붙여넣기 |
| `bound_service_account_namespaces can not be empty` | 줄 연속으로 인자가 누락됨 | role write를 한 줄로 다시 실행 |
| `Must supply data or use -force` | 파라미터 없이 token create 실행 | `ttl=2h explicit_max_ttl=2h`를 포함(5.6) |
| `bao token lookup <token>`에서 `403` | operator는 다른 토큰을 조회할 수 없음 | 토큰 자신으로 조회(5.7) |
| bootstrap 토큰 TTL이 약 32일 | token role이 `token_ttl`/`token_max_ttl`을 무시하여 role에 상한이 없었음 | `BAO_TOKEN="$(cat /s/k8s/k8s-bootstrap.token)" bao token revoke -self`를 실행하여 폐기를 검증한다. 승인된 root 세션에서 role에 `token_explicit_max_ttl=2h`를 설정하고7200을 확인한 뒤에만5.6으로 재발급 |
| `ROOT STILL VALID` | 폐기 실패 | 중단하고 에스컬레이션, 세션은 열어 둠 |
| credential 변경 이후 클러스터 remote write가 `401` | gateway와 OpenBao/ESO 값 불일치 가능 | 자동 회전하지 않고 BLOCKED 조건과 승인된 rollback을 확인; 원인 확인 후 owner 승인 범위에서 복구 |
| Kiali가 Grafana에 연결할 수 없거나 `401`을 표시 | `secret/platform/grafana-api`가 없거나, 만료되었거나, 토큰이 삭제됨 | 토큰 재발급, 그다음 ESO refresh |
| 7.2에서 `cluster="k3d-hyhome"` 시리즈가 없음 | 클러스터 sender가 구성되지 않았거나 443에 도달할 수 없음 | 클러스터 소유자가 Alloy 로그, DNS, CA, egress를 확인 |

## Verification

### Evidence

Phase 8에 나열된 단계 출력, 소스 커밋, "When to Use"에서 적용된 상황을
기록한다.

## Rollback and Escalation

### Rollback or Recovery

- **Prometheus API:** 현재 source와 보호된 이전 credential 상태를 비교하여 owner가
  승인한 정확한 rollback만 수행한다. API router 제거는 모든 API consumer를
  끊는 containment 변경이므로 자동 rollback으로 실행하지 않는다. UI와 API
  검증을 각각 수행한다.
- **OpenBao:** 5.3의 스냅샷(`secrets/backup/openbao/` 또는 그 오프라인
  사본)이 복구 지점이다. 복원은 OpenBao 런북의 격리된 절차로만 한다.
- **Bootstrap 토큰:** 단독으로 폐기한다(Troubleshooting 참고).
- **Private registry와 `.env`:** Phase 2 백업에서 복원한다.

### Escalation

`ROOT STILL VALID`, `secret/platform/*` 밖을 읽는 토큰, 클러스터를 위해
OpenBao 앞에 SSO나 허용목록을 두라는 요청, 또는 인증 없이 Prometheus나
Grafana를 게시하라는 요청이 있으면 중단하고 @buenhyden에게 연락한다.

### Traceability

- [Guide](../guides/0096-k8s-integration.md) (`GDE-0096`)
- [Policy](../policies/0096-k8s-integration.md) (`POL-0096`)
- [OpenBao runbook](0085-openbao.md)

## Related Documents

- [Prometheus guide](../guides/0045-prometheus.md)
- [Secrets README](../../../secrets/README.md)
