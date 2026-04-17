<!-- SPECTRA:START v1.0.1 -->

# Spectra Instructions

This project uses Spectra for Spec-Driven Development(SDD). Specs live in `openspec/specs/`, change proposals in `openspec/changes/`.

## Use `$spectra-*` skills when:

- A discussion needs structure before coding → `$spectra-discuss`
- User wants to plan, propose, or design a change → `$spectra-propose`
- Tasks are ready to implement → `$spectra-apply`
- There's an in-progress change to continue → `$spectra-ingest`
- User asks about specs or how something works → `$spectra-ask`
- Implementation is done → `$spectra-archive`

## Workflow

discuss? → propose → apply ⇄ ingest → archive

- `discuss` is optional — skip if requirements are clear
- Requirements change mid-work? `ingest` → resume `apply`

## Parked Changes

Changes can be parked（暫存）— temporarily moved out of `openspec/changes/`. Parked changes won't appear in `spectra list` but can be found with `spectra list --parked`. To restore: `spectra unpark <name>`. The `$spectra-apply` and `$spectra-ingest` skills handle parked changes automatically.

<!-- SPECTRA:END -->

# claude-config — Agent Guidelines

## Project Overview

Global Claude Code configuration repository. Stores rules, skills, memory, and settings shared across all projects.

## Directory Structure

```
claude-config/
├── rules/           # Routing, triggers, SSOT, dev pipeline rules
├── skills/          # Claude Code custom skills
├── memory/          # Persistent memory files
├── mesh/            # Flow definitions and failure type references
└── CLAUDE.md        # Global entry point
```

## Key Files

| File | Purpose |
|------|---------|
| `rules/routing.md` | Model routing — who does what |
| `rules/triggers.md` | Auto-trigger rules |
| `rules/ssot.md` | Single Source of Truth table |
| `rules/dev-pipeline.md` | Phase flow definitions |
| `rules/mesh-flow.md` | Task execution and failure recovery |
| `rules/formatter.md` | Format check specs |
| `soul.md` | Persona and behavioral guidelines |
| `lessons.md` | Corrected rules from past mistakes |
| `memory/today.md` | Daily progress log |
| `memory/projects.md` | Strategic project status |

## Modification Rules

- Changes to `rules/` affect all projects globally — review carefully before editing
- `lessons.md` is append-only from corrections; never rewrite history
- `memory/today.md` resets daily; history goes to claude-mem
- Skills in `skills/` follow their own `SKILL.md` spec

## Commit Guidelines

- Conventional Commits: `chore:`, `docs:`, `feat:`
- Scope to the specific rule or skill changed (e.g., `chore(routing): update fallback order`)
