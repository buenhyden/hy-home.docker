---
description: Setup React/Vite frontend project with TypeScript, Tailwind, and tooling
---

1. **Create Vite project with React**

    Initialize new Vite project with React and TypeScript template.

    ```bash
    npm create vite@latest my-frontend-app -- --template react-ts
    cd my-frontend-app
    ```

    When prompted, select:
    - Framework: **React**
    - Variant: **TypeScript + SWC**

// turbo
2. **Install dependencies**

    Install base dependencies.

    ```bash
    npm install
    ```

// turbo
3. **Install Tailwind CSS**

    Setup Tailwind CSS for styling.

    ```bash
    npm install -D tailwindcss postcss autoprefixer
    npx tailwindcss init -p
    ```

    This creates `tailwind.config.js` and `postcss.config.js`.

4. **Configure Tailwind**

    Update `tailwind.config.js` with content paths.

    ```javascript
    /** @type {import('tailwindcss').Config} */
    export default {
      content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    }
    ```

    Update `src/index.css`:

    ```css
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    ```

// turbo
5. **Install development tools**

    Add ESLint, Prettier, and testing tools.

    ```bash
    # ESLint & Prettier
    npm install -D eslint prettier eslint-config-prettier eslint-plugin-react-hooks
    npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin

    # Testing
    npm install -D vitest @testing-library/react @testing-library/jest-dom
    npm install -D @testing-library/user-event @vitest/ui jsdom

    # Husky for git hooks
    npm install -D husky lint-staged
    ```

6. **Configure ESLint**

    Create `.eslintrc.cjs`:

    ```javascript
    module.exports = {
      root: true,
      env: { browser: true, es2020: true },
      extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:react-hooks/recommended',
        'prettier',
      ],
      ignorePatterns: ['dist', '.eslintrc.cjs'],
      parser: '@typescript-eslint/parser',
      plugins: ['react-refresh'],
      rules: {
        'react-refresh/only-export-components': [
          'warn',
          { allowConstantExport: true },
        ],
      },
    }
    ```

7. **Configure Prettier**

    Create `.prettierrc`:

    ```json
    {
      "semi": true,
      "singleQuote": true,
      "tabWidth": 2,
      "trailingComma": "es5",
      "printWidth": 80
    }
    ```

8. **Setup directory structure**

    Create recommended folder structure.

    ```bash
    mkdir -p src/{components,lib,hooks,store,types,assets}
    mkdir -p src/components/{ui,layout,forms}
    ```

    Final structure:

    ```
    src/
    ├── components/
    │   ├── ui/          # Reusable UI components
    │   ├── layout/      # Layout components
    │   └── forms/       # Form components
    ├── lib/             # Utilities (utils.ts, cn helper)
    ├── hooks/           # Custom React hooks
    ├── store/           # State management (Zustand)
    ├── types/           # TypeScript types
    ├── assets/          # Images, fonts
    ├── App.tsx
    ├── main.tsx
    └── index.css
    ```

9. **Create utility functions**

    Create `src/lib/utils.ts` with common utilities:

    ```typescript
    import { type ClassValue, clsx } from 'clsx';
    import { twMerge } from 'tailwind-merge';

    export function cn(...inputs: ClassValue[]) {
      return twMerge(clsx(inputs));
    }
    ```

    Install dependencies:

    ```bash
    npm install clsx tailwind-merge
    ```

10. **Configure Vitest**

    Create `vitest.config.ts`:

    ```typescript
    import { defineConfig } from 'vitest/config';
    import react from '@vitejs/plugin-react-swc';

    export default defineConfig({
      plugins: [react()],
      test: {
        environment: 'jsdom',
        globals: true,
        setupFiles: './src/test/setup.ts',
      },
    });
    ```

    Create `src/test/setup.ts`:

    ```typescript
    import { expect, afterEach } from 'vitest';
    import { cleanup } from '@testing-library/react';
    import * as matchers from '@testing-library/jest-dom/matchers';

    expect.extend(matchers);

    afterEach(() => {
      cleanup();
    });
    ```

11. **Setup package.json scripts**

    Add useful scripts to `package.json`:

    ```json
    {
      "scripts": {
        "dev": "vite",
        "build": "tsc && vite build",
        "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
        "lint:fix": "eslint . --ext ts,tsx --fix",
        "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
        "format:check": "prettier --check \"src/**/*.{ts,tsx,css}\"",
        "test": "vitest run",
        "test:watch": "vitest",
        "test:ui": "vitest --ui",
        "preview": "vite preview",
        "typecheck": "tsc --noEmit"
      }
    }
    ```

12. **Setup Husky git hooks**

    Initialize Husky and add pre-commit hook.

    ```bash
    npx husky init
    ```

    Create `.husky/pre-commit`:

    ```bash
    #!/usr/bin/env sh
    . "$(dirname -- "$0")/_/husky.sh"

    npx lint-staged
    ```

    Add to `package.json`:

    ```json
    {
      "lint-staged": {
        "*.{ts,tsx}": [
          "eslint --fix",
          "prettier --write"
        ],
        "*.{css,md}": [
          "prettier --write"
        ]
      }
    }
    ```

    // turbo
13. **Verify setup**

    Run all checks to ensure everything works.

    ```bash
    # Type check
    npm run typecheck

    # Lint
    npm run lint

    # Format check
    npm run format:check

    # Test
    npm test
    ```

    Expected: All checks pass.

    // turbo
14. **Run development server**

    Start the development server.

    ```bash
    npm run dev
    ```

    Open <http://localhost:5173> in browser.
    Expected: Vite + React app loads successfully.

15. **Initialize Git**

    Initialize git repository and make initial commit.

    ```bash
    git init
    git add .
    git commit -m "chore: initialize React + Vite project with TypeScript and Tailwind"
    ```

    **Next Steps:**
    - Review `agent/rules/100-Frontend` for React/TypeScript best practices
    - Add state management with `/workflow-*` if needed
    - Setup deployment (Vercel, Netlify) with `/workflow-deploy-check`
    - Add UI component library (shadcn/ui, MUI) if needed
