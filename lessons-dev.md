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
| L092 | **Codex prompt MUST 存成 `.md` 檔，不在對話輸出讓用戶複製**。存檔後直接告知路徑，讓用戶跑 `codex --file <path>.md`。禁止：在對話裡輸出完整 prompt 內容。 | 任何 Codex 派工前 |
| L096 | **用 orca 監看 Worktree 裡的 Codex/Kimi 是否完成，MUST 用 `orca terminal wait --for tui-idle`，禁止用 `--for exit`**。Codex/Kimi 是常駐互動式 TUI，做完一輪工作後停在自己的提示字元等下一步輸入，程序本身不會結束，`--for exit` 永遠等不到事件、背景輪詢空轉到 timeout 才會發現。`--for exit` 只適用於一次性 shell 指令（程序執行完真的會終止）。已直接修正 `~/.claude/skills/worktree-agent/SKILL.md` 第 3 步的範例指令，不只記 lesson。 | 派 Codex/Kimi 到 Worktree 後監看完成狀態 |
| L099 | **監工/協調類 subagent（開 terminal、輪詢、讀 git diff 這種執行導向、不需要深度推理的角色）預設用小模型（Haiku），不要讓它繼承主 session 的高階模型**。真正需要推理深度的是外部 CLI（agy/Kimi/cursor-agent）寫代碼那層，監工本身只是跑指令+讀輸出+比對，Sonnet/Opus 級別在這裡是浪費。已直接在 `~/.claude/agents/派工師.md` frontmatter 加 `model: haiku`，不是每次呼叫時才手動指定——寫進 agent 定義檔本身才是 SSOT，靠對話記住會在下個 session 失效。起因：Fish 發現派工師預設繼承 Sonnet 5，跟直接自己做没有省到用量。 | 建立或呼叫任何「監工/協調」性質的 subagent 時 |
| L100 | **派工外部 CLI（Codex/Cursor 等）到 orca terminal 後，MUST 用 `ScheduleWakeup` 排定喚醒持續盯著，禁止派完就不管、等 Fish 來問才發現斷線**。監控 SOP：(1) 每次 wakeup 先用 `orca terminal list --json` 比對 `lastOutputAt` 跟現在時間，判斷活著／卡住／額度用完；(2) 額度用完（畫面出現 "You've hit your usage limit"）要讀出畫面顯示的確切恢復時間，排「對應時長」的 wakeup 繼續等（不要用短間隔硬輪詢，浪費 prompt cache；ScheduleWakeup 單次上限 3600 秒，超過要分段排）；恢復後主動送續命指令，並 read 確認真的開始動作，不能只信 send 的 exit code；(3) 完成回報一律要自己動手驗證（curl 測網址／`git log --oneline` 確認 commit 存在且已 push／讀 CR 報告內容），不能只信 terminal 畫面文字；(4) 若 Codex 反覆卡在 approval 選單（需要人工 Yes/No 才能繼續），改用 `codex --dangerously-bypass-approvals-and-sandbox` 開一個新 terminal（YOLO 模式）接手，先用 `orca terminal close` 停掉舊的（避免兩邊同時動同一份代碼衝突），再把完整任務 context 交給新 terminal。**注意：`ScheduleWakeup` 是 session-bound 機制，只在目前對話視窗還開著時有效，視窗關掉監控就消失，不是真正跨 session 的保險網**——長時間任務若要不怕視窗關閉，需另外設系統層級排程（launchd/crontab）當保險，此規則只解決「視窗開著但派工中斷沒被發現」的問題。 | 派工外部 CLI 到 orca terminal 後、需要持續盯著進度直到完成時 |
| L101 | **Codex 額度用完（"You've hit your usage limit"）不用死等恢復時間，MUST 直接切換用 Grok CLI 接手繼續，Fish 已明確裁決此為標準備援方案**。已確認本機裝有 `~/.local/bin/grok`（1.0.5）且已登入可用。切換 SOP：(1) 先確認 Codex 那邊未提交的工作內容（`git status --short` 看 untracked/modified 檔案），不要漏看它做到一半的東西；(2) 開新 orca terminal 跑 `grok --always-approve --permission-mode bypassPermissions`（同一個 worktree，跟 Codex 共用同一份代碼，不要開新 worktree，否則接不上未提交的進度）；(3) 給 Grok 完整交接 prompt：目前整體任務狀態、Codex 已完成/中斷在哪、未提交檔案清單、下一步要做什麼、獨立 CR／驗證標準跟原本一致（0 Critical 才能過、只能用 ego-browser 做網頁驗證）；(4) 交接後 Codex 那個 terminal 不要再送指令給它，避免兩邊同時動同一份代碼衝突。之後同樣要用 L100 的監控 SOP 持續盯著 Grok。 | Codex 額度用完卡住、需要換 CLI 繼續同一份工作時 |

## 變更歷程

- 2026-05-19: 從 lessons.md 拆出，集中派工 / CLI SOP 規則（L049 / L050 / L053 / L069 / L075 / L076 / L078）
- 2026-05-25: 移除停用工具（Copilot CLI / Kimi CLI）相關 SOP（L049、L053、L069）；L050 移除 Copilot 專屬描述；L075 只保留 Codex CLI 部分
- 2026-06-27: 新增 L092 Codex prompt 存檔規則
- 2026-08-10: 新增 L096 orca terminal wait 條件錯誤（--for exit → --for tui-idle），並同步修正 worktree-agent SKILL.md
- 2026-08-20: 新增 L099 監工類 subagent 預設用小模型，直接寫進派工師.md frontmatter
- 2026-08-28: 新增 L100 派工外部 CLI 後用 ScheduleWakeup 持續監控的完整 SOP、L101 Codex 額度用完直接切換 Grok CLI 接手（Fish 裁決標準備援方案）
