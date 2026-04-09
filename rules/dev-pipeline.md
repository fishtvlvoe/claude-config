# 開發流水線 — Phase 流程

> 代理能力表、寫碼分配、Opus Checklist 見 routing.md。

## 開發 Phase 流程（每個功能/任務都走這個）

**Phase 1 — 規劃**：Opus 與用戶討論決策；cursor-agent 寫 spec.md + tasks.md + HTML UI mockup（零 token）；用戶確認後 commit。

**Phase 2 — TDD 測試**：Sonnet 寫紅燈測試（核心邏輯）；cursor-agent 寫 fixture/stub（零 token）；Kimi review 覆蓋率；commit。

**Phase 3 — 實作（多代理並行）**：Sonnet → 核心架構；cursor-agent → UI/簡單代碼/文案（並行）；Haiku → 更新紀錄（並行）。並行原則：不同檔案可並行，同檔案必須串行。每完成一個任務 → 跑測試 → 紅轉綠 → commit。

**Phase 4 — Review（三層 CR）**：
- Layer 1: Kimi → diff 全量 code review（3+ 檔案必用）
- Layer 2: Codex → 安全邏輯交叉驗證（額度不足時告知用戶跳過）
- Layer 3: `gh pr create` → GitHub Copilot 自動 review（最終關卡）
- 發現問題 → Sonnet/cursor-agent 修正 → commit

**Phase 5 — 驗收**：composer test 全綠；Chrome MCP 截圖驗證 UI（如適用）；用戶確認；以 Copilot review 結果作最終驗收依據。

## 原則

- **Review 即修**：Review 發現的小改善（5 分鐘內完成）當下直接修，不記 todo。涉及其他 Wave 的檔案或設計決策才延後。
- **並行安全**：不同檔案可並行派給不同代理，同一檔案必須串行執行。
