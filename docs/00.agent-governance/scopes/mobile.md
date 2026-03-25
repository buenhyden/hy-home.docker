---
layer: mobile
title: 'Mobile Engineering Scope'
---

# Mobile Engineering Scope

**Development standards and patterns for React Native and cross-platform mobile applications.**

## 1. Context & Objective

- **Goal**: Delivery of performant, accessible, and high-quality mobile experiences using React Native/Expo.
- **Standards**: Priority on native-like feel and `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Stack**: React Native 0.74+, Expo 51+, TypeScript, Tamagui/Tailwind.
- **Performance**: Ensure 60fps for animations and transitions. Target < 2s TTI (Time To Interactive).
- **Accessibility**: Compliance with WCAG 2.2 Mobile Accessibility Guidelines.

## 3. Implementation Flow

1. **Design Alignment**: Review Figma designs and mobile-specific UX patterns.
2. **Component Build**: Use atomic design principles for reusable UI components.
3. **Navigation**: Implement nested navigation using Expo Router/React Navigation.
4. **State**: Use Zustand or TanStack Query for state and data management.

## 4. Operational Procedures

- **Testing**: Manual verification on both iOS and Android simulators/devices.
- **Builds**: Use Expo Application Services (EAS) for cloud builds and deployments.

## 5. Maintenance & Safety

- **Native Modules**: Minimize use of custom native modules; prefer Expo SDK libraries.
- **Secrets**: Handle API keys securely via environment variables and Expo Secrets.
