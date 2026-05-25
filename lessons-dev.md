# lessons-dev.md — 派工 / CLI / 寫碼前置 SOP

> 從 lessons.md 主檔拆出（2026-05-19）。觸發情境屬於「派外部代理寫碼」「跨檔派工 SOP」「寫碼前置決策」。
> 主檔（核心跨領域）→ `~/.claude/lessons.md`

## 規則表

| # | 規則 | 觸發情境 |
|---|------|---------|
| L050 | 派任何外部代理（Sonnet 子代理等）前，MUST 跑 `git status` 檢查 untracked 的重要檔案；有則先 `git add openspec/ .claude/ docs/ && git commit -m "wip: pre-dispatch checkpoint"` 才派工。派工 prompt MUST 用白名單：「只允許跑 npm test、git status、git diff，禁止任何其他 git 指令（特別是 clean、restore、reset、checkout）」。 | 派工外部代理前 |
| L075 | 派 Codex CLI 前 MUST 用正確模型參數。已驗證預設：Codex CLI → `gpt-5.3-codex`（ChatGPT 帳號不支援 `o4-mini`/`o4`）。錯誤模型名會導致 CLI 直接報錯退出，非互動模式下看起來像「靜默失敗」。 | Codex CLI 派工 |
| L076 | Agent tool call 的 XML 參數值內禁止插入任何描述文字。錯誤：`<parameter name="subagent_type">general-purpose</parameter>(讀截圖...)\n<parameter name="model">haiku`。parser 會把 `</parameter>` 之後的文字全吞進前一個參數值。派工說明只能寫在 tool call 之外的文字輸出裡，不能夾在 XML 標籤之間。 | Agent tool call XML 格式 |
| L078 | **長任務每完成一個邏輯子步驟 MUST 建存檔點**（`git add -A && git commit -m "wip: <子步驟>"`），不依賴對話 history 當備份。觸發：超過 3 個子步驟的任務、跨 Wave 的 SDD、需要派多次外部代理的工作。理由：(1) 對話被 compact 或 session 換手時，未 commit 的工作會丟；(2) 用戶中途要看「目前做到哪」可以 `git log --oneline` 看。一個子步驟做完不 commit 就不算開始下一步。 | 多步任務每個子步驟結束 |

## 變更歷程

- 2026-05-19: 從 lessons.md 拆出，集中派工 / CLI SOP 規則（L049 / L050 / L053 / L069 / L075 / L076 / L078）
- 2026-05-25: 移除停用工具（Copilot CLI / Kimi CLI）相關 SOP（L049、L053、L069）；L050 移除 Copilot 專屬描述；L075 只保留 Codex CLI 部分
