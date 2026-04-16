---
name: feature-build
description: Use this skill when the task is to add or extend a feature in Field Network Checker. Keep scope tight, preserve current conventions, and include a concise validation summary.
---

# Feature Build

## Purpose

This skill standardizes how new work is scoped, implemented, and validated.

Use it for:
- new features
- targeted feature extensions
- controlled UI improvements
- small architectural additions that fit current patterns

## Required Inputs

Try to gather:
- requested behavior
- acceptance criteria
- constraints
- files or modules likely involved
- what must not change

## Procedure

1. Restate the requested feature and constraints.
2. Define the smallest defensible scope.
3. Produce a short implementation plan.
4. Edit only the files needed.
5. Keep code consistent with existing structure.
6. Validate the feature and adjacent behavior.
7. Update docs or user-facing wording if needed.
8. Summarize implementation, validation, and remaining risk.

## Guardrails

- Prefer minimal change sets.
- Avoid unrelated cleanup.
- Preserve local-first and field-ready behavior.
- Keep state logic explicit.
- Do not introduce new abstractions without clear benefit.

## Expected Output

### Scope
What will be built and what will not.

### Plan
Short ordered plan.

### Implementation
What changed and where.

### Validation
What was verified.

### Remaining Risk
What still needs watching.