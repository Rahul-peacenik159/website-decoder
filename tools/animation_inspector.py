"""
animation_inspector.py — Deep-dives into HOW animations work on the page.

Goes beyond "GSAP detected" to map:
- Which elements animate
- What triggers them (scroll, load, hover, click)
- How illustrations relate to surrounding copy
- Timing, easing, stagger patterns
- SVG composition (grouping, layers, paths)
- How color is used within illustrations
"""

from bs4 import BeautifulSoup
import re


def analyze(html: str, css_texts: list, js_urls: list) -> dict:
    soup = BeautifulSoup(html, "lxml")
    all_css = "\n".join(c.get("content", "") for c in css_texts) if css_texts else ""
    all_js_hints = " ".join(js_urls)

    return {
        "scroll_triggers": _find_scroll_triggers(html, all_css),
        "load_animations": _find_load_animations(all_css),
        "hover_interactions": _find_hover_interactions(all_css),
        "svg_composition": _analyze_svg_composition(soup),
        "illustration_content_pairing": _find_illustration_content_pairs(soup),
        "timing_patterns": _extract_timing_patterns(all_css),
        "stagger_patterns": _detect_stagger(html, all_css),
        "color_in_illustrations": _color_in_svgs(soup),
        "animation_triggers_summary": _summarize_triggers(html, all_css),
        "gsap_timeline_hints": _find_gsap_hints(html),
        "scroll_animation_sections": _find_scroll_animated_sections(soup, html),
    }


def _find_scroll_triggers(html: str, css: str) -> list:
    """Find scroll-triggered animation patterns."""
    triggers = []

    # ScrollTrigger (GSAP)
    if "ScrollTrigger" in html:
        triggers.append({
            "type": "GSAP ScrollTrigger",
            "description": "Elements animate as they enter/leave the viewport during scroll",
            "pattern": "JS-driven, tied to scroll position"
        })

    # Intersection Observer
    if "IntersectionObserver" in html:
        triggers.append({
            "type": "IntersectionObserver",
            "description": "CSS classes toggled when elements enter viewport",
            "pattern": "JS adds class → CSS transition fires"
        })

    # AOS (Animate on Scroll)
    if "data-aos" in html or "aos.js" in html:
        data_aos_attrs = re.findall(r'data-aos=["\']([^"\']+)["\']', html)
        triggers.append({
            "type": "AOS (Animate On Scroll)",
            "description": "data-aos attributes drive entrance animations",
            "animations_used": list(set(data_aos_attrs))[:10],
            "pattern": "Library adds/removes class on scroll"
        })

    # CSS scroll-driven (modern)
    if "animation-timeline" in css or "scroll-timeline" in css:
        triggers.append({
            "type": "CSS Scroll-Driven Animation",
            "description": "Native CSS animation-timeline property (modern browsers)",
            "pattern": "Pure CSS, no JS needed"
        })

    # Waypoints
    if "waypoint" in html.lower():
        triggers.append({
            "type": "Waypoints.js",
            "description": "Callback fires when element hits scroll position",
            "pattern": "JS callback → class toggle → CSS"
        })

    return triggers


def _find_load_animations(css: str) -> list:
    """Find animations that fire on page load (no scroll trigger)."""
    load_anims = []

    # Look for animation declarations without scroll-class dependencies
    pattern = re.compile(
        r'(\.[\w-]+)\s*\{[^}]*animation\s*:\s*([^;]+);[^}]*animation-delay\s*:\s*([^;]+);',
        re.DOTALL
    )
    for match in pattern.finditer(css):
        selector = match.group(1)
        animation = match.group(2).strip()
        delay = match.group(3).strip()
        load_anims.append({
            "selector": selector,
            "animation": animation,
            "delay": delay,
        })

    # Simpler: find any animation with a delay (implies staggered load)
    if not load_anims:
        delay_pattern = re.compile(r'animation-delay\s*:\s*([\d.]+s)')
        delays = [m.group(1) for m in delay_pattern.finditer(css)]
        if delays:
            load_anims.append({
                "type": "staggered load animation",
                "delays_found": delays[:10],
                "description": "Elements animate in with staggered delays on page load"
            })

    return load_anims


def _find_hover_interactions(css: str) -> list:
    """Find hover-state animations and transitions."""
    hovers = []
    pattern = re.compile(r'([\w\s.#:-]+):hover\s*\{([^}]+)\}', re.DOTALL)

    for match in pattern.finditer(css):
        selector = match.group(1).strip()
        props = match.group(2).strip()
        if any(p in props for p in ["transform", "opacity", "color", "background", "box-shadow", "scale"]):
            hovers.append({
                "selector": selector[:60],
                "properties": props[:120].strip(),
            })

    return hovers[:12]


def _analyze_svg_composition(soup) -> list:
    """Break down how inline SVGs are structured and what they contain."""
    svg_breakdown = []

    for i, svg in enumerate(soup.find_all("svg")[:8]):
        groups = svg.find_all("g")
        paths = svg.find_all("path")
        circles = svg.find_all("circle")
        rects = svg.find_all("rect")
        texts = svg.find_all("text")
        animated = svg.find_all(["animate", "animateTransform", "animateMotion"])

        # Collect fill/stroke colors used in this SVG
        colors = set()
        for el in svg.find_all(True):
            for attr in ["fill", "stroke"]:
                val = el.get(attr, "")
                if val and val not in ["none", "currentColor", "inherit", ""]:
                    colors.add(val)
            # Inline style
            style = el.get("style", "")
            for m in re.finditer(r'(?:fill|stroke)\s*:\s*([^;)"]+)', style):
                colors.add(m.group(1).strip())

        # Named groups (layers)
        group_ids = [g.get("id", g.get("class", "")) for g in groups if g.get("id") or g.get("class")]

        svg_breakdown.append({
            "index": i + 1,
            "viewBox": svg.get("viewBox", ""),
            "groups": len(groups),
            "paths": len(paths),
            "circles": len(circles),
            "rects": len(rects),
            "text_elements": len(texts),
            "has_native_animation": len(animated) > 0,
            "colors_used": sorted(list(colors))[:8],
            "named_layers": [str(g)[:40] for g in group_ids[:5]],
            "class": " ".join(svg.get("class", [])),
            "id": svg.get("id", ""),
        })

    return svg_breakdown


def _find_illustration_content_pairs(soup) -> list:
    """Find how illustrations sit relative to text content — do they explain, decorate, or contrast?"""
    pairs = []

    # Look for sections/divs that contain both an SVG/image and text
    containers = soup.find_all(["section", "div"], class_=re.compile(
        r'feature|hero|section|card|block|row|col|split|grid',
        re.I
    ))

    for container in containers[:12]:
        has_svg = bool(container.find("svg"))
        has_img = bool(container.find("img"))
        has_heading = container.find(["h1", "h2", "h3"])
        has_paragraph = container.find("p")

        if (has_svg or has_img) and (has_heading or has_paragraph):
            heading_text = has_heading.get_text(strip=True) if has_heading else ""
            para_text = has_paragraph.get_text(strip=True)[:80] if has_paragraph else ""
            classes = " ".join(container.get("class", []))[:60]

            # Guess relationship
            relationship = "decorative"
            if has_svg and has_heading:
                relationship = "explanatory (illustration supports headline)"
            if "hero" in classes.lower():
                relationship = "hero — illustration as primary visual anchor"
            if "feature" in classes.lower():
                relationship = "feature card — icon/illustration + copy pair"

            pairs.append({
                "container_classes": classes,
                "has_svg": has_svg,
                "has_image": has_img,
                "heading": heading_text[:60],
                "copy_preview": para_text,
                "relationship": relationship,
            })

    return pairs[:8]


def _extract_timing_patterns(css: str) -> dict:
    """Extract easing functions, durations, and timing patterns."""
    easings = set()
    durations = set()

    easing_pattern = re.compile(
        r'(?:transition|animation)[^;]*(?:cubic-bezier\([^)]+\)|ease-in-out|ease-in|ease-out|ease|linear|spring)'
    )
    for match in easing_pattern.finditer(css):
        val = match.group(0)
        # Extract cubic-bezier
        cb = re.search(r'cubic-bezier\([^)]+\)', val)
        if cb:
            easings.add(cb.group(0))
        else:
            for keyword in ["ease-in-out", "ease-in", "ease-out", "linear", "ease"]:
                if keyword in val:
                    easings.add(keyword)

    duration_pattern = re.compile(r'(?:transition|animation)[^;]*\b([\d.]+s)\b')
    for match in duration_pattern.finditer(css):
        durations.add(match.group(1))

    return {
        "easing_functions": sorted(list(easings))[:10],
        "durations": sorted(list(durations))[:10],
        "spring_detected": "cubic-bezier(0.34" in css or "spring" in css.lower(),
        "uses_custom_easing": any("cubic-bezier" in e for e in easings),
    }


def _detect_stagger(html: str, css: str) -> dict:
    """Detect staggered animation patterns."""
    has_stagger = False
    stagger_hints = []

    # GSAP stagger
    if "stagger" in html.lower():
        has_stagger = True
        stagger_hints.append("GSAP stagger() — items animate in sequence with delay between each")

    # CSS nth-child delays
    nth_pattern = re.compile(r':nth-child\(\d+\)\s*\{[^}]*animation-delay')
    if nth_pattern.search(css):
        has_stagger = True
        stagger_hints.append("CSS :nth-child + animation-delay — manual stagger via CSS selectors")

    # Multiple animation-delay values close together
    delays = re.findall(r'animation-delay\s*:\s*([\d.]+)s', css)
    if len(delays) > 3:
        has_stagger = True
        stagger_hints.append(f"Multiple animation-delay values ({', '.join(sorted(set(delays))[:6])}s) — staggered entrance")

    # SplitText
    if "SplitText" in html:
        has_stagger = True
        stagger_hints.append("GSAP SplitText — text split into chars/words, animated with stagger")

    return {
        "detected": has_stagger,
        "patterns": stagger_hints,
    }


def _color_in_illustrations(soup) -> list:
    """How are colors used within SVG illustrations?"""
    findings = []

    for i, svg in enumerate(soup.find_all("svg")[:6]):
        fills = []
        strokes = []
        opacities = []

        for el in svg.find_all(True):
            fill = el.get("fill", "")
            stroke = el.get("stroke", "")
            opacity = el.get("opacity", el.get("fill-opacity", ""))

            if fill and fill not in ["none", "currentColor"]:
                fills.append(fill)
            if stroke and stroke not in ["none", "currentColor"]:
                strokes.append(stroke)
            if opacity:
                try:
                    opacities.append(float(opacity))
                except:
                    pass

        if fills or strokes:
            avg_opacity = round(sum(opacities) / len(opacities), 2) if opacities else 1.0
            findings.append({
                "svg_index": i + 1,
                "fill_colors": list(set(fills))[:6],
                "stroke_colors": list(set(strokes))[:6],
                "uses_opacity_layering": avg_opacity < 0.7 and len(opacities) > 2,
                "avg_opacity": avg_opacity,
                "color_count": len(set(fills + strokes)),
                "technique": _guess_illustration_technique(fills, strokes, opacities),
            })

    return findings


# Alias for export (same function, different name in the outline)
_color_in_svgs = _color_in_illustrations


def _guess_illustration_technique(fills, strokes, opacities) -> str:
    if not fills and strokes:
        return "outline/line art — stroke-only, no fills"
    if fills and not strokes:
        return "flat illustration — fills only, no outlines"
    if fills and strokes:
        avg_op = sum(opacities) / len(opacities) if opacities else 1.0
        if avg_op < 0.5:
            return "ghost/translucent style — heavy use of opacity layering"
        return "mixed — fills + strokes with varying opacity"
    return "unknown"


def _summarize_triggers(html: str, css: str) -> str:
    """One-paragraph plain English summary of how animations are triggered."""
    parts = []

    if "ScrollTrigger" in html:
        parts.append("Most animations fire as the user scrolls — GSAP ScrollTrigger pins and reveals elements section by section")
    elif "IntersectionObserver" in html:
        parts.append("Elements animate when they enter the viewport (IntersectionObserver toggles CSS classes)")
    elif "data-aos" in html:
        parts.append("AOS library drives entrance animations — elements slide/fade in as they scroll into view")

    if "animation-delay" in css:
        parts.append("load-time staggered entrance on the hero section")

    if ":hover" in css and "transform" in css:
        parts.append("hover states use transform (scale/translate) for interactive lift effects")

    if "SplitText" in html:
        parts.append("GSAP SplitText splits headlines into individual characters or words for wave/stagger reveals")

    if not parts:
        parts.append("Animations appear to be CSS-only with transitions and keyframes — no heavy JS animation library detected")

    return ". ".join(parts) + "."


def _find_gsap_hints(html: str) -> list:
    """Pull out GSAP-specific patterns from HTML/inline scripts."""
    hints = []

    gsap_patterns = {
        "gsap.to()": "Tween element TO these values",
        "gsap.from()": "Tween element FROM these values (entrance animation)",
        "gsap.fromTo()": "Full control — define start AND end state",
        "gsap.timeline()": "Sequence of animations chained in order",
        "ScrollTrigger.create": "Scroll-triggered animation with pin/scrub support",
        "stagger:": "Multiple elements animate in sequence",
        "scrub:": "Animation speed tied directly to scroll speed (scrubbing)",
        "pin:": "Element pinned while scroll animation plays out",
        "SplitText": "Text split into chars/words for granular animation",
        "DrawSVGPlugin": "SVG paths draw themselves (stroke-dashoffset technique)",
        "MotionPathPlugin": "Elements follow a curved SVG path",
    }

    for pattern, description in gsap_patterns.items():
        if pattern in html:
            hints.append({"pattern": pattern, "what_it_does": description})

    return hints


def _find_scroll_animated_sections(soup, html: str) -> list:
    """Find sections that are likely scroll-animated based on class names and attributes."""
    animated_sections = []

    animation_class_patterns = re.compile(
        r'animate|reveal|fade|slide|zoom|parallax|sticky|pin|trigger|aos|motion|scroll',
        re.I
    )

    for section in soup.find_all(["section", "div"])[:30]:
        classes = " ".join(section.get("class", []))
        data_attrs = {k: v for k, v in section.attrs.items() if k.startswith("data-")}

        if animation_class_patterns.search(classes) or data_attrs:
            heading = section.find(["h1", "h2", "h3"])
            animated_sections.append({
                "classes": classes[:80],
                "data_attributes": data_attrs,
                "heading": heading.get_text(strip=True)[:60] if heading else "",
            })

    return animated_sections[:10]
