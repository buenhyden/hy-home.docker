#!/usr/bin/env bash
# RUN-0085 maintenance window steps after the W1 source bootstrap. The bootstrap
# copies this file with the protected helpers into $P01_SCRIPT_DIR and checks its
# hash; run that copy, never the checkout's. Each step reads the window state from
# $XDG_RUNTIME_DIR/p01-window.vars, so a failed step exits this script, not the
# owner's shell. No token, share, accessor or policy hash is printed.
set +x
set -uo pipefail
umask 077

usage() {
  echo "usage: $0 token <stage>|check-token <stage>|w1|root-sweep|roles-plan|roles-diff|roles-apply|revoke-root|evidence <dir>|cleanup [--keep-root] [--keep-w2] [--discard-root]|agent-restart" >&2
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
bao_as() { (cd "$HOME_ROOT" && BAO_TOKEN="$(cat "$1")" /usr/bin/docker compose exec -T -e BAO_TOKEN openbao bao "${@:2}"); }
# A fresh custody directory per attempt, recorded for later steps and cleanup.
new_dir() {
  local dir
  dir="$(/usr/bin/mktemp -d "${P01_RUNTIME_DIR:?run the W1 bootstrap first}/$2.XXXXXX")" || exit 1
  printf -v "$1" '%s' "$dir"
  declare -p "$1" >>"$vars"
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
  trap 'exit 130' INT TERM
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
  # After W1 and before W1c, every window. The only place a new root reaches the CLI.
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
  for d in p01-custody.* p01-roles-plan.* p01-roles.* p01-revoke.* p01-token.*; do
    for f in state.json prior-state.json operation-intent.json; do
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
  P01_KEEP_ROOT=0 P01_KEEP_W2=0 discard=0
  for a in "$@"; do
    case "$a" in --keep-root) P01_KEEP_ROOT=1 ;; --keep-w2) P01_KEEP_W2=1 ;; --discard-root) discard=1 ;; *) usage ;; esac
  done
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
    "$XDG_RUNTIME_DIR"/p01-w1.* "$XDG_RUNTIME_DIR"/p01-w3a.*; do
    [ -d "$d" ] || continue
    case "$d" in */p01-token.*) [ "${P01_KEEP_W2:-0}" = 1 ] && continue ;; esac
    case "$d" in */p01-custody.*) [ "${P01_KEEP_ROOT:-0}" = 1 ] && continue ;; esac
    find "$d" -type f -exec shred -u {} + && find "$d" -depth -type d -empty -delete
  done
  [ "${P01_KEEP_ROOT:-0}" = 1 ] ||
    for f in "$XDG_RUNTIME_DIR"/p01-op-*.token; do [ -f "$f" ] && shred -u "$f"; done
  [ "${P01_KEEP_ROOT:-0}" = 1 ] || rm -f "$vars"
  # What is left: the p01-client.* helper copies (no secret) and, if any, p01-inputs.*.
  find "$XDG_RUNTIME_DIR" -maxdepth 1 -name 'p01-*' -printf '%f\n'
  ;;
agent-restart)
  # Renderer SecretID delivery step 3: stop the Agent, mint the two 5-minute tokens
  # with the operator credential, and hand them to the installed issuer helper,
  # which delivers the SecretID and starts the Agent. Inputs are the Task's values.
  : "${issuer_commit:?}" "${operator_tools:?}" "${agent_volume:?}" "${issuance_journal:?}"
  issuer="$operator_tools/$issuer_commit/issue-renderer-secret-id.sh"
  [ -f "$issuer" ] || { echo "install the issuer helper first (RUN-0085 SecretID step 2)" >&2; exit 1; }
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
