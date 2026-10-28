# ARVI — "Swiss Reserve" Shopify theme (Dawn 16.0.0)

A luxury redesign of ARVI SA's Shopify storefront, built as an Online Store 2.0 theme on official Shopify Dawn 16.0.0 (the same version as the WIP theme).

| Deliverable | Location |
|---|---|
| A. Installable theme | `theme/` (source) · `dist/arvi-swiss-reserve_dawn-16.0.0.zip` (upload package, git-ignored) |
| B. Research | `docs/RESEARCH-AUDIT.md`, `docs/CONTENT-INVENTORY.md`, `docs/CURRENT-VS-SHOPIFY.md`, `research/screens/` |
| C. Creative direction | `docs/CREATIVE-DIRECTION.md`, `presentation/concepts/direction-{A,B,C}.png` |
| D. Asset library | `assets-library/` (originals, optimized WebP + manifest, icons), `docs/ASSET-INVENTORY.md`, `docs/ASSET-LICENSES.md` |
| E. Visual presentation | `presentation/site/index.html` (published privately as a claude.ai artifact), `presentation/screens/`, `presentation/video/` |
| F. QA report | `docs/QA-REPORT.md`, `presentation/qa-*.json`, `presentation/theme-check.json` |
| G. SEO & performance | `docs/SEO-PERFORMANCE-REPORT.md`, `presentation/lighthouse/` |
| H. Maintenance guide | `docs/MAINTENANCE-GUIDE.md` |
| I. Preview & installation | `docs/INSTALL-PREVIEW.md` |
| J. Remaining requirements | `docs/REMAINING-REQUIREMENTS.md` |
| Refinement pass (v2) | `docs/REFINEMENT-PASS.md`, `presentation/screens/before/`, `presentation/screens/after/` |

Local preview: `node preview/server.mjs` → http://localhost:9292 (see INSTALL-PREVIEW.md).

Git history: commit `7097aaf` is unmodified upstream Dawn 16.0.0; every ARVI change sits on top of it, so `git diff 7097aaf -- theme` is the full customisation.

Nothing was uploaded to or changed on the Shopify store.
