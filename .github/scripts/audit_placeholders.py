#!/usr/bin/env python3
"""Reject executable placeholder statements in project production Python."""
import ast
from pathlib import Path
SKIP={'.git','.venv','tests','__pycache__','.github/skills'}
issues=[]
for path in Path('.').rglob('*.py'):
    if any(part in SKIP for part in path.parts) or path.resolve()==Path(__file__).resolve():
        continue
    try:
        tree=ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError as e:
        issues.append(f"{path}:{e.lineno}: syntax error: {e.msg}")
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis:
            issues.append(f"{path}:{node.lineno}: ellipsis placeholder")
        if isinstance(node, ast.Pass):
            issues.append(f"{path}:{node.lineno}: bare pass placeholder")
if issues:
    print('\n'.join(issues))
    raise SystemExit(1)
print('No executable Python placeholders found.')
