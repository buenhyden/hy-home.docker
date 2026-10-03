---
title: "외부 프로젝트 인프라 등록 계약"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
---

# 외부 프로젝트 인프라 등록 계약

## Overview

외부 `Project-Template` 파생 프로젝트가 사용할 인프라 자원과 접속 위치를
비밀값 없이 기록하는 메타데이터 계약입니다. 등록 문서의 통과는 자원 생성,
비밀 발급, 배포 또는 운영 승인으로 해석하지 않습니다.

## Audience

프로젝트 연결을 검토하는 인프라 운영자와 외부 프로젝트 담당자입니다.

## Scope

인프라는 엔진, 공용 ingress·identity, 관측, 백업과 제한된 자원 등록을
소유합니다. 외부 프로젝트는 업무 API·UI·migration·수집 adapter·workflow·fixture·
E2E와 실행 Compose를 소유합니다. 이 저장소 root Compose는 외부 앱 소스를
include하지 않습니다. 실제 프로젝트 ID와 자원 범위가 승인되기 전에는
등록 문서를 생성하지 않습니다.

## Structure

- [`schema.json`](schema.json): 알 수 없는 필드를 거부하는 등록 문서 형식.
- [`check-project-registration.py`](../../../scripts/validation/check-project-registration.py):
  schema와 프로젝트 경계, 승인된 secret 참조 이름을 검사하는 명시적 검증기.
- [`test_project_registration.py`](../../../tests/validation/test_project_registration.py):
  비밀값 없는 합성 입력의 허용·거절 검사.

## Tech Stack

Python 표준 라이브러리와 저장소의 기존 `jsonschema` 의존성만 사용합니다.
Compose 서비스나 이미지를 추가하지 않습니다.

## Configuration

`schema_version`, `interface_version`, `project_id`, `environment`, 세 Git SHA
(`infra_ref`, `template_ref`, `project_ref`), 접속 위치별 구조화된 `endpoints`,
`allowed_networks`, DB 이름·schema·역할, Valkey ACL prefix, S3 bucket/prefix, OIDC client ID,
검색 collection·권한 경로, telemetry `service.name`, backup/restore 소유자,
`secret_refs`, `quota`, `approval`, `verification`을 기록합니다.

`endpoints`는 `same_daemon`, `host`, `external` 위치 아래 서비스 이름별
`scheme`·`host`·`port`·`path`만 받습니다. URI userinfo·query·fragment·환경변수
치환은 넣지 않습니다. 같은 Docker daemon의 서비스 이름을 다른 호스트의 DNS로
기록하지 않습니다. `host`·`external` endpoint에는 단일 Docker 서비스 이름을 넣지 않습니다.
`localhost`는 호스트 로컬 접속을 나타낼 때 `host` 위치에서만 허용합니다. `same_daemon`은
ASCII 소문자로 시작하는 한 단어 Docker 서비스 이름만 받으며 `external`은
ASCII 소문자로 시작하는 DNS FQDN만 받습니다. 외부 IP 리터럴은 TLS server-name
계약 전까지 허용하지 않습니다. `external`은 `https`·
`rediss` scheme만 받고 DB endpoint는 거절합니다. 외부 DB 연결은 명명된
프로젝트의 TLS mode·server name·CA 계약이 승인된 뒤 별도로 정의해야 합니다.
이 검사는 scheme 문자열만 확인하며 인증서 검증, DNS 해석, 사설망 도달성 또는
실제 egress 권한을 증명하지 않습니다.
S3 prefix는 `project_id/`로, 검색 권한 경로는 `/projects/<project_id>`로 시작하고
기본 Docker `host`·`none`·`bridge` 네트워크는 프로젝트 경계로 등록하지 않습니다.
현재 dev-pg 계약은 `development` 환경만 받으며 DB endpoint path는 `/<db.name>`입니다.
DB 이름·schema·역할은 개발 PG provisioner의 예약 이름을 피해야 합니다.
Valkey의 `acl_prefix`에는 끝 콜론을 넣지 않고 `project_id`를 그대로 기록합니다.
ACL 생성기가 `:<key>` 패턴을 붙입니다. `default`와 `devadmin`은 ACL 사용자로
예약되어 있습니다.
`secret_refs`에는 값이나 파일 내용이 아닌 이름만 넣습니다.
검증기의 허용 이름 목록은 기본적으로 비어 있으며, 승인된 Task의 이름을
`--allow-secret-ref`로 명시해야 합니다. `approval` 필드는 승인 증거를 대체하지
않습니다. quota의 실제 허용 상한과 경로 접근 권한은 후속 프로젝트별 승인이
결정합니다.

## Validation

저장소 루트에서 합성 계약 검사를 실행합니다.

```bash
python3 -m unittest tests.validation.test_project_registration
python3 scripts/validation/check-project-registration.py \
  /path/to/approved-registration.json --allow-secret-ref approved_reference_name
python3 scripts/validation/check-script-manifest.py
```

검증기는 운영 비밀을 읽지 않으며 문서 내용을 오류 출력에 복사하지 않습니다.
별도의 비밀 검사와 사람 검토가 필요합니다. 정적 통과는 route, OIDC, DB,
Valkey, S3, 검색, 관측의 접근 권한이나 실제 연결을 증명하지 않습니다.

## How to Work in This Area

실제 프로젝트가 승인되면 외부 저장소가 소비용 manifest를 작성합니다. 인프라
담당자는 해당 Task에서 참조 이름과 자원 범위를 확인하고, 이 schema와 검증기를
실행합니다. 이후의 provision·비밀 발급·HOME 변경은 각각 승인된 작업으로
진행합니다. 필드를 바꾸면 schema, 검증기, 합성 검사를 같은 변경에서 갱신합니다.

## Related Documents

[문서 진입점](../../../docs/README.md)에서 SPEC-0201과 SPEC-0204의 외부 프로젝트
계약을 확인하십시오.
