#!/usr/bin/env bash
# RUN-0105 window driver: steps 1-13 of the OpenBao 2.7.3 window in order, through the
# bootstrap's hash-checked owner-window.sh copy. Run it from the approved commit:
#   p01_run <approved commit> infra/03-security/openbao/scripts/window-run.sh <approved commit> [start step]
# It reads no secret value. Shares and operator tokens go only to the hidden /dev/tty
# prompts of owner-window.sh, and sudo asks for its own password. Every step must exit 0;
# the first failure stops the driver and prints the RUN-0105 abort rules. Nothing is
# retried. Start steps: prep w0 boot w1 sweep w1c silence w3 w3b w3a w4 w5 w6 w7 alerts finish.
set +x
set -uo pipefail
umask 077

# Owner inputs. operator_tools, issuance_journal and agent_volume default to the TSK-0006
# 2026-11-24 W0 record; the two paths below are new per window. Export a variable before
# p01_run only to change it, and record the W3 path in TSK-0006 afterwards.
operator_tools=${operator_tools:-/home/hyunyoun/.local/share/hy-home-openbao-tools}
issuance_journal=${issuance_journal:-/home/hyunyoun/.local/share/hy-home-openbao-journal}
agent_volume=${agent_volume:-hy-home-infra_openbao-agent-data}
P01_W3_DIR=${P01_W3_DIR:-/home/hyunyoun/storage/ops-snapshots/openbao-p01-$(date +%Y%m%d)}
P01_EVIDENCE_DIR=${P01_EVIDENCE_DIR:-$HOME/p01-evidence/$(date +%Y%m%d)-openbao-2.7.3}
P01_RETIRE_TOKEN=${P01_RETIRE_TOKEN:-}   # optional: a leftover p01-operator.token to retire in W0

# Facts this window was reviewed against (RUN-0105, TSK-0006).
HOME_ROOT=/home/hyunyoun/data/hy-home.docker
OLD_IMAGE=sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8
OLD_VERSION=2.7.1+hyhome.go1.27.3.net0.60.0.r1
NEW_VERSION=2.7.3+hyhome.go1.27.4.net0.62.0.r1
RAFT_ID=2064/115612005
SILENCE='alertname=~"OpenBao(Sealed|MetricsScrapeFailing|AgentMetricsScrapeFailing|AgentAuthFailure)"'
STEPS=(prep w0 boot w1 sweep w1c silence w3 w3b w3a w4 w5 w6 w7 alerts finish)
SEC01_LOOKUP_UNTIL=2026-12-01   # the 7-day latest-stable lookup of 2026-11-24 (TSK-0006)
CURRENT=start

usage() { echo "usage: $0 <40-hex approved commit> [${STEPS[*]}]" >&2; exit 2; }
[ "$#" -ge 1 ] || usage
[ "$#" -le 2 ] || usage
C=$1
START=${2:-prep}
case "$C" in *[!0-9a-f]*) usage ;; esac
[ "${#C}" = 40 ] || usage
start_index=-1
for i in "${!STEPS[@]}"; do [ "${STEPS[i]}" = "$START" ] && start_index=$i; done
[ "$start_index" -ge 0 ] || usage
: "${XDG_RUNTIME_DIR:?}"
STATE="$XDG_RUNTIME_DIR/p01-window-run.state"   # T0, silence ID and audit size; no secret
unset COMPOSE_FILE DOCKER_HOST DOCKER_CONTEXT DOCKER_CONFIG
cd "$HOME_ROOT" || exit 1

# The RUN-0085 Reviewed Script Runner, verbatim; a test keeps the two equal.
p01_git() {
  /usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 \
    /usr/bin/git --git-dir=/home/hyunyoun/data/hy-home.docker/.git "$@"
}
p01_run() {  # p01_run <40자리 commit> <저장소 경로> <인자…>
  local h=/home/hyunyoun/data/hy-home.docker c b f r
  unset LD_PRELOAD LD_LIBRARY_PATH PYTHONHOME PYTHONPATH BASH_ENV ENV
  case "$1" in *[!0-9a-f]*) return 1 ;; esac; [ "${#1}" = 40 ] || return 1
  [ "$h" = "$(/usr/bin/realpath -e -- "$h")" ] && [ ! -L "$h/.git" ] &&
    [ "$(/usr/bin/stat -c '%d:%i:%u' -- "$h" "$h/.git" | /usr/bin/paste -sd ' ')" = '64512:4338469:1000 64512:4338470:1000' ] &&
    [ "$(/usr/bin/stat -c '%u:%a' -- "${XDG_RUNTIME_DIR:?}")" = "$(/usr/bin/id -u):700" ] &&
    [ "$(/usr/bin/findmnt -n -T "$XDG_RUNTIME_DIR" -o FSTYPE)" = tmpfs ] || return 1
  c="$(p01_git rev-parse --verify "$1^{commit}")" && [ "$c" = "$1" ] || return 1
  b="$(p01_git rev-parse --verify "$1:$2")" || return 1
  f="$(umask 077; /usr/bin/mktemp "$XDG_RUNTIME_DIR/p01-run.XXXXXX")" || return 1
  # Re-hash the copy: a changed blob behind the same tree entry does not run.
  p01_git show --no-textconv "$1:$2" >"$f" && [ -s "$f" ] &&
    [ "$(p01_git hash-object --no-filters -- "$f")" = "$b" ] &&
    /usr/bin/bash "$f" "${@:3}"; r=$?
  /usr/bin/rm -f -- "$f"; return "$r"
}

say() { printf '\n=== %s: %s ===\n' "$CURRENT" "$*"; }
note() { printf '%s=%q\n' "$1" "$2" >>"$STATE"; }
ask() {
  local answer
  read -rp "$1 [yes/no] " answer </dev/tty
  [ "$answer" = yes ]
}
abort_help() {
  cat >&2 <<HELP

STOPPED at $CURRENT. Do not rerun a step that ended in exit 2 (INDETERMINATE).
RUN-0105 "Abort and Cleanup Rules" decide what follows:
  - backup timer:  sudo systemctl start hyhome-backup.timer
  - silence:       record ALERTS, then docker exec alertmanager amtool --alertmanager.url=http://127.0.0.1:9093 silence expire ${SILENCE_ID:-<id>}
  - in your shell: . "\$XDG_RUNTIME_DIR/p01-window.vars"   (sets P01_SCRIPT_DIR and the window paths)
  - root, if W1 ran: follow the runbook (unsealed: token w7, check-token w7, revoke-root after the
                   p01-op-proof OIDC check; W1 exit 2 or sealed: attempt cancel and cleanup --discard-root)
  - then:          bash "\$P01_SCRIPT_DIR/owner-window.sh" evidence "$P01_EVIDENCE_DIR"; ... cleanup (runbook options)
  - Agent stopped in W3 stays stopped until the next window's W5.
After fixing a cause that left no effect, resume with: p01_run $C infra/03-security/openbao/scripts/window-run.sh $C <step>
HELP
}
die() {
  printf '\nSTOP: %s\n' "$*" >&2
  abort_help
  exit 1
}
run() { "$@" || die "exit $? from: $*"; }
ow() {
  [ -n "${P01_SCRIPT_DIR:-}" ] || die "P01_SCRIPT_DIR unset: run the boot step first"
  bash "$P01_SCRIPT_DIR/owner-window.sh" "$@"
}
minutes() { echo $(( ($(date +%s) - T0) / 60 )); }
before() { [ "$(minutes)" -lt "$1" ] || die "T+$1 passed before $2 started"; }
server() { docker exec openbao bao status -format=json 2>/dev/null | jq -r "$1"; }
prom() { docker exec prometheus wget -qO- "http://127.0.0.1:9090/api/v1/query?query=$1"; }
agent_healthy() {
  local h
  for _ in $(seq 1 24); do
    h="$(docker inspect -f '{{.State.Health.Status}}' openbao-agent 2>/dev/null)"
    [ "$h" = healthy ] && return 0
    sleep 5
  done
  return 1
}
targets_up() {
  # up{job=~"openbao.*"}; both jobs must read 1 within two minutes.
  for _ in $(seq 1 24); do
    [ "$(prom 'up%7Bjob%3D~%22openbao.%2A%22%7D' | jq '[.data.result[] | select(.value[1] == "1")] | length')" = 2 ] && return 0
    sleep 5
  done
  return 1
}
audit_size() { docker exec openbao stat -c %s /openbao/audit/audit.json; }

step_prep() {
  say "1. checkout, backup timer, issuer helper"
  [ -z "$(p01_git --work-tree="$HOME_ROOT" status --porcelain)" ] || die "checkout is not clean"
  [ "$(p01_git rev-parse HEAD)" = "$C" ] || die "checkout HEAD is not $C"
  [ ! -e docker-compose.override.yml ] || die "docker-compose.override.yml present"
  [ "$(date +%F)" \< "$SEC01_LOOKUP_UNTIL" ] || [ "$(date +%F)" = "$SEC01_LOOKUP_UNTIL" ] ||
    die "the SEC01 latest-stable lookup is older than 7 days: repeat it (RUN-0105 SEC01 Image Gate)"
  # A oneshot backup reads "activating" while it runs; only "inactive" is idle.
  [ "$(systemctl is-active hyhome-backup.service)" = inactive ] || die "a backup run is not inactive; wait for it"
  run sudo systemctl stop hyhome-backup.timer
  [ "$(systemctl is-active hyhome-backup.timer)" = inactive ] || die "backup timer still active"
  if [ ! -f "$operator_tools/$C/issue-renderer-secret-id.sh" ]; then
    run p01_run "$C" infra/03-security/openbao/scripts/install-renderer-issuer.sh "$HOME_ROOT" "$C" "$operator_tools/$C"
  fi
  [ -z "$P01_RETIRE_TOKEN" ] || run p01_run "$C" infra/03-security/openbao/scripts/owner-window.sh retire-token "$P01_RETIRE_TOKEN"
}

step_w0() {
  say "2. W0 preflight"
  local tls image
  tls="$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/openbao/tls/ca.pem"}}{{.Source}}{{end}}{{end}}' openbao)"
  image="$(sed -n 's/^    image: //p' infra/03-security/openbao/docker-compose.yml | sort -u)"
  [ "$(printf '%s\n' "$image" | wc -l)" = 1 ] || die "expected one pinned OpenBao image"
  run sh infra/03-security/openbao/scripts/check-tls-material.sh "${tls%/ca.pem}" "$image"
  run bash infra/03-security/openbao/scripts/owner-window.sh preflight
  ask "preflight: R2 stored bytes plus 1.05x the snapshot stay under 9,000,000,000?" || die "R2 headroom not confirmed"
  [ "$(docker inspect -f '{{.Image}}' openbao)" = "$OLD_IMAGE" ] || die "openbao does not run the reviewed 2.7.1 image"
  [ "$(server .sealed)" = false ] || die "server is sealed"
  [ "$(server .version)" = "$OLD_VERSION" ] || die "server is not $OLD_VERSION"
  [ "$(docker exec openbao /bin/stat -c '%d/%i' /openbao/data)" = "$RAFT_ID" ] || die "Raft mount is not $RAFT_ID"
  agent_healthy || die "openbao-agent is not healthy"
  ! findmnt -n -o OPTIONS /dev/shm | grep -qw noexec || die "/dev/shm is noexec"
  [ "$(docker inspect -f '{{.Image}}' traefik)" = "$(docker image inspect -f '{{.Id}}' "$(docker compose --profile core config --images traefik)")" ] ||
    die "traefik does not run its Compose pin"
  docker exec traefik test -f /openbao-ca/ca.pem || die "traefik lacks /openbao-ca/ca.pem"
  docker inspect -f '{{range .Mounts}}{{.Destination}} {{end}}' prometheus | grep -q /etc/prometheus/openbao-ca.pem ||
    die "prometheus lacks the OpenBao CA mount"
  # W0 needs a passing last backup; W2 is skipped only while its snapshot token still works.
  [ "$(systemctl show hyhome-backup.service -p Result --value)" = success ] || die "the last HOME backup failed (RUN-0105 W0)"
  ! journalctl -u hyhome-backup.service --since '-1 day' --no-pager 2>/dev/null | grep -qi 'snapshot token' ||
    die "the last backup reported a snapshot token problem: W2 is needed, which this driver does not run"
  T0=$(date +%s)
  note T0 "$T0"
  echo "T0 $(date -d "@$T0" '+%F %T %Z'): T+15 W1 done, T+45 W3b, T+55 W3a, T+80 W4"
}

step_boot() {
  say "3a. W1 source bootstrap"
  run p01_run "$C" infra/03-security/openbao/scripts/p01-bootstrap.sh "$C"
}

step_w1() {
  say "3b. W1 root ceremony"
  echo "OpenBao UI: sign in with OIDC, Copy token, and stay signed in."
  run ow token w1
  local checked
  checked="$(ow check-token w1)" || die "check-token w1 failed"
  printf '%s\n' "$checked"
  grep -q '"started":false' <<<"$checked" || die "a generate-root attempt is already open"
  run ow w1
}

step_sweep() {
  say "3c. previous root sweep and audit/mount list"
  run ow root-sweep
  run ow audit-list
  ask "the audit, secrets and auth lists above hold nothing the isolated restore cannot open?" ||
    die "W3a gate: review the HOME audit and mount list"
  before 15 "W1c"
}

step_w1c() {
  say "4. W1c renderer policy and token roles"
  run ow roles-plan
  run ow roles-diff
  ask "accept every difference shown above (record it in TSK-0006)?" || die "W1c differences not accepted"
  run ow roles-apply
  agent_healthy || die "openbao-agent unhealthy after W1c"
}

step_silence() {
  say "5. W2 skipped; Alertmanager silence for the expected OpenBao alerts"
  SILENCE_ID="$(docker exec alertmanager amtool --alertmanager.url=http://127.0.0.1:9093 silence add "$SILENCE" \
    --duration="$((120 - $(minutes)))m" --comment="RUN-0105 window" --author=buenhyden)" || die "silence not created"
  note SILENCE_ID "$SILENCE_ID"
  echo "silence $SILENCE_ID"
}

step_w3() {
  say "6. W3 writers stopped and pre-upgrade snapshot into $P01_W3_DIR"
  echo "W3a HOME read token: sign in again now; no new login from here until W3a ends."
  run ow token w3a
  run docker stop openbao-agent
  run ow lease-start
  run ow w3 "$P01_W3_DIR" "$OLD_VERSION" --writers-checked
  run ow lease-bind
}

step_w3b() {
  say "7. W3b R2 artifact custody"
  before 45 "W3b"
  run ow w3b
}

step_w3a() {
  say "8. W3a isolated semantic restore"
  before 55 "W3a"
  run env issuer_commit="$C" operator_tools="$operator_tools" bash "$P01_SCRIPT_DIR/owner-window.sh" w3a-inputs
  run ow w3a
}

step_w4() {
  say "9. W4 server upgrade and manual unseal"
  before 80 "W4"
  run ow w4 "$RAFT_ID"
  [ "$(server .sealed)" = false ] || die "server is sealed after W4"
  [ "$(server .version)" = "$NEW_VERSION" ] || die "server is not $NEW_VERSION after W4"
}

step_w5() {
  say "10. W5 Agent upgrade and SecretID reissue"
  run ow w5-create
  echo "agent-restart asks for a fresh OIDC operator credential."
  run env issuer_commit="$C" operator_tools="$operator_tools" agent_volume="$agent_volume" \
    issuance_journal="$issuance_journal" bash "$P01_SCRIPT_DIR/owner-window.sh" agent-restart
  agent_healthy || die "openbao-agent unhealthy after W5"
  if [ "$(docker inspect -f '{{.Image}}' gatus)" = "$(docker image inspect -f '{{.Id}}' hy/gatus:local)" ]; then
    run docker compose --profile obs up -d --no-deps --no-build --pull never --force-recreate gatus
  else
    note GATUS_BLOCKED 1
    echo "gatus: running image differs from hy/gatus:local; left as is (RUN-0105: BLOCKED)"
  fi
  targets_up || die "up{job=~\"openbao.*\"} is not 1 for both jobs"
}

step_w6() {
  say "11. W6 audit device"
  [ "$(docker exec openbao stat -c '%a %u %g' /openbao/audit/audit.json)" = "600 100 1000" ] || die "audit.json is not 0600 100:1000"
  docker exec openbao stat -c 'audit.json device/inode %d/%i' /openbao/audit/audit.json
  AUDIT_SIZE="$(audit_size)" || die "audit.json unreadable"
  note AUDIT_SIZE "$AUDIT_SIZE"
  echo "audit.json size $AUDIT_SIZE"
}

step_w7() {
  say "12. W7 post check and root revocation"
  local firing
  agent_healthy || die "openbao-agent unhealthy (its health check covers every rendered template)"
  targets_up || die "openbao targets are not up"
  firing="$(prom 'ALERTS%7Balertname%3D~%22OpenBao.%2A%22%2Calertstate%3D%22firing%22%7D')" || die "Prometheus alert query failed"
  jq -r '.data.result[].metric.alertname' <<<"$firing" || die "Prometheus alert answer unreadable"
  ask "no unexpected OpenBao alert is firing (list above)?" || die "alerts need review before root revocation"
  echo "Sign in with OIDC once more for the W7 credential."
  run ow token w7
  run ow check-token w7
  [ -n "${AUDIT_SIZE:-}" ] || die "no W6 audit size: run w6 first"
  [ "$(audit_size)" -gt "$AUDIT_SIZE" ] || die "audit.json did not grow after an audited request"
  run ow revoke-root
}

step_alerts() {
  say "13a. record window alerts, then expire the silence"
  local seen
  mkdir -p "$P01_EVIDENCE_DIR" || die "no evidence directory"
  seen="$(prom "max_over_time(ALERTS%7Balertname%3D~%22OpenBao.%2A%22%7D%5B$(( $(minutes) + 5 ))m%5D)")" ||
    die "Prometheus alert query failed; the silence stays until the alerts are recorded"
  jq -r '.data.result[].metric | "\(.alertname) \(.alertstate)"' <<<"$seen" | sort -u >"$P01_EVIDENCE_DIR/window-alerts.txt" ||
    die "alert answer unreadable"
  cat "$P01_EVIDENCE_DIR/window-alerts.txt"
  [ -n "${SILENCE_ID:-}" ] || die "no silence ID recorded"
  run docker exec alertmanager amtool --alertmanager.url=http://127.0.0.1:9093 silence expire "$SILENCE_ID"
}

step_finish() {
  say "13b. evidence, cleanup, backup timer"
  [ -n "${P01_INPUTS:-}" ] || die "P01_INPUTS unset in the window path record"
  mkdir -p "$P01_EVIDENCE_DIR" || die "no evidence directory"
  run ow evidence "$P01_EVIDENCE_DIR"
  run cp -a "$P01_INPUTS" "$P01_EVIDENCE_DIR/inputs"
  run ow cleanup
  run sudo systemctl start hyhome-backup.timer
  [ -z "${GATUS_BLOCKED:-}" ] || echo "Gatus recreation: BLOCKED (record it in TSK-0006)"
  rm -f "$STATE"
  echo "Window finished. Record the status lines, P01_SNAPSHOT_DIRECTORY=$P01_W3_DIR and $P01_EVIDENCE_DIR in TSK-0006."
}

if [ "$start_index" -gt 0 ]; then
  [ -f "$STATE" ] || die "no $STATE: start from prep"
else
  : >"$STATE"
fi
for step in "${STEPS[@]:start_index}"; do
  CURRENT=$step
  # Reload at top level before every step: declare -p lines sourced inside a function would
  # be local, and each owner-window.sh call can add paths to these files.
  # shellcheck disable=SC1090
  . "$STATE"
  # shellcheck disable=SC1091
  [ ! -f "$XDG_RUNTIME_DIR/p01-window.vars" ] || . "$XDG_RUNTIME_DIR/p01-window.vars"
  "step_$step"
done
