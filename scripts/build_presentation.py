"""Builds the ARVI client presentation from the real screenshots in docs/ARVI-CLIENT-PRESENTATION/screenshots/.
Outputs (in docs/ARVI-CLIENT-PRESENTATION/):
  ARVI-LUXURY-PRESENTATION.pdf, ARVI-MOBILE-OVERVIEW.png, ARVI-DESKTOP-OVERVIEW.png, ARVI-RESPONSIVE-COMPARISON.png
  source/ (HTML + JPEG copies used by the layouts), source/pages/ (one PNG per PDF page, for review)
Usage: python3 scripts/build_presentation.py"""
import asyncio, os, html
from PIL import Image
from playwright.async_api import async_playwright

ROOT = os.path.abspath('docs/ARVI-CLIENT-PRESENTATION')
SHOTS = f'{ROOT}/screenshots'
SRC = f'{ROOT}/source'
FONT_DIR = os.path.abspath('theme/assets')
os.makedirs(f'{SRC}/img', exist_ok=True); os.makedirs(f'{SRC}/pages', exist_ok=True)

meta = {}
def prep(rel):
    """JPEG copy for layout (keeps the PDF light) + status-bar colour sampled from the top of the screen."""
    src = f'{SHOTS}/{rel}'; name = rel.replace('/', '-').replace('.png', '.jpg')
    im = Image.open(src).convert('RGB')
    if not os.path.exists(f'{SRC}/img/{name}'):
        im.save(f'{SRC}/img/{name}', 'JPEG', quality=84, optimize=True, progressive=True)
    top = im.crop((0, 0, im.width, 6)).resize((1, 1)).getpixel((0, 0))
    lum = 0.2126 * top[0] + 0.7152 * top[1] + 0.0722 * top[2]
    meta[rel] = {'src': f'img/{name}', 'bar': '#%02x%02x%02x' % top, 'ink': '#fff' if lum < 140 else '#111', 'w': im.width, 'h': im.height}
    return meta[rel]

STATUS_ICONS = '''<svg viewBox="0 0 68 12" aria-hidden="true"><g fill="currentColor"><rect x="0" y="7" width="3" height="5" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/><rect x="10" y="2.5" width="3" height="9.5" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/><path d="M30 3.2a10 10 0 0 1 13 0l-1.4 1.5a8 8 0 0 0-10.2 0zm2.6 2.9a6 6 0 0 1 7.8 0l-1.5 1.5a4 4 0 0 0-4.8 0zm2.6 2.8a2 2 0 0 1 2.6 0L36.5 11z"/><rect x="47" y="1" width="18" height="10" rx="3" fill="none" stroke="currentColor" stroke-opacity=".45"/><rect x="49" y="3" width="13" height="6" rx="1.6"/><rect x="66" y="4.2" width="1.6" height="3.6" rx=".8" fill-opacity=".45"/></g></svg>'''

def phone(rel, w=300, caption=None, sub=None, cls=''):
    """iPhone-style frame (titanium bezel, Dynamic Island, iOS status bar) around a 390x844 capture."""
    m = prep(rel)
    bezel = round(w * 0.034); inner = w - 2 * bezel
    bar_h = inner * 47 / 390; img_h = inner * 844 / 390
    r_out = round(w * 0.158); r_in = r_out - bezel
    cap = ''
    if caption:
        cap = f'<figcaption><span class="cap-t">{caption}</span>' + (f'<span class="cap-s">{sub}</span>' if sub else '') + '</figcaption>'
    return f'''<figure class="ph {cls}" style="width:{w}px">
  <div class="ph-body" style="padding:{bezel}px;border-radius:{r_out}px">
    <div class="ph-screen" style="border-radius:{r_in}px">
      <div class="ph-bar" style="height:{bar_h:.1f}px;background:{m['bar']};color:{m['ink']};font-size:{inner*0.042:.1f}px">
        <span class="ph-time">9:41</span><span class="ph-island" style="width:{inner*0.31:.0f}px;height:{inner*0.088:.0f}px"></span><span class="ph-icons" style="width:{inner*0.17:.0f}px">{STATUS_ICONS}</span>
      </div>
      <img src="{m['src']}" alt="" style="height:{img_h:.1f}px">
    </div>
  </div>{cap}
</figure>'''

def browser(rel, w=760, caption=None, sub=None, url='arvi.ch', crop_h=None):
    m = prep(rel)
    img_h = w * m['h'] / m['w'] if not crop_h else crop_h
    cap = f'<figcaption><span class="cap-t">{caption}</span>' + (f'<span class="cap-s">{sub}</span>' if sub else '') + '</figcaption>' if caption else ''
    return f'''<figure class="br" style="width:{w}px">
  <div class="br-body"><div class="br-bar"><i></i><i></i><i></i><span class="br-url">{url}</span></div>
  <div class="br-view" style="height:{img_h:.0f}px"><img src="{m['src']}" alt=""></div></div>{cap}
</figure>'''

def page(n, title, eyebrow, body, lede='', dark=False, label='Mobile experience'):
    return f'''<section class="page{' dark' if dark else ''}">
  <header class="pg-head"><span>ARVI · Swiss Reserve</span><span>{label} — {n:02d}</span></header>
  <div class="pg-intro"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2>{f'<p class="lede">{lede}</p>' if lede else ''}</div>
  <div class="pg-stage">{body}</div>
</section>'''

CSS = f'''
@font-face {{ font-family: Newsreader; font-weight: 200 800; font-style: normal; src: url("file://{FONT_DIR}/arvi-newsreader-normal-latin.woff2") format("woff2"); }}
@font-face {{ font-family: Newsreader; font-weight: 200 800; font-style: italic; src: url("file://{FONT_DIR}/arvi-newsreader-italic-latin.woff2") format("woff2"); }}
:root {{ --stone:#F3F0EA; --mist:#E9E4DA; --ink:#1C1A17; --bronze:#998A65; --bronze-t:#6E6246; --muted:rgba(28,26,23,.62); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: var(--stone); }}
body {{ font-family: Inter, system-ui, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }}
@page {{ size: 1920px 1080px; margin: 0; }}
.page {{ width: 1920px; height: 1080px; position: relative; overflow: hidden; background: var(--stone); page-break-after: always; display: grid; grid-template-columns: 470px minmax(0, 1fr); grid-template-rows: auto minmax(0, 1fr); padding: 64px 96px 72px; column-gap: 72px; }}
.page.dark {{ background: var(--ink); color: #F2EEE6; --muted: rgba(242,238,230,.66); }}
.pg-head {{ grid-column: 1 / -1; display: flex; justify-content: space-between; font-size: 11px; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: var(--muted); padding-bottom: 22px; border-bottom: 1px solid rgba(28,26,23,.14); margin-bottom: 56px; }}
.dark .pg-head {{ border-color: rgba(242,238,230,.16); }}
.pg-intro {{ align-self: center; }}
.eyebrow {{ font-size: 11px; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: var(--bronze-t); margin-bottom: 22px; }}
.dark .eyebrow {{ color: #CDBF9C; }}
h1, h2 {{ font-family: Newsreader, Georgia, serif; font-weight: 300; letter-spacing: -.02em; }}
h2 {{ font-size: 46px; line-height: 1.08; max-width: 14ch; }}
.lede {{ font-size: 16px; line-height: 1.75; color: var(--muted); margin-top: 26px; max-width: 40ch; }}
.notes {{ margin-top: 34px; display: grid; gap: 14px; max-width: 40ch; }}
.notes p {{ font-size: 13.5px; line-height: 1.6; color: var(--muted); padding-left: 22px; position: relative; }}
.notes p::before {{ content: ''; position: absolute; left: 0; top: .75em; width: 12px; height: 1px; background: var(--bronze); }}
.notes b {{ color: var(--ink); font-weight: 500; }}
.dark .notes b {{ color: #F2EEE6; }}
.pg-stage {{ display: flex; align-items: center; justify-content: center; gap: 44px; min-width: 0; }}
figure {{ display: flex; flex-direction: column; align-items: center; }}
figcaption {{ margin-top: 22px; text-align: center; display: grid; gap: 6px; }}
.cap-t {{ font-size: 10.5px; font-weight: 500; letter-spacing: .18em; text-transform: uppercase; }}
.cap-s {{ font-size: 12.5px; color: var(--muted); }}
/* Phone */
.ph-body {{ position: relative; background: linear-gradient(150deg, #4a4743 0%, #1d1c1a 22%, #2a2825 60%, #45423e 100%); box-shadow: inset 0 0 0 1.2px rgba(255,255,255,.14), 0 0 0 1px #0b0a09, 0 44px 70px -34px rgba(48,36,22,.55), 0 18px 30px -20px rgba(0,0,0,.4); }}
.dark .ph-body {{ box-shadow: inset 0 0 0 1.2px rgba(255,255,255,.18), 0 0 0 1px #000, 0 40px 80px -30px rgba(0,0,0,.8); }}
.ph-body::before, .ph-body::after {{ content: ''; position: absolute; width: 3px; border-radius: 2px; background: #2b2926; }}
.ph-body::before {{ left: -3px; top: 21%; height: 9%; box-shadow: 0 60px 0 #2b2926; }}
.ph-body::after {{ right: -3px; top: 27%; height: 14%; }}
.ph-screen {{ overflow: hidden; background: #000; position: relative; }}
.ph-screen img {{ display: block; width: 100%; object-fit: cover; object-position: top; }}
.ph-bar {{ position: relative; display: flex; align-items: center; justify-content: space-between; padding: 0 8.5% 0 11%; font-weight: 600; letter-spacing: .01em; }}
.ph-island {{ position: absolute; left: 50%; top: 62%; transform: translate(-50%, -50%); background: #000; border-radius: 999px; }}
.ph-icons svg {{ width: 100%; display: block; }}
/* Browser */
.br-body {{ border-radius: 12px; overflow: hidden; background: #fff; box-shadow: 0 0 0 1px rgba(28,26,23,.1), 0 40px 70px -34px rgba(48,36,22,.45); }}
.br-bar {{ height: 34px; display: flex; align-items: center; gap: 7px; padding: 0 14px; background: #ECE8E1; border-bottom: 1px solid rgba(28,26,23,.08); }}
.br-bar i {{ width: 10px; height: 10px; border-radius: 50%; background: #D3CCC0; }}
.br-url {{ margin: 0 auto; transform: translateX(-20px); font-size: 11px; color: rgba(28,26,23,.55); background: #F6F3EE; padding: 4px 70px; border-radius: 6px; letter-spacing: .02em; }}
.br-view {{ overflow: hidden; }}
.br-view img {{ display: block; width: 100%; }}
/* Special layouts */
.cover {{ grid-template-columns: minmax(0, 1fr) 640px; }}
.cover h1 {{ font-size: 76px; line-height: 1.02; margin-top: 6px; }}
.cover .lede {{ font-size: 18px; max-width: 34ch; }}
.cover .meta {{ margin-top: 64px; display: flex; gap: 48px; font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: rgba(242,238,230,.6); }}
.strips {{ display: flex; gap: 28px; align-items: flex-start; }}
.strip {{ width: 300px; height: auto; max-height: 820px; overflow: hidden; border-radius: 8px; box-shadow: 0 0 0 1px rgba(28,26,23,.1), 0 30px 60px -30px rgba(48,36,22,.4); background: #fff; }}
.strip img {{ display: block; width: 100%; }}
.detail {{ width: 520px; border-radius: 10px; overflow: hidden; box-shadow: 0 0 0 1px rgba(28,26,23,.1), 0 30px 60px -30px rgba(48,36,22,.4); }}
.detail img {{ display: block; width: 100%; }}
.pair {{ display: flex; align-items: flex-end; gap: 0; position: relative; }}
.pair .ph {{ margin-left: -96px; margin-bottom: -18px; position: relative; z-index: 2; }}
.stack {{ display: grid; gap: 30px; }}
.closing ul {{ list-style: none; display: grid; gap: 18px; margin-top: 8px; }}
.closing li {{ font-size: 15px; line-height: 1.6; color: rgba(242,238,230,.8); padding-left: 26px; position: relative; max-width: 52ch; }}
.closing li::before {{ content: ''; position: absolute; left: 0; top: .8em; width: 14px; height: 1px; background: #CDBF9C; }}
.closing h3 {{ font-family: Newsreader, serif; font-weight: 300; font-size: 28px; margin-bottom: 22px; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 96px; align-self: center; }}
'''

M = lambda f: f'mobile/{f}.png'
D = lambda f: f'desktop/{f}.png'

def pdf_pages():
    P = []
    # 1 Cover
    P.append(f'''<section class="page dark cover">
  <header class="pg-head"><span>ARVI · Swiss Reserve</span><span>Client presentation — October 2026</span></header>
  <div class="pg-intro"><p class="eyebrow">Shopify Dawn · Mobile-first redesign</p>
    <h1>ARVI<br>Swiss Reserve</h1>
    <p class="lede" style="color:rgba(242,238,230,.72)">A mobile-first storefront for fine and rare wines: calm, editorial and built entirely on Shopify's Dawn theme.</p>
    <div class="meta"><span>Melano</span><span>Lugano</span><span>Zurich</span></div></div>
  <div class="pg-stage" style="gap:40px">{phone(M('04-home-cellar'), 300)}{phone(M('07b-home-boutiques-rail'), 300, cls='lift')}</div>
</section>''')
    # 2 Hero
    P.append(page(2, 'A first screen that sets the tone', 'Mobile homepage · Hero',
        phone(M('01-home-hero'), 360, 'Homepage, first screen', 'Campaign image, serif headline, one clear action'),
        'On a phone the campaign photograph leads, followed by ARVI’s promise and a single primary action. Prices in CHF and pick-up in Melano are stated before anything else.'
        + '''</p><div class="notes"><p><b>Real content.</b> ARVI's own autumn campaign and copy; nothing invented.</p><p><b>Keeps the bottle in frame.</b> The mobile crop is a theme-editor setting, not a fixed image.</p><p><b>Logo, search, account and cart</b> stay within thumb reach.</p></div><p style="display:none">'''))
    # 3 Navigation
    P.append(page(3, 'Navigation that reads like a wine list', 'Mobile navigation',
        phone(M('12-nav-menu'), 330, 'Main menu', 'Serif entries, generous rows') + phone(M('13-nav-wines'), 330, 'Wines', 'By type, France, Italy, Europe & New World'),
        'The menu uses the same serif as the editorial pages, with full-width rows that are easy to tap. Wines opens into the cellar\u2019s structure: type, country, region.'))
    # 4 Journey I
    P.append(page(4, 'From regions to the cellar', 'Mobile homepage · Scrolling I',
        phone(M('02-home-regions'), 252, 'Regions', '1,742 to 16,792 references each') + phone(M('03-home-selection'), 252, 'Selection', 'Swipe through Champagne') + phone(M('05-home-quote'), 252, 'Proof', '30+ years · 10,000+ labels') + phone(M('06-home-producers'), 252, 'Icons', 'Pétrus, Ausone, Lafite…'),
        'The homepage reads as one story: where the wines come from, a curated selection, the cellar behind them, and the estates that define fine wine.'))
    # 5 Journey II
    P.append(page(5, 'Three boutiques, one house', 'Mobile homepage · Scrolling II',
        phone(M('07-home-boutiques'), 252, 'Boutiques', 'Melano, Lugano, Zurich') + phone(M('08-home-values'), 252, 'Why ARVI', 'Compact two-by-two') + phone(M('09-home-services'), 252, 'Services', 'Vault, En Primeur, Horeca, Events') + phone(M('10-footer-top'), 252, 'Footer', 'Brand, menus side by side'),
        'Long lists become horizontal rails on the phone, so the boutiques, services and selections never turn into an endless stack. The mobile homepage is 26% shorter than in the first build.'))
    # 6 Footer & payments
    m11 = prep(M('11-footer-payments'))
    im = Image.open(f'{SHOTS}/{M("11-footer-payments")}').convert('RGB')
    y = int(im.height * 0.862); crop = im.crop((0, y, im.width, im.height))
    crop.save(f'{SRC}/img/payment-detail.jpg', 'JPEG', quality=92)
    P.append(page(6, 'Closing with confidence', 'Mobile footer · Payments',
        phone(M('11-footer-payments'), 330, 'Footer, end of page', 'Language, payments, legal')
        + f'<figure><div class="detail"><img src="img/payment-detail.jpg" alt=""></div><figcaption><span class="cap-t">Payment row, detail</span><span class="cap-s">Shopify’s official logos at their native proportions</span></figcaption></figure>',
        'Payment logos are Shopify’s own official artwork and follow the store’s payment settings automatically.'
        + '''</p><div class="notes"><p><b>Shown today:</b> Visa and Mastercard, the methods ARVI’s FAQ confirms for online payment.</p><p><b>American Express, TWINT and Apple Pay</b> appear here automatically once enabled in Shopify Payments. They are not shown before that, so nothing is misrepresented.</p></div><p style="display:none">'''))
    # 7 Product
    P.append(page(7, 'The bottle, then the decision', 'Mobile product page',
        phone(M('14-product-hero'), 330, 'Product', 'Full bottle, never cropped') + phone(M('15-product-buy'), 330, 'Purchase', 'Price in CHF, size, packaging, Add to cart'),
        'The packshot sits on the same warm stone as the rest of the site. Size and packaging come from ARVI’s own catalogue options, presented as “75 cl” and “Single bottle”.'))
    # 8 Product details
    P.append(page(8, 'Details a collector expects', 'Mobile product details',
        phone(M('16-product-facts'), 252, 'Facts & service', 'Vintage, origin, alcohol; delivery') + phone(M('17-product-vintages'), 252, 'All vintages', 'Available, sold out, viewing') + phone(M('18-product-recommendations'), 252, 'You may also like', 'Other wines, never repeats') + phone(M('19-product-price-on-request'), 252, 'Price on request', 'Enquiry instead of a CHF 0.00 price'),
        'Every fact is read from ARVI’s product data. Critic scores appear only once they are connected to ARVI’s own metafields: nothing is shown without real data.'))
    # 9 Collections
    P.append(page(9, 'Browsing 10,000 labels on a phone', 'Mobile collections',
        phone(M('20-collection-top'), 300, 'Collection', 'Title, count, filter & sort') + phone(M('21-collection-grid'), 300, 'Product cards', 'Producer, name, formats, price') + phone(M('22-collection-filters'), 300, 'Filter & sort', 'Size, vintage, region, colour, producer'),
        'Two-column cards keep the bottle prominent. Wines without a photograph get a designed placeholder instead of an empty tile, and the title always stays visible.'))
    # 10 Responsive comparison
    P.append(page(10, 'One design, every screen', 'Responsive comparison',
        f'<div class="stack"><div class="pair">{browser(D("11-faq"), 480, url="arvi.ch/pages/faq")}{phone(M("23-faq"), 176)}</div><p class="cap-s" style="text-align:center">FAQ · desktop and mobile</p></div>'
        + f'<div class="stack"><div class="pair">{browser(D("10-boutiques-page"), 480, url="arvi.ch/pages/our-shops")}{phone(M("24-boutiques-page"), 176)}</div><p class="cap-s" style="text-align:center">Boutiques · desktop and mobile</p></div>',
        'The same sections adapt rather than shrink: two columns become one, rows become rails, and type scales fluidly between 375 and 1920 pixels.'))
    # 11 Desktop full homepage
    full = Image.open(f'{SHOTS}/{D("00-home-full-page")}').convert('RGB')
    third = full.height // 3; strips = ''
    for i in range(3):
        part = full.crop((0, i * third, full.width, min(full.height, (i + 1) * third)))
        part.save(f'{SRC}/img/home-strip-{i}.jpg', 'JPEG', quality=88)
        strips += f'<div class="strip"><img src="img/home-strip-{i}.jpg" alt=""></div>'
    P.append(page(11, 'The full homepage', 'Desktop · Homepage', f'<div class="strips">{strips}</div>',
        'The complete desktop homepage, read top to bottom in three columns: hero, regions, selection, cellar, producers, boutiques, values, services and footer.', label='Desktop'))
    # 12 Header / navigation
    P.append(page(12, 'Header, navigation and hero', 'Desktop · Navigation',
        f'<div class="stack">{browser(D("01-home-hero"), 760, url="arvi.ch")}{browser(D("06-navigation-mega-menu"), 760, url="arvi.ch", crop_h=290)}</div>',
        'A centred logo, quiet spaced-caps navigation and a mega menu organised the way ARVI’s cellar is: by type, country and region.', label='Desktop'))
    # 13 Product & collection
    P.append(page(13, 'Product and collection', 'Desktop · Shopping',
        f'<div class="stack">{browser(D("07-product"), 560, url="arvi.ch/products/salon-le-mesnil-1999")}{browser(D("08-product-vintages"), 560, url="arvi.ch/products/salon-le-mesnil-1999")}</div>{browser(D("09-collection"), 560, url="arvi.ch/collections/champagne")}',
        'On desktop the purchase column stays beside the bottle while the vintage index runs the full width below.', label='Desktop'))
    # 14 Brand story
    P.append(page(14, 'The brand story', 'Desktop · Editorial sections',
        f'<div class="stack">{browser(D("03-home-cellar-story"), 560, url="arvi.ch")}{browser(D("02-home-regions"), 560, url="arvi.ch")}</div><div class="stack">{browser(D("04-home-producers"), 560, url="arvi.ch")}{browser(D("05-home-boutiques"), 560, url="arvi.ch")}</div>',
        'Cellar, regions, icons and boutiques: the sections that turn a catalogue into a house.', label='Desktop'))
    # 15 Closing
    P.append('''<section class="page dark closing">
  <header class="pg-head"><span>ARVI · Swiss Reserve</span><span>Next steps — 15</span></header>
  <div class="pg-intro"><p class="eyebrow">Delivery</p><h2>Ready to review on the store</h2>
    <p class="lede">Every screen in this presentation is a real capture of the working theme, rendered with ARVI’s own catalogue.</p></div>
  <div class="cols">
    <div><h3>What ARVI receives</h3><ul>
      <li>An installable Shopify theme built on Dawn 16.0.0, the same base as the current Shopify project.</li>
      <li>Editable sections for every part of the homepage, product page and boutiques, in Italian, German, French and English.</li>
      <li>A maintenance guide, QA reports and before/after screenshots.</li></ul></div>
    <div><h3>Before launch</h3><ul>
      <li>Upload as an unpublished theme and review it in the Shopify editor; the live store has not been touched.</li>
      <li>Test cart, checkout and payments on the store. They are not yet verified.</li>
      <li>Confirm payment methods, connect critic scores to ARVI’s metafields, and plan high-resolution boutique photography.</li></ul></div>
  </div>
</section>''')
    return P

def doc(body, extra_css=''):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet"><style>{CSS}{extra_css}</style></head><body>{body}</body></html>'

BOARD_CSS = '''.board { width: 2400px; height: 1350px; padding: 80px 110px; display: grid; grid-template-rows: auto 1fr; background: var(--stone); }
.board .pg-head { margin-bottom: 40px; }
.board-row { display: flex; align-items: center; justify-content: center; gap: 46px; }
.board-title { font-family: Newsreader, serif; font-weight: 300; font-size: 40px; letter-spacing: -.02em; margin-bottom: 8px; }'''

def boards():
    mob = ''.join(phone(M(f), 270, c, s) for f, c, s in [
        ('01-home-hero', 'Homepage', 'Hero'), ('12-nav-menu', 'Navigation', 'Main menu'), ('04-home-cellar', 'Brand story', 'The cellar'),
        ('07b-home-boutiques-rail', 'Boutiques', 'Swipeable rail'), ('15-product-buy', 'Product', 'Purchase'), ('17-product-vintages', 'Product', 'All vintages'),
        ('20-collection-top', 'Collection', 'Filter & sort')])
    mobile_board = f'<section class="board"><header class="pg-head"><span>ARVI · Swiss Reserve</span><span>Mobile overview</span></header><div class="board-row">{mob}</div></section>'
    desk = f'''<section class="board" style="height:1600px"><header class="pg-head"><span>ARVI · Swiss Reserve</span><span>Desktop overview</span></header>
<div class="board-row" style="flex-wrap:wrap;gap:44px 56px;align-content:center">{browser(D("01-home-hero"), 900, "Homepage", "Editorial hero")}{browser(D("03-home-cellar-story"), 900, "Brand story", "The cellar")}{browser(D("07-product"), 900, "Product", "Salon Le Mesnil 1999")}{browser(D("09-collection"), 900, "Collection", "Champagne · filters")}</div></section>'''
    pairs = ''
    for d, mm, label in (('01-home-hero', '01-home-hero', 'Homepage'), ('07-product', '14-product-hero', 'Product'), ('09-collection', '20-collection-top', 'Collection')):
        pairs += f'<div class="stack" style="gap:26px"><div class="pair">{browser(D(d), 560)}{phone(M(mm), 184)}</div><p class="cap-t" style="text-align:center">{label}</p></div>'
    resp = f'<section class="board"><header class="pg-head"><span>ARVI · Swiss Reserve</span><span>Responsive comparison</span></header><div class="board-row" style="gap:64px">{pairs}</div></section>'
    return {'ARVI-MOBILE-OVERVIEW': mobile_board, 'ARVI-DESKTOP-OVERVIEW': desk, 'ARVI-RESPONSIVE-COMPARISON': resp}

async def render():
    P = pdf_pages()
    with open(f'{SRC}/presentation.html', 'w') as f: f.write(doc(''.join(P)))
    B = boards()
    for k, v in B.items():
        with open(f'{SRC}/{k}.html', 'w') as f: f.write(doc(v, BOARD_CSS))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
        await pg.goto(f'file://{SRC}/presentation.html', wait_until='networkidle'); await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(800)
        await pg.close()
        # Pages are rendered as images, then assembled into the PDF: Chromium's vector PDF turns blurred
        # box-shadows into black rectangles in Apple Preview/Quartz, so raster pages are the faithful option.
        rv = await b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
        await rv.goto(f'file://{SRC}/presentation.html', wait_until='networkidle'); await rv.evaluate('document.fonts.ready')
        await rv.wait_for_timeout(800)
        pages = []
        for i, el in enumerate(await rv.query_selector_all('section.page'), 1):
            await el.screenshot(path=f'{SRC}/pages/page-{i:02d}.png')
            pages.append(Image.open(f'{SRC}/pages/page-{i:02d}.png').convert('RGB'))
        pages[0].save(f'{ROOT}/ARVI-LUXURY-PRESENTATION.pdf', save_all=True, append_images=pages[1:], resolution=144, quality=88,
                      title='ARVI Swiss Reserve - Client presentation', author='ARVI Swiss Reserve')
        for k in B:
            bp = await b.new_page(viewport={'width': 2400, 'height': 1600}, device_scale_factor=2)
            await bp.goto(f'file://{SRC}/{k}.html', wait_until='networkidle'); await bp.evaluate('document.fonts.ready'); await bp.wait_for_timeout(500)
            await (await bp.query_selector('.board')).screenshot(path=f'{ROOT}/{k}.png'); await bp.close()
        await b.close()
    print(len(P), 'pages')

asyncio.run(render())
