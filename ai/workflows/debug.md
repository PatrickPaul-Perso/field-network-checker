# Debug Workflow

Use this workflow when the task is to investigate a bug, regression, or unexpected behavior.

## Goal

Identify the most likely root cause, make the smallest reliable fix, and state clearly what was verified.

## Step 1. Define The Symptom

Capture:
- observed behavior
- expected behavior
- trigger conditions
- whether the issue is constant or intermittent
- operator impact

## Step 2. Reproduce

Try to reproduce the issue in the smallest realistic setup.

Record:
- input or state
- environment
- steps
- actual output

If reproduction is not possible, state why.

## Step 3. Narrow The Fault Area

Look for the smallest likely zone:
- network polling
- normalization logic
- prefix matching
- frontend rendering
- config loading
- persistence
- deployment or environment issue

## Step 4. Form A Hypothesis

State the most likely cause before changing code.

Prefer a direct, testable hypothesis over a vague explanation.

## Step 5. Apply The Smallest Fix

Rules:
- do not refactor broadly
- change only what supports the fix
- keep the fix easy to review
- protect existing behavior

## Step 6. Validate The Fix

Validate:
- the original symptom
- nearby edge cases
- the core flow touched by the fix
- any operator-visible state that might regress

## Step 7. Document The Outcome

Summarize:
- root cause
- file changes
- validation performed
- residual risk
- any follow-up needed

## Output Template

### Symptom
What was wrong.

### Root Cause
What likely caused it.

### Fix
What changed.

### Validation
What was checked.

### Residual Risk
Any remaining uncertainty.