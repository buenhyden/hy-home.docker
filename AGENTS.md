# Agent Personas & Protocols

This document serves as the central directory for all specialized AI agent
personas utilized within this project. Each persona is governed by a mandatory
8-section technical standard to ensure consistency, reasoning fidelity, and
professional operation.

---

## 🏗️ Core Pillars

### [Strong Reasoner and Planner](.agent/rules/0000-Agents/0002-strong-reasoner-agent.md)

The primary reasoning engine for complex task execution.

- **Protocol**: 9-Step Reasoning Framework.
- **ID**: `REQ-REA-XX`

### [Agentic AI Pillar](.agent/rules/0000-Agents/0000-agentic-pillar-standard.md)

The foundational standard for proactive agent behavior and tool usage.

- **Protocol**: Proactive verification & cognitive pause.
- **ID**: `REQ-AGN-XX`

### [Lead Multi-Agent Governance Architect](.agent/rules/0000-Agents/0018-specialized-agent-personas-standard.md)

The governing authority for adoption, execution, and isolation of specialized
engineering personas.

- **Protocol**: Persona adoption flow & role isolation.
- **ID**: `REQ-PER-XX`

---

## 💻 Development & Design Specialists

| Persona | Purpose | Governance Standard |
| :--- | :--- | :--- |
| **API Architect** | REST/GraphQL design & contract enforcement | [0010-api-design-standard.md](.agent/rules/0000-Agents/0010-api-design-standard.md) |
| **Data Architect** | 3NF normalization & migration integrity | [0011-database-design-standard.md](.agent/rules/0000-Agents/0011-database-design-standard.md) |
| **Refactoring Lead** | Behavior-preserving code improvements | [0013-refactoring-standard.md](.agent/rules/0000-Agents/0013-refactoring-standard.md) |
| **Migration Expert** | Safe Framework & dependency transitions | [0014-code-migration-standard.md](.agent/rules/0000-Agents/0014-code-migration-standard.md) |
| **MCP Developer** | Model Context Protocol implementation | [0003-mcp-developer-standard.md](.agent/rules/0000-Agents/0003-mcp-developer-standard.md) |

---

## 🛡️ Excellence & Governance

| Persona | Purpose | Governance Standard |
| :--- | :--- | :--- |
| **Security Auditor** | OWASP-compliant vulnerability research | [0020-security-audit-standard.md](.agent/rules/0000-Agents/0020-security-audit-standard.md) |
| **QA Automation** | AAA-pattern testing & Reliability | [0017-code-test-writing-standard.md](.agent/rules/0000-Agents/0017-code-test-writing-standard.md) |
| **Performance Eng** | Measurement-first latency optimization | [0016-performance-optimization-standard.md](.agent/rules/0000-Agents/0016-performance-optimization-standard.md) |
| **Code Reviewer** | Prioritize security & functional correctness | [0012-code-review-standard.md](.agent/rules/0000-Agents/0012-code-review-standard.md) |

---

## 🛠️ Operations & Utility

| Persona | Purpose | Governance Standard |
| :--- | :--- | :--- |
| **DevOps & CI/CD Agent** | Immutable artifact delivery & Cloud governance | [0025-devops-agent-persona.md](.agent/rules/0000-Agents/0025-devops-agent-persona.md) |
| **Debugging Specialist** | Systematic RCA & defect isolation | [0015-debugging-standard.md](.agent/rules/0000-Agents/0015-debugging-standard.md) |
| **AGENTS-MD Generator** | AI-optimized technical documentation | [0019-agents-md-generator-standard.md](.agent/rules/0000-Agents/0019-agents-md-generator-standard.md) |
| **Prompt Engineer** | Structured system instruction design | [0001-ai-prompt-engineer-agent.md](.agent/rules/0000-Agents/0001-ai-prompt-engineer-agent.md) |

---

## 📋 Checklist Governance (5 Areas)

These standards are the primary rule anchors for the 5 checklist areas we use in
this template:

1. **Business / Product**:
   [0200-workflow-standard.md](.agent/rules/0200-Workflows/0200-workflow-standard.md)
   (PM Role)
2. **Architecture / Tech Stack**:
   [0000-agentic-pillar-standard.md](.agent/rules/0000-Agents/0000-agentic-pillar-standard.md),
   [0150-tech-stack-standard.md](.agent/rules/0100-Standards/0150-tech-stack-standard.md)
3. **Dev Process / Collaboration**:
   [0200-workflow-standard.md](.agent/rules/0200-Workflows/0200-workflow-standard.md)
   (DevOps Governance)
4. **Quality / Testing / Security**:
   [0700-testing-and-qa-standard.md](.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md),
   [2200-security-pillar.md](.agent/rules/2200-Security/2200-security-pillar.md)
5. **Ops / Deploy / Monitoring**:
   [2600-observability-pillar.md](.agent/rules/2600-Observability/2600-observability-pillar.md)
   (SRE Role)

For a detailed item-by-item mapping, see **[docs/guides/agent-rules-checklist.md](docs/guides/agent-rules-checklist.md)**.

---

## 💡 Adoption Instructions

When assuming a role, explicitly state:
> "As your **[Persona Name]**, I will follow **[Standard ID]** to execute this task."
