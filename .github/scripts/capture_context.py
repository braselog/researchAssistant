#!/usr/bin/env python3
"""Capture candidate project context from VS Code agent hook JSON on stdin."""
from __future__ import annotations
import hashlib, json, os, re, sys
from datetime import datetime
from pathlib import Path
from typing import Any
ROOT=Path.cwd()
CONTEXT_DIR=ROOT/'.research'/'context'/'daily'
MAX_TEXT=8000
SECRET_KEY=re.compile(r'(password|passwd|secret|token|api[_-]?key|private[_-]?key)',re.I)
DEFAULT_MATERIAL_TOOLS={'editFiles','createFile','runInTerminal','runTests','applyPatch'}
def read_payload()->dict[str,Any]:
    raw=sys.stdin.read()
    if not raw.strip(): return {}
    value=json.loads(raw)
    if not isinstance(value,dict): raise ValueError('Hook input must be a JSON object')
    return value
def sanitize(value:Any)->Any:
    if isinstance(value,dict): return {k:'[REDACTED]' if SECRET_KEY.search(str(k)) else sanitize(v) for k,v in value.items()}
    if isinstance(value,list): return [sanitize(v) for v in value]
    if isinstance(value,str):
        lines=['[REDACTED: possible secret]' if SECRET_KEY.search(x) else x for x in value.splitlines()]
        text='\n'.join(lines)
        return text if len(text)<=MAX_TEXT else text[:MAX_TEXT]+'\n[TRUNCATED]'
    return value
def session_id(p:dict[str,Any])->str:
    for k in ('session_id','sessionId','conversation_id','conversationId'):
        if p.get(k): return str(p[k])
    seed=f"{os.getenv('VSCODE_PID','')}|{ROOT.resolve()}|{datetime.now():%Y-%m-%d}"
    return hashlib.sha256(seed.encode()).hexdigest()[:12]
def append(entry:dict[str,Any]):
    CONTEXT_DIR.mkdir(parents=True,exist_ok=True)
    path=CONTEXT_DIR/f"{datetime.now().astimezone():%Y-%m-%d}.jsonl"
    with path.open('a',encoding='utf-8') as f: f.write(json.dumps(entry,ensure_ascii=False)+'\n')
def base(p,event): return {'timestamp':datetime.now().astimezone().isoformat(),'session_id':session_id(p),'event':event,'status':'unprocessed'}
def main():
    if len(sys.argv)!=2: raise SystemExit('usage: capture_context.py user-prompt|tool-result|pre-compact')
    event=sys.argv[1]; p=read_payload(); e=base(p,event)
    if event=='user-prompt':
        prompt=str(p.get('prompt','')).strip()
        if prompt: e['prompt']=sanitize(prompt); append(e)
    elif event=='tool-result':
        names=set(filter(None,os.getenv('RA_MATERIAL_TOOL_NAMES','').split(','))) or DEFAULT_MATERIAL_TOOLS
        name=str(p.get('tool_name',''))
        if name in names:
            e.update(tool_name=name,tool_use_id=p.get('tool_use_id'),tool_input=sanitize(p.get('tool_input',{})),tool_response=sanitize(str(p.get('tool_response',''))[:MAX_TEXT]))
            append(e)
    elif event=='pre-compact':
        e['trigger']=p.get('trigger','unknown'); append(e)
    else: raise SystemExit(f'unsupported event: {event}')
    print('{}')
if __name__=='__main__': main()
