---
name: spectra-propose
description: "Create a change proposal with all required artifacts"
effort: high
license: MIT
compatibility: Requires spectra CLI.
metadata:
  author: spectra
  version: "1.0"
  generatedBy: "Spectra"
---

Create a complete Spectra change proposal — from requirement to validated artifacts — in a single workflow.

**Input**: The argument after `/spectra-propose` is the requirement description. Examples:

- `/spectra-propose add dark mode`
- `/spectra-propose fix the login page crash`
- `/spectra-propose improve search performance`

If no argument is provided, the workflow will extract requirements from conversation context or ask.

**Prerequisites**: This skill requires the `spectra` CLI. If any `spectra` command fails with "command not found" or similar, report the error and STOP.

**Steps**

0. **Config 前置檢查（Project Setup Gate）** ⚠️ 強制，不可跳過

   > 目的：避免每次建立 artifact 時才發現 `openspec/config.yaml` 是空的，導致 AI 沒有專案背景知識、產出品質低落。
   > 處理原則：關鍵題問用戶（互動式），不自動猜、不沉默略過。

   a. **檢查 config.yaml 是否存在且有實質內容**：
      - 讀 `openspec/config.yaml`
      - 若檔案不存在 → 判定為「空」
      - 若檔案存在但 `context:` 欄位不存在 / 為空字串 / 只有註解骨架（無實質 tech stack 描述）→ 判定為「空」
      - 若檔案存在但 `rules:` 欄位不存在 / 為空 → 判定為「缺規則」

   b. **若判定為「空」→ 以 AskUserQuestion 詢問 3-5 題關鍵題（強制互動）**：
      - **Q1 產品定位**：「這個專案是做什麼的？一句話 + 目標用戶。」（無選項，自由作答）
      - **Q2 Tech Stack**：提供 4 選項 + 自由補充
        - Next.js + TypeScript + Supabase（Web App 主流）
        - WordPress + PHP（外掛）
        - Node.js + CLI（工具）
        - 其他（自由描述）
      - **Q3 部署方式**：提供 3 選項
        - Vercel（Production = main，Preview = staging）
        - 自架 VPS（rsync / ssh 部署）
        - GitHub Pages / 其他
      - **Q4 程式與註解語言規範**：提供 2 選項
        - 代碼英文 / 註解繁中（預設）
        - 全英文（跨國協作）
      - （可選 Q5）**特殊約束**：如「必須走 Spectra」「禁止 Emoji」等專案獨有規則

      問完後，基於答案 + 自動偵測 `package.json` / `CLAUDE.md` 寫一份完整 `context:`，並套用預設 `rules:` 模板（proposal / design / specs / tasks 四類）。

   c. **若判定為「缺規則」→ 不問用戶，直接套用預設 rules 模板**：
      - 預設模板包含 proposal / design / specs / tasks 四類的通用格式約束
      - 寫入後告知用戶：「已套用預設產出規則，如需客製請手動編輯 openspec/config.yaml」

   d. **若 config.yaml 完整 → 靜默通過**，進入 Step 1

   e. **回報**：不論是否修改 config.yaml，都向用戶顯示一行狀態：
      - 「✓ config.yaml 已就緒」或
      - 「✓ 已為專案建立 config.yaml（基於你的回答 + 偵測結果）」或
      - 「✓ 已補齊 config.yaml 的 rules 區段」

1. **Determine the requirement source**

   a. **Argument provided** (e.g., "add dark mode") → use it as the requirement description, skip to deriving the change name below.

   b. **Plan file available**:
   - Check if the conversation context mentions a plan file path (plan mode system messages include the path like `~/.claude/plans/<name>.md`)
   - If found, check if the file exists at `~/.claude/plans/`
   - If a plan file is found, use the **AskUserQuestion tool** to ask:
     - Option 1: Use the plan file
     - Option 2: Use conversation context
   - If conversation context has no relevant discussion, mention this when presenting the choice
   - If the user picks the plan file → read it and extract:
     - `plan_title` (H1 heading) → use as requirement description
     - `plan_context` (Context section) → use as proposal Why/Motivation content
     - `plan_stages` (numbered implementation stages) → use for artifact creation
     - `plan_files` (all file paths mentioned) → use for Impact section
   - If the user picks conversation context → fall through to (c)

   c. **Conversation context** → attempt to extract requirements from conversation history
   - If context is insufficient, use the **AskUserQuestion tool** to ask what they want to build

   From the resolved description, derive a kebab-case change name (e.g., "add dark mode" → `add-dark-mode`).

   **IMPORTANT**: Do NOT proceed without understanding what the user wants to build.

2. **Classify the change type**

   Based on the requirement, classify the change into one of three types:

   | Type     | When to use                                                         |
   | -------- | ------------------------------------------------------------------- |
   | Feature  | New functionality, new capabilities                                 |
   | Bug Fix  | Fixing existing behavior, resolving errors                          |
   | Refactor | Architecture improvements, performance optimization, UI adjustments |

   This determines the proposal template format in step 5.

3. **Scan existing specs for relevance**

   Before creating the change, check if any existing specs overlap:
   1. Use the **Glob tool** to list all files matching `openspec/specs/*/spec.md`
   2. Extract directory names as the spec identifier list
   3. Compare against the user's description to identify related specs (max 5 candidates)
   4. For each candidate (max 3), read the first 10 lines to retrieve the Purpose section
   5. If related specs are found, display them as an informational summary

   **IMPORTANT**:
   - If related specs are found, display them but do NOT stop or ask for confirmation — continue to the next step
   - If no related specs are found, silently proceed without mentioning the scan

4. **Create the change directory**

   ```bash
   spectra new change "<name>" --agent claude
   ```

   If a change with that name already exists, suggest continuing the existing change instead of creating a new one.

5. **Write the proposal**

   Get instructions:

   ```bash
   spectra instructions proposal --change "<name>" --json
   ```

   Write the proposal file using the template from instructions, with the following format based on change type:

   ### Feature

   ```markdown
   ## Why

   <!-- Why this functionality is needed -->

   ## What Changes

   <!-- What will be different -->

   ## Non-Goals (optional)

   <!-- Scope exclusions and rejected approaches. Required when design.md is skipped. -->

   ## Capabilities

   ### New Capabilities

   - `<capability-name>`: <brief description>

   ### Modified Capabilities

   (none)

   ## Impact

   - Affected specs: <new or modified capabilities>
   - Affected code: <list of affected files>
   ```

   ### Bug Fix

   ```markdown
   ## Problem

   <!-- Current broken behavior -->

   ## Root Cause

   <!-- Why it happens -->

   ## Proposed Solution

   <!-- How to fix -->

   ## Non-Goals (optional)

   <!-- Scope exclusions and rejected approaches. Required when design.md is skipped. -->

   ## Success Criteria

   <!-- Expected behavior after fix, verifiable conditions -->

   ## Impact

   - Affected code: <list of affected files>
   ```

   ### Refactor / Enhancement

   ```markdown
   ## Summary

   <!-- One sentence description -->

   ## Motivation

   <!-- Why this is needed -->

   ## Proposed Solution

   <!-- How to do it -->

   ## Non-Goals (optional)

   <!-- Scope exclusions and rejected approaches. Required when design.md is skipped. -->

   ## Alternatives Considered (optional)

   <!-- Other approaches considered and why not -->

   ## Impact

   - Affected specs: <affected capabilities>
   - Affected code: <list of affected files>
   ```

6. **Get the artifact build order**

   ```bash
   spectra status --change "<name>" --json
   ```

   Parse the JSON to get:
   - `applyRequires`: array of artifact IDs needed before implementation
   - `artifacts`: list of all artifacts with their status and dependencies

7. **Create remaining artifacts in sequence**

   Loop through artifacts in dependency order (skip proposal since it's already done):

   a. **For each artifact that is `ready` (dependencies satisfied)**:
   - **Check if the artifact is optional**: If the artifact is NOT in the dependency chain of any `applyRequires` artifact (i.e., removing it would not block reaching apply), it is optional. Get its instructions and read the `instruction` field. If the instruction contains conditional criteria (e.g., "create only if any apply"), evaluate whether any criteria apply to this change based on the proposal content. If none apply, skip the artifact and show: "⊘ Skipped <artifact-id> (not needed for this change)". Then continue to the next artifact.
   - Get instructions:
     ```bash
     spectra instructions <artifact-id> --change "<name>" --json
     ```
   - The instructions JSON includes:
     - `context`: Project background (constraints for you - do NOT include in output)
     - `rules`: Artifact-specific rules (constraints for you - do NOT include in output)
     - `template`: The structure to use for your output file
     - `instruction`: Schema-specific guidance
     - `outputPath`: Where to write the artifact
     - `dependencies`: Completed artifacts to read for context
     - `locale`: The language to write the artifact in (e.g., "Japanese (日本語)"). If present, you MUST write the artifact content in this language. Exception: spec files (specs/\*_/_.md) MUST always be written in English regardless of locale, because they use normative language (SHALL/MUST).
   - Read any completed dependency files for context
   - Create the artifact file using `template` as the structure
   - Apply `context` and `rules` as constraints - but do NOT copy them into the file
   - Show brief progress: "✓ Created <artifact-id>"

   b. **Continue until all `applyRequires` artifacts are complete**
   - After creating each artifact, re-run `spectra status --change "<name>" --json`
   - Check if every artifact ID in `applyRequires` has `status: "done"`
   - Stop when all `applyRequires` artifacts are done

   c. **If an artifact requires user input** (unclear context):
   - Use **AskUserQuestion tool** to clarify
   - Then continue with creation

8. **Inline Self-Review** (before CLI analysis)

   After creating all artifacts, scan them manually. Fix issues inline, then proceed to the CLI analyzer.

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

---

## Rationalization Table

| What You're Thinking                                          | What You Should Do                                                                    |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| "The requirements are clear enough, no need for discuss"      | Fine if true — but check you're not skipping because you're lazy                      |
| "This artifact isn't needed for this change"                  | Check `applyRequires` — if it's in the dependency chain, create it                    |
| "The spec doesn't need scenarios, the requirement is obvious" | Obvious to you now. Write scenarios for the implementer who doesn't have your context |
| "I'll keep the design brief, code will be self-explanatory"   | Design exists so implementers don't reverse-engineer intent. Be specific              |
| "This is a small change, skip the scope check"                | Small changes touching 5 subsystems aren't small. Check                               |
| "The placeholder is fine for now, I'll fill it in later"      | There is no "later" — implementation is next. Fill it in now                          |

---

9. **Analyze-Fix Loop — 四大面向全零（Four-Dimension Zero Gate）** ⚠️ 強制，不可跳過

   > 目的：Spectra GUI 會顯示四個徽章（Coverage / Consistency / Ambiguity / Gaps），用戶要求必須全零才算過關。
   > 處理原則：最多 3 輪自動修正，修不完不能靜默放行。

   1. 執行 `spectra analyze <change-name> --json`
   2. 解析四個 dimension 的 `finding_count`：
      - **Coverage**（覆蓋度）— 規格需求是否都有對應任務
      - **Consistency**（一致性）— 設計決策是否與任務對齊
      - **Ambiguity**（模糊度）— 是否有不明確需求
      - **Gaps**（缺漏）— 是否缺 artifact 或斷裂引用
   3. 計算 Critical + Warning 總數（Suggestion 忽略）：
      - **全部四大維度皆 0** → 顯示「✓ 四大面向徽章全零（Coverage 0 / Consistency 0 / Ambiguity 0 / Gaps 0）」→ 進入 Step 10
      - **任一維度有 Critical/Warning** → 進入修正流程
   4. **修正流程（最多 3 輪）**：
      a. 顯示進度：「🔧 第 M/3 輪修正，發現 N 個問題（Cov: X, Con: Y, Amb: Z, Gap: W）」
      b. 依序修每個 finding 的 affected artifact
      c. 重跑 `spectra analyze <change-name> --json`
      d. 四大全零 → 停，進入 Step 10
      e. 尚有警告且未達 3 輪 → 繼續下一輪
   5. **3 輪後仍有警告（例外處理）**：
      - 顯示剩餘警告清單 + dimension 分布（如「Coverage 還有 2 條」）
      - 主動分析：是否為 substring 比對偽陽性？是否為真實品質問題？
      - 用 **AskUserQuestion** 詢問用戶：
        - 選項 1：「這些警告是誤判，強制通過進 Validate」
        - 選項 2：「我看一下，暫停流程讓我手動決定」
      - **禁止靜默放行**：不論選哪個都要用戶確認，不能偷偷 proceed

10. **Validation**

    ```bash
    spectra validate "<name>"
    ```

    If validation fails, fix errors and re-validate.

11. **Show final status and end workflow**

    Show summary:
    - Change name and location
    - List of artifacts created
    - Validation result

    Use **AskUserQuestion tool** to ask what to do next. This ensures the workflow stops even when auto-accept is enabled. Provide exactly these options:
    - **First option (will be auto-selected)**: "Park" — Execute `spectra park "<name>"` to park the change, then inform the user they can run `/spectra-apply <change-name>` when ready (which will auto-unpark).
    - **Second option**: "Apply" — Invoke `/spectra-apply <change-name>` to start implementation.

    If **AskUserQuestion tool** is not available, execute `spectra park "<name>"` and inform the user to run `/spectra-apply <change-name>` when ready. Then STOP — do not continue.

    **After the user responds**, if they chose "Park", execute `spectra park "<name>"` and the workflow is OVER. If they chose "Apply", invoke `/spectra-apply <change-name>` to begin implementation.

**Artifact Creation Guidelines**

- Follow the `instruction` field from `spectra instructions` for each artifact type
- Read dependency artifacts for context before creating new ones
- Use `template` as the structure for your output file - fill in its sections
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output
- **Parallel task markers (`[P]`)**: When creating the **tasks** artifact, first read `.spectra.yaml`. If `parallel_tasks: true` is set, add `[P]` markers to tasks that can be executed in parallel. Format: `- [ ] [P] Task description`. A task qualifies for `[P]` if it targets different files from other pending tasks AND has no dependency on incomplete tasks in the same group. When `parallel_tasks` is not enabled, do NOT add `[P]` markers.

**Guardrails**

- Create all artifacts needed for implementation. Optional artifacts (those not in the `applyRequires` dependency chain) may be skipped if their inclusion criteria don't apply.
- Always read dependency artifacts before creating a new one
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
- If a change with that name already exists, suggest continuing that change instead
- Verify each artifact file exists after writing before proceeding to next
- **NEVER** write application code or implement features during this workflow
- **NEVER** skip the artifact workflow to write code directly
- **NEVER** reinterpret requirements by ignoring the proposal file
- **NEVER** invoke `/spectra-apply` — this workflow ends after artifact creation. The user decides when to start implementation
- If **AskUserQuestion tool** is not available, ask the same questions as plain text and wait for the user's response
