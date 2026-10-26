#!/bin/sh
# Optional dedicated broker monitor ACL; no arbitrary user or rule input.
set -eu

fail() {
  printf '%s\n' 'Valkey monitor ACL: invalid input' >&2
  exit 1
}

[ "$#" -eq 3 ] || fail
default_secret=$1
monitor_secret=$2
acl_file=$3
case "$acl_file" in /*/users.acl) ;; *) fail ;; esac
parent=${acl_file%/*}
[ -d "$parent" ] || fail
[ ! -L "$parent" ] || fail
[ "$(readlink -f "$parent")" = "$parent" ] || fail
[ "$(stat -c '%u %a' "$parent")" = "$(id -u) 700" ] || fail
if [ -e "$acl_file" ] || [ -L "$acl_file" ]; then
  [ -f "$acl_file" ] || fail
  [ ! -L "$acl_file" ] || fail
  [ "$(stat -c '%u %a %h' "$acl_file")" = "$(id -u) 600 1" ] || fail
fi

hash_secret() {
  secret_path=$1
  [ -f "$secret_path" ] || fail
  [ ! -L "$secret_path" ] || fail
  [ -r "$secret_path" ] || fail
  metadata=$(stat -c '%u %g %a %h' "$secret_path") || fail
  # Metadata is numeric stat output, never credential content.
  read -r secret_uid secret_gid secret_mode secret_links <<EOF
$metadata
EOF
  [ "$secret_links" = 1 ] || fail
  case "$secret_mode" in
    400|600) [ "$secret_uid" = "$(id -u)" ] || fail ;;
    440|640)
      case " $(id -G) " in *" $secret_gid "*) ;; *) fail ;; esac ;;
    *) fail ;;
  esac
  [ "$(awk 'END { print NR }' "$secret_path")" -eq 1 ] || fail
  if LC_ALL=C grep -q '[^ -~]' "$secret_path"; then fail; fi
  [ "$(tr -d '\n' < "$secret_path" | wc -c)" -gt 0 ] || fail
  digest=$(tr -d '\n' < "$secret_path" | sha256sum) || fail
  printf '%s\n' "${digest%% *}"
}

# All credential checks precede creating or replacing any ACL output.
default_hash=$(hash_secret "$default_secret") || fail
monitor_hash=$(hash_secret "$monitor_secret") || fail
[ "$default_hash" != "$monitor_hash" ] || fail
umask 077
tmp_file=$(mktemp "$parent/users.acl.XXXXXXXX") || fail
trap 'rm -f "$tmp_file"' 0
trap 'rm -f "$tmp_file"; exit 1' 1 2 3 15
{
  printf 'user default reset on #%s ~* &* +@all\n' "$default_hash"
  printf 'user monitor reset on #%s resetkeys resetchannels -@all +ping +info +command|info +slowlog|len +commandlog|len\n' "$monitor_hash"
} > "$tmp_file"
chmod 600 "$tmp_file"
mv -f "$tmp_file" "$acl_file"
trap - 0 1 2 3 15
