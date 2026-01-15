#!/bin/sh
set -eu

REDIS_PASSWORD=$(cat /run/secrets/redis_password)
echo "Waiting for Cluster nodes..."
sleep 5

# Node 0(6370)을 기준으로 상태 확인
if redis-cli -a "$REDIS_PASSWORD" -h redis-node-0 -p 6370 cluster info 2>/dev/null | grep -q "cluster_state:ok"; then
  echo "✅ Cluster already configured."
  exit 0
fi

echo "🚧 Creating Redis Cluster..."

# 변경된 포트(6370~6375)로 클러스터 생성
redis-cli -a "$REDIS_PASSWORD" --cluster create \
  redis-node-0:6379 \
  redis-node-1:6380 \
  redis-node-2:6381 \
  redis-node-3:6382 \
  redis-node-4:6383 \
  redis-node-5:6384 \
  --cluster-replicas 1 \
  --cluster-yes

echo "🎉 Cluster creation completed!"