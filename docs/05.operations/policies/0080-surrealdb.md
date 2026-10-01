---
title: "SurrealDB Policy"
version: "0.2.2"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0080"
parent_ids:
- "AD-0011"
created: "2026-09-19"
---

# SurrealDB Policy

## Overview

이 정책은 `08-ai` 티어 내에서 Open Notebook이 사용하는 `OPTIONAL`
단일 서비스 SurrealDB 배포를 다룬다.

## Policy Scope

- [작성된 Compose 소스](../../../infra/08-ai/open-notebook/docker-compose.yml), Dockerfile, entrypoint
- 서비스 `surrealdb`. 정확한 프로필은 `surrealdb`, `notebook`
- `surrealdb-data:/mydata`, 호스트 게시 없음, `ai_net`
- `surreal_db_password`와 root/namespace/database 인증 범위
- 연결된 가이드와 런북

## Controls

- **Required**: 현재 호스트 게시 없음과 `ai_net` 애플리케이션 경계를 유지한다.
  새 호스트 게시나 더 넓은 접근은 별도 승인된 네트워크 변경이 필요하다.
- **Required**: SurrealDB는 Open Notebook upstream 호환성을 위해 v2에
  고정된다. Open Notebook이 공식적으로 지원을 검증하기 전까지는 SurrealDB v3
  이상으로의 메이저 업그레이드가 금지된다.
- **Required**: 자격 증명은 Docker Secret을 사용한다. 문서와 증거에는 비밀번호
  값, 자격 증명을 포함한 URL, 원본 레코드, 토큰 자료가 포함되어서는 안 된다.
- **Required**: 모든 백업은 SurrealDB 버전, namespace, database, 인증 레벨,
  스키마/데이터 범위, 내보내기 옵션, 체크섬/위치, 보존/만료, 격리된 복구
  결과를 식별한다.
- **Required**: 복구는 새롭고 격리된 호환 대상과 승인된 root, namespace,
  또는 database 자격 증명을 사용한다. import 전에 선택한 v2 버전의 옵션·인증 범위·스키마 처리 근거를
  확인한다. 최신 버전의 `OPTION IMPORT` 설명을 그대로 적용하지 않는다.
- **Required**: import는 부분적으로 성공할 수 있으므로 실패한 대상은 진단용으로 격리 보존하고 재사용하지 않는다.
  재시도는 별도의 빈 대상에서 하며 이전 대상의 삭제는 따로 승인받는다. namespace/database, 테이블,
  스키마, 권한, 레코드 수 불변조건, 대표 읽기를 검증한다.
- **Required**: 업그레이드는 upstream 저장 형식 순서를 따르며 복구 테스트를
  거친 export, 용량 검토, 명시적 롤백 지점, 승인이 필요하다. 제거에는
  보존된 export 증거와 확인된 소비자 종료가 필요하다.
- **Allowed**: Compose 렌더링, 서비스 상태, 준비 상태, 마스킹된 인증 메타데이터
  점검.
- **Disallowed**: 준비 상태를 고치기 위해 비밀번호 파일을 변경하는 것,
  라이브 `/mydata`를 복사하는 것, 부분적으로 import된 대상을 재사용하는 것,
  또는 실행되지 않은 리허설을 테스트된 복구로 제시하는 것.

## Exceptions

소유자 `@buenhyden`은 편차 전에 범위, 위험, 만료, 종료 조건, 백업 식별자,
롤백 증거를 기록해야 한다.

## Verification

- `docker compose --profile surrealdb config --quiet`
- 서비스/프로필/마운트/시크릿 사실을 연결된 가이드, 런북, infra README와
  비교한다.
- `python3 scripts/validation/check-document-links.py --mode all`를 실행한다.

## Review Cadence

매월, 그리고 이미지, 저장 형식, 영속성, 인증, namespace/database, 노출,
업그레이드, 제거 변경 전에 검토한다.

## Traceability

- 상위 아키텍처: [AD-0011](../../02.architecture/descriptions/0011-laboratory-architecture.md)
- 대상 동위 문서: [가이드](../guides/0080-surrealdb.md), [런북](../runbooks/0080-surrealdb.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB 업그레이드 및 패치](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB 인증](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB 라이선스](https://surrealdb.com/license)
- [런타임 버전 projection](../../../infra/tech-stack.versions.json)
- [운영 인덱스](../README.md)
- [Infrastructure README](../../../infra/08-ai/open-notebook/README.md)
