---
title: "Mailpit Runbook"
version: "0.2.2"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0084"
parent_ids:
- "POL-0084"
created: "2026-09-19"
---

# Mailpit Runbook

## When to Use

synthetic mail이 캡처되지 않거나, database가 locked/corrupt 상태거나, 보존 한도가 예상과
다르거나, backup/restore/upgrade가 승인된 경우에 사용한다. 저장소 루트에서 작업하고 캡처된
콘텐츠를 증거로 노출하지 않는다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

1. root 선택과 한정된 런타임 상태를 확인한다.

   ```bash
   docker compose --profile mail-dev config --quiet
   docker compose --profile mail-dev ps mailpit
   docker compose --profile mail-dev logs --tail=200 mailpit
   ```

2. 실패를 구분한다.
   - `readyz` 실패: database 권한/lock과 여유 공간을 점검한다.
   - SMTP 실패: 클라이언트가 `edge_net`의 서비스 DNS나 loopback host port를 사용하는지
     확인한다. host bind는 열지 않는다.
   - UI 실패: Traefik/인증을 SMTP 캡처와 별도로 점검한다.
3. 재시작이 승인되면 Mailpit만 재시작하고 고유한 비민감 식별자를 가진 synthetic 메시지
   1건을 전송한다. 본문을 기록하지 않고 캡처를 검증한다.

### Consistent export and restore

1. 여유 공간이 충분한, Git 외부의 보호된 backup 디렉터리를 선택한다.
2. 실행 중인 인스턴스에서의 live export를 우선한다. 임시 컨테이너 경로에 dump를 생성하고,
   보호된 host 디렉터리로 복사하고, 파일 개수와 checksum을 검증한 뒤, 컨테이너의 임시
   사본을 제거한다. 메시지 파일은 로그에 남기지 않는다.
3. API가 비정상이면 Mailpit을 중단하고 bind-backed 데이터 디렉터리에서 `mailpit.db`와
   SQLite `-wal`/`-shm` sidecar 파일을 복사한다. 복사하는 동안 계속 중단 상태를 유지한다.
4. 격리된 Mailpit 인스턴스/network로 복원한다. export한 메시지는 격리된 local SMTP
   listener에 대해서만 `mailpit ingest`를 사용한다. 업스트림 문서에 따르면 ingest는 SMTP
   인증·TLS 지원 여부는 선택한 버전의 공식 옵션으로 확인해야 한다.
   이 근거와 격리된 listener를 확보하지 못하면 ingest를 실행하지 않는다. 개수와 synthetic 샘플을 검증한 뒤 현재 데이터를 교체하기
   전에 승인을 받는다.

### Upgrade

1. 위의 일관된 export 또는 정지 상태의 DB 캡처를 완료하고 개수·백업 checksum을
   기록한다. 쓰기 중인 SQLite 파일의 checksum만으로 일관성을 증명하지 않는다.
2. 릴리스 노트와 database 변경 사항을 검토하고, 소유 변경 내에서 source pin만 갱신한 뒤,
   `mailpit`만 재생성한다.
3. `readyz`, 인증된 UI, synthetic SMTP 캡처 1건, 설정된 메시지 개수 한도, 이전 메시지 개수를
   검증한다. 실패 시 새 컨테이너를 중단하고, 데이터 교체 전에 격리된 이전 버전 인스턴스로
   복구한다.

### 반출 방식과 업그레이드 사전 검토

현재 선언 버전에 맞는 CLI 옵션·인증 지원을 확인한 경우에만 `mailpit dump`와
`mailpit ingest` 기반 반출·반입을 사용한다. 최신 문서만으로 옵션 호환성을 단정하지 않는다. 활성 SQLite/WAL 파일을 복사하기보다
live HTTP dump를 우선 사용한다. database를 복사해야 한다면 Mailpit을 멈추고
database와 SQLite sidecar를 일관되게 함께 복사한다. 이미지 upgrade 전에는
메시지를 export하고, database checksum을 기록하고, Mailpit만 재생성한 뒤
capture와 메시지 수를 검증한다. restore는 먼저 격리된 Mailpit instance에서
수행한다. 이 절차는 문서로 남겼지만 이 task에서 실행하지는 않았다.

## Evidence

명령 exit, 이미지/source commit, database/export checksum, 메시지 개수, synthetic 식별자,
최종 상태를 기록한다. 수신자, 헤더, 본문, 첨부파일, credential은 절대 기록하지 않는다.

## Rollback or Recovery

backup/restore와 upgrade 리허설은 여기서 **계획됨, 미실행** 상태다. 격리된 restore가
성공하고 구체적 데이터 교체가 승인될 때까지 활성 SQLite database를 덮어쓰지 않는다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

실제 메일 캡처가 의심되거나, database 불일치, 보호된 backup 부재, 알 수 없는 SQLite
sidecar, 외부 노출, 또는 호환되지 않는 upgrade가 있으면 중단한다.

## Traceability

- [Guide](../guides/0084-mailpit.md) (`GDE-0084`)
- [Policy](../policies/0084-mailpit.md) (`POL-0084`)
- [Mailpit Compose](../../../infra/11-quality/mailpit/docker-compose.yml)

## Related Documents

- [Mailpit import/export](https://mailpit.axllent.org/docs/usage/import-export/)
- [Mailpit storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [운영 인덱스](../README.md)
