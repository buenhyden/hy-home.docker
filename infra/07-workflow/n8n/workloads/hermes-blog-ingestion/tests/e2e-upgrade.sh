#!/usr/bin/env bash
# Disposable synthetic check of the Gateway image change on one Docker host:
# a store written by the previous pin (DB schema 2) is backed up online,
# upgraded in place by the current pin (schema 3) without losing a receipt,
# restored from that backup into a fresh volume, and a schema-3 backup with an
# export is restored again. Synthetic tokens and keys only; no network, no live
# container, volume, path or secret. Removes everything it creates on exit.
# Needs Docker and gh access to the private Blog-data repository.
# Usage: tests/e2e-upgrade.sh [previous-blog-data-commit]
set -euo pipefail
workload=$(cd "$(dirname "$0")/.." && pwd)
root=$(git -C "$workload" rev-parse --show-toplevel)
compose=$root/infra/07-workflow/n8n/docker-compose.yml
new=$(sed -n 's#.*image: hy-home/blog-ingestion:\([0-9a-f]\{40\}\)$#\1#p' "$compose")
# The pin PR #699 shipped: Gateway without Resource Export, DB schema 2.
old=${1:-a43d824334e636ddeab034982b36c0700a9d8f93}
id=e2e-up-$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')
work=$(mktemp -d)
pass=0
cleanup() {
  docker rm -f "$id-old" "$id-new" "$id-restored" "$id-again" >/dev/null 2>&1 || true
  docker volume rm "$id-a" "$id-b" "$id-c" >/dev/null 2>&1 || true
  rm -rf "$work"
}
trap cleanup EXIT
ok() { pass=$((pass + 1)); echo "PASS $*"; }
fail() { echo "FAIL $*"; exit 1; }
hex() { od -An -N"$1" -tx1 /dev/urandom | tr -d ' \n'; }

# shellcheck source=gateway-image.sh
. "$workload/tests/gateway-image.sh"
for commit in "$old" "$new"; do
  build_gateway_image "$commit" "$work/src-$commit" "hy-home/blog-ingestion-e2e:$commit"
done

ingest=$(hex 24)
attest=$(hex 24)
read=$(hex 24)
python3 - "$work" "$ingest" "$attest" "$read" <<'PY'
import hashlib, json, os, sys
from cryptography.hazmat.primitives import serialization as s
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
work, ingest, attest, read = sys.argv[1:]
k = Ed25519PrivateKey.generate()
with open(f"{work}/attest.pem", "wb") as f:
    f.write(k.private_bytes(s.Encoding.PEM, s.PrivateFormat.PKCS8, s.NoEncryption()))
os.chmod(f"{work}/attest.pem", 0o600)
public = k.public_key().public_bytes(s.Encoding.PEM, s.PublicFormat.SubjectPublicKeyInfo).decode()
grant = lambda t, scopes: {"producer": "hermes", "scopes": scopes,
                           "token_sha256": hashlib.sha256(t.encode()).hexdigest()}
base = {"schema_version": "1.0", "data_dir": "/data", "host": "127.0.0.1", "port": 8787}
# The previous Gateway knows neither attest/export scopes nor the export block.
json.dump({**base, "credentials": [grant(ingest, ["ingest", "read"])]},
          open(f"{work}/config-old.json", "w"))
json.dump({**base, "credentials": [grant(ingest, ["ingest", "read"]), grant(attest, ["attest"]),
                                   grant(read, ["export_read"])],
           "export": {"attestation_keys": [{"key_id": "attest-e2e", "public_key": public}]}},
          open(f"{work}/config-new.json", "w"))
PY
python3 - "$workload/tests/fixtures/synthetic-report.json" "$work/devops.json" <<'PY'
import hashlib, json, sys
d = json.load(open(sys.argv[1]))
d.update(job_id="25674fbc0bf3", run_id="2026-10-31", fire_id="cron-02",
         source_text="Synthetic DevOps report.")
d["idempotency_key"] = "devops-" + d["run_id"]
d["source_sha256"] = hashlib.sha256(d["source_text"].encode()).hexdigest()
d["items"] = [{"item_id": "devops-1", "kind": "devops", "title": "Synthetic DevOps item",
               "body": "Synthetic body for the upgrade E2E.",
               "source_url": "https://example.org/devops-1"}]
json.dump(d, open(sys.argv[2], "w"))
PY
python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); from publisher import attestation as a
open(sys.argv[4], "wb").write(a.request_body("attest-e2e", a.load_signing_key(sys.argv[3]), a.message(open(sys.argv[2], "rb").read())))' \
  "$workload" "$work/devops.json" "$work/attest.pem" "$work/attestation.json"
chmod 0644 "$work"/config-*.json "$work"/devops.json "$work"/attestation.json

volume() { # volume <name> [store-file]: data/, backup/ and both configs, owned by 10001
  docker volume create "$1" >/dev/null
  docker run --rm --user 0 --network none --entrypoint sh -v "$1:/v" -v "$work:/in:ro" \
    "hy-home/blog-ingestion-e2e:$new" -c '
      set -e
      mkdir /v/data /v/backup
      cp /in/config-old.json /in/config-new.json /v/
      if [ -n "$1" ]; then cp "/in/$1" /v/data/ingestion.sqlite3; fi
      chown -R 10001:10001 /v
      chmod 0700 /v/data /v/backup
      chmod 0600 /v/config-old.json /v/config-new.json
      if [ -n "$1" ]; then chmod 0600 /v/data/ingestion.sqlite3; fi' sh "${2:-}"
}
req() { # req <container> <method> <path> <token> [body-file] -> "status json"
  docker exec -i "$1" node -e '
    const [m, p, t] = process.argv.slice(1);
    const body = m === "POST" ? require("fs").readFileSync(0) : undefined;
    fetch("http://127.0.0.1:8787" + p, { method: m, body,
      headers: { authorization: "Bearer " + t, "content-type": "application/json" } })
      .then(async (r) => console.log(r.status + " " + (await r.text())), () => console.log("000 {}"));
  ' "$2" "$3" "$4" <"${5:-/dev/null}" 2>/dev/null || echo "000 {}"
}
serve() { # serve <container> <volume> <commit> <config>
  docker run -d --name "$1" --network none --user 10001:10001 --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --mount "type=volume,src=$2,dst=/data,volume-subpath=data" \
    --mount "type=volume,src=$2,dst=/backup,volume-subpath=backup" \
    --mount "type=volume,src=$2,dst=/run/config.json,volume-subpath=$4,readonly" \
    "hy-home/blog-ingestion-e2e:$3" serve --config /run/config.json >/dev/null
  for _ in $(seq 30); do
    [ "$(req "$1" GET /v1/summary x | cut -d' ' -f1)" = 401 ] && return
    sleep 1
  done
  fail "$1 never listened: $(docker logs --tail 3 "$1" 2>&1)"
}
expect() { # expect <status> <label> <"status json"> [python assertion on b]
  [ "${3%% *}" = "$1" ] || fail "$2: got ${3:0:300}"
  [ -z "${4:-}" ] || python3 -c "import json,sys; b=json.loads(sys.argv[1]); assert $4, b" "${3#* }" ||
    fail "$2: ${3:0:300}"
  ok "$2 ($1)"
}
schema() {
  docker exec "$1" node -e "const {DatabaseSync}=require('node:sqlite'); console.log(new DatabaseSync('/data/ingestion.sqlite3',{readOnly:true}).prepare('PRAGMA user_version').get().user_version)" 2>/dev/null
}
backup() { # backup <container> <name>: online backup with that container's image
  docker exec "$1" node scripts/ops/ingestion-gateway.mjs backup --config /run/config.json \
    --output "/backup/$2" >/dev/null || fail "$1 backup"
  docker cp "$1:/backup/$2" "$work/$2" >/dev/null && chmod 0644 "$work/$2"
}

# 1. The previous pin writes a schema-2 store and takes an online backup.
volume "$id-a"
serve "$id-old" "$id-a" "$old" config-old.json
answer=$(req "$id-old" POST /v1/ingestions "$ingest" "$work/devops.json")
expect 201 "previous Gateway persists a report" "$answer" 'b["persisted"] is True'
report_id=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["id"])' "${answer#* }")
[ "$(schema "$id-old")" = 2 ] || fail "previous store is not schema 2"
ok "previous store is DB schema 2"
backup "$id-old" schema2.sqlite3
ok "online backup of the schema-2 store"
docker stop "$id-old" >/dev/null

# 2. The current pin upgrades that store in place; receipts survive.
serve "$id-new" "$id-a" "$new" config-new.json
[ "$(schema "$id-new")" = 3 ] || fail "store was not upgraded to schema 3"
ok "current Gateway upgrades the store to DB schema 3"
expect 200 "upgraded store keeps the receipt" "$(req "$id-new" GET "/v1/ingestions/$report_id" "$ingest")"
expect 200 "replay after upgrade is the same persisted report" \
  "$(req "$id-new" POST /v1/ingestions "$ingest" "$work/devops.json")" \
  "b[\"id\"] == \"$report_id\" and b[\"duplicate\"] is True"
expect 201 "a pre-upgrade report can be attested into a ready export" \
  "$(req "$id-new" POST "/v1/ingestions/$report_id/attestations" "$attest" "$work/attestation.json")" \
  '[e["state"] for e in b["exports"]] == ["ready"]'
export_id=$(req "$id-new" GET "/v1/exports?state=ready" "$read" | cut -d' ' -f2- |
  python3 -c 'import json,sys; print(json.load(sys.stdin)["items"][0]["export_id"])')
backup "$id-new" schema3.sqlite3
ok "online backup of the schema-3 store with an export"

# 3. The schema-2 backup restores into a fresh volume and upgrades there too.
volume "$id-b" schema2.sqlite3
serve "$id-restored" "$id-b" "$new" config-new.json
[ "$(schema "$id-restored")" = 3 ] || fail "restored schema-2 backup was not upgraded"
expect 200 "restored schema-2 backup keeps the receipt" \
  "$(req "$id-restored" GET "/v1/ingestions/$report_id" "$ingest")"

# 4. The schema-3 backup restores with its export and manifest intact.
volume "$id-c" schema3.sqlite3
serve "$id-again" "$id-c" "$new" config-new.json
expect 200 "restored schema-3 backup keeps the ready export" \
  "$(req "$id-again" GET "/v1/exports/$export_id" "$read")" 'b["state"] == "ready" and b["files"]'
echo "RESULT $pass PASS, 0 FAIL (blog-data $old -> $new)"
