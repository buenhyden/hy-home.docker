---
title: "k6 성능 시험 인프라"
version: "1.4.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-03-26"
---

<!-- [ID:11-quality:k6] -->
# k6 성능 시험 인프라

> `hy-home.docker`의 k6 실행 전 검증과 결과 증거 계약입니다.

## Overview

이 패키지는 k6 manifest 검증, 격리 실행 argv 준비, fail-closed 중단 증거, 결과 확정과 적재 봉투 생성을 제공합니다. 승인 path proxy가 없어 실제 트래픽 실행은 차단되어 있습니다.

> [!NOTE]
> **구현 정보**: 이 디렉터리(`infra/11-quality/k6`)는 `testing` 프로필이 선택하는 단일 `k6` 서비스를 소유합니다. 분산 master-worker 실습은 별도 LAB의 Locust가 담당합니다.

## Audience

- 부하 시험을 설계하고 판정하는 QA 담당자
- 용량과 장애 영향을 검토하는 운영 담당자
- 외부 프로젝트의 시나리오와 임계값을 관리하는 개발자

## Scope

### In Scope

- **inventory job**: `testing` 프로필에서 image version만 확인하는 no-traffic 작업.
- **실행 전 계약**: versioned manifest, target·redirect·budget, Docker network와
  WireMock peer 검증, 제한된 argv 준비.
- **중단 증거**: path confinement가 없을 때 container를 시작하지 않고
  interrupted evidence 생성.
- **결과 계약**: 불변 summary·exit·checksum·final, perf_db 적재 봉투와 receipt.

### Out of Scope

- **실제 부하**: 승인 path만 전달하는 HTTP proxy와 격리 runtime 인수 전까지
  `BLOCKED`.
- **실시간 지표**: Prometheus remote write 연결은 현재 executor에 없으며
  `BLOCKED`.
- **시각화**: Grafana 대시보드 자체의 소유는 `06-observability`에 있음.
- **업무 판정 변경**: 공식 판정 변경은 `perf_db` verdict 권한이 소유.

## Structure

```text
k6/
├── Dockerfile          # 고정된 grafana/k6 이미지
├── docker-compose.yml  # 부하 시험 작업 정의
├── quality_run.py      # 실행 전 검증, 격리 실행, 확정, 적재 봉투 CLI
├── container_executor.py # 전용 Docker network와 자원 제한 실행기
├── result_import.py    # perf_db 적재와 receipt 계약
├── result_inspection.py # summary/exit 안전성 검사
└── README.md           # 이 문서
```

시나리오 스크립트는 저장소가 아니라 `DEFAULT_TOOLING_DIR/k6`의 읽기 전용
bind mount에 둡니다. 결과는 `DEFAULT_TOOLING_DIR/k6-results`에서 실행별 새
디렉터리를 사용합니다. 기존 디렉터리를 재사용하거나 결과를 덮어쓰지 않습니다.

## Tech Stack

- k6 실행 이미지는 [Dockerfile](Dockerfile)이 소유합니다.
- 결과 계약 CLI는 Python 표준 라이브러리만 사용합니다.
- 종료 후 계약은 `perf_db` importer로 전달합니다. 실시간 Prometheus remote
  write는 승인된 격리 adapter가 없어 현재 구성에서 제거했습니다.

## Available Scripts

| 명령                                                       | 설명                             |
| ---------------------------------------------------------- | -------------------------------- |
| `bash scripts/hardening/check-all-hardening.sh 11-quality` | 정적 hardening 계약 검사 |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | 문서 및 오래된 리터럴 가드 |
| `docker compose ... logs -f k6` | 승인된 runtime context에서 실행 로그 확인 |
| `python3 infra/11-quality/k6/quality_run.py --help` | 결과 계약 단계와 인자 확인 |

## Configuration

### Environment Variables

| 변수 | 필수 | 설명 |
| --- | --- | --- |
| `DEFAULT_TOOLING_DIR` | Yes | 스크립트와 결과 볼륨의 호스트 경로 |

### 실행 manifest

`hyhome.quality-run/v1` manifest는 `run_id` UUID, 양의 `attempt`,
`project_id`, 환경, source revision, digest로 고정한 tool image, 시나리오
SHA-256, mock mode, 정확한 target origin, private CIDR, 요청 경로, 임계값과
부하·자원 예산을 모두 요구합니다. 알 수 없는 필드와 중복 JSON key를 거부합니다.

v1은 리다이렉트를 모두 거부하며 준비된 k6 argv에도
`--max-redirects 0`을 둡니다. 공개 origin, URL 자격 증명·query, 관리 경로,
넓거나 허용 범위 밖인 CIDR, 범위를 벗어난 예산을 거부합니다. executor는 host
DNS를 신뢰하지 않고 Docker network inspect의 subnet과 단일 WireMock endpoint를
manifest CIDR과 대조합니다.

### 결과 단계

1. `prepare`는 manifest와 시나리오 해시를 검증하고 비어 있는 새 attempt
   디렉터리에 `manifest.json`을 배타적으로 생성합니다.
2. `run`은 사전 준비된 internal Docker network와 WireMock peer를
   검사하고 scenario snapshot, 빈 summary file, digest image와 CPU·메모리·PID
   제한이 있는 Docker argv를 준비합니다. 현재 승인 path만 통과시키는 HTTP
   proxy가 없으므로 container를 시작하지 않고 `path_confinement_unavailable`
   interrupted 증거를 남깁니다.
3. `finalize`는 sample 수, 선언한 threshold, 종료 상태를 분리해
   `checksums.json`과 `final.json`을 만듭니다. 0 sample, 잘린 JSON,
   NaN/Infinity, 중단 또는 일부 결과는 통과 판정이 될 수 없습니다.
4. `prepare-import`는 checksum을 다시 확인하고 `hyhome.quality-import/v1`
   봉투를 배타적으로 생성합니다. 같은 identity와 같은 payload의 재실행만
   멱등이며 다른 byte는 충돌입니다.
5. `import-db`는 별도 프로세스에서 표준 `PG*` 접속 환경과 `psql`을 사용해
   `quality.import_payload(jsonb, bytea)` 한 문장만 호출합니다. 두 번째 인자는
   `payload_sha256`을 제외한 canonical byte여서 DB가 payload hash를 다시
   검증합니다. DB 장애는 새 receipt에
   `failed`로 기록하고 원본을 유지합니다. k6 자식 프로세스에는 PostgreSQL과
   S3 접속 환경을 전달하지 않습니다.

```bash
python3 infra/11-quality/k6/quality_run.py run \
  --manifest /approved/run.json \
  --scenario-root "${DEFAULT_TOOLING_DIR}/k6" \
  --attempt-dir "${DEFAULT_TOOLING_DIR}/k6-results/<run-id>-<attempt>" \
  --docker-context <approved-context> \
  --network <dedicated-internal-network> \
  --wiremock-container <approved-wiremock-container>
```

`run`은 명시한 Docker context에서 다음 조건을 모두 확인한 경우에만
실행됩니다. network는 `Internal=true`, local bridge, attachable=false이며
manifest run_id와 `k6-wiremock` purpose label, manifest와 정확히 같은 subnet을
가져야 합니다. 실행 전 peer는 하나뿐이어야 하며 WireMock container는 같은
run_id, role, mock_mode label, `wiremock` alias, 비공개 HTTP 8080만, 단일
network와 `--admin-api-require-https` command를 가져야 합니다. HTTPS port가
없어 WireMock admin HTTP 요청은 403이어야 합니다. 현재 root Compose는 이 network를 만들지 않으며 `version`만
실행하는 inventory/render job이므로 실제 실행은 계속 `BLOCKED`입니다. 자동
할당 CIDR을 승인된 값으로 추정하지 않습니다.

manifest의 `tool_image`는 `--pull never` Docker argv에 digest
reference로 들어가며, `fixture_sha256`을 다시 확인한 scenario snapshot만
read-only mount 후보가 됩니다. 현재 fail-closed 경계에서는 이 argv를 실행하지
않으므로 이를 runtime 증거로 보고하지 않습니다.

`run`은 승인 origin을 `HYHOME_TARGET_ORIGIN`으로만 전달할
argv를 준비합니다. WireMock admin HTTP는 HTTPS 요구 조건으로 차단하지만 임의 JavaScript가
manifest 밖의 path로 요청해 404를 만드는 행위까지 Docker network만으로 막을
수 없습니다. 승인 path를
강제하는 HTTP proxy와 그 회귀 검사가 추가될 때까지 실행은 `BLOCKED`입니다.
CPU·메모리·PID와 보안 옵션도 준비된 argv에서만 검증됐으며 실제 적용은
`NOT_RUN`입니다.

finalizer는 raw summary의 key와 문자열에서 URL, IP, Authorization, cookie와 query
형태를 검사합니다. 검출한 run은 `incomplete`이며 metric을 importer로 넘기지
않습니다. 해당 raw 파일은 로컬 attempt 디렉터리에서 `0440` 격리 증거로만
남고 `prepare-import`가 전체 run을 거부하므로 DB나 객체 저장소로 내보낼 수
없습니다. k6 system tag 제한은 사용자 JavaScript가 만드는 custom tag까지 막지
못합니다. 정적 검사는 PII 의미를 판별할 수 없으므로 외부 프로젝트가 scenario와
custom metric 이름을 검토할 책임은 남습니다.

격리 executor는 단일 WireMock peer 조건 때문에 Prometheus remote write를
사용하지 않습니다. 소비자가 없는 기존 Compose remote-write 환경 선언도
제거했습니다. 따라서 격리 실행의 실시간 dashboard 지표는 아직 `BLOCKED`이며
종료 후 perf_db 적재만 source 계약이 있습니다.

### 객체 보관 경계

현재 저장소에는 SeaweedFS bucket 준비 작업이 사용하는 AWS CLI 이미지가 있지만
관리자 identity 전용입니다. 품질 결과용 bucket/prefix와 제한된 writer identity가
승인되지 않았고 host에는 `aws`, `mc`, `rclone` CLI가 확인되지 않았습니다. 따라서
이번 source 계약의 `object_ref`는 `null`이며 multipart upload, 부분 실패 재개,
다운로드 checksum 대조는 `BLOCKED`입니다. 관리자 secret을 runner나 importer에
재사용하지 않습니다. 승인된 bucket과 전용 identity가 마련되면 AWS CLI의
multipart 계약과 합성 중단·재개 검사를 별도 작업으로 추가해야 합니다.

## Validation

- k6에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 11-quality`을 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.
- 루트 파일이 이 leaf를 무조건 include하고 `testing` 프로필이 해당 서비스의 해석 여부를 결정하므로, 런타임 렌더링에는 루트 네트워크 컨텍스트가 필요합니다.
- `python3 -m unittest tests.validation.test_k6_results -v`로 manifest,
  threshold/exit, 0 sample, 잘린/비정상 숫자, 중단, replay 충돌 계약을 검사합니다.

## Troubleshooting

- k6 네트워크, 볼륨, 지표 싱크 참조가 계속 선언되어 있는지 hardening 점검으로 먼저 확인합니다.
- 테스트 스크립트나 지표 대상을 변경하기 전에 k6 실행 출력과 연결된 런북을 확인합니다.

## Related Documents

- **Guide**: k6 Performance Testing Guide (`docs/05.operations/guides/0061-k6.md`)
- **Policy**: k6 operations policy (`docs/05.operations/policies/0061-k6.md`)
- **Runbook**: k6 recovery runbook (`docs/05.operations/runbooks/0061-k6.md`)
- [Documentation index](../../../docs/README.md)

## Service Readiness

| 항목 | 근거 |
| --- | --- |
| Purpose | `11-quality`의 k6 Performance Testing Infrastructure 서비스 leaf; 서비스: `k6`; 루트 [docker-compose.yml](../../../docker-compose.yml)이 이 leaf의 `docker-compose.yml`을 무조건 include함 |
| Config files | `Dockerfile`, `docker-compose.yml` |
| Config values | 프로필: `testing`; host script bind: `DEFAULT_TOOLING_DIR` |
| Compose linkage | 루트 include 활성; `testing` 프로필이 `k6`를 선택함 |
| Networks | `obs_net` |
| Volumes | root inventory job은 `k6-data:/scripts:ro`; 격리 executor가 승인된 scenario file(ro)과 summary file(rw)을 직접 mount |
| Ports | 선언되지 않음; k6는 CLI로 구동되며 호스트 포트를 게시하지 않음 |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | 선언되지 않음; `k6`는 시나리오 하나를 실행하고 종료하므로 `restart`는 `no` |
| Operations | Guide (`docs/05.operations/guides/0061-k6.md`), Policy (`docs/05.operations/policies/0061-k6.md`), Runbook (`docs/05.operations/runbooks/0061-k6.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | hardening 점검으로 시작한 뒤 승인된 런타임 컨텍스트에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증을 제공합니다.

Build source authority: [Dockerfile](Dockerfile).
