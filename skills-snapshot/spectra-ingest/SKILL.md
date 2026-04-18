---
name: spectra-ingest
description: "Update an existing Spectra change from external context"
effort: high
license: MIT
compatibility: Requires spectra CLI.
metadata:
  author: spectra
  version: "1.0"
  generatedBy: "Spectra"
---

Update an existing Spectra change — from a plan file or conversation context.

**Plan file support** is available when the tool has a plan directory (`~/.claude/plans/`). Otherwise, use conversation context to update artifacts.

**Prerequisites**: This skill requires the `spectra` CLI. If any `spectra` command fails with "command not found" or similar, report the error and STOP.

**Input**: Optionally specify a plan file path or name.

- `/spectra-ingest ~/.claude/plans/agile-discovering-rocket.md`
- `/spectra-ingest agile-discovering-rocket`
- `/spectra-ingest` (use conversation context or auto-detect plan file)

**Steps**

0. **Config 前置檢查（Project Setup Gate）** ⚠️ 強制，不可跳過

   > 同 `/spectra-propose` Step 0：確認 `openspec/config.yaml` 有實質內容，避免 AI 沒有專案背景知識。
   > ingest 場景下 config 通常已存在，這步主要檢查 rules 是否完整、context 是否過時。

   a. **讀 `openspec/config.yaml`**：
      - 不存在 → 判定「空」，與 propose 相同流程：用 AskUserQuestion 問 Q1-Q4 關鍵題後自動寫一份
      - 存在但 `context:` 空/僅註解 → 判定「空」，同上處理
      - 存在但 `rules:` 空 → 套用預設 rules 模板，不問用戶
      - 完整 → 靜默通過

   b. **回報狀態**：顯示「✓ config.yaml 已就緒」或「✓ 已補齊 config.yaml」

1. **Locate the requirement source**

   a. **Argument provided** → treat as plan file reference (prepend `~/.claude/plans/` and append `.md` if needed)
   - If the file exists → use it as the plan file source, proceed to Step 2
   - If the file does NOT exist → report the error and **stop**

   b. **No argument, plan file detectable**:
   - Check conversation context for plan file path (plan mode system messages include the path like `~/.claude/plans/<name>.md`)
   - If found and the file exists → use the **AskUserQuestion tool** to ask:
     - Option 1: Use the plan file
     - Option 2: Use conversation context
   - If the user picks plan file → proceed to Step 2
   - If the user picks conversation context → skip Step 2, go to Step 3

   c. **No argument, no plan file detectable**:
   - Check `~/.claude/plans/` for recent files
   - If recent files exist → list 5 most recent with the **AskUserQuestion tool**, include "Use conversation context" as an additional option
   - If the user picks a file → proceed to Step 2
   - If the user picks conversation context → skip Step 2, go to Step 3

   d. **Conversation context fallback** (no plan files found at all):
   - Use conversation context to update artifacts
   - If conversation context is insufficient, use the **AskUserQuestion tool** to get more details
   - Warn: "No plan file found. Using conversation context."

2. **Parse the plan structure** (skip if using conversation context)

   Claude Code plan files typically contain:
   - **Title** (`# ...`) — the high-level goal
   - **Context** section — background, motivation, current state
   - **Stages/Steps** — numbered implementation stages with goals and file lists
   - **Files involved** — list of files to modify/create
   - **Verification** section — how to test the changes

   Extract:
   - `plan_title`: from the H1 heading
   - `plan_context`: from the Context section
   - `plan_stages`: each numbered stage with its goal and file list
   - `plan_files`: all file paths mentioned
   - `plan_verification`: verification steps

3. **Check for active changes** (REQUIRED — ingest only updates existing changes)

   ```bash
   spectra list --json
   ```

   Also check for parked changes:

   ```bash
   spectra list --parked --json
   ```

   Parse both JSON outputs to get the full list of changes (active + parked). Parked changes should be annotated with "(parked)" in any selection list.
   - If one change exists (active or parked) → use the **AskUserQuestion tool** to confirm updating it
   - If multiple changes exist → use the **AskUserQuestion tool** to let user pick which one to update
   - If no changes at all (neither active nor parked) → tell the user: "No active change found. Use `/spectra-propose` first to create one." and **stop**

4. **Select the change**

   After selecting the change, check if it is parked:

   ```bash
   spectra list --parked --json
   ```

   If the selected change appears in the `parked` array:
   - Inform the user that this change is currently parked（暫存）
   - Use **AskUserQuestion tool** to ask: continue (unpark) or cancel
   - If continue: run `spectra unpark "<name>"` then proceed
   - If cancel: stop the workflow

   If there is no AskUserQuestion tool available (non-Claude-Code environment):
   Inform the user that this change is currently parked（暫存）and ask via plain text whether to unpark and continue, or cancel.
   Wait for the user's response. If the user confirms, run `spectra unpark "<name>"` then proceed.

   Read existing artifacts for context before updating.

5. **Update artifacts**

   For each artifact, get instructions first:

   ```bash
   spectra instructions <artifact-id> --change "<name>" --json
   ```

   Use the `template` from instructions as the output structure. Apply `context` and `rules` as constraints but do NOT copy them into the file.

   The instructions JSON includes `locale` — the language to write artifacts in. If present, you MUST write the artifact content in that language. Exception: spec files (specs/\*/\*.md) MUST always be written in English regardless of locale, because they use normative language (SHALL/MUST).

   **Plan-to-Artifact Mapping** (when using a plan file):

   | Plan Section       | Artifact         | How to Map                                        |
   | ------------------ | ---------------- | ------------------------------------------------- |
   | Title              | Change name      | Convert to kebab-case                             |
   | Context            | proposal: Why    | Direct content transfer                           |
   | Stages overview    | proposal: What   | Summarize all stages                              |
   | Individual stages  | tasks.md groups  | One stage = one `##` heading, sub-items = `- [ ]` |
   | File paths         | proposal: Impact | Affected code list                                |
   | Verification steps | tasks.md         | Final verification task group                     |

   **Context-to-Artifact Mapping** (when using conversation context):

   | Conversation Element | Artifact         | How to Map                         |
   | -------------------- | ---------------- | ---------------------------------- |
   | Goal / requirement   | proposal: Why    | Extract motivation from discussion |
   | Discussed approach   | proposal: What   | Summarize agreed approach          |
   | Mentioned files      | proposal: Impact | Affected code list                 |
   | Discussion phases    | tasks.md groups  | One topic = one `##` heading       |

   **When updating an existing change:**
   - Merge new context into existing proposal (don't replace)
   - Add new tasks from plan stages or conversation, **preserve completed `[x]` items**
   - **Preserve existing `[P]` markers** on tasks that still qualify
   - Do NOT remove existing content

   **Parallel task markers (`[P]`)**: When creating or updating the **tasks** artifact, first read `.spectra.yaml`. If `parallel_tasks: true` is set, add `[P]` markers to new tasks that can be executed in parallel. Format: `- [ ] [P] Task description`. A task qualifies for `[P]` if it targets different files from other pending tasks AND has no dependency on incomplete tasks in the same group. When `parallel_tasks` is not enabled, do NOT add `[P]` markers — but still preserve any existing `[P]` markers already in the file.

   After creating each artifact, re-check status:

   ```bash
   spectra status --change "<name>" --json
   ```

   Continue until all `applyRequires` artifacts are complete. Show progress: "✓ Created <artifact-id>"

6. **Inline Self-Review** (before CLI analysis)

   After updating all artifacts, scan them manually. Fix issues inline, then proceed to the CLI analyzer.

   **Check 1: No Placeholders**

   These patterns are artifact failures — fix each one before proceeding:
   - "TBD", "TODO", "FIXME", "implement later", "details to follow"
   - Vague instructions: "Add appropriate error handling", "Handle edge cases", "Write tests for the above"
   - Delegation by reference: "Similar to Task N" without repeating specifics
   - Steps describing WHAT without HOW: "Implement the authentication flow" (what flow? what steps?)
   - Empty template sections left unfilled
   - Weasel quantities: "some", "various", "several" when a specific number or list is needed

   **Check 2: Internal Consistency**
   - Does every capability in the proposal have a corresponding spec?
   - Does the design reference only capabilities from the proposal?
   - Do tasks cover all design decisions, and nothing outside proposal scope?
   - Are file paths consistent across proposal Impact, design, and tasks?

   **Check 3: Scope Check**
   - More than 15 pending tasks → consider decomposing into multiple changes
   - Any single task would take more than 1 hour → split it
   - Touches more than 3 unrelated subsystems → consider splitting

   **Check 4: Ambiguity Check**
   - Are success/failure conditions testable and specific?
   - Are boundary conditions defined (empty input, max limits, error cases)?
   - Could "the system" refer to multiple components? Be explicit.

   **Check 5: Preservation Check** (ingest-specific)
   - Are all completed tasks `[x]` still present and unchanged?
   - Were existing `[P]` markers preserved on tasks that still qualify?
   - Was existing content merged (not replaced)?

---

## Rationalization Table

| What You're Thinking                                             | What You Should Do                                                            |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| "The existing artifacts are close enough, just adjust the tasks" | Read the new context carefully. "Close enough" means you're missing something |
| "The proposal doesn't need updating, the change is the same"     | If new context exists, the proposal likely needs updates. At minimum, check   |
| "I can merge these tasks, they're basically the same"            | Keep tasks granular. Merged tasks are harder to track                         |
| "The completed tasks still apply, no need to review"             | Verify they're still relevant to updated scope. Don't blindly keep stale work |
| "This spec change is minor, skip the scenario update"            | If the requirement changed, the scenario must change                          |
| "The conversation didn't discuss this artifact, so skip it"      | Absence of discussion doesn't mean absence of impact. Check                   |

---

7. **Analyze-Fix Loop — 四大面向全零（Four-Dimension Zero Gate）** ⚠️ 強制，不可跳過

   > 目的：Spectra GUI 四個徽章（Coverage / Consistency / Ambiguity / Gaps）必須全零才算過關。
   > 處理原則：最多 3 輪自動修正，修不完不能靜默放行。

   1. 執行 `spectra analyze <name> --json`
   2. 解析四個 dimension 的 `finding_count`：
      - **Coverage**（覆蓋度）— 規格需求是否都有對應任務
      - **Consistency**（一致性）— 設計決策是否與任務對齊
      - **Ambiguity**（模糊度）— 是否有不明確需求
      - **Gaps**（缺漏）— 是否缺 artifact 或斷裂引用
   3. 計算 Critical + Warning 總數（Suggestion 忽略）：
      - **全部四大維度皆 0** → 顯示「✓ 四大面向徽章全零」→ 進入 Step 8
      - **任一維度有 Critical/Warning** → 進入修正流程
   4. **修正流程（最多 3 輪）**：
      a. 顯示進度：「🔧 第 M/3 輪修正，發現 N 個問題（Cov: X, Con: Y, Amb: Z, Gap: W）」
      b. 依序修每個 finding 的 affected artifact
      c. 重跑 `spectra analyze <name> --json`
      d. 四大全零 → 停，進入 Step 8
      e. 尚有警告且未達 3 輪 → 繼續下一輪
   5. **3 輪後仍有警告（例外處理）**：
      - 顯示剩餘警告清單 + dimension 分布
      - 主動分析：是否為 substring 比對偽陽性？是否為真實品質問題？
      - 用 **AskUserQuestion** 詢問用戶：
        - 選項 1：「這些警告是誤判，強制通過進 Validate」
        - 選項 2：「我看一下，暫停流程讓我手動決定」
      - **禁止靜默放行**

8. **Validation**

   ```bash
   spectra validate "<name>"
   ```

   If validation fails, fix errors and re-validate.

9. **Summary and next steps**

   Show:
   - Source used: plan file (`<path>`) or conversation context
   - Change name and location
   - Artifacts created/updated
   - Validation result

   Use **AskUserQuestion tool** to confirm the workflow is complete. This ensures the workflow stops even when auto-accept is enabled. Provide exactly these options:
   - **First option (will be auto-selected)**: "Done" — End the ingest workflow. Inform the user they can run `/spectra-apply <change-name>` when ready.
   - **Second option**: "Apply" — Invoke `/spectra-apply <change-name>` to start implementation.

   If **AskUserQuestion tool** is not available, display the summary and inform the user to run `/spectra-apply <change-name>` when ready. Then STOP — do not continue.

   **After the user responds**, if they chose "Done", the workflow is OVER. If they chose "Apply", invoke `/spectra-apply <change-name>` to begin implementation.

**Guardrails**

- **NEVER** modify the original plan file in `~/.claude/plans/`
- **NEVER** write application code — this skill only creates/updates Spectra artifacts
- **NEVER** create new changes — ingest only updates existing changes. If no active change exists, direct user to `/spectra-propose`
- When updating existing changes, **preserve all completed tasks** (`[x]`) — never revert progress
- If the source content is too brief to fill all artifact sections, use the **AskUserQuestion tool** to get more details rather than inventing content
- If `spectra` CLI is not available, report the error and stop
- Verify each artifact file exists after writing before proceeding to next
- **NEVER** skip the artifact workflow to write code directly
- If **AskUserQuestion tool** is not available, ask the same questions as plain text and wait for the user's response
