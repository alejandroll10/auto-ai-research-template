#!/usr/bin/env python3
"""Print agent names matching a category from one or more metadata files.

Single source of truth for the faithful-mode developing/evaluator
classification. Used by setup.sh to drive the inject loop and by
core.md/faithful.md placeholder substitution. One name per line on
stdout (deduped, preserving first-seen order).

Categories live in each metadata entry as `"category": "developing"` or
`"category": "evaluator"`. Utility agents have no category field and
are silently skipped.

Example:
    python3 scripts/list_agents_by_category.py --category developing \\
        --metadata templates/agent_metadata/claude_shared_agents.json \\
        --metadata templates/agent_metadata/claude_variant_agents.json
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", action="append", required=True,
                        help="Path to a metadata JSON file (repeatable). "
                             "Missing files are silently skipped so the caller "
                             "can pass an extension's metadata path even when "
                             "that extension isn't installed.")
    parser.add_argument("--category", required=True,
                        choices=["developing", "evaluator"])
    args = parser.parse_args()

    seen = set()
    for path in args.metadata:
        p = Path(path)
        if not p.exists():
            continue
        data = json.loads(p.read_text())
        for name, meta in data.items():
            if meta.get("category") == args.category and name not in seen:
                print(name)
                seen.add(name)


if __name__ == "__main__":
    main()
