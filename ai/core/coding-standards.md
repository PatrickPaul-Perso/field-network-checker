# Coding Standards

## General Rules

- Prefer small patches over broad rewrites.
- Match existing naming and structure unless there is a clear problem.
- Keep code easy to read in one pass.
- Avoid hidden side effects.
- Prefer explicit logic over clever shortcuts.
- Keep field-facing behavior obvious.

## Python

- Use clear function names.
- Keep functions focused.
- Add type hints where practical.
- Prefer standard library solutions unless a dependency is already part of the project.
- Handle error cases explicitly.
- Keep network-state logic easy to trace.

## Frontend

- Keep HTML semantic and simple.
- Keep CSS readable and organized by component or section.
- Keep JavaScript small and direct.
- Avoid complex client-side state patterns unless clearly needed.
- Map backend state to UI state with explicit conditions.

## UI Text

- Use short labels.
- Prefer direct wording.
- Avoid ambiguous status messages.
- Make state changes easy to understand during field use.

## Logging And Error Handling

- Log enough to support diagnosis.
- Do not flood logs with noise.
- Error messages should help narrow the issue quickly.
- Keep user-visible errors short and actionable.

## Comments

- Comment why, not what, when the code is otherwise clear.
- Remove stale comments when behavior changes.
- Do not narrate obvious syntax.

## Tests

When adding or changing behavior:
- add or update the smallest useful test
- prefer targeted tests over large test scaffolding
- cover state mapping and edge cases when logic changes
- protect operator-visible regressions

## Network Logic

- Keep prefix-match behavior explicit.
- Normalize input before comparing.
- Avoid magic constants without naming them clearly.
- Treat missing or invalid values conservatively.

## Change Scope

Do:
- isolate the real change
- keep collateral edits low
- update docs when behavior changes

Do not:
- rename broadly without need
- move files without need
- mix cleanup with behavior changes unless requested

## Definition Of A Good Change

A good change is:
- minimal
- correct
- testable
- easy to review
- easy to explain
- consistent with field use