#!/bin/sh
set -eu

require_secret() {
  if [ ! -s "$1" ]; then
    echo "missing required secret: $1" >&2
    exit 1
  fi
}

require_secret /run/secrets/n8n_db_password
broker_host=${N8N_VALKEY_HOST:-mng-valkey}
broker_user=${N8N_VALKEY_USERNAME-}
broker_secret=${N8N_VALKEY_SECRET:-mng_valkey_password}
broker_db=${N8N_VALKEY_DB-0}
case "$broker_host:$broker_user:$broker_secret:$broker_db" in
  mng-valkey::mng_valkey_password:0|n8n-valkey::n8n_valkey_password:0|mng-valkey:n8n:mng_valkey_n8n_password:0) ;;
  *) echo "unsupported n8n broker selection" >&2; exit 1 ;;
esac
if [ "${QUEUE_BULL_REDIS_HOST-$broker_host}" != "$broker_host" ] ||
   [ "${QUEUE_BULL_REDIS_USERNAME-$broker_user}" != "$broker_user" ] ||
   [ "${QUEUE_BULL_REDIS_DB-$broker_db}" != "$broker_db" ] ||
   [ "${QUEUE_BULL_REDIS_PASSWORD_FILE-/run/secrets/$broker_secret}" != "/run/secrets/$broker_secret" ] ||
   [ "${QUEUE_BULL_PREFIX-n8n}" != n8n ] ||
   [ "${N8N_REDIS_KEY_PREFIX-n8n}" != n8n ] ||
   [ -n "${QUEUE_BULL_REDIS_CLUSTER_NODES-}" ]; then
  echo "inconsistent n8n queue settings" >&2
  exit 1
fi
export QUEUE_BULL_REDIS_HOST="$broker_host" QUEUE_BULL_REDIS_USERNAME="$broker_user"
export QUEUE_BULL_REDIS_DB="$broker_db" QUEUE_BULL_REDIS_PASSWORD_FILE="/run/secrets/$broker_secret"
require_secret "$QUEUE_BULL_REDIS_PASSWORD_FILE"
require_secret /run/secrets/n8n_encryption_key
require_secret /run/secrets/n8n_runner_auth_token

# OPSFLOW PACKAGE BRIDGE
# One immutable package link; never install packages or modify unrelated assets.
node <<'OPSFLOW_NODE'
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const image = '/opt/hyhome/n8n-custom/opsflow';
const imageOwner = 0;
const packageName = 'n8n-nodes-opsflow';
function fail() { throw new Error('OPSFLOW_PACKAGE FAIL'); }
function stat(file) { return fs.lstatSync(file); }
function noSymlinkParents(file) {
  const parts = path.resolve(file).split(path.sep).filter(Boolean);
  let current = path.parse(file).root;
  for (const part of parts) {
    current = path.join(current, part);
    if (stat(current).isSymbolicLink()) fail();
  }
}
function trusted(file, directory) {
  const metadata = stat(file);
  if (metadata.uid !== imageOwner || (metadata.mode & 0o022) ||
      metadata.isSymbolicLink() ||
      (directory ? !metadata.isDirectory() : !metadata.isFile())) fail();
}
function files(directory, prefix = '') {
  trusted(directory, true);
  return fs.readdirSync(directory).sort().flatMap((name) => {
    const relative = prefix ? prefix + '/' + name : name;
    const absolute = path.join(directory, name);
    const metadata = stat(absolute);
    if (metadata.isDirectory()) return files(absolute, relative);
    trusted(absolute, false);
    return [relative];
  });
}
try {
  noSymlinkParents(image);
  for (const directory of ['/opt', '/opt/hyhome', '/opt/hyhome/n8n-custom']) trusted(directory, true);
  const deployed = files(image).filter((name) => name !== 'SHA256SUMS');
  const receipt = fs.readFileSync(path.join(image, 'SHA256SUMS'), 'utf8');
  const expected = new Map();
  for (const line of receipt.trimEnd().split('\n')) {
    const match = /^([a-f0-9]{64})  ([A-Za-z0-9_@+./-]+)$/.exec(line);
    if (!match || !match[2] || path.isAbsolute(match[2]) ||
        match[2].split('/').some((part) => !part || part === '.' || part === '..') ||
        expected.has(match[2])) fail();
    expected.set(match[2], match[1]);
  }
  if (deployed.length !== expected.size || !expected.has('package.json') ||
      !expected.has('dist/OpsflowSmtp.node.js') || !expected.has('dist/transport.js')) fail();
  for (const relative of deployed) {
    const digest = crypto.createHash('sha256').update(fs.readFileSync(path.join(image, relative))).digest('hex');
    if (expected.get(relative) !== digest) fail();
  }
  const metadata = JSON.parse(fs.readFileSync(path.join(image, 'package.json'), 'utf8'));
  if (metadata.name !== packageName || metadata.n8n?.n8nNodesApiVersion !== 1 ||
      JSON.stringify(metadata.n8n.nodes) !== JSON.stringify(['dist/OpsflowSmtp.node.js'])) fail();
  // Match exact upstream getN8nFolder without changing HOME.
  const userFolder = process.env.N8N_USER_FOLDER ?? process.env.HOME ?? process.cwd();
  if (!path.isAbsolute(userFolder) || path.normalize(userFolder) !== userFolder) fail();
  noSymlinkParents(userFolder);
  const folderMetadata = stat(userFolder);
  if (!folderMetadata.isDirectory() || folderMetadata.uid !== process.getuid() ||
      (folderMetadata.mode & 0o022)) fail();
  let parent = userFolder;
  for (const component of ['.n8n', 'nodes', 'node_modules']) {
    parent = path.join(parent, component);
    try { fs.mkdirSync(parent, { mode: 0o700 }); }
    catch (error) { if (error.code !== 'EEXIST') throw error; }
    const metadata = stat(parent);
    if (!metadata.isDirectory() || metadata.isSymbolicLink() ||
        metadata.uid !== process.getuid() || (metadata.mode & 0o022)) fail();
  }
  const destination = path.join(parent, packageName);
  try { fs.symlinkSync(image, destination, 'dir'); }
  catch (error) { if (error.code !== 'EEXIST') throw error; }
  if (!stat(destination).isSymbolicLink() || fs.readlinkSync(destination) !== image) fail();
} catch {
  console.error('OPSFLOW_PACKAGE FAIL');
  process.exit(1);
}
OPSFLOW_NODE
# END OPSFLOW PACKAGE BRIDGE

if [ -d /opt/custom-certificates ]; then
  echo "Trusting custom certificates from /opt/custom-certificates."
  export NODE_OPTIONS="--use-openssl-ca ${NODE_OPTIONS:-}"
  export SSL_CERT_DIR=/opt/custom-certificates
  c_rehash /opt/custom-certificates || true
fi

if [ "$#" -gt 0 ]; then
  # Got started with arguments
  exec n8n "$@"
else
  # Got started without arguments
  exec n8n
fi
