# 路由速查表

> 2026-05-24 更新：停用大多數外部 CLI，只用 CC 內建模型分工。Codex CLI 例外：批次/長任務/sandbox 執行者角色（2026-05-25 重新啟用）。

## 🔴 硬規則（不可違反）

1. **Spectra 強制入口**：執行類任務 → `/spectra-*`，禁用 TaskCreate/TodoList 替代
   - SDD Apply 預設 **Sonnet 子代理**（成本 1/4 Opus，複雜度足）
   - 升 Opus 條件 → 見本檔 `## SDD Phase 分層`
2. **外顯路由**：每個任務第一句說「派 X，因為 Y」
3. **超過 5 行代碼 → 派子代理**，不自己寫
4. **CC + Codex 雙軌**：Opus/Sonnet/Haiku（CC 互動）+ Codex CLI（批次執行），其他外部 CLI 不派
5. **說工具「不能用」前 → 先 `which <tool>` 確認**

## 速查表

### ✅ 程式碼撰寫

| 任務性質 | 派給 | 呼叫 |
|---------|------|------|
| 業務邏輯 / API / 測試 / UI / 一般修改 | **Sonnet 子代理** | `Agent(model="sonnet")` |
| 複雜整合 / 跨多模組 / E2E / 架構重構 | **Sonnet 子代理**（或升 Opus） | `Agent(model="sonnet")` |
| 機械式重構 / 批量改名 / 成本敏感 | **Sonnet 子代理** | `Agent(model="sonnet")` |
| 1-2 行 hotfix | 主對話 | — |

### 🔍 非程式碼（分析、研究、審查）

| 任務性質 | 派給 | 呼叫 |
|---------|------|------|
| 規劃 / 決策 | 主對話（Opus） | — |
| 3+ 檔案讀取 / 結構化摘要 / 文件撰寫 | Haiku 子代理 | `Agent(model="haiku")` |
| Code Review（diff > 10 行） | Sonnet 子代理（並行多角度） | `Agent(model="sonnet")` |
| 研究外部 API / 文件 | Sonnet 子代理 + WebSearch/WebFetch | `Agent(model="sonnet")` |

### ❌ 禁用工具 / ⚠️ 限定角色

| 工具 | 範圍 | 替代/用法 |
|------|------|-----------|
| **Copilot CLI** | 全面停用 | Sonnet 子代理 |
| **Kimi CLI** | 全面停用（MCP 分析仍可用） | Sonnet 子代理 |
| **Codex CLI** | ⚠️ 批次/長任務/sandbox | CC 派任 → Codex 執行 |
| **Gemini CLI** | 全面停用 | Sonnet 子代理 + WebSearch |
| **cursor-agent** | 全面停用 | Sonnet 子代理 |

Codex CLI 例外：批次執行者角色，由 CC 派任，見 `~/.codex/AGENTS.md`。其他 CLI：Fish 明確點名才用。

## 工作流層級

```
Fish（架構師）→ 定方向、邊界、裁決
Claude Opus（PM）→ 企劃、拆任務、驗證、整合
Sonnet 子代理（執行者）→ 寫碼、CR、研究
Haiku 子代理（助手）→ 讀檔摘要、輕量分析
```

## 代碼審核（diff > 10 行強制）

1. **CR 並行矩陣**：同訊息派 3 個 Sonnet subagent — correctness / security / performance
2. **Debug** → Sonnet 子代理或主對話

## 並行原則

任務之間無交互依賴 → 才並行。
- 審查 ✅ 同檔多濾鏡
- 寫碼 ⚠️ 只有不同檔案
- 研究 ⚠️ 只有不同主題
- 設計 / 搜檔 ❌

## SDD Phase 分層

**原則**：Opus 做決策層，Sonnet 做執行層（2026-05-24 起只用 CC 模型）

| Phase | 用途 | 模型 |
|-------|------|------|
| 1（規劃） | Discuss / Propose | **Opus**（主對話） |
| 2（TDD） | 紅燈測試 | **Sonnet 子代理** |
| 3（實作） | 代碼撰寫 | **Sonnet 子代理** |
| 4（Review） | CR 驗證 | **Sonnet 子代理**（並行多角度） |
| 5（驗收） | E2E 測試 + 部署 | **Sonnet 子代理** |

**SDD Apply 預設**：用 **Sonnet 子代理**（複雜度足，成本 1/4）

**升 Opus 的條件**（任一符合）：
- 架構決策題（上 /spectra-discuss → Opus）
- 跨棧重構（3+ 層改動）
- 文件變更 > 10 個
- 模型主觀判斷：「這很複雜，需要深思」

**工作包合併原則**：不要拆太碎（例：「修 API / 寫測試 / 再修 API」分三份）；應合併成一包給 Sonnet 子代理，或拆兩包並行。

## Wave SOP（強制）

### Wave 前
1. 前一 Wave 所有任務 `[x]`
2. `git status` 乾淨
3. `npm run build` 通過

### Wave 執行
```
同 Wave 任務 → 同一訊息多 tool call 並行派出（Sonnet 子代理）
→ 等回傳
→ Sonnet 子代理 CR（diff > 10 行，並行多角度）
→ build + test
→ git add + commit（conventional）
→ 下一 Wave
```

### Wave 完成驗收（缺一不過）
- `npm run build` 0 錯誤
- Sonnet CR 無 Critical
- git commit 存在
- tasks.md `[x]` 已更新

## 開發 Phase 職責

**Phase 1 — 規劃**：Opus 與用戶討論決策；Sonnet 子代理產出 spec.md + tasks.md + HTML UI mockup。

**Phase 2 — TDD 測試（強制不可跳）**：逆推失敗點 → 產出「失敗矩陣表」（每個失敗點對應紅燈測試名稱 + 預期錯誤訊息）→ Fish 確認 → 派 Sonnet 子代理只寫紅燈測試（不寫實作）→ 跑測試確認全紅燈 → 紅燈清單再給 Fish 確認後才進 Phase 3。

**Phase 3 — 實作**：核心架構、UI 元件、代碼、文案等多層級平行執行。並行原則：不同檔案可並行，同檔案必須串行。

**Phase 4 — Review**：並行審查：Sonnet 子代理多角度 CR（correctness / security / performance）。

**Phase 5 — 驗收**：測試全綠、UI 驗證、用戶確認。

**原則**：
- **Review 即修**：Review 發現的小改善（5 分鐘內完成）當下直接修，不記 todo；涉及其他 Wave 的檔案或設計決策才延後。
- **並行安全**：不同檔案可並行派給不同代理，同一檔案必須串行執行。

## Fallback（寫碼）

Sonnet 子代理 → 主對話直接做。

## 參考

詳細案例、失敗分類處置、Token 預算、完整並行策略：
→ `~/.claude/reference/spectra-agent-routing-full.md`
