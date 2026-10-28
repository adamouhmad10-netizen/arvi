# ARVI · Swiss Reserve — client presentation

Every image is a real capture of the working theme (Shopify Dawn 16.0.0), rendered from the local preview with
ARVI's own catalogue, copy and photography on 28 October 2026. No mock-ups, invented screens or stock imagery.
About 70% of the material is mobile.

## Files

| File | What it is | Use |
|---|---|---|
| **`ARVI-LUXURY-PRESENTATION.pdf`** | 15-page presentation, 16:9 (1920 × 1080), 6.4 MB | **Send this to the client** |
| `ARVI-MOBILE-OVERVIEW.png` | One board: 7 key phone screens (4800 × 2700) | Email body, cover image, social preview |
| `ARVI-DESKTOP-OVERVIEW.png` | Desktop board: homepage, brand story, product, collection (4800 × 3200) | Supporting image |
| `ARVI-RESPONSIVE-COMPARISON.png` | Desktop and phone side by side for homepage, product, collection (4800 × 2700) | Supporting image |
| `ARVI-MOBILE-SCROLL.mp4` | 35 s smooth scroll through the mobile homepage, hero to footer (780 × 1688, H.264) | Meeting or email attachment |
| `screenshots/mobile/` | 25 phone captures, 1170 × 2532 (390 pt at 3×) | Individual use |
| `screenshots/desktop/` | 11 desktop captures, 2880 × 1800 (1440 px at 2×), plus a full-page homepage | Individual use |
| `source/` | Board HTML, page renders (`source/pages/`) and JPEG copies used in the layouts | Rebuilding only |

## PDF contents
1. Cover
2. Mobile homepage: hero
3. Mobile navigation: menu and Wines submenu
4. Mobile homepage, scrolling I: regions, selection, proof, icons
5. Mobile homepage, scrolling II: boutiques, why ARVI, services, footer
6. Mobile footer and payments
7. Mobile product page: bottle and purchase
8. Mobile product details: facts and service, vintages, recommendations, price on request
9. Mobile collections: grid, cards, filter and sort
10. Responsive comparison: FAQ and boutiques, desktop and mobile
11. Desktop: full homepage
12. Desktop: header, navigation and hero
13. Desktop: product and collection
14. Desktop: brand story sections
15. Next steps

## Things to know before presenting
- **Payment logos.** The footer shows Shopify's official logos for the methods the store enables. Today that is
  **Visa and Mastercard**, as stated in ARVI's FAQ. American Express, TWINT and Apple Pay are not confirmed
  for ARVI, so they are not shown. They appear automatically once enabled in Shopify Payments (page 6 says so).
- **Critic scores** are not shown: they appear only after they are connected to ARVI's own metafields.
- **Cart and checkout** were not tested on Shopify (no store access); page 15 lists this as a pre-launch step.
- **URLs** in the browser frames read `arvi.ch` to show the intended domain. The screens were rendered locally, not on the live site.
- **Status bar.** The phone status bar ("9:41") is part of the frame, not the website.
- **PDF text.** The PDF pages are high-resolution images (2× the 16:9 page), so the text cannot be selected. The
  vector export rendered phone shadows as black boxes in Apple Preview.

## Rebuilding
With the preview running (`scripts/preview-restart.sh`):
```sh
python3 scripts/present_capture.py      # screenshots
python3 scripts/build_presentation.py   # PDF + boards
```
The MP4 was encoded with ffmpeg from 1,038 Playwright frames (30 fps, eased scroll).
