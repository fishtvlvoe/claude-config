# lessons.md 案例全文（2026-08-19 拆檔）

> `~/.claude/lessons.md` 核心表只留規則一句話，完整案例/起因搬到這裡，按需 Read。

## L016 — CLI 可用性判定

說「X 不能用」前必須先 `which X` 確認，不要用產品名猜指令名（2026-08-17 更新：Antigravity 的指令是 `agy` 不是 `antigravity`，猜錯過一次）。

已知可用（2026-08-17 實測）：`codex`（Codex CLI）、`cursor-agent`（Cursor CLI）、`kimi`（Kimi CLI）、`agy`（Antigravity CLI，`--dangerously-skip-permissions` 略過權限提示，首次啟動要過一個「信任資料夾」互動選單，send 空字串+Enter 確認預設選項即可）。

舊版「已停用 copilot/gemini/cursor/kimi」的說法已過期，別再引用。

## L096 — 派工外部 CLI 禁止 headless 呼叫，`--command` 禁止填 claude

派工外部 CLI 一律用 orca-cli 開真正互動 terminal session，禁止背景一次性 headless 呼叫（2026-08-17，重複違反升級；2026-08-18 補漏洞）。

用 `orca terminal create --worktree <path> --command "codex"`（或 kimi/cursor-agent 等）開一個真正的 session，讓工具在裡面用完整對話模式跑，可追問、有多輪記憶。**禁止**：`codex exec "..."`、`kimi -p "..."` 這類背景一次性呼叫冒充派工。

**2026-08-18 補漏洞**：`--command` 的值本身也 MUST 是外部 CLI（codex/kimi/cursor-agent/agy），**禁止填 `claude`**——填 `claude` 等於又開一個 Claude Code 在幹活，不是「派工」，是自己分身寫代碼，失去外部工具交叉驗證的意義，且吃自己的 Anthropic 額度而非分散到其他供應商。派工師子代理曾在建立 terminal 時把 `--command` 填成 `claude --dangerously-skip-permissions`，事後才被 Fish 發現。開 terminal 後 MUST 讀一次 preview 確認執行的指令名稱不是 `claude`。

此規則已寫在 `~/.claude/rules/routing.md`，但仍被忘記/違反，故升級進 lessons.md 強制層。

## L097 — 「重做比較快」訊號要信

Fish 說「重做比較快」時，預設信他，不要用「先分析看看」擋下來（2026-08-17）。

起因：startkiter 視覺對齊問題，Fish 質疑「這不是我要的」，我先做漸進修補判斷（截圖比對、改 CSS token），事後讀官方開發文件才發現真正問題是元件庫選錯（Radix UI vs 官方 Base UI，API 不相容）+ CSS 架構整個不同模式——這種規模的落差用「先分析再判斷要不要重做」根本抓不到，因為分析工具本身（截圖比對）解析力不夠，得先做重做才需要的動作（讀源碼/官方文件）才看得出來要重做。

**教訓**：使用者對「這東西感覺不對」的直覺，往往是根據他看不到但真實存在的系統性落差；當使用者主動提「重做比較快」，這是強訊號不是隨口一句，除非有具體證據反駁，否則不要用保守漸進判斷去擋，先問清楚「重做的範圍」而不是問「要不要重做」。

## L098 — orca worktree 派工監督完整 SOP

完整流程細節、每個坑的起因 → `~/.claude/reference/orca-worktree-sop.md`（session 開頭不用讀，動工前必讀）。

五條速記：
1. 先判斷要不要委派派工師子代理——標準是「要不要脫離 PM context」，只是開 worktree+送任務+等完成+看摘要，PM 自己直接管，委派子代理多一層生命週期不穩定風險（實測過：子代理自己等太久被系統回收，消失）
2. 建完 terminal 立刻用 `orca orchestration worker-start --terminal <handle> --worktree "path:<路徑>" --run <run_id>` 收編進 orchestration 監督，不要用 `orca terminal wait --for tui-idle` 判斷完成（實測連續誤判兩次）；改用 `Monitor` 包住 `orca orchestration check --wait ... --json 2>&1 | grep --line-buffered -v '"_heartbeat":true'`
3. 送指令前務必確認 terminal handle 是不是真的接著那個 CLI（`ps`+`lsof -p <pid>` 查 cwd 比對，`terminal show` 讀 preview 確認），送錯地方會被 zsh 當指令執行
4. 驗收動作只在產生的那一層做一次，逐層只傳壓縮結論（exit code+通過數字、Critical/Warning 數量），不重新執行同一項驗證
5. 超過 timeout 不代表任務失敗，先查底層是否還在動，還在動就重新包一次 Monitor 續等
