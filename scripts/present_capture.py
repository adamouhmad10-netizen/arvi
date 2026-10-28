"""Captures the client-presentation screenshots from the running local preview (http://localhost:9292).
Mobile: 390x844 CSS px at 3x (1170x2532), viewport captures that read like real phone screens.
Desktop: 1440x900 at 2x, plus a full-page homepage at 1x.
Usage: python3 scripts/present_capture.py"""
import asyncio, json
from playwright.async_api import async_playwright

BASE = 'http://localhost:9292'
OUT = 'docs/ARVI-CLIENT-PRESENTATION/screenshots'
PDP = '/products/maison-salon-champagne-le-mesnil-1999'
REQ = '/products/chateau-latour-ex-chateau-release-2023-2015?variant=59475133137244'
log = []

async def settle(pg):
    """Scroll the whole page once so scroll-reveal sections and lazy images are in their final state."""
    await pg.evaluate("""async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}window.scrollTo(0,0);}""")
    await pg.wait_for_timeout(900)

async def at(pg, js_y, name, folder='mobile'):
    y = await pg.evaluate(js_y)
    await pg.evaluate(f'window.scrollTo(0, {y})')
    await pg.wait_for_timeout(900)
    path = f'{OUT}/{folder}/{name}.png'
    await pg.screenshot(path=path)
    log.append(path)

def section_top(sid, offset=0):
    return f"(()=>{{const e=document.getElementById('shopify-section-template--1__{sid}');return Math.max(0, e.getBoundingClientRect().top+scrollY-({offset}));}})()"

async def mobile(b):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
    await ctx.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': BASE}])
    pg = await ctx.new_page()
    await pg.goto(BASE + '/', wait_until='networkidle'); await settle(pg)
    await at(pg, '0', '01-home-hero')
    # Strictly top-to-bottom: scrolling back up would reveal Dawn's sticky header over the content
    await at(pg, section_top('regions'), '02-home-regions')
    await at(pg, section_top('champagne'), '03-home-selection')
    await at(pg, section_top('heritage'), '04-home-cellar')
    await at(pg, "(()=>{const e=document.querySelector('.arvi-stats');return e.getBoundingClientRect().top+scrollY-40})()", '05-home-quote')
    await at(pg, section_top('icons'), '06-home-producers')
    await at(pg, section_top('boutiques'), '07-home-boutiques')
    await at(pg, "(()=>{const g=document.querySelector('.arvi-boutiques__grid');return g.getBoundingClientRect().top+scrollY-24})()", '07b-home-boutiques-rail')
    await pg.evaluate("document.querySelector('.arvi-boutiques__grid').scrollTo({left: document.querySelector('.arvi-boutiques__grid > li:nth-child(2)').offsetLeft - 20})")
    await pg.wait_for_timeout(700); await pg.screenshot(path=f'{OUT}/mobile/07b-home-boutiques-rail.png')
    await at(pg, section_top('values'), '08-home-values')
    await at(pg, section_top('services'), '09-home-services')
    await at(pg, "(()=>{const f=document.querySelector('.footer');return f.getBoundingClientRect().top+scrollY})()", '10-footer-top')
    await at(pg, 'document.body.scrollHeight', '11-footer-payments')
    # navigation
    await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(400)
    await pg.click('header-drawer summary'); await pg.wait_for_timeout(700)
    await pg.screenshot(path=f'{OUT}/mobile/12-nav-menu.png'); log.append('12-nav-menu')
    await pg.click('.menu-drawer__navigation > ul > li:first-child summary'); await pg.wait_for_timeout(700)
    await pg.screenshot(path=f'{OUT}/mobile/13-nav-wines.png'); log.append('13-nav-wines')
    await pg.close()
    # product page
    pg = await ctx.new_page(); await pg.goto(BASE + PDP, wait_until='networkidle'); await settle(pg)
    await at(pg, '0', '14-product-hero')
    await at(pg, "(()=>{const e=document.querySelector('.product__info-container');return e.getBoundingClientRect().top+scrollY-24})()", '15-product-buy')
    # Facts table and an opened service accordion
    await pg.evaluate("(()=>{const d=document.querySelector('.product__accordion details');if(d)d.open=true})()")
    await at(pg, "(()=>{const e=document.querySelector('product-info dl.arvi-facts');return e.getBoundingClientRect().top+scrollY-36})()", '16-product-facts')
    await at(pg, "(()=>{const e=document.querySelector('.arvi-vintages');return e.getBoundingClientRect().top+scrollY-60})()", '17-product-vintages')
    await at(pg, "(()=>{const e=document.querySelector('product-recommendations');return e.getBoundingClientRect().top+scrollY-20})()", '18-product-recommendations')
    await pg.close()
    pg = await ctx.new_page(); await pg.goto(BASE + REQ, wait_until='networkidle'); await settle(pg)
    await at(pg, "(()=>{const e=document.querySelector('.product__info-container');return e.getBoundingClientRect().top+scrollY-24})()", '19-product-price-on-request')
    await pg.close()
    # collection
    pg = await ctx.new_page(); await pg.goto(BASE + '/collections/champagne', wait_until='networkidle'); await settle(pg)
    await at(pg, '0', '20-collection-top')
    await at(pg, "(()=>{const e=document.querySelectorAll('#product-grid .grid__item')[4];return e.getBoundingClientRect().top+scrollY-90})()", '21-collection-grid')
    await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(300)
    await pg.click('.mobile-facets__open'); await pg.wait_for_timeout(800)
    await pg.screenshot(path=f'{OUT}/mobile/22-collection-filters.png'); log.append('22-collection-filters')
    await pg.close(); await ctx.close()

async def desktop(b):
    ctx = await b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    await ctx.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': BASE}])
    pg = await ctx.new_page(); await pg.goto(BASE + '/', wait_until='networkidle'); await settle(pg)
    await at(pg, '0', '01-home-hero', 'desktop')
    await at(pg, section_top('regions'), '02-home-regions', 'desktop')
    await at(pg, section_top('heritage'), '03-home-cellar-story', 'desktop')
    await at(pg, section_top('icons'), '04-home-producers', 'desktop')
    await at(pg, section_top('boutiques', -40), '05-home-boutiques', 'desktop')
    await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(300)
    await pg.click('header-menu details summary'); await pg.wait_for_timeout(600)
    await pg.screenshot(path=f'{OUT}/desktop/06-navigation-mega-menu.png')
    await pg.close()
    full = await b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
    await full.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': BASE}])
    fp = await full.new_page(); await fp.goto(BASE + '/', wait_until='networkidle'); await settle(fp)
    await fp.screenshot(path=f'{OUT}/desktop/00-home-full-page.png', full_page=True); await full.close()
    pg = await ctx.new_page(); await pg.goto(BASE + PDP, wait_until='networkidle'); await settle(pg)
    await at(pg, '0', '07-product', 'desktop')
    await at(pg, "(()=>{const e=document.querySelector('.arvi-vintages');return e.getBoundingClientRect().top+scrollY-110})()", '08-product-vintages', 'desktop')
    await pg.close()
    pg = await ctx.new_page(); await pg.goto(BASE + '/collections/champagne', wait_until='networkidle'); await settle(pg)
    await at(pg, '0', '09-collection', 'desktop')
    await pg.close()
    pg = await ctx.new_page(); await pg.goto(BASE + '/pages/i-nostri-negozi', wait_until='networkidle'); await settle(pg)
    await at(pg, "(()=>{const e=document.querySelector('.arvi-boutiques');return e.getBoundingClientRect().top+scrollY+40})()", '10-boutiques-page', 'desktop')
    await pg.close(); await ctx.close()

async def compare(b):
    """Extra pages for the responsive comparison, so the PDF never repeats a screenshot."""
    for w, h, dpr, folder in ((390, 844, 3, 'mobile'), (1440, 900, 2, 'desktop')):
        ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=dpr, is_mobile=(w < 500), has_touch=(w < 500))
        await ctx.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': BASE}])
        for path, name in (('/pages/faq', '23-faq' if w < 500 else '11-faq'), ('/pages/i-nostri-negozi', '24-boutiques-page')):
            if w > 500 and name == '24-boutiques-page':
                continue
            pg = await ctx.new_page(); await pg.goto(BASE + path, wait_until='networkidle'); await settle(pg)
            await at(pg, '0', name, folder); await pg.close()
        await ctx.close()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        await mobile(b); await desktop(b); await compare(b)
        await b.close()
    print(len(log), 'captures')

asyncio.run(main())
