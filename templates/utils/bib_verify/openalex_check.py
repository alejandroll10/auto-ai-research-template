#!/usr/bin/env python3
"""Look up a single citation against OpenAlex.

Reads one or more citations from stdin (one JSON object per line, schema:
  {"key": "Smith2020", "title": "...", "authors": ["..."], "year": 2020}
or, in --plain mode, one free-text citation per line).

Writes one JSON result per input line to stdout:
  {"key": ..., "status": "VERIFIED|RESOLVED|MISS", "openalex_id": ...,
   "matched_title": ..., "doi": ..., "url": ..., "venue": ..., "year": ...,
   "similarity": float, "cited": {...}, "note": "..."}

OpenAlex is free and unauthenticated. Pass EMAIL via env var to enter the
polite pool (faster, more reliable). Reads .env at the project root if present.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

OPENALEX = "https://api.openalex.org/works"
TIMEOUT = 12
RETRIES = 2
BACKOFF = 1.5


def load_env_email() -> str:
    email = os.environ.get("EMAIL", "").strip().strip('"').strip("'")
    if email:
        return email
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        env = parent / ".env"
        if env.is_file():
            for line in env.read_text().splitlines():
                if line.startswith("EMAIL="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
            break
    return ""


def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]+", " ", title)
    return " ".join(title.split())


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def query_openalex(title: str, mailto: str) -> list[dict]:
    params = {"search": title, "per-page": "3"}
    if mailto:
        params["mailto"] = mailto
    url = f"{OPENALEX}?{urllib.parse.urlencode(params)}"
    last_err: Exception | None = None
    for attempt in range(RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
                return payload.get("results", []) or []
        except Exception as exc:
            last_err = exc
            if attempt < RETRIES:
                time.sleep(BACKOFF * (attempt + 1))
    raise RuntimeError(f"OpenAlex query failed: {last_err}")


def parse_plain(line: str) -> dict:
    """Best-effort parse of a freeform citation into {key, title, authors, year}.

    Expected (loose) shape:
      Author, Author2 (Year). "Title." Journal/Venue. <url-or-tag>
    Falls back to using the entire line as the title.
    """
    raw = line.strip()
    if not raw:
        return {}
    year_match = re.search(r"\((\d{4})\)", raw)
    year = int(year_match.group(1)) if year_match else None
    title = raw
    quote_match = re.search(r'["“]([^"”]+)["”]', raw)
    if quote_match:
        title = quote_match.group(1).strip().rstrip(".")
    else:
        if year_match:
            tail = raw[year_match.end():].lstrip(" .")
            tail = tail.split(".")[0]
            if len(tail) > 12:
                title = tail.strip()
    authors_part = raw.split("(", 1)[0].strip().rstrip(",")
    authors = [a.strip() for a in re.split(r",| and ", authors_part) if a.strip()] if authors_part else []
    return {"key": title[:60], "title": title, "authors": authors, "year": year}


def best_match(cite: dict, results: list[dict]) -> tuple[dict | None, float]:
    cited_title = cite.get("title", "") or ""
    if not results or not cited_title:
        return None, 0.0
    scored = []
    for r in results:
        cand_title = r.get("title") or r.get("display_name") or ""
        sim = title_similarity(cited_title, cand_title)
        scored.append((sim, r))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1], scored[0][0]


def verify(cite: dict, mailto: str, threshold: float) -> dict:
    if not cite.get("title"):
        return {"key": cite.get("key", ""), "status": "MISS", "note": "no title to query", "cited": cite}
    try:
        results = query_openalex(cite["title"], mailto)
    except Exception as exc:
        return {"key": cite.get("key", ""), "status": "MISS", "note": f"api-error: {exc}", "cited": cite}
    match, sim = best_match(cite, results)
    if match is None:
        return {"key": cite.get("key", ""), "status": "MISS", "note": "no openalex results", "cited": cite}
    matched_title = match.get("title") or match.get("display_name") or ""
    matched_year = match.get("publication_year")
    cited_year = cite.get("year")
    year_ok = (cited_year is None) or (matched_year is None) or abs(matched_year - cited_year) <= 1
    venue = ""
    primary = match.get("primary_location") or {}
    src = (primary.get("source") or {})
    if src.get("display_name"):
        venue = src["display_name"]
    out = {
        "key": cite.get("key", ""),
        "status": "VERIFIED" if (sim >= threshold and year_ok) else ("RESOLVED" if sim >= 0.6 else "MISS"),
        "openalex_id": match.get("id"),
        "matched_title": matched_title,
        "doi": match.get("doi"),
        "url": (primary.get("landing_page_url") or match.get("doi") or match.get("id")),
        "venue": venue,
        "year": matched_year,
        "similarity": round(sim, 3),
        "cited": cite,
    }
    if not year_ok:
        out["note"] = f"year mismatch (cited {cited_year}, openalex {matched_year})"
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plain", action="store_true",
                    help="Each stdin line is freeform text; parse heuristically.")
    ap.add_argument("--threshold", type=float, default=0.85,
                    help="Title similarity threshold for VERIFIED (default 0.85).")
    ap.add_argument("--rate-delay", type=float, default=0.12,
                    help="Seconds to sleep between API calls (default 0.12).")
    args = ap.parse_args()

    mailto = load_env_email()
    first = True
    for line in sys.stdin:
        if not first:
            time.sleep(args.rate_delay)
        first = False
        line = line.rstrip("\n")
        if not line.strip():
            continue
        if args.plain:
            cite = parse_plain(line)
        else:
            try:
                cite = json.loads(line)
            except json.JSONDecodeError:
                cite = parse_plain(line)
        if not cite:
            continue
        result = verify(cite, mailto, args.threshold)
        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
