# Asset Inventory

## ARVI original assets (source: arvi.ch, publicly served)
Downloaded to `assets-library/arvi-original/`. Optimized WebP sets are in `assets-library/optimized/` (manifest: `manifest.json`) and copied into `theme/assets/`.

| Theme asset | Source file | Original size | Used in |
|---|---|---|---|
| `arvi-hero-autumn-{750,1100,1500,1874}.webp` | arvi.ch `/images/uploaded/Autumn_mobile2.png` (current campaign) | 1874×1406 | Homepage hero |
| `arvi-hero-autumn-wide-*` | `Autumn2.png` | 1920×480 | Spare wide banner |
| `arvi-cellar-*` | Shopify Files `AS_Background.png` (ARVI cellar) | 1920×1080 | Heritage section |
| `arvi-vault-*` | Shopify Files `WV_Background.png` | 1920×1080 | Spare (Wine Vault page) |
| `arvi-boutique-melano/lugano/zurich-*` | `Melano.png`, `Lugano.png`, `Zurigo.png` | 660×660 | Boutiques section/page |
| `arvi-wine-vault-detail-*` | `WV_01.png` | 600×660 | Services |
| `arvi-en-primeur-*` | `WIEP_660_01.png` | 600×660 | Services |
| `arvi-horeca-*` | `horeca_2.png` | 600×660 | Services |
| `arvi-events-table-*`, `arvi-events-*` | `Events_01.png`, `Events_Corporate.png` | 600×660 / 500×450 | Services |
| `arvi-consultant-*`, `arvi-bottles-*` | `Shops_01.png`, `AS_01.png` | 600×660 | Spare |
| Logo | Shopify Files `logoarvi.jpg` / `logoarvi_white.png` (3171×3525) | — | Header, age gate (referenced, not copied) |

Product photography is taken **from the Shopify catalogue at runtime**: transparent PNGs, 1500–1520×2000, served by the Shopify CDN with automatic WebP/AVIF. I created no product imagery.

## Quality notes and needs
- The boutique photos are only **660 px**. They look good at their current size (three columns, at most about 430 CSS px), but **high-resolution originals (≥ 2000 px) are needed** for larger editorial use or for a boutique hero.
- The hero campaign image is seasonal ("Hidden Treasures of Autumn"). The section is fully editable, with separate desktop and mobile images.
- 40 of the 250 sampled products have **no image** (e.g. Dom Pérignon 2013). The theme shows a quiet named niche; photography is needed.
- Several vintages reuse one vintage's bottle photo (e.g. Salon 2007 label shown for 2013/2015). The legal "illustrative image" note is kept on every product page.
- The producer images on arvi.ch (Pontet-Canet, Chavy-Chouet, Pavie) are not used because their usage rights are unclear.

## Icons
Lucide (lucide-static 0.460.0), 14 icons inlined in `snippets/arvi-icon.liquid`. Source SVGs and the licence are in `assets-library/icons/`.

## Fonts
Newsreader (Production Type, SIL OFL 1.1). Four woff2 subsets (latin and latin-ext, roman and italic) are in `theme/assets/`. Inter is served by Shopify's font library.
