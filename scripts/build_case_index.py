#!/usr/bin/env python3
"""Build a compact, metadata-only case index from the public source registry."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


TIER_PRIORITY = {
    "original_hantang_public_archive": 0,
    "secondary_mirror_with_origin_metadata": 1,
    "platform_reupload_or_clip_unverified": 2,
}

CATEGORY_KEYWORDS = {
    "cancer": ["癌", "腫瘤", "肿瘤", "骨髓瘤", "白血病", "腦瘤", "脑瘤"],
    "cardiovascular": ["心臟", "心脏", "心肌", "高血壓", "高血压", "中風", "中风", "動脈", "动脉"],
    "metabolic_renal": ["糖尿病", "尿毒", "腎衰", "肾衰", "洗腎", "洗肾", "透析", "肝硬化", "腹水"],
    "autoimmune_musculoskeletal": ["紅斑狼瘡", "红斑狼疮", "類風濕", "类风湿", "纖維肌痛", "纤维肌痛", "關節", "关节"],
    "neurological": ["癲癇", "癫痫", "帕金森", "漸凍", "渐冻", "ALS", "頭痛", "头痛"],
    "reproductive_womens_health": ["不孕", "月經", "月经", "痛經", "痛经", "婦人", "妇人", "懷孕", "怀孕", "產後", "产后"],
    "respiratory_ent": ["肺炎", "咳", "氣喘", "气喘", "感冒", "鼻炎", "鼻竇", "鼻窦", "中耳"],
    "digestive": ["胃", "腸", "肠", "腹瀉", "腹泻", "便秘", "肝炎"],
}


def classify(title: str) -> str:
    folded = title.casefold()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.casefold() in folded for keyword in keywords):
            return category
    return "other"


def build(source: Path) -> dict:
    payload = json.loads(source.read_text(encoding="utf-8"))
    records = [
        item
        for item in payload.get("records", [])
        if item.get("material_group") == "医案/日志"
    ]
    records.sort(
        key=lambda item: (
            TIER_PRIORITY.get(item.get("source_tier"), 9),
            item.get("title") or "",
            item.get("source_id") or "",
        )
    )

    seen = set()
    compact = []
    for item in records:
        title = " ".join((item.get("title") or "").split())
        if not title or len(title) > 160:
            continue
        family = item.get("provenance_family_id") or item.get("canonical_url")
        if family in seen:
            continue
        seen.add(family)
        compact.append(
            {
                "case_id": item.get("source_id"),
                "title": title,
                "topic": classify(title),
                "source_url": item.get("canonical_url"),
                "source_tier": item.get("source_tier"),
                "source_status": item.get("status"),
                "verification_status": item.get("verification_status"),
                "medical_risk": bool(item.get("medical_risk")),
                "provenance_family_id": family,
            }
        )

    counts = Counter(item["topic"] for item in compact)
    return {
        "schema_version": "1.0",
        "scope": "Metadata-only index of public Ni Haixia case and clinical-log sources; not proof of diagnosis or efficacy.",
        "input_record_count": len(records),
        "unique_indexed_count": len(compact),
        "topic_counts": dict(sorted(counts.items())),
        "usage": "Search title/topic, open source_url, verify the full record, and extract case facts before analysis.",
        "cases": compact,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = build(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {result['unique_indexed_count']} cases to {args.output}")


if __name__ == "__main__":
    main()
