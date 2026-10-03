---
title: "개발 Valkey"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-10-02"
---

# 개발 Valkey

## Overview

`dev-valkey`는 개발 프로젝트가 명시적으로 등록될 때 사용하는 단일 Valkey입니다.
관리용·LAB Valkey의 데이터와 계정을 공유하지 않습니다. 이 디렉터리는 설정과
ACL 생성 스크립트를 소유하며 서비스 선언은 [상위 Compose](../docker-compose.yml)가
소유합니다. 소스 선언은 승인된 기동 전까지 실행 상태가 아닙니다.

## Audience

개발 DB 운영자, 프로젝트 provision 담당자, 보안 검토자를 대상으로 합니다.

## Scope

서비스는 새 `${DEFAULT_DATA_DIR}/dev-valkey/data` 영속 경로와
`dev_data_net`을 사용하고 호스트 포트를 게시하지 않습니다. 관리자 자격 증명은
`dev_valkey_admin_password` Docker secret으로만 전달합니다. 기본
`config/projects.tsv`에는 프로젝트 행이 없고 관리자 ACL 외에는 계정이
생성되지 않습니다.

승인된 프로젝트 행은
`project_id|acl_user|key_prefix|secret_filename`의 네 필드를 명시합니다.
`DEV_VALKEY_PROJECTS_FILE`은 metadata 파일,
`DEV_VALKEY_PROJECT_SECRETS_DIR`은 참조된 비밀 파일의 읽기 전용 디렉터리를
가리킵니다. Override에는 절대 호스트 경로를 사용합니다. 상대 경로는 이를
선언한 Compose 조각의 디렉터리를 기준으로 해석됩니다. 누락·형식 오류·중복
프로젝트/계정/prefix/비밀 파일명·symlink·여러 줄의 비밀값은 기동을
거절합니다. 실제 비밀값은 추적된 소스나 문서에 두지 않습니다.

Valkey protected mode는 named-user ACL을 가진 원격 Compose peer의 인증 전 요청을 차단할 수 있어 끕니다. 서비스는 `dev_data_net`에만 expose하고 host port를 게시하지 않으며 `default off`와 필수 named-user ACL로 접근을 제한합니다. 격리 실행에서는 같은 network의 peer에서 `AUTH <user> <password>`/PING, 다른 prefix 접근 거절, 익명 접근 거절을 함께 확인해야 합니다.

프로젝트 계정은 명시된 `key_prefix:*`의 key/channel과 DB 0에만 접근합니다.
관리, 스크립트, pubsub, 전역 key 열거 명령은 허용하지 않습니다. DB 0 제한은
보조 명령 경계이며 DB 번호 자체는 프로젝트 격리 수단이 아닙니다. 이 ACL의
2026-10-03 합성 A/B 프로젝트의 prefix·관리 명령·DB1 접근 거절을 격리 엔진에서 확인했습니다. HOME 실행은 `NOT_RUN`입니다.

## Structure

- `config/valkey.conf`: 128 MiB `maxmemory`, `noeviction`, AOF `everysec`,
  정기 RDB snapshot.
- `config/projects.tsv`: 명시적 프로젝트 ACL metadata; 기본은 빈 목록.
- `config/empty-project-secrets/`: 미등록 상태에서 사용하는 빈 bind 소스.
- `scripts/render-acl.sh`: 비밀 파일을 읽어 해시 기반 ACL을 `/run/valkey`
  tmpfs에 원자적으로 생성합니다. 영속 `/data`에는 ACL 파일을 두지 않습니다.
- `scripts/start.sh`: ACL 생성이 성공한 뒤 Valkey를 시작합니다.

서비스의 자원 한도는 0.5 CPU, 컨테이너 메모리 256 MiB, Valkey 메모리
128 MiB입니다. 캐시 쓰기는 24시간 이내, 세션 쓰기는 12시간 이내의 TTL을
애플리케이션이 지정해야 합니다. 서버 ACL만으로 전역 TTL은 강제되지 않으므로
프로젝트 테스트가 이를 검증합니다. 큐 항목은 확인·정리 계약 없이 만료시키지
않습니다. 메모리 한도에 도달하면 쓰기를 거절합니다. 큐의 `noeviction`과
캐시의 LRU가 동시에 필요하면 별도 크기의 캐시 인스턴스를 승인받아야 합니다.

## Tech Stack

[상위 Compose](../docker-compose.yml)가 Valkey 이미지를 선언하고, [`config/`](config/)와 [`scripts/`](scripts/)가 ACL·시작 절차를 소유합니다.

## Configuration

`dev_data_net`과 별도 `/data` bind 경로를 사용합니다. 관리자 비밀은 Docker secret으로, 프로젝트 ACL은 승인된 `projects.tsv`와 별도 비밀 디렉터리로 공급합니다.

## Validation

아래 단위 검사는 ACL 생성 입력을 확인합니다. 실제 인증·prefix 거절·영속성은 격리 실행 결과를 따로 기록합니다.

## How to Work in This Area

합성 비밀값을 쓰는 집중 검사는 저장소 루트에서 다음과 같이 실행합니다.

```bash
python3 -m unittest tests/validation/test_dev_valkey_acl.py
```

실행 전 Docker context, 프로젝트, 포트, 네트워크, 새 볼륨, 비밀 참조,
정확한 정리 범위와 호스트 용량을 재확인합니다. 상위 Compose는 명시적으로 `999:999`로 실행하므로 새 bind 경로의
소유권을 맞춰야 합니다. 이미지 기본 UID/GID는 실제 이미지 검사로 확인해야 합니다.
격리 기동과 ACL 동작은 별도 Task에서 확인했고, HOME 기동·백업·복구는 `NOT_RUN`입니다.

## Related Documents

[문서 진입점](../../../../docs/README.md)에서 개발 데이터 계약과 운영
문서를 찾습니다. 공식 [Valkey ACL](https://valkey.io/topics/acl/) 및
[지속성](https://valkey.io/topics/persistence/) 문서를 참고합니다.
