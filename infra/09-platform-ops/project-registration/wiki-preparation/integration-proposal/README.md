---
title: "공통 등록 통합 인계"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 공통 등록 통합 인계

## Overview

P09는 기존 generic registration schema와 validator를 그대로 재사용합니다. schema는 메모리 URN `urn:hyhome:registration:v1`로만 참조하고, test harness가 기존 validator를 별도로 실행합니다. Public `wiki_preparation.py`는 parsed 문서, caller 정책, 합성 bytes와 prior receipt만 받으며 `PreparationError`를 re-export하는 유일한 API입니다. Private `wiki_preparation_semantics.py`는 그 validator 구현을 담고 직접 소비 API가 아닙니다. 두 모듈 모두 callback, filesystem, network, environment, secret, subprocess 또는 외부 쓰기를 사용하지 않습니다. generic schema PASS와 helper semantic PASS는 runtime, 권리, 원천 진위 또는 운영 readiness 보증이 아닙니다.

공통 등록은 coordinator single-writer가 구현했습니다. `scripts/manifest.yaml`은 public helper와 private semantics module을 P09 library surface로, 두 전용 테스트를 consumers/tests로 등록합니다. `.github/workflow-contract.yml`은 두 테스트를 `repository-integrity` regression에 추가하고, public helper 및 private semantics module과 전용 test 경로를 두 precise changed-path rules에 등록합니다. package root `infra/09-platform-ops/project-registration/wiki-preparation/`는 기존 `infra/` rule의 document-contract/document-graph/document-lifecycle/operations/repository-integrity suite를 유지합니다. Parent registration README, SPEC-0204 Spec/Plan과 in-progress TSK-0008은 preparation-only·실제 resource 변경 0·공통 등록 owner와 W25/criterion 13을 기록합니다. Historical proposal, RED/GREEN 및 Gitleaks receipt는 Task의 Work Log가 유일하게 보존합니다.

caller policy는 parsed mapping이며 trusted `project_id`, source repository/ref/revision/path allowlist, identity issuer/audience, resource namespace(DB/Valkey/Qdrant/S3), blog repository/base SHA/selected candidate/exact write-set allowlist를 제공합니다. registration refs `infra_ref`, `template_ref`, `project_ref`는 모두 caller가 제공한 exact 40-hex immutable SHA이며 source/ref 이름에서 파생하지 않습니다. permission은 `read`/`append-candidate`만, ACL reader는 `example-project-reader`만 받습니다. DB는 exact `example_project_db`/`example_project_app`/네 `example_project_*` role이고 top-level `allowed_networks`는 `example-project-net` subset입니다. quota는 CPU 500m, memory 512MiB, storage 2GiB, 60 requests/minute를 넘지 않습니다. registration endpoint는 parsed exact map으로 비교합니다: 합성 policy는 `same_daemon.db`의 `scheme=postgresql`, `host=dev-pg`, `port=5432`, `path=/example_project_db`입니다. policy는 `retention_days` 최대 30 및 backup exact 값 `owner=project`, `rpo_seconds=3600`, `rto_seconds=7200`, `restore_drill=NOT_RUN`, job exact identity `job_id=example-job`, `dedup_key`, `outbox.event_id=example-event`도 제공합니다. 이는 generic validator semantics의 복제가 아니라 caller가 승인한 입력 범위를 독립 비교해 admission을 제한하는 것입니다. `prior_receipts`는 `{idempotency_key: request_sha256}` mapping입니다. helper는 candidate와 write-set 순서를 canonicalize한 request SHA-256을 만들고, 같은 key가 같은 request SHA-256에만 idempotent임을 인정하며 다른 값은 거절합니다.

원본 키·scoped helper 결과 키·prior receipt key의 canonical 정의는 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)가 소유합니다.

P09의 public synthetic checksum Gitleaks 오탐은 coordinator review와
negative-boundary 확인을 거친 좁은 `AND`/target-rule/path/hash guard로
등록되었습니다. guard의 hash와 과거 실패·검증 receipt는 Task Work Log가
소유합니다. checksum을 rename·line-break해 detector를 피하지 않으며 global
lint skip 또는 넓은 glob 예외는 사용하지 않습니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[준비 패키지](../README.md), [schema](../schemas/README.md), [fixture 기대 결과](../fixtures/expectations.json)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Usage

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

## Related Documents

[project registration 계약](../README.md), [문서 진입점](../../../../../docs/README.md), 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.
