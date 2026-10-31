---
title: "Hermes 수집 전송 합성 시험"
version: "0.3.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-01"
---

# Hermes 수집 전송 합성 시험

## Overview

로컬 파일 보존과 전송 상태 처리, 비활성 흐름의 보안 경계를 검증합니다.
고정된 Gateway 계약·Fixture에 대한 합성 호환성을 확인합니다. 실제 엔진
가져오기·서버 간 통신과 영속 수신 성공은 별도 증거입니다.

## Scope

임시 합성 산출물과 가짜 전송 연결을 사용합니다. 실제 비밀값·원본 내용·외부
엔드포인트는 필요하지 않습니다. 실제 원본을 사용한 검증을 수행하면 합성 결과와
분리하여 작업 기록에 남깁니다. 기존 조사·이메일·서비스 중단 시험은 실행하지 않습니다.

## Structure

- [test_workflow.py](test_workflow.py): 비활성 흐름과 입력 선별, 분기, 고정 대상,
  영속 수신 응답을 합성 데이터와 빈 Node VM으로 검증합니다.
- [test_gateway_adapter.py](test_gateway_adapter.py)와
  [test_gateway_transport.py](test_gateway_transport.py): 고정 계약 어댑터와
  동일 요청 재전송·Outbox 처리를 합성 방식으로 검증합니다.
- [합성 보고서](fixtures/synthetic-report.json)와 같은 디렉터리의 계약 파일: Blog-data `dev` 커밋
  `a6d0957ad380f179f73bdd2a60ff23792d53f7ae`에서 고정한 계약과 합성 보고서입니다.
- [attestation-v2.vectors.json](fixtures/attestation-v2.vectors.json): Blog-data `dev` 커밋
  `b372de374ec589b1bec2ff8096ae2f7272461248`의 `scripts/lib/ingestion/contracts/attestation-v2.vectors.json`을
  바이트 단위로 그대로 복사한 v2 증명 벡터입니다. 합성 키만 담으며 수정하지 않습니다.

- [test_ingress_route.py](test_ingress_route.py): 제안 Traefik 경로가 흐름의 정확한
  경로·POST·호스트 출발지·본문·속도 제한만 허용하는지 확인합니다.
- [test_export_route.py](test_export_route.py): 제안 Export 경로가 Windows 조회·ACK와
  호스트 Attestation 세 요청 형태, 출발지, 본문, 속도 제한만 허용하는지 확인합니다.
- [test_attestation.py](test_attestation.py): Blog-data 코드로 계산한
  [교차 언어 벡터](fixtures/attestation-vector-v1.json)와의 메시지 일치, 신뢰 판정,
  서명 키 보관, 응답 분류, `attest` 명령을 검증합니다.
- [install-check.sh](install-check.sh): 보호 설치 시험입니다.
- [gateway-image.sh](gateway-image.sh): Blog-data Dockerfile의 빌드 컨텍스트 허용 목록대로
  정확한 커밋을 Sparse Checkout하여 Gateway 이미지를 빌드하는 공통 함수입니다.
- [e2e-ingress.sh](e2e-ingress.sh): 일회용 Traefik·n8n·Gateway로 직접 제출 경로와
  Attestation·Export·ACK 경로 전체를 합성 Token과 합성 키로 확인합니다.
- [e2e-upgrade.sh](e2e-upgrade.sh): 이전 고정본의 schema 2 저장소를 백업·제자리
  업그레이드·새 볼륨 복원하는 일회용 시험입니다.

그 밖의 준비·대기함·전송 시험 파일은 이 디렉터리의 전체 탐색 명령으로 함께
실행합니다. 실제 검증기의 누락·변경은 의존성 실패로 보고합니다.

## Usage

저장소 루트에서 실행합니다.

```bash
python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -v
```

흐름 소스만 확인하려면 다음 명령을 사용합니다.

```bash
python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p test_workflow.py -v
```

보호 설치 시험은 Docker와 PyPI 접근이 필요하며 일회용 root 컨테이너에서 커밋
하나를 설치한 뒤 별도 Publisher·Hermes 계정으로 쓰기 불가와 약화 시 거부를
확인합니다. 운영 호스트를 바꾸지 않습니다.

```bash
infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests/install-check.sh [commit]
```

직접 제출 경로 시험은 Docker, 비공개 Blog-data 저장소의 `gh` 접근과 로컬 n8n
이미지가 필요합니다. 고정 커밋에서 Gateway 이미지를 빌드하고 임의 접미사의
네트워크·볼륨·컨테이너를 만든 뒤 종료 시 모두 지웁니다. 운영 스택, 네트워크,
비밀, Traefik 디렉터리는 건드리지 않습니다. n8n은 같은 이미지의 기본 진입점으로
실행합니다. hy-home 진입점은 운영 비밀을 요구하므로 쓰지 않습니다.

```bash
infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests/e2e-ingress.sh [blog-data-commit]
infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests/e2e-upgrade.sh [previous-blog-data-commit]
```

Gateway 컨테이너는 Compose에서 렌더링한 사용자·읽기 전용 루트·권한·제한으로
실행합니다. 일회용 시험에서는 한 호스트가 Windows B와 서버 A 서명자를 함께 대신하므로
라우터별 출발지 분리는 `test_export_route.py`가 확인합니다. 실제 Windows 수신기,
운영 Traefik과 Compose 고정 시험 이미지의 버전 차이는 이 시험이 증명하지 않으며
측정값은 작업 기록에 둡니다.

전체 시험 결과·측정 범위·독립 검토는 작업 기록을 따릅니다. 합성 검증은
운영 n8n Queue·외부 Runner·실제 인증이나 운영 Gateway의 영속 수신을 증명하지 않습니다.
일부 시험은 별도 고정 검증기 또는 로컬 합성 HTTP/TLS 환경이 필요합니다.

## Related Documents

- [수집 전송 소스](../README.md)
- [로컬 발행기](../publisher/README.md)
