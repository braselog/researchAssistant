from pathlib import Path
import re, yaml
ROOT=Path(__file__).resolve().parents[1]
def test_skill_frontmatter_and_names():
    for p in (ROOT/'.github/skills').glob('*/SKILL.md'):
        text=p.read_text(); parts=text.split('---',2); assert len(parts)==3
        meta=yaml.safe_load(parts[1]); assert meta['name']==p.parent.name; assert meta.get('description')
def test_no_obsolete_ra_paths():
    hits=[]
    for p in ROOT.rglob('*'):
        if p != Path(__file__) and p.is_file() and '.git' not in p.parts and p.suffix in {'.md','.py','.sh','.json'}:
            if '.ra/skills' in p.read_text(errors='ignore'): hits.append(str(p.relative_to(ROOT)))
    assert not hits
def test_required_records_exist():
    for rel in ['.research/decisions/decision-index.md','.research/traceability/manuscript-evidence.md','.research/context/README.md']:
        assert (ROOT/rel).exists()
