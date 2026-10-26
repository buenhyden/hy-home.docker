---
title: "Opsflow SMTP 개발 캡처 노드"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-26"
---

# Opsflow SMTP 개발 캡처 노드

## Overview

native `smtp` credential API로 개발 Mailpit 캡처 설정만 확인하고
`n8n-nodes-opsflow.opsflowSmtp` version 1의 단일 통지를 구현합니다.
상위 workflow의 claim 검사와 별도로 닫힌 claim을 다시 검증합니다.

## Audience

P05 작성자, SEC01·P03·P02 담당자와 독립 검토자입니다.

## Scope

공개 source build와 합성 transport·node API 시험입니다. native import,
설치 이미지 호환성, DB 소비, 실제 SMTP 캡처, 예약·회전·복구는 `NOT_RUN`입니다.

## Structure

- [OpsflowSmtp.node.ts](OpsflowSmtp.node.ts): native credential 조회와 제한된 오류 envelope.
- [transport.ts](transport.ts): 고정 endpoint·envelope·Message-ID·socket 수명.
- [package.json](package.json), [lock](package-lock.json), [tsconfig](tsconfig.json): 재현 build 입력.
- [tests](tests/README.md): 네트워크 없는 합성 시험.

## Tech Stack

선택 upstream n8n commit
`34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7`의
[workflow package](https://github.com/n8n-io/n8n/blob/34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7/packages/workflow/package.json)
API와 동일한 `n8n-workflow` package pin을 개발·peer metadata에 둡니다.
서비스 버전과 package 버전은 서로 다릅니다. 검증된 compiler·Nodemailer pin은
package/lock에만 선언합니다. `npm ci --ignore-scripts`는 dependency lifecycle을 실행하지 않습니다.

개발용 workflow API dependency의 Axios advisory를
[공식 수정 release](https://github.com/axios/axios/releases/tag/v1.20.0)의 <!-- runtime-version-exception: advisory — immutable upstream remediation evidence; package and lock own the dependency pin -->
package-scoped override로 수정합니다. API package 자체를 downgrade하지 않습니다.
이 수정은 설치된 n8n 이미지의 dependency를 바꾸지 않으며 그 수용은 SEC01 담당입니다.

Nodemailer의 주소 parser 보안 수정은 검토된
[공식 수정 release](https://github.com/nodemailer/nodemailer/releases/tag/v10.1.4)의 <!-- runtime-version-exception: advisory — immutable upstream remediation evidence; package and lock own the dependency pin -->
정확한 package/lock pin으로 반영합니다. 고정 발신·수신·envelope와 기존 socket 수명은
유지합니다. 공개 dependency 감사에서 Nodemailer 항목은 제거됐고 production 감사는
0건입니다. 이 패키지의 전체 로컬 감사는 개발용으로 설치된 `n8n-workflow` →
expression runtime → Zod 경로의 단일 advisory와 그 의존성 파생 High 3건으로
여전히 실패합니다. 배포 패키지는 `node_modules`를 포함하지 않지만, `n8n-workflow`는
n8n 호스트가 제공하는 정확한 peer 의존성이기도 합니다. 호스트 peer와 실제 실행 환경에서의
영향·악용 가능성은 미확인입니다. API package downgrade나 Zod major override로
우회하지 않으며, 이 결과는 설치 이미지·실제 송신·전체 보안 수용의 PASS가 아닙니다.

## Configuration

draft P03 대상은 `mailpit:1025`와 합성
`notifier@opsflow.invalid` → `manifest@opsflow.invalid`입니다.
host·port는 정확히 일치해야 하며 native SMTP credential의 user/password는
빈 문자열, secure는 false, disableStartTls는 true, hostName은 빈 문자열 또는
미지정만 허용합니다. COMM-002 등 실제 SMTP credential은 거부합니다.
이 개발 캡처 설정은 생산 SMTP 인증·TLS 수용 증거가 아닙니다.

임의 endpoint·CC/BCC·첨부·파일/URL 읽기·header·Code credential 접근을 제공하지 않습니다.
claim은 native parameter `claim`에 object expression으로 전달하며 문자열 JSON은
받지 않습니다. lease token은 검증에만 쓰며 mail·출력·오류에는 포함하지 않습니다.
실제 credential ID는 공식 UI/API 경로로 관리하는 private import artifact에서만 해결합니다.

연결된 P04 v1 소스는 run_id가 64자리 소문자 hex이고 source는
`hy-home.docker`, `hy-home.k8s`, `Project-Template`, `blog-data` 중 하나이며
row_count는 1~5000입니다. id는 양의 safe integer 또는 PostgreSQL bigint 범위의
정규 십진수 문자열, lease_token은 소문자 UUID입니다. 검토된 SQL hash와
DB CONNECT·schema USAGE와 세 notifier 함수 EXECUTE만 허용하는 권한 소스는
상위 소비자 계약에 연결돼 있습니다. table·column·sequence 직접 접근은 거부합니다. 실제 DB 권한·migration
수용은 `NOT_RUN`이며 이 source 검사만으로 운영 계약을 충족하지 않습니다.

Message-ID는 `<opsflow.RUN@opsflow.invalid>`이며 fresh claim의 token/id가 바뀌어도
같은 run에서 안정적입니다. 출력은 `{run_id,state}`뿐입니다.
정확한 단일 허용 recipient만 accepted이고 rejected가 빈 배열일 때
`accepted_by_smtp`입니다. 나머지 결과와 send/close 실패는 `uncertain`,
send 시작 전 실행 취소만 `cancelled`입니다. send 시작 후 취소는 이미 서버가
받았을 가능성을 보존하여 `uncertain`입니다. SMTP acceptance와 DB ack는 원자적이지 않으므로
중복 가능성을 보존하고 recipient delivery 또는 exactly-once를 주장하지 않습니다.

연결·greeting은 3초, socket은 5초, 전체 send는 15초로 제한합니다.
전체 workflow·DB budget와 lease는 P04·총괄 binding에서 별도 확인합니다.
Nodemailer nonpool `close()`에 socket 취소를 맡기지 않고 `getSocket`에서 생성한
socket을 소유하여 취소·deadline·최종 정리 시 직접 destroy합니다.
[공식 transport 소스](https://github.com/nodemailer/nodemailer/blob/v10.1.4/src/smtp-transport/index.ts)를 <!-- runtime-version-exception: compatibility — immutable upstream protocol evidence; package and lock own the dependency pin -->
기준으로 실제 라이브러리와 in-memory SMTP byte 시험을 수행합니다.

## Validation

이 패키지 디렉터리에서 실행합니다.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run test:coverage
npm audit
npm audit --omit=dev
npm pack --dry-run --ignore-scripts --json
```

coverage gate는 compiled production source의 line·branch·function을 각각 80% 이상
요구합니다. generated `dist/`와 dependency `node_modules/`는 Git에 넣지 않습니다.
선택 이미지의 loader registration·credential binding·동일 main/worker artifact는
native 시험 전 별도로 입증해야 합니다.

## Usage

builder가 비활성 workflow에서 이 node type을 참조합니다. 위 build는 패키지를
생성할 뿐 실행 서비스에 설치하거나 mail을 보내지 않습니다. shared Dockerfile·mount·
Compose 변경은 총괄에 제안하고 최종 endpoint·SQL hash·이미지 인계 이후 통합합니다.

### 서버 lease deadline

닫힌 claim은 기존 다섯 필드와 필수 `lease_until`을 갖습니다. 서버가 UTC
`YYYY-MM-DDTHH:mm:ss.SSSZ`로 투영하며 impossible date와 다른 timezone 형식도 거부합니다.
Transport 생성 전과 send 직전에 SMTP 15초+ack 5초+clock skew 5초보다 남은 시간이
커야 합니다. 시작 전 취소는 cancelled, 시작 후 취소·timeout·수락 응답 유실은 uncertain입니다.
Workflow는 uncertain·ack 유실을 SQL004 unknown으로 격리하며 자동 재전송하지 않습니다.
실제 clock skew/DB timeout과 중단 후 재개는 별도 native acceptance이며 시간 확인만으로
분산 fencing 또는 exactly-once를 보장하지 않습니다.

## Related Documents

- [노드 탐색](../README.md)
- [시험](tests/README.md)
- [상위 workload](../../README.md)
- [native SMTP credential 소스](https://github.com/n8n-io/n8n/blob/34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7/packages/nodes-base/credentials/Smtp.credentials.ts)
- [upstream EmailSend 소스](https://github.com/n8n-io/n8n/blob/34ab9c7bf3d0c6d2ec3422e12e0b970aea5717c7/packages/nodes-base/nodes/EmailSend/v2/send.operation.ts)
