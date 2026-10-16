#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.55,<2"]
# ///
"""Exercise the actual marketing UI, privacy boundaries, and delivered brand assets."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://127.0.0.1:8794")
parser.add_argument("--artifacts", type=Path)
parser.add_argument("--site-regressions", action="store_true")
args = parser.parse_args()
base = args.url.rstrip("/")
root = Path(__file__).resolve().parent.parent
brand = root / "public/assets/brand"
checks = 0


def check(condition, message):
    global checks
    assert condition, message
    checks += 1


def contrast(first, second):
    def luminance(rgb):
        values = [float(value) / 255 for value in rgb.removeprefix("rgb(").removesuffix(")").split(",")]
        linear = [value / 12.92 if value <= .04045 else math.pow((value + .055) / 1.055, 2.4) for value in values]
        return sum(value * weight for value, weight in zip(linear, [.2126, .7152, .0722]))
    values = sorted([luminance(first), luminance(second)])
    return (values[1] + .05) / (values[0] + .05)


manifest = json.loads((brand / "manifest.json").read_text())
for item in manifest["files"]:
    data = (brand / item["path"]).read_bytes()
    check(hashlib.sha256(data).hexdigest() == item["sha256"], f"Manifest mismatch: {item['path']}")
for path in brand.rglob("*.svg"):
    check(ET.parse(path).getroot().tag.endswith("svg"), f"Invalid SVG: {path}")
with zipfile.ZipFile(brand / "atoma-brand-package.zip") as archive:
    check(archive.testzip() is None, "Archive integrity")
    names = archive.namelist()
    check(not any(name.endswith(".zip") for name in names), "Recursive ZIP in package")
    check(not any(part.startswith('.') for name in names for part in Path(name).parts), "No hidden metadata in package")
    for suffix in ["fonts/Geist-OFL.txt", "fonts/InstrumentSerif-OFL.txt", "DESIGN-GUIDE.md", "scripts/build-brand-vectors.py", "public/engineering/index.html", "public/engineering/brand/index.html", "docs/ATOMA_PACKAGE_README.md", "package.json"]:
        check(any(name.endswith(suffix) for name in names), f"Package missing {suffix}")
    with tempfile.TemporaryDirectory(prefix="atoma-kit-check-") as temporary:
        archive.extractall(temporary)
        kit = Path(temporary) / "atoma-design-package"
        environment = dict(os.environ, NODE_PATH=str(root / "node_modules"))
        # Reuse installed dependencies without installing into the user's checkout.
        rebuilt = subprocess.run(["npm", "run", "brand:build"], cwd=kit, env=environment, capture_output=True, text=True, timeout=60)
        check(rebuilt.returncode == 0, f"Standalone source rebuild: {rebuilt.stdout} {rebuilt.stderr}")
        for item in manifest["files"]:
            if item["path"].endswith((".svg", ".woff2", ".png")):
                check(hashlib.sha256((kit / "public/assets/brand" / item["path"]).read_bytes()).hexdigest() == item["sha256"], f"Rebuild differs: {item['path']}")

for path, expected in [
    ("/engineering", "text/html"), ("/engineering/brand", "text/html"),
    ("/assets/engineering.js", "javascript"), ("/assets/engineering.css", "text/css"),
    ("/assets/brand/atoma-brand-package.zip", "zip"),
    ("/assets/brand/atoma-brand-board.png", "image/png"),
]:
    with urllib.request.urlopen(base + path) as response:
        check(response.status == 200 and expected in response.headers["Content-Type"], f"Route failed: {path}")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="chrome", headless=True, args=["--disable-gpu", "--enable-unsafe-swiftshader"])
    context = browser.new_context(viewport={"width":1440,"height":1000}, reduced_motion="reduce", accept_downloads=True)
    page = context.new_page()
    errors, submissions = [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: submissions.append(request.url) if request.method not in ["GET", "HEAD"] else None)
    page.goto(base + "/engineering")
    page.evaluate("document.fonts.ready")
    check(page.get_by_role("heading", level=1).count() == 1, "One main heading")
    check(page.get_by_role("link", name="Explore Grant Intelligence").get_attribute("href") == "https://grantintelligence.sbarteau2022.workers.dev/", "Grant link resolves to independent product host")
    check(page.locator('a[href="/app/welcome/"],a[href="/app/login/"],a[href="/"]').count() == 0, "No cross-repository relative product links")
    page.locator("img").evaluate_all("imgs => imgs.forEach(image => image.loading='eager')")
    page.evaluate("Promise.all([...document.images].map(image => image.decode()))")
    check(page.locator("img").evaluate_all("imgs => imgs.every(i => i.complete && i.naturalWidth > 0)"), "Marketing images loaded")
    for selector in [".ae-hero .ae-lede", ".ae-hero .ae-button-blue", "#brief-goal"]:
        colors = page.locator(selector).evaluate("el => {const s=getComputedStyle(el);let bg=s.backgroundColor;let p=el.parentElement;while(bg==='rgba(0, 0, 0, 0)'&&p){bg=getComputedStyle(p).backgroundColor;p=p.parentElement}return [s.color,bg]}")
        check(contrast(*colors) >= 4.5, f"Text contrast: {selector}")
    colors = page.locator("#brief-goal").evaluate("el=>{const s=getComputedStyle(el);return [s.borderColor,s.backgroundColor]}")
    check(contrast(*colors) >= 3, "Input boundary contrast")
    check(page.locator(".ae-hero .ae-button-blue").evaluate("el=>getComputedStyle(el).transitionDuration==='0s'"), "Reduced motion disables transitions")
    for width in [1440, 1024, 800, 650, 390, 320]:
        page.set_viewport_size({"width":width,"height":1000})
        check(page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Marketing overflow at {width}px")
    page.set_viewport_size({"width":1440,"height":1000})
    tab = page.get_by_role("tab", name="Grant Intelligence", exact=False)
    tab.focus()
    tab.press("ArrowRight")
    check(page.locator("#work-rapid").is_visible() and page.locator("#work-grants").is_hidden(), "Arrow key product selection")
    page.get_by_role("tab", selected=True).press("End")
    check(page.locator("#work-web").is_visible(), "End selects last tab")
    page.get_by_role("tab", selected=True).press("Home")
    check(page.locator("#work-grants").is_visible(), "Home selects first tab")
    check(page.locator("#work-grants").get_attribute("aria-labelledby") == tab.get_attribute("id"), "Tab panel label relationship")
    page.goto(base + "/engineering#work-web")
    check(page.locator("#work-web").is_visible(), "Direct product deep link selects its panel")
    page.get_by_role("link", name="Plan your website").click()
    check(page.locator("#brief-type").input_value() == "website", "Offering preselects project brief type")
    page.set_viewport_size({"width":390,"height":844})
    menu = page.locator(".ae-mobile-menu")
    menu.locator("summary").click()
    check(menu.get_attribute("open") is not None, "Mobile menu opens")
    page.keyboard.press("Escape")
    check(menu.get_attribute("open") is None and menu.locator("summary").evaluate("el => el === document.activeElement"), "Escape closes and restores menu focus")
    menu.locator("summary").click()
    menu.get_by_role("link", name="Our mission").click()
    check(menu.get_attribute("open") is None, "Mobile navigation dismisses menu")
    question = page.locator(".ae-faq-list summary").first
    question.focus()
    question.press("Enter")
    check(page.locator(".ae-faq-list details").first.get_attribute("open") is not None, "Native FAQ keyboard behavior")
    page.locator("#brief-goal").fill("            ")
    page.get_by_role("button", name="Create my project brief").click()
    check(page.locator("#brief-result").is_hidden(), "Whitespace-only brief rejected")
    goal = 'Help our café support rural teams — access, clarity, and a useful next step. <img src=x onerror=alert(1)> 🧭'
    page.locator("#brief-name").fill("Zoë & 李")
    page.locator("#brief-org").fill("Community & Co.")
    page.locator("#brief-goal").fill(goal)
    page.locator("#brief-type").select_option("ai")
    page.get_by_role("button", name="Create my project brief").click()
    text = page.locator("#brief-text").input_value()
    check("Zoë & 李" in text and goal in text, "Unicode and literal markup preserved as text")
    check(page.locator("#brief-result img").count() == 0, "Project text cannot inject HTML")
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async()=>{throw new Error('blocked')}}})")
    page.get_by_role("button", name="Copy brief", exact=False).click()
    check("Command+C" in page.locator("#brief-status").inner_text(), "Clipboard-denied fallback")
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async(value)=>{window.__briefCopied=value}}})")
    page.get_by_role("button", name="Copy brief", exact=False).click()
    check(page.evaluate("window.__briefCopied") == text, "Project brief copy success")
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Download .txt").click()
    with tempfile.TemporaryDirectory(prefix="atoma-brief-check-") as temporary:
        downloaded = Path(temporary) / "brief.txt"
        download_info.value.save_as(downloaded)
        check(downloaded.read_text() == text, "Downloaded brief matches visible draft")
    page.get_by_role("button", name="Make a change", exact=False).click()
    check(page.locator("#brief-goal").input_value() == goal, "Editing preserves draft")
    page.locator("#brief-goal").fill("A" * 4000)
    page.get_by_role("button", name="Create my project brief").click()
    check("A" * 4000 in page.locator("#brief-text").input_value(), "Maximum-length brief")
    check(not submissions, "Brief performs no submission requests")
    page.reload()
    check(page.locator("#brief-goal").input_value() == "", "Draft is not persisted across reloads")
    check(page.locator(".ae-contact-placeholder").inner_text().find("PLACEHOLDER") >= 0, "Contact placeholder is labeled")
    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=True)
        page.set_viewport_size({"width":1440,"height":1000})
        page.evaluate("document.fonts.ready")
        page.evaluate("scrollTo(0,0)")
        page.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
        page.screenshot(path=str(args.artifacts / "atoma-hero-desktop.png"), animations="disabled")
        page.screenshot(path=str(args.artifacts / "atoma-home-desktop.png"), full_page=True, animations="disabled")
        page.set_viewport_size({"width":390,"height":844})
        page.evaluate("scrollTo(0,0)")
        page.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
        page.screenshot(path=str(args.artifacts / "atoma-hero-mobile.png"), animations="disabled")
        page.screenshot(path=str(args.artifacts / "atoma-home-mobile.png"), full_page=True, animations="disabled")
    page.goto(base + "/engineering/brand")
    page.evaluate("document.fonts.ready")
    for width in [1440, 1024, 800, 650, 390, 320]:
        page.set_viewport_size({"width":width,"height":1000})
        check(page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Brand book overflow at {width}px")
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async(value)=>{window.__copied=value}}})")
    page.get_by_role("button", name="Copy blue color #2F5BEA").click()
    check(page.evaluate("window.__copied") == "#2F5BEA", "Brand color copy action")
    check(page.locator(".ae-copy-status").inner_text().find("copied") >= 0, "Color-copy feedback")
    # The browser must not silently turn missing asset links into the SPA document.
    paths = page.locator("a[download]").evaluate_all("links => [...new Set(links.map(a=>a.pathname))]")
    for path in paths:
        response = context.request.get(base + path)
        check(response.ok and "text/html" not in response.headers.get("content-type", ""), f"Brand download: {path}")
    check(not errors, f"Browser errors: {errors}")
    if args.artifacts:
        page.set_viewport_size({"width":1440,"height":1000})
        page.locator("img[loading='lazy']").evaluate_all("imgs => imgs.forEach(image => image.loading='eager')")
        page.evaluate("Promise.all([...document.images].map(image => image.decode()))")
        check(page.locator("img").evaluate_all("imgs => imgs.every(i => i.complete && i.naturalWidth > 0)"), "Brand book images loaded")
        page.evaluate("scrollTo(0,0)")
        page.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
        page.screenshot(path=str(args.artifacts / "atoma-brandbook-desktop.png"), full_page=True, animations="disabled")
    nojs = browser.new_context(java_script_enabled=False, viewport={"width":390,"height":844})
    plain = nojs.new_page()
    plain.goto(base + "/engineering")
    for selector in ["#work-grants", "#work-rapid", "#work-web"]:
        check(plain.locator(selector).is_visible(), f"No-JS offering available: {selector}")
    check(plain.get_by_role("button", name="Create my project brief").is_disabled(), "No-JS brief cannot submit")
    plain.locator(".ae-faq-list summary").first.click()
    check(plain.locator(".ae-faq-list details").first.get_attribute("open") is not None, "No-JS FAQ works")
    if args.site_regressions:
        original = browser.new_context(viewport={"width":1440,"height":1000})
        preserved = original.new_page()
        for route, canvas in [("/", "eip-globe"), ("/master-atlas", "master-canvas")]:
            for width in [1440, 390]:
                preserved.set_viewport_size({"width":width,"height":1000})
                response = preserved.goto(base + route)
                check(response.status == 200, f"Preserved route: {route}")
                preserved.wait_for_function("id => {const c=document.getElementById(id);return c && c.width >= innerWidth*.9 && c.height > 150}", arg=canvas)
                check(preserved.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Preserved route overflow: {route}@{width}")
                check(preserved.locator("#" + canvas).evaluate("c=>{const gl=c.getContext('webgl2');return gl && !gl.isContextLost() && gl.drawingBufferWidth>0}"), f"Preserved live WebGL context: {route}@{width}")
                if args.artifacts:
                    preserved.evaluate("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
                    name = "observer-home" if route == "/" else "master-atlas"
                    preserved.screenshot(path=str(args.artifacts / f"preserved-{name}-{width}.png"), animations="disabled")
        for route in ["/elle", "/mission", "/app"]:
            response = original.request.get(base + route)
            check(response.ok and "text/html" in response.headers.get("content-type", ""), f"Preserved application route: {route}")
    browser.close()

print(json.dumps({"checks":checks,"status":"passed","url":base,"viewports":[1440,1024,800,650,390,320],"form_submissions":0,"assets":len(manifest['files']),"site_regressions":args.site_regressions}))
