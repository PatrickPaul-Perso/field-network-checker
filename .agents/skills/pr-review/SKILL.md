---
name: pr-review
description: Use this skill when the task is to review a diff, branch, or implementation for correctness, regression risk, readability, test coverage, and release readiness in Field Network Checker.
---

# PR Review

## Purpose

This skill standardizes code review and change-readiness review.

Use it for:
- pull request reviews
- local diff reviews
- pre-merge checks
- focused review of risky changes

## Review Areas

Always inspect:
- correctness
- regression risk
- edge cases
- readability
- consistency with project conventions
- validation quality
- documentation impact
- user-facing wording if affected

## Procedure

1. Restate the purpose of the change.
2. Identify the files and behaviors affected.
3. Look for functional risks first.
4. Check missing validation and missing tests.
5. Check docs and UI text alignment.
6. Separate blocking issues from non-blocking improvements.
7. Summarize merge readiness.

## Severity Labels

### Blocking
Likely bug, regression, broken assumption, or missing critical validation.

### Important
Strongly recommended before merge, but not clearly release-blocking.

### Nice To Have
Improvement that can follow later.

## Expected Output

### Summary
What the change appears to do.

### Blocking Issues
List only real blockers.

### Important Issues
List important gaps or risks.

### Nice To Have
Optional improvements.

### Merge Readiness
State whether the change looks ready, risky, or incomplete.