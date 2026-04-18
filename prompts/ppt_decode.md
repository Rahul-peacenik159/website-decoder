# PPT Content Generation Prompt

You are a senior product marketing strategist and presentation designer. I will provide you with three analysis documents about a website: a PMM brand decode, a frontend/animation decode, a design/illustration decode, and the raw analysis report.

Synthesize these into a structured JSON object for a **17-slide PowerPoint presentation** with deep PMM content.

## Output Rules

- Return ONLY valid JSON. No markdown fences, no explanation, no text before or after.
- Start your response with `{` and end with `}`.
- All strings must be properly escaped JSON strings.
- `body` arrays: plain strings, one bullet per string, no bullet characters.
- Strings with ✓ and ✗ prefixes are allowed in steal/avoid slides only.
- `screenshot` values must be exact filenames from the Available Screenshots list.
- `bg_color` and `accent_color` must be real hex strings from the brand palette.
- `colors` arrays: 4–8 objects with `hex` and `role` keys.
- `subtitle` may be null.
- All 17 slides must be present in order.
- Bullet max length: 18 words. Be specific — use exact copy, real numbers, real CTAs from the report.

## Slide Structure (17 slides)

---

**Slide 1 — layout: "cover"**
title: exact H1 from the site
subtitle: domain name
screenshot: "section-00.png"
bg_color: darkest brand color
accent_color: primary brand color

---

**Slide 2 — layout: "two-column"**
title: "Brand Identity at a Glance"
body (7 items):
- 5 brand personality adjectives (one per bullet)
- "Visual style: [describe in 8 words]"
- "First impression: [emotion they trigger in 8 words]"
screenshot: "section-01.png"
accent_color: primary brand color

---

**Slide 3 — layout: "bullets"**
title: "Core Positioning"
subtitle: null
body (5 items):
- "Positioning: [one sentence, max 18 words — what they do + who for + why different]"
- "Category play: [the market category they are trying to own or create]"
- "Wedge message: [the specific fear/urgency they lead with — exact words from site if possible]"
- "Primary value prop: [most important benefit they claim]"
- "Secondary value prop: [second most important benefit they claim]"
accent_color: primary brand color

---

**Slide 4 — layout: "bullets"**
title: "ICP & Buyer Profile"
subtitle: "Who they are selling to and how they speak to them"
body (6 items):
- "Primary buyer: [exact title/role — e.g. CISO, VP Engineering, Head of Growth]"
- "Industries targeted: [list the specific verticals from nav/solutions pages]"
- "Company stage/size: [enterprise, mid-market, startup — infer from pricing/CTA/nav]"
- "Buyer sophistication: [technical, executive, broad market — and what signals confirm this]"
- "Pain trigger: [the specific moment or event that makes them look for this product]"
- "Objection they pre-empt: [what doubt or fear does the site address before being asked]"
accent_color: primary brand color

---

**Slide 5 — layout: "two-column"**
title: "Messaging Architecture"
body (5 items):
- "H1: [exact H1 from site]"
- "Key H2: [most important section headline]"
- "Key H2: [second most important section headline]"
- "Key H2: [third most important section headline]"
- "Sub-headline: [most interesting H3 or supporting copy line]"
screenshot: "section-02.png"
accent_color: primary brand color

---

**Slide 6 — layout: "bullets"**
title: "Messaging Framework Deep Dive"
subtitle: "How they structure the narrative top to bottom"
body (6 items):
- "Hook (above fold): [exact hook copy or paraphrase — what grabs attention first]"
- "Problem frame: [how they define the problem — whose fault, how big, how urgent]"
- "Solution introduction: [how they introduce their product as the answer]"
- "Proof point: [the specific stat, customer, or claim they use to build trust]"
- "Feature-to-benefit translation: [how they connect features to buyer outcomes]"
- "Closing argument: [what they say in the last CTA section to drive action]"
accent_color: primary brand color

---

**Slide 7 — layout: "bullets"**
title: "GTM Motion & CTA Strategy"
subtitle: null
body (6 items):
- "GTM motion: [PLG / SLG / hybrid — and what signals confirm this]"
- "Primary CTA: [exact button text] → [what it leads to] — [what this signals about funnel]"
- "Secondary CTA: [exact button text] → [what it leads to]"
- "Lead magnet: [any free tool, assessment, report, or trial they offer]"
- "Trust signals before conversion: [social proof, logos, case studies used before CTA]"
- "Friction level: [describe form length, steps, barriers, and whether it matches the ask]"
accent_color: primary brand color

---

**Slide 8 — layout: "color-palette"**
title: "Brand Color System"
colors: extract 6–8 key colors from Color Palette section, use descriptive roles
accent_color: primary brand color

---

**Slide 9 — layout: "two-column"**
title: "Visual Identity"
body (5 items):
- "Illustration style: [flat / isometric / line art / abstract data-viz / character-based]"
- "Why this style: [the strategic reason — what does it signal to the buyer]"
- "Animation intent: [aggressive / subtle / ambient — what emotion does it create]"
- "Hero hierarchy: [text-first / visual-first / interaction-first — and what it means]"
- "Product shown directly or abstracted: [and why that choice was made]"
screenshot: "section-03.png"
accent_color: primary brand color

---

**Slide 10 — layout: "bullets"**
title: "Animation Stack"
subtitle: "How it's built technically"
body (5 items):
- "Primary stack: [list all animation libraries detected]"
- "Scroll animations: [what fires on scroll — describe the pattern]"
- "Load animations: [what fires on page load — hero sequence]"
- "Text animation: [character / word / line level — and which library handles it]"
- "Easing: [specific easing functions used — cubic-bezier values if available]"
accent_color: primary brand color

---

**Slide 11 — layout: "bullets"**
title: "3 Animation Techniques to Steal"
subtitle: null
body (3 items — each must be a single crisp actionable sentence):
- "1. [technique name]: [what it does + why it works + one sentence on how to implement]"
- "2. [technique name]: [what it does + why it works + one sentence on how to implement]"
- "3. [technique name]: [what it does + why it works + one sentence on how to implement]"
accent_color: primary brand color

---

**Slide 12 — layout: "two-column"**
title: "Illustration System Deep Dive"
body (5 items):
- "Style: [core illustration style in 6 words]"
- "Custom or library: [and what signals confirm this]"
- "Built for animation: [yes/no + how you can tell]"
- "Color in illustrations: [how many hues, how they relate to brand palette]"
- "Depth technique: [how depth/shadow is created without 3D]"
screenshot: "section-04.png"
accent_color: primary brand color

---

**Slide 13 — layout: "bullets"**
title: "What to Steal / What to Avoid"
subtitle: null
body (5 items):
- "✓ Steal: [specific, actionable technique #1 — name it, explain why it works]"
- "✓ Steal: [specific, actionable technique #2]"
- "✓ Steal: [specific, actionable technique #3]"
- "✗ Avoid: [specific weakness #1 — name it, explain why it hurts]"
- "✗ Avoid: [specific weakness #2]"
accent_color: primary brand color

---

**Slide 14 — layout: "bullets"**
title: "How to Replicate This Design System"
subtitle: "Minimum viable build to get 80% of the visual impact"
body (5 items):
- "Style rule: [one sentence defining the illustration rules for a designer or AI tool]"
- "Color system: [how many colors, what roles — dark anchor + glow + tints + success]"
- "Animation rule: [what moves, what stays still, timing principles]"
- "Tools: [Figma / AE + Bodymovin / GSAP / Rive — specific to this site's stack]"
- "Build first: [the single highest-impact illustration or animation to build first]"
accent_color: primary brand color

---

**Slide 15 — layout: "bullets"**
title: "Competitive Signals"
subtitle: null
body (5 items):
- "Category they're owning: [exact category name + whether they coined it or entered it]"
- "Benchmark 1: [company name] — [what specific element Cyera is mirroring or differentiating from]"
- "Benchmark 2: [company name] — [same format]"
- "JTBD framing: [the job-to-be-done in the buyer's own words — the outcome they're hiring for]"
- "Differentiation signal: [the single most specific claim that no competitor is making]"
accent_color: primary brand color

---

**Slide 16 — layout: "two-column"**
title: "Design–Copy Harmony"
body (5 items):
- "Does illustration reinforce headline: [yes/no + how]"
- "Metaphor system: [the through-line metaphor across the whole page]"
- "Color as narrative: [how color shifts signal the emotional journey]"
- "Icon/illustration consistency: [same style register or different — and why]"
- "One design principle this site nails: [the single most clever design decision]"
screenshot: "section-05.png"
accent_color: primary brand color

---

**Slide 17 — layout: "quote"**
quote: the one-line positioning brief from the PMM decode (max 40 words, must be a complete, punchy sentence)
attribution: domain name
bg_color: darkest brand color
accent_color: primary brand color

---

## JSON Template

{
  "title": "Website Decode: DOMAIN",
  "slides": [
    {"id": 1,  "layout": "cover",         "title": "...", "subtitle": "...", "screenshot": "section-00.png", "bg_color": "#hex", "accent_color": "#hex"},
    {"id": 2,  "layout": "two-column",    "title": "Brand Identity at a Glance", "body": ["...x7"], "screenshot": "section-01.png", "accent_color": "#hex"},
    {"id": 3,  "layout": "bullets",       "title": "Core Positioning", "subtitle": null, "body": ["...x5"], "accent_color": "#hex"},
    {"id": 4,  "layout": "bullets",       "title": "ICP & Buyer Profile", "subtitle": "...", "body": ["...x6"], "accent_color": "#hex"},
    {"id": 5,  "layout": "two-column",    "title": "Messaging Architecture", "body": ["...x5"], "screenshot": "section-02.png", "accent_color": "#hex"},
    {"id": 6,  "layout": "bullets",       "title": "Messaging Framework Deep Dive", "subtitle": "...", "body": ["...x6"], "accent_color": "#hex"},
    {"id": 7,  "layout": "bullets",       "title": "GTM Motion & CTA Strategy", "subtitle": null, "body": ["...x6"], "accent_color": "#hex"},
    {"id": 8,  "layout": "color-palette", "title": "Brand Color System", "colors": [{"hex": "#hex", "role": "..."}], "accent_color": "#hex"},
    {"id": 9,  "layout": "two-column",    "title": "Visual Identity", "body": ["...x5"], "screenshot": "section-03.png", "accent_color": "#hex"},
    {"id": 10, "layout": "bullets",       "title": "Animation Stack", "subtitle": "...", "body": ["...x5"], "accent_color": "#hex"},
    {"id": 11, "layout": "bullets",       "title": "3 Animation Techniques to Steal", "subtitle": null, "body": ["...x3"], "accent_color": "#hex"},
    {"id": 12, "layout": "two-column",    "title": "Illustration System Deep Dive", "body": ["...x5"], "screenshot": "section-04.png", "accent_color": "#hex"},
    {"id": 13, "layout": "bullets",       "title": "What to Steal / What to Avoid", "subtitle": null, "body": ["✓...", "✓...", "✓...", "✗...", "✗..."], "accent_color": "#hex"},
    {"id": 14, "layout": "bullets",       "title": "How to Replicate This Design System", "subtitle": "...", "body": ["...x5"], "accent_color": "#hex"},
    {"id": 15, "layout": "bullets",       "title": "Competitive Signals", "subtitle": null, "body": ["...x5"], "accent_color": "#hex"},
    {"id": 16, "layout": "two-column",    "title": "Design–Copy Harmony", "body": ["...x5"], "screenshot": "section-05.png", "accent_color": "#hex"},
    {"id": 17, "layout": "quote",         "quote": "...", "attribution": "DOMAIN", "bg_color": "#hex", "accent_color": "#hex"}
  ],
  "meta": {
    "domain": "DOMAIN",
    "run_id": "RUN_ID",
    "screenshot_path": "output/screenshots/DOMAIN/RUN_ID"
  }
}

## Source documents follow below.
