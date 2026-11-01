#!/usr/bin/env bash
# Install one committed release in a disposable root container and prove, as
# separate Publisher and Hermes accounts, that `python3 -I` loads it, that
# neither account can alter code, store, interpreter or library, and that any
# weakened path fails closed. Needs Docker and PyPI (wheels are hash-locked).
# Usage: tests/install-check.sh [commit] [image]
set -euo pipefail
commit=$(git rev-parse "${1:-HEAD}")
image=${2:-ghcr.io/astral-sh/uv:python3.12-bookworm-slim}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
git archive --format=tar -o "$work/release.tar" "$commit" -- \
  infra/07-workflow/n8n/workloads/hermes-blog-ingestion
docker run --rm --network bridge -v "$work:/in:ro" "$image" bash -euo pipefail -c '
python=$(readlink -f "$(command -v python3)")
installer=/src/infra/07-workflow/n8n/workloads/hermes-blog-ingestion/install.py
useradd --system --no-create-home hermes-publisher
useradd --system --no-create-home hermes
mkdir /src && tar -xf /in/release.tar -C /src
if python3 -I "$installer" --archive /in/release.tar --python "$python" 2>/dev/null; then
  echo "FAIL archive writable by a non-root owner was installed"; exit 1
fi
echo "PASS archive not owned by root refused"
install -m 0600 /in/release.tar /root/release.tar
mkdir -m 0755 /opt/taken && chown hermes /opt/taken
if python3 -I "$installer" --archive /root/release.tar --prefix /opt/taken/p --python "$python" 2>/dev/null \
  || [ -e /opt/taken/p ]; then
  echo "FAIL prefix under a Hermes-owned directory was used"; exit 1
fi
echo "PASS prefix with a non-root ancestor refused"
release=$(python3 -I "$installer" --archive /root/release.tar --python "$python")
venv=$release/venv
site=$("$venv/bin/python" -I -c "import sysconfig; print(sysconfig.get_path(\"purelib\"))")
crypto=$site/cryptography/hazmat/primitives/asymmetric/ed25519.py
store=$site/publisher/producer-keys.json
ok="{\"keys\": 0, \"runtime\": \"protected\"}"
bad="{\"error\": \"store_unprotected\"}"
verify() { runuser -u hermes-publisher -- "$venv/bin/python" -I -m publisher.cli verify-install || true; }
check() { [ "$1" = "$2" ] || { echo "FAIL $3: $1"; exit 1; }; echo "PASS $3"; }

check "$(verify)" "$ok" "dedicated account loads the protected release"
(cd "$site" && sha256sum --quiet -c "$release/MANIFEST.sha256") || { echo "FAIL manifest"; exit 1; }
echo "PASS installed files match the archive manifest"
for name in acquirer producer_sealer attestation attester source_check source_fetch; do
  if [ -e "$site/publisher/$name.py" ]; then echo "FAIL producer module $name installed"; exit 1; fi
done
echo "PASS only the Publisher module allowlist is installed"
for user in hermes-publisher hermes; do
  for target in "$site/publisher/trust.py" "$store" "$crypto" "$venv/pyvenv.cfg" "$site/publisher/x.py" "$python"; do
    if runuser -u "$user" -- sh -c "echo x >> \"$target\"" 2>/dev/null; then echo "FAIL $user wrote $target"; exit 1; fi
  done
done
echo "PASS neither account can alter code, store, library, venv or interpreter"

check "$(runuser -u hermes-publisher -- "$venv/bin/python" -m publisher.cli verify-install || true)" \
  "{\"error\": \"interpreter_unisolated\"}" "non-isolated run refused"
mkdir -p /tmp/evil/publisher && echo "print(1)" > /tmp/evil/publisher/cli.py && touch /tmp/evil/publisher/__init__.py
check "$(runuser -u hermes-publisher -- env PYTHONPATH=/tmp/evil "$venv/bin/python" -I -m publisher.cli verify-install || true)" \
  "$ok" "PYTHONPATH ignored under -I"
check "$("$venv/bin/python" -I -m publisher.cli verify-install || true)" "$bad" "root runner refused"

weaken() { $3 "$2"; check "$(verify)" "$bad" "$1"; $4 "$2"; }
weaken "library sub-file owned by Hermes" "$crypto" "chown hermes" "chown root"
weaken "store group-writable" "$store" "chmod g+w" "chmod g-w"
weaken "verifier module owned by Publisher" "$site/publisher/evidence.py" "chown hermes-publisher" "chown root"
weaken "venv config owned by Hermes" "$venv/pyvenv.cfg" "chown hermes" "chown root"
weaken "import directory other-writable" "$site" "chmod o+w" "chmod o-w"
weaken "interpreter owned by Hermes" "$python" "chown hermes" "chown root"
check "$(verify)" "$ok" "restored release is protected again"

if python3 -I "$installer" --archive /root/release.tar --python "$python" 2>/dev/null; then
  echo "FAIL reinstall overwrote a release"; exit 1
fi
echo "PASS releases are immutable"

# The attester role: its own account and prefix, plus the signing and fetching modules.
useradd --system --no-create-home hermes-attester
arelease=$(python3 -I "$installer" --role attester --archive /root/release.tar --python "$python")
case "$arelease" in /opt/hermes-attester/releases/*) echo "PASS attester release under its own prefix";;
  *) echo "FAIL attester release at $arelease"; exit 1;; esac
asite=$("$arelease/venv/bin/python" -I -c "import sysconfig; print(sysconfig.get_path(\"purelib\"))")
for name in attestation attester source_check source_fetch; do
  [ -e "$asite/publisher/$name.py" ] || { echo "FAIL attester module $name missing"; exit 1; }
done
echo "PASS attester release carries the attester modules"
runuser -u hermes-attester -- "$arelease/venv/bin/python" -I -m publisher.cli attest-queue --help >/dev/null \
  || { echo "FAIL attester account cannot run attest-queue"; exit 1; }
echo "PASS attester account runs attest-queue from the release"
refusal=$(runuser -u hermes-publisher -- "$venv/bin/python" -I -m publisher.cli attest-queue --gateway https://g.example \
  --auth-header-file /nonexistent --signing-key /nonexistent --key-id x --state-dir /tmp/s --evidence-dir /tmp/e 2>&1 || true)
check "$refusal" "{\"error\":\"operation_rejected\"}" "Publisher release refuses attest-queue"
'
