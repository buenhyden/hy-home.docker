---
title: "Security update evidence"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
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
관측된 124개 `blocked-evidence` 항목을 반환한다. 두 gate는 root input manifest SHA-256
`3a2e7451e6211b43b9d8f9c9760fed0fcf5cdac381e45e1b2323628b60756f66`.
에 연결된다. 이 수는 서비스 수 계약이 아닌 관측 증거다.

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

## Related Documents

- `infra/tech-stack.versions.json`: 기존 Compose image projection
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`: 기존 현재 서비스 inventory
- `scripts/security/verify-sample-service-supply-chain.sh`: 기존 sample 전용 Syft·Grype·Cosign 절차
- `docs/03.specs/0204-service-integration-security-and-operations/`: owning Spec

HTTP 429를 관찰한 image metadata 조회는 quota/backoff 뒤 다시 확인합니다.
공급자의 `test` tag나 NGINX mainline을 vendor stable로 자동 승격하지 않습니다.
Supabase Studio의 monorepo release와 DB image의 test release도 별도 공급 계약입니다.
