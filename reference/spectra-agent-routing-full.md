# Spectra Agent Routing — 開發任務分工模式

> 記錄日期：2026-04-13（2026-05-25 更新：停用外部 CLI，只用 CC 內建模型）
> 用途：Spectra apply 階段的 task 分工指南
> 適用範圍：所有使用 Spectra SDD 的專案

## 核心原則

**目標**：平均分擔代理工作，讓每個代理都發揮核心能力，而非堆積簡單任務。

**禁止**：
- 將複雜任務全部集中到單一代理
- 給代理分配超出其能力的瑣碎任務
- 讓某些代理閒置，其他代理過載

---

## 代理能力對應表

| Agent | 核心能力 | 應該處理的任務 | 例子 |
|-------|---------|-------------|------|
| **Codex CLI** | 有 shell 執行需求、測試驗證、sandbox 環境 | TDD 紅綠循環、測試驗證、需要跑命令確認的實作、本機 git 操作 | 修復 API + 寫測試並跑；資料庫遷移驗證；npm 套件更新並驗證 |
| **Sonnet 子代理（業務）** | 核心業務邏輯、API routes、複雜狀態管理 | 業務邏輯核心實作、搜尋/篩選/排序邏輯、資料轉換、複雜 state 管理 | 搜尋邏輯重構；複雜篩選條件組合；狀態機設計 |
| **Sonnet 子代理（重構）** | 需深度理解 codebase 再動手的寫碼任務、跨檔重構 | 讀完大量檔案後再改、橫跨 3+ 檔案的重構、需要推理架構再實作 | 理解整個模組後重構；分析依賴關係後修 bug；讀 spec 後生成實作 |
| **Sonnet 子代理（UI）** | 前端元件、UI 整合、簡單頁面改動 | React 元件新建、UI toggle/modal、表單改動、Tailwind 樣式調整 | React 元件新建；UI toggle/modal；表單改動；Tailwind 樣式調整 |
| **Kimi MCP** | 3+ 檔案分析、架構理解、交叉 review、純技術推理 | Code Review、多檔案影響分析、邏輯檢查、架構一致性驗證、演算法問答 | diff review（3+ 檔案）；邏輯漏洞偵測；命名一致性；第二意見 |
| **WebSearch/WebFetch** | 技術研究、外部 API 查詢、市場調查 | 新技術可行性評估、第三方 API 文件查詢、版本 changelog 研究 | Gmail API 最新端點確認；Supabase 新功能研究；套件版本相容性檢查 |

---

## 任務分類規則

### Rule 1: 優先按「核心邏輯類型」分類

**「業務邏輯」→ Sonnet 子代理（業務）**
- 搜尋、篩選、排序、資料轉換
- 狀態機、流程控制
- API 設計

例：「實作進階篩選的 AND/OR 邏輯」→ Sonnet（業務）

**「UI 元件」→ Sonnet 子代理（UI）**
- React/Vue 元件新建
- 表單、modal、drawer
- Tailwind 樣式

例：「新建 AdvancedFilterBuilder 元件」→ Sonnet（UI）

**「測試 + 驗證」→ Codex CLI**
- TDD（先寫失敗測試，再實作）
- 跑 npm test / composer test 確認
- 執行 shell 命令驗證

例：「修復 API + 寫測試並跑」→ Codex CLI

**「跨檔重構 / 分析後實作」→ Sonnet 子代理（重構）**
- 需要先讀懂大量檔案再動手的實作
- 橫跨 3+ 檔案的重構（不只是 review，是要真的改）
- 讀 spec → 理解現有架構 → 生成實作（一體完成）

例：「讀完整個 auth 模組後重構 token 刷新邏輯」→ Sonnet（重構）

**「交叉檢查」→ Kimi MCP**
- review 多個檔案的 diff
- 邏輯漏洞偵測
- 命名一致性

例：「review ProductsPageClient + AdvancedFilterBuilder 的交互」→ Kimi MCP

### Rule 2: 合併相關任務，給代理完整工作包

**不要**：
```
- [ ] 1.1 [Tool: sonnet] 修改 sync API
- [ ] 1.2 [Tool: codex] 寫 sync API 測試
- [ ] 1.3 [Tool: sonnet] 再修 sync API
```

**應該**：
```
- [ ] 1.1 [Tool: codex] TDD：寫測試 → 修 API → 跑測試驗證
```

**不要**：
```
- [ ] 2.1 [Tool: sonnet] 改 label 文字
- [ ] 2.2 [Tool: sonnet] 加中文名稱
- [ ] 2.3 [Tool: sonnet] 調 CSS
```

**應該**：
```
- [ ] 2.1 [Tool: sonnet] ProductsPageClient 卡片完整改動：label 翻譯 + 中文名稱 + 樣式
```

### Rule 3: 平衡工作量

檢查分工後，確保：
- 沒有任何代理的任務數超過其他的 2 倍
- 複雜度分布均勻（不能一個全是簡單、一個全是難的）
- 關鍵路徑上的代理不被堵住

例：
```
不平衡：Sonnet 8 tasks、Codex 0 tasks
平衡：Sonnet-業務 4 tasks、Sonnet-UI 4 tasks、Codex 3 tasks、Kimi 1 task
```

---

## Spectra Apply 時的操作步驟

### Step 1: 讀 tasks.md

檢查每個 task 的 `[Tool: ...]` 標記。
舊標記 `[Tool: copilot]` / `[Tool: cursor]` / `[Tool: kimi]` → 自動轉派 Sonnet 子代理。

### Step 2: 按代理分類

```
Codex CLI:
- 1.1 + 1.2（API 修復 + 測試，需 shell 跑驗證）

Sonnet（業務）:
- 2.1 + 2.2（卡片邏輯）
- 4.3 + 4.4（搜尋邏輯）

Sonnet（UI）:
- 3.1~3.4（條件建構器元件）
- 4.1 + 4.2（ProductsPageClient UI 整合）

Sonnet（測試）:
- 5.1（AdvancedFilterBuilder 測試）

Kimi MCP:
- 5.3（交叉 Review）
```

### Step 3: 檢查平衡性

- Codex: 1 Wave（shell 驗證需求）✓
- Sonnet 業務: 2 Wave（核心邏輯）✓
- Sonnet UI: 2 Wave（元件實作）✓
- Kimi: 1 Wave（最後檢查）✓

### Step 4: 派遣並行 Wave

每個 Wave 內的任務**獨立執行**（互不阻塞），則可並行派遣。

```
Wave 1（並行）:
  Codex: 1.1+1.2
  Sonnet-業務: 2.1+2.2
  Sonnet-UI: 3.1~3.4, 4.1+4.2

Wave 2（後續，依序）:
  Sonnet-測試: 5.1
  Codex: 5.2（shell 驗證）
  Kimi: 5.3（交叉 review）
```

---

## 特殊情況

### Case A: 新套件/技術調研

→ **WebSearch/WebFetch MCP** 先查文件 → 結果交給 Sonnet/Codex 實作

例：「Gmail API 新端點」→ WebFetch 查 → Codex 實作

### Case B: 大改動涉及多檔案

→ **Sonnet 子代理（UI）**做 UI → **Sonnet 子代理（業務）**做邏輯 → **Kimi MCP**做交叉 review

### Case C: Bug 修復（一行改動）

→ 不走代理，直接在主對話修（太瑣碎）

### Case D: 性能優化

→ **Sonnet 子代理（業務）**（邏輯層優化）+ **Codex CLI**（跑 benchmark 驗證）

---

## 檢查清單（每次 apply 前）

- [ ] 任務按「業務邏輯/UI/測試/Review」分類了嗎？
- [ ] 相關任務合併成完整工作包了嗎？
- [ ] 工作量平衡（沒有某個代理過載）？
- [ ] 有 `[P]` 標記的任務能並行派遣嗎？
- [ ] 依賴關係清晰（Wave 之間沒有反向依賴）？

---

## 使用範例

### 範例 1: Bug 修復 Change

```
## 1. 修復同步 API 500 錯誤

[Codex CLI] TDD：
- 寫失敗測試（upsert payload 不應含 updated_at）
- 修改 sync-old-emails/route.ts（移除 updated_at）
- 跑測試驗證綠燈

## 2. 測試驗證

[Codex CLI] 跑既有 sync 測試確認不破壞
```

### 範例 2: UI 重構 Change

```
## 1. 卡片顯示改動 [Sonnet-UI]
- ProductsPageClient 卡片完整改：label + 中文名 + 樣式

## 2. 篩選邏輯重構

[Sonnet-UI] UI 元件：
- AdvancedFilterBuilder 完整實作
- ProductsPageClient UI 整合（toggle + 新元件）

[Sonnet-業務] 業務邏輯：
- 搜尋觸發邏輯（從即時改手動）
- 條件組合邏輯

## 3. 測試 + Review

[Sonnet-測試] 寫元件測試
[Kimi MCP] Code Review（ProductsPageClient + AdvancedFilterBuilder 交互）
```

---

## 快速參考（貼紙版）

```
🔧 API/後端修復 + 需 shell 驗證？ → Codex CLI
💻 業務邏輯（搜尋/篩選/狀態）？ → Sonnet 子代理（業務）
🎨 UI 元件/表單/頁面改動？ → Sonnet 子代理（UI）
👀 多檔案 review/邏輯檢查？ → Kimi MCP
📚 技術研究/API 文件查詢？ → WebSearch/WebFetch MCP
```

---

## Spectra Apply 強制 SOP（每次，無例外）

### Wave 開始前（強制三步）

1. 確認前一 Wave 所有任務標記 `[x]`
2. `git status` 乾淨（前一波 diff 已 commit）
3. `npm run build`（或對應的 build 指令）通過，0 錯誤

### Wave 執行流程

```
同一 Wave 的任務 → 同一訊息並行派出（多個 tool call）
↓
等所有回傳
↓
Kimi MCP CR（diff > 10 行時強制執行）
↓
npm run build / npm test
↓
git add + commit（conventional commits）
↓
才進入下一個 Wave
```

### 用量不足：主動偵測，不等 Fish 發現（硬規則）

**每個 Wave 派工前，執行用量預檢（若使用 Codex CLI）：**
```bash
codex --version 2>&1 | head -1     # 無回應或錯誤 → 標記不可用
```

**執行中遇到以下訊號 → 立刻判定不可用：**

| Agent | 不可用訊號 |
|-------|----------|
| Kimi MCP | `context limit` / `session expired` / MCP timeout / `429` |
| Codex CLI | `quota` / `billing` / 非零 exit + API 錯誤 stderr |

**自動切換順序（不需 Fish 確認）：**

| 主力 | 備用 |
|------|------|
| Codex CLI | Sonnet 子代理 |
| Kimi MCP | Sonnet 子代理（多角度 CR） |

**切換時主動告知 Fish（一句話，不等被問）：**
```
⚠️ [Agent X] 不可用，已切換至 [備用 Y] 繼續執行。
   任務：[任務編號] [名稱] | 原因：[錯誤訊息]
```

**全部備用都失敗 → 停止本 Wave，主動說：**
```
⛔ Wave N 暫停：全部 Agent 不可用。
   請確認帳號用量後告知，我繼續從任務 [N.N] 接手。
```

### 代理產出失敗風控

| 失敗類型 | 判斷 | 處置 |
|---------|------|------|
| 代碼錯誤（build 紅燈、runtime error） | build/test 失敗 | 重派一次（更具體 prompt）→ 第二次失敗升規劃問題 |
| 規劃問題（方向跑偏、缺前置條件） | 代理不斷發問或產出錯誤 | 退回重寫 task prompt，補充前置條件再派 |
| 同一任務失敗超過 2 次 | — | 停止，主動回報 Fish，等決策 |

### Wave 完成驗收（缺一不過）

- `npm run build` 通過，0 TypeScript 錯誤
- Kimi MCP CR 無 Critical 問題
- git commit 存在（禁止「完成但未 commit」）
- tasks.md 對應任務標記 `[x]`
