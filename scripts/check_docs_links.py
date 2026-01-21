#!/usr/bin/env python3
"""
check_docs_links.py

Lightweight internal link checker for the GitHub Pages (Jekyll) wiki under ./docs.

Scope:
- Markdown files only: docs/**/*.md
- Checks relative/absolute *internal* links resolve to a file in docs/
- Ignores external URLs (http/https/mailto/tel) and pure anchors (#...)

Exit codes:
- 0: no broken internal links
- 1: broken internal links found
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"
BASEURL_PREFIX = "/openContextGraph"


LINK_RE = re.compile(r"\[[^\]]*?\]\(([^)]+)\)")


@dataclass(frozen=True)
class LinkIssue:
    source_file: Path
    line_no: int
    target_raw: str
    resolved_path: Optional[Path]
    reason: str


def _is_external(target: str) -> bool:
    t = target.lower()
    return t.startswith(("http://", "https://", "mailto:", "tel:"))


def _strip_wrappers(target: str) -> str:
    t = target.strip()
    # Remove optional angle brackets: (<path>)
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1].strip()
    # Remove optional quotes
    if (t.startswith('"') and t.endswith('"')) or (t.startswith("'") and t.endswith("'")):
        t = t[1:-1].strip()
    return t


def _normalize_target(target: str) -> str:
    t = _strip_wrappers(target)
    # Drop query string and anchor fragment for filesystem checks
    t = t.split("?", 1)[0]
    t = t.split("#", 1)[0]
    return t.strip()


def _candidate_paths(doc_file: Path, target_path: str) -> Iterable[Path]:
    """
    Generate candidate filesystem paths under DOCS_DIR that could satisfy the link.
    """
    if not target_path:
        return []

    # Ignore templated links we can't resolve statically
    if "{{" in target_path or "}}" in target_path:
        return []

    # Strip baseurl if present
    if target_path.startswith(BASEURL_PREFIX + "/"):
        target_path = target_path[len(BASEURL_PREFIX) :]
    elif target_path == BASEURL_PREFIX:
        target_path = "/"

    # Absolute path in site -> relative to docs root
    if target_path.startswith("/"):
        rel = target_path.lstrip("/")
        base = DOCS_DIR
        p = base / rel
    else:
        # Relative to current doc
        p = (doc_file.parent / target_path).resolve()

    # If link points outside docs, treat as broken internal link
    try:
        p.relative_to(DOCS_DIR)
    except ValueError:
        return [p]

    candidates: list[Path] = []

    # Exact path
    candidates.append(p)

    # If it's a directory link, try index.md
    candidates.append(p / "index.md")

    # If it's missing extension, try .md
    if p.suffix == "":
        candidates.append(p.with_suffix(".md"))

    # If it's .html (legacy), try .md and index.md in same folder
    if p.suffix.lower() == ".html":
        candidates.append(p.with_suffix(".md"))
        candidates.append(p.with_suffix("") / "index.md")

    # Normalize candidates
    dedup: list[Path] = []
    seen = set()
    for c in candidates:
        c = c.resolve()
        if c not in seen:
            seen.add(c)
            dedup.append(c)
    return dedup


def _check_one_link(doc_file: Path, line_no: int, raw_target: str) -> Optional[LinkIssue]:
    target = _normalize_target(raw_target)

    if not target:
        return None
    if target.startswith("#"):
        return None
    if _is_external(target):
        return None

    candidates = list(_candidate_paths(doc_file, target))
    if not candidates:
        return None

    # If candidate is outside docs, treat as broken (internal link should stay inside docs)
    for c in candidates:
        if not str(c).startswith(str(DOCS_DIR)):
            return LinkIssue(
                source_file=doc_file,
                line_no=line_no,
                target_raw=raw_target,
                resolved_path=c,
                reason="link resolves outside docs/",
            )

    if any(c.exists() for c in candidates):
        return None

    return LinkIssue(
        source_file=doc_file,
        line_no=line_no,
        target_raw=raw_target,
        resolved_path=candidates[0] if candidates else None,
        reason="target not found in docs/",
    )


def check_docs_links() -> list[LinkIssue]:
    issues: list[LinkIssue] = []

    if not DOCS_DIR.exists():
        raise RuntimeError(f"docs dir not found: {DOCS_DIR}")

    md_files = sorted(DOCS_DIR.rglob("*.md"))
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            issues.append(
                LinkIssue(
                    source_file=f,
                    line_no=0,
                    target_raw="",
                    resolved_path=None,
                    reason=f"failed to read file: {e}",
                )
            )
            continue

        for i, line in enumerate(text.splitlines(), start=1):
            for m in LINK_RE.finditer(line):
                raw_target = m.group(1)
                issue = _check_one_link(f, i, raw_target)
                if issue:
                    issues.append(issue)

    return issues


def main() -> int:
    issues = check_docs_links()
    if not issues:
        print("OK: no broken internal docs links found.")
        return 0

    print(f"BROKEN: {len(issues)} internal docs link issue(s) found.\n")
    for issue in issues:
        rel = issue.source_file.relative_to(DOCS_DIR)
        where = f"{rel}:{issue.line_no}" if issue.line_no else str(rel)
        print(f"- {where}: {issue.reason}")
        print(f"  link: ({issue.target_raw})")
        if issue.resolved_path:
            try:
                print(f"  resolved: {issue.resolved_path.relative_to(DOCS_DIR)}")
            except Exception:
                print(f"  resolved: {issue.resolved_path}")
        print()

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

