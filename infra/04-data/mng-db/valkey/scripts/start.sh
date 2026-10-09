#!/bin/sh
set -eu
/bin/sh /usr/local/libexec/mng-valkey/render-acl.sh
exec valkey-server --aclfile /run/valkey/users.acl --appendonly yes --port "${MNG_VALKEY_PORT:-6379}"
