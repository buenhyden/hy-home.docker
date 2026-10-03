#!/bin/sh
# Valkey Cluster Initialization Script (Example)
# 실제 사용 시에는 이 파일을 복사하여 valkey-cluster-init.sh로 저장하고 환경에 맞게 수정하세요.

set -eu

# Docker Secrets에서 비밀번호 로드
[ -s /run/secrets/lab_valkey_password ] || { echo "LAB Valkey password is missing" >&2; exit 1; }
REDISCLI_AUTH=$(cat /run/secrets/lab_valkey_password)
[ -n "$REDISCLI_AUTH" ] || { echo "LAB Valkey password is empty" >&2; exit 1; }
export REDISCLI_AUTH
echo "Waiting for Cluster nodes..."
sleep 5

# Node 0(6379)을 기준으로 상태 확인
if valkey-cli -h valkey-node-0 -p 6379 cluster info 2>/dev/null | grep -q "cluster_state:ok"; then
  echo "✅ Cluster already configured."
  exit 0
fi

echo "🚧 Creating Valkey Cluster..."

# 실제 포트(6379~6384)로 클러스터 생성 시도
if output=$(
  valkey-cli --cluster create \
    valkey-node-0:6379 \
    valkey-node-1:6380 \
    valkey-node-2:6381 \
    valkey-node-3:6382 \
    valkey-node-4:6383 \
    valkey-node-5:6384 \
    --cluster-replicas 1 \
    --cluster-yes 2>&1
); then
  echo "$output"
  echo "🎉 Cluster creation completed!"
  exit 0
fi

echo "$output"
if echo "$output" | grep -qi "is not empty"; then
  echo "ERROR: nodes contain data or cluster metadata but cluster state is not healthy; manual LAB review required" >&2
  exit 1
fi

echo "❌ Cluster creation failed with an unexpected error."
exit 1
