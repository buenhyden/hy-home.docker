---
title: "Storybook 공유 UI 패키지"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2026-10-03"
---

# Storybook 공유 UI 패키지

## Overview

`@hy-home/storybook-ui`는 검토된 `Button`, `AsyncState` 컴포넌트와 디자인 토큰을 제공하는 내부 전용 npm workspace 패키지입니다. Storybook URL이나 manifest는 코드 배포 수단이 아닙니다.

## Audience

내부 UI 개발자와 패키지 소비 계약 검토자입니다.

## Scope

`Button`, `AsyncState`, TypeScript 선언, 토큰을 포함한 CSS만 내보냅니다. 토큰 값의 권위는 `src/styles.css`의 `--hy-*` 변수입니다. 이 패키지는 `private: true`, `UNLICENSED`이며 외부 또는 공개 npm 배포를 허용하지 않습니다.

## Structure

`src/Button.tsx`와 `src/AsyncState.tsx`가 컴포넌트 원본, `src/styles.css`가 토큰과 스타일 진입점, `src/index.ts`가 유일한 코드 export입니다. `dist/`는 빌드 산출물입니다.

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

컴포넌트 API, 토큰 이름 또는 CSS를 변경하면 버전과 상태별 story를 함께 검토합니다. 별도 배포 승인이 없으므로 공개 레지스트리 업로드는 하지 않습니다.

0.2.0은 Button의 `primary`, `backgroundColor`를 `variant`, `disabled`, `loading`으로 대체한 호환되지 않는 변경입니다. 색은 prop이 아니라 토큰 재정의로 바꿉니다. 조사 기준 Project-Template(`6b1c739`)에는 이 패키지의 소비자가 없으므로 영향받는 소비자는 없습니다.

외부 프로젝트는 소스를 복사하지 않고 검토된 버전의 tarball을 고정해 소비합니다.

```sh
npm run build:ui
npm pack --workspace @hy-home/storybook-ui --pack-destination <소비 프로젝트의 vendor 경로>
# 소비 프로젝트: npm install ./vendor/hy-home-storybook-ui-0.2.0.tgz
```

소비 프로젝트의 lockfile이 tarball의 integrity hash를 기록합니다. 새 버전은 소비 프로젝트에서 tarball과 lockfile을 함께 바꾸고 해당 프로젝트의 UI 시험을 통과한 뒤 반영합니다.

## Related Documents

- [상위 Storybook 작업공간](../../README.md)
- [공유 Storybook 작업공간](../../../README.md)
