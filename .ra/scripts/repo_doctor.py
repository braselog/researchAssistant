#!/usr/bin/env python3
"""Fast, dependency-free structural check for the Research Assistant template."""
from pathlib import Path
import re, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
errors=[]; warnings=[]
required=['AGENTS.md','.github/copilot-instructions.md','.research/project_telos.md','.research/phase_checklist.md','tasks.md']
for name in required:
    if not (ROOT/name).exists(): errors.append(f'missing required file: {name}')
for p in sorted((ROOT/'.github/skills').glob('*/SKILL.md')):
    text=p.read_text(errors='replace')
    if not re.match(r'^---\nname: [^\n]+\ndescription: [^\n]+\n---\n',text): errors.append(f'invalid skill front matter: {p.relative_to(ROOT)}')
    if len(text.splitlines())>500: warnings.append(f'large skill may waste agent context: {p.relative_to(ROOT)} ({len(text.splitlines())} lines)')
for p in (ROOT/'scripts').rglob('*.py'):
    q=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True)
    if q.returncode: errors.append(f'Python syntax error: {p.relative_to(ROOT)}: {q.stderr.strip()}')
for p in (ROOT/'.github/skills').glob('*/scripts/*.py'):
    q=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True)
    if q.returncode: errors.append(f'Python syntax error: {p.relative_to(ROOT)}: {q.stderr.strip()}')
for x in warnings: print('WARNING:',x)
for x in errors: print('ERROR:',x)
print(f'repo_doctor: {len(errors)} error(s), {len(warnings)} warning(s)')
raise SystemExit(bool(errors))
