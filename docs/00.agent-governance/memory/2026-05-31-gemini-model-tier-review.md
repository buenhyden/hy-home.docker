---
layer: agentic
---

# Memory: Gemini Model Tier Review (2026-05-31)

- Date: 2026-05-31
- Layer: agentic
- Status: active
- Applies To: `subagent-protocol.md` Model Policy (Gemini column), `providers/gemini.md`, `.agents/` reference surface
- Tags: #governance #quality #model-policy
- Retrieval Keywords: gemini model policy, gemini-3.5-flash, gemini-3.1-pro, gemini-3.5-pro, supervisor worker tier inversion
- Last Verified: 2026-05-31

## Problem

The shared Model Policy assigns Gemini as supervisor=`gemini-3.1-pro` and
worker=`gemini-3.5-flash` (`subagent-protocol.md:22-23`). A 2026-05-31 web
re-verification shows this tier ordering is now questionable: the designated
_worker_ model out-benchmarks the designated _supervisor_ model.

This is recorded as an advisory decision item only. The Claude and Codex tiers
were re-verified the same day and remain correct; no policy edit is made here
because the proper Pro-tier successor is not yet available.

## Context

Web verification (2026-05, US sources):

- `gemini-3.5-flash` released 2026-05-20 (Google I/O). It outperforms
  `gemini-3.1-pro` on coding/agentic benchmarks (Terminal-Bench 2.1, MCP Atlas,
  GDPval-AA) and is ~40% cheaper on both token axes.
- `gemini-3.5-pro` is delayed to June 2026 with no committed date, so there is no
  available 3.5-tier "Pro" model to promote into the supervisor slot yet.
- Claude `opus-4.8` (2026-05-28) / `sonnet-4.6` (2026-02-17) confirmed current.
- Codex `gpt-5.5` (2026-04-23) / `gpt-5.4-mini` confirmed current;
  `gpt-5.3-codex` remains a valid optional code-specialized worker override.

Scope of the originating task was "verify + fix real drift only; log non-enforced
gaps" — a non-Claude provider tier judgment is a log item, not a silent edit.

## Resolution

No Model Policy table change applied for Gemini. Fixed only the directly
contradictory stale reference in the governance agent catalog
(`agents/agents/workflow-supervisor.md:31`: `gemini-3-pro` → `gemini-3.1-pro`,
`gpt-5.1-codex` → `gpt-5.5`) to match the canonical table.

## Prevention

- Re-evaluate the Gemini supervisor/worker tier assignment once `gemini-3.5-pro`
  ships (forecast June 2026). Candidate outcome: supervisor=`gemini-3.5-pro`,
  worker=`gemini-3.5-flash`, retiring `gemini-3.1-pro`.
- Until then, treat the Gemini supervisor=`3.1-pro` slot as a known soft spot:
  for high-reasoning Gemini work, `gemini-3.5-flash` may be equal or better.
- When updating the Gemini tier, also re-sync `providers/gemini.md`, `GEMINI.md`,
  and the `.agents/` pointer surface, then re-run `check-repo-contracts.sh`.

## Evidence

- Web sources: Anthropic Opus 4.8 (TechCrunch, 2026-05-28); OpenAI GPT-5.5 /
  GPT-5.4-mini; Google Gemini 3.5 Flash (Google blog / MarkTechPost, 2026-05-20).
- Drift fix verified: stale-model grep returns no hits post-edit.
- `check-repo-contracts.sh` and `check-doc-traceability.sh` both `failures=0`.

## Related Documents

- [Memory README](./README.md)
- [Progress log](./progress.md)
- [Subagent Protocol (Model Policy SSOT)](../subagent-protocol.md)
- [Provider Capability Matrix](../rules/provider-capability-matrix.md)
- [Gemini Provider Notes](../providers/gemini.md)
