#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
script="$root/scripts/operations/update-main-current-tag.sh"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

git init --bare -q "$tmp/remote.git"
git -C "$tmp/remote.git" config core.hooksPath "$tmp/remote.git/hooks"
git init -q "$tmp/work"
git -C "$tmp/work" config core.hooksPath /dev/null
git -C "$tmp/work" config user.name Test
git -C "$tmp/work" config user.email test@example.invalid
git -C "$tmp/work" checkout -q -b main
git -C "$tmp/work" commit -q --allow-empty -m initial
git -C "$tmp/work" remote add origin "$tmp/remote.git"
git -C "$tmp/work" push -q origin main
first=$(git -C "$tmp/work" rev-parse HEAD)
git -C "$tmp/work" tag 0.0.1 "$first"
git -C "$tmp/work" push -q origin 0.0.1

remote_tag() {
  git --git-dir="$tmp/remote.git" rev-parse -q --verify refs/tags/main-current 2>/dev/null || true
}
release_tag() {
  git --git-dir="$tmp/remote.git" rev-parse refs/tags/0.0.1
}
run_update() {
  (cd "$tmp/work" && GITHUB_REF=refs/heads/main GITHUB_SHA="$1" bash "$script")
}
assert_release() {
  test "$(release_tag)" = "$first"
}

# A missing channel tag is created; the same commit is idempotent.
receipt=$(run_update "$first")
[[ $receipt == *"main-current old=<absent> new=$first"* ]]
test "$(remote_tag)" = "$first"
receipt=$(run_update "$first")
[[ $receipt == *"main-current old=$first new=$first (unchanged)"* ]]
test "$(remote_tag)" = "$first"
assert_release

# A stale run cannot move the channel backward.
git -C "$tmp/work" commit -q --allow-empty -m second
git -C "$tmp/work" push -q origin main
second=$(git -C "$tmp/work" rev-parse HEAD)
if run_update "$first"; then exit 1; fi
test "$(remote_tag)" = "$first"
run_update "$second"
test "$(remote_tag)" = "$second"
assert_release

# Annotated channel tags are refused without touching a release tag.
git -C "$tmp/work" tag -fa main-current -m annotated "$first" >/dev/null
git -C "$tmp/work" push -q --force origin refs/tags/main-current
test "$(git --git-dir="$tmp/remote.git" cat-file -t refs/tags/main-current)" = tag
if run_update "$second"; then exit 1; fi
assert_release

# A failed remote update must report failure.
git -C "$tmp/work" tag -f main-current "$second" >/dev/null
git -C "$tmp/work" push -q --force origin refs/tags/main-current
cat > "$tmp/remote.git/hooks/pre-receive" <<'HOOK'
#!/usr/bin/env bash
exit 1
HOOK
chmod +x "$tmp/remote.git/hooks/pre-receive"
git -C "$tmp/work" commit -q --allow-empty -m third
# Main must advance before the tag update; permit this one main push.
cat > "$tmp/remote.git/hooks/pre-receive" <<'HOOK'
#!/usr/bin/env bash
while read -r old new ref; do
  if [[ $ref == refs/tags/main-current ]]; then exit 1; fi
done
HOOK
chmod +x "$tmp/remote.git/hooks/pre-receive"
git -C "$tmp/work" push -q origin main
third=$(git -C "$tmp/work" rev-parse HEAD)
if run_update "$third"; then exit 1; fi
test "$(remote_tag)" = "$second"
assert_release

# A concurrent tag move after the read is rejected by the remote lease.
rm "$tmp/remote.git/hooks/pre-receive"
mkdir "$tmp/bin"
cat > "$tmp/bin/git" <<'WRAPPER'
#!/usr/bin/env bash
if [[ ${1:-} == push ]]; then
  "$TAG_TEST_REAL_GIT" --git-dir="$TAG_TEST_REMOTE" update-ref \
    refs/tags/main-current "$TAG_TEST_RACE_SHA"
fi
exec "$TAG_TEST_REAL_GIT" "$@"
WRAPPER
chmod +x "$tmp/bin/git"
if (cd "$tmp/work" && PATH="$tmp/bin:$PATH" \
    TAG_TEST_REAL_GIT="$(command -v git)" \
    TAG_TEST_REMOTE="$tmp/remote.git" TAG_TEST_RACE_SHA="$first" \
    GITHUB_REF=refs/heads/main GITHUB_SHA="$third" bash "$script"); then
  exit 1
fi
test "$(remote_tag)" = "$first"
assert_release

printf 'PASS: main-current update guards\n'
