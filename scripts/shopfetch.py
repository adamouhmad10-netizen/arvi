"""Fetch storefront JSON/HTML from the password-protected preview. Usage: SHOP_PW=... shopfetch.py out_dir path1 path2..."""
import asyncio,os,sys
from playwright.async_api import async_playwright
async def m(out,paths):
  async with async_playwright() as p:
    b=await p.chromium.launch(); ctx=await b.new_context(); pg=await ctx.new_page()
    await pg.goto('https://myarvi.myshopify.com/password',wait_until='networkidle')
    async with pg.expect_navigation():
        await pg.evaluate("pw=>{const i=document.querySelector('input[type=password]');i.value=pw;i.form.requestSubmit()}", os.environ['SHOP_PW'])
    for path in paths:
        r=await ctx.request.get('https://myarvi.myshopify.com'+path)
        fn=os.path.join(out,path.strip('/').replace('/','_').replace('?','_')[:120] or 'root')
        open(fn,'wb').write(await r.body()); print(r.status,path,len(await r.body()))
    await b.close()
asyncio.run(m(sys.argv[1],sys.argv[2:]))
