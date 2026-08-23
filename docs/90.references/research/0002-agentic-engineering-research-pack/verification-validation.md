---
status: draft
artifact_id: reference:agentic-engineering-research:verification-validation
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
review_cycle: on-source-change
---

# Reference: Verification and Validation System

## Overview

Verification and validation are related but non-interchangeable decision
disciplines. Verification asks whether an identified artifact conforms to its
requirements, design, contract, or required activity outputs. Validation asks
whether the resulting system, product, service, or evidence is adequate for
its intended use, stakeholder needs, and operational context.

This Stage 90 reference connects current official primary-source guidance to
tracked workspace owners at Task 9a baseline
`ac51a53211887a12bb18e2209aa3af1af6eb4b7f`. It is advisory analysis: it
creates neither a release gate nor authority to accept defects or residual
risk. A local green check is not, by itself, product validation or acceptance.

## Purpose

Satisfy REQ-36 by defining a source-backed V&V system that covers planning,
entry and readiness, success and completion, static and dynamic methods,
evidence and traceability, independence and risk-based depth, environments,
data and oracles, defect disposition, acceptance and decision authority,
residual risk, release acceptance, monitoring, and revalidation across all
fourteen workspace scopes.

The reference maps those concepts to exact tracked paths, commands, evidence
states, gaps, and runtime or authority limits. It prevents the invalid
substitution "tests or CI passed, therefore the product was validated and
accepted."

## Repository Role

This leaf owns the cross-system V&V model, evidence trace, and evidence-state
vocabulary. The supporting research leaves retain their detailed SDLC, QA,
workflow, metadata, generated-output, Compose, security, baseline, and scope
matrices.

Stages 01-03 own stakeholder intent, acceptance criteria, architecture, and
technical contracts. Stage 04 records observed implementation, checks,
reviews, defects, decisions, and commits. Stage 05 owns operations and real
release-event evidence. Runtime or remote claims require separately authorized
observation of the named target and time. This leaf does not adopt policy,
certify security, accept a provider, mutate remote state, or observe runtime.

## Scope

### In scope

- Systems, software, documentation, configuration, testware, generated
  artifacts, and release-candidate evidence.
- V&V plans, readiness criteria, declared oracles, success criteria, and
  completion evidence.
- Static and dynamic verification plus intended-use and stakeholder validation.
- Risk-based depth, graded independence, evidence traceability, defect and
  residual-risk decisions, monitoring, and revalidation.
- All fourteen normative workspace scopes, including explicit current
  not-applicable and `UNVERIFIED` boundaries.

### Out of scope

- Clause-level IEEE or ISO requirements not exposed by the public official
  routes. Licensed normative text was not accessed.
- Secret values, private provider state, Docker or Compose runtime execution,
  hosted GitHub observation, deployment, backup or restore, rollback, incident
  exercise, and Graphify refresh.
- Implementing a gap, approving a release, accepting residual risk, or changing
  policy, workflow, runtime, provider, lifecycle, or remote configuration.

## Definitions / Facts

### Terminology and non-substitution rules

- **Verification**: evidence that a named artifact or activity output conforms
  to a declared requirement, design, schema, rule, or oracle.
- **Validation**: evidence that the result is adequate for intended use,
  stakeholder needs, and the relevant operational context.
- **V&V**: coordinated verification and validation work with separate questions,
  evidence, and authorities where the risk requires them.
- **Static verification**: evaluation without executing the target, including
  requirements, design, review, lint, type, schema, provenance, and trace checks.
- **Dynamic verification**: execution against a declared oracle, including
  tests, fuzzing, smoke checks, and controlled deployment checks.
- **Acceptance**: an authorized decision that the identified candidate and its
  known evidence and risk are suitable for the declared handoff or use.
- **Oracle**: the explicit rule or expected result used to decide whether an
  observation succeeds.
- **Environment**: the versioned configuration, dependencies, data, resources,
  and execution context in which evidence was produced.
- **Independence**: separation between authoring, execution, review, and
  acceptance roles, graded according to consequence and risk.
- **Residual risk**: uncertainty or exposure remaining after V&V and defect
  treatment, accepted only by a named authority.
- **Revalidation**: repeating or extending validation after a change invalidates
  the scope, assumptions, environment, or evidence of an earlier decision.

This leaf reserves "validation" for intended-use or stakeholder adequacy.
Ordinary CI contract checks are verification gates unless an approved scenario,
representative context, oracle, and acceptance authority establish more.

### V&V planning and decision model

A V&V plan identifies the item and immutable candidate, the requirement or
expectation being evaluated, the method and risk-based depth, the required
independence, the environment/data/oracle, entry and exit criteria, the defect
route, durable evidence owner, acceptance authority, and revalidation triggers.

Planning must also state exclusions and uncertainty. If required authority,
representative data, environment fidelity, or an oracle is missing, the
relevant result is `UNVERIFIED`; a convenient substitute is not acceptable.

### Evidence trace

The minimum evidence chain is:

```text
requirement or stakeholder expectation
  -> identified artifact/candidate
  -> method and risk depth
  -> environment, data, and oracle
  -> observation/result
  -> defect disposition and repeated evidence where needed
  -> acceptance decision and residual risk
  -> monitoring and revalidation trigger
```

Every link names its owner. Metadata and human links support navigation, but
requirement IDs, candidate identity, exact commands, results, defect decisions,
review ranges, and runtime observations provide the decision trace.

### Methods and coverage

Static verification includes requirements/design/traceability inspection,
code and document review, lint/type/schema checks, static security and secret
pattern checks, dependency/SBOM/provenance review, and generated-output
comparison. Dynamic verification includes unit, integration, component, E2E,
black-box, structural, regression, fuzz, smoke, recovery, and deployment checks
when their environments and oracles are declared.

Validation methods include representative user or operator scenarios,
demonstrations, accessibility and usability acceptance, recovery exercises,
stakeholder decisions, and post-release observation. Coverage is adequate only
relative to the approved requirements, risks, environments, and exclusions; a
test count or percentage alone does not establish sufficiency.

### Risk-based depth and independence

Independence is graded rather than binary. Higher-consequence changes require
stronger requirement traceability, negative and adversarial cases, realistic
environments, independent review or execution, explicit residual-risk decisions,
and stronger release evidence. Self-review can find mistakes but cannot replace
a required independent reviewer or acceptance authority.

IEEE 1012-2024 publicly describes different integrity levels, but this
workspace does not claim a level: the licensed criteria were not accessed and
no local contract adopts one.

### Environments, data, and oracles

Evidence records the candidate revision, tool/dependency versions, relevant
configuration, and environment limits. Data should represent ordinary,
boundary, negative, and adversarial conditions without exposing secrets or
private data. Oracles must be deterministic enough to distinguish a product
failure from a test/procedure, environment, data, or oracle defect.

Reproducibility records uncertainty and flakes rather than retrying until green.
An environment mismatch narrows the claim; local results do not automatically
transfer to hosted CI, a provider runtime, a Compose deployment, or production.

### Entry, success, and completion criteria

Entry/readiness requires a baselined target, identifiable candidate, prepared
method, environment, data, oracle, known-risk statement, and required reviewer
or decision authority. Success means the observation meets the declared oracle
for that candidate and environment, not that every stakeholder need is met.

Completion requires every failure to be routed, defects to be corrected,
accepted, or deferred by the correct authority, invalidated checks to be
repeated, evidence to be durable, residual risk and skipped checks to be
explicit, and monitoring/revalidation triggers to be assigned. A partial pass
cannot silently satisfy the completion criteria.

### Defect disposition and residual risk

Classify whether a finding belongs to the product/artifact, test or procedure,
environment, data/oracle, or documentation/traceability. Route it to the
earliest canonical owner. A correction that changes the candidate, method,
environment, data, or oracle requires affected evidence to be repeated.

Deferral is not resolution. It records owner, impact, evidence, expiry or
trigger, and the named authority accepting the residual risk. The author of
this Stage 90 leaf cannot grant that acceptance.

### Workspace owner and evidence table

Counts below were remeasured from the Task 9a base and candidate on 2026-08-09;
historical leaf counts remain tied to their original commits.

| V&V area                                                                 | Canonical owner path(s)                                                                                    | Exact command or gate                                                                                                             | Re-measured result                                                                                                                                                  | Class                           | Current state or gap                                                                    | Runtime or authority limit                                                                                   |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Corpus and pack identity                                                 | Git index; both research-pack prefixes                                                                     | `git ls-files \| wc -l`; exact-prefix `git ls-files` counts                                                                       | Base 1,669; candidate 1,670; new 21; retiring 20                                                                                                                    | Verification                    | One safe tracked leaf added; retiring pack unchanged                                    | Path inventory only; no runtime implication                                                                  |
| Scope and catalog                                                        | `docs/00.agent-governance/scopes/*.md`; `docs/00.agent-governance/contracts/agent-catalog.yaml`            | sorted `git ls-files` plus complete YAML parse                                                                                    | 14 scopes; 8 catalog scopes; 14 agents; 24 functions; 11 fixtures; 16 regressions                                                                                   | Verification                    | Six normative scopes remain outside the typed enum and `architecture` remains enum-only | Catalog reachability is not provider execution                                                               |
| Stage/repository contracts                                               | `docs/00.agent-governance/`; Stage 99 profiles; `scripts/validation/check-repo-contracts.sh`               | `env PATH=/tmp/agentic-research-validation-venv/bin:$PATH bash scripts/validation/check-repo-contracts.sh`                        | PASS; `failures=0`                                                                                                                                                  | Verification                    | Aggregate repository contract passed in the isolated environment                        | Does not replace a named runtime or freshness gate                                                           |
| Stage/repository contracts, default interpreter (re-verified 2026-08-14) | same owner path                                                                                            | `bash scripts/validation/check-repo-contracts.sh` run directly in this session's default (non-isolated) interpreter at `ece3eda9` | FAIL; `failures=1`: `AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime` under Governance memory contract; every other subsection produced no failure | Verification                    | Environment-dependent result: identical gate, different interpreter, different outcome  | Confirms the pre-existing html5lib gap is environmental, not logical; does not itself install the dependency |
| Changed metadata                                                         | Stage 99 profiles; `scripts/validation/check-document-metadata.py`                                         | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref ac51a53211887a12bb18e2209aa3af1af6eb4b7f`  | PASS; selected 16, violations 0, legacy exceptions 0, transition overrides 0                                                                                        | Verification                    | Applies only to the changed/new registered documents                                    | Metadata validity is not content or product acceptance                                                       |
| Traceability and alignment                                               | `scripts/validation/check-doc-traceability.sh`; `scripts/validation/check-doc-implementation-alignment.sh` | both named scripts                                                                                                                | Trace predecessor 46/0; alignment predecessor 184; Task 9a attributable delta required to be 0                                                                      | Verification                    | The 184 inherited findings remain a predecessor, not a pass                             | Link alignment does not prove implementation/runtime behavior                                                |
| Workflow contract                                                        | `.github/workflow-contract.yml`; `scripts/validation/check-github-workflow-contract.py`                    | `python3 scripts/validation/check-github-workflow-contract.py` plus full YAML parse                                               | PASS: 7 workflows, 23 jobs, 8 actions; 80 nodes = 26 aggregate/48 leaf/6 setup; 16 job roots; 3 profiles                                                            | Verification                    | Tracked topology and strict static projection are implemented                           | No hosted run, required check, branch rule, or environment observed                                          |
| Typed gate runner                                                        | `.github/workflow-contract.yml`; `scripts/validation/ci_gate_{runner,contract,adapters}.py`                | `python3 scripts/validation/ci_gate_runner.py --profile <profile> --all --dry-run` or selected execution                          | Configured; not selected or executed by this docs unit                                                                                                              | Both/gap                        | Dry-run can verify topology; execution is environment-specific                          | Hosted selection/conclusion and release authority remain `UNVERIFIED`                                        |
| Pre-commit                                                               | `.pre-commit-config.yaml`; approved wrappers                                                               | scoped wrapper; controlled all-files wrapper only with separate approval                                                          | 10 configured repositories; not executed here                                                                                                                       | Both/gap                        | Configuration is reachable; no hook result claimed                                      | Hooks can modify files; controlled all-files evidence is separately approval-bound                           |
| LLM Wiki freshness                                                       | both `scripts/knowledge/generate-llm-wiki-*.sh` owners and outputs                                         | canonical write then both `--check` modes                                                                                         | Base 1,338/1,337; candidate 1,339 index rows/1,338 coverage paths                                                                                                   | Verification                    | Fresh only for the staged 1,670-path candidate                                          | Generated freshness does not prove content correctness or runtime discovery                                  |
| Security readiness                                                       | generator and `docs/90.references/data/security/security-automation-readiness.md`                          | `bash scripts/validation/generate-security-automation-readiness.sh --check`                                                       | PASS; 13 controls = 11 implemented/1 partial/1 gap                                                                                                                  | Verification                    | Broad dependency SCA remains the one gap                                                | Static tracked readiness is not a vulnerability assessment or security certification                         |
| Lifecycle contracts                                                      | target-surface and corpus-lifecycle owners                                                                 | named advisory and `check-*` modes                                                                                                | Reviewed pinned predecessor 9/26/9; Task 9a changes none of its selectors                                                                                           | Verification                    | Gate 9, deletion, and lifecycle reconciliation remain closed                            | Historical selectors cannot authorize deletion or a lifecycle transition                                     |
| Compose structure                                                        | `scripts/validation/validate-docker-compose.sh`                                                            | default structural check; `--preflight` only when authorized                                                                      | Not executed in this docs unit                                                                                                                                      | Both/gap                        | Static definitions have separate coverage/provenance checks                             | Live Docker, health, networks, ports, secrets, backup, and rollback stay `UNVERIFIED`                        |
| Compose coverage                                                         | coverage generator and snapshot                                                                            | `bash scripts/operations/generate-compose-profile-service-coverage.sh --check`                                                    | PASS; 48 total files/47 infra variants/168 entries/25 profiles                                                                                                      | Verification                    | Tracked variant declarations are fresh                                                  | Counts are not unique or running services                                                                    |
| Tech-stack provenance                                                    | `infra/tech-stack.versions.json`; provenance generator/snapshot                                            | `bash scripts/operations/generate-tech-stack-version-provenance.sh --check`                                                       | PASS; 18 components/21 images; 20 pinned/1 approved floating                                                                                                        | Verification                    | Declared provenance is fresh                                                            | No registry resolution, SBOM, signature, deployed-image, or runtime proof                                    |
| Hardening                                                                | `scripts/hardening/check-all-hardening.sh`; infra registries                                               | `bash scripts/hardening/check-all-hardening.sh`                                                                                   | PASS; 11 tier checks                                                                                                                                                | Verification                    | Selected repository assertions only                                                     | Not a live host/container posture certification                                                              |
| Template security                                                        | `scripts/validation/check-template-security-baseline.sh`; Stage 99                                         | `bash scripts/validation/check-template-security-baseline.sh`                                                                     | PASS; 46 Compose YAML files, 1 explicit exclusion, 0 missing adoption or required-control findings                                                                  | Verification                    | Path, placeholder, and secret-handling contract only                                    | No secret value was inspected                                                                                |
| Supply-chain fixture                                                     | supply-chain policy, generator, and focused tests                                                          | typed gates and focused sample-service tests                                                                                      | Configured sample scope; not executed by this leaf                                                                                                                  | Both/gap                        | Fixture rehearsal exists; release integration remains a gap                             | No signing, public Scorecard, provenance publication, or SLSA-level claim                                    |
| Frontend fixture                                                         | `projects/storybook/nextjs/`; typed CI adapters                                                            | lint/type/build/Storybook/coverage adapter gates                                                                                  | 51 tracked files, 3 stories, 6 TSX/JSX; not executed here                                                                                                           | Both/gap                        | Component fixture exists; product journey validation is absent                          | No product E2E, accessibility, or usability acceptance claimed                                               |
| Python validation tests                                                  | `tests/validation`; typed adapters                                                                         | exact selected `unittest` modules                                                                                                 | 26 test files; focused 1/1 and full module 4/4 passed after the intended RED                                                                                        | Both/gap                        | Selected tests only; shared Python lint/type/coverage remains incomplete                | Not full test discovery or product validation                                                                |
| Independent review                                                       | active Task and immutable committed ranges                                                                 | exact-range specification and quality reviews                                                                                     | Prerequisite `ac51a532` reviews Approved C0/I0/M0; implementation reviews pending                                                                                   | Validation of evidence adequacy | Review independence is enforced per logical commit                                      | Does not validate an unobserved product or runtime outcome                                                   |

### Who performs verification vs. validation in this workspace

The abstract distinction only earns its keep if it is bound to named
performers instead of left as a slogan. Re-surveyed directly at
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` on 2026-08-14:

- **Verification performers.** Every tracked automated gate this workspace
  runs — `scripts/validation/*.py`/`*.sh`, the 24 `.pre-commit-config.yaml`
  hooks, the typed `ci_gate_runner.py`/`ci_gate_contract.py` expansion, and
  the 24 `tests/validation/test_*.py` `unittest` modules — answers a
  verification question: does this artifact conform to its declared schema,
  contract, lint rule, type rule, or test oracle? None of them asks whether
  the result is adequate for a reader's or operator's intended use. This is
  not a gap in those tools; conformance checking is what they are for.
- **Validation performers.** No tracked script or CI job performs validation
  in this leaf's sense. The performers that do exist are human and
  procedural: the two independent quality reviewers named in the workspace
  owner/evidence table below (who judge whether re-derived evidence is
  adequate to support this leaf's claims, not merely whether a script
  exited zero); the Stage 01 requirement authors and Stage 04 Task
  reviewers, who judge whether an implementation serves its stated
  requirement; and, for research-pack leaves specifically, the reader who
  uses a leaf as a router — its adequacy for that reader's task is decided
  by the reader, not asserted by the document.
- **Where validation has no owner at all.** Three areas in this cluster
  currently have verification coverage and no validation owner: (1) whether
  the automation-pipeline leaf's promotion-path narrative actually helps an
  agent avoid a false "required check passed" claim in practice — no
  usability or task-success evidence exists, only conformance-to-source
  evidence; (2) whether the quality-ci-formatting leaf's five-state
  vocabulary changes agent behavior at the point of PR completion claims —
  same gap; (3) whether this leaf's own cross-cutting routing actually
  prevents the "tests/CI passed, therefore validated" substitution it names
  as invalid, for a real agent under real task pressure. Closing any of
  these requires observing agent behavior against a stated success
  criterion — a validation activity this Stage 90 leaf cannot itself
  perform, since it has no access to future agent runs.
- **This leaf's own evidence class.** Every count and command result in the
  table below that carries a 2026-08-14 date was independently re-derived by
  this Task, not copied from the Task 9a leaf text. That re-derivation is
  verification of this document against tracked sources. It is not
  validation of the leaf's usefulness to a downstream reader; that
  determination belongs to the reader, consistent with the non-substitution
  rule stated above.

### Evidence-state vocabulary

Use these states without collapsing them into one automatic ladder:

- `configured`: a tracked definition exists.
- `reachable`: the catalog, registry, or graph can route to it.
- `selected`: an execution plan chose the exact gate or target.
- `executed`: the named command ran in the recorded environment.
- `passed`: the execution met its declared oracle.
- `reviewed`: an independent reviewer evaluated the identified evidence range.
- `hosted`: a remote control-plane object or run exists.
- `enforced`: the named authority prevents nonconforming transitions.
- `runtime-observed`: the live target was directly observed at a recorded time.
- `UNVERIFIED`: required evidence is missing, inaccessible, unapproved, or
  outside the observed boundary.

A hosted job can exist without remote enforcement; a local pass can occur
without hosted execution; reviewed evidence can remain runtime-unobserved.

### Release acceptance and decision authority

Green CI is necessary only where an approved contract makes it necessary and
is never sufficient by itself. A release decision names the immutable artifact,
required checks and reviews, known-issue disposition, rollout/rollback/recovery
evidence, monitoring, residual risk, and human or downstream authority.

If the authority or required evidence is absent, release acceptance is
`UNVERIFIED`. A Stage 90 statement, successful generator, tracked Release
template, tag, or local check cannot supply the missing authority.

### Monitoring and revalidation

Revalidate when requirements, design, dependencies, runtime, environment,
threat model, reused-component context, acceptance authority, or source version
changes; after an incident, failed canary, telemetry anomaly, material defect,
or corrected test/data/oracle; and whenever monitoring shows the assumptions
behind an earlier decision no longer hold.

Monitoring evidence names target, metric or signal, interval, threshold,
owner, response, and retention. Tracked observability configuration is not a
runtime observation.

### Do not infer

- No provider behavior, entitlement, model availability, hook interception, or
  agent outcome is established.
- No branch protection, ruleset, required check, hosted workflow run,
  environment, or deployment enforcement was observed.
- No live Compose/container/network/port/volume/secret/backup/restore/SLO state
  was observed.
- No security certification, absence of vulnerabilities, or operational
  security acceptance is claimed.
- No release acceptance, deployment, rollback, recovery, or incident outcome
  is established.
- No generated artifact is fresh unless its named canonical `--check` ran
  against the recorded candidate path set.

## Scope Implications

| Scope          | Status                      | Required V&V emphasis                                                                                                                                                            |
| -------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Direct                      | Verify catalogs, prompts, tools, permissions, stop criteria, and evidence schemas; validate intended human handoff and task outcome; provider runtime remains `UNVERIFIED`.      |
| `architecture` | Direct                      | Verify requirement, ADR, ARD, Spec, interface, and quality-attribute traceability; validate against stakeholder constraints and operational concept.                             |
| `backend`      | Not applicable now          | No current backend product surface; define API, authorization, data, migration, error, load, and runtime acceptance only after an approved surface exists.                       |
| `common`       | Direct                      | Verify shared scripts, contracts, and conventions; validate that common rules reduce drift without erasing legitimate scope variation.                                           |
| `docs`         | Direct                      | Verify metadata, headings, links, templates, generated freshness, and traceability; validate intended reader tasks and maintenance decisions.                                    |
| `entry`        | Partial                     | Verify gateway, TLS, authentication, and routing configuration; edge reachability, certificates, log forwarding, and user ingress remain `UNVERIFIED`.                           |
| `frontend`     | Partial                     | Verify Storybook lint, type, build, component, and coverage evidence; product journey, accessibility, and usability validation are not established.                              |
| `infra`        | Direct, mostly verification | Verify Compose, configuration, network, volume, secret metadata, provenance, and hardening; live health, recovery, latency, backup, and rollback remain `UNVERIFIED`.            |
| `meta`         | Direct                      | Verify profiles, transitions, taxonomy, lifecycle, and generated inventories; validate usefulness for discovery and governance decisions.                                        |
| `mobile`       | Not applicable now          | No mobile source; require platform build, signing, device, accessibility, and user-context evidence after approved creation.                                                     |
| `ops`          | Partial                     | Verify Runbook, Incident, Release, monitoring, and rollback definitions; drills, service outcomes, MTTR, backup/restore, and release runtime remain `UNVERIFIED`.                |
| `product`      | Partial                     | Verify PRD acceptance criteria and traceability; stakeholder validation and acceptance remain with the human product authority.                                                  |
| `qa`           | Direct                      | Verify plan, environment, data, oracle, coverage, flakes, and results; validate suite sufficiency against approved risk and release decision.                                    |
| `security`     | Direct                      | Verify threat models, secure checks, approvals, supply-chain evidence, and redaction; residual-risk and operational-security acceptance require named authority and observation. |

## Sources

All required official routes were reopened at `2026-08-09T12:37:24Z`. Public
IEEE/ISO pages support only the displayed status and abstract-level material;
licensed normative clauses were not accessed.

| Source                                                                                                                                                                       | Class                                  | Supported fact                                                                                                                                                                                                                                 | Limitation                                                                                                                                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [IEEE 1012-2024](https://standards.ieee.org/ieee/1012/7324/)                                                                                                                 | External mutable official route        | Active V&V standard; public scope distinguishes conformance from intended use/user needs and lists analysis, review, inspection, assessment, and testing                                                                                       | Purchase/subscription route; no clause, integrity-level, or local-conformance claim                                                                                                                                                                                                                                                     |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)                                                                                                           | External mutable official route        | Edition 2, published 2026-04; full software lifecycle and concurrent/iterative/recursive application                                                                                                                                           | Public preview/abstract only; no purchased-clause or local-conformance claim                                                                                                                                                                                                                                                            |
| [IEEE/ISO/IEC 12207-2026](https://standards.ieee.org/ieee/12207/11416/)                                                                                                      | External mutable official route        | Active publication, published 2026-04-15, superseding 12207-2017                                                                                                                                                                               | Route and abstract only                                                                                                                                                                                                                                                                                                                 |
| [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/)                                                                            | External mutable official guidance     | Current official handbook route and systems-engineering context                                                                                                                                                                                | NASA guidance, not universal compliance authority                                                                                                                                                                                                                                                                                       |
| [NASA Product Realization](https://www.nasa.gov/reference/5-0-product-realization/)                                                                                          | External mutable official guidance     | Verification against design specifications, validation against stakeholder expectations, planning, evidence, and repeat logic                                                                                                                  | NASA-specific engineering framing                                                                                                                                                                                                                                                                                                       |
| [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final)                                                                                                     | External fixed official publication    | Secure-development practices integrated into SDLCs                                                                                                                                                                                             | Security/SDLC scope, not complete systems V&V or release acceptance                                                                                                                                                                                                                                                                     |
| [NIST SP 800-160 Vol. 1 Rev. 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)                                                                                           | External fixed official publication    | Trustworthy secure-systems engineering across the lifecycle                                                                                                                                                                                    | Security/trustworthiness context, not a replacement for IEEE 1012/12207                                                                                                                                                                                                                                                                 |
| [NISTIR 8397](https://www.nist.gov/publications/guidelines-minimum-standards-developer-verification-software)                                                                | External fixed official publication    | Minimum developer-verification techniques including static, black-box, structural, regression, fuzzing, and component review                                                                                                                   | Explicitly not the totality of software verification and not complete V&V                                                                                                                                                                                                                                                               |
| [GitHub status checks](https://docs.github.com/en/pull-requests/reference/status-checks)                                                                                     | External mutable official product docs | Check status/conclusion and skip/request semantics                                                                                                                                                                                             | Product capability only; this repository's hosted runs and required checks remain `UNVERIFIED`                                                                                                                                                                                                                                          |
| [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | External mutable official product docs | Review, check, merge, and deployment protection capabilities                                                                                                                                                                                   | Repository enforcement remains `UNVERIFIED` without authorized observation                                                                                                                                                                                                                                                              |
| [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)                                                         | External mutable official product docs | Workflow and job configuration semantics; route redirected to the current workflow-syntax reference                                                                                                                                            | Tracked workflow intent is not hosted execution                                                                                                                                                                                                                                                                                         |
| [NASA-STD-8739.8 Rev. B](https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/NASA-STD-87398-Revision-B_0.pdf)                                                  | External fixed official publication    | Software Assurance and Software Safety Standard, Revision B approved 2022-09-08, superseding Revision A; introduces Independent Verification and Validation (IV&V) as a distinct, separately resourced discipline from developer-performed V&V | Retrieved 2026-08-14: the PDF fetches (200, 680.7KB) but automated text extraction of clause-level content failed; the revision/date/IV&V-scope facts above are corroborated by a secondary technical summary, not read from the raw clause text, and require the same clause-level revalidation caveat as the licensed IEEE/ISO routes |

IEEE 1012-2016 and ISO/IEC/IEEE 12207:2017 are historical/superseded; they are
not cited as current authority. NASA-STD-8739.8 Revision A (2020) is
superseded by Revision B and is not cited as current NASA policy.

## Maintenance

Reopen mutable official routes and remeasure tracked owners whenever sources,
requirements, workflow contracts, scripts, tests, metadata, Compose, security
readiness, lifecycle contracts, generated path sets, or acceptance authority
change. Revalidate after every trigger listed above.

The documentation maintainer owns reference freshness, with independent QA,
security, architecture, infra/ops, and stakeholder review appropriate to the
claim. Preserve each baseline commit and historical count; add dated evidence
rather than rewriting an earlier observation into current state.

Needs revalidation: re-verification attempted on 2026-08-11 could not reach
[ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)
(`iso.org` returned HTTP 403 on three separate fetch attempts). The claim is
retained, not deleted, because the sibling official route
[IEEE/ISO/IEC 12207-2026](https://standards.ieee.org/ieee/12207/11416/)
independently corroborates the same edition, 2026-04-15 publication date, and
supersession of 12207-2017. Re-open the `iso.org` route directly (outside an
automated fetch tool) at the next scheduled review to confirm it still
resolves.

A second re-verification attempt on 2026-08-14 also could not reach
[ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)
(`iso.org` again returned HTTP 403, single automated attempt this session).
This is now two independently dated observations (2026-08-11 and 2026-08-14)
of the same automated-retrieval refusal; the claim remains retained under the
same IEEE-corroboration basis stated above, and the same manual, out-of-band
re-open recommendation still applies. The NASA-STD-8739.8 source added in
this pass (above) carries its own, separate revalidation caveat for the same
reason — a PDF fetch succeeding is not the same evidence class as reading its
normative clauses.

## Related Documents

- [Research pack index](./README.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [SDLC document roles](./sdlc-document-roles.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [LLM Wiki system](./llm-wiki-system.md)
- [Automation pipeline workflow](./automation-pipeline-workflow.md)
- [Quality, CI, and formatting](./quality-ci-formatting.md)
- [Docker Compose and infrastructure](./docker-compose-infrastructure.md)
- [Security governance](./security-governance.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
