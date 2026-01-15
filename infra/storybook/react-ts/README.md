# React (TypeScript) + Storybook Design System Infrastructure

This directory contains a complete **React (TypeScript) Design System** environment powered by **Storybook**, **Vite**, and **Docker**. It is configured for type-safe library building, interaction testing, and automated CI/CD.

## 🚀 Features

- **React 19 + Vite (TS)**: Fast development with strict TypeScript support.
- **Type Definitions (`.d.ts`)**: Automated type generation using `vite-plugin-dts`.
- **Storybook 8**: Component isolation, documentation, and testing.
- **Interaction Testing**: Play functions and testing-library integration.
- **Accessibility (A11y)**: Automated WCAG compliance checks.
- **Figma Integration**: Design-to-code syncing.
- **CI/CD**: GitHub Actions for testing, linting, and semantic releases.
- **Dockerized**: Run the documentation site anywhere with Docker Compose.

## 🛠 Setup & Installation

```bash
# Install dependencies
npm install

# Start development server
npm run storybook
```

Storybook will open at `http://localhost:6006`.

## 📦 Building the Library

To package the components as a distributable library (ESM/UMD) with type definitions:

```bash
npm run build
```

Output will be in `dist/` including `index.d.ts`.

## 🧪 Testing

### Interaction Tests

Run interaction tests via the test runner:

```bash
npm run test-storybook
```

### Visual Regression Testing

See [VISUAL_REGRESSION.md](./VISUAL_REGRESSION.md) for setup instructions.

## 🐋 Docker Usage

To run the static Storybook documentation in a container:

```bash
# Build and Start
docker-compose up --build
```

Access at `http://localhost:6006`.

## 🎨 Integrations

- **Figma**: See [FIGMA_INTEGRATION.md](./FIGMA_INTEGRATION.md) for linking designs.
- **Theming**: Toggle background colors in the Storybook toolbar to test Light/Dark modes.

## 🔄 CI/CD & Release

- **CI**: Runs on Pull Request. Checks Lint, Build, and Tests.
- **Release**: Runs on push to `main`. Uses **Semantic Release** to publish to NPM/GitHub Packages.

## 📂 Project Structure

```text
.
├── .github/              # CI/CD Workflows
├── .storybook/           # Storybook Config (Addons, Preview)
├── src/                  # Component Source Code
│   ├── stories/          # Story Files (*.stories.tsx)
│   ├── index.ts          # Library Entry Point
├── vite.config.ts        # Vite & Library Config
├── tsconfig.json         # TypeScript Config
├── docker-compose.yml    # Docker Services
└── package.json          # Dependencies & Scripts
```
