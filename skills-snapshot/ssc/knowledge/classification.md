# 分類決策樹

## 快速判斷（兩個問題）

```
問題 1：需要跟用戶來回對話嗎？
│
├── 是 → Skill
│
└── 否 → 問題 2：需要 AI 思考嗎？
            │
            ├── 是 → Agent
            │
            └── 否 → Hook
```

## 信號對照表

| 信號 | → 類型 | 原因 |
|------|--------|------|
| 要問用戶「方向對嗎？」 | Skill | 需要 GATE |
| 有強制停止點等用戶確認 | Skill | 互動式流程 |
| 輸出品質取決於用戶回饋 | Skill | 需要來回調整 |
| 丟一個指令就能獨立做完 | Agent | 不需互動 |
| 需要 AI 分析但不需用戶參與 | Agent | 專家型任務 |
| 可以並行跑多個 | Agent | 獨立 context |
| 每次 session 開始都要做 | Hook | 事件驅動 |
| 固定動作不需判斷 | Hook | Shell 腳本即可 |
| 攔截/守門（如禁止危險指令） | Hook | PreToolUse |
| 純資料注入不需思考 | Hook | 零成本 |

## 三種類型的完整對比

|  | Skill | Agent | Hook |
|---|---|---|---|
| 一句話定義 | 互動式工作流 | 獨立執行的專家 | 事件觸發的自動化 |
| 存放位置 | `~/.claude/skills/<name>/` | `~/.claude/agents/<name>.md` | `~/.claude/settings.json` |
| 觸發方式 | `/skill-name` 或 AI 判斷 | Agent tool 自動路由 | 事件驅動（SessionStart 等） |
| 執行者 | 主對話（同 context） | 子代理（獨立 context） | Shell（harness 層） |
| Context 成本 | 載入時消耗 token | 獨立 context，不影響主對話 | 零 token |
| 跟用戶的關係 | 對話式（你來我往） | 報告式（做完回報） | 隱形（用戶不感知） |
| 適合場景 | 寫文章、寫計畫、除錯流程 | Code Review、安全掃描、分析 | 記憶載入、日誌、守門 |

## 灰色地帶處理

### Skill + Agent 混合

某些流程既需要互動又有可獨立執行的子任務。

**解法：** Skill 當主流程，裡面呼叫 Agent 做子任務。

範例：`debug-buygo`
- Phase 1-2（分析 + TDD）→ 需要跟用戶確認方向 → Skill
- Phase 3（Code Review）→ 獨立分析，不需互動 → 內部呼叫 Agent

### Hook + Skill 混合

某些功能需要在特定事件觸發，但觸發後又要 AI 互動。

**解法：** Hook 觸發 → 注入提示 → Skill 接手。

範例：`standup`
- 每天 SessionStart 自動觸發 → Hook
- 整理資訊後跟用戶互動 → Skill

### Agent + Hook 混合

某些功能既是自動觸發又需要 AI 分析。

**解法：** Hook 觸發 → 呼叫 Agent 子代理。

## 轉換模式專用判斷

分析別人的 Skill 時，額外檢查：
1. 原始 Skill 有沒有互動步驟？→ 有則保持 Skill
2. 原始 Skill 是不是純檢查清單？→ 是則考慮轉 Agent
3. 原始 Skill 有沒有事件觸發邏輯？→ 有則拆出 Hook
