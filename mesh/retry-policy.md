# Retry Policy — 升級規則與 Halt 通知

系統根據 failure_type 的重複出現自動升級，最終達到 halt 並通知使用者。

## Retry 次數限制

每個 step 最多允許 **2 次失敗相同 failure_type** 後升級。

| 第 1 次失敗 | 第 2 次失敗 | 第 3 次... |
|-----------|-----------|---------|
| fail_apply | fail_apply → 升級 fail_proposal | 進入 fail_proposal 的循環 |
| fail_proposal | fail_proposal → 升級 fail_discuss | 進入 fail_discuss 的循環 |
| fail_discuss | fail_discuss → halt + notify | 停止，通知使用者 |

## 升級規則詳解

### 規則 1：fail_apply × 2 → fail_proposal

**觸發**：同一任務在 `build` step 失敗 2 次，都是 fail_apply

**行為**：
1. 系統自動記錄第一次失敗的內容（測試 log、error 訊息等）
2. 在 build 第二次失敗、仍是 fail_apply 時，系統判定「可能不是單純的實作 bug，而是規劃問題」
3. 自動升級為 fail_proposal，路由回 `propose` step
4. 向使用者報告：「重新實作仍然失敗，懷疑是規劃或 spec 問題，回到任務拆解階段」

**使用者可以做**：
- 補充 spec 中的邊界情況
- 重新拆分任務（可能 task 粒度太大）
- 調整 acceptance criteria

### 規則 2：fail_proposal × 2 → fail_discuss

**觸發**：任務重新規劃後仍然失敗，又出現 fail_proposal

**行為**：
1. 第一次 fail_proposal → 回到 propose，重新規劃
2. 規劃完後重新 build，再次進入 review，仍然 fail_proposal（不同原因或根本性矛盾）
3. 系統判定「規劃層已經調整過，仍無法解決，可能需求本身就有問題」
4. 自動升級為 fail_discuss，路由回 `discuss` step
5. 向使用者報告：「多次重新規劃都失敗，需要重新澄清需求」

**使用者可以做**：
- 重新審視需求，檢查是否有矛盾
- 簡化需求範圍，分階段交付
- 提供更多上下文資訊

### 規則 3：fail_discuss × 2 → halt

**觸發**：需求澄清後仍然失敗 2 次，仍是 fail_discuss

**行為**：
1. 第一次 fail_discuss → 回到 discuss，與使用者澄清需求
2. 澄清後重新開始整個流程（discuss → propose → build → review），仍然 fail_discuss
3. 系統判定「已無法自動修復，需要人工介入」
4. **Halt 執行**：停止自動流程，進入 halt 狀態
5. 生成並發送 halt 通知到使用者

---

## Halt 通知格式

當達到 halt 時，系統生成結構化通知，包含完整 failure history。

### 通知結構

```json
{
  "event": "halt",
  "task": "task_name",
  "total_attempts": 3,
  "failure_history": [
    {
      "attempt": 1,
      "step": "build",
      "failure_type": "fail_apply",
      "timestamp": "2026-04-13T02:30:00Z",
      "summary": "Test failure: getUserById() 不拋出 NotFoundError"
    },
    {
      "attempt": 2,
      "step": "build",
      "failure_type": "fail_apply",
      "timestamp": "2026-04-13T02:35:00Z",
      "summary": "相同的 test failure，邏輯 bug 原因"
    },
    {
      "attempt": 3,
      "step": "propose",
      "failure_type": "fail_proposal",
      "timestamp": "2026-04-13T02:45:00Z",
      "summary": "重新規劃後 build，發現 spec 遺漏分頁邏輯"
    }
  ],
  "escalation_path": "fail_apply (×2) → fail_proposal → halt",
  "recommendation": "重新澄清需求，確認以下問題：(1) 列表無限長是否可接受、(2) 如不可接受，分頁應該如何設計、(3) 是否需要簡化其他需求以降低複雜度",
  "next_steps": [
    "與使用者重新討論需求",
    "更新 acceptance criteria",
    "或決定延後此功能，進入下一個 sprint"
  ]
}
```

### 通知輸出方式

**主對話**（Slack / Email / 終端輸出）：

```
⛔ Task Halt Notification

Task: "建立 Mesh Flow System"

Multiple failures detected after escalation path:
- Attempt 1: fail_apply (build step) - Test failure
- Attempt 2: fail_apply (build step) - Same test failure
  → Escalated to fail_proposal (重新規劃)
- Attempt 3: fail_proposal (propose step) - Spec 遺漏分頁邏輯
  → Escalated to fail_discuss (重新澄清)

Current Status: HALTED - Awaiting user intervention

Recommendation:
確認以下 3 點是否可行：
1. 列表無限捲動（infinite scroll）是否可接受？
2. 如不可，分頁應該如何分（page/limit, cursor-based, offset？
3. 其他需求是否有優先級，可延後？

Please clarify requirements before proceeding.
```

---

## Halt 後的恢復

### 選項 1：修改需求後重試

使用者重新提供澄清後的需求 → 返回 discuss step，產生新的 acceptance criteria → 重新開始流程

### 選項 2：分解需求

當前任務太複雜 → 拆成更小的子任務，各自完成 → 最後整合

### 選項 3：延期

決定此功能不在本 sprint，存入 backlog

---

## 系統實作細節

### Retry Counter 管理

```python
retry_state = {
  "task": "task_name",
  "step": "build",
  "failure_type": "fail_apply",
  "count": 1,  # 此 failure_type 在此 step 出現次數
  "escalated": False
}
```

### 升級判斷邏輯

```
if retry_state.count == 2 and not retry_state.escalated:
    next_failure_type = escalation_path[retry_state.failure_type]
    next_step = routing[next_failure_type]
    retry_state.escalated = True
    route_to(next_step, next_failure_type)
    
if failure_type == "fail_discuss" and retry_state.count >= 2:
    halt(task, failure_history)
```

### Memory 記錄

每次 fail 都寫入 task-history，包含 failure_type 和 escalation 狀態，以便下次 discuss 時讀取
