---
name: analysis-audit
description: Audit a computational analysis for scientific correctness, provenance, sample integrity, and silent failures. Use before trusting results, after pipeline changes, or when outputs differ from expectations.
---

# Analysis Audit

## 1. Reconstruct the claim
State the scientific question, experimental unit, comparison, expected signal, and output used to support the conclusion.

## 2. Trace provenance
Follow one representative sample from raw input through every pipeline stage. Record exact inputs, commands, parameters, versions, outputs, and transformations. Verify methods text against executable configuration, not comments alone.

## 3. Verify identity and cardinality
At every stage compare expected and observed sample IDs, replicate level, row/record counts, duplicates, exclusions, and ordering. A skipped sample requires an explicit reason.

## 4. Verify analytical semantics
State and check:
- numerator and denominator;
- reads, alignments, fragments, molecules, cells, or biological replicates;
- coordinate system and interval conventions;
- units, normalization, controls, filtering, missing-data handling;
- random seeds and nondeterminism;
- exploratory versus confirmatory decisions.

## 5. Challenge silent success
Test missing, empty, malformed, mismatched, stale, and partial inputs. Confirm they fail or are handled by a documented scientific rule. Check that final files are validated before being treated as complete.

## 6. Independent triangulation
Recalculate a small subset manually or with a second implementation/tool. Compare summary counts before and after each transformation. Inspect representative outputs visually when appropriate.

## 7. Report
Create `.research/audits/YYYY-MM-DD-analysis-name.md` containing:
- claim and scope;
- provenance trace;
- checks and evidence;
- assumptions and decisions;
- discrepancies ranked critical/high/medium/low;
- conclusion: trusted, conditionally trusted, or not trusted;
- exact remediation and regression tests.

Do not infer correctness from reproducibility alone. A perfectly reproducible pipeline can reproduce the wrong analysis.
