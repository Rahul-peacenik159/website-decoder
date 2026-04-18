# Website Decoder

Analyze any website and generate a structured PMM + brand brief — screenshots, color palette, CSS animations, site structure, illustration style — all in one markdown report.

Built to work with Claude Code for competitive research and brand decoding.

---

## How it works

1. You trigger the GitHub Actions workflow with a URL
2. It runs a headless Playwright browser in the cloud
3. Captures full-page + section screenshots
4. Downloads and parses all CSS (keyframes, colors, fonts, animations)
5. Maps site structure (nav, sections, headings, CTAs)
6. Extracts color palette from screenshots
7. Detects animation libraries (GSAP, Lottie, Rive, Framer Motion, etc.)
8. Commits everything back into this repo as a markdown report

---

## Usage

### Option A: GitHub Actions (no local setup)

1. Go to **Actions** tab in this repo
2. Click **Website Decoder** → **Run workflow**
3. Paste the URL (e.g. `https://wisprflow.ai`)
4. Click **Run workflow**
5. Wait ~2 minutes
6. Pull the repo — find your report in `output/reports/` and screenshots in `output/screenshots/`

### Option B: With Claude Code

```bash
# In Claude Code, just say:
# "Analyze https://wisprflow.ai and decode it as a PMM"
# Claude will run the workflow, wait for it, pull results, and give you the full decode.

gh workflow run analyze.yml -f url="https://wisprflow.ai"
gh run watch
git pull
```

### Option C: Run locally

```bash
pip install -r requirements.txt
playwright install chromium
python analyze.py https://wisprflow.ai
```

---

## Output structure

```
output/
├── screenshots/
│   └── {domain}/
│       └── {timestamp}/
│           ├── full-page.png
│           ├── section-00.png
│           ├── section-01.png
│           └── ...
├── reports/
│   └── report-{domain}.md       ← Main analysis report
└── assets/
    └── {domain}/
        ├── style-00.css          ← Downloaded CSS files
        └── ...
```

---

## PMM Decode

After the report is generated, copy the prompt from `prompts/pmm_decode.md` and paste it into Claude with the report attached. Claude will give you:

- Core positioning + ICP
- Brand personality + color/type analysis
- Visual and illustration strategy
- CTA and GTM motion signals
- Competitive positioning signals
- What to steal, what to avoid

---

## Stack

- **Playwright** — headless browser, screenshots
- **BeautifulSoup4** — HTML parsing
- **tinycss2** — CSS parsing
- **ColorThief** — color palette extraction
- **GitHub Actions** — cloud runner
