# lessons-dev.md — 派工 / CLI / 寫碼前置 SOP

> 從 lessons.md 主檔拆出（2026-05-19）。觸發情境屬於「派外部代理寫碼」「跨檔派工 SOP」「寫碼前置決策」。
> 主檔（核心跨領域）→ `~/.claude/lessons.md`

## 規則表

| # | 規則 | 觸發情境 |
|---|------|---------|
| L049 | 派工給 Copilot CLI（`copilot --yolo`）時，MUST 加 `--add-dir src/` 限制只能動 src 目錄。`--yolo` 模式下 Copilot 有完整寫/刪權限，會動到 openspec/、.claude/、.agent/ 等非代碼目錄。正確呼叫：`copilot --yolo --add-dir src/ --model gpt-5.2 -p @prompt.txt` | Copilot CLI 派工 |
| L050 | 派任何外部代理（Copilot CLI / Sonnet 子代理）前，MUST 跑 `git status` 檢查 untracked 的重要檔案；有則先 `git add openspec/ .claude/ docs/ && git commit -m "wip: pre-dispatch checkpoint"` 才派工。`--add-dir src/` 只限制「主動編輯」範圍，不限制 bash 指令；Copilot --yolo 會跑 `git restore` / `git clean -fd` 把 untracked 檔案永久刪除（unlink，git reflog 也救不回）。prompt MUST 用白名單：「只允許跑 npm test、git status、git diff，禁止任何其他 git 指令（特別是 clean、restore、reset、checkout）」。 | 派工外部代理前 |
| L053 | L050 補強：Copilot CLI 即使加 `--add-dir`，看到 `git diff --stat` 出現「跟我這個任務無關的檔案」就會自作主張 restore 它們。真正的防護：每個 Wave 結束就 `git add -A && git commit -m "wip: ..."`，不留 untracked / modified 給下個 Wave；prompt 結尾明文「只允許 `git diff --stat` `git diff` `git status`，禁止 `git restore` `git checkout` `git clean` `git reset`」。 | Copilot CLI 派工 |
| L069 | 派 Kimi CLI 寫碼前 MUST 防護 SDD 檔案。Kimi CLI 沒有排除目錄的 flag，`-w` 設工作目錄 = 它能動的全部範圍。SOP：(1) 派工前 `git add openspec/ .claude/ && git commit -m "wip: pre-kimi checkpoint"`；(2) `-w` 只指向程式碼目錄（如 `-w src/`），不指向專案根目錄；(3) prompt 結尾加禁令：「只修改程式碼檔案，禁止動 openspec/、.claude/、docs/」；(4) 派工後 `git diff --stat` 檢查。**`--add-dir` 是「擴展」scope 不是「限制」**。 | Kimi CLI 派工 |
| L075 | 派工 CLI 代理前 MUST 用正確模型參數。已驗證預設：Copilot CLI → `gpt-5.2`、Codex CLI → `gpt-5.3-codex`（ChatGPT 帳號不支援 `o4-mini`/`o4`）、Kimi CLI → 內建預設。錯誤模型名會導致 CLI 直接報錯退出，非互動模式下看起來像「靜默失敗」。 | CLI 代理派工 |
| L076 | Agent tool call 的 XML 參數值內禁止插入任何描述文字。錯誤：`<parameter name="subagent_type">general-purpose</parameter>(讀截圖...)\n<parameter name="model">haiku`。parser 會把 `</parameter>` 之後的文字全吞進前一個參數值。派工說明只能寫在 tool call 之外的文字輸出裡，不能夾在 XML 標籤之間。 | Agent tool call XML 格式 |
| L078 | **長任務每完成一個邏輯子步驟 MUST 建存檔點**（`git add -A && git commit -m "wip: <子步驟>"`），不依賴對話 history 當備份。觸發：超過 3 個子步驟的任務、跨 Wave 的 SDD、需要派多次外部代理的工作。理由：(1) 對話被 compact 或 session 換手時，未 commit 的工作會丟；(2) 派外部代理踩 L050/L053 坑會把 untracked 工作 git clean 掉；(3) 用戶中途要看「目前做到哪」可以 `git log --oneline` 看。一個子步驟做完不 commit 就不算開始下一步。 | 多步任務每個子步驟結束 |

## 變更歷程

- 2026-05-19: 從 lessons.md 拆出，集中派工 / CLI SOP 規則（L049 / L050 / L053 / L069 / L075 / L076 / L078）
