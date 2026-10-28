"""Screenshot local preview pages. Usage: shoot.py outprefix path [widths...]"""
import asyncio,sys
from playwright.async_api import async_playwright
async def m(prefix,path,widths,full=True):
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for w in widths:
      h=900 if w>=1000 else (1024 if w>=768 else 844)
      ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1 if w>=1000 else 2)
      await ctx.add_cookies([{'name':'arvi_age_ok','value':'1','url':'http://localhost:9292'}])
      pg=await ctx.new_page()
      errs=[]; pg.on('console',lambda msg: errs.append(msg.text) if msg.type=='error' else None); pg.on('pageerror',lambda e: errs.append(str(e)))
      await pg.goto('http://localhost:9292'+path,wait_until='networkidle')
      await pg.evaluate("""async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,90));}window.scrollTo(0,0);}""")
      await pg.wait_for_timeout(900)
      ov=await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
      await pg.screenshot(path=f'{prefix}-{w}.png',full_page=full)
      print(w,'overflow:',ov,'errors:',errs[:5])
      await ctx.close()
    await b.close()
a=sys.argv; asyncio.run(m(a[1],a[2],[int(x) for x in a[3:]] or [1440,390]))
