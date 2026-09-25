---
title: "Offsite Backup Target"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "architecture"
artifact_id: "ADR-0041"
parent_ids:
- "AD-0004"
created: "2026-09-25"
---

# ADR-0041: Offsite Backup Target

## Context

POL-0021 control 1에 따라 Restic과 pgBackRest 저장소는 원본과 다른 물리 디스크에
있다. 그러나 모든 사본이 한 host에 있다.

- `BACKUP_STATE_REPO_DIR`(system SSD): pgBackRest 저장소 `pgbackrest/`
  (`aes-256-cbc`, BKP-001)와 data-disk 상태용 Restic 저장소 `restic/`(BKP-002).
- `BACKUP_HOST_REPO_DIR`(data disk): `secrets/`와 `.env`를 담는 Restic 저장소
  (BKP-002). 이 저장소에는 BKP-001과 SEC-003(OpenBao unseal share 파일)도 들어 있다.

그래서 host 도난, 화재, 침수, 전원 사고, 두 디스크의 동시 손상, 또는 host 전체를 암호화하는
ransomware가 생기면 **모든 사본을 잃는다**. BKP-001/BKP-002의 오프라인 사본(control 3)만
남고 복구할 데이터는 남지 않는다.

측정값(`hyhome-backup.service` journal의 `repository sizes` 줄, 비밀값 없음):

| 날짜 (KST) | state 저장소 (pgBackRest + Restic) | host 저장소 |
| --- | --- | --- |
| 2026-09-23 | 429 MiB | 1 MiB |
| 2026-09-24 | 581 MiB | 1 MiB |
| 2026-09-25 | 777 MiB | 1 MiB |

state 저장소는 `BACKUP_STATE_MAX_GIB` 예산 5 GiB로 묶인다(control 2). 따라서 아래 비용은
**5 GiB 상한** 기준으로 추정한다. pgBackRest는 `repo1-retention-full=2`로 스스로
줄어들지만, Restic은 승인된 `forget-prune` 전까지 계속 늘어난다.

## Decision Drivers

- host를 잃어도 복구할 수 있어야 한다(POL-0021 control 1의 공백).
- 이미 Restic이 client 쪽에서 암호화하므로 원격지는 암호문만 받는다.
  pgBackRest 저장소도 BKP-001로 암호화되어 있다.
- 복구 경로가 OpenBao에 의존하면 안 된다. host를 잃으면 OpenBao도 함께 잃는다.
- 새 자격 증명은 최소로 두고, 오프라인 보관 대상을 늘리지 않는다.
- 운영 부담은 개인 home lab 수준이어야 한다(무인 timer, 수동 절차 최소).
- ransomware나 실수로 원격 사본까지 지워지지 않아야 한다.

## Options Considered

비용은 공개 정가 기준의 **자릿수 추정**이며 결정 시점에 다시 확인한다.

| 옵션 | 월 비용 (≤5 GiB) | host 손실 대비 | 복구 시간 (5 GiB) | 운영 부담 | 새 비밀 |
| --- | --- | --- | --- | --- | --- |
| (a) 둘째 로컬 디스크 / USB 교대 | 디스크 1회 구매 | 같은 장소라 화재·도난에는 약함. 교대 디스크를 집 밖에 두면 부분 대비 | 분 단위 (로컬) | 수동 교대, 잊기 쉬움 | 없음 |
| (b) S3 호환 클라우드 | 거의 0 ~ 약 $7 | 대비함 | 수십 분 이내 (회선 속도) | 무인 timer | 원격 접근 키 1~2개 |
| (c) 다른 기기에 SFTP / rest-server | 상대 기기 비용 | 대비함 (다른 장소일 때) | 상대 회선에 따라 다름 | 상대 기기 유지와 신뢰 필요 | SSH 키 또는 rest-server 계정 |
| (d) 연기 | 0 | 없음 | 해당 없음 | 없음 | 없음 |

### (a) 둘째 로컬 디스크 또는 USB 교대

- **방법**: 외장 디스크에 `restic init --from-repo … --copy-chunker-params`로 저장소를
  만들고 `restic copy`로 두 저장소를 복제한다. pgBackRest 저장소는 디렉터리를 복사하거나
  `repo2-path`로 둘째 저장소를 둔다.
- **Good**: 비용이 가장 낮고 복구가 빠르다. 네트워크와 외부 계정이 필요 없다.
- **Bad**: 연결된 디스크는 같은 host 사고(ransomware, 전원)에 함께 노출된다. 교대 디스크를
  다른 장소에 두지 않으면 화재와 도난을 막지 못한다. 수동 교대는 쉽게 멈춘다.
- **암호화**: Restic과 pgBackRest 암호화가 그대로 적용된다.
- **저장소 변경**: 오케스트레이터에 선택적 copy 단계와 마운트 여부 검사, POL-0021 행 추가.

### (b) S3 호환 클라우드 (Restic 기본 backend)

Compose가 고정한 Restic 버전은 `s3:`, `b2:`, `azure:`, `gs:`, `rest:`, `sftp:` backend를 기본으로 지원한다.
pgBackRest는 `repo2-type=s3`(그리고 `gcs`, `azure`, `sftp`)로 둘째 저장소를 둘 수 있다.

| 제공자 | 저장 단가 (정가) | 5 GiB 월 비용 | 주의점 |
| --- | --- | --- | --- |
| Backblaze B2 | 약 $6~7/TB-월 | 약 $0.03 | 저장량의 3배까지 egress 무료. bucket 범위 application key와 Object Lock 지원 |
| Cloudflare R2 | 약 $0.015/GB-월, 10 GB 무료 | $0 (무료 구간) | egress 무료. bucket 범위 API token |
| Wasabi | 약 $7/TB-월, 최소 1 TB 과금 | 약 $7 | 최소 90일 보관 과금. 작은 저장소에 비쌈 |
| AWS S3 Glacier Instant Retrieval | 약 $0.004/GB-월 + 조회 약 $0.03/GB | 약 $0.02 + 복구 시 조회비 | 최소 90일 과금. Restic `check`/`prune`이 index와 pack을 읽어 조회비가 쌓임. 작은 저장소에는 이득이 적음 |

- **방법**: 원격 Restic 저장소를 state 저장소의 chunker 설정으로 만들고, 로컬 backup과
  `check` 뒤에 `restic copy`로 state와 host snapshot을 올린다. pgBackRest는
  `repo2-type=s3`로 WAL과 backup을 직접 보내거나, 원격 Restic에 pgBackRest 저장소 디렉터리를
  올린다. 전자는 WAL 단위 RPO를 원격에도 유지하지만 `mng-pg` 컨테이너에 원격 키와 egress가
  필요하다. 후자는 일 단위 RPO이고 복사 도중 쓰이는 파일을 조심해야 한다.
- **Good**: 장소가 분리되고 무인으로 돈다. 비용이 거의 없다. Restic이 이미 암호화하므로
  제공자는 암호문만 본다.
- **Bad**: 새 원격 자격 증명과 egress 경로가 생긴다(현재 `restic`은 `network_mode: none`).
  제공자 계정 자체가 새 단일 실패 지점이다. 삭제 권한이 있는 키가 유출되면 원격 사본도
  지워질 수 있으므로 Object Lock 또는 삭제 권한 분리가 필요하다.
- **암호화**: Restic(BKP-002 또는 새 저장소 암호)과 pgBackRest(BKP-001) client 쪽 암호화.
  원격 저장소가 host 저장소를 받으면 모든 `secrets/`가 BKP-002 하나로 보호된 채 외부에
  있게 된다. BKP-002의 오프라인 보관이 그만큼 중요해진다.
- **자격 증명 보관**: `secrets/backup/` 아래 새 파일과 `SENSITIVE_ENV_VARS` 행
  (예: BKP-003 원격 저장소 key ID/application key, pgBackRest `repo2`를 쓰면 BKP-004).
  0600, Docker Secret으로만 주입하고 오프라인 사본을 둔다. **OpenBao에 두지 않는다**:
  host 손실 뒤 복구에 OpenBao가 필요하면 복구가 순환 의존에 빠진다.
- **복구 시간**: 5 GiB를 100 Mbps로 받으면 약 7분. 여기에 Restic restore와 pgBackRest
  restore 시간이 더해진다. B2와 R2는 이 규모의 egress 비용이 사실상 없다.
- **저장소 변경**: egress가 있는 별도 `restic-offsite` job(또는 copy 전용 network),
  오케스트레이터의 copy 단계와 실패 시 exit code, 새 secret 두 개와 registry 행,
  `gen-secrets.sh` metadata, POL-0021 control 1 수정, RUN-0021의 초기화·복구 절차,
  `BackupContractTests` 확장.

### (c) 다른 기기로 SFTP 또는 rest-server (가족, 친구, NAS)

- **방법**: 다른 장소의 기기에 `rest-server --append-only` 또는 SFTP 계정을 두고
  `restic copy`로 보낸다. 연결은 WireGuard 같은 사설 경로가 필요하다.
- **Good**: 월 요금이 없다. `--append-only` rest-server는 이 host가 원격 snapshot을 지울 수
  없게 막는다.
- **Bad**: 상대 기기의 가용성, 디스크, 업데이트, 신뢰에 의존한다. 복구 시 상대가 도와야 할 수
  있다. 네트워크 경로와 포트 개방 또는 VPN을 새로 운영해야 한다.
- **암호화**: Restic client 쪽 암호화이므로 상대는 내용을 읽지 못한다.
- **자격 증명 보관**: SSH 키 또는 rest-server 계정을 `secrets/backup/`와 registry 행에 두고
  오프라인 사본을 둔다.
- **저장소 변경**: (b)와 같은 job과 copy 단계, VPN 또는 SSH 설정.

### (d) 연기

- **Good**: 지금은 할 일이 없다.
- **Bad**: host 손실 시 전부 잃는 상태가 그대로 남는다. SPEC-0182 criterion 10은 연기 시
  owner와 trigger 또는 날짜를 요구한다.

## Decision

**(b) S3 호환 클라우드, Cloudflare R2**를 쓴다(owner 결정, 2026-09-25).

- 원격 Restic 저장소 하나를 R2 bucket에 두고, 로컬 backup과 `check` 뒤에 `restic copy`로
  state와 host snapshot을 올린다. 무료 구간(10 GB)과 무료 egress 안에 5 GiB 상한이 들어간다.
- pgBackRest는 원격 Restic에 저장소 디렉터리를 싣는 방식으로 시작한다(일 단위 원격 RPO,
  `mng-pg`에 egress와 키 없음). 원격에서도 WAL 단위 RPO가 필요해지면 `repo2-type=s3`로
  옮기는 새 결정을 연다.
- bucket에 lock(보존 규칙)을 켜고, 이 host의 token은 해당 bucket 범위로만 준다. 원격
  `forget-prune`은 별도 수동 절차로 둔다.
- R2 자격 증명은 `secrets/backup/`의 파일(0600, Docker Secret 주입)과 오프라인 사본으로만
  보관하고 OpenBao에는 두지 않는다.

## Consequences

- **(b)를 고르면**:
  - POL-0021 control 1이 "offsite recovery is not provided"에서 원격 사본과 그 RPO를
    적는 문장으로 바뀐다.
  - 백업 job 하나가 처음으로 외부 egress를 갖는다. 그 job만 egress network에 붙인다.
  - 새 비밀(BKP-003, 필요 시 BKP-004)의 오프라인 보관과 교체 절차가 생긴다.
  - 원격 사본에는 `secrets/` 전체와 SEC-003이 BKP-002로 암호화되어 들어간다.
    BKP-002가 유출되면 원격 계정 접근만으로 모든 비밀이 노출된다.
  - host 손실 복구 절차(새 host, 오프라인 키, 원격 restore 순서)를 RUN-0021에 추가한다.
- **(a) 또는 (c)를 고르면**: 비용은 낮지만 수동 교대나 상대 기기 유지가 운영 부담이 된다.
- **(d)를 고르면**: 위험을 그대로 받아들이며 trigger가 오면 이 ADR을 다시 연다.

## Traceability

- Parent: [AD-0004 Data Architecture](../descriptions/0004-data-architecture.md)
- Spec: [SPEC-0182](../../03.specs/0182-home-residual-backlog/spec.md) criterion 10, Plan W10,
  [Task 0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
- Policy: [POL-0021](../../05.operations/catalog/04-data/0021-backup-and-restore/policy.md)
  control 1–3; Runbook: [RUN-0021](../../05.operations/catalog/04-data/0021-backup-and-restore/runbook.md)
- Runtime sources: [Restic Compose](../../../infra/09-tooling/restic/docker-compose.yml),
  [orchestrator](../../../infra/09-tooling/restic/bin/hyhome-backup.sh),
  [pgBackRest configuration](../../../infra/04-data/operational/mng-db/pg/backup/pgbackrest.conf)
- 크기 근거: `journalctl -u hyhome-backup.service`의 `repository sizes` 줄(2026-09-23~25).

## Follow-up

- R2 offsite copy를 구현하고 owner가 bucket, token, 첫 `restic init`을 준비한 증거를
  Task 0003에 적는다.
- [ADR-0042](0042-openbao-unseal-method.md)에서 cloud KMS를 고르면 같은 제공자 계정을
  쓸지 함께 정한다.

### Official references

- [Restic repository backends](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
  and [copying snapshots between repositories](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)
- [pgBackRest multiple repositories and S3](https://pgbackrest.org/user-guide.html)
- [rest-server append-only mode](https://github.com/restic/rest-server)
