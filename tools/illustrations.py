"""
illustrations.py — Detects illustration types, SVG usage,
animation libraries, and visual design patterns.
"""

from bs4 import BeautifulSoup
import re


LIBRARY_PATTERNS = {
    "GSAP": ["gsap.min.js", "gsap.js", "TweenMax", "gsap.com/r/"],
    "GSAP SplitText": ["SplitText"],
    "GSAP ScrollTrigger": ["ScrollTrigger"],
    "GSAP DrawSVG": ["DrawSVGPlugin"],
    "GSAP MotionPath": ["MotionPathPlugin"],
    "Lottie": ["lottie.min.js", "lottie-web", "bodymovin.js"],
    "Rive": ["rive.wasm", "@rive-app", "rive-canvas"],
    "Three.js": ["three.min.js", "three.js", "THREE."],
    "Framer Motion": ["framer-motion", "motion.js"],
    "AOS": ["aos.js", "aos.min.js"],
    "Anime.js": ["anime.min.js", "anime.js"],
    "Swiper": ["swiper.min.js", "swiper-bundle"],
    "Splide": ["splide.min.js"],
    "Spline": ["spline.design", "@splinetool"],
}


def analyze(html: str, js_urls: list) -> dict:
    soup = BeautifulSoup(html, "lxml")

    return {
        "svg": _analyze_svg(soup),
        "canvas": _analyze_canvas(soup),
        "video_bg": _analyze_video(soup),
        "animation_libraries": _detect_libraries(html, js_urls),
        "illustration_style": _guess_style(soup, html),
        "lottie_files": _find_lottie(html),
        "rive_files": _find_rive(html),
        "image_count": len(soup.find_all("img")),
        "webgl": _detect_webgl(html),
    }


def _analyze_svg(soup) -> dict:
    inline_svgs = soup.find_all("svg")
    external_svgs = [img["src"] for img in soup.find_all("img") if img.get("src", "").endswith(".svg")]

    # Count animated SVGs (those with animateTransform, animate, or CSS animation classes)
    animated_count = sum(
        1 for svg in inline_svgs
        if svg.find(["animateTransform", "animate", "animateMotion"])
        or any("anim" in " ".join(svg.get("class", [])).lower() for _ in [1])
    )

    return {
        "inline_count": len(inline_svgs),
        "external_count": len(external_svgs),
        "animated_count": animated_count,
        "external_files": external_svgs[:10],
    }


def _analyze_canvas(soup) -> dict:
    canvases = soup.find_all("canvas")
    return {
        "count": len(canvases),
        "ids": [c.get("id", "") for c in canvases if c.get("id")],
    }


def _analyze_video(soup) -> dict:
    videos = soup.find_all("video")
    bg_videos = [
        v for v in videos
        if "background" in " ".join(v.get("class", [])).lower()
        or v.get("autoplay") is not None
    ]
    return {
        "count": len(videos),
        "background_video_count": len(bg_videos),
        "has_autoplay": any(v.get("autoplay") is not None for v in videos),
    }


def _detect_libraries(html: str, js_urls: list) -> list:
    combined = html + " ".join(js_urls)
    detected = []

    for lib, patterns in LIBRARY_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in combined.lower():
                detected.append(lib)
                break

    return list(set(detected))


def _guess_style(soup, html: str) -> str:
    """Guess the overall illustration/visual style."""
    hints = []

    inline_svgs = len(soup.find_all("svg"))
    canvases = len(soup.find_all("canvas"))
    images = len(soup.find_all("img"))
    lottie = "lottie" in html.lower() or "bodymovin" in html.lower()
    rive = "rive" in html.lower()
    three = "three.js" in html.lower() or "webgl" in html.lower()
    spline = "spline" in html.lower()

    if three or spline:
        hints.append("3D / WebGL")
    if rive:
        hints.append("Rive vector animation")
    if lottie:
        hints.append("Lottie animation")
    if inline_svgs > 10:
        hints.append("heavy inline SVG illustration")
    elif inline_svgs > 3:
        hints.append("SVG icons/graphics")
    if canvases > 0:
        hints.append("canvas-based")
    if images > 20:
        hints.append("photo-heavy")
    elif images < 5:
        hints.append("minimal / mostly typographic")

    return ", ".join(hints) if hints else "standard (images + CSS)"


def _find_lottie(html: str) -> list:
    pattern = re.compile(r'["\']([^"\']+\.json)["\']')
    files = [m.group(1) for m in pattern.finditer(html) if "lottie" in m.group(1).lower() or "animation" in m.group(1).lower()]
    return files[:10]


def _find_rive(html: str) -> list:
    pattern = re.compile(r'["\']([^"\']+\.riv)["\']')
    return [m.group(1) for m in pattern.finditer(html)][:10]


def _detect_webgl(html: str) -> bool:
    return "webgl" in html.lower() or "WebGLRenderer" in html or "getContext('webgl')" in html
