# 開發流水線 — Phase 流程

> 代理能力表、寫碼分配、Opus Checklist 見 routing.md。

## 開發 Phase 職責定義

**Phase 1 — 規劃**：由 Opus 與用戶討論決策；cursor-agent 負責產出 spec.md + tasks.md + HTML UI mockup。

**Phase 2 — TDD 測試**：撰寫紅燈測試以定義成功條件；建立 fixture/stub；進行覆蓋率審查。

**Phase 3 — 實作**：核心架構、UI 元件、代碼、文案等多層級平行執行。並行原則：不同檔案可並行，同檔案必須串行。

**Phase 4 — Review**：三層審查流程確保品質：全量 code review → 安全邏輯驗證 → GitHub Copilot 自動 review。

**Phase 5 — 驗收**：測試全綠、UI 驗證、用戶確認、Copilot review 結果作為最終依據。

具體 flow 見 mesh/flow.yaml。

## 原則

- **Review 即修**：Review 發現的小改善（5 分鐘內完成）當下直接修，不記 todo。涉及其他 Wave 的檔案或設計決策才延後。
- **並行安全**：不同檔案可並行派給不同代理，同一檔案必須串行執行。
