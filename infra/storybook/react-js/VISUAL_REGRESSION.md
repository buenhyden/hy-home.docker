# Visual Regression Testing

Visual Regression Testing ensures that UI changes (styling, layout) are intentional by comparing screenshots of components against a baseline.

## Recommended Tool: Chromatic

[Chromatic](https://www.chromatic.com/) is the official visual testing tool for Storybook and is highly recommended for its ease of use and zero-config setup.

### Setup

1. Sign up at Chromatic.com.
2. Install: `npm install --save-dev chromatic`.
3. Run: `npx chromatic --project-token=<your-token>`.

## Alternative: Local Dockerized Setup (Loki / Storycap)

If you prefer an open-source, infra-contained solution:

### Loki

1. Install: `npm install --save-dev loki loki-transform-to-story`.
2. Configure `loki.config.js` to target the static storybook build or docker container.
3. Run `npm run jest-loki` (requires Docker).

### Storycap + Reg-suit

1. **Storycap**: Crawls your Storybook and saves screenshots.
2. **Reg-suit**: Compares the screenshots and generates an HTML report.

## Implementation Status

Currently, this project provides the **build artifacts** (Storybook static build) that are compatible with any of these tools. We recommend **Chromatic** for the best developer experience or **Loki** for a strictly containerized pipeline.
