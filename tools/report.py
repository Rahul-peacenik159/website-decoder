"""
report.py — Generates the final markdown analysis report.
Combines all tool outputs into a single structured brief.
"""

from datetime import datetime
from pathlib import Path


def generate(
    url: str,
    domain: str,
    browser_data: dict,
    css_data: dict,
    structure_data: dict,
    color_data: dict,
    illustration_data: dict,
    animation_data: dict,
    output_dir: Path,
    screenshots_rel_path: str,
) -> str:
    """Build and write the full markdown report. Returns path to report file."""

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []

    # Header
    lines += [
        f"# Website Decode: {domain}",
        f"",
        f"> **URL:** {url}  ",
        f"> **Analyzed:** {timestamp}  ",
        f"> **Page title:** {browser_data.get('page_title', '')}  ",
        f"> **Meta description:** {browser_data.get('meta_description', '')}",
        f"",
        f"---",
        f"",
    ]

    # 01 Site Structure
    lines += [
        f"## 01 Site Structure",
        f"",
        f"**Navigation links:**",
    ]
    nav = structure_data.get("navigation", {})
    for link in nav.get("links", []):
        lines.append(f"- {link['text']} → `{link['href']}`")
    if not nav.get("links"):
        lines.append("- (No nav detected)")

    lines += ["", f"**Sections found:** {len(structure_data.get('sections', []))}"]
    for section in structure_data.get("sections", []):
        marker = "🖼️ " if section["has_image"] else "  "
        cta_marker = " ◀ CTA" if section["has_cta"] else ""
        lines.append(f"{marker}**{section['index']}.** `{section['tag']}` — {section['heading'] or '(no heading)'}{cta_marker}")

    lines += [""]

    # 02 Messaging / Headings
    lines += [
        f"## 02 Messaging & Headlines",
        f"",
    ]
    headings = structure_data.get("headings", {})
    h1s = headings.get("h1", [])
    h2s = headings.get("h2", [])
    h3s = headings.get("h3", [])

    if h1s:
        lines.append(f"**H1 (main headline):**")
        for h in h1s[:3]:
            lines.append(f'> "{h}"')

    if h2s:
        lines.append(f"\n**H2 (section headlines):**")
        for h in h2s[:8]:
            lines.append(f"- {h}")

    if h3s:
        lines.append(f"\n**H3 (sub-headlines):**")
        for h in h3s[:6]:
            lines.append(f"- {h}")

    lines += [""]

    # 03 CTAs
    lines += [
        f"## 03 Calls to Action",
        f"",
    ]
    ctas = structure_data.get("ctas", [])
    if ctas:
        for cta in ctas:
            lines.append(f'- **"{cta["text"]}"** → `{cta["href"] or "#"}`')
    else:
        lines.append("- (No CTAs detected)")

    forms = structure_data.get("forms", [])
    if forms:
        lines.append(f"\n**Forms found:** {len(forms)}")
        for form in forms:
            lines.append(f"- Inputs: {', '.join(form['input_types'])} | Submit: \"{form['submit_text']}\"")

    lines += [""]

    # 04 Typography
    lines += [
        f"## 04 Typography",
        f"",
    ]
    fonts = css_data.get("fonts", [])
    if fonts:
        for font in fonts:
            lines.append(f"- `{font}`")
    else:
        lines.append("- (No explicit font-family declarations found in CSS)")

    lines += [""]

    # 05 Color Palette
    lines += [
        f"## 05 Color Palette",
        f"",
        f"| Color | Hex | Role |",
        f"|-------|-----|------|",
    ]
    for color in color_data.get("palette", []):
        lines.append(f"| ██ | `{color['hex']}` | {color['category']} |")

    # Also add CSS color variables
    css_vars = css_data.get("css_variables", {})
    color_vars = {k: v for k, v in css_vars.items() if any(
        x in v for x in ["#", "rgb", "hsl"]
    )}
    if color_vars:
        lines += [
            "",
            "**CSS custom properties (color tokens):**",
        ]
        for var, val in list(color_vars.items())[:20]:
            lines.append(f"- `{var}`: `{val}`")

    lines += [""]

    # 06 Animation & Interactions
    lines += [
        f"## 06 Animation & Interactions",
        f"",
        f"**Libraries detected:**",
    ]
    libs = illustration_data.get("animation_libraries", []) + css_data.get("animation_libraries", [])
    libs = list(set(libs))
    if libs:
        for lib in libs:
            lines.append(f"- {lib}")
    else:
        lines.append("- None detected (likely CSS-only animations)")

    keyframes = css_data.get("keyframes", [])
    if keyframes:
        lines += [
            f"\n**CSS @keyframes ({len(keyframes)} found):**",
        ]
        for kf in keyframes[:15]:
            lines.append(f"- `{kf['name']}`")

    transitions = css_data.get("transitions", [])
    if transitions:
        lines += [
            f"\n**Transitions (sample):**",
        ]
        for t in transitions[:8]:
            lines.append(f"- `{t}`")

    lines += [""]

    # 07 Visual / Illustration Style
    lines += [
        f"## 07 Visual & Illustration Style",
        f"",
        f"**Overall style:** {illustration_data.get('illustration_style', 'unknown')}",
        f"",
        f"| Element | Count |",
        f"|---------|-------|",
        f"| Inline SVGs | {illustration_data['svg']['inline_count']} |",
        f"| External SVGs | {illustration_data['svg']['external_count']} |",
        f"| Canvas elements | {illustration_data['canvas']['count']} |",
        f"| Images | {illustration_data.get('image_count', 0)} |",
        f"| Background videos | {illustration_data['video_bg']['background_video_count']} |",
        f"| WebGL detected | {'Yes' if illustration_data.get('webgl') else 'No'} |",
    ]

    if illustration_data.get("rive_files"):
        lines += ["", "**Rive animation files:**"]
        for f in illustration_data["rive_files"]:
            lines.append(f"- `{f}`")

    if illustration_data.get("lottie_files"):
        lines += ["", "**Lottie animation files:**"]
        for f in illustration_data["lottie_files"]:
            lines.append(f"- `{f}`")

    lines += [""]

    # 08 Social & External Links
    socials = structure_data.get("social_links", [])
    if socials:
        lines += [
            f"## 08 Social Presence",
            f"",
        ]
        for s in socials:
            lines.append(f"- {s}")
        lines += [""]

    # 08b Deep Animation Inspection
    if animation_data:
        lines += [
            f"## 08 Animation Inspector (Frontend Deep Dive)",
            f"",
        ]

        summary = animation_data.get("animation_triggers_summary", "")
        if summary:
            lines += [f"**How animations are triggered:**", f"> {summary}", ""]

        scroll_triggers = animation_data.get("scroll_triggers", [])
        if scroll_triggers:
            lines += ["**Scroll trigger mechanisms:**"]
            for t in scroll_triggers:
                lines.append(f"- **{t['type']}** — {t.get('description', '')}")
            lines.append("")

        gsap_hints = animation_data.get("gsap_timeline_hints", [])
        if gsap_hints:
            lines += ["**GSAP patterns detected:**"]
            for h in gsap_hints:
                lines.append(f"- `{h['pattern']}` — {h['what_it_does']}")
            lines.append("")

        stagger = animation_data.get("stagger_patterns", {})
        if stagger.get("detected"):
            lines += ["**Stagger patterns:**"]
            for p in stagger.get("patterns", []):
                lines.append(f"- {p}")
            lines.append("")

        timing = animation_data.get("timing_patterns", {})
        if timing.get("easing_functions"):
            lines += [f"**Easing functions used:**"]
            for e in timing["easing_functions"]:
                lines.append(f"- `{e}`")
            if timing.get("spring_detected"):
                lines.append("- ✦ **Spring/overshoot easing detected** (cubic-bezier with overshoot)")
            lines.append("")

        svg_comp = animation_data.get("svg_composition", [])
        if svg_comp:
            lines += [
                "**SVG Composition Breakdown:**",
                "",
                "| SVG | Groups | Paths | Circles | Colors Used | Animated |",
                "|-----|--------|-------|---------|-------------|----------|",
            ]
            for s in svg_comp:
                colors_str = ", ".join(s.get("colors_used", [])[:4])
                lines.append(
                    f"| #{s['index']} ({s.get('id') or s.get('class','') or 'unnamed'}) "
                    f"| {s['groups']} | {s['paths']} | {s['circles']} "
                    f"| {colors_str or '—'} | {'Yes' if s['has_native_animation'] else 'No'} |"
                )
            lines.append("")

        color_in_svgs = animation_data.get("color_in_illustrations", [])
        if color_in_svgs:
            lines += ["**How color is used inside illustrations:**"]
            for item in color_in_svgs:
                lines.append(
                    f"- SVG #{item['svg_index']}: {item['technique']} "
                    f"| fills: {', '.join(item['fill_colors'][:4]) or 'none'} "
                    f"| avg opacity: {item['avg_opacity']}"
                )
            lines.append("")

        pairs = animation_data.get("illustration_content_pairing", [])
        if pairs:
            lines += ["**Illustration ↔ Content relationships:**"]
            for p in pairs:
                lines.append(f"- {p['relationship']} | heading: \"{p['heading']}\"")
            lines.append("")

    # 09 Screenshots
    lines += [
        f"## 09 Screenshots",
        f"",
        f"**Full page:**  ",
        f"![Full page]({screenshots_rel_path}/full-page.png)",
        f"",
        f"**Sections:**",
    ]
    for i, shot in enumerate(browser_data.get("screenshots", [])[:12]):
        shot_name = Path(shot).name
        lines.append(f"![Section {i+1}]({screenshots_rel_path}/{shot_name})")

    lines += [
        "",
        "---",
        "",
        f"## 10 Decode Prompts",
        "",
        "Paste this report into Claude with any of these prompts depending on what you want to learn:",
        "",
        "| Prompt file | What you get |",
        "|-------------|-------------|",
        "| `prompts/pmm_decode.md` | Positioning, ICP, messaging, GTM motion, brand identity |",
        "| `prompts/frontend_decode.md` | Exactly HOW animations are built, timing, easing, SVG techniques, how to rebuild |",
        "| `prompts/design_decode.md` | Illustration style, color theory, composition, design-copy harmony, how to replicate |",
        "",
    ]

    report_text = "\n".join(lines)

    # Write report
    report_path = output_dir / f"report-{domain.replace('.', '-')}.md"
    report_path.write_text(report_text, encoding="utf-8")
    print(f"  → Report saved: {report_path}")

    return str(report_path)
