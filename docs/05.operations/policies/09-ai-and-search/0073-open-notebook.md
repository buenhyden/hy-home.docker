---
title: "Open Notebook Operations Policy"
version: "1.1.5"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "POL-0073"
parent_ids:
- "AD-0011"
created: "2026-05-17"
---

# Open Notebook Operations Policy

## Purpose

### Objective

Open Notebook은 OPTIONAL 지식/모델 워크스페이스다. 콘텐츠, 데이터베이스,
provider 자격 증명, 암호화 키가 하나의 복구 경계를 이룬다.

### Authority

- [가이드](../../guides/09-ai-and-search/0073-open-notebook.md) (`GDE-0073`)
- [런북](../../runbooks/09-ai-and-search/0073-open-notebook.md) (`RUN-0073`)
- [Laboratory 아키텍처](../../../02.architecture/descriptions/0011-laboratory-architecture.md)

- [Open Notebook Compose 소스](../../../../infra/08-ai/open-notebook/docker-compose.yml)

## Scope

### Applies To

활성화, UI/API 노출, 앱/데이터베이스 인증, provider/모델 접근, 콘텐츠 보존,
백업/복구, floating 이미지 업그레이드, 제거.

### Exclusions

이 정책은 위 Applies To에 나열한 대상 밖의 서비스와 환경에는 적용하지 않는다.

## Rules

### Requirements

- `notebook`만 사용한다. `admin`은 이를 선택해서는 안 된다. HOME 밖에 유지한다.
- Open Notebook upstream은 SurrealDB v2를 요구한다. upstream Open Notebook이
  v3를 명시적으로 지원하고 검증하기 전까지는 SurrealDB v3 이상으로의
  업그레이드가 금지된다.
- CIDR allowlist를 보존하고 API 호스트 포트를 loopback에 바인딩된 상태로
  유지한다. 공유 SSO가 없는 한 애플리케이션 비밀번호가 유일한 신원 통제이므로
  이 비밀번호와 SurrealDB 인증은 계속 필수다. SSO 재도입은 별도의 소유자 결정이다.
- provider 키는 앱의 암호화된 저장소에 보관하고 `open_notebook_encryption_key`는
  별도로 보호한다. 승인된 재암호화/내보내기 계획 없이는 절대로 회전하거나
  분실하지 않는다.
- 노트북, 소스 문서, 임베딩, 채팅, provider 설정을 민감 정보로 취급한다.
  사용 전에 보존과 내보내기 소유권을 정의한다.
- SurrealDB를 논리적으로 백업하고 `/app/data`, 소스 커밋, 보호된 키/자격 증명
  보관을 함께 백업한다. provider egress를 비활성화한 상태로 리허설한다.
- 추적 중인 이미지가 의도적으로 floating이므로 릴리스/보안 노트를 검토한다.
  승격 전에 마이그레이션과 자격 증명 복호화를 테스트한다.
- 제거 전에 콘텐츠/provider 자격 증명을 내보내거나 명시적으로 폐기한다.
  데이터베이스와 앱 볼륨 삭제는 별개의 파괴적 작업이다.
- 현재 기본 provider 경로는 local-only Ollama다. Ollama-mediated cloud와 direct
  cloud는 별도 credential, 허용 목적, network 및 비용 계약을 요구하며 자동 fallback
  이나 동일 instance의 `OLLAMA_NO_CLOUD=1` 예외로 도입하지 않는다.
- 저장된 모델 등록은 지원되는 product UI/API를 사용한다. 환경 fallback, healthcheck,
  DB online 또는 디렉터리 존재로 저장된 모델·provider·embedding 기능을 수용하지
  않는다. 다른 credential과 충돌하는 동명 등록은 보존하고 거부한다.

### Enforcement

UI/앱 인증, API 경계, DB 준비 상태, 키 복호화, 하나의 합성 노트북을
검증하며, provider 접근은 별도로 승인된 경우에만 검증한다. 모델 기능은 저장된
연결, terminal embedding job, 입력/응답 및 재시작 후 보존을 별도로 검증한다.

## Exceptions

### Exception Conditions

공유 SSO 제거는 소유자 커밋 `b90b74837`, 포괄 admin 선택 제거는 `d5912ab03`의
승인된 경계다. 변경 가능한 이미지 예외는 저장소의 image-tag 예외 원본에 따라
Laboratory Operator가 매월 검토하고 사용할 rollback 이미지 식별자를 보존한다.
책임자 `@buenhyden`의 별도 검토 없이 이 예외를 인증 생략·API 확대·v3 전환으로
확장하지 않는다. 암호화 키 손실은 DB 복원만으로 복구되지 않는다.

API를 광범위하게 노출하거나, 키를 소스에 저장하거나, 대응하는 암호화 키와
격리된 검증 없이 데이터를 복구하는 예외는 없다.

### Approval and Review

릴리스, provider/모델, API 경로, DB 스키마, 키, 보존 정책 변경 시
검토한다.

## Ownership

### Responsibilities

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Change and Adoption

- [Open Notebook 보안](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
- [SurrealDB 백업 및 복구](https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery)
