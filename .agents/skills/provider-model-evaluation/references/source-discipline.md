# Source discipline for fast-moving provider facts

Detail the skill body should not inline. Model names, context limits, pricing,
and availability change without notice, so a fact about them is only as good as
its retrieval date.

## What counts as an official source

The provider's own documentation, catalog, or changelog. A blog post by the
provider counts. A summary elsewhere does not, however accurate, because the
next reader cannot tell when it was last true.

## Recording a fact

Every fast-moving fact carries its source URL and the date it was retrieved. A
fact without both is `unverified`. This is not bookkeeping: an undated fact and
a current fact are indistinguishable once written down, and the undated one is
the reason a stale model id survives a review.

## The four boundaries that get conflated

Keep these apart. Collapsing any pair is how a catalog row becomes a claim that
a model is usable here.

1. **Provider lifecycle** — what the provider says about the model's status.
2. **Repository disposition** — whether this repository chose to adopt it.
3. **Entitlement** — whether this account may call it.
4. **Runtime acceptance** — whether a call actually succeeded, under an approved
   runtime boundary.

A model can be generally available, adopted here, unentitled, and refused at
runtime simultaneously. Each boundary needs its own evidence.

## What may not be inferred

- Presence in a catalog does not imply entitlement.
- A configured default does not imply runtime acceptance.
- A synthetic fixture score does not imply quality, cost, or latency.
- Another model's entitlement does not extend to this one.

## When evidence is missing

Return the disposition as `unverified` and stop. Do not call a provider to find
out; that is a separately approved runtime action, and this procedure is
read-only by design.
