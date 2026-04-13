# Mesh Flow — 任務執行流程與失敗回退（強制）

> 來源：mesh/flow.yaml + failure-types.md + retry-policy.md
> 適用：所有開發任務（含 Spectra 和非 Spectra 專案）

## 任務執行流程

每個開發任務依序走以下步驟：

```
discuss → propose → build → format_check → review → memory_write
```

- discuss 可跳過（需求已清楚時）
- format_check 由 Haiku 執行
- memory_write 無論成功或失敗都執行

---

## 失敗分類（三種）

任務失敗時，必須判定屬於哪一種，不同種類退回不同步驟：

### fail_apply — 代碼層問題 → 退回 build

測試跑不過、runtime 錯誤、邏輯 bug、API 用法錯、型別錯誤、邊界情況處理錯。

**判斷方式**：任務拆解和需求是對的，只是代碼寫錯了。

### fail_proposal — 規劃層問題 → 退回 propose

Spec 遺漏邊界情況、任務無法涵蓋需求、架構不匹配、依賴順序錯、驗收標準太模糊。

**判斷方式**：需求本身清楚，但拆解或設計有問題。

### fail_discuss — 需求層問題 → 退回 discuss

需求矛盾、驗收標準無法測試、解決的問題跟用戶要的不同、範圍沒定義。

**判斷方式**：連需求本身都有問題，寫再多代碼也不對。

---

## 回退與升級規則（強制）

### 基本回退

| 失敗類型 | 退回到 |
|---------|--------|
| fail_apply | build（重新實作） |
| fail_proposal | propose（重新規劃） |
| fail_discuss | discuss（重新澄清需求） |

### 升級（同類型失敗 2 次）

同一個任務，同一種失敗出現 2 次 → 自動升級到上一層：

```
fail_apply × 2    → 升級為 fail_proposal → 退回 propose
fail_proposal × 2 → 升級為 fail_discuss  → 退回 discuss
fail_discuss × 2  → halt → 停止，通知用戶
```

**白話說**：代碼改了兩次還是錯 → 不是代碼的問題，是規劃的問題。規劃改了兩次還是錯 → 不是規劃的問題，是需求的問題。需求討論了兩次還是錯 → 停下來，等用戶決定。

---

## Halt 通知（強制格式）

當升級到 halt 時，必須輸出以下格式：

```
⛔ Task Halt

任務：[任務名稱]
失敗路徑：[例：fail_apply ×2 → fail_proposal → halt]

失敗記錄：
1. [第幾次] [哪個步驟] [什麼錯] [一句話原因]
2. ...

建議：
1. [具體問題需要用戶決定]
2. [具體問題需要用戶決定]
```

Halt 後等用戶指示，不自行繼續。

---

## 失敗記憶（每次任務結束必做）

### 寫入

無論任務成功或失敗，結束時記一筆：

- **成功**：記錄任務名稱、使用的方法、花了幾輪
- **失敗**：記錄失敗類型、失敗原因、升級路徑

寫入位置：`memory/task-history/`（依 SSOT 規則）

### 讀取

開始新任務時，查 `memory/failure-patterns/` 找同類任務的常見踩坑，提前告知：

「這類任務過去常見的問題：[列出 1-3 個]，我會注意避開。」

如果沒有歷史記錄，不用提。

---

## 與現有系統的關係

| 系統 | 負責什麼 | Mesh 補充什麼 |
|------|---------|-------------|
| routing.md | 誰做（模型分工） | 不衝突，Mesh 不管誰做 |
| Spectra | 文件管理（propose → apply → archive） | 不衝突，Mesh 管的是失敗時怎麼退 |
| dev-pipeline.md | Phase 順序（規劃→TDD→實作→Review→驗收） | 不衝突，Mesh 補充每個 Phase 內的回退邏輯 |
| formatter.md | 格式檢查 | 對應 Mesh 的 format_check 步驟 |

---

## 判定責任

- **Review 層**（Kimi / Codex / GitHub Copilot）：判定失敗類型
- **主對話**：執行回退，不自行改變 Review 層的判定
- **禁止**：主對話跳過回退直接繼續、主對話自己改 failure_type
