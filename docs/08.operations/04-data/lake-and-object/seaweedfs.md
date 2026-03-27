# SeaweedFS Operations Policy

> Governance and operational standards for SeaweedFS distributed storage.

---

## Overview (KR)

이 문서는 SeaweedFS의 안정성을 보장하기 위한 운영 정책과 가이드라인을 정의한다. 데이터 무결성 보호, 성능 모니터링, 백업 및 보안 거버넌스를 아우르며, `hy-home.docker` 데이터 레이어의 오브젝트 및 파일 저장을 담당하는 SeaweedFS의 핵심 운영 기준을 제시한다.

## Policy ID

`OP-DATA-SWFS-001`

## Scope

- Master, Volume, Filer, S3 서비스 관리.
- `/mnt/seaweedfs` 마운트 지점 관리.
- 데이터 레이크 자산의 생명주기 관리.

## Controls & Standards

- **Metadata Sync**: Filer 메타데이터의 영속성을 위해 정기적인 메타데이터 백업을 수행해야 한다.
- **Volume Replication**: 데이터 손실 방지를 위해 최소 `001` (동일 데이터센터 내 2개 복제본) 이상의 복제 레벨을 권장한다.
- **Resource Limits**: 대용량 파일 업로드 시 Filer의 GOMAXPROCS와 메모리 사용량을 모니터링하여 병목 현상을 관리한다.
- **Security**: 내부망(`infra_net`) 외부로의 S3 포트 노출은 최소화하며, 필요 시 `security.toml` 기반의 JWT 인증을 활성화한다.

## Monitoring & Alerting

- **Master Status**: `http://seaweedfs-master:9333/cluster/status`를 통해 가용 볼륨 수와 프리 공간을 모니터링한다.
- **Volume Health**: 개별 볼륨 서버의 응답 지연 시간이 500ms를 초과할 경우 경고를 발생시킨다.
- **FUSE Mount**: 마운트 컨테이너의 CPU 점유율이 지속적으로 높을 경우, I/O 경합이나 네트워크 지연 여부를 점검한다.

## Backup & Lifecycle

- **Volume Backup**: `weed export`를 사용하여 볼륨 데이터를 주기적으로 아카이빙한다.
- **Filer Meta Backup**: LevelDB를 사용하는 경우 컨테이너 볼륨(`seaweedfs-master-data`) 전체를 백업한다.

## Compliance Requirements

- 모든 데이터 접근 로그는 90일간 보관되어야 한다.
- S3 인터페이스를 통한 접근은 HTTPS 전용으로 제한한다.

## Related Documents

- **Guide**: [../docs/07.guides/04-data/lake-and-object/seaweedfs.md](../../../docs/07.guides/04-data/lake-and-object/seaweedfs.md)
- **Runbook**: [../docs/09.runbooks/04-data/lake-and-object/seaweedfs.md](../../../docs/09.runbooks/04-data/lake-and-object/seaweedfs.md)
