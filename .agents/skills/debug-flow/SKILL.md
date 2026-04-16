---
name: debug-flow
description: Use this skill for bug reproduction, root-cause isolation, minimal corrective changes, and validation in Field Network Checker.
---

# Debug Flow

## Purpose

Use this skill when the task is to investigate a bug, regression, or unexpected behavior.

This skill is especially appropriate for:
- incorrect link-up or link-down reporting
- incorrect IP display
- legacy-prefix detection errors
- config loading or saving issues
- frontend state mismatches
- deployment-caused regressions

## Required Inputs

Gather these when available:
- observed symptom
- expected behavior
- reproduction steps
- relevant files or modules
- logs, screenshots, or error output
- environment details

## Process

1. Restate the symptom, constraints, and expected behavior.
2. Reproduce the issue, or state clearly why reproduction is not possible.
3. Identify the smallest likely fault area.
4. Form one primary root-cause hypothesis.
5. Apply the smallest defensible fix.
6. Validate the original symptom and the nearest related edge cases.
7. Summarize root cause, code changes, validation, and residual risk.

## Guardrails

- Do not refactor unrelated areas.
- Do not widen scope without a correctness reason.
- Prefer explicit logic over broad cleanup.
- Preserve existing field behavior unless the bug is in that behavior.
- Update docs or tests when the fix changes user-visible behavior or verified expectations.

## Output Structure

### Symptom
What was observed.

### Root Cause
What likely caused it.

### Fix
What changed.

### Validation
What was checked and what passed.

### Residual Risk
What remains uncertain or unverified.