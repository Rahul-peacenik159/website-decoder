# Frontend Developer Decode Prompt

Use this prompt when you want to understand exactly HOW a site's animations and interactions are built — technically.

Attach the full analysis report and say:

---

## Prompt

You are a senior frontend developer specializing in animation and interactive UI. I've shared a structured analysis of a website. Break down exactly how their animations and interactions are built — technically and specifically.

---

### 01 Animation Architecture

- What is the primary animation stack? (GSAP, CSS keyframes, Framer Motion, etc.)
- Are animations JS-driven, CSS-driven, or hybrid? What are the tradeoffs of their approach?
- Is this a "scroll-driven" site, a "load-driven" site, or "interaction-driven"? What percentage of animations fall into each category?

---

### 02 Scroll Animation Breakdown

- Which elements animate on scroll and what exactly happens to them? (translate, opacity, scale, draw, etc.)
- Are they using ScrollTrigger scrubbing (animation tied to scroll speed) or snap (fires when element hits viewport)?
- Are any sections "pinned" during scroll (element stays fixed while content animates past)?
- How is the scroll progress mapped to visual change? Is it subtle or dramatic?

---

### 03 Entrance Animation Patterns

- How does the hero section animate on load? What's the sequence?
- Is text animated at the character, word, or line level?
- What easing functions are being used? Are they standard (ease-in-out) or custom cubic-bezier springs?
- What is the stagger timing between sequential elements? (e.g. 80ms apart, 150ms apart)

---

### 04 Illustration Animation Breakdown

- Which SVG elements are animated and how? (rotation, draw, path follow, scale, opacity)
- Is the SVG animation driven by CSS keyframes or JS (GSAP)?
- How does the illustration animation sync with surrounding copy? (Does text reveal as illustration draws? Do they animate together or in sequence?)
- Are illustrations broken into layers/groups for independent animation?
- What technique creates the "draw" effect on SVG paths? (stroke-dashoffset?)
- Are any elements following a motion path?

---

### 05 Hover & Interaction States

- What happens on hover — transform, color change, shadow, scale?
- Are hover transitions instant or eased? What duration?
- Are there any cursor-following effects or magnetic button effects?
- Do cards tilt or respond to mouse position (3D perspective)?

---

### 06 Color in Motion

- How does color change during animation? (e.g. elements fade from grey to purple as they enter)
- Are gradients animated?
- Is color used to signal progress through a scroll sequence?
- How does the illustration palette relate to the page's brand colors?

---

### 07 Performance Signals

- Are they using `will-change`, `transform: translateZ(0)`, or GPU-composited properties?
- Are heavy animations paused off-screen (IntersectionObserver)?
- Do they use `prefers-reduced-motion` media query?
- What would be the biggest performance risk in this animation stack?

---

### 08 How I'd Rebuild It

For each major animation effect on the page, give me:
- **What the effect is** (in plain terms)
- **The exact technique** to recreate it (CSS-only vs GSAP, what properties, rough code concept)
- **Difficulty level** (easy / medium / hard)
- **Free vs paid tools needed**

---

### 09 Three Things I'd Steal Immediately

Pick the 3 most clever or effective animation techniques on this site and explain:
1. What makes it work so well (psychologically and technically)
2. Exactly how to implement it
3. Where it would work best on my own site

---

_Attach the full report markdown + animation inspector output below this prompt._
