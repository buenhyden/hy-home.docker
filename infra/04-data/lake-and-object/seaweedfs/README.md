<!-- [ID:04-data:seaweedfs] -->
# SeaweedFS

> High-performance distributed file system and object storage for tiered data lake architectures.

---

## 1. Context & Objective (KR)

SeaweedFS는 빌리언 단위의 파일을 저장하고 제공하기 위해 설계된 초고성능 분산 스토리지 시스템이다. `hy-home.docker` 환경에서 비정형 데이터, 미디어 콘텐츠 및 대규모 로그를 위한 확장 가능하고 탄력적인 저장 계층을 제공하며, Filer(파일시스템)와 S3 인터페이스를 동시에 지원한다.

## 2. Requirements & Constraints

- **Architecture**: Master-Volume-Filer 계층 구조.
- **Resource Templates**: 
  - Master/Filer: `template-stateful-med`
  - Volume: `template-stateful-high` (I/O 집중형)
- **Networking**: `infra_net` 격리 네트워크 사용.
- **Port Mapping**:
  - Master: 9333 (HTTP), 19333 (gRPC)
  - Filer: 8888 (HTTP), 18888 (gRPC)
  - S3: 8333 (HTTP)

## 3. Setup & Installation

### 3.1. Deployment

```bash
# SeaweedFS 스택 배포
docker compose up -d
```

### 3.2. Service Stack

| Service | Role | Data Persistence |
| :--- | :--- | :--- |
| `seaweedfs-master` | 메타데이터 및 클러스터 관리 | `seaweedfs-master-data` |
| `seaweedfs-volume` | 실제 데이터 볼륨 저장 | `seaweedfs-volume-data` |
| `seaweedfs-filer` | POSIX/HTTP 파일시스템 인터페이스 | - |
| `seaweedfs-s3` | S3 API 호환 계층 | - |
| `seaweedfs-mount` | 호스트 FUSE 마운트 (`/mnt/seaweedfs`) | - |

## 4. Usage & Integration

### 4.1. Entrypoints

- **Master Console**: `https://seaweedfs.${DEFAULT_URL}`
- **Filer API (CDN)**: `https://cdn.${DEFAULT_URL}`
- **S3 Gateway**: `https://s3.${DEFAULT_URL}`

### 4.2. Local Access

```bash
# 클러스터 상태 확인
curl http://seaweedfs-master:9333/cluster/status
```

## 5. Maintenance & Safety

- **Health Monitoring**: 모든 서비스에 `wget` 기반 헬스체크 구성됨.
- **FUSE Mount Security**: `privileged: true` 및 `SYS_ADMIN` 권한 필요.
- **Volume Management**: 볼륨 파일당 1GB 제한(`volumeSizeLimitMB=1024`).
- **Security**: `config/security.toml`을 통한 인증 및 권한 관리 (필요 시 활성화).

## 6. Known Issues & Troubleshooting

- **Mount Disconnect**: Filer 서비스 재시작 시 `seaweedfs-mount` 컨테이너 재시작이 필요할 수 있음.
- **Replication Lag**: 볼륨 간 복제 설정 시 네트워크 대역폭 확인 필수.

## 7. Canonical References

- **S3 API Compatibility**: [SeaweedFS Wiki](https://github.com/chrislusf/seaweedfs/wiki/S3-API)
- **FUSE Mount Guide**: [SeaweedFS Mount](https://github.com/chrislusf/seaweedfs/wiki/Mount)

## 8. Related Documents

- **Guide**: [../docs/07.guides/04-data/lake-and-object/seaweedfs.md](../../../docs/07.guides/04-data/lake-and-object/seaweedfs.md)
- **Operation**: [../docs/08.operations/04-data/lake-and-object/seaweedfs.md](../../../docs/08.operations/04-data/lake-and-object/seaweedfs.md)
- **Runbook**: [../docs/09.runbooks/04-data/lake-and-object/seaweedfs.md](../../../docs/09.runbooks/04-data/lake-and-object/seaweedfs.md)
