---
title: "Lake & Object Storage (04-data/lake-and-object)"
version: "1.1.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-05-15"
---

# Lake and object storage

## Overview

이 영역은 저장소의 lake 및 오브젝트 저장소 패키지를 문서화합니다.

## Audience

오브젝트 저장소 tier의 operator와 maintainer를 대상으로 합니다.

## Scope

HOME SeaweedFS 스토어를 다룹니다.

## Structure

### Packages and relationship

- [`seaweedfs`](seaweedfs/README.md)는 HOME S3 스토어이며 각 소비자에게는
  bucket 범위의 identity가 있습니다. MinIO는 모든 소비자가 이전된 뒤
  제거되었고(SPEC-0180 S07) 데이터 디렉터리는 복구 자료로 보존됩니다
  (RUN-0024).

## How to Work in This Area

루트 Compose profile을 사용하고 별도의 저장소 경로, secret, 네트워크
경계를 유지하십시오.

## Related Documents

[문서 진입점](../../../docs/README.md)에서 Stage 05 subject
`docs/05.operations/guides/0024-seaweedfs.md`와 백업 정책 POL-0021을
찾으십시오.
