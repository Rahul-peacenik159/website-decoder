"""
structure.py — Parses HTML to extract site structure.
Maps: navigation, sections, headings, CTAs, meta info, and semantic layout.
"""

from bs4 import BeautifulSoup
import re


def analyze(html: str, url: str) -> dict:
    """Parse HTML and return structured site map."""
    soup = BeautifulSoup(html, "lxml")

    return {
        "meta": _extract_meta(soup),
        "navigation": _extract_nav(soup),
        "sections": _extract_sections(soup),
        "headings": _extract_headings(soup),
        "ctas": _extract_ctas(soup),
        "forms": _extract_forms(soup),
        "social_links": _extract_social(soup),
    }


def _extract_meta(soup) -> dict:
    meta = {}
    title = soup.find("title")
    meta["title"] = title.text.strip() if title else ""

    for name in ["description", "keywords", "og:title", "og:description", "twitter:title"]:
        tag = soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"property": name})
        if tag:
            meta[name] = tag.get("content", "").strip()

    return meta


def _extract_nav(soup) -> dict:
    nav_links = []
    nav = soup.find("nav") or soup.find(attrs={"role": "navigation"})
    if nav:
        for a in nav.find_all("a", href=True):
            text = a.get_text(strip=True)
            if text:
                nav_links.append({"text": text, "href": a["href"]})

    return {"links": nav_links, "found": bool(nav)}


def _extract_sections(soup) -> list:
    sections = []

    # Find semantic sections, divs with section-like classes
    section_tags = soup.find_all(["section", "main", "article"])
    if not section_tags:
        # Fallback: large divs that look like sections
        section_tags = soup.find_all("div", class_=re.compile(
            r'section|hero|banner|feature|about|pricing|testimonial|footer|cta|team|faq',
            re.I
        ))

    for i, section in enumerate(section_tags[:20]):
        heading = section.find(["h1", "h2", "h3"])
        paragraphs = section.find_all("p")
        text_preview = heading.get_text(strip=True) if heading else (
            paragraphs[0].get_text(strip=True)[:80] if paragraphs else ""
        )

        classes = " ".join(section.get("class", []))
        id_attr = section.get("id", "")

        sections.append({
            "index": i + 1,
            "tag": section.name,
            "id": id_attr,
            "classes": classes[:80],
            "heading": text_preview,
            "paragraph_count": len(paragraphs),
            "has_image": bool(section.find(["img", "svg", "canvas", "video"])),
            "has_cta": bool(section.find("a", class_=re.compile(r'btn|button|cta', re.I))),
        })

    return sections


def _extract_headings(soup) -> dict:
    headings = {"h1": [], "h2": [], "h3": []}
    for level in ["h1", "h2", "h3"]:
        for tag in soup.find_all(level):
            text = tag.get_text(strip=True)
            if text and len(text) > 2:
                headings[level].append(text)
    return headings


def _extract_ctas(soup) -> list:
    ctas = []
    # Buttons and CTA-like links
    candidates = soup.find_all(["button", "a"], class_=re.compile(
        r'btn|button|cta|primary|get-started|sign-up|download|try|start',
        re.I
    ))

    # Also any link with short, action-oriented text
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if text and len(text) < 50 and any(w in text.lower() for w in [
            "get", "start", "try", "sign", "download", "book", "join", "subscribe", "buy", "free", "demo"
        ]):
            candidates.append(a)

    seen = set()
    for el in candidates:
        text = el.get_text(strip=True)
        href = el.get("href", "")
        key = text.lower()
        if text and key not in seen and len(text) < 80:
            seen.add(key)
            ctas.append({"text": text, "href": href, "tag": el.name})

    return ctas[:15]


def _extract_forms(soup) -> list:
    forms = []
    for form in soup.find_all("form"):
        inputs = [i.get("type", "text") for i in form.find_all("input")]
        submit = form.find(["button", "input"], attrs={"type": "submit"})
        submit_text = submit.get_text(strip=True) if submit else ""
        forms.append({
            "input_types": inputs,
            "submit_text": submit_text,
            "action": form.get("action", ""),
        })
    return forms


def _extract_social(soup) -> list:
    social_patterns = re.compile(
        r'twitter\.com|linkedin\.com|instagram\.com|facebook\.com|youtube\.com|github\.com|tiktok\.com',
        re.I
    )
    socials = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if social_patterns.search(href) and href not in seen:
            seen.add(href)
            socials.append(href)
    return socials
