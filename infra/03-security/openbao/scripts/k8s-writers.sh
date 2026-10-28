#!/usr/bin/env bash
# RUN-0105 hy-home.k8s writer quiescence (W3) and the ESO Finish gate, for the
# external cluster operator with a per-window approval. Stops the two Argo CD
# controllers and External Secrets, then restores only the writers it changed,
# in reverse order. State (original UID, replicas, selector, changed list, Finish
# time) lives in $P01_K8S_STATE so a lost shell can still restore. No Secret
# data is read or printed.
set +x
set -uo pipefail

usage() {
  echo "usage: $0 discover|stop|check|restore|finish|force-refresh <namespace> <name>|finish-wait" >&2
  exit 2
}
[ "$#" -ge 1 ] || usage
step=$1
shift

p01_ns=(argocd argocd external-secrets)
p01_resource=(statefulset/argocd-application-controller deployment/argocd-applicationset-controller deployment/external-secrets)
p01_changed=()
p01_restore_writers() {
  local i uid replicas failed=0
  for i in 2 1 0; do
    [[ " ${p01_changed[*]} " == *" $i "* ]] || continue
    uid="$(kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" get "${p01_resource[i]}" -o jsonpath='{.metadata.uid}')" || { failed=1; continue; }
    [[ "$uid" == "$(jq -er '.uid' "$P01_K8S_STATE/$i.json")" ]] || { failed=1; continue; }
    replicas="$(jq -er '.desired' "$P01_K8S_STATE/$i.json")" || { failed=1; continue; }
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" scale "${p01_resource[i]}" --replicas="$replicas" || { failed=1; continue; }
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" rollout status "${p01_resource[i]}" --timeout=90s || { failed=1; continue; }
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" get "${p01_resource[i]}" -o json |
      jq -e --arg uid "$uid" --argjson n "$replicas" '.metadata.uid == $uid and .spec.replicas == $n and (.status.replicas // 0) == $n and (.status.readyReplicas // 0) == $n' >/dev/null || failed=1
  done
  return "$failed"
}
p01_writers_zero() {
  local i selector pods
  for i in 0 1 2; do
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" get "${p01_resource[i]}" -o json |
      jq -e --arg uid "$(jq -er '.uid' "$P01_K8S_STATE/$i.json")" '.metadata.uid == $uid and .spec.replicas == 0 and (.status.replicas // 0) == 0 and (.status.readyReplicas // 0) == 0 and .status.observedGeneration >= .metadata.generation' >/dev/null || return 1
    selector="$(jq -er '.selector' "$P01_K8S_STATE/$i.json")" || return 1
    pods="$(kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" get pods -l "$selector" -o name)" || return 1
    [[ -z "$pods" ]] || return 1
  done
}
p01_eso_gate() {
  local store actual applications
  store="$(kubectl --context k3d-hyhome --request-timeout=5s get clustersecretstore vault-backend -o json)" || return 2
  jq -e 'any(.status.conditions[]?; .type == "Ready" and .status == "True")' <<<"$store" >/dev/null || return 1
  actual="$(kubectl --context k3d-hyhome --request-timeout=5s get externalsecrets -A -o json)" || return 2
  jq -e --slurpfile expected "$P01_EXPECTED_ES" --argjson since "$P01_FINISH_EPOCH" '
    [.items[] | select(.spec.secretStoreRef.kind == "ClusterSecretStore" and .spec.secretStoreRef.name == "vault-backend")] as $actual |
    ($actual | map({namespace:.metadata.namespace,name:.metadata.name,store:{kind:.spec.secretStoreRef.kind,name:.spec.secretStoreRef.name}}) | sort_by(.namespace,.name)) == ($expected[0] | map({namespace,name,store}) | sort_by(.namespace,.name)) and
    all($actual[]; any(.status.conditions[]?; .type == "Ready" and .status == "True" and .reason == "SecretSynced") and ((.status.refreshTime // "1970-01-01T00:00:00Z" | sub("\\.[0-9]+Z$";"Z") | fromdateiso8601) > $since))' <<<"$actual" >/dev/null || return 1
  applications="$(kubectl --context k3d-hyhome --request-timeout=5s -n argocd get applications root-platform platform-cluster-config platform-external-secrets-operator -o json)" || return 2
  jq -e '.items | length == 3 and all(.[]; .status.sync.status == "Synced" and .status.health.status == "Healthy")' <<<"$applications" >/dev/null
}
# end p01_eso_gate

# The reviewed exact six ExternalSecrets bound to ClusterSecretStore/vault-backend.
expected_six() {
  : "${P01_EXPECTED_ES:?검토된 정확한 여섯 namespace/name/store JSON 파일 필요}"
  : "${P01_ES_SET_APPROVAL:?여섯 대상의 외부 운영자 승인 참조 필요}"
  jq -e 'length == 6 and (map([.namespace,.name]) | unique | length) == 6 and all(.[]; (.namespace | type == "string" and length > 0) and (.name | type == "string" and length > 0) and .store.kind == "ClusterSecretStore" and .store.name == "vault-backend")' "$P01_EXPECTED_ES" >/dev/null ||
    { echo "P01_EXPECTED_ES is not the exact six" >&2; exit 1; }
}
# Every step after stop reads the saved state; the changed list survives a lost shell.
load_state() {
  : "${P01_K8S_STATE:?stop가 출력한 P01_K8S_STATE 필요}"
  [ -d "$P01_K8S_STATE" ] || exit 1
  if [ -f "$P01_K8S_STATE/changed" ]; then mapfile -t p01_changed <"$P01_K8S_STATE/changed"; fi
}
restored() { [ -e "$P01_K8S_STATE/restored" ] || { echo "writers not restored: run finish first" >&2; exit 1; }; }

case "$step" in
discover)
  # Read-only: what the operator reviews before fixing P01_EXPECTED_ES. No Secret data.
  kubectl --context k3d-hyhome --request-timeout=15s get externalsecrets -A -o json |
    jq '[.items[] | select(.spec.secretStoreRef.kind == "ClusterSecretStore" and .spec.secretStoreRef.name == "vault-backend") | {namespace:.metadata.namespace,name:.metadata.name,store:.spec.secretStoreRef,refreshPolicy:(.spec.refreshPolicy // "Periodic"),refreshInterval:.spec.refreshInterval,refreshTime:.status.refreshTime,conditions:.status.conditions}]' || exit 1
  kubectl --context k3d-hyhome --request-timeout=15s -n external-secrets get deployment external-secrets -o json |
    jq '{name:.metadata.name,uid:.metadata.uid,containers:[.spec.template.spec.containers[] | {name,image}]}' || exit 1
  ;;
stop)
  : "${P01_K8S_WINDOW_APPROVED:?창별 클러스터 운영 승인 참조 필요}"
  expected_six
  P01_K8S_STATE="$(umask 077; mktemp -d "${XDG_RUNTIME_DIR:?}/p01-k8s.XXXXXX")" || exit 1
  echo "P01_K8S_STATE=$P01_K8S_STATE"
  [ ! -f "$XDG_RUNTIME_DIR/p01-window.vars" ] || declare -p P01_K8S_STATE >>"$XDG_RUNTIME_DIR/p01-window.vars"
  for i in 0 1 2; do
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" get "${p01_resource[i]}" -o json |
      jq -e 'select(.spec.replicas >= 0 and (.status.replicas // 0) == .spec.replicas and (.status.readyReplicas // 0) == .spec.replicas and ((.spec.selector.matchExpressions // []) | length) == 0) | {uid:.metadata.uid, desired:.spec.replicas, current:(.status.replicas // 0), ready:(.status.readyReplicas // 0), selector:(.spec.selector.matchLabels | to_entries | map("\(.key)=\(.value)") | join(","))} | select(.uid != null and .selector != "")' >"$P01_K8S_STATE/$i.json" || exit 1
    jq -e . "$P01_K8S_STATE/$i.json" >/dev/null || exit 1
  done
  for i in 0 1 2; do
    uid="$(kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" get "${p01_resource[i]}" -o jsonpath='{.metadata.uid}')" || { p01_restore_writers; exit 1; }
    [[ "$uid" == "$(jq -er '.uid' "$P01_K8S_STATE/$i.json")" ]] || { p01_restore_writers; exit 1; }
    p01_changed+=("$i") # 요청 결과가 불확실해도 복구 대상에 포함한다.
    printf '%s\n' "${p01_changed[@]}" >"$P01_K8S_STATE/changed" || { p01_restore_writers; exit 1; }
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" scale "${p01_resource[i]}" --replicas=0 || { p01_restore_writers; exit 1; }
    selector="$(jq -er '.selector' "$P01_K8S_STATE/$i.json")" || { p01_restore_writers; exit 1; }
    kubectl --context k3d-hyhome --request-timeout=15s -n "${p01_ns[i]}" wait --for=delete pod -l "$selector" --timeout=90s || { p01_restore_writers; exit 1; }
  done
  sleep 30
  p01_writers_zero || { p01_restore_writers; exit 1; }
  echo "WRITERS_ZERO"
  ;;
check)
  # Again right before the W3 snapshot; any drift restores the changed writers.
  load_state
  if p01_writers_zero; then echo "WRITERS_ZERO"; else p01_restore_writers; echo "writers not zero; restored" >&2; exit 1; fi
  ;;
restore)
  load_state
  if p01_restore_writers; then echo "WRITERS_RESTORED"; else echo "restore FAIL: record UID, replicas, pods and owner" >&2; exit 1; fi
  ;;
finish)
  # Finish time first, then restore, then one gate run (exit 2 is an API error).
  load_state
  expected_six
  P01_FINISH_EPOCH="$(date -u +%s)" || exit 1
  echo "$P01_FINISH_EPOCH" >"$P01_K8S_STATE/finish-epoch" || exit 1
  p01_restore_writers || { printf '%s\n' 'Finish FAIL: writer 복구 실패' >&2; exit 1; }
  # force-refresh and finish-wait require a successful restore.
  : >"$P01_K8S_STATE/restored"
  if p01_eso_gate; then echo "ESO_GATE_PASS"; exit 0; else gate=$?; fi
  [ "$gate" != 2 ] || { echo "Finish FAIL: API error" >&2; exit 1; }
  echo "ESO gate not yet passed: investigate, then force-refresh if approved, then finish-wait" >&2
  exit 1
  ;;
force-refresh)
  # One approved failing target at a time, at most once each.
  [ "$#" -eq 2 ] || usage
  : "${P01_FORCE_REFRESH_APPROVAL:?정확한 실패 대상의 강제 갱신 승인 필요}"
  load_state
  restored
  expected_six
  jq -e --arg ns "$1" --arg name "$2" 'any(.[]; .namespace == $ns and .name == $name)' "$P01_EXPECTED_ES" >/dev/null || exit 1
  kubectl --context k3d-hyhome --request-timeout=15s -n "$1" get externalsecret "$2" -o json |
    jq -e '.spec.secretStoreRef.kind == "ClusterSecretStore" and .spec.secretStoreRef.name == "vault-backend" and ((.spec.refreshPolicy // "Periodic") == "OnChange" or ((.spec.refreshPolicy // "Periodic") == "Periodic" and (.spec.refreshInterval // "1h" | test("[1-9]") )))' >/dev/null || exit 1
  [ ! -e "$P01_K8S_STATE/refreshed-$1-$2" ] || { echo "already force-refreshed once" >&2; exit 1; }
  : >"$P01_K8S_STATE/refreshed-$1-$2"
  kubectl --context k3d-hyhome --request-timeout=15s -n "$1" annotate externalsecret "$2" force-sync="$(date -u +%s)" --overwrite || exit 1
  ;;
finish-wait)
  # At most six checks, 10 s apart, within 180 s; an API error stops at once.
  load_state
  restored
  expected_six
  P01_FINISH_EPOCH="$(cat "$P01_K8S_STATE/finish-epoch")" || exit 1
  deadline=$(( $(date -u +%s) + 180 ))
  gate=1
  for attempt in 1 2 3 4 5 6; do
    [[ $(date -u +%s) -lt "$deadline" ]] || break
    if p01_eso_gate; then gate=0; break; else gate=$?; fi
    [[ "$gate" != 2 ]] || break
    [[ "$attempt" == 6 ]] || sleep 10
  done
  [[ "$gate" == 0 ]] || { printf '%s\n' 'Finish FAIL: ESO gate 미통과' >&2; exit 1; }
  echo "ESO_GATE_PASS"
  ;;
*) usage ;;
esac
