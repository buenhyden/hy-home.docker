#!/usr/bin/env bash
# RUN-0105 maintenance window steps after the W1 source bootstrap. The bootstrap
# copies this file with the protected helpers into $P01_SCRIPT_DIR and checks its
# hash; run that copy, never the checkout's. Each step reads the window state from
# $XDG_RUNTIME_DIR/p01-window.vars, so a failed step exits this script, not the
# owner's shell. No token, share, accessor or policy hash is printed.
set +x
set -uo pipefail
umask 077

usage() {
  echo "usage: $0 token <stage>|check-token <stage>|retire-token <file>|w1|audit-list|root-sweep|roles-plan|roles-diff|roles-apply|w2|lease-start|w3 <new dir> <expected version> [--writers-checked]|lease-bind|w3a-inputs|w3a|w3b|w4 <recorded device/inode>|preflight|metrics-rotate|metrics-revoke|renderer-expiry <since>|host-hold|status|w5-create|agent-restart|revoke-root|evidence <dir>|cleanup [--keep-root] [--keep-w2] [--discard-root] [--discard-metrics]" >&2
  exit 2
}
[ "$#" -ge 1 ] || usage
step=$1
shift

: "${XDG_RUNTIME_DIR:?}"
vars="$XDG_RUNTIME_DIR/p01-window.vars"
# The bootstrap appends with declare -p; a retry appends again. The last value wins,
# except for the bootstrap's readonly variables, where the first one stays.
# shellcheck disable=SC1090
[ -f "$vars" ] && . "$vars" 2>/dev/null
HOME_ROOT=/home/hyunyoun/data/hy-home.docker
CA="$HOME_ROOT/secrets/certs/rootCA.pem"
CA_SHA256=6b7c5c752a6dee074b7f9c83da98b2b8784831edde3d8f50b694acd0e280af87
CONNECT_IP=192.168.0.13
CLUSTER_ID=51fbfa38-a715-7dca-629f-3f07233749f4
TLS=(--ca "$CA" --ca-sha256 "$CA_SHA256" --connect-ip "$CONNECT_IP" --expected-cluster-id "$CLUSTER_ID")
helper() { /usr/bin/env -i PATH=/usr/bin:/bin /usr/bin/python3 -I -S "${P01_SCRIPT_DIR:?run the W1 bootstrap first}/$1" "${@:2}"; }
token_file() {
  case "$1" in w0|w1|w3a|w5|w7|kv) printf '%s\n' "$XDG_RUNTIME_DIR/p01-op-$1.token" ;; *) usage ;; esac
}
private() { [ "$(stat -c '%a %h' "$1" 2>/dev/null)" = "600 1" ]; }
# The OpenBao CLI inside the server container, authenticated from a token file.
bao_as() { (unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG COMPOSE_FILE; cd "$HOME_ROOT" && BAO_TOKEN="$(cat "$1")" /usr/bin/docker compose exec -T -e BAO_TOKEN openbao bao "${@:2}"); }
# A fresh custody directory per attempt, recorded for later steps and cleanup.
new_dir() {
  local dir
  dir="$(/usr/bin/mktemp -d "${P01_RUNTIME_DIR:?run the W1 bootstrap first}/$2.XXXXXX")" || exit 1
  printf -v "$1" '%s' "$dir"
  declare -p "$1" >>"$vars"
}

# metrics-rotate and metrics-revoke: $root is the W1 root, $d the p01-metrics custody
# directory and $custody the metrics custody file. Values go over stdin only.
feed() { printf '%s' "$(cat "$1")"; }
# A root call; its error text stays in the custody directory for the checks below.
as_root() { bao_as "$root" "$@" 2>"$d/last.err"; }
errs() { [ "$(grep -c "$1" "$d/last.err")" = 1 ]; }
# Positive controls: root still authenticates and the server is unsealed.
controls() { bao_as "$root" token lookup </dev/null >/dev/null 2>&1 && docker exec openbao bao status >/dev/null 2>&1; }
# The new token counts as revoked only when the server then refuses its lookup with "bad token".
revoke_new() {
  if feed "$d/new.token" | as_root write auth/token/revoke token=- >/dev/null &&
    ! feed "$d/new.token" | as_root write -format=json auth/token/lookup token=- >/dev/null && errs 'bad token'; then
    rm -f "$d/new.unrevoked"
    echo "new token revoked" >&2
  else
    : >"$d/new.unrevoked"
    echo "new token: NOT confirmed revoked; run metrics-revoke before revoke-root" >&2
    return 1
  fi
}
# The old token counts as revoked only on "invalid accessor" plus the positive controls.
revoke_old() {
  if feed "$d/old.accessor" | as_root write auth/token/revoke-accessor accessor=- >/dev/null &&
    ! feed "$d/old.accessor" | as_root write -format=json auth/token/lookup-accessor accessor=- >/dev/null &&
    errs 'invalid accessor' && controls; then
    rm -f "$d/old.unrevoked"
    echo "old: revoked"
  else
    : >"$d/old.unrevoked"
    echo "old token: NOT confirmed revoked; run metrics-revoke before revoke-root" >&2
    return 1
  fi
}
write_custody() {
  local next="${custody%/*}/.openbao_metrics_token.custody.new"
  rm -f "$next"
  if (umask 077; printf 'accessor=%s\nexpires=%s\nissued=%s\npolicy=prometheus\n' "$(cat "$d/new.accessor")" \
    "$(jq -r '.data.expire_time' "$d/new.json")" "$(date -u +%FT%TZ)" >"$next") && mv "$next" "$custody"; then
    rm -f "$d/custody.unwritten"
  else
    : >"$d/custody.unwritten"
    echo "custody write failed: run metrics-revoke before revoke-root" >&2
    return 1
  fi
}

case "$step" in
token)
  # A new OIDC login per stage; keep the UI session signed in (sign-out revokes it).
  [ "$#" -eq 1 ] || usage
  f="$(token_file "$1")" || exit 2
  # Only into the tmpfs runtime directory the bootstrap checked.
  [ "$XDG_RUNTIME_DIR" = "${P01_RUNTIME_DIR:-}" ] || { echo "run the W1 bootstrap first" >&2; exit 1; }
  [ ! -e "$f" ] && [ ! -L "$f" ] || shred -u "$f" || exit 1
  IFS= read -rsp "$1 operator token> " v </dev/tty
  printf '\n'
  (set -C; printf '%s' "$v" >"$f") || exit 1
  unset v
  private "$f" || { echo "token file is not 0600 single-link" >&2; exit 1; }
  echo "token ok $1"
  ;;
check-token)
  # Field checks only: what protected-maintenance.py and revoke-root require.
  [ "$#" -eq 1 ] || usage
  f="$(token_file "$1")" || exit 2
  api() {
    # -q: no ~/.curlrc, which could turn on a trace that prints the header.
    printf 'header = "X-Vault-Token: %s"\n' "$(cat "$f")" |
      /usr/bin/curl -q -s -m 10 --noproxy '*' --proto =https --config - --cacert "$CA" \
        --resolve "openbao.hy.home.arpa:443:$CONNECT_IP" "https://openbao.hy.home.arpa/v1/$1"
  }
  api auth/token/lookup-self | jq -c '{errors, entity_id_set: ((.data.entity_id // "") != ""),
    policies: .data.policies, ttl: .data.ttl, creation_ttl: .data.creation_ttl,
    renewable: .data.renewable, path: .data.path, meta: .data.meta, identity_policies: .data.identity_policies}'
  api sys/generate-root-token/attempt | jq -c '{errors, started: .data.started, progress: .data.progress, complete: .data.complete}'
  ;;
w1)
  f="$(token_file w1)"
  private "$f" || { echo "run: $0 token w1" >&2; exit 1; }
  # An attempt that got as far as the server keeps its custody for recovery (exit 2).
  if [ -n "${P01_CUSTODY_DIR:-}" ] && [ -e "$P01_CUSTODY_DIR/initialization.json" ] && [ ! -e "$P01_CUSTODY_DIR/state.json" ]; then
    echo "previous W1 attempt in $P01_CUSTODY_DIR is unresolved: recover it before a new attempt" >&2
    exit 1
  fi
  new_dir P01_CUSTODY_DIR p01-custody
  secrets="$(/usr/bin/mktemp -d "$P01_RUNTIME_DIR/p01-w1.XXXXXX")" || exit 1
  # Shares never outlive this step, even on Ctrl-C.
  trap 'find "$secrets" -type f -exec shred -u {} + 2>/dev/null; rmdir "$secrets" 2>/dev/null' EXIT
  trap 'exit 130' INT TERM HUP QUIT
  for n in share-1 share-2; do
    IFS= read -rsp "W1 $n> " v </dev/tty
    printf '\n'
    printf '%s' "$v" >"$secrets/$n" || exit 1
  done
  unset v
  exec 5<"$f" 6<"$secrets/share-1" 7<"$secrets/share-2" || exit 1
  helper protected-maintenance.py "${TLS[@]}" \
    --custody-directory "$P01_CUSTODY_DIR" --operator-fd 5 --share-one-fd 6 --share-two-fd 7
  status=$?
  exec 5<&- 6<&- 7<&-
  exit "$status"
  ;;
root-sweep)
  # After W1 and before W1c, every window. With audit-list, the only places a new root reaches the CLI.
  root="${P01_CUSTODY_DIR:?run w1 first}/root.token"
  err="$(/usr/bin/mktemp "$XDG_RUNTIME_DIR/p01-sweep-err.XXXXXX")" || exit 1
  trap 'rm -f "$err"' EXIT
  root_accessors() {
    local list a p
    list="$(bao_as "$root" list -format=json auth/token/accessors | jq -er '.[]')" || return 1
    for a in $list; do
      [ "$a" = "$self" ] && continue
      # A token that expired or was revoked with its parent since the list is gone, not a failure.
      # stdout holds only the policy list; errors stay on stderr.
      if p="$(bao_as "$root" write -field=policies auth/token/lookup-accessor accessor="$a" 2>"$err")"; then
        case " $(printf '%s' "$p" | tr -d '[]') " in *" root "*) printf '%s\n' "$a" ;; esac
      else
        grep -qE 'invalid accessor|No token found' "$err" || { cat "$err" >&2; return 1; }
      fi
    done
    return 0
  }
  self="$(bao_as "$root" read -field=accessor auth/token/lookup-self)" && [ -n "$self" ] || exit 1
  stale="$(root_accessors)" || exit 1
  for a in $stale; do
    bao_as "$root" write auth/token/revoke-accessor accessor="$a" >/dev/null 2>"$err" ||
      grep -qE 'invalid accessor|No token found' "$err" || { cat "$err" >&2; exit 1; }
  done
  printf 'revoked=%s\n' "$(printf '%s' "$stale" | grep -c .)"
  left="$(root_accessors)" || exit 1
  printf 'remaining=%s\n' "$(printf '%s' "$left" | grep -c .)"
  [ -z "$left" ]
  ;;
roles-plan | roles-apply)
  if [ "$step" = roles-plan ]; then
    new_dir P01_ROLES_PLAN_DIR p01-roles-plan
    dir=$P01_ROLES_PLAN_DIR mode=plan
  else
    : "${P01_ROLES_PLAN_DIR:?run roles-plan first}"
    new_dir P01_ROLES_CUSTODY_DIR p01-roles
    dir=$P01_ROLES_CUSTODY_DIR mode=apply
  fi
  exec 3<"${P01_CUSTODY_DIR:?run w1 first}/root.token" || exit 1
  helper protected-renderer-roles.py "$mode" "${TLS[@]}" \
    --custody-directory "$dir" --w1-custody-directory "$P01_CUSTODY_DIR" --root-fd 3
  status=$?
  exec 3<&-
  [ "$status" = 0 ] || exit "$status"
  jq -c '.targets[] | {path, changed}' "$dir/state.json"
  if [ "$mode" = apply ]; then
    # A different prior value means someone changed a target between plan and apply.
    prior() { jq -c '[.targets[] | {path, prior_sha256}]' "$1/state.json"; }
    if [ "$(prior "$P01_ROLES_PLAN_DIR")" = "$(prior "$dir")" ]; then echo prior:same; else echo prior:DIFFERENT; status=1; fi
    echo "agent: $(docker inspect -f '{{.State.Health.Status}}' openbao-agent)"
    docker exec openbao-agent sh -c 'ls -l /openbao/out/*/*.version' | awk '{print $6, $7, $8, $9}'
  fi
  exit "$status"
  ;;
roles-diff)
  # HOME's current policy text against the approved files; policy text holds no credential.
  : "${P01_ROLES_PLAN_DIR:?run roles-plan first}"
  for p in renderer:renderer operator:hy-home-operator renderer-issuer:renderer-issuer renderer-cleanup:renderer-cleanup; do
    f=${p%%:*} n=${p#*:}
    echo "== $n (< HOME / > approved)"
    diff <(jq -r --arg k "sys/policies/acl/$n" '.[$k] // ""' "$P01_ROLES_PLAN_DIR/prior-state.json") \
      "${P01_CLIENT_DIR:?}/infra/03-security/openbao/config/policies/$f.hcl" | grep '^[<>]'
  done
  exit 0
  ;;
revoke-root)
  f="$(token_file w7)"
  private "$f" || { echo "run: $0 token w7" >&2; exit 1; }
  new_dir P01_REVOKE_CUSTODY_DIR p01-revoke
  exec 3<"${P01_CUSTODY_DIR:?run w1 first}/root.token" 4<"$f" || exit 1
  helper protected-token-operations.py revoke-root "${TLS[@]}" \
    --custody-directory "$P01_REVOKE_CUSTODY_DIR" --w1-custody-directory "$P01_CUSTODY_DIR" --root-fd 3 --operator-fd 4
  status=$?
  exec 3<&- 4<&-
  exit "$status"
  ;;
evidence)
  # Credential-free receipts to owner storage outside tmpfs, the repository and docs.
  [ "$#" -eq 1 ] || usage
  case "$1" in /*) ;; *) usage ;; esac
  target="$(realpath -m -- "$1")"
  case "$target" in "$HOME_ROOT"* | "$XDG_RUNTIME_DIR"* | /dev/shm* | /tmp*)
    echo "evidence must be outside the repository and tmpfs" >&2; exit 1 ;; esac
  install -d -m 0700 "$target" || exit 1
  set -- "$target"
  cd "$XDG_RUNTIME_DIR" || exit 1
  n=0
  for d in p01-custody.* p01-roles-plan.* p01-roles.* p01-revoke.* p01-token.* p01-k8s.*; do
    # p01-k8s.*: original UID/replicas/selector, changed list and Finish time; no Secret data.
    for f in state.json prior-state.json operation-intent.json 0.json 1.json 2.json changed finish-epoch restored; do
      [ -f "$d/$f" ] || continue
      cp --preserve=mode --parents "$d/$f" "$1"/ || exit 1
      n=$((n + 1))
    done
  done
  echo "copied=$n"
  for f in "$1"/*/state.json; do
    [ -f "$f" ] && printf '%s %s\n' "${f#"$1"/}" "$(jq -r '.state // "-"' "$f")"
  done
  ;;
cleanup)
  # Revoke the stage tokens, then delete every custody and secret file.
  # --keep-root: an unsealed server whose OIDC is broken keeps root, tokens and vars.
  # --keep-w2: an unresolved W2 exit 2 keeps its custody.
  # --discard-root: delete W1 custody before W7 proved root revoked (W1 exit 2, sealed server).
  # --discard-metrics: delete a metrics-rotate directory whose token was not confirmed revoked.
  P01_KEEP_ROOT=0 P01_KEEP_W2=0 discard=0 discard_metrics=0
  for a in "$@"; do
    case "$a" in --keep-root) P01_KEEP_ROOT=1 ;; --keep-w2) P01_KEEP_W2=1 ;; --discard-root) discard=1 ;;
      --discard-metrics) discard_metrics=1 ;; *) usage ;; esac
  done
  if [ "$discard_metrics" != 1 ] && compgen -G "$XDG_RUNTIME_DIR/p01-metrics.*/*.un*" >/dev/null; then
    echo "metrics-rotate left an unconfirmed revoke or custody write: run metrics-revoke, or pass --discard-metrics" >&2
    exit 1
  fi
  if [ "$P01_KEEP_ROOT" != 1 ] && [ "$discard" != 1 ] && compgen -G "$XDG_RUNTIME_DIR/p01-custody.*/root.token" >/dev/null; then
    revoked=0
    for r in "$XDG_RUNTIME_DIR"/p01-revoke.*/state.json; do
      [ -f "$r" ] && [ "$(jq -r .state "$r")" = ROOT_REVOKED_OPERATOR_HEALTHY ] && revoked=1
    done
    [ "$revoked" = 1 ] || {
      echo "root custody exists and W7 did not revoke root: run revoke-root, or pass --keep-root or --discard-root" >&2
      exit 1
    }
  fi
  if [ "$P01_KEEP_ROOT" != 1 ]; then
    for f in "$XDG_RUNTIME_DIR"/p01-op-*.token; do
      [ -f "$f" ] || continue
      bao_as "$f" token revoke -self </dev/null >/dev/null 2>&1 &&
        echo "revoked ${f##*/}" || echo "revoke failed ${f##*/} (expired or already revoked)"
    done
  fi
  for d in "$XDG_RUNTIME_DIR"/p01-custody.* "$XDG_RUNTIME_DIR"/p01-token.* \
    "$XDG_RUNTIME_DIR"/p01-roles.* "$XDG_RUNTIME_DIR"/p01-roles-plan.* "$XDG_RUNTIME_DIR"/p01-revoke.* \
    "$XDG_RUNTIME_DIR"/p01-w1.* "$XDG_RUNTIME_DIR"/p01-w3a.* "$XDG_RUNTIME_DIR"/p01-metrics.*; do
    [ -d "$d" ] || continue
    case "$d" in */p01-token.*) [ "${P01_KEEP_W2:-0}" = 1 ] && continue ;; esac
    case "$d" in */p01-custody.*) [ "${P01_KEEP_ROOT:-0}" = 1 ] && continue ;; esac
    find "$d" -type f -exec shred -u {} + && find "$d" -depth -type d -empty -delete
  done
  [ "${P01_KEEP_ROOT:-0}" = 1 ] ||
    for f in "$XDG_RUNTIME_DIR"/p01-op-*.token; do [ -f "$f" ] && shred -u "$f"; done
  [ "${P01_KEEP_ROOT:-0}" = 1 ] || rm -f "$vars"
  # What is left: the p01-client.* helper copies (no secret) and, if any, p01-inputs.* and p01-k8s.*.
  find "$XDG_RUNTIME_DIR" -maxdepth 1 -name 'p01-*' -printf '%f\n'
  ;;
retire-token)
  # A leftover operator token from an earlier window: revoke it, prove it is gone, delete it.
  [ "$#" -eq 1 ] || usage
  t="$(realpath -e -- "$1")" || exit 1
  if [ -L "$1" ] || ! private "$t"; then echo "token file must be a 0600 single-link regular file" >&2; exit 1; fi
  set -- "$t"
  err="$(/usr/bin/mktemp "$XDG_RUNTIME_DIR/p01-retire-err.XXXXXX")" || exit 1
  trap 'rm -f "$err"' EXIT
  if ! policies="$(bao_as "$1" read -field=policies auth/token/lookup-self </dev/null 2>"$err")"; then
    # Only a token the server refuses is gone; any other failure keeps the file.
    if grep -qiE 'permission denied|bad token|invalid token|Code: 403' "$err"; then
      shred -u "$1" && echo "already expired; file removed"
      exit 0
    fi
    echo "lookup failed for another reason; file kept" >&2
    exit 1
  fi
  [ "$policies" = "[hy-home-operator]" ] || { echo "not an operator token: $policies" >&2; exit 1; }
  bao_as "$1" token revoke -self </dev/null >/dev/null || exit 1
  ! bao_as "$1" token lookup </dev/null >/dev/null 2>&1 || { echo "token still valid" >&2; exit 1; }
  shred -u "$1" && echo "revoked; file removed"
  ;;
audit-list)
  # W3a gate input, with the W1 root after W1 and before W1c. Names and types only.
  root="${P01_CUSTODY_DIR:?run w1 first}/root.token"
  for kind in audit secrets auth; do
    out="$(bao_as "$root" "$kind" list -format=json </dev/null)" || { echo "$kind: rc=1" >&2; exit 1; }
    echo "== $kind"
    jq -r 'to_entries[] | "\(.key) \(.value.type)"' <<<"$out" || { echo "$kind: rc=1" >&2; exit 1; }
  done
  ;;
w2)
  # Snapshot token into the fixed secrets/backup/openbao target, never overwriting.
  new_dir P01_TOKEN_CUSTODY_DIR p01-token
  exec 3<"${P01_CUSTODY_DIR:?run w1 first}/root.token" || exit 1
  helper protected-token-operations.py issue-snapshot-token "${TLS[@]}" \
    --custody-directory "$P01_TOKEN_CUSTODY_DIR" --w1-custody-directory "$P01_CUSTODY_DIR" --root-fd 3 \
    --home-root "$HOME_ROOT" --expected-home-device 64512 --expected-home-inode 4338469 \
    --policy-sha256 1aa658e05aee76127c7961abd218020fe6a319fd26253c78ecefb3ae99d4b622
  status=$?
  exec 3<&-
  exit "$status"
  ;;
lease-start)
  # The moment the writers were confirmed stopped, before the snapshot.
  new_dir P01_INPUTS p01-inputs
  helper protected-restore-inputs.py lease-start --directory "$P01_INPUTS"
  ;;
w3)
  # The writers must be zero right before the snapshot: checked here when this shell
  # holds the K8s state, otherwise the external operator's check is attested.
  if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then usage; fi
  : "${P01_INPUTS:?run lease-start first}"
  case "$1" in /*) ;; *) usage ;; esac
  if [ -n "${P01_K8S_STATE:-}" ]; then
    P01_K8S_STATE="$P01_K8S_STATE" bash "$P01_SCRIPT_DIR/k8s-writers.sh" check || exit 1
  else
    [ "${3:-}" = --writers-checked ] || { echo "run k8s-writers.sh check, then pass --writers-checked" >&2; exit 1; }
  fi
  P01_SNAPSHOT_DIRECTORY=$1
  declare -p P01_SNAPSHOT_DIRECTORY >>"$vars"
  # A new path only: mkdir fails on an existing one.
  (umask 077; /usr/bin/mkdir -- "$P01_SNAPSHOT_DIRECTORY") || exit 1
  exec 3<"$HOME_ROOT/secrets/backup/openbao/snapshot_token.txt" || exit 1
  helper protected-raft-snapshot.py "${TLS[@]}" --output-directory "$P01_SNAPSHOT_DIRECTORY" \
    --artifact-name raft-pre-upgrade.snap --token-fd 3 --expected-version "$2"
  status=$?
  exec 3<&-
  exit "$status"
  ;;
lease-bind)
  helper protected-restore-inputs.py lease-bind --directory "${P01_INPUTS:?run lease-start first}" \
    --snapshot-receipt "${P01_SNAPSHOT_DIRECTORY:?run w3 first}/raft-pre-upgrade.snap.receipt.json" --minutes 60
  ;;
w3a-inputs)
  # Bundle, security receipt and contract from the same approved commit as the issuer helper.
  : "${issuer_commit:?}" "${operator_tools:?}" "${P01_INPUTS:?}" "${P01_SNAPSHOT_DIRECTORY:?}"
  [ "$issuer_commit" = "${P01_COMMIT:?}" ] || { echo "issuer_commit must equal P01_COMMIT" >&2; exit 1; }
  # A rerun keeps a bundle and receipt that were already written and retries the contract;
  # a failed bundle or receipt leaves nothing behind (the producer never overwrites).
  [ -e "$P01_INPUTS/bundle" ] || helper protected-restore-inputs.py bundle --repository "$HOME_ROOT" \
    --revision "$P01_COMMIT" --target "$P01_INPUTS/bundle" || exit 1
  [ -e "$P01_INPUTS/security-receipt.json" ] || helper protected-restore-inputs.py security-receipt --repository "$HOME_ROOT" \
    --revision "$P01_COMMIT" --output "$P01_INPUTS/security-receipt.json" || exit 1
  line="$(helper protected-restore-inputs.py contract --output "$P01_INPUTS/restore-contract.json" \
    --snapshot "$P01_SNAPSHOT_DIRECTORY/raft-pre-upgrade.snap" \
    --snapshot-receipt "$P01_SNAPSHOT_DIRECTORY/raft-pre-upgrade.snap.receipt.json" \
    --lease "$P01_INPUTS/quiescence-lease.json" \
    --helper-directory "$operator_tools/$issuer_commit" --bundle "$P01_INPUTS/bundle" \
    --revision "$P01_COMMIT" --security-receipt "$P01_INPUTS/security-receipt.json" \
    --repository "$HOME_ROOT")" || exit 1
  echo "$line"
  P01_RESTORE_CONTRACT="$P01_INPUTS/restore-contract.json"
  P01_RESTORE_CONTRACT_SHA256="${line#CONTRACT_WRITTEN }"
  P01_SECURITY_RECEIPT="$P01_INPUTS/security-receipt.json"
  declare -p P01_RESTORE_CONTRACT P01_RESTORE_CONTRACT_SHA256 P01_SECURITY_RECEIPT >>"$vars"
  ;;
w3a)
  # Isolated semantic restore: HOME read token, W1 root and two shares on four FDs.
  f="$(token_file w3a)"
  private "$f" || { echo "run: $0 token w3a (before W3)" >&2; exit 1; }
  exec 4<"${P01_INPUTS:?}/quiescence-lease.json" || exit 1
  secrets="$(/usr/bin/mktemp -d "$P01_RUNTIME_DIR/p01-w3a.XXXXXX")" || exit 1
  trap 'find "$secrets" -type f -exec shred -u {} + 2>/dev/null; rmdir "$secrets" 2>/dev/null' EXIT
  trap 'exit 130' INT TERM HUP QUIT
  for n in share-1 share-2; do
    IFS= read -rsp "W3a $n> " v </dev/tty
    printf '\n'
    printf '%s' "$v" >"$secrets/$n" || exit 1
  done
  unset v
  exec 5<"$f" 6<"${P01_CUSTODY_DIR:?}/root.token" 7<"$secrets/share-1" 8<"$secrets/share-2" || exit 1
  helper protected-semantic-restore.py \
    --contract "${P01_RESTORE_CONTRACT:?}" --contract-sha256 "${P01_RESTORE_CONTRACT_SHA256:?}" \
    --snapshot "$P01_SNAPSHOT_DIRECTORY/raft-pre-upgrade.snap" \
    --snapshot-receipt "$P01_SNAPSHOT_DIRECTORY/raft-pre-upgrade.snap.receipt.json" \
    --security-receipt "${P01_SECURITY_RECEIPT:?}" --quiescence-fd 4 \
    --ca "$CA" --ca-sha256 "$CA_SHA256" --connect-ip "$CONNECT_IP" \
    --home-read-fd 5 --root-fd 6 --share-1-fd 7 --share-2-fd 8
  status=$?
  exec 4<&- 5<&- 6<&- 7<&- 8<&-
  # w4 requires this marker; only RESTORE_ACCEPTED (exit 0) writes it.
  [ "$status" != 0 ] || : >"$P01_INPUTS/w3a-accepted"
  exit "$status"
  ;;
w3b)
  # The W3 snapshot and receipt to the R2 Restic repository, read back and compared.
  (cd "$HOME_ROOT" && /usr/bin/docker compose --profile backup run --rm --no-deps restic-offsite cmd snapshots --no-lock >/dev/null) || exit 1
  out="$(cd "$HOME_ROOT" && /usr/bin/docker compose --profile backup run --rm --no-deps \
    -v "${P01_SNAPSHOT_DIRECTORY:?run w3 first}:/artifact:ro" restic-offsite artifact)"
  status=$?
  printf '%s\n' "$out"
  [ "$status" = 0 ] || exit "$status"
  # The value-free last line is the W3b receipt; w4 requires it.
  printf '%s\n' "$out" | tail -n 1 | jq -e '.state == "W3B_STORED"' >/dev/null || exit 1
  printf '%s\n' "$out" | tail -n 1 >"${P01_INPUTS:?}/w3b-receipt.json"
  ;;
w4)
  # Server upgrade: the Raft mount must keep its identity. Never accept a Compose
  # prompt to recreate a volume; answer no and stop.
  # Gate: W3a accepted and the W3b receipt for this attempt; the recorded Raft identity.
  [ "$#" -eq 1 ] || usage
  [ -e "${P01_INPUTS:?}/w3a-accepted" ] || { echo "W3a not accepted: no w4" >&2; exit 1; }
  [ -s "$P01_INPUTS/w3b-receipt.json" ] || { echo "no W3b receipt: no w4" >&2; exit 1; }
  mount_id() {
    # Name, source and the device/inode the server sees at the mount (the same as the host's).
    local src
    src="$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/openbao/data"}}{{.Name}} {{.Source}}{{end}}{{end}}' openbao)" || return 1
    printf '%s %s\n' "$src" "$(docker exec openbao /bin/stat -c '%d/%i' /openbao/data)"
  }
  before="$(mount_id)" || exit 1
  echo "before: $before"
  [ "${before##* }" = "$1" ] || { echo "Raft mount is not the recorded $1: stop" >&2; exit 1; }
  (cd "$HOME_ROOT" && /usr/bin/docker compose --profile security up -d --no-deps --no-build --pull never openbao) || exit 1
  after="$(mount_id)" || exit 1
  echo "after:  $after"
  [ "$before" = "$after" ] || { echo "Raft mount identity changed: stop" >&2; exit 1; }
  for n in 1 2; do
    echo "unseal share $n (hidden prompt)"
    (cd "$HOME_ROOT" && /usr/bin/docker compose exec openbao bao operator unseal) || exit 1
  done
  (cd "$HOME_ROOT" && /usr/bin/docker compose exec -T openbao bao status)
  ;;
metrics-rotate)
  # RUN-0104 with the W1 root: issue the 1-year Prometheus token, swap the deployed file,
  # recreate Prometheus alone, write the new custody, then revoke a valid old token.
  # Tokens and accessors go over stdin, never argv or output.
  root="${P01_CUSTODY_DIR:?run w1 first}/root.token"
  private "$root" || { echo "no W1 root custody: run w1 first" >&2; exit 1; }
  policy="${P01_CLIENT_DIR:?run the W1 bootstrap first}/infra/03-security/openbao/config/policies/prometheus.hcl"
  [ -s "$policy" ] || { echo "reviewed prometheus.hcl missing from the bootstrap copy" >&2; exit 1; }
  unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
  deployed="${metrics_token_file:-$HOME_ROOT/secrets/security/openbao/openbao_token.txt}"
  custody="${metrics_custody:-$HOME_ROOT/secrets/security/openbao/openbao_metrics_token.custody}"
  [ -f "$deployed" ] && [ -f "$custody" ] || { echo "deployed token or custody missing" >&2; exit 1; }
  [ "$(grep -c '^accessor=' "$custody")" = 1 ] || { echo "custody needs exactly one accessor" >&2; exit 1; }
  new_dir P01_METRICS_DIR p01-metrics
  d="$P01_METRICS_DIR"
  sed -n 's/^accessor=//p' "$custody" >"$d/old.accessor"
  [ -s "$d/old.accessor" ] || { echo "custody accessor is empty" >&2; exit 1; }
  install -m 600 "$deployed" "$d/old.token" || exit 1
  [ -s "$d/old.token" ] || { echo "deployed token file is empty" >&2; exit 1; }
  old_expires="$(sed -n 's/^expires=//p' "$custody")"
  as_root policy write prometheus - <"$policy" >/dev/null || { echo "policy write failed" >&2; exit 1; }
  as_root auth tune -max-lease-ttl=8760h token/ </dev/null >/dev/null || { echo "token/ tune failed" >&2; exit 1; }
  # The custody directory is new, so new.token cannot already exist.
  as_root token create -orphan -no-default-policy -policy=prometheus -ttl=8760h \
    -explicit-max-ttl=8760h -renewable=false -field=token </dev/null >"$d/new.token" || { echo "token create failed" >&2; exit 1; }
  [ -s "$d/new.token" ] || { echo "token create returned nothing" >&2; exit 1; }
  feed "$d/new.token" | as_root write -format=json auth/token/lookup token=- >"$d/new.json" ||
    { echo "new token lookup failed" >&2; revoke_new; exit 1; }
  jq -e '.data.policies == ["prometheus"] and .data.renewable == false and .data.orphan == true
    and .data.explicit_max_ttl == 31536000 and .data.ttl > 0 and (.data.accessor | length) > 0' \
    "$d/new.json" >/dev/null || { echo "new token shape is wrong" >&2; revoke_new; exit 1; }
  jq -r '.data.accessor' "$d/new.json" >"$d/new.accessor"
  bao_as "$d/new.token" read sys/metrics </dev/null >/dev/null 2>&1 || { echo "metrics: DENIED" >&2; revoke_new; exit 1; }
  echo "metrics: allowed"
  ! bao_as "$d/new.token" policy list </dev/null >/dev/null 2>&1 || { echo "policy list: LEAK" >&2; revoke_new; exit 1; }
  echo "policy list: denied"
  # The old token: the deployed file is the truth, and custody must describe it.
  if feed "$d/old.token" | as_root write -format=json auth/token/lookup token=- >"$d/old.json"; then
    [ "$(jq -r '.data.accessor' "$d/old.json")" = "$(cat "$d/old.accessor")" ] &&
      jq -e '.data.policies == ["prometheus"]' "$d/old.json" >/dev/null ||
      { echo "custody is stale: it does not describe the deployed token" >&2; revoke_new; exit 1; }
    old=valid
  elif errs 'bad token'; then
    if feed "$d/old.accessor" | as_root write -format=json auth/token/lookup-accessor accessor=- >/dev/null; then
      echo "custody is stale: its accessor is valid but the deployed token is not" >&2; revoke_new; exit 1
    fi
    errs 'invalid accessor' && controls || { echo "old token: INDETERMINATE" >&2; revoke_new; exit 1; }
    old=expired
  else
    echo "old token: INDETERMINATE" >&2; revoke_new; exit 1
  fi
  echo "old token: $old"
  group="$(stat -c %g "$deployed")"
  tmp="${deployed%/*}/.openbao_token.new"
  swap() { { install -m 640 -g "$group" "$1" "$tmp" && mv "$tmp" "$deployed"; } || { rm -f "$tmp"; return 1; }; }
  # Up only on a sample scraped after the recreate: timestamp() is the sample's own time,
  # so an up=1 replayed from before the restart does not count.
  prom_up() {
    local start
    start="$(date +%s)"
    (cd "$HOME_ROOT" && /usr/bin/docker compose --profile obs up -d --no-deps --force-recreate --wait prometheus) >/dev/null 2>&1 || return 1
    for _ in $(seq "${metrics_wait:-12}"); do
      sleep "${metrics_interval:-10}"
      docker exec prometheus wget -qO- 'http://localhost:9090/api/v1/query?query=timestamp%28up%7Bjob%3D%22openbao%22%7D%3D%3D1%29' 2>/dev/null |
        jq -e --argjson s "$start" '.data.result[0].value[1] | tonumber > $s' >/dev/null && return 0
    done
    return 1
  }
  swap "$d/new.token" || { echo "file swap failed" >&2; revoke_new; exit 1; }
  if ! prom_up; then
    if [ "$old" = expired ]; then
      # Restoring an expired token gains nothing: keep the verified new token and record it.
      write_custody || exit 1
      echo "openbao target not up; the new token stays deployed and in custody: check Prometheus (RUN-0104)" >&2
      exit 1
    fi
    echo "openbao target not up: restoring the old file and Prometheus" >&2
    if ! swap "$d/old.token"; then
      # The new token stays deployed: record it, and keep the still-valid old one for metrics-revoke.
      write_custody
      : >"$d/old.unrevoked"
      echo "RESTORE FAILED: the new token stays deployed and in custody; the old token is still valid" >&2
      exit 1
    fi
    if prom_up; then echo "restored" >&2; else echo "restored file; Prometheus not up" >&2; fi
    revoke_new
    exit 1
  fi
  echo "target: openbao up"
  write_custody || exit 1
  echo "new: expires $(jq -r '.data.expire_time' "$d/new.json")"
  if [ "$old" = valid ]; then
    revoke_old || exit 1
  else
    echo "old: expired ($old_expires)"
  fi
  find "$d" -type f -exec shred -u {} + && rmdir "$d"
  ;;
metrics-revoke)
  # Retry what metrics-rotate could not confirm, with the W1 root, before W7 revoke-root.
  root="${P01_CUSTODY_DIR:?run w1 first}/root.token"
  private "$root" || { echo "no W1 root custody" >&2; exit 1; }
  d="${P01_METRICS_DIR:?no metrics-rotate directory}"
  [ -d "$d" ] || { echo "nothing to resolve: metrics-rotate finished or cleanup ran"; exit 0; }
  custody="${metrics_custody:-$HOME_ROOT/secrets/security/openbao/openbao_metrics_token.custody}"
  unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
  rc=0
  [ ! -e "$d/custody.unwritten" ] || write_custody || rc=1
  [ ! -e "$d/new.unrevoked" ] || revoke_new || rc=1
  [ ! -e "$d/old.unrevoked" ] || revoke_old || rc=1
  [ "$rc" = 0 ] && find "$d" -type f -exec shred -u {} + && rmdir "$d" && echo "metrics custody resolved"
  exit "$rc"
  ;;
renderer-expiry)
  # Value-free: when the server revoked renderer AppRole login leases since $1. Timestamps only.
  [ "$#" -eq 1 ] || usage
  unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
  stamp='^[0-9]{4}-[0-9-]+T[0-9:.]+Z'
  logs="$(docker logs openbao --since "$1" 2>&1)" || { echo "docker logs failed" >&2; exit 1; }
  times="$(grep 'revoked lease: lease_id=auth/approle/login/' <<<"$logs" | grep -oE "$stamp")"
  [ -z "$times" ] || printf '%s\n' "$times"
  echo "revocations: $(grep -c . <<<"$times")"
  # An empty result proves nothing when the retained log starts after $1.
  echo "log starts: $(head -n 1 <<<"$logs" | grep -oE "$stamp" || echo unknown)"
  echo "server active since: $(docker exec openbao bao status -format=json 2>/dev/null | jq -r '.active_time // "unknown"')"
  ;;
host-hold)
  # Keep apt and needrestart from restarting containerd or Docker outside a window (RUN-0085).
  sudo apt-mark hold containerd.io docker-ce docker-ce-cli </dev/null >/dev/null || exit 1
  if dpkg-query -W -f='${Status}' needrestart 2>/dev/null | grep -q 'ok installed'; then
    printf '%s\n' '$nrconf{override_rc}{qr(^containerd)} = 0;' '$nrconf{override_rc}{qr(^docker)} = 0;' |
      sudo tee /etc/needrestart/conf.d/hy-home.conf >/dev/null || exit 1
    echo "needrestart: containerd and docker excluded"
  fi
  apt-mark showhold | grep -E '^(containerd\.io|docker-ce|docker-ce-cli)$'
  ;;
preflight)
  # RUN-0105 W0: read-only checks before the bootstrap. It handles no secret, so the checkout
  # copy may run it. It ends by clearing this window's path-variable record.
  cd "$HOME_ROOT" || exit 1
  HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
  docker compose exec -T openbao bao status
  docker compose --profile security config --images | grep '^hy-home/openbao' | sort -u |
    xargs docker image inspect --format '{{.Id}}'   # fails when the image is missing
  df -h /home
  systemctl show hyhome-backup.service -p Result,ExecMainExitTimestamp
  echo "dockerd debug: $(docker info -f '{{.Debug}}')"   # must be false: true logs the exec environment
  command -v jq                                          # root-sweep needs it
  loginctl show-user "$USER" -p Linger                   # not yes: keep another login session open
  docker compose --profile backup run --rm --no-deps restic-offsite cmd snapshots --no-lock --compact | tail -4
  docker compose --profile backup run --rm --no-deps restic-offsite cmd stats --no-lock --mode debug 2>&1 |
    grep -A2 '^File Type: data'
  : >"$vars"
  echo "window path variables cleared"
  ;;
status)
  # Read-only, value-free health summary. It prints states and dates only, never a
  # token, accessor or secret value, and handles no secret, so the checkout copy may
  # run it. Every problem prints a WARN line; exit 1 when there is any.
  # Inputs: issuance_journal (the Task's journal directory); metrics_custody overrides
  # the custody file for tests.
  unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
  problems=0
  warn() { echo "WARN: $*"; problems=$((problems + 1)); }
  seen=0
  while read -r line; do
    seen=$((seen + 1))
    echo "$line"
    case "$line" in *"(healthy)"*) ;; *) warn "not healthy: $line" ;; esac
  done < <(docker ps -a --filter name='^openbao$' --filter name='^openbao-agent$' --format '{{.Names}}: {{.Status}}')
  [ "$seen" = 2 ] || warn "expected openbao and openbao-agent, found $seen"
  seal="$(docker exec openbao bao status -format=json 2>/dev/null)"
  if sealed="$(printf '%s' "$seal" | jq -r '.sealed' 2>/dev/null)" && [ -n "$sealed" ] && [ "$sealed" != null ]; then
    echo "server: sealed=$sealed $(printf '%s' "$seal" | jq -r '"ha=\(if .sealed then "-" elif .is_self then "active" elif .ha_enabled then "standby" else "-" end) version=\(.version)"')"
    [ "$sealed" = false ] || warn "server sealed: unseal (RUN-0085), then agent-restart"
  else
    warn "server unreachable"
  fi
  if [ -z "${issuance_journal:-}" ]; then
    warn "issuance_journal not set: give the Task's journal directory"
  elif [ -r "$issuance_journal/issuance.anchor" ]; then
    jq -r '"journal: \(.state) schema=\(.schema_version // 1)"' "$issuance_journal/issuance.anchor"
    [ ! -e "$issuance_journal/issuance.json" ] || warn "active issuance journal: reconcile before a new W5"
    for pending in "$issuance_journal"/*.pending; do
      [ ! -e "$pending" ] || warn "interrupted journal write: ${pending##*/}"
    done
  else
    warn "no journal anchor in $issuance_journal"
  fi
  custody="${metrics_custody:-$HOME_ROOT/secrets/security/openbao/openbao_metrics_token.custody}"
  expires="$(sed -n 's/^expires=//p' "$custody" 2>/dev/null)"
  if [ "$(printf '%s\n' "$expires" | grep -c .)" = 1 ] && end="$(date -d "$expires" +%s 2>/dev/null)"; then
    days=$(( (end - $(date +%s)) / 86400 ))
    echo "metrics token: expires $expires ($days days)"
    [ "$days" -ge 30 ] || warn "metrics token expires in $days days: rotate (RUN-0104)"
  else
    warn "metrics token expiry unknown"
  fi
  prom() { docker exec prometheus wget -qO- "http://127.0.0.1:9090/api/v1/$1" 2>/dev/null; }
  if ! alerts="$(prom alerts | jq -r '.data.alerts[] | select(.labels.alertname | startswith("OpenBao")) | "\(.labels.alertname) \(.state) since \(.activeAt)"' 2>/dev/null)"; then
    warn "Prometheus alerts unreadable"
  fi
  while read -r line; do
    [ -n "$line" ] || continue
    case "$line" in *" firing "*) warn "alert: $line" ;; *) echo "alert: $line" ;; esac
  done <<<"$alerts"
  targets="$(prom 'targets?state=active' | jq -r '.data.activeTargets[] | select(.labels.job | startswith("openbao")) | "\(.labels.job) \(.health) \(.lastError)"' 2>/dev/null)"
  [ -n "$targets" ] || warn "Prometheus targets unreadable"
  while read -r job health rest; do
    [ -n "$job" ] || continue
    case "$job $health" in "openbao up"|"openbao-agent up") echo "target: $job up" ;; *) warn "target: $job $health $rest" ;; esac
  done <<<"$targets"
  # Exit 0 is done, and 137/143 is a deliberate docker stop; anything else stopped the hard way.
  while read -r line; do
    [ -n "$line" ] || continue
    case "$line" in *" Exited (0) "*|*" Exited (137) "*|*" Exited (143) "*) ;; *) warn "stopped: $line" ;; esac
  done < <(docker ps -a --filter label=com.docker.compose.project=hy-home-infra --filter status=exited --format '{{.Names}} {{.Status}}')
  echo "problems: $problems"
  [ "$problems" = 0 ]
  ;;
w5-create)
  # Agent container only; the issuer helper requires it stopped. Then agent-restart.
  (cd "$HOME_ROOT" && /usr/bin/docker compose --profile security up --no-start --no-deps --no-build --pull never openbao-agent)
  ;;
agent-restart)
  # Renderer SecretID delivery step 3: stop the Agent, mint the two 5-minute tokens
  # with the operator credential, and hand them to the installed issuer helper,
  # which delivers the SecretID and starts the Agent. Inputs are the Task's values.
  : "${issuer_commit:?}" "${operator_tools:?}" "${agent_volume:?}" "${issuance_journal:?}"
  issuer="$operator_tools/$issuer_commit/issue-renderer-secret-id.sh"
  [ -f "$issuer" ] || { echo "install the issuer helper first (RUN-0103 SecretID step 2)" >&2; exit 1; }
  # The helper requires the exact owned image; the OpenBao Compose file owns the pin.
  image="$(sed -n 's/^    image: //p' "$HOME_ROOT/infra/03-security/openbao/docker-compose.yml" | sort -u)"
  [ "$(printf '%s\n' "$image" | wc -l)" = 1 ] || { echo "expected one pinned OpenBao image" >&2; exit 1; }
  case "$image" in hy-home/openbao:*@sha256:*) ;; *) echo "expected one pinned OpenBao image" >&2; exit 1 ;; esac
  unset DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
  read -rsp 'Enter current OIDC operator credential> ' BAO_TOKEN </dev/tty
  printf '\n'
  export BAO_TOKEN
  # Check the credential before the stop: a revoked or mistyped one would leave the Agent down.
  policies="$( (cd "$HOME_ROOT" && /usr/bin/docker compose exec -T -e BAO_TOKEN openbao bao token lookup -format=json) </dev/null 2>/dev/null |
    jq -r '.data.policies // [] | join(",")')"
  case ",$policies," in *,hy-home-operator,*) ;; *) echo "operator credential rejected; Agent not stopped" >&2; exit 1 ;; esac
  /usr/bin/docker stop openbao-agent >/dev/null || exit 1
  trap '[ "${status:-1}" = 0 ] || echo "Agent may be stopped: fix the cause and rerun agent-restart" >&2' EXIT
  mint() {
    # JSON booleans: the operator policy's allowed_parameters reject "false"/"true" strings.
    printf '{"policies":"%s","ttl":"5m","explicit_max_ttl":"5m","renewable":false,"no_default_policy":true}' "$1" |
      (cd "$HOME_ROOT" && /usr/bin/docker compose exec -T -e BAO_TOKEN openbao bao write -field=token "auth/token/create/$1" -)
  }
  issuer_token="$(mint renderer-issuer)" || exit 1
  cleanup_token="$(mint renderer-cleanup)" || exit 1
  unset BAO_TOKEN
  printf '%s\n%s\n' "$issuer_token" "$cleanup_token" |
    /bin/sh "$issuer" openbao "$agent_volume" "$image" openbao-agent "$issuance_journal" "$issuer_commit"
  status=$?
  unset issuer_token cleanup_token
  echo "issue rc=$status"
  [ "$status" = 0 ] || exit "$status"
  # The helper ran health-agent.sh itself; Docker's status reads "starting" until its
  # first interval, so wait for a settled status.
  for _ in $(seq 1 18); do
    health="$(docker inspect -f '{{.State.Health.Status}}' openbao-agent)"
    [ "$health" = starting ] || break
    sleep 5
  done
  echo "agent: $health"
  # Names and modes only: every rendered .txt should be 0640 and every .version 0600.
  docker exec openbao-agent sh -c 'ls -l /openbao/out/*/*' | awk '{print $1, $NF}'
  ;;
*) usage ;;
esac
