# Reading the gate DAG

Detail the skill body should not inline. `.github/workflow-contract.yml` owns
the gates themselves; this explains how to read it well enough to fill the
verdict table, and it defers to that file wherever the two could disagree.

## Shape

The contract is JSON with four parts that matter here.

- `gate_nodes` lists every gate. A node is a `leaf` (one entrypoint plus argv)
  or an aggregate that names ordered `children`.
- `public_gate.suite_roots` groups gates into the named suites a profile runs.
- `public_gate.validators` lists standalone validators outside the leaf tree.
- `workflows` maps the hosted jobs onto those suites.

## Turning it into rows

1. Resolve the profile the change requires. The
   [execution boundary](../../../governance/quality-standards.md#4-execution-boundary)
   owns which profiles may run locally; the contract owns what each contains.
2. Expand each suite root through its aggregates until only leaves remain. An
   aggregate is not a result; only its leaves produce one.
3. Give every expanded leaf a row. This is the step that makes an unrun gate
   visible, because the row exists before the result does.

## Reading a result honestly

- A leaf that exits zero is `PASS`.
- A leaf the profile did not select is `NOT_APPLICABLE`, not `PASS`.
- A leaf that a missing tool, absent credential, or unavailable runtime stopped
  is `BLOCKED`. It is the most frequently mislabelled case, because a blocked
  gate produces no failure output and reads like silence.
- A job that only exists in the hosted workflow is `REMOTE_ONLY` until its run
  is read back from the pull request.
- A leaf that was never invoked is `NOT_RUN`, whatever the reason.

## Why the distinction is load-bearing

A verdict that collapses these into pass and fail claims coverage the run never
had. This repository has already had a case where two local passes and a green
summary hid a required hosted check that had not run at all, so the shape above
keeps the categories apart rather than trusting the reader to remember them.
