---
description: Create Next.js App Router project with TypeScript and best practices
---

1. **Initialize Next.js project**

    In your desired directory, create a new Next.js project with App Router, TypeScript, Tailwind CSS, and src directory.

    ```bash
    npx create-next-app@latest my-app --typescript --tailwind --app --src-dir --import-alias "@/*"
    cd my-app
    ```

    When prompted:

    - Would you like to use ESLint? **Yes**
    - Would you like to use `src/` directory? **Yes**
    - Would you like to use App Router? **Yes**
    - Would you like to customize the default import alias? **Yes** (@/*)

2. **Install recommended dependencies**

    Install commonly used packages for Next.js development based on agent/rules standards.

    // turbo

    ```bash
    npm install zod react-hook-form @hookform/resolvers
    npm install -D @types/node
    ```

3. **Create project structure**

    Set up the recommended directory structure according to `100-Frontend/130-frontend-next-general.md`.

    Create the following directories:

    ```bash
    mkdir -p src/components/{ui,forms,layout}
    mkdir -p src/lib/{utils,types,api}
    mkdir -p src/app/api
    ```

4. **Configure ESLint and Prettier**

    Create `.prettierrc` file with standard configuration:

    ```json
    {
      "semi": true,
      "singleQuote": true,
      "tabWidth": 2,
      "trailingComma": "es5"
    }
    ```

    Update `.eslintrc.json` to extend Next.js recommended config.

5. **Setup environment variables**

    Create `.env.local` file with template variables:

    ```bash
    # API
    NEXT_PUBLIC_APP_URL=http://localhost:3000

    # Database (if needed)
    # DATABASE_URL=

    # Auth (if needed)
    # NEXTAUTH_SECRET=
    # NEXTAUTH_URL=http://localhost:3000
    ```

    Add `.env.local` to `.gitignore` if not already present.

6. **Create initial components**

    Create a basic layout component in `src/components/layout/RootLayout.tsx` following Server Component patterns.

7. **Verify setup**

    Run the development server and verify the app loads without errors.

    // turbo

    ```bash
    npm run dev
    ```

    Open <http://localhost:3000> in your browser.

    Expected: Next.js welcome page loads successfully.

8. **Initialize Git (if not already done)**

    Initialize git repository and make initial commit.

    ```bash
    git init
    git add .
    git commit -m "chore: initialize Next.js project with TypeScript and Tailwind"
    ```

    **Next Steps:**

    - Review `agent/rules/100-Frontend/130-frontend-next-general.md` for App Router best practices
    - Review `agent/rules/100-Frontend/107-frontend-typescript-expert-specific.md` for TypeScript patterns
    - Consider setting up testing with `/vitest-testing` or `/jest-testing` workflows
