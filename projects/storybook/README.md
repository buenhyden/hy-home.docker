# Design System Infrastructure (Storybook)

## Overview

This directory acts as the **Design System Monorepo** foundation, providing standardized templates for building, documenting, and testing React 19 component libraries. It uses **Storybook 8+** for UI development and **Vite** for high-performance builds.

```mermaid
graph LR
    subgraph "Design"
        Figma[Figma Assets]
    end
    
    subgraph "Development (Storybook)"
        Code[React Components]
        Docs[Documentation.mdx]
        Test[Interaction Tests]
    end
    
    subgraph "Output"
        Static[Static Site<br/>(Nginx)]
        Lib[NPM Package<br/>(ESM/UMD)]
    end
    
    subgraph "Production"
        App[Consumer App]
        GW[Traefik<br/>(design.${DEFAULT_URL})]
    end
    
    Figma -.-> Code
    Code --> Docs
    Code --> Test
    
    Docs --> Static
    Test --> Static
    
    Code --> Lib
    Lib --> App
    
    Static --> GW
```

## 📂 Project Templates

| Directory | Stack | Features | Recommended For |
| :--- | :--- | :--- | :--- |
| **[`react-ts/`](./react-ts)** | **TypeScript** + React 19 + Vite | Type generation (`d.ts`), Strict Mode | **New Projects** & Enterprise Apps |
| **`react-js/`** | JavaScript + React 19 + Vite | Babel setup, Loose typing | Rapid prototyping / Legacy migration |

## 🚀 Key Features

- **⚡ Vite Build**: Instant dev server start and optimized library bundling (ESM/CJS).
- **🧪 Interaction Testing**: Run user simulation tests (`play` function) directly in the browser via Storybook.
- **♿ Accessibility (A11y)**: integrated `addon-a11y` for strict WCAG compliance checks.
- **🎨 Theming**: Native Dark/Light mode support compatible with Tailwind or CSS Modules.
- **🤝 Figma Integration**: Embed live Figma design frames into component docs.
- **📦 Dual Export**: Builds both an interactive Documentation Site (`storybook-static/`) and a consumable Library (`dist/`).

## 🛠 Local Development via Docker

Each template includes a `docker-compose.yml` for isolated development.

```bash
cd react-ts

# Start Storybook on http://localhost:6006
docker-compose up -d --build
```

### Docker Services

| Service | Context | Internal Port | Host Port | Role |
| :--- | :--- | :--- | :--- | :--- |
| `storybook` | `./react-ts` | `80` (Nginx) | `6006` | Serves static build |

## 🚢 Production Deployment

To expose the Design System via the infrastructure's Traefik gateway (e.g., `https://design.${DEFAULT_URL}`):

1. **Build**: `npm run build-storybook` inside the container.
2. **Serve**: The Dockerfile uses Nginx to serve the `storybook-static` folder.
3. **Traefik Config**: Add the following labels to `docker-compose.yml`:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.storybook.rule=Host(`design.${DEFAULT_URL}`)"
  - "traefik.http.routers.storybook.tls=true"
  - "traefik.http.routers.storybook.middlewares=sso-auth@file" # Optional: Protect with Keycloak
```

## 🔗 Reference Documentation

- [Figma Integration Guide](./react-ts/FIGMA_INTEGRATION.md)
- [Visual Regression Testing](./react-ts/VISUAL_REGRESSION.md)

## 🪝 Git Hooks (Local)

Commit-time checks are available via a repo-level `pre-commit` hook that runs lint/format/markdownlint for Storybook templates touched by your staged files.

```bash
# Enable hooks for this repo
git config core.hooksPath .githooks
```

Notes:
- Run `npm install` in each template once so the checks can execute.
- Checks run only for `projects/storybook/react-js/` and/or `projects/storybook/react-ts/` when those paths are staged.

## File Map

| Path | Description |
| --- | --- |
| `react-ts/` | TypeScript Storybook template (Vite, Nginx, CI workflows). |
| `react-js/` | JavaScript Storybook template (Vite, Nginx, CI workflows). |
| `README.md` | Monorepo-level overview and usage notes. |
