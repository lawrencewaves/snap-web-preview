# Prueba responsive: todas las páginas × 7 anchos (desbordes, zonas táctiles, imágenes). Uso: python3 src/check.py
import asyncio, pathlib
from playwright.async_api import async_playwright
root=pathlib.Path('/home/claude/site/dist/preview')
pages=sorted(str(p.relative_to(root)) for p in root.rglob('index.html'))
CHK="""()=>{const W=document.documentElement.clientWidth;
const o=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>W+1||r.left<-1)&&!e.closest('.hp,.skip,svg,.ticker')}).slice(0,3).map(e=>e.tagName+'.'+e.className);
const small=[...document.querySelectorAll('a.btn,button,input:not([type=hidden]):not(.hp):not([type=checkbox]),select,label.check,.social a')].filter(e=>{const r=e.getBoundingClientRect();return r.height>0&&r.height<40}).map(e=>e.tagName+'.'+e.className);
const img=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length;
return {sw:document.documentElement.scrollWidth,W,o,small,img}}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for w in (320,360,390,768,1024,1366,1920):
            pg = await b.new_page(viewport={"width":w,"height":800}); bad=[]
            for u in pages:
                await pg.goto("file://"+str(root/u), wait_until="load")
                await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); await pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))"); await pg.wait_for_timeout(150)
                r=await pg.evaluate(CHK)
                if r['sw']>r['W'] or r['o'] or r['small'] or r['img']: bad.append((u,r))
            print(w,'px →',f'OK ({len(pages)} páginas)' if not bad else bad[:3]); await pg.close()
        pg = await b.new_page(viewport={"width":390,"height":844})
        await pg.goto("file://"+str(root/"es/viajes-surf/sagres/index.html"), wait_until="load")
        await pg.screenshot(path="/tmp/m-top.jpg", type="jpeg", quality=75)
        await pg.click(".menu-btn"); await pg.wait_for_timeout(200)
        print("menú:", await pg.get_attribute(".menu-btn","aria-expanded"))
        await pg.screenshot(path="/tmp/m-menu.jpg", type="jpeg", quality=75)
        pg2 = await b.new_page(viewport={"width":1366,"height":300})
        await pg2.goto("file://"+str(root/"index.html"), wait_until="load")
        await pg2.screenshot(path="/tmp/d-top.jpg", type="jpeg", quality=80)
        await pg2.evaluate("window.scrollTo(0,document.body.scrollHeight)"); await pg2.set_viewport_size({"width":1366,"height":420}); await pg2.wait_for_timeout(200)
        await pg2.screenshot(path="/tmp/d-foot.jpg", type="jpeg", quality=80)
        await b.close()
asyncio.run(main())

# SEO estático sobre dist/public: 1 H1, JSON-LD válido, enlaces internos, longitud de títulos y descripciones
import re, json as _j
pub = pathlib.Path('/home/claude/site/dist/public'); bad = []
for f in pub.rglob('index.html'):
    h = f.read_text()
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): _j.loads(m)
    if h.count('<h1') != 1: bad.append((str(f), 'h1', h.count('<h1')))
    t = re.search(r'<title>(.*?)</title>', h).group(1).replace('&amp;', '&'); d = re.search(r'name="description" content="(.*?)"', h).group(1)
    if len(t) > 65 or len(d) > 160: bad.append((str(f.parent.relative_to(pub)), len(t), len(d)))
    for u in re.findall(r'href="(/[^"#?]*)', h):
        g = pub / u.lstrip('/')
        if not (g.is_file() or (g / 'index.html').is_file()): bad.append((str(f), 'roto', u))
print('SEO:', len(list(pub.rglob('index.html'))), 'páginas ·', 'OK' if not bad else bad[:6])
