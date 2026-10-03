#!/bin/sh
set -eu
/bin/sh /usr/local/libexec/dev-valkey/render-acl.sh
exec valkey-server /etc/dev-valkey/valkey.conf --aclfile /run/valkey/users.acl
