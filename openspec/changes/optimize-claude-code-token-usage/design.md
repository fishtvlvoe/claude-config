# Design: optimize-claude-code-token-usage

## Context

本次優化的根本原因是 Claude Code 4.7 改版 + 長期設定累積，讓單次 session 啟動成本升到 $0.05-0.1（估算），7 天累計 $146.39。

Fish 之前在 2026-04-10 做過一次優化（15,380 → 9,300，省 43%），但今天量測是 10,285（漂移 +985），加上新增的 defer 機制讓常用工具卡頓。

## Goals / Non-Goals

### Goals
- 恢復 TaskUpdate/AskUserQuestion/WebSearch 等工具的直接可用
- 把 session 啟動 context 從 10,285 降到 6,000 以下
- 清理從未運作的背景服務
- 保留所有核心功能（記憶載入、Spectra 工作流、專案 context）

### Non-Goals
- 不重構 memory 系統架構（session-start.js 只調參數，不重寫）
- 不動 MCP / git repo / 對話歷史
- 不做需要大幅改 JS 程式碼的優化（風險高）

## Decisions

### D1: Rules 觸發表 + on-demand 架構（方案 B）

**決策**：把大檔（routing.md、spectra-agent-routing.md）拆成「速查表」+「詳細檔」。

**理由**：
- 參考 johnlindquist gist（實測省 54% context）
- 速查表保留所有硬規則、路由表、呼叫方式
- 詳細檔放長說明、例子、SOP，需要時 Claude 自己 `Read`

**替代方案拒絕**：
- caveman 壓縮法：對繁中效果差（檔案已精簡）
- 全文保留：成本太高
- 完全刪除：會失去細節查閱能力

### D2: Session Hook 只調參數不重寫（方案 C）

**決策**：session-start.js 保持 207 行架構，只改 3 個常數。

**理由**：
- 核心記憶載入功能必須保留（L1 索引層）
- 重寫風險高（可能壞掉記憶系統）
- 參數調整可精準控制 token 量

**參數選擇**：
- `MAX_AGE_DAYS = 3`：你很少超過 3 天不開工
- `SUMMARY_HEAD_LINES = 25`：足夠看到上次做了什麼、有哪些決策
- `SMART_CONTEXT_MAX_FILES = 1`：其他檔列檔名，需要時主動 Read

### D3: Spectra 硬規則放 soul.md 頂端

**決策**：把 Spectra 預設開啟規則放在 soul.md 最前面（頂端 #2 位置，在「我是誰」之前）。

**理由**：
- soul.md 是每次 session 必讀
- 放頂端確保「第一句話路由判斷」不會被後面規則稀釋
- 用 🔴 強調視覺優先級

### D4: 備份而非直接刪除

**決策**：所有被改/刪的檔案都備份到 `~/.claude/backups/2026-04-17-optimization/`。

**理由**：
- 優化是漸進式實驗，可能發現某些功能被砍太深
- 備份讓回滾成本低（單檔 `cp` 還原）
- 檔案小（<1MB），保留沒壞處

## Risks / Trade-offs

### R1: 摘要截前 25 行可能不夠
**風險**：上次 session 做得很多時，25 行不夠呈現。
**緩解**：已在輸出中保留「... (完整摘要見 /path/to/file)」提示，Claude 看到可主動 Read。

### R2: Smart Context 只載 1 檔可能漏資訊
**風險**：跨專案切換時只看到 1 個檔，可能錯過重要記憶。
**緩解**：其他檔案會列出檔名（「其他記憶檔待命：A, B, C」），Claude 可按需載入。

### R3: Rules detail/ 檔 Claude 不知道要讀
**風險**：精簡 routing.md 末尾雖然寫了「細節見 detail/」，但 Claude 可能忽略。
**緩解**：硬規則全部保留在精簡版，detail/ 只放「什麼時候需要更深理解」的例子；忽略 detail/ 不會違反硬規則。

### R4: launchd 刪錯
**風險**：刪掉的 3 個 plist 之後發現還在用。
**緩解**：plist 刪除前都有確認內容；備份整個 `~/Library/LaunchAgents/` 可從 Time Machine 還原。

## 重現步驟（未來要再做同類優化時照這個順序）

### Phase 1: 量測（先拿 baseline）
1. 跑自寫 Python 腳本算 `~/.claude/{CLAUDE.md,soul.md,lessons.md,rules/*.md}` 總 token
2. 跑 `rtk gain` 看 RTK 歷史省下的量
3. 跑 `/token-report` 看最近 7 天花費
4. 記下三個數字

### Phase 2: 查設定
1. `cat ~/.claude/settings.json` 看 hooks / env
2. `ls ~/Library/LaunchAgents/` 看背景服務
3. `launchctl list | grep fishtv` 看實際在跑的
4. 找哪些是殭屍（log 噴錯、專案不存在）

### Phase 3: 三層優化
1. **設定層**：`ENABLE_TOOL_SEARCH=false`、刪無用 SessionStart hook
2. **Rules 層**：檢查 `wc -l ~/.claude/rules/*.md`，>100 行的考慮拆 detail/
3. **Hook 層**：`session-start.js` 三個常數調整

### Phase 4: 清理
1. `/bin/rm -rf ~/Library/Caches/*`
2. `brew upgrade`
3. 檢查 Development 未提交 repos

### Phase 5: 驗證
1. 重新量測 token 數
2. 算省多少 %
3. 開新 session 試是否正常
