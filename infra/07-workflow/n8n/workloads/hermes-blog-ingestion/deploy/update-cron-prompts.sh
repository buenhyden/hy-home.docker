#!/usr/bin/env bash
# Replace the direct-submission paragraph of every plugin-allowed Hermes cron
# job with research-submission-prompt.txt of merged origin/main. Text before
# the paragraph (the job's own report/email work), schedule and delivery stay.
# Run as the Hermes user, without sudo:  bash deploy/update-cron-prompts.sh
# Rollback: copy the printed jobs.json backup back and restart
# hermes-gateway.service.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$HERE" rev-parse --show-toplevel)
WL=infra/07-workflow/n8n/workloads/hermes-blog-ingestion
JOBS=$HOME/.hermes/cron/jobs.json
MARK="DIRECT RESEARCH SUBMISSION"

git -C "$REPO" fetch --quiet origin
BLOCK=$(git -C "$REPO" show "origin/main:$WL/deploy/research-submission-prompt.txt")
[[ $BLOCK == "$MARK"* ]] || { echo "prompt file does not start with $MARK" >&2; exit 1; }
# The jobs the plugin accepts, read from the same tracked source it enforces.
mapfile -t IDS < <(git -C "$REPO" show "origin/main:$WL/hermes-plugin/tools.py" |
  sed -n '/^_ALLOWED_JOBS = {/,/^}/s/^ *"\([0-9a-f]\{12\}\)": .*/\1/p')
[[ ${#IDS[@]} -gt 0 ]] || { echo "no allowed jobs found" >&2; exit 1; }

BACKUP=$JOBS.pre-prompt-$(date -u +%Y%m%dT%H%M%SZ)
cp -p "$JOBS" "$BACKUP"
echo "backup: $BACKUP"
# Build every new prompt before editing any job, so a missing paragraph stops
# the run with nothing changed.
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
printf '%s' "$BLOCK" > "$STAGE/block"
for id in "${IDS[@]}"; do
  python3 -I - "$BACKUP" "$id" "$MARK" "$STAGE/block" "$STAGE/$id" <<'PY'
import json, sys
jobs, job_id, mark, block, out = sys.argv[1:]
(job,) = [j for j in json.load(open(jobs))["jobs"] if j["id"] == job_id]
prompt = job["prompt"]
if mark not in prompt:
    sys.exit(f"{job_id}: no {mark} paragraph")
open(out, "w").write(prompt[: prompt.index(mark)] + open(block).read())
PY
done
for id in "${IDS[@]}"; do
  hermes cron edit "$id" --prompt "$(cat "$STAGE/$id")" >/dev/null
  echo "$id updated"
done
