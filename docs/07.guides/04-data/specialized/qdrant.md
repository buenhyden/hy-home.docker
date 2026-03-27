# Qdrant Vector Database Guide

> Technical guide for understanding and using Qdrant within the `04-data/specialized` tier.

## Overview (KR)

이 문서는 Qdrant 벡터 데이터베이스에 대한 기술 가이드다. 고차원 벡터 임베딩의 저장 및 검색(Similarity Search)을 위한 아키텍처와 RAG(Retrieval-Augmented Generation) 워크플로 통합 방법을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- AI/ML Engineers
- Backend Developers
- Operators
- AI Agents

## Purpose

이 가이드는 Qdrant의 컬렉션 관리, 벡터 검색 최적화 및 gRPC/REST API를 통한 서비스 연동을 돕는다.

## Prerequisites

- Docker 및 Docker Compose 설치
- `ai` 또는 `data` 프로필 활성화
- 벡터 임베딩(Vector Embeddings)에 대한 기본 이해

## Step-by-step Instructions

### 1. Connecting to Qdrant
Qdrant는 REST와 gRPC 프로토콜을 모두 지원한다.
- **REST URL**: `https://qdrant.${DEFAULT_URL}`
- **gRPC URL**: `qdrant-grpc.${DEFAULT_URL}:6334`

### 2. Collection Management (REST)
컬렉션을 생성하여 벡터 데이터를 격리한다.
```bash
curl -X PUT "https://qdrant.${DEFAULT_URL}/collections/my_collection" \
     -H "Content-Type: application/json" \
     --data '{
        "vectors": { "size": 1536, "distance": "Cosine" }
     }'
```

### 3. Vector Similarity Search
임베딩을 사용하여 유사한 문서를 검색한다.
```bash
curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/points/search" \
     -H "Content-Type: application/json" \
     --data '{
        "vector": [0.1, 0.2, ...],
        "limit": 10
     }'
```

## Common Pitfalls

- **Payload Size**: 대용량 페이로드 저장 시 메모리 및 디스크 사용량이 급증할 수 있으므로, 필요한 메타데이터만 포함한다.
- **Indexing Latency**: 데이터 대량 삽입 후 Indexing이 완료될 때까지 검색 성능이 저하될 수 있다.

## Related Documents

- **Spec**: `[infra/04-data/specialized/qdrant/README.md](../../../../infra/04-data/specialized/qdrant/README.md)`
- **Operation**: `[../../08.operations/04-data/specialized/qdrant.md](../../../08.operations/04-data/specialized/qdrant.md)`
- **Runbook**: `[../../09.runbooks/04-data/specialized/qdrant.md](../../../09.runbooks/04-data/specialized/qdrant.md)`
