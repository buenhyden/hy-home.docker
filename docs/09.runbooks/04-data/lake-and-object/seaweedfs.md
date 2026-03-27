# SeaweedFS Recovery Runbook

> Emergency procedures for SeaweedFS cluster restoration and troubleshooting.

---

## Overview (KR)

이 문서는 SeaweedFS 클러스터 내 마스터, 볼륨, 필러 서비스 장애 발생 시의 복구 절차를 설명한다. 데이터 유실을 최소화하고 서비스를 신속하게 정상 상태로 되돌리기 위한 단계별 실행 지침을 제공한다.

## Runbook ID

`RB-DATA-SWFS-001`

## Criticality

`High-Infrastructure`

## Target Audience

- Site Reliability Engineers (SRE)
- System Administrators

## Diagnosis Steps

1. **클러스터 상태 확인**:

   ```bash
   curl http://seaweedfs-master:9333/cluster/status
   ```

2. **볼륨 서버 로그 확인**:

   ```bash
   docker logs seaweedfs-volume
   ```

3. **Filer 연결 상태 점검**:
   - `seaweedfs-filer` 컨테이너 내에서 마스터와의 통신 가능 여부를 확인한다.

## Remediation Procedures

### 1. Master 서버 데이터 손상 시 복구

마스터 서버의 메타데이터가 손상된 경우, 기존 볼륨 서버들을 다시 스캔하여 메타데이터를 재구성해야 할 수 있다.

1. 마스터 컨테이너 중지.
2. `seaweedfs-master-data` 볼륨 복구 또는 초기화.
3. 마스터 서버 시작 후 볼륨 서버들이 자동으로 조인되는지 확인.

### 2. 읽기 전용 모드(Read-Only) 전환 해결

볼륨 서버의 가용 공간이 부족할 경우 읽기 전용으로 전환된다.

1. 부족한 공간 확보 또는 새로운 볼륨 서버 추가 배포.
2. 마스터 서버에서 `volumeSizeLimitMB` 설정 확인 및 조정.

### 3. FUSE 마운트 중단 복구

호스트의 `/mnt/seaweedfs` 접근이 불가능할 경우:

1. `seaweedfs-mount` 컨테이너 재시작.
2. 필요 시 호스트에서 마운트 지점을 강제로 언마운트(`umount -l /mnt/seaweedfs`) 후 컨테이너 재시작.

## Post-Mortem Tasks

- 장애 원인 분석 (디스크 풀, 네트워크 단절 등).
- 향후 동일 장애 방지를 위한 모니터링 임계값 조정.
- 복구 소요 시간(RTO) 기록.

## Related Documents

- **Guide**: [../docs/07.guides/04-data/lake-and-object/seaweedfs.md](../../../docs/07.guides/04-data/lake-and-object/seaweedfs.md)
- **Operation**: [../08.operations/04-data/lake-and-object/seaweedfs.md](../../../docs/08.operations/04-data/lake-and-object/seaweedfs.md)
- **Infra README**: [infra/04-data/lake-and-object/seaweedfs/README.md](../../../infra/04-data/lake-and-object/seaweedfs/README.md)
