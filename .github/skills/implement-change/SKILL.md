---
name: implement-change
description: Implement an approved or clearly specified change using small diffs, explicit failures, and tests. Use after change-plan or for a well-scoped coding task.
---

# Implement Change

## Preconditions
Read `AGENTS.md`, the change plan if present, and the actual files being modified.

## Steps
1. Start from a clean understanding of `git status` and preserve unrelated user changes.
2. Implement only the requested behaviour. Do not perform adjacent refactors.
3. Add validation at trust boundaries: CLI arguments, files, schemas, sample mappings, units, ranges, and external tool outputs.
4. Fail loudly on missing, empty, malformed, unsupported, or inconsistent states. Never substitute a placeholder result.
5. For restartable stages, write temporary output, validate it, then atomically publish the final output or completion marker.
6. Add tests concurrently:
   - one normal case;
   - one manually checkable known-answer case for analytical logic;
   - one malformed or missing-input case;
   - one regression case for the reported bug when applicable.
7. Run focused checks after each logical edit, then the project-wide checks.
8. Inspect the final diff for scope drift.

## Completion report
List changed files, behaviour added, commands run and outcomes, assumptions, exceptions caught, fallbacks/defaults introduced, skipped work, and residual risks. If any requirement is incomplete, say so and do not describe the task as complete.
