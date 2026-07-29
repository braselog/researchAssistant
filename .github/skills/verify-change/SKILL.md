---
name: verify-change
description: Verify AI-generated code or analysis independently. Use after implementation, before merge, when code passes but behaviour is uncertain, or when silent failure is a concern.
---

# Verify Change

Treat the implementation as wrong until evidence supports it. Do not merely rerun the builder's happy-path test.

## Verification ladder
1. **Requirement traceability**: map each requirement to code and at least one observation or test.
2. **Static checks**: inspect the diff; run lint, type, syntax, and placeholder scans available in the repository.
3. **Known-answer test**: use the smallest input whose result can be calculated independently.
4. **Failure tests**: missing file, empty file, malformed schema, duplicate or mismatched sample, invalid range, interrupted/partial output.
5. **Invariants**: assert row/sample sets, uniqueness, finiteness, sensible ranges, monotonic count changes, and domain constraints.
6. **Adversarial review**: look for swallowed exceptions, broad catches, defaults, stale outputs, wrong units, wrong denominator, reads-versus-fragments errors, coordinate errors, and tests that duplicate implementation logic.
7. **Diff review**: confirm no unrelated behaviour or scientific decision changed.

Run when available:

```bash
python .ra/scripts/scan_placeholders.py --changed
python .ra/scripts/repo_doctor.py
```

## Verdict
Return one of: `PASS`, `PASS WITH RESIDUAL RISKS`, or `FAIL`.
Include evidence, unverified areas, and the next corrective action. Passing tests alone is not sufficient for PASS.
