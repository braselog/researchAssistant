#!/usr/bin/env python3
"""Fail on suspicious placeholder and silent-failure constructs.

Defaults to tracked Python, R, shell, YAML, and workflow files. Use --changed to
scan only added lines in the working-tree diff, which is suitable for gradual
adoption in an existing repository.
"""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path

PATTERNS = {
    "marker": re.compile(r"\b(TODO|FIXME|HACK|XXX|PLACEHOLDER|DUMMY)\b", re.I),
    "bare except": re.compile(r"^\s*except\s*:\s*(?:#.*)?$"),
    "broad exception": re.compile(r"^\s*except\s+(?:Exception|BaseException)\b"),
    "pass statement": re.compile(r"^\s*pass\s*(?:#.*)?$"),
    "not implemented": re.compile(r"\bNotImplemented(?:Error)?\b"),
}
EXTS={'.py','.r','.R','.sh','.bash','.yaml','.yml','.smk'}
IGNORE_PARTS={'.git','.dvc','.venv','venv','build','dist','__pycache__'}

def tracked_files():
    p=subprocess.run(['git','ls-files'], text=True, capture_output=True)
    if p.returncode:
        return [x for x in Path('.').rglob('*') if x.is_file()]
    return [Path(x) for x in p.stdout.splitlines()]

def scan_line(path, number, line):
    if 'ra-placeholder-ok' in line:
        return []
    return [(path,number,name,line.rstrip()) for name,rx in PATTERNS.items() if rx.search(line)]

def scan_changed():
    p=subprocess.run(['git','diff','--unified=0','--no-color','HEAD'], text=True, capture_output=True)
    if p.returncode: return []
    findings=[]; path=None; line_no=0
    for line in p.stdout.splitlines():
        if line.startswith('+++ b/'):
            path=Path(line[6:])
        elif line.startswith('@@'):
            m=re.search(r'\+(\d+)',line); line_no=int(m.group(1)) if m else 0
        elif line.startswith('+') and not line.startswith('+++') and path:
            findings += scan_line(path,line_no,line[1:]); line_no += 1
        elif line.startswith(' '): line_no += 1
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--changed',action='store_true'); args=ap.parse_args()
    if args.changed: findings=scan_changed()
    else:
        findings=[]
        for p in tracked_files():
            if p.suffix not in EXTS or any(x in IGNORE_PARTS for x in p.parts) or not p.exists(): continue
            try: lines=p.read_text(errors='replace').splitlines()
            except OSError: continue
            for i,line in enumerate(lines,1): findings += scan_line(p,i,line)
    for p,n,name,line in findings: print(f'{p}:{n}: {name}: {line.strip()}')
    if findings:
        print(f'Found {len(findings)} suspicious construct(s). Review or annotate intentional lines with ra-placeholder-ok.',file=sys.stderr)
        return 1
    print('No suspicious placeholder constructs found.')
    return 0
if __name__=='__main__': raise SystemExit(main())
