---
title: "Claude Provider Adapter"
version: "2.1.0"
type: "governance/provider"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: claude provider adapter
  layer: provider
updated: "2026-11-20"
runtime: "claude"
---

# Claude Provider Adapter

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the provider payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

Translate provider-neutral canonical governance into Claude Code syntax.

#### Loading

Root `CLAUDE.md` imports the shared
[bootstrap policy](../.agents/governance/bootstrap.md) and this authored adapter.
Load the active Spec Package and current Task when repository state changes.
Read the selected canonical role and procedure before acting.
Per the [Claude Code memory documentation](https://code.claude.com/docs/en/memory),
Claude Code reads `AGENTS.md` only where no `CLAUDE.md` sits on the path (its
default `claude-md-or-agents-md` mode), and the `instructionFiles` setting that
makes it read both is ignored in project settings. Root `CLAUDE.md` is on every
path here, so Claude does not read a folder `AGENTS.md` on its own. Each folder
that carries an `AGENTS.md` therefore also carries a generated `CLAUDE.md`
whose only content is the renderer marker comment, a heading and the import
`@AGENTS.md`. Claude loads a folder
`CLAUDE.md` on demand the first time it reads or writes a file below that
folder, and again on demand after compaction, so the guide reaches it
natively. The shared PreToolUse dispatcher (`scripts/hooks/agent-event-hook.sh`,
through `scripts/lib/hooks/folder_guides.py`) delivers guide content to
Claude only on an edit below a folder whose `CLAUDE.md` is missing or does not
import `@AGENTS.md`. Otherwise it adds a one-line reminder naming the nearest
folder guide on each edit, and after a SessionStart `compact` or `resume` an instruction to re-read
it. The bootstrap step that requires reading that guide applies when neither
route runs.
`.agents/knowledge/` and `.agents/prompts/` are canonical categories read
directly, in the order the bootstrap policy sets. Claude has no generated
projection of either, and their absence under `.claude/` is not a defect.

#### Native Controls

- `.claude/agents/` and `.claude/skills/` contain generated native adapters.
  Thin skill adapters point to `.agents/skills/<skill_id>/SKILL.md`; they do not
  copy procedure bodies or become a second authority.
- Generated Claude skill adapters set `disable-model-invocation: true` and are
  explicitly invoked. A discovered skill grants no additional tools or approval.
- Skills are generated adapter files, not symlinks to `.agents/skills/`. A
  symlink would load the canonical `SKILL.md` as is, without
  `disable-model-invocation: true`, so Claude could start a shared skill on its
  own, and the canonical file must stay provider-neutral. Codex needs neither,
  because it reads `.agents/skills/` directly.
- `.claude/settings.json`, `.claude/hooks/`, and `.claude/output-styles/` are
  native mechanics that route to shared policies and scripts. The `.claude/hooks/`
  wrappers are authored, not rendered. The Registry PreToolUse binding's
  `on_failure: block` is written `"onFailure": "block"` here; per the Claude
  Code documentation (2.1.295 or later) a hook that then times out denies the
  tool, which has not been observed. On Claude Code 2.1.327, a PreToolUse
  hook that exited 1 under this key was refused ("blocking because onFailure
  is \"block\""), while invalid JSON printed with exit 0 is not a failure
  and the tool ran, so the dispatcher must print a well-formed decision. The `permissions.deny` rules are native
  extra protection, not Registry translations: they back the
  [secret boundary](../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records),
  the [no-direct-push rule](../docs/00.workspace/03.process/github-governance.md#1-repository-protection-contract),
  and, for `docker system prune`, `docker compose down`, `docker volume rm`
  and `rm -rf`, the exact-target rule for live mutation and deletion in
  [approval boundaries](../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records),
  the [runtime mutation protocol](../.agents/governance/environment-constraints.md#21-approved-runtime-mutation-protocol)
  and the [pruning constraint](../.agents/governance/environment-constraints.md#2-infrastructure-constraints).
- This `provider.md` is an authored input. `.claude/README.md` and
  `.claude/CLAUDE.md` are generated pointers and never renderer inputs. Each
  folder `CLAUDE.md` beside a folder `AGENTS.md` is a generated import shim
  that `scripts/operations/provider_surface_renderer.py` writes, checks and
  retires with its guide.
- Provider/model selections and permission translations come only from the
  [Provider Registry](../.agents/governance/providers/registry.yaml).
- Generated files may adapt syntax but do not define shared policy, role intent,
  lifecycle, templates, model selection, or completion criteria. Canonical
  `.agents/` files are never generated, quarantined, or overwritten as outputs.
- Native memory is off through `autoMemoryEnabled: false` in
  `.claude/settings.json`; no `.claude/agents/*.md` sets `memory:`.
- The closing reminder is returned from `Stop`. Claude discards JSON output
  from `SessionEnd`, so this repository registers no reminder there. The
  `Stop` decision asks Claude to continue the turn. It does not record
  implementation acceptance or grant permission.

##### Selected restricted CLI review

Installed Claude Code2.1.329 supports a foreground review using the existing
account, with file tools confined to an owned disposable working directory.
The controller provides the review request on stdin and starts this command
in that directory:

```bash
claude --print --safe-mode --restricted --permission-mode dontAsk \
  --tools Read,Grep,Glob --allowedTools Read,Grep,Glob \
  --settings '{"permissions":{"deny":["Write","Edit","NotebookEdit","Bash","PowerShell","Agent"]}}' \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --setting-sources '' --disable-slash-commands --no-session-persistence \
  --model claude-opus-5-5 --effort high --output-format stream-json --verbose
```

The model/effort match the current Registry review selection; a flag does not
prove entitlement or runtime acceptance. Safe mode keeps normal authentication
and permissions while disabling user customizations, including auto-discovered
instruction files, installed plugins, hooks and custom agents. Built-in
plugins and admin-managed policy are not disabled by that claim. Restricted mode also
ignores user/project/local settings and confines file tools to the working
directories. Explicitly provide the canonical loading/role context. This fresh
CLI context is the independent reviewer; the routine route offers no Agent or
writer tool and also denies writer, command and Agent APIs in native policy.
Do not claim the disabled project agent was discovered or that a child review
occurred. Verify the actual offered tools and effective restrictions.
Do not use `--bare` as an authentication substitute: this installed version
would not read the existing OAuth account on that route.

Admin-managed settings and hooks still apply in safe/restricted mode; inspect
the effective sources without printing credentials. Empty strict MCP and the
explicit tool list address review-tool access, not the model provider's
necessary authentication traffic or a blanket whole-process network sandbox.
The shell sandbox alone also does not cover file tools, MCP or hooks. A
managed setting that prevents the planned restriction is a real prerequisite
or failure, never a reason to bypass that setting.

For a synthetic negative control only, a controller may offer the Write API
while applying a path-scoped native deny such as `Write(./**)` to the owned
source working directory with `dontAsk`. Catalog availability is not write
permission. Record the actual permission-denial event and unchanged dummy
hash; if Write is absent, or the call never occurs, do not report that as an
observed native write refusal. Keep this instrumented control distinct from
the generated inspection role's Read/Grep/Glob catalog. No control targets an
operating file or actual secret. An instrumented parent/child case proves only
its recorded catalog and permission configuration; it is not evidence that
the no-Writer/no-Agent routine route attempted a Write call. The routine
route's actual catalog and review need their own bounded observation. Keep
older2.1.326/327 witnesses and any current instrumented case at their original
scope, without silently relabelling them as this routine route's result.

Consume a required structured stream in memory and retain only the selected,
redacted permission witnesses and final review in the current Task; do not
write a raw session JSONL copy. The [workspace environment guide](../docs/00.workspace/05.environment/onboarding.md#independent-review-environment)
owns the finite case and cleanup. Installed help supports `--max-budget-usd`
in print mode, but no existing numeric per-call cap is known here; an estimate
is not a billing guarantee. Do not invent a `--max-turns` option from its
presence in bundled strings: installed help does not expose it. Use the
controller's bounded time and worker limits and record unobservable usage.

#### Limitations

Select checks through the [shared verification matrix](../docs/00.workspace/04.quality/quality-standards.md#5-change-type-verification-matrix)
and [completion checklist](../docs/00.workspace/04.quality/task-checklists.md#before-completion).
The shared policy and approved Task determine scope; this adapter adds no gate.
Hook behavior remains subject to shared policy and workflow-contract-owned public suites.
The [shared output contract](../.agents/governance/output-style.md) keeps
`FAIL`, `BLOCKED`, `SKIPPED`, `NOT_RUN`, partial results, and required
approval visible; this adapter cannot present any of them as completion.
Static configuration and renderer parity prove tracked configuration only; native
invocation, hook trust, entitlement, and runtime acceptance need direct evidence.
Do not change user-global or ignored local settings under this adapter's authority.

#### Related Documents

- [Canonical governance](../.agents/README.md)
- <https://code.claude.com/docs/en/sub-agents>
- <https://code.claude.com/docs/en/hooks>

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
