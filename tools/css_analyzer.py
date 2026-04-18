"""
css_analyzer.py — Downloads and parses all CSS files from a site.
Extracts: keyframes, transitions, CSS variables, animation library hints,
typography declarations, and all color values.
"""

import re
import requests
import tinycss2
from pathlib import Path
from urllib.parse import urljoin


ANIMATION_LIBRARY_SIGNATURES = {
    "GSAP": ["gsap", "TweenMax", "TweenLite", "ScrollTrigger", "SplitText", "DrawSVG", "MotionPath"],
    "Framer Motion": ["framer-motion", "useAnimation", "motion.div"],
    "Lottie": ["lottie", "lottie-web", "bodymovin"],
    "Rive": ["rive-canvas", "@rive-app", "RiveCanvas"],
    "Three.js": ["three.js", "THREE.", "WebGLRenderer"],
    "AOS": ["aos.js", "data-aos"],
    "Anime.js": ["anime.js", "anime({"],
    "CSS only": [],  # detected via keyframes
}


def fetch_css(css_urls: list, base_url: str, assets_dir: Path) -> list:
    """Download all CSS files, save locally, return their text content."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    css_texts = []

    for i, url in enumerate(css_urls):
        try:
            full_url = urljoin(base_url, url)
            resp = requests.get(full_url, timeout=10)
            if resp.ok:
                text = resp.text
                css_texts.append({"url": full_url, "content": text})
                (assets_dir / f"style-{i:02d}.css").write_text(text, encoding="utf-8")
        except Exception as e:
            print(f"  ! Could not fetch CSS {url}: {e}")

    print(f"  → {len(css_texts)} CSS files downloaded")
    return css_texts


def extract_keyframes(css_text: str) -> list:
    """Extract all @keyframes definitions."""
    keyframes = []
    pattern = re.compile(r'@(?:-webkit-)?keyframes\s+([\w-]+)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', re.DOTALL)
    for match in pattern.finditer(css_text):
        name = match.group(1)
        body = match.group(2).strip()
        keyframes.append({"name": name, "definition": body[:300]})
    return keyframes


def extract_css_variables(css_text: str) -> dict:
    """Extract CSS custom properties (--var-name: value)."""
    variables = {}
    pattern = re.compile(r'--([\w-]+)\s*:\s*([^;]+);')
    for match in pattern.finditer(css_text):
        variables[f"--{match.group(1)}"] = match.group(2).strip()
    return variables


def extract_colors(css_text: str) -> list:
    """Extract all color values from CSS (hex, rgb, hsl)."""
    colors = set()
    hex_pattern = re.compile(r'#([0-9a-fA-F]{3,8})\b')
    rgb_pattern = re.compile(r'rgba?\([\d\s,.%]+\)')
    hsl_pattern = re.compile(r'hsla?\([\d\s,.%]+\)')

    for match in hex_pattern.finditer(css_text):
        val = f"#{match.group(1)}"
        if len(val) in [4, 7, 9]:
            colors.add(val.upper())

    for match in rgb_pattern.finditer(css_text):
        colors.add(match.group(0))

    for match in hsl_pattern.finditer(css_text):
        colors.add(match.group(0))

    return sorted(list(colors))


def extract_fonts(css_text: str) -> list:
    """Extract font-family declarations."""
    fonts = set()
    pattern = re.compile(r'font-family\s*:\s*([^;]+);')
    for match in pattern.finditer(css_text):
        raw = match.group(1).strip().strip("'\"")
        for font in raw.split(","):
            cleaned = font.strip().strip("'\"")
            if cleaned and cleaned.lower() not in ["inherit", "initial", "unset", "sans-serif", "serif", "monospace"]:
                fonts.add(cleaned)
    return sorted(list(fonts))


def extract_transitions(css_text: str) -> list:
    """Extract transition declarations."""
    transitions = set()
    pattern = re.compile(r'transition\s*:\s*([^;]+);')
    for match in pattern.finditer(css_text):
        transitions.add(match.group(1).strip())
    return list(transitions)[:20]


def detect_animation_libraries(js_urls: list, html: str) -> list:
    """Detect animation libraries from script URLs and HTML content."""
    detected = []
    combined = " ".join(js_urls) + html.lower()

    for lib, signatures in ANIMATION_LIBRARY_SIGNATURES.items():
        if lib == "CSS only":
            continue
        for sig in signatures:
            if sig.lower() in combined:
                detected.append(lib)
                break

    return list(set(detected))


def analyze(css_urls: list, js_urls: list, base_url: str, html: str, assets_dir: Path) -> dict:
    """Run full CSS analysis, return structured results."""
    css_files = fetch_css(css_urls, base_url, assets_dir)

    all_text = "\n".join(f["content"] for f in css_files)

    keyframes = extract_keyframes(all_text)
    variables = extract_css_variables(all_text)
    colors = extract_colors(all_text)
    fonts = extract_fonts(all_text)
    transitions = extract_transitions(all_text)
    animation_libraries = detect_animation_libraries(js_urls, html)

    if keyframes:
        animation_libraries.append("CSS Keyframes")

    print(f"  → {len(keyframes)} keyframes, {len(colors)} colors, {len(fonts)} fonts found")

    return {
        "keyframes": keyframes,
        "css_variables": variables,
        "colors": colors,
        "fonts": fonts,
        "transitions": transitions,
        "animation_libraries": list(set(animation_libraries)),
        "css_file_count": len(css_files),
    }
