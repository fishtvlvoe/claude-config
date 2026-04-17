# Spec: Claude Code Configuration Token Optimization

## ADDED Requirements

### Requirement: Session Startup Context Budget

Session startup automatic context loading SHALL be bounded by a measurable token budget.

**Target**: ≤ 6,000 tokens per session startup (excluding MCP tool schemas, conversation history, and on-demand loads).

**Measurement**: Sum of auto-loaded files (global CLAUDE.md + soul.md + lessons.md + RTK.md + project CLAUDE.md + all `~/.claude/rules/*.md`) using 3.5 chars per token estimate.

#### Scenario: Baseline measurement

- **WHEN** measuring session startup context
- **THEN** total token count SHALL be reported with breakdown by file
- **AND** each `rules/*.md` file exceeding 100 lines SHALL be flagged as optimization candidate

#### Scenario: Regression detection

- **WHEN** total exceeds 7,000 tokens
- **THEN** the system SHALL warn during optimization review
- **AND** the largest contributing files SHALL be identified for splitting into `rules/detail/`

### Requirement: Tool Search Behavior

Deferred tool loading SHALL be disabled via `ENABLE_TOOL_SEARCH=false` in `~/.claude/settings.json` env block.

**Justification**: Frequently used tools (TaskCreate, TaskUpdate, WebSearch, AskUserQuestion, MCP tools) deferred by default create workflow interruptions in Claude Code 4.7+.

#### Scenario: TaskUpdate direct availability

- **WHEN** a new session starts
- **THEN** TaskUpdate schema SHALL be immediately available without ToolSearch call
- **AND** marking tasks complete SHALL not require ToolSearch preamble

### Requirement: Rules Index Architecture

Rule files exceeding 100 lines SHALL be split into speed-reference (`~/.claude/rules/<name>.md`) and detail (`~/.claude/rules/detail/<name>-full.md`) files.

**Speed-reference contents**:
- All hard rules (禁止項、強制項)
- Routing lookup tables
- Critical decision flows

**Detail contents**:
- Full explanations, examples, SOP walkthroughs
- Edge cases and historical context
- Extended troubleshooting

#### Scenario: Hard rules preserved in speed-reference

- **WHEN** a rule file is split
- **THEN** all 🔴 hard rules SHALL remain in the speed-reference version
- **AND** the speed-reference SHALL end with `> 細節 → Read ~/.claude/rules/detail/<name>.md`

### Requirement: Session Start Hook Token Budget

`~/.claude/scripts/hooks/session-start.js` output SHALL be bounded by these parameters:

- `MAX_AGE_DAYS`: 3 (session summaries older than 3 days ignored)
- `SUMMARY_HEAD_LINES`: 25 (truncate past session summary)
- `SMART_CONTEXT_MAX_FILES`: 1 (auto-load at most 1 memory file per project match)

**Target output**: < 1,500 tokens per session start.

#### Scenario: Truncated summary signals full path

- **WHEN** session summary exceeds 25 lines
- **THEN** output SHALL append `... (完整摘要見 <full path>)` so Claude can Read on demand
- **AND** no information SHALL be silently dropped

#### Scenario: Smart Context overflow signal

- **WHEN** more than 1 memory file matches the current CWD
- **THEN** additional files SHALL be listed by name as `（其他記憶檔待命，Read 即可載入：<names>）`

### Requirement: Spectra Default-On Rule

All execution-type tasks (bug fix, feature add, refactor, debug, modification) MUST route through Spectra (`/spectra:propose`, `/spectra:ingest`, `/spectra:apply`, `/spectra:archive`).

The Claude assistant MUST declare routing as the first sentence of the response in format:
`這任務會走 Spectra。對應 change：[名稱] / 需新建 / 續用既有`

#### Scenario: Execution task without explicit routing

- **WHEN** user sends a task involving code changes, bug fixes, or feature additions
- **THEN** the response SHALL begin with a Spectra routing declaration
- **AND** TaskCreate/TodoList/Task tools SHALL NOT be used as a substitute

#### Scenario: Skippable contexts

- **WHEN** the task is one of: pure Q&A, pure research query, 1-line hotfix (explicitly declared), or system configuration adjustment (launchd/settings/hooks)
- **THEN** the response MAY skip Spectra routing
- **AND** the response MUST explicitly state the skip reason: `這不走 Spectra，因為 X`

### Requirement: Launchd Service Hygiene

Background services registered as `~/Library/LaunchAgents/com.fishtv.*.plist` SHALL meet these criteria:

- Target executable SHALL exist at the specified path
- Service SHALL have documented purpose (script comment or proposal)
- Services that have never run successfully (log shows only errors) SHALL be removed
- Services that have been replaced by alternative mechanisms (GitHub sync, cron, etc.) SHALL be removed

#### Scenario: Zombie service detection

- **WHEN** auditing launchd services
- **THEN** services whose logs show only "No such file or directory" errors SHALL be removed
- **AND** their plist files SHALL be deleted (not just unloaded)

### Requirement: Backup Before Destructive Changes

Any optimization that modifies or deletes configuration files under `~/.claude/` SHALL create a timestamped backup under `~/.claude/backups/YYYY-MM-DD-<reason>/` before the change.

#### Scenario: Rollback capability

- **WHEN** an optimization change is made to `session-start.js`, `rules/*.md`, or `settings.json`
- **THEN** the original file SHALL be copied to `~/.claude/backups/YYYY-MM-DD-optimization/<filename>.before-<step>`
- **AND** the backup path SHALL be documented in the Spectra change proposal
