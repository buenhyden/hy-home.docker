# React + Storybook Design System Infrastructure

This directory contains a complete **React Design System** environment powered by **Storybook**, **Vite**, and **Docker**. It is configured for library interaction testing, visual regression readiness, and automated CI/CD.

## 🚀 Features

- **React 19 + Vite**: Fast development and optimized library build.
- **Storybook 8**: Component isolation, documentation, and testing.
- **Interaction Testing**: Play functions and testing-library integration.
- **Accessibility (A11y)**: Automated WCAG compliance checks.
- **Theming**: Built-in support for Dark/Light mode visualization.
- **Figma Integration**: Design-to-code syncing via addons.
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

To package the components as a distributable library (UMD/ESM):

```bash
npm run build
```

Output will be in `dist/`.

## 🧪 Testing

### Interaction Tests

Run interaction tests via the test runner:

```bash
npm run test-storybook
```

### Visual Regression Testing

See [VISUAL_REGRESSION.md](./VISUAL_REGRESSION.md) for setup instructions (Chromatic or Loki).

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
- **Release**: Runs on push to `main`. Uses **Semantic Release** to determine version bump and publish.

## 📂 Project Structure

```text
.
├── .github/              # CI/CD Workflows
├── .storybook/           # Storybook Config (Addons, Preview)
├── src/                  # Component Source Code
│   ├── stories/          # Story Files (*.stories.js)
├── vite.config.js        # Vite & Library Config
├── docker-compose.yml    # Docker Services
└── package.json          # Dependencies & Scripts
```
