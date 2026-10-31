#!/usr/bin/env bash
# Disposable synthetic E2E of the Hermes direct path on one Docker host:
#   host curl -> Traefik (proposed exact-path route) -> n8n (native, imported
#   workflow) -> Blog-data Gateway (built from the pinned commit) -> SQLite,
# then attestation -> Resource Export -> pull and ACK through the proposed
# export routes, as the host attester and the Windows receiver would.
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
  docker network rm "$id-edge" "$id-ingest" "$id-export" >/dev/null 2>&1 || true
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
# shellcheck source=gateway-image.sh
. "$workload/tests/gateway-image.sh"
build_gateway_image "$commit" "$work/blog-data" "$gateway_image"
echo "INFO gateway image $gateway_image $(docker image inspect -f '{{.Id}}' "$gateway_image")"
# The Resource Export renderer reads these; a missing one would hold every export.
docker run --rm --network none --entrypoint sh "$gateway_image" -c \
  'test -f 00_System/Templates/Vault/PARA/T-Resource.md && test -f 00_System/Contracts/Metadata/document-profile-registry.json && test -f scripts/lib/ingestion/research-map.json' ||
  fail "gateway image lacks the Resource Export templates"
ok "gateway image carries the Resource templates, profile registry and research map"

# 2. Disposable networks: a plain edge, an internal isolated ingest net (n8n
# worker) and an internal isolated export net (Traefik), as in Compose.
docker network create "$id-edge" >/dev/null
for net in "$id-ingest" "$id-export"; do
  docker network create --internal \
    -o com.docker.network.bridge.gateway_mode_ipv4=isolated "$net" >/dev/null
done

# 3. Gateway: synthetic token digests and attestation key only, config 0600
# owned by 10001. One single-scope credential per role, as in operations.
hermes_token=$(hex 24)
gateway_token=$(hex 24)
attest_token=$(hex 24)
read_token=$(hex 24)
ack_token=$(hex 24)
python3 - "$work" "$gateway_token" "$attest_token" "$read_token" "$ack_token" <<'PY'
import hashlib, json, os, sys
from cryptography.hazmat.primitives import serialization as s
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
work, ingest, attest, read, ack = sys.argv[1:]
def key(name):
    k = Ed25519PrivateKey.generate()
    path = f"{work}/{name}.pem"
    with open(path, "wb") as f:
        f.write(k.private_bytes(s.Encoding.PEM, s.PrivateFormat.PKCS8, s.NoEncryption()))
    os.chmod(path, 0o600)
    return k.public_key().public_bytes(s.Encoding.PEM, s.PublicFormat.SubjectPublicKeyInfo).decode()
public = key("attest")
key("unregistered")
digest = lambda t: hashlib.sha256(t.encode()).hexdigest()
grant = lambda t, scopes: {"producer": "hermes", "token_sha256": digest(t), "scopes": scopes}
json.dump({
    "schema_version": "1.0", "data_dir": "/data", "host": "0.0.0.0", "port": 8787,
    "credentials": [grant(ingest, ["ingest", "read"]), grant(attest, ["attest"]),
                    grant(read, ["export_read"]), grant(ack, ["export_ack"])],
    "export": {"attestation_keys": [{"key_id": "attest-e2e", "public_key": public}]},
}, open(f"{work}/config.json", "w"))
PY
chmod 0644 "$work/config.json"
# The hardening the Compose service declares, rendered from the repository.
mapfile -t hardening < <(cd "$root" && COMPOSE_DISABLE_ENV_FILE=1 docker compose \
  --env-file .env.example -f docker-compose.yml --profile blog-ingestion config --format json |
  python3 -c '
import json, sys
s = json.load(sys.stdin)["services"]["blog-ingestion"]
assert s["image"].endswith(":" + sys.argv[1]), s["image"]
out = ["--user", s["user"], "--pids-limit", str(s["pids_limit"])]
out += ["--read-only"] if s["read_only"] else []
for cap in s["cap_drop"]:
    out += ["--cap-drop", cap]
for opt in s["security_opt"]:
    out += ["--security-opt", opt]
out += ["--memory", str(s["mem_limit"])] if s.get("mem_limit") else []
print("\n".join(out))' "$commit")
[ "${#hardening[@]}" -ge 8 ] || fail "could not render the Compose Gateway hardening"
docker volume create "$id-gateway" >/dev/null
docker run --rm --user 0 --entrypoint sh -v "$id-gateway:/v" -v "$work/config.json:/in.json:ro" \
  "$gateway_image" -c 'mkdir /v/data && cp /in.json /v/config.json && chown -R 10001:10001 /v && chmod 0600 /v/config.json && chmod 0700 /v/data'
docker run -d --name "$id-gateway" --network "$id-ingest" --network-alias blog-ingestion \
  "${hardening[@]}" \
  --mount "type=volume,src=$id-gateway,dst=/data,volume-subpath=data" \
  --mount "type=volume,src=$id-gateway,dst=/run/config.json,volume-subpath=config.json,readonly" \
  "$gateway_image" serve --config /run/config.json >/dev/null
docker network connect --alias blog-ingestion "$id-export" "$id-gateway"
ok "gateway runs with the Compose-declared user, read-only root, caps and limits"

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

# 5. Traefik with the live routes; an SSO stand-in guards everything else.
mkdir "$work/dynamic"
sed -e "s#192.168.0.13/32#$lan_ip/32#" -e 's#n8n@docker#n8n-e2e@file#' \
  "$root/infra/01-gateway/traefik/dynamic/hermes-webhook.yml" >"$work/dynamic/hermes-webhook.yml"
# One host stands in for both Windows B and the server-A attester here; the
# per-router source split is asserted by test_export_route.py.
sed -e "s#192.168.0.22/32#$lan_ip/32#" -e "s#192.168.0.13/32#$lan_ip/32#" \
  "$root/infra/01-gateway/traefik/dynamic/blog-export.yml" >"$work/dynamic/blog-export.yml"
# The routes chain the live POL-0013 standard chain; carry exactly its parts.
python3 - "$root/infra/01-gateway/traefik/dynamic/middleware.yml" "$work/dynamic/standard-chain.yml" <<'PY2'
import sys, yaml
m = yaml.safe_load(open(sys.argv[1]))["http"]["middlewares"]
names = ["gateway-standard-chain", *m["gateway-standard-chain"]["chain"]["middlewares"]]
yaml.safe_dump({"http": {"middlewares": {n: m[n] for n in names}}}, open(sys.argv[2], "w"))
PY2
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
docker network connect "$id-export" "$id-traefik"
port=$(docker port "$id-traefik" 443/tcp | head -1 | sed 's/.*://')
url=https://n8n.hy.home.arpa:$port/webhook/hermes-blog-ingestion
post() {
  curl -sk -o "$work/body" -w '%{http_code}' --resolve "n8n.hy.home.arpa:$port:$lan_ip" \
    --resolve "blog-export.hy.home.arpa:$port:$lan_ip" "$@" || true
}
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
cp "$work/body" "$work/held-receipt"
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
call 403 "wrong webhook token refused by n8n" -X POST -H "X-Hermes-Ingest-Token: $(hex 24)" -H "$json" --data-binary @"$report" "$url"
call 401 "trailing-slash webhook path stays behind SSO" -X POST -H "$header" -H "$json" --data-binary @"$report" "$url/"
call 401 "case-changed webhook path stays behind SSO" -X POST -H "$header" -H "$json" --data-binary @"$report" "${url/hermes-blog/Hermes-blog}"

# 7. Resource Export: attestation -> ready export -> pull -> ACK, through the
# proposed export routes with one single-scope token per role.
xb=https://blog-export.hy.home.arpa:$port
read="Authorization: Bearer $read_token"
ack="Authorization: Bearer $ack_token"
attest="Authorization: Bearer $attest_token"
field() { python3 -c 'import json,sys; print(eval(sys.argv[2], {"b": json.load(open(sys.argv[1]))}))' "$@"; }
sign() { # sign <request-json> <key-pem> <out>: what the host attester sends
  python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); from publisher import attestation as a
open(sys.argv[4], "wb").write(a.request_body("attest-e2e", a.load_signing_key(sys.argv[3]), a.message(open(sys.argv[2], "rb").read())))' "$workload" "$@"
}
held_id=$(field "$work/held-receipt" 'b["id"]')
# A report for an approved research job (devops), unlike the synthetic "daily".
python3 - "$report" "$work/devops.json" <<'PY'
import hashlib, json, sys
d = json.load(open(sys.argv[1]))
d.update(job_id="25674fbc0bf3", run_id="2026-10-31", fire_id="cron-02",
         source_text="Synthetic DevOps report.")
d["idempotency_key"] = "devops-" + d["run_id"]
d["source_sha256"] = hashlib.sha256(d["source_text"].encode()).hexdigest()
d["items"] = [{"item_id": "devops-1", "kind": "devops", "title": "Synthetic DevOps item",
               "body": "Synthetic body for the Resource Export E2E.",
               "source_url": "https://example.org/devops-1"}]
json.dump(d, open(sys.argv[2], "w"))
PY
sleep 20  # the webhook route allows 6 a minute; let it refill
call 201 "devops report persisted" -X POST -H "$header" -H "$json" --data-binary @"$work/devops.json" "$url"
ready_id=$(field "$work/body" 'b["id"]')
call 200 "persisted reports have no export before attestation" -H "$read" "$xb/v1/exports"
body 'b["items"] == []'
sign "$work/devops.json" "$work/attest.pem" "$work/att-ready"
sign "$work/conflict.json" "$work/attest.pem" "$work/att-tampered"
sign "$work/devops.json" "$work/unregistered.pem" "$work/att-forged"
sign "$report" "$work/attest.pem" "$work/att-held"
call 403 "export_read token cannot attest" -X POST -H "$read" -H "$json" --data-binary @"$work/att-ready" "$xb/v1/ingestions/$ready_id/attestations"
call 422 "signature over changed items is refused" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-tampered" "$xb/v1/ingestions/$held_id/attestations"
call 422 "signature by an unregistered key is refused" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-forged" "$xb/v1/ingestions/$ready_id/attestations"
call 201 "trusted attestation creates a ready export" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-ready" "$xb/v1/ingestions/$ready_id/attestations"
body 'b["duplicate"] is False and [e["state"] for e in b["exports"]] == ["ready"]'
call 200 "attestation replay is idempotent" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-ready" "$xb/v1/ingestions/$ready_id/attestations"
body 'b["duplicate"] is True'
call 201 "unapproved job attests to held exports only" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-held" "$xb/v1/ingestions/$held_id/attestations"
body 'b["exports"] and all(e["state"] == "held" and e["hold_reason"] == "UNKNOWN_JOB" for e in b["exports"])'
held_export=$(field "$work/body" 'b["exports"][0]["export_id"]')
call 409 "held export serves no file" -H "$read" "$xb/v1/exports/$held_export/files/0"
call 200 "ready export listed for Windows" -H "$read" "$xb/v1/exports?state=ready"
body 'len(b["items"]) == 1'
export_id=$(field "$work/body" 'b["items"][0]["export_id"]')
call 200 "manifest readable" -H "$read" "$xb/v1/exports/$export_id"
cp "$work/body" "$work/manifest"
files=$(field "$work/manifest" '" ".join(str(f["seq"]) for f in b["files"])')
for seq in $files; do
  [ "$(post -H "$read" "$xb/v1/exports/$export_id/files/$seq")" = 200 ] || fail "file $seq"
  python3 -c 'import hashlib,json,sys; m=json.load(open(sys.argv[1])); f=[x for x in m["files"] if x["seq"]==int(sys.argv[3])][0]; raw=open(sys.argv[2],"rb").read(); raw.decode("utf-8"); assert (hashlib.sha256(raw).hexdigest(), len(raw)) == (f["markdown_sha256"], f["byte_length"])' \
    "$work/manifest" "$work/body" "$seq" || fail "file $seq differs from its manifest entry"
done
ok "every Resource file ($files) matches its manifest SHA-256, length and UTF-8"
python3 - "$work/manifest" "$work" <<'PY'
import json, sys, uuid
m = json.load(open(sys.argv[1]))
files = [{"seq": f["seq"], "result": "installed"} for f in m["files"]]
for name in ("ack", "ack-other"):
    json.dump({"schema_version": "1.0", "ack_id": str(uuid.uuid4()), "manifest_sha256": m["manifest_sha256"],
               "outcome": "published", "files": files}, open(f"{sys.argv[2]}/{name}.json", "w"))
PY
call 401 "export list without a token is refused" "$xb/v1/exports"
call 401 "export list with a wrong token is refused" -H "Authorization: Bearer $(hex 24)" "$xb/v1/exports"
call 403 "export_ack token cannot read" -H "$ack" "$xb/v1/exports"
call 403 "export_read token cannot ACK" -X POST -H "$read" -H "$json" --data-binary @"$work/ack.json" "$xb/v1/exports/$export_id/acks"
call 201 "ACK records the Windows delivery" -X POST -H "$ack" -H "$json" --data-binary @"$work/ack.json" "$xb/v1/exports/$export_id/acks"
body 'b["state"] == "acknowledged" and b["duplicate"] is False'
call 200 "ACK replay is idempotent" -X POST -H "$ack" -H "$json" --data-binary @"$work/ack.json" "$xb/v1/exports/$export_id/acks"
call 409 "a different ACK after acknowledgment conflicts" -X POST -H "$ack" -H "$json" --data-binary @"$work/ack-other.json" "$xb/v1/exports/$export_id/acks"
call 404 "summary is not routed on the export host" -H "$read" "$xb/v1/summary"
call 404 "ingest is not routed on the export host" -X POST -H "Authorization: Bearer $gateway_token" -H "$json" --data-binary @"$report" "$xb/v1/ingestions"
call 404 "GET on the attestation path is not routed" -H "$attest" "$xb/v1/ingestions/$ready_id/attestations"
call 404 "dot-segment path is not routed" --path-as-is -H "$read" "$xb/v1/exports/$export_id/../../summary"
call 404 "export host never reaches n8n webhooks" -X POST -H "$header" -H "$json" --data-binary @"$report" "$xb/webhook/hermes-blog-ingestion"
sleep 10  # refill the webhook bucket before the outage probe

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
call 200 "acknowledged export survives Gateway restart" -H "$read" "$xb/v1/exports/$export_id"
body 'b["state"] == "acknowledged" and b["ack_id"] is not None'
call 200 "ACK replay after restart is idempotent" -X POST -H "$ack" -H "$json" --data-binary @"$work/ack.json" "$xb/v1/exports/$export_id/acks"
call 200 "attestation replay after restart is idempotent" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-ready" "$xb/v1/ingestions/$ready_id/attestations"
# The body the attest command signs: verified_request rebuilds the Publisher
# adapter request from synthetic producer-signed evidence (test trust store).
python3 - "$workload" "$work" <<'PY'
import sys
from pathlib import Path
from unittest.mock import patch
sys.path[:0] = [sys.argv[1], sys.argv[1] + "/tests"]
import producer
from test_trust import material
from publisher import attestation, trust
work = Path(sys.argv[2])
key = producer.new_key()
producer.write_store(work / "producer-keys.json", producer.entry(key))
snapshot, evidence = material("d" * 32)
with patch.object(trust, "TRUST_STORE", work / "producer-keys.json"), \
        patch.object(trust, "_runtime_protected", lambda: None):
    body, _ = attestation.verified_request(snapshot, evidence, producer.sign(key, evidence))
(work / "publisher.json").write_bytes(body)
PY
sign "$work/publisher.json" "$work/attest.pem" "$work/att-publisher"
sleep 12  # refill the webhook bucket after the outage probe
call 201 "Publisher-adapter report persisted through n8n" -X POST -H "$header" -H "$json" --data-binary @"$work/publisher.json" "$url"
publisher_id=$(field "$work/body" 'b["id"]')
call 201 "attester signature over the Publisher body creates ready exports" -X POST -H "$attest" -H "$json" --data-binary @"$work/att-publisher" "$xb/v1/ingestions/$publisher_id/attestations"
body 'b["exports"] and all(e["state"] == "ready" for e in b["exports"])'

gateway_ip=$(docker inspect -f "{{(index .NetworkSettings.Networks \"$id-ingest\").IPAddress}}" "$id-gateway")
[ -n "$gateway_ip" ] || fail "Gateway has no address on the ingest network"
if curl -s -m 3 -o /dev/null "http://$gateway_ip:8787/v1/summary"; then
  fail "host process reached the Gateway on the isolated network"
fi
ok "host cannot reach the Gateway on the internal isolated network"
export_ip=$(docker inspect -f "{{(index .NetworkSettings.Networks \"$id-export\").IPAddress}}" "$id-gateway")
[ -n "$export_ip" ] || fail "Gateway has no address on the export network"
if curl -s -m 3 -o /dev/null "http://$export_ip:8787/v1/summary"; then
  fail "host process reached the Gateway on the export network"
fi
ok "host cannot reach the Gateway on the internal isolated export network"

limited=0
for _ in $(seq 8); do
  [ "$(post -X POST -H "$header" -H "$json" --data-binary @"$report" "$url")" = 429 ] && limited=1 && break
done
[ "$limited" = 1 ] || fail "burst was never rate limited"
ok "burst above the route rate limit returns 429"
echo "RESULT $pass PASS, 0 FAIL (blog-data $commit, $n8n_image, $traefik_image)"
