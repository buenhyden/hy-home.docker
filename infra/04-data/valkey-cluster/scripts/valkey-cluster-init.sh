#!/bin/sh
set -eu

VALKEY_PASSWORD=$(cat /run/secrets/valkey_password)
echo "Waiting for Cluster nodes..."
sleep 5

# Node 0(6370)을 기준으로 상태 확인
if valkey-cli -a "$VALKEY_PASSWORD" -h valkey-node-0 -p 6370 cluster info 2>/dev/null | grep -q "cluster_state:ok"; then
  echo "✅ Cluster already configured."
  exit 0
fi

echo "🚧 Creating Valkey Cluster..."

# 변경된 포트(6370~6375)로 클러스터 생성
valkey-cli -a "$VALKEY_PASSWORD" --cluster create \
  valkey-node-0:6379 \
  valkey-node-1:6380 \
  valkey-node-2:6381 \
  valkey-node-3:6382 \
  valkey-node-4:6383 \
  valkey-node-5:6384 \
  --cluster-replicas 1 \
  --cluster-yes

echo "🎉 Cluster creation completed!"
