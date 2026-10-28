#!/usr/bin/env bash
# RUN-0105 W1 source bootstrap: copy the reviewed helpers of one approved commit into a
# fresh owner-only tmpfs directory and check each against the pinned hash below.
# Run it only through p01_run (RUN-0085), which reads this file from that same commit:
#   p01_run <commit> infra/03-security/openbao/scripts/p01-bootstrap.sh <commit>
# Path variables go to $XDG_RUNTIME_DIR/p01-window.vars; load them with
# `. "$XDG_RUNTIME_DIR/p01-window.vars"`. A stale pin stops here, before any secret is read.
[ "$#" -eq 1 ] || { echo "usage: p01-bootstrap.sh <approved 40-character commit>" >&2; exit 2; }
P01_APPROVED_COMMIT=$1
unset LD_PRELOAD LD_LIBRARY_PATH PYTHONHOME PYTHONPATH
P01_HOME_ROOT=/home/hyunyoun/data/hy-home.docker
test "$P01_HOME_ROOT" = "$(/usr/bin/realpath -e -- "$P01_HOME_ROOT")" || exit 1
test "$(/usr/bin/stat -c '%d:%i:%u' -- "$P01_HOME_ROOT")" = 64512:4338469:1000 || exit 1
test ! -L "$P01_HOME_ROOT/.git" || exit 1
test "$(/usr/bin/stat -c '%d:%i:%u' -- "$P01_HOME_ROOT/.git")" = 64512:4338470:1000 || exit 1
case "${P01_APPROVED_COMMIT:?}" in *[!0-9a-f]*) exit 1 ;; esac
test "${#P01_APPROVED_COMMIT}" = 40 || exit 1
P01_COMMIT="$(/usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 \
  GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 /usr/bin/git \
  --git-dir="$P01_HOME_ROOT/.git" rev-parse --verify "$P01_APPROVED_COMMIT^{commit}")" || exit 1
test "$P01_COMMIT" = "$P01_APPROVED_COMMIT" || exit 1
P01_RUNTIME_DIR="${XDG_RUNTIME_DIR:?}"
test -d "$P01_RUNTIME_DIR" || exit 1
test ! -L "$P01_RUNTIME_DIR" || exit 1
test "$P01_RUNTIME_DIR" = "$(/usr/bin/realpath -e -- "$P01_RUNTIME_DIR")" || exit 1
test "$(/usr/bin/stat -c '%u:%a' -- "$P01_RUNTIME_DIR")" = "$(/usr/bin/id -u):700" || exit 1
test "$(/usr/bin/findmnt -n -T "$P01_RUNTIME_DIR" -o FSTYPE)" = tmpfs || exit 1
P01_CLIENT_DIR="$(/usr/bin/mktemp -d "$P01_RUNTIME_DIR/p01-client.XXXXXX")" || exit 1
# A copy that failed a pin never survives, and the window records no path to it.
ok=0
trap '[ "${ok:-}" = 1 ] || /usr/bin/rm -rf -- "$P01_CLIENT_DIR"' EXIT
P01_SCRIPT_DIR="$P01_CLIENT_DIR/infra/03-security/openbao/scripts"
/usr/bin/install -d -m 0700 "$P01_SCRIPT_DIR" "$P01_CLIENT_DIR/infra/03-security/openbao/config/policies" || exit 1
set -C  # never overwrite a copied source file
while read -r P01_SOURCE_HASH P01_SOURCE_PATH; do
  /usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
    GIT_NO_REPLACE_OBJECTS=1 /usr/bin/git --git-dir="$P01_HOME_ROOT/.git" \
    show --no-textconv "$P01_COMMIT:$P01_SOURCE_PATH" > "$P01_CLIENT_DIR/$P01_SOURCE_PATH" || exit 1
  printf '%s  %s\n' "$P01_SOURCE_HASH" "$P01_CLIENT_DIR/$P01_SOURCE_PATH" | /usr/bin/sha256sum -c - || exit 1
  /usr/bin/chmod 0400 "$P01_CLIENT_DIR/$P01_SOURCE_PATH" || exit 1
done <<'P01_SOURCE_MANIFEST'
b6b820b6561558020842376a06729f7663de3410188a544a6662024c4575568c infra/03-security/openbao/scripts/protected-maintenance.py
1ffe30c089361c7a7129bcce2407d08418222722aad2cba6e90804213b7c433b infra/03-security/openbao/scripts/protected-token-operations.py
05be43d5e2b9e8f067c2b81d4872666e89a1300fd2d21ecfee12db13e8aa5853 infra/03-security/openbao/scripts/protected-raft-snapshot.py
48ff7d0e0ee6e39b00c5105df5fa20891b70ac5e0e820715aad0b675ab028868 infra/03-security/openbao/scripts/protected-snapshot-archive.py
fd266cdd46d950cc8d6cc8704497fd1454bd51c47f1c4b071b24cfbf79bba724 infra/03-security/openbao/scripts/protected-snapshot-custody.py
32412b2a6f4d28f6e6105066dafd61d876443cd3160bb4feb120d7e175e3c6ef infra/03-security/openbao/scripts/protected-semantic-restore.py
b5aa92bdf528eb92993fc46061ead65b72bf71efe30182cca7cc5b5706ab396e infra/03-security/openbao/scripts/protected-semantic-execution.py
1aa658e05aee76127c7961abd218020fe6a319fd26253c78ecefb3ae99d4b622 infra/03-security/openbao/config/policies/backup-snapshot.hcl
d2bfabe2b12271d5fdb3785c32f41c2a534fafed4126712e710c3ad0a3be2ec3 infra/03-security/openbao/scripts/protected-renderer-roles.py
3a24759ae95ac6363353c9d5d28de787c75bb3c60e1af6bc4bbe34b103799a4e infra/03-security/openbao/config/policies/renderer.hcl
0ab86b526e0506b658184e0be20a9713a737262f921f1019f2f38609c394d3e5 infra/03-security/openbao/config/policies/renderer-issuer.hcl
a42f0b23de31acbeaf3c88761ebc2ba5a696fbdfcfe6667062ed864e9998a7a5 infra/03-security/openbao/config/policies/renderer-cleanup.hcl
fd277c7e09cd9a9ade1f1067664dafb39b6d91be524f285d6851919f2144847b infra/03-security/openbao/config/policies/operator.hcl
1693e2326f4aa74f5134490e6a1af8d2ed4727e11fb9d6167fec2634d4a493d4 infra/03-security/openbao/scripts/protected-restore-inputs.py
4a1052b4e888e5e0c5b025db7f6447f4719264343abc8f67e0c17fc3269e3a0f infra/03-security/openbao/config/renderer-issuer-token-role.json
bceb1e97853f173b5011f1af34033d01c07309e582137d0e67f85ae33b9eb17e infra/03-security/openbao/config/renderer-cleanup-token-role.json
e0dafc929bd037ef7910c04ee5ec343566ef7000ed7172032be3bfd95cabeb11 infra/03-security/openbao/config/renderer-role.json
38755318a3b585c78611f54fead604218ee6abd6f6c005ac15db1134ff3609c0 infra/03-security/openbao/scripts/owner-window.sh
68c20addfcfab05118c75ff5f0b25330743c82f7f7f1305f26b3f0fe65652d50 infra/03-security/openbao/config/policies/prometheus.hcl
6e99a1fa6ba153642b66be1fd353e237cc25640e81386de203d2b232a6c00eed infra/03-security/openbao/scripts/k8s-writers.sh
P01_SOURCE_MANIFEST
# Only now, with every pin checked, does the window learn these paths.
declare -p P01_CLIENT_DIR P01_RUNTIME_DIR P01_COMMIT P01_SCRIPT_DIR >>"$XDG_RUNTIME_DIR/p01-window.vars" || exit 1
ok=1
echo "bootstrap ok: $P01_SCRIPT_DIR"
