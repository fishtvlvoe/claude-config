# Failure Type System — 失敗分類與回退

系統識別三種 failure_type，每一種對應不同的回退目標和處理層級。

## 三種 Failure Type

### 1. fail_apply — 實作層問題

**定義**：代碼實作錯誤，但任務拆解和需求定義是正確的

**判定標準**：
- 測試失敗（test assertions 不通過）
- Runtime 錯誤（exception、crash、undefined behavior）
- 邏輯 bug（if-else 分支錯誤、計算公式錯誤）
- API 用法錯誤（呼叫端點時參數格式不對、authentication header 遺漏）
- 類型錯誤（傳入錯誤的資料型別、array 期望 object）
- 邊界情況實作有誤（處理 null 時 crash、array 為空時行為不對）

**範例**：
- ✓ Task 要寫 `GET /user/:id` endpoint，代碼寫成 `POST /user/:id`
- ✓ 迴圈邏輯錯誤，導致陣列遍歷少了元素
- ✓ Database query 語法錯誤，執行時拋出 SQL error
- ✓ Async 操作沒有 await，導致 promise 未被 resolve

**回退目標**：`build` step（重新實作）

**預期修復**：修改代碼邏輯，讓測試通過

---

### 2. fail_proposal — 規劃層問題

**定義**：任務拆解或 spec 不完整/不正確，但使用者的需求本身是清楚的

**判定標準**：
- 邊界情況缺失（spec 沒有定義 empty list、null input、permission denied 的行為）
- 任務無法涵蓋需求（某個 spec requirement 沒有對應的 task）
- 架構不匹配（設計決策與實作時發現的真實約束不符）
- 相依性漏掉（Task A 需要 Task B 先完成，但順序安排錯誤）
- Acceptance criteria 不夠具體（「用戶介面應該美觀」太模糊）

**範例**：
- ✓ Spec 說「列出使用者」，但沒定義分頁行為 → 實作後發現需要分頁
- ✓ Task 拆成「寫 API」和「寫 UI」，但沒有「寫整合測試」
- ✓ 決定用 Redux，寫到一半發現 Context API 更輕量，需要重新規劃
- ✓ Acceptance criteria「所有測試通過」，但沒列出具體的測試場景

**回退目標**：`propose` step（重新規劃）

**預期修復**：補充 spec、補充/重新拆 task、調整架構決策

---

### 3. fail_discuss — 需求層問題

**定義**：使用者的需求本身模糊、矛盾或定義不清

**判定標準**：
- Acceptance criteria 自相矛盾（「儘快載入但不犯任何錯誤」，實務無法同時達成）
- Acceptance criteria 無法測試（「系統應該易於使用」，無法量化驗證）
- Spec 解決的問題和使用者實際需要的問題不同
- Scope 未定義（「改進效能」，但沒說要改進多少、改進哪個部分）
- 隱藏的相依性（提供的材料假設 X，但實務環境不符合）

**範例**：
- ✓ 使用者要「加快載入速度」，但沒說是 API 層、渲染層還是兩者都要
- ✓ Acceptance criteria：「所有使用者都滿意」→ 不可測試
- ✓ 需求描述假設「資料庫是 PostgreSQL」，但實務環境用 MongoDB
- ✓ AC 相互矛盾：「支援 IE11」vs「使用 ES2020 語法」

**回退目標**：`discuss` step（重新澄清需求）

**預期修復**：與使用者重新討論，澄清需求、更新 acceptance criteria、定義 scope

---

## Review Output 格式

### Pass（通過）

```json
{
  "verdict": "pass"
}
```

**注意**：Pass 時不含 `failure_type` 欄位

### Fail（失敗）

```json
{
  "verdict": "fail",
  "failure_type": "fail_apply" | "fail_proposal" | "fail_discuss",
  "reason": "具體說明為什麼分類成這個 type"
}
```

**範例**：

```json
{
  "verdict": "fail",
  "failure_type": "fail_apply",
  "reason": "測試失敗：getUserById() 當 ID 不存在時未拋出 NotFoundError，導致 10 個測試不通過"
}
```

```json
{
  "verdict": "fail",
  "failure_type": "fail_proposal",
  "reason": "Spec 遺漏分頁邏輯。實作完後發現列表無限長，需要補充 page/limit 參數的設計"
}
```

```json
{
  "verdict": "fail",
  "failure_type": "fail_discuss",
  "reason": "Acceptance criteria '支援所有主流瀏覽器' 與 'ES2020 語法' 衝突。IE11 不支援 Promise.allSettled。需要使用者選擇：(1) 放棄 IE11、(2) 改用 ES6 語法"
}
```

---

## Escalation 機制

同一 failure_type 在同一任務重複出現時自動升級：

| 出現次數 | 行為 |
|---------|------|
| 1 次 | 回退到對應目標 step，重試 |
| 2 次 | 升級 failure_type，回退到上層 |

### 升級路徑

```
fail_apply (2 次) → fail_proposal (回到 propose)
fail_proposal (2 次) → fail_discuss (回到 discuss)
fail_discuss (2 次) → halt + notify_user
```

**例子**：
- Task 1 first attempt：fail_apply （回到 build，重新實作）
- Task 1 second attempt：又是 fail_apply （升級為 fail_proposal，回到 propose）
- 重新規劃後 Task 1 再試一次：success ✓

---

## 判定責任

- **Flow.yaml**：定義回退路徑（fail_apply → build 等）
- **Review 層**（Kimi / Codex）：輸出 failure_type，決定是 fail_apply / fail_proposal / fail_discuss
- **主對話**：不判斷 failure_type，完全信任 review 層的分類

**禁止**：主對話自己改變 failure_type 的判定（避免角色衝突）
