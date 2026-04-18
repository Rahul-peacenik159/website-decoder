# PPT Content Generation Prompt

You are a presentation designer and brand strategist. I will provide you with three analysis documents about a website: a PMM brand decode, a frontend/animation decode, a design/illustration decode, and the raw analysis report.

Synthesize these into a structured JSON object for a 14-slide PowerPoint deck.

## Output Rules

- Return ONLY valid JSON. No markdown fences, no explanation, no text before or after the JSON.
- Start your response with `{` and end with `}`.
- All strings must be properly escaped JSON strings.
- `body` arrays contain plain strings, one bullet per string. Do not include bullet characters.
- Strings with ✓ and ✗ prefixes are allowed in the What to Steal / Avoid slide only.
- `screenshot` values must be filenames only (e.g. "section-03.png"), chosen from the Available Screenshots list.
- `bg_color` and `accent_color` must be hex strings like "#1A1A2E". Use actual colors from the brand palette.
- `colors` arrays contain 4–8 objects with `hex` and `role` keys.
- `subtitle` may be null.
- All 14 slides must be present in the `slides` array, in order.
- `body` bullet max length: 15 words per bullet.

## Required Slide Structure

Generate exactly these 14 slides in this order:

Slide 1 — layout: "cover"
  title: site H1 headline
  subtitle: domain name
  screenshot: "section-00.png"
  bg_color: darkest brand color
  accent_color: primary brand color

Slide 2 — layout: "two-column"
  title: "Brand Identity at a Glance"
  body: 5 brand adjectives as bullets, then visual style sentence, then first-impression emotion
  screenshot: "section-01.png"
  accent_color: primary brand color

Slide 3 — layout: "bullets"
  title: "Core Positioning"
  subtitle: null
  body: ["One-liner: ...", "ICP: ...", "Pain point: ...", "Category: ..."]
  accent_color: primary brand color

Slide 4 — layout: "two-column"
  title: "Messaging Architecture"
  body: ["H1: " + exact H1, then 3 key H2s each as a bullet]
  screenshot: "section-02.png"
  accent_color: primary brand color

Slide 5 — layout: "bullets"
  title: "GTM Motion & CTA Strategy"
  subtitle: null
  body: ["GTM type: ...", "Primary CTA: ...", "Funnel signal: ...", "Trust approach: ..."]
  accent_color: primary brand color

Slide 6 — layout: "color-palette"
  title: "Brand Color System"
  colors: extract 4–8 key colors from the Color Palette section, with descriptive roles
  accent_color: primary brand color

Slide 7 — layout: "two-column"
  title: "Visual Identity"
  body: ["Illustration style: ...", "Animation intent: ...", "Emotional register: ...", "Visual weight: ..."]
  screenshot: "section-03.png"
  accent_color: primary brand color

Slide 8 — layout: "bullets"
  title: "Animation Stack"
  subtitle: null
  body: ["Primary library: ...", "Scroll animations: ...", "Load animations: ...", "Easing approach: ..."]
  accent_color: primary brand color

Slide 9 — layout: "bullets"
  title: "3 Animation Techniques to Steal"
  subtitle: null
  body: ["1. ...", "2. ...", "3. ..."] — from the frontend decode "Three Things I'd Steal" section
  accent_color: primary brand color

Slide 10 — layout: "two-column"
  title: "Illustration System Deep Dive"
  body: ["Style: ...", "Color usage: ...", "Built for animation: ...", "Depth technique: ..."]
  screenshot: "section-04.png"
  accent_color: primary brand color

Slide 11 — layout: "bullets"
  title: "What to Steal / What to Avoid"
  subtitle: null
  body: ["✓ Steal: ...", "✓ Steal: ...", "✓ Steal: ...", "✗ Avoid: ...", "✗ Avoid: ..."]
  accent_color: primary brand color

Slide 12 — layout: "bullets"
  title: "How to Replicate This Design System"
  subtitle: null
  body: ["Style rule: ...", "Color system: ...", "Animation rule: ...", "Tool: ...", "Build first: ..."]
  accent_color: primary brand color

Slide 13 — layout: "bullets"
  title: "Competitive Signals"
  subtitle: null
  body: ["Category owned: ...", "Benchmarks: ...", "JTBD framing: ...", "Key differentiator: ..."]
  accent_color: primary brand color

Slide 14 — layout: "quote"
  quote: the one-line positioning brief from the PMM decode (max 40 words)
  attribution: domain name
  bg_color: darkest brand color
  accent_color: primary brand color

## Full JSON Template

{
  "title": "Website Decode: DOMAIN",
  "slides": [
    {"id": 1, "layout": "cover", "title": "...", "subtitle": "...", "screenshot": "section-00.png", "bg_color": "#hex", "accent_color": "#hex"},
    {"id": 2, "layout": "two-column", "title": "Brand Identity at a Glance", "body": ["...", "...", "..."], "screenshot": "section-01.png", "accent_color": "#hex"},
    {"id": 3, "layout": "bullets", "title": "Core Positioning", "subtitle": null, "body": ["...", "..."], "accent_color": "#hex"},
    {"id": 4, "layout": "two-column", "title": "Messaging Architecture", "body": ["...", "..."], "screenshot": "section-02.png", "accent_color": "#hex"},
    {"id": 5, "layout": "bullets", "title": "GTM Motion & CTA Strategy", "subtitle": null, "body": ["...", "..."], "accent_color": "#hex"},
    {"id": 6, "layout": "color-palette", "title": "Brand Color System", "colors": [{"hex": "#hex", "role": "Primary"}, {"hex": "#hex", "role": "Background"}], "accent_color": "#hex"},
    {"id": 7, "layout": "two-column", "title": "Visual Identity", "body": ["...", "..."], "screenshot": "section-03.png", "accent_color": "#hex"},
    {"id": 8, "layout": "bullets", "title": "Animation Stack", "subtitle": null, "body": ["...", "..."], "accent_color": "#hex"},
    {"id": 9, "layout": "bullets", "title": "3 Animation Techniques to Steal", "subtitle": null, "body": ["1. ...", "2. ...", "3. ..."], "accent_color": "#hex"},
    {"id": 10, "layout": "two-column", "title": "Illustration System Deep Dive", "body": ["...", "..."], "screenshot": "section-04.png", "accent_color": "#hex"},
    {"id": 11, "layout": "bullets", "title": "What to Steal / What to Avoid", "subtitle": null, "body": ["✓ Steal: ...", "✓ Steal: ...", "✓ Steal: ...", "✗ Avoid: ...", "✗ Avoid: ..."], "accent_color": "#hex"},
    {"id": 12, "layout": "bullets", "title": "How to Replicate This Design System", "subtitle": null, "body": ["...", "..."], "accent_color": "#hex"},
    {"id": 13, "layout": "bullets", "title": "Competitive Signals", "subtitle": null, "body": ["...", "..."], "accent_color": "#hex"},
    {"id": 14, "layout": "quote", "quote": "...", "attribution": "DOMAIN", "bg_color": "#hex", "accent_color": "#hex"}
  ],
  "meta": {
    "domain": "DOMAIN",
    "run_id": "RUN_ID",
    "screenshot_path": "output/screenshots/DOMAIN/RUN_ID"
  }
}

## Source documents follow below.
