---
name: change-plan
description: Plan a code or analysis change before implementation. Use for non-trivial features, bug fixes, pipeline changes, or whenever requirements or scientific assumptions could be ambiguous.
---

# Change Plan

## Purpose
Convert a request into a small, testable contract before editing code. Planning is brief for simple changes and detailed only where risk warrants it.

## Steps
1. Inspect the actual repository, relevant files, configuration, tests, and recent diff. Do not edit yet.
2. Restate the requested outcome in one sentence.
3. Record:
   - inputs and outputs, including schemas and units;
   - scientific assumptions and decisions;
   - constraints and files that must not change;
   - failure behaviour;
   - acceptance criteria observable by a command or known-answer fixture.
4. Identify ambiguity. Ask only questions that could materially alter implementation. Otherwise choose the safest interpretation and state it.
5. Propose the smallest implementation, files to change, tests to add, and verification commands.
6. Identify risks, especially sample mismatches, reads-versus-fragments, coordinate systems, denominators, partial outputs, and nondeterminism.

## Output
Write a concise plan in chat. For changes spanning multiple sessions, save it to `.research/plans/YYYY-MM-DD-short-name.md` using:

- Goal
- Current behaviour and evidence
- In scope / out of scope
- Scientific assumptions
- Inputs / outputs / invariants
- Failure behaviour
- Files to change
- Acceptance tests
- Verification commands
- Open questions and risks

Do not implement until the plan is coherent. User approval is not required when the request already authorizes implementation, but deviations from the plan must be reported.
