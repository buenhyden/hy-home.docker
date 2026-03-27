# SeaweedFS Storage Guide

> High-performance distributed storage with S3 and FUSE interfaces.

---

## Overview (KR)

이 문서는 SeaweedFS 분산 스케일아웃 스토리지에 대한 기술 가이드를 제공한다. SeaweedFS는 메타데이터와 실제 데이터를 분리하여 관리함으로써 수십억 개의 파일에 대한 저지연 접근을 보장한다. `hy-home.docker` 환경에서의 연결 방법, 인터페이스 활용법 및 성능 최적화 방안을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- DevOps Engineer
- Data Engineer

## Purpose

사용자가 SeaweedFS의 다양한 인터페이스(S3, Filer API, FUSE)를 목적에 맞게 선택하고 연동할 수 있도록 돕는다.

## Prerequisites

- `infra/04-data/lake-and-object/seaweedfs` 서비스가 실행 중이어야 함.
- S3 SDK 또는 WebDAV/Filer API 호출을 위한 `curl`, `mc` 툴 필요.

## Step-by-step Instructions

### 1. S3 API 활용 (Using S3 API)

MinIO와 동일한 S3 호환 API를 제공한다.
- **Endpoint**: `https://s3.${DEFAULT_URL}`
- **Bucket 생성**: `mc mb myseaweed/bucket-name`

### 2. Filer API (CDN) 활용 (Using Filer API)

파일시스템 수준의 정적 자원 서빙에 최적화되어 있다.
- **Endpoint**: `https://cdn.${DEFAULT_URL}`
- **파일 업로드 예시**:
  ```bash
  curl -F file=@picture.jpg http://seaweedfs-filer:8888/path/to/save/
  ```

### 3. FUSE 호스트 마운트 (FUSE Host Mount)

컨테이너 외부 호스트 환경에서 SeaweedFS를 로컬 디렉토리처럼 사용할 수 있다.
- **Mount Point**: `/mnt/seaweedfs`
- **사용 사례**: 대용량 로그 분석, 미디어 파일 직접 편집 등.

### 4. 클러스터 모니터링 (Cluster Monitoring)

Master UI를 통해 볼륨 서버 상태와 복제 상태를 확인한다.
- **Dashboard**: `https://seaweedfs.${DEFAULT_URL}`

## Common Pitfalls

- **Volume Size Limit**: 볼륨 파일 하나가 가득 차면 자동으로 새로운 볼륨이 할당되지만, 마스터 서버에서 이를 확인하지 못할 경우 쓰기 장애가 발생할 수 있다.
- **Filer Persistence**: Filer의 메타데이터는 Cassandra, MySQL, Redis 등 외부 DB에 저장할 수 있다. 기본 설정은 Filer 내장 LevelDB를 사용하므로 데이터 유실에 주의해야 한다.

## Related Documents

- **Spec**: [Data Persistence Spec](../../../../docs/04.specs/04-data/spec.md)
- **Operation**: [SeaweedFS Operations Policy](../../../../docs/08.operations/04-data/lake-and-object/seaweedfs.md)
- **Runbook**: [SeaweedFS Recovery Runbook](../../../../docs/09.runbooks/04-data/lake-and-object/seaweedfs.md)

