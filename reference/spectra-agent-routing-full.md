# Spectra Agent Routing — 開發任務分工模式

> 記錄日期：2026-04-13  
> 用途：Spectra apply 階段的 task 分工指南  
> 適用範圍：所有使用 Spectra SDD 的專案

## 核心原則

**目標**：平均分擔代理工作，讓每個代理都發揮核心能力，而非堆積簡單任務。

**禁止**：
- 將複雜任務全部集中到單一代理（如全派 Copilot）
- 給代理分配超出其能力的瑣碎任務
- 讓某些代理閒置，其他代理過載

---

## 代理能力對應表

| Agent | 核心能力 | 應該處理的任務 | 例子 |
|-------|---------|-------------|------|
| **Codex CLI** | 有 shell 執行需求、測試驗證、sandbox 環境 | TDD 紅綠循環、測試驗證、需要跑命令確認的實作、本機 git 操作 | 修復 API + 寫測試並跑；資料庫遷移驗證；npm 套件更新並驗證 |
| **Copilot CLI** | 核心業務邏輯、API routes、複雜狀態管理 | 業務邏輯核心實作、搜尋/篩選/排序邏輯、資料轉換、複雜 state 管理 | 搜尋邏輯重構；複雜篩選條件組合；狀態機設計 |
| **Kimi CLI** | 需深度理解 codebase 再動手的寫碼任務、跨檔重構、分析+實作一體 | 讀完大量檔案後再改、橫跨 3+ 檔案的重構、需要推理架構再實作 | 理解整個模組後重構；分析依賴關係後修 bug；讀 spec 後生成實作 |
| **Cursor-agent** | 本機偵察、UI 原型、簡單檔案操作 | 前端元件開發、UI 整合、簡單頁面改動、HTML/CSS 調整 | React 元件新建；UI toggle/modal；表單改動；Tailwind 樣式調整 |
| **Kimi MCP** | 3+ 檔案分析、架構理解、交叉 review、純技術推理 | Code Review、多檔案影響分析、邏輯檢查、架構一致性驗證、演算法問答 | diff review（3+ 檔案）；邏輯漏洞偵測；命名一致性；第二意見 |
| **Gemini CLI** | 技術研究、外部 API 查詢、市場調查 | 新技術可行性評估、第三方 API 文件查詢、版本 changelog 研究 | Gmail API 最新端點確認；Supabase 新功能研究；套件版本相容性檢查 |

---

## 任務分類規則

### Rule 1: 優先按「核心邏輯類型」分類

**「業務邏輯」→ Copilot**
- 搜尋、篩選、排序、資料轉換
- 狀態機、流程控制
- API 設計

例：「實作進階篩選的 AND/OR 邏輯」→ Copilot

**「UI 元件」→ Cursor**
- React/Vue 元件新建
- 表單、modal、drawer
- Tailwind 樣式

例：「新建 AdvancedFilterBuilder 元件」→ Cursor

**「測試 + 驗證」→ Codex**
- TDD（先寫失敗測試，再實作）
- 跑 npm test / composer test 確認
- 執行 shell 命令驗證

例：「修復 API + 寫測試並跑」→ Codex

**「跨檔重構 / 分析後實作」→ Kimi CLI**
- 需要先讀懂大量檔案再動手的實作
- 橫跨 3+ 檔案的重構（不只是 review，是要真的改）
- 讀 spec → 理解現有架構 → 生成實作（一體完成）

例：「讀完整個 auth 模組後重構 token 刷新邏輯」→ Kimi CLI

**「交叉檢查」→ Kimi MCP**
- review 多個檔案的 diff
- 邏輯漏洞偵測
- 命名一致性

例：「review ProductsPageClient + AdvancedFilterBuilder 的交互」→ Kimi MCP

### Rule 2: 合併相關任務，給代理完整工作包

**不要**：
```
- [ ] 1.1 [Tool: copilot] 修改 sync API
- [ ] 1.2 [Tool: codex] 寫 sync API 測試
- [ ] 1.3 [Tool: copilot] 再修 sync API
```

**應該**：
```
- [ ] 1.1 [Tool: codex] TDD：寫測試 → 修 API → 跑測試驗證
```

**不要**：
```
- [ ] 2.1 [Tool: copilot] 改 label 文字
- [ ] 2.2 [Tool: copilot] 加中文名稱
- [ ] 2.3 [Tool: copilot] 調 CSS
```

**應該**：
```
- [ ] 2.1 [Tool: cursor] ProductsPageClient 卡片完整改動：label 翻譯 + 中文名稱 + 樣式
```

### Rule 3: 平衡工作量

檢查分工後，確保：
- 沒有任何代理的任務數超過其他的 2 倍
- 複雜度分布均勻（不能一個全是簡單、一個全是難的）
- 關鍵路徑上的代理不被堵住

例：
```
不平衡：Copilot 8 tasks、Cursor 2 tasks
平衡：Copilot 4 tasks、Cursor 4 tasks、Codex 3 tasks、Kimi 1 task
```

---

## Spectra Apply 時的操作步驟

### Step 1: 讀 tasks.md

檢查每個 task 的 `[Tool: ...]` 標記。

### Step 2: 按代理分類

```
Codex:
- 1.1 + 1.2（API 修復 + 測試）
- 5.2（search 測試驗證）

Copilot:
- 2.1 + 2.2（卡片邏輯）
- 4.3 + 4.4（搜尋邏輯）
- 5.1（AdvancedFilterBuilder 測試）

Cursor:
- 3.1~3.4（條件建構器元件）
- 4.1 + 4.2（ProductsPageClient UI 整合）

Kimi:
- 5.3（交叉 Review）
```

### Step 3: 檢查平衡性

- Codex: 2 Wave（邏輯清晰）✓
- Copilot: 3 Wave（核心邏輯）✓
- Cursor: 2 Wave（UI 實作）✓
- Kimi: 1 Wave（最後檢查）✓

### Step 4: 派遣並行 Wave

每個 Wave 內的任務**獨立執行**（互不阻塞），則可並行派遣。

```
Wave 1（並行）:
  Codex: 1.1+1.2
  Copilot: 2.1+2.2
  Cursor: 3.1~3.4, 4.1+4.2

Wave 2（後續，依序）:
  Copilot: 5.1
  Codex: 5.2
  Kimi: 5.3
```

---

## 特殊情況

### Case A: 新套件/技術調研

→ **Gemini CLI** 先查文件 → 結果交給 Copilot/Codex 實作

例：「Gmail API 新端點」→ Gemini 查 → Codex 實作

### Case B: 大改動涉及多檔案

→ 先讓 **Cursor** 做 UI 原型 → **Copilot** 做邏輯 → **Kimi** 做交叉 review

### Case C: Bug 修復（一行改動）

→ 不走代理，直接在主對話修（太瑣碎）

### Case D: 性能優化

→ **Copilot**（邏輯層優化） + **Codex**（跑 benchmark 驗證）

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

[Codex] TDD：
- 寫失敗測試（upsert payload 不應含 updated_at）
- 修改 sync-old-emails/route.ts（移除 updated_at）
- 跑測試驗證綠燈

## 2. 測試驗證

[Codex] 跑既有 sync 測試確認不破壞
```

### 範例 2: UI 重構 Change

```
## 1. 卡片顯示改動 [Cursor]
- ProductsPageClient 卡片完整改：label + 中文名 + 樣式

## 2. 篩選邏輯重構

[Cursor] UI 元件：
- AdvancedFilterBuilder 完整實作
- ProductsPageClient UI 整合（toggle + 新元件）

[Copilot] 業務邏輯：
- 搜尋觸發邏輯（從即時改手動）
- 條件組合邏輯

## 3. 測試 + Review

[Copilot] 寫元件測試
[Kimi] Code Review（ProductsPageClient + AdvancedFilterBuilder 交互）
```

---

## 快速參考（貼紙版）

```
🔧 API/後端修復 + 測試驗證？ → Codex
💻 業務邏輯（搜尋/篩選/狀態）？ → Copilot
🎨 UI 元件/表單/頁面改動？ → Cursor
👀 多檔案 review/邏輯檢查？ → Kimi
📚 技術研究/API 文件查詢？ → Gemini
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

**每個 Wave 派工前，執行用量預檢：**
```bash
copilot --version 2>&1 | head -1   # 無回應或錯誤 → 標記不可用
codex --version 2>&1 | head -1     # 同上
```

**執行中遇到以下訊號 → 立刻判定用量不足，不 retry 同一 Agent：**

| Agent | 用量不足訊號 |
|-------|------------|
| Copilot CLI | `rate limit` / `quota exceeded` / `429` / 無回應 >30s |
| Kimi MCP/CLI | `context limit` / `session expired` / MCP timeout / `429` |
| Codex CLI | `quota` / `billing` / 非零 exit + API 錯誤 stderr |
| Cursor | `ECONNREFUSED` / 無法啟動 |

**自動切換順序（不需 Fish 確認）：**

| 主力 | 第一備用 | 第二備用 |
|------|---------|---------|
| Copilot CLI | Kimi CLI | Codex CLI |
| Kimi CLI | Copilot CLI | Sonnet 子代理 |
| Codex CLI | Copilot CLI | Bash 直接執行 |
| Cursor | Copilot CLI (gpt-4.1) | Sonnet 子代理 |

**切換時主動告知 Fish（一句話，不等被問）：**
```
⚠️ [Agent X] 用量不足，已切換至 [備用 Y] 繼續執行。
   任務：[任務編號] [名稱] | 原因：[CLI 錯誤訊息]
```

**全部備用都失敗 → 停止本 Wave，主動說：**
```
⛔ Wave N 暫停：[Agent X/Y/Z] 全部不可用。
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
