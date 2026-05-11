# 路由速查表（精簡版）

> 詳細規則、例子、完整呼叫方式 → 需要時 Read `~/.claude/reference/routing-full.md`

## 🔴 硬規則（不可違反）

1. **Spectra 強制入口**：執行類任務 → `/spectra:*`，禁止用 TaskCreate/TodoList 替代
2. **外顯路由**：每個任務第一句話說「路由：X，派 Y」
3. **超過 5 行代碼 → 派外部 Agent**，不自己寫
4. **程式碼撰寫只能派 Copilot CLI、Kimi CLI 或 Sonnet 子代理**（無例外）。其他工具（Codex、Cursor、Gemini、Haiku）一律不准寫程式碼
5. **研究 / 網路查詢 → 派 Gemini / Kimi CLI**，Claude 子代理沒上網能力
6. **說工具「不能用」前 → 先 `which <tool>` 確認**

## 路由速查表

### ✅ 程式碼撰寫（只能用以下三個）

| 任務性質 | 派給 | 呼叫 |
|---------|------|------|
| 業務邏輯 / API / 測試 / UI 元件 / scaffold / 簡單修改 | **Copilot CLI** | `copilot -p --yolo --model gpt-5.2` |
| 機械式重構 / 批量改名 / 格式統一 / 模式套用 / 成本敏感任務 | **Kimi CLI** | `kimi --print -w <code-dir> -p "..."`（見下方 Kimi CLI 用法備忘） |
| 複雜整合 / 跨多模組 / E2E 測試 / 高複雜度推理 | **Sonnet 子代理** | `Agent` with `claude-sonnet` |
| 1-2 行 hotfix | 主對話 | — |

### 🔍 非程式碼撰寫（分析、研究、審查、雜事）

| 任務性質 | 派給 | 呼叫 |
|---------|------|------|
| 規劃、決策 | 主對話（Opus/Sonnet） | — |
| 3+ 檔案讀取 / 架構審查 / 結構化摘要 | Haiku 子代理 | `Agent` with `claude-haiku` |
| Code Review（diff > 10 行 / 多檔 CR） | Kimi CLI | `kimi -p --print -w <dir>` |
| 演算法問答 / 第二意見 | Kimi CLI | `kimi -p --print "..."` |
| 跨檔讀大量 codebase（只分析不寫碼） | Haiku 子代理或 Kimi CLI | `Agent` with `claude-haiku` / `kimi -p --print -w <dir>` |
| 研究外部 API / 文件 | Gemini CLI | `gemini -p "..."` |
| 批量 100+ 筆非即時查詢 | Gemini Batch | `batch_runner.py` |
| 文件撰寫（README、註解、CHANGELOG 等非程式碼） | Haiku 子代理 | `Agent` with `claude-haiku` |

### Kimi CLI 寫碼用法備忘

```bash
# 標準寫碼派工（-w 只指程式碼目錄，不指專案根）
kimi --print -w src/ -p "重構 X 模組... 只修改 src/ 下的檔案，禁止動 openspec/、.claude/、docs/"

# 複雜任務先規劃再執行
kimi --print --plan -w src/ -p "..."

# 限制步數防失控（預設由 config 決定）
kimi --print --max-steps-per-turn 20 -w src/ -p "..."

# 只拿最終結果（省 log 噪音，適合串接腳本）
kimi --quiet -w src/ -p "..."

# 需要讀額外目錄但不改（如讀 types/ 參考但只改 src/）
kimi --print -w src/ --add-dir types/ -p "..."
```

**防護 SDD 檔案**（L069）：派工前先 `git add openspec/ .claude/ && git commit`；`-w` 只指程式碼目錄；prompt 結尾加禁令；派工後 `git diff --stat` 檢查。

### ❌ 禁用工具（品質不穩，永不派工）

| 工具 | 禁用範圍 | 替代方案 |
|------|---------|---------|
| **cursor-agent** | 全面禁用（不寫 UI、不 scaffold、不本機偵察） | UI → Copilot；複雜元件 → Sonnet；偵察 → 主對話 Grep/Glob |

**例外**：Fish 明確點名要用 Cursor 做某件事 → 才用，否則一律不准。

### ⚠️ 外部代理（Fish 手動餵 prompt，非 Claude 派工）

| 工具 | 使用方式 | 備註 |
|------|---------|------|
| **Codex** | Fish 自己餵 prompt，Claude 負責打包 SDD 和監控產出 | 2026-05 解禁，已付費 |

## 工作流層級

```
Fish（架構師）→ 定方向、邊界、裁決
Claude（PM）→ 企劃、拆任務、驗證、整合
外部 Agent（實習生）→ 執行小任務
```

**實習生任務原則**：輸入清楚 + 輸出格式定好 + 粒度小 + 不需推理判斷。違反 → 留在主對話處理。

## 代碼審核三層（任何 diff > 10 行，強制）

1. **CR 並行矩陣** → **同一訊息並行派 3 個 subagent**（每個戴不同濾鏡全讀 diff）：
   - `correctness-auditor` — 只看邏輯錯誤、邊界條件、型別誤用
   - `security-lens` — 只看 OWASP / 注入 / 權限 / WP nonce
   - `performance-auditor` — 只看 N+1 / 迴圈 IO / 記憶體 / 缺快取
   - 三份報告回來後主對話整合，派 Copilot 一次修
   - 備用：跨檔（3+ 檔案）改用 Kimi CLI `kimi -p --print -w <dir>`
2. **Debug** → Sonnet 子代理或主對話
3. **Coverage** → Copilot CLI 跑 `--coverage`，目標 > 80%

## 並行 vs 單派決策表

| 任務 | 並行？ | 條件 |
|------|-------|------|
| 審查 | ✅ | 同檔多濾鏡（correctness / security-lens / performance） |
| 寫碼 | ⚠️ | 只有「不同檔案」才並行（同檔會打架） |
| 研究 | ⚠️ | 只有「不同主題」才並行（同主題合併一次問） |
| 設計 | ❌ | 單一 Copilot 或 Sonnet 子代理（一致性優先） |
| 搜檔 | ❌ | 單一 Explore 或 Grep（並行無意義） |

原則：**任務之間無交互依賴 → 才並行**。

## Fallback 順序（程式碼撰寫）

Copilot CLI 失敗 → Kimi CLI → Sonnet 子代理 → 主對話直接寫。切換時主動告知用戶。**永遠不會 fallback 到 Codex 或 Cursor。**

---

> 細節（WBS 拆任務原則、Opus/Sonnet 自律 Checklist、完整模型分工表、審核流程細節、fallback 觸發條件）
> → `Read ~/.claude/reference/routing-full.md`
