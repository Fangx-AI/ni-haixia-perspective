#!/usr/bin/env python3
"""Validate the public skill's runtime structure without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from build_case_index import build


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "expression_style.md",
    "references/medical-help-protocol.md",
    "references/distilled/01-six-meridian-quick-ref.md",
    "references/distilled/02-formula-differentiation.md",
    "references/distilled/03-medical-intake.md",
    "references/distilled/04-source-and-safety.md",
    "cases/case-index.json",
    *[f"modules/{number:02d}-{name}.md" for number, name in [
        (1, "six-meridian"),
        (2, "formula-map"),
        (3, "huangdi-baseline"),
        (4, "jingui-map"),
        (5, "bencao-acupuncture"),
        (6, "liangdong-claims"),
        (7, "critical-illness"),
        (8, "common-questions"),
    ]],
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_required_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8-sig")
    if not skill.startswith("---\nname: ni-haixia-perspective\n"):
        fail("SKILL.md frontmatter is missing or malformed")
    for path in REQUIRED[1:]:
        if (path.startswith("modules/") or path == "cases/case-index.json") and path not in skill:
            fail(f"SKILL.md does not route to {path}")
    for route in ("expression_style.md", "references/distilled/"):
        if route not in skill:
            fail(f"SKILL.md does not route to {route}")


def validate_json() -> None:
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8-sig"))


def validate_case_index() -> None:
    source = ROOT / "references/source-registry/global-source-registry.json"
    index_path = ROOT / "cases/case-index.json"
    current = json.loads(index_path.read_text(encoding="utf-8"))
    regenerated = build(source)
    if current != regenerated:
        fail("cases/case-index.json is stale; run scripts/build_case_index.py")

    cases = current["cases"]
    if current["unique_indexed_count"] != len(cases):
        fail("case count metadata does not match case records")
    if any(not item.get("source_url") for item in cases):
        fail("case index contains an empty source URL")
    if len({item["case_id"] for item in cases}) != len(cases):
        fail("case index contains duplicate IDs")
    if len({item["provenance_family_id"] for item in cases}) != len(cases):
        fail("case index contains duplicate provenance families")


def validate_markdown_links() -> None:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    broken: list[str] = []
    for page in ROOT.rglob("*.md"):
        for raw in pattern.findall(page.read_text(encoding="utf-8-sig")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (page.parent / target).resolve().exists():
                broken.append(f"{page.relative_to(ROOT)} -> {raw}")
    if broken:
        fail("broken local Markdown links:\n" + "\n".join(broken))


def main() -> None:
    validate_required_files()
    validate_json()
    validate_case_index()
    validate_markdown_links()
    print("runtime validation passed")


if __name__ == "__main__":
    main()
