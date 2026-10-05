---
title: "Storybook 공유 UI 패키지"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-10-03"
---

# Storybook 공유 UI 패키지

## Overview

`@hy-home/storybook-ui`는 검토된 Button 컴포넌트만 제공하는 내부 전용 npm workspace 패키지입니다. Storybook URL이나 manifest는 코드 배포 수단이 아닙니다.

## Audience

내부 UI 개발자와 패키지 소비 계약 검토자입니다.

## Scope

Button, TypeScript 선언, CSS만 내보냅니다. Header와 Page는 Storybook 예제로 남습니다. 이 패키지는 `private: true`, `UNLICENSED`이며 외부 또는 공개 npm 배포를 허용하지 않습니다.

## Structure

`src/Button.tsx`가 컴포넌트 원본, `src/styles.css`가 명시적 스타일 진입점, `src/index.ts`가 유일한 코드 export입니다. `dist/`는 빌드 산출물입니다.

## Tech Stack

React 19 peer dependency와 TypeScript 6 빌드를 사용합니다. 실제 버전은 이 폴더의 `package.json`과 상위 lockfile이 소유합니다.

## Configuration

상위 `projects/storybook/nextjs/package-lock.json`이 workspace 설치를 소유합니다. 소비자는 `Button`을 패키지에서 import하고 CSS를 한 번 별도로 import해야 합니다.

```tsx
import { Button } from '@hy-home/storybook-ui';
import '@hy-home/storybook-ui/styles.css';

<Button label="확인" onClick={() => {}} />
```

## Validation

`npm run build:ui` 뒤 `npm run test:artifacts`로 실행 export와 선언·스타일 계약을 확인합니다. 외부 프로젝트의 합성 소비 시험은 로컬 `npm pack` 산출물로 수행합니다.

## Usage

Button의 API 또는 CSS를 변경하면 버전과 Storybook 상태별 story를 함께 검토합니다. 별도 배포 승인이 없으므로 공개 레지스트리 업로드는 하지 않습니다.

## Related Documents

- [상위 Storybook 작업공간](../../README.md)
- [공유 Storybook 작업공간](../../../README.md)
