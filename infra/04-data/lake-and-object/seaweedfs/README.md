<!-- [ID:04-data:seaweedfs] -->
# SeaweedFS

> High-performance distributed file system and object storage for tiered data lake architectures.

---

## 1. Context & Objective (KR)

SeaweedFS는 빌리언 단위의 파일을 저장하고 제공하기 위해 설계된 초고성능 분산 스토리지 시스템이다. `hy-home.docker` 환경에서 비정형 데이터, 미디어 콘텐츠 및 대규모 로그를 위한 확장 가능하고 탄력적인 저장 계층을 제공하며, Filer(파일시스템)와 S3 인터페이스를 동시에 지원한다.

## 2. Requirements & Constraints

- **Architecture**: Master-Volume-Filer 계층 구조
- **Engine**: Chrislusf SeaweedFS (v4.05)
- **Resource Templates**:
  - Master/Filer: `template-stateful-med`
  - Volume: `template-stateful-high` (I/O 집중형)
- **Networking**: `infra_net` 격리 네트워크 사용 및 `DEFAULT_URL` 기반 도메인 구성
- **Constraints**: 볼륨 파일당 1GB 제한(`volumeSizeLimitMB=1024`)

## 3. Setup & Installation

### 3.1. Full Stack Deployment

```bash
# SeaweedFS 전체 스택(Master, Volume, Filer, S3, Mount) 배포
docker compose up -d
```

### 3.2. Verification

```bash
# 클러스터 상태 및 볼륨 조인 확인
curl http://seaweedfs-master:9333/cluster/status
```

## 4. Usage & Integration

### 4.1. Access Endpoints

- **Master UI**: `https://seaweedfs.${DEFAULT_URL}`
- **Filer API/CDN**: `https://cdn.${DEFAULT_URL}`
- **S3 Gateway**: `https://s3.${DEFAULT_URL}`

### 4.2. Storage Interfaces

- **S3 Compatible**: `mc` 툴 또는 S3 SDK를 통한 오브젝트 저장.
- **Filer API**: `curl`을 통한 다이렉트 파일 업로드/다운로드.
- **FUSE Mount**: 호스트 경로 `/mnt/seaweedfs`를 통한 로컬 FS 연동.

## 5. Maintenance & Safety (Maintenance & Safety)

- **Health Checks**: `wget` 기반 헬스체크가 모든 서비스에 구성되어 배포 안정성을 유지한다.
- **FUSE Mount Stability**: Filer 재시작 시 `seaweedfs-mount` 컨테이너의 재시작이 필요할 수 있으므로 의존성 순서를 준수한다.
- **Security Control**: `config/security.toml`을 통해 gRPC 및 API 인증을 활성화할 수 있다 (현재는 내부망 중심 격리).

## 6. Known Issues & Troubleshooting

- **Replication Lag**: 복제 모드 활성화 시 볼륨 서버 간 네트워크 대역폭 부족이 발생하면 쓰기 지연이 나타날 수 있다.
- **Metadata Persistence**: 기본 설정은 Filer 내장 LevelDB를 사용한다. 대규모 운영 시에는 외부 정합성 DB로의 전환을 권장한다.

## 7. Canonical References

- **Official Wiki**: [https://github.com/chrislusf/seaweedfs/wiki](https://github.com/chrislusf/seaweedfs/wiki)
- **S3 API Compatibility**: [SeaweedFS S3-API](https://github.com/chrislusf/seaweedfs/wiki/S3-API)
- **FUSE Mount Guide**: [SeaweedFS Mount](https://github.com/chrislusf/seaweedfs/wiki/Mount)

## 8. Related Documents

- **Guide**: [Technical Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md)
- **Operation**: [Operations Policy](../../../../docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md)
- **Runbook**: [Recovery Runbook](../../../../docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md)

---
Copyright (c) 2026. Licensed under the MIT License.

---

## Overview

`infra/04-data/lake-and-object/seaweedfs`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/04-data/lake-and-object/seaweedfs/
├── config/  # 하위 구성 영역
├── docker-compose.yml  # Docker Compose 정의
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify volume server health by checking `docker logs seaweedfs | grep -i 'error\|warn'` and confirming master/volume/filer status via the SeaweedFS UI.
- Confirm S3 API compatibility by testing a PUT/GET operation against the filer's S3 endpoint.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For volume server errors: verify master address configuration and confirm volume servers can register with the master.
- For filer errors: check filer metadata store connectivity and confirm the filer config references the correct master address.
- For S3 API errors: verify the filer's S3 gateway is enabled and credentials match the client configuration.

## Related Documents

- [infra/README.md](../../../README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
