"""
browser.py — Playwright-based site crawler.
Opens URL, scrolls through, captures full page + section screenshots,
returns HTML and all linked CSS/JS URLs.
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time


def crawl(url: str, output_dir: Path) -> dict:
    """
    Launch headless Chromium, visit the URL, scroll through the page,
    capture screenshots at viewport intervals, and return raw data.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "url": url,
        "html": "",
        "css_urls": [],
        "js_urls": [],
        "screenshots": [],
        "full_page_screenshot": "",
        "page_title": "",
        "meta_description": "",
        "viewport_height": 0,
        "page_height": 0,
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        # Collect network requests for CSS/JS
        css_urls = []
        js_urls = []

        def on_request(request):
            if ".css" in request.url:
                css_urls.append(request.url)
            if ".js" in request.url and "analytics" not in request.url:
                js_urls.append(request.url)

        page.on("request", on_request)

        print(f"  → Opening {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(2)  # Let animations settle

        # Basic page info
        results["page_title"] = page.title()
        results["meta_description"] = page.evaluate(
            "() => document.querySelector('meta[name=\"description\"]')?.content || ''"
        )

        # Page dimensions
        page_height = page.evaluate("() => document.body.scrollHeight")
        results["viewport_height"] = 900
        results["page_height"] = page_height

        # Full page screenshot
        full_path = output_dir / "full-page.png"
        page.screenshot(path=str(full_path), full_page=True)
        results["full_page_screenshot"] = str(full_path)
        print(f"  → Full page screenshot saved")

        # Section screenshots — scroll through at viewport intervals
        scroll_step = 800
        scroll_position = 0
        section_index = 0

        while scroll_position < page_height:
            page.evaluate(f"window.scrollTo(0, {scroll_position})")
            time.sleep(0.4)
            shot_path = output_dir / f"section-{section_index:02d}.png"
            page.screenshot(path=str(shot_path))
            results["screenshots"].append(str(shot_path))
            scroll_position += scroll_step
            section_index += 1

        print(f"  → {section_index} section screenshots captured")

        # Raw HTML
        results["html"] = page.content()

        # CSS/JS collected via network listener
        results["css_urls"] = list(set(css_urls))
        results["js_urls"] = list(set(js_urls))

        browser.close()

    return results
