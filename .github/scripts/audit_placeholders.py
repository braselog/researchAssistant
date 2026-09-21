#!/usr/bin/env python3
"""Fail when obvious placeholders occur in production Python paths."""
from pathlib import Path
import re

SKIP = {".git", ".venv", "tests", "__pycache__"}
PATTERNS = {
    "placeholder marker": re.compile(r"\b(TODO|FIXME|HACK|XXX|placeholder|stub)\b", re.I),
    "ellipsis statement": re.compile(r"^\s*\.\.\.\s*(?:#.*)?$"),
    "bare pass": re.compile(r"^\s*pass\s*(?:#.*)?$"),
}
issues=[]
for path in Path('.').rglob('*.py'):
    if any(part in SKIP for part in path.parts) or path.resolve() == Path(__file__).resolve():
        continue
    lines = path.read_text(errors='replace').splitlines()
    for number,line in enumerate(lines,1):
        for label,pattern in PATTERNS.items():
            if pattern.search(line) and not (label == 'bare pass' and number > 1 and lines[number-2].lstrip().startswith('except ')): issues.append(f"{path}:{number}: {label}: {line.strip()}")
if issues:
    print("\n".join(issues))
    raise SystemExit(1)
print("No obvious production placeholders found.")
