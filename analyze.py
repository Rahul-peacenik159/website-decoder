"""
analyze.py — Main entry point for Website Decoder.

Usage:
    python analyze.py https://wisprflow.ai

Runs all analysis tools, saves output to output/{domain}/{timestamp}/,
and generates a markdown report.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

from tools import browser, css_analyzer, structure, colors, illustrations, animation_inspector, report


def get_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.replace("www.", "")


def main():
    parser = argparse.ArgumentParser(description="Decode a website for PMM analysis")
    parser.add_argument("url", help="Full URL to analyze (e.g. https://wisprflow.ai)")
    args = parser.parse_args()

    url = args.url.rstrip("/")
    if not url.startswith("http"):
        url = "https://" + url

    domain = get_domain(url)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M")

    # Output paths
    base_output = Path("output")
    run_dir = base_output / "screenshots" / domain / timestamp
    assets_dir = base_output / "assets" / domain
    reports_dir = base_output / "reports"

    for d in [run_dir, assets_dir, reports_dir]:
        d.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"  Website Decoder")
    print(f"  URL: {url}")
    print(f"  Domain: {domain}")
    print(f"  Run: {timestamp}")
    print(f"{'='*50}\n")

    # Step 1: Browser crawl + screenshots
    print("[ 1/5 ] Crawling site & capturing screenshots...")
    browser_data = browser.crawl(url, run_dir)

    # Step 2: CSS analysis
    print("\n[ 2/5 ] Downloading & analyzing CSS...")
    css_data = css_analyzer.analyze(
        css_urls=browser_data["css_urls"],
        js_urls=browser_data["js_urls"],
        base_url=url,
        html=browser_data["html"],
        assets_dir=assets_dir,
    )

    # Step 3: Site structure
    print("\n[ 3/5 ] Parsing site structure...")
    structure_data = structure.analyze(browser_data["html"], url)

    # Step 4: Color palette
    print("\n[ 4/5 ] Extracting color palette...")
    all_screenshots = [browser_data["full_page_screenshot"]] + browser_data["screenshots"]
    color_data = colors.analyze(all_screenshots)

    # Step 5: Illustrations + animation libraries
    print("\n[ 5/5 ] Detecting illustrations & animation libraries...")
    illustration_data = illustrations.analyze(browser_data["html"], browser_data["js_urls"])

    # Step 6: Deep animation inspection
    print("\n[ 6/6 ] Deep animation & illustration inspection...")
    css_files = [{"content": f.read_text(encoding="utf-8")}
                 for f in assets_dir.glob("*.css")] if assets_dir.exists() else []
    animation_data = animation_inspector.analyze(
        html=browser_data["html"],
        css_texts=css_files,
        js_urls=browser_data["js_urls"],
    )

    # Generate report
    print("\n[ ✓ ] Generating report...")
    screenshots_rel = f"../screenshots/{domain}/{timestamp}"
    report_path = report.generate(
        url=url,
        domain=domain,
        browser_data=browser_data,
        css_data=css_data,
        structure_data=structure_data,
        color_data=color_data,
        illustration_data=illustration_data,
        animation_data=animation_data,
        output_dir=reports_dir,
        screenshots_rel_path=screenshots_rel,
    )

    print(f"\n{'='*50}")
    print(f"  DONE")
    print(f"  Report: {report_path}")
    print(f"  Screenshots: {run_dir}")
    print(f"  CSS assets: {assets_dir}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
