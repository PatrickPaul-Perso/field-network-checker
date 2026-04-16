# Feature Workflow

Use this workflow when implementing a new feature or extending behavior.

## Goal

Deliver the smallest useful version of the requested feature with clear validation and low regression risk.

## Step 1. Understand The Request

Capture:
- the user goal
- the operator-visible change
- constraints
- acceptance criteria
- dependencies
- what must not change

## Step 2. Read The Relevant Context

Always read:
- `ai/core/project.md`
- `ai/core/architecture.md`
- `ai/core/coding-standards.md`

Then inspect the code areas most likely involved.

## Step 3. Define The Smallest Defensible Scope

State:
- what will be changed
- what will not be changed
- why this scope is enough

Do not expand the task unless required for correctness.

## Step 4. Plan Before Editing

Write a short plan with:
1. files likely to change
2. logic to add or adjust
3. validation to run
4. docs or UI text updates needed

## Step 5. Implement

Implementation rules:
- keep changes local
- preserve current conventions
- avoid unrelated cleanup
- keep behavior explicit
- prefer maintainability over novelty

## Step 6. Validate

Run the smallest relevant checks first.

Typical validation:
- app starts
- main flow still works
- new feature behaves as intended
- legacy behavior still works
- tests pass for changed areas

## Step 7. Update Docs

If the feature changes user-visible behavior:
- update README or docs
- update status labels or help text
- update any workflow notes if needed

## Step 8. Final Summary

Summarize:
- what was built
- files changed
- what was validated
- known risks or follow-up items

## Output Template

### Scope
Short description of the feature and exact scope.

### Plan
Short ordered plan.

### Implementation
What changed and where.

### Validation
What was checked and what passed.

### Remaining Risk
Any incomplete validation or edge case to watch.