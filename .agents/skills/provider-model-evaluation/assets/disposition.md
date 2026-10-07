<!-- Output shapes for the three results this skill names. Not stage documents:
     Stage 99 owns those. These exist because the skill previously named three
     outputs by identifier and defined none of them, which let a catalog row be
     reported as a live-model claim. -->

# sourced-model-disposition

| Field | Value |
| --- | --- |
| Model or profile | `<identifier exactly as the provider spells it>` |
| Proposed disposition | adopt / hold / reject |
| Official source | `<url>` |
| Retrieved | `<YYYY-MM-DD>` |
| Lifecycle stated by that source | `<the source's own words>` |

A disposition without a dated official source is `unverified`, and `unverified`
is a result, not a gap to fill in later.

# native-acceptance-verdict

| Boundary | State | Evidence |
| --- | --- | --- |
| Catalog presence | present / absent | `<where in the provider catalog>` |
| Native schema accepts the value | yes / no / `needs_revalidation` | `<schema fact>` |
| Entitlement | granted / absent / `needs_revalidation` | `<direct evidence, or why none>` |
| Runtime acceptance | accepted / refused / `needs_revalidation` | `<approved runtime observation>` |

Entitlement and runtime acceptance stay `needs_revalidation` unless a separately
approved runtime boundary supplied direct evidence. Catalog presence never
promotes either: a model can be listed, unentitled, and refused at once.

# regression-comparison

| Source or schema boundary | Baseline | Candidate | Evidence | Disposition |
| --- | --- | --- | --- | --- |
| `<scoped boundary>` | `<documented fact>` | `<documented fact>` | `<dated official source or native schema>` | unchanged / changed / unverified |

This manual comparison describes sourced or native-schema differences. It does
not execute a retired scoring fixture or create a recurring delivery gate.
Live quality, cost and latency remain unverified without a separately approved
observation.
