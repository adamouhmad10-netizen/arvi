# Preview & Installation

## A. Install on Shopify as an unpublished theme (recommended next step)
**Nothing has been uploaded to the store, and the live/published theme was not touched.** No hosted Shopify preview URL exists yet.

Option 1 — admin upload:
1. Shopify admin › Online Store › Themes › *Add theme* › *Upload zip file*.
2. Choose `dist/arvi-swiss-reserve_dawn-16.0.0.zip`. It is added as an **unpublished** theme.
3. *Customize* to review it, or use *Actions › Preview* to get a shareable preview link.

Option 2 — Shopify CLI (needs staff access to `myarvi.myshopify.com`):
```sh
cd theme
shopify theme push --unpublished --store myarvi.myshopify.com   # creates a new unpublished theme
shopify theme dev --store myarvi.myshopify.com                    # live-reload local development
```
Never use `--publish`, and never push to the theme ID of the live theme.

After upload:
- Assign templates: FAQ page → `page.faq`; *I nostri negozi* → `page.boutiques`.
- Check menus (`main-menu`; footer menus `footer-wines` and `footer` are referenced by the footer, so create or rename as needed).
- Connect the critic-score blocks to metafields (MAINTENANCE-GUIDE.md).
- Merge the WIP-only sections (see MAINTENANCE-GUIDE.md › Merging).

## B. Local preview (no store access needed)
Requirements: Node 18+ (a portable Node 22 is used here: `~/.local/node-v22.11.0-darwin-x64`), plus the dev dependencies in `.tooling/` (`liquidjs`).
```sh
cd .tooling && npm install liquidjs@10 && cd ..
node preview/server.mjs 9292        # or: scripts/preview-restart.sh
open http://localhost:9292/
```
Useful URLs:
- `/`
- `/collections/champagne`, `/collections/bordeaux`
- `/products/maison-salon-champagne-le-mesnil-1999`
- `/products/chateau-latour-ex-chateau-release-2023-2015?variant=59475133137244` (price on request)
- `/search?q=krug`, `/pages/faq`, `/pages/i-nostri-negozi`

Preview options (environment variables): `PREVIEW_PAYMENT_TYPES=visa,master,…` (default: the two methods verified in ARVI's FAQ) and `PREVIEW_SIMULATE_CRITICS=1` (fills critic blocks with data scraped from the WIP store, for layout checks only; off by default).

The harness needs the captured catalogue in `research/raw/shop/`. That folder is git-ignored; re-create it with `scripts/shopfetch.py` and the storefront password. Cart, checkout, accounts and filtering logic are not functional in the harness.

## C. Regenerate screenshots and QA
```sh
python3 scripts/shoot.py presentation/screens/home / 1440 390
python3 scripts/shoot_interactions.py
python3 scripts/qa_responsive.py
python3 scripts/qa_axe.py
```
