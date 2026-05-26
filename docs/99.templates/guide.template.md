---
title: "Guide Template"
status: draft
type: guide
stage: docs/05.operations/guides
template: docs/99.templates/guide.template.md
project: ""
linked_zk: []
lessons_extracted: false
stable_after: "[이 가이드가 안정적이라고 간주되는 조건 — 예: Spec v2.0 승인 후 / 구현 배포 후 30일 경과]"
---

<!-- Target: docs/05.operations/guides/####-<topic>.md -->

# [Topic Name] Guide

> Use this template for `docs/05.operations/guides/####-<topic>.md`.
>
> Rules:
>
> - This document explains how to do something or how to understand a system.
> - This document is not an operations policy.
> - This document is not a real-time incident response procedure.
> - If command order, rollback, or recovery is the primary purpose, write a Runbook instead.

---

## Overview (KR)

이 문서는 [주제]에 대한 가이드다. 특정 대상 독자가 작업을 이해하고 재현할 수 있도록 단계별 절차와 주의사항을 제공한다.

## Autonomous SDLC Contract

| Field                 | Value                                                                           |
| :-------------------- | :------------------------------------------------------------------------------ |
| Stage                 | `05.operations/guides`                                                          |
| Methodology Alignment | SDD knowledge transfer, operational enablement                                  |
| Upstream              | Spec, Plan, verified implementation, Operations policy                          |
| Downstream            | Runbook, onboarding, user/operator workflow                                     |
| Stage Exit Gate       | Audience, prerequisites, steps, pitfalls, and related source docs are explicit. |

## Stability Condition

> 이 가이드는 다음 조건이 충족될 때 안정(stable)으로 간주된다:
>
> - [ ] [조건 1 — 예: 연관 Spec이 approved 상태]
> - [ ] [조건 2 — 예: 구현이 배포되어 30일 이상 운영됨]
>
> 조건 미충족 시 `status: draft`를 유지한다.

## Guide Type

`onboarding | how-to | style-guide | troubleshooting-guide | system-guide`

## Target Audience

- Developer
- Operator
- Contributor
- Agent-tuner

## Purpose

[What this guide helps the reader achieve.]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]

## Step-by-step Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Common Pitfalls

- [Pitfall 1]
- [Pitfall 2]

## Verification

- **Procedure Dry Run**: [Who ran it / when / result]
- **Link Check**: [Cross-link validation command or evidence]
- **Stability Check**: [Draft or stable condition result]

## Content Publishing Checklist (blog-data)

> Include this section when the guide covers content authoring or publishing workflows.

- [ ] Public content frontmatter complete: `title`, `date`, `tags`, `draft`, `category`
- [ ] Content contract valid: `cd web && npm run validate:content-contracts` passes
- [ ] Post structure valid: `node web/scripts/validate-structure.mjs` passes when `content/posts` structure changed
- [ ] Internal links use repo-relative paths
- [ ] Images placed in `public/` or `content/` (not absolute paths)
- [ ] Vault cross-references use vault-relative paths
- [ ] Human approval recorded before changing public content `draft` to `false`

## Related Documents

> Replace each placeholder with a real target-relative link from the generated guide.
> If no real upstream exists, write `N/A - no upstream source`.
> If a required upstream is missing, write `Blocked - real upstream required`.

- **Spec**: Real target-relative spec link, or `N/A - no upstream source`
- **Operation**: Real target-relative operation policy link, or `N/A - no upstream source`
- **Runbook**: Real target-relative runbook link, or `N/A - no upstream source`

## SDLC/PARA Boundary & ZK Extraction

> [!NOTE]
> AI Agent는 SDLC 문서를 작성/수정할 때 `30_PARA/31_Projects/`를 필수 소유자, 링크 대상, 증적 저장소로 사용하지 않는다.
> `30_PARA/31_Projects/`는 사용자의 개인/업무 프로젝트를 관리하는 별도 Vault 영역이다.
> 작성 중 발견한 독립적인 지식, 패턴, 의사결정 기준만 `20_ZK/22_Permanent/` 또는 `20_ZK/23_Maps/`로 추출한다.

- **Extracted ZK Notes**:
  - `[Link to 20_ZK/...]`
