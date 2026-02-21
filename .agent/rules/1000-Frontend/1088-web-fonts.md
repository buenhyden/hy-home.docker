---
trigger: always_on
glob: "**/*.{css,html}"
description: "Web Fonts & Typography Standards: Enforces font loading optimization, subsetting, and accessible typography."
---

# Web Fonts & Typography Standards

- **Role**: Typography & Layout Specialist
- **Purpose**: Define standards for fast-loading, readable, and accessible web typography.
- **Activates When**: Configuring font faces, importing web fonts, or defining global typography styles.

**Trigger**: always_on — Apply during the setup of design systems and font assets.

## 1. Standards

### Principles

- **[REQ-FONT-01] Visibility First**
  - Text MUST be immediately visible during font loading (no invisible text).
- **[REQ-FONT-02] Layout Stability**
  - Proper font fallback strategies MUST be used to minimize layout shifts (CLS) during swap.
- **[REQ-FONT-03] Asset Efficiency**
  - Font files MUST be optimized (subsetting, WOFF2) to reduce total page weight.

### Format Priority

| Format | Support | Recommendation |
| --- | --- | --- |
| WOFF2 | Modern | **Primary Choice (30% smaller)** |
| WOFF | Legacy | Fallback |
| Variable Fonts | Modern | Preferred for multiple weights |

### Must

- **[REQ-FONT-04] CSS font-display**
  - Every `@font-face` declaration MUST include `font-display: swap`.
- **[REQ-FONT-05] Subsetting**
  - Fonts MUST be subset to only include required glyphs (e.g., Latin-1) for production assets.
- **[REQ-FONT-06] Semantic Sizing**
  - Typography MUST use relative units (`rem`, `em`) rather than absolute `px` for scalability.

### Must Not

- **[BAN-FONT-01] External JS Loaders**
  - Font loading MUST NOT depend on external JavaScript libraries (like WebFont Loader) unless legacy-required.
- **[BAN-FONT-02] Excessive Weights**
  - A single page MUST NOT load more than 3 different font families or 6 total weights.

### Failure Handling

- **Stop Condition**: Stop font integration if it increases LCP by more than 500ms.

## 2. Procedures

- **[PROC-FONT-01] Variable Transition**
  - IF a font has 3+ weights THEN MUST prefer using a single Variable Font file over multiple static files.
- **[PROC-FONT-02] Preload Audit**
  - Inspect the critical rendering path to ensure primary fonts are preloaded via `<link rel="preload">`.

## 3. Examples

### Optimized Font Face

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;
  font-weight: 100 900;
}
```

## 4. Validation Criteria

- **[VAL-FONT-01] Swap Verification**
  - [ ] Text is visible using system fallbacks during font load.
- **[VAL-FONT-02] Payload Accuracy**
  - [ ] Font files do not exceed 50KB per specific weight (subset).
- **[VAL-FONT-03] Contrast Compliance**
  - [ ] Typography meets WCAG AA contrast targets across all themes.
