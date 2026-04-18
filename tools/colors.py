"""
colors.py — Extracts the dominant color palette from page screenshots.
Uses ColorThief to pull the most prominent colors, then categorizes them.
"""

from colorthief import ColorThief
from pathlib import Path


def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def is_dark(rgb: tuple) -> bool:
    r, g, b = rgb
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance < 0.4


def is_light(rgb: tuple) -> bool:
    r, g, b = rgb
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance > 0.8


def is_neutral(rgb: tuple) -> bool:
    r, g, b = rgb
    diff = max(abs(r - g), abs(g - b), abs(r - b))
    return diff < 30


def categorize_color(rgb: tuple) -> str:
    if is_light(rgb) and is_neutral(rgb):
        return "background"
    if is_dark(rgb) and is_neutral(rgb):
        return "text / dark bg"
    if is_neutral(rgb):
        return "neutral"
    r, g, b = rgb
    if r > g and r > b:
        return "accent (warm)"
    if b > r and b > g:
        return "primary (cool/blue-purple)"
    if g > r and g > b:
        return "accent (green)"
    return "accent"


def extract_from_screenshot(screenshot_path: str, color_count: int = 12) -> list:
    """Extract dominant colors from a single screenshot."""
    try:
        ct = ColorThief(screenshot_path)
        palette = ct.get_palette(color_count=color_count, quality=3)
        return palette
    except Exception as e:
        print(f"  ! Color extraction failed for {screenshot_path}: {e}")
        return []


def analyze(screenshots: list) -> dict:
    """
    Run color extraction across section screenshots.
    Returns deduplicated, categorized palette.
    """
    if not screenshots:
        return {"palette": [], "categories": {}}

    # Use full page screenshot if available, otherwise first section
    target = screenshots[0]

    raw_palette = extract_from_screenshot(target, color_count=16)

    palette = []
    seen = set()

    for rgb in raw_palette:
        hex_val = rgb_to_hex(rgb)
        if hex_val in seen:
            continue
        seen.add(hex_val)
        category = categorize_color(rgb)
        palette.append({
            "hex": hex_val,
            "rgb": rgb,
            "category": category,
            "dark": is_dark(rgb),
            "light": is_light(rgb),
        })

    # Group by category
    categories = {}
    for color in palette:
        cat = color["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(color["hex"])

    print(f"  → {len(palette)} dominant colors extracted")
    return {
        "palette": palette,
        "categories": categories,
    }
