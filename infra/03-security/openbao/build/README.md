---
title: "Owned OpenBao Build"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Owned OpenBao build

## Purpose

### Service Role

OpenBao 2.7.2의 공개 서명된 source distribution과 UI를 보존하고 Go 1.27.3, <!-- runtime-version-exception: migration — 검토된 build packet의 고정 migration material이며 build-inputs.json이 pin을 소유함 -->
`golang.org/x/net` 0.62.0, `go-jose/v4` 4.1.9, `klauspost/compress` 1.20.4 세 module 버전을 사용합니다. <!-- runtime-version-exception: migration — 검토된 build packet의 고정 module migration material이며 build-inputs.json이 pin을 소유함 -->
결과 버전은 `2.7.2+hyhome.go1.27.3.net0.62.0.r1`이며 upstream OpenBao의 <!-- runtime-version-exception: migration — 검토된 build packet을 식별하는 owned result version이며 build-inputs.json이 authority임 -->
서명된 이미지가 아닙니다. 다른 의존성의 취약점 해결을 보장하지 않습니다.

#### Audience

이 선택된 이미지의 source, 재현성, SEC01 증거를 검토하는 Developer와 Operator.

[build-inputs.json](build-inputs.json)은 실제 source, builder, Alpine, APK closure,
patch와 resource 한도를 고정합니다. [Dockerfile](Dockerfile)은 실제 runtime
조립 recipe이며 [helper](../scripts/build-owned-image.py)가 제한된 명령과
OCI config로 해석합니다. [OCI helper](owned_image_oci.py)는 이 공개 runtime
export만 정렬된 한 layer로 포장합니다. HOME 배포, 인증, 발급은 실행하지 않습니다.

2026-10-21 packet은 Go 1.27.3 builder로 다시 고정했습니다(CVE-2026-111943, crypto/x509). <!-- runtime-version-exception: migration — 검토된 build packet의 고정 builder 변경이며 build-inputs.json이 pin을 소유함 -->
source, module, APK 입력은 그대로이고 builder와 그 서명 receipt만 바뀌었습니다.
이 README는 packet의 일부이므로 바꾸면 packet SHA와 image label이 달라집니다.

2026-11-10 packet(`r3`)은 source를 서명된 최신 stable release로 올리고(upstream 보안 수정 GHSA 4건) <!-- runtime-version-exception: migration — 검토된 build packet의 고정 source 변경이며 build-inputs.json이 pin을 소유함 -->
patch를 그 release의 root go.mod/go.sum 위에서 다시 만들어 x/net, go-jose v4, klauspost/compress의 보안 수정 버전만 올렸습니다.
Go builder, Alpine runtime과 APK closure는 그대로입니다. go-jose v3는 수정 버전이 없고 hashicorp/cap과 okta SDK를 통해
binary에 링크되므로 이 packet이 해결하지 않는 잔여 위험으로 남습니다.

2026-11-10 packet(`r2`)은 runtime을 Alpine 3.24 계열 최신 digest로, APK closure를 현재 서명된
v3.24 main/community APKINDEX 기준으로 다시 고정했습니다. source, Go module, patch 입력은 그대로이고
두 publisher receipt는 새로 검증했습니다. 정확한 digest와 version은 build-inputs.json이 소유합니다.

#### Structure

- [build-inputs.json](build-inputs.json): 선택된 source, builder, runtime, module, APK closure와 resource 한도를 고정합니다.
- [Dockerfile](Dockerfile): 공개 material을 검증하고 owned runtime rootfs를 조립하는 recipe입니다.
- [go-modules.patch](go-modules.patch): root module의 검토된 module 변경만 담습니다.
- [owned_image_oci.py](owned_image_oci.py): 검증된 공개 runtime export를 결정론적 OCI archive로 포장합니다.
- [build-owned-image.py](../scripts/build-owned-image.py): plan, 두 번의 build, 비교와 receipt 생성을 제한된 단계로 실행합니다.

### Supported Environment

선택된 [build-inputs.json](build-inputs.json)이 이 owned build의 고정 build input과
결과 version/tag의 권위입니다. [Dockerfile](Dockerfile)은 실제 runtime 조립 recipe이며,
[공유 버전 레지스트리](../../../../infra/tech-stack.versions.json)는 Compose와 build
source에서 파생된 투영으로서 이 build packet이나 배포 manifest를 대신하지 않습니다.

## Interfaces

### Inputs and Outputs

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

### Security Boundary

없음: 이 폴더에는 Compose 서비스와 secret 정의가 없으며, secret 값을 저장소에 두지 않는다.

## Development

### Local Workflow

새 build를 검토할 때는 [build-inputs.json](build-inputs.json)의 선택된 입력과
[Dockerfile](Dockerfile), 공개 material receipt를 같은 packet으로 확인합니다.
실제 build와 OCI 검증은 [helper](../scripts/build-owned-image.py)의 제한된 phase를
사용하며, HOME 배포·인증·발급·복구는 소유 Runbook의 별도 수용 절차를 따릅니다.

#### Material 준비 절차

다음 build를 같은 방식으로 재현하려면 [준비 script](../../../../scripts/operations/prepare-openbao-materials.py)를
사용합니다. 공개 자료만 받으며 HOME, 인증, secret, `labs/`는 건드리지 않습니다.

1. 전제: [network 승인 문서](../../../supply-chain.network-approvals.md)에
   `OpenBao material network approval: confirmed` 줄이 있어야 합니다. 허용 host는 `github.com`
   (OpenBao release asset), `dl-cdn.alpinelinux.org`, `alpinelinux.org`, `cgr.dev`와 Sigstore 공개 TUF/Rekor/Fulcio뿐입니다.
   Go module 캐시를 받는 `proxy.golang.org`와 `sum.golang.org`는 별도 승인이 있을 때만 `--allow-go-proxy`로 엽니다.
2. 실행: `python3 -I scripts/operations/prepare-openbao-materials.py`. 출력은 새 0700
   `/tmp/hyhome-p01-owned-build-<UTC>/` 아래이며(helper가 이 경로만 받습니다) 이미 있으면 거부합니다.
   `materials/`가 `--materials-directory`, `materials/materials.json`의 SHA-256이 `--materials-sha256`입니다.
3. 순서: 고정된 Alpine key(URL과 SHA-256 pin)와 source archive(pin) 받기 → 두 APKINDEX를 key로 RSA 서명 검증 →
   cosign 컨테이너로 publisher receipt 생성 → `apk_requested` 이름을 현재 index에서 dependency와 `install_if`까지
   풀어 closure 계산 → 각 APK를 받아 크기, index control checksum, key 서명 검증 → source를 풀고(symlink는
   manifest가 거부하므로 제외하고 `omitted_symlinks`로 기록) go-modules.patch 적용 → 격리 컨테이너로 module 캐시를 받고
   network 없이 `go mod verify`와 `go list -deps`로 확인 → `materials.json` 작성.
4. Receipt: `source_checksums`는 release의 `checksums.txt`를 `cosign verify-blob --bundle checksums.txt.sigstore.json`과
   OpenBao 공식 문서의 identity regexp `^https://github.com/openbao/openbao/.github/workflows/release.yml@refs/heads/(main|release/.+)$`,
   issuer `https://token.actions.githubusercontent.com`으로 검증한 뒤 pin된 source archive의 SHA-256이 그 파일에 있는지 확인합니다.
   `builder`는 pin된 `cgr.dev/chainguard/go` index와 child digest를 `cosign verify`와 Chainguard 공식 문서의 identity
   `https://github.com/chainguard-images/images/.github/workflows/release.yaml@refs/heads/main`, 같은 issuer로 검증합니다.
   Identity는 검증 대상 인증서에서 가져오지 않고 다음 공식 문서에서만 가져옵니다.
   <https://openbao.org/docs/install/#cosign>(원문은 OpenBao 저장소의 `website/content/docs/install.mdx`)와
   <https://edu.chainguard.dev/chainguard/containers/security-and-compliance/verifying-chainguard-images-and-metadata-signatures-with-cosign/>.
   OpenBao 문서는 고정 identity 대신 이 regexp를 제시합니다. Receipt에는 PASS, exit 0, 정확한 명령, identity, issuer와
   subject digest가 들어갑니다.
5. Cosign은 [tool 이미지 registry](../../../supply-chain.tool-images.json)의 `bounded_contracts`에 등록된
   고정 digest 이미지만 쓰며 read-only rootfs, cap drop ALL, no-new-privileges, CPU 1, RAM 512 MiB, PID 32,
   150초 한도로 실행합니다. Docker socket, 인증 설정, HOME, secret, 쓰기 가능한 host 경로는 mount하지 않습니다.
6. 출력된 `apk_indexes`, `apk_requested`, `apk_closure`, `publisher_receipts`를 build-inputs.json에 반영하고
   `recipe_sha256`(Dockerfile의 SHA-256)을 다시 계산한 뒤, packet SHA(`current_packet` 규칙)를 계산하여
   `build-owned-image.py --phase plan`이 FAIL 없이 끝나는지 확인합니다. 그 뒤에만 `--phase build`를 승인된 창에서 실행합니다.

### Checks

[contract tests](../../../../tests/validation/test_openbao_owned_image_contract.py)는
경로·소유권·material hash·실제 container 제한·재현성 및 공개 export 경계를
합성 입력으로 검증합니다. 실제 binary version, SBOM과 fresh offline CVE,
P01 격리 rehearsal은 build 이후 해당 기존 gate에서 별도로 검증합니다.
이 README와 build 성공만으로 runtime 수용을 선언하지 않습니다.

## Operations

### Runbook Links

#### Related Documents

- [OpenBao implementation](../README.md)
- [Shared runtime version projection](../../../../infra/tech-stack.versions.json)
- [Owned image contract tests](../../../../tests/validation/test_openbao_owned_image_contract.py)

### Observability and Recovery

없음: 이 폴더에는 헬스체크나 관측 대상 선언이 없다.
