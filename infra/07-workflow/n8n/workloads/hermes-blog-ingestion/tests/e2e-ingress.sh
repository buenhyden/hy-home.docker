#!/usr/bin/env bash
# Disposable synthetic E2E of the Hermes direct path on one Docker host:
#   host curl -> Traefik (proposed exact-path route) -> n8n (native, imported
#   workflow) -> Blog-data Gateway (built from the pinned commit) -> SQLite.
# Synthetic tokens only. It creates its own networks, volume and containers
# with a random suffix and removes them on exit; the live stack, its networks,
# secrets and Traefik directory are never touched.
# Needs Docker, gh access to the private Blog-data repository and the local
# n8n image. Usage: tests/e2e-ingress.sh [blog-data-commit]
set -euo pipefail
workload=$(cd "$(dirname "$0")/.." && pwd)
root=$(git -C "$workload" rev-parse --show-toplevel)
compose=$root/infra/07-workflow/n8n/docker-compose.yml
commit=${1:-$(sed -n 's#.*image: hy-home/blog-ingestion:\([0-9a-f]\{40\}\)$#\1#p' "$compose")}
n8n_image=$(sed -n 's#^ *image: \(hyhome/n8n:[^ ]*\)$#\1#p' "$compose" | head -1)
traefik_image=$(sed -n 's#^ *image: \(traefik:[^ ]*\)$#\1#p' "$root/infra/01-gateway/traefik/docker-compose.yml")
id=e2e-$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')
# Live Traefik publishes only on the LAN address, so Hermes connects there too.
lan_ip=${E2E_LAN_IP:-$(ip -4 route get 1.1.1.1 | sed -n 's/.* src \([0-9.]*\).*/\1/p')}
gateway_image=hy-home/blog-ingestion-e2e:$commit
work=$(mktemp -d)
pass=0
cleanup() {
  docker rm -f "$id-traefik" "$id-n8n" "$id-gateway" >/dev/null 2>&1 || true
  docker network rm "$id-edge" "$id-ingest" >/dev/null 2>&1 || true
  docker volume rm "$id-gateway" >/dev/null 2>&1 || true
  rm -rf "$work"
}
trap cleanup EXIT
ok() { pass=$((pass + 1)); echo "PASS $*"; }
fail() { echo "FAIL $*"; exit 1; }
hex() { od -An -N"$1" -tx1 /dev/urandom | tr -d ' \n'; }
ready() {
  for _ in $(seq 120); do
    [ "$(docker inspect -f '{{.State.Running}}' "$id-n8n")" = true ] ||
      fail "n8n exited: $(docker logs --tail 5 "$id-n8n" 2>&1)"
    docker exec "$id-n8n" wget -q --spider http://127.0.0.1:5678/healthz/readiness 2>/dev/null && return
    sleep 5
  done
  fail "n8n never became ready"
}

# 1. Gateway image from the pinned Blog-data commit, sparse and read-only.
git init -q "$work/blog-data"
git -C "$work/blog-data" remote add origin "https://github.com/buenhyden/blog-data.git"
git -C "$work/blog-data" -c "credential.helper=!gh auth git-credential" \
  fetch -q --depth 1 --filter=blob:none origin "$commit"
git -C "$work/blog-data" sparse-checkout set --no-cone /.github/docker/ \
  /site/web/package.json /site/web/package-lock.json /scripts/lib/ \
  /scripts/ops/ingestion-gateway.mjs /docs/99.templates/ \
  /00_System/Templates/Vault/Capture/T-Inbox-Capture.md \
  /00_System/Contracts/Metadata/document-profile-registry.json
git -C "$work/blog-data" -c "credential.helper=!gh auth git-credential" checkout -q FETCH_HEAD
docker build -q -f "$work/blog-data/.github/docker/ingestion.Dockerfile" \
  -t "$gateway_image" "$work/blog-data" >/dev/null
echo "INFO gateway image $gateway_image $(docker image inspect -f '{{.Id}}' "$gateway_image")"

# 2. Disposable networks: a plain edge and an internal, isolated ingest net.
docker network create "$id-edge" >/dev/null
docker network create --internal \
  -o com.docker.network.bridge.gateway_mode_ipv4=isolated "$id-ingest" >/dev/null

# 3. Gateway: synthetic token digests only, config 0600 owned by 10001.
hermes_token=$(hex 24)
gateway_token=$(hex 24)
digest=$(printf %s "$gateway_token" | sha256sum | cut -d' ' -f1)
printf '{"schema_version":"1.0","data_dir":"/data","host":"0.0.0.0","port":8787,"credentials":[{"producer":"hermes","token_sha256":"%s","scopes":["ingest","read"]}]}' \
  "$digest" >"$work/config.json"
chmod 0644 "$work/config.json"
docker volume create "$id-gateway" >/dev/null
docker run --rm --user 0 --entrypoint sh -v "$id-gateway:/v" -v "$work/config.json:/in.json:ro" \
  "$gateway_image" -c 'mkdir /v/data && cp /in.json /v/config.json && chown -R 10001:10001 /v && chmod 0600 /v/config.json && chmod 0700 /v/data'
docker run -d --name "$id-gateway" --network "$id-ingest" --network-alias blog-ingestion \
  --user 10001:10001 --read-only --cap-drop ALL --security-opt no-new-privileges:true \
  --mount "type=volume,src=$id-gateway,dst=/data,volume-subpath=data" \
  --mount "type=volume,src=$id-gateway,dst=/run/config.json,volume-subpath=config.json,readonly" \
  "$gateway_image" serve --config /run/config.json >/dev/null

# 4. n8n natively: import the committed workflow with synthetic credentials.
python3 - "$workload/workflow.json" "$work" "$hermes_token" "$gateway_token" <<'PY'
import json, sys
src, out, hermes, gateway = sys.argv[1:]
wf = json.load(open(src))
wf["id"] = "HermesE2E000001"
for node in wf["nodes"]:
    if node["name"] == "Authenticated Ingress":
        node["credentials"] = {"httpHeaderAuth": {"id": "e2eHermesIngress", "name": "hermes ingress"}}
    if node["name"] == "Send to Gateway":
        node["credentials"] = {"httpHeaderAuth": {"id": "e2eGatewayIngest", "name": "gateway ingest"}}
json.dump(wf, open(f"{out}/workflow.json", "w"))
creds = [
    {"id": "e2eHermesIngress", "name": "hermes ingress", "type": "httpHeaderAuth",
     "data": {"name": "X-Hermes-Ingest-Token", "value": hermes}},
    {"id": "e2eGatewayIngest", "name": "gateway ingest", "type": "httpHeaderAuth",
     "data": {"name": "Authorization", "value": "Bearer " + gateway}},
]
json.dump(creds, open(f"{out}/credentials.json", "w"))
PY
chmod 0644 "$work/workflow.json" "$work/credentials.json"
# The upstream entrypoint of the same image: the hy-home wrapper requires the
# live stack's Docker secrets, which a disposable run must never mount.
docker create --name "$id-n8n" --network "$id-edge" --network-alias n8n \
  --entrypoint tini \
  -e N8N_ENCRYPTION_KEY="$(hex 24)" -e N8N_RUNNERS_MODE=internal \
  -e N8N_DIAGNOSTICS_ENABLED=false -e N8N_PROXY_HOPS=1 -e EXECUTIONS_MODE=regular \
  -e N8N_HOST=n8n.hy.home.arpa -e N8N_PROTOCOL=https -e WEBHOOK_URL=https://n8n.hy.home.arpa/ \
  -v "$work/workflow.json:/import/workflow.json:ro" -v "$work/credentials.json:/import/credentials.json:ro" \
  "$n8n_image" -- /docker-entrypoint.sh >/dev/null
docker network connect "$id-ingest" "$id-n8n"
docker start "$id-n8n" >/dev/null
ready
docker exec "$id-n8n" n8n import:credentials --input=/import/credentials.json >/dev/null
docker exec "$id-n8n" n8n import:workflow --input=/import/workflow.json >/dev/null
docker exec "$id-n8n" n8n publish:workflow --id=HermesE2E000001 >/dev/null
docker restart "$id-n8n" >/dev/null
ready
ok "n8n imported and published the committed workflow natively"

# 5. Traefik with the proposed route; an SSO stand-in guards everything else.
mkdir "$work/dynamic"
sed -e "s#192.168.0.13/32#$lan_ip/32#" -e 's#n8n@docker#n8n-e2e@file#' \
  "$workload/traefik/hermes-webhook.yml" >"$work/dynamic/hermes-webhook.yml"
sso_hash=$(hex 16 | openssl dgst -sha1 -binary | base64)
cat >"$work/dynamic/standin.yml" <<YAML
http:
  routers:
    n8n-sso-standin:
      rule: Host(\`n8n.hy.home.arpa\`)
      entryPoints: [websecure]
      tls: {}
      middlewares: [sso-standin]
      service: n8n-e2e
  middlewares:
    sso-standin:
      basicAuth:
        users: ["sso:{SHA}$sso_hash"]
  services:
    n8n-e2e:
      loadBalancer:
        servers: [{url: "http://n8n:5678"}]
YAML
chmod -R a+rX "$work/dynamic"
docker run -d --name "$id-traefik" --network "$id-edge" -p "$lan_ip::443" \
  -v "$work/dynamic:/dynamic:ro" "$traefik_image" \
  --entrypoints.websecure.address=:443 --providers.file.directory=/dynamic \
  --accesslog=true --accesslog.format=json --log.level=ERROR >/dev/null
port=$(docker port "$id-traefik" 443/tcp | head -1 | sed 's/.*://')
url=https://n8n.hy.home.arpa:$port/webhook/hermes-blog-ingestion
post() { curl -sk -o "$work/body" -w '%{http_code}' --resolve "n8n.hy.home.arpa:$port:$lan_ip" "$@" || true; }
call() { # call <expected-status> <label> [curl args...]
  local expected=$1 label=$2 status
  shift 2
  status=$(post "$@")
  [ "$status" = "$expected" ] || fail "$label: got $status $(head -c 300 "$work/body")"
  ok "$label ($status)"
}
body() { python3 -c "import json,sys; b=json.load(open(sys.argv[1])); assert $1, b" "$work/body"; }
for _ in $(seq 30); do
  [ "$(post "https://n8n.hy.home.arpa:$port/")" = 401 ] && break
  sleep 1
done
report=$workload/tests/fixtures/synthetic-report.json
header="X-Hermes-Ingest-Token: $hermes_token"
json='Content-Type: application/json'

# 6. Scenarios. The route allows 6 requests a minute, so order is deliberate.
call 201 "host POST with token persisted in the Gateway" -X POST -H "$header" -H "$json" --data-binary @"$report" "$url"
body 'b["persisted"] is True and b["duplicate"] is False'
call 200 "identical replay is a duplicate" -X POST -H "$header" -H "$json" --data-binary @"$report" "$url"
body 'b["duplicate"] is True'
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["items"][0]["title"]+=" changed"; json.dump(d, open(sys.argv[2],"w"))' "$report" "$work/conflict.json"
call 409 "same idempotency key with other content conflicts" -X POST -H "$header" -H "$json" --data-binary @"$work/conflict.json" "$url"
call 403 "missing webhook token refused by n8n" -X POST -H "$json" --data-binary @"$report" "$url"
call 400 "invalid shape refused without echo" -X POST -H "$header" -H "$json" --data '{"schema_version":"1.0"}' "$url"
body 'b == {"error": "INVALID_REQUEST"}'
head -c 1100000 /dev/zero | tr '\0' a >"$work/large"
call 413 "body above 1 MiB stopped at Traefik" -X POST -H "$header" -H "$json" --data-binary @"$work/large" "$url"
call 401 "GET on the webhook path stays behind SSO" -H "$header" "$url"
call 401 "other webhook paths stay behind SSO" -X POST -H "$header" -H "$json" --data-binary @"$report" "${url%hermes-blog-ingestion}other"
call 401 "n8n UI stays behind SSO" "https://n8n.hy.home.arpa:$port/rest/settings"
lan=$(docker exec -e NODE_TLS_REJECT_UNAUTHORIZED=0 "$id-n8n" node -e "require('https').request({host:'$id-traefik',port:443,path:'/webhook/hermes-blog-ingestion',method:'POST',servername:'n8n.hy.home.arpa',headers:{host:'n8n.hy.home.arpa'}},s=>console.log(s.statusCode)).end()" 2>/dev/null)
[ "$lan" = 403 ] || fail "non-host source on the webhook path: got $lan"
ok "non-host source refused by the allowlist (403)"
source_ip=$(docker logs "$id-traefik" 2>/dev/null | python3 -c '
import json, sys
for line in sys.stdin:
    try:
        entry = json.loads(line)
    except ValueError:
        continue
    if entry.get("RouterName", "").startswith("hermes-blog-ingestion-webhook") and entry.get("DownstreamStatus") == 201:
        print(entry["ClientHost"])
        break')
[ "$source_ip" = "$lan_ip" ] || fail "host process via $lan_ip arrived as $source_ip"
ok "host process connecting to $lan_ip arrives as $source_ip"

docker stop "$id-gateway" >/dev/null
sleep 10
status=$(post -X POST -H "$header" -H "$json" --data-binary @"$report" "$url")
case $status in 5??) ok "Gateway down fails as $status, never 2xx" ;; *) fail "Gateway down returned $status" ;; esac
docker start "$id-gateway" >/dev/null
for _ in $(seq 30); do
  docker exec "$id-n8n" node -e "fetch('http://blog-ingestion:8787/v1/summary').then(r=>process.exit(r.status===401?0:1),()=>process.exit(1))" 2>/dev/null && break
  sleep 2
done
sleep 10
call 200 "replay after Gateway restart is a persisted duplicate" -X POST -H "$header" -H "$json" --data-binary @"$report" "$url"
body 'b["duplicate"] is True and b["persisted"] is True'

gateway_ip=$(docker inspect -f "{{(index .NetworkSettings.Networks \"$id-ingest\").IPAddress}}" "$id-gateway")
[ -n "$gateway_ip" ] || fail "Gateway has no address on the ingest network"
if curl -s -m 3 -o /dev/null "http://$gateway_ip:8787/v1/summary"; then
  fail "host process reached the Gateway on the isolated network"
fi
ok "host cannot reach the Gateway on the internal isolated network"

limited=0
for _ in $(seq 8); do
  [ "$(post -X POST -H "$header" -H "$json" --data-binary @"$report" "$url")" = 429 ] && limited=1 && break
done
[ "$limited" = 1 ] || fail "burst was never rate limited"
ok "burst above the route rate limit returns 429"
echo "RESULT $pass PASS, 0 FAIL (blog-data $commit, $n8n_image, $traefik_image)"
