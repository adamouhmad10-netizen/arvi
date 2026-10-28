# Functional QA Report

**Test environment:** macOS 12 (Intel). The theme was rendered by the local preview harness (`preview/`: LiquidJS 10.30 plus Shopify tag and filter shims) using real catalogue data captured from myarvi.myshopify.com. Browser checks ran in Playwright Chromium (build 1223). Tools: Shopify CLI 3.94.3 (`theme check`), axe-core 4.10.2, Lighthouse 12.2.1. Date: 28 Oct 2026.

> **What this does not cover:** the harness renders the real theme files, but it is not Shopify. The cart and checkout, the cart drawer's AJAX responses, predictive search, Search & Discovery filtering logic, customer accounts, apps, markets and language switching **were not tested end-to-end**. They need the theme uploaded to the store as an unpublished theme (see INSTALL-PREVIEW.md).

## Static checks
| Check | Result |
|---|---|
| `shopify theme check` | ✅ **0 errors**, 14 warnings. 11 are pre-existing upstream Dawn warnings. 3 are `OrphanedSnippet` false positives (`arvi-pdp-vendor`, `arvi-pdp-scripts`, `arvi-request-price` are rendered from Custom Liquid blocks in `templates/product.json`). Report: `presentation/theme-check.json` |
| Errors found and fixed during the build | Schema name over 25 characters (`arvi-collection-tiles`); invalid SVG markup in the icon snippet; font preload not using `preload_tag` |
| Package | `shopify theme package` → `dist/arvi-swiss-reserve_dawn-16.0.0.zip` (422 files, 4.4 MB) |

## Rendered checks (`scripts/qa_responsive.py`, `presentation/qa-responsive.json`)
7 pages × 6 widths (375, 390, 768, 1024, 1440, 1920): home, Champagne collection, Salon 1999 product page, Latour product page with a zero-priced variant, search "krug", FAQ, boutiques.
| Check | Result |
|---|---|
| Horizontal overflow (`scrollWidth − innerWidth`) | ✅ 0 px on all 42 combinations |
| Exactly one H1 per page | ✅ after fix (Dawn's homepage logo H1 is now opt-in) |
| Images without `alt` | ✅ 0 |
| Heading-level skips | ✅ 0, except the search page (upstream Dawn: H1 → H3 cards) and fixed ones on the FAQ and boutiques pages |
| Console errors | ✅ none (after stubbing `window.Shopify`, which real stores define) |

## Accessibility (axe-core, WCAG 2.0/2.1/2.2 A + AA rules, after full scroll)
✅ **0 violations on all 14 page/width combinations** (`presentation/qa-axe.json`).
Fixed during QA: product count contrast (3.0:1 → 5.4:1), unavailable vintage chips (2.8:1 → ≈5:1), muted text and hairlines on dark schemes (tokens re-scoped per colour scheme), the non-focusable announcement slider (now a single message), and Dawn 16's quantity input with no computable name (patched in `arvi-product.js`, not in core).
Manual: keyboard tab order and visible focus checked (`presentation/screens/a11y-focus-1440.png`). The age-gate `<dialog>` traps focus natively, Escape is blocked by design, and there is a "No" path. The mobile drawer and mega menu open via `<details>`/`<summary>`.

## Interaction checks (`scripts/shoot_interactions.py`)
| Interaction | Result |
|---|---|
| Age gate shows without cookie → "Yes" sets `arvi_age_ok=1` and removes the dialog | ✅ |
| Desktop mega menu (Wines) opens with 5 columns | ✅ `nav-mega-1440.png` |
| Mobile drawer and submenu | ✅ `nav-drawer-390.png`, `nav-drawer-sub-390.png` |
| Size + packaging selectors (WIP `arvi-variant-formato.js`) build from "Formato" and show "75 cl" labels | ✅ |
| Zero-priced variant → "Price on request", Add to cart hidden, enquiry button shown | ✅ `pdp-request-1440.png` |
| Sibling vintages (13 Salon vintages, sold-out states) | ✅ matches what the WIP theme renders |
| Filters show "75 cl" instead of "75.00" | ✅ display only; parameters unchanged |
| Search results grid | ✅ |

## Simulated data (disclosed)
- **Critic scores** on the product page come from the WIP theme's rendered data for that product. The harness fills the "Critic score" blocks as if the merchant had connected them to metafields, because the metafield keys could not be read without admin access.
- `arvi.alcol` and `arvi.nazione` are **assumed key names**. The confirmed keys are `annata`, `colore`, `regione` and `produttore`.
- The navigation menu is a mock that mirrors the WIP menu's handles. The live store's menus are used as-is.
- Payment icons in the footer are placeholders drawn by the harness.

## Known limitations / open items
- The mobile Lighthouse LCP target (≤ 2.5 s) **is not met in the local harness** (median 3.7–4.4 s). See SEO-PERFORMANCE-REPORT.md.
- Products without images render as a named empty niche (data issue).
- Long product titles with release notes (e.g. "Latour (Ex-Château) - Release 2023 2015") wrap to two lines; this is acceptable but would benefit from cleaner titles.
