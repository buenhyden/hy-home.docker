---
title: "독립 매니페스트 outbox 통지"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# 독립 매니페스트 outbox 통지

## Overview

P04의 DEV 매니페스트 게시 outbox에서 한 건을 claim하고 제한된 Mailpit에
캡처하는 n8n 소비자입니다. 현재 산출물은 공개 소스와 합성 시험이며 workflow는
비활성입니다. 실제 import·capture·예약·회전·복구는 NOT_RUN입니다.

## Scope

SQL·migration·DB role·dead requeue는 P04가 단독 소유합니다.
[소비자 계약](outbox-contract.json)은 검토된 P04 SHA를 기다리는 초안입니다.
P04 source SQL의 여섯 claim 필드 중 소비자가 쓰는 다섯 필드만 명시적으로
조회합니다. `lease_until`은 SQL에 남으며 SMTP 입력으로 전달하지 않습니다.
계약의 source hash는 합성 호환성 검사에만 쓰고 native DB·권한·게시 수용은
`NOT_RUN`입니다. 실행 binding은 계속 비어 있습니다.
계약 확정 전 설치하거나 운영 워크플로우로 취급하지 않습니다.

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
받습니다. 선택 root-model overlay는 `n8n-worker`와 Mailpit만 내부
`opsflow_capture_net`에 연결하고 worker를 Stalwart 공유 `mail_net`에 연결하지
않습니다. 기존 n8n 관리·queue network와 Mailpit의 다른 consumer network는
유지됩니다. 이 source topology만으로 실제 peer 거부나 native SMTP capture를
증명하지 않습니다.

## Usage

저장소 루트에서 전용 Python·Node 시험을 실행합니다. 정확한 생성·build 명령은
하위 README에 있습니다. 공개 JSON에는 credential 값·pinData가 없고 성공·오류·수동
실행 데이터 저장을 끕니다. 이 설정은 관리자 접근이나 진행 중 메모리의 비밀값을
격리한다는 뜻이 아닙니다.

정상 수락은 `accepted_by_smtp`이며 외부 배달 증거가 아닙니다. SMTP 수락과 DB ack는
원자적이지 않아 응답 또는 ack 유실 후 중복 전송될 수 있습니다. 같은 run의
Message-ID는 진단을 돕지만 exactly-once를 보장하지 않습니다. ack/retry가 false이면
stale lease로 처리하고 성공으로 보고하지 않습니다. 장애 후에는 전체 workflow에서
새 claim을 받습니다. 오래된 실행의 SMTP node부터 재개하지 않습니다.

dead 복구는 원인·수락/불확실 증거 확인 후 P04의 검토된 함수와 지정 operator role로
해당 건만 requeue하고 새 claim합니다. 직접 table UPDATE나 전체 상태 reset은 금지합니다.
rollback은 이 workflow의 polling 중지·inactive·선택 실행 조정과 outbox 보존입니다.

## Validation

```sh
python -m unittest tests.lib.ops.test_n8n_outbox_workflow \
  tests.validation.test_n8n_outbox_contract \
  tests.validation.test_n8n_outbox_rehearsal -v
```

합성 시험은 실제 DB claim·SMTP capture·native n8n 동작을 증명하지 않습니다.
native 실행은 P04 SQL 검토 SHA와 실제 게시 인계, SEC01의 설치 이미지·node 호환성,
P02 credential 분류, P03 endpoint·실행 worker·접근 경계가 확정된 뒤 진행합니다.
먼저 inactive import와 manual capture를 확인하고 이후 1분 polling 하나만 활성화합니다.
두 notifier 경쟁·lease 만료·outage·응답/ack 유실·dead·restart·공식 credential 회전과
빈 격리 대상에 metadata DB와 동일 encryption key를 함께 복원하는 시험이 남아 있습니다.
각 운영 작업의 정확한 대상·효과·backup·cleanup·rollback은 Task에 먼저 기록합니다.

## Related Documents

- [워크로드 목록](../README.md)
- [Spec Package 탐색](../../../../../docs/03.specs/README.md): P05 정본은 SPEC-0204-TSK-0013, P04 정본은 SPEC-0204-TSK-0012입니다.
