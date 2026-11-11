---
title: "독립 매니페스트 outbox 통지"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-11"
---

# 독립 매니페스트 outbox 통지

## Overview

DEV 매니페스트 게시 outbox에서 한 건을 claim하고 제한된 Mailpit에 캡처하는
n8n 소비자입니다. 공개 workflow는 비활성을 유지합니다. SPEC-0204의 C19/C22는
선택 이미지와 당시 격리 queue·수동/예약·불확실 전송·복원 범위에서 수용됐습니다.
이전 readiness 실패도 이력으로 보존하며 이후 수용을 취소하는 근거로 쓰지 않습니다.
현재 P05의 수동 재처리·복원 장벽·인증 STARTTLS 보완은 별도
SPEC-0212 Task0044(`docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0044-opsflow-notifier-recovery.md`)가 기록합니다.
과거 수용은 현재 이미지·사설 workflow·HOME 운영의 독립 PASS가 아닙니다.

## Scope

기존 게시 SQL·데이터 소유권은 P04 계약을 재사용합니다. 현재 P05의 신규 SQL007/008은
지정 SQL 작성자가 통합하며 발급된001–006은 보존합니다.
[소비자 계약](outbox-contract.json)은 P04 Task의 독립 SQL·보안 검토와 일치하는
v1 commit·migration hash를 연결합니다. `reviewed`는 이 소스 인터페이스의 상태입니다.
P04 source SQL의 여섯 claim 필드를 조회하며 `lease_until`은 서버에서 UTC millisecond
문자열로 고정합니다. SMTP 입력 경계에서 형식·만료·남은 시간을 확인하지만 메일에는
lease capability나 deadline을 넣지 않습니다. SQL004의 새 안전 계약은 Task0018이 소유합니다.
계약의 source hash는 소스 호환성 검사에만 쓰고 native DB·권한·게시 수용은
`NOT_RUN`입니다. 실제 실행 대상·credential·DB timeout은 계속 미확정입니다.
native 인계 전 설치하거나 운영 워크플로우로 취급하지 않습니다.

## Structure

- [tools](tools/README.md): import 시 파일을 쓰지 않는 결정적 생성기입니다.
- [workflows](workflows/README.md): 생성된 비활성 JSON입니다.
- [fixtures](fixtures/README.md): 입력·실패·개인정보 경계의 합성 사례입니다.
- [nodes](nodes/README.md): 이 소비자만 허용하는 SMTP node입니다.

## Configuration

공개 JSON의 credential ID는 placeholder입니다. 운영자가 확인한 공식 n8n
UI/API 경로로 private import 사본에 연결하며, 값이나 lease token을 Git·출력에
남기지 않습니다. n8n encryption key로 보호한 native credential은 실행 사본이며
환경 파일 변경으로 자동 갱신되지 않습니다. 외부 secret-store의 에디션·provider
지원은 [공식 문서](https://docs.n8n.io/external-secrets/)와 설치 이미지에서 확인합니다.

main과 worker는 같은 custom node artifact와 encryption key를 사용해야 합니다.
공통 custom bind가 이미지 설치를 가릴 수 있으므로 실제 등록을 검증해야 합니다.
[queue mode](https://docs.n8n.io/hosting/scaling/queue-mode/)의 선언과 실제 manual·예약
executor 배치는 별도 증거입니다. P03이 확정한 executor만 DEV와 capture 접근권한을
받습니다. base Compose(`n8n`·`mailpit`·`dev-db` 조각과 루트 선언)는 `n8n-worker`와 Mailpit만 내부
`opsflow_capture_net`에, `n8n-worker`와 dev-pg만 내부 `opsflow_notifier_db_net`에 연결하고
worker를 Stalwart 공유 `mail_net`과 `dev_data_net`에 연결하지 않습니다. Mailpit UI/API(8025)는
`opsflow_capture_net`으로 worker에서 닿으며, capture 전용이고 외부 전달이 없는 수용된 잔여 위험입니다. 기존 n8n 관리·queue network와 Mailpit의 다른 consumer network는
유지됩니다. 이 source topology만으로 실제 peer 거부나 native SMTP capture를
증명하지 않습니다.

## Usage

저장소 루트에서 전용 Python·Node 시험을 실행합니다. 정확한 생성·build 명령은
하위 README에 있습니다. 공개 JSON에는 credential 값·pinData가 없고 성공·오류·수동
실행 데이터 저장을 끕니다. 이 설정은 관리자 접근이나 진행 중 메모리의 비밀값을
격리한다는 뜻이 아닙니다.

정상 수락은 `accepted_by_smtp`이며 외부 배달 증거가 아닙니다. SMTP 수락과 DB ack는
원자적이지 않아 응답 또는 ack 유실 후 중복 전송될 수 있습니다. 같은 run의
Message-ID는 진단을 돕지만 exactly-once를 보장하지 않습니다. ack 유실·SMTP 응답 유실·node 오류는 unknown으로 격리하며 자동으로 다시 보내지 않습니다.
SQL004의 legacy retry도 격리하므로 구버전 workflow가 불확실 전송을 자동 재시도하지 않습니다.
실제 SMTP 시작 전 취소만 새 no-send retry 함수로 제한합니다. 기록이 실패하면 불확실한
sending을 유지하고 만료 뒤 격리합니다. 오래된 SMTP node에서 재개하지 않습니다.

dead 복구는 SQL007의 `requeue_dead_notification(id,attempt,request_id,evidence_sha256)`만
사용합니다. 현재 attempt의 no-send 증거와 개별 승인마다 한 번의 추가 claim을 허용하고
기존 attempt·대조·감사 이력을 보존합니다. 같은 요청의 재호출은 허용량을 늘리지 않습니다.
직접 table UPDATE나 전체 상태 reset은 금지합니다. 관리 함수는 migrator session에서
명시적으로 `SET ROLE opsflow_owner`한 context로 호출하며 runtime notifier에는 권한이 없습니다. 정확한 권한·오류·적용 순서는
[SQL 계약](../../../airflow/workloads/manifest-pipeline/sql/README.md)을 따릅니다.

복원 전 입력·polling을 중지하고 전송 가능한 실행·worker·socket을 drain/종료한 증거를
확보합니다. 복원된 sending은 lease가 남아 있어도
`quarantine_restored_notification`으로 unknown에 격리한 뒤 재개합니다.
함수는 외부 장벽의 증거 지문을 기록할 뿐 SMTP fencing이나 미전송을 증명하지 않습니다.
SMTP capture 부재만으로 no-send를 판단하지 않습니다. rollback은 이 workflow의 polling
중지·inactive·선택 실행 조정과 outbox·audit 보존이며 실제 schema 복구와 구분합니다.

### Lease와 대조 조건

Transport 생성 전과 send 직전에 SMTP 15초·ack 5초·시계 오차 5초를 합한 25초보다
많은 lease가 남아야 합니다. 누락·비정상·만료·시간 부족은 전송 전에 취소합니다.
DB와 worker의 실제 시계 오차가 5초 이내이고 DB timeout/cancellation이 ack 예산에
맞는지 native로 검증하기 전에는 활성화하지 않습니다. 이 시간 검사는 분산 fencing이나
exactly-once 보장이 아닙니다. Unknown은 SQL owner의 capture/증거 대조 후에만 해제하며,
정확한 함수·권한·독립 복원 조건은 P04 SQL README를 따릅니다.

## Validation

합성 시험과 owned loopback STARTTLS 시험은 실제 n8n Worker·DB·Mailpit native 실행과
구분합니다. 신규 실행 결과·독립 검토·실행 환경·잔여는 Task0044에 기록하며,
SPEC-0204의 C19/C22 수용은 당시 version·환경·Criterion 범위로 재사용합니다.
P04의 현재 Worker/독립 복원 잔여가 P05 독립 fixture의 숨은 시작 조건은 아닙니다.
실제 Airflow가 게시한 같은 outbox를 n8n에 인계하는 P12 종단 수용은 별도입니다.

기존 native 실행 명령·직렬 lock·자원·capture·cleanup 조건은 RUN-0053을 따릅니다.
새 인증 profile은 명시적 선택이며 실제 비밀 발급·운영 회전·외부 송신을 허용하지 않습니다.
metadata DB와 같은 encryption key의 일관된 복원, 진행 중 전송의 장벽, accepted/unknown
상태와 다음 claim 결과를 각각 대조합니다. SQL-only dump/restore를 전체 서비스 복원으로
승격하지 않습니다. 실행하지 않은 운영·원격 CI·최종 P12 인수는 NOT_RUN입니다.

## Related Documents

- [워크로드 목록](../README.md)
- [Spec Package 탐색](../../../../../docs/03.specs/README.md): 과거 수용은 SPEC-0204-TSK-0013, 현재 P05 보완은 SPEC-0212-TSK-0044가 소유합니다.
