---
name: explain-code
description: Build and test the user’s understanding of an AI-generated code path. Use when the user asks what code does, before merging unfamiliar code, or when comprehension has fallen behind generation.
---

# Explain Code

Explain the selected code from execution and data flow, not line-by-line paraphrase.

1. Identify entry point, inputs, outputs, and external side effects.
2. Trace one concrete example through the main branches.
3. Explain the scientific or business assumptions, including units and denominators.
4. Identify the five most consequential lines or functions and why they matter.
5. Describe how errors, empty inputs, skipped work, and partial outputs behave.
6. State what tests establish and what they do not establish.
7. Ask the user to predict one edge-case outcome, then verify it from code or by running a focused test if interaction continues.

End with a compact mental model and a list of anything the code does that is surprising or not enforced.
