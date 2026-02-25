#!/bin/sh
set -eu

VALKEY_PASSWORD=$(cat /run/secrets/service_valkey_password)
echo "Waiting for Cluster nodes..."
sleep 5

# Node 0(6379)을 기준으로 상태 확인
if valkey-cli -a "$VALKEY_PASSWORD" -h valkey-node-0 -p 6379 cluster info 2>/dev/null | grep -q "cluster_state:ok"; then
  echo "✅ Cluster already configured."
  exit 0
fi

echo "🚧 Creating Valkey Cluster..."

# 실제 포트(6379~6384)로 클러스터 생성 시도
if output=$(
  valkey-cli -a "$VALKEY_PASSWORD" --cluster create \
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
  echo "ℹ️  Nodes already contain data/cluster metadata. Skipping destructive re-init."
  echo "ℹ️  To rebuild the cluster, run the manual reset runbook."
  exit 0
fi

echo "❌ Cluster creation failed with an unexpected error."
exit 1
