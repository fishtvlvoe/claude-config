# Orca Worktree 派工完整 SOP

> 從 `~/.claude/rules/routing.md` 拆出的操作細節與踩坑記錄（2026-08-19 拆檔）。routing.md 保留派工判斷原則+精簡指令；本檔是「動手派工前」的完整手冊，含每個坑的起因、時間戳、指令範例。動工前 Read 這份，不用每次 session 常駐。

## 派工給外部 CLI 的方式（orca CLI，2026-08-17）

Fish 說「派 Codex」「派 Kimi」「派 Cursor」等外部 CLI 時，MUST 用 orca CLI 開一個真正獨立的 worktree + 互動式 terminal session，讓工具在裡面用完整對話模式跑：

```bash
orca worktree create --name "<task-name>" --repo name:<repo-name> --json   # 回傳的 result.worktree.path 記下來
orca terminal create --worktree path:<上面拿到的完整 path> --command "codex"   # 或 "kimi"、"cursor-agent" 等
```

**已確認 orca 原生支援的 agent**：codex、claude、kimi、opencode、gemini、cursor、grok、droid 等（`orchestration` 的 group address 有 `@codex` `@cursor` `@gemini` 等對應）。走 `orchestration` 的 `--agent` 參數時用 `cursor`（不是執行檔名 `cursor-agent`）；走 `orca-cli` 的 `terminal create --command` 時用實際 shell 執行檔名 `cursor-agent`。兩邊代稱不同，別搞混。

**`--worktree active` 陷阱**：`active` 不是「剛建立的那個 worktree」，是「Orca UI 目前焦點中的 worktree」——建完新 worktree 不會自動切過去，用 `active` 會誤開在原本的主 worktree 裡。MUST 用 `orca worktree create` 回傳的 `path`（或 `name:<displayName>`）明確指定，不要用 `active`。起因：2026-08-17 建了 worktree 後用 `--worktree active` 開 terminal，實際跑在 `~/Development/bni` 主目錄而非新建的隔離 worktree。

**禁止**：用 `codex exec "..."` / `kimi -p "..."` 這類背景一次性 headless 呼叫冒充派工——沒有 session、沒有多輪記憶、工具沒辦法追問，不算「真的開一個對話」。起因：2026-08-17 用 `codex exec` + `kimi -p` 背景跑驗證測試被 Fish 當場糾正。

**已確認可用的 CLI（2026-08-17 實測，`which` 過）**：`codex`、`cursor-agent`、`kimi`、`agy`（Antigravity CLI，執行檔名是 `agy` 不是 `antigravity`，別用產品名猜指令名）。舊記憶裡「cursor/kimi 已停用」的說法已過期。

**🔴 新開 worktree 派工，任何 CLI 都要驗證「真的開始做了」才能放著等，不能送出指令就假設成功（2026-08-17）**：在全新 worktree 裡第一次啟動 CLI，可能卡在「信任這個資料夾嗎」之類的 onboarding 選單（agy 遇過），或者第一則訊息送太快被吃掉、工具直接跳回 shell（kimi 遇過，看起來像自己 `exit`，其實是沒接住訊息）。標準動作：
1. 建立 terminal 後先等它把啟動畫面跑完，讀一次 terminal 確認出現的是「可以打字」的提示，不是選單或 shell prompt
2. 送出任務簡報後，再讀一次 terminal，確認 context 用量真的在漲、或看到它在讀檔案/思考，不是又回到空的初始畫面
3. 如果看起來像重開了一輪（標題列、歡迎畫面重新出現），視為訊息沒送達，重送一次，不要放著不管
4. 別假設「這個工具應該沒有這個問題」——每一個 CLI 都要照這個流程走一遍，出過包的是 agy（信任選單）和 kimi（吃掉第一則訊息），不代表 codex/cursor-agent 就一定沒有，沒驗證過的不能當作沒問題

**🔴 派工師與協調者盯工與主動回報硬規則（2026-08-17）**：
派工師監督外部 Agent（Codex/Kimi/Cursor等）時，必須全程盯緊完成訊號（`worker_done`）。**一旦 worker 完成，主代理／協調者必須立即主動驗收、自動開啟/呈現成果（如 `open` 網頁預覽或輸出檔案），並第一時間主動回報老魚結果**，絕對嚴禁靜默等待老魚來問「是不是好了」。

## 🔴 orca worktree 監督 SOP（2026-08-18，L098，一次踩齊全部坑後的最終版）

先判斷要不要委派給「派工師」子代理。判斷標準不是任務大不大，是**要不要脫離 PM 的 context**：
- 只是「開一個 worktree、送任務簡報、等完成、看摘要驗收」→ PM 自己直接管，不要委派。委派多一層子代理生命週期不穩定的風險（實測撞過：子代理自己呼叫超長阻塞等待，撐爆自己的生命週期上限被系統回收，消失）。
- 要做大量前置調查/判斷才能寫出任務簡報、或要同時平行管理多個 worktree，才值得委派給派工師去扛。

PM 自己管的正確 SOP（2026-08-18 修正版，取代舊的 tui-idle 輪詢法）：
1. `orca worktree create` + `orca terminal create --command "codex"`（或其他 CLI）送出**一次講完整範圍**的任務簡報，不要留著之後一批一批補指令。`orca terminal send` 記得加 `--enter`，沒加訊息只會停在輸入框沒送出。
2. **建完 terminal 立刻收編進 orchestration**（`run-create` → `task-create` → `worker-start --terminal <handle> --worktree "path:<該 terminal 的 worktree 絕對路徑>" --run <run_id>`），不要用 `orca terminal wait --for tui-idle` 當完成判斷——`tui-idle` 對啟動階段的短暫停頓、工具呼叫間的畫面閃爍會誤判成「閒置」，實測連續誤判兩次。收編後用 `Monitor` 包住 `orca orchestration check --wait --types worker_done,escalation,question --timeout-ms <長時間> --json 2>&1 | grep --line-buffered -v '"_heartbeat":true'`（心跳行不濾掉會變成每 15 秒吵一次），事件觸發通知，PM 可以繼續正常互動。細節與指令範例見下方「orca-cli vs orchestration」段落。
3. **確認 handle 對，別送錯地方**：一個 worktree 可能開了不只一個 terminal（例如一個空 shell + 一個真正跑 CLI 的），送錯 handle 會被 zsh 當成指令執行然後 `command not found`。送指令前用 `ps aux | grep <cli名>` 找到真正在跑的進程 PID，`lsof -p <pid>` 看它的 `cwd` 確認是對的 worktree，再用 `orca terminal show --terminal <handle>` 讀 `preview` 欄位比對，確認這個 handle 底下真的是那個 CLI 在說話，不是猜。
4. **超過 timeout 不代表任務失敗**：`orchestration check --wait` 到 timeout 只會回一個 timeout 結果。收到後先查 `git log`/檔案系統確認底層 CLI 是否還在正常推進（大工程本來就可能超過預估時間），還在動就重新包一次 Monitor 續等；只有長時間完全沒動靜才需要介入診斷（`ps` 查 CPU% 是否持續在動、`find -mmin` 查最近有沒有檔案被寫入）。
5. **禁止**：自己寫 `sleep + git log 輪詢` 迴圈；每完成一小批次就中斷回來發一則「還在等」的空洞通知；同一件「等它做完」的事同時開兩層監督（例如派工師自己等一次，PM 又另開 Monitor/手動 `terminal wait` 再等一次）。

**驗收動作只在產生的那一層做一次，往上傳壓縮結論不傳原始輸出（2026-08-18）**：CLI 收工前自己跑測試/產 diff（份內工作，只回報 exit code+通過數字，不傳整份 log）；CR 需要獨立視角審查但也只回報 Critical/Warning 各幾個，不傳整份報告；派工師讀這些壓縮指標確認達標才回報 PM；PM 讀派工師的精簡摘要，**不重新執行任何一項驗證動作**（不重新跑測試、不重新逐行讀 diff、不重新讀 CR 全文），只有指標顯示異常才逐層往下深挖原始內容。「誰盯著」不是重點，重點是驗證動作有沒有在每層都重複執行一遍——重複執行 = 換誰盯著都一樣貴。

另外：分頭派工時，各工具在自己的 worktree 裡亂試指令（例如對著不屬於自己的 change 亂跑 `spectra task done`）不會波及其他 worktree（各自獨立 git checkout），但事後要用 `git diff`／`git status` 確認它實際改動的檔案，不能只看它嘴上回報「做完了」。

**🔴 目前沒有「哪個 CLI 適合做什麼」的分工依據，這是空白，不是刻意選擇（2026-08-18）**：現況是每次派工幾乎都預設丟給 Codex，不是評估過 Kimi/Cursor/Antigravity 更適合或更不適合這類任務之後的決定，純粹是習慣。但這不代表要回頭寫死「這類任務用 X CLI」的死板對照表——soul.md 已經在 2026-08-17 明確拆掉這種表，改成憑判斷力決定；沒有實測依據就先寫規則表，等於憑空編一套可能是錯的規矩。**正確路徑**：遇到可以拆成互不依賴子任務的機會（例如同一批工作裡有幾組獨立的檔案範圍），平行分給不同 CLI 各做一組，事後比較品質、速度、有沒有搞砸，把結果記進 lessons.md 或這裡，用實測經驗一點一點堆出真正的分工依據，而不是先驗地規定。在依據建立起來之前，選哪個 CLI 就是判斷力問題（划不划算、能不能驗證、值不值得），不是查表問題。

## orca-cli vs orchestration（2026-08-17，兩者都已實測可用）

派工預設用上面的 orca-cli 流程（開 worktree + terminal，單次任務不用監督結果）。只有下列情境才切換到 `orchestration` skill：

- 需要**等 worker 完成回報**（`worker_done`）才能繼續
- 需要**多個 worker 協調**、有依賴關係的任務 DAG
- 需要**decision gate**（卡點要等裁決才能往下走）
- worker 執行中需要能**回頭問協調者問題**（`ask`/`reply`）

判斷依據：Fish 說「交給/派給/hand off」且沒要求盯結果 → orca-cli 就夠。Fish 說「監督」「等結果」「等它做完」「協調」「DAG」→ 才用 orchestration。

orchestration 標準流程（已實測跑通，Codex 真實回報過）：

```bash
orca orchestration run-create --objective "<目標>" --json          # 拿 run_id
orca orchestration task-create --spec "<任務內容>" --json           # 拿 task_id
orca orchestration worker-start --task <task_id> --worktree current --agent codex --json   # 拿 dispatch_id
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json   # 等回報，真實任務給長 timeout（15-60分鐘正常）
orca orchestration check --ack <delivery_id> --json                # 處理完訊息後才確認
orca orchestration worker-release --dispatch <dispatch_id> --json  # 收尾，除非 Fish 要求保留 worker 現場
```

前置條件：orchestration 是 Orca 實驗性功能，Settings > Experimental 要開啟（這台機器已開）。

### 🔴 已經誤開成 orca-cli 陽春 terminal，事後才發現要等結果 → 用 `--terminal` 收編，不用重開（2026-08-18）

實測踩過：開始以為只是單次交接用 orca-cli 開了 terminal，後來發現要等它做完才能驗收下一步，此時**不用砍掉重開**，直接把現有 terminal 收編進 orchestration 監督：

```bash
orca orchestration run-create --objective "<目標>" --json                          # 拿 run_id
orca orchestration task-create --run <run_id> --spec "<任務內容>" --json            # 拿 task_id
orca orchestration worker-start --task <task_id> --terminal <既有 terminal handle> \
  --worktree "path:<該 terminal 實際所在的 worktree 絕對路徑>" --run <run_id> --json  # 注意：--worktree 一定要填該 terminal 真正的路徑，用 current 或漏填會報 terminal_worktree_mismatch
```

worker 本身完全不用配合、不用重新下指令、不用「知道」自己被 orchestration 接管——監督能力在 Orca 這層（Orca 認得 Claude/Codex/Cursor 等已知 agent 的狀態），不是 worker 要主動回報。收編後原本手動輪詢 `orca terminal wait --for tui-idle` 全部停用，改走下面的 heartbeat 過濾流程。

### 🔴 `check --wait --json` 會吐 heartbeat 雜訊，包進 Monitor 前必須過濾（2026-08-18）

`orca orchestration check --wait --types worker_done,...` 執行中會持續吐 `{"_heartbeat":true,...}` 心跳行，Monitor 工具逐行推播的特性會讓這些心跳變成每 15 秒一次的騷擾通知。**MUST** 接 `grep -v '"_heartbeat":true'` 濾掉：

```bash
orca orchestration check --run <run_id> --wait --types worker_done,escalation,question --timeout-ms <ms> --json 2>&1 | grep --line-buffered -v '"_heartbeat":true'
```

另外偶爾會在對話裡直接跳出「You have 1 orchestration message」提示（非心跳、單則），跑 `orca orchestration check --run <run_id> --json` 讀取，若只是 `type: heartbeat`／`phase: implementing` 這種進度心跳，`--ack <deliveryId>` 讀掉即可，不是完成，不用轉告 Fish。

### 🔴 raw `orca terminal wait --for tui-idle` 不可靠，不要拿來判斷「真的做完了」（2026-08-18）

`tui-idle` 對啟動階段（MCP server 載入完的短暫停頓）、工具呼叫間的畫面閃爍都會誤判成「閒置」，實測連續誤判兩次。**只要是需要等完成才能往下走的任務，一律走上面的 orchestration `worker_done` 事件，不要用 `terminal wait --for tui-idle` 當完成判斷依據**——它只適合「單次交接不用盯結果」的 orca-cli 場景，用來確認訊息有沒有送達就好，不能當完成信號。

## Worktree/Agent 收尾 SOP（2026-08-18，有開必有關，不能無限累積）

閒置的 worktree + 裡面沒關掉的 CLI（codex/agy/kimi 等）持續佔 RAM/CPU，不會自己消失。**每個 worktree 都要能對應到一個「還沒 archive 的 Spectra change」**——change 一旦 archive（功能進 main、驗收完），對應的 worktree 就該收；change 還 active/parked，才有理由留著。

**三個強制觸發點（不是等 Fish 提醒才處理）**：
1. **worker_done 事件一到** → 當場判定去留，不放著等下次想起來
2. **開新 worktree 前** → 先 `git worktree list` 掃一次既有的，每個問一次「done / still-active / stale」
3. **change archive 時** → 一次收尾所有相關 worktree

**判定三態**：
- **done**（worker_done 已回報，或 terminal 讀起來沒有 Working 動畫、停在 prompt）→ 立刻走下面的收尾流程，不留著
- **still-active**（還在跑、或有明確排定的下一批任務）→ 留著，但要講得出「下一步會拿它做什麼」，講不出來就是 stale
- **stale**（沒有 worker_done、沒在動、也沒有下一步）→ 立即收尾，不要放著自然累積

**收尾流程（判定為 done 或 stale 之後）**：
1. 先查有沒有進程還占著：`lsof +D <worktree路徑> | awk '{print $1,$2}' | sort -u`
2. 查有沒有未 commit 的東西：`cd <worktree> && git status --short`——有真正的工作成果（不是純 untracked 參考文件）要先問 Fish 要不要撿回來，不能直接丟
3. 查這支分支的內容有沒有價值：`git diff main...HEAD --stat`、`git log main..HEAD --oneline` / `git log HEAD..main --oneline`——判斷是要合併還是直接關（內容已被 main 或別的分支蓋過去 = 關，不合併）
4. 決定後動手：合併走正常 PR/merge 流程；不合併就 `orca terminal close --terminal <handle>` 關掉裡面還在跑的 CLI，再視情況 `git worktree remove` 移除整個 worktree（有未 commit 東西不能直接 remove，要先處理掉）
5. 對應的 Spectra change 如果還在 active/parked 但已經沒有 worktree 在做了，順手更新狀態（archive 或留 parked 給下次接手），不要留著孤兒 change 對不到任何 worktree

**禁止**：worker_done 回報後放著不處理；囤積一堆說不出「下一步要幹嘛」的 worktree；未查證內容價值就直接刪除（可能撿了別人還要用的東西）。
