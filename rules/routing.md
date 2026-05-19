# 路由速查表

> 細節（CLI 用法、CR 三層、Fallback 觸發） → `Read ~/.claude/reference/routing-details.md`

## 🔴 硬規則（不可違反）

1. **Spectra 強制入口**：執行類任務 → `/spectra-*`，禁用 TaskCreate/TodoList 替代
   - SDD Apply 預設 **Sonnet 子代理**（成本 1/4 Opus，複雜度足）
   - 升 Opus 條件 → 見 `spectra-agent-routing.md`
2. **外顯路由**：每個任務第一句說「派 X，因為 Y」
3. **超過 5 行代碼 → 派外部 Agent**，不自己寫
4. **寫碼只能派 Copilot / Kimi / Codex CLI 或 Sonnet 子代理**（無例外），Cursor/Gemini/Haiku 不准寫碼
5. **研究 / 網路查詢 → Gemini / Kimi CLI**，Claude 子代理無上網
6. **說工具「不能用」前 → 先 `which <tool>` 確認**

## 速查表

### ✅ 程式碼撰寫

| 任務性質 | 派給 | 呼叫 |
|---------|------|------|
| 業務邏輯 / API / 測試 / UI / 簡單修改 | **Copilot CLI** | `copilot -p --yolo --model gpt-5.2` |
| 機械式重構 / 批量改名 / 成本敏感 | **Kimi CLI** | `kimi --print -w <code-dir> -p "..."` |
| 複雜整合 / 跨多模組 / E2E | **Sonnet 子代理** | `Agent(subagent_type="general-purpose", model="sonnet")` |
| 大型 agentic / 沙盒隔離多檔 | **Codex CLI** | `codex exec -C <dir> -s workspace-write "..."` |
| 1-2 行 hotfix | 主對話 | — |

### 🔍 非程式碼（分析、研究、審查）

| 任務性質 | 派給 | 呼叫 |
|---------|------|------|
| 規劃 / 決策 | 主對話（Opus/Sonnet） | — |
| 3+ 檔案讀取 / 結構化摘要 / 文件撰寫 | Haiku 子代理 | `Agent(subagent_type="general-purpose", model="haiku")` |
| Code Review（diff > 10 行） | Kimi CLI | `kimi -p --print -w <dir>` |
| 演算法問答 / 第二意見 | Kimi CLI | `kimi -p --print "..."` |
| 研究外部 API / 文件 | Gemini CLI | `gemini -p "..."` |
| 批量 100+ 非即時查詢 | Gemini Batch | `batch_runner.py` |

### ❌ 禁用工具

| 工具 | 範圍 | 替代 |
|------|------|------|
| **cursor-agent** | 全面禁用 | UI → Copilot；複雜 → Sonnet/Codex；偵察 → 主對話 Grep |

例外：Fish 明確點名才用。

## 工作流層級

```
Fish（架構師）→ 定方向、邊界、裁決
Claude（PM）→ 企劃、拆任務、驗證、整合
外部 Agent（實習生）→ 執行小任務
```

實習生任務原則 → `reference/routing-details.md`

## 代碼審核三層（diff > 10 行強制）

1. **CR 並行矩陣**：同訊息派 3 個 subagent — correctness-auditor / security-lens / performance-auditor
2. **Debug** → Sonnet 子代理或主對話
3. **Coverage** → Copilot CLI `--coverage`，> 80%

細節（並行條件、跨檔備用方案） → `reference/routing-details.md`

## 並行原則

任務之間無交互依賴 → 才並行。
- 審查 ✅ 同檔多濾鏡
- 寫碼 ⚠️ 只有不同檔案
- 研究 ⚠️ 只有不同主題
- 設計 / 搜檔 ❌

## Fallback（寫碼）

Copilot → Kimi → Codex → Sonnet 子代理 → 主對話。**永不 fallback 到 Cursor**。

派工後自動驗證 + Fallback 觸發條件 → `reference/routing-details.md`
