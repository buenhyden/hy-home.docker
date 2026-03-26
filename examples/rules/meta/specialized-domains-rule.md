---
layer: meta
description: "Rule for containing specialized domain standards without polluting core scope governance."
---

# Meta — Specialized Domains Rule

## Case
- **[REQ-WEB3-01]** Keep Web3-specific standards isolated from generic frontend/backend rules.
- **[REQ-EXT-01]** Keep extension development concerns scope-contained.
- **[REQ-SCRAPE-01]** Keep scraping-specific risk controls explicit and separated.
- **[REQ-CM6-01]** Keep framework-specific editor rules isolated.

## Style
- **[PROC-EXT-01]** Reference specialized rules only when the task context requires them.
- **[REQ-MISC-06]** Prevent accidental inheritance of niche constraints in core workflows.
- **[BAN-EXT-01]** Avoid applying niche standards as default policy across unrelated scopes.

## Validation
- [ ] Specialized domains are documented with clear boundaries.
- [ ] Core scope rules do not depend on niche-only assumptions.
- [ ] Cross-references to specialized domains are intentional and minimal.
