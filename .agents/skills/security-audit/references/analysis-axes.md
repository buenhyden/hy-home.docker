# The four axes of a read-only security analysis

Detail the skill body should not inline. The body names four axes; this says
what to look at on each and, for every one, the mistake that makes an audit
look complete when it is not.

## 1. Trust boundaries

Where does data or control cross from something less trusted to something more?
Network edges, container boundaries, volume mounts, and any place a value from
outside becomes an argument inside.

The mistake: treating a boundary as safe because a component behind it validates
its own input. The question is what crosses, not who checks afterwards.

## 2. Exposed inputs

Every value the change lets an outside party influence: request fields, headers,
filenames, environment variables read from an untrusted source, and the contents
of a mounted path.

The mistake: enumerating only the inputs the code obviously parses, and missing
the ones it passes through to a shell, a query, or a template.

## 3. Privileges

What can the changed component do that it could not do before? New capabilities,
a wider mount, a broader token scope, a service account gaining a role, a
container dropping a restriction.

The mistake: reading the grant and not the path. A privilege matters when
something reachable from an exposed input can use it.

## 4. Dependencies

What did the change pull in, and what does that transitively carry? Pinned or
floating, and whether the source is the one the project already trusts.

The mistake: checking the direct dependency and stopping. A floating transitive
pin is a supply-chain decision made by someone else, later.

## What this analysis never does

It reads. It does not exploit, does not call an external system, does not reveal
a secret value, and does not change a credential. A finding is described by its
mechanism and its evidence, never by demonstrating it.
