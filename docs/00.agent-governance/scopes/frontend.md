---
layer: frontend
title: 'Frontend UI/UX Scope'
---

# Frontend UI/UX Scope

**Standardized implementation of responsive, accessible, and high-performance user interfaces.**

## 1. Context & Objective

- **Goal**: Delivery of premium, "WOW" factor user experiences with a focus on performance and inclusion.
- **Core Web Vitals**: Target LCP < 2.5s, CLS < 0.1, and FID < 100ms.
- **Standard**: Adhere to `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Stack**: 
    - **Framework**: Next.js 15+ (App Router), React 19+.
    - **Styling**: Tailwind CSS v4 (Modern Patterns), Framer Motion for animations.
    - **State**: TanStack Query (Server State), Zustand (Client State).
- **Accessibility**: Mandatory compliance with **WCAG 2.2 Level AA**.
- **Design System**: Use predefined design tokens; avoid ad-hoc utility hacks.

## 3. Implementation Flow

1. **Prototypes**: Verify design intent via `scripts/vibe-check.sh` or visual regression tools.
2. **Componentry**: Build modular, reusable components with strict TypeScript types.
3. **Validation**: Run `npm run lint` and `npm run build` before pushing to verify bundle optimization.

## 4. Operational Procedures

- **Local Development**: Use `npm run dev` for hot-reloading with integrated mocking (MSW) where applicable.
- **SEO**: Automatic title tags, meta descriptions, and semantic HTML structure on every page.

## 5. Maintenance & Safety

- **Visual Regression**: Use Playwright or similar for visual verification of UI changes.
- **Theming**: Support Dark Mode by default using Tailwind's `class` or `media` strategy.
