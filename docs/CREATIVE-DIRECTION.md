# Creative Direction

Boards: `presentation/concepts/direction-A.png`, `direction-B.png`, `direction-C.png`. They are rendered from `presentation/concepts/boards.html` using real ARVI boutique photos and real catalogue bottles.

## Three directions explored

| | A — Swiss Reserve ✅ selected | B — Modern Connoisseur | C — Heritage Wine Maison |
|---|---|---|---|
| Idea | The Arvino oak gallery, translated: warm stone, ink, lit niches, one bronze accent | Gallery-white index, grotesk-only, product-first | Candle-lit cellar, oxblood, italic serif, antique gold |
| Palette | Stone #F5F3EE · Oak mist #EDE9E1 · Linen #DDD6C8 · Bronze #998A65 · Ink #1C1A17 | White · #F4F4F2 · Graphite #0D0D0D | #17110F · #3A1D19 · Parchment #EADFCB · Gold #B89A5E |
| Type | Newsreader (display, optical sizes) + Inter | Inter Tight only | Cormorant Garamond italic + Inter |
| Strength | Rooted in ARVI's own CSS tokens and the real boutiques; warm, legible, timeless | Fastest and most scalable for 19k SKUs | Dramatic heritage |
| Weakness | Needs good photography (mitigated by real boutique images and transparent bottle PNGs) | Loses ARVI's serif heritage and the boutiques' warmth; risks a generic DTC look | Contradicts the bright oak boutiques; gold-on-black is a category cliché; harder contrast compliance |
| Dawn fit | Colour schemes + one CSS layer | Excellent | Fine, but clashes with checkout and app UIs |

## Why A
1. **It comes from ARVI's own identity:** `#998a65` (main-gold), `#ebe7dd`, `#f5f4f0` and `#d6d0c1` are ARVI's production CSS tokens. I refined them rather than replaced them.
2. **It matches the stores customers actually visit.** Melano, Lugano and Zurich are pale oak with backlit bottle niches, black leather and brass pendants. They are not dark cellars. The product card is designed as a "lit niche".
3. **Typography lineage.** ARVI uses Minion Pro and Helvetica Neue. Newsreader (SIL OFL, self-hosted) and Inter (Shopify font library) are their open, web-optimised successors. I didn't use Minion or Helvetica because their web licences could not be verified.
4. **Restraint.** Bronze appears only in eyebrows, rules, icons and the cart count, never as gold everywhere.

## Design system (implemented in `theme/assets/arvi-base.css`)
- **Colour schemes** (theme editor): 1 Stone (default), 2 Oak mist (niches, alternating sections), 3 Ink (hero, Icons index, footer), 4 Cellar (spare dark), 5 White, 6 Linen.
- **Type scale (fluid, `clamp`):** XL 44→96 px, L 34→64 px, M 24→32 px, S 20→24 px, body 16 px/1.7, meta 13 px, micro 11 px tracked 0.14–0.18 em uppercase.
- **Spacing:** section rhythm S/M/L = 32–56 / 48–96 / 64–144 px. Gutters are 20 px mobile, 40 px tablet and 56 px desktop. Page width is 1400 px.
- **Components:** eyebrow + display heading header, underline arrow link, ink button (sharp corners), hairline lists, numbered index rows, niche product card (vendor → name → formats → price), facts list (`dl`), vintage chips, critic score.
- **Motion:** 240 ms ease-out transitions. There's a one-time hero settle (1.6 s), Dawn's scroll reveal (shortened to 24 px of travel), and a 1.03 image lift on hover. Nothing auto-plays. Under `prefers-reduced-motion` all motion is disabled.
- **Icons:** Lucide line icons (ISC) with a 1.25 stroke, used only where they carry meaning (boutique facts, values).
