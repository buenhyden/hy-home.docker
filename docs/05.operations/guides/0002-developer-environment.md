---
title: "Developer Environment Operations"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0002"
parent_ids: []
created: "2026-06-04"
---

# Developer Environment Operations

## Usage

이 가이드는 개발자·운영자·AI Agent가 로컬 작업 환경과 검증 범위를 구분하도록
돕는다. 저장소 checkout이 있다고 HOME 서비스 운영이나 credential 접근 권한이
생기는 것은 아니다. [bootstrap](../../../.agents/governance/bootstrap.md), 해당
provider adapter와 현재 Task에서 승인 범위를 먼저 확인한다.

### Local tools and configuration

저장소 스크립트는 Bash를 사용한다. Windows에서는 WSL2처럼 Bash와 저장소 도구를
지원하는 환경을 사용한다. Docker Engine과 Compose plugin은 실제 선택한 선언의
기능을 지원해야 한다. 루트 `include`만으로도 Compose 2.20.0 이상이 필요하다. <!-- runtime-version-exception: compatibility — root include requires Compose 2.20.0 or later; selected features may require a newer release. -->
설치 버전이나 Docker 접근 가능 여부는 현재 호스트에서 별도로 확인하며, 도구
설치·업데이트는 문서 검토의 부수 작업으로 실행하지 않는다.
[공식 include 설명](https://docs.docker.com/reference/compose-file/include/)과
[루트 선언](../../../docker-compose.yml)을 함께 확인한다.

공유 permission은 [Claude 설정](../../../.claude/settings.json)과
[Codex adapter](../../../.codex/provider.md)가 canonical governance를 소비한다.
`Bash(docker:*)`, `Bash(python3:*)` 같은 포괄적 local 허용이나 `allow: ["*"]`를
추가하지 않는다. runtime·비밀 작업은 도구 허용과 별개로 정확한 대상과 승인이
필요하다. 공유 설정에 개인 절대 경로를 넣지 않고 Claude hook 경로는
`$CLAUDE_PROJECT_DIR`를 사용한다. 개인 설정 파일 자체는 공유하지 않는다.

### Environment and certificates

공개 [.env.example](../../../.env.example)은 키 계약이며, `.env`는 해당
checkout 운영자의 로컬 값이다. 처음 준비할 때만 공개 예제를 바탕으로 필요한
profile 입력을 채우고 기존 파일을 덮어쓰지 않는다. 키 비교는
[0003](0003-env-key-comparison.md), secret metadata는
[0010](0010-sensitive-env-vars-comparison.md), 값 보관은
[secrets 안내](../../../secrets/README.md)를 따른다. 개인 값을 commit하거나
전체 환경·rendered Compose를 출력하지 않는다. `.env`를 shell로 source하면
내용이 실행되므로 단순 문서·키 점검에 사용하지 않는다.

로컬 TLS는 `mkcert`와 public root CA를 사용하는 현재 gateway 계약을 따른다.
`mkcert -install`은 호스트 trust store를 바꾸고 인증서 재발급은 기존 소비자에
영향을 주므로 owner가 별도로 승인한다. `cert.pem`, `key.pem`, `rootCA.pem`의
대상 경로, 도메인과 `CERT_GROUP_GID`를 [Traefik Guide](0013-traefik.md)에서
확인한다. key는 소비자가 읽을 수 있는 승인된 certificate group 권한을 유지하며
일률적인 `0600`으로 바꾸지 않는다. public `rootCA.pem`만 필요한 소비자에게
전달하고 CA private key는 복사하거나 출력하지 않는다. 기존 인증서를 보존한
상태에서 [Traefik Runbook](../runbooks/0013-traefik.md)으로 교체·검증을 넘긴다.

## Common Checks

저장소 README와 대상 package README에서 필요한 도구·입력을 확인한다.
[RUN-0086의 공개 구성 검증](../runbooks/0086-dependency-version-management.md#static-configuration-validation)은
임시 `.env`와 dummy secret 파일의 생성·정리 및 기존 입력 읽기 경계를 설명한다.
이 검사 성공은 실제 credential, host trust, 서비스 health나 복구 성공이 아니다.
도구 또는 승인된 입력이 없으면 실패 원인과 `BLOCKED`/`NOT_RUN`을 기록한다.

## Runbook Handoff

이 비서비스 주제에는 별도 서비스 Runbook을 만들지 않는다. 반복 검증은
[하네스 Runbook](../runbooks/0004-harness-agent-first-engineering.md), 설정 반영은
[RUN-0086](../runbooks/0086-dependency-version-management.md), 인증서와 gateway는
[RUN-0013](../runbooks/0013-traefik.md)이 소유한다. 알 수 없는 대상·권한·기존 값의
변경이 필요하면 중단하고 @buenhyden에게 값 없는 증거로 전달한다.

## Traceability

- 이 주제에는 같은 번호의 Policy/Runbook이 없다.
- [환경·승인 경계](../../../.agents/governance/environment-constraints.md)

## Related Documents

- [Operations index](../README.md)
- [공개 개발환경 입력](../../../.env.example)
- [Secret 관리](../../../secrets/README.md)
