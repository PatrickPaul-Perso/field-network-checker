# Skill Policy

This file explains when to rely on a workflow file and when to rely on a skill.

## Rule

Use `AGENTS.md` for durable repository-wide instructions.

Use files under `ai/workflows/` for human-readable task guidance and reusable process references.

Use skills under `.agents/skills/` when a task is repeated often enough that Codex should follow a standard process with less ambiguity.

## When To Use A Workflow File

Use a workflow file when:
- the task needs human-readable process guidance
- the process is still evolving
- the guidance is mostly descriptive
- the task benefits from reading broader project context first

Examples:
- `ai/workflows/debug.md`
- `ai/workflows/feature.md`
- `ai/workflows/docs.md`

## When To Use A Skill

Use a skill when:
- the task happens often
- the process is stable
- the output structure should be consistent
- Codex should have a strong hint to follow a repeatable method

Examples:
- `.agents/skills/debug-flow/`
- `.agents/skills/feature-build/`
- `.agents/skills/pr-review/`

## Practical Rule Of Thumb

- Repository rules go in `AGENTS.md`
- Project knowledge goes in `ai/core/`
- Process guidance goes in `ai/workflows/`
- Repeated execution patterns go in `.agents/skills/`

## Review Rule

When the same type of task causes confusion more than once:
- first improve the matching workflow file
- then decide whether the process is stable enough to become or update a skill