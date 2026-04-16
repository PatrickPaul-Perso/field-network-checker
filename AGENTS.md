# AGENTS.md

Repository instructions for Codex in the Field Network Checker project.

## Purpose

This repository builds and maintains Field Network Checker.

The product is local-first, field-ready, and optimized for fast validation of Ethernet connectivity and network context in operational environments.

Prefer changes that are:
- small
- easy to validate
- easy to explain
- safe in the field
- aligned with the current architecture

## Repository Map

Update this section to match the real project structure.

- Build book uses ansible all under: `ansible`
- Main application entry: `app.py`
- Docker and local run files: `compose.yaml`, `Dockerfile`
- Project documentation and agent context: `ai/`
- Skills: `.agents/skills/`
- Tests: `app/tests/`, `app/run_tests.py`

## Read Order

Before starting work, read these files in this order:

1. `ai/core/project.md`
2. `ai/core/architecture.md`
3. `ai/core/coding-standards.md`

Then read the workflow that matches the task:

- Bug fix: `ai/workflows/debug.md`
- New feature: `ai/workflows/feature.md`
- Docs or UI text: `ai/workflows/docs.md`

If the task needs role-specific framing, use:
- `ai/templates/roles.md`

## Working Rules

- Start by restating the task, constraints, and done criteria.
- For non-trivial work, produce a short plan before editing code.
- Prefer the smallest defensible change.
- Do not refactor unrelated areas.
- Keep naming and structure consistent with the repository.
- Do not invent new architecture when an existing pattern already fits.
- Keep field behavior explicit. Avoid hidden logic.
- Preserve local-first operation unless the task explicitly requires otherwise.
- When behavior changes, update docs and tests where relevant.
- When a trade-off exists, prefer reliability and clarity over cleverness.

## Product Priorities

In order of importance:

1. Correctness of network state reporting
2. Simplicity for field use
3. Fast visual interpretation
4. Maintainability of the codebase
5. Minimal operator friction
6. Clear documentation

## Task Modes

Use these modes as needed. They are thinking modes, not rigid phases.

### Navigator mode
Use for:
- scope
- acceptance criteria
- dependency checks
- implementation ordering

### Engineer mode
Use for:
- code changes
- bug fixes
- tests
- integration work

### Reviewer mode
Use for:
- edge cases
- regression risks
- missing tests
- documentation gaps
- maintainability concerns

### Stylist mode
Use for:
- README updates
- UI copy
- status messages
- labels
- release notes

### Coordinator mode
Use for:
- final summary
- risk summary
- next-step recommendation

### Free Spirit mode
Use only when explicitly asked for:
- alternatives
- experiments
- unconventional ideas
- cross-domain inspiration

## Skill Routing

Use these skills when the task matches their purpose:

- `debug-flow`
  - Use for bug reproduction, fault isolation, minimal fixes, and validation of regressions.
- `feature-build`
  - Use for scoped feature work, feature extensions, and controlled UI behavior changes.
- `pr-review`
  - Use for review of diffs, regressions, edge cases, validation gaps, and merge readiness.

When a task clearly matches one of these workflows, prefer using the skill instead of improvising a new process.

## Validation

Run the smallest relevant validation first.

Use the project’s real commands. Replace the examples below with the exact commands used in this repository.

Typical validation areas:
- app starts successfully
- main page loads
- live Ethernet status still updates correctly
- legacy-prefix detection still behaves correctly
- saved readings and config behavior still work if touched
- tests pass for changed code
- lint or format checks pass if configured

Project commands:
- bootstrap the installation using ansible: `ansible-playbook ansible/site.yml --syntax-check; ansible-playbook ansible/site.yml`
- Build the app runtime container: `docker compose -f deploy/compose.yaml build`
- Run app: `docker compose -f deploy/compose.yaml up -d`
- Verify the app is running: `docker compose -f deploy/compose.yaml ps`
- Further verify the app outputs logs: `docker logs fnc-app --tail 50`
- Test by calling: curl http://192.168.50.1:8080/api/status

If a command cannot be run in the current environment, state that clearly and describe what remains unverified.

## Done Means

Work is complete when:
- the requested behavior is implemented or the root cause is identified
- the change is minimal and coherent
- relevant validation has been run, or any gap is stated clearly
- docs and user-facing text are updated when behavior changed
- the final summary states:
  - what changed
  - what was validated
  - what risk remains, if any

## Update Discipline

When a repeated mistake or ambiguity is discovered:
- update `AGENTS.md` if it is a durable repo-wide rule
- update a file under `ai/` if it is project knowledge, workflow guidance, or reusable phrasing
- update or add a skill under `.agents/skills/` if the issue is really a repeated workflow problem