---
title: "SurrealDB Policy"
version: "0.4.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0080"
parent_ids:
- "AD-0011"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# SurrealDB Policy

## Purpose and Scope

### Objective

이 정책은 `08-ai` 티어 내에서 Open Notebook이 사용하는 `OPTIONAL`
단일 서비스 SurrealDB 배포를 다룬다.

#### Authority

- 상위 아키텍처: [AD-0011](../../../02.architecture/descriptions/0011-laboratory-architecture.md)

### Applies To

- [작성된 Compose 소스](../../../../infra/08-ai/open-notebook/docker-compose.yml), Dockerfile, entrypoint
- 서비스 `surrealdb`. 정확한 프로필은 `surrealdb`, `notebook`
- `surrealdb-data:/mydata`, 호스트 게시 없음, `ai_net`
- `surreal_db_password`와 root/namespace/database 인증 범위
- 연결된 가이드와 런북

#### Exclusions

이 정책은 단일 서비스 `surrealdb` 배포만 다루며 Open Notebook 애플리케이션 서비스는 대상에 포함하지 않는다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0080-R1 | 항상 | 필수: 현재 호스트 게시 없음과 `ai_net` 애플리케이션 경계를 유지한다 | none | none |
| POL-0080-R2 | 새 호스트 게시/더 넓은 접근 | 필수: 별도 승인된 네트워크 변경을 거친다 | 수동 | none |
| POL-0080-R3 | 항상 | 필수: Open Notebook upstream 호환성을 위해 SurrealDB를 v2에 고정한다 | none | none |
| POL-0080-R4 | Open Notebook의 공식 지원 검증 전 | 금지: SurrealDB v3 이상으로의 메이저 업그레이드 | none | none |
| POL-0080-R5 | 항상 | 필수: 자격 증명은 Docker Secret을 사용한다 | none | none |
| POL-0080-R6 | 문서/증거 | 금지: 비밀번호 값/자격 증명을 포함한 URL/원본 레코드/토큰 자료 포함 | none | none |
| POL-0080-R7 | 모든 백업 | 필수: SurrealDB 버전/namespace/database/인증 레벨/스키마·데이터 범위/내보내기 옵션/체크섬·위치/보존·만료/격리된 복구 결과를 식별한다 | none | none |
| POL-0080-R8 | 복구 | 필수: 새롭고 격리된 호환 대상과 승인된 root/namespace/database 자격 증명을 사용한다 | none | none |
| POL-0080-R9 | import 전 | 필수: 선택한 v2 버전의 옵션·인증 범위·스키마 처리 근거를 확인한다 | none | none |
| POL-0080-R10 | 항상 | 금지: 최신 버전의 `OPTION IMPORT` 설명을 그대로 적용 | none | none |
| POL-0080-R11 | import 실패 | 필수: 실패한 대상을 진단용으로 격리 보존한다 | none | none |
| POL-0080-R12 | 항상 | 금지: 부분적으로 import된 대상의 재사용 | none | none |
| POL-0080-R13 | 재시도 | 필수: 별도의 빈 대상에서 한다 | none | none |
| POL-0080-R14 | 이전 대상 삭제 | 필수: 따로 승인받는다 | 수동 | none |
| POL-0080-R15 | 복구 검증 | 필수: namespace/database/테이블/스키마/권한/레코드 수 불변조건/대표 읽기를 검증한다 | none | none |
| POL-0080-R16 | 업그레이드 | 필수: upstream 저장 형식 순서를 따른다 | none | none |
| POL-0080-R17 | 업그레이드 | 필수: 복구 테스트를 거친 export/용량 검토/명시적 롤백 지점/승인을 갖춘다 | 수동 | none |
| POL-0080-R18 | 제거 | 필수: 보존된 export 증거와 확인된 소비자 종료를 갖춘다 | none | none |
| POL-0080-R19 | 점검 | 허용: Compose 렌더링/서비스 상태/준비 상태/마스킹된 인증 메타데이터 점검 | none | none |
| POL-0080-R20 | 항상 | 금지: 준비 상태를 고치기 위한 비밀번호 파일 변경 | none | none |
| POL-0080-R21 | 항상 | 금지: 라이브 `/mydata` 복사 | none | none |
| POL-0080-R22 | 항상 | 금지: 실행되지 않은 리허설을 테스트된 복구로 제시 | none | none |
| POL-0080-R23 | 구성 검증 | 필수: `docker compose --profile surrealdb config --quiet`를 실행한다 | `docker compose --profile surrealdb config --quiet` | none |
| POL-0080-R24 | 문서 동기화 | 필수: 서비스/프로필/마운트/시크릿 사실을 연결된 가이드/런북/infra README와 비교한다 | 수동 | none |
| POL-0080-R25 | 문서 검증 | 필수: `python3 scripts/validation/check-document-links.py --mode all`을 실행한다 | `python3 scripts/validation/check-document-links.py --mode all` | none |

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

### Exceptions

#### Exception Conditions

소유자 `@buenhyden`은 편차 전에 범위, 위험, 만료, 종료 조건, 백업 식별자,
롤백 증거를 기록해야 한다.

#### Approval and Review

매월, 그리고 이미지, 저장 형식, 영속성, 인증, namespace/database, 노출,
업그레이드, 제거 변경 전에 검토한다.

## Enforcement

### Mechanisms

- `docker compose --profile surrealdb config --quiet`
- 서비스/프로필/마운트/시크릿 사실을 연결된 가이드, 런북, infra README와
  비교한다.
- `python3 scripts/validation/check-document-links.py --mode all`를 실행한다.

### Limits

이 정책에서 이름 붙은 검사는 compose render와 문서 링크 검사뿐이며, 아래 규칙은 자동 검사 없이 검토·승인에 의존합니다.

- 노출: 자동 검사 없음(none) `POL-0080-R1`; 수동 검토/승인 `POL-0080-R2`
- 버전: 자동 검사 없음(none) `POL-0080-R3`, `POL-0080-R4`
- secret: 자동 검사 없음(none) `POL-0080-R5`, `POL-0080-R6`
- 백업/복구: 자동 검사 없음(none) `POL-0080-R7`, `POL-0080-R8`, `POL-0080-R9`, `POL-0080-R10`, `POL-0080-R11`, `POL-0080-R12`, `POL-0080-R13`, `POL-0080-R15`; 수동 검토/승인 `POL-0080-R14`
- 업그레이드/제거: 자동 검사 없음(none) `POL-0080-R16`, `POL-0080-R18`; 수동 검토/승인 `POL-0080-R17`
- 허용/금지: 자동 검사 없음(none) `POL-0080-R19`, `POL-0080-R20`, `POL-0080-R21`, `POL-0080-R22`
- 검사: 수동 검토/승인 `POL-0080-R24`
- 정책이 밝힌 범위: 정책이 지정한 검사는 compose render/문서 비교/문서 링크 검사뿐이며 문서와 서비스 사실의 일치는 사람이 비교하는 검토에 의존한다.

## Ownership

### Owner

정책 소유자는 @buenhyden이다.

### Review Triggers

- 대상 동위 문서: [가이드](../../guides/05-databases-and-storage/0080-surrealdb.md), [런북](../../runbooks/05-databases-and-storage/0080-surrealdb.md)

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB 업그레이드 및 패치](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB 인증](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB 라이선스](https://surrealdb.com/license)
- [런타임 버전 projection](../../../../infra/tech-stack.versions.json)
- [운영 인덱스](../../README.md)
- [Infrastructure README](../../../../infra/08-ai/open-notebook/README.md)
