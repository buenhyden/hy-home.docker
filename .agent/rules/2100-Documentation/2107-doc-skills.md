---
trigger: model_decision
glob: [".agent/skills/**/SKILL.md", "agents_settings/agent/skills/**/SKILL.md"]
description: "Skills Standards: Guidelines for creating and packaging Agent Skills."
---

# 0870-Documentation-Skills

- **Role**: Skill Developer
- **Purpose**: Standardize `SKILL.md` format to ensure Agents can discover and use skills correctly.
- **Activates When**: Creating or editing Agent Skills.

## 1. Standards

### 1.1 Principles

- **[REQ-SKL-GEN-01] Modularity**: Skills MUST focus on a single capability.
- **[REQ-SKL-GEN-02] Discoverability**: `description` MUST clearly state _when_ to use the skill.
- **[REQ-SKL-GEN-03] Reliability**: Instructions MUST be deterministic.

### 1.2 Scope

- **In-Scope**: `SKILL.md` files, Skill directory structure.
- **Out-of-Scope**: Rules, Workflows.

### 1.3 Inputs & Outputs

- **Inputs**: Specialized tool/script.
- **Outputs**: Documented Skill Package.

### 1.4 Must / Must Not

- **[REQ-SKL-FMT-01] Frontmatter**: MUST include `name` and `description`.
- **[REQ-SKL-STR-01] Layout**: MUST follow `SKILL.md` + `scripts/` + `examples/` structure.
- **[BAN-SKL-CPX-01] No Complex Logic**: Instructions MUST NOT ask the agent to "think" too much; delegate to scripts.

## 2. Procedures

### 2.1 Skill Creation

1. **Create Folder**: `.agent/skills/<name>/`.
2. **Create SKILL.md**: Add frontmatter and instructions.
3. **Add Scripts**: Place executable logic in `scripts/`.
4. **Test**: Ask Agent to perform the task.

## 3. Examples

### 3.1 Standard SKILL.md

```markdown
---
name: code-review
description: Analyze code for style and security issues.
---

### Capabilities
- Linting
- Security Scan

### Instructions
1. Run `python scripts/analyze.py --path <target>`
2. Read the output report.
3. Summarize findings for the user.
```

## 4. Validation Criteria

- [ ] **[VAL-SKL-FMT-01]** YAML frontmatter exists.
- [ ] **[VAL-SKL-STR-01]** Detailed `Instructions` section exists.
- [ ] **[VAL-SKL-DSC-01]** Description clearly explains usage context.

## 5. References

- None.
