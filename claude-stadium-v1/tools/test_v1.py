"""Headless preflight test for the V1.0 candidate. Serves site/public_html locally (never the live site)."""
import sys, json, threading, http.server, functools, pathlib
from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1])
web = root / "site/public_html"
shots = root / "reports/screenshots"; shots.mkdir(parents=True, exist_ok=True)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(web))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
Handler = functools.partial(Q, directory=str(web))
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8765/index.html"

VIEWPORTS = {
    "phone-portrait": (390, 844, True), "phone-landscape": (844, 390, True),
    "phone-small": (320, 640, True), "foldable-closed": (344, 882, True),
    "foldable-open": (673, 841, True), "tablet": (1180, 820, True), "desktop": (1440, 900, False),
}
results = {"viewports": {}, "checks": []}
def check(name, ok, detail=""):
    results["checks"].append({"check": name, "pass": bool(ok), "detail": detail})

with sync_playwright() as p:
    b = p.chromium.launch()
    for vname, (w, h, touch) in VIEWPORTS.items():
        ctx = b.new_context(viewport={"width": w, "height": h}, has_touch=touch, is_mobile=touch and w < 1000)
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" and "ERR_FAILED" not in m.text else None)
        page.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        page.route("**/fonts.gstatic.com/**", lambda r: r.abort())
        page.goto(BASE, wait_until="load")
        ids = page.eval_on_selector_all(".pv-page", "els => els.map(e => e.dataset.page)")
        overflow = {}
        for pid in ids:
            page.evaluate(f"location.hash = '#{pid}'"); page.wait_for_timeout(120)
            visible = page.eval_on_selector_all(".pv-page", "els => els.filter(e => !e.hidden).map(e => e.dataset.page)")
            if visible != [pid]: check(f"{vname}: route #{pid} shows only its page", False, str(visible))
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ov > 0: overflow[pid] = ov
        results["viewports"][vname] = {"pages": len(ids), "sideways_overflow_px": overflow, "errors": errors[:5]}
        check(f"{vname}: no sideways scroll", not overflow, json.dumps(overflow))
        check(f"{vname}: no script errors", not errors, "; ".join(errors[:3]))
        # home screenshot + flip card
        page.evaluate("location.hash = '#home'"); page.wait_for_timeout(200)
        page.screenshot(path=str(shots / f"{vname}-home.png"))
        card = page.locator("#g-cc")
        if card.count():
            card.scroll_into_view_if_needed()
            before = card.get_attribute("aria-pressed") or card.get_attribute("class")
            card.click(); page.wait_for_timeout(700)
            after = card.get_attribute("aria-pressed") or card.get_attribute("class")
            check(f"{vname}: flip card toggles on tap/click", before != after, f"{before} -> {after}")
            page.screenshot(path=str(shots / f"{vname}-flip.png"))
        check(f"{vname}: Championship Ladder held off public view", not page.locator("#ladder").is_visible())
        ctx.close()

    # Content and behavior checks (phone)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    page = ctx.new_page()
    page.route("**/fonts.g*/**", lambda r: r.abort())
    page.goto(BASE, wait_until="load")
    html = page.content()
    check("No 'Live Cast' anywhere", "Live Cast" not in html)
    check("No preview ribbon", page.locator(".preview-ribbon").count() == 0)
    page.evaluate("location.hash='#media'"); page.wait_for_timeout(150)
    shows = page.eval_on_selector_all("[data-page=media] .show h3", "e=>e.map(x=>x.textContent)")
    check("Media lists 4 shows, no Million Dollar Opportunity", len(shows) == 4 and "Million Dollar Opportunity" not in shows, str(shows))
    page.evaluate("location.hash='#coaching'"); page.wait_for_timeout(150)
    check("MDO workshop destination visible on Coaching", page.locator("#million-dollar-opportunity").is_visible())
    page.screenshot(path=str(shots / "phone-coaching-mdo.png"), full_page=True)
    page.evaluate("location.hash='#saturday-school'"); page.wait_for_timeout(150)
    check("Saturday School makes no 'in session' claim", "in session" not in page.inner_text("[data-page=saturday-school]"))
    page.evaluate("location.hash='#investigator-training'"); page.wait_for_timeout(150)
    page.screenshot(path=str(shots / "phone-investigator.png"))
    page.evaluate("location.hash='#connect'"); page.wait_for_timeout(150)
    page.fill("#cf-name", "Test"); page.fill("#cf-email", "test@example.com"); page.fill("#cf-message", "hello")
    page.click("#connect-form [type=submit]"); page.wait_for_timeout(150)
    check("Contact form honest when inbox unset", "hasn't been set" in page.inner_text("#cf-status"), page.inner_text("#cf-status"))
    page.evaluate("location.hash='#nope'"); page.wait_for_timeout(150)
    check("Unknown route shows 404 page", page.locator("[data-page='404']").is_visible())
    page.evaluate("location.hash='#home'"); page.wait_for_timeout(150)
    page.click(".menu-btn"); page.wait_for_timeout(150)
    check("Phone menu opens", page.locator("#site-nav.open").count() == 1)
    page.screenshot(path=str(shots / "phone-menu.png"))
    page.keyboard.press("Escape")
    dock = page.eval_on_selector_all(".dock a", "e=>e.map(x=>x.getAttribute('href'))")
    check("Phone dock present", len(dock) >= 4, str(dock))
    links = page.eval_on_selector_all("a[href^='#']", "e=>[...new Set(e.map(x=>x.getAttribute('href')))]")
    ids = set(page.eval_on_selector_all(".pv-page", "e=>e.map(x=>'#'+x.dataset.page)")) | set(page.eval_on_selector_all("[id]", "e=>e.map(x=>'#'+x.id)"))
    dead = [l for l in links if l not in ids and l not in ("#", "#main")]
    check("Every in-site link resolves", not dead, str(dead))
    ext = page.eval_on_selector_all("a[href^='http']", "e=>[...new Set(e.map(x=>x.href))]")
    results["external_links"] = ext
    ctx.close(); b.close()
httpd.shutdown()
(root / "reports/test-results.json").write_text(json.dumps(results, indent=2))
fails = [c for c in results["checks"] if not c["pass"]]
print(f"{len(results['checks'])} checks, {len(fails)} failed")
for f in fails: print("FAIL", f)
print("external links:", results["external_links"])
