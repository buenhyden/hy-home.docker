# Laboratory Dashboard (Homer) Guide

> This guide explains how to manage and customize the static service dashboard (Homer) in the 11-laboratory tier.

---

## Overview (KR)

이 문서는 Homer 대시보드의 서비스 링크 관리, 테마 커스터마이징, 레이아웃 변경 방법을 설명한다. 하이홈 인프라의 모든 도구에 대한 접근성을 유지하고 관리하는 중앙 관리 지침을 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Operator
- Developer
- Agent-tuner

## Purpose

- 신규 인프라 서비스의 대시보드 등록 자동화 및 표준화.
- 대시보드의 가독성 및 가시성 향상을 위한 스타일링 관리.
- 서비스 메타데이터(아이콘, 태그) 관리 표준 확립.

## Prerequisites

- `infra/11-laboratory/dashboard/config/config.yml` 파일 접근 권한.
- FontAwesome 아이콘 이름 지식.
- Traefik 서비스 도메인 정보.

## Step-by-step Instructions

### 1. Adding New Services

신규 서비스를 대시보드에 추가하려면 다음 절차를 따른다.

1. `infra/11-laboratory/dashboard/config/config.yml` 파일을 연다.
2. `services` 배열 아래 적절한 그룹을 찾거나 새 그룹을 생성한다.
3. `items` 리스트에 다음 형식으로 서비스를 추가한다:

   ```yaml
   - name: "Service Name"
     icon: "fa-solid fa-server" # FontAwesome 아이콘
     subtitle: "Brief description"
     tag: "monitoring" # 색상 구분을 위한 태그
     url: "https://service.${DEFAULT_URL}"
   ```

4. 파일을 저장한다 (볼륨 바인딩을 통해 즉시 반영된다).

### 2. Customizing Icons and Logos

- **Icons**: [FontAwesome v6](https://fontawesome.com/icons) 클래스명을 사용한다 (예: `fa-solid fa-cube`).
- **Logos**: `dashboard/config/` 폴더에 이미지 파일을 두고 `logo: "my-logo.png"`와 같이 참조한다.

### 3. Layout and Theming

- **Columns**: `columns: "3"` 옵션을 통해 한 줄에 표시될 카드 개수를 조정한다.
- **Theme**: `theme: default` 섹션에서 색상이나 스타일을 정의할 수 있다.

## Common Pitfalls

- **YAML Indentation**: 들여쓰기 오류 발생 시 대시보드가 로드되지 않는다. 수정 후 `yq` 등으로 검증을 권장한다.
- **URL Syntax**: `${DEFAULT_URL}` 변수 사용 시 따옴표(`${DEFAULT_URL}`) 유의.

## Related Documents

- **Implementation**: `[../../../infra/11-laboratory/dashboard/README.md]`
- **Operation**: `[../../08.operations/11-laboratory/dashboard.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/dashboard.md]`
