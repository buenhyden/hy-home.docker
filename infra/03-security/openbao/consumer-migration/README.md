---
title: "OpenBao Consumer Migration Contracts"
version: "0.1.14"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-28"
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
- [verify-oidc-client-secret.sh](verify-oidc-client-secret.sh): OIDC client secret 소비자 하나의
  검사입니다. 렌더링 파일, 서비스 파일, Keycloak client secret의 일치를 container 안에서 비교합니다.
- [oidc-client-secrets.sh](oidc-client-secrets.sh): OIDC client secret 일괄 전환의 owner 단계입니다.
  `import <token 파일>`(KV 반입과 metadata 확인), `prepare`(Agent 출력 디렉터리와 읽기 권한
  확인), `cutover <서비스>`·`rollback <서비스>`(`.env`의 경로 변수 한 줄만 바꾸고 그 서비스를
  다시 만든 뒤 검사)를 실행합니다. 값·hash·길이는 출력하지 않습니다.

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

Compose secret은 저장소 `./secrets/` 아래 실제 파일이어야 하므로(변수·절대·symlink 경로 거부)
Grafana는 Compose secret 대신 Agent 출력 디렉터리를 `/run/openbao/observability`에 읽기 전용으로
bind하고 `GF_SECURITY_ADMIN_PASSWORD__FILE`을 `GRAFANA_ADMIN_PASSWORD_FILE`로 고릅니다.
비어 있으면 기존 `/run/secrets/grafana_admin_password`를 씁니다.

1. 선행 조건: Agent는 Grafana 비밀번호 파일만 `0640`(group 1000 읽기)으로 렌더링하고
   `health-agent.sh`도 그 파일에만 `640`을 요구합니다. 이 소스를 반영한 뒤 `openbao-agent`를
   다시 만들고 healthy를 확인합니다.
2. 전환 전 검사: `bash infra/03-security/openbao/consumer-migration/verify-grafana-consumption.sh`
   결과가 모두 `PASS`여야 합니다. 검사는 먼저 Grafana가 healthy가 될 때까지 최대 180초 기다리고(`grafana_healthy`),
   `consumed_file`은 Grafana가 실제로 읽는 파일입니다.
3. 전환: 로컬 `.env`에 `GRAFANA_ADMIN_PASSWORD_FILE=/run/openbao/observability/grafana_admin_password.txt`를
   넣고 `grafana`만 다시 만든 뒤 같은 검사를 실행합니다. `consumed_file`이 Agent 경로여야 합니다.
4. 되돌리기: 그 줄을 지우거나 비우고 `grafana`만 다시 만든 뒤 같은 검사를 실행합니다.

디렉터리 bind이므로 다시 렌더링된 파일도 container 안에 보이지만, Grafana는
`__FILE`을 시작할 때 한 번 읽고 관리자 비밀번호는 DB를 처음 만들 때만 적용합니다.
순서를 지켜야 합니다. `0640` 소스로 Agent를 다시 만들고 healthy를 확인한 뒤에만
변수를 설정합니다. Grafana는 읽지 못한 `__FILE`을 빈 값으로 넘기므로, 새 `grafana-data`
volume이라면 기본 관리자 비밀번호로 계정을 만들 수 있습니다. 검사는 이 경우
`mounted_equals_rendered` 또는 `admin_login`을 `FAIL`로 보고합니다. bootstrap 값이므로 KV 변경만으로
Grafana에 저장된 비밀번호가 바뀌지 않으며, 실제 회전은 별도 단계입니다. 로그인 검사는
시도마다 비상 관리자 계정에 한 번 로그인하므로, `FAIL`이 반복되면 원인을 찾기 전에
반복 실행하지 않습니다.

Agent는 내용이 같은 출력 파일을 다시 쓰지 않으므로 template의 `perms` 변경은 다시 렌더링될 때만
적용됐습니다. 이제 `start-agent.sh`가 시작할 때 `agent.hcl`의 `perms`를 이미 있는 파일에 적용하므로
Agent를 다시 시작하면 반영됩니다. 실행 중인 Agent의 health script는 main checkout에서 바로 읽히므로,
재시작 없이 병합하는 경우에는 병합 직전에 그 파일의 mode를 Agent 사용자(UID 100)로 맞춥니다.

### 두 번째 소비자 Keycloak 전환

Keycloak(UID 1000, group 1000)은 Agent의 `out/auth` 디렉터리를 `/run/openbao/auth`에 읽기 전용으로
bind하고(`create_host_path: false`), entrypoint가 `KEYCLOAK_ADMIN_PASSWORD_FILE`이 가리키는 파일을
읽습니다. 비어 있으면 기존 `/run/secrets/keycloak_admin_password`를 씁니다. DB 비밀번호는 그대로
`./secrets`의 Compose secret입니다. Agent는 `keycloak_admin_password.txt`를 `0640`으로 렌더링하고
`health-agent.sh`는 두 `.txt`에 `640`, `.version`에 `600`을 요구하며 `out/auth`에 그 파일 외의
group-readable 파일이 있으면 실패합니다.

`KC_BOOTSTRAP_ADMIN_PASSWORD`는 master realm에 관리자가 없을 때만 적용됩니다. 파일 경로를
바꿔도 Keycloak에 저장된 실제 관리자 비밀번호는 바뀌지 않습니다. 전환은 값의 출처만 바꾸며,
`admin_login`은 두 값이 같을 때만 통과합니다. 실제 회전은 별도 단계입니다.

1. GitHub 병합 뒤 main checkout을 fast-forward하는 순간 실행 중인 Agent의 health 기준이 바뀝니다.
   먼저 `docker exec openbao-agent find /openbao/out/auth -mindepth 1 -perm -040`이 아무것도
   출력하지 않는지 확인하고, `docker exec -u 100 openbao-agent chmod 0640 /openbao/out/auth/keycloak_admin_password.txt`와
   fast-forward를 연달아 실행한 뒤 Agent가 healthy인지 확인합니다. 되돌릴 때는 main의 병합을
   revert해 health 기준을 되돌린 뒤 `0600`으로 바꿉니다. `0600`만 되돌리면 새 health가 실패합니다.
2. 전환 전 검사: `bash infra/03-security/openbao/consumer-migration/verify-keycloak-consumption.sh`.
   Keycloak healthy를 최대 360초 기다린 뒤 `consumed_file`, `rendered_version`,
   `mounted_equals_rendered`, `admin_login`을 확인합니다. 로그인은 container 안의 `kcadm.sh config credentials`가
   `KC_CLI_PASSWORD` 환경 변수로 받으며 argv에는 비밀번호가 없습니다.
3. 전환: 로컬 `.env`에 `KEYCLOAK_ADMIN_PASSWORD_FILE=/run/openbao/auth/keycloak_admin_password.txt`를 넣고
   `docker compose up -d --no-deps keycloak --dry-run`으로 대상이 `keycloak` 하나인지 확인한 뒤
   다시 만듭니다. 재생성 동안 SSO가 잠시 끊깁니다. 같은 검사에서 `consumed_file`이 Agent 경로여야 합니다.
4. 되돌리기: 변수를 비우고 `keycloak`만 다시 만든 뒤 같은 검사를 실행합니다.

실행 중인 Agent는 다음 재시작 전까지 예전 설정(`0600`)을 메모리에 들고 있습니다. 그동안 Keycloak
KV 값이 바뀌면 파일이 `0600`으로 다시 렌더링되어 Agent health가 실패하고 Keycloak은 읽지 못합니다.
따라서 다음 Agent 재시작 전에는 Keycloak KV를 쓰지 않고, Keycloak을 다시 만들기 전마다 Agent
healthy를 확인합니다. 재시작하면 `start-agent.sh`가 `agent.hcl`의 `0640`을 적용합니다.
변수를 비워도 bind는 남으므로 `out/auth` 디렉터리가 없으면 Keycloak은 만들어지지 않습니다.
파일 group은 Agent의 기본 group(1000)이므로 `SECRETS_GID`가 1000이 아니면 읽을 수 없습니다.

Entrypoint는 파일의 CR·LF를 모두 지우므로 검사도 같은 방식으로 비교합니다. 읽을 수 없거나
빈 파일이면 Keycloak은 시작하지 않습니다. 로그인 거부(`kcadm=invalid`)는 재시도하지 않으므로
반복되면 원인을 찾기 전에 다시 실행하지 않습니다.

### 세 번째 소비자 Grafana OIDC client secret 전환

`grafana_client_secret`은 매 기동마다 읽히는 첫 비-bootstrap 값입니다. Agent는 같은 Grafana KV
경로의 `grafana_client_secret` field를 `out/observability/grafana_client_secret.txt`(`0640`)로
렌더링하고, 같은 경로의 `grafana_admin_password.version`이 version을 대표합니다.
`GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE`은 `GRAFANA_CLIENT_SECRET_FILE`로 고르며 비어 있으면
`/run/secrets/grafana_client_secret`을 씁니다. Grafana는 이미 `out/observability`를 bind합니다.

1. KV 반입(owner, operator 인증): field가 아직 KV에 없습니다. `bao kv metadata get`으로 현재
   version을 확인한 뒤 `./secrets/auth/grafana/grafana_client_secret.txt`를 stdin으로
   `bao kv patch -method=rw secret/hy-home/06-observability/grafana grafana_client_secret=-`에 넣습니다.
   값을 출력하지 않습니다. version이 하나 오르고 Agent가 5분 안에 `.version`을 다시 렌더링합니다.
2. 병합 후 main fast-forward 직후 Agent를 다시 시작합니다(RUN-0103 SecretID 전달).
   새 health는 client secret 파일을 요구하므로 fast-forward와 재시작 사이에는 Agent가 unhealthy입니다.
3. 전환 전 검사: `bash infra/03-security/openbao/consumer-migration/verify-grafana-client-secret.sh`.
   `consumed_file`, `rendered_version`, `mounted_equals_rendered`와 Keycloak이 가진 client secret과의
   일치(`keycloak_client_matches`)를 확인합니다. Keycloak 값은 `kcadm.sh`로 관리자 로그인 한 번에
   읽으며 pipe 안에서만 비교합니다.
4. 전환과 되돌리기: 로컬 `.env`에 `GRAFANA_CLIENT_SECRET_FILE=/run/openbao/observability/grafana_client_secret.txt`를
   넣고 `grafana`만 다시 만든 뒤 검사합니다. 비우고 다시 만들면 되돌아갑니다.

bootstrap 값과 달리 KV를 바꾸면 다음 Grafana 기동부터 새 값이 쓰입니다. Keycloak의 client secret과
함께 바꾸지 않으면 OIDC 로그인이 실패하므로 회전은 두 쪽을 함께 바꾸는 별도 단계입니다.

- 이 KV 경로에는 `kv patch`만 씁니다. `kv put`은 다른 field를 지우고, 빠진 field는 `<no value>`로
  렌더링됩니다. Agent health는 실패하지만 Grafana는 다음 기동에서 그 값을 읽어 OIDC 로그인 전체가
  막힙니다. 그래서 Grafana를 다시 만들기 전마다 Agent healthy와 `keycloak_client_matches`
  PASS를 확인합니다.
- KV 반입 직후 Agent는 다음 렌더링(최대 5분)까지 `.version` 불일치로 unhealthy일 수 있습니다.
  반입은 병합보다 5분 이상 먼저 합니다.
- 코드 되돌리기 순서: Grafana를 `/run/secrets`로 되돌림 → 병합 revert → 남은
  `out/observability/grafana_client_secret.txt` 삭제 → Agent 재시작(SecretID 전달). Agent는 렌더링한
  파일을 지우지 않으므로 삭제 전에는 이전 health가 group-readable 파일 때문에 실패합니다.
- 보호 복구 bundle은 새 template을 포함합니다. 반입 이전 snapshot으로 복구하면 field가 없어 health가
  실패하므로, 이 revision 이후의 복구 계약에는 반입 이후 snapshot이 필요합니다.

### OIDC client secret 일괄 전환(7개)

남은 OIDC client secret 7개를 한 번에 Agent 출력으로 옮깁니다. 소비자마다 KV 경로와 출력
디렉터리가 하나씩이고, Compose 파일은 그 디렉터리만 `/run/openbao/<디렉터리>`에 읽기 전용으로
bind합니다(`create_host_path: false`). 각 `<stem>.txt`는 `0640`, `<stem>.version`은 `0600`입니다.
변수가 비어 있으면 기존 `/run/secrets/<secret>`을 씁니다.

| 서비스 | KV 경로(`secret/hy-home/…`) | 출력 파일 | 경로 변수 |
| --- | --- | --- | --- |
| `oauth2-proxy` | `02-auth/oauth2-proxy` | `oauth2-proxy/oauth2_proxy_client_secret.txt` | `OAUTH2_PROXY_CLIENT_SECRET_FILE` |
| `opensearch-dashboards` | 위와 같음 | 위와 같음 | `OPENSEARCH_OIDC_CLIENT_SECRET_FILE` |
| `kafbat-ui` | `05-messaging/kafbat` | `kafbat/kafbat_client_secret.txt` | `KAFBAT_CLIENT_SECRET_FILE` |
| `dozzle` | `06-observability/dozzle` | `dozzle/dozzle_client_secret.txt` | `DOZZLE_CLIENT_SECRET_FILE` |
| `gatus` | `06-observability/gatus` | `gatus/gatus_oidc_client_secret.txt` | `GATUS_CLIENT_SECRET_FILE` |
| `airflow-apiserver` | `07-workflow/airflow` | `airflow/airflow_client_secret.txt` | `AIRFLOW_CLIENT_SECRET_FILE` |
| `open-webui` | `08-ai/open-webui` | `open-webui/openwebui_oidc_client_secret.txt` | `OPENWEBUI_OIDC_CLIENT_SECRET_FILE` |
| `superset` | `12-analytics/superset` | `superset/superset_oidc_client_secret.txt` | `SUPERSET_OIDC_CLIENT_SECRET_FILE` |

모든 KV field 이름은 `client_secret`입니다. `health-agent.sh`는 이제 `agent.hcl`에서 template
목록을 읽어 각 `.txt`의 bytes와 mode, 각 `.version`과 KV `current_version`을 비교하고, `out` 아래에
목록에 없는 group/other-readable 파일이 있으면 실패합니다.

`renderer`와 `hy-home-operator` 정책이 새 경로를 읽고 쓰려면 root가 필요합니다. 순서는 다음과
같고 1~3단계는 owner가 실행합니다. 정책은 권한을 더하기만 하므로 병합 전에 적용해도 실행 중인
Agent와 소비자에 영향이 없습니다.

1. 정책 적용(RUN-0105 W1 → W1c → W7): RUN-0105의 `owner-window.sh` 단계로 W1 root ceremony,
   이전 root 정리, W1c `roles-plan`·`roles-diff`(`renderer`·`hy-home-operator`의 차이가 새 7개
   경로뿐인지 확인하고 Task에 기록)·`roles-apply`, W7 `revoke-root`를 실행합니다. helper·정책과
   script는 이 PR head에서 manifest로 받습니다(manifest hash가 이 revision에 고정됨).
2. KV 반입(operator 인증): W7 token처럼 W1c 뒤에 받은 operator token 파일로, window의 승인 commit
   (`$P01_COMMIT`) 객체에서 RUN-0085 Reviewed Script Runner의 `p01_run`으로 실행합니다. window의
   `cleanup`은 이 token을 폐기하므로 반입 뒤에 합니다. 경로마다
   `secrets/auth/<서비스>/<파일>`을 stdin으로 넣고 7개 경로의 metadata를 확인합니다. `-cas=0`은
   경로가 이미 있으면 거부하므로 다른 field를 지우지 않습니다. `put FAIL`이면 멈추고
   `kv patch -method=rw`로 바꿉니다. 값을 출력하지 않습니다. token은 window의 `cleanup`이 폐기합니다.

   ```sh
   p01_run "$P01_COMMIT" infra/03-security/openbao/consumer-migration/oidc-client-secrets.sh \
     import "$XDG_RUNTIME_DIR/p01-op-w7.token"
   ```

   병합 전 종료 조건: 7개 경로 모두 `bao kv metadata get`이 성공해야 합니다. 하나라도 빠지면 그
   template이 렌더링되지 않아 3단계 Agent 재시작이 90초 health 조건에서 `BLOCKED`로 끝납니다.
3. 병합 → 출력 디렉터리 생성 → main fast-forward → Agent 재시작(RUN-0103 SecretID 전달).
   - 병합하면 8개 소비자 정의에 새 bind가 생겨 다음 `docker compose up -d`가 변수와 상관없이 모두
     다시 만듭니다. bind는 `create_host_path: false`이므로 디렉터리가 없으면 container를 만들지
     못하고, 기존 container는 이미 지워진 뒤라 그 서비스가 멈춥니다(`oauth2-proxy`면 SSO 전체).
     fast-forward 전에 Agent 사용자로 디렉터리를 만듭니다. health는 디렉터리를 보지 않습니다.
     main checkout에는 아직 script가 없으므로, script를 담은 PR이 병합된 commit의 전체 SHA에서
     `p01_run`으로 읽어 실행합니다. 그 commit에 script가 없으면 실패하고 아무것도 하지 않습니다.

     ```sh
     git -C /home/hyunyoun/data/hy-home.docker fetch origin
     p01_run <병합 commit 40자리> infra/03-security/openbao/consumer-migration/oidc-client-secrets.sh prepare
     ```

   - fast-forward하면 `scripts/`의 새 health가 바로 적용되지만 `agent.hcl`은 단일 파일 bind라 실행 중인
     Agent는 재시작 전까지 예전 5개 template만 검사합니다. 새 health는 `out` 전체에서 목록에 없는
     group/other-readable 파일을 찾으므로, `prepare`가 마지막에 출력하는 읽기 가능 파일이 현재
     `.txt` 3개뿐인지 확인한 뒤 fast-forward합니다.
   - 재시작은 RUN-0103 Renderer SecretID Delivery 3단계의 `owner-window.sh agent-restart`로 합니다.
     끝에 출력되는 Agent health(최대 90초 대기)가 `healthy`이고 7개 디렉터리의 `.txt`가 `0640`, `.version`이 `0600`인지
     확인합니다.
4. 서비스마다 전환 전 검사:
   `bash infra/03-security/openbao/consumer-migration/verify-oidc-client-secret.sh <서비스>`.
   `healthy`, `consumed_file`, `rendered_version`, `mounted_equals_rendered`,
   `keycloak_client_matches`가 모두 `PASS`여야 합니다. 서비스 파일은 `docker cp`로 읽으므로
   shell이 없는 image도 검사합니다. `docker cp`는 daemon 권한으로 읽으므로 `PASS`는 서비스 사용자가
   파일을 읽을 수 있다는 증거가 아닙니다. 전환 뒤 실제 OIDC 로그인으로 확인합니다.
5. 전환: 실행 중인 서비스에만 합니다(멈춘 서비스는 `--no-deps`가 의존 서비스 없이 띄우므로 거부합니다).
   `oidc-client-secrets.sh cutover <서비스>`가 로컬 `.env`에 표의 경로 변수를
   `/run/openbao/<출력 파일>`로 넣고(같은 변수의 기존 줄은 지움) `docker compose up -d --no-deps`로
   그 서비스만 다시 만든 뒤 같은 검사를 실행합니다. `consumed_file`이 Agent 경로여야 합니다. `oauth2-proxy`와
   `opensearch-dashboards`는 같은 파일을 읽지만 변수가 따로이므로 하나씩 전환합니다.
   `opensearch-dashboards`가 `out/oauth2-proxy` 전체를 bind하므로 그 디렉터리와 KV 경로에는
   `client_secret`만 둡니다. cookie secret 등을 더하려면 먼저 디렉터리를 나눕니다.
6. 되돌리기: `oidc-client-secrets.sh rollback <서비스>`가 그 변수 줄을 지우고 그 서비스만 다시
   만든 뒤 검사합니다. `consumed_file`이 `/run/secrets/…`여야 합니다.

실행 중이 아닌 서비스(`kafbat-ui`, `opensearch-dashboards`, `superset`, `airflow-apiserver`)는
다음에 기동할 때 4~5단계를 합니다. 변수를 비워도 bind는 남으므로 Agent 출력 디렉터리가 없으면
그 서비스는 만들어지지 않습니다. Grafana client secret과 같이 KV 값과 Keycloak client를 함께
바꾸지 않으면 OIDC 로그인이 실패하므로 회전은 별도 단계입니다. 코드 되돌리기는 모든 서비스를
`/run/secrets`로 되돌림 → 병합 revert → 멈춘 것을 포함해 8개 서비스를 되돌린 정의로 다시 만듦 →
남은 `out` 디렉터리 7개 삭제 → Agent 재시작 순서입니다. 다시 만들지 않은 container는 예전 bind를
그대로 가지므로 디렉터리를 지운 뒤에는 `docker start`나 재부팅에서 실패합니다.

출력 파일 group은 Agent image의 group(1000)이고 소비자는 `group_add: ${SECRETS_GID:-1000}`으로 읽습니다.
`SECRETS_GID`가 1000이 아니면 8개 소비자 모두 읽지 못합니다. `opensearch-dashboards`와 `kafbat-ui`는
경로를 잘못 주면 빈 값으로 시작하므로 검사의 `mounted_equals_rendered`로 확인합니다.
보호 복구 bundle은 21개 파일을 요구하므로 이 revision의 bundle 영수증과 반입 이후 off-host snapshot이
생기기 전까지 복구 계약은 `BLOCKED`입니다. 복구 값 비교는 아직 두 관리자 비밀번호만 대상입니다.

### `./secrets` 사본 제거 계획

계획만 있고 실행하지 않았습니다. 전환한 소비자도 아직 `./secrets` 파일을 rollback 기본값
(`${변수:-/run/secrets/…}`)과 root `docker-compose.yml`의 `secrets:` 선언으로 참조합니다. P02
catalog에서 확정 lane이 있는 항목은 `gen-secrets`가 `keep-catalog-protected`로 두므로 다시 만들지
않습니다.

선행 조건(값마다):

- 소비자가 Agent 경로로 전환됐고 검사가 `PASS`인 상태가 owner가 정한 관찰 기간 동안 유지됨.
- KV 반입 이후의 snapshot이 off-host에 있고 그 snapshot의 격리 복구가 검증됨. 사본을 지운 뒤에는
  KV snapshot이 유일한 복구 경로입니다.
- 같은 파일을 읽는 다른 소비자가 없음(`oauth2-proxy`·`opensearch-dashboards`는 함께 처리).

값마다의 순서:

1. 소스 PR: 경로 변수 기본값을 Agent 경로로 바꾸고, 서비스의 `secrets:` 항목과 root
   `docker-compose.yml`의 선언을 지웁니다. 선언이 남아 있으면 파일이 없을 때 Compose가 실패합니다.
   Airflow는 공유 `x-airflow-common`의 `secrets:` 목록에서 지웁니다.
   `secret-file-support.json`, Compose secret 계약 시험, `.env.example`, catalog의 목적지 기록을
   함께 고칩니다. `examples/`의 readiness override는 별도 합성 경로이므로 영향이 없는지만 확인합니다.
2. 병합 후 그 서비스만 다시 만들고 검사합니다. 이때부터 rollback은 소스 revert입니다.
3. owner가 파일을 삭제합니다. 되돌릴 수 없는 단계이므로 2단계 검사 결과를 확인한 뒤에만 합니다.

순서: 영향이 작은 `dozzle`·`gatus` → `open-webui`·`kafbat-ui`·`superset`·`airflow-apiserver` →
`oauth2-proxy`(모든 SSO 앞단) → Grafana 두 값 → Keycloak 관리자 비밀번호.

위험:

- 사본이 없으면 Agent가 멈춘 동안 소비자를 다시 만들 수 없습니다. cold boot는 OpenBao 수동 unseal →
  Agent → 소비자 순서가 됩니다.
- Keycloak entrypoint는 파일을 읽지 못하면 시작하지 않고, 사람의 OpenBao 로그인은 Keycloak OIDC를
  거칩니다. Agent 장애와 Keycloak 재생성이 겹치면 break-glass root 절차로만 복구할 수 있으므로,
  Keycloak 관리자 비밀번호 사본은 마지막에 지우거나 off-host custody로 옮기는 별도 결정이 필요합니다.
- DB 비밀번호 등 Agent가 렌더링하지 않는 `./secrets` 파일은 이 계획의 대상이 아닙니다.

## Related Documents

- [OpenBao 구현 안내](../README.md)
- [운영 라이브러리](../../../../scripts/lib/ops/README.md)
- [검증 시험 안내](../../../../tests/validation/README.md)
- [OpenBao KV-v2 CAS·삭제·metadata 공식 계약](https://openbao.org/docs/secrets/kv/kv-v2/)
