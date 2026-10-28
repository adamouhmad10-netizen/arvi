"""Interaction screenshots: mega menu, mobile drawer, age gate, keyboard focus."""
import asyncio
from playwright.async_api import async_playwright
B='http://localhost:9292'; OUT='presentation/screens/'
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    # Mega menu (desktop)
    ctx=await b.new_context(viewport={'width':1440,'height':900}); await ctx.add_cookies([{'name':'arvi_age_ok','value':'1','url':B}])
    pg=await ctx.new_page(); await pg.goto(B+'/',wait_until='networkidle')
    await pg.click('header-menu summary:has-text("Wines")'); await pg.wait_for_timeout(500)
    await pg.screenshot(path=OUT+'nav-mega-1440.png')
    # keyboard focus visibility
    await pg.keyboard.press('Escape'); await pg.goto(B+'/',wait_until='networkidle')
    for _ in range(6): await pg.keyboard.press('Tab')
    await pg.screenshot(path=OUT+'a11y-focus-1440.png',clip={'x':0,'y':0,'width':1440,'height':260})
    await ctx.close()
    # Age gate (no cookie)
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page()
    await pg.goto(B+'/',wait_until='networkidle'); await pg.wait_for_timeout(600)
    await pg.screenshot(path=OUT+'age-gate-1440.png')
    open_ok=await pg.evaluate("!!document.querySelector('dialog.arvi-age[open]')")
    await pg.click('[data-arvi-age="yes"]'); await pg.wait_for_timeout(300)
    cookie=[c for c in await ctx.cookies() if c['name']=='arvi_age_ok']
    gone=await pg.evaluate("!document.querySelector('dialog.arvi-age')")
    print('age gate open:',open_ok,'cookie set:',bool(cookie),'dismissed:',gone)
    await ctx.close()
    # Mobile drawer
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); await ctx.add_cookies([{'name':'arvi_age_ok','value':'1','url':B}])
    pg=await ctx.new_page(); await pg.goto(B+'/',wait_until='networkidle')
    await pg.click('header-drawer summary'); await pg.wait_for_timeout(600)
    await pg.screenshot(path=OUT+'nav-drawer-390.png')
    await pg.click('#menu-drawer summary:has-text("Wines")'); await pg.wait_for_timeout(500)
    await pg.screenshot(path=OUT+'nav-drawer-sub-390.png')
    await ctx.close(); await b.close()
asyncio.run(m())
