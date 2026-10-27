---
title: "OpenBao Consumer Migration Contracts"
version: "0.1.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-27"
created: "2026-10-11"
---

# OpenBao 소비자 이관 공개 계약

## Overview

소비자별 이관을 준비하는 값 없는 공개 계약과 합성 검사 경로입니다. 공개 CLI는
형식과 선택 거부 조건만 검증합니다. 별도 Python API에는 보호 파일과 실제 HTTPS를
사용하는 제한된 KV-v2 복사 실행기가 있습니다. 현재 실제 catalog 승인 연결과
운영 실행 입력은 공급되지 않았으며, 실제 이관·소비·복구·삭제·회전 영수증은 없습니다. 실행 증거와 선행 조건은 [문서 인덱스](../../../../docs/README.md)를
통해 현재 작업에서 확인합니다.

## Audience

이관 계약을 통합하는 개발자와 공개 검사 결과를 확인하는 운영자.

## Scope

공개 wave/receipt 계약은 합성 준비 단계에 한정됩니다. 복사 실행 API는 이 문서를
읽거나 형식 검사를 통과했다고 활성화되지 않습니다. 기존 catalog 소유자가 발급한
실제 항목과 승인된 목적지, 인증·전달·소비·복구 계약 및 현재 신뢰된 운영자 입력의
연결이 실제 실행의 선행 조건입니다.
형식 검사 통과와 입력의 hash 일치는 운영 승인이나 실제 수용 증거가 아닙니다.

## Structure

- [wave.schema.json](wave.schema.json): 한 소비자의 공개 ID 선택과 공개 catalog 입력
  바인딩을 선언합니다. 임의 필드, 중복 ID, wildcard와 비밀값 칸은 거부합니다.
- [receipt.schema.json](receipt.schema.json): 합성 준비 결과만 선언합니다. 상태는
  `inventoried`와 `classified`, KV version은 `null`입니다. native 표시나 실제 복사
  이후 상태는 거부하며, 후속 단계는 소유자가 검토한 별도 계약 확장이 필요합니다.
- [verify-grafana-consumption.sh](verify-grafana-consumption.sh): 첫 소비자 Grafana의
  관리자 비밀번호 소비 검사입니다. Agent가 렌더링한 값과 Grafana에 mount된 값의 일치,
  렌더링 version, 관리자 로그인 HTTP 상태만 출력하고 값·hash·길이는 출력하지 않습니다.

## Tech Stack

기존 Python과 `jsonschema` 검증기를 재사용합니다. 별도 Agent, catalog, 분류기,
workflow 또는 운영 자원을 만들지 않습니다.

## Configuration

`catalog`의 `revision`, `schema_version`, `catalog_sha256`, `schema_sha256`,
`source_sha256`은 공개 catalog·schema·API 소스의 바인딩입니다. 비밀값이나 비밀값에서
계산한 hash를 넣지 않습니다. 호출자가 후보 문서와 별도로 고정한 입력과 대조합니다.

`FrozenAuthority`와 `CatalogSelection`은 합성 시험용 임시 주입 인터페이스입니다.
합성 시험은 P02의 `load_catalog` API로 공개 metadata를 읽어 ID·nullable 목적지·alias·
보존 상태를 그대로 투영합니다. 실행용 catalog adapter는 아직 없습니다.
`APPROVED`는 기존 독립 합성 fixture의 상태이며 실제
catalog의 `BLOCKED_P01` 항목이나 초안 목적지 경로를 승인으로 바꾸지 않습니다.
선택 검사는 alias, 미확인 소비자, 복구용·bootstrap·암호화·미사용·LAB 항목,
안전하지 않은 경로와 중복 목적지를 거부합니다. 원본 파일은 열지 않습니다.

API 호환 시험은 공개 catalog·schema·API 소스 bytes의 hash와 호출자 고정 revision을
wave 입력과 대조합니다. 이 세 hash는 호환성 fingerprint이며 운영 승인 인증이
아닙니다. P02 loader는 추가로 공개 metadata·support matrix와 내부 I/O helper에도
의존합니다. W48 실행 binding은 이 전체 입력과 승인된 대상·ACL·delivery를 묶는
소유자 계약을 기다립니다. COMM-003은 canonical ID로 해석해 복사하지 않으며
PG-020의 초기화·복구 보존 판단을 유지합니다.

`SyntheticKvObservation`과 `decide_synthetic_copy`는 W48 준비용 순수 판단
모델입니다. 입력은 합성 data 상태·metadata 상태·양의 version 또는 `null`뿐입니다.
`equal`이나 `never_created`는 시험이 선언한 상태이며, 함수가 실제 bytes 동일성이나
KV 부재를 확인하지 않습니다. 파일·token·HTTP·catalog 선택에 접근하지 않으며
출력은 고정된 `SyntheticCopyDecision`입니다. 입력과 출력은 변경할 수 없습니다.

| 합성 관찰과 단계 | 판단 | CAS / version |
| --- | --- | --- |
| 쓰기 전 `not_found` + `never_created` + version 없음 | `WOULD_CREATE` | `0` / `null` |
| 쓰기 전 `equal` + `present` + 양의 version | `WOULD_NOOP` | 없음 / 관찰 version |
| 응답 유실·CAS race 후 `equal` + `present` + 양의 version | `RECONCILED_EQUAL` | 없음 / 관찰 version |
| `different` + `present` + 양의 version | `CONFLICT` | 없음 / 관찰 version |
| 그 외 삭제·파기·권한 거부·mount 누락·version 불명·불일치 | `UNRESOLVED` | 없음 / `null` |

응답 유실과 CAS race 뒤에는 부재 선언만으로 생성·재시도 후보를 만들지 않습니다.
404에 대응하는 `not_found`만으로도 신규 생성 후보를 만들 수 없습니다.
위 판단은 운영 승인·명령·이관 영수증이 아니며 기존 receipt schema는 이 상태들을
계속 거부합니다. 실제 transport 복사 primitive의 동작은 아래 Python API에 따릅니다.
P02 catalog의 실제 승인 연결, P01의 실제 token·권한·mount·신뢰·복구 인계와 운영자
실행 adapter는 여전히 필요합니다. 소스 시험 성공은 이 선행 조건의 승인이나
실제 HOME 실행 수용을 대신하지 않습니다.

### Controller-bound copy API

[openbao_consumer_migration.py](../../../../scripts/lib/ops/openbao_consumer_migration.py)의
`execute_copy(CopyPlan, authorize=...)`는 공개 CLI와 분리된 실제 파일/HTTPS 실행 API입니다.
호출하는 controller가 현재 신뢰된 사용자 또는 native 허가 채널을 해석하고 정확한
catalog 전체 입력·revision, 소비자, source/token/CA 파일 경로와 stat metadata,
KV-v2 mount/data 경로, token identity·짧은 비갱신 TTL·최소 권한, 복구 경계 및
P01의 공개 CA hash를 대조해야 합니다. 승인 callback이 literal `True`를 반환해야
private I/O가 시작됩니다. Task, JSON, `FrozenAuthority` 또는 입력의 승인 필드는
인증 수단이 아니며 실제 catalog 항목을 승인 상태로 바꾸는 adapter도 없습니다.

`CopyPlan`은 정확한 HTTPS DNS origin, 별도로 승인된 숫자 IPv4/IPv6 연결 주소,
보호 입력 경로와 UID/GID/mode/size 및 root dev/ino, 연결·읽기·전체 wave 예산을
묶습니다. origin은 길이 1–63의 alnum 양끝·hyphen 내부 DNS label과 전체 hostname
253자 이하를 요구하며 빈 label과 IPv4/IPv6 literal을 거부합니다. 단일 DNS label은
허용합니다. 숫자 연결 주소를 사용하므로 ambient DNS/proxy를 사용하지 않으며, TLS는
origin의 hostname/SAN을 유지하고 보호 CA bytes를 SSLContext에 직접 적재합니다.
모든 경로 요소를 no-follow descriptor로 열고 root/parent/leaf 재결합과 mutation을
검사합니다. source·copy token·metadata token·CA 및 서로 다른 source의 절대 경로
binding이 겹치면 파일을 열기 전에 거부합니다. 실제 held descriptor의 dev/ino도
전부 달라야 하므로 다른 경로나 mount로 동일 inode를 가리켜 역할 경계를 넘는
입력은 HTTP 전에 거부합니다. source/token은 0600/0640, 공개 CA는 승인된 0600/0640/0644만 허용하며
정규 single-link leaf와 exact metadata·bounded snapshot을 요구합니다. source의
UTF-8 roundtrip이 불가능하면 변환 없이 거부하여 최초 복사 bytes를 보존합니다.

복사 token은 선택한 data GET/POST에만 쓰입니다. 별도의 P01 승인 reconciliation
입력 token만 선택한 mount config와 metadata GET에 사용합니다. 두 token이 같으면
거부합니다. token 값은 argv나 반환 결과에 없으며 이 API는 발급·갱신·회전하지
않습니다. 실제 token 권한·TTL·정책 검증은 controller/P01의 선행 인계입니다.

TLS HTTP 응답은 헤더 32 KiB, body 128 KiB, JSON 깊이 12/node 4096으로 제한하며
중복 키·nonfinite 값·버전 불명·redirect를 거부합니다. 연결/읽기 timeout과 전체
wave monotonic 예산 및 socket watchdog이 TLS/header/body 대기를 제한합니다.
전체 예산은 private 입력 준비부터 계산하고 HTTP 전에 검사합니다. kernel 파일 I/O의
고장 격리나 운영자 인증 단계의 시간 제한을 제공한다는 주장은 하지 않습니다.

생성은 data와 metadata가 모두 빈 오류 목록으로 404이고 같은 mount의 KV-v2 config가
정상 검증된 경우에만 CAS=0으로 한 번 요청합니다. 404 하나로 생성하지 않으며
삭제·파기·권한 거부·mount 부재는 unresolved입니다. 기존 bytes와 version이
일치하면 no-op, 다르면 conflict입니다. 응답 유실/CAS race에서는 제한된
metadata/data/metadata readback으로 동일 bytes와 안정된 version을 대조합니다.
POST는 재시도하지 않으며 확인되지 않은 상태는 unresolved로 남깁니다. 결과의
`write_attempted`는 POST 호출을 시도했음을 보수적으로 나타내며 실제 서버 변경의
확인 표시가 아닙니다. `accepted_version`은 검증된 POST 응답의 version이며
`kv_version`은 안정된 readback으로 관찰한 version입니다. 확인되지 않은 version은
각각 `null`로 유지하고 서로 대체하지 않습니다. POST 뒤의 실패·conflict는 실제
변경 여부나 version을 몰라도 PARTIAL입니다. 예를 들어 생성 응답 version1 뒤에
conflict version2를 관찰하면 accepted1과 observed2를 모두 유지합니다. POST 전에
막히고 이전 쓰기도 없으면 BLOCKED입니다. 이후 항목이 실패해도 앞선 항목의
write/version 정보를 보존하고 기존 source 파일을 삭제·덮어쓰지 않습니다. 결과는
public ID·고정 상태·쓰기 시도 표시·두 version뿐이며 비밀값 또는 비밀값에서 계산한
hash가 없습니다. held descriptor를 닫는 정리 단계가 실패해도 이미 완성한 항목의
상태·쓰기 시도·acknowledged/observed version을 유지합니다. 기존 PARTIAL 또는
POST 시도가 있으면 전체 PARTIAL이며, 쓰기 시도 없이 정리만 실패하면 기존 관찰
항목을 남긴 BLOCKED입니다. 진단은 예외 payload 없이 `copy_cleanup_failed`입니다.
실제 운영 영수증 schema 연결은
후속 owner 작업이고 기존 synthetic receipt schema는 계속 runtime 상태를 거부합니다.

내부 구현은 [_openbao_copy_io.py](../../../../scripts/lib/ops/_openbao_copy_io.py)와
[_openbao_copy_transport.py](../../../../scripts/lib/ops/_openbao_copy_transport.py)입니다.
실행용 CLI와 P02 승인 연결이 없으므로 현재 W48은 source primitive까지의 부분 구현이며,
실제 W50 pilot·전달·소비·복구·authority·폐기·회전은 미실행입니다.

## Validation

저장소 루트에서 공개 합성 JSON을 표준 입력으로 전달합니다. 입력은 128 KiB,
깊이 12, node 4096으로 제한하며 표준 입력 대기는 총 5초로 제한합니다.
오류에는 입력 본문·argv·경로·예외 payload를 출력하지 않습니다.

```sh
python3 scripts/operations/openbao-consumer-migration.py --help
```

전용 시험은 `tests/lib/ops/test_openbao_consumer_migration.py`,
`tests/validation/test_openbao_consumer_migration_contract.py`와
`tests/lib/ops/test_openbao_copy_runtime.py`입니다. 마지막 시험은 OpenSSL로 생성한
임시 합성 인증서와 loopback HTTPS 서버로 실제 transport·CAS·file/privacy 실패를
검증합니다. 실제 credential·HOME API나 외부 runtime에는 접속하지 않습니다. 공통 Script
Manifest·QA 등록은 현재 통합 소스를 재사용합니다. 공통 등록과 상위 README의 후속
변경은 단일 통합 작성자가 소유합니다.

## Usage

`validate-wave`와 `validate-receipt`는 공개 형식만 검사합니다. 파일 읽기·KV 복사·삭제·
비밀번호 변경 실행 옵션은 없습니다. 별도 Python API의 실제 사용은 controller의
현재 승인과 정확한 선행 입력을 필요로 합니다. 실제 단계의 계약과 영수증이 없으면 대기하며,
이 합성 결과를 HOME·이관·복구·배포 성공으로 사용하지 않습니다.

### 첫 소비자 Grafana 전환 계획

Agent가 렌더링하는 소비자는 Keycloak과 Grafana 관리자 비밀번호 두 개입니다. 둘 다
아직 저장소 로컬 `./secrets/` 파일을 읽으며 Agent 출력은 소비되지 않습니다. 두 값 모두
최초 기동 때만 적용되는 bootstrap 값입니다. 첫 소비자는 영향 범위가 작은 Grafana입니다.
Grafana는 로그인 화면을 끄고 OIDC를 쓰므로 관리자 비밀번호는 비상 경로에만 쓰입니다.

1. 선행 조건: Agent는 `100:1000` 소유의 `0600` 파일을 렌더링하므로 group 1000을 추가로
   가진 Grafana(UID 472)도 읽을 수 없습니다. P01 소유자가 Grafana 비밀번호 template의
   `perms`만 `0640`으로 바꾸고, `health-agent.sh`에서도 Grafana `.txt` mode 검사만
   `640`으로 맞춘 뒤 Agent를 다시 만듭니다. Keycloak 파일과 `.version` 파일은 `600`으로 둡니다.
2. 전환 전 검사: Agent가 healthy여야 렌더링 값이 KV 값과 같습니다. 그 상태에서
   `bash infra/03-security/openbao/consumer-migration/verify-grafana-consumption.sh`
   결과 세 줄이 모두 `PASS`여야 현재 파일 값이 렌더링 값과 같고 로그인됩니다.
3. 전환: 루트 Compose의 `grafana_admin_password` 파일 경로를 Agent 출력으로 바꾸고
   `grafana`만 다시 만든 뒤 같은 검사를 다시 실행합니다.
4. 되돌리기: 파일 경로를 원래 `./secrets/` 경로로 돌리고 `grafana`만 다시 만든 뒤 같은
   검사를 실행합니다.

Compose 파일 secret은 파일 하나를 bind mount합니다. Agent가 파일을 교체해 다시
렌더링하면 실행 중인 container는 이전 파일을 계속 봅니다. KV 값이 바뀌면 container를
다시 만들 때까지 `mounted_equals_rendered`가 `FAIL`입니다. bootstrap 값이므로 KV 변경만으로
Grafana에 저장된 비밀번호가 바뀌지 않으며, 실제 회전은 별도 단계입니다. 로그인 검사는
시도마다 비상 관리자 계정에 한 번 로그인하므로, `FAIL`이 반복되면 원인을 찾기 전에
반복 실행하지 않습니다.

## Related Documents

- [OpenBao 구현 안내](../README.md)
- [운영 라이브러리](../../../../scripts/lib/ops/README.md)
- [검증 시험 안내](../../../../tests/validation/README.md)
- [OpenBao KV-v2 CAS·삭제·metadata 공식 계약](https://openbao.org/docs/secrets/kv/kv-v2/)
