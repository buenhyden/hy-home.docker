---
title: "Owned OpenBao Build"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
---

# Owned OpenBao build

## Overview

OpenBao 2.7.1의 공개 서명된 source distribution과 UI를 보존하고 Go 1.27.2, <!-- runtime-version-exception: migration — 검토된 build packet의 고정 migration material이며 build-inputs.json이 pin을 소유함 -->
`golang.org/x/net` 0.60.0 및 그 모듈 그래프가 요구하는 일곱 버전을 사용합니다. <!-- runtime-version-exception: migration — 검토된 build packet의 고정 module migration material이며 build-inputs.json이 pin을 소유함 -->
결과 버전은 `2.7.1+hyhome.go1.27.2.net0.60.0.r1`이며 upstream OpenBao의 <!-- runtime-version-exception: migration — 검토된 build packet을 식별하는 owned result version이며 build-inputs.json이 authority임 -->
서명된 이미지가 아닙니다. 다른 의존성의 취약점 해결을 보장하지 않습니다.

## Audience

이 선택된 이미지의 source, 재현성, SEC01 증거를 검토하는 Developer와 Operator.

## Scope

[build-inputs.json](build-inputs.json)은 실제 source, builder, Alpine, APK closure,
patch와 resource 한도를 고정합니다. [Dockerfile](Dockerfile)은 실제 runtime
조립 recipe이며 [helper](../scripts/build-owned-image.py)가 제한된 명령과
OCI config로 해석합니다. [OCI helper](owned_image_oci.py)는 이 공개 runtime
export만 정렬된 한 layer로 포장합니다. HOME 배포, 인증, 발급은 실행하지 않습니다.

이번 README metadata 정리는 문서 구조만 바로잡습니다. 기존 build artifact를 다시
만들거나 recipe packet을 변경하지 않으며, 기존 c318 packet은 변경 전 README
bytes를 계속 보존합니다.

## Structure

- [build-inputs.json](build-inputs.json): 선택된 source, builder, runtime, module, APK closure와 resource 한도를 고정합니다.
- [Dockerfile](Dockerfile): 공개 material을 검증하고 owned runtime rootfs를 조립하는 recipe입니다.
- [go-modules.patch](go-modules.patch): root module의 검토된 module 변경만 담습니다.
- [owned_image_oci.py](owned_image_oci.py): 검증된 공개 runtime export를 결정론적 OCI archive로 포장합니다.
- [build-owned-image.py](../scripts/build-owned-image.py): plan, 두 번의 build, 비교와 receipt 생성을 제한된 단계로 실행합니다.

## Tech Stack

선택된 [build-inputs.json](build-inputs.json)이 이 owned build의 고정 build input과
결과 version/tag의 권위입니다. [Dockerfile](Dockerfile)은 실제 runtime 조립 recipe이며,
[공유 버전 레지스트리](../../../../infra/tech-stack.versions.json)는 Compose와 build
source에서 파생된 투영으로서 이 build packet이나 배포 manifest를 대신하지 않습니다.

## Configuration

공개 material directory의 `materials.json` SHA와 일곱 source 파일의 packet SHA를
명시하여 helper의 `--phase plan`을 실행합니다. packet은 정렬된 상대 경로,
NUL, 파일 bytes, NUL을 순서대로 SHA-256에 넣습니다. `--phase build`는 동일한
입력의 두 독립적인 빈 Go cache compile 및 runtime 조립을 실행합니다.

Source archive와 Chainguard Go builder의 publisher 서명 검증 receipt, 독립적인
공식 Alpine RSA key, 서명된 두 APKINDEX, 정확한 19 APK 및 전체 Go module cache
manifest가 필요합니다. Cache의 `.zip`, `.mod`, `.info` 파일과 source hash를
보존하며 compile 전후 모두 확인합니다. Patch는 root `go.mod`와 최소 `go.sum`만
바꿉니다. 원본 vendor 및 nested module은 보존하고 `-mod=readonly`로 빌드합니다.

Compile은 linux/amd64 builder child digest, UID/GID 1000, network none,
readonly root, cap drop ALL, no-new-privileges, CPU 2, PID 128, RAM 4 GiB,
2700초 한도입니다. `memory-swap=4g`는 RAM을 포함한 총량이므로 swap은 0입니다.
Runtime은 network none, CPU 1, PID 64, RAM 1 GiB, 300초 한도이며 격리 rootfs에
공개 APK와 binary, entrypoint, license만 넣습니다. CHOWN만 추가하여 upstream
UID 100/GID 1000의 data/config/logs 디렉터리를 만듭니다. 독립 검증한 key로 APK를
다시 검증하고 `--no-network`로 설치하며 `--allow-untrusted`는 금지합니다.

Host Docker daemon은 명시적으로 orchestration/export에 사용합니다. 그 socket,
인증 config, HOME 파일은 container에 mount하지 않습니다. 새 0700 출력 directory,
concurrency lock, 시작 시 가용 RAM 12 GiB 및 disk 32 GiB 이상을 요구합니다.
16 GiB scratch 예산과 16 GiB disk reserve를 두며 실패·OOM·cleanup 실패는 FAIL입니다.
실패한 invocation의 receipt를 덮어쓰지 않고 새 directory로만 재시도합니다.

두 binary SHA와 OCI config/layer/manifest가 모두 같아야 재현성 PASS입니다.
원본 timestamp 대신 upstream commit epoch를 사용하고 uid/gid/mode/symlink는
보존합니다. 새 잠긴 openbao 계정의 shadow 마지막 변경 날짜만 commit epoch의
일수로 고정하며 다른 계정·필드와 원본 파일 권한은 보존합니다.
Packet/material/patch hash는 OCI label로 연결됩니다. OCI archive를
Docker에 load한 뒤 `hy-home/openbao:<tag>@sha256:<manifest>`를 `--pull=never`로
조회 및 실행하여 고정 reference가 작동하는지 확인해야 합니다.

## Validation

[contract tests](../../../../tests/validation/test_openbao_owned_image_contract.py)는
경로·소유권·material hash·실제 container 제한·재현성 및 공개 export 경계를
합성 입력으로 검증합니다. 실제 binary version, SBOM과 fresh offline CVE,
P01 격리 rehearsal은 build 이후 해당 기존 gate에서 별도로 검증합니다.
이 README와 build 성공만으로 runtime 수용을 선언하지 않습니다.

## Usage

새 build를 검토할 때는 [build-inputs.json](build-inputs.json)의 선택된 입력과
[Dockerfile](Dockerfile), 공개 material receipt를 같은 packet으로 확인합니다.
실제 build와 OCI 검증은 [helper](../scripts/build-owned-image.py)의 제한된 phase를
사용하며, HOME 배포·인증·발급·복구는 소유 Runbook의 별도 수용 절차를 따릅니다.

## Related Documents

- [OpenBao implementation](../README.md)
- [Shared runtime version projection](../../../../infra/tech-stack.versions.json)
- [Owned image contract tests](../../../../tests/validation/test_openbao_owned_image_contract.py)
