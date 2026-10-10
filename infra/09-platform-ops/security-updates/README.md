---
title: "Security update evidence"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# 보안 업데이트 조사 증거

## Overview

이 폴더는 SEC01의 현재 source·runtime 조사 자료와 미실행 경계를 보관합니다.
수용 책임은 SPEC-0204와 정식 발급된
`SPEC-0204-TSK-0009`에
있으며 공통 문서 통합은 총괄 순서를 따릅니다.
JSON 자료는 기존 inventory·버전 projection을 대체하는 Registry가 아닙니다.
이 README는 `scripts/lib/supply_chain/latest_version_gate.py`와
`scripts/lib/supply_chain/security_update_gate.py`의 durable gate contract
authority입니다. script manifest는 Task가 아니라 이 README를 authority로
참조합니다.

## Scope

root include closure의 서비스와 선택된 custom build 입력을 조사합니다.
LAB runtime, 학습 앱, 실제 HOME 변경·비밀값 변경·자료 삭제는 포함하지 않습니다.
관찰 시점의 서비스 개수는 결과이며 검사 상수로 사용하지 않습니다.

## Structure

| 파일 | 용도 |
| --- | --- |
| `update-ledger.json` | include 입력 SHA, 현재 선언·실행 metadata, 서비스별 미검증 경계 |
| `build-inputs.json` | 선택 Dockerfile·inline FROM/ARG/설치 입력·lockfile hash |
| `image-source-lookups.json` | 현재 image/FROM의 amd64 OCI source label 조회 결과 |
| `release-lookups.json` | 확인한 정확한 공급자 repository의 공식 release API 응답 |
| `vendor-channel-references.json` | 공급자 문서에서 확인한 stable/current 판정과 API 차이 |
| `tool-readiness.json` | 기존 scanner Registry pin·cache·trust/database 미검증 경계 |
| `package-lookups.json` | 선택한 Python/Node source 의존성의 공식 package index 조회 |
| `verification.json` | 실제 local 시험 결과·입력 hash·미실행 상태 |
| `integration-handoff.json` | 총괄 선행 조건·GoTrue 계약·P09 단독 작성자 인계 |
| `common-validator-integration.patch` | 수신 당시 공통 runtime·AI 버전·Renovate 검증기 수정 제안; 현재 authoritative diff가 아닌 역사 입력 |
| `service-inventory-integration.patch` | 수신 당시 renderer Airflow Env 셀 갱신 제안; 현재 authoritative diff가 아닌 역사 입력 |

## Usage

### 현재 후보 release-channel provenance

이번 service-local 후보를 구성하는 공급자 identity의 exact tag/ref object, annotated-tag
dereference, full commit, 요청별 종료 코드와 관찰 시각은
[`release-lookups.json`](./release-lookups.json)에 구조화했습니다. 아래 표는 공급자
channel과 resolved source revision의 사람이 읽는 색인입니다. runtime pin은 각 서비스
Compose/Dockerfile과 [`infra/tech-stack.versions.json`](../../tech-stack.versions.json)이
소유합니다. 이 근거는 image 서명·SBOM·CVE scan·native 호환·stateful 복원·HOME
배포를 증명하지 않으며 해당 항목은 계속 `NOT_RUN`입니다.

| 공급자 identity | 공식 channel 근거 | resolved full commit | latest/ref 관찰 시각 (UTC) |
| --- | --- | --- | --- |
| Prometheus | [Prometheus download](https://prometheus.io/download/) | [`5241a27fe3c6983549fccc32f6e65917408c63cd`](https://github.com/prometheus/prometheus/commit/5241a27fe3c6983549fccc32f6e65917408c63cd) | `2026-10-10T16:43:49.415475+00:00` / `2026-10-10T16:43:49.898722+00:00` |
| Grafana Alloy | [Alloy release channel](https://grafana.com/docs/alloy/latest/) | [`95e12cf8961fabc9db6858f7e79bde5c814a07a0`](https://github.com/grafana/alloy/commit/95e12cf8961fabc9db6858f7e79bde5c814a07a0) | `2026-10-10T16:43:50.787604+00:00` / `2026-10-10T16:43:51.303195+00:00` |
| cAdvisor | [cAdvisor publisher latest](https://github.com/google/cadvisor/releases/latest) | [`5bf5d43ac6f60d7ee36a13b4d5b4a78ad2d0abc7`](https://github.com/google/cadvisor/commit/5bf5d43ac6f60d7ee36a13b4d5b4a78ad2d0abc7) | `2026-10-10T16:43:51.758805+00:00` / `2026-10-10T16:43:52.259505+00:00` |
| Grafana Pyroscope | [Pyroscope support/release channel](https://grafana.com/docs/pyroscope/latest/release-notes/) | [`1c9109674636cfd5c5e61ee3b01ed93c06bff8be`](https://github.com/grafana/pyroscope/commit/1c9109674636cfd5c5e61ee3b01ed93c06bff8be) | `2026-10-10T16:43:52.674952+00:00` / `2026-10-10T16:43:53.220849+00:00` |
| Pushgateway | [Prometheus download](https://prometheus.io/download/) | [`3e29338978f3046ba1a602d6cca520121ab91112`](https://github.com/prometheus/pushgateway/commit/3e29338978f3046ba1a602d6cca520121ab91112) | `2026-10-10T16:43:54.115027+00:00` / `2026-10-10T16:43:54.625186+00:00` |
| Dozzle | [Dozzle install channel](https://dozzle.dev/guide/getting-started) | [`309a3a6edae7f7b8e0443105b674b57985e04848`](https://github.com/amir20/dozzle/commit/309a3a6edae7f7b8e0443105b674b57985e04848) | `2026-10-10T16:43:55.656643+00:00` / `2026-10-10T16:43:56.088389+00:00` |
| Conftest | [Conftest installer channel](https://www.conftest.dev/install/) | [`8f7ac015cb51d81992f2ffbe2b0c1451fd05d1c5`](https://github.com/open-policy-agent/conftest/commit/8f7ac015cb51d81992f2ffbe2b0c1451fd05d1c5) | `2026-10-10T16:43:56.880818+00:00` / `2026-10-10T16:43:57.341048+00:00` |
| Mailpit | [Mailpit stable tag contract](https://mailpit.axllent.org/docs/install/docker/) | [`ccb524a62b3a14b6a3fd55c1275a16945d10e36b`](https://github.com/axllent/mailpit/commit/ccb524a62b3a14b6a3fd55c1275a16945d10e36b) | `2026-10-10T16:43:57.773291+00:00` / `2026-10-10T16:43:58.236070+00:00` |
| Qdrant | [Qdrant release channel](https://qdrant.tech/documentation/installation/) | [`016542aa5deb6c66380bb137badf73d54f742bde`](https://github.com/qdrant/qdrant/commit/016542aa5deb6c66380bb137badf73d54f742bde) | `2026-10-10T16:43:59.059872+00:00` / `2026-10-10T16:43:59.508184+00:00` |
| Renovate | [Renovate image flavors](https://docs.renovatebot.com/getting-started/running/) | [`182de2759f0bb31ee6216f4076875948d39c4c1b`](https://github.com/renovatebot/renovate/commit/182de2759f0bb31ee6216f4076875948d39c4c1b) | `2026-10-10T16:44:00.383717+00:00` / `2026-10-10T16:44:00.894131+00:00` |
| SeaweedFS | [SeaweedFS release-image contract](https://github.com/seaweedfs/seaweedfs/blob/master/docker/README.md) | [`530be3e37337488ecc34d58441e0bc476e121c93`](https://github.com/seaweedfs/seaweedfs/commit/530be3e37337488ecc34d58441e0bc476e121c93) | `2026-10-10T16:44:01.350015+00:00` / `2026-10-10T16:44:01.901164+00:00` |
| AWS CLI | [AWS official image contract](https://hub.docker.com/r/amazon/aws-cli/) | [`9469a4d8191c8139b54dd119526648d29a4b5f72`](https://github.com/aws/aws-cli/commit/9469a4d8191c8139b54dd119526648d29a4b5f72) | `2026-10-10T16:44:07.222358+00:00` / `2026-10-10T16:44:06.407222+00:00` |
| Stalwart Server | [Stalwart stable/newest contract](https://www.stalw.art/docs/install/platform/docker/) | [`3f657330c0f49a015a3a372fb59669b5cccbca6d`](https://github.com/stalwartlabs/stalwart/commit/3f657330c0f49a015a3a372fb59669b5cccbca6d) | `2026-10-10T16:44:02.302946+00:00` / `2026-10-10T16:44:02.834291+00:00` |
| Stalwart CLI | [Stalwart CLI installer channel](https://stalw.art/docs/management/cli/) | [`e78e596eca9a352b8b3db3379001f9384dd15c17`](https://github.com/stalwartlabs/cli/commit/e78e596eca9a352b8b3db3379001f9384dd15c17) | `2026-10-10T16:44:03.240338+00:00` / `2026-10-10T16:44:03.732929+00:00` |
| Open Notebook | [Open Notebook latest-only support](https://github.com/lfnovo/open-notebook/security) | [`315d5255af2a5132aada41c94d5c3c5dc8e837aa`](https://github.com/lfnovo/open-notebook/commit/315d5255af2a5132aada41c94d5c3c5dc8e837aa) | `2026-10-10T16:44:04.157274+00:00` / `2026-10-10T16:44:04.655896+00:00` |
| CNCF Distribution | [Distribution stable release](https://github.com/distribution/distribution/releases/latest) | [`3220848f15d9279c66a41aa0a257469e6aede1e9`](https://github.com/distribution/distribution/commit/3220848f15d9279c66a41aa0a257469e6aede1e9) | `2026-10-10T16:44:05.085071+00:00` / `2026-10-10T16:44:05.552356+00:00` |

`python3 -m scripts.lib.supply_chain.latest_version_gate --input infra/09-platform-ops/security-updates/update-ledger.json`
은 공급자 최신판·channel 미확인 항목을 `ready=false`, 종료 코드 2로 남깁니다.
CLI는 장부의 `expected_services`를 신뢰하지 않고 기존 operations catalog의
parser/include helper로 실제 root Compose source를 다시 읽습니다. `--repo-root`는
검사할 checkout을 지정하며 기본값은 이 helper가 속한 저장소입니다. 출력에는 공개
Compose 입력별 SHA와 입력 집합 SHA를 남깁니다. 장부의 항목과 expected 배열에서
동시에 서비스를 제거해도 실제 source 집합 대비 누락으로 실패합니다.
이 source 집합은 활성 profile·runtime 관찰을 대신하지 않습니다.

현재 총괄 입력은 여전히 DEFER 영수증이다. latest gate는 `ready=false`,
`deployed=false`, `externalfacts=false`, exit 2와 missing/unexpected 서비스 없음을
반환한다. security gate는 `ledger_complete=false`, `coverage_checked=true`, exit 2와
관측된 124개 `blocked-evidence` 항목을 반환한다. latest gate의 전체 후보 중
61개는 여전히 미완결이며, 이번 20개 service-local 후보는 channel/source 기준만
충족한다. 두 gate는 root input manifest SHA-256
`26c4328eac56770d91f39f7a56ba2d5ed99311d05b5d149724824bd9d66d4555`에
연결된다. 이 수는 서비스 수 계약이 아닌 관측 증거다.

`python3 -m scripts.lib.supply_chain.security_update_gate --input <reviewed-security-ledger.json>`
은 같은 독립 root source 집합과 별도 담당자가 검토한 보안 장부의 필드 완전성을 검사합니다.
필드가 완결된 행도 `ledger-complete-pending-independent-verification`이며
공급자·scan·호환·복원·승인을 독립 검증한 결과가 아닙니다. CLI 종료 코드 0도
장부의 형식·집합 정합만 뜻하고 rollout 허가나 실제 보안 해소를 뜻하지 않습니다.
아직 해당 보안 장부에 scan·compatibility·recovery 증거가 없으므로 배포 준비를 주장하지 않습니다.

OCI source label은 서명 검증을 하지 않은 공급자 metadata입니다. label이나
`isPrerelease=false`만으로 repository 소유권·vendor stable 지정·지원 기간을 확정하지 않습니다.
GitHub latest release 조회 실패는 최신판이 없다는 판정이 아닙니다.
index·platform manifest·config/image ID는 별도로 구분합니다.

활성 profile 선택, source에 없는 운영 job/복구 소비, 설치 package/SBOM,
후보 동일 플랫폼 signature·scan, native migration·복원·15분 HOME 중단 한도는 추가 검증 대상입니다.
각 미확인 행은 SEC01 담당과 발견일로부터 7일 이내 다음 검증 기한을 가집니다.
단순 image tag 하향은 DB·data format migration rollback 근거가 아닙니다.
HOME rollout은 실제 backup·독립 custody·빈 환경 복원 및 총괄 순서 확인 후 수행합니다.

최초 `include_inputs`와 runtime 관찰 시각·값은 보존합니다. `source_refreshes`와
`initial_source_observation`은 현재 dirty 후보의 선언 변화와 최초 입력을 구분합니다.
Grafana·Ollama·OpenBao·Airflow·n8n의 새 source pin과 플랫폼 digest는 HOME에서
실행 중인 이전 image를 대체한 증거가 아닙니다. 당시 owning Task `UNISSUED` 및
common runtime compatibility 2 FAIL은 수신 당시 역사 사실입니다. TSK-0009이
현재 formal owner이며 coordinator integration의 current replay는 runtime 30 PASS와
AI/Renovate 15 PASS를 기록합니다. 이는 latest-head delivery PASS가 아닙니다.
signature·SBOM·scanner는 실제 tool/cache/DB/trust facts가 없어 `NOT_RUN`이고,
HOME은 별도의 target/custody/recovery boundary가 없어 `NOT_RUN`입니다.

workflow 후보의 마지막 index·amd64 manifest·config와 두 n8n build variant는
최종 worker receipt로 갱신했습니다. worker가 새로 실행한 UNIT 5건·ISOLATED 3건은
장부의 `candidate_workflow_receipt`에 명령·입력 SHA·범위와 함께 별도 기록합니다.
이 담당자가 실행한 장부 시험이나 HOME 기능 성공으로 합치지 않습니다.
`build-inputs.json`의 최초 snapshot은 보존하며 현재 Dockerfile·Compose build args·
FROM/ARG/COPY/SHELL·설치 입력·constraints hash를 새 snapshot으로 구분합니다.
OpenBao helper 추가 수정 가능성은 수신 당시 상태이며, 현재 final integration은
TSK-0009의 latest/security gate와 review/delivery receipt가 결정합니다.

### 2026-10-11 Grype candidate scan

후보 image는 모두 digest 또는 local tag 기준으로 pull/build한 뒤 Docker socket 없이 `docker-archive` tar 입력으로 스캔했습니다. scanner는 기존 local `anchore/grype` image ID `fd4ab4d1042b`의 Grype `0.116.0` / Syft `1.48.0`이며, <!-- runtime-version-exception: history — scanner evidence versions, not runtime image pins --> DB는 네트워크 허용 상태에서 갱신한 뒤 각 image 스캔은 `--network none`과 `GRYPE_CHECK_FOR_APP_UPDATE=false`로 실행했습니다. 중간 tar 입력은 삭제했고 scanner JSON은 `/tmp/sec01-*-grype.json`에 남겼습니다. 이 위치의 JSON은 작업 증거이며 repository source가 아닙니다.

| 후보 | Critical | High | 총 match | fixable 경계 |
| --- | ---: | ---: | ---: | --- |
| qdrant | 0 | 55 | 158 | High 1 |
| seaweedfs | 2 | 20 | 48 | Critical 2, High 12 |
| aws-cli | 1 | 4 | 17 | Critical 1, High 4 |
| prometheus | 6 | 24 | 38 | Critical 6, High 21 |
| alloy | 3 | 13 | 101 | Critical 3, High 13 |
| cadvisor | 2 | 22 | 51 | Critical 2, High 14 |
| pyroscope | 0 | 0 | 0 | 없음 |
| pushgateway | 1 | 9 | 13 | Critical 1, High 6 |
| dozzle | 2 | 11 | 17 | Critical 2, High 11 |
| open-notebook | 33 | 391 | 1007 | Critical 1, High 49 |
| registry | 2 | 20 | 50 | Critical 2, High 12 |
| renovate | 9 | 101 | 861 | Critical 9, High 97 |
| stalwart | 17 | 84 | 249 | High 1 |
| stalwart-config | 17 | 84 | 249 | High 1 |
| conftest | 2 | 19 | 46 | Critical 2, High 11 |
| mailpit | 1 | 8 | 13 | Critical 1, High 8 |

이 결과는 latest/source 후보 선정과 digest pull/build가 끝난 상태를 나타낼 뿐이며 SEC01 security PASS가 아닙니다. Pyroscope만 현재 scanner match 0이고, 나머지 후보에는 Critical 또는 High 결과가 남아 있습니다. 다음 SEC01 단계는 JSON별 CVE·package·fix state triage, 공급자 advisory와 false-positive 근거 확인, update/replace 또는 잔여 위험 승인 기록, SBOM·signature·native compatibility·stateful recovery 재실행입니다. 이 절차 전까지 HOME rollout과 전체 최신화·보안 완료 주장은 차단됩니다.

## Related Documents

- `infra/tech-stack.versions.json`: 기존 Compose image projection
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`: 기존 현재 서비스 inventory
- `scripts/security/verify-sample-service-supply-chain.sh`: 기존 sample 전용 Syft·Grype·Cosign 절차
- `docs/03.specs/0204-service-integration-security-and-operations/`: owning Spec

HTTP 429를 관찰한 image metadata 조회는 quota/backoff 뒤 다시 확인합니다.
공급자의 `test` tag나 NGINX mainline을 vendor stable로 자동 승격하지 않습니다.
Supabase Studio의 monorepo release와 DB image의 test release도 별도 공급 계약입니다.
