"""
ppt_content.py — Calls Claude API with report + three decode files to produce
a structured ppt_content.json for the pptx-builder repo.
"""

import json
import os
import re
from pathlib import Path

import anthropic


def generate(
    report_path: str,
    domain: str,
    run_id: str,
    decodes_dir: Path,
    output_dir: Path,
) -> str | None:
    """
    Read the 3 decode files + report, call Claude with the ppt_decode prompt,
    parse the JSON response, and write ppt_content.json.
    Returns the path to the saved file, or None on failure.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    prompt_path = Path("prompts/ppt_decode.md")
    if not prompt_path.exists():
        print("  ! prompts/ppt_decode.md not found — skipping PPT content generation")
        return None

    prompt_text = prompt_path.read_text(encoding="utf-8")
    prompt_text = prompt_text.replace("DOMAIN", domain).replace("RUN_ID", run_id)

    report_text = Path(report_path).read_text(encoding="utf-8")

    decode_texts = {}
    for key, filename in [
        ("pmm", "pmm-decode.md"),
        ("frontend", "frontend-decode.md"),
        ("design", "design-decode.md"),
    ]:
        p = decodes_dir / filename
        decode_texts[key] = p.read_text(encoding="utf-8") if p.exists() else "(not available)"

    full_input = (
        f"{prompt_text}\n\n"
        f"---\n\n## PMM + Brand Decode\n\n{decode_texts['pmm']}\n\n"
        f"---\n\n## Frontend Developer Decode\n\n{decode_texts['frontend']}\n\n"
        f"---\n\n## Design + Illustration Decode\n\n{decode_texts['design']}\n\n"
        f"---\n\n## Raw Analysis Report\n\n{report_text}"
    )

    print("  → Generating PPT content JSON...")
    client = anthropic.Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=8096,
            messages=[{"role": "user", "content": full_input}],
        )
        raw = message.content[0].text.strip()
    except Exception as e:
        print(f"  ! Claude API call failed: {e}")
        return None

    # Strip accidental markdown fences
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw)
    raw = re.sub(r"\n?```\s*$", "", raw)
    raw = raw.strip()

    # Find the outermost JSON object if there's surrounding text
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        raw = match.group(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ! JSON parse error: {e}")
        print(f"  ! First 300 chars of response: {raw[:300]}")
        return None

    # Ensure meta is correct
    data["meta"] = {
        "domain": domain,
        "run_id": run_id,
        "screenshot_path": f"output/screenshots/{domain}/{run_id}",
    }

    # Cap bullet lengths to prevent overflow
    for slide in data.get("slides", []):
        if "body" in slide and isinstance(slide["body"], list):
            slide["body"] = [b[:120] for b in slide["body"]]

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "ppt_content.json"
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"    ✓ Saved: {out_path}")
    return str(out_path)
