"""Integration test for the unified Stadium (Claude V1.0 + preserved room pages).

Serves site/public_html from a SUBFOLDER over local HTTP (the way GitHub Pages serves a project
site at /<repo>/), crawls every page and link, and checks each viewport. Local only; never the live site.

Usage: python3 claude-stadium-v1/tools/test_integration.py claude-stadium-v1 [report_dir]
"""
import sys, json, threading, http.server, functools, pathlib, tempfile, os
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else root / "reports/integration").resolve()
(out / "screenshots").mkdir(parents=True, exist_ok=True)
web = root / "site/public_html"

# serve as /Thebrianwarner/ to mimic a GitHub Pages project site
serve_root = pathlib.Path(tempfile.mkdtemp())
os.symlink(web, serve_root / "Thebrianwarner")
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 8766), functools.partial(Q, directory=str(serve_root)))
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8766/Thebrianwarner/"

VP = {"phone-320": (320, 640), "phone-390": (390, 844), "phone-landscape": (844, 390),
      "fold-closed": (344, 882), "fold-open": (673, 841), "tablet": (1180, 820), "desktop": (1440, 900)}
checks = []
def check(name, ok, detail=""): checks.append({"check": name, "pass": bool(ok), "detail": str(detail)[:400]})

with sync_playwright() as p:
    b = p.chromium.launch()
    # 1) crawl: every file page + every link target
    ctx = b.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page(); pg.route("**/fonts.g*/**", lambda r: r.abort())
    to_visit, seen, broken, pages = [BASE + "index.html"], set(), [], []
    while to_visit:
        url = to_visit.pop(); base_url = url.split("#")[0]
        if base_url in seen: continue
        seen.add(base_url)
        resp = pg.goto(base_url)
        if not resp or resp.status != 200: broken.append((base_url, resp.status if resp else None)); continue
        pages.append(base_url)
        for href in pg.eval_on_selector_all("a[href]", "e=>e.map(a=>a.getAttribute('href'))"):
            if href.startswith(("http", "mailto:", "tel:")) or href == "#main":  # #main = skip link, handled in script
                continue
            target = urljoin(base_url, href)
            path, frag = target.split("#")[0], (target.split("#")[1] if "#" in target else "")
            if not urlparse(path).path.startswith("/Thebrianwarner/"):
                broken.append((base_url + " -> " + href, "escapes site root")); continue
            if path.endswith(".html") or path.endswith("/"):
                to_visit.append(path)
            # hash route on the interactive Stadium must exist
            if frag and path.endswith("public_html/index.html") is False and path.endswith("/index.html") and "rooms" not in path:
                pg2 = ctx.new_page(); pg2.goto(path)
                ok = pg2.evaluate("f=>!!document.querySelector('[data-page=\"'+f+'\"]')||!!document.getElementById(f)", frag)
                if not ok: broken.append((base_url + " -> " + href, "missing route"))
                pg2.close()
    check("Every page loads (HTTP 200) and every internal link resolves, served from a /Thebrianwarner/ subfolder", not broken, broken)
    check("Pages reached by crawling from the Stadium", len(pages) >= 9, [u.replace(BASE, "") for u in pages])
    ctx.close()

    # 2) per viewport: overflow, script errors, brand centering, room-page tap targets
    for vn, (w, h) in VP.items():
        ctx = b.new_context(viewport={"width": w, "height": h}, has_touch=w < 1000)
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.route("**/fonts.g*/**", lambda r: r.abort())
        overflow, offcenter = {}, {}
        for u in pages:
            pg.goto(u); pg.wait_for_timeout(80)
            ov = pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            if ov > 0: overflow[u.replace(BASE, "")] = ov
            if "/rooms/" in u:
                off = pg.evaluate("()=>{const b=document.querySelector('header a, .brand');if(!b)return null;const r=b.getBoundingClientRect();return Math.round((r.left+r.right)/2-document.documentElement.clientWidth/2)}")
                if off is not None and abs(off) > 4: offcenter[u.replace(BASE, "")] = off
        check(f"{vn}: no sideways scroll on any page", not overflow, overflow)
        check(f"{vn}: no script errors", not errs, errs)
        check(f"{vn}: brand centered on room pages (Oct 11 QB1 direction)", not offcenter, offcenter)
        pg.goto(BASE + "index.html#home"); pg.wait_for_timeout(200)
        pg.screenshot(path=str(out / "screenshots" / f"{vn}-stadium.png"))
        pg.goto(BASE + "rooms/index.html"); pg.screenshot(path=str(out / "screenshots" / f"{vn}-rooms.png"))
        ctx.close()

    # 3) the bridge: menu -> Room Previews -> a room -> back to the interactive Stadium
    ctx = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); pg.route("**/fonts.g*/**", lambda r: r.abort())
    pg.goto(BASE + "index.html#home"); pg.click(".menu-btn"); pg.wait_for_timeout(150)
    link = pg.locator("#site-nav a[href*='rooms/']")
    check("Phone menu shows a link to the room previews", link.count() >= 1, link.count())
    if link.count():
        link.first.click(); pg.wait_for_load_state()
        check("Menu link opens the room previews index", pg.url.endswith("rooms/index.html"), pg.url)
        pg.click("a[href='film-room.html']"); pg.wait_for_load_state()
        pg.click("a[href='../index.html#home']"); pg.wait_for_load_state(); pg.wait_for_timeout(200)
        check("Room page returns to the interactive Stadium home", pg.locator("[data-page=home]").is_visible(), pg.url)
    card = pg.locator("#g-cc"); card.scroll_into_view_if_needed()
    before = card.get_attribute("class"); card.click(); pg.wait_for_timeout(600)
    check("Stadium flip cards still flip after integration", before != card.get_attribute("class"))
    desk = b.new_page(viewport={"width": 1440, "height": 900}); desk.route("**/fonts.g*/**", lambda r: r.abort())
    desk.goto(BASE + "index.html#home")
    vis = desk.locator("a[href*='rooms/']").evaluate_all("e=>e.filter(x=>x.offsetParent!==null).length")
    check("Desktop (1440px) shows a visible way into the room previews", vis > 0, vis)
    ctx.close(); b.close()
httpd.shutdown()
(out / "integration-results.json").write_text(json.dumps(checks, indent=1))
fails = [c for c in checks if not c["pass"]]
print(f"{len(checks)} checks, {len(fails)} failed")
for f in fails: print("FAIL:", f["check"], "|", f["detail"])
