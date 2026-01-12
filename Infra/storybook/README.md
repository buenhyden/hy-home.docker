# Design System Infrastructure (Storybook)

This directory hosts the **Design System** and **Storybook** environment, providing ready-to-use templates for React library development.

## 📂 Templates

Two fully configured templates are provided for immediate use:

| Directory | Stack | Description |
| :--- | :--- | :--- |
| **`react-ts/`** | **TypeScript** + React 19 + Vite | **(Recommended)** Type-safe development with automated `.d.ts` generation. |
| **`react-js/`** | JavaScript + React 19 + Vite | Standard JavaScript setup for legacy compatibility or rapid prototyping. |

## 🚀 Key Features

Both templates share a robust, "Ultra-Lean" configuration:

* **⚡ Build System**: **Vite** Library Mode for high-performance builds and easy bundling.
* **🧩 Component Library**: Configured to export as `ESM` and `UMD` modules for consumption in other apps.
* **🧪 Interaction Testing**: Pre-configured with `@storybook/addon-interactions` and `play` functions to test component logic within the browser.
* **♿ Accessibility**: Automated A11y checks via `@storybook/addon-a11y` (WCAG compliance).
* **🎨 Theming**: Native support for Light/Dark mode toggles in Storybook toolbar.
* **🤝 Figma Integration**: `@storybook/addon-designs` installed for embedding Figma frames directly in documentation.
* **🚢 CI/CD**: GitHub Actions pipelines for:
  * **CI**: Linting, Building, Unit Testing, and Interaction Testing.
  * **Release**: Automated Semantic Versioning and NPM publishing via `semantic-release`.
* **🐋 Dockerized**: Multi-stage Dockerfile for optimizing static asset generation and serving via Nginx.
* **👀 Visual Regression**: Readiness for visual testing tools like **Chromatic** or **Loki** (see `VISUAL_REGRESSION.md`).

## 🛠 Infrastructure & Networking

The Docker container runs a static Nginx server hosting the build artifacts.

| Service | Image | Internal Port | Traefik Domain | Authentication |
| :--- | :--- | :--- | :--- | :--- |
| `storybook` | `design-system-storybook:latest` | `80` | `design.${DEFAULT_URL}` | SSO (Keycloak) |

### Networking

* **Network**: `infra_net`
* **IP Assignment**: Dynamic

## 📖 Usage Guide

### 1. Local Development

Choose your preferred flavor (`react-ts` recommended):

```bash
cd react-ts
npm install
npm run storybook
```

Access at `http://localhost:6006`.

### 2. Building for Production

To build the static Storybook site and the component library:

```bash
npm run build            # Builds library (dist/)
npm run build-storybook  # Builds documentation (storybook-static/)
```

### 3. Running with Docker

Deploy the selected template using Docker Compose:

```bash
cd react-ts
docker-compose up -d --build
```

This enables the Nginx server on port `6006`.

## 🔗 Reference Documentation

* [Figma Integration](./react-ts/FIGMA_INTEGRATION.md)
* [Visual Regression Testing](./react-ts/VISUAL_REGRESSION.md)
