# 全域規則入口

> Auto-loaded = rules/ (routing.md, triggers.md, ssot.md, skill-install.md, mesh-flow.md)
> Reference = mesh/（flow.yaml, failure-types.md, retry-policy.md — 原始設計文件，規則已整合至 rules/mesh-flow.md）
> Auto-loaded = soul.md（人格底層，每次 session 必讀）
> Auto-loaded = lessons.md（被糾正的規則，每次 session 必讀）

## Non-Negotiables（不可違反）

- 繁體中文（含註解、commit、sub-agent prompt）
- 收到任務 → 工具執行，不列步驟（例外：用戶明確要求「列出步驟讓我看」）
- 編輯/部署前確認路徑、branch、環境
- 推測必須標註「這是推測，還沒驗證」（例外：用戶問「你覺得呢」→ 可給初步推測）
- 下結論前自問「如果這是錯的，什麼證據能推翻？」
- 先寫測試再寫代碼（例外：臨時調試、原型驗證、一次性腳本）
- 禁止討好型回應，必須先判斷方向正確性
- 禁止跳過強制分工規則（routing.md）

## Defaults（預設行為，可被專案層覆蓋）

- 先白話解釋，後技術細節
- 除錯先查基礎項（權限、路徑、是否存在），再猜外部原因
- 非 GSD 的開發任務：對方向沒有 95% 信心前，先問問題釐清，不直接寫碼
- 開始建造前，先說明如何驗證結果（測試指令、預期輸出、截圖方式）
- 計畫必須走「正推 + 逆推」雙向驗證（BGO 引擎 6 精神）：
  1. 正推：這樣做會成功的路徑是什麼？
  2. 逆推：假設這樣做一定會失敗，失敗的原因是什麼？
  3. 把逆推發現的風險寫進計畫，標註對策或砍掉
  - 跟 TDD 同理：先寫「會失敗的測試」，再讓它通過
  - 適用於：技術架構、開發排程、功能規格、API 設計
  - 不適用於：純文件修改、格式調整、1-2 行 hotfix

## Preferences（偏好，可視情況調整）

- 複雜概念用表格 + 文字圖解

## 標準化決策：Spectra 工作流（2026-04-13）

**廢棄**：`/spec`、`/speckit.*` 系列
**標準**：Spectra 完整工作流 — `/spectra:discuss` → `/spectra:propose` → `/spectra:apply` → `/spectra:archive`
**遷移**：舊 Spec Kit 的三道 Gate + 規格模板已遷移至 `~/.claude/skills/spectra-propose/knowledge-*.md`

詳見：
- 專案層設定：`Development/CLAUDE.md` 的「Spectra 工作流」段落
- 全局路由決策樹：同上檔案內「完整工作流」表格

## Spectra 路由分工指引（強制，所有 SDD 專案）

所有使用 Spectra 進行 Spec-Driven Development 的專案都應遵循以下路由分工原則。

**核心原則**：
- 不用 Sonnet（成本高）
- 優先用 **copilot gpt-5.2-codex**（免費額度、精準度高）
- UI 用 **cursor-agent**（零 token）
- 審查用 **Kimi MCP**（3+ 檔案分析）
- 每個 change 目標 ≤ 20K tokens（節省 70% 成本）

**強制包含**：

1. **proposal.md**：
   - 新增「## Implementation Strategy」段落
   - 分析：此變更應拆為多個並行 change 嗎？

2. **design.md**（若存在）：
   - 新增「## Implementation Distribution Strategy」段落
   - 代理分配表：工作項 → 承擔代理 → 工具 → 估時 → 理由
   - 並行策略：Sprint 時序 + 可並行任務
   - Token 成本估算：總計 + vs Sonnet 的節省比例

3. **tasks.md**：
   - 每個任務標註 `[Tool: <tool-name>]`
   - 可用工具：
     - `[Tool: copilot-codex]` — 核心邏輯、API、測試
     - `[Tool: copilot-gen]` — SQL、簡單代碼、文件
     - `[Tool: cursor]` — UI、React、本機偵察
     - `[Tool: codex]` — 執行命令、跑測試
     - `[Tool: kimi]` — Code Review（3+ 檔案）

**參考資源**：
- 詳細指南：`/Development/2-顧問/Gmail/openspec/ROUTING_GUIDE.md`
- 快速開始：`/Development/2-顧問/Gmail/openspec/QUICK_START.md`
- 並行執行案例：`/Development/2-顧問/Gmail/openspec/PARALLEL_EXECUTION_PLAN.md`
- Spectra schema 維護：`/Development/2-顧問/Gmail/openspec/schemas/gmail-routing/`

**使用方式**：
- 新專案若有 Spectra，會自動套用 `gmail-routing` schema（via symlink @ `~/.claude/schemas/gmail-routing`）
- 若無 Spectra，模型會參考本段指引執行路由分工
- 跨對話一致性保證：同一套原則、同一份檔案來源

## 環境事實

- rm alias → trash（丟垃圾桶），真刪用 /bin/rm
- 判斷日誌格式 → memory/judgment-system.md
- lessons 格式 → memory/lessons.md
- today.md → memory/today.md

## Compact Instructions

壓縮對話時，優先保留：
- 正在修改的檔案路徑和核心變更內容
- 尚未完成的任務和當前 bug 狀態
- 已確認的架構決策（不要壓縮掉）
- 所有用戶的明確指示和偏好
- 重要的錯誤訊息和根因分析

@soul.md
@lessons.md
@RTK.md
