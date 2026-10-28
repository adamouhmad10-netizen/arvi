"""Full-page screenshots of the main pages at desktop and mobile, plus viewport-height slices for review.
Usage: shoot_pages.py OUTDIR [page ...]   (pages: home coll pdp pdpreq search faq shops; default all)"""
import asyncio, os, sys
from playwright.async_api import async_playwright
from PIL import Image
PAGES = {'home': '/', 'coll': '/collections/champagne', 'pdp': '/products/maison-salon-champagne-le-mesnil-1999',
         'pdpreq': '/products/chateau-latour-ex-chateau-release-2023-2015?variant=59475133137244',
         'search': '/search?q=krug', 'faq': '/pages/faq', 'shops': '/pages/i-nostri-negozi'}
async def main(out, keys):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1440, 390):
            ctx = await b.new_context(viewport={'width': w, 'height': 900 if w > 1000 else 844})
            await ctx.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': 'http://localhost:9292'}])
            for k in keys:
                pg = await ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                await pg.goto('http://localhost:9292' + PAGES[k], wait_until='networkidle')
                await pg.evaluate("""async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,90));}window.scrollTo(0,0);}""")
                await pg.wait_for_timeout(1200)
                ov = await pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
                f = f'{out}/{k}-{w}.png'; await pg.screenshot(path=f, full_page=True)
                im = Image.open(f); step = 1100 if w > 1000 else 1600
                for n, y in enumerate(range(0, im.height, step)):
                    im.crop((0, y, w, min(im.height, y + step))).save(f'{out}/{k}-{w}-{n:02d}.png')
                print(k, w, 'height', im.height, 'overflow', ov, 'errors', errs[:3])
                await pg.close()
            await ctx.close()
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2:] or list(PAGES)))
