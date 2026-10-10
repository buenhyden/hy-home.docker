---
title: "미래 consumer 계약"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 미래 consumer 계약

## Overview

consumer-manifest는 기존 registration schema를 메모리 내 URN으로 참조합니다. namespace·classification·OIDC issuer/audience·원천 repo/ref allowlist·DB 네 역할·Valkey ACL/명령·S3 prefix·Qdrant collection 및 non-admin role·egress·metric cardinality·retention·backup/RPO/RTO 및 disabled_by_design을 계획합니다. Qdrant collection은 project_id와 같고 role은 `project-reader`/`project-writer`만 허용하는 정책으로 pure helper가 확인합니다. fixture 수치는 합성 예제이며 운영 최적값 또는 실제 할당이 아닙니다.

등록은 draft/not_run만 허용합니다. wildcard/admin·교차 프로젝트·경로 탈출·빈 필수값·외부 schema 조회를 거절합니다. 기존 generic registration validator는 test harness에서 별도로 실행하고 P09 helper는 caller policy만 소비합니다. 실제 endpoint 도달성·TLS/OIDC·ACL·resource quota는 NOT_RUN입니다. P02는 canonical SMTP secret catalog만 소유하고 P03는 기존 서비스 endpoint·port 계약 조건만 소유합니다. 미래 Wiki의 runtime/resource/retention/RPO/RTO와 deletion/recovery는 이름 있는 별도 exact Task가 정할 때까지 UNKNOWN입니다.

helper의 신뢰 경계는 문서 자기선언이 아닌 caller policy입니다. policy는 `project_id`, source별 repository/ref/immutable revision/path allowlist, issuer/audience, DB·Valkey·Qdrant·S3 namespace를 제공합니다. registration refs는 caller가 명시한 `infra_ref`, `template_ref`, `project_ref`의 정확한 40-hex immutable SHA여야 하며 source 문서나 ref 이름에서 추정하지 않습니다. permission은 정확한 `read`와 `append-candidate` allowlist이고 ACL reader는 정확한 `example-project-reader` allowlist입니다. DB는 `example_project_db`, `example_project_app`, 네 `example_project_*` role, top-level `allowed_networks`의 `example-project-net` subset과 일치해야 하며 quota는 CPU 500m, memory 512MiB, storage 2GiB, 60 requests/minute를 초과할 수 없습니다. 합성 registration endpoint는 exact parsed `same_daemon.db` map(`postgresql`, `dev-pg`, `5432`, `/example_project_db`)과 비교하고, retention은 최대 30일, backup은 `owner=project`, RPO 3600초, RTO 7200초, restore drill `NOT_RUN`으로 제한합니다. 이는 generic validator semantics 복제가 아닌 별도 admission allowlist입니다. document 값은 이 범위와 일치해야 하며, policy의 존재와 static 일치는 실제 identity issuer, role grant, network egress 또는 resource provision을 증명하지 않습니다.

consumer validation이 돌려주는 scoped idempotency result는 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)를 따릅니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[schema](../schemas/consumer-manifest.schema.json), [통합 제안](../integration-proposal/README.md)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Usage

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

## Related Documents

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.
