#!/bin/sh
set -eu
umask 077

password=$(cat /run/secrets/lab_couchdb_password)
case "$password" in
  ''|*[!A-Za-z0-9_+./=:@#%-]*)
    echo 'Unsupported LAB CouchDB password characters' >&2
    exit 1
    ;;
esac
case "${LAB_COUCHDB_USERNAME:-}" in
  ''|*[!A-Za-z0-9_]*) echo 'Invalid LAB CouchDB username' >&2; exit 1 ;;
esac
case "${COUCHDB_PORT:-}" in
  ''|*[!0-9]*) echo 'Invalid LAB CouchDB port' >&2; exit 1 ;;
esac

printf 'user = "%s:%s"\n' "$LAB_COUCHDB_USERNAME" "$password" > /tmp/couch-auth.conf
base="http://couchdb-1:$COUCHDB_PORT"
ensure_system_databases() {
  for database in _users _replicator _global_changes; do
    status=$(curl -sS --output /dev/null --write-out '%{http_code}' \
      --config /tmp/couch-auth.conf -X PUT "$base/$database")
    case "$status" in
      2??|412) : ;;
      *) echo "LAB CouchDB system database failed: $database (HTTP $status)" >&2; exit 1 ;;
    esac
  done
}

curl -fsS --config /tmp/couch-auth.conf "$base/_cluster_setup" > /tmp/couch-state.json
if grep -Eq '"state"[[:space:]]*:[[:space:]]*"cluster_finished"' /tmp/couch-state.json; then
  ensure_system_databases
  echo 'LAB CouchDB cluster is already configured'
  exit 0
fi

for node in 2 3; do
  printf '{"action":"enable_cluster","bind_address":"0.0.0.0","username":"%s","password":"%s","port":%s,"node_count":"3","remote_node":"couchdb@couchdb-%s.infra_net","remote_current_user":"%s","remote_current_password":"%s"}\n' \
    "$LAB_COUCHDB_USERNAME" "$password" "$COUCHDB_PORT" "$node" "$LAB_COUCHDB_USERNAME" "$password" > /tmp/couch-request.json
  curl -fsS --config /tmp/couch-auth.conf -X POST -H 'Content-Type: application/json' \
    --data-binary @/tmp/couch-request.json "$base/_cluster_setup" > /dev/null
  printf '{"action":"add_node","host":"couchdb-%s.infra_net","port":%s,"username":"%s","password":"%s"}\n' \
    "$node" "$COUCHDB_PORT" "$LAB_COUCHDB_USERNAME" "$password" > /tmp/couch-request.json
  curl -fsS --config /tmp/couch-auth.conf -X POST -H 'Content-Type: application/json' \
    --data-binary @/tmp/couch-request.json "$base/_cluster_setup" > /dev/null
done

printf '{"action":"finish_cluster"}\n' > /tmp/couch-request.json
curl -fsS --config /tmp/couch-auth.conf -X POST -H 'Content-Type: application/json' \
  --data-binary @/tmp/couch-request.json "$base/_cluster_setup" > /dev/null
ensure_system_databases
rm -f /tmp/couch-auth.conf /tmp/couch-request.json /tmp/couch-state.json
printf '%s\n' 'LAB CouchDB cluster setup completed'
