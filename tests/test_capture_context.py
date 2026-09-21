import json, os, subprocess, sys
from pathlib import Path
SCRIPT=Path('.github/scripts/capture_context.py').resolve()
def run(tmp_path,event,payload,env=None):
    e=os.environ.copy(); e.update(env or {})
    return subprocess.run([sys.executable,str(SCRIPT),event],input=json.dumps(payload),text=True,capture_output=True,cwd=tmp_path,env=e)
def entries(tmp_path):
    files=list((tmp_path/'.research/context/daily').glob('*.jsonl'))
    return [json.loads(x) for x in files for x in x.read_text().splitlines()]
def test_prompt_capture_and_redaction(tmp_path):
    p=run(tmp_path,'user-prompt',{'prompt':'Decision made\napi_key=abc','session_id':'s1'})
    assert p.returncode==0
    row=entries(tmp_path)[0]
    assert row['session_id']=='s1' and '[REDACTED' in row['prompt'] and 'abc' not in row['prompt']
def test_nonmaterial_tool_is_ignored(tmp_path):
    assert run(tmp_path,'tool-result',{'tool_name':'readFile'}).returncode==0
    assert not (tmp_path/'.research/context/daily').exists()
def test_material_tool_nested_secret_redacted(tmp_path):
    run(tmp_path,'tool-result',{'tool_name':'editFiles','tool_input':{'token':'abc','files':['x.py']},'tool_response':'ok'})
    assert entries(tmp_path)[0]['tool_input']['token']=='[REDACTED]'
def test_precompact_marker(tmp_path):
    run(tmp_path,'pre-compact',{'trigger':'auto'})
    assert entries(tmp_path)[0]['trigger']=='auto'
def test_invalid_json_fails(tmp_path):
    p=subprocess.run([sys.executable,str(SCRIPT),'user-prompt'],input='{',text=True,capture_output=True,cwd=tmp_path)
    assert p.returncode!=0
