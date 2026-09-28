---
title: "Mailpit Runbook"
version: "0.2.2"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
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
   인증이나 TLS를 지원하지 않는다. 개수와 synthetic 샘플을 검증한 뒤 현재 데이터를 교체하기
   전에 승인을 받는다.

### Upgrade

1. 위의 export를 완료하고 현재 메시지 개수/database checksum을 기록한다.
2. 릴리스 노트와 database 변경 사항을 검토하고, 소유 변경 내에서 source pin만 갱신한 뒤,
   `mailpit`만 재생성한다.
3. `readyz`, 인증된 UI, synthetic SMTP 캡처 1건, 설정된 보존 기간, 이전 메시지 개수를
   검증한다. 실패 시 새 컨테이너를 중단하고, 데이터 교체 전에 격리된 이전 버전 인스턴스로
   복구한다.

## Evidence

명령 exit, 이미지/source commit, database/export checksum, 메시지 개수, synthetic 식별자,
최종 상태를 기록한다. 수신자, 헤더, 본문, 첨부파일, credential은 절대 기록하지 않는다.

## Rollback or Recovery

backup/restore와 upgrade 리허설은 여기서 **계획됨, 미실행** 상태다. 격리된 restore가
성공하고 구체적 데이터 교체가 승인될 때까지 활성 SQLite database를 덮어쓰지 않는다.

## Escalation

실제 메일 캡처가 의심되거나, database 불일치, 보호된 backup 부재, 알 수 없는 SQLite
sidecar, 외부 노출, 또는 호환되지 않는 upgrade가 있으면 중단한다.

## Traceability

- [Guide](../guides/0084-mailpit.md) (`GDE-0084`)
- [Policy](../policies/0084-mailpit.md) (`POL-0084`)
- [Mailpit Compose](../../../infra/10-communication/mailpit/docker-compose.yml)

## Related Documents

- [Mailpit import/export](https://mailpit.axllent.org/docs/usage/import-export/)
- [Mailpit storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [운영 인덱스](../README.md)
